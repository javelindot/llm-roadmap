---
group: 3. RAG 检索增强
id: vector-db
title: RAG · 向量数据库
toc: RAG · 向量库
---

存几万条向量，**任何数据库都能撑**。但要存千万、亿级，向量数据库的选型直接影响**延迟、成本、运维难度**。

## 2026 主流方案对比

| 数据库 | 类型 | 适合规模 | 延迟（top-10）| 部署 | 价格 |
|--------|-----|---------|--------------|------|------|
| **ChromaDB** | 嵌入式 | < 100 万 | <50ms | 进程内 | 免费 |
| **Qdrant** | 独立服务 | 千万 - 亿 | <30ms | 单机/集群 | 开源 / SaaS |
| **Milvus** | 分布式 | 亿+ | <30ms | 集群（复杂） | 开源 |
| **Weaviate** | 独立服务 | 千万 | <50ms | 单机/集群 | 开源 / SaaS |
| **pgvector** | PG 扩展 | 千万 | <100ms | 复用 PG | 免费 |
| **Pinecone** | SaaS | 任意 | <50ms | 全托管 | 付费 |
| **Elasticsearch** | 通用 | 千万 | <100ms | 已有 ES | 开源 |

## 选型决策树

```
你的数据规模？
├─ < 10 万条 → 任何方案都行，推荐 ChromaDB（最简单）
├─ 10 万 - 100 万
│  ├─ 已有 PostgreSQL → pgvector（少一套服务）
│  └─ 新项目 → Qdrant（性能好、社区活跃）
├─ 100 万 - 1000 万
│  ├─ 内部项目 → Qdrant
│  ├─ 多语言混合检索需求 → Weaviate
│  └─ 已有 ES 集群 → Elasticsearch（用同一套基础设施）
└─ 1000 万 +
   ├─ 自托管 → Milvus（专为大规模设计）
   └─ 不想运维 → Pinecone / Qdrant Cloud
```

## 详细方案介绍

### ChromaDB - 入门首选

最快上手。**进程内嵌入式**，无需启动服务。

```python
import chromadb

# 持久化到本地目录
client = chromadb.PersistentClient(path="./chroma_db")
col = client.get_or_create_collection(
    name="docs",
    metadata={"hnsw:space": "cosine"}  # 距离度量
)

# 添加（embedding 可选 —— Chroma 内置 embedding 模型）
col.add(
    ids=["doc1", "doc2"],
    embeddings=[[0.1, 0.2, ...], [0.3, 0.4, ...]],  # 自己 embed
    documents=["原文1", "原文2"],
    metadatas=[{"source": "hr"}, {"source": "policy"}]
)

# 查询
res = col.query(
    query_embeddings=[[0.15, 0.25, ...]],
    n_results=5,
    where={"source": "hr"}  # metadata 过滤
)
```

✅ **优点**：零配置、Python 原生、有 metadata 过滤
❌ **缺点**：> 100 万条性能下降、单机限制

### Qdrant - 性价比之王

Rust 写的高性能向量库，**自托管首选**。

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition

# 本地 / 远程
client = QdrantClient(url="http://localhost:6333")
# 或 client = QdrantClient(":memory:")  # 内存模式

# 创建集合
client.create_collection(
    collection_name="docs",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
)

# 添加
client.upsert(
    collection_name="docs",
    points=[
        PointStruct(
            id=1,
            vector=[0.1, 0.2, ...],
            payload={"text": "...", "source": "hr", "lang": "zh"}
        )
    ]
)

# 查询（带 metadata 过滤）
hits = client.search(
    collection_name="docs",
    query_vector=[0.15, 0.25, ...],
    query_filter=Filter(must=[
        FieldCondition(key="source", match={"value": "hr"})
    ]),
    limit=5
)
```

✅ **优点**：性能强、过滤功能强大、容易部署
❌ **缺点**：千亿级仍需要 Milvus

部署：

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### pgvector - 已有 PG 集群必选

PostgreSQL 扩展。**复用现有 DB 集群**，少一个组件。

```sql
-- 安装扩展
CREATE EXTENSION vector;

-- 建表
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    metadata JSONB,
    embedding vector(1024)
);

-- 建索引（关键！否则慢成龟）
CREATE INDEX ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 查询
SELECT content, embedding <=> '[0.1,0.2,...]' AS distance
FROM documents
WHERE metadata->>'source' = 'hr'
ORDER BY embedding <=> '[0.1,0.2,...]'
LIMIT 5;
```

Python 调用：

```python
import psycopg2
from pgvector.psycopg2 import register_vector

conn = psycopg2.connect(...)
register_vector(conn)
cur = conn.cursor()

# 插入
cur.execute(
    "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
    ("文档内容", embedding_vector)
)

# 查询
cur.execute("""
    SELECT content, embedding <=> %s AS distance
    FROM documents
    ORDER BY embedding <=> %s
    LIMIT 5
""", (query_vec, query_vec))
results = cur.fetchall()
```

✅ **优点**：复用现有基础设施、事务一致性、SQL 表达力
❌ **缺点**：性能比专用库差 30-50%、千万级开始吃力

### Milvus - 大规模生产级

分布式架构。亿级以上数据必备。

```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility

