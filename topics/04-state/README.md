---
status: draft
updated: 2026-11-08
---

# 04 状态派：怎么让它记得对

## 核心主张

**记忆是状态，不是事实集合。**

把记忆当一堆独立条目会丢掉三样东西：事实之间的约束、失效条件、冲突记录。丢掉之后每轮都要重新做一次一致性推导，而每次结论可能不同。

这一派的工程思想是**克制**：本体只定义槽位、关系与印证条件，不承担自由推理。克制不等于本体不变——EvoMem 的本体是增量构建并修订层级的；它仍然不做自由推理。

## 子主题地图

| 子主题 | 回答什么 | 状态 | 已发现 / 未发现 | 先读 |
|---|---|---|---|---|
| [memory](./memory/README.md) | 事实集合 vs 状态；两层状态 | `draft`，已拆 F/G | 5 F / 5 G | dashboard |
| [identity](./identity/README.md) | 跨源、跨期的同一性 | `draft`，已拆 F/G | 4 F / 5 G | dashboard |
| [determinism](./determinism/README.md) | 跨运行的一致性锚点 | `seed`，薄页（未拆 F/G） | 3 / 3（未编号） | README（薄页） |

## 本派当前判断

- **本体不承担自由推理；但「给定且改动不扩散」只对 FIRME 成立。** FIRME 的 product–topic 本体只供给槽位、关系与印证条件（`已核`），跨期身份由 registry 负责；「本体改动只影响槽位/条件、不扩散」没有改动对照，是架构推断（`推测`）。EvoMem 的本体不是现成的：它增量建 concept/fact 图，并用 `CREATE/MERGE/SPLIT` 修订层级（`已核` 机制），层级错误会传进 relational state，错误幅度未测（`推测`）。详见 [memory/F1](./memory/findings.md)。
- **身份先于内容，但 alias 不是无条件主增量。** registry 锚定是身份主题唯一的一手评估证据（无「完全不做身份对齐」对照）；alias 复用是在 registry + 语义兜底之上的已测增量——final-period CMR +7.8–12.1 pp、human-audit CMR +9.0–16.5 pp（4 settings；`已核` 增量 / `推测` 主增量）。false merge 会把后续同名观察路由到错误 anchor，但「长期污染」幅度未测、无自动回滚（`推测`）。详见 [identity](./identity/README.md)。
- **增益在「会用」，不在「检索更多」。** EvoMemState Complete Retrieval 85.6%（MemoryBank 86.4%，相当），但 Acc@complete 只有 70.8%（LoCoMo-Refined，同基准最强 baseline +11.5）/ 68.5%（MemSyco，+31.2）；两个数分属不同基准，不可相减。`已核` 详见 [memory/F4](./memory/findings.md)。
- **评估分三层，Reasoning State 不是形式保证。** CMR、human audit、抽取保真/round-trip 不能互相替代（`已核` 分层 / `推测` 不可互替）；推理状态是自然语言/结构化规则，不可形式验证（`已核`）。详见 [memory/F3](./memory/findings.md)、[F5](./memory/findings.md)。

## 两种克制的做法

| 做法 | 本体做什么 | 代表 |
|---|---|---|
| 本体引导归纳 | 增量建 concept/fact 图并修订层级（CREATE/MERGE/SPLIT），挂 relational state | EvoMemState（关系状态 + 推理状态） |
| 本体只做对齐与印证 | 跨期身份锚定、槽位定义、关系赋值条件 | FIRME（product–topic 本体 + registry） |

## 何时用 · 何时别用

**用**：跨会话、跨期的实体知识；需要保留冲突与来源；下游判断依赖历史一致性。

**别用**：单轮任务；本体本身还在建设期（没有稳定槽位，状态结构会一直变）。

## 本目录怎么长

| 文件/目录 | 作用 |
|---|---|
| `README.md` | 本页：派地图 + top claims；不展开机制 |
| `claims.md` | 本派局部结论账本（`04-Lx`） |
| `sources.md` | 本派引用的 digest/card 索引（含跨派借用） |
| `frontier.md` | 本派候选队列 |
| `<子主题>/README.md` | dashboard：覆盖/计数/当前判断/文件地图 |
| `<子主题>/findings.md` | 该子主题的发现与证据 |
| `<子主题>/frontier.md` | 该子主题的 gap/next |
| `<子主题>/mechanism.md` | 机制怎么跑（按需） |

例外：`determinism/` 是薄页——判断在 `README.md`、机制在 `mechanism.md`，未拆 `findings.md`/`frontier.md`；其开放问题写在 README。

## 持续挖掘

派级前沿、检索式与候选见 [frontier.md](./frontier.md)；memory/identity 的 gap/next 在各自 `frontier.md`，determinism 的开放问题在 [README](./determinism/README.md)。
