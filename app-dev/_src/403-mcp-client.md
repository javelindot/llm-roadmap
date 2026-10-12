---
group: 4. MCP 协议
id: mcp-client
title: MCP · Client 集成与生态
toc: MCP · Client
---

本章保留连接级 ClientSession.initialize 等接入样例，不作为 2026-07-28 的实现证明。固定 SDK 与协议版本，按[版本差异](401-mcp-spec.html)和[授权契约](404-mcp-security.html)验收后使用；供应商 Connector 的 beta 参数单独核对。

## 三种集成方式

### 方式 1: 用现成客户端（最快）

直接用 Claude Desktop / Cursor / VSCode 等，配 `mcpServers` 即可。
**适合**：终端用户、个人使用。

### 方式 2: 用 Anthropic 官方 SDK（最简单）

```python
from anthropic import Anthropic
# 一句话集成 MCP
```

**适合**：基于 Anthropic API 开发 LLM 应用。

### 方式 3: 自己写 Client（最灵活）

直接用 MCP SDK 写 Client，可控制所有细节。
**适合**：自研 Agent 框架、特殊集成需求。

下面分别详解后两种。

## 集成方式 2: Anthropic SDK + MCP Connector

Anthropic 2025 推出的「**MCP Connector**」功能 —— 一行配置让 Claude API 直接使用 MCP Server。

```python
from anthropic import Anthropic
client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "列出仓库 octocat/hello 的所有 issue"}],
    mcp_servers=[
        {
            "type": "url",
            "url": "https://my-mcp.example.com",  # 远程 Server
            "name": "github",
            "authorization_token": "..."
        }
    ],
    betas=["mcp-client-2025-04-04"]
)
# Claude 会自动:
# 1. 连接 MCP Server
# 2. 列出可用 tools/resources
# 3. 决定要不要调
# 4. 调用并返回结果
print(response.content[0].text)
```

完全不用写 tool 处理循环。**适合快速搭建有「外部能力」的 LLM 应用**。

## 集成方式 3: 自己写 Client

直接用 MCP SDK，能控制每个细节。

### Python Client 示例

```python
import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

async def run_with_mcp(user_message: str):
    # 启动 Server
    params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={"GITHUB_TOKEN": "ghp_xxx"}
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化
            await session.initialize()

            # 列出工具
            tools_response = await session.list_tools()
            tools = tools_response.tools
            print(f"可用工具: {[t.name for t in tools]}")

            # 转换为 Anthropic FC 格式
            anthropic_tools = [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.inputSchema
                }
                for t in tools
            ]

            # 让 Claude 决策
            from anthropic import Anthropic
            client = Anthropic()
            resp = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=2048,
                tools=anthropic_tools,
                messages=[{"role": "user", "content": user_message}]
            )

            # 处理 tool_use
            for block in resp.content:
                if block.type == "tool_use":
                    # 调用 MCP Server
                    result = await session.call_tool(block.name, block.input)
                    print(f"工具 {block.name} 返回: {result.content[0].text}")

asyncio.run(run_with_mcp("给 octocat/hello 创建一个 bug issue"))
```

### TypeScript Client 示例

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({
    command: "npx",
    args: ["-y", "@modelcontextprotocol/server-github"]
});

const client = new Client({
    name: "my-client",
    version: "1.0.0"
}, {capabilities: {}});

await client.connect(transport);

const tools = await client.listTools();
console.log("Tools:", tools.tools);

