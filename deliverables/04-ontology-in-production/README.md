---
status: draft
deliverable_status: draft
updated: 2026-11-10
target: 要落地一个小型本体查询应用的团队
basis: E-02/E-04/E-06/E-12/E-19/E-20/E-21/E-22/E-23/E-24/E-25/E-26/E-27；工程产物；未测
---

# 04 · 从本体到应用：建、用、治

> **给谁**：一个要落地小型本体查询应用的小团队——做数据/本体的人、做应用/agent 的人、做治理/安全的人，共用一套产物。
> **解决什么**：把「消费者要什么」变成可加载的 Turtle、能跑的 3 条查询、可判定的策略、可回放的审计。
> **不解决**：值不值得做（去 [01](../01-capability-status/README.md)）、接缝怎么选（去 [02](../02-engineering-playbook/README.md)）、为什么是这些位置（去 [03](../03-mechanism-reference/README.md)）。
>
> **怎么用**：第一次读 §0 → §1 → §3 选一个起点；不要从第一页读到最后一页。卡住查 [症状地图](./sections/map.md)，做完查 [验收清单](./sections/acceptance.md)。
>
> **读者姿态**：本份面向人；主路径不要求打开 `topics/`。矩阵、失败目录、用例已消化到 [参考表](./sections/reference.md)；出处附录在 [evidence](./evidence/README.md)，可选。

## 0. 你带着什么问题来

