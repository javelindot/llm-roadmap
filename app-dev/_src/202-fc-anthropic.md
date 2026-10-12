---
group: 2. Function Call
id: fc-anthropic
title: Function Call · Anthropic 实战
toc: FC · Anthropic
---

Claude 的客户端工具通过 Messages API 的 tool_use 和 tool_result 往返。接口核对日期为 2026-10-12；真实调用需固定 anthropic 版本和已验收模型。

## 客户端与服务端工具

客户端工具由应用执行，模型返回请求不代表操作已经发生。服务端工具在供应商环境执行，其事件、停机原因和费用按具体工具处理。浏览器、电脑和 Shell 等能力还需要运行环境与权限控制。

## 完整客户端循环

设置 ANTHROPIC_API_KEY 和 ANTHROPIC_MODEL。本例仅用只读模拟天气，不启用 thinking、服务端工具或 beta 功能，这些组合需要另做契约测试。

```python
import json
import os
from anthropic import Anthropic

# 请求重试交给应用预算管理，避免多层重复重试。
client = Anthropic(timeout=20, max_retries=0)
model = os.environ["ANTHROPIC_MODEL"]
tools = [{
    "name": "get_weather",
    "description": "只读查询北京模拟天气；其他城市返回无数据。",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
        "additionalProperties": False,
    },
}]


def get_weather(arguments):
    """验证模型参数后读取模拟事实，不返回虚构的默认温度。

    模型输入只是候选，业务服务仍需独立验证。
    真实服务还需数据来源、新鲜度和资源授权检查。
    """
    if not isinstance(arguments, dict) or set(arguments) != {"city"}:
        raise ValueError("invalid_arguments")
    if not isinstance(arguments["city"], str):
        raise ValueError("invalid_arguments")
    if arguments["city"] != "北京":
        return {"status": "not_found"}
    return {"status": "ok", "temperature": 32, "unit": "celsius", "source": "demo"}


def weather_reply(question, max_rounds=4):
    """保留完整 assistant 内容，按 ID 返回全部客户端工具结果。

    多个结果放入紧随请求的同一 user 消息。
    本例对其他停机原因明确停止，不把截断误报为完成。
    """
    messages = [{"role": "user", "content": question}]
    for _ in range(max_rounds):
        response = client.messages.create(model=model, max_tokens=1024,
                                          tools=tools, messages=messages)
        if response.stop_reason == "end_turn":
            text = "\n".join(block.text for block in response.content if block.type == "text")
            if not text:
                raise RuntimeError("empty_model_response")
            return text
        if response.stop_reason != "tool_use":
            raise RuntimeError("unhandled_stop_reason:" + str(response.stop_reason))
        calls = [block for block in response.content if block.type == "tool_use"]
        if not calls or len(calls) > 8:
            raise RuntimeError("invalid_tool_call_count")
        # 保留全部协议内容；不能假定 content[0] 就是目标工具。
        messages.append({"role": "assistant", "content": response.content})
        results = []
        for call in calls:
            error = False
            if call.name != "get_weather":
                value, error = {"error": "unknown_tool"}, True
            else:
                try:
                    value = get_weather(call.input)
                except (ValueError, TypeError):
                    value, error = {"error": "invalid_arguments"}, True
            results.append({"type": "tool_result", "tool_use_id": call.id,
                            "content": json.dumps(value, ensure_ascii=False), "is_error": error})
        messages.append({"role": "user", "content": results})
    raise RuntimeError("model_round_budget_exceeded")


print(weather_reply("北京的模拟天气是多少摄氏度？"))
```

## 严格工具与结构化结果

当前官方文档提供 strict tool use，可在受支持的自定义工具定义中设置 strict。支持模型、schema 子集及组合按具体接口确认，不能将“通常遵守 schema”当成协议保证。

JSON 输出用于提取与分类，工具请求用于能力执行，两者均需语义和授权校验，见[结构化输出](204-structured-outputs.html)。

## thinking、缓存与发现

thinking 参数、输出预算关系与需要保留的内容块按模型契约处理。不提供脱离版本的固定 budget_tokens 配方，也不要求私有推理文本。

Prompt Caching、Tool Search 和 Programmatic Tool Calling 分别处理部分重复输入计算、按需工具定义及工具编排。它们不能自动赋予业务授权或解决动作幂等。

缓存命中与计费按实际 usage 核对，移除过期 beta 头。跨供应商比较使用同一任务、权限与预算，不凭品牌断言质量优劣。

## 集成验收

覆盖多个内容块、多工具关联、错误结果、max_tokens、拒绝、pause_turn 等适用停机原因。本例只涵盖基本客户端循环，未在认证环境调用真实模型；功能扩展需要独立契约测试。

参考：[Claude Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)。下一节：[并行与错误处理](203-parallel-errors.html)。
