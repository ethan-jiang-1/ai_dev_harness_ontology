---
status: draft
source_type: preprint
reading: 摘要级
provenance: 原文摘要
updated: 2026-11-08
arxiv: 2610.41785
title: Peeling the Matryoshka: Extracting Ontological Structure from Retrieval Embeddings
authors: Eunchan Kim（汉阳大学）
pdf: 2610.41785-peeling-matryoshka.pdf
direction: 2
home: topics/05-produce
subtopic: generation
updates: []
---

# Peeling the Matryoshka

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 做了什么

一个经验发现 + 一个探针：

- **发现**：在 MRL（Matryoshka Representation Learning）嵌入里，**前缀长度**与金标分类法的**粗→细粒度**对齐。用打乱维度、逆序维度做对照，把对齐定位到「学出来的前缀维度」上；三个架构不同的 MRL 模型都成立。
- **探针**：PEEL，98K 参数，在冻结嵌入上用 order-embedding 目标训练一次，解码出分类 DAG。

## 结果

- Graph F1：Wikipedia 0.885，arXiv 0.931。
- 从 wiki-ol 零样本迁移到 arXiv-ol 有效。
- 迁移只验证到「目标本体不比源域更深」。

## 没测什么

**作者自述**：只两个域；标签生成质量与下游效用（检索、问答）**不在本文范围**。

**读者补充**：这只在 MRL 系列嵌入上成立——不是通用方法，是对一种训练技巧的利用。

## 对本仓库的意义

| 关联 | 关系 |
|---|---|
| 05 生产派 | 「表征挖掘」这一来源：不建本体，从模型里挖 |
| 06 测量派 | 提醒：结构保真度 ≠ 有用；它自己承认没测下游 |

**一句话**：检索训练顺带产生了可解码的层级结构。这既不等于模型「懂」本体，也不等于这个结构能用于判定。

## 待核

- [ ] 非 MRL 嵌入是否有类似信号
- [ ] 抽出的层级与人工本体在**约束**上的差距

## 原文

- PDF：同目录 `2610.41785-peeling-matryoshka.pdf`
- arXiv:2610.41785
