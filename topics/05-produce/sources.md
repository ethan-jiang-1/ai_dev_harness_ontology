---
status: draft
updated: 2026-11-09
---

# 05 生产派 · 证据源

| 来源（digest） | 类型 | 阅读 | 支撑 | 备注 |
|---|---|---|---|---|
| [CASTON digest](../../src/papers/2610.21466-caston-refinement/digest.md) | preprint | 精读 | 05-L2 / 05-L5 / 05-L9 | [card](../../src/papers/2610.21466-caston-refinement/card.md)（provenance）；精化；high 6/6、pretrained 4/7、GPT-4o mini 5/16；medium 0/2、1/4、1/5 |
| [SFE-O digest](../../meta/audits/2026-11-11-source-purge.md#src-2610-37123) | preprint | 摘要级 | 05-L4 | [card](../../meta/audits/2026-11-11-source-purge.md#src-2610-37123)（provenance）；表示≠执行；三处数据矛盾（第三处 `possible`） |
| [OntoDoc digest](../../meta/audits/2026-11-11-source-purge.md#src-2611-01276) | preprint | 精读 | 05-L6 / 05-L7 | [card](../../meta/audits/2026-11-11-source-purge.md#src-2611-01276)（provenance）；假设层；completeness 3.43→3.84；无下游 |
| [Peeling digest](../../meta/audits/2026-11-11-source-purge.md#src-2610-41785) | preprint | 摘要级 | 05-L3 | [card](../../meta/audits/2026-11-11-source-purge.md#src-2610-41785)（provenance）；表征挖掘；只在 MRL 嵌入、未测下游 |
| [Evontree digest](../../meta/audits/2026-11-11-source-purge.md#src-2510-26683) | preprint | 摘要级 | 05-L3 | [card](../../meta/audits/2026-11-11-source-purge.md#src-2510-26683)（provenance）；规则引导自演化；gap 1,396；增益仅报告值（`存疑`） |
| [ReX-GG digest](../../meta/audits/2026-11-11-source-purge.md#src-2610-41901) | preprint | 摘要级 | 05-L3 | [card](../../meta/audits/2026-11-11-source-purge.md#src-2610-41901)（provenance）；关系抽取；本体只当标签表（4 种关系） |
| [FIRME digest](../../src/papers/2610.40482-firme/digest.md) | preprint | 精读 | 05-L1 / lifecycle 工程发现 1–3 | [card](../../src/papers/2610.40482-firme/card.md)（provenance）；对齐/演化；观察级 source_indicator；`CMR=MMR×precision` |
| [OntoAct digest](../../meta/audits/2026-11-11-source-purge.md#src-2610-21983) | preprint | 精读 | 05-L1 / lifecycle 工程发现 4 | [card](../../meta/audits/2026-11-11-source-purge.md#src-2610-21983)（provenance）；只借写入准入；推理期机制归 01 |
| [What Does an Ontology Catch digest](../../meta/audits/2026-11-11-source-purge.md#src-2610-37809) | preprint | 精读 | 05-L1 / 05-L8 | [card](../../meta/audits/2026-11-11-source-purge.md#src-2610-37809)（provenance）；三源 catch/FA/precision；主归 02，与 05 共享 |
| [semantica digest](../../src/open-source/semantica-agi-semantica/digest.md) | open-source | 未读（已跑最小示例） | generation F7 | [card](../../src/open-source/semantica-agi-semantica/card.md)（provenance）；ontology → SHACL → pyshacl 跑通；派生 shapes 质量未测 |
| [open-ontologies digest](../../src/open-source/fabio-rovai-open-ontologies/digest.md) | open-source | 已读代码（未跑） | lifecycle 判断 4 | [card](../../src/open-source/fabio-rovai-open-ontologies/card.md)（provenance）；SHACL/闭包差分；C2 阻塞（网络）；不改 claims |

> 阅读列按各 `card.md` 的 `reading` 填：CASTON/OntoDoc/FIRME/OntoAct/Ontology Catch 为原文精读，SFE-O/Peeling/Evontree/ReX-GG 为摘要级（`provenance: 原文摘要`）；digest 的 E3 吸收深度不改变这个口径。`05-L1` 是政策判断（来源字段要进判定），`05-L8` 记录「偏向标签」的缺口；FIRME/OntoAct 只支撑 lifecycle 的来源落账与准入，不把它们的推理期机制搬进本派。
