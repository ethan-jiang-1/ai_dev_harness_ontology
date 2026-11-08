---
status: draft
updated: 2026-11-08
---

# 05 生产派：本体从哪来、怎么修

## 核心主张

**来源决定可信度，而可信度必须能被下游看见。**

本仓库与多数本体文献的一个差别：不假设本体已经存在。本体怎么来的，决定了它能被信到什么程度——因为判定器的可信度**继承自**本体来源。

第二条：**精化比新建更常见。** 真实项目大多在修一个已存在的本体，而文献更喜欢研究从零建。这个错位是当前最被低估的空档。

## 子主题地图

| 子主题 | 回答什么 | 状态 | 已发现 / 未发现 | 先读 |
|---|---|---|---|---|
| [generation](./generation/README.md) | 本体从哪来：四条生成路线 | `draft`，已拆 F/G | 4 F / 4 G | dashboard |
| [refinement](./refinement/README.md) | 在既有本体上修子类/约束 | `draft`，已拆 F/G | 4 F / 4 G | dashboard |
| [representation](./representation/README.md) | 形式化到什么程度 | `seed`，薄页 dashboard | 3 F / 3 G | 本页 |
| [lifecycle](./lifecycle/README.md) | 来源、精化、对齐、演化 | `seed`，薄页 dashboard | 3 F / 3 G | 本页 |
| [modeling](./representation/modeling.md) | 规范如何压缩自由度 | 机制页 | — | 本页 |

## 本派当前判断

- **生成产出候选，不是完备本体。** OntoDoc 的 assumptions 层能提升完整性，但没有下游任务；可消费性评估缺失。详见 [generation/F1](./generation/findings.md)。
- **精化可以自动化到小规模，但下游未闭环。** CASTON high 6/6；medium 全 mixed；「下游错误 → 该修哪条公理」没有通用答案。详见 [refinement/F4](./refinement/findings.md)。
- **来源决定系统性偏向。** 专家覆盖窄、LLM 语义漂移、数据挖掘把常见当应然、表征挖掘限 MRL、规则自演化要种子。`推测`

## 六种来源（索引）

| 来源 | 代表 | 系统性偏向 |
|---|---|---|
| 专家手工 | SFE-O | 覆盖窄、维护贵、易过时 |
| LLM 生成 | OntoDoc、ReX-GG | 语义漂移、关系方向易错 |
| 数据挖掘 | 综述 | 把「常见」当「应然」，缺约束 |
| 表征挖掘 | Peeling | 只在特定嵌入族上成立；未测下游 |
| 规则引导自演化 | Evontree | 需要人工种子 |
| 精化 | CASTON | 只覆盖少量高置信修复 |

## 三条工程判断

1. **来源标记要进入判定逻辑**，否则不同可信度的约束被平等使用。
2. **冲突显式化优于静默消解。** SFE-O 的范本：发现矛盾就标出来，交给人判断。
3. **表示不是瓶颈，执行才是。** OWL 能表达，但缺 SHACL/数值求解/外部服务；形式化程度应按消费位置选。

## 何时用 · 何时别用

**用**：有存量本体需要维护；领域术语密集且错误代价高；下游需要一个可追溯的可信度来源。

**别用**：指望自动生成一个「完备」本体——现有证据表明生成只能产出候选，约束与边界仍需人。

## 本目录怎么长

| 文件/目录 | 作用 |
|---|---|
| `README.md` | 本页：派地图 + top claims；不展开机制 |
| `claims.md` | 本派局部结论账本（`05-Lx`） |
| `sources.md` | 本派 digest/card 索引 |
| `frontier.md` | 本派候选队列 |
| `<子主题>/README.md` | dashboard：覆盖/计数/当前判断/文件地图 |
| `<子主题>/findings.md` | 该子主题的发现与证据 |
| `<子主题>/frontier.md` | 该子主题的 gap/next |
| `<子主题>/mechanism.md` | 机制怎么跑（按需） |

## 持续挖掘

派级前沿、检索式与候选见 [frontier.md](./frontier.md)；子主题的 gap/next 在各自 `frontier.md`。
