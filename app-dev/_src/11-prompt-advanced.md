---
group: 1. Prompt 工程
id: prompt-advanced
title: Prompt 工程 · 高级技巧
toc: Prompt · 高级技巧
---

### Chain-of-Thought（CoT）

在 prompt 末尾添加 `让我们一步步思考`，可显著提高模型在复杂推理任务上的准确率。

### Few-shot Learning

提供 2–5 个高质量示例，比纯文字描述更能稳定模型行为：

```python
User: 把下面句子改写为更正式的版本：
"这玩意儿挺好用的"

Examples:
"搞砸了" → "出现了重大失误"
"牛批" → "表现卓越"

Answer: "此工具具有较高的实用价值"
```

### Self-Consistency

对同一问题采样 N 次、取众数答案，在数学/逻辑题上能进一步提高准确率。
