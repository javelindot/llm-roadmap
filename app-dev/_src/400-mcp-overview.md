---
group: 4. MCP 协议
id: mcp-overview
title: MCP · 协议概览
toc: MCP · 概览
---

**MCP**（Model Context Protocol）= **大模型的「USB-C 协议」**。Anthropic 2024 年 11 月开源，**2025 年成为事实标准** —— 几乎所有主流模型厂商（OpenAI / Google / DeepSeek / Mistral）和 IDE（Cursor / VSCode / Zed）都已支持。

## 一句话理解 MCP

> **MCP 标准化了「大模型 ↔ 外部工具/数据源」之间的对接方式**。

之前每个工具都要为每个模型厂商单独适配；现在写一个 MCP Server，所有支持 MCP 的客户端**即插即用**。

```
没有 MCP（M × N 难题）:
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Claude  │  │ ChatGPT │  │ Cursor  │
└────┬────┘  └────┬────┘  └────┬────┘
     │ × 3 套不同 API
     ↓            ↓            ↓
  GitHub      Slack       Postgres ... 100 个工具
  
  → 需要写 3 × 100 = 300 个集成

有 MCP（M + N）:
所有客户端 ──MCP 协议──→ 所有 Server
  → 只需 3 + 100 = 103 个实现
```

## 为什么需要 MCP

### 痛点 1：Function Call 不能跨模型/平台

```python
# OpenAI 写法
tools = [{"type":"function","function":{"name":"...","parameters":{...}}}]

# Anthropic 写法
tools = [{"name":"...","input_schema":{...}}]

# Gemini 写法
tools = [Tool(function_declarations=[FunctionDeclaration(...)])]

→ 同一个工具集成进 3 个平台 = 写 3 份代码
```

### 痛点 2：工具复用难

你为公司写的「查订单」工具，**只能用在你的应用里**。
其他人/团队/产品想用 → 必须重新实现一遍。

### 痛点 3：用户切换 IDE 痛苦

在 Cursor 里配的工具，换到 VSCode 又要重新配。

### MCP 解决方案

```
统一协议:
  - 客户端（Claude Desktop / Cursor / Zed / 自研 app）按 MCP 调用
  - 服务端（任何人写的 MCP Server）按 MCP 响应

效果:
  - 写一次 Server，处处可用
  - 用户在任何 MCP 客户端里都能用同一套工具
  - 工具市场化（社区可分享 Server）
```

## MCP 的三大原语（Primitives）

MCP 不只是 Function Call 的「标准化」 —— 它定义了**三种暴露给模型的资源**：

| 原语 | 类型 | 用途 |
|------|------|------|
| **Tools** | 可调用函数 | 让模型主动调用（同 FC）|
| **Resources** | 可读数据 | 文件、数据库表、API 响应等，模型按需读取 |
| **Prompts** | 模板化提示词 | Server 预定义的常用 prompt 模板 |

举例 —— 一个「GitHub MCP Server」可以提供：
- Tools: `create_issue`, `merge_pr`, `add_comment`
- Resources: `repo_readme`, `recent_commits`, `open_issues`
- Prompts: `code_review_prompt`, `release_notes_prompt`

模型可以根据需要混合使用这三种能力。

## MCP 架构：Client / Server 模式

```
┌──────────────────────────────────────────────┐
│  Host（模型宿主：Claude Desktop / Cursor）     │
│  ┌────────────────────────────────────────┐  │
│  │  Client（每个 Server 一个 Client）      │  │
│  └──┬─────────┬─────────┬──────────┬────┘  │
└─────┼─────────┼─────────┼──────────┼───────┘
      ↓         ↓         ↓          ↓
   ┌─────┐  ┌─────┐  ┌─────┐    ┌─────┐
   │Server│ │Server│ │Server│    │Server│
   │GitHub│ │ DB  │ │File │    │自定义│
   └─────┘  └─────┘  └─────┘    └─────┘
```

- **Host**：用户实际操作的程序（如 Claude Desktop）
- **Client**：MCP 协议的客户端实现（Host 内部，每个 Server 一个）
- **Server**：暴露 Tools / Resources / Prompts 的进程

## 传输层：3 种 transport

MCP 不绑死任何传输方式：

| Transport | 适合 | 典型场景 |
|-----------|------|---------|
| **stdio** | 本地 Server | Claude Desktop 启动子进程通信 |
| **HTTP + SSE** | 远程 Server | Web 服务、跨机器调用 |
| **Streamable HTTP** | 高吞吐 | 2025 新增，替代 SSE |

