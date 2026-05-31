---
group: 6. AI Agent
id: agent-eval
title: Agent · 评估与部署
toc: Agent · 评估部署
---

**Agent 比传统软件更难测试**：它有随机性、有状态、会调用外部工具、可能陷入循环。没有系统化的评估和部署策略，Agent 很难从 demo 走到生产环境。

## 为什么 Agent 评估特别难

| 传统软件测试 | Agent 测试 |
|-------------|-----------|
| 输入 → 输出 确定 | 同样输入，LLM 可能给出不同策略 |
| 单元测试覆盖逻辑分支 | Agent 的「分支」是 LLM 自由生成的 |
| 失败时堆栈清晰 | Agent 可能默默用了错误策略但没报错 |
| 无外部依赖易 mock | Agent 依赖真实工具、API、数据库 |

## 评估维度

### 1. 任务完成度（Task Success）

最直观的指标：Agent 是否完成了用户请求？

```python
def evaluate_success(prediction: str, reference: str) -> bool:
    """用 LLM 判断预测结果是否满足参考标准"""
    prompt = f"""
用户请求：{reference}
Agent 输出：{prediction}

请判断 Agent 是否完成了用户请求。只回答"是"或"否"。
"""
    return "是" in llm.generate(prompt)
```

**更精细的指标**：
- **完全成功**：所有子任务完成，结果正确
- **部分成功**：完成了主要任务，有 minor 遗漏
- **失败**：任务未完成或结果错误

### 2. 工具调用正确性

Agent 调了哪些工具、参数对不对、顺序是否合理？

```python
# 期望的工具调用序列
expected_calls = [
    {"name": "search", "args": {"query": "国产大模型 2025"}},
    {"name": "compare", "args": {"models": ["DeepSeek", "Qwen", "Yi"]}}
]

# 实际调用序列
actual_calls = trace["tool_calls"]

# 评估：名字和关键参数是否匹配
def match_score(expected, actual):
    if expected["name"] != actual["name"]:
        return 0.0
    # 关键参数匹配度
    keys = set(expected["args"].keys())
    matched = sum(1 for k in keys if actual["args"].get(k) == expected["args"][k])
    return matched / len(keys)
```

### 3. 效率指标

| 指标 | 说明 | 目标 |
|------|------|------|
| **步数** | 完成任务用了多少轮 thought-action | 越少越好 |
| **Token 消耗** | 总输入+输出 token 数 | 控制成本 |
| **延迟** | 端到端响应时间 | 用户可接受 |
| **工具调用次数** | 外部 API 调用次数 | 越少越省 |

### 4. 安全性与边界

- **权限越界**：Agent 是否调用了不该调的工具？
- **信息泄露**：是否把敏感数据传给了外部 API？
- **幻觉输出**：最终结果是否包含编造的信息？
- **无限循环**：是否设置了 max_steps 并生效？

## 评估数据集构建

### 1. 人工标注案例

```json
{
  "input": "帮我查一下北京明天的天气，然后发邮件提醒我带伞",
  "expected_steps": [
    {"tool": "weather", "args": {"city": "北京", "date": "明天"}},
    {"tool": "send_email", "args": {"subject": "天气提醒", "body": "..."}}
  ],
  "success_criteria": "获取了北京明天天气并发送了提醒邮件"
}
```

### 2. 对抗测试（Adversarial Cases）

专门设计让 Agent 出错的输入：
- **模糊指令**："帮我处理一下那个文档"
- **矛盾需求**："用最快的速度做最详细的分析"
- **边界条件**：空输入、超长输入、特殊字符
- **恶意注入**： prompt 中夹带「忽略之前指令」类的攻击

### 3. A/B 对比测试

同一批测试集，跑两个版本的 Agent，对比指标：

```python
# 跑测试集
results_v1 = [agent_v1.run(case["input"]) for case in test_set]
results_v2 = [agent_v2.run(case["input"]) for case in test_set]

# 对比
print(f"V1 成功率: {success_rate(results_v1):.1%}")
print(f"V2 成功率: {success_rate(results_v2):.1%}")
print(f"V1 平均步数: {avg_steps(results_v1):.1f}")
print(f"V2 平均步数: {avg_steps(results_v2):.1f}")
```

## 部署策略

### 1. 渐进式发布

不要一次性全量替换旧系统：

```
Phase 1: Shadow Mode（影子模式）
   → Agent 并行运行，结果只记录不生效，对比旧系统
   
Phase 2: Canary（灰度）
   → 5% 流量走 Agent，监控错误率和用户反馈
   
Phase 3: Rollout（全量）
   → 逐步切到 100%，保留快速回滚能力
```

### 2. 关键设计：人机协同（Human-in-the-Loop）

生产环境不要完全自动，关键操作给人确认：

```python
async def execute_with_guardrails(action, tools):
    if action["risk_level"] == "high":
        # 高敏感操作：发审批通知
        approval = await request_human_approval(action)
        if not approval:
            return {"status": "rejected", "reason": "未通过人工审核"}

    return await tools.execute(action)
```

### 3. 监控与告警

| 监控项 | 告警阈值 | 响应 |
|--------|----------|------|
| 错误率 | > 5% | 自动降级到旧系统 |
| 平均步数 | > 15 | 排查是否陷入循环 |
| P99 延迟 | > 30s | 检查工具超时配置 |
| Token 成本 | 超日预算 | 限流或切换 cheaper 模型 |
| 工具失败率 | > 10% | 检查外部 API 状态 |

### 4. 版本管理与回滚

Agent 的 prompt、工具配置、模型参数都是「代码」，要版本化：

```bash
# prompt-v1.yaml
system_prompt: "你是一个谨慎的助手..."
max_steps: 10
model: gpt-4o

# 切换版本只需改配置，无需重新部署代码
```

## 从评估到上线的完整流程

```
开发 Agent → 本地单元测试 → 构建评估数据集
   ↓
跑自动化评估 → 指标达标？
   ↓ 否 → 调 prompt / 加工具 / 改策略 → 重新评估
   ↓ 是
Shadow Mode 验证 → 灰度发布 → 全量上线
   ↓
持续监控 + 定期回归测试
```

:::callout 🚀
**Agent 上线不是终点，而是起点**。上线后的真实用户反馈才是最好的评估数据——持续收集、迭代优化。
:::
