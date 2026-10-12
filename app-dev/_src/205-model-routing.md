---
group: 2. Function Call
id: model-routing
title: 模型 API · 能力契约与路由
toc: API · 路由与降级
---

路由先排除不满足任务契约的候选，再在合格候选中权衡质量、费用和延迟。一个能返回文本的备用模型，不一定能完成原任务的工具调用、图片理解或严格输出。

## 能力清单与适配层

| 字段 | 记录什么 | 来源 |
|------|----------|------|
| model / provider / api | 精确模型标识、服务与 API 形态 | 供应商文档及部署配置 |
| capabilities | tools、structured_output、image 等能力 | 针对该模型、API、SDK 的集成验收 |
| schema_profile | 支持的 JSON Schema 子集与限制 | 官方契约和正反例测试 |
| region / data_policy | 执行区域、保存与数据处理策略 | 服务配置与业务要求 |
| limits | 上下文、输出、速率和并发 | 账号级约束与压测 |
| quality_profile | 分任务的成功率与失败类型 | 自己的固定评测集 |
| health / cost | 时效受控的健康状态与成本估计 | 实测及可追溯价格快照 |

能力不是模型品牌的属性，必须覆盖具体接入方式。OpenAI 兼容接口也可能只实现 Chat Completions 的一部分，不能只改 base_url 就假定支持 Responses 或同一严格模式。

适配层统一应用事件：文本、工具请求、工具结果、拒绝、输出不完整、费用与错误。供应商专有的关联字段和必要推理项应完整保留，不能只拼接最终文本。

## 路由顺序

```text
可信身份与数据策略
  -> 输入模态、工具与输出契约
  -> 已验收的能力候选
  -> 当前健康状态、时限与预算
  -> 质量要求下的成本/延迟选择
  -> 固定本次 Run 的配置并记录原因
```

仓库 [select_model](../examples/business_runtime.py)使用虚构能力清单演示区域、能力、健康和预算过滤。它选择合格候选中估计费用最低者，不预测任务难度，也不证明真实模型能力。

```python
from business_runtime import ModelProfile, select_model

# 能力清单来自已验收的部署，费用单位仅用于本地实验。
profiles = [
    ModelProfile("demo-text", frozenset({"text"}), "local", 1),
    ModelProfile("demo-tools", frozenset({"text", "tools"}), "local", 3),
]
model = select_model(profiles, {"tools"}, {"local"}, 5, {"demo-text", "demo-tools"})
print(model.name)  # demo-tools；便宜的纯文本模型不满足工具契约。
```

以上片段在 app-dev/examples 目录运行。真实路由还需要任务质量门槛、token 估算、速率限制和供应商错误映射。

## 区分三类恢复

| 故障 | 处理 | 不应做什么 |
|------|------|------------|
| 模型请求在执行任何工具前失败 | 在预算内切换合格候选 | 降级到缺少必要能力的模型 |
| 工具请求格式或语义非法 | 返回明确错误，限制纠正次数 | 以 strict 开启为由跳过业务校验 |
| 写动作已发出但结果未知 | 用业务幂等键查回执，恢复既有动作 | 因更换模型或 Run 就重新提交 |

切换模型可能改变参数契约和上下文容量。要重新装配兼容上下文，同时保留已执行动作和有效约束；原审批不能被模型修改参数后继续沿用。

## 如何证明路由有价值

用同一任务集比较固定基线模型、规则路由与候选路由。同时报告任务成功、严重违规、有效完成成本、P95 完成时间和降级比例。单次便宜但需要更多补问和重试，最终可能更贵。

低信心分数是模型输出，只有校准后才能作为路由信号。政策约束应由确定性检查优先执行。

参考：[OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling)、[Claude Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)。下一模块：[RAG](300-rag-overview.html)。
