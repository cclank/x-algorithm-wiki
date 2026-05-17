---
title: 运营迷思 vs 源码真相
created: 2026-05-17
updated: 2026-05-17
type: guide
tags: [guide, overview, myths, scoring, ranking]
sources: [README.md, home-mixer/scorers/ranking_scorer.rs, home-mixer/scorers/vm_ranker.rs, phoenix/grok.py, home-mixer/candidate_pipeline/phoenix_candidate_pipeline.rs]
---

# 运营迷思 vs 源码真相

> X 算法开源后,"涨号攻略"满天飞。这一页只做一件事:把最流行的几条运营说法,逐条拉到 `xai-org/x-algorithm` 源码前对质。
> 规矩:**每条结论都给 `文件:行号`**。给不出来的,就是没读过源码。

## 先打地基:这套系统到底怎么给帖子打分

一条帖子进你的 For You,要过两阶段:**召回**(从全网粗筛)→ **排序**(精细打分)。排序的核心是一个 Grok 改造来的 transformer,它对每条候选**预测 22 种行为概率**(点赞、回复、转发、点击、停留……以及"不感兴趣""举报"等负向行为)。`RankingScorer` 把这 22 个概率**加权求和**成最终分,再做两步调整:作者多样性衰减、站外降权。

一个定调的事实:README 第一段就写明 ——「我们删除了系统里**每一个**手工特征和**大部分**启发式规则」(`README.md:55`),"无手工特征"还是 Key Design Decision 第一条(`README.md:324-325`)。**打分/排序侧没有人工规则**,模型直接从用户的行为序列里学。这一条会反复用到。

> 想先看整体怎么运转:[[how-it-works]];打分细节:[[scoring-and-ranking]]。

## 六个流行迷思,逐条对源码

### 迷思一|「多发帖 = 多曝光」

**流行说法**:号要勤更新,一天多发几条,曝光自然涨。

**源码怎么说**:`RankingScorer` 第二步是**作者多样性衰减**(`ranking_scorer.rs:190-217`)。它先把候选按加权分降序排,再给每个作者记一个出现计数 `position`;同一作者第 N 次出现的帖子,分数乘 `diversity_multiplier = (1-floor)·decay^position + floor`(`ranking_scorer.rs:186-188`)。衰减因子 `decay`(`AuthorDiversityDecay`)小于 1 —— position 越大,乘数越小。第 0 条 ×1.0,第 1 条起就打折,越往后压得越狠,直到地板 `floor`。

**所以**:在同一次 For You 计算里,你发的内容里第一条机会最大,后面每一条都在被你自己的前一条压分。刷屏不是多曝光,是自我稀释。(注意边界:这是"单次信息流计算内"的衰减,不是账号级永久惩罚 —— 但方向很明确。)

### 迷思二|「互动量越高越好」

**流行说法**:想办法冲互动数据,点赞评论转发越多权重越高。

**源码怎么说**:最终分是 22 种**预测行为概率**的加权和(`ranking_scorer.rs:125-170`)。其中 5 个是负向行为 —— `not_interested`(点了"不感兴趣")、`block_author`、`mute_author`、`report`、`not_dwelled`(刷到没停留就划走),权重为负,汇成 `negative_sum = -(...)`(`ranking_scorer.rs:83`)。README 自己也写:负向行为「have negative weights, pushing down content the user would likely dislike」(`README.md:292`)。

**所以**:算法算的是"正向行为概率 − 负向行为概率"的加权结果,不是"互动总量"。靠标题党、骗点击换来的互动,如果同时招来大量"划走""不感兴趣""举报",加权分会被直接拉低甚至变负。反直觉的一点:**"没人理"不是最差的;"很多人划走/举报"才是最差的** —— `not_dwelled`("划走没停留")被显式建模成一个扣分项。

### 迷思三|「做泛内容就能轻松破圈」

**流行说法**:内容够好,算法自然把你推给全网陌生人。

