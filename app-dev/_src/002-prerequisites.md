---
group: 0. 导读
id: prerequisites
title: 前置要求与环境准备
toc: 环境准备
---

跑通本指南所有代码示例，需要的最小环境：

## 编程基础

| 能力 | 必需度 | 备注 |
|------|--------|------|
| Python 3.10+ | 🔴 必需 | 所有示例用 Python |
| 异步编程 (async/await) | 🟡 推荐 | MCP / Agent 章节会用 |
| HTTP / REST API | 🟡 推荐 | 调用模型本质就是 API |
| Git | 🟢 加分 | 管理 prompt 版本 |
| Docker | 🟢 加分 | 部署本地模型时用 |

零 Python 基础？先去补 [《Python 速成》](https://docs.python.org/zh-cn/3/tutorial/index.html) 再回来。

## API Keys（至少 1 个）

```python
# 推荐至少准备 2 家的 key，便于对比和降级
ANTHROPIC_API_KEY    # 推荐：Claude 4.5（应用场景首选）
OPENAI_API_KEY       # 推荐：GPT-5 / o3 系列
DEEPSEEK_API_KEY     # 国内场景首选，成本极低
GEMINI_API_KEY       # Google 系，长上下文优势
```

:::callout 💰
**预算建议**：跑完整套示例约消耗 $5–10 等值 API 费用。Anthropic / OpenAI 都有 free trial 额度，DeepSeek 充 $1 也能跑很多。
:::

## Python 环境

推荐用 `uv` 或 `poetry`，比 `pip` 快 10×。

```bash
# 方案 A: uv（推荐）
curl -LsSf https://astral.sh/uv/install.sh | sh
uv init llm-app && cd llm-app
uv add anthropic openai

# 方案 B: 传统 pip + venv
python3 -m venv .venv
source .venv/bin/activate
pip install anthropic openai
```

## 关键 SDK 一览

```bash
# 模型 SDK（按需装，不必一次全装）
anthropic                # Claude
openai                   # GPT / DeepSeek（DeepSeek 兼容 OpenAI 协议）
google-generativeai      # Gemini

# Function Call / Structured Outputs
pydantic                 # 数据模型，所有结构化输出都需要

# RAG 全家桶
sentence-transformers    # 本地 Embedding
chromadb                 # 入门级向量库
qdrant-client            # 生产级向量库
rank-bm25                # BM25 关键词检索
cohere                   # Reranker（可选）

# MCP
mcp                      # 官方 SDK

# Agent
langgraph                # 当前最主流的编排框架
```

## 环境变量管理

把 key 放进 `.env`，**永远不要 commit**：

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx

# .gitignore（必加）
.env
.env.*
```

代码里用 `python-dotenv` 加载：

```python
from dotenv import load_dotenv
load_dotenv()  # 自动读 .env
```

## 编辑器与调试工具

| 工具 | 用途 | 推荐度 |
|------|------|--------|
| **Cursor / Claude Code** | AI 辅助写代码 | ⭐⭐⭐⭐⭐ |
| VS Code + Python ext | 经典选项 | ⭐⭐⭐⭐ |
| Jupyter Notebook | 调试 prompt 用 | ⭐⭐⭐⭐ |
| **Langfuse / Phoenix** | 生产级 Trace 必备 | ⭐⭐⭐⭐⭐ |

## Hello World 自检

跑通这段代码 = 环境就绪：

```python
import os
from anthropic import Anthropic
client = Anthropic()

msg = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=200,
    messages=[{"role": "user", "content": "用一句话介绍你自己"}]
)
print(msg.content[0].text)
```

输出能正常打印 → 你已就绪，可以开干了。

:::callout 🚀
**下一步**：直接进入 [Prompt 工程基础](#prompt-basics)，跑通第一个结构化提示词。
:::
