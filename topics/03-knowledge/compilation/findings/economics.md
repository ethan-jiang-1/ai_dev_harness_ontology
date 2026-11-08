# 成本与盈亏平衡

## F2

- **判断**：claim-leaf 的 token 收益是条件性的：证据充分 −91%，不充分 +1.9%，平均 −38%。
- **等级**：`已核`（CAI 一手正文）。
- **条件**：FRAMES；gate hit/miss 由 `p_h` 决定；N=200；token 为相对变化。
- **反例/边界**：平均掩盖两端；miss 高的语料会亏；抽取质量差会抬高 miss。
- **来源**：[CAI 卡](../../../../src/papers/2610.41172-context-as-infrastructure/card.md) · [E-08](../../../conclusions.md)

## F3

- **判断**：盈亏平衡是条件性的：`p_h > 2% + c/(0.929Q)`；证据替换用检索轮次换 token，配对子集时延约 3×。
- **等级**：`已核`（CAI 一手正文）。
- **条件**：无限视野 2.0%；Q=1,000、c=10 → 3.12%；p_h=2.5% 仍亏 5.8 query-equivalent；回本 p_h≈0.43、c=10 → ≈26 问。
- **反例/边界**：有限视野公式依赖 `c` 与 `Q` 的估计；时延硬约束时不应买 token 节省；token 价格下降改变美元账，不改变相对 token 账。
- **来源**：[CAI 卡](../../../../src/papers/2610.41172-context-as-infrastructure/card.md) · [E-14](../../../conclusions.md)
