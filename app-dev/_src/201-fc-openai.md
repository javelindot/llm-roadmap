---
group: 2. Function Call
id: fc-openai
title: Function Call · OpenAI 实战
toc: FC · OpenAI
---

```python
from openai import OpenAI
client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询指定城市天气",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }
}]

resp = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "北京今天热吗？"}],
    tools=tools
)
# resp.choices[0].message.tool_calls 即模型决定调用的函数
```