**源码怎么说**:候选分**站内**(in-network,你关注的人)和**站外**(out-of-network)。`RankingScorer` 最后一步:站外候选的最终分要乘一个 OON 系数 `effective_oon`,站内候选不乘 —— `Some(false) => after_diversity * effective_oon`(`ranking_scorer.rs:272-275`)。系数取自 feature switch 参数(`OonWeightFactor`、话题场景的 `TopicOonWeightFactor`、新用户的 `NEW_USER_OON_WEIGHT_FACTOR`,见 `ranking_scorer.rs:220-239`)。

**所以**:系统结构上对站外内容设了一道折扣闸。破圈不是不可能,但你的站外帖子带着一个小于 1 的乘数,在和别人关注流里的内容竞争。对陌生受众,你得明显更强才追得平。(边界:具体系数值是线上参数,不在开源仓库 —— 能确定"机制是降权",不能说"降到几折"。)

### 迷思四|「套爆款模板 / 加特定关键词能骗算法」

**流行说法**:有一套"算法喜欢的"格式、词、结构,套上就涨。

**源码怎么说**:README 开宗明义删掉了打分侧**每一个**手工特征(`README.md:55, 324-325`)。排序靠 Grok transformer 直接读用户的行为序列学相关性 —— 打分模型里**没有**"这帖带没带某关键词""是不是某种格式"这类人工特征。系统里关键词唯一的角色,是**用户自己设的屏蔽词**(`MutedKeywordFilter`,命中即剔除,纯负向),不是创作者堆词的加分位。

**所以**:不存在"算法喜欢的格式"可被你套用,因为打分侧根本没有识别格式/关键词的特征。能"骗"的不是算法,是真实用户的行为 —— 模型预测的是"像这个用户,看到这类内容,会不会产生正向行为"。(精确澄清:README 说的是删除手工特征 + 大部分启发式,指**打分/排序侧**;**过滤侧**仍是明确规则 —— 见 [[filtering-pipeline]] 的 17 个过滤器。准确说法:**打分靠学习,过滤靠规则**。)

### 迷思五|「我的帖子会被同批的大 V 挤掉」

**流行说法**:和大号同时段发会被压,要错开大 V 发帖。

**源码怎么说**:排序 transformer 用了**候选隔离注意力掩码**。`make_recsys_attn_mask`(`phoenix/grok.py:39-71`)先给整条序列建因果掩码(`jnp.tril`,`grok.py:62`),再把"候选区 → 候选区"的注意力整块置 0(`grok.py:65`),只在对角线放开每条候选对自己(`grok.py:69`)。效果:每条候选只能"看到"用户上下文和它自己,看不见同批其他候选。README Key Design Decision #2 明说「the score for a post doesn't depend on which other posts are in the batch」(`README.md:327-328`)。

**所以**:你的帖子得几分,只取决于(你的帖子 × 这个用户),和同批有没有大 V、大 V 多强**完全无关**。打分阶段是"单独判卷",不是"同场打擂"。真正的高低比拼发生在之后的[[candidate-selection|选择阶段]] —— 按分排序取 top-K,那是分数排名,不是互相干扰。

### 迷思六|「存在一套人人适用的涨号攻略」

**流行说法**:跟着某套通用攻略做就能涨。

**源码怎么说**:模型的核心输入是**这个用户的行为历史**,打分是 per-(用户, 候选) 的预测(`README.md:55, 230`)。所有权重 —— 22 个行为权重、多样性 `decay`、OON 系数 —— 都来自 feature switch 参数(`ScoringWeights::from_params`,`ranking_scorer.rs:42-66`),X 不发版就能随时改、还能跑 A/B。系统里甚至还有一个可选的二次重排器 `VMRanker`,由 `EnableVMRanker` 开关控制(`vm_ranker.rs:18-20`)。

