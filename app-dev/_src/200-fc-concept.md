---
group: 2. Function Call
id: fc-concept
title: Function Call · 工作原理
toc: FC · 原理
---

**Function Call**（也叫 Tool Use）让大模型从「**会说话的文档库**」进化成「**能干活的助手**」 —— 这是 LLM 应用从玩具到生产工具的分水岭。

## 为什么需要 Function Call

纯 LLM 有 4 个**天生缺陷**：

| 缺陷 | 例子 |
|------|------|
| 知识截止 | 不知道今天美股收盘价、最新 iOS 版本号 |
| 不会算 | 复杂数学算错率 30%+，金融计算不能信 |
| 没记忆 | 不知道你的订单状态、不知道用户偏好 |
| 没双手 | 不能发邮件、不能下单、不能调外部 API |

Function Call 把这 4 个缺陷一次性补齐 —— **让模型决定何时调用外部能力**，开发者负责执行。

## 核心机制：决策 + 调用 + 反馈 + 生成

```
┌────────────────────────────────────────────────┐
│  ① 开发者定义工具 (JSON Schema)                  │
│       ↓                                        │
│  ② 用户提问                                     │
│       ↓                                        │
│  ③ 模型决策: 要不要调？调哪个？传什么参数？        │
│       ↓ (输出 tool_call: {name, arguments})    │
│  ④ 开发者执行工具 (调 API / 查 DB / 跑代码)       │
│       ↓                                        │
│  ⑤ 把结果返回给模型                              │
│       ↓                                        │
│  ⑥ 模型生成最终回答                              │
└────────────────────────────────────────────────┘
```

**关键认知**：模型**不直接执行代码** —— 它只输出「我想调用 get_weather('北京')」这样的结构化指令，由你的代码去真正执行。

## 一个最小例子

任务：「北京今天热吗？」

```python
# Step 1: 定义工具
tools = [{
    "name": "get_weather",
    "description": "查询指定城市当前天气",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "城市名"}
        },
        "required": ["city"]
    }
}]

# Step 2-3: 模型决策
resp = client.messages.create(
    model="claude-sonnet-4-5",
    tools=tools,
    messages=[{"role": "user", "content": "北京今天热吗？"}]
)
# resp.stop_reason == "tool_use"
# resp.content 包含 tool_use block:
#   {name: "get_weather", input: {"city": "北京"}}

# Step 4: 开发者执行
weather = get_weather_api(city="北京")  # 你的真实函数
# 返回: {"temp": 32, "condition": "晴"}

# Step 5-6: 把结果喂回去
resp2 = client.messages.create(
    model="claude-sonnet-4-5",
    tools=tools,
    messages=[
        {"role": "user", "content": "北京今天热吗？"},
        {"role": "assistant", "content": resp.content},  # 含 tool_use
        {"role": "user", "content": [{
            "type": "tool_result",
            "tool_use_id": tool_use.id,
            "content": json.dumps(weather)
        }]}
    ]
)
# resp2.content[0].text: "北京今天 32°C 晴天，挺热的，注意防晒。"
```

## 工具定义就是 JSON Schema

所有主流模型（OpenAI / Anthropic / Gemini / DeepSeek）都用 JSON Schema 描述参数。**写好 schema 比写好代码更重要**。

```json
{
  "name": "search_orders",
  "description": "查询用户订单，支持按状态、日期范围筛选",
  "input_schema": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string",
        "description": "用户 ID（必填）"
      },
      "status": {
        "type": "string",
        "enum": ["pending", "paid", "shipped", "refunded"],
        "description": "订单状态（可选，不填查全部）"
      },
      "date_from": {
        "type": "string",
        "format": "date",
        "description": "起始日期 YYYY-MM-DD"
      },
      "limit": {
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "default": 20
      }
    },
    "required": ["user_id"]
  }
}
```

3 个**关键质量要素**：

1. **description 必须清晰** —— 模型靠这段文字判断「这个工具能干啥」
2. **enum 比 string 好** —— 限定枚举值能大幅降低参数错误
3. **required 明确标注** —— 模型不知道哪些必填会乱传

## Function Call 解决了什么

| 之前（纯 LLM）| 之后（带 FC）|
|---------------|------------|
| 「我不知道今天股价」 | 调 `get_stock_price("AAPL")` → 准确回答 |
| 「我算不准」 | 调 `calculator(expr)` → 算数学题 |
| 「我看不到你的订单」 | 调 `query_orders(user_id)` → 私域数据 |
| 「我没法发邮件」 | 调 `send_email(to, subject, body)` → 真发 |

简单说：**模型从「说」进化到「做」**。

## Function Call 不是银弹

理想很美好，工程上要注意 3 个坑：

:::callout ⚠️
**坑 1：调用决策可能错**
模型可能该调用却不调（直接编答案），或不该调却调了（瞎调一通）。需要靠 prompt 和评测改进。

**坑 2：参数可能错**
模型可能漏传必填、传错类型、传不存在的枚举值。**永远要在代码里 validate**。

**坑 3：成本翻倍**
一次完整的 FC 闭环要调用 LLM 2 次（决策 + 总结），延迟和成本都翻倍。
:::

## 何时用 / 何时不用

✅ **该用 FC**：
- 需要实时数据（股价、天气、库存）
- 需要查私域信息（订单、用户、内部文档）
- 需要执行操作（发邮件、改数据、调用服务）
- 需要精确计算

❌ **不需要 FC**：
- 纯对话 / 闲聊
- 内容生成（写作、翻译、改写）
- 信息总结（已经在 prompt 里给的内容）
- 用 RAG 就能解决的知识问答

## 与 RAG / MCP / Agent 的关系

```
RAG       = 给模型「读」外部知识的能力
Function Call = 给模型「调用 API」的能力（最基础）
MCP       = Function Call 的标准化协议（让工具可复用）
Agent     = 多步 Function Call 编排 + 自主决策
```

学习顺序建议：**FC → MCP → Agent**，先打地基。

下一节：[OpenAI Function Calling 实战](#fc-openai) —— 写第一个真实可跑的代码。
