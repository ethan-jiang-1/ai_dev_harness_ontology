---
status: draft
updated: 2026-11-09
---

# 05 生产派 · 证据源

| 来源（digest） | 类型 | 阅读 | 支撑 | 备注 |
|---|---|---|---|---|
| [CASTON digest](../../src/papers/2610.21466-caston-refinement/digest.md) | preprint | 精读 | 05-L2 / 05-L5 / 05-L9 | [card](../../src/papers/2610.21466-caston-refinement/card.md)（provenance）；精化；high 6/6、pretrained 4/7、GPT-4o mini 5/16；medium 0/2、1/4、1/5 |
| [SFE-O digest](../../src/papers/2610.37123-sfe-o/digest.md) | preprint | 摘要级 | 05-L4 | [card](../../src/papers/2610.37123-sfe-o/card.md)（provenance）；表示≠执行；三处数据矛盾（第三处 `possible`） |
| [OntoDoc digest](../../src/papers/2611.01276-ontodoc/digest.md) | preprint | 精读 | 05-L6 / 05-L7 | [card](../../src/papers/2611.01276-ontodoc/card.md)（provenance）；假设层；completeness 3.43→3.84；无下游 |
| [Peeling digest](../../src/papers/2610.41785-peeling-matryoshka/digest.md) | preprint | 摘要级 | 05-L3 | [card](../../src/papers/2610.41785-peeling-matryoshka/card.md)（provenance）；表征挖掘；只在 MRL 嵌入、未测下游 |
| [Evontree digest](../../src/papers/2510.26683-evontree/digest.md) | preprint | 摘要级 | 05-L3 | [card](../../src/papers/2510.26683-evontree/card.md)（provenance）；规则引导自演化；gap 1,396；增益仅报告值（`存疑`） |
| [ReX-GG digest](../../src/papers/2610.41901-rex-gg/digest.md) | preprint | 摘要级 | 05-L3 | [card](../../src/papers/2610.41901-rex-gg/card.md)（provenance）；关系抽取；本体只当标签表（4 种关系） |
| [FIRME digest](../../src/papers/2610.40482-firme/digest.md) | preprint | 精读 | 05-L1 / lifecycle 工程发现 1–3 | [card](../../src/papers/2610.40482-firme/card.md)（provenance）；对齐/演化；观察级 source_indicator；`CMR=MMR×precision` |
| [OntoAct digest](../../src/papers/2610.21983-ontoact/digest.md) | preprint | 精读 | 05-L1 / lifecycle 工程发现 4 | [card](../../src/papers/2610.21983-ontoact/card.md)（provenance）；只借写入准入；推理期机制归 01 |
| [What Does an Ontology Catch digest](../../src/papers/2610.37809-what-does-an-ontology-catch/digest.md) | preprint | 精读 | 05-L1 / 05-L8 | [card](../../src/papers/2610.37809-what-does-an-ontology-catch/card.md)（provenance）；三源 catch/FA/precision；主归 02，与 05 共享 |
| [semantica digest](../../src/open-source/semantica-agi-semantica/digest.md) | open-source | 未读（已跑最小示例） | generation F7 | [card](../../src/open-source/semantica-agi-semantica/card.md)（provenance）；ontology → SHACL → pyshacl 跑通；派生 shapes 质量未测 |
| [open-ontologies digest](../../src/open-source/fabio-rovai-open-ontologies/digest.md) | open-source | 已读代码（未跑） | lifecycle 判断 4 | [card](../../src/open-source/fabio-rovai-open-ontologies/card.md)（provenance）；SHACL/闭包差分；C2 阻塞（网络）；不改 claims |

> 阅读列按各 `card.md` 的 `reading` 填：CASTON/OntoDoc/FIRME/OntoAct/Ontology Catch 为原文精读，SFE-O/Peeling/Evontree/ReX-GG 为摘要级（`provenance: 原文摘要`）；digest 的 E3 吸收深度不改变这个口径。`05-L1` 是政策判断（来源字段要进判定），`05-L8` 记录「偏向标签」的缺口；FIRME/OntoAct 只支撑 lifecycle 的来源落账与准入，不把它们的推理期机制搬进本派。
