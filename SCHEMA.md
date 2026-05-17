# Wiki Schema

## Domain
X For You 推荐算法 —— X(Twitter)"For You" 信息流推荐系统的架构与实现细节。覆盖 home-mixer 编排层、candidate-pipeline 流水线框架、Thunder 站内帖子内存库、Phoenix ML(双塔召回 + Grok transformer 排序)、Grox 内容理解服务、广告混排。基于 `xai-org/x-algorithm` 开源仓库源码(2026-05-15 release,commit `0bfc279`)。

## Conventions
- 文件名:小写 + 连字符,无空格(如 `phoenix-ranking.md`)
- 每个 wiki 页面必须以 YAML frontmatter 开头
- 使用 wiki 双向链接(如 `[[phoenix-retrieval]]`)连接页面;每页正文至少 2 个出站链接
- 更新页面时必须更新 frontmatter 的 `updated` 日期
- 新页面必须添加到 `index.md` 对应分类下
- 每个操作必须追加到 `log.md`
- 结论只来自已核验源码,未验证的内容不写入页面;不确定处明确标注
- 源码引用使用 x-algorithm 仓库相对路径(如 `phoenix/recsys_model.py`、`home-mixer/scorers/weighted_scorer.rs`),并尽量附行号或关键函数 / 结构体名
- 正文用中文;代码、标识符、文件路径保持原文

## Frontmatter
```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | guide | changelog
tags: [来自下方分类法]
sources: [phoenix/recsys_model.py, home-mixer/scorers/weighted_scorer.rs]
---
```

- `sources` 列出该页面主要依据的源码文件路径(x-algorithm 仓库相对路径)

## Tag Taxonomy
- **架构**: architecture, pipeline, data-flow, component, framework, two-stage, overview
- **编排(home-mixer)**: home-mixer, orchestration, candidate-pipeline, query-hydrator, source, hydrator, selector, side-effect, grpc
- **候选源**: in-network, out-of-network, thunder-source, phoenix-source, ads-source
- **召回**: retrieval, two-tower, user-tower, candidate-tower, ann, similarity-search, corpus
- **排序**: ranking, scoring, weighted-scorer, author-diversity, oon, multi-action, candidate-isolation
- **模型**: phoenix, grok, transformer, attention, rope, rmsnorm, glu, gqa, embedding, hashing, jax, haiku
- **站内库(Thunder)**: thunder, post-store, in-memory, kafka, ingestion, retention, deserialization
- **内容理解(Grox)**: grox, content-understanding, classifier, spam, safety, ptos, banger, reply-ranking, embedder, multimodal, vlm, task, plan, dispatcher
- **广告**: ads, blending, brand-safety, safe-gap
- **过滤**: filter, visibility-filtering, dedup, social-graph
- **基础设施**: rust, python, grpc, kafka, strato, async
- **Meta**: changelog, guide, overview, glossary, faq

## Page Thresholds
- **创建页面**:当某个实体 / 概念是一个子系统的核心,或在多个源码文件中出现
- **更新已有页面**:当源码细节涉及已覆盖的内容时
- **不创建页面**:对于偶然提及、次要细节或超出领域的内容
- **拆分页面**:超过 ~700 行时拆分为子主题并交叉链接
- **归档页面**:内容被完全取代时移至 `_archive/`,从 index 中移除

## Entity Pages
针对具体代码构件(结构体 / 类 / 关键函数 / 可运行入口)。每个实体一页,包括:
- 概述 / 是什么
- 关键事实(文件路径、类型 / 结构体定义、关键函数签名、常量值)
- 与其他实体 / 概念的关系(使用 wiki 双向链接)
- Mermaid 图(流程或结构,适用时)
- 设计决策(决策点 / 选择 / 理由 表格)
- 源码锚点(文件路径 + 行号或关键函数名)
- 相关页面(语义化交叉引用,作为最后一章)

## Concept Pages
针对一个架构概念 / 子系统 / 机制。每个概念一页,包括:
- 定义 / 该页回答什么问题
- 核心结论
- 已验证结构(架构、数据流、关键模块)—— 配实际代码片段、真实常量值
- Mermaid 图(辅助说明复杂流程)
- 设计决策(决策点 / 选择 / 理由 表格)
- FAQ(复杂页面,2-4 条,可选)
- 源码锚点(文件路径 + 行号或关键函数名)
- 相关页面(语义化交叉引用,作为最后一章)

## Guide Pages
面向"快速理解"的白话页,位于 `guide/`。不替代 concept / entity 技术页,而是作为通俗入口层。每页:
- 用大白话与类比讲清,**不放代码、不放公式**
- 配 Mermaid 图(适用时)
- 关键处链接到对应的 concept / entity 技术页,供读者深入
- frontmatter `type: guide`

## Update Policy
当新信息与已有内容冲突时:
1. 检查日期 —— 较新源码通常覆盖旧源码
2. 如果确实矛盾,同时记录两种说法并注明来源
3. 在 frontmatter 中标记:`contradictions: [page-name]`
4. 在 `log.md` 中记录供审核
