---
group: 2. Function Call
id: structured-outputs
title: Function Call · Structured Outputs
toc: FC · Structured Outputs
---

**Structured Outputs**（结构化输出）让模型**100% 按 JSON Schema 输出** —— 不是 prompt 里求模型「请输出 JSON」那种祈祷式编程，而是 API 层面**保证**。

## 为什么需要 Structured Outputs

经典痛点：

```python
# 旧时代：在 prompt 里求 JSON
prompt = """请返回 JSON 格式: {"name": str, "age": int}
用户描述: 张三 30 岁"""

# 模型可能返回:
# ✅ {"name": "张三", "age": 30}              ← 完美
# ⚠️ ```json\n{"name": "张三", "age": 30}\n``` ← 多了 markdown
# ⚠️ {'name': '张三', 'age': 30}              ← 单引号 → json 解析失败
# ⚠️ {"name": "张三", "age": "30"}            ← 类型错
# ❌ {"姓名": "张三", "年龄": 30}              ← key 翻译了
# ❌ 这是张三的信息：{"name": "张三"...        ← 加废话
```

业界统计：纯 prompt 求 JSON，**失败率 5%–15%**。生产环境不可接受。

## OpenAI Structured Outputs

OpenAI 2024 推出，**100% 保证符合 schema**。

### 方式 1: response_format

```python
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class PersonInfo(BaseModel):
    name: str
    age: int
    occupation: str | None = None

resp = client.beta.chat.completions.parse(
    model="gpt-5",
    messages=[{"role":"user", "content":"张三 30 岁，是个工程师"}],
    response_format=PersonInfo  # 直接传 Pydantic 模型
)

person = resp.choices[0].message.parsed  # 直接是 PersonInfo 对象
print(person.name)         # "张三"
print(person.age)          # 30
print(person.occupation)   # "工程师"
```

### 方式 2: tools + strict

```python
tools = [{
    "type": "function",
    "function": {
        "name": "extract_person",
        "description": "从文本提取人物信息",
        "parameters": PersonInfo.model_json_schema(),
        "strict": True  # ← 关键
    }
}]
```

启用 `strict: True` 后，模型**绝对不会**返回不符合 schema 的内容。

## Anthropic：用 Tool 模拟

Claude 没有专门的 `response_format`，但用 **Tool Use** 可以达到同样效果：

```python
from anthropic import Anthropic
client = Anthropic()

tools = [{
    "name": "extract_person",
    "description": "提取人物信息",
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "occupation": {"type": "string"}
        },
        "required": ["name", "age"]
    }
}]

resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "tool", "name": "extract_person"},  # 强制调
    messages=[{"role":"user", "content":"张三 30 岁，是个工程师"}]
)

# 不需要真的执行工具 —— 直接拿模型输出的 input 作为结构化结果
person = resp.content[0].input
print(person)  # {"name": "张三", "age": 30, "occupation": "工程师"}
```

Claude 4.5 的 Tool Use schema 遵守率 **>99%**，实战中可以认为是 100%。

## Pydantic 加持

Pydantic 是 Python 的 schema 标准库。用它定义 → 自动生成 JSON Schema → 验证输出。

```python
from pydantic import BaseModel, Field
from typing import Literal
from datetime import date

class OrderQuery(BaseModel):
    """订单查询参数"""
    user_id: str = Field(description="用户 ID，必填")
    status: Literal["pending", "paid", "shipped", "refunded"] | None = None
    date_from: date | None = Field(default=None, description="起始日期 YYYY-MM-DD")
    limit: int = Field(default=20, ge=1, le=100, description="返回数量 1-100")

# Pydantic 自动生成 JSON Schema
schema = OrderQuery.model_json_schema()
# {
#   "type": "object",
#   "properties": {
#     "user_id": {"type": "string", "description": "..."},
#     "status": {"enum": ["pending","paid","shipped","refunded"], ...},
#     ...
#   },
#   "required": ["user_id"]
# }
```

**Pydantic 的好处**：
- 类型注解 = 自动 schema
- `Field(description=...)` 让模型理解每个字段
- `Literal[...]` 限定枚举值
- `ge` / `le` 加范围约束
- 输出后自动验证 + 类型转换

## 实战场景

