---
status: draft
source_type: paper
reading: 精读
provenance: 原文正文
updated: 2026-11-12
admission: admitted
gate_checked: 2026-11-12
published: 2026-09-23
liveness: "ICDM 2026 Demo track（accepted）；arXiv v2 2026-10-08（首次 2026-09-23）"
impact_evidence: "I1: ICDM 2026 Demo track（同行评审）；I2: 中国联通软件研究院 + 南开大学"
provenance_type: academic
region: China
venue: "ICDM 2026 Demo track（accepted）；arXiv v2 2026-10-08；4 页短文"
reliability: medium
impact: medium
arxiv: 2609.27257
title: "UniDataAgent: An Ontology-Grounded Agent for Enterprise Question-to-Report Automation"
authors: Yutai Duan, Yahui Zhao, Zhangti Li, Yu Ma, Zhenfeng Qi, Shaoyang Yuan, Jing Fan, Jie Liu
pdf: 2609.27257-unidataagent.pdf
home: topics/06-measure
subtopic: feasibility
also_supports: []
evidence_role: mechanism-only
execution_form: compiled
updates:
  - topics/06-measure/feasibility/mechanism.md
  - topics/06-measure/feasibility/findings.md
  - topics/06-measure/claims.md
  - topics/conclusions.md
  - deliverables/05-production-landscape/02-sections/04-china.md
  - deliverables/05-production-landscape/02-sections/06-cases.md
  - deliverables/05-production-landscape/02-sections/90-sources.md
---

# UniDataAgent（中国联通）· 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

企业问数-报表自动化的难点不在 SQL，而在「组织特有的语义」；中国联通软研院把流程拆成「离线本体获取与验证（OAV）+ 在线问报到报表（QRE）」——本体从元数据/业务材料/专家技能里长出来并版本化，在线用语义契约约束执行——27 张企业表、数千指标类型，本体构建从约一周降到数小时，40 问严格准确率 95.0%（文档 RAG 72.5%）。

## 问题与设定

- **场景**：企业内「问题 → 报表」的自动化；难点是指标口径、范围、维度与物理映射的组织特有语义，而不是把问题翻译成 SQL。
- **方法**：OAV（四阶段构造循环 + 约束生成 + 问题验证 + 专家评审，产出**版本化本体**）；QRE（语义契约检索 → 技能/工具编排 → ReAct 循环 → 结果校验 → 证据链报告）。
- **数据**：27 张企业表、约数千指标类型；评测 40 个真实业务问题（按任务类型互斥分组）。
- **基线**：文档 RAG（同一企业数据环境）。
- **模型**：DeepSeek-V4。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 总体架构（OAV + QRE） | Fig. 1，§III |
| OAV 四阶段构造循环 | §III-A |
| QRE 的 plan–act–observe 与证据约束 | §III-B |
| 严格准确率分任务类型 | Table I（§IV） |
| 本体构建与报表生成的工时对比 | §I、§III-A（「a few hours / about one week」「minutes / several working days」） |

## 图表索引

| 图/表 | 页码 | 说明 | 是否已提取 |
|---|---|---|---|
| Fig. 1 | p.1–2 | UniDataAgent 总览（OAV/QRE） | 否 |
| Table I | p.3 | 40 问、分任务类型、Doc-RAG vs Ours | 是 |
| Fig. 5 | p.3 | 生成报告示例 | 否 |

## 作者自述局限

- 单企业（中国联通）、27 张表、40 个问题；「数千指标类型」是量级描述，不是精确计数。
- 工时对比是**定性**（「a few hours vs about one week」「minutes vs several working days」），没有实测人月。
- 对比基线只有文档 RAG，没有和「人工语义层/人工建模」做同任务对照。
- 没有失败率、没有错误类型分布、没有跨企业验证（只声称「可复制」）。
