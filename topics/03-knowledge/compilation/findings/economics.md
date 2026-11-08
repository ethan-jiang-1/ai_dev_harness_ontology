# 成本与盈亏平衡

## F2

- **判断**：claim-leaf 的 token 收益是条件性的：证据充分 −91%，不充分 +1.9%，平均 −38%。
- **等级**：`已核`（CAI 一手正文）。
- **条件**：FRAMES；gate hit/miss 由 `p_h` 决定；N=200；token 为相对变化。E3 的 −52%/−30% 是另一组 arm mean（见 F3），不与这里的 hit/miss 混算。
- **反例/边界**：平均掩盖两端；miss 高的语料会亏；抽取质量差会抬高 miss。
- **来源**：[CAI 卡](../../../../src/papers/2610.41172-context-as-infrastructure/card.md) · [E-08](../../../conclusions.md)

## F3

- **判断**：盈亏平衡是条件性的：`p_h > 2% + c/(0.929Q)`；证据替换用检索轮次换 token，配对子集时延约 3×。
- **等级**：`已核`（CAI 一手正文）。
- **条件**：无限视野 2.0%；Q=1,000、c=10 → 3.12%；p_h=2.5% 仍亏 5.8 query-equivalent；回本示例 p_h≈0.43、c=10 → ≈26 问（0.43 即 43%，是由平均 −38% 反推的 p_h，不是实测计数）。时延 3× 只来自 7 道配对题。E3 读深决策门（独立小模型，不是 `p_h` 证据门）另有 arm mean：有证据 −52%、无证据 −30%；Fig. 2 的 140→30 s 是 gate arm 的均值，不是未编译基线；题数更少，不能与 −91%/−38% 对读。
- **反例/边界**：有限视野公式依赖 `c` 与 `Q` 的估计；时延硬约束时不应买 token 节省；token 价格下降改变美元账，不改变相对 token 账。把 arm mean 当 hit/miss 条件分支、把 140→30 当未编译基线对比，都会高估决策门的收益。
- **来源**：[CAI 卡](../../../../src/papers/2610.41172-context-as-infrastructure/card.md) · [digest](../../../../src/papers/2610.41172-context-as-infrastructure/digest.md) · [E-14](../../../conclusions.md)

## F7

- **判断**：盈亏平衡的不确定性由 miss penalty 主导：miss 端 ±1.5pp 会让 `p_h*` 在 0.4–3.6% 间移动，而 hit 端 ±1.5pp 只动 2.0–2.1%。所以先量 miss，不要先优化 hit。
- **等级**：`已核`（CAI 成本模型的解析推导，非实测）。
- **条件**：模型为 `p_min=2%+c/(0.929Q)`；±1.5pp 是 CAI 成本模型的敏感度设定（[digest](../../../../src/papers/2610.41172-context-as-infrastructure/digest.md) §6.5 转述）。
- **反例/边界**：解析值不是实测；miss 由抽取质量与语料形态决定，企业语料（表格/扫描/行话）会更高；把敏感度当预测区间会高估精度。
- **来源**：[CAI digest](../../../../src/papers/2610.41172-context-as-infrastructure/digest.md) §6.5 · [E-14](../../../conclusions.md)
