---
group: 3. RAG 检索增强
id: hybrid-rerank
title: RAG · 混合检索 + Reranker
toc: RAG · 混合+Rerank
---

**让准确率从 70% 跃升到 90%+ 的两个杀手锏**：混合检索 + Reranker。如果你的 RAG 只用了向量检索，这一章读完就能立刻提升一档。

## 为什么纯向量检索不够

向量检索的盲点：

| 场景 | 向量检索的问题 |
|------|--------------|
| **专有名词查询** | "查 GPT-5 的价格" → 向量可能召回 GPT-4 / Claude 的内容（语义相近）|
| **稀有词** | 训练数据中没见过的词，embedding 不准 |
| **精确数字** | "型号 ABC-1234"，向量不擅长精确匹配 |
| **缩写** | "RAG" vs "Retrieval-Augmented Generation"，可能召回不全 |

**关键词检索（BM25 等）补齐这些短板** —— 精确匹配关键词。

## 1. 混合检索（Hybrid Search）

= **向量检索 + 关键词检索** 结果合并。

```
用户查询: "GPT-5 的价格"
   ↓
   ├─ 向量检索: 召回 10 条（语义相关）
   │   - "OpenAI 最新模型定价..."
   │   - "GPT 系列对比..."
   │
   └─ BM25 检索: 召回 10 条（关键词匹配）
       - "GPT-5 input: $5/M, output: $20/M..."
       - "对比 GPT-5 和 Claude..."
   ↓
合并 + 去重 + 重排 → top 5
   ↓
丢给 LLM
```

### 用 RRF 融合（最简单的合并算法）

**RRF**（Reciprocal Rank Fusion）= 倒数排名融合，行业最常用。

```python
def reciprocal_rank_fusion(rank_lists, k=60):
    """
    rank_lists: [[doc_id_1, doc_id_2, ...], [doc_id_3, doc_id_1, ...]]
    每个列表是一种检索方式的排名
    """
    scores = {}
    for ranks in rank_lists:
        for rank, doc_id in enumerate(ranks):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)

    # 按融合分数排序
    return sorted(scores.items(), key=lambda x: -x[1])

# 使用
vector_hits = ["doc3", "doc1", "doc7", "doc2", "doc5"]
bm25_hits = ["doc1", "doc4", "doc3", "doc8", "doc7"]

fused = reciprocal_rank_fusion([vector_hits, bm25_hits])
top_5 = [doc_id for doc_id, _ in fused[:5]]
# → ["doc1", "doc3", "doc7", "doc2", "doc4"]
```

### BM25 实现（用 rank_bm25 库）

```python
from rank_bm25 import BM25Okapi
import jieba

# 构建 BM25 索引（中文要先分词）
documents = ["GPT-5 的价格...", "Claude 性能...", ...]
tokenized_docs = [list(jieba.cut(doc)) for doc in documents]
bm25 = BM25Okapi(tokenized_docs)

# 查询
query = "GPT-5 的价格"
tokenized_q = list(jieba.cut(query))
scores = bm25.get_scores(tokenized_q)
top_k_bm25 = sorted(enumerate(scores), key=lambda x: -x[1])[:10]
bm25_hits = [documents[idx] for idx, _ in top_k_bm25]
```

### 完整 Hybrid Search 函数

```python
def hybrid_search(query: str, top_k: int = 10):
    # 1. 向量检索
    q_emb = embedder.encode(query).tolist()
    vector_results = qdrant.search(
        collection_name="docs", query_vector=q_emb, limit=top_k
    )
    vector_ids = [str(h.id) for h in vector_results]

    # 2. BM25 检索
    bm25_scores = bm25.get_scores(list(jieba.cut(query)))
    bm25_indices = sorted(enumerate(bm25_scores), key=lambda x: -x[1])[:top_k]
    bm25_ids = [str(idx) for idx, _ in bm25_indices]

    # 3. RRF 融合
    fused = reciprocal_rank_fusion([vector_ids, bm25_ids])
    return [doc_id for doc_id, _ in fused[:top_k]]
```

### 业界主流向量库的内置混合搜索

