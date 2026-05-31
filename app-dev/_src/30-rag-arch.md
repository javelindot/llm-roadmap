---
group: 3. RAG 检索增强
id: rag-arch
title: RAG · 系统架构
toc: RAG · 架构
---

RAG（Retrieval-Augmented Generation）的核心：**把外部知识库的相关片段作为上下文喂给模型**，让模型基于事实回答，规避幻觉。

```python
# 标准 RAG 流水线
User Query
   ↓ (1) Embed
Query Vector
   ↓ (2) Vector DB 召回 Top-K 片段
Retrieved Chunks
   ↓ (3) 拼接到 Prompt
Augmented Prompt
   ↓ (4) LLM 生成
Final Answer
```
