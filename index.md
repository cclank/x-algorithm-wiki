# Wiki Index

> 内容目录。每个 wiki 页面按类型与分类列出,附一行摘要。
> 查询前先读此文件定位相关页面。
> Last updated: 2026-05-17 | Total pages: 25(4 guides + 16 concepts + 5 entities)| 5200+ lines

## 白话导览(Guide)

> 不想读代码、想快速理解整套系统?从这里开始 —— 这几页零代码、多类比。

- [[how-it-works]] — 白话总览:一条帖子怎么一步步走进你的 For You
- [[the-five-components]] — 五大组件速览:每个组件是干嘛的、为什么需要它
- [[glossary]] — 术语速查表:召回 / 排序 / 双塔 / 候选隔离… 一句话解释
- [[faq]] — 常见疑问:为什么刷到陌生人、广告怎么插进来、点"不感兴趣"有没有用

## 总览

- [[system-architecture]] — For You 信息流端到端:两层流水线嵌套、十阶段、召回+排序、五大组件

## Concepts

### 在线服务(Rust)

- [[candidate-pipeline-framework]] — 可复用流水线框架:7 个组件 trait、enable 门、并行/顺序执行模型
- [[home-mixer-orchestration]] — 编排层:两条嵌套流水线、两个 gRPC 服务、候选源、数据模型
- [[scoring-and-ranking]] — 3 个打分器:PhoenixScorer 取预测、RankingScorer 加权+多样性+OON、VMRanker
- [[filtering-pipeline]] — 两道过滤:14 个预打分过滤器 + 3 个选后过滤器
- [[ads-blending]] — 广告混排:safe-gap / partition-organic 两策略、品牌安全四档裁定

### 站内库(Thunder)

- [[thunder-in-network-store]] — 站内帖子内存库:三套时间线、gRPC 服务、信号量限流、时效打分
- [[thunder-kafka-ingestion]] — Kafka 实时摄入:v1 feeder / v2 serving 双 listener、反序列化、保留期裁剪

### ML — Phoenix

- [[phoenix-retrieval]] — 双塔召回:用户塔 + 候选塔、L2 归一化、点积 top-K
- [[phoenix-ranking]] — Grok transformer 排序:[用户|历史|候选] 序列、多行为预测
- [[candidate-isolation-masking]] — 候选隔离注意力掩码:候选互不可见,保证分数独立可缓存
- [[grok-transformer]] — 移植自 Grok-1 的 transformer:RoPE、RMSNorm、GLU-FFN、GQA、软封顶,无 MoE
- [[hash-based-embeddings]] — 哈希嵌入:多哈希函数、统一嵌入表、reduce 投影

### 内容理解(Grox)

- [[grox-architecture]] — 内容理解服务:dispatcher/engine 三进程、Task/Plan DAG、PlanMaster
- [[grox-classifiers]] — 基于 VLM 的内容分类器:垃圾、安全/PTOS、banger 质量、回复打分
- [[multimodal-embedders]] — 多模态帖子嵌入器:v5 主力(1024 维)与 v2 多模型实验型

## Entities

- [[candidate-pipeline]] — `CandidatePipeline` 执行器 trait,`execute()` 十阶段编排
- [[recsys-model]] — `PhoenixModel` 排序模型构件:配置、block_*_reduce、forward
- [[recsys-retrieval-model]] — `PhoenixRetrievalModel` 召回模型构件:CandidateTower、用户塔
- [[post-store]] — Thunder 的 `PostStore` 结构体:三套 DashMap、写入/查询/裁剪
- [[run-pipeline]] — `run_pipeline.py` 端到端推理脚本:加载 → 召回 → 排序

## Changelog

- [[2026-05-17-plain-language-guide]] — 新增 4 页白话导览(guide/),面向快速理解
- [[2026-05-16-initial-creation]] — 基于 xai-org/x-algorithm 源码深度分析,初始创建 21 页