| 你的问题 | 先看 |
|---|---|
| 我该不该做本体查询应用？ | 04 不回答；先看 [01](../01-capability-status/README.md) |
| 我第一步做什么？ | [§1 30 分钟路径](#1-30-分钟路径) |
| 我要准备什么？ | [A.1 消费者契约](./body/build.md) |
| 我怎么建最小本体？ | [A.3](./body/build.md) → [A.4](./body/build.md) |
| 我怎么知道建够了？ | [A.5 三关](./body/build.md) |
| 我该选哪条查询路线？ | [B.0 决定表](./body/consume.md) |
| 查询 0 行怎么办？ | [B.2 空结果分因](./body/consume.md) |
| 我怎么防止泄漏？ | [C.3 泄漏用例](./body/govern.md) |
| 我怎么审计？ | [C.4 audit schema](./body/govern.md) |
| 我做到什么程度算完？ | [§4 验收](#4-验收6-条) + [验收清单](./sections/acceptance.md) |
| 我卡住了？ | [症状地图](./sections/map.md) |
| 哪些话能信？ | [§5 不能证明什么](#5-不能证明什么3-条) + [边界](./sections/boundaries.md) |

## 1. 30 分钟路径

> 目标不是建完，是**跑通一条最小链**：契约 → TBox → shapes → 1 条 CQ → 1 条策略 → 1 条 audit → 回填。

| 步 | 做什么 | 产物 | 做完看哪 |
|---|---|---|---|
| 1 | 填 3 行消费者契约（consumer / principal / moment / answers / refuses / load） | 契约表 | [A.1](./body/build.md) |
| 2 | 按消费者选表示档位，建最小 TBox + ABox（本 fixture 11 类/5 属性；5 表/13 列） | `ontology.ttl` + `catalog.ttl` | [A.2](./body/build.md)–[A.3](./body/build.md) |
| 3 | 每条约束配一个 shape + 一个已知违反 + 一个干净样本 | `shapes.ttl` | [A.4](./body/build.md) |
| 4 | 跑 `rdflib` + `pyshacl`，把结果写进 `build_report` | `build_report` | [A.5](./body/build.md) |
| 5 | 按资产选查询路线，跑 CQ1（Email 列） | 1 条 SPARQL | [B.0](./body/consume.md)–[B.2](./body/consume.md) |
| 6 | 写 `policy.json`（7 条规则），跑 T1/T2/T7 | policy 表 + decision | [C.2](./body/govern.md) |
| 7 | 填 2 条 audit（CQ2 + LEAK-T1），确认能 replay | `audit_records.json` | [C.4](./body/govern.md) |
| 8 | 回填 `build_report` 的 `answer` 与版本（B/C 完成后） | `build_report` v2 | [A.5](./body/build.md) |

第 4 步的 `answer` 与版本字段，在 B.2/C.2 完成后回填 A.5；跑完这 8 步，再决定要不要做全量 3 条 CQ、12 条泄漏用例与 10 类故障矩阵。

## 2. 九件产物地图

| # | 产物 | 谁产 | 何时 | 怎么验 | 文件 |
|---|---|---|---|---|---|
| 1 | 消费者契约 | 数据/应用/治理三方 | 立项 | 6 项无空；每行有 1 个 CQ 或拒绝条件 | [build A.1](./body/build.md) |
| 2 | TBox + ABox | 数据/本体 | 建 | `rdflib` 解析；11 类/5 属性 | [ontology.ttl](./example/ontology.ttl) · [catalog.ttl](./example/catalog.ttl) |
| 3 | shapes + 负例 | 数据/本体 | 建 | `pyshacl` 报 2 violations | [shapes.ttl](./example/shapes.ttl) · [A.4](./body/build.md) |
| 4 | 3 条 SPARQL | 应用 | 用 | CQ1 2 / CQ2 7 列 4 表 / CQ3 4 | [B.2](./body/consume.md) |
| 5 | policy 表 | 治理 | 治 | 7 条规则；T9 未定 | [policy.json](./example/policy.json) · [C.2](./body/govern.md) |
| 6 | 策略测试 | 治理 | 治 | 10 条输入→期望 | [policy_tests.json](./example/policy_tests.json) |
| 7 | 泄漏用例 | 治理 | 治 | 12 条；object/alias/聚合 | [leak_cases.json](./example/leak_cases.json) |
| 8 | audit schema + 2 条记录 | 治理 | 治 | 必填字段齐；至少 1 条 replay | [audit.schema.json](./example/audit.schema.json) · [audit_records.json](./example/audit_records.json) · [C.4](./body/govern.md) |
| 9 | 故障矩阵 | 三段共同 | 验收 | 10 类 × 3 段 | [fault_matrix.json](./example/fault_matrix.json) |

## 3. 四个常见起点

| 你的情况 | 走法 | 可以跳过 |
|---|---|---|
| 只有 5 张表，想先跑通 | A.1 → A.3 → A.4 → A.5 → B.2（CQ1/CQ3；A.2 默认结构表） | OBDA、纠错 2×2、故障矩阵 |
| 有关系库 + 稳定 schema | B.0 → B.4（OBDA） → C.1 | KG 构建、agentic navigation |
| 还没有本体，只有 endpoint | A.3（最小 11 类） → B.0（agentic navigation） | 完整 OWL、reasoner |
| 查询能跑，但不敢上线 | C.1 → C.3（LEAK-T1 探针） → C.4（audit） | 建/用全章 |

## 4. 验收（6 条）

> 6 个检查归成 5 组门槛；GUIDE 的 3 条是阅读路径，不是验收数。完整可勾版见 [验收清单](./sections/acceptance.md)。

| # | 检查 | 通过长什么样 |
|---|---|---|
| 1 | 契约 | 6 项无空；每行能指出 1 个 CQ 或 1 个拒绝条件 |
| 2 | 可加载/可校验 | 3 个 TTL 解析；`pyshacl` 报 2 个已知 violation；`targeted>0` |
| 3 | 可查询 | CQ1 2 行、CQ2 7 列/4 表、CQ3 4 个 dataset；0 行必须分因 |
| 4 | 可判定 | 10 条策略测试中 9 条有唯一期望；T9 必须显式 `undetermined` |
| 5 | 可审计 | `audit.schema.json` 必填字段齐；同一 `decision_id` 能用版本+快照 replay |
| 6 | 治理 | LEAK-T1 探针应为 0 行；当前 fixture 预期返回行 → 默认 `conditional`，不是 pass |

> 这些是 fixture 的期望值，不是运行记录；跑出不同数先查 `rdflib`/`pyshacl` 版本与 ABox 类型，不要先改数据。

完整可勾版：[验收清单](./sections/acceptance.md)。

## 5. 不能证明什么（3 条）

- **不证明效果**：建=标准/工程产物；用=三条路线各单设置、无头对头；治=单企业 + 单实现。
- **不证明跨域/规模**：fixture 只有 5 表/13 列；200 表/5,000 列只是 Glyph 的量级参照，不是本 fixture。
- **不证明生产**：没有真实误报率、延迟、审计 replay 实测；示例数字只证明这张例子跑通。

更细的 12 条边界见 [boundaries](./sections/boundaries.md)。

## 6. 三章与附录

| 你要做的事 | 读 |
|---|---|
| 建：契约 → 表示 → 本体 → shapes → 三关 | [A · 建](./body/build.md) |
| 用：资产 → 路线 → 3 CQ → 空结果 → 纠错/OBDA | [B · 用](./body/consume.md) |
| 治：三层 → 策略 → 泄漏 → 审计 | [C · 治](./body/govern.md) |
| 跑一遍同一 fixture | [example](./example/README.md) |
| 查矩阵/坏样本/失败目录 | [参考表](./sections/reference.md) |
| 卡住了 | [症状地图](./sections/map.md) |
| 验收 | [验收清单](./sections/acceptance.md) |
| 与 01/02/03 的分工 | [关系](./sections/relations.md) |
| 附录索引（四个问题） | [sections/README](./sections/README.md) |
| 证据台账（附录） | [evidence](./evidence/README.md) |

> 读法：**先读本章开头「本章回答 / 你需要准备 / 做完得到什么」，再按小节做**。章末的「证据与边界」第一遍可跳过。
>
> 内码：`E-xx` = 跨派结论；`T:` = topics 页；`S:` = src digest；`推测 / 未测` = 证据等级。第一遍可以跳过；需要时再回 [evidence](./evidence/README.md)。
