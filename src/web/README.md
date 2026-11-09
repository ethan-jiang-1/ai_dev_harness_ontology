---
updated: 2026-11-09
---

# src/web：博客 / 网页 / 工程材料 / 非 arXiv 论文

这里放 `source_type` 为 `blog` / `engineering` / `standard` / `talk` / `survey` / `paper` 的原样材料；arXiv 论文 PDF 在 [papers](../papers/)。

## 2026 影响力门槛（2026-11-09 起）

- 只收 **2026 年**（优先 2026-07 以后）的讨论；作者/机构/平台要有可核的影响力证据：HN points/comments、Reddit upvotes、业内引用、标准/厂商采用、作者 reputation。
- 论坛帖也收，但卡里写清：谁说的、在哪、多少讨论/阅读、哪些是作者经验、哪些是转述。
- **博客/论坛不是 E**：`已核` 只到“作者报告了 X”；一般性结论默认 `推测`；只有改变判断时才进 topics。
- 卡加 `influence` 字段，写证据（“HN 612 points / 340 comments”“Thoughtworks Radar Vol.34”），不写“很有影响力”。

## 规则

1. **原样存档。** 不摘编、不改写；网页转 markdown 时保留标题、作者、日期与链接。
2. **同名配对。** 原文 `{来源}/{slug}.md`，卡是同目录的 `{来源}/{slug}.card.md`。
3. **登记。** 卡与原文同目录；在 [src/README](../README.md) 的台账加一行。
4. **一手/二手。** 博客可能是作者的一手观察，也可能是转述；卡片写清 `source_type` 与 `provenance`。
5. **证据天花板。** 见 [source-types](../../meta/source-types.md)：博客的 `已核` 只指「作者报告了 X」，一般规律默认 `推测`。
6. **非 arXiv 论文/数据集。** 会议论文、Zenodo/DLR 报告、数据集放这里，`source_type: paper`；原文 `{slug}.md` + 自包含 `{slug}.card.md`，**不另建 digest**。卡要能独立回答「它主张什么 / 证据强度 / 与已有判断的关系」。
