---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-08
arxiv: 2611.01276
title: OntoDoc: Automatically Generating Ontology Resource Descriptions
authors: Juan Guajardo Gutierrez, Mike Tran, Nasim Shirvani Mahdavi, Chengkai Li
pdf: 2611.01276-ontodoc.pdf
direction: 2
home: topics/05-produce
subtopic: generation
updates:
  - topics/05-produce/generation/README.md
  - topics/05-produce/claims.md
  - topics/05-produce/sources.md
  - topics/conclusions.md
---

# OntoDoc: Automatically Generating Ontology Resource Descriptions · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

给任意 IRI 自动写 `rdfs:comment` 式的自然语言说明：四阶段 pipeline（自适应 SPARQL 探索 → 网页背景检索 → **显式假设生成** → 描述生成）；在 151 个术语、3 个知识图上，完整性从 3.43 提到 3.84（5 分制），明显优于模板 verbalizer，但**没有测下游任务是否变好**。

## 问题与设定

- **问题**：大量本体术语没有 `rdfs:comment`，人工写不可扩展；模板/规则 verbalizer 只能覆盖显式公理，读不出实例数据里的语义。
- **数据**：151 IRIs：
- BioBricks-MeSH：51 IRIs，17 classes / 21 object properties / 28 datatype properties。
- SOCKG：70 IRIs，92 classes / 62 object properties / 10 datatype properties。
- DBpedia：30 IRIs，790 classes / 1,167 object properties / 1,857 datatype properties。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 机制/设定 | digest §1–3；原文见 `paper.md` |
| 关键数字 | §5.3 / Table 5 / Table 6 / Table 4 / Table 3 / Table 7 |
| 图表 | 见下表 / `figures/` |
| 判断/工程用法 | [digest.md](./digest.md) |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| `fig-1-pipeline.png` | — | 见 digest 图注 | ✓ |

## 作者自述局限

- 假设阶段是**语义瓶颈**：漏掉的关键细节后面拿不回来；可能降低 completeness。
- 没有测下游任务（用户是否更容易理解/使用）；只测描述质量。
- 151 个术语、3 个本体；跨更多本体/语言未测。
- LLM judge 可能偏好冗长；人工评估只评 OntoDoc 输出，没做 baseline 盲评。
- 描述质量 ≠ 本体质量；生成说明不能替代本体修正。

## 原文

- PDF：同目录 `2611.01276-ontodoc.pdf`
- arXiv:2611.01276
