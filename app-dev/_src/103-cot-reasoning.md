---
group: 1. Prompt 工程
id: cot-reasoning
title: Prompt · CoT 链式思维
toc: Prompt · CoT
---

复杂推理任务（数学、逻辑、多步骤分析）上，纯 prompt 经常翻车 —— **让模型「写出推理过程」**是最简单也最有效的解法。

## Chain-of-Thought（CoT）核心

在 prompt 末尾加一句「**让我们一步步思考**」（Let's think step by step），模型会先输出推理过程再给答案。

```python
# 不用 CoT
Q: 一个商店有 23 个苹果，卖出 10 个，又进货 15 个，最后送出去 8 个，
   现在有几个？
A: 30

# 用 CoT
Q: 同上问题
A: 让我们一步步思考：
   - 初始: 23 个
   - 卖出 10: 23 - 10 = 13
   - 进货 15: 13 + 15 = 28
   - 送出 8: 28 - 8 = 20
   答案: 20 个
```

**为什么有效**：模型本质是「下一个 token 预测」。让它先写过程，相当于给了它工作内存，每一步基于前面的结果，错误率显著下降。

数据：在 GSM8K（小学数学）上，CoT 把 GPT-3.5 的准确率从 17% → 78%。

## CoT 的几种触发方式

```python
# 方式 1: 经典触发词
"让我们一步步思考"
"Let's think step by step"

# 方式 2: 显式要求结构
"先列出已知条件，再推导，最后给答案"

# 方式 3: Few-shot CoT（给带推理过程的示例）
示例:
Q: 小明有 5 个苹果，吃了 2 个，剩几个？
A: 已知: 5 个苹果，吃了 2 个
   推理: 5 - 2 = 3
   答案: 3 个

Q: {user_question}
A:
```

## Self-Consistency：CoT 升级版

CoT 一次推理可能出错。**采样 N 次取众数**，能进一步降低错误率。

```python
from anthropic import Anthropic
from collections import Counter
client = Anthropic()

def cot_self_consistency(question, n=5):
    answers = []
    for _ in range(n):
        resp = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=500,
            temperature=0.7,  # 加一点温度才有多样性
            messages=[{"role":"user", "content": f"{question}\n\n让我们一步步思考，最后一行给出答案。"}]
        )
        # 假设答案在最后一行
        last_line = resp.content[0].text.strip().split("\n")[-1]
        answers.append(last_line)

    # 取众数
    most_common = Counter(answers).most_common(1)[0][0]
    return most_common
```

效果：在数学推理上能再提升 5–10 个百分点。代价：**成本 ×N**。

适用场景：高价值、容错低的场景（医疗、金融、法律分析）。日常对话不需要。

## Tree of Thoughts（ToT）

CoT 是「直线推理」，ToT 是「树形搜索」 —— 每步都生成多个分支，剪枝后继续。

```
ToT 流程：
   问题
    │
    ├─ 思路 A
    │   ├─ 子方案 A1 ✓
    │   └─ 子方案 A2 ✗（剪枝）
    │
    ├─ 思路 B
    │   ├─ 子方案 B1 ✓ ← 最优
    │   └─ 子方案 B2 ✓
    │
    └─ 思路 C ✗（早期剪枝）
```

适合：需要规划的任务（24 点、数独、5×5 数字华容道）、需要回溯的任务（代码生成、复杂规划）。

实现上比较复杂，通常用框架（如 LangGraph）。日常应用 90% 的场景，CoT 已经够用。

## 2026 新趋势：原生推理模型

**重大变化**：OpenAI o3、Claude 4.5 with Extended Thinking、DeepSeek-R1 等「**原生推理模型**」已经**内置 CoT 能力**。

```python
# 对推理模型：CoT 不需要你写，模型自己就会推理
resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=2000,
    thinking={"type": "enabled", "budget_tokens": 10000},  # 启用 thinking
    messages=[{"role":"user", "content": "证明：任意正整数 n，若 n³+1 是质数，则 n=1"}]
)
# 模型内部会推理大量 token，最终给出答案
```

| 模型类型 | 是否需要 CoT prompt | 适用场景 |
|---------|---------------------|----------|
| **指令模型**（Claude 4.5 / GPT-5 / Gemini 3）| 需要 | 通用任务、对话 |
| **推理模型**（o3 / Claude Thinking / R1）| **不需要** | 数学、代码、复杂逻辑 |

下一节 [模型类型](#model-types) 详细讲两类模型的 prompt 写法差异。

## 实战 Tips

:::callout 💡
1. **简单任务别用 CoT** —— 浪费 token 还可能让模型「想太多」翻车
2. **CoT 配合 Few-shot 最强** —— 给带推理过程的示例
3. **推理模型只在复杂任务用** —— 单次成本是普通模型的 5–10 倍
4. **Self-Consistency 用在最关键的几次调用** —— 不要全程用，破产警告
:::

## 什么时候用什么

```
简单分类       → 不用 CoT
通用问答       → 不用 CoT（除非答案需要推理）
数学 / 逻辑    → 用 CoT
代码生成       → 用 CoT（或直接用推理模型）
关键决策       → CoT + Self-Consistency
长规划         → ToT 或推理模型
```

下一节：[指令模型 vs 推理模型](#model-types) —— 不同模型族的 prompt 写法差异。
