---
group: 3. RAG 检索增强
id: advanced-rag
title: RAG · 进阶模式
toc: RAG · 进阶
---

标准 RAG 解决 80% 的场景。这一章讲剩下 20% —— **Self-RAG / GraphRAG / Agentic RAG / 多模态 RAG / RAG 评测**。

## 1. Self-RAG：让模型自我反思

**问题**：标准 RAG 是「**先检索后回答**」，但有时检索的根本不相关，模型就会基于无关内容编答案。

**Self-RAG 的思路**：让模型**自己判断要不要检索、检索内容相关吗、要不要再检索**。

```
用户问题
   ↓
[判断 1] 这个问题需要检索吗？
   │
   ├─ 不需要（如"今天星期几"）→ 直接回答
   │
   └─ 需要 → 检索
       ↓
   [判断 2] 检索到的内容相关吗？
       │
       ├─ 相关 → 用这些内容回答
       │
       └─ 不相关 → 重新检索（改 query）或拒答
       ↓
   生成回答
       ↓
   [判断 3] 回答有事实依据吗？
       │
       ├─ 有 → 输出
       │
       └─ 没有 → 重新生成 或 标注"未确认"
```

### 实现（用 LangGraph）

```python
from langgraph.graph import StateGraph
from typing import TypedDict

class RAGState(TypedDict):
    question: str
    documents: list
    answer: str
    needs_retrieval: bool
    documents_relevant: bool

def decide_retrieve(state):
    """判断是否需要检索"""
    resp = llm.invoke([{
        "role":"user",
        "content": f"以下问题是否需要查询知识库？回答 yes/no:\n{state['question']}"
    }])
    return {"needs_retrieval": "yes" in resp.content.lower()}

def retrieve(state):
    docs = vector_db.search(state["question"], top_k=5)
    return {"documents": docs}

def grade_documents(state):
    """评估文档相关性"""
    grades = []
    for doc in state["documents"]:
        resp = llm.invoke([{
            "role":"user",
            "content": f"文档是否与问题相关？yes/no\n问题:{state['question']}\n文档:{doc}"
        }])
        grades.append("yes" in resp.content.lower())
    relevant = [d for d, g in zip(state["documents"], grades) if g]
    return {"documents": relevant, "documents_relevant": len(relevant) > 0}

def generate(state):
    context = "\n".join(state["documents"])
    resp = llm.invoke([{"role":"user","content": f"基于材料回答:\n{context}\n\n问题:{state['question']}"}])
    return {"answer": resp.content}

# 构建图
graph = StateGraph(RAGState)
graph.add_node("decide", decide_retrieve)
graph.add_node("retrieve", retrieve)
graph.add_node("grade", grade_documents)
graph.add_node("generate", generate)

graph.set_entry_point("decide")
graph.add_conditional_edges(
    "decide",
    lambda s: "retrieve" if s["needs_retrieval"] else "generate"
)
graph.add_edge("retrieve", "grade")
graph.add_conditional_edges(
    "grade",
    lambda s: "generate" if s["documents_relevant"] else "retrieve"  # 不相关就重试
)
graph.add_edge("generate", END)

app = graph.compile()
result = app.invoke({"question": "公司年假政策？"})
```

**适用**：高质量问答场景（医疗、法律、金融），错答代价大。

## 2. GraphRAG：基于知识图谱的 RAG

**问题**：标准 RAG 只能找「**这段文字相关吗**」，无法回答「**跨文档的关系推理**」。

**例子**：「张三和李四的关系？」需要从多份文档拼出关系链。

**GraphRAG 的思路**：先**从文档构建知识图谱**，检索时用图查询替代/补充向量检索。

```
文档库
   ↓
[实体抽取] 提取人名、组织、事件、概念
[关系抽取] 提取"任职"、"投资"、"合作"等关系
   ↓
知识图谱
   ↓
查询时：
  - 向量检索（找相关文档）
  - 图查询（找实体关系）
  - 融合后生成答案
```

