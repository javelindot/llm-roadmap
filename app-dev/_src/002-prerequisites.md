---
group: 0. 导读
id: prerequisites
title: 前置要求与环境准备
toc: 环境准备
---

跑通本指南的代码示例，需要先准备一套轻量但完整的开发环境。建议从 Python 起步；如果你要做前端 AI 产品，再补 TypeScript。

## 编程基础

| 能力 | 必需度 | 备注 |
|------|--------|------|
| Python 3.10+ | 必需 | RAG、MCP、Agent 示例以 Python 为主 |
| HTTP / REST API | 必需 | 调模型、调工具、本质都是 API 集成 |
| JSON Schema / Pydantic | 必需 | Function Call 和 Structured Outputs 的核心 |
| async/await | 推荐 | MCP、Agent、并行工具调用都会用到 |
| Git | 推荐 | Prompt、评测集、工具 schema 都要版本管理 |
| Docker | 推荐 | 本地向量库、MCP Server、沙箱工具会用到 |
| TypeScript | 按需 | 做 Streaming UI、Vercel AI SDK、前端产品时必备 |

零 Python 基础可以先过一遍官方教程，再回来跑示例。不要一开始就把所有框架装满，先跑通一个最小闭环。

## API Keys

建议至少准备 2 家模型提供商，方便做对比、降级和成本路由。

```bash
# 至少任选 1 个
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GEMINI_API_KEY=...
DEEPSEEK_API_KEY=...
QWEN_API_KEY=...

# 推荐显式配置模型名，避免教程里写死版本
LLM_MODEL=...
REASONING_MODEL=...
EMBEDDING_MODEL=...
```

:::callout 💰
**预算建议**：学习阶段先用小模型和低成本模型跑通流程，复杂推理、批量评测、多模态和长上下文任务再切到更强模型。具体价格变化很快，以各家官方价格页为准。
:::

## Python 环境

推荐用 `uv`，速度快、依赖隔离清楚。

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv init llm-app && cd llm-app

# 基础模型 API
uv add openai anthropic google-genai python-dotenv

# 结构化输出
uv add pydantic
```

如果你习惯传统方式，也可以用 `venv + pip`：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install openai anthropic google-genai python-dotenv pydantic
```

## 关键 SDK 一览

按模块安装，不建议一次性全装。

```bash
# 模型 API
openai                   # OpenAI Responses / Chat / Embeddings / Agents SDK 相关入口
anthropic                # Claude Messages / Tool Use / Extended Thinking
google-genai             # Gemini API

# Function Call / Structured Outputs
pydantic                 # 数据模型与 JSON Schema
instructor               # 可选：结构化输出辅助库

# RAG
sentence-transformers    # 本地 Embedding
chromadb                 # 入门向量库
qdrant-client            # 生产常用向量库
rank-bm25                # BM25 检索
cohere                   # Rerank / Embed 可选
llama-index              # RAG / Agentic RAG / Workflows

# MCP
mcp                      # MCP 官方 Python SDK

# Agent / Workflow
langgraph                # 有状态 Agent 工作流
openai-agents            # OpenAI Agents SDK
autogen-agentchat        # 多 Agent 对话场景可选
crewai                   # 角色分工型 Agent 可选

# 评测与可观测性
promptfoo                # Prompt/模型回归测试，可用 npm 版本
ragas                    # RAG 评测
langfuse                 # Trace / Evals
arize-phoenix            # 本地观测与评测
opentelemetry-sdk        # 标准化链路追踪
```

## TypeScript 环境

做全栈 AI App 时再安装。前端推荐从 Vercel AI SDK 起步。

```bash
npm create next-app@latest ai-app
cd ai-app
npm install ai @ai-sdk/openai @ai-sdk/anthropic zod
```

你需要掌握：

- 流式响应：边生成边展示
- 工具调用 UI：让用户看见模型正在查资料或执行工具
- 结构化结果渲染：JSON Schema / Zod schema 到组件
- 错误与重试：网络失败、模型失败、工具失败都要有状态

## 环境变量管理

把 key 放进 `.env`，不要提交到 Git。

```bash
# .env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
LLM_MODEL=...

# .gitignore
.env
.env.*
```

代码里加载：

```python
from dotenv import load_dotenv

load_dotenv()
```

## 编辑器与调试工具

| 工具 | 用途 | 推荐度 |
|------|------|--------|
| Cursor / Claude Code / Codex | AI 辅助开发、代码审查、项目协作 | 高 |
| VS Code + Python / TypeScript 扩展 | 通用开发环境 | 高 |
| Jupyter Notebook | 调 prompt、看 RAG 检索结果 | 中 |
| Langfuse / Phoenix / LangSmith | LLM Trace、评测、回放 | 高 |
| MCP Inspector | 调试 MCP Server | 高 |
| Postman / HTTPie | 调试普通 API 工具 | 中 |

## Hello World 自检

这段代码只验证模型 API 能通。模型名通过环境变量传入，避免教程随着模型发布过期。

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

resp = client.responses.create(
    model=os.getenv("LLM_MODEL"),
    input="用一句话说明什么是大模型应用开发。"
)

print(resp.output_text)
```

如果你用的是兼容 OpenAI 协议的模型服务，可以在初始化时配置 `base_url`：

```python
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
```

:::callout ✅
能成功打印回答，就可以进入 Prompt 与上下文工程。后面每学一个模块，都建议保留一份最小可运行 demo。
:::
