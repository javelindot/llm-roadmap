---
group: 4. MCP 协议
id: mcp-server
title: MCP · 编写 Server
toc: MCP · Server
---

用 Python 写一个真实可跑的 MCP Server，**接入 Claude Desktop 验证**。这章是 MCP 学习中最实操的一节。

## 开发环境

```bash
# 用官方 SDK
uv add mcp[cli]

# 验证
python -c "import mcp; print(mcp.__version__)"  # ≥ 1.0.0
```

## 最小可跑 Server（30 行）

`server.py`：

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types
import asyncio

# 创建 Server
server = Server("my-first-mcp")

# 定义一个工具
@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="add",
            description="计算两个数的和",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        )
    ]

# 工具执行处理器
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "add":
        result = arguments["a"] + arguments["b"]
        return [types.TextContent(type="text", text=f"结果：{result}")]
    raise ValueError(f"Unknown tool: {name}")

# 主循环（stdio transport）
async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

### 接入 Claude Desktop

编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`：

```json
{
    "mcpServers": {
        "my-first": {
            "command": "uv",
            "args": ["run", "python", "/abs/path/to/server.py"]
        }
    }
}
```

重启 Claude Desktop → 在对话里问「2 加 3 等于几？」→ Claude 会调用 `add` 工具。

## 添加 Resources

资源 = 模型可读取的数据。

```python
from mcp.server import Server
import mcp.types as types
import json
from pathlib import Path

server = Server("notes-mcp")

# 模拟笔记数据
NOTES_DIR = Path.home() / "Documents" / "Notes"

@server.list_resources()
async def list_resources() -> list[types.Resource]:
    """列出所有笔记"""
    return [
        types.Resource(
            uri=f"notes://{file.stem}",
            name=file.stem,
            description=f"Note: {file.stem}",
            mimeType="text/markdown"
        )
        for file in NOTES_DIR.glob("*.md")
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    """读取笔记内容"""
    # uri 形如 "notes://my-note"
    name = uri.replace("notes://", "")
    file = NOTES_DIR / f"{name}.md"
    if not file.exists():
        raise FileNotFoundError(uri)
    return file.read_text(encoding="utf-8")
```

模型可以：
- 通过 `resources/list` 看到所有笔记
- 通过 `resources/read` 读取特定笔记内容
- 在对话中："我有哪些笔记？" → "读一下'2024 计划'那篇"

## 添加 Prompts

Prompts = 预定义的提示词模板。

```python
@server.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="summarize_note",
            description="总结一篇笔记",
            arguments=[
                types.PromptArgument(
                    name="note_name",
                    description="笔记名（不含 .md）",
                    required=True
                )
            ]
        )
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict) -> types.GetPromptResult:
    if name == "summarize_note":
        note_name = arguments["note_name"]
        content = (NOTES_DIR / f"{note_name}.md").read_text()
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"请用 3 句话总结以下笔记：\n\n{content}"
                    )
                )
            ]
        )
```

在 Claude Desktop 里，用户可以点击 prompt 模板，填入参数后自动生成对话。

## 实战 Server：GitHub Issue 助手

一个真实有用的 Server —— 帮你管理 GitHub Issues。

```python
import os
import asyncio
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

server = Server("github-issues")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}

