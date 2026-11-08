# 动作前拦截 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。
> 「工程发现 1–4」是从 POLAR/CASEL digest 吸收的落地口径（接口/参数/标注协议/成本/替代方案/stop/客户指标），不是新增结论。

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

**admissibility**：评分前先过滤注释——provisional / revoked / disputed / 未接地的边不进入逆序列。

**反向搜索**：从最近的动作往回找 undo 边，组合候选逆序列 π；成功则 `φ(π)=min φ(u)`（最弱一步），失败则报告第一个不可执行步骤。阈值 τ=0.80；低于阈值或没有完整 π → Veto。

**判定与执行分离**：APPROVE / VETO / ESCALATE 是 DecisionPolicy，不是本体的一部分。被评估的 wrapper **不模拟完整 post-action state s′**；只对可用 Layer B 当前投影检查。只有 VetoPolicy 有可比的 reward 结果；Escalate/Advisory 的归档均值与提交表冲突，作者撤回比较。

## 机制二：多模式分配（CASEL）

不是二值 veto，而是六选一：direct / verify / sandbox / clarify / approve / abstain（abstain 本文未启用）。

- 信号：`p̂`（校准失败率）、`ĉ`（后果）、`ρ`（可逆性）、`g`（歧义）、`d`（证据新鲜度）。
- 代价：`J(m)=γ_m·p̂ĉ + λk(m) + μq(m)`；`γ_m` 是干预后的残余失败比例，**论文是假设值，不是测量**。
- 前置门：`g>τ_g=0.2` 先走 clarify、`d>τ_d` 先走 verify，发生在 `J(m)` 之前；不是所有模式都由 J 选。
- 可行性：sandbox 只对 reversible mutation/dry-run；approve 只对 compensable/irreversible；模拟里 approve 仅对 irreversible 且 `ĉ≥0.55` 开放。
- 选择性风险：直接执行集 `A_τ={S≤τ}`；Hoeffding + union bound 给有限样本阈值。Proposition 1 要求校准记录 i.i.d. **且与拟合 `f_cal` 的数据 disjoint**，并因轨迹内动作相关而 **one record per trajectory**。
- 轨迹总账：`H_t=Σ D_i r̄_i ≤ B_H`；只在 `r̄` 每步上界真实条件风险时成立。模拟里 54% 直接执行步骤 `p_t c_t > r̄_t`，前提失败；full ledger 在 harm–compute 面被支配，但在低审批端（4.3% approvals / 11.82% HSR）仍是前沿点。

**主表口径**：CASEL 的 7.02% HSR / 8.7% approvals 是 `τ̂=∞`（阈值关闭）下的结果；阈值规则在 §VI-E，不能把主表当「开了阈值」的成绩。

## 失效模式

- **T1-only ≈ blanket veto。** 结构反向组合的贡献未被隔离。
- **可逆性 ≠ 安全性 ≠ 授权。** 外部副作用可能完全合法；retail 的 return/exchange 在 block log 里出现，但没有授权标签，不能判定是不是误拦。
- **漏掉一条不可逆关系 → false approval。** 本体错误是 fail-open 的。
- **判据依赖运行时状态。** 静态本体不够；需要 Layer B。
- **阈值错置。** airline 在 0.80 只保留 36.6%，retail 100%。
- **只判不记。** 剪枝事件不记录，false-veto 无法算。
- **不验证逆执行。** 「有逆序列」不等于「恢复会成功」。
- **CASEL 的干预有效性是假设。** `γ_m` 不是测量；审批疲劳未建模。
- **把 7.02% 当阈值开启的结果。** 主表 `τ̂=∞`；阈值规则另测。
- **把 CASEL-NoRev 当单变量。** NoRev 是 verify-only，同时去掉 sandbox/approve；15.53% 不能只归因给「可逆性路由」。

## 与本体 / 回路的关系

本体在动作前以**类型化逆关系**出现；约束强度强（能阻止副作用），覆盖率窄（只覆盖 mutating tools）。被违反时，系统能报出哪条边缺失/哪个 bound 不满足/哪一步 φ=0；但无法证明语义真值或授权。

