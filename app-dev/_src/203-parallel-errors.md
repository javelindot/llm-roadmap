---
group: 2. Function Call
id: parallel-errors
title: Function Call · 并行调用与错误处理
toc: FC · 并行+错误
---

生产环境的 FC 必须处理 3 类问题：**并行加速、错误恢复、循环防御**。这一章讲清楚。

## 1. 并行工具调用

### 模型为什么要并行调

任务：「比较北京和上海今天的天气，给我穿搭建议」

```
❌ 串行（旧模式）:
   调 get_weather("北京")  → 等结果 → 调 get_weather("上海")  → 等结果 → 答
   总耗时 = T1 + T2 + 推理 ≈ 3-5 秒

✅ 并行（GPT-4o+ / Claude 4.5 默认）:
   一次返回 [get_weather("北京"), get_weather("上海")] → 并行执行 → 答
   总耗时 = max(T1, T2) + 推理 ≈ 1.5-2 秒
```

### 实现并行执行

```python
import asyncio
import json

async def execute_tools_parallel(tool_calls: list, tool_handlers: dict):
    """并行执行所有工具调用"""

    async def run_one(tc):
        try:
            args = json.loads(tc.function.arguments)  # OpenAI 格式
            handler = tool_handlers[tc.function.name]

            # 区分同步 / 异步函数
            if asyncio.iscoroutinefunction(handler):
                result = await handler(**args)
            else:
                # 同步函数放线程池跑（避免阻塞 event loop）
                result = await asyncio.to_thread(handler, **args)

            return {
                "tool_call_id": tc.id,
                "role": "tool",
                "content": json.dumps(result, ensure_ascii=False)
            }
        except Exception as e:
            # 单个工具失败不应该让整批 fail
            return {
                "tool_call_id": tc.id,
                "role": "tool",
                "content": json.dumps({"error": str(e)})
            }

    return await asyncio.gather(*[run_one(tc) for tc in tool_calls])
```

### 性能数据

5 个工具并行 vs 串行（每个工具 1s）：

| 模式 | 总耗时 | LLM 调用次数 |
|------|--------|------------|
| 串行 | 5s + 推理 | 6 次（每工具 1 次 + 总结）|
| 并行 | 1s + 推理 | 2 次（决策 + 总结）|

**并行 = 5× 加速 + ⅓ LLM 成本**。

## 2. 错误处理：让模型知道失败了

### 错误的处理方式

```python
# ❌ 出错直接抛
try:
    result = get_weather(city="火星")
except Exception as e:
    raise  # 整个调用链断了，模型无法恢复
```

### 正确做法：把错误返回给模型

```python
# ✅ 把错误信息当成 tool_result 返回
try:
    result = get_weather(city="火星")
    tool_result = {
        "tool_use_id": tu.id,
        "content": json.dumps(result),
        "is_error": False
    }
except CityNotFoundError as e:
    tool_result = {
        "tool_use_id": tu.id,
        "content": json.dumps({
            "error": "city_not_found",
            "message": f"找不到城市 '{e.city}'",
            "suggestion": "请确认城市名拼写，目前只支持地球上的城市"
        }),
        "is_error": True  # Anthropic 专有字段
    }
except RateLimitError as e:
    tool_result = {
        "tool_use_id": tu.id,
        "content": json.dumps({
            "error": "rate_limit",
            "retry_after": e.retry_after
        }),
        "is_error": True
    }
```

**模型看到错误后会智能处理** —— 比如改用其他工具、给用户解释、推荐 fallback。

### 错误类型设计

给模型可读的错误结构：

```python
{
    "error": "machine_readable_code",     # 程序可判断
    "message": "human readable text",      # 模型可理解并解释给用户
    "suggestion": "下一步建议",             # 可选，指导模型 retry
    "retry_after": 30                      # 可选，retry 信号
}
```

### 哪些错误应该重试

```python
RETRYABLE_ERRORS = {
    "rate_limit",        # 限流，等 retry_after 后重试
    "timeout",           # 超时
    "internal_error",    # 5xx
    "network_error"
}

NON_RETRYABLE_ERRORS = {
    "invalid_argument",  # 参数错（模型问题，重试也错）
    "not_found",         # 资源不存在
    "permission_denied", # 权限错
    "validation_failed"
}

# 重试只在循环外层做，不要在工具内 retry
async def call_tool_with_retry(handler, args, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await handler(**args)
        except RateLimitError as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(e.retry_after or 2 ** attempt)
                continue
            raise
        except (TimeoutError, NetworkError) as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
                continue
            raise
```

## 3. 循环防御：防止无限调用

### 死循环的常见场景

```python
# 场景 1: 工具一直失败，模型一直 retry
LLM → "调 search_db" → 失败 → "再调 search_db" → 失败 → ...

# 场景 2: 模型理解错了，反复用错误参数调用
LLM → "调 get_weather('TBD')" → 错 → "调 get_weather('TBD')" → ...

# 场景 3: 工具返回需要再次调用其他工具
LLM → A → 返回需要 B → 调 B → 返回需要 A → ...
```