connections.connect("default", host="localhost", port="19530")

# 定义 Schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=10000),
    FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=100),
]
schema = CollectionSchema(fields, description="RAG docs")
col = Collection(name="docs", schema=schema)

# 建索引（HNSW 推荐）
index_params = {"index_type": "HNSW", "metric_type": "COSINE",
                "params": {"M": 16, "efConstruction": 200}}
col.create_index(field_name="embedding", index_params=index_params)

# 查询
col.load()
results = col.search(
    data=[query_vec],
    anns_field="embedding",
    param={"metric_type": "COSINE", "params": {"ef": 100}},
    limit=10,
    expr='source == "hr"'  # metadata 过滤
)
```

✅ **优点**：分布式、亿级仍然快、企业级特性丰富
❌ **缺点**：部署复杂（K8s）、运维门槛高

## 关键概念：索引算法

向量数据库本质就是「快速找最相似的 K 个向量」。算法选择直接影响性能。

| 算法 | 召回率 | 速度 | 内存 | 适合 |
|------|-------|------|------|------|
| **HNSW** | 95-99% | 极快 | 大 | 大部分场景的默认选择 |
| **IVF** | 90-95% | 快 | 小 | 内存敏感、能接受略低召回 |
| **IVF_PQ** | 80-90% | 很快 | 极小 | 亿级数据、内存极紧张 |
| **Flat** | 100% | 慢 | 小 | 数据少、要 100% 准确 |

**默认用 HNSW**。

### HNSW 关键参数

```
M               连接数（一般 16-64）。越大召回越好，但建索引慢。
efConstruction  建索引时探索深度（一般 100-500）。越大质量越好，但慢。
ef             查询时探索深度（一般 50-200）。越大召回越高，但慢。
```

**调优建议**：
- 入门：用默认值（M=16, ef=100）
- 追求召回：M=32, ef=200
- 追求速度：M=8, ef=50

## 性能优化技巧

### 1. 用 metadata 提前过滤

```python
# ❌ 慢：先向量检索 1000 条，再 metadata 过滤剩 10 条
hits = client.search(query_vec, limit=1000)
filtered = [h for h in hits if h.payload["source"] == "hr"]

# ✅ 快：先按 metadata 过滤，再向量检索
hits = client.search(
    query_vec, 
    query_filter=Filter(must=[FieldCondition(key="source", match={"value":"hr"})]),
    limit=10
)
```

性能差 10-100 倍。

### 2. Quantization（量化）

对向量精度进行压缩，节省内存。

```python
# Qdrant 启用 scalar quantization
client.create_collection(
    collection_name="docs",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
    quantization_config=ScalarQuantization(
        scalar=ScalarQuantizationConfig(type=ScalarType.INT8, always_ram=True)
    )
)
# 内存 ↓ 75%，召回 ↓ 1-3%
```

### 3. 多向量字段

存「问题」和「答案」两个 embedding，分别检索：

```python
# Qdrant 多向量
vectors_config={
    "question": VectorParams(size=1024, distance=Distance.COSINE),
    "answer": VectorParams(size=1024, distance=Distance.COSINE)
}

# 查询时指定 field
client.search(
    collection_name="docs",
    query_vector=("question", query_emb),  # 用 question 字段检索
    limit=10
)
```

### 4. 批量操作

```python
# ❌ 单条插入慢
for doc in docs:
    client.upsert(collection_name="docs", points=[PointStruct(...)])

# ✅ 批量插入（10-100 倍快）
points = [PointStruct(...) for doc in docs]
client.upsert(collection_name="docs", points=points)
```

### 5. 分片（千万级）

按业务维度分集合，不要把所有数据塞一个 collection：

```python
# ❌ 单集合 5000 万条
collection_name="all_docs"

# ✅ 按租户/部门/语言分
collection_name=f"docs_{tenant_id}_{language}"
```

## 监控关键指标

生产环境必须监控：

| 指标 | 目标值 | 报警阈值 |
|------|-------|---------|
| 查询延迟 P95 | <100ms | >500ms |
| 召回率（评测集）| >90% | <80% |
| 索引大小 | 监控增长 | 达存储 80% |
| QPS | 按业务 | 持续 90% 容量 |

## 总结：3 种典型架构

### 架构 A：单机入门
```
应用 → ChromaDB（同进程）
```
适合：POC、< 10 万条

### 架构 B：单机生产
```
应用 → Qdrant（独立 Docker）
```
适合：< 千万条、单机够用

### 架构 C：集群生产
```
应用 → 负载均衡 → Milvus 集群（K8s）
                  ↓
             对象存储（S3 / OSS）
```
适合：亿级以上、高可用要求

下一节：[混合检索 + Reranker](#hybrid-rerank) —— 把准确率从 70% 推到 90%+。