## 实施与客户价值（A3/A4）

### 实施决策

- 弱模型 + 高不可逆风险：硬 veto；强模型/合法意图主导：advisory + 授权层（后者是推测，无阈值）。
- 不先建六模式：POLAR 路径先做可逆性路由 + shadow；CASEL 路径先 log-only 估动作混合与 `γ_verify`，再上静态 `p̂ĉ` gate，最后才考虑多模式。
- 验收用 harm–approval–cost–task success 四轴，不用单一 reward/HSR。

### 工程发现 1｜接口：门挂在哪、输出什么

- **POLAR**：pre-tool-call middleware；输入 `(tool, args, state_hash)`；输出 `{decision, phi, pi, bottleneck}`；ESCALATE 路由到具名队列，VETO 返回可读理由（哪条边/哪个 bound/哪一步 φ=0）。
- **CASEL**：位于 agent 与工具执行器之间；可选 MCP proxy、pre-execution hook、policy engine，均不需重训。输入 proposed tool call、tool schema、user context、state/evidence 时间戳；输出 `{mode, p̂, ĉ, ρ, g, d, J(m), reason}`。
- **执行分支**：`direct` 直接执行；`verify` 调 checker；`sandbox` 需可回滚/dry-run 接口；`approve` 只对 compensable/irreversible；`abstain` 可关。
- **`p̂` 必须校准**（isotonic / temperature scaling）；不校准，阈值和账本都没有意义。
- **日志**：POLAR 记 `{tool, entity, tier, phi, tau, decision, reason}`；CASEL 每个 call 记动作、可逆性、`c_base`、`p̂`、决策、审批人/时间、是否回滚。没有日志就算不出 false-veto/审批成本。
- **工具 schema**：`tool, args, mutating, slots[]`；Layer A 五谓词；Layer B `slot(entity_type,id)=value` + `state_hash`。

来源：[POLAR digest](../../../src/papers/2610.08082-polar/digest.md) · [CASEL digest](../../../src/papers/2610.36570-casel/digest.md)

### 工程发现 2｜参数：能抄的是条件，不是值

- **POLAR 注释准入**：评分前过滤 provisional / revoked / disputed / 未接地的注释，它们不进入逆序列；实现时把这四类写成状态位并记日志，审计时才能解释「为什么少了一条逆路径」。
- **POLAR curator rubric**（digest 工程配方，不是论文测量）：`w` 1.0=有测试/生产验证的精确逆；0.8=文档化但未测试；0.6=部分可逆/有损；0.3=仅理论可能；0=不可逆；`w_loss` 按损失类别（金钱/时间/数据）给 0–1。
- **POLAR 反向搜索**（工程配方）：深度上限 3–5、环路检测；多候选取 `max min φ`，同分取最短；τ=0.80 是论文设置，按域保留率校准，不跨域照搬。
- **CASEL 前置门**：`g>τ_g=0.2` → clarify；`d>τ_d` → verify；在 `J(m)` 之前。approve 在模拟里只对 irreversible 且 `ĉ≥0.55` 开放。
- **CASEL 的 γ/k/q 是模拟假设**：direct/verify/sandbox/approve 的 γ 1.00/0.42/0.15/0.04；k 0/1.0/1.6/2.2；q 0/0/0.04/0.65；λ:μ=0.02:0.015。换域要重标；**没有 γ_m 数据不要算 J(m)**。
- **Prop 1 的校准契约**：校准记录 i.i.d. 且与拟合 `f_cal` 的数据 disjoint；one record per trajectory。校准量见 Eq(5)：40,000 条校准轨迹、20 点网格、δ=0.1；ε=0.014 时 20/20 seed 绑定（coverage 62.3%、risk 0.0035）；160,000 条时 ε=0.009 才可认证。
- **CASEL 最小标注协议**（digest 数据契约；**论文未给**，`推测`）：2,000–10,000 条轨迹、每条轨迹一个记录；20% 双标，κ≥0.6；分歧由第三人裁决；每季度重标。低于这个量不要用 Eq(5) 认证；Eq(5) 的 40,000 条/ε=0.014 是另一档（上条），不能拿 2,000 条当 40,000 条用。
- **`c_base` 锚点**（论文无 rubric；下列是 digest 给的可抄起点）：read-only 搜索 0.05；可逆编辑 0.4；不可逆转账/对外发送 0.9；删除唯一副本 1.0。粒度先 per-tool，金额/敏感工具再 per-arg；评审人=工具 owner，季度复审。
- **动作混合**：论文 58% read / 28% reversible / 14% irreversible；自己的流量先统计，偏离会改 approvals/HSR；不可逆长尾要过采样。
- **维护**：工具/槽位变更后更新 Layer A 注释与 Layer B 投影；否则逆搜索用的是过期边。

