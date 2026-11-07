---
status: draft
updated: 2026-11-07
quality: B
based_on: card.md
claims: [01-L4, 01-L5]
---

# CASEL · 消化

> 事实、数字、页码回 [card.md](./card.md)。这里只写**我们怎么用**、值不值得、哪里会坏。

## 工程思路

**要做「执行前分配审查」，按这个顺序：**

1. **先把动作分成四类可逆性。** read / reversible / compensable / irreversible；它决定**哪些干预可行**，不是决定风险分。
2. **再给每个工具一个审计过的后果基线。** write 权限、特权、数据敏感度、金额；乘上 scope（记录数、金额、回滚成本）。不要让模型自由估后果。
3. **校准失败概率。** raw score 用 isotonic/temperature scaling 校准；不校准的 HSR 会高 1.2 点（8.22 vs 7.02）。
4. **按 `p̂ĉ` 排序，而不是只按 `p̂`。** 在同等 coverage 下，product 的 selective-risk AUC 比 uncertainty 低 49.2%。
5. **按 `J(m)=γ_m·r̂+λk+μq` 选模式。** γ_m 是干预后的残余失败比例；k/q 是算力/交互成本。**没有 γ_m 数据就不要假装能算 J(m)**。
6. **歧义走 clarify，不要走 verify。** 缺失意图不是「多试一次」能解决的；CASEL 在 10% 歧义动作上 clarify 9.8%，precision 94%、recall 92%，HSR 19.1→8.4%。
7. **不要用 trajectory 总账。** 它把低风险动作留到后期再升级，反而抬高 HSR（11.82 vs 7.02）；且前提 `r̄` 上界真值在 54% 步上失败。要记账，只对不可逆动作记。
8. **按前端比较，不要只报一个 HSR。** CASEL 的 HSR 不是最低（5.82 的 Risk-Menu 更低），但审批少 30%；用 harm–approval–cost 前沿选点。
9. **同时报 task success 与 HSR。** 两者可以反向：CASEL HSR 低 7.7 点，但 task success 低 1.79 点。

## 实用意义

它解决的操作问题：

- **「同一个 20% 失败概率，读操作和转账不能同样处理。」** → consequence × reversibility 路由。
- **「审批量太大，团队被淹没。」** → 按后果分配，而不是全量人工；CASEL 8.7% approvals vs Risk-Menu 12.6%。
- **「沙箱只能用于可逆变更，不可逆转账不能沙箱。」** → 可行性由可逆性决定，不是由风险分决定。
- **「歧义动作反复验证也没用。」** → clarify 分支，直接问用户。
- **「想用轨迹风险预算控制总伤害。」** → 模拟显示会反噬；不要用总账。
- **「不知道该优化 HSR 还是 task success。」** → 两个都报，按业务定 front。

**何时用**：长程工具 agent；动作后果差异大；有可审计的 per-tool severity；有审批/沙箱能力；能校准失败概率。

**何时别用**：没有 γ_m 数据；审批能力不足；动作后果不可估；需要形式保证；单步短任务（收益小）。

## 质量评估

- **证据类型**：实证·模拟（`已核`，一手正文；受控但非部署）。
- **样本与对照**：20 seeds；120,000 test actions；所有方法同 menu、同 cost；10 个对照/消融；paired tests；stress tests。
- **优点**：对照干净；成本/审批/覆盖都报；有负结果（ledger）；有 misspecification 压力测试；诚实声明「effectiveness assumed」。
- **主要威胁**：模拟的 γ_m/k/q 是假设；审批疲劳未建模；abstain/staleness 未启用；单步决策，不覆盖多步组合后果；task success 与 HSR 反向。
- **`quality: B` 理由**：受控模拟很强，但不是部署；核心机制依赖未测量的 γ_m，外部效度有限。

## 洞察

