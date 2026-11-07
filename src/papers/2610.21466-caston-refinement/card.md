---
status: draft
source_type: preprint
reading: 摘要级
provenance: 原文摘要
updated: 2026-11-07
arxiv: 2610.21466
title: Ontology Refinement with Embeddings and LLMs: A Case Study on CASTON
authors: Hui Yang, Ziyu Li, Xuan Liu, Anders Jarfors, He Tan, Jiaoyan Chen
pdf: 2610.21466-caston-refinement.pdf
direction: 2
home: topics/05-produce
subtopic: refinement
updates: []
---

# CASTON 精化

## 做了什么

处理**已有本体**里的隐蔽上义错误。流程轻量：

1. 微调的本体嵌入模型挑出少量候选公理 + 可能的替换候选。
2. LLM 给出修复建议。
3. 专家判定。

案例：`chromite_sand` 原本挂在 `green_sand_molding`（一个**工艺**）下，建议改为 `foundry_sand`（一个**材料**）。

## 结果

- 识别出一小组高置信修复，两位领域专家判定**全部完全正确**。
- 规模小：单一本体、替换型建议、少量修复。

## 没测什么

**作者自述**：只一个本体；只做替换；专家评估的修复数很少；未扩展到关系限制等更复杂公理。

**读者补充**：未测「改完之后下游是否变好」——精化的最终判据应是下游，而不是专家点头。

## 对本仓库的意义

| 关联 | 关系 |
|---|---|
| 05 生产派 | 精化路线的代表：**修比建更常见** |
| [lifecycle](../../../topics/05-produce/lifecycle/README.md) | 阶段 2「精化」的一手例子 |

**最值得记的**：这个错误类型（把工艺当材料）是结构性的、形式检查发现不了的——正好说明为什么需要本体嵌入这类「语义邻近」信号来触发候选。

## 待核

- [ ] 候选公理的选取阈值
- [ ] 微调嵌入模型的数据来源
