---
group: 6. AI Agent
id: agent-memory
title: Agent · 记忆机制设计
toc: Agent · 记忆
---

**记忆让 Agent 从「一次性问答」进化成「有状态的伙伴」**。没有记忆，Agent 每次对话都是陌生人；有了记忆，它能记得你姓什么、偏好什么、上一步做到了哪。

## 三层记忆架构

参考人类认知，Agent 记忆通常分三层：

```
┌─────────────────────────────────────────────┐
│  🧠 短期记忆（Short-Term / Working Memory）   │
│     当前对话上下文窗口                         │
│     容量：模型 context limit（8K~2M tokens）  │
│     生命周期：一次会话                         │
├─────────────────────────────────────────────┤
│  💾 中期记忆（Session / Buffer Memory）        │
│     当前会话的摘要、关键事实                   │
│     容量：几百 ~ 几千 tokens                   │
│     生命周期：一次会话，可持久化               │
├─────────────────────────────────────────────┤
│  🗄️ 长期记忆（Long-Term / Vector Memory）     │
│     向量数据库 + 结构化知识库                  │
│     容量：理论上无限                           │
│     生命周期：永久                             │
└─────────────────────────────────────────────┘
```

## 短期记忆：用好上下文窗口

最简单，把历史消息直接塞进 `messages` 数组：

```python
messages = [
    {"role": "system", "content": "你是一个专业的数据分析助手..."},
    {"role": "user", "content": "帮我分析 sales.csv"},
    {"role": "assistant", "content": "好的，我先用 head 查看结构..."},
    {"role": "user", "content": "再画个趋势图"},
    # ...
]
```

**问题**：上下文窗口有限（尤其长对话 + 长工具返回结果）。

**优化策略**：
- **滑动窗口**：只保留最近 N 轮
- **摘要压缩**：把早期对话压缩成摘要，释放 token
- **关键信息提取**：把用户偏好、事实单独抽出来存到中期记忆

## 中期记忆：会话内状态管理

中期记忆解决「Agent 做了 10 步后忘了第一步的结论」的问题。

实现方式：

```python
class SessionMemory:
    def __init__(self):
        self.facts = {}       # 提取的关键事实
        self.preferences = {} # 用户偏好
        self.plan_steps = []  # 当前执行计划
        self.intermediate_results = {}  # 中间结果缓存

    def extract_facts(self, text: str):
        """用 LLM 从对话中提取结构化事实"""
        prompt = f"从以下对话提取关键事实（JSON 格式）：\n{text}"
        result = llm.generate(prompt)
        self.facts.update(json.loads(result))

    def summarize_early_turns(self, messages: list, keep_recent=4):
        """把早期消息压缩成摘要"""
        old = messages[:-keep_recent]
        recent = messages[-keep_recent:]
        summary = llm.generate(f"总结以下对话的关键信息：{old}")
        return [{"role": "system", "content": f"历史摘要：{summary}"}] + recent
```

**典型应用场景**：
- 用户说「用之前的配置」→ 从 `preferences` 读取
- 多步骤数据分析 → `plan_steps` 记录当前做到第几步
- 工具返回大量文本 → `intermediate_results` 缓存，避免重复调用

## 长期记忆：向量数据库 + 结构化存储

跨会话、跨用户的信息需要持久化。两种存储方式互补：

| 存储方式 | 适合存什么 | 检索方式 |
|----------|-----------|----------|
| **向量数据库** | 非结构化文本（对话记录、文档、笔记） | 语义相似度搜索 |
| **结构化数据库** | 关系型数据（用户画像、配置、权限） | SQL / KV 查询 |

### 向量记忆实现

```python
from typing import List
import numpy as np

class VectorMemory:
    def __init__(self, embedding_model, vector_store):
        self.embed = embedding_model
        self.store = vector_store  # 如 Chroma / Milvus / pgvector

    async def add(self, text: str, metadata: dict = None):
        """存入一段记忆"""
        vec = await self.embed(text)
        self.store.add(ids=[generate_id()], embeddings=[vec], documents=[text], metadatas=[metadata])

    async def recall(self, query: str, top_k=5, filter_dict=None) -> List[str]:
        """根据当前问题召回相关记忆"""
        vec = await self.embed(query)
        results = self.store.query(query_embeddings=[vec], n_results=top_k, where=filter_dict)
        return results["documents"][0]
```

### 在 Agent 中注入记忆

```python
async def agent_with_memory(user_input: str, user_id: str):
    # 1. 召回长期记忆
    relevant = await vector_memory.recall(user_input, filter_dict={"user_id": user_id})
    memory_context = "\n".join(relevant) if relevant else "无相关历史记忆"

    # 2. 组装系统提示
    system_prompt = f"""你是用户的个人助手。以下是与该用户相关的历史记忆（按相关度排序）：
{memory_context}
请基于这些信息更好地服务用户。"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    # 3. 正常执行 Agent 循环...
    return await agent_loop(messages)
```

## 记忆写入时机

不是每句话都要存，否则噪音太多：

| 触发时机 | 写入内容 | 存储层 |
|----------|----------|--------|
| 会话开始时 | 用户偏好、背景信息 | 长期记忆 |
| 关键事实确认后 | 「用户是产品经理」「项目代号 Alpha」 | 长期记忆 |
| 任务完成时 | 完整执行摘要 | 向量记忆 |
| 用户显式要求 | 「记住我更喜欢 JSON 格式」 | 长期记忆 |

:::callout 🧠
**记忆设计的黄金法则**：先想「如果我是一个真人助手，我需要记住什么」，再决定存在哪一层。不要为存而存。
:::
