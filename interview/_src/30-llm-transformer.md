---
group: 3. LLM 八股
id: llm-transformer
title: LLM 八股 · Transformer 细节
toc: LLM · Transformer
---

### Self-Attention 计算公式

```python
Attention(Q, K, V) = softmax(Q·Kᵀ / √d_k) · V

# 关键点
# 1. 为什么除以 √d_k：防止 softmax 进入饱和区，梯度消失
# 2. Multi-Head：把 d_model 拆成 h 份并行计算，捕捉不同子空间信息
# 3. 复杂度：O(n²·d)，n 是序列长度
```

### 位置编码演进

- **原始 sin/cos**：固定，不能外推
- **Learned**：可学但仍不能外推
- **RoPE（旋转位置编码）**：当前主流，相对位置友好、可外推
- **ALiBi**：通过 attention bias 注入位置信息，长文本表现好
