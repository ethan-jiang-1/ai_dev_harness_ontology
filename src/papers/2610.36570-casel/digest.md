---
status: draft
updated: 2026-11-08
quality: B
based_on: card.md
claims: [01-L4, 01-L5]
---

# CASEL：不是「拦不拦」，而是「用哪种审查」

> 这篇消化不假设你读过论文。先讲清「后果感知的运行时分配」是什么，再看它在模拟里的收益、代价、前沿与边界。

## 0. 三句话

1. **它问什么**：两个动作同样 20% 失败概率，读操作重试很便宜，不可逆转账很贵；能不能按「后果 × 可逆性」分配不同强度的审查，而不是一刀切？
2. **它怎么做**：在 agent 与工具执行器之间加一层控制器，估计失败概率、后果、可逆性、歧义、证据新鲜度；在 direct / verify / sandbox / clarify / approve / abstain 六种模式里按代价选一个。
3. **它发现什么**：模拟中把有害副作用轨迹（HSR）从 14.75% 降到 7.02%，但**最低 HSR 不是 CASEL**（Risk-Menu 5.82%）；CASEL 的价值是「相近 harm、审批少约 30%」。轨迹风险总账反而会反噬（11.82%）。

## 1. 它解决什么问题

### 1.1 背景

长程工具 agent 会在外部系统里连续动作：查、改、转账、下单、删数据。大多数护栏只按「不确定性」排序，或者只按「是否 mutating」粗分。问题是：

- **不确定性不够。** 同样 20% 失败概率，读操作重试便宜，不可逆转账很贵。
- **mutation 也不够。** 可逆的编辑和不可逆的提交都是「mutation」，代价完全不同。
- **审查有成本。** 每次都 verify/sandbox/approve，会把系统拖慢、把人工拖垮。

### 1.2 论文的立场

审查强度应该随**后果加权风险**缩放，干预方式应该匹配**可逆性**；直接执行应该被建模为**选择性预测**（selective prediction），而不是「模型说行就行」。

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **p̂（failure probability）** | 校准后的失败概率。 |
| **ĉ（consequence）** | 这个动作失败时的后果大小；由 per-tool severity × scope 估计。 |
| **ρ（reversibility）** | read / reversible / compensable / irreversible；决定哪些干预可行。 |
| **g（ambiguity）** | 用户意图缺失/歧义；不是「模型不确定」。 |
| **d（staleness）** | 证据是否过期。 |
| **r̂ = p̂ĉ** | 后果加权风险；排序/路由的核心。 |
| **六模式** | direct / verify / sandbox / clarify / approve / abstain。 |
| **J(m)** | 模式代价：`γ_m·r̂ + λk(m) + μq(m)`。 |
| **γ_m** | 干预后的残余失败比例（effectiveness）；**本文是假设，不是测量**。 |
| **HSR** | harmful-side-effect trajectory rate：至少一个真后果 ≥0.45 的失败动作的轨迹比例。 |
| **MNH** | mean normalized harm：轨迹的归一化伤害均值。 |
| **selective prediction** | 只在「有把握」的样本上直接执行；其余转审查。 |
| **trajectory ledger** | 用累计风险预算限制整条轨迹的伤害。 |

## 3. 它怎么做

### 3.1 位置

运行时层，位于任意 base agent 与工具执行器之间；每个 proposed tool call 做一次路由决策。

### 3.2 五个信号

- `p̂`：raw score 用 isotonic / temperature scaling 校准。
- `ĉ = clip(c_base(z_t) · M_scope(θ_t,h_t), 0,1)`；`c_base` 是审计过的 per-tool severity（写权限、特权、敏感度、金额），`M_scope` 是幅度因子。
- `ρ`：read / reversible / compensable / irreversible；它改变**可行模式集**，不是缩放 `ĉ`。
- `g`：缺失意图；`d`：证据过期。

### 3.3 六种模式与代价

| 模式 | 做什么 | 何时可行 |
|---|---|---|
| direct | 直接执行 | 默认可行 |
| verify | 先跑 checker | 默认可行 |
| sandbox | 在隔离环境/dry-run 执行 | 只对 reversible mutation |
| clarify | 问用户 | 默认可行 |
| approve | 人工审批 | 只对 compensable/irreversible |
| abstain | 拒绝 | 默认可行（本文未启用） |

