---
status: draft
updated: 2026-11-12
---

# 落地经济学 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `feasibility/Fx`。
>
> **2026-11-12 对账**：F2（CAI，E-14）/ F3（CASEL，E-15）仍 admitted，保持 `已核`；F4 引用的 POLAR 斜率已撤回（作历史示例），N&D 零结果仍 admitted。横切综合本就是 `推测`。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 值不值得 = 位置 × 成本 × 使能条件，不是本体质量 | 推测 |
| F2 | 编译有可算盈亏平衡；平均 −38% 不能当上线依据 | 已核 |
| F3 | 分配没有单一最优；按 harm–approval–cost 前沿选点（模拟，CASEL 主表 τ=∞） | 已核 |
| F4 | 没有一条适用于所有机制的能力曲线 | 推测 |
| F5 | 护栏 NPV 的分母是 do-nothing；缺单价只给公式与敏感性 | 推测 |
| F6 | 没有 γ 实测，不做多模式；先上静态 gate | 推测 |

## F1 · 位置 × 成本 × 使能

- **判断**：同一机制，在一种配置下是护栏，另一种是纯开销；值不值得不是本体质量。
- **依据**：POLAR 强模型回退；CAI 时延约束；N&D 答案不在文本里；EvoMemState 无训练信号退化成 prompt。
- **等级**：`推测`（横切综合，不是单篇实证）。
- **来源**：本页 + 各派 digest。

## F2 · 编译盈亏平衡

- **数字**：`p_h > 2% + c/(0.929Q)`；Q=1,000、c=10 → 3.12%；p_h=2.5% 仍亏 5.8 query-equivalent。
- **含义**：平均 −38% 不能当上线依据；要看 hit/miss 分布、时延、复用次数。
- **来源**：[CAI digest](../../../src/papers/2610.41172-context-as-infrastructure/digest.md) §4.3/§6.5；E-14。

## F3 · 分配前沿

- **数字**：CASEL 8.7% approvals/7.02% HSR；Risk-Menu 12.6%/5.82%；Consequence-Menu 13.8%/4.38%。都是模拟主表值，**CASEL 的 7.02%/8.7% 在 τ=∞（阈值关闭）下**；阈值规则另测（§VI-E），不能把 7.02% 当「开了阈值」的结果。
- **含义**：没有单一 HSR 最小；审批少 30% vs 多 1.2 点 HSR，是业务选择。
- **来源**：[CASEL digest](../../../src/papers/2610.36570-casel/digest.md) Table 2；E-15。

## F4 · 没有单一能力曲线

- **数字/方向**：POLAR 约束收益随基线能力下降（六点描述性拟合，斜率 −0.76/−0.67/−0.31，不能当阈值）；N&D 投影增益不随容量上升（H2 单向检验 p=0.85，是「未检出」不是「证明无效应」）；9B 带投影 0.737 > 750B 不带 0.672（区间约 0.3 宽）。
- **含义**：不能用一个「能力越强越有用/越没用」的曲线概括所有机制。
- **等级**：`推测`（横切综合；POLAR 斜率已撤回作历史示例，N&D 零结果仍 admitted；「所有机制」是外推，E-19 也把这条列为推测）。
- **来源**：[POLAR digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-08082) §4.2；[N&D digest](../../../src/papers/2610.11768-narrow-and-deep/digest.md) §4；E-12/E-13。

## F5 · 护栏 NPV 的分母是 do-nothing

- **判断**：分配/护栏机制也能写成 NPV；统一反事实只能是「不上护栏」，不是 Uncertainty-Menu/Risk-Menu。缺单价时只能给公式与敏感性，不能给点估计。
- **公式**（[CASEL digest](../../../src/papers/2610.36570-casel/digest.md) §6.5 E4，建模约定）：伤害节省/千次 `= (32.76% − HSR) × (1000/L) × incidents_per_harmful_trajectory × cost_per_incident`（L=20 动作/轨迹）；审批成本/千次 `= approval_rate × 1000 × minutes_per_approval/60 × hourly_rate`；12 个月 TCO = 建设 + 运行（`0.58 × 基线算力成本`）+ 审批人时 + 维护；`NPV_build = Σ(伤害节省 − 审批成本 + task success 收益)/(1+r)^t − TCO`；`NPV_buy` 同口径（RFQ + 集成 + 迁移/退出），`NPV_do_nothing = 0`，取 argmax；硬约束 task success 降 ≤2pp、false-veto ≤5%。
- **边界**：公式与决策线是工程配方，不是 CASEL 论文结果——论文只给模拟 HSR/审批/compute（0.486），没有金额。`minutes_per_approval`、`hourly_rate`、`cost_per_incident`、`value_per_success`、`r` 全空（G1–G3）。
- **等级**：`推测`（公式与决策线）；代入的模拟基线 32.76%/0%/29.48% 为 `已核`（Table 2，模拟）。
- **来源**：CASEL digest §6.5 E4、Table 2；[frontier](./frontier.md) G1–G3。

## F6 · 没有 γ 实测，不做多模式

- **判断**：多模式分配按 `J(m)` 选模式，前提是 `γ_m` 可估；γ 只有假设值、或 CI 分不开模式时，先上静态 `p̂ĉ` gate，不做 verify/sandbox/approve 路由。
- **依据**：CASEL 的 γ 是模拟假设（direct/verify/sandbox/approve = 1.00/0.42/0.15/0.04），审批疲劳也未建模；其工程 stop 是：`γ_verify` 的 CI 宽到分不开 direct/verify 的 `J` 差 → 只上静态 gate；校准量不足以把 `γ_verify` 压到 ±3pp → 停、补标注；`p̂ĉ` 的 selective-risk AUC 未显著低于 `p̂` → 停。
- **等级**：`推测`（门槛是工程线；γ 是假设、论文未实测，`已核` digest 自述）。
- **来源**：CASEL digest §4.1/§6.5 stop；[mechanism §stop](./mechanism.md#stop-condition)。
