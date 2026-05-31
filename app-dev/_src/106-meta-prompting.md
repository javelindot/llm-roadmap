---
group: 1. Prompt 工程
id: meta-prompting
title: Prompt · Meta-Prompting
toc: Prompt · Meta-Prompting
---

**让 LLM 帮你写 LLM 的 prompt** —— 这不是噱头，是 2024–2026 业界的真实主流做法。

## 什么是 Meta-Prompting

```
Meta-Prompting：用一个 prompt 让 LLM 优化另一个 prompt
```

3 种典型应用：

1. **生成 prompt**：你描述目标，LLM 给你写出 prompt
2. **优化 prompt**：给一条现有 prompt，LLM 改进它
3. **自动迭代**：基于评测结果，LLM 自动调整 prompt

## 1. Anthropic Prompt Generator

Anthropic 官方提供了 **Prompt Generator**（Console 里可用），输入任务描述，自动生成结构化 prompt。

```python
# 你的输入
我需要一个 prompt，让模型识别用户邮件的意图，
分类为：咨询 / 投诉 / 退款 / 其他

# Generator 输出的 prompt（自动生成）
你是一名客户服务助理，专门负责分类客户邮件的意图。

<task>
分析以下邮件，确定客户的主要意图。
</task>

<categories>
- 咨询：客户在询问产品功能、价格、可用性等信息
- 投诉：客户对产品或服务表达不满
- 退款：客户请求退款或退货
- 其他：不属于以上三类
</categories>

<email>
{user_email}
</email>

请按以下 JSON 格式输出：
{
  "category": "咨询|投诉|退款|其他",
  "confidence": 0-1 之间的浮点数,
  "reasoning": "1-2 句话解释分类依据"
}
```

复制后稍作调整就能直接用。Anthropic 官方推荐的 prompt 写法（XML 标签、清晰边界）全部体现。

## 2. 手写 Meta-Prompt

如果你不想用官方工具，可以自己写一条「meta prompt」：

```python
META_PROMPT = """你是 Prompt 工程专家。

任务：为以下场景生成一条高质量的 prompt。

场景描述：
{user_description}

生成的 prompt 必须包含：
1. 明确的角色设定
2. 清晰的任务描述
3. 步骤化的执行方案
4. 结构化的输出格式（推荐 JSON 或 Markdown）
5. 至少 1 个 Few-shot 示例
6. 边界限制和错误处理说明
7. 使用 XML 标签分隔不同部分（如 <task>, <examples>, <output>）

请输出完整的、可直接使用的 prompt。
"""

def generate_prompt(description: str) -> str:
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[{"role":"user", "content": META_PROMPT.format(user_description=description)}]
    )
    return resp.content[0].text
```

## 3. Prompt 自动优化

更进阶：给现有 prompt 和评测结果，让 LLM 给出改进建议。

```python
OPTIMIZE_PROMPT = """你是 Prompt 优化专家。

当前 Prompt：
<current_prompt>
{prompt}
</current_prompt>

最近 10 次失败案例：
<failures>
{failure_examples}
</failures>

请分析失败原因，给出 3 个具体改进建议，并输出修改后的 Prompt。

输出格式：
## 失败模式分析
（2-3 句话）

## 改进建议
1. ...
2. ...
3. ...

## 新版 Prompt
<new_prompt>
（完整的新 prompt）
</new_prompt>
"""
```

实战效果：在客服意图分类任务上，迭代 3 轮后准确率从 78% → 91%（基于 200 条测试集）。

## 4. DSPy：声明式 Prompt 优化

**DSPy** 是 Stanford 出的框架，把 prompt 优化变成「编译过程」 —— 你定义任务签名，框架自动找最优 prompt。

```python
import dspy

# 1. 定义任务签名
class EmailClassifier(dspy.Signature):
    """分类邮件意图"""
    email = dspy.InputField()
    category = dspy.OutputField(desc="咨询|投诉|退款|其他")

# 2. 定义模块
classifier = dspy.Predict(EmailClassifier)

# 3. 用训练集自动优化（DSPy 会自动找最佳 prompt + Few-shot 示例）
optimizer = dspy.BootstrapFewShot(metric=my_metric)
optimized = optimizer.compile(classifier, trainset=train_examples)

# 4. 用优化后的 classifier
result = optimized(email="我想退款...")
print(result.category)  # → "退款"
```

DSPy 适合：你有数据集 + 评测指标，想用机器学习的方式优化 prompt。

## 5. Constitutional AI 思路

Anthropic 的方法：让模型**先生成初版**，再让另一个 prompt **批判并改进**。

```python
# Step 1: 初版回答
draft = client.messages.create(
    messages=[{"role":"user", "content": user_question}]
).content[0].text

# Step 2: 自我批判 + 改进
final = client.messages.create(
    messages=[{
        "role":"user",
        "content": f"""
原问题: {user_question}

初版回答: {draft}

请按以下标准批判这个回答：
1. 是否准确？
2. 是否完整？
3. 是否有冒犯性？
4. 是否清晰易懂？

然后给出改进后的版本。
"""}]
).content[0].text
```

适合：高质量内容生成（如客服话术、营销文案、政策解读）。

## 何时用 Meta-Prompting

✅ **适合**
- 起始 prompt（冷启动，没思路时）
- 优化已有 prompt（有评测数据时）
- A/B 时让 LLM 提供多个候选版本
- 改进客户面向的内容（用 Constitutional AI）

❌ **不适合**
- 简单任务（直接写更快）
- 对延迟敏感的实时调用（多一轮 LLM 调用）
- 已经很稳定的成熟 prompt（边际收益小）

## 实战 Workflow

```
1. 描述任务 → Anthropic Prompt Generator 出初版
2. 在你的测试集上跑，记录失败 case
3. 用 Optimize meta-prompt 改进
4. 重复 2–3 直到准确率达标
5. （可选）用 DSPy 自动调参
6. 进 Git，作为 v1 发布
```

:::callout 💡
**经验**：Meta-Prompting 不是「让 LLM 完全代写」，而是**提供启发**。最终的 prompt 还是要人工 review + 测试。
:::

## 限制与陷阱

- LLM 生成的 prompt 可能过度复杂（堆砌技巧）
- 优化方向可能偏离实际场景（评测集要覆盖全面）
- 不要让模型「优化自己被评测的 prompt」 → 容易过拟合

下一节：[6 大实战案例](#real-cases) —— 看 prompt 在真实场景的落地。
