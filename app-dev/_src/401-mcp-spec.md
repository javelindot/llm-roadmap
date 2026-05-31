---
group: 4. MCP 协议
id: mcp-spec
title: MCP · 协议规范
toc: MCP · 规范
---

懂得 MCP **协议层细节**才能：调试问题、自研 Server / Client、理解性能瓶颈。这一章把 MCP 的底层机制讲透。

## 协议基础：JSON-RPC 2.0

MCP 基于 **JSON-RPC 2.0**。每条消息都是 JSON 对象，三种类型：

```json
// Request（需要响应）
{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {...}}

// Response（对 Request 的回复）
{"jsonrpc": "2.0", "id": 1, "result": {...}}
// 或者错误
{"jsonrpc": "2.0", "id": 1, "error": {"code": -32600, "message": "..."}}

// Notification（不需要响应）
{"jsonrpc": "2.0", "method": "notifications/cancelled", "params": {...}}
```

`id` 用于匹配 request 与 response（异步通信关键）。Notification 没有 id。

## 完整生命周期

```
Client                              Server
  │                                   │
  ├──── 1. initialize ──────────────→ │
  │     (协议版本、Client 信息)        │
  │                                   │
  │ ←──── 1'. initialize result ────  │
  │       (Server 能力、版本)          │
  │                                   │
  ├──── 2. initialized (notif) ───→  │
  │     （Client 准备就绪）            │
  │                                   │
  │  ═══════════════════════════════  │
  │       正常工作期（可能很长）        │
  │                                   │
  │ ──── tools/list ───────────────→  │
  │ ←─── tools 列表 ────────────────  │
  │ ──── tools/call ───────────────→  │
  │ ←─── 执行结果 ─────────────────   │
  │ ──── resources/list ───────────→  │
  │ ←─── resources 列表 ──────────   │
  │ ──── resources/read ───────────→  │
  │ ←─── 资源内容 ─────────────────   │
  │  ═══════════════════════════════  │
  │                                   │
  ├──── shutdown ──────────────────→  │
  │ ←─── shutdown result ──────────   │
  ├──── exit (notif) ─────────────→   │
  ▼                                   ▼
 (close)                          (close)
```

## 阶段 1: 初始化与能力协商

Client 先告诉 Server「**我支持什么**」，Server 回复「**我提供什么**」。

### initialize 请求

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "sampling": {},        // Client 可以代 Server 调 LLM
            "roots": {            // Client 暴露文件系统根目录
                "listChanged": true
            }
        },
        "clientInfo": {
            "name": "claude-desktop",
            "version": "1.0.0"
        }
    }
}
```

### initialize 响应

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {"listChanged": true},      // Server 提供 Tools
            "resources": {"subscribe": true},     // Server 提供 Resources，支持订阅
            "prompts": {"listChanged": true},     // Server 提供 Prompts
            "logging": {}                         // Server 支持日志
        },
        "serverInfo": {
            "name": "github-mcp-server",
            "version": "0.5.0"
        }
    }
}
```

### 能力协商详解

`capabilities` 字段决定双方支持哪些功能。常见字段：

| 字段（在 Server `capabilities` 下）| 含义 |
|--------------------------------|------|
| `tools` | 提供 Tools |
| `tools.listChanged` | 工具列表会动态变化（会发 notification）|
| `resources` | 提供 Resources |
| `resources.subscribe` | 支持订阅资源变化 |
| `resources.listChanged` | 资源列表会变化 |
| `prompts` | 提供 Prompts |
| `prompts.listChanged` | Prompt 列表会变化 |
| `logging` | 接受 Client 设置日志级别 |
| `completions` | 支持参数自动补全 |

## 阶段 2: 三大原语的协议格式

### 2.1 Tools（工具）

#### tools/list

```json
// 请求
{"jsonrpc":"2.0","id":2,"method":"tools/list"}

// 响应
{
    "jsonrpc":"2.0","id":2,
    "result": {
        "tools": [
            {
                "name": "create_issue",
                "description": "Create a new GitHub issue",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo": {"type": "string", "description": "owner/repo"},
                        "title": {"type": "string"},
                        "body": {"type": "string"},
                        "labels": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["repo", "title"]
                }
            }
        ]
    }
}
```

