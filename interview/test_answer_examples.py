"""直接执行新答案中的代码，避免文档与测试副本偏离。"""
import importlib.util
import math
import random
import re
import unittest
from pathlib import Path


def answer_code(qid):
    """仅提取指定题目的 Python 示例，在独立命名空间执行仓库内代码。"""
    path = Path(__file__).parent / "questions" / f"q-{qid}.md"
    blocks = re.findall(r"^```python\n(.*?)^```", path.read_text(encoding="utf-8"), re.M | re.S)
    if not blocks:
        raise ValueError(f"q-{qid}: Python example missing")
    namespace = {}
    exec(compile("\n".join(blocks), str(path), "exec"), namespace)
    return namespace


class Node:
    """仅提供算法题依赖的节点字段。"""

    def __init__(self, value):
        """初始化无后继的节点。"""
        self.val, self.next = value, None


def linked(values):
    """构造独立节点，保留身份以验证原地修改。"""
    nodes = [Node(value) for value in values]
    for left, right in zip(nodes, nodes[1:]):
        left.next = right
    return (nodes[0] if nodes else None), nodes


def walk(head):
    """读取链表并显式检测意外成环。"""
    nodes, seen = [], set()
    while head:
        if head in seen:
            raise AssertionError("unexpected cycle")
        seen.add(head)
        nodes.append(head)
        head = head.next
    return nodes