`J(m)=γ_m·p̂ĉ + λk(m)+μq(m)`；选可行模式里 J 最小的。`k` 是算力成本，`q` 是交互成本。

### 3.4 选择性风险

- 直接执行集 `A_τ={S≤τ}`；目标：最大化 coverage s.t. selective risk ≤ ε。
- 用 Hoeffding + union bound 给有限样本阈值规则；Proposition 1 保证 i.i.d. calibration records 下真实风险 ≤ ε。
- **trajectory ledger**：`H_t=Σ D_i r̄_i ≤ B_H`；Proposition 2 只在 `r̄` 每步上界真实条件风险时成立——calibrated point estimate 不满足，且被干预动作的 residual harm 不在账本内。

### 3.5 一个具体例子

同一个 `p̂=0.20`：
- 读操作，`ĉ=0.05` → `r̂=0.010`；J：direct 0.010、verify 0.024 → **direct**。
- 可逆编辑，`ĉ=0.40` → `r̂=0.080`；J：direct 0.080、verify 0.054、sandbox 0.045 → **sandbox**。
- 不可逆转账，`ĉ=0.90` → `r̂=0.180`；J：direct 0.180、verify 0.096、approve 0.061 → **approve**。

**可逆性决定可行模式，后果决定代价权重**——这两个旋钮不能合并成一个「风险分」。

## 4. 结果：数字与条件

### 4.1 实验设置

- **受控模拟**：20 seeds；每 seed 40,000 calibration + 6,000 trajectories × 20 actions = 120,000 test actions。
- 动作分布：58% read-only、28% reversible、14% irreversible。
- 所有方法同一 intervention menu、同一 compute cost（0.486）。
- γ_m：direct 1.00 / verify 0.42 / sandbox 0.15 / approve 0.04；k：0/1.0/1.6/2.2；q：0/0/0.04/0.65；λ:μ=0.02:0.015。

### 4.2 主结果

| 方法 | task success | HSR | MNH | approvals |
|---|---|---|---|---|
| Base | 29.48% | 32.76% | 0.428 | 0% |
| Always-Verify | 47.01% | 15.47% | 0.180 | — |
| Uncertainty-Menu（p̂） | 48.79% | 14.75% | 0.184 | 6.9% |
| Risk-Menu（p̂ĉ） | — | **5.82%** | 0.120 | 12.6% |
| Consequence-Menu | — | 4.38% | 0.136 | 13.8% |
| **CASEL** | **47.01%** | **7.02%** | **0.123** | **8.7%** |
| CASEL-NoRev | 46.56% | 15.53% | 0.194 | 0.0% |
| CASEL+Budget | — | 11.82% | 0.167 | — |
| CASEL-Uncal | — | 8.22% | 0.129 | — |

- CASEL 相对 Uncertainty-Menu：HSR **−7.73 pp**（paired [−7.87,−7.60]）。
- **CASEL 不是最低 HSR**；Risk-Menu 5.82% 更低，但审批 12.6% vs CASEL 8.7%。CASEL 用约 30% 更少审批达到相近 harm，task success 还高一点。
- 去掉 reversibility routing：HSR 回到 15.53%，几乎等于 uncertainty gate。
- 轨迹总账：11.82%，比 CASEL 高 4.8 点；54% 的直接执行步骤 `p_t c_t > r̄_t`，ledger 前提失败。
- 未校准：8.22% vs 7.02%；ECE 降 94.5% 才让阈值/预算有意义。
- ambiguity stress：10% 动作缺意图；CASEL clarify 9.8%，precision 94%、recall 92%，HSR 19.1→8.4%。

> 出处：Table 2；§VI-B, p.4–5；Fig. 4。

## 5. 这些数字不能说明什么

