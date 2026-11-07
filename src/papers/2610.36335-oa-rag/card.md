---
status: draft
source_type: preprint
reading: 摘要级
provenance: 原文摘要
updated: 2026-11-07
arxiv: 2610.36335
title: OA-RAG: Ontology-based Agentic RAG for Faithful LLM Reasoning
authors: Hui Yang, Jiaoyan Chen, Yongsheng Gao
pdf: 2610.36335-oa-rag.pdf
direction: 1
home: topics/02-judgment
subtopic: evidence
updates: []
---

# OA-RAG

## 做了什么

把本体的**形式推理**与 LLM 的**非形式推理**结合：既用逻辑结构，也用域本体的自然语言标注。

关键设计不在检索，而在**输出契约**：每个答案必须报告所用作证据的本体观察，并给出一个 grounding 等级——`entailed` / `supported` / `related` / `unrelated`。

## 结果

- 在三个大规模本体派生的基准、六个真实医学问答任务上，整体优于**本体微调方法**与主流 RAG；推理密集型任务上优势明显。
- grounding 等级与正确率正相关（综述转述；摘要中该句被截断，待核）。

## 没测什么

**作者自述**：未在摘要中列出。
**读者补充**：等级由系统判定还是模型自评，摘要未说明——这决定了该机制是否可被信任（见下）。

## 对本仓库的意义

| 关联 | 关系 |
|---|---|
| P1 | 支持「证据结构化」比「知识注入」更有效 |
| P2 | 支持：等级是 harness 侧的契约，不是提示词技巧 |
| E-03 | 本卡是其一手依据 |
| [evidence-and-provenance](../../../topics/02-judgment/evidence/README.md) | 核心文献 |

**可借鉴的是「证据强度显式化」，不是再做一个 RAG 变体。** 这个区分对本仓库很关键：前者是可迁移的 harness 机制，后者是又一个检索管线。

## 待核

- [ ] grounding 等级的判定主体（模型自评 / 外部判定器 / 本体推导）
- [ ] 等级与正确率相关性的具体数值
- [ ] 等级分布是否出现「通胀」（大量 supported）
