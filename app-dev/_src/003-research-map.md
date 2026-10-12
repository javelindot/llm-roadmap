---
group: 0. 导读
id: research-map
title: 研究地图 · 来源、版本与实验方法
toc: 研究地图
---

本轮资料核对日期为 **2026-10-12**。这里的更新体系由三部分组成：稳定的工程原理、带版本的接口契约、可以重复运行的业务实验。模型发布和框架换名不能直接证明业务系统变好。

## 主线：同一个业务问题贯穿八个模块

共同案例是企业服务助手：回答政策、查询授权订单、处理异常、创建确认过的工单，必要时转人工。全部使用虚构租户和模拟业务数据。

| 模块 | 要解决的问题 | 验收证据 |
|------|--------------|----------|
| Prompt / Context | 当前任务应该看到哪些信息？ | 证据来源、版本、预算与信息缺失处理 |
| 模型 API | 哪个候选模型满足任务契约？ | 能力过滤、参数校验、错误与降级记录 |
| RAG | 当前用户能否找到有效材料？ | 授权范围内的召回、引用与过期文档处理 |
| MCP | 服务怎么连接、认证和区分身份？ | 协议版本、传输绑定与业务授权测试 |
| Skills | 哪些处理方法能复用？ | 应触发/不应触发案例、资源版本和执行约束 |
| Agent | 遇到缺失信息和执行中断怎么继续？ | Case/Run/Action 状态、审批与恢复回执 |
| Evals | 哪次改动提升了问题解决效果？ | 独立数据分区、逐案例差异与发布门槛 |
| AI App | 用户如何确认、停止和接续处理？ | 用户事件、已发生动作、人工交接与业务验收 |

## 本轮核对的一手资料

| 来源 | 核对到的内容 | 使用边界 |
|------|--------------|----------|
| [OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling) | Responses 工具结果使用 call_id 关联；严格模式有 schema 要求 | 不把 Chat Completions 的字段直接搬到 Responses |
| [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) | 支持的 schema、拒绝与不完整输出处理 | 结构正确不代表事实正确或已获授权 |
| [OpenAI Agent Runtime](https://developers.openai.com/api/docs/guides/agents-sdk) | 托管 Harness、应用内 SDK 与直接 API 的责任分工 | SDK 会话不等于完整业务事务 |
| [OpenAI Agent Evals](https://developers.openai.com/api/docs/guides/agent-evals) | 轨迹评分、数据集和可重复评测 | 轨迹与业务状态需要可信关联 |
| [Claude Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) | 客户端/服务端工具、tool_use/tool_result、严格工具调用 | 参数与 beta 要求按模型和 SDK 版本检查 |
| [MCP 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports) | 请求携带元数据；stdio 与 Streamable HTTP 的传输规则 | 不混用旧版初始化、服务端请求和取消约定 |
| [Agent Skills](https://agentskills.io/specification) | 技能目录、必填元数据、渐进加载 | 格式规范不提供执行权限或业务授权 |
| [A2A Specification](https://a2a-protocol.org/latest/specification/) | Agent Card、任务、产物、流式与异步交互 | 跨 Agent 协议不替代业务状态机 |
| [LangChain Retrieval](https://docs.langchain.com/oss/python/deepagents/retrieval) | 两阶段、Agentic 与混合 RAG 的取舍 | 收益与延迟需要在自己的任务集上验证 |

这些页面中的可用型号、价格、上下文上限和 SDK 支持会继续变化。接入项目应记录精确包版本、模型标识、协议版本、部署区域与核对日期，不能把动态的 latest 链接当作部署锁定。

## 研究与工程实践怎样互相校验

[《AI Agent 设计原理与工程实践》](https://bojieli.github.io/ai-agent-book/astro/)强调 Model + Harness：上下文、工具、约束、验证与纠错共同决定效果。对应的实验应同时固定模型与运行环境，分别改变上下文策略、工具定义或编排策略，观察哪一项解释了收益。

历史研究可以作为假设来源。例如 [GraphRAG，2024](https://arxiv.org/abs/2404.16130)研究全局问题的图与社区摘要检索；它不是“所有知识库都应该升级图数据库”的证据。研究结论需要带上任务、数据、基线和计算预算。

## 近期研究怎样改变验收方法

| 研究或基准 | 实际研究的问题 | 对本项目的启发 |
|------------|----------------|----------------|
| [τ²-bench，2025](https://arxiv.org/abs/2506.07982) | 用户和 Agent 都能改变共享环境的协作任务 | 客户补材料与实际操作也要进入状态验证，不能只测 Agent 工具 |
| [τ-Knowledge，2026](https://arxiv.org/abs/2603.04370) | 在交互中结合非结构化知识和工具，实现可核验且符合规则的状态变更 | 将 RAG、政策理解、授权和业务动作放在同一案例中评测 |
| [τ-Voice，2026](https://arxiv.org/abs/2603.13686) | 全双工语音、真实音频条件与复杂任务完成 | 文本效果不能直接推算语音效果；打断、噪声与任务完成一起验收 |
| [τ³-bench 项目更新](https://github.com/sierra-research/tau2-bench) | 知识与语音域、任务质量修正及重新评分 | 固定任务和评分器版本，不能把修正前后的成绩当成模型提升 |

本轮读取的官方项目说明指出：2026 年 7 月 v1.0.1 修正了 banking_knowledge 的任务错误，该域在修正前后的结果不可直接比较。这是基准版本影响结论的具体例子；复现实验应锁定 release 或 commit，并保存数据与评分配置。

这些研究提供实验方法，不能把论文中的单次成功率或排行榜分数当作本项目的客服自动化率。本仓库尚未运行上述外部基准，研究启发对应的本地入口见[评测实验](703-eval-lab.html)和[实时语音](801-realtime-multimodal.html)。

一次有效对比至少记录：案例分区、证据版本、权限、模型与能力清单、Prompt/Skill 版本、预算、外部工具状态、实际结果和失败原因。模型裁判只是一种评分渠道，应与确定性规则及人工校准共同使用。

## 更新流程

1. 提出业务假设，例如“按需加载规则能减少无关信息，同时保持审批要求”。
2. 选择一手来源，标记哪些是规范、哪些是历史研究、哪些只是待验证建议。
3. 建立基线和包含失败场景的脱敏案例集。
4. 改一个主要因素；涉及安全边界时单独判断，不用平均分抵消越权。
5. 保存逐案例差异，通过门槛后发布版本；线上故障脱敏后进入回归集。

本地示例验证控制逻辑，不调用模型，不能代表真实模型效果。继续阅读[上下文装配](108-context-engineering.html)、[模型路由](205-model-routing.html)和[业务闭环项目](803-business-automation.html)。