来源：[POLAR digest](../../../src/papers/2610.08082-polar/digest.md) · [CASEL digest](../../../src/papers/2610.36570-casel/digest.md)

### 工程发现 3｜成本：人时没有实测，E4 只给公式

- **POLAR 人时**（`推测`，论文未测）：Layer A 每域 2–5 curator 人日；接 DB/工具日志 1–2 人周；阈值校准/false-veto 标注 3–5 人日/域。
- **审批人时**：无实测。POLAR 未测；CASEL 只给 approvals 比例（6.9–13.8%），没给分钟；在没有实测前，审批人时应写未知。
- **CASEL 模拟成本**：表 2 的 menu 类方法同 compute 0.486；Base 0.000、Always-Verify 1.000、Mutation-Gated 0.420。E4 的 TCO 另用 CASEL factor 0.58 估算运行算力（见下），不要把 0.486 当部署单价。
- **E4 公式**（把部署单价代进去，不编价；统一反事实=不上护栏：HSR 32.76%、approvals 0%、task success 29.48%）：
  - 伤害节省/千次 = `(32.76% − HSR) × (1000/L) × incidents_per_harmful_trajectory × cost_per_incident`（L=20 动作/轨迹；`incidents_per_harmful_trajectory` = 每个有害轨迹的事故数）。
  - 审批成本/千次 = `approval_rate × 1000 × minutes_per_approval / 60 × hourly_rate`。
  - task success 收益/千次 = `(47.01% − 29.48%) × (1000/L) × value_per_success`（CASEL 对 do-nothing；可选）。
  - 12 个月 TCO = 建设（2–4 人周 × 人周价 + sandbox/审批集成，`推测`）+ 运行（`0.58 × 基线算力` + 审批人时）+ 维护（γ/阈值/c_base 重标 × 次数 × 人日价）。
  - 决策线：`NPV_build = Σ(伤害节省 − 审批成本 + task success 收益)/(1+r)^t − TCO`；`NPV_buy` 同口径（RFQ 报价+集成+迁移/退出）；`NPV_do_nothing=0`；取 argmax。硬约束：task success 降 ≤2pp、false-veto ≤5%。
  - 没有单价/基线时，只给公式与敏感性，不给结论。

来源：[CASEL digest](../../../src/papers/2610.36570-casel/digest.md)

### 工程发现 4｜stop 与客户指标

- **POLAR stop**（工程门，不是论文阈值）：shadow false-veto >5% → 降 advisory/停；同轨迹配对 Δ≤0 且 T1-only≈full → 结构贡献不成立，停；保留率 <20% 或 >95% → 阈值失效，重校准；拿不到真实状态 → 不做硬 veto。
- **CASEL stop**（工程门；数字是示例）：
  - `γ_verify` 的 CI 宽到无法区分 direct/verify 的 J 差 → 只上静态 `p̂ĉ` gate，不做多模式。
  - 校准量不足以把 `γ_verify` 压到 ±3pp → 停，先补标注。
  - 审批率 > 业务上限（例如 >15%）或 false-veto 投诉超阈值 → 降级到 always-verify/静态 gate，或关闭。
  - `p̂ĉ` 的 selective-risk AUC 未显著低于 `p̂` → 机制不迁移，停。
