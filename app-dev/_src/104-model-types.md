---
group: 1. Prompt 工程
id: model-types
title: Prompt · 指令模型 vs 推理模型
toc: Prompt · 模型类型
---

2026 年的大模型分成两大流派，**prompt 写法完全不同** —— 用错就是事倍功半。

## 两大流派

| 流派 | 代表模型 | 训练目标 | 输出风格 |
|------|----------|----------|----------|
| **指令模型** (Instruct) | Claude 4.5 / GPT-5 / Gemini 3 / DeepSeek-V3 / Qwen3 | 听指令、做对话 | 简洁直接 |
| **推理模型** (Reasoning) | o3 / Claude Sonnet 4.5 Thinking / DeepSeek-R1 / Qwen3-Reasoning | 内部深度推理 | 推理过程 + 答案 |

## 指令模型的 Prompt 写法

**核心：指令清晰、上下文充分、约束明确**。模型默认是「快思考」，需要你引导它慢下来。

### 适合场景

- 对话、问答、客服
- 内容生成（写作、翻译、改写）
- 简单分类、信息提取
- 工具调用 / Function Call
- RAG 问答

### 推荐 prompt 风格

```python
# 用清晰的「四要素」结构
你是 资深 Python 工程师
任务：审查代码安全性
执行：
  1. 检查 SQL 注入风险
  2. 检查 secret 硬编码
  3. 检查依赖漏洞
输出格式：Markdown 表格
代码：{code}
```

### CoT 在指令模型上的作用

**有用，要主动加**。指令模型默认不会自己推理，需要你写「让我们一步步思考」。

```python
# 让指令模型做数学题
"Q: ...（数学题）...
让我们一步步思考，最后一行给出答案。"
```

## 推理模型的 Prompt 写法

**核心：少干预、给空间、相信模型**。模型已经被训练成「慢思考」，你写一堆步骤反而干扰它。

### 适合场景

- 数学证明 / 复杂计算
- 算法设计 / 代码优化
- 多步逻辑推理 / 因果分析
- 科学问题求解
- 复杂规划 / 决策

### 推荐 prompt 风格

```python
# ❌ 不要这样（反模式）
你是数学专家。
任务：求解微分方程
执行步骤:
1. 先写出特征方程
2. 求解特征根
3. 写出通解
4. 代入初值条件
...

# ✅ 推荐这样（言简意赅）
求解 y'' + 4y = 0，y(0)=1，y'(0)=2
```

为什么？推理模型已经知道如何分步求解，你硬塞步骤反而限制了它的内部推理路径。

### 启用 Extended Thinking（Claude）

```python
from anthropic import Anthropic
client = Anthropic()

resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # 留给推理的 token 上限
    },
    messages=[{
        "role": "user",
        "content": "证明任意 5 个连续整数的乘积可被 120 整除"
    }]
)
# 响应里会有 thinking block（推理过程）+ text block（最终答案）
```

### OpenAI o3 系列调用

```python
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="o3",  # 或 o3-mini
    messages=[{"role": "user", "content": "..."}],
    reasoning_effort="medium"  # low / medium / high
)
```

## 对比：同一问题的 prompt 写法差异

任务：「设计一个 LRU 缓存的 Python 类」

### 指令模型版

```python
你是 Python 高级工程师。

任务：实现一个线程安全的 LRU 缓存类。

要求：
1. 使用 OrderedDict + threading.Lock
2. 支持 get(key) 和 put(key, value)
3. capacity 满了时淘汰最久未用的
4. 写 docstring 和类型注解
5. 末尾加 1 个示例用法

输出：可直接运行的 Python 代码块
```

### 推理模型版

```python
实现线程安全的 LRU 缓存，要求高性能、可读性好
```

**就这一行**。推理模型会内部权衡数据结构选择、锁粒度、淘汰策略，给出深思熟虑的实现。

## 不同任务的模型选型

| 任务 | 推荐模型 | 原因 |
|------|---------|------|
| 客服 / 通用对话 | 指令模型（Claude / GPT-5）| 快、便宜 |
| RAG 问答 | 指令模型 | 主要是「读+答」，推理需求低 |
| 简单代码生成 | 指令模型 | CoT 已足够 |
| 数学竞赛 / 算法题 | 推理模型（o3 / R1）| 需要深度推理 |
| 复杂代码 review | 推理模型 | 需要权衡多个因素 |
| 论文撰写 | 指令模型 + 大量上下文 | 主要靠知识不靠推理 |
| 长程规划 (10+ 步) | 推理模型 | 推理模型规划能力强 |

## 成本对比（2026 年价格）

| 模型 | Input ($/M tokens) | Output ($/M tokens) | 速度 |
|------|--------------------|--------------------|------|
| Claude Sonnet 4.5 | $3 | $15 | 快 |
| GPT-5 | $5 | $20 | 中 |
| **o3** | $20 | $80 | 慢（含推理 token）|
| Claude 4.5 Thinking | $3 + 推理 token 单算 | $15 | 中 |
| DeepSeek-V3 | $0.27 | $1.1 | 快 |
| **DeepSeek-R1** | $0.55 | $2.2 | 慢 |

推理模型贵 5–10 倍 + 慢 3–5 倍。**只在真正需要深度推理时用**。

## 混合使用模式

生产中常见的模式：

```python
# 路由模式：根据任务复杂度选模型
def smart_route(question: str) -> str:
    # 用便宜模型判断复杂度
    classifier = anthropic_client.messages.create(
        model="claude-haiku-4-5",
        messages=[{
            "role":"user",
            "content": f"以下问题是否需要深度推理（数学/逻辑/规划）？只答 yes/no:\n{question}"
        }],
        max_tokens=10
    )

    if "yes" in classifier.content[0].text.lower():
        return openai_client.chat.completions.create(model="o3", ...)
    else:
        return anthropic_client.messages.create(model="claude-sonnet-4-5", ...)
```

简单问题用便宜快速模型，复杂问题升级到推理模型 —— **平均成本降 70%+，准确率不降**。

:::callout 💡
**经验法则**：90% 的应用场景用指令模型就够了。把推理模型留给那 10% 真正需要深度思考的关键决策。
:::

下一节：[Prompt 工程化](#prompt-as-code) —— 把 prompt 当代码管理。
