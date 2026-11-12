---
updated: 2026-11-10
---

# src/web：博客 / 网页 / 工程材料 / 非 arXiv 论文

这里放 `source_type` 为 `blog` / `engineering` / `standard` / `talk` / `survey` / `paper` 的原样材料；arXiv 论文 PDF 在 [papers](../papers/)。

## 素材准入（2026-11-11 起，CHARTER §4）

- **G1**：发布 ≥ **2026-06-01**；旧材料立即移出，不留“历史语料”。
- **G3**：卡上 `impact_evidence` 至少列 2 个独立信号（I1–I5），至少 1 个 I1–I3；浏览/points/会议主 track 不单独算。
- **G4**：组织/社区/标准优先；公司博客、CEO 演讲、产品页只作 `signal`，不进 `src/`；有独立采用/社区印证的按 §4.4 窄例。
- **G5**：URL + 日期 + 作者/机构 + 快照；缺一不建卡。
- 卡必填 `admission` / `gate_checked` / `impact_evidence` / `liveness` / `provenance_type`；没有 `impact_evidence` 的按 `signal` 处理。
- **标准/规范**：走 §4.4.1 在役例外——仍是现行版本 + 2026-06 后维护/≥2 活跃实现；休眠/被取代的按 `excluded`。全文有版权时只存自包含卡 + `source:` URL，条款号未核标 `待核`。

> 旧“2026 影响力门槛”“标准不套影响力线”两节由本节替代。判定示例见 [来源清除审计](../../meta/audits/2026-11-11-source-purge.md) 与 [材料审计](../../meta/audits/2026-11-11-material-gate.md)。

## 规则

1. **原样存档。** 不摘编、不改写；网页转 markdown 时保留标题、作者、日期与链接。
2. **同名配对。** 原文 `{来源}/{slug}.md`，卡是同目录的 `{来源}/{slug}.card.md`。
3. **登记。** 卡与原文同目录；在 [src/README](../README.md) 的台账加一行。
4. **一手/二手。** 博客可能是作者的一手观察，也可能是转述；卡片写清 `source_type` 与 `provenance`。
5. **证据天花板。** 见 [source-types](../../meta/rules/source-types.md)：博客的 `已核` 只指「作者报告了 X」，一般规律默认 `推测`。
6. **非 arXiv 论文/数据集。** 会议论文、Zenodo/DLR 报告、数据集放这里，`source_type: paper`；原文 `{slug}.md` + 自包含 `{slug}.card.md`，**不另建 digest**。卡要能独立回答「它主张什么 / 证据强度 / 与已有判断的关系」。
