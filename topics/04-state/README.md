---
status: draft
updated: 2026-11-08
---

# 04 状态派：怎么让它记得对

## 核心主张

**记忆是状态，不是事实集合。**

把记忆当一堆独立条目会丢掉三样东西：事实之间的约束、失效条件、冲突记录。丢掉之后每轮都要重新做一次一致性推导，而每次结论可能不同。

这一派的工程思想是**克制**：本体只定义槽位与关系，不承担自由推理；它承担对齐与印证条件。

## 子主题地图

| 子主题 | 回答什么 | 状态 | 已发现 / 未发现 | 先读 |
|---|---|---|---|---|
| [memory](./memory/README.md) | 事实集合 vs 状态；两层状态 | `draft`，已拆 F/G | 4 F / 5 G | dashboard |
| [identity](./identity/README.md) | 跨源、跨期的同一性 | `draft`，机制页 | 3 F / 3 G | dashboard |
| [determinism](./determinism/README.md) | 跨运行的一致性锚点 | `seed`，待拆 | — | 机制页 |

## 本派当前判断

- **本体在记忆里是克制的：对齐与印证条件，不是自由推理。** FIRME 的 product-topic 本体 + registry 只影响槽位/条件；本体改动不扩散成不可控推理。详见 [memory/F1](./memory/findings.md)。
- **身份先于内容。** alias memory 让 CMR +7.8–12.1 pp，但 false merge 会长期污染；registry 分层匹配是关键。详见 [identity](./identity/README.md)。
- **增益在「会用」，不在「检索更多」。** EvoMemState Complete Retrieval 与最好 baseline 相当，Acc@complete 70.8 vs 36.8。详见 [memory/F4](./memory/findings.md)。

## 两种克制的做法

| 做法 | 本体做什么 | 代表 |
|---|---|---|
| 本体引导归纳 | 从多源记忆构建关系状态 | EvoMemState（关系状态 + 推理状态） |
| 本体只做对齐与印证 | 跨期身份锚定、槽位定义、关系赋值条件 | FIRME（product–topic 本体 + registry） |

## 何时用 · 何时别用

**用**：跨会话、跨期的实体知识；需要保留冲突与来源；下游判断依赖历史一致性。

**别用**：单轮任务；本体本身还在建设期（没有稳定槽位，状态结构会一直变）。

## 本目录怎么长

| 文件/目录 | 作用 |
|---|---|
| `README.md` | 本页：派地图 + top claims；不展开机制 |
| `claims.md` | 本派局部结论账本（`04-Lx`） |
| `sources.md` | 本派 digest/card 索引 |
| `frontier.md` | 本派候选队列 |
| `<子主题>/README.md` | dashboard：覆盖/计数/当前判断/文件地图 |
| `<子主题>/findings.md` | 该子主题的发现与证据 |
| `<子主题>/frontier.md` | 该子主题的 gap/next |
| `<子主题>/mechanism.md` | 机制怎么跑（按需） |

## 持续挖掘

派级前沿、检索式与候选见 [frontier.md](./frontier.md)；子主题的 gap/next 在各自 `frontier.md`。
