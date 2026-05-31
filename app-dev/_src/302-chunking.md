---
group: 3. RAG 检索增强
id: chunking
title: RAG · 切片策略
toc: RAG · 切片
---

**切片决定了 RAG 的天花板** —— 切得不好，后面 Embedding 再强、Reranker 再准也救不了。

## 为什么切片是 RAG 的命门

```
完整文档（10000 字）
   ↓ 切片
[ 片段 1 ] [ 片段 2 ] ... [ 片段 N ]
   ↓ Embedding
[ 向量 1 ] [ 向量 2 ] ... [ 向量 N ]
   ↓ 检索
返回 top-K 个最相关片段
   ↓
拼到 prompt 给 LLM
```

**核心矛盾**：
- 切太大：单个片段包含太多无关内容，检索精度差，浪费 context
- 切太小：相关上下文被割裂，检索到了也不完整

举个例子：

```
文档原文（不切）:
"我们的退款政策如下。
普通商品：7 天无理由退货。
特殊商品：拆封后不可退（如内衣、化妆品）。
售后联系：support@xx.com。"

问题: "化妆品能退吗？"

切片 A（粗切 - 整段一片）:
召回 → 整段 → 答案准确

切片 B（细切 - 一句一片）:
召回 → "特殊商品：拆封后不可退（如内衣、化妆品）"
     → 缺少"退款政策"上下文 → 模型可能误解
```

## 6 种主流切片策略

### 策略 1：固定大小切片（Fixed Size）

最简单。按字符/token 数硬切。

```python
def fixed_chunking(text, chunk_size=500, overlap=50):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks
```

✅ **优点**：实现简单、可预测、对所有文档都能用
❌ **缺点**：可能切断完整段落、表格、代码块

适合：连续叙述类文本（小说、新闻、纯说明文）。

### 策略 2：按句子/段落切（Sentence/Paragraph）

按自然边界切。

```python
import re

def paragraph_chunking(text, max_size=500):
    # 按段落切（双换行）
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    for p in paragraphs:
        if len(current) + len(p) <= max_size:
            current += "\n\n" + p
        else:
            if current: chunks.append(current.strip())
            current = p
    if current: chunks.append(current.strip())
    return chunks
```

✅ **优点**：保留语义完整性
❌ **缺点**：段落长度差异大；某段过长仍要二次切

### 策略 3：递归切片（Recursive Character）

LangChain 推荐的方式。按**多级分隔符**优先尝试：

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", ".", " ", ""]  # 按优先级
)
chunks = splitter.split_text(text)
```

逻辑：先按 `\n\n` 切，太长再按 `\n`，再太长按句号，最后按字符。

✅ **优点**：兼顾语义完整 + 长度可控（业界默认选择）
❌ **缺点**：跨标题/章节切断时仍可能丢上下文

### 策略 4：基于文档结构（Structure-Aware）

利用 Markdown / HTML 等结构。

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
)
chunks = splitter.split_text(md_text)
# 每个 chunk 自带 metadata: {"Header 1": "...", "Header 2": "..."}
```

✅ **优点**：保留文档层次结构、可作为 metadata 用于过滤
❌ **缺点**：只适用于结构化文档

### 策略 5：语义切片（Semantic Chunking）

用 Embedding 判断**相邻句子的语义距离**，距离大的地方切。

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain.embeddings import HuggingFaceEmbeddings

embedder = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
splitter = SemanticChunker(
    embeddings=embedder,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=95  # 语义距离前 5% 的位置切
)
chunks = splitter.create_documents([text])
```

✅ **优点**：切在真正的话题转换处，召回精度高
❌ **缺点**：计算量大（每对相邻句都要算 embedding）、超参难调

适合：质量优先、不在乎离线计算时间。

### 策略 6：Late Chunking（2024 新方法）

**Jina AI 2024 提出的新范式** —— 颠覆传统流程：

```
传统流程:
切片 → 每片单独 Embed → 入库

Late Chunking:
整篇 Embed（保留全文上下文）→ 在向量层面切 → 入库
```

效果：每个 chunk 的向量都"知道"全文上下文，**召回准确率提升 5-15%**。

```python
# 用支持 Late Chunking 的模型
from jina import Client
c = Client(host="https://api.jina.ai/v1")

