---
status: draft
updated: 2026-11-12
---

# 02 判定派：怎么知道它做错了

> **2026-11-12 撤源对账**：本派 Ontology Catch（E-02）与 OA-RAG（E-03）已移出，checker/evidence/calibration 三页的效应量作历史示例。**`findings.md` 索引里的旧「已核」不作现役等级。** 仍 admitted：E-20 代码级三态/覆盖、E-24 策略语义标准。

## 核心主张

**判据必须外部、且必须可度量。**

「挂个本体就变准」是本派最想否掉的直觉。判定器本身也是一个会犯错的法官：它会漏掉错误，也会把正确答案标错，并把 agent 推去「修复」本来没错的东西。本派的工程问题不是「用不用本体」，而是**这条漏检/误报曲线在哪、代价是什么**。

## 子主题地图

> **计数只写在子主题 dashboard**（`<子主题>/README.md`）与 `findings.md`；本表不抄数字，避免派级与叶级漂移。

| 子主题 | 回答什么 | 状态 | 计数 | 先读 |
|---|---|---|---|---|
| [checker](./checker/README.md) | 输出后：本体当语义判据，漏检/误报怎么换 | `draft`，已拆 F/G | **不在此抄数** → dashboard | dashboard |
| [evidence](./evidence/README.md) | 输出时：答案带什么证据、接地等级怎么报 | `draft`，已拆 F/G | **不在此抄数** → dashboard | dashboard |
| [calibration](./calibration/README.md) | 判定器的曲线与代价 | `seed`，已拆 F/G | **不在此抄数** → dashboard | dashboard |

**薄页（<2 篇独立来源）**：checker（1 篇，**源已撤回 → 作历史**）、evidence（1 篇，**源已撤回**）、calibration（1 篇，**源已撤回**）。三页均已成文（各有 F 条目），但效应量不作现役判断。

## 本派当前判断

- **`[已撤回/历史]` curated 不等于可靠。** 原实证（Ontology Catch / E-02 已于 2026-11-11 撤回）称真实答案上 curated 精确度仅略优于随机、按发布状态使用的 schema 甚至可能与自身数据矛盾；现作待重证问题，详见 [checker/F2](./checker/findings.md)。
- **`[已撤回/历史]` 空结果重试是必须超过的基线。** 原人工 fault 79.2%/FA 0% 源自已撤回的 E-02，现作比较基线设计提示，不作现役实证，详见 [checker/F3](./checker/findings.md)。
- **`[已撤回/历史]` 接地等级要显式化，但别把它当保证。** 原 OA-RAG（E-03 已撤回）仅作结构提示，详见 [evidence](./evidence/README.md)。
- **误报比漏检更贵。** 漏检只是放过一个错误；误报会让 agent 去改对的东西，产生新的、更隐蔽的错误。目前是 `推测`，待仓库外验证。

## 何时用 · 何时别用

**用**：产出可被结构性检查（有 schema、有约束、有可查的关系）；需要在不看全量人工复核的前提下筛出可疑项。

**别用**：判定器与生成器同源（自我审核几乎总失效）；没有标注集就无法知道曲线，此时判定器只是给人一种安全感。

## 本目录怎么长

| 文件/目录 | 作用 |
|---|---|
| `README.md` | 本页：派地图 + top claims；不展开机制 |
| [claims.md](./claims.md) | 本派局部结论账本（`02-Lx`） |
| [sources.md](./sources.md) | 本派 digest/card 索引 |
| [frontier.md](./frontier.md) | 本派候选队列 |
| `<子主题>/README.md` | dashboard：覆盖/计数/当前判断/文件地图 |
| `<子主题>/findings.md` | 该子主题的发现与证据 |
| `<子主题>/frontier.md` | 该子主题的 gap/next |
| `<子主题>/mechanism.md` | 机制怎么跑（按需） |

## 持续挖掘

派级前沿、检索式与候选见 [frontier.md](./frontier.md)；子主题的 gap/next 在各自 `frontier.md`。
