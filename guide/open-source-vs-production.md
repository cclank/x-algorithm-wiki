---
title: 开源版 vs 线上真实算法:已知差异清单
created: 2026-05-18
updated: 2026-05-18
type: guide
tags: [guide, overview, faq, model]
sources: [README.md, phoenix/README.md, phoenix/grok.py, home-mixer/scorers/mod.rs, home-mixer/scorers/ranking_scorer.rs]
---

# 开源版 vs 线上真实算法:已知差异清单

> 这一页只回答一个问题:`xai-org/x-algorithm` 这份开源代码,和 X 线上真实跑的 For You 算法,**已知的差距有哪些**?
> 规矩和别的 guide 页一样 —— 只写有依据的:要么是 README / 源码自己说的,要么是本 wiki 逐行核验过、并在 [[faq]] 里记下来的。**仓库没说、代码里看不出来的,就写"无法从仓库得知",不臆测线上长什么样。**
>
> 它是 [[operating-myths]] 末尾「边界」一节和 [[faq]]「这就是 X 线上跑的真实代码吗」那一条的展开版。

## 一句话定位:有代表性的简化快照

仓库自己的定性是 "representative simplified snapshot" —— **架构有代表性,但是一份简化的、冻结的快照**。

`phoenix/README.md:5` 的原话:这份代码 "is **representative of** the model used internally **with the exception of specific scaling optimizations**"(代表了内部使用的模型,但省略了特定的扩展优化)。配合 `phoenix/README.md:28-31` 的 "About This Release" 一节:公开的是 mini 版模型、是持续训练过程中的一个**冻结 checkpoint**、配的是一份演示用的体育语料。

所以读这份代码的正确姿势:**学的是机制和架构,不是线上的具体规模与数值。** 这条贯穿整页。

## 简化与省略:仓库明确说了"这里删过"

下面每一条,要么 README 自己点名,要么本 wiki 的技术页逐行核验过。

### 1|模型是 mini 版,不是生产规模

`phoenix/README.md:29` 写得很直接:这是 "a **mini version** of the Phoenix model",而 "Production uses a **larger model** with more layers and wider embeddings"(线上用的是更大的模型,层更多、嵌入更宽)。

公开 mini 模型有多小,看 `phoenix/README.md:254-268` 的配置表:嵌入维度 128、4 层 transformer、4 个注意力头。线上具体大到什么程度 —— **仓库没给数字,无法得知**,只知道方向是"更大、更宽、更深"。

> 注:关于 mini 模型尺寸,仓库内部有一处自相矛盾,见下面「源码与文档的 3 处出入」第①条。

### 2|完整 Grok 的 MoE 被拿掉了,换成稠密 FFN

线上排序用的是 Grok 改造的 transformer。完整的 Grok-1 是 **MoE(Mixture-of-Experts,多专家)** 架构 —— 多个专家子网络 + 一个路由器决定每个 token 走哪个专家。

开源版**没有 MoE**:它的前馈层是一个普通的稠密块 `DenseBlock`,没有专家、没有路由。这是开源版与完整 Grok-1 最显著的一处差异。详见 [[grok-transformer]](该页确认 `grok.py` 全文搜不到任何 expert / router / gating 代码)。`phoenix/README.md:5` 把这类删减归在 "specific scaling optimizations" 名下。

### 3|"特定扩展优化"被省略

承上,`phoenix/README.md:5` 明说省略了 "specific scaling optimizations" —— 那些让模型能在生产规模上高效训练 / 推理的工程优化。MoE 是其中一类。**这句话本身是个口袋**:仓库没有逐条列出省了哪些优化,所以"线上还多做了什么"这一层,**只能确定有、无法确定具体是什么**。

### 4|没有线上 feature switch 的真实数值

这是对运营 / 创作者最关键的一条。系统里**所有**可调的权重和系数 —— 22 个行为权重、作者多样性的衰减因子、站外(OON)降权系数 —— 都不是写死在代码里的常量,而是从 feature switch 参数读进来的(`ScoringWeights::from_params`,`ranking_scorer.rs:42-66`)。

开源仓库给的是**读参数的代码**,不是**参数的线上取值**。也就是说:

- 你能从代码确认"负向行为是负权重""站外候选会乘一个小于 1 的系数"——**机制是确定的**;
- 你**无法**得知"点赞权重到底是几""OON 系数是 0.5 还是 0.8"——**数值不在仓库里**。

而且这些参数 X 不发版就能随时改、还能跑 A/B(`operating-myths` 迷思六已展开)。所以即便某天泄露了一组数值,它也只是某一刻、某一组用户的快照。

### 5|不含训练数据与训练管线

仓库带的是**一个预训练好的 mini 模型 + 一条推理脚本**,不是训练系统。

