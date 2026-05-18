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

## [2026-05-17] update | 迷思三「破圈」深化
- 反馈:operating-myths 迷思三只讲了排序的 OON 折扣,没说透
- 补上更关键的第一道关——召回:站外内容靠双塔相似度 top-K,泛内容向量"对谁都不够像",进不了 top-K(recsys_retrieval_model.py:381-388)
- 迷思三重写为"窄门(召回)+ 折扣(OON)"两道关;点明"做泛内容破圈"在召回这关方向就反了
- 同步更新:x-algorithm-运营迷思.md 长文迷思三、guide/posting-guide.md「破圈」节、operating-myths 出处表/相关页面/sources

## [2026-05-17] update | operating-myths:删冗节、深层机制补例
- 反馈:「怎么认出一篇"真解读"」一节属媒体批评、与算法主题无关 → 删除
- 反馈:「深层机制」节补案例 → 表格由 3 列改 4 列,7 个机制各加一个具体例子

## [2026-05-17] update | operating-myths:补「总结」节 + 例子纠偏
- 反馈:页面缺最终总结 → 末尾新增「总结:六个迷思,错在同一处」(六迷思对照表 + 结论:算法是传导线、不是守门人)
- 反馈:Grox 例子被误读成"一次性盖章" → 改为准确表述(异步旁路管线、不在 feed 请求路径上;核 grox-architecture)
- 候选隔离例子补"同一个用户"前提,消除歧义

## [2026-05-18] update | 质量核查:system-architecture / home-mixer-orchestration / ads-blending
- 逐行核对三页全部源码锚点(正文内联 + 「源码锚点」一节)对 commit 0bfc279
- system-architecture.md:核对约 25 个锚点,函数名/行号/常量/行为全部一致,未改动
- home-mixer-orchestration.md:补全 4 处组件内相对路径(blender_selector/query/candidate/user_features → 加 home-mixer/ 前缀);修正 get_debug_scored_posts 描述——force_sample 在 server.rs:236-267,build_debug_json 才是 scored_posts_server.rs:115-132;为 feature switches 补一句术语解释
- ads-blending.md:补全 3 处组件内相对路径(blender_selector/brand_safety/util → 加 home-mixer/ 前缀);PartitionOrganic.enforcement 指标描述由变量名 bsr_drop 改为实际 action 标签值 drop;为 mermaid 图中 "tweet_id ≥ PTOS 截止" 补一句说明(雪花 ID 比大小等价于比发布时间)

## [2026-05-18] lint | 余下 14 页逐行源码重核 + 晦涩处补人话
- 承接上一条:对其余 14 页技术页(9 概念 + 5 实体)逐个源码锚点核验 commit 0bfc279
- 机械层:全 29 页 482 锚点全部指向真实文件与有效行号、无悬空链接、frontmatter 完整、统计一致
- 修正实质问题:thunder-in-network-store 代码块锚点 21-41→21-46;grok-transformer 3 处 README.md:5→phoenix/README.md:5(移植与 scaling 说明实在 phoenix README);grox-classifiers BangerInitialScreenResult 补回漏列字段 is_image_editable_by_grok;grox-architecture 2 处组件相对路径补全
- 晦涩处补约 13 句外科手术式人话/示例:RoPE 旋转直觉、线性同余哈希、multi-hot 动作向量、2*actions-1、-INF 掩码、argpartition 分步、PTOS 雪花 ID、feature switches、DELETE_EVENT_KEY、ASR、嵌入占位符 等
- 结论:全量核查未发现源码与 wiki 结论的实质性偏差

## [2026-05-18] update | faq 增"恶意刷不感兴趣"问答
- 读者问:被恶意刷"不感兴趣"会不会害到自己
- faq 新增一条:打分用的是模型对每个浏览者的预测、非事件计数;RankingScorer 无"按某帖负反馈次数扣分"路径;刷负反馈改不了你的帖给第三方的分;边界——训练管线不在开源仓库
- 收紧"举报会压制吗"答案里"举报多→分数低"的模糊措辞,改为"模型预测、非计数"

## [2026-05-18] create | 话题扩充:5 新页 + operating-myths 增 3 迷思
- 反馈:列出"还值得写的话题",获准做 A/B/C 三组
- B 组并入 operating-myths(六迷思 → 九迷思):迷思七 外链降权、迷思八 Premium 加权、迷思九 特定账号后门 —— 均逐条对源码(grep elon/musk 零命中、22 权重无订阅/外链项)
- operating-myths 迷思二补「预测 ≠ 计数」澄清(承接读者对"恶意刷不感兴趣"的疑问)
- A 组 3 新页(guide):visibility-and-shadowban、new-account-cold-start、your-data
- C 组 2 新页:end-to-end-dataflow(concept)、open-source-vs-production(guide)
- 5 新页由 5 个并行 agent 按源码核验创建,逐页复核源码锚点;index/README 更新为 34 页(6800+ 行)
- 创建 changelog/2026-05-18-topic-expansion.md
