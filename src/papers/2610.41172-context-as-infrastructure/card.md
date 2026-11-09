---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-09
arxiv: 2610.41172
title: Context as Infrastructure - Knowledge Compilation for Retrieval in Agentic Systems with Harnesses
authors: Zhichang Yu, Baining Cao, Sbaaoui Idriss, et al.（infiniflow / RAGFlow）
pdf: 2610.41172-context-as-infrastructure.pdf
direction: 3
home: topics/03-knowledge
subtopic: compilation
also_supports: []
evidence_role: harness-evidence
execution_form: none
updates:
  - topics/03-knowledge/compilation/README.md
  - topics/03-knowledge/compilation/findings.md
  - topics/03-knowledge/compilation/frontier.md
  - topics/03-knowledge/claims.md
  - topics/03-knowledge/sources.md
  - topics/00-harness/context.md
---

# CAI · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

在强词法 harness 下，检索前的「知识编译」不提高准确率；带逐字证据的 claim–leaf 树能条件性省 token（充分 −91%、不充分 +1.9%、平均 −38%），盈亏平衡 2%，但省 token 可能用检索轮次/时延换。

## 问题与设定

- 问题：agentic retrieval 的上下文成本；编译能否作为「供给层」降预算。
- 数据：FRAMES N=200；BrowseComp-Plus 参考；英文 Wikipedia。
- 模型：MiniMax M3 作答；glm-4-flash 抽取；BM25/grep harness。
- 基线：无编译 harness；RAPTOR/PageIndex/wiki/entity graph/ontology。
- 条件：同一 harness、同一抽取器、同一 gate，只变工件/服务模式。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 三层结构（供给/契约/控制） | §3 / Fig. 1, p.4 |
| 六段编译流水线 | §3.2 |
| claim 单元 / tree 模板 | §3.3 |
| 三种服务模式 E1/E2/E3 | §4 |
| 准确率/token/时延 | §5 / Table 4 / Fig. 2 |
| 成本模型 2%/43% | §6 |
| 部署 ledger（空） | Table 2 / §7 |
| 消融与 PageIndex | §8 |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| Fig. 1 | p.4 | 三层结构（supply/contract/control） | ✓ |
| Fig. 2 | p.6 | 条件性 token + 决策门时延 | ✓ |
| Table 4 | p.10 | FRAMES 主测量（准确率/token/时延） | — |
| Table 2 | — | 部署 ledger；无一行达标 | — |

## 作者自述局限

- 单基准、单 compiler、单 answer model；无 CI、无重复种子。
- FRAMES 是英文 Wikipedia；企业表格/扫描/行话未测。
- PageIndex 负面是规模观察，75% routing 是解析模型。
- `p_h` 不是正确率；φ 未测；部署层无观测。

## 原文

- PDF：同目录 `2610.41172-context-as-infrastructure.pdf`
- arXiv:2610.41172
- 代码/数据：论文未给独立仓库。