#### tools/call

```json
// 请求
{
    "jsonrpc":"2.0","id":3,"method":"tools/call",
    "params": {
        "name": "create_issue",
        "arguments": {
            "repo": "octocat/hello-world",
            "title": "Bug: button not working",
            "body": "When I click the button..."
        }
    }
}

// 响应（成功）
{
    "jsonrpc":"2.0","id":3,
    "result": {
        "content": [
            {"type": "text", "text": "Issue #42 created: https://github.com/..."}
        ],
        "isError": false
    }
}

// 响应（失败）
{
    "jsonrpc":"2.0","id":3,
    "result": {
        "content": [
            {"type": "text", "text": "Error: repository not found"}
        ],
        "isError": true  // 关键：错误是放在 result 里，不是 error 字段
    }
}
```

注意：**工具调用失败用 `isError: true`**，而不是 JSON-RPC 的 `error` 字段。这样模型才能看到错误信息并自行处理。

### 2.2 Resources（资源）

资源类似「文件」，由 URI 标识，Client 主动按需读取。

#### resources/list

```json
{
    "jsonrpc":"2.0","id":4,"method":"resources/list",
    "result": {
        "resources": [
            {
                "uri": "file:///workspace/README.md",
                "name": "Project README",
                "mimeType": "text/markdown"
            },
            {
                "uri": "github://repos/octocat/hello-world/issues",
                "name": "Open Issues",
                "mimeType": "application/json"
            }
        ]
    }
}
```

#### resources/read

```json
// 请求
{
    "jsonrpc":"2.0","id":5,"method":"resources/read",
    "params": {"uri": "file:///workspace/README.md"}
}

// 响应
{
    "jsonrpc":"2.0","id":5,
    "result": {
        "contents": [{
            "uri": "file:///workspace/README.md",
            "mimeType": "text/markdown",
            "text": "# Hello World\n..."
        }]
    }
}
```

#### 资源订阅（Server 主动推送变化）

```json
// Client 订阅
{"jsonrpc":"2.0","id":6,"method":"resources/subscribe",
 "params":{"uri":"github://repos/octocat/issues"}}

// Server 后续主动推送
{"jsonrpc":"2.0","method":"notifications/resources/updated",
 "params":{"uri":"github://repos/octocat/issues"}}

// Client 收到后可以重新 read
```

### 2.3 Prompts（模板）

预定义的可参数化 prompt。

```json
// 列出
{"jsonrpc":"2.0","id":7,"method":"prompts/list"}

// 响应
{
    "result": {
        "prompts": [{
            "name": "code_review",
            "description": "Generate code review for a PR",
            "arguments": [
                {"name": "pr_number", "required": true},
                {"name": "focus", "required": false}
            ]
        }]
    }
}

// 获取实际 prompt 内容
{
    "jsonrpc":"2.0","id":8,"method":"prompts/get",
    "params": {
        "name": "code_review",
        "arguments": {"pr_number": "42", "focus": "security"}
    }
}

// 响应
{
    "result": {
        "messages": [
            {"role": "user", "content": {"type": "text", "text": "Review PR #42 focusing on security..."}}
        ]
    }
}
```

## 阶段 3: 三种 Transport

### Transport 1: stdio

最简单。Client 启动 Server 作为子进程，通过 stdin / stdout 通信。**每行一条 JSON 消息**。

```python
# Server 端（伪代码）
import sys, json

def main():
    for line in sys.stdin:  # 阻塞读取
        msg = json.loads(line)
        response = handle(msg)
        if response:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()  # 一定要 flush
```

✅ **优点**：最简单、零网络配置、安全（不开端口）
❌ **缺点**：Server 与 Client 必须在同一台机器

适合：本地工具（Claude Desktop / Cursor 集成）。

### Transport 2: HTTP + SSE（已逐步淘汰）

