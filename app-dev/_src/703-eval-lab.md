---
group: 7. 评测与生产治理
id: eval-lab
title: Evals · 轨迹、故障与对照实验
toc: Evals · 实验闭环
---

评测同时验证最终环境状态和执行过程。Agent 声称“工单已创建”只是文本；真实成功应来自业务服务中可查询的工单和有效回执。

## 一个案例的最小结构

```json
{
  "case_id": "ticket-timeout-001",
  "split": "regression",
  "input": "查询订单异常并提交确认过的工单",
  "identity": {"tenant": "demo-a", "user": "demo-user"},
  "knowledge_version": "policy-demo-v1",
  "allowed_tools": ["read_order", "create_ticket", "query_receipt"],
  "fault": "external_write_succeeded_before_timeout",
  "expected": {
    "ticket_count": 1,
    "verified_receipt": true,
    "approval_matches_arguments": true
  },
  "forbidden": ["cross_tenant_read", "duplicate_write"]
}
```

输入数据、工具 fixture 和预期环境状态都应版本化。测试工具向评测器提供真实计数或回执，不能用被测 Agent 自己的“已成功”字段作真值。

## 分层评分

| 层次 | 检查方式 | 例子 |
|------|----------|------|
| 契约 | 确定性验证 | schema、工具名、授权资源和金额 |
| 环境 | 独立业务读回 | 只有一个工单，动作回执可查询 |
| 轨迹 | 过程约束和必要条件 | 写入前有效审批，未知结果先核对 |
| 语义 | 人工或校准模型裁判 | 回复是否准确解释证据与下一步 |
| 产品 | 业务验收与后续反馈 | 问题解决、合理转人工、再次联系 |

轨迹不必逐字逐步相同。可以允许无依赖的查询交换顺序，检查“必须先授权再访问”等偏序关系；对任意合理路径都要求同一最终状态与安全约束。

## 轨迹前缀测试

把一次执行暂停在某个关键点，向候选版本提供相同可信状态，观察接下来的行为。例如工具已发出但回执未知，模型应选择查询而不是重发。

前缀测试便于定位上下文、工具定义或策略造成的问题；端到端测试则检验整条业务闭环。两者配合使用，不应只检查一个最终回答。

## 本地实验入口

```bash
python -m unittest discover -s app-dev/examples -v
python app-dev/examples/business_runtime.py
```

基础示例覆盖上下文预算、只读并发、授权证据和 checkpoint；业务示例补充能力路由、动作参数不可变、审批过期、并发领取、持久化重启和未知结果核对。

这些实验不调用模型、不连接真实业务系统。它们证明本地控制逻辑的性质，不能推出某个模型成功率或生产系统 exactly-once 保证。

## 建立公平的对照组

比较规则流程、流程内单 Agent、单 Agent 加 Skills；只有存在独立证据、权限隔离或有效并行理由时，再加入多 Agent。固定业务权限、工具、案例与总预算，记录配置差异。

报告逐案例结果、样本数、置信区间或重复执行波动、严重违规、P95 时间和有效完成成本。更高费用换来更高成功率时，需要明确业务是否接受该取舍。

数据按客户、文档、事件或时间划分。线上故障用于回归之前先脱敏并标注，不将生产访问令牌、真实资金权限或客户机密带入测试环境。

## 从观察到发布

```text
脱敏 trace -> 分类故障 -> 独立核验与标注 -> 回归案例
  -> 单因素改进 -> 保留集验收 -> 影子运行 -> 灰度与回退
```

生产 trace 是改进原料，不等于模型已经学习。Prompt、工具、Skill、策略或模型的更新均应形成独立候选版本。严重越权用例单独拦截发布，合理人工接管按交接质量评分。

## 借鉴近期交互式基准

[τ²-bench](https://arxiv.org/abs/2506.07982)把用户行动纳入共享环境；[τ-Knowledge](https://arxiv.org/abs/2603.04370)把政策检索与可核验工具动作结合。对应本项目，用户补材料后应通过模拟业务服务验证，而不是让 Agent 根据一句“已经上传”改成完成。

同时固定用户模拟器、任务数据、工具环境与评分器。模拟用户不应获得不符合角色的答案或隐藏状态，模拟器失败与 Agent 失败分别归因。用多次执行衡量同一任务的波动，不能将一次成功当作可靠性证明。

[τ³-bench 官方说明](https://github.com/sierra-research/tau2-bench)记录了任务修正导致部分历史结果不可比。引入基准时保存 release/commit、任务与评分版本；升级评分器后对旧轨迹重新评分，或将两批结果分开报告。本仓库的本地控制测试不等于已经运行这些模型基准。

参考：[OpenAI Agent Evals](https://developers.openai.com/api/docs/guides/agent-evals)。继续阅读[业务自动化验收项目](803-business-automation.html)。