- **指标**：每千次工具调用的不可逆伤害/HSR、false-veto 率、审批/千次、task success；CASEL 另加 p95 时延。
- **反事实**：统一反事实是「不上护栏」，不是 Uncertainty-Menu/Risk-Menu；blanket veto 的反事实是误拦合法动作，但 false-veto 未测。
- **替代方案同口径**（对比时必须齐 TCO / 年省伤害 / 审批率 / task success / 硬约束；论文只覆盖部分模拟轴，下面是现有证据与缺口）：
  - **不上护栏**：CASEL 模拟 Base = HSR 32.76%、审批 0%、task success 29.48%、compute 0.000；这是模拟反事实，不是自己的基线。
  - **blanket veto**（digest 视为最便宜的替代，但无成本实测）：POLAR 没有可比的 HSR/false-veto 数字；T1-only 在 airline 退化成「凡 mutating 就拒」，只能当近似。
  - **静态 `p̂ĉ` gate + 仅 mutating 审批**：CASEL 没单独跑；最接近的 Risk-Menu 是 CASEL 模拟的 menu 类（5.82% HSR / 12.6% 审批），不能把它的数字当静态 gate 的成绩。
  - **Always-Verify**：CASEL 模拟 15.47% HSR / 58.81% task success / compute 1.000；approvals 未列，menu 与 CASEL 不同。
  - **纯人工复核**：论文未测；所有动作走人工，时延/成本未知，不能从 CASEL 的 8.7% 审批率外推。
  - **事后补偿 / LLM-as-judge / 现成护栏产品**：POLAR digest 只把它们列为替代，没给同条件成本-效果，没有可抄的数。
  - **证据缺口**：论文没与 REFLEX/CA2I、现成护栏产品或纯人工比；build/buy 边界要自己补同口径 TCO。`推测`
- **V3（`推测`）**：
  - POLAR：单域 shadow 200–500 决策；成功 = false-veto ≤5%、配对 Δ>0 且 CI 不跨零、审批 ≤10%；失败 = Δ≤0 或 false-veto >5%；停止线 = 年省事故 < curator+审批成本。
  - CASEL：单工具集两段，不是一次 log-only。
    - **Stage 1（2 周，log-only）**：只估动作混合、`γ_verify±CI`、coverage–risk；**不测 HSR 降幅**。
    - **Stage 2（4–6 周，shadow/A-B）**：主指标 HSR；按基线 HSR 与最小可检测差异先算样本量/功效；预注册审批率、false-veto、task success 为副指标；不要用 Stage 1 的 2 周样本硬判 HSR（HSR 是稀疏事件）。
    - 成功 = 审批 ≤10% 且 HSR 相对降 ≥30%、task success 不降 >2pp；失败 = AUC 无差异或 false-veto >5%；停止线 = 年省伤害 < 年化（建设+算力+审批人时+维护），不是只比审批人力。

来源：[POLAR digest](../../../src/papers/2610.08082-polar/digest.md) · [CASEL digest](../../../src/papers/2610.36570-casel/digest.md)

### 第一个 sprint

2 周、单域 shadow，不接线上写权限：列 mutating tools/槽位 → 写 T1/T4/T5 本体 v0 → 接只读状态 → 反向搜索+日志 → 回放 200–500 决策 → 标 100 blocked false-veto → 出 build/buy/不做 memo 与配对 A/B 方案。

### 反例

强模型/retail 回退；合法意图可能被误拦（block log 无授权标签，误拦率未测）；状态投影不准；本体无人维护；T1-only≈blanket veto。

## 关联

- [POLAR 卡](../../../src/papers/2610.08082-polar/card.md) · [digest](../../../src/papers/2610.08082-polar/digest.md)
- [CASEL 卡](../../../src/papers/2610.36570-casel/card.md) · [digest](../../../src/papers/2610.36570-casel/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
