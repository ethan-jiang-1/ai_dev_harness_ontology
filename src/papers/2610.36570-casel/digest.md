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
3. **它发现什么**：模拟中把有害副作用轨迹（HSR）从 14.75% 降到 7.02%，但**最低 HSR 不是 CASEL**（Consequence-Menu 4.38%，Risk-Menu 5.82%）；CASEL 的价值是「相近 harm、审批少约 30%」。轨迹风险总账在 harm–compute 面被支配，但在低审批端是前沿点（11.82%，approvals 4.3%）。

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
| **ECE** | Expected Calibration Error；越低越校准。 |
| **AUC** | 排序质量；本文 selective-risk AUC 越低越好。 |
| **compensable** | 可补偿但非精确逆；与 reversible 不同，approve 只对它/irreversible 开放。 |
| **coverage** | 直接执行的动作比例；selective risk 是 coverage 内的条件风险。 |
| **S** | selective-risk 分数；A_τ={S≤τ} 是直接执行集。 |
| **checker** | verify 模式调用的验证器。 |

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
| sandbox | 在隔离环境/dry-run 执行 | 只对 reversible mutation 或可 dry-run 的接口；不对 irreversible commitment |
| clarify | 问用户 | 默认可行 |
| approve | 人工审批 | 只对 compensable/irreversible；模拟里仅 irreversible 且 **ĉ≥0.55** 开放 |
| abstain | 拒绝 | 默认可行（本文未启用） |

`J(m)=γ_m·p̂ĉ + λk(m)+μq(m)`；选可行模式里 J 最小的。`k` 是算力成本，`q` 是交互成本。但 **g>τ_g（0.2）先走 clarify、d>τ_d 先走 verify**，在 J(m) 之前；不是所有模式都由 J 选。**主表 CASEL 的 7.02% HSR / 8.7% approvals 是在阈值 τ̂=∞（阈值关闭）下得到的**；阈值验证在 §VI-E，不在主表。

### 3.4 选择性风险

- 直接执行集 `A_τ={S≤τ}`；目标：最大化 coverage s.t. selective risk ≤ ε。
- 用 Hoeffding + union bound 给有限样本阈值规则；Proposition 1 要求校准记录 i.i.d. **且与拟合 f_cal 的数据 disjoint**，并因轨迹内动作相关而 **one record per trajectory**。
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
- **不是所有方法同 menu/cost**：Mutation-Gated **以下**同 compute 0.486；Mutation-Gated 自身 cost 0.420；Base/Always-Verify 分别是 0.000/1.000，menu 为 —/verify。
- γ_m：direct 1.00 / verify 0.42 / sandbox 0.15 / approve 0.04；k：0/1.0/1.6/2.2；q：0/0/0.04/0.65；λ:μ=0.02:0.015。

### 4.2 主结果

| 方法 | task success | HSR | MNH | approvals |
|---|---|---|---|---|
| Base | 29.48% | 32.76% | 0.428 | 0% |
| Always-Verify | **58.81%** | 15.47% | 0.180 | — |
| Uncertainty-Menu（p̂） | 48.79% | 14.75% | 0.184 | 6.9% |
| Risk-Menu（p̂ĉ） | 46.26% | **5.82%** | 0.120 | 12.6% |
| Consequence-Menu | 43.54% | 4.38% | 0.136 | 13.8% |
| **CASEL** | **47.01%** | **7.02%** | **0.123** | **8.7%** |
| CASEL-NoRev | 46.56% | 15.53% | 0.194 | 0.0% |
| CASEL+Budget | 45.82% | 11.82% | 0.167 | 4.3% |
| CASEL-Uncal | 47.83% | 8.22% | 0.129 | 8.4% |

- CASEL 相对 Uncertainty-Menu：HSR **−7.73 pp**（paired 95% CI [−7.87,−7.60]）。
- **CASEL 不是最低 HSR**；Risk-Menu 5.82% 更低，但审批 12.6% vs CASEL 8.7%。CASEL 用约 30% 更少审批达到相近 harm，task success 还高一点。
- **CASEL-NoRev = verify-only**（只保留 verification，不开放 sandbox/approve；Table 2 menu=verify、approvals 0.0%、coverage 51.4%）；HSR 回到 15.53%。15.53% 不能只归因给「可逆性路由」，它同时去掉了 sandbox/approve 多模式。
- 轨迹总账：11.82%，比 CASEL 高 4.8 点；54% 的直接执行步骤 `p_t c_t > r̄_t`，ledger 前提失败。**但它在 harm–approval 面上是一个低审批端点（4.3% approvals），与 CASEL 曲线相交；不是「一律禁用」，而是被 harm–compute 面支配。**
- 未校准：8.22% vs 7.02%；作者把「ECE 降 94.5%」作为阈值/预算的设计前提，不是跑过未校准阈值规则的实验结果。
- ambiguity stress：10% 动作缺意图；CASEL clarify 9.8%，precision 94%、recall 92%，HSR 19.1→8.4%。

