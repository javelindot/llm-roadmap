---
group: 3. RAG 检索增强
id: rag-tips
title: RAG · 工程实践
toc: RAG · 工程实践
---

- **切片粒度**：通常 200–500 token，按语义边界切分（标题/段落），避免硬切
- **Embedding 选型**：中文场景推荐 `bge-large-zh` / `m3e-base`，英文用 `text-embedding-3-large`
- **召回策略**：向量召回 + BM25 混合，再用 Reranker 精排
- **Prompt 模板**：明确告诉模型「只能基于以下材料回答，材料未提及时回复『未知』」

:::callout ⚠️
**常见坑**：RAG 不是「向量检索 + LLM」就完事 —— 真正的工程难点在**数据清洗**和**评测体系**。
:::
