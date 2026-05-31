---
group: 3. LLM 八股
id: llm-pretrain
title: LLM 八股 · 预训练与微调
toc: LLM · 预训练微调
---

| 方法 | 训练数据 | 代表模型 | 适用 |
|------|----------|----------|------|
| Pre-training | 万亿 token 通用语料 | GPT-4、Llama 3 | 基础能力 |
| SFT | 高质量指令-答案对 | InstructGPT | 对齐指令 |
| LoRA | 小数据集 + 适配器 | 各类下游微调 | 低成本垂域 |
| QLoRA | 同上 + 4bit 量化 | 消费级 GPU | 显存受限场景 |