resp = c.post(
    on="/embed",
    inputs={"text": long_document, "late_chunking": True}
)
# 返回多个 chunk 向量，每个都带全文上下文
```

适用：长文档（论文、技术手册），上下文非常关键的场景。

## 切片大小怎么选

经验值：

| 场景 | chunk_size | overlap |
|------|-----------|---------|
| 法律 / 政策文档 | 300–500 | 50 |
| 技术文档 / API 文档 | 500–800 | 100 |
| 学术论文 | 800–1200 | 150 |
| 客服对话 / FAQ | 200–400 | 30 |
| 代码 | 函数级别（不按字符）| 0 |
| 表格数据 | 整行 | 0 |

**通用调参法**：先按 500/50 跑评测，准确率不够再调。

## 几个常见误区

### 误区 1：overlap 越大越好？
不是。overlap 太大会让相邻 chunk 高度相似，检索 top-K 时容易召回重复内容。**经验值 10–20%**。

### 误区 2：所有文档用同一切片策略？
不行。技术文档用结构切，新闻用递归切，代码必须按函数切。**按文档类型分别处理**。

### 误区 3：切完就完事？
还要**清洗** —— 去掉页眉页脚、广告、空段、目录。这些垃圾 chunk 会污染检索结果。

```python
def clean_chunk(chunk):
    # 过滤过短
    if len(chunk.strip()) < 50: return None
    # 过滤目录类（连续短句）
    if chunk.count(".") > 20 and len(chunk) < 200: return None
    # 过滤页码
    chunk = re.sub(r'第\s*\d+\s*页', '', chunk)
    return chunk
```

### 误区 4：忘了保留 metadata
chunk 入库时**必须带 metadata**：

```python
chunk_metadata = {
    "doc_id": "policy_2025_v3",
    "section": "退款政策",
    "page": 12,
    "url": "https://internal/policy/12",
    "updated_at": "2025-10-15",
    "permission_level": "all_employees"
}
```

用途：
- **检索过滤**：只查特定部门 / 时间范围
- **引用追溯**：告诉用户来源
- **权限控制**：按用户角色筛选

## 特殊文档的切片技巧

### PDF 含表格

```python
# 表格单独提取，转 Markdown 再 embed
import camelot
tables = camelot.read_pdf("doc.pdf", pages="all")
for table in tables:
    md_table = table.df.to_markdown(index=False)
    chunks.append(md_table)  # 整张表作为一个 chunk
```

### 代码库

```python
# 按函数 / 类切片，不按行数
from tree_sitter import Language, Parser

def split_code(code, language="python"):
    parser = Parser(Language(...))
    tree = parser.parse(code.encode())
    chunks = []
    for node in tree.root_node.children:
        if node.type in ("function_definition", "class_definition"):
            chunks.append({
                "code": code[node.start_byte:node.end_byte],
                "type": node.type,
                "name": extract_name(node)
            })
    return chunks
```

### 长 PDF（白皮书 / 论文）

两阶段切片：
1. 先按章节切大块（保留层次）
2. 大块内再按段落细切
3. 元数据保留章节路径："Chapter 3 / Section 2 / Para 5"

## 切片质量评测

简单方法：

```python
def evaluate_chunking(test_questions, chunks):
    """对每个测试问题，看是否有 chunk 包含答案"""
    hits = 0
    for q, gold_answer in test_questions:
        # 简单字符串匹配（更精确可用 LLM-as-Judge）
        if any(gold_answer in c for c in retrieve(q, chunks, top_k=3)):
            hits += 1
    return hits / len(test_questions)
```

如果命中率低 → 重新设计切片策略。

## 总结：切片决策树

```
你的文档是什么？
├─ Markdown / 有清晰标题
│  → 用 MarkdownHeaderTextSplitter
├─ PDF / Word（含表格）
│  → unstructured / llamaparse 解析后递归切
├─ 代码
│  → 按函数/类切（tree-sitter）
├─ 长文档（论文 / 手册）
│  → 两阶段切（章节 → 段落）+ Late Chunking
└─ 其他
   → RecursiveCharacterTextSplitter (chunk_size=500, overlap=50)
```

下一节：[Embedding 选型](#embedding) —— 切完之后用哪个模型转向量。
