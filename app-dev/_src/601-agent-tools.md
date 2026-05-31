---
group: 6. AI Agent
id: agent-tools
title: Agent · 工具调用与 MCP 集成
toc: Agent · 工具调用
---

**工具调用是 Agent 的「双手」**。没有工具，Agent 只能聊天；有了工具，它能查天气、调 API、改数据库、发邮件、甚至操控浏览器。

前面 Module 2（Function Call）和 Module 4（MCP）已经分别讲了「怎么让模型调工具」和「怎么标准化工具对接」。这一节把它们**串进 Agent 的完整工作流**里。

## Agent 里的工具调用链路

```
用户提问
   ↓
[ Agent 大脑 ] LLM 判断是否需要工具
   ↓
是 → 输出 tool_call（name + arguments）
   ↓
[ 工具执行层 ] 安全校验 → 执行 → 拿到结果
   ↓
结果回传给 LLM
   ↓
LLM 生成最终回答（或继续下一轮工具调用）
```

和单纯的 Function Call  demo 不同，Agent 里的工具调用要处理**多轮、错误、超时、权限**等生产问题。

## 三类常用工具

| 类型 | 典型工具 | Agent 用它们做什么 |
|------|----------|-------------------|
| **信息检索** | 搜索引擎、RAG 知识库、数据库查询 | 回答实时/私域问题 |
| **代码执行** | Python 解释器、Bash、Jupyter | 做计算、跑脚本、画图 |
| **外部 API** | 邮件、日历、GitHub、Slack、CRM | 执行操作、触发工作流 |

## 从 Function Call 升级到 Agent 工具层

### 1. 工具注册表（Tool Registry）

```python
class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name: str, schema: dict, handler: callable):
        """注册一个工具：JSON Schema + 执行函数"""
        self._tools[name] = {"schema": schema, "handler": handler}

    def get_schemas(self) -> list:
        """返回给 LLM 的所有工具描述"""
        return [
            {"type": "function", "function": {"name": n, **t["schema"]}}
            for n, t in self._tools.items()
        ]

    async def execute(self, name: str, arguments: dict) -> str:
        """执行工具 + 统一错误处理"""
        if name not in self._tools:
            raise ValueError(f"未知工具: {name}")
        handler = self._tools[name]["handler"]
        try:
            result = await handler(**arguments)
            return json.dumps({"status": "ok", "result": result}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False)
```

### 2. 多轮工具调用循环

```python
async def agent_loop(user_input: str, registry: ToolRegistry, max_steps=10):
    messages = [{"role": "user", "content": user_input}]
    tools = registry.get_schemas()

    for step in range(max_steps):
        response = await llm.chat(messages, tools=tools)
        msg = response.choices[0].message

        # 模型选择不调用工具 → 直接返回答案
        if not msg.tool_calls:
            return msg.content

        # 执行所有 tool_calls（支持并行）
        messages.append({"role": "assistant", "content": msg.content, "tool_calls": msg.tool_calls})
        for tc in msg.tool_calls:
            result = await registry.execute(tc.function.name, json.loads(tc.function.arguments))
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result
            })

    raise RuntimeError("超过最大步数，可能陷入循环")
```

## 接入 MCP：让 Agent 即插即用

Agent 写死工具 = 每次加功能都要改代码。用 MCP 解耦：

```
┌─────────────┐      MCP 协议       ┌─────────────┐
│   Agent     │ ←────────────────→ │ MCP Server  │
│  (Client)   │   stdio / SSE      │  (工具提供者) │
└─────────────┘                    └─────────────┘
        ↓                               ↓
   统一调用接口                    GitHub / DB / 浏览器
```

接入方式（以 `mcp` Python SDK 为例）：

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 启动一个 MCP Server（如文件系统工具）
server_params = StdioServerParameters(
    command="npx", args=["-y", "@modelcontextprotocol/server-filesystem", "/data"]
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        # 获取 Server 提供的所有工具
        tools = await session.list_tools()
        # 直接调用
        result = await session.call_tool("read_file", {"path": "/data/report.md"})
```

**关键收益**：Agent 开发者不用关心 GitHub API 怎么调、Postgres 怎么连，MCP Server 已经封装好了。

## 生产级注意事项

| 问题 | 解决方案 |
|------|----------|
| **工具调用无限循环** | 设置 `max_steps`；给模型加上「如果无法完成请直接告诉用户」的提示 |
| **敏感操作误触发** | 关键工具（写库、发邮件）加人工确认或二次 LLM 审核 |
| **超时与重试** | 工具执行层加 timeout + 指数退避重试 |
| **错误信息暴露** | 不要把原始异常堆栈直接给 LLM，包装成友好的 JSON |
| **成本爆炸** | 监控每轮调用的 token 消耗；对长循环设预算上限 |

:::callout 🔗
**把前面学的串起来**：Agent 的「工具层」= Function Call（决策机制）+ MCP（标准化对接）+ Registry（统一管理）+ 循环（多轮执行）。
:::
