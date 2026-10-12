"""验证能力路由与动作账本的业务不变量，不调用外部模型。

费用、租户、时钟和回执都是测试数据；测试结果不代表模型任务成功率。
竞争测试使用独立 SQLite 连接，验证真实原子领取而非模拟调用顺序。
测试把模型服务和业务系统排除在外，失败原因能定位到控制逻辑。
审批到期与调用时钟采用固定整数，边界判断不受执行机器时间影响。
所有写动作都使用同一业务键，验证重启或重试不会重置已有事实。
真实集成另需测试外部幂等服务、鉴权、回执验签和任务恢复。
"""

import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Barrier

from business_runtime import ActionLedger, ModelProfile, action_fingerprint, select_model


class ModelRoutingTests(unittest.TestCase):
    """能力、数据区域与预算均为必要条件，降级不得放宽这些条件。

    便宜、健康与质量合格是不同属性，测试仅覆盖前两者的过滤。
    合法候选为空应显式失败，不能输出缺少能力的模型名称。
    配置采用虚构区域和费用，不能用于推断真实部署的数据策略。
    输入既可为集合也可为迭代器，遍历候选不应改变约束内容。
    """

    def test_required_capabilities_survive_fallback(self):
        """排除便宜纯文本、错误区域和失效部署，再选择合格工具模型。

        候选费用刻意更低，确保选择规则不会先按价格忽略约束。
        这验证路由控制逻辑，不验证候选部署的真实工具能力。
        text 费用最低但缺少工具，remote 有工具但区域不允许。
        offline 能力和区域都合法，但未在健康清单中。
        valid 恰好处于预算上限，证明预算检查包含等于的情况。
        一次性迭代器用来发现过滤时重复消耗输入的错误。
        """
        profiles = [ModelProfile("text", frozenset({"text"}), "local", 0),
                    ModelProfile("remote", frozenset({"tools"}), "other", 1),
                    ModelProfile("offline", frozenset({"tools"}), "local", 1),
                    ModelProfile("valid", frozenset({"tools"}), "local", 3)]
        chosen = select_model(profiles, iter({"tools"}), iter({"local"}), 3,
                              iter({"text", "remote", "valid"}))
        # 检查明确的部署名，比只断言返回了某个候选更能发现约束丢失。
        self.assertEqual(chosen.name, "valid")

    def test_incompatible_or_over_budget_candidates_fail(self):
        """没有合法候选时停止，不能丢弃必要工具能力或突破预算。

        分别验证能力不足和预算不足，两种失败均不返回备用文本模型。
        上层可转人工或采用其他合法流程，但不能伪装模型已经完成任务。
        同一部署分别受到两个独立约束，避免混淆能力失败与预算失败。
        保持其他条件有效，使失败只能由正在检查的条件解释。
        错误信息采用稳定代码，调用方无需解析供应商异常。
        subTest 标记具体组合，失败时能区分是哪一种约束失效。
        """
        profiles = [ModelProfile("valid", frozenset({"tools"}), "local", 3)]
        for required, budget in [({"image"}, 3), ({"tools"}, 2)]:
            with self.subTest(required=required, budget=budget):
                with self.assertRaisesRegex(ValueError, "no compatible"):
                    select_model(profiles, required, {"local"}, budget, {"valid"})

    def test_invalid_budget_and_duplicate_identity_are_rejected(self):
        """拒绝布尔预算和同名部署，避免费用与能力身份出现歧义。

        同名部署可能具有不同区域或能力，简单覆盖会产生不可审计结果。
        这里验证配置边界，不使用额外模型调用处理配置错误。
        Python 会把 True 当作整数，预算接口必须主动拒绝。
        重复项即使是同一个配置对象也应报错，避免健康身份歧义。
        这类错误属于部署配置，不应要求模型自行选择或修复。
        """
        profile = ModelProfile("demo", frozenset({"tools"}), "local", 1)
        with self.assertRaisesRegex(ValueError, "budget"):
            select_model([profile], {"tools"}, {"local"}, True, {"demo"})
        with self.assertRaisesRegex(ValueError, "duplicate"):
            select_model([profile, profile], {"tools"}, {"local"}, 5, {"demo"})


