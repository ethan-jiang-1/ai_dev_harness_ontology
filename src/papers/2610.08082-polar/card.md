---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-08
arxiv: 2610.08082
title: "POLAR: Ontology-Guided Risk Prevention for Tool-Calling LLM Agents"
authors: Yunju Kang, Seonghyeon Cho, Irene Li, Yeo-Chan Yoon, Chanjun Park
pdf: 2610.08082-polar.pdf
direction: 1
home: topics/01-constraint
subtopic: action-gate
updates:
  - topics/01-constraint/action-gate/README.md
  - topics/01-constraint/action-gate/findings.md
  - topics/01-constraint/action-gate/frontier.md
  - topics/01-constraint/claims.md
  - topics/01-constraint/sources.md
  - topics/conclusions.md
---

# POLAR · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

把动作前安全从「LLM 判断危不危险」换成「是否存在可接受的逆操作序列」：T1–T5 可逆关系 + 状态投影 + 反向搜索，取最弱一步分数；但收益随基线能力下降，T1-only 接近 blanket veto。

## 问题与设定

- 问题：tool-calling agent 的不可逆动作；结构化可逆性判据能否在动作前阻止。
- 基准：τ²-bench；6 模型 × 3 域（airline/retail/telecom）× 4 臂；18 格；10,800 rollouts。
- 数据：airline 2,954 / retail 2,882 / telecom 2,785 初始 DB 行；agent 可见 1,758/1,079/1,325。
- 方法：Layer A（Datalog 逆关系）+ Layer B（状态投影）+ 反向搜索 π；φ=最弱一步；τ=0.80。
- 对照：no guard、blanket veto、uncertainty ranking、full、tier ablation。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 两层本体 / T1–T5 | §3 / Table 2, p.4 |
| 反向搜索 / 评分 | §4 |
| 18 格 Δ | Table 3, p.6 |
| 能力斜率 | Fig. 2 / §5.3 |
| τ 保留率 | Table 4, p.7 |
| tier ablation | Table 5, p.7–8 |
| block log | §5.4 |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| Fig. 1 | p.2 | 任务示例 / 可逆性 | ✓ |
| Fig. 2 | p.3 | 架构（Layer A/B + 反向搜索） | ✓ |
| Table 3 | p.6 | 18 格 Δ | — |
| Table 5 | p.8 | tier ablation | — |

## 作者自述局限

- reward 不是防伤害的直接度量；被 veto 的风险动作不体现在 reward。
- T1-only 接近 blanket veto；结构贡献未隔离。
- 不模拟完整 s′、不验证逆执行；单基准；1,745 blocked decisions 无 harm 标签。
- 阈值斜率是六点描述性拟合，不是部署阈值。

## 原文

- PDF：同目录 `2610.08082-polar.pdf`
- arXiv:2610.08082
- 代码/数据：论文未给独立仓库。
