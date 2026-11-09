---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-09
arxiv: 2610.36325
title: Ontology-guided multi-agent reasoning for explainable differential diagnosis
authors: Roxana Ramona Szomiu, George Ursu, Adrian Groza（UTCN）
pdf: 2610.36325-ontology-multiagent-diagnosis.pdf
direction: 1
home: topics/01-constraint
subtopic: reasoning-gate
also_supports: []
evidence_role: execution-test
execution_form: compiled
updates:
  - topics/01-constraint/reasoning-gate/README.md
  - topics/01-constraint/claims.md
  - topics/01-constraint/sources.md
  - topics/conclusions.md
---

# Ontology-guided multi-agent reasoning for explainable differential diagnosis · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

把鉴别诊断做成**确定性评分 + 多 agent 分工**：LLM 只做症状抽取/提问/解释，所有排序与评分由代码在 curated 医学本体（SYMP/DOID/HPO）上算；用 Yes/No 追问补缺失症状；交互 refinement 在聚合上只提升 2.5 pp，但在可解决的歧义 case 上可以把 Top-1 从 0.340 拉到 1.0。

## 问题与设定

- **问题**：单轮 QA 假设诊断所需信息已齐；真实鉴别诊断是迭代追问。LLM 直接推理不可审计、易幻觉。
- **基准**：Q4DX `PatientCases.csv`，99 cases / 29 diagnoses；80% 与 50% symptom completeness；100% 排除（没有可追问的症状）；N=198。
- **患者**：确定性 simulated patient agent，可访问完整 profile；这是**乐观估计**，不是真人。
- **评分**：SapBERT cosine ≥0.6 对 reference label；Top-1/Top-3。
- **本体**：SYMP + DOID + HPO（HPO 作 synonym bridge）；GraphDB/SPARQL；不靠 LLM 生成症状-疾病关系。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 机制/设定 | digest §1–3；原文见 `paper.md` |
| 关键数字 | 见 digest §4 |
| 图表 | 见下表 / `figures/` |
| 判断/工程用法 | [digest.md](./digest.md) |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| `fig-1-architecture.png` | — | 见 digest 图注 | ✓ |
| `fig-3-accuracy.png` | — | 见 digest 图注 | ✓ |

## 作者自述局限

- 本体覆盖/准确性决定上限；missing/outdated 关系无法进推理。
- 本体术语 vs 数据集术语不匹配；91.3% 映射，仍有 8.7% 丢失。
- 有些 benchmark label 是症状不是疾病（Jaundice、Vertigo），系统按 ontology 无法输出为诊断，准确率恒为 0。
- KG 稀疏/诊断粒度不足（需要 lab results）。
- Yes/No/unsure 限制表达；不能捕捉 severity/temporal。
- 错误主要来自结构约束，不是语言理解；换更强 LLM 不会解决。

## 原文

- PDF：同目录 `2610.36325-ontology-multiagent-diagnosis.pdf`
- arXiv:2610.36325