> 出处：Table 2；§VI-B（主表）、§VI-D（NoRev/ledger）、§VI-E（ambiguity/阈值）；Fig. 4。

### 4.3 为什么 CASEL 不是最低 HSR

- **Risk-Menu** 只按 `p̂ĉ` 排序；它的直接执行覆盖 74.2%（CASEL 69.1%），总审查更少，但人工审批更多（12.6% vs 8.7%）。HSR 5.82% 低于 CASEL，但不是最低。
- **CASEL** 的 `J(m)` 只含审查成本（γ_m·p̂ĉ + λk + μq），**不含 task success**；task success 是评估指标。它在「相近 harm」下换更少审批（8.7%）；task success 比 Uncertainty-Menu 低 1.78 点（表值相减；正文写 1.79，取整口径不同）。
- **Consequence-Menu** 更低 HSR（4.38%），但审批 13.8%，task success 也更低。
- 所以「最低 HSR」不是唯一目标；**harm–approval–cost 前沿**才是。CASEL 的位置是「审批少约 30%、harm 相近」，不是「harm 最低」。

## 5. 这些数字不能说明什么

1. **不是部署效果。** 这是模拟；γ_m、k、q 都是假设；真实系统的干预效果/成本不同。
2. **不是「CASEL 最优」。** 最低 HSR 是 Consequence-Menu 4.38%；Risk-Menu 5.82% 次低；CASEL 7.02% 的位置是 harm–approval 前沿。
3. **task success 与 HSR 反向。** CASEL HSR 低 7.7 点，但 task success 低 1.78 点；只报一个会得出相反结论。
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
7. **轨迹总账不是默认。** full ledger 在 harm–compute 面被支配，但在低审批端（4.3% approvals / 11.82% HSR）是前沿点；「只对不可逆动作记账」未验证，不要写成结论。
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

### 6.4 最小落地清单

1. **动作分四类可逆性**：read / reversible / compensable / irreversible；决定哪些干预可行。
2. **给每个工具审计过的后果基线**：写权限、特权、敏感度、金额；乘 scope。
3. **校准失败概率**：isotonic/temperature scaling；不校准 HSR 会高 1.2 点。
4. **按 `p̂ĉ` 排序**，不只按 `p̂`；product 的 selective-risk AUC 低 49.2%。
5. **按 `J(m)` 选模式**；没有 γ_m 数据就不要假装能算 J(m)。
6. **歧义走 clarify**；缺失意图不是 verify 能解决的。
7. **轨迹总账不是默认**；full ledger 在 harm–compute 面被支配，但在低审批端是前沿点（4.3% approvals / 11.82% HSR）；「只对不可逆动作记账」未验证。
8. **按 harm–approval–cost 前沿选点**，同时报 task success 与 HSR；「不校准 HSR 高 1.2 点」「AUC 低 49.2%」都是模拟条件，不是通用规律。

## 6.5 工程配方（E3）

### 接口

- **位置**：agent 与工具执行器之间；可选 MCP proxy、pre-execution hook、policy engine（论文 §VII 给了三选项，均不需重训）。
- **输入**：proposed tool call、tool schema、user context、state/evidence 时间戳；**输出**：`{mode, p̂, ĉ, ρ, g, d, J(m), reason}`。
- **p̂ 来源**：策略模型自评分或独立校准分类器；必须校准（isotonic/temperature scaling），否则阈值/账本无意义。
- **执行**：direct/verify/sandbox/clarify/approve/abstain；verify 调 checker；sandbox 需可回滚/dry-run 接口；approve 只对 compensable/irreversible；abstain 可关。
- **日志**：每个 call 记录动作、可逆性、c_base、p̂、决策、审批人/时间、是否回滚；没有日志就算不出 false-veto/审批成本。

### 参数标定

