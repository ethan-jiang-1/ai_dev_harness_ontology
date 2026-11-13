---
status: draft
source_type: standard
standing: normative
admission: admitted
gate: standard-in-force
gate_checked: 2026-11-11
impact_evidence: I1 标准组织（ISO/IEC JTC 1/SC 32）；I2 多主体（国家成员体投票，BFO 由多机构维护）；I3 采用（BFO 官网自述 550+ 项目使用，待核）
liveness: 2026-06 后：-3:2023 / -4:2023 现行；BFO 持续发布（具体版本待核）
reading: 摘要级
provenance_type: standard-body
provenance: 原文摘要
updated: 2026-11-11
batch: 2026-11-11 基线批
source: https://www.iso.org/standard/74572.html
author: ISO/IEC JTC 1/SC 32
published: 2021-11（-1/-2）；2023（-3/-4）
updates: []
---

# ISO/IEC 21838 系列：顶层本体（TLO）

> 标准卡。读的是 ISO 目录摘要、BFO 官网、中国标准服务网的条目；**未读标准正文**，条款号一律 `待核`。
> 用途只有一个：给「本体 / 顶层本体」这两个词一个 `normative` 锚，并划清它与领域本体的边界。

## 它定义什么

1. **-1:2021 Requirements**：规定顶层本体应具备什么——范围、规范性引用、术语与定义、公理、文档，以及一致性（conformance）要求。标题即 "Part 1: Requirements"。
2. **-2:2021 BFO**：把 **Basic Formal Ontology** 作为参考顶层本体写进国际标准。
3. **-3:2023 DOLCE** / **-4:2023 TUpper**：另外两个被标准化的顶层本体，作为 BFO 之外的选项。

| 部分 | 年份 | 内容 |
|---|---|---|
| 21838-1 | 2021 | 顶层本体的要求与合格性 |
| 21838-2 | 2021 | BFO（参考 TLO） |
| 21838-3 | 2023 | DOLCE |
| 21838-4 | 2023 | TUpper |

## 它不定义什么

- **不定义领域本体**：不管企业本体、工业本体、金融本体怎么建；这些在别的标准/联盟里。
- **不给成熟度分级**：没有 L1–L5，也没有评分表。
- **不规定实现技术**：OWL 是常见载体，但标准管的是本体内容与合格性，不是序列化格式。
- **不保证互操作**：两个都「符合 21838」的 TLO 不等于能自动对齐；它只定合格性。

## 对我们的用法

- **「本体」的硬锚**：顶层本体（TLO）是「小、通用、不含领域词」的上层；我们的「本体塔」是 **domain tower**，不是 TLO。这个区分要写进 GLOSSARY。
- **判「broader」**：如果我们的「本体」定义把实例、图谱、词表都塞进去，那是 `broader`——按 ADR 0011 拆开，标准义归 N，扩展标 `local`。
- **不能撑效应量**：它能说「什么叫合格 TLO」，不能说「用了本体 agent 就更好」。

## 证据强度

- **一手还是转述**：ISO 目录摘要 + BFO 官网 + 标准服务商条目；正文未读，条款号 `待核`。
- **等级**：
  - 标准存在、版本、分部分——`已核`（ISO / cssn 条目）。
  - 「BFO 被 550+ 项目使用」——BFO 官网自述，`待核`（未见独立统计）。
  - 「-1 规定一致性要求」——目录摘要级，`待核` 具体条款。

## 与已有判断的关系

| 结论编号 | 关系 | 说明 |
|---|---|---|
| —（06 暂无对应 L） | 新锚 | 给 GLOSSARY 的「本体」「顶层本体」提供 `normative` 锚；不改变现有 E |

## 待核项

- [ ] -1 的合格性条款号与具体判据
- [ ] -2 是否规定 BFO 的 OWL 实现与版本
- [ ] BFO「550+」的独立来源
- [ ] -4 TUpper 的维护机构

## 喂到哪个主题

- `GLOSSARY`：本体 / 顶层本体 的 `origin: standard` 锚
- `meta/status/term-baseline.md`：差异表 v0（本体、顶层本体、领域本体）
- `topics/05-produce`：本体构建的边界（TLO vs 领域塔）

## 原文摘录

> BFO is a small, upper level ontology that is designed for use in supporting information retrieval, analysis and integration in scientific and other domains. … it does not contain physical, chemical, biological or other terms which would properly fall within the coverage domains of the special sciences.

> BFO is used by more than 550 ontology-driven endeavors throughout the world.（BFO 官网自述）
