---
group: 2. Function Call
id: parallel-errors
title: Function Call · 并行调用与错误处理
toc: FC · 并行+错误
---

模型一次提出多个工具请求，与应用并行执行是两件事。调度需要先验证调用身份、授权、参数和依赖，不能把所有工具直接放进 gather。

## 可并行的边界

独立的只读查询可以在限制下并行。查询后提交工单有依赖，必须等待；对同一资源的写操作由业务执行器协调和去重。

理想情况下等待时间从各工具耗时之和降低到最大耗时，但真实收益受并发上限、速率限制、连接池和聚合处理影响。模型调用次数与工具数没有固定对应关系。

## 可运行的只读执行器

仓库 [execute_readonly_calls](../examples/core_patterns.py)先检查重复调用 ID、工具注册与 allowlist，再校验参数，并用 semaphore 和 timeout 控制异步执行。返回结果保留输入调用 ID 与顺序。

在 app-dev/examples 目录运行以下代码，无需模型账户：

```python
import asyncio
from core_patterns import Tool, execute_readonly_calls


def validate_order(arguments):
    """验证候选参数；身份应由外层可信会话提供。

    只接受确定的订单字段，防止任意参数进入处理器。
    真实服务还需对象级授权，不接受模型自填租户作为身份。
    """
    if set(arguments) != {"order_id"} or not isinstance(arguments["order_id"], str):
        raise ValueError("invalid_order")


async def read_order(order_id):
    """返回只读模拟数据，未知订单明确说明不存在。

    本例不连接业务服务，也不证明真实用户已获订单访问权。
    生产处理器应复核可信身份、对象、新鲜度和数据来源。
    """
    if order_id != "demo-order":
        return {"status": "not_found"}
    return {"order_id": order_id, "status": "pending", "source": "demo"}


registry = {"read_order": Tool(read_order, validate_order, read_only=True)}
calls = [{"id": "call-1", "name": "read_order", "arguments": {"order_id": "demo-order"}}]
results = asyncio.run(execute_readonly_calls(calls, registry, {"read_order"},
                                            concurrency=2, timeout=1))
print(results)
```

结果需要由 API 适配层转为 Responses 的 function_call_output 或 Claude 的 tool_result。不要用数组位置替代协议关联 ID。

## 错误分类

| 类型 | 动作 | 是否重试 |
|------|------|----------|
| 未授权或未知工具 | 拒绝并记录稳定原因 | 不通过模型重试绕过 |
| 非法参数 | 返回有限错误信息，允许有限纠正 | 受轮数与总预算约束 |
| 只读临时故障 | 按状态重试或降级 | 退避、抖动及总时限内 |
| 业务拒绝 | 展示可解释结果或走合法替代路径 | 不盲目重复 |
| 写请求结果未知 | 查询同一业务动作回执 | 确认后决定，不能当未执行 |
| 确定不可恢复错误 | 停止并保存状态 | 转人工或明确失败 |

内部异常只在脱敏日志中记录，对模型返回稳定错误代码。原始 HTTP 错误可能包含凭证、路径或客户数据，不能直接 str(exception) 后回传。

## 超时与取消

协程 timeout 可以停止本地等待，但不能保证远程服务或线程中的操作停止。取消后核对已发生副作用，运行状态、动作账本和业务补偿分别记录。

未知写结果不会因为 SDK 自动重试或模型路由而变安全。模型重试预算、工具重试预算和 Case 总预算应统一控制，避免相乘放大请求量。

## 循环控制

设置总轮数、工具调用数、总时间、费用和并发上限。检测相同意图重复调用、没有新增信息的反思与无效查询；对确有时间变化的查询考虑新鲜度后判断。

预算耗尽保留已发生动作和可信状态，明确停止原因。不要通过截断历史把尚未核对的动作回执删掉。

## 验收

```bash
python -m unittest discover -s app-dev/examples -v
```

现有测试覆盖未授权与写工具拦截、非法参数、重复 ID、超时、并发上限和结果关联。业务账本进一步验证写动作未知结果，见[Harness](607-agent-harness.html)。

下一节：[Structured Outputs](204-structured-outputs.html)。
