---
status: draft
updated: 2026-11-09
---

# 03 知识派 · 证据源

> **三层读法**：N（规范性）见 [规范主干](../trunk.md)；本表是 I（资料性）/ S（线索）。定义性表述只引 N；效应只引 I；S 只进 `frontier.md`。


| 来源（digest） | 类型 | 阅读 | 支撑 | 备注 |
|---|---|---|---|---|
| [Narrow & Deep digest](../../src/papers/2610.11768-narrow-and-deep/digest.md) | preprint | 精读 | 03-L1 / 03-L7 / 03-L8 | [card](../../src/papers/2610.11768-narrow-and-deep/card.md)（provenance）；投影 pooled 分最高但非普适排序；9B 带投影 > 750B 不带（区间约 0.3 宽）；日志检索 4/80、H3 未支持 |
| [Context as Infrastructure digest](../../src/papers/2610.41172-context-as-infrastructure/digest.md) | preprint | 精读 | 03-L2 / 03-L5 / 03-L6 / 03-L10 | [card](../../src/papers/2610.41172-context-as-infrastructure/card.md)（provenance）；claim–leaf 省 token 条件性；PageIndex 在 FRAMES 规模为负；成本模型与 miss 敏感度 |
| [Grid Agents digest](../../meta/audits/2026-11-11-source-purge.md#src-2611-03534) | preprint | 精读 | 03-L9 / 03-L11 | [card](../../meta/audits/2026-11-11-source-purge.md#src-2611-03534)（provenance）；法规证据 + solver + 人；对最强 baseline 仅 +0.5pp；citation/strict-pass/签核契约 |
| [ontop digest](../../src/open-source/ontop-ontop/digest.md) | open-source | 已读代码 | 03 frontier（供给型；无 L/F） | [card](../../src/open-source/ontop-ontop/card.md)（provenance）；本体+映射查询时编译成 SQL；最小示例跑通；不改 claims |
| [GGC digest](../../src/papers/2607.28082-ggc/digest.md) | preprint | 精读 | 03-L13 | [card](../../src/papers/2607.28082-ggc/card.md)（provenance）；答案集匹配 90.23→98.33；全量纠错 92.34；45% 相对全量纠错的墙钟；单 KG/单骨干 |
| [NLKGQ digest](../../meta/audits/2026-11-11-source-purge.md#src-2609-14652) | preprint | 精读 | 03-L14 | [card](../../meta/audits/2026-11-11-source-purge.md#src-2609-14652)（provenance）；完整 OWL 进上下文；3.1 上 89.9 Match/81.3 Exact；单 snapshot；Match 允许 superset |
| [KGVoyager digest](../../meta/audits/2026-11-11-source-purge.md#src-2609-01780) | preprint | 精读 | 03-L15 | [card](../../meta/audits/2026-11-11-source-purge.md#src-2609-01780)（provenance）；4 小 benchmark F1 +3.7pp（不是 4×）；成本 −38.3%；class index ~68% endpoint；rdf:type 限制 |
| [Qlever digest](../../src/open-source/ad-freiburg-qlever/digest.md) | open-source | 已读代码 | 03 frontier（执行层 adjunct） | [card](../../src/open-source/ad-freiburg-qlever/card.md)（provenance）；SPARQL 1.1 引擎；不做 OWL/SHACL；NLKGQ/QRAKEN 使用；未在本仓跑 |
