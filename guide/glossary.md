---
title: 术语速查表
created: 2026-05-17
updated: 2026-05-17
type: guide
tags: [guide, glossary, overview]
sources: [home-mixer/scorers/ranking_scorer.rs, phoenix/recsys_retrieval_model.py, phoenix/grok.py, candidate-pipeline/candidate_pipeline.rs, grox/classifiers/content/classifier.py]
---

# 术语速查表

> 看技术页时遇到不懂的词,查这里。每个词一句大白话,需要深入就点"详见"。

## 推荐流程类

| 术语 | 大白话 | 详见 |
|------|--------|------|
| **召回**(retrieval) | 第一步粗筛:从全网几百万条里快速挑出几百条候选。求快不求精。 | [[phoenix-retrieval]] |
| **排序**(ranking) | 第二步精选:给召回来的几百条候选认真打分、排名次。 | [[phoenix-ranking]] |
| **候选**(candidate) | 一条"可能会展示给你"的帖子。还没定下来,要经过过滤和打分。 | [[home-mixer-orchestration]] |
| **站内 / 站外** | 站内 = 你关注的人发的;站外 = 你没关注但系统觉得你可能喜欢的。 | [[thunder-in-network-store]] |
| **两阶段** | "先召回再排序"这套路。因为帖子太多,不能每条都精算。 | [[system-architecture]] |
| **水合**(hydration) | 给只有编号的候选"填资料":查正文、作者、媒体等。 | [[home-mixer-orchestration]] |
| **过滤器**(filter) | 把不该给你看的候选踢掉的一道道关卡(拉黑、看过、太旧…)。 | [[filtering-pipeline]] |
| **流水线**(pipeline) | 把"召回→水合→过滤→打分→选择"这串步骤串起来的标准流程。 | [[candidate-pipeline-framework]] |

## 打分类

| 术语 | 大白话 | 详见 |
|------|--------|------|
| **多行为预测** | 模型不只猜"你喜不喜欢",而是同时猜你会点赞、回复、转发、划走、举报…各自的概率。 | [[phoenix-ranking]] |
| **加权打分** | 把各种行为概率乘上权重再加起来,得一个总分。点赞加分,举报减分。 | [[scoring-and-ranking]] |
| **负反馈** | 你的"不喜欢"信号 —— 点不感兴趣、拉黑、举报、快速划走。会拉低帖子的分。 | [[scoring-and-ranking]] |
| **作者多样性** | 同一个作者的帖子在你信息流里出现越多次,后面的越降分,防刷屏。 | [[scoring-and-ranking]] |
| **OON 降权** | OON = Out-Of-Network(站外)。站外帖子的分会乘一个小于 1 的系数,略微让步给站内。 | [[scoring-and-ranking]] |
| **候选隔离** | 打分时让每条候选互相"看不见",保证一条帖子的分只取决于它自己,稳定可缓存。 | [[candidate-isolation-masking]] |

## 模型与 AI 类

| 术语 | 大白话 | 详见 |
|------|--------|------|
| **Grok** | xAI 自家的大模型。这套推荐系统的核心模型就是从 Grok 改造来的。 | [[grok-transformer]] |
| **transformer** | 一种 AI 模型结构,和 ChatGPT 同源。这里用来"读懂"你的兴趣序列。 | [[grok-transformer]] |
| **双塔模型** | 召回用的办法:一座"塔"把你压成一串数字,另一座塔把每条帖子压成数字,比谁最接近。 | [[phoenix-retrieval]] |
| **嵌入**(embedding) | 把一个东西(用户、帖子、词)变成一串数字,方便计算机比较"像不像"。 | [[hash-based-embeddings]] |
| **哈希嵌入** | 用户/帖子数量太多,用哈希把它们的编号塞进固定大小的"格子"再取嵌入。 | [[hash-based-embeddings]] |
| **互动序列** | 你最近一连串的操作记录(点了什么赞、回了谁…),是模型判断你兴趣的主要依据。 | [[phoenix-ranking]] |
| **注意力 / attention** | transformer 内部的机制:让模型决定"看你的历史时,重点看哪几条"。 | [[grok-transformer]] |
| **MoE** | Mixture-of-Experts,完整 Grok 用的"多专家"结构。本开源版**没有**用,是简化版。 | [[grok-transformer]] |

## 内容理解与广告类

| 术语 | 大白话 | 详见 |
|------|--------|------|
| **VLM** | 视觉语言模型 —— 能同时看文字和图片的 AI。Grox 的分类器都用它。 | [[grox-classifiers]] |
| **PTOS** | 一套内容安全策略。Grox 用 AI 判断帖子有没有违反(暴力、成人、仇恨等类别)。 | [[grox-classifiers]] |
| **banger** | "爆款潜质"。Grox 给帖子打一个质量分,判断它是不是高质量内容。 | [[grox-classifiers]] |
| **多模态嵌入** | 把帖子的文字 + 图片 + 视频一起转成一串数字。 | [[multimodal-embedders]] |
| **品牌安全** | 判断一条帖子"广告主敢不敢挨着它投广告"。分安全/低风险/中风险几档。 | [[ads-blending]] |
| **广告混排** | 把广告插进排好序的帖子流里,且避开不安全的"邻居"。 | [[ads-blending]] |

## 工程基础设施类

| 术语 | 大白话 | 详见 |
|------|--------|------|
| **gRPC** | 服务之间互相调用的一种通信方式。home-mixer、Thunder 都靠它对外提供接口。 | [[home-mixer-orchestration]] |
| **Kafka** | 一条"消息流水线"。新帖子事件源源不断从 Kafka 流出,Thunder、Grox 在它下游接收。 | [[thunder-kafka-ingestion]] |
| **保留期**(retention) | Thunder 只在内存里留最近一段时间(约两天)的帖子,过期自动清掉。 | [[thunder-kafka-ingestion]] |
| **side effect** | 流水线的"收尾杂活":写缓存、发日志等。不影响给你的结果,在后台做。 | [[candidate-pipeline-framework]] |

## 出处

本表术语提炼自各技术页,不引入新定义。**每条「详见」的技术页都附 `文件:行号` 源码锚点** —— 顺着「详见」即可一路追到源码。术语的精确语义以技术页与源码为准。

## 相关页面

- [[how-it-works]] —— 端到端白话总览
- [[the-five-components]] —— 五大组件速览
- [[operating-myths]] —— 运营迷思 vs 源码真相:逐条对源码行号
- [[posting-guide]] —— 发帖指南:从算法机制反推发帖技巧
- [[faq]] —— 常见疑问
- [[system-architecture]] —— 技术版系统架构
