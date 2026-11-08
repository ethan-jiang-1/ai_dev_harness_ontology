# 多模式分配与前沿

## F5

- **判断**：在同等成本下，后果感知的多模式分配优于不确定性排序（模拟）。
- **等级**：`已核`（CASEL 一手正文；**模拟**，不是部署）。
- **条件**：20 seeds、120,000 test actions；所有方法同 intervention menu、同 compute cost；γ_m 为假设常数。
- **数字**：HSR 14.75% → 7.02%（paired −7.73 pp）；MNH 0.184 → 0.123；审批 8.7%；task success 47.01 vs 48.79（低 1.79 pp）。
- **反例/边界**：CASEL 不是最低 HSR（Risk-Menu 5.82%）；task success 与 HSR 反向；`γ_m` 未测量。
- **来源**：[CASEL 卡](../../../../src/papers/2610.36570-casel/card.md) · [digest](../../../../src/papers/2610.36570-casel/digest.md)

## F6

- **判断**：护栏评估应报 **harm–approval–cost 前沿**；轨迹总账会反噬；可逆性路由贡献大部分增益。
- **等级**：`已核`（CASEL 模拟）。
- **条件/数字**：Risk-Menu 5.82% HSR / 12.6% approvals；CASEL 7.02% / 8.7%；CASEL-NoRev 15.53%；CASEL+Budget 11.82%；未校准 8.22%；E-15。
- **反例/边界**：模拟；审批疲劳未建模；task success 与 HSR 反向；单步决策，不覆盖多步组合后果。
- **来源**：[CASEL digest](../../../../src/papers/2610.36570-casel/digest.md) · [E-15](../../../conclusions.md)