### Microsoft GraphRAG

微软开源的实现：

```bash
pip install graphrag

# 1. 索引（耗时长，要调多次 LLM）
graphrag index --root ./project

# 2. 查询
graphrag query --root ./project \
    --method local \
    --query "张三在公司的角色变化？"
```

GraphRAG 的两种查询模式：
- **Local Search**：聚焦特定实体，问"X 是什么"
- **Global Search**：跨文档汇总，问"公司整体战略是什么"

### 适用场景

- **企业知识图谱**：员工 / 项目 / 客户关系
- **医疗记录**：病人 / 症状 / 治疗历史
- **学术文献**：作者 / 论文 / 引用关系
- **金融分析**：公司 / 高管 / 投资关系

### 缺点

- **构建成本极高**：每篇文档都要调 LLM 抽取实体关系
- **更新慢**：新增文档要重新更新图
- **小数据量收益低**：< 100 篇文档不值得

## 3. Agentic RAG：让 Agent 自主决策检索

更进一步 —— **让 LLM Agent 自己选择用什么检索方式**。

```
用户问题
   ↓
Agent 决策树:
  - 需要查向量库？→ 调 vector_search 工具
  - 需要查实时数据？→ 调 web_search 工具
  - 需要查内部 API？→ 调 api_call 工具
  - 需要计算？→ 调 calculator 工具
   ↓
基于多源结果综合回答
```

### 实现：把检索包成 Function Call

```python
tools = [
    {
        "name": "internal_doc_search",
        "description": "搜索公司内部文档（HR政策、产品手册、技术文档）",
        "input_schema": {...}
    },
    {
        "name": "web_search",
        "description": "搜索互联网公开信息（新闻、当前事件）",
        "input_schema": {...}
    },
    {
        "name": "database_query",
        "description": "查询业务数据库（订单、用户、库存）",
        "input_schema": {...}
    }
]

# LLM 自主决策调哪个工具
agent = create_agent(tools=tools)
answer = agent.invoke("查最新的 GPT-5 价格，然后比较我们公司当前用的模型成本")
# Agent 会自动：
# 1. 调 web_search 查 GPT-5 价格
# 2. 调 database_query 查公司账单
# 3. 综合生成对比答案
```

适用：复杂、多源、模糊的查询需求。

详见 [Agent 章节](#agent-concept)。

## 4. 多模态 RAG

**纯文本 RAG 不够** —— 文档里有图、表格、视频、音频。

### 处理 PDF 中的图表

```python
# 用 llamaparse 提取（含图表识别）
from llama_parse import LlamaParse

parser = LlamaParse(api_key=os.getenv("LLAMA_CLOUD_KEY"))
docs = parser.load_data("technical_paper.pdf")

# 表格自动转 Markdown
for doc in docs:
    if "table" in doc.metadata:
        # doc.text 已是 Markdown 表格
        ...
```

### 多模态 Embedding

直接 embed 图片或图文混合：

```python
# Cohere multimodal v3
import cohere
co = cohere.Client()

resp = co.embed(
    texts=["这是技术架构图"],
    images=[image_bytes],  # 同时 embed 图像
    model="embed-english-v3.0",
    input_type="search_document"
)
```

模型推荐：
- **Cohere embed-multimodal-v3**
- **Voyage multimodal-3**
- **Jina CLIP-v2**

### 实战架构

```python
# 多模态文档入库
for page in pdf.pages:
    # 提取文字
    text = page.text
    text_emb = embed_text(text)

    # 提取图片
    for img in page.images:
        # 图片向量
        img_emb = embed_image(img)
        # 同时让 LLM 描述图片，做文本 fallback
        caption = vlm.describe(img)

    # 入库（多个向量字段）
    db.add({
        "page": page.num,
        "text": text,
        "text_emb": text_emb,
        "image_emb": img_emb,
        "image_caption": caption
    })
```

## 5. RAG 评测：怎么知道效果好不好

「**没评测的优化等于猜**」。RAG 必须有评测体系。

### 评测的 4 个维度

```
┌──────────────────────────────────────┐
│  ① 检索质量                            │
│    - Hit Rate@K: 相关文档在 top-K 吗  │
│    - MRR: 第一个相关文档的位置         │
│    - NDCG: 综合排序质量                │
│                                       │
│  ② 答案质量                            │
│    - Faithfulness: 答案是否忠于材料    │
│    - Relevance: 答案是否回答了问题     │
│    - Completeness: 答案是否完整        │
│                                       │
│  ③ 鲁棒性                              │
│    - 无关问题能拒答吗                  │
│    - 故意误导能识别吗                  │
│                                       │
│  ④ 业务指标                            │
│    - 用户满意度（👍/👎）              │
│    - 转人工率                          │
│    - 平均响应时长                      │
└──────────────────────────────────────┘
```

### RAGAS：开源评测框架

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness, answer_relevancy,
    context_precision, context_recall
)
from datasets import Dataset

