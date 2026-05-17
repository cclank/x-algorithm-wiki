# Wiki Log

> 所有 wiki 操作的按时间顺序记录。只追加,不修改。
> 格式:`## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> 当此文件超过 500 条时,轮换:重命名为 `log-YYYY.md`,重新开始。

## [2026-05-16] create | Wiki initialized
- Domain: X For You 推荐算法(`xai-org/x-algorithm` 开源仓库,commit `0bfc279`)
- 创建 SCHEMA.md(x-algorithm 专属标签体系)、log.md、.gitignore、.obsidian 配置
- 目标结构:16 概念页 + 5 实体页,对标 OpenClaw-wiki 深度

## [2026-05-16] create | 21 pages from source
- 概念页(16):system-architecture、candidate-pipeline-framework、home-mixer-orchestration、
  scoring-and-ranking、filtering-pipeline、thunder-in-network-store、thunder-kafka-ingestion、
  ads-blending、phoenix-retrieval、phoenix-ranking、candidate-isolation-masking、grok-transformer、
  hash-based-embeddings、grox-architecture、grox-classifiers、multimodal-embedders
- 实体页(5):candidate-pipeline、recsys-model、recsys-retrieval-model、post-store、run-pipeline
- 每页结论追溯到 x-algorithm 源码,附文件:行号锚点;总计 4900+ 行

## [2026-05-16] lint | 全量源码核对
- 21 页全部与组件级源码逐一核对验证,结论与源码一致
- 交叉链接检查:全部 [[wiki-link]] 目标存在,无悬空链接
- 记录 3 处源码与官方文档的出入(mini 模型尺寸、打分器数量、候选隔离掩码),详见 changelog

## [2026-05-16] create | index、README、changelog
- 创建 index.md(分类目录)、README.md(badges + 目录 + 统计)
- 创建 changelog/2026-05-16-initial-creation.md

## [2026-05-17] create | 白话导览(guide/,4 页)
- 反馈:原 21 页技术性/代码性偏强,缺"快速理解"层
- 新增 guide/ 页面类型(零代码、多类比):how-it-works、the-five-components、glossary、faq
- SCHEMA.md 增 guide 类型与「Guide Pages」章;index.md / README.md 增「白话导览」分类
- system-architecture.md 相关页面增到 how-it-works 的链接
- 创建 changelog/2026-05-17-plain-language-guide.md
