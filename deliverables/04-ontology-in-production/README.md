---
status: draft
deliverable_status: draft
updated: 2026-11-10
target: 要落地一个小型本体查询应用的团队
basis: E-02/E-04/E-06/E-12/E-19/E-20/E-21/E-22/E-23/E-24/E-25/E-26/E-27；工程产物；未测
---

# 04 · 从本体到应用：建、用、治

> **给谁**：一个要落地小型本体查询应用的小团队——做数据/本体的人、做应用/agent 的人、做治理/安全的人，共用一套产物。
> **解决什么**：把「消费者要什么」变成可读的 Turtle、可对照的 3 条查询、可判定的策略、可回放的审计。
> **不解决**：值不值得做（去 [01](../01-capability-status/README.md)）、接缝怎么选（去 [02](../02-engineering-playbook/README.md)）、为什么是这些位置（去 [03](../03-mechanism-reference/README.md)）。
>
> **怎么用**：第一次读 §0 → §1 → §3 选一个起点；不要从第一页读到最后一页。卡住查 [症状地图](./sections/map.md)，做完查 [验收清单](./sections/acceptance.md)。
>
> **读者姿态**：本份面向人；主路径不要求打开 `topics/`。矩阵、失败目录、用例已消化到 [参考表](./sections/reference.md)；出处附录在 [evidence](./evidence/README.md)，可选。
>
> **宪章**：[CHARTER](../../CHARTER.md)。本份是读本/验收材料；示例是阅读对照用的 fixture，不是要交付的系统。命令片段是可选说明，不是实施任务。
>
> **为什么不用 SQL/表直接做？** 04 不展开；它只说明本链假设的差异：本体把类/属性/标签/策略写成可查询的图，才能让 TBox、shape、CQ、policy 共用同一套标识。若你还在比较表/视图/本体，先看 [01](../01-capability-status/README.md)；04 不在这里下结论。

## 0. 你带着什么问题来

