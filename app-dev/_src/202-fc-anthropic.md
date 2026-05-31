---
group: 2. Function Call
id: fc-anthropic
title: Function Call · Anthropic 实战
toc: FC · Anthropic
---

Anthropic Claude 的 Tool Use 与 OpenAI 协议相似但有几处关键差异 —— **理解差异能少踩 80% 的坑**。

## 与 OpenAI 的差异速览

| 维度 | OpenAI | Anthropic |
|------|--------|-----------|
| 工具字段名 | `tools[].function` | `tools[]` 直接（无嵌套）|
| 参数 schema | `parameters` | `input_schema` |
| 调用 block | `tool_calls[]` | `content[].type == "tool_use"` |
| 结果 block | `role: tool` | `role: user` + `content[type:tool_result]` |
| 严格模式 | `strict: true` | 默认就比较严格 |
| 并行调用 | 默认开启 | `disable_parallel_tool_use: false` 启用 |

## 完整 5 步代码

### Step 1：定义工具（注意是 input_schema）

```python
from anthropic import Anthropic
import json

client = Anthropic()  # 自动读 ANTHROPIC_API_KEY

tools = [{
    "name": "get_weather",  # 注意：没有嵌套在 function 里
    "description": "查询指定城市的当前天气情况",
    "input_schema": {  # 注意：叫 input_schema，不是 parameters
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "城市名称"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "default": "celsius"
            }
        },
        "required": ["city"]
    }
}]
```

### Step 2：业务函数（同 OpenAI）

```python
def get_weather(city: str, unit: str = "celsius") -> dict:
    fake_data = {"北京": {"temp": 32, "condition": "晴"}}
    return fake_data.get(city, {"temp": 20, "condition": "未知"})
```

### Step 3：第一轮 —— 模型决策

```python
messages = [{"role": "user", "content": "北京今天热吗？"}]

resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

# resp.stop_reason 可能值:
# "end_turn"   → 正常结束
# "tool_use"   → 要调用工具
# "max_tokens" → 截断
# "stop_sequence" → 遇到停止符

assert resp.stop_reason == "tool_use"

# 找到 tool_use block（content 可能混合文本和工具调用）
tool_uses = [b for b in resp.content if b.type == "tool_use"]
tu = tool_uses[0]
print(tu.name)   # "get_weather"
print(tu.input)  # {"city": "北京"}（已经是 dict，不用 json.loads）
print(tu.id)     # "toolu_xxx" 唯一 ID
```

### Step 4：执行工具

```python
result = get_weather(**tu.input)
# {"temp": 32, "condition": "晴"}
```

### Step 5：第二轮 —— 返回结果

```python
messages.extend([
    {"role": "assistant", "content": resp.content},  # 模型的 content（含 tool_use）
    {
        "role": "user",  # 注意：tool_result 用 user 角色
        "content": [{
            "type": "tool_result",
            "tool_use_id": tu.id,
            "content": json.dumps(result, ensure_ascii=False)
        }]
    }
])

resp2 = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    messages=messages
)
print(resp2.content[0].text)
# "北京今天 32°C 晴天，挺热的，注意防晒。"
```

## 通用调度循环（Anthropic 版）

```python
def chat_with_tools_anthropic(user_message: str, tools: list, 
                              tool_handlers: dict, max_iterations: int = 5):
    messages = [{"role": "user", "content": user_message}]

    for _ in range(max_iterations):
        resp = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            tools=tools,
            messages=messages
        )
        messages.append({"role": "assistant", "content": resp.content})

        # 没有工具调用 → 结束
        if resp.stop_reason != "tool_use":
            # 提取最终文本
            text_blocks = [b.text for b in resp.content if b.type == "text"]
            return "\n".join(text_blocks)

        # 执行所有工具调用
        tool_results = []
        for block in resp.content:
            if block.type == "tool_use":
                fn = tool_handlers[block.name]
                try:
                    result = fn(**block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=False)
                    })
                except Exception as e:
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": f"Error: {str(e)}",
                        "is_error": True  # 告诉模型这次调用失败
                    })

        messages.append({"role": "user", "content": tool_results})

    raise RuntimeError(f"超过 {max_iterations} 轮仍未结束")
```

## tool_choice 选项

Anthropic 也支持强制工具调用：

```python
resp = client.messages.create(
    model="claude-sonnet-4-5",
    tools=tools,
    tool_choice={"type": "auto"},      # 默认
    # tool_choice={"type": "any"},      # 必须调一个工具（任意）
    # tool_choice={"type": "tool", "name": "get_weather"},  # 指定工具
    messages=messages
)
```

## 并行工具调用控制

Claude 4.5 默认会**并行调用工具**。可以禁用：

```python
resp = client.messages.create(
    model="claude-sonnet-4-5",
    tools=tools,
    tool_choice={
        "type": "auto",
        "disable_parallel_tool_use": True  # 强制串行
    },
    messages=messages
)
```

何时需要禁用：
- 工具之间有**依赖关系**（必须先查 A 再查 B）
- 后端 API 有**并发限制**
- 调试时想要**确定性顺序**

## 与 Computer Use（电脑操作能力）结合

Claude 4.5 独有的能力：**直接操作电脑屏幕** —— 截图、点击、打字。

```python
# Claude 可以"看见"屏幕并控制电脑
resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[{
        "type": "computer_20250124",  # 内置 computer use 工具
        "name": "computer",
        "display_width_px": 1920,
        "display_height_px": 1080
    }],
    messages=[{"role": "user", "content": "帮我在淘宝搜索 iPhone 16 Pro"}]
)
# 模型会返回 tool_use: {action: "screenshot"} 或 {action: "left_click", coordinate: [x,y]}
```

这是 Anthropic 的独特优势 —— OpenAI 还在追赶。

## Extended Thinking + Tool Use

Claude 4.5 的推理模式可以和工具调用结合 —— 模型先深度思考再决定调哪个工具。

```python
resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    thinking={"type": "enabled", "budget_tokens": 5000},
    tools=tools,
    messages=[{"role": "user", "content": "..."}]
)
# resp.content 可能包含:
# - thinking block（推理过程）
# - tool_use block（调用决策）
# - text block（说明）
```

适合复杂决策场景：在多个工具之间精挑细选、参数推算需要计算等。

## Prompt Caching + Tools

工具定义是个长 JSON，每次都传浪费 token。开启 cache：

```python
resp = client.messages.create(
    model="claude-sonnet-4-5",
    tools=tools,
    system=[{
        "type": "text",
        "text": SYSTEM_PROMPT,
        "cache_control": {"type": "ephemeral"}  # 缓存系统 prompt
    }],
    messages=messages,
    extra_headers={"anthropic-beta": "tools-2024-04-04"}
)
# 工具定义 + 系统 prompt 都被缓存，第 2 次起便宜 90%
```

## Anthropic vs OpenAI 总结

✅ **Anthropic 更强的地方**：
- 推理质量更高（Extended Thinking）
- Computer Use 能直接操作电脑
- Prompt Caching 折扣更大
- 工具调用的 reasoning 更稳定

✅ **OpenAI 更强的地方**：
- `strict: true` 100% schema 保证
- 国内模型几乎都兼容它的 API（迁移成本低）
- 生态更成熟（LangChain 默认就是 OpenAI 风格）

**实战建议**：客服 / 高频调用用 DeepSeek（OpenAI 兼容），复杂决策 / Agent 用 Claude。

下一节：[并行调用与错误处理](#parallel-errors) —— 生产环境的硬核话题。