1. **「只按不确定性排序」是错的。** 同等成本下 HSR 14.75% vs 7.02%；把后果乘进去，AUC 降 49.2%。`已核`（模拟）
2. **CASEL 的价值不是「最低 harm」，是「harm–approval 前沿」。** Risk-Menu HSR 5.82% 更低，但审批 12.6% vs 8.7%；CASEL 用约 30% 更少审批达到相近 harm，task success 还高一点。`已核`
3. **可逆性路由贡献了大部分增益。** 去掉 reversibility routing，HSR 回到 15.53%，几乎等于 uncertainty gate。**「能不能撤销」比「风险多大」更能决定干预方式。** `已核`
4. **轨迹总账会反噬。** CASEL+Budget HSR 11.82%，比 CASEL 高 4.8 点；它把低风险动作留到后期升级，且 `r̄` 不满足上界前提（54% 步失败）。`已核`
5. **校准是前置条件。** 未校准的 CASEL HSR 8.22% vs 7.02%；ECE 降 94.5% 才让阈值/预算有意义。`已核`
6. **歧义要靠澄清，不靠验证。** 10% 动作有缺失意图；verify/sandbox 都留错，approve 减半，clarify 去掉 95%。`已核`
7. **指标会打架。** HSR 降 7.7 点，task success 降 1.79 点；只报一个会得出相反结论。`已核`
8. **「effectiveness assumed」是全文最大的洞。** γ_m 是假设常数；真实系统里 verify/sandbox/approve 的效果必须实测，否则 J(m) 只是算术。`已核`（作者自述）

## 成本与使能条件

| 成本 | 一次性 / 每次 | 说明 |
|---|---|---|
| 校准集 | 一次性/周期 | 需要带标签的失败样本；isotonic/temperature scaling |
| per-tool consequence 元数据 | 一次性 | 写权限、特权、敏感度、金额；要审计 |
| 干预能力 | 集成一次性 | verify checker、sandbox/dry-run、approval 队列 |
| 每次调用 | 每次 | p̂/ĉ 估计 + J(m) 计算；轻量 |
| 审批 | 每次 approve | 真实人力成本未建模；8.7–13.8% approvals |
| 维护 | 工具/策略变更 | consequence 基线、γ_m、阈值要更新 |

**使能条件**：可校准的失败分数；可审计的工具元数据；sandbox/approval 基础设施；能承受审批量。

**2022 年做会卡在哪**：长程工具 agent 不成熟；没有 τ²-bench/AgentDojo 这类状态化工具环境；校准与 selective prediction 工具链不普及。

**反向条件**：没有 γ_m 数据；审批能力不足；后果不可估；动作组合不可逆；需要形式保证。

## 与现有判断的关系

| 关联 | 关系 |
|---|---|
| **01-L4** | 支撑「把干预拆成多模式比单一剪枝更省代价」：六模式 + 按后果选。 |
| **01-L5** | 支撑「审批量是护栏的隐性成本」：CASEL 8.7% vs Risk-Menu 12.6% vs Consequence 13.8%。 |
| **P3** | 强支撑：不存在单一向优的分配；harm / approval / task success 是三个方向。 |
| **C-03** | 又一例：只用 task success 会认为 CASEL 更差（47.01 vs 48.79），但它把 HSR 从 14.75 降到 7.02。 |
| [action-gate](../../../topics/01-constraint/action-gate/README.md) | 核心文献；机制细节回 card。 |
| [POLAR](../2610.08082-polar/digest.md) | 对比：POLAR 是二值 veto，CASEL 是多模式分配；两者都说明「可逆性」是核心变量。 |

## 不可迁移

- 模拟的 γ_m/k/q 是假设；真实系统的干预效果与成本不同。
- 单步决策；多步组合后果、跨轨迹依赖未覆盖。
- 审批疲劳/信任成本未建模；approvals 只是比例。
- abstain 与 staleness 分支未启用；完整六模式未验证。
- 任务分布（58% read-only / 28% reversible / 14% irreversible）是模拟设定，真实 agent 可能不同。

## 开放问题

- γ_m 的真实值：verify/sandbox/approve 在真实工具上各降低多少失败率？
- 审批的真实成本（时间、疲劳、信任）怎么进 J(m)？8.7% vs 12.6% 的差异值多少？
- 多步组合后果：单步 c 小但组合不可逆，怎么算？
- trajectory ledger 的替代形式：只对不可逆动作记账？
- task success 与 HSR 的取舍由谁定？业务风险偏好如何进目标函数？
- 在真实 τ²-bench/AgentDojo 上，CASEL 的排序是否保持？