- `γ_m`：干预后的残余失败比例；论文是假设值。工程上在 trajectory-disjoint 的历史轨迹上回放 verify/sandbox/approve，估点估计 + CI；没有 γ_m 不要算 J(m)。
- `k`（算力）、`q`（交互）：从部署自身成本读；论文的 0/1.0/1.6/2.2 与 0/0/0.04/0.65 是模拟值。
- `λ:μ=0.02:0.015`、`τ_g=0.2`、approve `ĉ≥0.55` 是模拟配置；换域要重新标定，不能照搬。
- 阈值规则 Eq(5)：40,000 条校准轨迹、20 点网格、δ=0.1；ε=0.014 时 20/20 seed 绑定（coverage 62.3%、risk 0.0035）；160,000 条时 ε=0.009 才可认证。工程上先看标注量够不够。
- **校准记录必须与拟合 f_cal 的数据 disjoint，且 one record per trajectory**；否则 Prop 1 不成立。

### 数据契约

- 校准集：带标签的失败样本；失败定义、标注人、分歧处理、样本量-精度关系要写死。**最小协议**：2,000–10,000 条轨迹、每条轨迹一个记录；20% 双标，κ≥0.6；分歧由第三人裁决；每季度重标；没有这个量就不要用 Eq(5) 认证。
- 动作混合：论文 58% read-only / 28% reversible / 14% irreversible；自己的流量要先统计，偏离会改变 approvals/HSR。
- 不可逆长尾要**过采样**；否则 14% 里的高风险动作在测试集太少。
- `c_base`：per-tool severity（写权限/特权/敏感度/金额）× scope；论文没有 rubric。**可抄的锚点**：read-only 搜索 0.05；可逆编辑 0.4；不可逆转账/对外发送 0.9；删除唯一副本 1.0。粒度先 per-tool，金额/对象敏感的工具再 per-arg；评审人=工具 owner，季度复审。

### 成本

- 论文无金额/人时；只给 compute 0.486 与 approvals 8.7–13.8%。
- 建设：控制器 + 校准 + c_base 审计 + sandbox/approval 集成；按 2–4 人周估（`推测`）。
- 运行：p̂/ĉ/J(m) 计算轻量；approve 的人力是主成本；sandbox 的算力另计。
- 维护：γ_m/k/q/阈值随工具/流量变化重标；c_base 随工具变更复审。

### stop condition

- 上线前：γ_verify 的 CI 宽到无法区分 direct/verify 的 J 差 → 只上静态 p̂ĉ gate，不做多模式。
- 校准量不足以把 γ_verify 压到 ±3pp → 停，先补标注。
- 运行中：审批率 > 业务上限（例如 >15%）或 false-veto 投诉超阈值 → 降级到 always-verify/静态 gate，或关闭。
- p̂ĉ 的 selective-risk AUC 未显著低于 p̂ → 机制不迁移，停。

### 替代方案

- 每个替代方案给一行同口径：TCO / 年省伤害 / 审批率 / task success / 硬约束。静态 p̂ĉ gate + 仅 mutating 审批；Always-Verify；纯人工复核；不上护栏。
- 论文模拟里比了 Risk/Consequence/Always-Verify，但没与 REFLEX/CA2I 或纯人工比；build/buy 边界要自己补。

### 失败模式

- γ_m 用假设值当测量；c_base 拍脑袋；审批疲劳未建模；abstain/staleness 未启用；单步决策不覆盖多步组合。
- 主表 τ=∞，阈值规则另测；不要把 7.02% 当“开了阈值”的结果。
- NoRev 是 verify-only，不是“去掉可逆性路由”。

### 第一个 sprint

2 周、单仓库单工具集、**只记日志不接护栏**：

1. 在 MCP proxy/pre-execution hook 记录 proposed call、reversibility、c_base 候选、p̂ 候选、决策、审批/回滚。
2. 统计真实动作混合，和论文 58/28/14 对比；偏离大就重估。
3. 在已有 verify 分支回放，给 verify 打「是否抓到真实缺陷」标签，估 `γ_verify±CI`；sandbox/approve 没基础设施就记 N/A。
4. 离线画 `p̂ vs ĉ vs p̂ĉ` 的 coverage–risk 曲线，看 `p̂ĉ` 的 selective-risk AUC 是否显著低于 `p̂`。
5. 预写出口：AUC 无差异 → 停；γ_verify CI > ±3pp → 补标注；两者都过 → 第二 sprint 接静态 gate，不直接上多模式。

交付：一页 action-mix、一条 coverage–risk 曲线、`γ_verify±CI`、go/no-go。

### E4 成本/收益模型（公式，不编价）

E4 不要求论文给金额；要求**能把部署单价代进去**。用这三个式子：

**统一反事实 = 不上护栏（do nothing）**，不是 Uncertainty-Menu/Risk-Menu。do-nothing 基线：HSR 32.76%、approvals 0%、task success 29.48%（Table 2）。

