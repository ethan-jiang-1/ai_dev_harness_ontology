---
status: draft
updated: 2026-11-09
---

# 01 约束派 · 证据源

| 来源（digest） | 类型 | 阅读 | 支撑 | 备注 |
|---|---|---|---|---|
| [POLAR digest](../../meta/audits/2026-11-11-source-purge.md#src-2610-08082) | preprint | 精读 | 01-L1, 01-L2, 01-L6, 01-L7 | [card](../../meta/audits/2026-11-11-source-purge.md#src-2610-08082)（provenance）；T1-only ≈ blanket veto；false-veto 未测；retail 回退不能归因误拦 |
| [Commit Boundary digest](../../meta/audits/2026-11-11-source-purge.md#src-2610-37407) | preprint | 精读 | 01-L13 / 01-L14 | [card](../../meta/audits/2026-11-11-source-purge.md#src-2610-37407)（provenance）；概念架构，无实现；未升 E；**不要挂 E-05**（E-05 = FIRME） |
| [OntoAct digest](../../meta/audits/2026-11-11-source-purge.md#src-2610-21983) | preprint | 精读 | 01-L3 / 01-L11 / 01-L12 / 01-L15 | [card](../../meta/audits/2026-11-11-source-purge.md#src-2610-21983)（provenance）；三值条件 + 假设 revision；Tacit-FLE 三个规模；elimination 上 IfR 匹配/超过 |
| [多 agent 差分诊断 digest](../../meta/audits/2026-11-11-source-purge.md#src-2610-36325) | preprint | 精读 | 01-L3 / 01-L15 | [card](../../meta/audits/2026-11-11-source-purge.md#src-2610-36325)（provenance）；Q4DX 单基准；curated KG 未覆盖诊断恒 0 |
| [CASEL digest](../../src/papers/2610.36570-casel/digest.md) | paper | 精读 | 01-L4, 01-L5, 01-L8, 01-L9, 01-L10 | [card](../../src/papers/2610.36570-casel/card.md)（provenance）；模拟；γ_m 假设；主表 `τ̂=∞`；NoRev 非单变量 |
| [Same Operation, Different Permission digest](../../meta/audits/2026-11-11-source-purge.md#src-2610-16838) | preprint | 精读 | —（E-04 边界） | [card](../../meta/audits/2026-11-11-source-purge.md#src-2610-16838)（provenance）；同操作/不同权限的 guardrail 评测；无本体、非 commit gate；不升 E |
| [What Can Be Enforced? digest](../../meta/audits/2026-11-11-source-purge.md#src-2607-22868) | preprint | 精读 | —（E-04 边界） | [card](../../meta/audits/2026-11-11-source-purge.md#src-2607-22868)（provenance）；false-block/miss 前沿 + conformal 校准 + 闭环；理论/诊断；无本体；不升 E |
| [trustgraph digest](../../src/open-source/trustgraph-ai-trustgraph/digest.md) | open-source | 已读代码 | 01-L13 / 01-L18 / commit-gate F5 | [card](../../src/open-source/trustgraph-ai-trustgraph/card.md)（provenance）；读路径 SHACL-AF 策略过滤，31 条单测已跑；写路径 commit gate 未定位 |
| [Glyph digest](../../src/papers/2609.10430-glyph/digest.md) | preprint | 精读 | 01-L16 / 01-L17 | [card](../../src/papers/2609.10430-glyph/card.md)（provenance）；Apple 单企业；标签层，不产策略/不执行；NDCG/MAP 是检索指标、生产接受率对 FN 盲 |
| [OPA digest](../../src/open-source/open-policy-agent-opa/digest.md) | open-source | 已读代码 | 01-L16（策略层候选） | [card](../../src/open-source/open-policy-agent-opa/card.md)（provenance）；Rego/decision API/bundle/logs；不解析 OWL/SHACL；不消费 Glyph 标签；未与 trustgraph 集成 |

> **本派没有 Commit Boundary 的 E-xx**：`01-L13/L14` 只在派内使用。`conclusions` 的 E-05 是 FIRME；Commit Boundary digest 的 `claims: [E-05]` 与 §8 的 E-05 回链都是错挂，**2026-11-09 已回改**（`claims: []`，§8 改为“不挂 E-xx”）。
>
> **数字口径**：01-L11 用 OntoAct digest 的 78.6/83.3/90.0%（IfR 64.3/66.7/65.0%）、SI `1.6–2.4`；`conclusions` 的 E-16 已于 2026-11-09 按同口径回改。CASEL 主表是 `τ̂=∞`，不要把 7.02% 当阈值开启后的结果。

## 策略层来源（2026-11-10）

> 标准已入材料卡（`src/web/`），但仍是**摘要级**：条款/API 未逐字核的标 `待核`；OSS 未建卡。**没有 digest 不算论文入库**，标准按材料卡算。

| 来源 | 类型 | 支撑 | 状态 | 待核 |
|---|---|---|---|---|
| [GB/T 43697-2024 数据分类分级规则](../../src/web/gbt-43697/gbt-43697.card.md) | 标准（CN） | policy F3；04 C.2 level | 已入库（材料卡） | 条款号；一般数据是否再分级；级别→处置接口 |
| [GB/T 35273-2020 个人信息安全规范](../../src/web/gbt-35273/gbt-35273.card.md) | 标准（CN） | policy F3；PII 类别 | 已入库（材料卡） | 条款；个人敏感信息清单；是否给授权判定 |
| [W3C ODRL 2.2](../../src/web/w3c-odrl-2.2/w3c-odrl-2.2.card.md) | 标准（W3C） | policy F2；冲突/义务 | 已入库（材料卡） | §2.10 默认冲突策略；审计/decision log |
| [OASIS XACML 3.0](../../src/web/oasis-xacml-3.0/oasis-xacml-3.0.card.md) | 标准（OASIS） | policy F2；合并算法/obligation | 已入库（材料卡） | obligation 能否挂 Deny；版本匹配 |
| Apache Atlas | OSS（US） | policy F1；标签传播 | 待入库 | 分类版本；是否含 enforcement |
| Apache Ranger | OSS（US） | policy F1/F2；tag policy/audit | 待入库 | deny/priority 默认；审计字段 |
| OpenFGA | OSS（US） | policy F2；ReBAC/version | 待入库 | 默认拒绝；blocklist；obligation |

> 链接与摘要见 [policy/frontier](./policy/frontier.md)；入库后补 `card.md` / `digest.md`，再回写本表。
