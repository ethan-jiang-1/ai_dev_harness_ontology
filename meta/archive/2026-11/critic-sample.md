---
status: superseded
updated: 2026-11-08
---

> **历史快照（2026-11-08/09）**：已归档，不再维护。现行规则见 `meta/README.md`，当前状态见 `meta/state.md`。文中的计数与结论可能已被后续修复取代。


# 独立 critic 抽样（G7）

平台：workflow 单/多 agent（subagent 通道不可用）。样本：**7/22 = 32%**，覆盖 L3 的机制型（MIOE、POLAR）、成本型（CAI、N&D）、判定型（Ontology Catch、CASEL）、状态型（FIRME）。

## 结果

| 论文 | 轮次 | 最终 verdict | 主要修正 |
|---|---|---|---|
| MIOE | 4 | **pass** | Entity/Context 是评估切分不是 prompt 写法；删除无出处的类级 0.03–0.65；区分单层 MDAS 0.59 与四层 DAS 0.667；SAE Iso 限 instance-of；标题加「干净、模块化」 |
| CAI | 4 | **pass** | 修正 Table 4/§8 引用；3× 时延是 7 题配对；46.7 s 是这 7 题未编译臂；85%/91% 不可比；43% 是反推；PageIndex 负面是 FRAMES 规模，10^5 是解析模型 |
| POLAR | 4 | **pass** | 补 gemini-flash-lite 行；说明 Δ 是 error-filtered arm mean、非配对；示例不再把 airline cancel 当 T1；T1 是「没有」不是「很少」；Δ 随 baseline 上升而下降；reward 不能证明防伤害 |
| N&D | 4 | **pass** | 补 H3 零结果及「K4/K4x 都含教训」限定；K4x 不是探索性；塔的 L0/L1–L4 顺序；物理深度未被测；评分规则改版；工具调用不是「从不」；24–68% 仅 GLM |
| Ontology Catch | 4 | **pass** | precision 是「人工故障 + 25% 错答案」不是真实答案；FA 15.0/9.7 是人工故障、16.8/3.5 是真实答案；type swap 定义与方向；C2 设计偏向 data-derived；C1a/C1b；C4 对 data-derived −10.6 |
| CASEL | 4 | **pass** | Always-Verify task success 58.81%；主表 τ=∞；NoRev 是 verify-only；J(m) 不含 task success；最低 HSR 是 Consequence 4.38%；approve 需 ĉ≥0.55；clarify 先于 J(m)；ledger 是低审批前沿点 |
| FIRME | 4 | **pass** | 状态机示例按 period 修正；no-alias/LLM-Norm 定义；MMR 是 Table 3 列、CMR=MMR×precision；CMR 协议（judge vs human audit）；token 不含 registry；normalization 的 S&P 值；0.8 阈值在 T−1 上选 |

## 限制

- 只有 7/22 做了独立 critic；其余 15 篇仍靠自评 + 数字回原文。
- critic 是 LLM agent，不是人类审稿；它也会漏/误判。
- 抽查不等于全文复现；数字仍以 `digest.md` 的出处为准。

## 结论

G7 的「≥30% 抽样」达成；7 篇最终 pass。剩余风险已写入 [quality-report](./quality-report.md) 的「未通过/限制」。
