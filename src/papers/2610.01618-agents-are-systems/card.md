---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-09
arxiv: 2610.01618
title: "Agents Are Systems, Not Models: Rethinking Agentic Evaluation"
authors: Luis Wiedmann, Leander Girrbach, Cordelia Schmid, Zeynep Akata
pdf: 2610.01618-agents-are-systems.pdf
home: topics/06-measure
subtopic: metrics
also_supports: []
evidence_role: harness-evidence
execution_form: none
updates:
  - topics/06-measure/metrics/README.md
  - topics/06-measure/claims.md
  - topics/06-measure/sources.md
  - topics/conclusions.md
published: 2026-10
admission: admitted (probation)
gate_checked: 2026-11-11
impact_evidence: "I2: TUM + Helmholtz + Inria"
liveness: arXiv 2026-10
provenance_type: academic
---

# Agents Are Systems, Not Models: Rethinking Agentic Evaluation · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

把 agent 当作**可配置系统**而不是固定模型：在 4 个 AI4S 任务上系统变化五个配置轴（信息 / 推理 / 验证 / 时间 / 模型），发现 **54% 的结果方差来自同一配置的重复运行**；**信息**的影响最大，超过模型大小与时间预算，并且同时降低成本和改善校准；**提示 agent 自检几乎不改变行为，给一个专用验证工具才会**。

## 问题与设定

- **问题**：agent 评测通常把 agent 当固定对象，只报一个 success rate；实际上用户可配置「告诉它什么、让它跑多久、用哪个模型」，这些选择会改变能力与可靠性。
- **任务**：4 个科学任务——redshift-estimation、mmlu-astronomy、promoter-prediction、rna-folding；agent 要找到并正确操作一个已发表的 specialist model。
- **规模**：432 cells × 5 runs × 4 tasks = 8,640 runs；18,240 trajectories。
- **五轴**：

| 轴 | 水平 |
|---|---|
| Information | none / identity / interface / protocol |
| Reasoning | act-only / think-act / ReAct |
| Verification | none / asked / reported / binding |
| Budget | 5 / 10 / 20 min |
| Model | Qwen3.5-35B-A3B / 122B-A10B / 397B-A17B |

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 机制/设定 | digest §1–3；原文见 `paper.md` |
| 关键数字 | §4.2 / Table 3 / §5 / §4.3 |
| 图表 | 见下表 / `figures/` |
| 判断/工程用法 | [digest.md](./digest.md) |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| `fig-1-axes.png` | — | 见 digest 图注 | ✓ |
| `fig-4-verification.png` | — | 见 digest 图注 | ✓ |

## 作者自述局限

- 只 4 个任务、2 个科学域；更多任务/域才能泛化。
- 排除了 memory、multi-agent 等其他轴；未来要加。
- 「系统设计比 prompt 更有效」只在一个维度（verification）上验证，不能当普遍原则。
- 模型 FP8 量化；预算只有 3 档；任务/模型规模有限。
- 结果依赖 specialist reference；任务选择可能影响轴效应。

## 原文

- PDF：同目录 `2610.01618-agents-are-systems.pdf`
- arXiv:2610.01618
