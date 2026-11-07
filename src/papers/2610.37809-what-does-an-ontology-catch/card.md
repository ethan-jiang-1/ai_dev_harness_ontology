---
status: draft
source_type: preprint
reading: 摘要级
provenance: 原文摘要
updated: 2026-11-07
arxiv: 2610.37809
title: What Does an Ontology Catch? Curated, LLM-Generated and Data-Derived Ontologies as Checkers of LLM Agents over Knowledge Graphs
authors: Michal Orzechowski, Rund Tawfiq, Tomasz Kosciolek
pdf: 2610.37809-what-does-an-ontology-catch.pdf
direction: 1
home: topics/02-judgment
subtopic: checker
updates: []
---

# What Does an Ontology Catch?

## 做了什么

把**判定器本身**当作研究对象。比较三种本体来源（专家 curated、LLM 现写、从数据挖出的 schema），并让它们分别以三种方式介入：仅作提示上下文、仅作判定器、两者兼用。统计每种组合**抓到了什么错**、**错误标记了什么对**。

覆盖公开 Web 图与一个近 10⁹ 三元组的私有图，跨开源与闭源 agent。

## 结果

- 在 UniProt 上，curated 本体**误报的正确答案更多**——比数据派生的本体、比从遮蔽标识符的摘要生成的 LLM 本体都多。
- 在真实 agent 答案上，curated 本体的标记**精确度仅略优于随机标记**。
- 按发布状态使用的 curated schema 可能**与它自己的数据矛盾**。
- 结构性检查存在系统性盲区（摘要提及，具体类型待正文）。

## 没测什么

**作者自述**：未在摘要中列出。
**读者补充**：主比较集中在 UniProt 单域；跨域外推需正文确认。

## 对本仓库的意义

| 关联 | 关系 |
|---|---|
| P3（判定是权衡） | **直接支持**：三种来源各有偏向，无单一向优 |
| P1（价值在约束） | 支持但需限定：判定器价值不来自「用了本体」，来自其错误结构 |
| E-02 | 本卡是其一手依据 |
| [ontology-as-checker](../../../topics/02-judgment/checker/README.md) | 核心文献 |

**最重要的启示**：误报的破坏力在于 agent 会去「修复」正确的东西。判定器的假阳性不是浪费，是把对的改成错的。

## 待核

- [ ] 结构性检查漏掉的具体错误类型
- [ ] 「略优于随机」的具体数值与置信区间
- [ ] 「两种兼用」是否优于单一用法
