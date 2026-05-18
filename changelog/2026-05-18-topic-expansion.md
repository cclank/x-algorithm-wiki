---
title: 话题扩充——5 新页 + operating-myths 增 3 迷思（2026-05-18）
created: 2026-05-18
updated: 2026-05-18
type: changelog
tags: [changelog]
---

# 话题扩充:5 新页 + operating-myths 增 3 迷思

应反馈 —— 在 wiki 已讲透"算法是什么、怎么运转"之后,列出"还值得写的、大家关心的话题",获准按 A/B/C 三组推进。

## 动机

按"读者需求 × 源码有没有料"挑出三组:A 组(读者最焦虑、源码料足)、B 组(最出圈的争议问题、适合做成迷思)、C 组(技术补全)。

## B 组:operating-myths 从六迷思扩到九迷思

三条"出圈"争议,先翻源码确认有料,再写成新迷思:

- **迷思七「带外链的帖子会被降权」** —— 翻打分 / 过滤 / Grox 三侧,无任何针对"外链"的机制(`ranking_scorer.rs:12-39` 22 权重无链接项;17 个过滤器无外链过滤器;Grox 分类器无链接分类器)。
- **迷思八「Premium / 蓝V 买曝光」** —— 22 个行为权重无订阅项;订阅在源码里只做"订阅专属帖可见性门槛"(`ineligible_subscription_filter.rs:6`),方向是收窄触达,不是加权。
- **迷思九「算法给某些大账号开后门」** —— 全仓 grep `elon`/`musk` 零命中;打分输入无作者身份特例;"无手工特征"决定结构上没有后门位置。

另:**迷思二补「预测 ≠ 计数」澄清** —— 承接读者对"恶意刷不感兴趣会不会害我"的疑问,点明被加权的是模型预测概率、不是事件计数。

## A 组:3 个新 guide 页

| 页面 | 内容 |
|------|------|
| `guide/visibility-and-shadowban` | 限流与 shadowban 源码级真相:三类真实"压制"机制 + 民间说法逐条对质 |
| `guide/new-account-cold-start` | 新号与冷启动:四条新用户专属代码路径,各用各的阈值 |
| `guide/your-data` | 算法用了你的哪些数据:开源代码所示的用户数据输入清单 |

## C 组:2 个技术补全页

| 页面 | 内容 |
|------|------|
| `concepts/end-to-end-dataflow` | 端到端数据流:一条帖子从发布到被推荐,写入侧(异步)vs 读取侧(实时) |
| `guide/open-source-vs-production` | 开源版 vs 线上真实算法:已知差异清单 + 3 处源码与文档出入 |

## 工作方式与核验

- 5 个新页由 5 个并行 agent 按源码逐锚点核验创建,完成后逐页复核(源码锚点、诚实边界、交叉链接)。
- agent 核验中发现并如实记录的边界:`user_action_seq` / `user_features` query hydrator 属未挂载的旧代码;`impressed_post_ids` 字段当前无 hydrator 填充 —— 均已在 `your-data` 页注明。

## 规模变化

| 指标 | 变化 |
|------|------|
| 总页数 | 29 → 34(+4 guide +1 concept) |
| 白话导览 | 7 → 11 |
| 概念页 | 17 → 18 |
| operating-myths 迷思数 | 6 → 9 |

## 相关页面

- [[operating-myths]] —— 扩到九迷思
- [[visibility-and-shadowban]]、[[new-account-cold-start]]、[[your-data]]、[[end-to-end-dataflow]]、[[open-source-vs-production]] —— 五个新页
- [[2026-05-17-posting-guide]] —— 上一次更新
