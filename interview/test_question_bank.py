"""题库内容保护回归测试：python -m unittest discover -s interview -p 'test_*.py'。"""
from contextlib import ExitStack, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import io
import json
import unittest

import parse_questions as parser
import sync_answers as sync
from question_bank import read_question


class QuestionBankTests(unittest.TestCase):
    """在临时目录验证导入与同步，避免测试改动真实题库。"""

    def setUp(self):
        """为每个用例建立独立题库并替换脚本的输入输出路径。"""
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.src = self.root / "_src"
        self.questions = self.root / "questions"
        self.src.mkdir()
        self.questions.mkdir()
        self.data = self.root / "quiz-data.json"
        self.index = self.root / "quiz-index.json"
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        for module, values in [
            (parser, {"SRC_DIR": self.src, "QUESTIONS_DIR": self.questions,
                      "OUTPUT_FULL": self.data, "OUTPUT_INDEX": self.index}),
            (sync, {"QUESTIONS_DIR": self.questions, "DATA_JSON": self.data,
                    "INDEX_JSON": self.index}),
        ]:
            for name, value in values.items():
                self.stack.enter_context(patch.object(module, name, value))
        self.stack.enter_context(patch.object(parser.sys, "argv", ["parse_questions.py"]))

    def add_question(self, qid, title, answer, has_answer=True):
        """生成测试单题，覆盖已答题和人工暂存但未确认的答案。"""
        path = self.questions / f"{qid}.md"
        parser.write_question_md(qid, {
            "question": title, "answer": answer, "category": "RAG/检索",
            "tags": ["RAG"], "companies": ["公司甲"], "frequency": 1,
            "hot": 0, "hasAnswer": has_answer, "source": "quiz-test",
            "created": "2026-06-01",
        }, path)
        return path

    def run_import(self):
        """隐藏常规导入日志，让测试输出只呈现失败原因。"""
        with redirect_stdout(io.StringIO()):
            parser.main()
        return json.loads(self.data.read_text(encoding="utf-8"))

    def test_import_preserves_answers_ids_and_unselected_questions(self):
        """先插入新题再导入，旧题编号、答案、日期和未选题仍应保留。"""
        path = self.add_question("q-9", "原有的检索问题？", "人工补充的详细答案。\n\n## 第二节\n\n不能截断。")
        before = path.read_bytes()
        self.add_question("q-15", "未在本次源文件中的问题？", "已有的参考答案也必须保留。")
        (self.src / "quiz-test.md").write_text(
            "## 公司甲\n\n1. 新加入的检索问题？\n\n2. 原有的检索问题？\n", encoding="utf-8")
        data = self.run_import()
        self.assertEqual([q["id"] for q in data], ["q-9", "q-15", "q-16"])
        self.assertIn("不能截断", data[0]["answer"])
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(data, self.run_import())

    def test_title_edit_is_matched_through_previous_title(self):
        """题目标题润色后，原始 dump 应匹配旧题号并记录标题别名。"""
        self.add_question("q-7", "润色后的问题？", "已经由人工认真补充的答案。")
        self.index.write_text(json.dumps({"questions": [{
            "id": "q-7", "title": "原始的问题？", "source": "quiz-test", "variants": [],
        }]}), encoding="utf-8")
        (self.src / "quiz-test.md").write_text("## 公司甲\n\n1. 原始的问题？\n", encoding="utf-8")
        self.assertEqual([q["id"] for q in self.run_import()], ["q-7"])
        self.assertEqual([q["id"] for q in self.run_import()], ["q-7"])
        index = json.loads(self.index.read_text(encoding="utf-8"))
        self.assertEqual(index["questions"][0]["variants"][0]["title"], "原始的问题？")

    def test_curated_metadata_is_not_overwritten_by_old_dump(self):
        """再次导入旧源文件不能覆盖人工修订的公司信息和答案。"""
        path = self.add_question("q-3", "已有的检索问题？", "## 原理\n\n这是人工维护的完整答案。")
        body = read_question(path)[1]
        (self.src / "quiz-test.md").write_text("## 公司乙\n\n1. 已有的检索问题？\n", encoding="utf-8")
        data = self.run_import()
        self.assertEqual(data[0]["companies"], ["公司甲"])
        self.assertEqual(data[0]["frequency"], 1)
        self.assertEqual(read_question(path)[1], body)
        self.assertEqual(read_question(path)[0]["created"], "2026-06-01")

    def test_new_question_aggregates_companies(self):
        """首次录入同一道题时合并不同公司，并计算出现频次。"""
        (self.src / "quiz-test.md").write_text(
            "## 公司甲\n\n1. 新录入的同一道问题？\n\n## 公司乙\n\n1. 新录入的同一道问题？\n", encoding="utf-8")
        data = self.run_import()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["companies"], ["公司甲", "公司乙"])
        self.assertEqual(data[0]["frequency"], 2)

    def test_long_questions_with_same_prefix_are_distinct(self):
        """超过六十字且前缀相同的不同场景题不能合并。"""
        prefix = "相同的场景描述" * 12
        (self.src / "quiz-test.md").write_text(
            f"## 公司甲\n\n1. {prefix}如何检索？\n\n2. {prefix}如何重排？\n", encoding="utf-8")
        self.assertEqual(len(self.run_import()), 2)

    def test_yaml_title_and_unconfirmed_draft_roundtrip(self):
        """标题中的 YAML 特殊字符和未确认草稿应完整往返。"""
        title = '问题: 如何处理 "引号" 与 # 标记？'
        path = self.add_question("q-2", title, "## 草稿\n\n```python\n# 注释\n```", False)
        data = self.run_import()
        self.assertEqual(read_question(path)[0]["title"], title)
        self.assertFalse(data[0]["hasAnswer"])
        with redirect_stdout(io.StringIO()):
            sync.main()
        self.assertEqual(data, json.loads(self.data.read_text(encoding="utf-8")))

    def test_invalid_markdown_stops_before_json_write(self):
        """元数据格式错误时，两个 JSON 均不能发生部分更新。"""
        path = self.add_question("q-1", "用于校验格式的问题？", "格式正确时的详细参考答案。")
        self.run_import()
        before = (self.data.read_bytes(), self.index.read_bytes())
        path.write_text(path.read_text(encoding="utf-8").replace("hasAnswer: true", "hasAnswer: 'false'"), encoding="utf-8")
        with self.assertRaises(ValueError):
            sync.main()
        with self.assertRaises(ValueError):
            self.run_import()
        self.assertEqual((self.data.read_bytes(), self.index.read_bytes()), before)


if __name__ == "__main__":
    unittest.main()