### 场景 1：信息提取

从非结构化文本提取结构化数据。

```python
class JobPosting(BaseModel):
    title: str = Field(description="职位名")
    company: str
    location: str
    salary_min: int | None = Field(default=None, description="月薪下限（人民币元）")
    salary_max: int | None = None
    requirements: list[str] = Field(description="技能要求列表")
    experience_years: int = Field(description="所需经验年数")

# 从招聘文本提取
job_text = "..."  # 一段招聘 JD
result = extract_with_schema(job_text, JobPosting)
# 直接入库
db.insert_job(result.model_dump())
```

### 场景 2：分类 + 路由

```python
class Intent(BaseModel):
    category: Literal["咨询", "投诉", "退款", "物流", "其他"]
    confidence: float = Field(ge=0, le=1)
    urgency: Literal["low", "medium", "high"]
    summary: str = Field(max_length=100)

# 客服消息路由
intent = classify_intent(user_message, Intent)
if intent.urgency == "high":
    route_to_human(intent)
elif intent.category == "退款":
    handle_refund(intent)
```

### 场景 3：复杂嵌套结构

```python
class Address(BaseModel):
    province: str
    city: str
    street: str
    postal_code: str | None = None

class Person(BaseModel):
    name: str
    age: int
    addresses: list[Address]  # 嵌套
    contact: dict[str, str]   # email/phone

# 模型可以输出复杂嵌套
result = extract(text, Person)
print(result.addresses[0].city)
```

## 流式输出 Structured Outputs

边生成边解析：

```python
# OpenAI 流式
with client.beta.chat.completions.stream(
    model="gpt-5",
    messages=[...],
    response_format=PersonInfo
) as stream:
    for event in stream:
        if event.type == "content.delta":
            print(event.parsed, end="\r")  # 实时显示部分解析结果
    final = stream.get_final_completion().choices[0].message.parsed
```

## Pydantic Schema 设计技巧

### 1. 详尽的 description

```python
# ❌ 模糊
class Order(BaseModel):
    status: str

# ✅ 明确
class Order(BaseModel):
    status: Literal["pending", "paid", "shipped", "refunded"] = Field(
        description="订单状态: pending=待支付, paid=已支付, shipped=已发货, refunded=已退款"
    )
```

### 2. 用 Literal 而非 str

```python
# ❌ 容易乱传
priority: str  # 模型可能输出 "高"/"high"/"High"/"P0"/"urgent"

# ✅ 限定
priority: Literal["P0", "P1", "P2", "P3"]
```

### 3. 嵌套结构有层次

```python
class Recipe(BaseModel):
    name: str
    servings: int
    ingredients: list[Ingredient]  # 嵌套类
    steps: list[str] = Field(description="按顺序列出步骤")
    cooking_time_minutes: int = Field(ge=1, le=600)
```

### 4. 可选字段用 None 默认

```python
class Customer(BaseModel):
    name: str
    email: str
    phone: str | None = None  # 可能缺失
    notes: str | None = None
```

## 限制与注意

:::callout ⚠️
**限制 1**：response_format 的 schema 不能太深（OpenAI 限 5 层嵌套）
**限制 2**：strict 模式不支持 `oneOf` / `anyOf`（Pydantic 的 Union）
**限制 3**：strict 模式所有字段都必须 `required`，可选字段要用 `T | None`
**限制 4**：首次启用 strict 会延迟（schema 预编译），后续正常
:::

## Function Call vs Structured Outputs 何时用什么

| 场景 | 推荐 |
|------|------|
| 真的要执行外部工具 | **Function Call**（多个工具，模型选） |
| 只想要结构化输出，不执行 | **Structured Outputs**（response_format） |
| 数据提取 / 分类 | **Structured Outputs** |
| 复杂 Agent | **Function Call**（多轮决策） |

## 总结

Structured Outputs = **类型安全的 LLM 输出**。

```
✅ 100% 符合 schema → 无需写 try/except 解析
✅ Pydantic 类型校验 → 直接进数据库 / 业务逻辑
✅ 字段缺失 / 类型错 → 模型自动修正
✅ 比纯 prompt 求 JSON 节省大量代码
```

下一模块：[RAG 检索增强](#rag-overview) —— 让模型读你的私域知识。