很多向量库已经**内置混合搜索**，不用自己实现：

```python
# Qdrant（用 named vectors + 自定义 score function）
client.search_batch(...)

# Weaviate（原生支持 hybrid）
result = weaviate_client.query.get(
    "Document", ["text", "source"]
).with_hybrid(
    query="GPT-5 的价格",
    alpha=0.5  # 0=纯关键词, 1=纯向量, 0.5=混合
).with_limit(10).do()

# Elasticsearch（用 dense_vector + match）
es.search(index="docs", body={
    "query": {
        "bool": {
            "should": [
                {"match": {"content": "GPT-5 的价格"}},  # BM25
                {"knn": {"field": "embedding", "query_vector": q_emb, "k": 10}}
            ]
        }
    }
})
```

### Hybrid 的效果数据

业界基准数据（MTEB / BEIR）：

| 方法 | 召回率@10 |
|------|----------|
| 纯向量 | 75% |
| 纯 BM25 | 65% |
| **Hybrid (RRF)** | **85%** |

**+10 个百分点是非常显著的提升**。

## 2. Reranker（重排）

混合检索召回 top-K，但**排序不一定对**。Reranker 用更精细的模型重新排序。

```
Hybrid 召回 50 条（粗排）
   ↓
Reranker 精排 → top 5
   ↓
喂给 LLM
```

### 为什么需要 Reranker

Embedding 模型是**双塔结构** —— query 和 doc 分别编码，速度快但精度有限。

Reranker 是**交叉编码器**（cross-encoder）—— query 和 doc 一起输入，精度高但速度慢。

```
Embedding:
  query → [向量 Q]
  doc   → [向量 D]
  比较  → 余弦相似度 (粗略)

Reranker:
  (query, doc) → 一起输入 → 相关性分数 (精确)
  → 但每对都要重新算，所以只能对 top-K 用
```

### 主流 Reranker 模型

| 模型 | 多语言 | 价格 | 速度 |
|------|-------|------|------|
| **Cohere Rerank 3.5** | ✅ | $0.002/搜索 | 快 |
| **Jina Reranker v2** | ✅ | $0.018/M tokens | 快 |
| **BGE-reranker-v2-m3** | ✅ | 免费（自托管）| 中 |
| **BGE-reranker-large** | 中英 | 免费 | 中 |
| Voyage Rerank-2 | ✅ | $0.05/M tokens | 快 |

### Cohere Rerank 实战

```python
import cohere
co = cohere.Client()

# 上一步检索到的 50 条候选
candidates = ["文档 1...", "文档 2...", ...]  # 50 个

# 重排，返回 top-5
results = co.rerank(
    query="GPT-5 的价格是多少？",
    documents=candidates,
    top_n=5,
    model="rerank-multilingual-v3.0"
)

for r in results.results:
    print(f"分数 {r.relevance_score:.3f}: {candidates[r.index][:80]}")
```

### 自托管 BGE Reranker

不想付费？用 BGE 本地跑。

```python
from FlagEmbedding import FlagReranker

reranker = FlagReranker("BAAI/bge-reranker-v2-m3", use_fp16=True)

candidates = ["文档1", "文档2", ...]
pairs = [[query, doc] for doc in candidates]
scores = reranker.compute_score(pairs)

# 取 top 5
top_5 = sorted(zip(candidates, scores), key=lambda x: -x[1])[:5]
```

### Reranker 的效果数据

| 方法 | 召回率@5（实际相关的能进 top5）|
|------|----------|
| Hybrid 只 | 70% |
| Hybrid + Cohere Rerank | **88%** |
| Hybrid + BGE-reranker | 85% |

**+15-18 个百分点**，巨大提升。

## 3. 完整生产级管道

