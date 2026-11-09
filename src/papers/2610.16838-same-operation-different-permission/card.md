---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-09
arxiv: 2610.16838
title: "Same Operation, Different Permission: Evaluating Whether Guardrails Honor Authorization"
authors: Huihao Jing, Shaojin Chen, Wenbin Hu, Yuxuan Liu, Haochen Shi, Zhongwei Xie, Haoran Li, Yangqiu Song
pdf: 2610.16838-same-operation-different-permission.pdf
direction: 5
home: topics/01-constraint
subtopic: action-gate
also_supports: [commit-gate]
evidence_role: harness-evidence
execution_form: none
updates: []
---

# Same Operation, Different Permission · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

同一个操作，在合法授权与禁止授权下应当得到相反决策；现有 guardrail 评测只看「拦住了多少」，不看「放过了多少合法请求」。作者用 50 个场景 × 4 种授权证据 + 1,594 条 native policy 请求，测「blocked 是不是正确拒绝」；发现很多 blocked 是 review 失败，不是正确拒绝。

## 问题与设定

- 问题：guardrail 的决策是否跟随授权——拦住未授权动作，同时放行同一操作的合法授权。
- 语言轨：50 scenarios × 4 contexts = 200；40 dev / 160 test；80 lawful / 80 forbidden；1,600 effects。
- Native 轨：1,594 OpenFGA/Cedar 请求（47 apps / 60 policies）；379 dev / 1,215 test；引擎复现参考标签。
- Guardrail：8 个配置；Qwen3.5-9B/27B、Safeguard、Granite、PolicyGuard、NeMo、Qwen3Guard、Nemotron。
- 评分：决策正确性、可用性（usable/unavailable）、实际 effect；同一请求跨 guardrail 变化按 identity 配对。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 语言轨 case 格式 / 4 contexts | §3.1 |
| 标注与一致性（κ=0.91） | §3.2 / Appendix B |
| Native 轨（OpenFGA/Cedar） | §3.3 |
| Effect 检查（1,600 effects） | §3.4 |
| 8 个 guardrail 配置 | §4.1 |
| 语言轨主表（Table 1） | §5.1 / Table 1 |
| Native 轨主表（Table 2） | §5.1 / Table 2 |
| 结构化 review 的 unavailable | §5.2 / Table 1 |
| 加 reviewer 的 veto | §5.3 / Table 2 |
| 作者局限 | §5 / Limitations |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| Table 1 | p.7 | matched-interface 结果：forbidden effects / lawful completions / unavailable | — |
| Table 2 | p.9 | native 轨单 reviewer 与 all-must-allow 组合 | — |
| Figure 1 | p.6 | interface 变化下 lawful requests 的 gained/lost | — |
| Figure 2 | p.6 | native 轨各 reviewer 的 correct/lawful/false denial | — |
| Table 4 | Appendix C.1 | 8 个原始配置 | — |

## 作者自述局限

- 50 个语言场景由 AI 辅助起草；三位标注者都是安全背景，缺临床/法律/金融从业者视角。
- 语言轨是合成场景；native 轨是 decision-only，无 execution effect。
- 单次 attempt、32K context、一小时 deadline；模型配置不同，比较的是完整体验，不是孤立模型因素。
- 3 seeds；不能把单次 seed 的增减当稳定效应。
- 没有本体；不是 commit gate；不测 harm。

## 原文

- PDF：同目录 `2610.16838-same-operation-different-permission.pdf`
- arXiv：https://arxiv.org/abs/2610.16838
- 代码/数据：论文附录 A 有 reproduction guide；未在本地跑。