**所以**:不存在一张固定的"权重表"。同一条内容对不同用户分数不同(各自行为历史不同);今天和下个月的权重也可能不同(参数可调,还在实验)。任何"算法就吃这一套"的通用攻略,在一个 per-user、参数化、还在 A/B 的系统面前,都是刻舟求剑。

## 那些真正在起作用、却很少被提的机制

| 机制 | 一句话 | 详见 |
|------|--------|------|
| **候选隔离注意力掩码** | 每条候选打分时互相看不见,分数只取决于自己 + 用户 | [[candidate-isolation-masking]] |
| **双塔召回** | 你被推给陌生人的真实路径:用户塔 × 候选塔,比向量相似度 | [[phoenix-retrieval]] |
| **哈希嵌入** | 用户/帖子太多,用多个哈希函数把 ID 压进固定大小的嵌入表 | [[hash-based-embeddings]] |
| **`not_dwelled` 负信号** | "划走没停留"是一个被显式建模、给负权重的预测目标 | [[scoring-and-ranking]] |
| **作者多样性衰减** | 同一作者在你这屏里出现越多,后面越降分 | [[scoring-and-ranking]] |
| **Grox 后台内容理解** | 在你刷之前,spam / 安全 / 质量(banger)标签已贴好 | [[grox-architecture]] |
| **几乎删光人工特征** | 工业级推荐系统,打分侧没有人工特征 —— 这本身最反常识 | [[system-architecture]] |

## 怎么认出一篇"真解读"

1. **看它敢不敢给 `文件:行号`**。给不出来 = 没翻过源码,只是在复述别的解读。
2. **看它区不区分"打分(学习)"和"过滤(规则)"**。把两者混为一谈 = 没读懂这套系统。
3. **看它承不承认边界**。一篇斩钉截铁说"权重是 X、做 Y 涨 Z%"的,在编 —— 因为那些数值根本不在开源仓库里。

## 边界:开源仓库给了什么、没给什么

**给了**:算法机制代码(Rust 服务 + Python ML)、一个 mini 演示模型(256 维嵌入、4 注意力头、2 层,`README.md:32`)、一条端到端推理脚本。

**没给**:线上 feature switch 的真实数值(所有权重/系数)、生产级训练模型、训练数据、Grok 的完整行为。

所以本页所有结论都是**机制层面**的("方向是降权""这是负权重"),不是**数值层面**的("降到几折""涨多少")。承认这条边界,本身就是和那 95% 的区别。

## 出处

| 核心结论 | 源码 |
|----------|------|
| 打分/排序侧删除每一个手工特征 | `README.md:55, 324-325` |
| 22 种行为预测 → 加权求和 | `ranking_scorer.rs:125-170`、`README.md:265-292` |
| 5 个负向行为,权重为负 | `ranking_scorer.rs:83`、`README.md:292` |
| 作者多样性衰减 `(1-floor)·decay^N+floor` | `ranking_scorer.rs:186-217` |
| 站外候选乘 OON 系数降权 | `ranking_scorer.rs:220-239, 272-275` |
| 候选隔离:因果掩码 + 候选间互不可见 | `phoenix/grok.py:39-71`、`README.md:327-328` |
| 权重全部来自 feature switch 参数 | `ranking_scorer.rs:42-66` |
| `VMRanker` 由 `EnableVMRanker` 门控 | `vm_ranker.rs:18-20` |

精确语义以技术页与源码为准;每条「详见」的技术页都附 `文件:行号` 锚点。

## 相关页面

- [[posting-guide]] —— 配对页:把这些机制反过来用 —— 发帖到底该怎么做
- [[how-it-works]] —— 端到端白话总览
- [[scoring-and-ranking]] —— 打分三步:加权求和 / 多样性衰减 / OON 降权
- [[candidate-isolation-masking]] —— 候选隔离掩码的技术细节
- [[filtering-pipeline]] —— 17 个过滤器:打分靠学习、过滤靠规则
- [[faq]] —— 常见疑问
- [[system-architecture]] —— 技术版系统架构总览
