---
group: 3. RAG 检索增强
id: vector-db
title: RAG · 向量数据库
toc: RAG · 向量库
---

向量存储的选择取决于授权过滤、索引更新、实际查询、可用性和运维。仅凭文档条数，不能断言某个库满足延迟或容量要求。

## 候选方案与验证项

| 方案 | 适合讨论的条件 | 必须验证 |
|------|----------------|----------|
| 嵌入式索引/Chroma | 本地原型与简单部署 | 持久化、并发、过滤与备份 |
| pgvector | 已有 PostgreSQL，需复用事务与运维 | 过滤后 ANN 召回、查询计划与索引更新 |
| Qdrant / Weaviate | 专用检索服务与过滤需求 | 当前版本的稀疏/稠密能力、部署与租户隔离 |
| Milvus | 分布式检索与已有集群运维能力 | 副本、写入可见性、索引构建与恢复 |
| Elasticsearch | 已有关键词检索与业务过滤 | 向量/关键词融合、权限与版本契约 |
| 托管服务 | 希望减少基础设施维护 | 数据区域、限额、费用、导出和故障恢复 |

开源不意味着运行免费，托管也没有无限规模保证。建立向量维度、数据分布、过滤选择率、查询并发与更新频率的压测快照。

## 一个 Qdrant 接口示例

以下使用人工三维向量理解过滤与查询，不评估语义检索质量。安装并固定 qdrant-client 版本；不调用 Embedding 或大模型。SDK 集成需核对所选版本，本仓库本地测试不覆盖该外部库。

```python
from qdrant_client import QdrantClient, models

# 内存模式只用于示例，进程结束后数据不会保留。
client = QdrantClient(":memory:")
try:
    client.create_collection(
        collection_name="demo-docs",
        vectors_config=models.VectorParams(size=3, distance=models.Distance.COSINE),
    )
    client.upsert(collection_name="demo-docs", points=[
        models.PointStruct(id=1, vector=[1.0, 0.0, 0.0], payload={"tenant": "demo-a"}),
        models.PointStruct(id=2, vector=[1.0, 0.0, 0.0], payload={"tenant": "demo-b"}),
    ])
    # 租户来自可信会话，示例中固定为虚构租户，不能从模型参数读取。
    trusted_tenant = "demo-a"
    result = client.query_points(
        collection_name="demo-docs", query=[1.0, 0.0, 0.0], limit=3,
        query_filter=models.Filter(must=[
            models.FieldCondition(key="tenant", match=models.MatchValue(value=trusted_tenant)),
        ]),
    )
    print([point.id for point in result.points])  # [1]
finally:
    client.close()
```

真实权限还涉及用户、文档 ACL、生效版本与撤权。租户过滤只是示例的一层，不是完整访问控制。

## 索引与召回指标

| 索引 | 特征 | 需要测量 |
|------|------|----------|
| Flat | 对全部候选进行精确距离计算 | 容量、查询费用与延迟 |
| HNSW | 图近似搜索，空间与探索预算换召回 | 参数、构建时间、内存、过滤影响 |
| IVF | 分区后搜索有限候选 | 训练分布、分区与搜索参数 |
| PQ/其他量化 | 压缩表征，可能引入距离误差 | 存储、重评分与召回损失 |

ANN Recall 是相对同一向量空间的精确近邻召回，不是业务相关文档准确率。即使 Flat 找到全部真实近邻，错误 Embedding 或无效文档仍可能让答案失败。

## 更新与迁移

模型、维度、距离或预处理改变时，创建新索引版本并重编码。保持查询与文档空间一致，通过固定任务集比较后切换；保留回退与删除传播机制。

按租户分集合或共享集合加过滤，各有容量和管理成本。对共享集合检查过滤是在候选生成前还是后、是否造成召回损失、日志是否泄露其他租户。

索引成功写入不一定立即可查，使用所选库的可见性契约。变更应同时失效检索缓存、答案引用及其他衍生摘要。

## 压测与验收

测量 P50/P95/P99、吞吐、更新可见延迟、ANN Recall、业务 Recall@K、内存、磁盘、备份恢复和单任务费用。目标由业务 SLO 与基线设定，不使用无来源的通用毫秒数或百分比。

测试典型与极端过滤、删除、撤权、大文档、冷启动、索引构建和并发更新。量化和批处理收益按整体系统实测，不承诺固定倍数。

参考：[Qdrant 查询](https://qdrant.tech/documentation/concepts/search/)、[Qdrant Python SDK](https://python-client.qdrant.tech/)、[pgvector](https://github.com/pgvector/pgvector)。下一节：[混合召回与重排](305-hybrid-rerank.html)。
