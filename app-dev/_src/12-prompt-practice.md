---
group: 1. Prompt 工程
id: prompt-practice
title: Prompt 工程 · 实战模板
toc: Prompt · 实战模板
---

> 📌 **实战 Tip**：把高频使用的 prompt 抽成模板，参数化变量部分，可大幅提升迭代效率。

```python
def build_prompt(task, context, examples):
    return f"""
你是{role}。
任务：{task}
背景：{context}

参考示例：
{examples}

请按以下格式输出：
1. 分析（< 100 字）
2. 方案（步骤化）
3. 代码（如适用）
"""
```
