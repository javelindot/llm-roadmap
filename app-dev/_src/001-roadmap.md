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
| 0 | 总览与环境 | 应用架构、API Key、Python/TypeScript 环境、成本意识 | 0.5 天 | 可运行的 Hello World |
| 1 | Prompt 与 Context Engineering | 任务定义、上下文组织、Few-shot、推理预算、Prompt as Code | 4-6 天 | Prompt/Context 模板库 |
| 2 | 模型 API 与结构化输出 | Function Call、JSON Schema、并行工具、错误恢复、流式结构化输出 | 3-4 天 | 类型安全的工具调用 demo |
| 3 | RAG 与数据工程 | 文档解析、切片、Embedding、Hybrid Search、Rerank、RAG 评测 | 7-10 天 | 私域知识问答系统 |
| 4 | MCP 与能力封装 | MCP Server/Client、权限、工具注册、Skills、能力复用 | 5-7 天 | 可复用的工具/能力平台 |
| 5 | Agent 运行时 | 状态、规划、记忆、checkpoint、handoff、human-in-the-loop | 7-10 天 | 可恢复的业务 Agent |
| 6 | 评测与生产治理 | Evals、trace、监控、红队、安全、成本路由、灰度发布 | 4-6 天 | 上线检查清单和评测集 |
| 7 | 全栈 AI App | Streaming UI、AI SDK、实时语音、多模态、浏览器/电脑操作 | 5-7 天 | 端到端 AI 产品原型 |

:::callout 📌
当前版本已经覆盖阶段 0-5 的主体内容，阶段 6 的内容分散在 Prompt 工程化、RAG 评测、Skills 部署、Agent 评估章节里；阶段 7 会在后续版本独立成章。
:::

## 学习节奏建议

```
Week 1    总览 + Prompt 与 Context Engineering
Week 2    模型 API + Function Call + Structured Outputs
Week 3    RAG 基础：解析、切片、Embedding、向量库
Week 4    RAG 进阶：Hybrid、Rerank、GraphRAG、评测
Week 5    MCP + Skills + 工具能力封装
Week 6    Agent 运行时、规划、记忆、多 Agent
Week 7    Evals、观测、安全、成本、灰度发布
Week 8    全栈 AI App 项目整合
```

如果时间只有 4 周，优先顺序是：**Prompt/Context → Structured Outputs/Tools → RAG → Agent/Evals**。MCP、Skills、全栈 UI 可以按项目需要穿插。

## 四种典型路径

:::callout 💼
**企业知识问答 / 客服系统**：Prompt → RAG → Structured Outputs → RAG Evals → MCP。核心是数据质量、召回率、引用溯源、拒答边界。
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

## 后续修改计划

为了让路线图更贴近最新应用开发实践，后续文档会按这个顺序补强：

1. **总览层**：持续更新模型选型、API 形态、主流框架和成本治理。
2. **Agent 层**：扩展 OpenAI Agents SDK、LangGraph、LlamaIndex Workflows、Google ADK/A2A 的对比。
3. **生产层**：新增独立的 Evals、Observability、Guardrails、安全和灰度发布章节。
4. **全栈层**：新增 Vercel AI SDK、流式 UI、Realtime、语音和多模态交互章节。

## 不在范围内的话题

为聚焦应用层，本指南暂不包含：

- 模型训练、SFT、RLHF、DPO
- Transformer / Attention 底层原理
- 数学基础和深度学习入门
- GPU 集群训练和推理服务底层优化

应用层已经足够深。先把能上线、能评测、能迭代的系统做扎实，再继续往底层模型方向挖。
