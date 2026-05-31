---
group: 1. Prompt 工程
id: prompt-basics
title: Prompt 工程 · 基础原则
toc: Prompt · 基础原则
---

一条好的 prompt 通常包含四要素：**角色、目标、约束、输出格式**。

```python
# ❌ 模糊的 prompt
帮我写一篇关于 RAG 的文章

# ✅ 结构化 prompt
角色：资深 LLM 工程师
目标：撰写 RAG 系统的最佳实践
约束：聚焦工程落地、不超过 800 字、面向中级读者
输出：Markdown，含「核心问题 / 解决方案 / 代码示例」三个章节
```

这样的提示词在 Claude、GPT-4 上的输出稳定性可提升 **3–5 倍**。