### 必加：max_iterations 上限

```python
async def chat_with_tools(user_msg, tools, handlers, max_iterations=10):
    messages = [{"role": "user", "content": user_msg}]

    for iteration in range(max_iterations):
        resp = await client.messages.create(...)
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason != "tool_use":
            return extract_text(resp)

        # 执行工具
        results = await execute_tools_parallel(...)
        messages.append({"role": "user", "content": results})

    # 触发上限 → 强制让模型给一个总结
    messages.append({
        "role": "user",
        "content": "已达到最大调用次数。请基于当前信息给出最终回答，不要再调用工具。"
    })
    final = await client.messages.create(
        messages=messages,
        tool_choice={"type": "none"}  # 强制不调用
    )
    return extract_text(final)
```

### 进阶：去重检测

```python
from collections import Counter

def detect_loop(messages, threshold=3):
    """检测重复调用同样的工具+参数"""
    tool_signatures = []
    for msg in messages:
        if msg["role"] == "assistant":
            for block in msg["content"]:
                if hasattr(block, "type") and block.type == "tool_use":
                    sig = f"{block.name}({json.dumps(block.input, sort_keys=True)})"
                    tool_signatures.append(sig)

    if Counter(tool_signatures).most_common(1)[0][1] >= threshold:
        return True  # 检测到循环
    return False

# 在循环中检查
if detect_loop(messages):
    raise LoopDetectedError("模型陷入工具调用循环")
```

## 4. 超时控制

每个工具都该有超时：

```python
async def call_with_timeout(handler, args, timeout=30):
    try:
        return await asyncio.wait_for(handler(**args), timeout=timeout)
    except asyncio.TimeoutError:
        return {"error": "timeout", "message": f"工具调用超过 {timeout}s"}
```

不同工具的合理超时参考：

| 工具类型 | 超时 |
|---------|-----|
| 内部数据库查询 | 5–10s |
| 外部 API（同区域）| 10–20s |
| 跨国 API（如 OpenAI） | 30–60s |
| 大文件处理 / Embedding | 60–120s |
| 长流程（写文档）| 300s+ |

## 5. 完整生产级模板

集大成版本：

```python
import asyncio
import json
import time
from typing import Callable, Any

class ToolExecutor:
    def __init__(self, tools: list, handlers: dict[str, Callable],
                 max_iterations: int = 10, timeout: int = 30):
        self.tools = tools
        self.handlers = handlers
        self.max_iterations = max_iterations
        self.timeout = timeout

    async def _execute_one(self, name, args, tool_use_id):
        try:
            handler = self.handlers[name]
            coro = handler(**args) if asyncio.iscoroutinefunction(handler) \
                   else asyncio.to_thread(handler, **args)
            result = await asyncio.wait_for(coro, timeout=self.timeout)
            return {
                "type": "tool_result",
                "tool_use_id": tool_use_id,
                "content": json.dumps(result, ensure_ascii=False)
            }
        except asyncio.TimeoutError:
            return {
                "type": "tool_result", "tool_use_id": tool_use_id,
                "content": json.dumps({"error": "timeout"}),
                "is_error": True
            }
        except Exception as e:
            return {
                "type": "tool_result", "tool_use_id": tool_use_id,
                "content": json.dumps({"error": type(e).__name__, "message": str(e)}),
                "is_error": True
            }

    async def chat(self, user_message: str) -> str:
        messages = [{"role": "user", "content": user_message}]
        seen_calls = []

        for i in range(self.max_iterations):
            resp = await client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=2048,
                tools=self.tools,
                messages=messages
            )
            messages.append({"role": "assistant", "content": resp.content})

            if resp.stop_reason != "tool_use":
                return "\n".join(b.text for b in resp.content if b.type == "text")

            # 循环检测
            tool_uses = [b for b in resp.content if b.type == "tool_use"]
            for tu in tool_uses:
                sig = f"{tu.name}:{json.dumps(tu.input, sort_keys=True)}"
                seen_calls.append(sig)

            if seen_calls.count(seen_calls[-1]) >= 3:
                raise RuntimeError(f"Loop detected: {seen_calls[-1]}")

            # 并行执行
            tool_results = await asyncio.gather(*[
                self._execute_one(tu.name, tu.input, tu.id) for tu in tool_uses
            ])
            messages.append({"role": "user", "content": tool_results})

        # 兜底
        return "已达到调用上限，请简化问题或拆解为多步"
```

## 总结：生产 FC 检查清单

```
☐ 并行工具调用（asyncio.gather）
☐ 错误返回模型而非抛异常（is_error 字段）
☐ 区分可重试 / 不可重试错误
☐ 每个工具有超时
☐ max_iterations 上限 + 兜底回复
☐ 循环检测（同参重复调用 ≥3 次报警）
☐ Trace 接入（Langfuse / Phoenix）
☐ 工具调用打点（成功率、延迟分布）
```

下一节：[Structured Outputs](#structured-outputs) —— 让普通 LLM 调用也能返回严格 JSON。
