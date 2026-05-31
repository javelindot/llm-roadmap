---
group: 4. MCP 协议
id: mcp-spec
title: MCP · 协议规范
toc: MCP · 协议规范
---

MCP（Model Context Protocol）由 Anthropic 提出，统一了「大模型 ↔ 外部工具/数据源」之间的对接方式，可类比为 **「大模型时代的 USB 协议」**。

核心概念：

- **Server**：暴露工具、资源、Prompt 模板的进程
- **Client**：模型宿主（如 Claude Desktop、Cursor）
- **Transport**：stdio / HTTP / WebSocket 三种传输层