- 模型以导出的 `.npz` checkpoint 形式分发,`run_pipeline.py` 只做加载和前向推理(详见 [[run-pipeline]])。
- `phoenix/README.md:30` 点明这是 "a **frozen checkpoint**" —— 线上 Phoenix 是 "trained **continuously** on real-time data"(在实时数据上持续训练),开源的只是这个持续过程中"某一时刻的快照"。
- 配套语料 `sports_corpus.npz` 是约 53.7 万条体育帖、取自一个 6 小时窗口、按 "Sports" 话题筛出来的 **demo 语料**(`phoenix/README.md:31`),不是线上真实候选库。

所以:训练用什么数据、损失函数怎么设计、持续训练怎么调度 —— **这些都不在仓库里,无法得知**。

### 6|在线服务依赖 X 内部基础设施,无法独立跑起来

仓库分 ML 部分和在线服务部分,可运行性不一样:

- **能跑**:Phoenix(ML 部分)。带 mini 模型和 `run_pipeline.py`,能在示例语料上完整跑通"召回 → 排序"。
- **不能独立跑**:在线服务 —— home-mixer(编排)、Thunder(站内库)、Grox(内容理解)。它们依赖大量 X 内部基础设施(gRPC 服务、Kafka 流、Strato 等),仓库**主要供阅读架构**,不能脱离 X 环境运行。

这一点 [[faq]]「我想自己跑一下,可以吗」已说明,[[run-pipeline]] 是能跑的那条路径的入口。

## 源码与官方文档的 3 处出入

本 wiki 在初次逐行核验时,发现仓库**自己内部**有 3 处对不上 —— 不是"开源 vs 线上"的差异,而是"README 怎么说 vs 代码怎么写"的出入。处理原则统一:**以代码为准**。这 3 条全部经过亲自打开源码核对。

### ① mini 模型尺寸:两个 README 数字不一致

| 出处 | 说法 |
|------|------|
| 仓库根 `README.md:32` | "256-dim embeddings, **4** attention heads, **2** transformer layers" |
| `phoenix/README.md:29` | "**128-dim, 4-layer** transformer" |
| `phoenix/README.md:254-268` 配置表 | 嵌入维度 **128**、**4** 层、**4** 头、key_size 32 |

两处对不上:根 README 说 256 维 / 2 层,phoenix README 说 128 维 / 4 层。

**裁定**:`phoenix/README.md` 的配置表与代码导出的真实配置一致,wiki 以 128 维 / 4 层为准。技术细节见 [[phoenix-ranking]] 与 [[grok-transformer]]。

### ② 打分器数量:README 说 4 个独立 Scorer,代码只编译 3 个

仓库根 `README.md` 在架构图、Pipeline Stages、Scoring 三处都把打分描述成几个**独立的 Scorer**:Phoenix Scorer、Weighted Scorer、Author Diversity Scorer、OON Scorer(见 `README.md:107-122, 251-256, 286`)。

但实际编译进系统的只有 3 个。模块声明文件 `home-mixer/scorers/mod.rs` 全文只有三行,声明的是 `phoenix_scorer`、`ranking_scorer`、`vm_ranker` —— 仅此三个。

`scorers/` 目录里**确实有** `weighted_scorer.rs`、`author_diversity_scorer.rs`、`oon_scorer.rs` 这三个文件 —— 但 `mod.rs` 没有声明它们,**它们不在编译模块树内**。加权求和、作者多样性衰减、站外降权这三段逻辑,实际是**合并实现在 `RankingScorer` 一个打分器内部**的(`ranking_scorer.rs` 的 `score()` 分三步做完)。

**裁定**:README 描述的是**概念阶段**;代码实现里三段逻辑合并进了 `RankingScorer`。以代码为准,详见 [[scoring-and-ranking]]。

> 这条出入有实际意义:看 README 容易以为"加权""多样性""OON"是三个能独立开关、独立替换的部件;代码里它们是强耦合的三步(多样性依赖加权结果、OON 依赖多样性结果),合在一个打分器里。

### ③ 候选隔离掩码:README 图说"双向",代码是"因果"

[[candidate-isolation-masking|候选隔离掩码]]把"用户 + 历史 + 候选"拼成一条序列。问题出在"用户段和历史段之间怎么注意":

- `phoenix/README.md:158` 的掩码示意图,图例写 "User + History: Full **bidirectional** attention among themselves"(用户和历史段彼此**完全双向**注意力)。
- 但代码 `make_recsys_attn_mask`(`grok.py:62`)是从一个 **`jnp.tril`(下三角)** 因果掩码起步的;`grok.py:47` 的函数注释也明写 "Positions 0 to candidate_start_offset-1 (user+history): **causal** attention"。

