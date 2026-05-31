---
group: 3. RAG 检索增强
id: rag-pipeline
title: RAG · 标准流水线
toc: RAG · 流水线
---

最小可跑的 RAG。**100 行 Python 完成端到端**，跑通后再考虑优化。

## 标准 4 步

```
① 加载文档 → ② 切片 → ③ 向量化入库 → ④ 检索+生成
   (一次性)              (查询时)
```

前 3 步通常是**离线/异步**，第 4 步是**实时**响应用户。

## 最小代码（30 行）

依赖：`pip install sentence-transformers chromadb anthropic`

```python
from sentence_transformers import SentenceTransformer
import chromadb
from anthropic import Anthropic

# === 一次性：构建知识库 ===
docs = [
    "公司年假政策：入职满 1 年享 5 天，满 3 年享 10 天，满 5 年享 15 天。",
    "病假政策：每年累计不超过 15 天，超过需提交医院证明并扣 50% 工资。",
    "婚假政策：法定 3 天，晚婚（25 岁后）额外加 10 天。",
    "丧假政策：直系亲属去世可享 3 天，非直系 1 天。",
]

# Embedding 模型（中文友好的开源模型）
embedder = SentenceTransformer("BAAI/bge-small-zh-v1.5")

# 向量库
chroma = chromadb.Client()
col = chroma.create_collection("hr_policy")
col.add(
    ids=[f"doc_{i}" for i in range(len(docs))],
    embeddings=embedder.encode(docs).tolist(),
    documents=docs
)

# === 查询时：检索 + 生成 ===
def ask(question: str, top_k: int = 2) -> str:
    # 1. 检索
    q_emb = embedder.encode([question]).tolist()
    res = col.query(query_embeddings=q_emb, n_results=top_k)
    context = "\n\n".join(res["documents"][0])

    # 2. 生成
    client = Anthropic()
    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""基于以下材料回答问题。如果材料中没有相关信息，回答"未在公司政策中查到"。

材料:
{context}

问题: {question}"""
        }]
    )
    return msg.content[0].text

# 测试
print(ask("入职 2 年能休几天年假？"))
# → "根据公司政策，入职满 1 年享 5 天年假..."
print(ask("可以请陪产假吗？"))
# → "未在公司政策中查到陪产假相关信息。"
```

跑通了？恭喜，你已经实现了一个 RAG。接下来讲每一步要注意什么。

## 第 1 步：加载文档

实际场景的文档格式多样：PDF、Word、HTML、Markdown、Notion、Confluence、网页、Slack 消息、数据库表。

```python
# 用 unstructured 解析（业界主流）
from unstructured.partition.auto import partition

elements = partition("policy.pdf")  # 自动识别格式
text = "\n\n".join([str(e) for e in elements])
```

支持的格式：

| 格式 | 推荐工具 |
|------|---------|
| PDF | `unstructured` / `pymupdf` / `llamaparse`（高质量）|
| Word | `python-docx` / `unstructured` |
| HTML/网页 | `trafilatura` / `BeautifulSoup` |
| Markdown | 直接读 |
| Notion | `notion-client` API |
| Confluence | `atlassian-python-api` |
| 数据库 | 直接查 + 拼成自然语言 |

**多模态文档（PDF 含表格/图）**：
- 2024 后推荐 `llamaparse`（LlamaIndex 出品）—— 用 GPT-4V 解析复杂 PDF
- 或 `marker`（开源、本地）
- 表格用 `pandas` 提取后转 Markdown

## 第 2 步：切片（最关键的一步）

**为什么要切**：
1. Embedding 模型有最大输入长度（512–8192 token）
2. LLM context 有限，不能塞全文
3. 检索粒度 = 切片粒度，切太大会包含无关内容