```python
# stdio 示例（本地子进程）
# Claude Desktop config:
{
    "mcpServers": {
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_TOKEN": "ghp_xxx"}
        }
    }
}
```

## 应用场景（2026 真实案例）

### IDE 增强

- **Cursor / VSCode + GitHub MCP**：直接在编辑器问 "最近 PR 有哪些 review 意见"
- **Cursor + Database MCP**：让 AI 帮你查询生产数据库（带权限）
- **Cursor + Sentry MCP**：「最近哪个服务报错最多？」

### 桌面 AI 助手

- **Claude Desktop + File System MCP**：让 Claude 读写你的本地文件
- **Claude Desktop + Slack MCP**：让 Claude 总结昨天的群消息
- **Claude Desktop + Notion MCP**：让 Claude 维护你的知识库

### 企业内部 AI

- 自研 MCP Server 暴露：CRM / ERP / 工单系统 / 日志查询 / 部署工具
- 全公司任何 AI 应用（Claude / Cursor / 内部产品）共用同一套 Server

### Agent 平台

- LangGraph / AutoGen 等 Agent 框架**直接读取 MCP Server**作为工具源
- 不需要在 Agent 代码里硬编码工具列表

## 生态现状（2026 年）

### 官方 Server（Anthropic 维护）

```
@modelcontextprotocol/server-filesystem    本地文件系统
@modelcontextprotocol/server-github        GitHub
@modelcontextprotocol/server-gitlab        GitLab
@modelcontextprotocol/server-postgres      PostgreSQL
@modelcontextprotocol/server-sqlite        SQLite
@modelcontextprotocol/server-slack         Slack
@modelcontextprotocol/server-google-maps   Google Maps
@modelcontextprotocol/server-puppeteer     浏览器自动化
@modelcontextprotocol/server-memory        知识图谱记忆
... 30+ 官方 Server
```

### 社区 Server

[awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) 列表里已有 **500+** 社区 Server，覆盖：

- 各家云服务（AWS / GCP / Cloudflare）
- 各种 SaaS（Linear / Jira / Notion / Airtable / HubSpot）
- 各种数据源（Snowflake / BigQuery / Elasticsearch）
- 各种工具（Figma / Adobe / Office）

### 客户端支持情况

| 客户端 | MCP 支持度 |
|--------|----------|
| Claude Desktop | ⭐⭐⭐⭐⭐ 原生 |
| Cursor | ⭐⭐⭐⭐⭐ 原生 |
| Continue.dev | ⭐⭐⭐⭐ 内置 |
| Zed | ⭐⭐⭐⭐ 内置 |
| VSCode (官方扩展) | ⭐⭐⭐⭐ 2025 加入 |
| Cline | ⭐⭐⭐⭐ 内置 |
| Claude Agent SDK | ⭐⭐⭐⭐⭐ 一等公民 |

## MCP vs Function Call：核心差异

| 维度 | Function Call | MCP |
|------|--------------|-----|
| 标准化 | 各厂商不同 | 统一协议 |
| 工具复用 | 每个应用自己写 | Server 一次写到处用 |
| 资源访问 | 只能调函数 | Tools + Resources + Prompts |
| 部署 | 内嵌在应用代码 | 独立进程，可热插拔 |
| 用户场景 | 应用开发者 | 终端用户 + 应用开发者 |

**简单说**：FC 是「**程序内**用的工具调用」，MCP 是「**跨程序、跨用户**复用工具」。

## 学习路径

| 章节 | 内容 |
|------|------|
| [协议规范](#mcp-spec) | 消息格式 / 生命周期 / 能力协商 |
| [编写 Server](#mcp-server) | Python SDK 完整示例 |
| [客户端集成 + 生态](#mcp-client) | TypeScript Client / 配置 / 安全 |

## 何时该用 MCP

✅ **强烈推荐**：
- 工具需要被**多个应用**共用
- 用户需要在**多个 IDE/客户端**用同样的工具
- 公司想建立**内部 AI 工具平台**
- 集成开源工具生态（GitHub / Slack / DB 等）

❌ **不需要**：
- 一次性的小脚本（直接 FC 更快）
- 工具只在自己应用里用（FC 够了）
- 极致性能要求（多一层 IPC 有少量开销）

下一节：[协议规范详解](#mcp-spec) —— 真正搞懂 MCP 的内部机制。