下三角 = 因果:位置 `i` 只能注意 `≤ i` 的位置。代码是**因果注意力**,README 图例说**双向** —— 两者不符。

**裁定**:以代码为准,用户 + 历史段是因果注意力。详见 [[candidate-isolation-masking]]。

## 怎么用这份理解

把上面汇总成一条可操作的判断准则:

**本 wiki 的所有结论,都是"机制层面"的,不是"线上数值层面"的。**

- ✅ 可以说:"负向行为是负权重""站外候选会被乘一个小于 1 的系数降权""每条候选打分时互相看不见"——这些是**代码里写死的机制**,开源版和线上一致(架构有代表性)。
- ❌ 不能说:"点赞权重是 X""OON 降权降到几折""线上模型有多少层"——这些是**线上参数 / 规模**,不在仓库里。

所以你会看到 [[operating-myths]] 反复强调"方向是降权""这是负权重",而从不给一个具体倍数 —— 这不是含糊,是**严格停在仓库能支撑的边界上**。一个判断别人解读靠不靠谱的简单标准:**凡是给出"线上具体数值"的算法解读,要么来自仓库之外的渠道,要么是编的** —— 因为这份开源仓库里根本没有那些数。

## 一页速查

| 维度 | 开源仓库给了什么 | 线上是什么 / 能否得知 |
|------|------------------|------------------------|
| 整体定位 | representative simplified snapshot(`phoenix/README.md:5`) | 架构代表性强,但实现有简化 |
| 模型规模 | mini 版:128 维 / 4 层 / 4 头(`phoenix/README.md:254-268`) | 更大、更宽、更深;**具体数字无法得知** |
| Grok 结构 | 稠密 `DenseBlock` FFN,无 MoE([[grok-transformer]]) | 完整 Grok-1 是 MoE |
| 扩展优化 | 明确省略 "specific scaling optimizations"(`phoenix/README.md:5`) | 省了哪些**未逐条列出** |
| 权重 / 系数 | 读 feature switch 参数的代码(`ranking_scorer.rs:42-66`) | 真实数值**不在仓库**,且可随时改 + A/B |
| 训练 | 一个冻结的预训练 mini checkpoint(`phoenix/README.md:30`) | 线上持续训练;训练数据 / 管线**不在仓库** |
| 语料 | demo 体育语料 ~53.7 万条(`phoenix/README.md:31`) | 非线上真实候选库 |
| 可运行性 | Phoenix 能跑;home-mixer / Thunder / Grox 不能独立跑 | 在线服务依赖 X 内部基础设施 |
| README 内部出入 | 3 处:模型尺寸 / 打分器数量 / 掩码"双向 vs 因果" | 统一以代码为准(见上一节) |

## 出处

| 核心结论 | 出处 |
|----------|------|
| "representative... with the exception of specific scaling optimizations" | `phoenix/README.md:5` |
| mini 版 vs 线上更大模型 | `phoenix/README.md:29` |
| mini 模型配置 128 维 / 4 层 / 4 头 | `phoenix/README.md:254-268` |
| 冻结 checkpoint / 持续训练 | `phoenix/README.md:30` |
| demo 体育语料 ~53.7 万条、6 小时窗口 | `phoenix/README.md:31` |
| MoE 被去掉、改用稠密 `DenseBlock` | [[grok-transformer]];`phoenix/README.md:5` |
| 权重 / 系数来自 feature switch 参数 | `home-mixer/scorers/ranking_scorer.rs:42-66` |
| 出入②:`mod.rs` 只声明 3 个打分器 | `home-mixer/scorers/mod.rs:1-3`;`README.md:107-122, 251-256, 286` |
| 出入③:掩码代码用 `jnp.tril`(因果),注释写 "causal" | `phoenix/grok.py:47, 62`;`phoenix/README.md:158` |
| 在线服务依赖内部基础设施、无法独立运行 | [[run-pipeline]];[[faq]] |

三处「源码与文档出入」的逐行核验记录,见 `changelog/2026-05-16-initial-creation.md`。精确语义以技术页与源码为准。

## 相关页面

- [[operating-myths]] —— 运营迷思 vs 源码真相;本页是其末尾「边界」一节的展开
- [[faq]] —— 「这就是 X 线上跑的真实代码吗」一条的展开
- [[grok-transformer]] —— Grok transformer 骨架:MoE 为何被去掉、改成什么
- [[phoenix-ranking]] —— 排序模型:mini 配置的尺寸细节
- [[scoring-and-ranking]] —— 打分器为何只有 3 个、权重为何全是参数
- [[candidate-isolation-masking]] —— 候选隔离掩码:因果 vs 双向的代码真相
- [[run-pipeline]] —— 能跑起来的那条路径:Phoenix 端到端推理脚本
- [[how-it-works]] —— 端到端白话总览
