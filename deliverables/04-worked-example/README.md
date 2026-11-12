---
status: draft
deliverable_status: draft
updated: 2026-11-12
target: 要落地一个小型本体查询应用的团队
basis: E-12/E-19/E-20/E-21/E-22/E-23/E-24/E-25/E-27；E-02/E-04/E-06/E-26 已撤回；工程产物；未测
---

# 04 · 合成走查：一条建用治示例链

> **读者**：要落地小型本体查询应用的小团队（数据/本体、应用/agent、治理/安全） ｜ **回答**：一条最小建用治链长什么样（合成示例） ｜ **不回答**：值不值得做（去 01）、接缝怎么选（去 02）、为什么是这些位置（去 03）、**业界真实落地现状（去 05）**。
> **状态**：`draft` ｜ **证据重置**：E-02/E-04/E-06/E-26 撤回（W 表见 [04-evidence/01-ledger](04-evidence/01-ledger.md#w-table)）；E-12/E-19/E-20/E-21–E-25/E-27 仍可用。
>
> **本页只做索引**。正文从 [00-overview](02-sections/00-overview.md) 开始；三章正文从 [03-body](03-body/01-build.md) 开始。
>
> **定性：合成示例，不是生产现状**（曾名 ontology-in-production，名实不符已改）。fixture 数字是期望值、非实测；「业界落地现状」之问归 [05](../05-production-landscape/README.md)。**改/建前必读 [SCOPE.md](./SCOPE.md)**。

## 30 秒结论

1. **第 1 周不建 TBox**：先写 6 行消费者契约，写不出就停；这是 04 的第一个 gate。详见 [overview §0.1](02-sections/00-overview.md#01-案例一个-3-人小团队的第-1-周)。
2. **9 件产物 + 5 组门槛**：契约、TBox/ABox、shapes、CQ、policy、测试、泄漏用例、audit、故障矩阵；`conditional` 不是失败。详见 [overview §0.2/§0.4](02-sections/00-overview.md#02-九件产物地图)。
3. **fixture 数字是期望值，不是实测**：不证明效果、跨域/规模、生产；边界见 [04-boundaries](02-sections/04-boundaries.md)。

## 目录

> 编号规则：目录号（`02-sections`）= 书里的第几块；文件号（`02-map`）= 第几章/第几页；同号不同层正常。若预览器不解析相对链接，按「路径」列在文件树里打开（目录行给出目录）。

| 用途 | 读 | 路径 |
|---|---|---|
| 落地摘要、前 7 天、九件产物、验收 | [00-overview](02-sections/00-overview.md) | `deliverables/04-worked-example/02-sections/00-overview.md` |
| 怎么读、按什么顺序 | [01-GUIDE](02-sections/01-GUIDE.md) | `deliverables/04-worked-example/02-sections/01-GUIDE.md` |
| 症状地图 | [02-map](02-sections/02-map.md) | `deliverables/04-worked-example/02-sections/02-map.md` |
| 建 / 用 / 治三章 | [03-body](03-body/) | `deliverables/04-worked-example/03-body/` |
| 边界、反例 | [04-boundaries](02-sections/04-boundaries.md) | `deliverables/04-worked-example/02-sections/04-boundaries.md` |
| 验收清单 | [05-acceptance](02-sections/05-acceptance.md) | `deliverables/04-worked-example/02-sections/05-acceptance.md` |
| 决策、成本、conditional | [06-decision](02-sections/06-decision.md) | `deliverables/04-worked-example/02-sections/06-decision.md` |
| 术语与内码 | [90-glossary](02-sections/90-glossary.md) | `deliverables/04-worked-example/02-sections/90-glossary.md` |
| 矩阵/坏样本/失败目录 | [91-reference](02-sections/91-reference.md) | `deliverables/04-worked-example/02-sections/91-reference.md` |
| 从自己的表推到 TBox/CQ | [92-transfer](02-sections/92-transfer.md) | `deliverables/04-worked-example/02-sections/92-transfer.md` |
| 空表模板 | [93-templates](02-sections/93-templates.md) | `deliverables/04-worked-example/02-sections/93-templates.md` |
| 第二个 worked domain | [94-worked-example](02-sections/94-worked-example.md) | `deliverables/04-worked-example/02-sections/94-worked-example.md` |
| 一条查询的旅程 | [95-journey](02-sections/95-journey.md) | `deliverables/04-worked-example/02-sections/95-journey.md` |
| 标签/等级从哪来 | [96-label-source](02-sections/96-label-source.md) | `deliverables/04-worked-example/02-sections/96-label-source.md` |
| 与 01/02/03 的分工 | [97-relations](02-sections/97-relations.md) | `deliverables/04-worked-example/02-sections/97-relations.md` |
| 证据台账 / 标准卡 | [04-evidence](04-evidence/) | `deliverables/04-worked-example/04-evidence/` |
| fixture（可选跑） | [05-example](05-example/README.md) | `deliverables/04-worked-example/05-example/` |

## 阅读顺序

| 时间 | 读什么 |
|---|---|
| 10 分钟 | 本页 → [overview §0.1–§0.4](02-sections/00-overview.md) → [6 行契约模板](02-sections/93-templates.md) |
| 30 分钟 | [01-GUIDE](02-sections/01-GUIDE.md) 的 8 步：契约 → TBox → shape → 三关 → CQ → policy → audit → journey |
| 动手 | 03-body/01-build → 02-consume → 03-govern；配合 92-transfer 与 93-templates |
| 评审 | 04-boundaries → 05-acceptance → 91-reference → 06-decision |

## 维护

- **验收与 `conditional` 以 [05-acceptance](02-sections/05-acceptance.md) 与 [06-decision](02-sections/06-decision.md) 为准**。
- 改产物：先改 [03-body](03-body/)，再回 00-overview 与 91-reference。
- 术语来源：`N:` / `local` 读法见 [90-glossary §0](02-sections/90-glossary.md#term-sources)。
- 本页只做索引；不新增判断，不复制正文。
