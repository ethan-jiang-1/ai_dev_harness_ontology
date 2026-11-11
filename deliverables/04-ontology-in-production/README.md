---
status: draft
deliverable_status: draft
updated: 2026-11-11
target: 要落地一个小型本体查询应用的团队
basis: E-12/E-19/E-20/E-21/E-22/E-23/E-24/E-25/E-27；E-02/E-04/E-06/E-26 已撤回；工程产物；未测
---

# 04 · 从本体到应用：建、用、治

> **证据重置**：E-02/E-04/E-06/E-26 撤回（W 表见 [evidence/ledger](./evidence/ledger.md)）；E-12/E-19/E-20/E-21–E-25/E-27 仍可用。


> **给谁**：一个要落地小型本体查询应用的小团队——做数据/本体的人、做应用/agent 的人、做治理/安全的人，共用一套产物。
> **解决什么**：把「消费者要什么」变成可读的 Turtle、可对照的 3 条查询、可对照的策略（10/11 有唯一期望；11 条测试未跑）、可审计的决策记录。
> **不解决**：值不值得做（去 [01](../01-capability-status/README.md)）、接缝怎么选（去 [02](../02-engineering-playbook/README.md)）、为什么是这些位置（去 [03](../03-mechanism-reference/README.md)）。
>
> **怎么用**：第一次读 §0 → [GUIDE](./GUIDE.md) 选一条路径 → §3 选一个起点；不要从第一页读到最后一页。卡住查 [症状地图](./sections/map.md)，做完查 [验收清单](./sections/acceptance.md)。
>
> **第一次来**：先读 [START](../START.md)（10 分钟），再回本份。
>
> **内码**：A.x/B.x/C.x = 建/用/治三册；E-xx = 跨派结论；T: = topics 页；S: = src digest；O-xx = 对象地址；T9 = steward 读表这条优先级测试；X1–X5 = 04 的验收期待。完整解释见 [术语](./sections/glossary.md)。
>
> **词源（只定词，不撑效果）**：本体/顶层本体 = `N: ISO/IEC 21838-1/-2`；约束/校验/shape/三态 = `N: W3C SHACL`；策略表达/判定架构 = `N: W3C ODRL 2.2` / `N: OASIS XACML 3.0`；数据分级/个人信息 = `N: GB/T 43697-2024` / `N: GB/T 35273-2020`；数据契约 = `N: ODCS v3.1.0`。TBox/ABox、principal、level 1–4、`skip`、leak oracle = `local`（工程映射，不是标准条款）。逐词见 [术语 §0](./sections/glossary.md#term-sources)。
>
> **读者姿态**：本份面向人；主路径不要求打开 `topics/`。矩阵、失败目录、用例已消化到 [参考表](./sections/reference.md)；出处附录在 [evidence/ledger.md](./evidence/ledger.md)，可选。
>
> **宪章**：[CHARTER](../../CHARTER.md)。本份是读本/验收材料；示例是阅读对照用的 fixture，不是要交付的系统。命令片段是可选说明，不是实施任务。
>
> **为什么不用 SQL/表？** 见 [relations](./sections/relations.md)；04 不在这里下结论。

## 先看前 7 天

你带 3 个人做一个小型本体查询应用。第 1 周不要建 TBox；先写 6 行消费者契约（consumer / principal / moment / answers / refuses / load）。6 项写不出就停——这是 04 的第一个 gate（A.1）。

第 1 周结束，你手上应该有 3 件东西：

| # | 产物 | 现在的验收 | 没有怎么办 |
|---|---|---|---|
| 1 | 消费者契约 6 项 | **A1 硬检查**：6 项无空；governance 行 principal=governance；每行 1 个 CQ 或拒绝条件 | 回 A.1，不建 TBox |
| 2 | principal 模型 + 多标签规则两个决策 | **没有硬验收**：X2/X3 自己标「未闭合 / 缺多标签 fixture」；至少要写决策、owner、失败条件 | 标 `conditional`（有条件通过，不是失败），不要假装通过 |
| 3 | 3 条 CQ 草稿 | **fixture 之外没有硬验收**：每条有 expected + 0 行分因（[transfer §3](./sections/transfer.md) / §7）；A5 只对 fixture 的 2/2、7/4、4 负责 | 回 transfer §2–§3，不要先写查询 |

> 这三件是 04 的「第一周可交付」，不是工期承诺；成本/阶段见 [decision](./sections/decision.md)。

**前 7 天怎么排（示意，不是报价）**：

| 天 | 做什么 | 产出 | 验收 |
|---|---|---|---|
| 1 | 拉 3 个 owner（数据/应用/治理），写 6 行契约 | 契约草稿 | 6 项无空 |
| 2 | 定 principal 模型 + 多标签规则 | 两个决策 + owner | 写失败条件；否则 `conditional` |
| 3–4 | 从契约推 TBox（≤11 类） | `ontology.ttl` / `catalog.ttl` | 类/属性计数对得上 |
| 5 | 写 2 条 shape + 负例 | `shapes.ttl` + 负例表 | 2/2 有 target |
| 6 | 3 条 CQ + expected | 查询草稿 | 每条 expected + 0 行分因 |
| 7 | 跑三关，写 `build_report` | `build_report` | load/validate/answer 有记录 |

> 第 7 天的最小声响是「三关有记录」，不是「全部通过」；`targeted=0` 不是 pass。

> **只读 5 页（约 30 分钟）**：本页 §0 → [GUIDE 30 分钟 8 步](./GUIDE.md#p-30min) → [A.1 / A.3 / A.5](./body/build.md) → [B.2](./body/consume.md) → [C.3 / C.4](./body/govern.md)。
>
> **证据等级**：本份是读本/验收材料；示例是 fixture，数字是期望值，不是实测；`conditional` 不是失败，是未决项。

## 0. 你带着什么问题来

| 你的问题 | 先看 |
|---|---|
| 我该不该做本体查询应用？ | 04 不回答；先看 [01](../01-capability-status/README.md) |
| 我第一步做什么？ | [GUIDE 30 分钟 8 步](./GUIDE.md#p-30min) |
| 我怎么从自己的表开始？ | [从你的表到这条链](./sections/transfer.md) · [第二个例子](./sections/worked-example.md) |
| 我的标签/等级从哪来？ | [标签来源](./sections/label-source.md) |
| 有没有空表可填？ | [可填模板](./sections/templates.md) |
| 我要准备什么？ | [A.1 消费者契约](./body/build.md) |
| 我怎么建最小本体？ | [A.3](./body/build.md) → [A.4](./body/build.md) |
| 我怎么知道建够了？ | [A.5 三关](./body/build.md) |
| 我该选哪条查询路线？ | [B.0 决定表](./body/consume.md) |
| 查询 0 行怎么办？ | [B.2 空结果分因](./body/consume.md) |
| 我怎么防止泄漏？ | [C.3 泄漏用例](./body/govern.md) |
| 我怎么审计？ | [C.4 audit schema](./body/govern.md) |
| 我做到什么程度算完？ | [§4 验收](#4-验收5-组门槛) + [验收清单](./sections/acceptance.md) |
| 这笔投入该不该批？ | [决策支持](./sections/decision.md) |
| 我卡住了？ | [症状地图](./sections/map.md) |
| 哪些话能信？ | [§5 不能证明什么](#5-不能证明什么3-条) + [边界](./sections/boundaries.md) |

## 1. 怎么读

> 30 分钟 8 步、2 小时、1 天的路径都在 [GUIDE](./GUIDE.md)；本页只留入口，不重复读法。

- 先判断要不要读：§0。
- 要一条最小链：[GUIDE 30 分钟](./GUIDE.md#p-30min)（8 步）。
- 要动手：[transfer](./sections/transfer.md) + [templates](./sections/templates.md)。
- 要拍板：[decision](./sections/decision.md)。

## 2. 九件产物地图

| # | 产物 | 谁产 | 何时 | 怎么验 | 文件 |
|---|---|---|---|---|---|
| 1 | 消费者契约 | 数据/应用/治理三方 | 立项 | 6 项无空；每行有 1 个 CQ 或拒绝条件 | [build A.1](./body/build.md) |
| 2 | TBox + ABox | 数据/本体 | 建 | `rdflib` 解析；11 类/5 属性 | [ontology.ttl](./example/ontology.ttl) · [catalog.ttl](./example/catalog.ttl) |
| 3 | shapes + 负例 | 数据/本体 | 建 | `pyshacl` 报 2 violations | [shapes.ttl](./example/shapes.ttl) · [A.4](./body/build.md) |
| 4 | 3 条 SPARQL | 应用 | 用 | CQ1 2 列 2 表（steward，数据管家身份）/ CQ2 7 列 4 表（steward）/ CQ3 4 数据集（governance），raw | [B.2](./body/consume.md) |
| 5 | policy 表 | 治理 | 治 | 8 条规则；T9（steward 读表的优先级测试）未定；T11 governance dataset allow | [policy.json](./example/policy.json) · [C.2](./body/govern.md) |
| 6 | 策略测试 | 治理 | 治 | 11 条输入→期望；T9 undetermined | [policy_tests.json](./example/policy_tests.json) |
| 7 | 泄漏用例 | 治理 | 治 | 12 条测试设计；object/alias/聚合/版本；部分需额外 fixture | [leak_cases.json](./example/leak_cases.json) |
| 8 | audit schema + 3 条记录 | 治理 | 治 | 必填字段齐；同 fixture 对照；严格 replay 需 hash/parser | [audit.schema.json](./example/audit.schema.json) · [audit_records.json](./example/audit_records.json) · [C.4](./body/govern.md) |
| 9 | 故障矩阵 | 三段共同 | 验收 | 10 类 × 3 段；骨架，不是实测 | [fault_matrix.json](./example/fault_matrix.json) |

> `build_report` 是 [A.5](./body/build.md) 的内联样例，不单独成文件；9 件产物不变。

## 3. 四个常见起点

| 你的情况 | 走法 | 可以跳过 |
|---|---|---|
| 只有 5 张表，想先读懂一条链 | A.1 → A.3 → A.4 → A.5 → B.2（CQ1/CQ3；A.2 默认结构表） | OBDA、纠错 2×2、故障矩阵 |
| 有关系库 + 稳定 schema | B.0 → B.4（OBDA） → C.1 | KG 构建、agentic navigation |
| 还没有本体，只有 endpoint | A.3（最小 11 类） → B.0（agentic navigation） | 完整 OWL、reasoner |
| 查询能返回，但不敢上线 | C.1 → C.3（LEAK-T1 探针） → C.4（audit） | 建/用全章 |

> 如果你只是想在自己的表上动手，不走上面四个起点：直接读 [transfer](./sections/transfer.md) §2–§7，再用 [templates](./sections/templates.md)。

## 4. 验收（5 组门槛）

> 5 组、通过长什么样、可勾项与当前 `conditional` 结论都在 [验收清单](./sections/acceptance.md)。入口：A1–A4 / A5+B1–B3 / C1–C3 / C4–C5 / 无未修漏洞。
>
> `conditional`（有条件通过，不是失败）的处置与停见 [decision](./sections/decision.md)；GUIDE 的 10 分钟/2 小时/1 天是阅读路径，不是门槛数。

## 5. 不能证明什么（3 条）

> 不证明效果、不证明跨域/规模、不证明生产；细节、17 条边界与反例见 [边界](./sections/boundaries.md)。

## 6. 三章与支持页

| 你要做的事 | 读 |
|---|---|
| 建：契约 → 表示 → 本体 → shapes → 三关 | [A · 建](./body/build.md) |
| 用：资产 → 路线 → 3 CQ → 空结果 → 纠错/OBDA | [B · 用](./body/consume.md) |
| 治：三层 → 策略/判定顺序 → skip/leak → 审计 | [C · 治](./body/govern.md) |
| 看一条查询从头到尾 | [journey](./sections/journey.md) |
| 查术语/内码/版本 | [glossary](./sections/glossary.md) |
| 对照同一 fixture（可选跑） | [example/README.md](./example/README.md#5-分钟跑通可选) |
| 查矩阵/坏样本/失败目录 | [参考表](./sections/reference.md) |
| 从自己的表推到 TBox/CQ | [transfer](./sections/transfer.md) · [worked-example](./sections/worked-example.md) |
| 标签/等级从哪来 | [label-source](./sections/label-source.md) |
| 填空模板 | [templates](./sections/templates.md) |
| 成本/工期/conditional | [decision](./sections/decision.md) |
| 卡住了 | [症状地图](./sections/map.md) |
| 验收 | [验收清单](./sections/acceptance.md) |
| 与 01/02/03 的分工 | [关系](./sections/relations.md) |
| 证据台账（附录） | [evidence/ledger.md](./evidence/ledger.md) |
| 标准卡/外部 signal | [evidence/sources.md](./evidence/sources.md) | 6 张标准卡；未入库 signal 清单 |

> 读法：**先读本章开头「本章回答 / 你需要准备 / 做完得到什么」，再按小节读**。章末的「证据与边界」第一遍可跳过。
>
> 内码：`E-xx` = 跨派结论；`T:` = topics 页；`S:` = src digest；`O-xx` = 对象地址；`F/K` = 派内 finding / N&D 实验条件代号（非标准）；`推测 / 未测` = 证据等级。完整解释见 [glossary](./sections/glossary.md)。第一遍可以跳过；需要时再回 [evidence/ledger.md](./evidence/ledger.md)。
