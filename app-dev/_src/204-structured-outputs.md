---
group: 2. Function Call
id: structured-outputs
title: Function Call · Structured Outputs
toc: FC · Structured Outputs
---

结构化输出把支持范围内的模型结果约束到 JSON Schema。结构符合契约、内容符合事实和动作被授权，是三个不同的验收条件。

## 选择机制

| 机制 | 目标 | 仍需检查 |
|------|------|----------|
| Prompt 要求 JSON | 影响格式 | 解析、schema 与语义 |
| JSON 模式 | 合法 JSON | 字段、类型和业务语义 |
| Structured Outputs | 支持的 schema 契约 | 拒绝、不完整输出、事实与权限 |
| Strict Function Call | 工具参数结构契约 | 允许的工具、资源与参数语义 |

提取或分类使用结构化结果；请求外部动作使用工具。JSON 中出现退款指令不能直接触发退款。

## Responses 与 Pydantic

安装 openai、pydantic，设置 OPENAI_API_KEY、LLM_MODEL，并选择已验收支持该接口的模型。本例未在认证环境实测。

```python
import os
from openai import OpenAI
from pydantic import BaseModel, ConfigDict


class PersonInfo(BaseModel):
    """定义提取结果，用必填可空字段表达缺失语义。

    禁止额外字段，业务范围在接收后另行检查。
    此结构不证明信息真实，应与输入证据核对。
    """
    model_config = ConfigDict(extra="forbid")
    name: str
    age: int
    occupation: str | None


client = OpenAI(timeout=20, max_retries=0)
response = client.responses.parse(
    model=os.environ["LLM_MODEL"],
    input=[{"role": "user", "content": "张三 30 岁，是工程师。请提取信息。"}],
    text_format=PersonInfo,
)
if response.status != "completed":
    raise RuntimeError("incomplete_output")
refusals = [part for item in response.output if item.type == "message"
            for part in item.content if part.type == "refusal"]
if refusals:
    raise RuntimeError("model_refused")
person = response.output_parsed
if person is None:
    raise RuntimeError("missing_parsed_result")
# 类型检查通过后仍验证业务范围，不能直接写入数据库。
if not person.name.strip() or not 0 <= person.age <= 130:
    raise ValueError("invalid_person_semantics")
print(person.model_dump())
```

Pydantic 是第三方库，不是 Python 标准库。其通用 schema 不一定符合供应商支持的全部子集；使用固定 SDK 的转换能力，检查是否丢失了业务约束。

## schema 设计

对象要有明确 properties、required 和额外字段规则。OpenAI 严格对象 schema 要求属性列为 required、additionalProperties=false；可缺失语义用 null，不能只漏掉字段。

不要泛称“anyOf 完全不支持”。根对象、嵌套组合、深度与字段数等限制按当前官方子集核对，不能固化旧阈值。首次 schema 处理开销也取决于模型与接口。

动态字典、日期、金额和复杂验证可拆成供应商支持的结构，配合独立校验。身份和租户不接受模型自填作为可信值；金额须有币种与精度。

## 供应商接口边界

OpenAI Responses 使用 text.format 或 SDK 的 text_format，Chat Completions 使用 response_format，不能互换。Claude 当前也提供结构化输出和严格工具调用，字段与支持模型按其接口确认。

内容可能包含文本、工具、拒绝或其他块，不能假定 content[0] 必然是目标对象。工具结果必须按类型与 ID 关联。

## 流式与失败

部分 JSON 可显示生成进度，不能作为确定业务动作。等待完整输出、正确结束状态和独立校验，再进入预览与审批。

超时、截断、拒绝、schema 不支持、解析失败和语义无效分别记录。格式失败可有限重试，证据缺失应补问，业务拒绝不能通过重生成绕过。

## 验收

覆盖可空值、额外字段、枚举、拒绝、截断、语义错误与恶意输入。分开统计结构成功、事实支持和业务有效性，不用格式成功率替代任务成功率。

参考：[OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)、[Claude Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)。下一节：[能力契约与路由](205-model-routing.html)。
