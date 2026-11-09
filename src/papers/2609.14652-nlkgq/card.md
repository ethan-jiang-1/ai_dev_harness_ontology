---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-09
batch: 补给
published: 2026-09-13
region: Germany (Max Planck Institute for Biological Cybernetics)
venue: arXiv preprint
reliability: medium
impact: medium
arxiv: 2609.14652
title: Natural Language Knowledge Graph Query Execution: Leveraging Controlled Semantics in the LLM Context Window
authors: Blake G. Fitch
pdf: 2609.14652-nlkgq.pdf
direction: 3
home: topics/03-knowledge
subtopic: querying
also_supports: []
evidence_role: mechanism-only
execution_form: context
updates: []
---

# NLKGQ · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

把**完整领域 OWL ontology**（Turtle）与 SPARQL 系统提示、简短 domain rider、用户问题一起放进**单次** LLM 调用，零样本生成 SPARQL；DBLP 原生词汇不透明时用 **dblpx wrapper ontology + 确定性 runtime rewriter** 还原。作者报 DBLP-QuAD 3.1 **89.9% Match / 81.3% Exact**（1,000 题）、2.0 确定性协议 **57.6% / 20.1%**、SemOpenAlex **98/100**、neuroimaging **21/21**。评级依据：Max Planck（德国）单作者 preprint，无同行评审、无采用；但有可运行系统、公开 benchmark、10 模型扫描与逐题审计 → `reliability: medium`、`impact: medium`，不升 high。

## 问题与设定

- **任务**：Text-to-SPARQL；自然语言问题 → SPARQL → 在 RDF KG 上执行。
- **数据**：DBLP-QuAD 2.0（5,000 对，1,000 题测试；DBLP + OpenCitations；28 条 federated）；作者修订的 QuAD 3.1（同 1,000 题，确定性参考）；SemOpenAlex（100 题）；neuroimaging（21 题，前作）。
- **模型**：主 Qwen3.6-27B；10 模型扫描（Gemma-4-31B、Qwen3.6-27B/FP8、Qwen3-Coder-30B、Mistral-Small-24B、Llama3.3-70B、Qwen3-8B、Qwen3.6-35B/FP8、Qwen3-14B）；本地 AMD APU，开源权重。
- **设定/指标**：单次调用、t=0.0、无微调、无 few-shot、无 entity linking；QLever；单一固定 snapshot。Match（二元，生成结果包含参考结果，允许 superset）、Exact（二元严格）、QuAD F1（扁平 set-of-values）、SPINACH F1（行对齐）。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 单次调用的 prompt 组织 + wrapper/rewriter + worked example | digest §3.1–3.3；原文 p.1–3 |
| OWL 五类 token / controlled semantics | digest §3.2；原文 p.3 |
| 主结果（2.0→3.1 progression） | digest §4.1；Table 2, p.6 |
| 跨域 + 模型扫描 | digest §4.2–4.3；Table 3–4, p.6 |
| 错误分析 / 敏感性 / 作者局限 | digest §4.4–4.5、§7；原文 p.6–7 |

## 图表索引（全文无图）

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| Table 1 | p.5 | 四个指标的定义 | ✗（`paper.md` 有文本表） |
| Table 2 | p.6 | QuAD 2.0→3.1 progression（Match/Exact/两个 F1） | ✗ |
| Table 3 | p.6 | 三域结果 + baseline | ✗ |
| Table 4 | p.6 | 10 模型扫描 | ✗ |

## 作者自述局限

- wrapper-vs-native 消融只跑 Qwen3.6-27B；10 模型扫描只覆盖 wrapper 配置；wrapper 设计手工；未测 proprietary 模型；entity resolution 不在范围（266 题带 bracketed URI）。
- 每次调用都带完整 ontology；词汇超出上下文窗口时需要选择/缩减，本文未处理。
- Match 允许 superset；Exact（81.3%）才是严格数。
- QuAD 3.1 的修复与所评系统同一作者；只能用逐题日志与修复前 margin 作检查；继承数据限制：仅 71% DBLP 出版物有 OpenCitations 标识，DBLP 的 BibTeX 继承分类可能不再最合适。

## 原文

- PDF：同目录 `2609.14652-nlkgq.pdf`；正文 [paper.md](./paper.md)、参考文献 [references.md](./references.md)、附录 [appendix.md](./appendix.md)
- arXiv：2609.14652v1（2026-09-13，cs.DB）；代码/数据：论文未给链接，QuAD 3.1 称将发布
