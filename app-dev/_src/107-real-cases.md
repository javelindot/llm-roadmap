---
group: 1. Prompt 工程
id: real-cases
title: Prompt · 6 大实战案例
toc: Prompt · 实战案例
---

把前面学的全部应用起来。6 个真实场景，覆盖大模型应用的高频需求。

## 案例 1：SQL 生成

**目标**：让模型把自然语言查询变成可直接执行的 SQL。

```python
PROMPT = """你是 PostgreSQL 14+ SQL 专家。

数据库 Schema：
<schema>
TABLE users (
  id BIGINT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(200) UNIQUE,
  created_at TIMESTAMP
)
TABLE orders (
  id BIGINT PRIMARY KEY,
  user_id BIGINT REFERENCES users(id),
  amount DECIMAL(10,2),
  status VARCHAR(20),  -- pending/paid/refunded
  created_at TIMESTAMP
)
</schema>

任务：将用户的自然语言查询转换为 PostgreSQL 14+ SQL。

约束：
- 只输出 SQL，不要任何解释
- 使用参数化查询（$1, $2 占位符），避免 SQL 注入
- 时间使用 PostgreSQL 标准格式
- 加上合理的索引提示注释（如果该查询会全表扫描）

示例：
查询：「最近 7 天每个用户的订单总额」
SQL：
SELECT u.id, u.name, SUM(o.amount) AS total
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE o.created_at >= NOW() - INTERVAL '7 days'
  AND o.status = 'paid'
GROUP BY u.id, u.name
ORDER BY total DESC;

待转换查询：
{user_query}

SQL：
"""
```

**关键技巧**：把 schema 作为 system context，约束输出 SQL only（方便后续直接执行）。

## 案例 2：客服意图分类

**目标**：把用户消息自动分类，路由到不同处理流程。

```python
PROMPT = """你是客服意图识别助手。

<categories>
- 咨询：询问产品信息、功能、价格、库存
- 投诉：表达不满、反馈问题、负面情绪
- 退款：请求退货、退款、换货
- 物流：询问订单状态、配送、延迟
- 其他：上述都不属于
</categories>

请按 JSON 格式输出，不要任何额外文字：
{
  "category": "咨询|投诉|退款|物流|其他",
  "confidence": 0.0-1.0,
  "urgency": "low|medium|high",
  "reasoning": "1 句话"
}

用户消息：
<message>
{user_message}
</message>
"""
```

**关键技巧**：
- 类别用 `<categories>` 标签清晰列出
- 输出 confidence + urgency 便于下游决策
- 强制 JSON 格式便于程序消费

## 案例 3：情感分析（带 reasoning）

**目标**：不只判断正负面，还要解释原因（便于客户洞察）。

```python
PROMPT = """对用户评论做情感分析。

输出 JSON：
{
  "sentiment": "positive|negative|neutral|mixed",
  "intensity": 1-5（强度）,
  "aspects": [
    {"aspect": "...", "sentiment": "positive|negative|neutral", "snippet": "原文片段"}
  ],
  "summary": "用 1 句话概括"
}

约束：
- aspect 限于：价格 / 质量 / 服务 / 物流 / 外观 / 性能
- snippet 必须是原文逐字摘抄
- 即使是 positive 整体，也要列出 negative aspects（如果有）

评论：
<review>
{review}
</review>
"""

# 示例输入: "手机外观很赞，但电池续航太差了，客服态度倒是不错"
# 输出:
# {
#   "sentiment": "mixed",
#   "intensity": 3,
#   "aspects": [
#     {"aspect": "外观", "sentiment": "positive", "snippet": "外观很赞"},
#     {"aspect": "性能", "sentiment": "negative", "snippet": "电池续航太差"},
#     {"aspect": "服务", "sentiment": "positive", "snippet": "客服态度倒是不错"}
#   ],
#   "summary": "外观和服务好评，但电池续航差"
# }
```

**关键技巧**：限定 aspect 集合 → 输出可直接进数据库做统计。

## 案例 4：营销文案生成（带个性化）

**目标**：基于产品特性 + 目标人群，生成多版本文案。

