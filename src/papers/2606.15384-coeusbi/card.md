---
status: draft
source_type: paper
reading: 精读
provenance: 原文正文
updated: 2026-11-12
admission: admitted
gate_checked: 2026-11-12
published: 2026-06-13
liveness: "PVLDB Vol.19 p.4076 (2026)；arXiv v1 2026-06-13"
impact_evidence: "I1: PVLDB Vol.19（2026，同行评审）；I2: Baidu Inc. + 北京邮电大学；I5: 官方 artifact https://github.com/rebornDanny/CoeusBI"
provenance_type: academic
region: China
venue: "PVLDB Vol.19, p.4076 (2026)；DOI 10.14778/3827998.3828017；本地 PDF 为 arXiv extended version"
reliability: high
impact: high
arxiv: 2606.15384
title: "CoeusBI: A Comprehensive Interactive Business Intelligence System Powered by LLMs at Baidu"
authors: Jinqing Lian, Chaofan Li, Yingxia Shao, Ming Wang, Yang Dong, Xinyi Liu, Wei Zhang, Chaoxian Gui, Tianqi Wan, Ming Dong
pdf: 2606.15384-coeusbi.pdf
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

# CoeusBI · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

百度的 BI 系统里，手写指标/维度/关系（YAML/LookML）跟不上 schema 变化；CoeusBI 用**离线视图生成 agent** 把 JOIN 密集的查询自动改写成单视图查询，用**两级 schema linking** 处理超宽 schema，再用**确定性 SQL 编译器**消掉方言与生成幻觉——部署在百度数据平台上、服务数千用户/日。

## 问题与设定

- **场景**：企业 BI 的自然语言问数。真实环境的三个难点：(a) 大量 JOIN 导致 SQL 生成准确率低；(b) 宽 schema 让 schema linking 变难；(c) 方言、多轮对话带来高成本与低准确率。
- **数据**：公开集 MS-Financial-Views（200 表/7,400 列/37 列每表）、MS-Commercial（2,281/65,000/28.5）；生产集 BD-Business Line A（百度某业务线）。
- **基线**：DIN-SQL（配 DeepSeek-R1-0528）等；另有灰度对照（25 人用 CoeusBI vs 25 人用旧工具，3 周）。
- **规模**：百度数据平台上的独立服务，覆盖视频/搜索/广告多条业务线，**数千用户/日**。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 架构（离线准备 + 在线查询） | Fig. 2、§3 |
| 视图生成 agent（错误反馈闭环） | §4 |
| 两级 schema linking（Word2View / View2Column） | §5 |
| 路由 agent + 确定性编译器 | §6 |
| 公开集与生产集统计 | Table 1 |
| 视图生成前后查询分布与 EX | Table 2 |
| 灰度可用性研究（55.7%、93%、89%） | §8.4.4 |
| 作者局限 | §5、§8、§9 |

## 图表索引

| 图/表 | 页码 | 说明 | 是否已提取 |
|---|---|---|---|
| Fig. 1 | p.2 | BI 流水线示例 | 否 |
| Fig. 2 | p.3 | CoeusBI 架构（离线/在线） | 否 |
| Table 1 | p.4 | 公开集 + 生产集表/列统计 | 是 |
| Table 2 | p.6 | 视图生成前后 Easy/Non-nested/Nested 分布与 EX | 是 |
| Fig. 3 | p.5 | 两级 schema linking | 否 |
| §8.4.4 | p.12 | 灰度对照（50 分析师/3 周） | 是 |

## 作者自述局限

- 生产集只有**一条业务线**（BD-Business Line A），不是全平台；其它业务线只给「覆盖」说法，无逐条数字。
- 「数千用户/日」是**定性量级**，没有精确 DAU、没有查询量、没有失败率。
- EX（execution accuracy）是**结果集匹配**，不等于「业务答案正确」；作者没有报人工正确率。
- 全文**没有美元成本**；token 效率是相对比较，不是账单。
- 部署时用到的粗排模型（如 Ernie-Tiny v2）、阈值参数（相似度阈值、融合系数）**未给具体取值**。