@server.list_tools()
async def list_tools():
    return [
        types.Tool(
            name="list_issues",
            description="列出仓库的 open issues",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {"type": "string", "description": "owner/repo"},
                    "labels": {"type": "array", "items": {"type": "string"}, "description": "按标签筛选（可选）"}
                },
                "required": ["repo"]
            }
        ),
        types.Tool(
            name="create_issue",
            description="创建新 issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {"type": "string"},
                    "title": {"type": "string"},
                    "body": {"type": "string"},
                    "labels": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["repo", "title"]
            }
        ),
        types.Tool(
            name="add_comment",
            description="给 issue 添加评论",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {"type": "string"},
                    "issue_number": {"type": "integer"},
                    "comment": {"type": "string"}
                },
                "required": ["repo", "issue_number", "comment"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    async with httpx.AsyncClient(headers=HEADERS) as client:
        if name == "list_issues":
            params = {"state": "open"}
            if arguments.get("labels"):
                params["labels"] = ",".join(arguments["labels"])

            resp = await client.get(
                f"https://api.github.com/repos/{arguments['repo']}/issues",
                params=params
            )
            issues = resp.json()
            text = "\n".join([
                f"#{i['number']}: {i['title']} (by {i['user']['login']})"
                for i in issues[:20]
            ])
            return [types.TextContent(type="text", text=text or "No open issues")]

        elif name == "create_issue":
            body = {
                "title": arguments["title"],
                "body": arguments.get("body", ""),
                "labels": arguments.get("labels", [])
            }
            resp = await client.post(
                f"https://api.github.com/repos/{arguments['repo']}/issues",
                json=body
            )
            if resp.status_code == 201:
                issue = resp.json()
                return [types.TextContent(
                    type="text",
                    text=f"✅ Created issue #{issue['number']}: {issue['html_url']}"
                )]
            return [types.TextContent(type="text", text=f"❌ Failed: {resp.text}")]

        elif name == "add_comment":
            resp = await client.post(
                f"https://api.github.com/repos/{arguments['repo']}/issues/{arguments['issue_number']}/comments",
                json={"body": arguments["comment"]}
            )
            return [types.TextContent(
                type="text",
                text="✅ Comment added" if resp.status_code == 201 else f"❌ {resp.text}"
            )]

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

接入 Claude Desktop：

```json
{
    "mcpServers": {
        "github": {
            "command": "uv",
            "args": ["run", "python", "/path/to/github_server.py"],
            "env": {"GITHUB_TOKEN": "ghp_xxx"}
        }
    }
}
```

试试：「列出 my-org/my-repo 的所有 bug 标签的 issue」「给 issue #42 加个 'urgent' 标签的备注」。

## 进阶：错误处理

工具失败时**不要抛异常**，而是返回 `isError`：

```python
@server.call_tool()
async def call_tool(name, arguments):
    try:
        result = await do_work(arguments)
        return [types.TextContent(type="text", text=result)]
    except ValidationError as e:
        # 参数错误 → 模型可能改正后重试
        return [types.TextContent(
            type="text",
            text=f"❌ 参数错误：{e}"
        )]
    except APIError as e:
        # 外部 API 错误 → 模型可能告知用户
        return [types.TextContent(
            type="text",
            text=f"❌ API 调用失败：{e.status_code} {e.message}"
        )]
```

错误信息让模型「**可读、可决策**」，例如：「请检查参数后重试」、「服务器暂不可用，稍后再试」。

## 进阶：参数验证（Pydantic）

```python
from pydantic import BaseModel, Field, ValidationError

class CreateIssueArgs(BaseModel):
    repo: str = Field(pattern=r"^[\w-]+/[\w-]+$", description="owner/repo")
    title: str = Field(min_length=1, max_length=200)
    body: str | None = None
    labels: list[str] = Field(default_factory=list, max_length=10)

@server.call_tool()
async def call_tool(name, arguments):
    if name == "create_issue":
        try:
            args = CreateIssueArgs(**arguments)
        except ValidationError as e:
            return [types.TextContent(type="text", text=f"参数错误: {e}")]
        # ... 用 args.repo, args.title 等
```

Pydantic 给你**自动校验 + 类型转换**，比手动检查可靠多了。

## 进阶：日志输出

stdio transport 下**绝对不能用 `print()`** —— 会把 stdout 当成 MCP 消息发出去把 Client 搞崩。

正确做法：用 logging + stderr。

```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,  # 关键：用 stderr 不是 stdout
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger("github-mcp")

@server.call_tool()
async def call_tool(name, arguments):
    log.info(f"Tool called: {name}")  # 安全
    # print(...)  # ❌ 绝对禁止
```

Claude Desktop 会把 Server 的 stderr 日志显示在「Developer」面板里。

## 进阶：sampling（让 Client 帮忙调 LLM）

Server 不需要自己的 API key，可以**反向请求 Client 调 LLM**：

```python
@server.call_tool()
async def call_tool(name, arguments):
    if name == "summarize_repo":
        readme = fetch_readme(arguments["repo"])
        
        # 让 Client 调 LLM 做摘要
        result = await server.request_context.session.create_message(
            messages=[{
                "role": "user",
                "content": {"type": "text", "text": f"用 3 句话总结：\n{readme}"}
            }],
            max_tokens=300
        )
        summary = result.content.text
        return [types.TextContent(type="text", text=summary)]
```

注意：sampling 需要 Client 支持（Claude Desktop 支持，部分 Client 不支持）。

## Server 编写最佳实践

```
☐ 用 Pydantic 校验参数
☐ 工具失败返回 error message，不要抛异常
☐ 日志用 stderr 不要用 stdout
☐ 工具描述写清楚（模型靠它判断）
☐ inputSchema 用 enum / pattern / minLength 等约束
☐ 异步操作用 httpx.AsyncClient，不要用 requests
☐ 敏感参数（API key）从 env 读，不硬编码
☐ 长时间操作发送 progress 通知
☐ 编写 README 说明用法 + 配置
```

## 调试技巧

### 方法 1: MCP Inspector

官方调试工具：

```bash
npx @modelcontextprotocol/inspector uv run python server.py
# 浏览器打开 http://localhost:5173
# 可以可视化测试 tools / resources / prompts
```

### 方法 2: 用 Python Client 直接连

```python
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
import asyncio

async def test():
    params = StdioServerParameters(
        command="python", args=["server.py"]
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("Tools:", tools)
            result = await session.call_tool("add", {"a": 2, "b": 3})
            print("Result:", result)

asyncio.run(test())
```

### 方法 3: Claude Desktop 开发者面板

`Settings → Developer → MCP Servers` 可以看到：
- Server 启动日志
- 实时消息流
- 错误信息

## 发布与分享

写好 Server 想分享？

### 方式 1: PyPI 包

```python
# pyproject.toml
[project]
name = "mcp-server-mything"
[project.scripts]
mcp-server-mything = "mcp_server_mything:main"
```

用户安装 + 配置：
```bash
pip install mcp-server-mything
```
```json
{"mcpServers": {"mything": {"command": "mcp-server-mything"}}}
```

### 方式 2: npm 包（用 uvx 调）

如果是 TypeScript 实现，发到 npm，用户用 `npx` 调：
```json
{"mcpServers": {"x": {"command": "npx", "args": ["-y", "mcp-server-x"]}}}
```

### 方式 3: 提交到 awesome-mcp-servers

让你的 Server 进入社区列表：
[github.com/punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)

下一节：[Client 集成与生态](#mcp-client) —— 怎么在自己的应用里集成 MCP。
