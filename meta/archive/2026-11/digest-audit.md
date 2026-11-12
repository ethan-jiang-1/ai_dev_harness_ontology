---
status: superseded
updated: 2026-11-08
---

> **历史快照（2026-11-08/09）**：已归档，不再维护。现行规则见 `meta/README.md`，当前状态见 `meta/status/state.md`。文中的计数与结论可能已被后续修复取代。


# digest 自包含审计

## 标准

单篇 `digest.md` 必须能**脱离 `card.md` / `paper.md` 独立阅读**。检查项：

1. **三句话**：问什么、怎么做、发现什么。
2. **术语**：读数字前必须懂的词有解释。
3. **方法**：数据/模型/方法/指标讲得清，有一个具体例子。
4. **数字**：带条件（数据、模型、样本量、设置）；不是裸数字。
5. **不能说明什么**：外推边界、指标混淆、作者限定、读者推断分开。
6. **工程用法**：复刻第一步、关键参数/成本、何时用/别用。
7. **自包含**：不靠「详见 card」补内容；链接只放原文/代码。
8. **长度**：L3 150–250 行；L2 100–200；L1 50–100。

## 审计表

| 级别 | 论文 | 当前行数 | card 链接 | G1/G2 | 状态 |
|---|---|---|---|---|---|
| L1 | 2510.26683-evontree | 84 | 1 | pass（Wave 2 数字抽查） | 已达标 |
| L1 | 2610.37123-sfe-o | 83 | 1 | pass（Wave 2 数字抽查） | 已达标 |
| L1 | 2610.41785-peeling-matryoshka | 82 | 1 | pass（Wave 2 数字抽查） | 已达标 |
| L1 | 2610.41901-rex-gg | 81 | 1 | pass（Wave 2 数字抽查） | 已达标 |
| L2 | 2610.01618-agents-are-systems | 185 | 1 | pass（Wave 2 数字抽查） | 已达标 |
| L2 | 2610.21466-caston-refinement | 156 | 1 | pass（Wave 2 数字抽查） | 已达标 |
| L2 | 2610.36325-ontology-multiagent-diagnosis | 167 | 1 | pass（Wave 2 数字抽查） | 已达标 |
| L2 | 2610.36335-oa-rag | 200 | 1 | pass（Wave 2 数字抽查） | 已达标 |
| L2 | 2610.37407-commit-boundary | 156 | 1 | pass（Wave 2 数字抽查） | 已达标 |
| L2 | 2611.03743-evomemstate | 163 | 1 | pass（Wave 2 数字抽查） | 已达标 |
| L3 | 2610.08082-polar | 214 | 1 | pass（Wave 1） | 已达标 |
| L3 | 2610.11768-narrow-and-deep | 206 | 1 | pass（Wave 1） | 已达标 |
| L3 | 2610.21983-ontoact | 192 | 1 | pass（Wave 1） | 已达标 |
| L3 | 2610.35267-diagnose-workflow | 176 | 1 | pass（Wave 1） | 已达标 |
| L3 | 2610.36570-casel | 192 | 1 | pass（Wave 1） | 已达标 |
| L3 | 2610.37809-what-does-an-ontology-catch | 206 | 1 | pass（Wave 1） | 已达标 |
| L3 | 2610.38326-mioe | 150 | 1 | pass（Wave 1） | 已达标 |
| L3 | 2610.40482-firme | 188 | 1 | pass（Wave 1） | 已达标 |
| L3 | 2610.41172-context-as-infrastructure | 211 | 1 | pass（Wave 1） | 已达标 |
| L3 | 2611.01276-ontodoc | 164 | 1 | pass（Wave 1） | 已达标 |
| L3 | 2611.02395-solver-like-behavior | 195 | 1 | pass（Wave 1） | 已达标 |
| L3 | 2611.03534-power-system-agentic | 181 | 1 | pass（Wave 1） | 已达标 |

## 状态

22 篇全部重写为自包含版本；如需复核，按下面顺序抽样即可。

## 重写顺序

1. **先 L3 承重**：CAI、POLAR、N&D、Ontology Catch、CASEL、FIRME、OntoAct、SLB、Grid、OntoDoc。
2. **再 L2**：OA-RAG、Commit Boundary、多 agent 诊断、EvoMemState、Agents are Systems、CASTON。
3. **最后 L1**：Peeling、Evontree、SFE-O、ReX-GG（50–80 行，仍要自包含）。

每改完一篇，把状态改为「已达标」并更新行数；不要用链接替代内容。
