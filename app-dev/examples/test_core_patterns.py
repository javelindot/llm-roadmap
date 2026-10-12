"""本地边界验证：python -m unittest discover -s app-dev/examples -v。"""
import asyncio
import json
import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from core_patterns import (Tool, authorized_chunks, build_context, create_checkpoint,
                           execute_readonly_calls, load_checkpoint, mcp_aliases,
                           open_checkpoints, save_checkpoint, sum_csv)


class CorePatternsTests(unittest.TestCase):
    """验证授权、预算、资源限制和并发提交的真实行为。"""

    def test_context_keeps_question_and_skips_oversized_evidence(self):
        """超长证据不会挤掉问题，后续较小证据仍可进入。"""
        counter = lambda messages: len(json.dumps(messages, ensure_ascii=False))
        chunks = [{"id": "large", "content": "x" * 1000},
                  {"id": "small", "content": "可信内容"},
                  {"id": "small", "content": "重复内容"}]
        messages, ids = build_context("问题", chunks, counter, 500, 100)
        self.assertEqual(ids, ["small"])
        self.assertEqual(json.loads(messages[1]["content"])["question"], "问题")
        self.assertLessEqual(counter(messages), 400)
        with self.assertRaises(ValueError):
            build_context("x" * 1000, [], counter, 500, 100)

    def test_tool_authorization_and_validation_precede_execution(self):
        """未授权、写工具或参数非法均不能进入实际处理函数。"""
        executed = []

        async def handler(value):
            """记录真实调用，供测试判断是否有越权执行。"""
            executed.append(value)
            return value * 2

        def validate(args):
            """拒绝额外参数以及布尔值等非整数输入。"""
            if set(args) != {"value"} or type(args["value"]) is not int:
                raise ValueError("invalid arguments")

        registry = {"read": Tool(handler, validate), "write": Tool(handler, validate, False)}
        calls = [{"id": "1", "name": "read", "arguments": {"value": 2}},
                 {"id": "2", "name": "write", "arguments": {"value": 3}},
                 {"id": "3", "name": "unknown", "arguments": {}},
                 {"id": "4", "name": "read", "arguments": {"value": True}}]
        results = asyncio.run(execute_readonly_calls(calls, registry, {"read", "write"}))
        self.assertEqual(executed, [2])
        self.assertEqual(results[0]["result"], 4)
        self.assertEqual([r.get("error") for r in results[1:]],
                         ["write_blocked", "forbidden", "invalid_arguments"])

    def test_tool_timeout_concurrency_and_call_identity(self):
        """并发不超过预算，慢工具超时，重复调用编号在执行前拒绝。"""
        active = peak = 0

        async def handler(delay):
            """模拟可取消的异步只读操作。"""
            nonlocal active, peak
            active += 1
            peak = max(peak, active)
            try:
                await asyncio.sleep(delay)
                return delay
            finally:
                active -= 1

        registry = {"read": Tool(handler, lambda args: None)}
        calls = [{"id": str(i), "name": "read", "arguments": {"delay": 0.1}}
                 for i in range(5)]
        results = asyncio.run(execute_readonly_calls(calls, registry, {"read"}, 2, 0.01))
        self.assertLessEqual(peak, 2)
        self.assertEqual(active, 0)
        self.assertTrue(all(r["error"] == "timeout" for r in results))
        with self.assertRaises(ValueError):
            asyncio.run(execute_readonly_calls([calls[0], calls[0]], registry, {"read"}))

    def test_rag_filters_tenant_acl_deletion_and_versions(self):
        """跨租户、未授权、删除和旧版本证据都不能返回。"""
        base = {"document_id": "doc", "tenant_id": "a", "readers": ["user"], "version": 2}
        chunks = [{**base, "id": "ok"}, {**base, "tenant_id": "b", "id": "other"},
                  {**base, "readers": [], "id": "denied"},
                  {**base, "deleted": True, "id": "deleted"},
                  {**base, "version": 1, "id": "stale"}]
        self.assertEqual([c["id"] for c in authorized_chunks(chunks, "a", "user", {"doc": 2})], ["ok"])
        with self.assertRaises(ValueError):
            authorized_chunks(chunks, "", "user", {"doc": 2})

    def test_mcp_same_named_tools_keep_distinct_targets(self):
        """两个服务提供同名工具时仍映射到各自服务。"""
        aliases = mcp_aliases([("crm", "search"), ("docs", "search")])
        self.assertEqual(set(aliases.values()), {("crm", "search"), ("docs", "search")})
        with self.assertRaises(ValueError):
            mcp_aliases([("crm", "search"), ("crm", "search")])

    def test_csv_decimal_limits_and_invalid_data(self):
        """金额精确相加，拒绝目录越界、超大文件和非有限数字。"""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "workspace"
            workspace.mkdir()
            file = workspace / "sales.csv"
            file.write_text("amount\n0.1\n0.2\n", encoding="utf-8")
            self.assertEqual(sum_csv("sales.csv", workspace), {"rows": 2, "amount_total": "0.3"})
            (root / "outside.csv").write_text("amount\n1\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                sum_csv("../outside.csv", workspace)
            with self.assertRaises(ValueError):
                sum_csv("sales.csv", workspace, max_bytes=1)
            file.write_text("amount\nNaN\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                sum_csv("sales.csv", workspace)

    def test_checkpoint_survives_restart_and_rejects_stale_worker(self):
        """状态重启后可读取，过期版本与重复任务不能覆盖现有记录。"""
        with TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.db"
            connection = open_checkpoints(path)
            self.addCleanup(connection.close)
            create_checkpoint(connection, "task", {"status": "pending"})
            version, _ = load_checkpoint(connection, "task")
            self.assertEqual(save_checkpoint(connection, "task", version, {"status": "done"}), 1)
            with self.assertRaises(RuntimeError):
                save_checkpoint(connection, "task", version, {"status": "stale"})
            with self.assertRaises(sqlite3.IntegrityError):
                create_checkpoint(connection, "task", {})
            connection.close()
            restored = open_checkpoints(path)
            try:
                self.assertEqual(load_checkpoint(restored, "task"), (1, {"status": "done"}))
            finally:
                restored.close()


if __name__ == "__main__":
    unittest.main()