| 你的问题 | 先看 |
|---|---|
| 我该不该做本体查询应用？ | 04 不回答；先看 [01](../01-capability-status/README.md) |
| 我第一步做什么？ | [§1 30 分钟读路径](#1-30-分钟读路径不要求跑) |
| 我要准备什么？ | [A.1 消费者契约](./body/build.md) |
| 我怎么建最小本体？ | [A.3](./body/build.md) → [A.4](./body/build.md) |
| 我怎么知道建够了？ | [A.5 三关](./body/build.md) |
| 我该选哪条查询路线？ | [B.0 决定表](./body/consume.md) |
| 查询 0 行怎么办？ | [B.2 空结果分因](./body/consume.md) |
| 我怎么防止泄漏？ | [C.3 泄漏用例](./body/govern.md) |
| 我怎么审计？ | [C.4 audit schema](./body/govern.md) |
| 我做到什么程度算完？ | [§4 验收](#4-验收5-组门槛) + [验收清单](./sections/acceptance.md) |
| 我卡住了？ | [症状地图](./sections/map.md) |
| 哪些话能信？ | [§5 不能证明什么](#5-不能证明什么3-条) + [边界](./sections/boundaries.md) |

## 1. 30 分钟读路径（不要求跑）

> 目标不是建完，是**读懂一条最小链**：契约 → TBox → shapes → 3 条 CQ → policy → audit → 回填。下面的“核对”都是读文件/看表，不运行代码。

| 步 | 读什么 | 核对什么 | 去哪 |
|---|---|---|---|
| 1 | 消费者契约 3 行 | consumer/principal/moment/answers/refuses/load 是否齐；governance 是 `governance` 不是 analyst | [A.1](./body/build.md) |
| 2 | 最小 TBox + ABox | 11 类/5 属性；`WorkEmail` 是 `Email` 子类；5 表/13 列 | [A.2](./body/build.md)–[A.3](./body/build.md) |
| 3 | 2 条 shape + 负例表 | 每条约束有已知违反 + 干净样本；范围 1–4 | [A.4](./body/build.md) |
| 4 | `build_report` 三关 | load/validate/answer 各记什么；`targeted=0` 不是 pass；版本来源表 | [A.5](./body/build.md) |
| 5 | 3 条 CQ | raw 2 / 7 列 4 表 / 4；每条 principal；0 行分因 | [B.0](./body/consume.md)–[B.2](./body/consume.md) |
| 6 | 8 条 policy + 判定顺序 | 复算 T1/T2/T7/T9/T11；T9 为什么 undetermined | [C.2](./body/govern.md) |
| 7 | 3 条 audit + query log | per-subject vs query 级；skip/returned vs skip/withheld | [C.4](./body/govern.md) |
| 8 | journey | 能说出 CQ1 steward vs analyst 的差别 | [journey](./sections/journey.md) |

这 8 步只读；不要求安装 `rdflib`/`pyshacl`，不要求跑 SPARQL。要看“一条查询从头到尾”，读 [journey](./sections/journey.md)；要自己试跑，见 [example](./example/README.md) 的可选片段。

## 2. 九件产物地图

| # | 产物 | 谁产 | 何时 | 怎么验 | 文件 |
|---|---|---|---|---|---|
| 1 | 消费者契约 | 数据/应用/治理三方 | 立项 | 6 项无空；每行有 1 个 CQ 或拒绝条件 | [build A.1](./body/build.md) |
| 2 | TBox + ABox | 数据/本体 | 建 | `rdflib` 解析；11 类/5 属性 | [ontology.ttl](./example/ontology.ttl) · [catalog.ttl](./example/catalog.ttl) |
| 3 | shapes + 负例 | 数据/本体 | 建 | `pyshacl` 报 2 violations | [shapes.ttl](./example/shapes.ttl) · [A.4](./body/build.md) |
| 4 | 3 条 SPARQL | 应用 | 用 | CQ1 2（steward）/ CQ2 7 列 4 表（steward）/ CQ3 4（governance），raw | [B.2](./body/consume.md) |
| 5 | policy 表 | 治理 | 治 | 8 条规则；T9 未定；T11 governance dataset allow | [policy.json](./example/policy.json) · [C.2](./body/govern.md) |
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

## 4. 验收（5 组门槛）

> 5 组门槛；完整可勾项见 [验收清单](./sections/acceptance.md)。GUIDE 的 10 分钟/2 小时/1 天是阅读路径，不是门槛数。

| # | 组 | 通过长什么样 |
|---|---|---|
| 1 | A1–A4 | 契约 6 项无空；3 个 TTL 可解析；2 个 shape 有 target；2/2 坏样本被抓住 |
| 2 | A5 + B1–B3 | CQ1 2 / CQ2 7 列 4 表 / CQ3 4（raw，标 principal）；路线有记录；0 行分因 |
| 3 | C1–C3 | 三层来源清；11 条策略测试 10 条唯一、T9 undetermined；LEAK-T1 敏感 object 不出现 |
| 4 | C4–C5 | 3 条 audit 必填齐；同 fixture 对照；12 条 leak 有期望 |
| 5 | 无未修漏洞 | object 泄漏、T9、`targeted=0`、写授权 |

> 这些是 fixture 的期望值，不是运行记录；跑出不同数先查 `rdflib`/`pyshacl` 版本与 ABox 类型，不要先改数据。

完整可勾版：[验收清单](./sections/acceptance.md)。

## 5. 不能证明什么（3 条）

- **不证明效果**：建=标准/工程产物；用=三条路线各单设置、无头对头；治=单企业 + 单实现。
- **不证明跨域/规模**：fixture 只有 5 表/13 列；200 表/5,000 列只是 Glyph 的量级参照，不是本 fixture。
- **不证明生产**：没有真实误报率、延迟、审计 replay 实测；示例数字只说明这张例子自洽，不是运行记录。

更细的 17 条边界见 [boundaries](./sections/boundaries.md)。

## 6. 三章与附录

| 你要做的事 | 读 |
|---|---|
| 建：契约 → 表示 → 本体 → shapes → 三关 | [A · 建](./body/build.md) |
| 用：资产 → 路线 → 3 CQ → 空结果 → 纠错/OBDA | [B · 用](./body/consume.md) |
| 治：三层 → 策略/判定顺序 → skip/leak → 审计 | [C · 治](./body/govern.md) |
| 看一条查询从头到尾 | [journey](./sections/journey.md) |
| 查术语/内码/版本 | [glossary](./sections/glossary.md) |
| 对照同一 fixture（可选跑） | [example](./example/README.md) |
| 查矩阵/坏样本/失败目录 | [参考表](./sections/reference.md) |
| 卡住了 | [症状地图](./sections/map.md) |
| 验收 | [验收清单](./sections/acceptance.md) |
| 与 01/02/03 的分工 | [关系](./sections/relations.md) |
| 附录索引 | [sections/README](./sections/README.md) |
| 证据台账（附录） | [evidence](./evidence/README.md) |

> 读法：**先读本章开头「本章回答 / 你需要准备 / 做完得到什么」，再按小节读**。章末的「证据与边界」第一遍可跳过。
>
> 内码：`E-xx` = 跨派结论；`T:` = topics 页；`S:` = src digest；`O-xx` = 对象地址；`F/K` = 派内 finding/知识层级；`推测 / 未测` = 证据等级。完整解释见 [glossary](./sections/glossary.md)。第一遍可以跳过；需要时再回 [evidence](./evidence/README.md)。
