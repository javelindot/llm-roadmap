---
group: 3. RAG 检索增强
id: hybrid-rerank
title: RAG · 混合检索 + Reranker
toc: RAG · 混合+Rerank
---

混合召回和重排是互补的候选优化：关键词匹配补充精确标识，重排在候选中估计相关性。收益依赖数据、标注与模型，不能承诺固定准确率提升。

## 混合召回解决什么问题

| 查询 | 需要保留的条件 | 候选方法 |
|------|----------------|----------|
| 查订单 demo-123 | 完整编号、当前用户权限 | 精确查询或关键词检索 |
| 如何催办异常订单 | 诉求、规则版本、订单类型 | 语义检索与关键词互补 |
| 某型号的价格 | 精确型号、生效日期与区域 | 型号匹配加有效版本过滤 |
| 概念的不同表达 | 缩写与全称的关系 | 语义检索、词表或受控改写 |

BM25 按词项相关性排序，也依赖分词和索引字段，不等于精确 ID 查询。对于订单编号等权威业务对象，优先使用授权业务接口。

```text
可信身份、原问题与有效版本
  -> 同一权限范围内的向量召回与关键词召回
  -> 使用统一文档/版本/chunk ID 融合与去重
  -> 复核权限和有效期 -> 重排候选
  -> 按预算装配完整证据与出处 -> 生成与引用检查
```

## RRF：按排名融合

Reciprocal Rank Fusion 使用各路的排名，而不是直接相加不可比较的 BM25 分数和向量相似度。以下代码只验证融合算法，不调用模型或检索服务：

```python
def reciprocal_rank_fusion(rank_lists, smoothing=60):
    """融合已经排序的统一证据 ID，返回 ID 与融合分数。

    每一路必须先完成权限、版本与检索范围的检查。
    同一路重复证据只计一次，避免重复记录放大该证据权重。
    不同路径都命中同一证据时累加其排名贡献。
    smoothing 是平滑参数，默认值仅作算法演示，应通过实验选择。
    分数仅用于排序，不是事实可信度或回答正确概率。
    """
    if type(smoothing) is not int or smoothing < 1:
        raise ValueError("positive smoothing required")
    scores = {}
    for ranks in rank_lists:
        seen = set()
        for rank, doc_id in enumerate(ranks, start=1):
            if not isinstance(doc_id, str) or not doc_id:
                raise ValueError("stable evidence ID required")
            # 同一路保留首次出现的排名，不重复累计同一条证据。
            if doc_id in seen:
                continue
            seen.add(doc_id)
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (smoothing + rank)
    # 平分时按稳定 ID 排序，避免实验结果依赖输入合并顺序。
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))


vector_hits = ["doc3", "doc1", "doc7", "doc2", "doc5"]
keyword_hits = ["doc1", "doc4", "doc3", "doc8", "doc7"]
fused = reciprocal_rank_fusion([vector_hits, keyword_hits])
print([doc_id for doc_id, _ in fused[:5]])
# ['doc1', 'doc3', 'doc7', 'doc4', 'doc2']
```

ID 应包含足够的信息区分版本和片段。关键词索引的数组位置不是向量库的业务 ID；将两者直接转成字符串，不会让它们自动对应同一证据。

不要先把融合结果放入 set 再截取前若干项，集合会丢失排名。多查询融合应明确各路的候选上限、去重与最终排序规则。

## 重排改善的是候选排序

常见 cross-encoder 联合读取 query 与证据，估计相关性；也有其他重排架构。重排无法恢复从未召回的材料，更不能创造不存在的政策。

| 选择 | 必须核对 |
|------|----------|
| 托管 Rerank API | 当前型号、SDK、输入上限、区域、计费与数据策略 |
| 自托管重排模型 | 语言与领域质量、硬件、批处理、截断与运维费用 |
| 不增加重排 | 当前排序是否已满足引用质量和响应时间 |

开源权重不代表运行免费。不能根据供应商品牌给出固定速度排名或无日期的价格表，应保存实际部署快照并在同一任务集比较。

先确定相关性标注与候选 Recall，再测重排后的 nDCG/MRR、最终证据 Recall 和引用支持率。重排分数通常不是经过校准的正确概率，不能直接用固定阈值决定“可以执行工单”。

## 查询改写要保留业务限定

| 方法 | 可能的收益 | 需要检查的错误 |
|------|------------|----------------|
| Multi-Query | 不同表达覆盖同一诉求 | 丢失型号、日期、国家、否定或对象条件 |
| HyDE | 用假设文档补充检索表达 | 把虚构答案变成事实，或偏离原意 |
| Step-back | 搜索更通用的规则 | 泛化后命中不适用的例外或历史条款 |

原问题保留为一路查询，生成的改写作为额外候选，并限制数量、长度和总时限。例如“目标型号在某区域的当前价格”不能直接改成“最新模型价格”，否则可能检索到另一型号。

HyDE 生成的是检索辅助文本，不能作为回答证据。改写前后的身份、授权过滤与有效期约束必须保持一致；原查询本就足够明确时，额外生成可能只增加时间和费用。

## 对照实验与故障定位

固定文档、权限、案例、模型和输入预算，比较纯向量、关键词、RRF、RRF 加重排，以及受限改写。至少报告：

- 授权范围内 Recall@K，注明 K 是召回候选数还是最终装配数。
- nDCG/MRR、引用支持率、答案正确与正确拒答。
- 过期材料、撤权后命中、精确型号混淆和跨租户泄露。
- 整个请求的 P95 时间与有效解决问题的成本。

没有召回有效材料时检查解析、切片、索引与查询；召回后被丢弃时检查重排和预算；材料充分但回答错误时检查生成与引用。不要用一个总体平均分决定应该购买更强重排服务。

向量库的内置混合接口按实际 SDK 版本接入；[向量数据库](304-vector-db.html)中的 query_points 示例和本章的纯算法示例属于不同验证范围。

参考：[Elasticsearch RRF](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion)、[检索架构](https://docs.langchain.com/oss/python/deepagents/retrieval)。继续阅读[Advanced RAG](306-advanced-rag.html)与[证据生命周期](307-rag-production.html)。
