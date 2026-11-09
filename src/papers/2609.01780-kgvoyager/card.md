---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-09
batch: 补给
published: 2026-09-01
venue: arXiv preprint (cs.IR)
reliability: medium
impact: medium
region: US (University of Texas at Arlington)
arxiv: 2609.01780
title: KGVoyager - Knowledge Graph Agnostic Question Answering via Agentic Navigation
authors: Essam Wisam, Chengkai Li
pdf: 2609.01780-kgvoyager.pdf
direction: 3
home: topics/03-knowledge
subtopic: querying
also_supports: []
evidence_role: mechanism-only
execution_form: none
updates:
  - topics/03-knowledge/querying/README.md
---

# KGVoyager · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

领域 KG 常没有 ontology、没有 text–SPARQL 例子，只剩一个 SPARQL endpoint；KGVoyager 用 think–act–observe 循环加 search/exploration/execution 三类通用工具，运行时把问题里的词映射到 IRI、探属性实际怎么连、用执行反馈改草稿——只预置一个 KB 级 class index。四个领域 benchmark、四个骨干、三次运行上平均 F1 64.6% vs GRASP 60.9%（**+3.7 个百分点**，不是 4 倍），成本 $2.43 vs $3.94（−38%），墙钟 85.6s vs 112.4s（−24%）（Table 3, p.7）。

**评级依据**：UT Arlington 单组 preprint、无同行评审；但评估面在同类里算宽（4 benchmark × 4 骨干 × 3 次运行、28 个 okn.us endpoint 的索引可行性扫描、三组件消融、156 例失败分析），主基线是 ISWC 2025 的 GRASP 且被给了最好条件（entity index）。数字可核、无独立复现、成本口径未报告 → `reliability: medium`；2026-09 新出、无采用证据 → `impact: medium`。它是 03/querying 的机制源，不单独撑 E。

## 问题与设定

- **任务**：NL→SPARQL（KGQA 的 query 生成侧），在**只有 endpoint** 的领域 KG 上答题，零样本、无微调。
- **数据**：4 个 benchmark 共 394 题——Climate Models KG（108，气候科学文献）、SOCKG（98，土壤碳建模）、DREAM-KG（88，地方政府服务）、DBLP-QuAD（100，test split 随机抽样，学术元数据）；前三者题–query 对由各 KG 作者提供。
- **模型与基线**：GPT-6 Sol、GPT-OSS-120B（117B/5.1B active）、Nemotron 3 Ultra（550B/55B）、Muse Glimmer 30B（开源模型经 OpenRouter）；主基线 GRASP（被给了 entity index 的"最好情况"），另加仅 SOCKG 的 Grep Ontology 基线（整份 Turtle 本体交给 grep + SPARQL 执行）。
- **指标**：沿用 Spinach 的 row-major F1；另报成本（$）、每题迭代数、墙钟、每题工具调用/SPARQL 执行次数。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 三类工具与 think–act–observe | digest §3.1–3.4；原文 §3、Fig. 1（p.4）、Fig. 2（p.5）、Fig. 9–12（p.14–16） |
| class index 怎么来/多大；28 endpoint 可行性 | digest §3.5、§4.3；原文 §3.1（p.3–4）、Table 1（p.2）、Table 2（p.6） |
| 主结果与口径 | digest §4.1–4.2；原文 Table 3（p.7）、Fig. 3（p.7） |
| 消融 / 成本 / 失败模式 | digest §4.5–4.8；原文 Table 4（p.8）、Fig. 8（p.13）、Table 6/10（p.13–14） |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| Fig. 1 / 2 | p.4–5 | 工具总览；DBLP 十步端到端例子（答案 count=1） | ✗（`paper.md` 有文本版） |
| Table 1–2 | p.2, 6 | 索引条数/体积；28 个 okn.us endpoint 的 entity/class 成功率 | ✗（有文本表） |
| Table 3 / Fig. 3–4 | p.7–8 | 主结果（F1/cost/iter/time）；逐模型结果；SOCKG grep 基线 | ✗（有文本表） |
| Table 4 | p.8 | 三组件消融（10 组，带 ±std） | ✗（有文本表） |
| Fig. 5–8 / Table 6–11 | p.12–14 | 复杂度分层、工具调用分布、156 例失败的两级分类 | ✗（Table 有文本版） |
| Fig. 9–12 | p.14–16 | 完整 system prompt 与五个工具的 schema | ✗ |

## 作者自述局限

- 只支持用 `rdf:type` 标注类型的图；Wikidata 那类自有类型体系的图**不直接支持**，要写 adapter，留作未来工作。
- 领域 text–SPARQL benchmark 太少；联系多个 KG 作者仍拿不到更大数据集，只能靠 88–108 题级的四个题集。
- 伦理段：LLM 仍可能生成语法合法但语义错的 query，决策场景要人工核；作者用 −38% 成本 / −24% 时间来对冲推理的环境成本。

## 原文

- PDF：同目录 `2609.01780-kgvoyager.pdf`；正文 [paper.md](./paper.md)、参考文献 [references.md](./references.md)、附录 [appendix.md](./appendix.md)
- arXiv：2609.01780v2（2026-10-15 更新；首次提交 2026-09-01，cs.IR）；代码/数据：https://anonymous.4open.science/r/nl2sparql2-C171 （匿名仓库，未 pin commit）
