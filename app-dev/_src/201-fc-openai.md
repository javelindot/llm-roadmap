---
group: 2. Function Call
id: fc-openai
title: Function Call · OpenAI 实战
toc: FC · OpenAI
---

OpenAI 是 Function Call 的开创者，**API 设计也是事实标准** —— DeepSeek / Qwen / Moonshot 等国内模型都兼容这套协议。

## 完整 5 步代码

任务：让模型查询天气并回答用户问题。

### Step 1：定义工具

```python
from openai import OpenAI
import json

client = OpenAI()  # 自动读 OPENAI_API_KEY 环境变量

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询指定城市的当前天气情况",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，如「北京」「San Francisco」"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "温度单位",
                    "default": "celsius"
                }
            },
            "required": ["city"]
        },
        "strict": True  # 启用严格模式（推荐）
    }
}]
```

:::callout 💡
**strict: True** 是 OpenAI 2024 推出的「**保证 100% 符合 schema**」模式 —— 强烈推荐打开。模型生成的参数不再可能出现拼写错误、漏字段等问题。
:::

### Step 2：实现真实函数

```python
def get_weather(city: str, unit: str = "celsius") -> dict:
    """这是你真实的业务函数 —— 模型不会执行它"""
    # 真实实现会调气象 API
    fake_data = {
        "北京": {"temp": 32, "condition": "晴"},
        "San Francisco": {"temp": 18, "condition": "Cloudy"}
    }
    result = fake_data.get(city, {"temp": 20, "condition": "未知"})
    if unit == "fahrenheit":
        result["temp"] = result["temp"] * 9/5 + 32
    return result
```

### Step 3：第一轮 —— 模型决策

```python
messages = [
    {"role": "user", "content": "北京今天热吗？建议穿什么？"}
]

resp = client.chat.completions.create(
    model="gpt-5",
    messages=messages,
    tools=tools,
    tool_choice="auto"  # auto / none / required / {specific}
)

msg = resp.choices[0].message
# msg.tool_calls 是个列表（可能并行调多个）
tool_call = msg.tool_calls[0]
print(tool_call.function.name)       # "get_weather"
print(tool_call.function.arguments)  # '{"city": "北京", "unit": "celsius"}'
```

### Step 4：执行工具

```python
args = json.loads(tool_call.function.arguments)
result = get_weather(**args)
# {"temp": 32, "condition": "晴"}
```

### Step 5：第二轮 —— 模型综合结果

```python
# 把工具调用 + 结果都加进消息历史
messages.append(msg)  # 模型的 tool_calls 消息
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": json.dumps(result)
})

resp2 = client.chat.completions.create(
    model="gpt-5",
    messages=messages,
    tools=tools
)
final_answer = resp2.choices[0].message.content
print(final_answer)
# "北京今天 32°C 晴天，比较热。建议穿轻薄透气的衣物，记得防晒。"
```

## 通用调度循环

实际应用中，模型可能**多轮调用工具**（先查天气再查穿搭推荐）。封装成循环：

```python
def chat_with_tools(user_message: str, tools: list, tool_handlers: dict,
                    max_iterations: int = 5):
    """通用调度循环：处理多轮 FC"""
    messages = [{"role": "user", "content": user_message}]

    for _ in range(max_iterations):
        resp = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        msg = resp.choices[0].message
        messages.append(msg)

        # 没有工具调用 → 模型给出最终答案
        if not msg.tool_calls:
            return msg.content

        # 有工具调用 → 执行所有调用
        for tc in msg.tool_calls:
            fn = tool_handlers[tc.function.name]
            args = json.loads(tc.function.arguments)
            result = fn(**args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result, ensure_ascii=False)
            })

    raise RuntimeError(f"超过 {max_iterations} 轮仍未结束")

# 使用
answer = chat_with_tools(
    user_message="北京今天热吗？建议穿什么？",
    tools=tools,
    tool_handlers={"get_weather": get_weather}
)
```

## tool_choice 的 4 种模式

| 取值 | 行为 |
|------|------|
| `"auto"` （默认）| 模型自主判断要不要调 |
| `"none"` | 强制不调用，只生成文本 |
| `"required"` | 强制必须调一个工具 |
| `{"type":"function","function":{"name":"..."}}` | 强制调指定工具 |

实战场景：
- **客服意图分类**：`tool_choice="required"` + 多个分类工具，强制必须分类
- **闲聊**：`tool_choice="none"`，不让模型乱调工具
- **复杂任务**：`tool_choice="auto"`，让模型自由决策

## 多工具并行调用

GPT-4o / GPT-5 默认支持**一次调多个工具**。例如「查北京和上海的天气」 → 模型一次返回 2 个 tool_calls。

```python
# 模型可能一次返回：
[
    {name: "get_weather", arguments: '{"city": "北京"}'},
    {name: "get_weather", arguments: '{"city": "上海"}'}
]

# 并行执行
import asyncio

async def run_tool(tc):
    args = json.loads(tc.function.arguments)
    return await tool_handlers[tc.function.name](**args)

results = await asyncio.gather(*[run_tool(tc) for tc in msg.tool_calls])
```

详见 [并行调用与错误处理](#parallel-errors)。

## 国内模型兼容性

OpenAI Function Call 协议是事实标准，以下都兼容：

| 模型 | 兼容性 | 备注 |
|------|--------|------|
| DeepSeek-V3 | ⭐⭐⭐⭐⭐ | 完全兼容，价格 1/10 |
| Qwen3 | ⭐⭐⭐⭐⭐ | 完全兼容 |
| Moonshot Kimi | ⭐⭐⭐⭐⭐ | 完全兼容，长上下文 |
| 智谱 GLM-4.5 | ⭐⭐⭐⭐ | 基本兼容，schema 严格度略低 |

切换 base_url 就能直接用 OpenAI SDK 调国内模型：

```python
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)
# 代码其他都不用改
```

## 常见坑

| 坑 | 解决方案 |
|----|---------|
| arguments 是字符串不是对象 | 始终 `json.loads()` 一下 |
| 大模型乱传参数 | 开 `strict: True` |
| 一直循环调用 | 设 `max_iterations` 上限 |
| 多轮历史太长 | 截断或用 Prompt Caching |
| description 不够清晰 | 写明用例 + 边界条件 |

下一节：[Anthropic Tool Use](#fc-anthropic) —— Claude 的实现差异。