```python
def production_rag_search(query: str, top_k: int = 5):
    # === 阶段 1: 粗排（召回多 → 50 条）===

    # 1.1 Query 改写（可选，但提升效果）
    expanded_queries = query_expansion(query)  # 见后面

    # 1.2 多 query 各自 Hybrid Search
    all_candidates = set()
    for q in expanded_queries:
        # 向量检索
        q_emb = embedder.encode(q).tolist()
        vector_hits = qdrant.search(query_vector=q_emb, limit=30)

        # BM25 检索
        bm25_hits = bm25_search(q, top_k=30)

        # RRF 融合
        fused = rrf_merge([vector_hits, bm25_hits])
        all_candidates.update(fused[:30])

    candidates = list(all_candidates)[:50]  # 去重后取 50 条

    # === 阶段 2: 精排（50 → top 5）===
    reranked = cohere_rerank(
        query=query,
        documents=candidates,
        top_n=top_k
    )

    return reranked
```

## 4. Query 改写：进一步提升召回

用户的 query 可能写得不规范。**改写后再检索**效果更好。

### 方式 1：Multi-Query（一个 query 改成多个）

```python
def multi_query(original):
    """让 LLM 生成 3 个改写版本"""
    prompt = f"""为以下用户问题生成 3 个不同表述的检索查询。
要求保留核心意图但用词、角度不同。

原问题: {original}

输出 3 行，每行一个改写后的查询，不要其他文字:"""

    resp = client.messages.create(model="claude-haiku-4-5", ...)
    return [original] + resp.content[0].text.strip().split("\n")

# 原: "GPT-5 价格"
# 改: ["OpenAI 最新模型定价", "GPT-5 API 收费标准", "GPT-5 token 价格"]
```

### 方式 2：HyDE（假设性回答）

让 LLM 先**生成一个假设回答**，用回答的 embedding 去检索（比 query embedding 准）。

```python
def hyde_search(query):
    # 1. 让 LLM 生成假设答案
    hypothetical = client.messages.create(
        messages=[{"role":"user","content":f"假设你知道答案，请直接回答: {query}"}]
    ).content[0].text

    # 2. 用假设答案的 embedding 检索（而非 query 的）
    answer_emb = embedder.encode(hypothetical)
    return qdrant.search(query_vector=answer_emb.tolist(), limit=10)
```

HyDE 适合：query 短而答案具体的场景（如「python 装饰器怎么用」）。

### 方式 3：Step-back（提取上层概念）

```python
def step_back(query):
    """把具体问题抽象成上层概念，扩大召回"""
    prompt = f"""把以下具体问题改写为一个更上层、更抽象的问题。
保留核心主题但去掉具体限定。

原问题: {query}
上层问题: """

    abstract = client.messages.create(...).content[0].text
    return [query, abstract]

# 原: "在 Python 3.12 中如何用 asyncio 实现并发限流？"
# 上层: "Python 中如何控制并发量？"
```

适合：用户问题非常具体，但答案在更通用的文档里。

## 5. 性能 vs 准确率的取舍

| 配置 | 召回率 | 延迟 | 成本 |
|------|-------|------|------|
| 纯向量 top-5 | 65% | 30ms | 极低 |
| Hybrid top-5 | 75% | 50ms | 低 |
| Hybrid + Rerank | 88% | 200ms | 中（reranker 成本）|
| Hybrid + Rerank + Multi-Query | 92% | 500ms | 高（多次 LLM 调用）|
| Hybrid + Rerank + HyDE | 90% | 800ms | 高 |

**实战建议**：
- 客服 / 实时场景：Hybrid + Rerank（够快、够准）
- 科研 / 离线场景：加 Multi-Query / HyDE
- 简单 demo：纯向量就行

## 6. 调参时机

按以下顺序优化：

```
1. 切片策略对吗？      → 检查 chunking
   ↓ 如还差
2. Embedding 选对吗？  → 评测多个模型
   ↓ 如还差
3. 加 BM25 → Hybrid    → 通常 +10%
   ↓ 如还差
4. 加 Reranker         → 通常 +10-15%
   ↓ 如还差
5. Query 改写          → 通常 +3-5%
   ↓ 如还差
6. 微调 Embedding      → 垂直领域 +10-20%
```

**90% 的 RAG 问题在 1-4 步解决**。第 5-6 步是锦上添花。

下一节：[Advanced RAG](#advanced-rag) —— Self-RAG / GraphRAG / Agentic RAG 等前沿模式。
