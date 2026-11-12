---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-09
batch: 补给
published: 2026-07-30
venue: arXiv preprint
reliability: medium
impact: medium
region: Singapore (NTU / A*STAR)
arxiv: 2607.28082
title: GGC - Selective Query Correction for Reliable Text-to-SPARQL Generation
authors: Yang Ziyi, Thanh-Son Nguyen, Nguyen Tuan Anh, Lihui Chen
pdf: 2607.28082-ggc.pdf
home: topics/03-knowledge
subtopic: querying
also_supports: []
evidence_role: mechanism-only
execution_form: none
updates:
  - topics/03-knowledge/querying/README.md
  - topics/execution-forms.md
admission: admitted (probation)
gate_checked: 2026-11-11
impact_evidence: "I2: NTU + A*STAR"
liveness: arXiv v1 2026-07-30
provenance_type: academic
---

# GGC · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

LLM 生成的 SPARQL 大多「能跑但语义错」，所以关键不是改所有 query，而是**先判断该不该改**：一个监督训练的 Gate 在 `(问题, 初始 query)` 上判风险，只把约 9% 的高风险样本送进 Corrector；MCQA 上 query-level accuracy 90.23% → 98.33%，推理时间约为全量纠错的 55%。

**评级依据**：NTU / A*STAR 是强机构，原文表格与数字可核；但**无正式 venue、单 benchmark、无独立复现**，且三处内部数字不一致（digest 已标存疑）→ `reliability: medium`、`impact: medium`。它是 03/querying 的支撑源，不单独撑 E；E 的锚点是 SPARQL-LLM（challenge 冠军 + 生产）。

## 问题与设定

- **任务**：Text-to-SPARQL（NLQ → SPARQL → 在 RDF KG 上执行取答案）。
- **数据**：MCQA（Hoang et al. 2024），电影域，单 KG（iMKG，据称基于 Wikidata + MovieKG）；训练 119,409 / 验证 15,785 / 测试 31,570；每条含 NLQ、question type、topic entity、answer、gold SPARQL。补充实验 SciQA/ORKG（2,565 例，测试 513 → 剔除 43 条 gold 跑不通后 470）。
- **模型**：Generator 与 Corrector 均为 Llama-3.2-3B-Instruct（LoRA + 4-bit SFT）；Gate 默认 RoBERTa-base（vs SBERT all-MiniLM-L6-v2）。
- **基线**：Generator-only、Gen.+Corr.（全量纠错）、NSMh、QGG；无 LLM-based Text-to-SPARQL 主基线（作者称缺标准实现）。
- **主指标**：query-level accuracy = 生成 query 与 gold query 的**答案集匹配率**（不是执行成功率，也不是字符串匹配）。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 三段流水线 + 伪代码（含 Gate 输入/标签/阈值） | digest §3.1、§4.3–4.4；原文 Fig. 1（p.4）、Algorithm 1（p.5）、§3.4（p.4）、Table 4–5（p.8） |
| 主结果与口径 | digest §4.1；原文 Table 2（p.6） |
| 改对/改坏证据 | digest §4.5；原文 Table 12（p.17）、Table 9–11（p.14–16） |
| 训练成本 | digest §3.2；原文 Table 6（p.12） |
| 作者自述局限 | digest §7；原文 Limitations（p.9） |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| Fig. 1 | p.4 | GGC 框架图 | ✗（见 PDF） |
| Table 2 / 3 | p.6–7 | 主结果（query/item 指标 + 推理时间）；错误分布 650/2,397/38 | ✗（`paper.md` 有文本表） |
| Table 4–5a/b/c | p.8 | Gate 骨干对比；阈值 / KG 反馈 / Corrector 配比消融 | ✗ |
| Table 6 | p.12 | 各模块训练样本量与耗时 | ✗ |
| Table 7–8 | p.13 | Generator / Corrector 的 prompt 模板 | ✗ |
| Table 9–11 | p.14–16 | 案例：改对 / 改坏 / 修不动 | ✗ |
| Table 12–13 | p.17 | 子集级准确率；SciQA 结果（正文与表不一致） | ✗ |

## 作者自述局限

- 主实验只有 MCQA（电影域、label-based SPARQL）；跨域/跨 KG/跨 SPARQL 形式/跨骨干的评估有限，SciQA 只算 preliminary；ID-based SPARQL 需要实体链接与 schema 对齐。
- Gate 与 Corrector 依赖特定 Generator 的误差分布，换模型要重训/适配。
- 离线造训练数据要在大规模训练集上跑一遍 Generator，有额外算力成本。
- 伦理段：错 query 会给出误导性答案；真实部署需验证、不确定性提示与人工监督。

## 原文

- PDF：同目录 `2607.28082-ggc.pdf`；正文 [paper.md](./paper.md)、参考文献 [references.md](./references.md)、附录 [appendix.md](./appendix.md)
- arXiv：2607.28082v1（2026-07-30，cs.CL）；代码/数据：未报告
