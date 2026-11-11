---
status: draft
source_type: paper
reading: 精读
provenance: 原文正文
updated: 2026-11-09
arxiv: 2610.36570
title: "CASEL: Consequence-Aware Selective Execution for Reliable Long-Horizon Tool-Using Agents"
authors: Yanyan Zhang, Fei Shen, Ting Yan, Hao Zhang
pdf: 2610.36570-casel.pdf
direction: 5
home: topics/01-constraint
subtopic: action-gate
also_supports: []
evidence_role: harness-evidence
execution_form: none
updates:
  - topics/01-constraint/action-gate/README.md
  - topics/01-constraint/claims.md
  - topics/01-constraint/sources.md
  - topics/conclusions.md
published: 2026-10
admission: admitted (probation)
gate_checked: 2026-11-11
impact_evidence: "I2: CMU + Dartmouth"
liveness: arXiv 2026-10
provenance_type: academic
---

# CASEL: Consequence-Aware Selective Execution for Reliable Long-Horizon Tool-Using Agents · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

把「执行前要不要拦」从单一不确定性分数改成**后果感知的运行时分配**：用校准失败概率 × 后果、可逆性、歧义、证据新鲜度，在 direct / verify / sandbox / clarify / approve / abstain 六种模式里按代价选一个；模拟中把有害副作用轨迹从 14.75% 降到 7.02%，但代价是审批量。

## 问题与设定

- **问题**：两个动作同样 20% 失败概率，读操作重试很便宜，不可逆转账很贵；只看不确定性或只看「是否 mutating」都会把不同后果的动作同等对待。
- **机制**：运行时层，位于任意 base agent 与工具执行器之间；每步估计 `p̂`（校准失败概率）、`ĉ`（后果）、`ρ`（可逆性）、`g`（歧义）、`d`（证据新鲜度），选模式最小化 `J(m)=γ_m·p̂ĉ + λk(m) + μq(m)`。
- **六模式**：direct / verify / sandbox / clarify / approve / abstain；实际只用了 5 个（abstain 与 staleness 分支未启用）。
- **评估**：**受控模拟**，20 seeds；每 seed 40,000 calibration + 6,000 trajectories × 20 actions = 120,000 test actions；58% read-only、28% reversible、14% irreversible；所有方法同一 intervention menu、同一 compute cost（0.486）。
- **假设**：intervention effectiveness（γ_m）是**假定常数**，不是测量；成本 k/q 也是假定。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 机制/设定 | digest §1–3；原文见 `paper.md` |
| 关键数字 | Table 2 |
| 图表 | 见下表 / `figures/` |
| 判断/工程用法 | [digest.md](./digest.md) |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| `fig-1-runtime.png` | — | 见 digest 图注 | ✓ |
| `fig-4-harm-frontier.png` | — | 见 digest 图注 | ✓ |

## 作者自述局限

- **模拟**：intervention effectiveness 是假设，不是测量；结果只排序分配规则，不证明部署有效。
- **成本假设**：γ_m、k、q 都是常数；真实系统里它们随工具/上下文变化。
- **abstain 与 staleness 分支未启用**。
- **trajectory ledger 前提失败**：54% 直接执行步骤 `p_t c_t > r̄_t`；residual harm 不在账本内。
- **审批疲劳/信任成本未建模**；approvals 只是一个比例。
- **任务 success 与 HSR 可以反向**：CASEL 的 HSR 更低，但 task success 低 1.79 pp。

## 原文

- PDF：同目录 `2610.36570-casel.pdf`
- arXiv:2610.36570
