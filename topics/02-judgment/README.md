---
status: draft
updated: 2026-11-09
---

# 02 判定派：怎么知道它做错了

## 核心主张

**判据必须外部、且必须可度量。**

「挂个本体就变准」是本派最想否掉的直觉。判定器本身也是一个会犯错的法官：它会漏掉错误，也会把正确答案标错，并把 agent 推去「修复」本来没错的东西。本派的工程问题不是「用不用本体」，而是**这条漏检/误报曲线在哪、代价是什么**。

## 子主题地图

| 子主题 | 回答什么 | 状态 | 已发现 / 未发现 | 先读 |
|---|---|---|---|---|
| [checker](./checker/README.md) | 输出后：本体当语义判据，漏检/误报怎么换 | `draft`，已拆 F/G | 5 F / 5 G | dashboard |
| [evidence](./evidence/README.md) | 输出时：答案带什么证据、接地等级怎么报 | `draft`，已拆 F/G | 3 F / 4 G | dashboard |
| [calibration](./calibration/README.md) | 判定器的曲线与代价 | `seed`，待拆 | — | 机制页 |

**薄页（<2 篇独立来源）**：checker（1 篇）、evidence（1 篇）、calibration（0 篇，待建）。薄页只作候选/边界，不承担稳定判断。

## 本派当前判断

- **curated 不等于可靠。** 真实答案上 curated 精确度仅略优于随机；按发布状态使用的 schema 甚至可能与自身数据矛盾。详见 [checker/F2](./checker/findings.md)。
- **空结果重试是必须超过的基线。** 人工 fault 上 catch 79.2%、FA 0%；ontology check 只有抓到它抓不到的错才有价值。详见 [checker/F3](./checker/findings.md)。
- **接地等级要显式化，但别把它当保证。** OA-RAG 让答案报告本体观察 + grounding level，整体最优；但等级是模型自评、未校准。详见 [evidence](./evidence/README.md)。
- **误报比漏检更贵。** 漏检只是放过一个错误；误报会让 agent 去改对的东西，产生新的、更隐蔽的错误。目前是 `推测`，待仓库外验证。

## 何时用 · 何时别用

**用**：产出可被结构性检查（有 schema、有约束、有可查的关系）；需要在不看全量人工复核的前提下筛出可疑项。

**别用**：判定器与生成器同源（自我审核几乎总失效）；没有标注集就无法知道曲线，此时判定器只是给人一种安全感。

## 本目录怎么长

| 文件/目录 | 作用 |
|---|---|
| `README.md` | 本页：派地图 + top claims；不展开机制 |
| `claims.md` | 本派局部结论账本（`02-Lx`） |
| `sources.md` | 本派 digest/card 索引 |
| `frontier.md` | 本派候选队列 |
| `<子主题>/README.md` | dashboard：覆盖/计数/当前判断/文件地图 |
| `<子主题>/findings.md` | 该子主题的发现与证据 |
| `<子主题>/frontier.md` | 该子主题的 gap/next |
| `<子主题>/mechanism.md` | 机制怎么跑（按需） |

## 持续挖掘

派级前沿、检索式与候选见 [frontier.md](./frontier.md)；子主题的 gap/next 在各自 `frontier.md`。