- 伤害节省/千次 = `(32.76% − HSR) × (1000/L) × incidents_per_harmful_trajectory × cost_per_incident`（L=20 动作/轨迹；HSR 按轨迹）。
- 审批成本/千次 = `approval_rate × 1000 × minutes_per_approval / 60 × hourly_rate`（对 do-nothing，approval 从 0 增到 8.7%，是**成本**不是节省）。
- task success 收益/千次 = `(47.01% − 29.48%) × 1000 × value_per_success`（可选，若业务能货币化）。
- 12 个月 TCO = 建设（2–4 人周 × 人周价 + sandbox/审批集成）+ 运行（`0.486` 是论文匹配的公共 compute；CASEL 自身 factor 0.58，按 `0.58 × 基线算力成本` 估）+ 审批人时 + 维护（γ/阈值/c_base 重标 × 次数 × 人日价）。

**build/buy/不做**：

- build：TCO 如上；收益 = 伤害成本下降 + 审批工时下降 + task success 变化折算。
- buy：商用护栏/审批产品的报价 + 集成人周；没有 RFQ 就写「待报价」，不要编价。
- 不做：当前 HSR/审批/伤害成本基线；这是反事实。
- 决策线：12 个月 `NPV_build = Σ(伤害节省 − 审批成本 + task success 收益)/(1+r)^t − TCO`；`NPV_buy` 同口径（RFQ 报价+集成+迁移/退出）；`NPV_do_nothing=0`。取 argmax；task success 下降 ≤2pp、false-veto ≤5% 是硬约束。没有单价/基线时，只能给公式与敏感性，不能给结论。

### E4 验证设计（两段，不是一次 log-only）

- **Stage 1（2 周，log-only）**：估动作混合、`γ_verify±CI`、coverage–risk；不测 HSR 降幅。
- **Stage 2（4–6 周，shadow/A-B）**：主指标 HSR；按基线 HSR 与最小可检测差异算样本量；预注册审批率、false-veto、task success 为副指标；成功线「HSR 相对降 ≥30%、审批 ≤10%、task success 不降 >2pp」；失败线「AUC 无差异或 false-veto >5%」；停止线「年省伤害 < 年化(建设+算力+审批人时+维护)」，不是只比审批人力。
- **功效**：HSR 是稀疏事件，样本量按基线率算；不要用 2 周 log-only 的样本硬判 HSR。

## 6.6 客户价值假设（V2/V3，`推测`）

- **受益者**：agent 平台/风控/合规；痛点：不可逆动作的伤害、审批排队、误拦合法动作。
- **指标**：每千次工具调用的有害副作用（HSR）、审批数/千次、false-veto 率、task success、p95 时延。
- **反事实**：不上护栏 → HSR 32.76%（模拟）；只 always-verify → task success 高但 compute 1.0；不做多模式 → 审批/算力换 harm。
- **V3 试点**：单工具集、2 周 log-only；先估 γ_verify 与动作混合，再画 coverage-risk；预注册「p̂ĉ 排序的 selective-risk AUC 显著低于 p̂」；成功 = 审批 ≤10% 且 HSR 相对降 ≥30%、task success 不降 >2pp；失败 = AUC 无差异或 false-veto >5%；停止线 = 年省伤害 < 审批人力成本。
- **反例**：γ_m 估不准；审批疲劳；动作混合偏离 58/28/14；多步组合后果；模拟与真实流量差异。

## 7. 质量与边界

- **证据类型**：实证·模拟（受控但非部署）。
- **强项**：对照干净；成本/审批/覆盖都报；有负结果（ledger）；有 misspecification 压力测试；诚实声明「effectiveness assumed」。
- **主要威胁**：模拟的 γ_m/k/q 是假设；审批疲劳未建模；abstain/staleness 未启用；单步决策；task success 与 HSR 反向。
- **`quality: B`**：受控模拟很强，但不是部署；核心机制依赖未测量的 γ_m。

## 8. 与仓库判断的关系

- **01-L4**：把干预拆成多模式比单一剪枝更省代价（模拟）。
- **01-L5**：审批量是护栏的隐性成本（CASEL 8.7% vs Risk-Menu 12.6%）。
- **E-15（已核）**：护栏评估应报 harm–approval–cost 前沿，不是单一 HSR。
- **P3a/P3b**：仓库 P3a 是「判定是漏检/误报/审批的权衡」，P3b 是「不存在单一向优的本体来源」。本页的 harm–approval–cost 三轴属 **P3a**，不是 P3b（没测来源）；别把两者混写。
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
- PDF：同目录 `2610.36570-casel.pdf`
- 代码/数据：论文未给公开仓库。
