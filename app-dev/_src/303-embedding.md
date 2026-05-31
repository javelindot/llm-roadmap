---
group: 3. RAG 检索增强
id: embedding
title: RAG · Embedding 选型
toc: RAG · Embedding
---

Embedding 模型把文本变成向量。**选型直接决定检索质量** —— 选错型号，整个 RAG 都翻车。

## Embedding 在做什么

```
"今天天气真好" → [0.23, -0.45, 0.78, ..., 0.12]   ← 768 维向量
"今儿天气不错"  → [0.21, -0.43, 0.76, ..., 0.10]   ← 几乎相同
"程序员崩溃了"  → [-0.81, 0.23, -0.05, ..., 0.91]  ← 距离很远

→ 用余弦相似度衡量"语义距离"
→ 检索时找向量最近的 top-K
```

好的 Embedding 满足：**语义相近 → 向量距离近**，**语义无关 → 向量距离远**。

## 2026 主流模型对比

### 中文场景

| 模型 | 维度 | MTEB-zh 分数 | 速度 | 价格 |
|------|------|------------|------|------|
| **BGE-large-zh-v1.5** | 1024 | 69.5 | 中 | 免费（本地）|
| **BGE-M3** | 1024 | 73.2 | 中 | 免费（多语言）|
| **bge-small-zh-v1.5** | 512 | 65.3 | 快 | 免费 |
| **gte-Qwen2-7B** | 3584 | 72.0 | 慢 | 免费 |
| OpenAI `text-embedding-3-large` | 3072 | 71.0 | 中 | $0.13/M tokens |
| Voyage `voyage-3-large` | 1024 | 72.5 | 中 | $0.18/M |
| Cohere `embed-multilingual-v3` | 1024 | 69.8 | 中 | $0.10/M |
| **Jina `jina-embeddings-v3`** | 1024 | 70.5（多语言）| 中 | $0.10/M |

**推荐**：
- 入门 / 自托管：**BGE-M3**（中英双语 + 高性能 + 开源）
- 商业 / 不想运维：**Voyage 3** 或 **Cohere v3**

### 英文场景

| 模型 | 维度 | MTEB-en 分数 | 备注 |
|------|------|------------|------|
| OpenAI `text-embedding-3-large` | 3072 | 64.6 | 通用首选 |
| Voyage `voyage-3-large` | 1024 | 67.2 | 当前 SOTA |
| `e5-mistral-7b-instruct` | 4096 | 66.6 | 开源最强 |
| `bge-large-en-v1.5` | 1024 | 64.2 | 开源轻量 |

## 4 个核心选型维度

### 1. 维度（dim）

向量维度越高，理论上表达能力越强，但：
- 占存储和内存（512 维 vs 3072 维 → 6 倍存储）
- 检索速度变慢
- 边际收益递减

**经验**：
- 千万级数据：用 512 / 768 维
- 百万级：用 1024 维
- 几十万：可以上 3072 维（追求精度）

### 2. 上下文长度

| 模型 | 最大输入 token |
|------|---------------|
| BGE-small/large | 512 |
| BGE-M3 | 8192 |
| OpenAI text-embedding-3 | 8191 |
| Voyage-3-large | 32000 |
| Jina v3 | 8194 |

**意义**：超过最大长度的文本要截断，可能丢信息。所以**切片大小不能超过 embedding 上下文**。

### 3. 多语言能力

如果文档是**纯中文**：选 `bge-large-zh-v1.5`
如果是**中英混合**：必选 `BGE-M3` / `voyage-3` / `Cohere multilingual`
如果是**纯英文**：选 `voyage-3` / `text-embedding-3-large`

:::callout ⚠️
**坑**：用纯英文模型 embed 中文文本，检索效果会暴跌 30%+
:::

### 4. 微调能力

如果有垂直领域（医疗 / 法律 / 金融），考虑**微调**：

```python
# 用 sentence-transformers 微调
from sentence_transformers import SentenceTransformer, losses
from torch.utils.data import DataLoader

model = SentenceTransformer("BAAI/bge-large-zh-v1.5")
train_examples = [
    InputExample(texts=["问题1", "正答1"], label=1.0),
    InputExample(texts=["问题1", "错答1"], label=0.0),
    ...
]
loss = losses.CosineSimilarityLoss(model)
model.fit(
    train_objectives=[(DataLoader(train_examples, batch_size=16), loss)],
    epochs=3
)
model.save("./bge-zh-finetuned")
```

效果：垂直领域准确率可提升 10–20%（前提：有 1000+ 高质量训练对）。

