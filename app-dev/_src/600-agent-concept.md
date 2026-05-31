---
group: 6. AI Agent
id: agent-concept
title: Agent · 概念与四要素
toc: Agent · 概念
---

Agent 不是简单的「LLM + 工具」组合，它需要：

1. **规划（Planning）**：把目标拆解为子任务
2. **记忆（Memory）**：短期工作记忆 + 长期向量记忆
3. **反思（Reflection）**：执行失败后修正策略
4. **工具使用**：通过 Function Call / MCP 调用能力

主流框架对比：

| 框架 | 定位 | 适合场景 |
|------|------|----------|
| LangGraph | 状态机式工作流 | 多步骤业务流 |
| AutoGen | 多 Agent 对话 | 角色协作类 |
| CrewAI | 团队化角色分工 | 内容生产/调研 |
| Claude Agent SDK | 原生 Anthropic 栈 | 生产级 Agent |
