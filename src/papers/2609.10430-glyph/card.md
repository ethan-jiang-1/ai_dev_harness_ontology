---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-09
batch: 补给
published: 2026-09-09
venue: arXiv preprint (Apple production system)
reliability: high
impact: high
region: US (Apple, Seattle / Cupertino)
arxiv: 2609.10430
title: Glyph - A Multi-Strategy Agentic System for Column Description and Sensitivity-Ontology Tagging of Enterprise Data Catalogs
authors: Kostia Kudriavtsev, Parvez Rafi, Sha Sundaram
pdf: 2609.10430-glyph.pdf
direction: 1
home: topics/01-constraint
subtopic: access-control
also_supports: []
evidence_role: mechanism-only
execution_form: label
updates: [topics/01-constraint/access-control/README.md, topics/01-constraint/sources.md]
---

# Glyph · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

企业目录里「列是什么」和「这一列属于哪类敏感数据」长期欠账，而最敏感的表又不许先读值再分类；Glyph 用两个 LangGraph agent 把两件事分开做——Descriptor 从**生产该列的流水线源码**（企业 GitHub 搜索，active RAG）造描述，Tagger 用 description / 正则 / 元数据三策略并行、RRF(k=60) 融合后按敏感性 tier 重排，从内部 **275-leaf Data Classification Ontology** 出标签，全程不读 cell value，每个标签带 per-tag provenance。**评级依据**：`reliability: high` 取「Apple 生产目录上的真实部署 + 评估口径/留出方式/指标缺陷都写明 + Table 2/3 可复算」；`impact: high` 因为它是本仓库目前唯一「企业级敏感性本体 + 真实规模目录 + 生产人审回路」的标签层来源，直接对应 04 C.1 的「标签/分类」一行。但单企业单目录、本体不公开、无 OOD/公开基准，故 `已核` 只指「作者报告了什么」。

## 问题与设定

- **任务与规模**：两件事耦合——(i) 列描述生成；(ii) 列级**多标签**敏感性分类（标签来自受治理的敏感性本体，不是开放域类型）；运行在单一组织（Apple）的生产目录上，约 **3.4M 列 / 98,000 表 / 4 条业务线 / 3 种存储后端**（Iceberg、RDBMS、Cassandra）（§1, p.1）。
- **输入**：只用元数据键 `catalog.database.table.column`（+ 可选人工描述），**不读 cell value**；训练语料是已验证的 `metadata_key → tags`；评估集是 steward 按业务线写的 `{column metadata, expected tags}`，1,905 表与 15,205 表的向量索引表级不相交（§4.4–§5, p.6–7）。
- **模型/基线**：commercial LLM（Table 3 写明 Claude Sonnet 4.5）+ 自微调 6 层 all-MiniLM-L6-v2（384 维，~90 MB）；无公开 benchmark，消融是「三策略各自单跑 vs 全融合」（Table 3, p.7），编码器对比是**同一模型 pre/post fine-tuning**（Table 2, p.6）。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 两 agent 状态图、judge 位置 | digest §3.1；原文 Fig. 1（p.4） |
| Descriptor 四段 / 三策略的输入·输出·失败模式 | digest §3.2–§3.3；原文 §4.2–4.3（p.4–5） |
| RRF 公式、k=60、tier 权重、provenance 优先级 | digest §3.4；原文 §4.3.4（p.5–6） |
| 检索数字 / 端到端 F1-F2 / 生产接受率 | digest §4.2–§4.5；原文 Table 2（p.6）、Table 3（p.7）、Fig. 2（p.7） |
| 作者自述「证明了什么/没证明什么」 | digest §5、§7；原文 §6 末、§7（p.8） |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| Fig. 1 | p.4 | 两 agent 的 LangGraph 拓扑：Descriptor 四节点 + Tagger 三策略 + merge_all_tags(RRF k=60) | ✗（见 PDF） |
| Fig. 2 | p.7 | 6 周 steward 接受率 63.3%→99.8%；**纵轴自 50% 起**，视觉斜率被放大 | ✗ |
| Table 1 / 2 | p.6 | 单列三策略投票与 RRF 分数 0.333/0.667/0.328；编码器 pre/post 的 NDCG@10/MRR@10/Acc@1,5/MAP@100 | ✗（`paper.md` 两表同段交错） |
| Table 3 | p.7 | 端到端 F1/F2 × 三组 + overall + p50 延迟，四配置 | ✗ |
| Table 4 | p.8 | 与 Sherlock/Sato/Doduo/Korini&Bizer 的定位对比（taxonomy 不同，不可比） | ✗ |

## 作者自述局限

- 与公开 CTA 的 F1 **不可直接比**：taxonomy（275 内部标签 + 敏感级 vs 78–91 开放域类型）、标签基数（多标签、极度偏斜）、可用信息（元数据+代码 vs cell value）都不同（§5.3, p.8）。
- 编码器数字是**同分布上界**：列级留出，同表列可能同时出现在 query 与 corpus，未控表内泄漏（§4.4, p.6）。
- 生产接受率是 **association 不是因果**（判定量 6 周涨 21×、受审人群也在变），且 steward 只看系统吐出的标签，接受率**对漏标不敏感**（§5.2, p.7）；本体与内部代码不公开、标签名是占位符（§3 脚注 1, p.3），public-benchmark generalization 与 judge–human agreement 明确留给未来（§7, p.8）。

## 原文

- PDF：同目录 `2609.10430-glyph.pdf`；正文 [paper.md](./paper.md)、参考文献 [references.md](./references.md)、附录 [appendix.md](./appendix.md)（原文无附录）
- arXiv：2609.10430v1（2026-09-09，cs.MA；版式带 AAAI 2027 版权声明，但未声明录用，按 preprint 记）
- 代码/数据：未报告（无仓库、无数据集、无本体发布）
