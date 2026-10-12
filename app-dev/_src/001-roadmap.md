---
group: 0. 导读
id: roadmap
title: 学习路径
toc: 学习路径
---

这份指南按「能交付一个生产级 LLM 应用」来组织。建议全栈路线用 **6-8 周**推进，每周 8-10 小时；如果已经有项目目标，可以按后面的路径裁剪。

## 全栈推进路线

| 阶段 | 模块 | 核心能力 | 建议耗时 | 产出 |
|------|------|----------|----------|------|
| 0 | 总览与环境 | 架构、来源与版本、环境、基线和业务目标 | 0.5 天 | 运行环境与实验基线 |
| 1 | Prompt 与 Context Engineering | 任务定义、来源、装配、压缩、缓存与推理预算 | 4-6 天 | 可验收的上下文策略 |
| 2 | 模型 API 与结构化输出 | 工具协议、schema、错误、能力契约与路由 | 3-4 天 | 工具循环及合法降级实验 |
| 3 | RAG 与数据工程 | 解析、检索、重排、ACL、版本、撤权与引用 | 7-10 天 | 可追溯的知识查询系统 |
| 4 | MCP 与能力封装 | 协议版本、授权、工具身份、Skills、A2A 边界 | 5-7 天 | 版本化能力契约与验证 |
| 5 | Agent 运行时 | Harness、Case/Run/Action、等待、审批与恢复 | 7-10 天 | 可恢复的业务执行闭环 |
| 6 | 评测与生产治理 | 轨迹、环境状态、故障、对照实验与发布门槛 | 4-6 天 | 评测基线和回归案例 |
| 7 | 全栈 AI App | 流式交互、确认、停止、回执与人工接管 | 5-7 天 | 业务自动化与非标客服原型 |

:::callout 📌
当前版本包含 52 章、8 个核心模块。新增工程章节贯穿同一业务案例；本地示例验证控制逻辑，真实模型与外部服务仍需集成验收。资料来源见[研究地图](003-research-map.html)。
:::

## 学习节奏建议

```
Week 1    总览 + Prompt 与 Context Engineering
Week 2    模型 API + Function Call + Structured Outputs
Week 3    RAG 基础：解析、切片、Embedding、向量库
Week 4    RAG 进阶：Hybrid、Rerank、GraphRAG、评测
Week 5    MCP + Skills + 工具能力封装
Week 6    Agent Harness、业务状态、恢复与必要的协作
Week 7    Evals、观测、安全、成本、灰度发布
Week 8    全栈 AI App 项目整合
```

如果时间只有 4 周，优先顺序是：**Prompt/Context → Structured Outputs/Tools → RAG → Agent/Evals**。MCP、Skills、全栈 UI 可以按项目需要穿插。

## 四种典型路径

:::callout 💼
**企业知识问答 / 客服系统**：Context → RAG → Structured Outputs → 业务工具 → Harness/Evals。核心是可信证据、问题状态、动作权限与合理人工接管；纯问答可以裁剪执行层。
:::

:::callout 🤖
**业务自动化 Agent**：Prompt → Function Call → MCP → Agent Runtime → Evals。核心是状态管理、工具权限、错误恢复、人工审批。
:::

:::callout 🔌
**SaaS / 插件生态**：Function Call → MCP → Skills → 安全治理。核心是把产品能力暴露给模型生态，同时控制权限和审计。
:::

:::callout 🧩
**全栈 AI 产品**：Structured Outputs → Streaming UI → RAG/Tools → Agent → Observability。核心是让后端智能能力变成用户可感知、可操作的产品体验。
:::

## 阶段验收标准

| 能力 | 验收标准 |
|------|----------|
| 拆解需求 | 看到一个需求，能判断需要 Prompt、RAG、Tool、MCP、Agent 还是传统代码 |
| 设计上下文 | 能区分系统指令、用户输入、检索材料、工具结果和长期记忆 |
| 调用工具 | 能用 JSON Schema 定义工具，并处理并行、失败、重试和权限 |
| 构建 RAG | 能解释召回失败原因，并用评测集调切片、Embedding、Rerank |
| 封装能力 | 能判断什么时候用 Function Call、MCP、Skills 或内部 API |
| 设计 Agent | 能画出 state graph，定义 checkpoint、max steps、人工审批和回滚 |
| 上线治理 | 能提供 trace、评测集、监控指标、成本预算、红队测试和灰度方案 |

## 工程深化路线

| 专题 | 阅读入口 | 必须证明的性质 |
|------|----------|----------------|
| 上下文生命周期 | [Context](108-context-engineering.html) | 压缩后仍保留有效事实与关键约束 |
| 能力与模型路由 | [API 路由](205-model-routing.html) | 降级不丢失必要能力和数据边界 |
| 知识生命周期 | [生产 RAG](307-rag-production.html) | 更新、撤权和删除传播到引用与缓存 |
| 协议与授权 | [MCP/A2A](404-mcp-security.html) | 规范版本、服务身份与业务权限分别验收 |
| 可靠执行 | [Harness](607-agent-harness.html) | 审批、动作幂等与结果未知的核对 |
| 对照与故障 | [评测实验](703-eval-lab.html) | 环境状态和执行过程均可独立核验 |
| 综合项目 | [业务闭环](803-business-automation.html) | 客服交互、流程、工具与人工接管一致 |

验证入口：python -m unittest discover -s app-dev/examples -v。后续接入真实模型时固定 SDK、能力快照与数据策略，并保存可重复的评测结果。

## 不在范围内的话题

为聚焦应用层，本指南暂不包含：

- 模型训练、SFT、RLHF、DPO
- Transformer / Attention 底层原理
- 数学基础和深度学习入门
- GPU 集群训练和推理服务底层优化

应用层已经足够深。先把能上线、能评测、能迭代的系统做扎实，再继续往底层模型方向挖。
