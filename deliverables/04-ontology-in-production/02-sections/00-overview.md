---
status: draft
updated: 2026-11-12
parent: ../README.md
---

<a id="0-一页结论"></a>
# 0. 落地摘要：前 7 天、九件产物与验收

> 本页是 04 的正文第 0 章。索引与阅读顺序见 [README](../README.md)；三章正文从 [03-body/01-build](../03-body/01-build.md) 开始。

<a id="0-你带着什么问题来"></a>
## 0.1 案例：一个 3 人小团队的第 1 周

一个 3 人小团队（数据/本体、应用/agent、治理/安全）落地小型本体查询应用。第 1 周不建 TBox；先写 6 行消费者契约（consumer / principal / moment / answers / refuses / load）。6 项写不出就停——这是 04 的第一个 gate（A.1）。

第 1 周结束应有三件东西：

| # | 产物 | 现在的验收 | 没有怎么办 |
|---|---|---|---|
| 1 | 消费者契约 6 项 | **A1 硬检查**：6 项无空；governance 行 principal=governance；每行 1 个 CQ 或拒绝条件 | 回 A.1，不建 TBox |
| 2 | principal 模型 + 多标签规则两个决策 | **没有硬验收**：X2/X3 自己标「未闭合 / 缺多标签 fixture」；至少要写决策、owner、失败条件 | 标 `conditional`（有条件通过，不是失败），不要假装通过 |
| 3 | 3 条 CQ 草稿 | **fixture 之外没有硬验收**：每条有 expected + 0 行分因（[92-transfer §3](./92-transfer.md) / §7）；A5 只对 fixture 的 2/2、7/4、4 负责 | 回 transfer §2–§3，不要先写查询 |

**前 7 天怎么排（示意，不是报价）**：

| 天 | 做什么 | 产出 | 验收 |
|---|---|---|---|
| 1 | 拉 3 个 owner（数据/应用/治理），写 6 行契约 | 契约草稿 | 6 项无空 |
| 2 | 定 principal 模型 + 多标签规则 | 两个决策 + owner | 写失败条件；否则 `conditional` |
| 3–4 | 从契约推 TBox（≤11 类） | `ontology.ttl` / `catalog.ttl` | 类/属性计数对得上 |
| 5 | 写 2 条 shape + 负例 | `shapes.ttl` + 负例表 | 2/2 有 target |
| 6 | 3 条 CQ + expected | 查询草稿 | 每条 expected + 0 行分因 |
| 7 | 跑三关，写 `build_report` | `build_report` | load/validate/answer 有记录 |

> 第 7 天的最小声响是「三关有记录」，不是「全部通过」；`targeted=0` 不是 pass。三件是第一周可交付，不是工期承诺；成本见 [06-decision](./06-decision.md)。

## 0.2 九件产物地图

| # | 产物 | 谁产 | 何时 | 怎么验 | 文件 |
|---|---|---|---|---|---|
| 1 | 消费者契约 | 数据/应用/治理三方 | 立项 | 6 项无空；每行有 1 个 CQ 或拒绝条件 | [03-body/01-build](../03-body/01-build.md) |
| 2 | TBox + ABox | 数据/本体 | 建 | `rdflib` 解析；11 类/5 属性 | [ontology.ttl](../05-example/ontology.ttl) · [catalog.ttl](../05-example/catalog.ttl) |
| 3 | shapes + 负例 | 数据/本体 | 建 | `pyshacl` 期望 2 violations（未跑） | [shapes.ttl](../05-example/shapes.ttl) · [A.4](../03-body/01-build.md) |
| 4 | 3 条 SPARQL | 应用 | 用 | CQ1 2 列 2 表（steward）/ CQ2 7 列 4 表（steward）/ CQ3 4 数据集（governance），raw | [02-consume](../03-body/02-consume.md) |
| 5 | policy 表 | 治理 | 治 | 8 条规则；T9 未定；T11 governance dataset allow | [policy.json](../05-example/policy.json) · [C.2](../03-body/03-govern.md) |
| 6 | 策略测试 | 治理 | 治 | 11 条输入→期望；T9 undetermined | [policy_tests.json](../05-example/policy_tests.json) |
| 7 | 泄漏用例 | 治理 | 治 | 12 条测试设计；object/alias/聚合/版本；部分需额外 fixture | [leak_cases.json](../05-example/leak_cases.json) |
| 8 | audit schema + 3 条记录 | 治理 | 治 | 必填字段齐；同 fixture 对照；严格 replay 需 hash/parser | [audit.schema.json](../05-example/audit.schema.json) · [audit_records.json](../05-example/audit_records.json) · [C.4](../03-body/03-govern.md) |
| 9 | 故障矩阵 | 三段共同 | 验收 | 10 类 × 3 段；骨架，不是实测 | [fault_matrix.json](../05-example/fault_matrix.json) |

## 0.3 四个常见起点

| 情况 | 走法 | 可以跳过 |
|---|---|---|
| 只有 5 张表，想先读懂一条链 | A.1 → A.3 → A.4 → A.5 → B.2（CQ1/CQ3；A.2 默认结构表） | OBDA、纠错 2×2、故障矩阵 |
| 有关系库 + 稳定 schema | B.0 → B.4（OBDA） → C.1 | KG 构建、agentic navigation |
| 还没有本体，只有 endpoint | A.3（最小 11 类） → B.0（agentic navigation） | 完整 OWL、reasoner |
| 查询能返回，但不敢上线 | C.1 → C.3（LEAK-T1 探针） → C.4（audit） | 建/用全章 |

> 如果只想在自己的表上动手：读 [92-transfer §2–§7](./92-transfer.md)，再用 [93-templates](./93-templates.md)。

<a id="4-验收5-组门槛"></a>
## 0.4 验收（5 组门槛）

> 5 组、通过长什么样、可勾项与当前 `conditional` 结论都在 [05-acceptance](./05-acceptance.md)。入口：A1–A4 / A5+B1–B3 / C1–C3 / C4–C5 / 无未修漏洞。

`conditional`（有条件通过，不是失败）的处置与停见 [06-decision](./06-decision.md)；GUIDE 的 10 分钟/2 小时/1 天是阅读路径，不是门槛数。

<a id="5-不能证明什么3-条"></a>
## 0.5 不能证明什么（3 条）

> 不证明效果、不证明跨域/规模、不证明生产；细节、17 条边界与反例见 [04-boundaries](./04-boundaries.md)。