const result = await client.callTool({
    name: "create_issue",
    arguments: {repo: "octocat/hello", title: "Bug"}
});
```

## 多 Server 集成（Agent 场景）

实战中通常会接**多个 Server**：

```python
async def multi_server_agent(user_msg):
    # 启动多个 MCP Servers
    server_configs = {
        "github": StdioServerParameters(command="npx", args=["-y", "@modelcontextprotocol/server-github"]),
        "filesystem": StdioServerParameters(command="npx", args=["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]),
        "postgres": StdioServerParameters(command="npx", args=["-y", "@modelcontextprotocol/server-postgres", "postgres://..."])
    }

    sessions = {}
    contexts = []  # 用于 cleanup

    for name, params in server_configs.items():
        ctx = stdio_client(params)
        read, write = await ctx.__aenter__()
        contexts.append((ctx, read, write))

        session = ClientSession(read, write)
        await session.__aenter__()
        await session.initialize()
        sessions[name] = session

    # 汇总所有工具
    all_tools = []
    tool_to_server = {}  # 记录每个 tool 属于哪个 server
    for name, session in sessions.items():
        tools_resp = await session.list_tools()
        for tool in tools_resp.tools:
            qualified_name = f"{name}__{tool.name}"  # 加前缀避免冲突
            all_tools.append({
                "name": qualified_name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            })
            tool_to_server[qualified_name] = (name, tool.name)

    # Agent 循环
    messages = [{"role": "user", "content": user_msg}]
    while True:
        resp = anthropic_client.messages.create(
            model="claude-sonnet-4-5",
            tools=all_tools,
            messages=messages
        )

        if resp.stop_reason != "tool_use":
            return [b.text for b in resp.content if b.type == "text"]

        # 路由到对应 server
        tool_results = []
        for block in resp.content:
            if block.type == "tool_use":
                server_name, orig_tool_name = tool_to_server[block.name]
                result = await sessions[server_name].call_tool(orig_tool_name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result.content[0].text
                })

        messages.append({"role": "assistant", "content": resp.content})
        messages.append({"role": "user", "content": tool_results})
```

**关键点**：用 `{server}__{tool}` 命名避免不同 Server 的同名工具冲突。

## 2026 主流客户端配置示例

### Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
`%APPDATA%/Claude/claude_desktop_config.json` (Windows)

```json
{
    "mcpServers": {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem",
                     "/Users/me/workspace"]
        },
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_TOKEN": "${GITHUB_TOKEN}"}
        },
        "postgres": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres",
                     "postgresql://localhost/mydb"]
        }
    }
}
```

### Cursor

`~/.cursor/mcp.json` (或 IDE 内 Settings → MCP):

```json
{
    "mcpServers": {
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"]
        }
    }
}
```

### VSCode (官方 MCP 扩展)

`Settings.json`:

```json
{
    "mcp.servers": {
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"]
        }
    }
}
```

### Continue.dev

`~/.continue/config.json`:

```json
{
    "mcpServers": [{
        "name": "github",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"]
    }]
}
```

## 安全考虑

MCP Server **能拿到模型的指令并执行真实操作**，安全很重要。

### 1. 沙盒化敏感 Server

```bash
# 给 filesystem MCP Server 限制目录
npx @modelcontextprotocol/server-filesystem /workspace  # 只能访问 /workspace
# 不要给 / 或 home 目录
```

### 2. 最小权限原则

- GitHub Token：只给必要 scope（如 `repo:read`，不给 `delete_repo`）
- 数据库：用只读账号，不给 DROP / DELETE 权限
- API Key：用 scoped key，限定特定资源

### 3. 命令注入防御

Server 收到的参数可能含恶意内容：

```python
# ❌ 危险
def run_shell(cmd: str):
    os.system(cmd)  # 模型可能传 "rm -rf /"

# ✅ 安全
def run_safe_cmd(cmd: str):
    ALLOWED = {"ls", "pwd", "echo"}
    parts = cmd.split()
    if parts[0] not in ALLOWED:
        raise ValueError(f"Command {parts[0]} not allowed")
    subprocess.run(parts, capture_output=True, check=True)
```

### 4. 用户确认（关键操作）

破坏性操作（删除 / 发送 / 支付）应**要求用户确认**：

```python
@server.call_tool()
async def call_tool(name, arguments):
    if name == "delete_repo":
        # 不能直接执行，先返回需要确认
        return [types.TextContent(
            type="text",
            text=f"⚠️ 即将删除仓库 {arguments['repo']}。请用户在客户端确认后再调用 confirm_delete_repo 工具。"
        )]
```

Claude Desktop 等客户端通常会**默认弹窗确认**所有 MCP 调用（用户可设置免确认列表）。

### 5. 速率限制

防止模型死循环触发 API 限流：

```python
from collections import defaultdict
import time

rate_limit = defaultdict(list)

@server.call_tool()
async def call_tool(name, arguments):
    now = time.time()
    # 同工具 1 分钟内最多 30 次
    rate_limit[name] = [t for t in rate_limit[name] if now - t < 60]
    if len(rate_limit[name]) >= 30:
        return [types.TextContent(type="text", text="Rate limit exceeded")]
    rate_limit[name].append(now)
    # ... 执行工具
