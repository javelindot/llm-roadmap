---
group: 6. AI Agent
id: agent-concept
title: Agent · 概念与四要素
toc: Agent · 概念
---

Agent 不是「LLM + 工具」这么简单。真正能上线的 Agent，是一个有目标、有状态、有工具、有边界、有评测的运行系统。

一句话理解：

> **Agent = 模型决策 + 状态管理 + 工具执行 + 运行时控制 + 评测治理。**

## Agent 解决什么问题

普通 LLM 应用通常是一次输入、一次输出；Agent 面向的是多步骤任务：

- 需要先查资料，再计算，再写报告
- 需要在多个工具之间选择
- 需要根据失败结果重新规划
- 需要等待用户确认后继续执行
- 需要跨会话记住任务状态

如果任务只需要一次问答，别急着上 Agent。Agent 带来能力，也带来成本、延迟和测试复杂度。

## 生产级 Agent 的六要素

| 要素 | 作用 | 常见实现 |
|------|------|----------|
| 目标 | 明确要完成什么，以及成功标准 | system prompt、任务 schema、验收规则 |
| 状态 | 保存当前进度、上下文、工具结果 | state object、checkpoint、thread/session |
| 工具 | 访问外部能力和真实世界数据 | Function Call、MCP、内部 API、浏览器/电脑操作 |
| 策略 | 决定下一步做什么 | planner、router、state graph、policy |
| 边界 | 控制风险和权限 | allowlist、approval、sandbox、预算上限 |
| 评测 | 判断是否真的完成任务 | offline eval、trace replay、LLM-as-Judge、人工复核 |

这六要素缺一个，Agent 都容易停留在 demo。

## 基本架构

```
用户目标
   ↓
[任务理解 / 路由]
   ↓
[状态 State] ←→ [记忆 Memory]
   ↓
[规划 Planner]
   ↓
[工具选择 Tool Selection]
   ↓
[工具执行层 Tool Runtime]
   ↓
[观察结果 Observation]
   ↓
[反思 / 继续 / 停止]
   ↓
最终结果 + 引用 + Trace
```

工程上要特别注意：模型可以决定「调什么工具」，但真实执行必须经过工具运行时，统一做权限、参数校验、超时、重试、审计和回滚。

## 三种 Agent 形态

| 形态 | 适合场景 | 优点 | 风险 |
|------|----------|------|------|
| Workflow Agent | 流程稳定的业务任务，如工单处理、报表生成 | 可控、易测、易上线 | 灵活性较低 |
| Autonomous Agent | 目标明确但路径不固定，如调研、排障、数据分析 | 灵活、能处理开放任务 | 容易跑偏，成本难控 |
| Multi-Agent | 需要多角色协作，如研究、写作、评审、客服升级 | 分工清晰，可并行 | 协调成本高，评测更难 |

优先顺序通常是：**Workflow Agent → Autonomous Agent → Multi-Agent**。能用单 Agent 解决，就不要一开始拆成多个 Agent。

## 主流框架怎么选

| 框架 / SDK | 定位 | 适合场景 |
|------------|------|----------|
| LangGraph | 有状态图编排、checkpoint、human-in-the-loop | 多步骤业务流、需要可恢复和可观测 |
| OpenAI Agents SDK | Agent、tool、handoff、guardrail、trace 的一体化开发 | OpenAI 生态、快速搭建工具型 Agent |
| Claude Agent SDK | Claude 生态、Skills、MCP、长上下文任务 | 文档/代码/办公自动化、能力包复用 |
| LlamaIndex Workflows | RAG 与 Agentic RAG 工作流 | 知识库、研究助手、数据检索型 Agent |
| Google ADK / A2A | Agent 开发与跨 Agent 通信 | 多 Agent 系统、企业内部 Agent 协作 |
| AutoGen | 多 Agent 对话与实验 | 研究原型、角色协作探索 |
| CrewAI | 角色和任务驱动 | 内容生产、调研、轻量协作 |

框架不是重点，关键是你是否能描述清楚：状态在哪里、工具怎么执行、失败怎么恢复、谁来审批高风险动作、怎么评测。

## Agent 与前面模块的关系

```
Prompt / Context
  → 决定 Agent 的任务理解和输出稳定性

Function Call / Structured Outputs
  → 决定 Agent 能否安全地产生工具参数

RAG
  → 给 Agent 提供可追溯的知识来源

MCP / Skills
  → 把工具和方法论封装成可复用能力

Evals / Observability
  → 判断 Agent 是否可上线、可回放、可迭代
```

所以 Agent 是集大成，但不是跳过前面模块的捷径。

## 设计 Agent 的最小清单

上线前至少回答这些问题：

| 问题 | 不回答的后果 |
|------|--------------|
| 成功标准是什么？ | Agent 看似忙碌，但不知道何时算完成 |
| 最大步数是多少？ | 陷入循环，成本失控 |
| 每个工具的权限是什么？ | 越权访问数据或执行危险操作 |
| 工具失败怎么处理？ | 一次 API 抖动导致整个任务失败 |
| 哪些动作需要人工确认？ | 自动执行高风险操作 |
| 状态如何持久化？ | 中断后无法恢复 |
| Trace 存在哪里？ | 失败无法复盘 |
| 评测集覆盖哪些场景？ | 改了 prompt 不知道是变好还是变坏 |

## 一个最小 Agent 状态

```python
from typing import Literal, TypedDict

class AgentState(TypedDict):
    user_goal: str
    plan: list[str]
    step_index: int
    observations: list[dict]
    final_answer: str | None
    status: Literal["running", "needs_approval", "failed", "done"]
```

有了状态，Agent 才能被检查、恢复、回放和评测。

## 什么时候不要用 Agent

- 任务可以用一次结构化输出完成
- 业务流程非常固定，普通后端代码更可靠
- 工具权限边界还没设计好
- 没有评测集，也没有 trace
- 用户不能接受多轮延迟
- 错误代价高，但没有人工审批

Agent 是强能力，不是默认架构。默认先做简单系统，复杂度真的需要时再升级。

## 学习路径

本模块会按这个顺序推进：

1. [工具调用与 MCP 集成](#agent-tools)：把工具层接进 Agent。
2. [记忆机制设计](#agent-memory)：设计短期上下文和长期记忆。
3. [规划与反思循环](#agent-planning)：让 Agent 能处理多步骤任务。
4. [实战项目](#agent-projects)：用项目把 Prompt、RAG、MCP、Agent 串起来。
5. [Multi-Agent 架构](#agent-multi)：在必要时拆分角色协作。
6. [评估与部署](#agent-eval)：把 Agent 从 demo 推到生产。
