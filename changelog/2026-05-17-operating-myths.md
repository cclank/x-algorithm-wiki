---
title: 新增运营迷思页（2026-05-17）
created: 2026-05-17
updated: 2026-05-17
type: changelog
tags: [changelog]
---

# 新增「运营迷思 vs 源码真相」

应反馈 —— X 算法开源后网上解读铺天盖地,但绝大多数是 AI 批量生产的同质化内容,没翻过源码。本次新增一页源码级"打脸"页,并配套产出一篇可对外发布的长文。

## 动机

读者原话:网上 95% 的分析是 AI 废话,连源码文件名都没翻过;「多互动」「多发帖」「账号要垂直」这类话说了等于没说。需要一份**带行号、可逐条核对**的高价值内容,把流行说法对到源码上。

## 新增页面

| 页面 | 类型 | 内容 |
|------|------|------|
| `guide/operating-myths` | guide | 六个流行运营迷思逐条对源码行号 + 深层机制清单 + "如何识别真解读"方法论 + 开源仓库边界声明 |

## 六个迷思与源码依据

1. **「多发帖 = 多曝光」** → 作者多样性衰减:同一作者第 N 条乘 `(1-floor)·decay^N+floor`(`ranking_scorer.rs:186-217`)
2. **「互动量越高越好」** → 22 行为预测,5 个负权重;`not_dwelled`(划走)被显式建模扣分(`ranking_scorer.rs:83`)
3. **「做泛内容轻松破圈」** → 站外候选乘 OON 系数降权(`ranking_scorer.rs:272-275`)
4. **「套模板/堆关键词骗算法」** → 打分侧删光每一个手工特征(`README.md:55, 324-325`)
5. **「被同批大 V 挤掉」** → 候选隔离注意力掩码,候选分数互不影响(`phoenix/grok.py:39-71`)
6. **「人人适用的万能攻略」** → per-user 预测 + 权重全是 feature switch 参数(`ranking_scorer.rs:42-66`)

## 配套:站外长文

产出一篇可对外发布的中文深度长文 `x-algorithm-运营迷思-源码打脸.md`(置于 `code/` 目录,不进 wiki 仓库),承接读者给的开头,把六个迷思写成可发布形态。长文与 wiki 页共用同一套源码论据。

## 可追溯性(出处)

- 全部六条迷思的源码依据已亲自核对实际源文件:`home-mixer/scorers/ranking_scorer.rs`、`home-mixer/scorers/vm_ranker.rs`、`phoenix/grok.py`、顶层 `README.md`
- wiki 页设「出处」表,每条核心结论对应 `文件:行号`
- 页内单列「边界」一节,声明开源仓库不含线上权重数值、生产模型、训练数据 —— 结论只到机制层面

## 配套改动

- `index.md` / `README.md`:更新为 28 页(6 白话导览 + 17 概念 + 5 实体)
- 6 个相关页补 `[[operating-myths]]` 交叉链接:`how-it-works`、`faq`、`the-five-components`、`glossary`、`scoring-and-ranking`、`candidate-isolation-masking`

## 规模变化

| 指标 | 变化 |
|------|------|
| 总页数 | 27 → 28(+1 guide) |
| 白话导览 | 5 → 6 |

## 相关页面

- [[operating-myths]] —— 新增的源码级打脸页
- [[2026-05-17-candidate-selection]] —— 上一次:新增选帖过程页
