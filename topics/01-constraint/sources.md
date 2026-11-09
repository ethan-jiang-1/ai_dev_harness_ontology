---
status: draft
updated: 2026-11-09
---

# 01 约束派 · 证据源

| 来源（digest） | 类型 | 阅读 | 支撑 | 备注 |
|---|---|---|---|---|
| [POLAR digest](../../src/papers/2610.08082-polar/digest.md) | preprint | 精读 | 01-L1, 01-L2, 01-L6, 01-L7 | [card](../../src/papers/2610.08082-polar/card.md)（provenance）；T1-only ≈ blanket veto；false-veto 未测；retail 回退不能归因误拦 |
| [Commit Boundary digest](../../src/papers/2610.37407-commit-boundary/digest.md) | preprint | 精读 | 01-L13 / 01-L14 | [card](../../src/papers/2610.37407-commit-boundary/card.md)（provenance）；概念架构，无实现；未升 E；**不要挂 E-05**（E-05 = FIRME） |
| [OntoAct digest](../../src/papers/2610.21983-ontoact/digest.md) | preprint | 精读 | 01-L3 / 01-L11 / 01-L12 / 01-L15 | [card](../../src/papers/2610.21983-ontoact/card.md)（provenance）；三值条件 + 假设 revision；Tacit-FLE 三个规模；elimination 上 IfR 匹配/超过 |
| [多 agent 差分诊断 digest](../../src/papers/2610.36325-ontology-multiagent-diagnosis/digest.md) | preprint | 精读 | 01-L3 / 01-L15 | [card](../../src/papers/2610.36325-ontology-multiagent-diagnosis/card.md)（provenance）；Q4DX 单基准；curated KG 未覆盖诊断恒 0 |
| [CASEL digest](../../src/papers/2610.36570-casel/digest.md) | paper | 精读 | 01-L4, 01-L5, 01-L8, 01-L9, 01-L10 | [card](../../src/papers/2610.36570-casel/card.md)（provenance）；模拟；γ_m 假设；主表 `τ̂=∞`；NoRev 非单变量 |
| [trustgraph digest](../../src/open-source/trustgraph-ai-trustgraph/digest.md) | open-source | 已读代码 | 01-L13 / commit-gate F5 | [card](../../src/open-source/trustgraph-ai-trustgraph/card.md)（provenance）；读路径 SHACL-AF 策略过滤，31 条单测已跑；写路径 commit gate 未定位 |

> **本派没有 Commit Boundary 的 E-xx**：`01-L13/L14` 只在派内使用。`conclusions` 的 E-05 是 FIRME；Commit Boundary digest 的 `claims: [E-05]` 与 §8 的 E-05 回链都是错挂，**2026-11-09 已回改**（`claims: []`，§8 改为“不挂 E-xx”）。
>
> **数字口径**：01-L11 用 OntoAct digest 的 78.6/83.3/90.0%（IfR 64.3/66.7/65.0%）、SI `1.6–2.4`；`conclusions` 的 E-16 已于 2026-11-09 按同口径回改。CASEL 主表是 `τ̂=∞`，不要把 7.02% 当阈值开启后的结果。