1. **不是部署效果。** 这是模拟；γ_m、k、q 都是假设；真实系统的干预效果/成本不同。
2. **不是「CASEL 最优」。** 最低 HSR 是 Risk-Menu/Consequence-Menu；CASEL 的位置是 harm–approval 前沿。
3. **task success 与 HSR 反向。** CASEL HSR 低 7.7 点，但 task success 低 1.79 点；只报一个会得出相反结论。
4. **审批疲劳未建模。** approvals 只是比例；真实审批的时间/信任成本没进 J(m)。
5. **单步决策。** 多步组合后果、跨轨迹依赖未覆盖。
6. **abstain/staleness 未启用。** 完整六模式没有全部验证。

## 6. 工程上怎么用

### 6.1 复刻顺序

1. **先把动作分四类可逆性。** read / reversible / compensable / irreversible；决定哪些干预可行。
2. **给每个工具一个审计过的后果基线。** 写权限、特权、敏感度、金额；乘 scope。
3. **校准失败概率。** isotonic/temperature scaling；不校准 HSR 会高 1.2 点。
4. **按 `p̂ĉ` 排序，不只按 `p̂`。** product 的 selective-risk AUC 比 uncertainty 低 49.2%。
5. **按 `J(m)` 选模式。** 没有 γ_m 数据就不要假装能算 J(m)。
6. **歧义走 clarify。** 缺失意图不是 verify 能解决的。
7. **不要用轨迹总账。** 它会反噬；要记账，只对不可逆动作记。
8. **按 harm–approval–cost 前沿选点。** 不要只报一个 HSR。
9. **同时报 task success 与 HSR。**

### 6.2 成本与使能

| 成本 | 一次性/每次 | 说明 |
|---|---|---|
| 校准集 | 一次性/周期 | 带标签的失败样本；isotonic/temperature scaling |
| per-tool consequence 元数据 | 一次性 | 写权限、特权、敏感度、金额；要审计 |
| 干预能力 | 集成一次性 | verify checker、sandbox/dry-run、approval 队列 |
| 每次调用 | 每次 | p̂/ĉ 估计 + J(m)；轻量 |
| 审批 | 每次 approve | 真实人力成本未建模；8.7–13.8% |
| 维护 | 工具/策略变更 | consequence 基线、γ_m、阈值更新 |

**使能条件**：可校准失败分数；可审计工具元数据；sandbox/approval 基础设施；能承受审批量。

### 6.3 何时用 / 何时别用

**用**：长程工具 agent；动作后果差异大；有可审计 per-tool severity；有审批/沙箱能力；能校准失败概率。

**别用**：没有 γ_m 数据；审批能力不足；动作后果不可估；需要形式保证；单步短任务。

## 7. 质量与边界

- **证据类型**：实证·模拟（受控但非部署）。
- **强项**：对照干净；成本/审批/覆盖都报；有负结果（ledger）；有 misspecification 压力测试；诚实声明「effectiveness assumed」。
- **主要威胁**：模拟的 γ_m/k/q 是假设；审批疲劳未建模；abstain/staleness 未启用；单步决策；task success 与 HSR 反向。
- **`quality: B`**：受控模拟很强，但不是部署；核心机制依赖未测量的 γ_m。

## 8. 与仓库判断的关系

- **01-L4**：把干预拆成多模式比单一剪枝更省代价（模拟）。
- **01-L5**：审批量是护栏的隐性成本（CASEL 8.7% vs Risk-Menu 12.6%）。
- **E-15（已核）**：护栏评估应报 harm–approval–cost 前沿，不是单一 HSR。
- **P3**：不存在单一向优的分配；harm/approval/task success 是三个方向。
- **C-03**：只用 task success 会认为 CASEL 更差（47.01 vs 48.79），但它把 HSR 从 14.75 降到 7.02。

## 9. 还没解决 / 下一步

- **γ_m 实测**：verify/sandbox/approve 在真实工具上各降低多少失败率？
- **审批真实成本**：时间、疲劳、信任怎么进 J(m)？
- **多步组合后果**：单步 c 小但组合不可逆，怎么算？
- **ledger 替代形式**：只对不可逆动作记账？
- **真实 τ²-bench/AgentDojo 上排序是否保持？**
- **task success 与 HSR 的取舍由谁定？**

## 10. 原文

- arXiv:2610.36570
- PDF：`src/papers/2610.36570-casel/`
- 代码/数据：论文未给公开仓库。
