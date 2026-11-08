# 动作前拦截 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 问题

工具调用 agent 获得写权限后，最危险的失败不是答错，而是**不可恢复的动作**。动作前是唯一能阻止副作用的位置。

## 机制一：可逆性门（POLAR）

### 两层本体

| 层 | 内容 | 何时有 |
|---|---|---|
| Layer A | 静态动作本体：每个 mutating tool 的类型化逆关系 T1–T5，带 curator 权重 | 域级，手写 |
| Layer B | 状态投影：`slot(entity,id)=value`，从真实 DB + 已执行工具重建 | 每轮 |

| tier | 关系 | 每步 φ | 含义 |
|---|---|---|---|
| T1 | `inverse_of` | `w` | 有精确逆操作 |
| T2 | `bounded_reversibility` | `w · 1[Bound]` | 在边界内可逆 |
| T3 | `compensates` | `w · (1−w_loss)` | 可补偿，但有损 |
| T4 | `irreversibly_consumes` | 0 | 不可逆消费 |
| T5 | `external_side_effect` | 0 | 外部副作用，fail-closed |

**反向搜索**：从最近的动作往回找 undo 边，组合候选逆序列 π；成功则 `φ(π)=min φ(u)`（最弱一步），失败则报告第一个不可执行步骤。阈值 τ=0.80；低于阈值或没有完整 π → Veto。

**判定与执行分离**：APPROVE / VETO / ESCALATE 是 DecisionPolicy，不是本体的一部分。被评估的 wrapper **不模拟完整 post-action state s′**；只对可用 Layer B 当前投影检查。

## 机制二：多模式分配（CASEL）

不是二值 veto，而是六选一：direct / verify / sandbox / clarify / approve / abstain。

- 信号：`p̂`（校准失败率）、`ĉ`（后果）、`ρ`（可逆性）、`g`（歧义）、`d`（证据新鲜度）。
- 代价：`J(m)=γ_m·p̂ĉ + λk(m) + μq(m)`；`γ_m` 是干预后的残余失败比例。
- 可行性：sandbox 只对 reversible mutation/dry-run；approve 只对 compensable/irreversible。
- 选择性风险：直接执行集 `A_τ={S≤τ}`；Hoeffding + union bound 给有限样本阈值。
- 轨迹总账：`H_t=Σ D_i r̄_i ≤ B_H`；只在 `r̄` 每步上界真实条件风险时成立。

## 失效模式

- **T1-only ≈ blanket veto。** 结构反向组合的贡献未被隔离。
- **可逆性 ≠ 安全性 ≠ 授权。** 外部副作用可能完全合法；零售退货会被误拦。
- **漏掉一条不可逆关系 → false approval。** 本体错误是 fail-open 的。
- **判据依赖运行时状态。** 静态本体不够；需要 Layer B。
- **阈值错置。** airline 在 0.80 只保留 36.6%，retail 100%。
- **只判不记。** 剪枝事件不记录，false-veto 无法算。
- **不验证逆执行。** 「有逆序列」不等于「恢复会成功」。
- **CASEL 的干预有效性是假设。** `γ_m` 不是测量；审批疲劳未建模。

## 与本体 / 回路的关系

本体在动作前以**类型化逆关系**出现；约束强度强（能阻止副作用），覆盖率窄（只覆盖 mutating tools）。被违反时，系统能报出哪条边缺失/哪个 bound 不满足/哪一步 φ=0；但无法证明语义真值或授权。

## 关联

- [POLAR 卡](../../../src/papers/2610.08082-polar/card.md) · [digest](../../../src/papers/2610.08082-polar/digest.md)
- [CASEL 卡](../../../src/papers/2610.36570-casel/card.md) · [digest](../../../src/papers/2610.36570-casel/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