老式远程 transport。Client 调 POST 发请求，Server 用 SSE 推流响应。

```
Client → POST /messages → Server
Client ← SSE: event/data ← Server (推流多个响应)
```

❌ 2025 后被新的 Streamable HTTP 取代。

### Transport 3: Streamable HTTP（2025 推荐）

替代 SSE。**支持双向流、可恢复、更标准**。

```
单一 endpoint: POST /mcp
- 请求方向: Client 发 JSON 消息
- 响应方向: Server 用 chunked transfer 流式返回
- 支持长连接，无须重连
```

```python
# Server 端（用官方 SDK）
from mcp.server.streamable_http import streamable_http_server
import asyncio

async def main():
    async with streamable_http_server(my_server, port=8080) as server:
        await server.serve_forever()

asyncio.run(main())
```

✅ **优点**：跨机器、负载均衡友好、防火墙穿越好
❌ **缺点**：需要鉴权 / TLS / 限流等基础设施

适合：企业内部 / 公网 MCP Server。

## 阶段 4: 高级特性

### Sampling（Server 反向调 LLM）

Server 可以**让 Client 帮忙调 LLM**。例如 Server 需要 LLM 总结一段长文：

```json
// Server 发请求
{
    "jsonrpc":"2.0","id":9,"method":"sampling/createMessage",
    "params": {
        "messages": [{"role":"user","content":{"type":"text","text":"总结：..."}}],
        "maxTokens": 500
    }
}

// Client 调 LLM 后返回结果
{
    "jsonrpc":"2.0","id":9,
    "result": {
        "role": "assistant",
        "content": {"type":"text","text":"摘要：..."}
    }
}
```

好处：
- Server 不需要自己有 LLM API key（用户的 Client 已经有了）
- 统一计费（用户付一次钱用所有 Server）

### Progress（长任务进度）

```json
// 任务发起时带 progressToken
{
    "method":"tools/call",
    "params": {"name":"build_project","arguments":{...},
               "_meta":{"progressToken":"job-001"}}
}

// Server 持续推送进度（notification）
{"method":"notifications/progress",
 "params":{"progressToken":"job-001","progress":50,"total":100}}
```

### Cancellation（取消请求）

```json
// Client 请求取消
{"method":"notifications/cancelled",
 "params":{"requestId":3, "reason":"User cancelled"}}

// Server 应中止该 request 并清理资源
```

### Logging

Client 可设置 Server 日志级别：

```json
{"method":"logging/setLevel","params":{"level":"debug"}}

// Server 推日志（notification）
{"method":"notifications/message",
 "params":{"level":"info","logger":"github","data":"Fetched issue #42"}}
```

## 错误处理

### JSON-RPC 标准错误码

| 代码 | 含义 |
|------|------|
| -32700 | Parse error（JSON 错）|
| -32600 | Invalid request |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |

### MCP 扩展错误码

| 代码 | 含义 |
|------|------|
| -32000 | Server error 起始 |
| -32001 | Resource not found |
| -32002 | Resource access denied |

业务错误 → 用 `isError: true` 在 result 里返回，而非 error 字段。

## 关键设计原则

MCP 协议设计的几个**核心思想**：

1. **简单胜过复杂**：JSON-RPC 2.0 而非自创协议
2. **能力协商**：双方动态决定支持什么功能
3. **去中心化**：Server 完全独立，可随时增删
4. **多 Transport**：协议层不绑死传输方式
5. **错误透明**：模型能感知工具错误并自行恢复

## 总结：消息流速查表

```
初始化:
  → initialize
  ← initialize result
  → initialized (notif)

发现能力:
  → tools/list, resources/list, prompts/list
  ← 列表

调用:
  → tools/call, resources/read, prompts/get
  ← 结果

订阅与推送:
  → resources/subscribe
  ← resources/updated (notif)

进度与取消:
  ← progress (notif)
  → cancelled (notif)

关闭:
  → shutdown
  → exit (notif)
```

下一节：[编写 MCP Server](#mcp-server) —— 用 Python 写第一个能跑的 Server。