```

## MCP 生态全景（2026）

### 官方 Server 速查

| 类别 | Server 名 | 用途 |
|------|----------|------|
| 文件 | `server-filesystem` | 本地文件读写 |
| 代码 | `server-github` / `server-gitlab` | 仓库操作 |
| 数据库 | `server-postgres` / `server-sqlite` | SQL 查询 |
| 沟通 | `server-slack` | Slack 消息 |
| 浏览 | `server-puppeteer` | 浏览器自动化 |
| 地图 | `server-google-maps` | 路线、地点 |
| 知识 | `server-memory` | 持久化知识图谱 |
| 搜索 | `server-brave-search` | Web 搜索 |
| 时间 | `server-time` | 时区、时间转换 |

完整列表：[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

### 热门社区 Server

| 类别 | Server | 提供方 |
|------|--------|--------|
| 云 | aws-mcp / cloudflare-mcp / gcp-mcp | 各家社区 |
| SaaS | linear-mcp / jira-mcp / notion-mcp / hubspot-mcp | 社区 |
| 数据仓库 | snowflake-mcp / bigquery-mcp | 社区 |
| 设计 | figma-mcp / canva-mcp | 官方 |
| 监控 | sentry-mcp / datadog-mcp | 官方 |
| 支付 | stripe-mcp | 官方 |

[awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) 列出 500+。

### 商业 MCP 平台

| 平台 | 定位 |
|------|------|
| **Cloudflare Agents** | Hosted MCP Servers，零运维 |
| **Stainless MCP Builder** | API → MCP 自动生成 |
| **Composio** | 200+ 集成的统一 MCP 网关 |
| **MCP Hub** | MCP Server 市场 |

## 实战架构：企业级 MCP 平台

中大型公司常见的部署模式：

```
┌────────────────────────────────────────┐
│   员工的 Claude / Cursor / 自研 AI 工具  │
└──────────────────┬─────────────────────┘
                   │ MCP (HTTPS)
                   ↓
┌────────────────────────────────────────┐
│       公司内部 MCP Gateway              │
│   - SSO 鉴权                            │
│   - 权限路由（按部门/角色）              │
│   - 日志审计                            │
│   - 限流                                │
└────┬─────────┬──────────┬──────────────┘
     ↓         ↓          ↓
  ┌──────┐  ┌──────┐  ┌──────────┐
  │CRM MCP│ │ DB MCP│ │ Slack MCP │
  └──────┘  └──────┘  └──────────┘
```

好处：
- 所有 AI 工具用同一套基础设施
- 中心化管理权限和审计
- 新业务只需加新 Server，所有 AI 应用立刻可用

## 学完 MCP 后能做什么

✅ 写一个 Server 让 Claude 直接操作你的内部系统
✅ 在团队内部建 MCP 工具库
✅ 接入开源 MCP Server，给 Agent 扩展能力
✅ 设计企业级 MCP 平台
✅ 评估 Function Call / MCP / Skills 的技术选型

## 接入验收：身份、生命周期与同名工具

MCP 接入需按服务保存连接与能力清单，模型侧工具别名映射到明确的 (server, tool) 二元组。两个服务都提供 search 时，不能用工具名作为唯一字典键，否则会静默覆盖。

本仓库 [mcp_aliases](../examples/core_patterns.py) 使用会话内短别名保留服务身份。别名表应跟随当次工具清单，不能把旧会话的 tool_0 当作稳定的全局工具标识。

| 验收项 | 检查方式 |
|--------|----------|
| 初始化 | 协议版本、能力协商、认证失败 |
| 工具发现 | 分页、同名、动态清单变化 |
| 调用 | 参数验证、业务权限、isError 与不同内容类型 |
| 连接 | 超时、断开、取消、清理子进程和会话 |
| 远程地址 | 只接入批准的服务，拒绝任意输入地址 |
| 凭证 | 不进入模型上下文，按服务绑定并审计 |

stdio 的 stdout 应留给协议，诊断日志写 stderr；远程使用所选版本支持的 Streamable HTTP，旧 HTTP+SSE 是兼容方式。Streamable HTTP 本身也可能使用 SSE，因此不应将两者描述为完全互斥的传输原理。

服务返回的文字、资源和工具描述属于外部输入。连接 MCP 不代表获得所有操作授权；同样，客户端确认也不能替代 Server 的业务权限检查。

下一模块：[Skills 技能开发](500-skills-overview.html)。
