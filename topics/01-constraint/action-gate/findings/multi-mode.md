# 多模式分配与前沿

## F5

- **判断**：把 menu 的排序信号从 `p̂` 换成 `p̂ĉ`、并用可逆性限制可行模式（CASEL），在表 2 同一 compute（0.486）下能把 HSR 压下来，但不是单轴支配：CASEL 的审批更多、task success 更低。它的位置是 harm–approval 前沿上的取舍——相对 Risk-Menu「相近 harm、审批少约 30%」。范围限定：Base / Always-Verify / Mutation-Gated 的 menu 与 compute 都不同于 menu 类方法。
- **等级**：`已核`（CASEL 一手正文；**模拟**，不是部署）。
- **条件**：20 seeds；每 seed 40,000 calibration + 6,000 trajectories × 20 actions = 120,000 test actions；动作混合 58% read / 28% reversible / 14% irreversible；主表在 `τ̂=∞`（阈值关闭）下；`γ_m/k/q` 是假设值；menu 类方法同 compute 0.486，Base 0.000 / Always-Verify 1.000 / Mutation-Gated 0.420（menu 分别 —/verify/—）。
- **数字**：相对 Uncertainty-Menu（只按 `p̂`）：HSR 14.75% → 7.02%（paired −7.73 pp，95% CI [−7.87,−7.60]）；MNH 0.184 → 0.123；审批 6.9% → 8.7%；task success 48.79% → 47.01%（低 1.78 pp；正文取整写 1.79）。相对 Risk-Menu：HSR 5.82% / 审批 12.6%；CASEL 7.02% / 8.7%。
- **反例/边界**：CASEL 不是最低 HSR（Consequence-Menu 4.38% / 审批 13.8%；Risk-Menu 5.82% / 12.6%）；task success 与 HSR 反向；`γ_m` 未测量；审批疲劳未建模。验证边界：HSR 是稀疏事件，2 周 log-only 不能判 HSR 降幅；Stage 2 shadow/A-B 需按基线 HSR 与最小可检测差异先算样本量（`推测`；见 [mechanism 工程发现 4](../mechanism.md)）。
- **来源**：[CASEL 卡](../../../../src/papers/2610.36570-casel/card.md) · [digest](../../../../src/papers/2610.36570-casel/digest.md) · [E-15](../../../conclusions.md)

## F6

- **判断**：护栏评估应报 **harm–approval–cost 前沿**；full trajectory ledger 在 harm–compute 面被支配，但在低审批端仍是前沿点；不能把 CASEL-NoRev 的 15.53% 归因给「可逆性路由」——NoRev 是 verify-only，同时去掉了 sandbox/approve。
- **等级**：`已核`（CASEL 模拟；前沿是作者的解释，不是部署结果）。
- **条件/数字**：Risk-Menu 5.82% HSR / 12.6% approvals；CASEL 7.02% / 8.7%；CASEL-NoRev 15.53% / 0.0%（menu=verify，coverage 51.4%）；CASEL+Budget 11.82% / 4.3%；CASEL-Uncal 8.22% / 8.4%；54% 直接执行步骤 `p_t c_t > r̄_t`，ledger 前提失败；E-15。
- **反例/边界**：模拟；审批疲劳未建模；task success 与 HSR 反向；单步决策，不覆盖多步组合后果；NoRev 不能当单变量消融；full ledger 不是「一律禁用」，是低审批端的前沿点。替代方案缺口（`推测`）：blanket veto / 静态 `p̂ĉ` gate / 纯人工都没有同口径 TCO、审批率、task success；不能把 CASEL 的 8.7% 审批率当纯人工复核成本（见 [mechanism 工程发现 4](../mechanism.md)）。
- **来源**：[CASEL digest](../../../../src/papers/2610.36570-casel/digest.md) · [E-15](../../../conclusions.md)
