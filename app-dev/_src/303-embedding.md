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

## 建立候选集与选型快照

本章保留 BGE、OpenAI、Cohere 等历史接口样例，不作为 2026 型号排名。不同 MTEB 版本、语言和数据的分数不能混排，自托管也有硬件和维护成本。

| 维度 | 记录内容 | 验收方法 |
|------|----------|----------|
| 版本与许可 | 模型 revision、SDK 与许可 | 固定制品和来源 |
| 语言与领域 | 中文、混合语言、业务术语 | 分任务 Recall@K、MRR 与错误分析 |
| 输入与表征 | 长度、维度、query/doc 模式、归一化 | 截断、前缀与向量空间契约测试 |
| 服务成本 | 批量、吞吐、延迟、硬件或 API 价格 | 实测并记录价格快照 |
| 迁移 | 文档重编码、索引与缓存版本 | 新旧索引对照、灰度和回退 |

候选应在自己的授权文档上比较，不能仅凭榜单决定检索效果。知识生命周期见[生产 RAG](307-rag-production.html)。

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
如果是**中英混合**：建立多语言候选，分别评测同语言和跨语言查询。
如果是**纯英文**：选 `voyage-3` / `text-embedding-3-large`

:::callout ⚠️
候选的语言表现可能不同，应分别报告中文、英文与混合任务，不承诺固定降幅。
:::

### 4. 微调能力

如果有垂直领域（医疗 / 法律 / 金融），考虑**微调**：

```python
# 用 sentence-transformers 微调
from sentence_transformers import InputExample, SentenceTransformer, losses
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

微调需要独立数据分区、代表性负例与通用能力回归，收益和样本需求依任务而定。

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
    dimensions=1024  # 该模型支持的维度选项，接入时核验。
)
embs = [d.embedding for d in resp.data]
```

降维可减少存储，质量和查询性能需要对照验证。查询与文档使用相同向量空间、维度及预处理版本。

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

距离按训练和输出归一化方式选择，不同度量的分数不能未经校准混合。

## Embedding 的 7 个最佳实践

### 1. 归一化（normalize）

让所有向量长度为 1，余弦距离 = 内积，计算更快。

```python
embs = model.encode(texts, normalize_embeddings=True)
```

### 2. 批量处理

按服务和硬件支持批量处理，实测吞吐、延迟、重试与限速，不预设加速倍数。

### 3. 缓存

同样的文本不要重复 embed。

```python
import hashlib
import diskcache

cache = diskcache.Cache("./emb_cache")

def cached_encode(text):
    """示意版本化向量缓存，真实服务还需租户隔离与撤权失效。"""
    key = hashlib.sha256(("demo-model-revision|normalize-v1|" + text).encode()).hexdigest()
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
    """该 BGE 样例使用查询前缀，具体字符串按模型卡核验。"""
    return model.encode("为这个句子生成表示以用于检索相关文章：" + q)

def encode_doc(d):
    """文档侧遵循相同模型的预处理契约。"""
    return model.encode(d)  # 文档不加 prefix
```

前缀按精确模型版本确认，不把某个 BGE 样例推广到整个系列。

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