class AnswerExamplesTests(unittest.TestCase):
    """覆盖算法边界、穷举对照、数值稳定和训练梯度。"""

    def test_reorder_list_preserves_nodes_without_cycles(self):
        """不同奇偶长度均按首尾交替排列，节点不得新增或丢失。"""
        reorder = answer_code(1003)["reorder_list"]
        for length in range(21):
            head, nodes = linked(range(length))
            reorder(head)
            expected = []
            for i in range((length + 1) // 2):
                expected.append(nodes[i])
                if i != length - 1 - i:
                    expected.append(nodes[length - 1 - i])
            self.assertEqual(walk(head), expected)

    def test_cycle_detection_uses_identity(self):
        """重复值不构成环，各种环入口都应识别。"""
        detect = answer_code(1042)["has_cycle"]
        self.assertFalse(detect(None))
        for length in range(1, 12):
            head, nodes = linked([1] * length)
            self.assertFalse(detect(head))
            for entry in nodes:
                nodes[-1].next = entry
                self.assertTrue(detect(head))
            nodes[-1].next = None

    def test_assignment_formula_matches_exhaustive_enumeration(self):
        """容斥结果与小范围全部分配方案一致，包含零任务和不足容量。"""
        count = answer_code(1065)["count_assignments"]
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    for n in range(15):
                        expected = sum(a + b + c == n for a in range(x + 1)
                                       for b in range(y + 1) for c in range(z + 1))
                        self.assertEqual(count(n, x, y, z), expected)
        with self.assertRaises(ValueError):
            count(1, -1, 2, 3)

    def test_expression_precedence_unary_and_invalid_input(self):
        """四则优先级、一元符号和括号正确，非法表达式不得被执行。"""
        calculate = answer_code(1102)["calculate"]
        for text, expected in [("2*(3+4)-5/2", 11.5), ("-2*-3", 6),
                               ("8/4/2", 1), ("1--2", 3), (" -(2+3) ", -5),
                               ("--2 + +3", 5), ("0", 0)]:
            self.assertEqual(calculate(text), expected)
        for text in ["", "1+", "1 2", "1//2", "1**2", "2(3)", "a+1",
                     "()", "(1", "1)", "1.5", "__import__('os')"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                calculate(text)
        with self.assertRaises(ZeroDivisionError):
            calculate("1/(2-2)")

    def test_label_mask_keeps_real_eos_but_ignores_padding(self):
        """EOS 与 pad 共用 id 时仍按可见性和回答边界区分。"""
        labels = answer_code(1034)["make_labels"]
        self.assertEqual(labels([1, 2, 0, 0], [False, True, True, True], [1, 1, 1, 0]),
                         [-100, 2, 0, -100])
        with self.assertRaises(ValueError):
            labels([1], [], [1])

    def test_matrix_search_matches_membership(self):
        """不同矩阵形状与范围外目标均与直接查找一致。"""
        search = answer_code(1120)["search_matrix"]
        self.assertFalse(search([], 1))
        self.assertFalse(search([[]], 1))
        for rows in range(1, 7):
            for cols in range(1, 8):
                values = list(range(0, rows * cols * 2, 2))
                matrix = [values[i * cols:(i + 1) * cols] for i in range(rows)]
                for target in range(-1, values[-1] + 2):
                    self.assertEqual(search(matrix, target), target in values)

    def test_parenthesization_keeps_duplicate_results(self):
        """所有括号结构产生的重复值保留，多位整数正确解析。"""
        compute = answer_code(1121)["diff_ways"]
        self.assertEqual(sorted(compute("2*3-4*5")), [-34, -14, -10, -10, 10])
        self.assertEqual(sorted(compute("2-1-1")), [0, 2])
        self.assertEqual(compute("10+5"), [15])
        self.assertEqual(compute("42"), [42])
        with self.assertRaises(ValueError):
            compute("2/3")

    def test_hash_count_preserves_first_seen_order(self):
        """哈希计数与游程压缩语义不同，空串和非连续字符正确处理。"""
        encode = answer_code(1122)["encode_counts"]
        self.assertEqual(encode(""), "")
        self.assertEqual(encode("xxxxyy"), "4x2y")
        self.assertEqual(encode("xyx"), "2x1y")
        self.assertEqual(encode("中文中"), "2中1文")

    def test_merge_k_lists_with_empty_and_duplicate_values(self):
        """随机有序链表合并后保持全局顺序和全部原节点身份。"""
        merge = answer_code(1125)["merge_k_lists"]
        rng = random.Random(20261012)
        for _ in range(100):
            lists, originals, values = [], [], []
            for _ in range(rng.randrange(8)):
                items = sorted(rng.randrange(-5, 6) for _ in range(rng.randrange(12)))
                head, nodes = linked(items)
                lists.append(head)
                originals.extend(nodes)
                values.extend(items)
            result = walk(merge(lists))
            self.assertEqual([node.val for node in result], sorted(values))
            self.assertEqual(set(result), set(originals))

    @unittest.skipUnless(importlib.util.find_spec("numpy"), "NumPy not installed")
    def test_binary_classifier_learns_and_stays_numerically_stable(self):
        """真实训练应降低交叉熵，极端 logits 不得产生 NaN。"""
        import numpy as np
        model = answer_code(1103)["BinaryLogistic"]()
        X = np.array([[-2], [-1], [1], [2]], dtype=float)
        y = np.array([0, 0, 1, 1])
        losses = model.train(X, y)
        self.assertLess(losses[-1], 0.1)
        self.assertTrue(np.isfinite(losses).all())
        np.testing.assert_array_equal(model.predict(X), y)
        model.w, model.b = np.array([1.0]), 0.0
        np.testing.assert_allclose(model.predict_proba([[-1000], [1000]]), [0, 1])
        with self.assertRaises(ValueError):
            model.train([[1]], [2])

    @unittest.skipUnless(importlib.util.find_spec("torch"), "PyTorch not installed")
    def test_ppo_clips_correct_side_and_detaches_baselines(self):
        """正负优势裁剪方向正确，旧策略与优势无梯度。"""
        import torch
        loss_fn = answer_code(1012)["ppo_policy_loss"]
        new = torch.tensor([math.log(r) for r in [1.5, 0.5, 1.5, 0.5]], requires_grad=True)
        old = torch.zeros(4, requires_grad=True)
        advantage = torch.tensor([1., 1., -1., -1.], requires_grad=True)
        loss = loss_fn(new, old, advantage, torch.ones(4))
        self.assertAlmostEqual(loss.item(), 0.15, places=6)
        loss.backward()
        self.assertIsNone(old.grad)
        self.assertIsNone(advantage.grad)
        self.assertAlmostEqual(new.grad[0].item(), 0)
        self.assertGreater(new.grad[2].item(), 0)
        with self.assertRaises(ValueError):
            loss_fn(new, old, advantage, torch.zeros(4))

    @unittest.skipUnless(importlib.util.find_spec("torch"), "PyTorch not installed")
    def test_dual_tower_prefers_correct_pairs_and_backpropagates(self):
        """正配对损失小于错配，梯度有限，温度非法时明确报错。"""
        import torch
        loss_fn = answer_code(1075)["in_batch_loss"]
        users = torch.eye(3, requires_grad=True)
        items = torch.eye(3, requires_grad=True)
        correct = loss_fn(users, items, 0.1)
        wrong = loss_fn(users, items.roll(1, 0), 0.1)
        self.assertLess(correct.item(), wrong.item())
        correct.backward()
        self.assertTrue(torch.isfinite(users.grad).all())
        self.assertTrue(torch.isfinite(items.grad).all())
        with self.assertRaises(ValueError):
            loss_fn(users, items, 0)


if __name__ == "__main__":
    unittest.main()
