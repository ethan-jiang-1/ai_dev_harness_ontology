---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-09
arxiv: 2610.21466
title: Ontology Refinement with Embeddings and LLMs - A Case Study on CASTON
authors: Hui Yang, Ziyu Li, Xuan Liu, Anders Jarfors, He Tan, Jiaoyan Chen
pdf: 2610.21466-caston-refinement.pdf
home: topics/05-produce
subtopic: refinement
also_supports: []
evidence_role: mechanism-only
execution_form: none
updates:
  - topics/05-produce/refinement/README.md
  - topics/05-produce/claims.md
  - topics/05-produce/sources.md
  - topics/conclusions.md
published: 2026-10
admission: admitted
gate_checked: 2026-11-11
impact_evidence: "I2: Manchester + Jonkoping + NUS; I5: code"
liveness: arXiv 2026-10
provenance_type: academic
---

# Ontology Refinement with Embeddings and LLMs - A Case Study on CASTON · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

用**微调的本体嵌入**先把「可疑的上位公理」缩到 30 条、每条给 10 个候选父类，再让 LLM 只在这些局部候选里做 yes/no/替换判断；CASTON 上 default（CASTON-fine-tuned OnT + Qwen3-8B）的 6 条高置信替换被两位专家全部接受。

## 问题与设定

- **问题**：本体里的 asserted subsumption（`A ⊑ B`）可能有隐蔽错误；让 LLM 看整个本体既不准也贵。
- **本体**：CASTON v1.0.0（2026-02-22）：270 named classes、306 axioms、292 条 atomic subsumption。
- **评估**：2 位领域专家独立打 5 分制（−2 完全错 … +2 完全对）；两人都正 → accepted；都负 → rejected；其余 mixed。
- **设置**：
- Default：CASTON-fine-tuned OnT + Qwen3-8B。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 机制/设定 | digest §1–3；原文见 `paper.md` |
| 关键数字 | §3 / §1 / Table 1 |
| 图表 | 见下表 / `figures/` |
| 判断/工程用法 | [digest.md](./digest.md) |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| `fig-1-workflow.png` | — | 见 digest 图注 | ✓ |

## 作者自述局限

- 单一本体（CASTON）、单一公理类型（subsumption）、少量修复（6 条高置信）。
- 初步结果（poster）；没有大规模/跨本体评估。
- Medium-confidence 全 mixed，说明 confidence 只能粗分。
- 没有下游任务收益；没有长期维护评估。
- 失败案例显示：本体层级本身不一致时，fine-tuned embedding 也会给错。

## 原文

- PDF：同目录 `2610.21466-caston-refinement.pdf`
- arXiv:2610.21466
