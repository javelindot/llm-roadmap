---
group: 2. Function Call
id: fc-openai
title: Function Call · OpenAI 实战
toc: FC · OpenAI
---

本章采用 **Responses API** 演示应用执行的只读工具。模型由环境变量固定到已验收部署，不承诺某个型号在所有账号都可用。接口核对日期：2026-10-12。

## 区分接口契约

| 字段 | Responses | Chat Completions |
|------|-----------|------------------|
| 工具定义 | name、parameters 直接放在 function 类型工具对象 | 嵌套 tools[].function |
| 工具请求 | output 中的 function_call | message.tool_calls |
| 参数 | arguments JSON 字符串 | function.arguments JSON 字符串 |
| 工具结果 | function_call_output + call_id | role=tool + tool_call_id |
| 延续状态 | 完整 output 或合法的响应关联 | 按协议保存消息历史 |

部分新模型的工具调用要求 Responses；第三方 OpenAI 兼容接口可能仅支持 Chat Completions。能力要覆盖具体模型、API 和 SDK，不能只替换 base_url。

## 完整只读循环

安装 openai，设置 OPENAI_API_KEY、LLM_MODEL。代码调用真实模型，但天气数据是本地模拟，不能作为真实天气服务。

```python
import json
import os
from openai import OpenAI

# 请求重试由应用管理，避免 SDK 与工具层重复重试。
client = OpenAI(timeout=20, max_retries=0)
model = os.environ["LLM_MODEL"]
tools = [{
    "type": "function",
    "name": "get_weather",
    "description": "只读查询北京模拟天气；其他城市返回无数据。",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string"},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["city", "unit"],
        "additionalProperties": False,
    },
}]


def get_weather(arguments):
    """验证参数并读取模拟事实，不为未知城市编造温度。

    严格输出约束不替代本地验证。
    真实服务还需来源、新鲜度与资源授权检查。
    """
    if not isinstance(arguments, dict) or set(arguments) != {"city", "unit"}:
        raise ValueError("invalid_arguments")
    if not isinstance(arguments["city"], str) or arguments["unit"] not in {"celsius", "fahrenheit"}:
        raise ValueError("invalid_arguments")
    if arguments["city"] != "北京":
        return {"status": "not_found"}
    temperature = 32 if arguments["unit"] == "celsius" else 89.6
    return {"status": "ok", "temperature": temperature, "unit": arguments["unit"], "source": "demo"}


def weather_reply(question, max_rounds=4):
    """保留协议项，按 call_id 关联结果，并限制只读工具循环。

    写工具应接独立授权与动作执行器。
    拒绝、不完整和空结果分别停止，不伪装成完成。
    """
    items = [{"role": "user", "content": question}]
    for _ in range(max_rounds):
        response = client.responses.create(
            model=model,
            instructions="天气工具是模拟数据；明确来源，无数据时说明缺失。",
            input=items, tools=tools,
        )
        if response.status != "completed":
            raise RuntimeError("model_response_incomplete")
        refusals = [part for item in response.output if item.type == "message"
                    for part in item.content if part.type == "refusal"]
        if refusals:
            raise RuntimeError("model_refused")
        # 完整保留工具请求及必要推理项，不能只复制最终文本。
        items.extend(response.output)
        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            if not response.output_text:
                raise RuntimeError("empty_model_response")
            return response.output_text
        if len(calls) > 8:
            raise RuntimeError("tool_call_budget_exceeded")
        for call in calls:
            if call.name != "get_weather":
                result = {"error": "unknown_tool"}
            else:
                try:
                    result = get_weather(json.loads(call.arguments))
                except (ValueError, TypeError):
                    result = {"error": "invalid_arguments"}
            items.append({"type": "function_call_output", "call_id": call.call_id,
                          "output": json.dumps(result, ensure_ascii=False)})
    raise RuntimeError("model_round_budget_exceeded")


print(weather_reply("北京的模拟天气是多少摄氏度？"))
```

数据留存、推理项延续及无状态模式按所选模型的官方契约配置并验证，不依赖示例默认值。单次 timeout 与轮数上限不等于完整总时间、token 和费用预算。

## 严格模式与授权

严格 schema 应符合接口支持的子集。本例全部属性列为 required，禁止额外属性；可缺失语义可用必填的可空字段表达。

结构正确不证明参数对应真实需求、资源已授权或业务状态允许执行。拒绝、输出不完整和网络失败仍需处理，执行层校验不可省略。

## 工具选择与并行

auto 允许选择，none 禁止工具，required 要求一个或多个调用，指定函数可限制某个工具。参数形状区分 API，调用次数由应用控制。

多个请求不等于应用已经并行执行。互不依赖的只读工具可限并发；写操作及依赖步骤交给业务运行时，见[并行与错误处理](203-parallel-errors.html)。

## 集成验收

覆盖零调用、多调用、非法参数、未知工具、拒绝、不完整输出、故障和结果关联。本章未在认证环境调用真实模型；真实集成应固定 SDK 版本并验证上述契约。

参考：[OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling)。下一节：[Claude Tool Use](202-fc-anthropic.html)。