```python
PROMPT = """你是资深营销文案策划。

产品信息：
<product>
{product_description}
</product>

目标人群：
<audience>
{audience_persona}  
例如：25-35 岁一线城市职场女性，注重健康
</audience>

平台：{platform}（小红书 / 微博 / 微信公众号 / 朋友圈）

任务：生成 3 个差异化文案版本，分别采用不同策略：
- 版本 A：场景化叙事（讲故事）
- 版本 B：数据+权威（理性派）
- 版本 C：情感共鸣（戳痛点）

约束：
- 符合 {platform} 平台风格（小红书要 emoji + 排版，公众号要标题党）
- 每版不超过 {max_length} 字
- 不允许「赋能 / 颠覆 / 闭环」等无意义词
- 不允许虚假宣传（疗效、绝对化用词）

输出格式：Markdown，每版本一节
"""
```

**关键技巧**：明确禁词清单 + 多版本对比，让运营选最优。

## 案例 5：技术文档摘要

**目标**：长文档（10K+ 字）→ 结构化摘要 + 关键点。

```python
PROMPT = """你是技术文档分析师。

任务：阅读以下技术文档，输出结构化摘要。

输出格式（严格遵守）：
## TL;DR
（1 句话概括，≤50 字）

## 关键概念
- 概念 1：定义
- 概念 2：定义
（最多 5 个）

## 核心流程
（用编号步骤描述主要工作流，≤7 步）

## 适用场景
（列出 3-5 个典型用例）

## 限制与坑
（列出文档中明确提到的局限性，≤5 条）

## 代码示例提取
（从文档中提取最有代表性的 1 段代码，原样保留）

文档内容：
<document>
{document}
</document>
"""
```

**关键技巧**：固定输出 schema → 多份文档摘要可对比、可入库。

## 案例 6：复杂任务多步骤拆解（数据分析报告）

**目标**：从原始数据 + 业务目标 → 完整分析报告。这是「多步骤 Prompt」的典型应用。

```python
# Step 1: 数据预览 + 问题识别
PROMPT_1 = """
数据样本（前 10 行）：
{data_preview}

业务目标：{business_goal}

请输出：
1. 数据完整性评估
2. 可能的分析方向（≥3 个）
3. 推荐优先分析的 1 个方向，并说明原因
"""

# Step 2: 基于 Step 1 选定方向做分析
PROMPT_2 = """
基于以下数据和方向，输出分析结论：

数据：{data_summary}
分析方向：{chosen_direction}

输出：
1. 核心发现（3-5 条）
2. 支撑数据（每条结论都要引用具体数字）
3. 可视化建议（推荐用什么图表）
"""

# Step 3: 生成行动建议
PROMPT_3 = """
分析结论：{analysis}
业务目标：{business_goal}

请给出 5 条具体可执行的行动建议，每条包含：
- 行动描述
- 优先级（high/medium/low）
- 预期效果
- 执行时间预估
"""

# 编排
def generate_report(data, business_goal):
    step1 = llm(PROMPT_1.format(data_preview=data[:10], business_goal=business_goal))
    direction = parse_direction(step1)

    step2 = llm(PROMPT_2.format(data_summary=summarize(data), chosen_direction=direction))
    analysis = parse_analysis(step2)

    step3 = llm(PROMPT_3.format(analysis=analysis, business_goal=business_goal))
    actions = parse_actions(step3)

    return assemble_report(step1, step2, step3)
```

**关键技巧**：拆步骤后每步任务简单 → 每步可单独评测 → 整体 reliability 大幅提升。

:::callout 💡
**多步骤 vs Agent 的边界**：固定流程用「多步骤 Prompt」；流程不固定（需要决策）用 [Agent](#agent-concept)。
:::

## 7 个跨场景的通用 Tip

1. **永远用 system message 设角色**（不要混在 user message 里）
2. **结构化输出 > 自由文本**（除非是创意场景）
3. **每 prompt 加 1–3 个 Few-shot 示例**（哪怕任务简单）
4. **限制条件比指令更重要**（说「不要做什么」比说「要做什么」更有效）
5. **长 prompt 用 XML 标签分段**（`<task>`, `<context>`, `<examples>`）
6. **温度按任务调**：分类/提取用 0，创意用 0.7–1.0
7. **永远做评测**（哪怕只有 20 条用例）

## 进阶资源

- [Anthropic Prompt Library](https://docs.anthropic.com/en/prompt-library) —— 官方 60+ 经典 prompt
- [OpenAI Cookbook](https://cookbook.openai.com/) —— 实战示例代码
- [LangChain Hub](https://smith.langchain.com/hub) —— 社区 prompt 仓库

下一模块：[Function Call](#fc-concept) —— 让模型不只输出文字，还能调外部 API。
