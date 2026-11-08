---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-08
arxiv: 2611.02395
title: Solver-Like Behavior in Large Language Models as Formalizers
authors: Rikhil Amonkar, Stuti Mohan, Kevin Nguyen, Ceyhun Efe Kayan, Ronan Le Bras, Li Zhang（Drexel / AI2）
pdf: 2611.02395-solver-like-behavior.pdf
direction: 3
home: topics/06-measure
subtopic: trace
updates:
  - topics/06-measure/trace/README.md
  - topics/06-measure/claims.md
  - topics/06-measure/sources.md
  - topics/conclusions.md
---

# Solver-Like Behavior in Large Language Models as Formalizers · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

LLM-as-formalizer 的推理轨迹经常**自己把求解器该做的搜索做完了**（solver-like behavior, SLB），而程序只是复述答案；只看程序输出的评估区分不出「搜索」与「复述」。2,000 条生成中 85% 轨迹有 SLB、占 24% 推理 token；把问题的值藏到运行时占位符后面，SLB 减少 97% 且不损准确率。

## 问题与设定

- **问题**：formalizer 的承诺是「LLM 写程序，solver 搜索」；如果推理轨迹已经算完答案，程序只是复述，solver 的保证就失效。输出评估看不出来。
- **数据**：4 个约束满足数据集（Calendar Scheduling、Meeting Planning、ZebraLogic、BlocksWorld），每个 100 instances；2 种形式语言（Python imperative；Z3/PDDL declarative）。
- **模型**：DeepSeek-V4-Flash、GPT-OSS-120B、Qwen3.8-27B（都是会写长 trace 的 reasoning model）。
- **规模**：2,000 generations；LLM judge（Gemma 4 31B-it）标注，与盲人标签一致率 90–98%。
- **能证明**：SLB 普遍、冗余、与准确率无关；形式语言影响最大；占位符能几乎消除 SLB。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 机制/设定 | digest §1–3；原文见 `paper.md` |
| 关键数字 | §5 / §6 |
| 图表 | 见下表 / `figures/` |
| 判断/工程用法 | [digest.md](./digest.md) |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| `fig-2-ontology.png` | — | 见 digest 图注 | ✓ |
| `fig-6-interventions.png` | — | 见 digest 图注 | ✓ |

## 作者自述局限

- 3 个模型、4 个 CSP 数据集、2 种 FL；定理证明/优化/其他语言未测。
- DeepSeek 每个数据集只跑一种 FL（API 模型变了），H4 主要靠 Qwen/GPT-OSS。
- 同一数据集的两种 prompt 不只差 FL（PDDL 还给了参考 problem file），H4 的 PDDL 差异可能被 prompt 混淆。
- 每个设置只生成一次，区间不含采样方差。
- LLM judge 的参考样本小（A1 110 段、A2 40 traces、B 60 programs）；A1 只检查段落，不检查整条 trace。
- B/C 覆盖非随机子集（只程序能跑、只 complete reasoning answer）。

## 原文

- PDF：同目录 `2611.02395-solver-like-behavior.pdf`
- arXiv:2611.02395
