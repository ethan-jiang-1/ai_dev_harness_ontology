# 动作前拦截 · 未发现与下一步

> `G` = gap（还没站住的判断）；`N` = next（下一步看什么）。稳定判断回 [findings](./findings.md)。

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | False-veto / false-defer 率 | 护栏的隐性成本；retail 回退可能主要是误拦 | 对 1,745 条 blocked decisions 人工标注「本可合法执行」 | POLAR 附录 B.3；CASEL 审批日志 | 高 |
| G2 | 复合动作的可逆性 | 单步都可逆，组合可能不可逆；当前只看单步/当前 state | 多步动作的逆序列组合 + 状态模拟 | POLAR 后续；规划/事务补偿（Saga） | 高 |
| G3 | T1-only 与 full 的配对差异 | 决定「结构」是否真的贡献，还是保守拒绝 | 同一 baseline、同一轨迹的配对实验 | POLAR tier ablation | 高 |
| G4 | 真实部署的审批成本/疲劳 | CASEL 的 8.7% vs 12.6% 只是模拟 | 真实 approval 队列的时间/信任测量 | CASEL 部署路径；人因研究 | 中 |
| G5 | 意图/授权层怎么接 | 可逆性不能单独裁决合法用户意图 | 可逆性门 + 用户确认 + 策略引擎的组合 | retail、客服、金融场景 | 中 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变哪条 F/G | 成本 |
|---|---|---|---|---|
| N1 | T1-only vs full 的配对复现 | POLAR 附录；`solver-like`? 不；查 "tier ablation reversible gate" | F3 / G3 | 中 |
| N2 | 动态/不确定性感知门 | `uncertainty-aware guardrail tool calling`；POLAR future work | F1/F2 / G1 | 中 |
| N3 | CASEL 的 γ_m 实测 | `consequence-aware selective execution deployment`；CASEL 作者后续 | F5/F6 / G4 | 高 |
| N4 | 审批疲劳/信任成本 | `human approval fatigue agent guardrail` | G4 | 中 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-08 | 本地 01 派深读（POLAR/CASEL） | F1–F6 成形；G1–G5 明确 | 先做 G1/G3 的标注/复现 |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| POLAR 后续 / 动态门 | 可能解决强模型回退 | 待扫描 | N2 |
| CASEL 部署版 | γ_m/审批成本的实测 | 待扫描 | N3 |
| Saga/事务补偿线 | 复合可逆性 | 待扫描 | G2 |
