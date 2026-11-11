---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-09
arxiv: 2607.22868
title: "What Can Be Enforced? A Theory of Certified Runtime Safety for Tool-Using Agents"
authors: Shawn Ray
pdf: 2607.22868-what-can-be-enforced.pdf
direction: 5
home: topics/01-constraint
subtopic: action-gate
also_supports: []
evidence_role: harness-evidence
execution_form: none
updates: []
---

# What Can Be Enforced? · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

运行时 guardrail 的保证取决于三件事：策略状态是否可表示、judge 能观察到什么、阻断是否改变未来行为。作者把这三件事拆成 T1 表达力边界、T2 统计/安全边界、T3 可判定性边界；给出 Neyman–Pearson false-block/miss 前沿、conformal 有限样本证书（可能是 vacuous block-all）、闭环前沿不可由静态分数识别的条件。

## 问题与设定

- 问题：tool-using agent 的动作前 gate 能执行哪些安全策略？在 fallible judge 下，false-block/miss 的极限是什么？阻断改变未来 proposal 后，静态评测还够不够？
- 模型：固定 oracle 谓词 + register automaton；fallible judge；有限受控模型 + occupancy program。
- 实验：AgentDojo 132 条（97 user-task + 35 injection-goal）× 23 judges；有限两步 retry 模型；表示攻击；paired closed-loop reruns。
- 代码/缓存分数：`https://github.com/shawnray-research/certified-agent-guardrails`。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| T1 表达力边界 | §4 |
| T2 统计/安全边界（NP 前沿、conformal） | §5 |
| T3 可判定性边界 | §6 |
| AgentDojo 23 judges / block-all | §7 / Figure 1 |
| 有限受控 retry 模型 | §7 / Appendix B.2 |
| 表示攻击 | §5 / §7 |
| 证明 | Appendix A |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| Figure 1 | p.2 / §7 | 三个 regime、三个 estimand | — |
| Table/Figure（ROC/conformal） | §7 | δ 点、block-all、false-block 区间 | — |
| Appendix B.2 | — | 两步 retry 的 occupancy polytope | — |

## 作者自述局限

- 理论 + 诊断，不是部署；AgentDojo 是 prompt-injection 安全评测，不是工具授权/commit gate。
- Conformal 证书是 marginal、label-conditional、per deployment proposal；不是 within-episode independence，也不是语义正确性。
- block-all 的「零 miss」是 vacuous certificate；不能当「安全」。
- 表示攻击的 margin 是分布性的，不是 universal semantic soundness。
- 代码未在本地跑。

## 原文

- PDF：[2607.22868-what-can-be-enforced.pdf](./2607.22868-what-can-be-enforced.pdf)
- 正文 MD：[paper.md](./paper.md)
- arXiv：https://arxiv.org/abs/2607.22868
- 代码/数据：见上；未跑。
