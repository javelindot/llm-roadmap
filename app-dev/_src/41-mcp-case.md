---
group: 4. MCP 协议
id: mcp-case
title: MCP · 实战集成
toc: MCP · 实战集成
---

一个最小 MCP Server 示例（Python）：

```python
from mcp.server import Server
import mcp.types as types

server = Server("my-tools")

@server.list_tools()
async def list_tools():
    return [types.Tool(
        name="search_docs",
        description="搜索内部文档",
        inputSchema={"type": "object",
                     "properties": {"q": {"type": "string"}}}
    )]

@server.call_tool()
async def call(name, args):
    if name == "search_docs":
        results = my_search(args["q"])
        return [types.TextContent(type="text", text=str(results))]
```
