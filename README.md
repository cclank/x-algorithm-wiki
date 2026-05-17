# X For You 推荐算法 Wiki

<p align="center">
  <img src="https://img.shields.io/badge/Wiki-x--algorithm-blue?style=for-the-badge&logo=markdown" alt="Wiki" height="28">
  <img src="https://img.shields.io/badge/Source-xai--org%2Fx--algorithm-green?style=for-the-badge&logo=github" alt="Source" height="28">
  <img src="https://img.shields.io/badge/Knowledge_Base-25_pages-orange?style=for-the-badge&logo=obsidian" alt="Knowledge Base" height="28">
  <img src="https://img.shields.io/badge/Content-4900%2B_lines-purple?style=for-the-badge" alt="Content" height="28">
  <img src="https://img.shields.io/badge/Verified-Source_Code-brightgreen?style=for-the-badge" alt="Verified" height="28">
</p>

> 基于 `xai-org/x-algorithm` 开源仓库源码(commit `0bfc279`,2026-05-15 release)的深度架构知识库。
> 所有页面结论均追溯到源码,附 `文件:行号` 锚点;遵循 [LLM Wiki 模式](https://github.com/xai-org/x-algorithm)。

---

## 这是什么

X(Twitter)开源的 "For You" 信息流推荐系统由五大组件构成 —— 编排层、流水线框架、站内帖子库、ML 召回/排序、内容理解服务。本 wiki 把这套系统的架构与实现拆成 25 个相互链接的页面:**4 页零代码的「白话导览」** + 21 页源码级技术页。

- **想快速理解整套系统**:从白话导览读起 —— [how-it-works](guide/how-it-works.md)
- **想看技术细节**:入口页 [system-architecture](concepts/system-architecture.md)

---

## 目录

### 白话导览 · 先读这个(4 页,零代码)

- [how-it-works](guide/how-it-works.md) — 白话总览:一条帖子怎么一步步走进你的 For You
- [the-five-components](guide/the-five-components.md) — 五大组件速览:各组件是干嘛的、为什么需要它
- [glossary](guide/glossary.md) — 术语速查表:召回 / 排序 / 双塔 / 候选隔离… 一句话解释
- [faq](guide/faq.md) — 常见疑问:为什么刷到陌生人、广告怎么插进来、负反馈有什么用

### 总览(1 页)

- [system-architecture](concepts/system-architecture.md) — For You 端到端:两层流水线嵌套、十阶段、召回+排序、五大组件

### 在线服务 · Rust(5 页)

- [candidate-pipeline-framework](concepts/candidate-pipeline-framework.md) — 可复用流水线框架:7 个组件 trait、`enable()` 门、并行/顺序执行模型
- [home-mixer-orchestration](concepts/home-mixer-orchestration.md) — 编排层:两条嵌套流水线、两个 gRPC 服务、候选源、数据模型
- [scoring-and-ranking](concepts/scoring-and-ranking.md) — 3 个打分器:PhoenixScorer / RankingScorer(加权+多样性+OON)/ VMRanker
- [filtering-pipeline](concepts/filtering-pipeline.md) — 两道过滤:14 个预打分过滤器 + 3 个选后过滤器
- [ads-blending](concepts/ads-blending.md) — 广告混排:safe-gap / partition-organic 两策略、品牌安全四档裁定

### 站内库 · Thunder(2 页)

- [thunder-in-network-store](concepts/thunder-in-network-store.md) — 站内帖子内存库:三套时间线、gRPC 服务、信号量限流、时效打分
- [thunder-kafka-ingestion](concepts/thunder-kafka-ingestion.md) — Kafka 实时摄入:v1 feeder / v2 serving 双 listener、反序列化、保留期裁剪

### ML · Phoenix(5 页)

- [phoenix-retrieval](concepts/phoenix-retrieval.md) — 双塔召回:用户塔 + 候选塔、L2 归一化、点积 top-K
- [phoenix-ranking](concepts/phoenix-ranking.md) — Grok transformer 排序:`[用户|历史|候选]` 序列、多行为预测
- [candidate-isolation-masking](concepts/candidate-isolation-masking.md) — 候选隔离注意力掩码:候选互不可见,分数独立可缓存
- [grok-transformer](concepts/grok-transformer.md) — 移植自 Grok-1 的 transformer:RoPE、RMSNorm、GLU-FFN、GQA、软封顶,无 MoE
- [hash-based-embeddings](concepts/hash-based-embeddings.md) — 哈希嵌入:多哈希函数、统一嵌入表、reduce 投影

### 内容理解 · Grox(3 页)

- [grox-architecture](concepts/grox-architecture.md) — 内容理解服务:dispatcher/engine 三进程、Task/Plan DAG、PlanMaster
- [grox-classifiers](concepts/grox-classifiers.md) — 基于 VLM 的内容分类器:垃圾、安全/PTOS、banger 质量、回复打分
- [multimodal-embedders](concepts/multimodal-embedders.md) — 多模态帖子嵌入器:v5 主力(1024 维)与 v2 多模型实验型

### 实体参考(5 页)

- [candidate-pipeline](entities/candidate-pipeline.md) — `CandidatePipeline` 执行器 trait,`execute()` 十阶段编排
- [recsys-model](entities/recsys-model.md) — `PhoenixModel` 排序模型构件:配置、`block_*_reduce`、forward
- [recsys-retrieval-model](entities/recsys-retrieval-model.md) — `PhoenixRetrievalModel` 召回模型构件:CandidateTower、用户塔
- [post-store](entities/post-store.md) — Thunder 的 `PostStore` 结构体:三套 DashMap、写入/查询/裁剪
- [run-pipeline](entities/run-pipeline.md) — `run_pipeline.py` 端到端推理脚本:加载 → 召回 → 排序

---

## 统计信息

| 指标 | 数值 |
|------|------|
| **白话导览页** | 4 |
| **概念页面** | 16 |
| **实体页面** | 5 |
| **总行数** | 5200+ |
| **源码版本** | `xai-org/x-algorithm` @ `0bfc279`(2026-05-15 release) |
| **最后更新** | 2026-05-17 |

## 内容特点

- 每页含真实代码片段(Rust / Python)、真实常量值、函数签名
- 源码锚点附 `文件:行号`,结论可逐条追溯
- Mermaid 流程图辅助说明架构与数据流
- 每页附「设计决策」表,解释架构选型理由
- 复杂页面附 FAQ;统一「相关页面」交叉引用
- Wiki `[[links]]` 交叉链接,支持 Obsidian 导航
- 核对中发现的源码/文档出入已在 [changelog](changelog/2026-05-16-initial-creation.md) 记录
- 另有 4 页「白话导览」(`guide/`):零代码、多类比,面向快速理解,与技术页双向链接

## 使用方式

- **Obsidian 本地知识库**:用 Obsidian 打开本目录,即可用 `[[wiki-link]]` 导航与关系图谱
- **查询入口**:先读 [index.md](index.md) 定位相关页面,再读具体页
- **规则**:页面格式、标签体系、命名规范见 [SCHEMA.md](SCHEMA.md)

---

*本 wiki 基于 `xai-org/x-algorithm` 源码深度分析生成,非 xAI 官方文档。*
