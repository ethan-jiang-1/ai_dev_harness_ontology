---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# 4. 边界与反例

> 边界页回答：15 条边界 + 12 条反例里最常被越过的部分。 ｜ 目标：说出这条判断不能证明什么、常见主张在哪被已测反例打掉。

### 4.1 证据边界：15 条边界 + 12 条反例

完整表在 [boundaries.md](../05-evidence/02-boundaries.md)：B1–B15（每条带「挂在哪 / 什么会改变它」）与 [N01–N12 反例集](../05-evidence/02-boundaries.md#0-反例集n-table)（每条带数、条件、O 地址）。这里只留最容易被越过的五条边界：

1. **B1**：强度–覆盖率反向没有被直接测量；直线是 H，矩阵是 D。
2. **B2**：E-01 的 ontology 是 `not measured`；不能写「本体无增益」。
3. **B3**：E-04 撤回（W-03）；「结构贡献未隔离」待新源。
4. **B13**：commit 写路径无实现；E-20 只给否定性证据。
5. **B14**：单来源为主、无独立复现；最高等级是已核。

> 反例集单独看：[N-table](../05-evidence/02-boundaries.md#0-反例集n-table)——12 条「常见主张 × 已测反例」，例如「平均 −38% 可上线」「有引擎就能拦」「审批越多越安全」。

> 每条 E 的限定在 [evidence-ledger.md](../05-evidence/01-ledger.md)；更细的逐条解释见 [附录 §3.7](../05-appendix-constraint-spectrum.md#37-本章不能证明什么)。