class ActionLedgerTests(unittest.TestCase):
    """围绕重复写入、批准参数与故障恢复验证业务动作状态。

    测试对象是本地账本，succeeded 只代表登记了调用方提供的回执。
    工具名、订单和租户均为匿名模拟标识，没有真实外部副作用。
    原子领取、意图绑定和持久化分别测试，避免一个总分掩盖失败。
    未执行动作不能跳到成功，未知动作不能以重新领取代替对账。
    """

    def setUp(self):
        """每个案例建立独立持久化文件，避免测试之间共享动作或批准。

        路径由测试代码创建，所有租户和业务字段均为虚构数据。
        固定时钟用于验证审批边界，测试不依赖机器当前时间。
        初始动作只有参数快照，尚未批准，也尚未调用外部服务。
        每个测试从 pending 开始，状态转换由该测试显式驱动。
        SQLite 文件可重新打开，覆盖内存数据库无法验证的恢复路径。
        """
        self.directory = TemporaryDirectory()
        self.path = Path(self.directory.name) / "actions.sqlite"
        self.ledger = ActionLedger(self.path)
        self.key = ("tenant-a", "case-a", "action-a")
        self.fingerprint = self.ledger.prepare(*self.key, "create_ticket", {"order_id": "order-a"})

    def tearDown(self):
        """先释放数据库连接再删除临时数据，兼容 Windows 文件锁。

        每个案例创建的文件仅位于其临时目录。
        测试失败时也执行此步骤，避免遗留连接影响后续竞争测试。
        重启测试会替换 self.ledger，因此始终关闭最新有效连接。
        清理临时文件不影响真实数据，文件路径由 TemporaryDirectory 管理。
        """
        self.ledger.close()
        self.directory.cleanup()

    def test_changed_arguments_cannot_reuse_action_or_approval(self):
        """同一业务键的参数变化不能覆盖原动作，也不能套用旧批准。

        新参数指纹用于批准旧动作时应被拒绝。
        最后读回原参数，确认失败路径没有修改已有动作。
        action_id 没变但订单变了，应视为意图冲突，不能继续重放。
        分别验证 prepare 与 approve，防止其中一个接口绕过绑定。
        原参数仍存在说明异常路径保留了可继续处理的动作。
        """
        with self.assertRaisesRegex(ValueError, "intent changed"):
            self.ledger.prepare(*self.key, "create_ticket", {"order_id": "order-b"})
        changed = action_fingerprint("create_ticket", {"order_id": "order-b"})
        # 拒绝套用新指纹，批准必须对应已经持久化的参数快照。
        with self.assertRaisesRegex(ValueError, "approval"):
            self.ledger.approve(*self.key, changed, 200)
        self.assertEqual(self.ledger.get(*self.key)["arguments"]["order_id"], "order-a")

    def test_approval_is_required_and_expiry_is_enforced(self):
        """未批准或恰好过期时无法领取，续期后才可以执行。

        当前时间与审批有效期相等时按过期处理。
        领取后无法再次批准，防止执行中的参数授权被覆盖。
        缺少批准时先验证不能执行，再加入与当前时间相等的批准。
        只有真正未过期的批准才允许 pending 转入 executing。
        续期仅改变待执行动作的有效期，不能产生新的业务动作。
        """
        self.assertFalse(self.ledger.claim(*self.key, now=100))
        self.ledger.approve(*self.key, self.fingerprint, 100)
        self.assertFalse(self.ledger.claim(*self.key, now=100))
        self.ledger.approve(*self.key, self.fingerprint, 200)
        # 续期后恰好一个领取成功，后续审批更新必须被状态条件拒绝。
        self.assertTrue(self.ledger.claim(*self.key, now=100))
        with self.assertRaisesRegex(ValueError, "approval"):
            self.ledger.approve(*self.key, self.fingerprint, 300)

    def test_unknown_result_requires_reconciliation(self):
        """动作超时后不可重领，独立核对回执后登记成功。

        同一回执重复投递保持幂等，不同回执则触发冲突。
        已成功动作重复准备不重置为待执行，不会再产生一次写入。
        unknown 保留“可能已经写入”的事实，不等价于可重试失败。
        同回执的重复登记模拟重复通知，必须收敛到同一成功状态。
        不同回执模拟冲突通知，必须交给对账而不是覆盖已有结果。
        """
        self.ledger.approve(*self.key, self.fingerprint, 200)
        self.assertTrue(self.ledger.claim(*self.key, now=100))
        self.ledger.mark_unknown(*self.key)
        # 先阻止未知动作重领，再用已核验回执收敛，验证恢复顺序。
        self.assertFalse(self.ledger.claim(*self.key, now=100))
        self.ledger.settle(*self.key, "receipt-a")
        self.ledger.settle(*self.key, "receipt-a")
        self.ledger.prepare(*self.key, "create_ticket", {"order_id": "order-a"})
        self.assertEqual(self.ledger.get(*self.key)["state"], "succeeded")
        self.assertFalse(self.ledger.claim(*self.key, now=100))
        with self.assertRaisesRegex(ValueError, "conflicts"):
            self.ledger.settle(*self.key, "receipt-b")

    def test_restart_preserves_pending_reconciliation(self):
        """关闭再打开连接后恢复未知状态、参数指纹和已有批准。

        此处使用真实文件而非内存数据库，覆盖进程重建所需的持久化。
        恢复记录仍不可重新领取，应继续使用既有动作进行对账。
        保存 unknown 后释放连接，使读回过程经过真实文件存储。
        指纹不变说明恢复没有悄悄创建另一组参数或另一动作。
        重启本地连接并不查询外部服务，因此不能直接认定业务成功。
        """
        self.ledger.approve(*self.key, self.fingerprint, 200)
        self.ledger.claim(*self.key, now=100)
        self.ledger.mark_unknown(*self.key)
        self.ledger.close()
        # 使用相同文件重建连接，不能用重新创建动作替代故障恢复。
        self.ledger = ActionLedger(self.path)
        self.assertEqual(self.ledger.get(*self.key)["state"], "unknown")
        self.assertEqual(self.ledger.get(*self.key)["fingerprint"], self.fingerprint)
        self.assertFalse(self.ledger.claim(*self.key, now=100))

    def test_concurrent_workers_have_one_winner(self):
        """两个独立 worker 同时领取同一动作，只有一个成功。

        每个线程自行打开连接，屏障确保双方在领取前均已就绪。
        原子更新控制竞争，不能依靠内存布尔值保护跨 worker 状态。
        主线程先准备批准，再让两个 worker 同时争取同一记录。
        统计布尔结果验证唯一领取者，读回状态验证更新已提交。
        该断言不证明外部服务只写一次，外部仍需同键幂等。
        """
        self.ledger.approve(*self.key, self.fingerprint, 200)
        barrier = Barrier(2)

        def claim_in_worker():
            """在独立连接中竞争，结束时释放连接，避免共享线程对象。

            屏障设置超时，单个 worker 失败时不让整个测试无限等待。
            返回真实 SQL 领取结果，测试据此统计成功执行者。
            SQLite 连接在本线程创建，避免共享连接导致线程错误。
            finally 同样覆盖屏障超时和数据库异常路径。
            """
            worker = ActionLedger(self.path)
            try:
                barrier.wait(timeout=5)
                return worker.claim(*self.key, now=100)
            finally:
                worker.close()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: claim_in_worker(), range(2)))
        # 用独立主线程连接读回状态，确认 worker 写入的持久化可见性。
        self.assertEqual(results.count(True), 1)
        self.assertEqual(self.ledger.get(*self.key)["state"], "executing")

    def test_tenant_scope_and_unexecuted_receipt_are_checked(self):
        """另一个租户不能读到动作，未执行动作不能凭回执文本变成功。

        租户检查验证存储作用域，真实调用权限仍由应用鉴权提供。
        成功登记的状态前提可阻止跳过执行流程伪造本地完成状态。
        只改变 tenant 而保持 Case 和动作名，确保作用域隔离确实有效。
        原租户仍为 pending，拒绝错误回执不会污染真实动作状态。
        KeyError 只表示当前作用域缺少记录，不代表完成了用户鉴权。
        """
        with self.assertRaises(KeyError):
            self.ledger.get("tenant-b", "case-a", "action-a")
        with self.assertRaisesRegex(ValueError, "conflicts"):
            self.ledger.settle(*self.key, "receipt-a")
        self.assertEqual(self.ledger.get(*self.key)["state"], "pending")

    def test_fingerprint_preserves_json_semantics_and_snapshot(self):
        """键顺序不影响指纹，非有限数值被拒绝，返回值不修改存储。

        外部对象被修改后，动作仍保留准备时的确定参数。
        这些校验不能代替业务字段的 schema 与语义检查。
        排序后两个对象编码一致，但 NaN 不属于标准 JSON 数值。
        输入对象和查询返回值均可变，存储必须保持自己的参数快照。
        这验证本地 Python 编码约定，不证明跨语言的规范化一致。
        """
        self.assertEqual(action_fingerprint("tool", {"a": 1, "b": 2}),
                         action_fingerprint("tool", {"b": 2, "a": 1}))
        with self.assertRaises(ValueError):
            action_fingerprint("tool", {"amount": float("nan")})
        # 准备后修改原对象，确认账本没有保留可被外界修改的引用。
        arguments = {"order_id": "order-c"}
        other_key = ("tenant-a", "case-a", "action-c")
        self.ledger.prepare(*other_key, "create_ticket", arguments)
        arguments["order_id"] = "modified-after-prepare"
        self.assertEqual(self.ledger.get(*other_key)["arguments"]["order_id"], "order-c")
        # 再修改查询返回值，验证读取快照也不能绕过不可变参数规则。
        record = self.ledger.get(*self.key)
        record["arguments"]["order_id"] = "changed"
        self.assertEqual(self.ledger.get(*self.key)["arguments"]["order_id"], "order-a")


if __name__ == "__main__":
    unittest.main()