# 准备评测集
test_data = Dataset.from_dict({
    "question": ["公司有陪产假吗？", "病假最多请几天？"],
    "answer": [...],          # RAG 系统的回答
    "contexts": [[...], ...], # 检索到的片段
    "ground_truth": [...]     # 人工标注的标准答案
})

result = evaluate(
    test_data,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
)
print(result)
# {'faithfulness': 0.89, 'answer_relevancy': 0.92, ...}
```

4 个核心指标：

| 指标 | 含义 |
|------|------|
| **Faithfulness** | 答案是否仅基于检索到的材料 |
| **Answer Relevancy** | 答案是否切题 |
| **Context Precision** | 检索到的材料中相关的比例 |
| **Context Recall** | 应该检索到的材料是否都召回了 |

### LLM-as-Judge：自动化评测

```python
JUDGE_PROMPT = """你是 RAG 评测专家。

问题: {question}
标准答案: {ground_truth}
模型回答: {answer}
检索材料: {context}

请按 1-5 分评估：
1. 准确性: 回答与标准答案的事实一致程度
2. 完整性: 是否覆盖所有要点
3. 忠实度: 是否仅基于检索材料（无幻觉）
4. 相关性: 是否切题

输出 JSON: {{"accuracy": x, "completeness": x, "faithfulness": x, "relevance": x, "reasoning": "..."}}
"""

def llm_judge(question, gt, answer, context):
    resp = client.messages.create(
        model="claude-sonnet-4-5",  # 用强模型当裁判
        messages=[{"role":"user","content": JUDGE_PROMPT.format(...)}]
    )
    return json.loads(resp.content[0].text)

# 批量评测
scores = [llm_judge(q, gt, a, c) for q, gt, a, c in test_set]
avg_accuracy = sum(s["accuracy"] for s in scores) / len(scores)
```

### 评测集怎么构建

最少要有：

```
20-50 条标注用例:
  - 70% 正常问题（应该能答）
  - 20% 边界情况（模糊、复杂）
  - 10% 应拒答（知识库外、违规、敏感）

每条包含:
  - question
  - ground_truth (人工写的正确答案)
  - reference_docs (人工标的相关文档 ID)
```

**冷启动技巧**：上线后收集用户的真实问题 + 满意度反馈 → 滚动扩充评测集。

## 6. 总结：RAG 进阶路线图

```
基础 RAG（300-305 章已讲）
  ├─ 标准流水线
  ├─ Hybrid + Rerank
  └─ Query 改写
        ↓
进阶 RAG（本章）
  ├─ Self-RAG: 自我反思
  ├─ GraphRAG: 知识图谱
  ├─ Agentic RAG: 多源决策
  ├─ 多模态 RAG
  └─ 完整评测体系
        ↓
RAG-Agent 融合（下一站）
  └─ 见 Agent 章节
```

下一模块：[MCP 协议](#mcp-overview) —— 让工具集成标准化。
