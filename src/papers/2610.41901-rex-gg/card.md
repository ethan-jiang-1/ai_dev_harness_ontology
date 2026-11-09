---
status: draft
source_type: preprint
reading: 摘要级
provenance: 原文摘要
updated: 2026-11-09
arxiv: 2610.41901
title: ReX-GG: a LLM Ensemble Pipeline for Relation-extraction and Graph Generation
authors: Giacomo Magnifico, Eduard Barbu（塔尔图大学）
pdf: 2610.41901-rex-gg.pdf
direction: 2
home: topics/05-produce
subtopic: generation
also_supports: []
evidence_role: harness-evidence
execution_form: label
updates: []
---

# ReX-GG

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 做了什么

轻量关系抽取流水线：**七个独立模型集成** + JSON 结构化输出 + **匿名互评排序**。

关系类型由本体定义四种：强因果、弱因果、对比、组合。输出可交互的因果图。

工程取向很明确：不堆模块、加重流程，而是用结构化输出约束格式、用互评压掉幻觉**和**单模型失效点。

## 结果

- 英语科普文章上，平均信息准确率 **0.778**（匿名标注者聚合评分），接近人工金标。
- 作者称模块化程度足以让非专业用户部署；输出为交互式 HTML。

## 没测什么

**作者自述**：只用短文档测过；长文档（整篇论文）超出范围；全在线 API，无法分析推理过程。

**读者补充**：0.778 是「所给信息的准确率」，未报告召回——漏抽多少不知道。

## 对本仓库的意义

| 关联 | 关系 |
|---|---|
| 05 生产派 | 「先固定本体再抽关系」的务实形态：关系类型必须由本体给定，自由抽取才会漂 |
| 00-harness/orchestration | 匿名互评 = 用独立性替代更强模型 |
| [orchestration](../../../topics/00-harness/orchestration.md) | 多体协作的一个低成本实现 |

## 待核

- [ ] 匿名互评的具体排序规则与稳定性
- [ ] 召回率

## 原文

- PDF：同目录 `2610.41901-rex-gg.pdf`
- arXiv:2610.41901
