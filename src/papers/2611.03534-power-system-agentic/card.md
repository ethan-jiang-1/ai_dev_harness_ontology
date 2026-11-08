---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-08
arxiv: 2611.03534
title: An Agentic Framework for Automated Power System Studies and Grid Connection Assessment
authors: MaoXun Huang, Kshitij Kapoor, Eli Louise（Grid Agents）
pdf: 2611.03534-power-system-agentic.pdf
direction: 1
home: topics/03-knowledge
subtopic: compilation
updates:
  - topics/03-knowledge/compilation/README.md
  - topics/03-knowledge/claims.md
  - topics/03-knowledge/sources.md
  - topics/domains.md
  - topics/conclusions.md
---

# An Agentic Framework for Automated Power System Studies and Grid Connection Assessment · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

面向受监管工程工作的完整 agent 系统：**答案必须引用法规证据、数字必须由成熟求解器算、人做最终决策**；Grid Ontology 做知识/记忆（27 docs/6,347 pages），Grid Studio 用领域工具+求解器跑 519 个电力系统任务；99.9% 端到端得分、中位 13.9 s，比所有 baseline 又快又准。

## 问题与设定

- **问题**：并网评估需要两种稀缺技能——按不断变化的法规核查申请；跑电力系统研究（潮流/N-1/短路）。agent 的三种失败：无来源的流畅文本；不可信的大网络算术；答案对但「背后的工作」不可验证。
- **任务**：8 个已发表电力系统 benchmark 家族，合并为 **519 tasks**；网络 4–9,241 buses；统一评分尺度。
- **系统**：
- **Grid Ontology**：法规/标准/工程知识 + 可检索 + 记忆（semantic/procedural/episodic）；共享变更需人批准。
- **Grid Studio**：领域工具 + 研究框架 + 求解器；optimizer 在环做 reinforcement 规划。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 机制/设定 | digest §1–3；原文见 `paper.md` |
| 关键数字 | §5.1 / Table 4 / §5.2 / Table 5 |
| 图表 | 见下表 / `figures/` |
| 判断/工程用法 | [digest.md](./digest.md) |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| `fig-1-score-time.png` | — | 见 digest 图注 | ✓ |
| `fig-2-system.png` | — | 见 digest 图注 | ✓ |

## 作者自述局限

- 技术报告；系统/数据不完全公开；GB corpus 是特定法规集。
- benchmark 是单个研究任务；真实 connection study 会串联多个研究。
- 最大 9,241 buses；真实运营商可达数万。
- 没有形式安全保证；human sign-off 是流程保证，不是证明。
- 长期部署/维护成本未量化。

## 原文

- PDF：同目录 `2611.03534-power-system-agentic.pdf`
- arXiv:2611.03534
