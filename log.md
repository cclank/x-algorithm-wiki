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

## [2026-05-17] update | 白话导览补「出处」
- 反馈:白话页核心结论也要注明出处、有迹可循
- 4 页白话导览补 `sources` frontmatter(列真实源码文件)与「出处」章节
- how-it-works / the-five-components:出处表把核心结论对应到技术页 + 关键源码文件
- glossary / faq:出处说明 + 借「详见」链到带源码锚点的技术页;faq 补全 2 处缺失链接
- SCHEMA.md「Guide Pages」增"核心结论须可追溯"规定

## [2026-05-17] create | 选帖过程页(技术 + 白话各 1)
- 反馈:wiki 缺"如何选择帖子、选帖过程"专页 —— 原内容散在 candidate-pipeline-framework / candidate-pipeline / filtering-pipeline / home-mixer-orchestration
- 新增 concepts/candidate-selection.md(技术页):Selector trait「排序+截断」、TopKScoreSelector、选后水合→过滤→截断、BlenderSelector
- 新增 guide/how-posts-are-picked.md(白话页):选秀收尾类比,附「出处」表
- index.md / README.md 更新为 27 页;6 个相关页补 [[candidate-selection]] / [[how-posts-are-picked]] 交叉链接
- 创建 changelog/2026-05-17-candidate-selection.md

## [2026-05-17] create | 运营迷思 vs 源码真相(打脸页 + 站外长文)
- 反馈:网上 95% 的 X 算法解读是 AI 同质化废话、没翻过源码;要一份带行号、能打脸的高价值内容
- 新增 guide/operating-myths.md:六个流行运营迷思(多发帖/多互动/破圈/套模板/被大V挤掉/万能攻略)逐条对源码行号,附深层机制清单与"如何识别真解读"方法论
- 新读源码核对:ranking_scorer.rs(作者多样性衰减、22 行为/5 负权重、OON 降权)、vm_ranker.rs、phoenix/grok.py(候选隔离因果掩码)、顶层 README
- 配套站外可发布长文:/Users/lank/code/x-algorithm-运营迷思-源码打脸.md(不在 wiki 仓库,供对外发布)
- index.md / README.md 更新为 28 页;6 个相关页补 [[operating-myths]] 交叉链接
- 创建 changelog/2026-05-17-operating-myths.md

## [2026-05-17] create | 发帖指南(基于全算法机制)
- 反馈:基于所有算法机制,出一页发帖指南,涵盖要点与技巧,必要时配例子
- 新增 guide/posting-guide.md:从召回/排序/过滤/候选隔离/Grox 各机制反推发帖建议,每条对源码行号;含正向信号表、扣分项、破圈、发帖节奏、反面清单、一个完整 before/after 例子
- 与 operating-myths 配对(立/破);每条建议标机制出处,单列「边界」说明算法只分发不创作
- index.md / README.md 更新为 29 页;6 个相关页补 [[posting-guide]] 交叉链接
- 创建 changelog/2026-05-17-posting-guide.md