## 实战代码

### 用 sentence-transformers（开源）

```python
from sentence_transformers import SentenceTransformer

# 加载（首次会下载 ~400MB）
model = SentenceTransformer("BAAI/bge-large-zh-v1.5")

# 单条
emb = model.encode("我们的退款政策是 7 天无理由")
print(emb.shape)  # (1024,)

# 批量（更快）
embs = model.encode(
    ["文档 1", "文档 2", "文档 3"],
    batch_size=32,
    show_progress_bar=True,
    normalize_embeddings=True  # 归一化便于余弦计算
)
```

### 用 OpenAI API

```python
from openai import OpenAI
client = OpenAI()

resp = client.embeddings.create(
    model="text-embedding-3-large",
    input=["文档 1", "文档 2"],
    dimensions=1024  # 可降维（OpenAI 独有）
)
embs = [d.embedding for d in resp.data]
```

`dimensions` 参数允许把 3072 维降到 1024 / 512，**速度更快、效果几乎不降**。

### 用 Cohere

```python
import cohere
co = cohere.Client()

resp = co.embed(
    texts=["文档 1", "文档 2"],
    model="embed-multilingual-v3.0",
    input_type="search_document"  # 区分 query 和 doc
)
embs = resp.embeddings
```

`input_type` 区分使用场景，提升检索效果：
- `search_document`：文档入库时用
- `search_query`：查询时用
- `classification`：用于分类任务
- `clustering`：用于聚类

## Query 与 Document 的对称性

**重要细节**：查询 query 和文档 doc 都要用**同一个模型** embed。

```python
# ❌ 错：用不同模型
doc_emb = bge_model.encode(documents)
query_emb = openai_client.embeddings.create(...)
# → 检索结果完全乱

# ✅ 对
doc_emb = model.encode(documents)
query_emb = model.encode(query)
```

部分模型支持**非对称 embed**（如 Cohere 的 `input_type`），效果更好。

## 距离度量选哪个

向量距离的 3 种主流算法：

| 算法 | 公式 | 适合 |
|------|-----|------|
| **Cosine** | 角度（方向）| 文本（最常用）|
| **Dot Product** | 内积（含模长）| 用归一化向量时和 Cosine 等价 |
| **Euclidean (L2)** | 几何距离 | 图像、坐标 |

**99% 文本场景用 Cosine**。

## Embedding 的 7 个最佳实践

### 1. 归一化（normalize）

让所有向量长度为 1，余弦距离 = 内积，计算更快。

```python
embs = model.encode(texts, normalize_embeddings=True)
```

### 2. 批量处理

单条 embed 极慢。批量调用快 10-50 倍。

### 3. 缓存

同样的文本不要重复 embed。

```python
import hashlib
import diskcache

cache = diskcache.Cache("./emb_cache")

def cached_encode(text):
    key = hashlib.md5(text.encode()).hexdigest()
    if key in cache: return cache[key]
    emb = model.encode(text)
    cache[key] = emb
    return emb
```

### 4. 加 prefix（部分模型需要）

BGE 系列需要在 query 前加特定前缀：

```python
# BGE 中文模型
def encode_query(q):
    return model.encode("为这个句子生成表示以用于检索相关文章：" + q)

def encode_doc(d):
    return model.encode(d)  # 文档不加 prefix
```

不加 prefix 效果会差 5-10%。

### 5. 控制单条长度

避免输入超过模型最大长度。**切片大小应 ≤ embedding 模型最大长度**。

### 6. 多语言文档加语言标识

```python
metadata = {"text": doc, "language": "zh"}
# 检索时按语言过滤，避免跨语言召回噪音
```

### 7. 监控漂移

embedding 模型升级后，旧数据需要重新 embed。**记录模型版本**：

```python
metadata = {
    "embedding_model": "bge-large-zh-v1.5",
    "embedding_version": "1.5.0"
}
# 升级时按 metadata 增量重 embed
```

## 选型决策树

```
预算 / 部署需求？
├─ 不想运维（用云服务）
│  ├─ 中英混合 → Voyage-3 / Cohere multilingual
│  └─ 纯英文 → OpenAI text-embedding-3-large
├─ 自托管（隐私 / 成本）
│  ├─ 中文为主 → BGE-large-zh-v1.5
│  ├─ 中英混合 → BGE-M3
│  └─ 纯英文 → bge-large-en-v1.5
└─ 垂直领域 → 微调 + 自托管
```

下一节：[向量数据库](#vector-db) —— 几亿条向量怎么存怎么查。