**切片策略**（详细见 [chunking 章](#chunking)）：

```python
# 最简单：按字符数切（适合连续文本）
def simple_split(text, chunk_size=500, overlap=50):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

# 更好：按 Markdown 标题切（保留结构）
from langchain.text_splitter import MarkdownHeaderTextSplitter
splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")]
)
chunks = splitter.split_text(markdown_text)
```

**经验默认值**：
- 普通文档：chunk_size=500 tokens, overlap=50
- 长技术文档：chunk_size=800 tokens, overlap=100
- 短问答：chunk_size=200 tokens, no overlap

## 第 3 步：向量化入库

### Embedding 模型选择（[详见专章](#embedding)）

| 模型 | 维度 | 速度 | 中文 | 价格 |
|------|-----|------|------|------|
| `bge-small-zh-v1.5` | 512 | 快 | ⭐⭐⭐⭐⭐ | 免费（本地）|
| `bge-large-zh-v1.5` | 1024 | 中 | ⭐⭐⭐⭐⭐ | 免费 |
| `text-embedding-3-large` (OpenAI) | 3072 | 中 | ⭐⭐⭐⭐ | $0.13/M tokens |
| `voyage-3-large` (Voyage) | 1024 | 中 | ⭐⭐⭐⭐ | $0.18/M |
| `embed-multilingual-v3.0` (Cohere) | 1024 | 中 | ⭐⭐⭐⭐ | $0.10/M |

入门用 `bge-small-zh-v1.5`（免费且效果好），上规模考虑商业模型。

### 向量数据库（[详见专章](#vector-db)）

| 数据库 | 适合规模 | 部署难度 |
|--------|---------|---------|
| ChromaDB | < 100 万条 | ⭐ 进程内 |
| Qdrant | 千万 - 亿级 | ⭐⭐ 单机/集群 |
| Milvus | 亿级+ | ⭐⭐⭐ 集群 |
| pgvector | 已有 PG 集群 | ⭐ 加扩展 |
| Pinecone | 任意 | ⭐ SaaS（要付费） |

入门用 ChromaDB，生产用 Qdrant / pgvector。

```python
# Qdrant 示例
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(":memory:")  # 或 url="http://localhost:6333"

client.create_collection(
    collection_name="hr_policy",
    vectors_config=VectorParams(size=512, distance=Distance.COSINE)
)

points = [
    PointStruct(id=i, vector=embedder.encode(doc).tolist(),
                payload={"text": doc, "source": "hr_handbook"})
    for i, doc in enumerate(docs)
]
client.upsert(collection_name="hr_policy", points=points)
```

## 第 4 步：检索 + 生成

### 简单版（向量检索）

```python
def retrieve(question, top_k=5):
    q_emb = embedder.encode([question]).tolist()[0]
    hits = client.search(
        collection_name="hr_policy",
        query_vector=q_emb,
        limit=top_k
    )
    return [h.payload["text"] for h in hits]

def generate(question, contexts):
    prompt = f"""基于以下材料回答问题。

材料：
{chr(10).join(f'[{i+1}] {c}' for i, c in enumerate(contexts))}

问题：{question}

要求：
- 仅基于材料回答，不要编造
- 在回答末尾用 [1][2] 等标注引用了哪些材料
- 如材料未提及，回答"未查到相关信息"
"""
    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=800,
        messages=[{"role":"user","content": prompt}]
    )
    return msg.content[0].text

# 完整流程
answer = generate(question, retrieve(question))
```

### Prompt 模板要点

```python
RAG_PROMPT = """你是公司知识助手，基于提供的材料回答员工问题。

【材料】
{context}

【规则】
1. 仅基于材料回答，不要使用你的内部知识
2. 如材料未明确提及，回答"未在文档中找到相关信息"
3. 用 [文档1][文档2] 标注引用来源
4. 回答简洁直接，不要寒暄

【问题】
{question}
"""
```

3 个**关键约束**：
- 强制基于材料（否则模型会用内部知识混着答）
- 显式标"未查到"（否则会编造）
- 引用追溯（用户可以核实）

## 评测 RAG 的最小方法

无评测 = 不知道做得好不好。最简单的评测：

```python
# 准备 20-50 条 (问题, 期望答案) 测试集
test_cases = [
    ("入职 2 年能休几天年假？", "5 天"),
    ("生病请假超过 15 天怎么办？", "需医院证明 + 扣 50% 工资"),
    ("公司有陪产假吗？", "未查到"),  # 故意测拒答
]

correct = 0
for q, expected in test_cases:
    answer = ask(q)
    if expected in answer or judge_with_llm(answer, expected):
        correct += 1

print(f"准确率: {correct / len(test_cases):.1%}")
```

**起步阶段**：准确率 60%+ 说明基本能跑；< 50% 多半是检索阶段问题。

## 接下来怎么优化

按性价比排序：

1. **检索质量**：上 Reranker（→ +10-20% 准确率）
2. **切片策略**：用语义切片代替固定大小（→ +5-10%）
3. **混合检索**：向量 + BM25（→ +5%）
4. **Query 改写**：长问题先抽取关键词（→ +3-5%）
5. **Prompt 优化**：调引用规则、加 Few-shot（→ +2-5%）

每步都在后面章节详细讲。

下一节：[切片策略](#chunking) —— RAG 第一道分水岭。
