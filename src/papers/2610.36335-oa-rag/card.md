---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-09
arxiv: 2610.36335
title: OA-RAG: Ontology-based Agentic RAG for Faithful LLM Reasoning
authors: Hui Yang, Jiaoyan Chen, Yongsheng Gao
pdf: 2610.36335-oa-rag.pdf
direction: 1
home: topics/02-judgment
subtopic: evidence
also_supports: []
evidence_role: execution-test
execution_form: engine
updates:
  - topics/02-judgment/evidence/README.md
  - topics/02-judgment/claims.md
  - topics/02-judgment/sources.md
  - topics/conclusions.md
---

# OA-RAG: Ontology-based Agentic RAG for Faithful LLM Reasoning · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

把本体的**形式推理**（OWL/DL reasoner）与**非形式注释**（label/definition）接进同一个 ReAct agent：每个答案必须报告所用本体观察 + 一个 grounding level（entailed / supported / related / unrelated）；在三个大本体基准与六个医学 QA 任务上整体最优，且 grounding level 与正确率正相关。

## 问题与设定

- **问题**：RAG 常把检索到的文本当等价证据，忽略逻辑关系；LLM 的推理不受本体约束。能否让 agent 同时用本体的形式公理与文本注释，并报告「答案对本体的忠实度」？
- **三种推理模式**（Fig. 1）：formal reasoning（可由 reasoner 推出）、ontology-grounded LLM reasoning（形式+注释，需要 LLM 推理）、ontology-assisted LLM reasoning（答案不必忠实于本体，LLM 可自由推理）。
- **本体**：GO、FoodOn、SNOMED CT（三个大规模真实本体）。
- **数据**：每本体 300 MCQ + 200 OQ = 1,500 Test 1（formal）；1,477 Test 2（grounded）；Test 3 用 OntoTune 设置，6,781 题（MedQA、USMLE Step 1/2/3、MedMCQA、PubMedQA）。
- **backbone**：Llama-3-8B-Instruct、Qwen3.5-9B。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 机制/设定 | digest §1–3；原文见 `paper.md` |
| 关键数字 | §6.2 / §1 / §6.3.1 / Table 2 |
| 图表 | 见下表 / `figures/` |
| 判断/工程用法 | [digest.md](./digest.md) |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| `fig-2-framework.png` | — | 见 digest 图注 | ✓ |
| `fig-3-grounding-accuracy.png` | — | 见 digest 图注 | ✓ |

## 作者自述局限

- grounding level 是模型自评，不是形式保证；没有独立的校准/审计。
- Test 3 的强项依赖同 context 预算；i-MedRAG 在 262k 下仍有竞争力。
- Test 2 的 OQ 表现差；检索是主要瓶颈（gold evidence 完全检索 23.6%）。
- 本体覆盖有限；问题超出本体范围时，grounding level 会退化。
- 三个本体都是生物医学；跨域未测。

## 原文

- PDF：同目录 `2610.36335-oa-rag.pdf`
- arXiv:2610.36335
