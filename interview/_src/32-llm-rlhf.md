---
group: 3. LLM 八股
id: llm-rlhf
title: LLM 八股 · RLHF / DPO
toc: LLM · RLHF/DPO
---

**RLHF**：3 阶段 = SFT → Reward Model → PPO。痛点：训练复杂、不稳定。

**DPO**：用偏好数据直接优化策略，跳过 RM 训练，更稳定、更易复现。当前业界主流。

:::callout 💬
**常考**：「为什么 DPO 比 RLHF 更受欢迎？」→ 训练简单、超参少、效果与 PPO 持平甚至更好。
:::
