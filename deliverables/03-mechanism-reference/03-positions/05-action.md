---
status: draft
deliverable_status: draft
updated: 2026-11-11
position: action
evidence: [E-04, E-13, E-15, E-16]  # E-04/13/16 withdrawn
---

# action：动作能不能做

> **W-03**：主锚 E-04/E-13 撤回（E-16 见 W-04）；本卡保留机制与边界，效应量不引用。CASEL（E-15）是非本体参照，不能补这一格。
>
> **词源**：「策略表达」有 `N: W3C ODRL 2.2`（许可/禁止/义务的写法），「判定架构」有 `N: OASIS XACML 3.0`（PDP/PEP/PAP/PIP）；但两者都**不定义「可逆」、不给阈值、不含执行点**。「可逆性 / 动作闸 / min φ / τ」是本仓库工作词（`local`），阈值与效应回 E-xx，不引标准。


> **一句话**：这是唯一能在副作用发生前改变走向的位置。它问的不是「模型觉得安全吗」，而是「有没有可接受的逆序列 / 前提条件成不成立 / 该分配多少审查」；但它只在窄条件下有效，强模型/合法意图场景会回退。

**为什么是 min φ**：POLAR 的整条逆序列分数取最弱一步；一步不可逆就把整条拉到 0，所以「平均可逆性」会骗人；低于 τ 就 veto（τ 是论文参数，源已移出，只作机制示例）。**条件**：Layer B 状态准确；**反例**：reward 不是 harm（作者声明），T1-only≈full；**决策**：只在弱模型/不可逆/高代价时 shadow。 **原锚 E-04/E-13 已撤回**；旧格数/改善数、T1-only 观察停用，待新源。

## 1. 机制

这一格其实是三种子机制，判据不同，不能混：

| 子机制 | 问什么 | 机器做什么 | 代表 |
|---|---|---|---|
| 可逆性闸 | 存在可接受的逆操作序列吗？ | 两层本体：T1–T5 类型化逆关系 + 状态投影；反向搜索，取最弱一步 φ；低于 τ 或没有完整 π → veto | POLAR（E-04） |
| 条件验证 | 结论/动作的前提条件成不成立？ | 三值条件 ⊤/⊥/? + 假设 revision；缺证据转观察 | OntoAct / reasoning-gate（E-16） |
| 多模式分配 | 这个动作该 direct/verify/sandbox/clarify/approve？ | `J(m)=γ_m·p̂ĉ + λk(m) + μq(m)`；前置门 `g`/`d` 先走 clarify/verify | CASEL（E-15） |

POLAR 的两层：Layer A 静态动作本体（每个 mutating tool 的 T1–T5 + curator 权重）；Layer B 状态投影 `slot(entity,id)=value`，从真实 DB + 已执行工具重建。**判定与执行分离**：APPROVE/VETO/ESCALATE 是 DecisionPolicy，不是本体；被评估的 wrapper 不模拟完整 post-action state s′。

## 2. 触发、输入、输出

| 项 | 内容 |
|---|---|
| 触发 | 工具调用前 / 动作执行前 |
| 输入 | `(tool, args, state_hash)`；CASEL 另加 `p̂, ĉ, ρ, g, d`、user context、evidence 时间戳 |
| 输出 | `{decision, phi, pi, bottleneck}` 或 `{mode, p̂, ĉ, ρ, g, d, J(m), reason}` |
| 下一步 | approve 执行；veto 返回可读理由；escalate 进审批队列；shadow 只记录 |

## 3. 能改变什么（E-04/E-13/E-16 撤回；E-15 为现役非本体参照）

> E-04/E-13/E-16 均已撤回；本节数字不得作为效应量引用。E-15 是非本体参照。

- **可逆性闸可能在窄条件下改善任务表现，但整体改善面很窄。** 旧观察是「部分模型/域有提升，模型-域组合里只有少数整体改善，retail 与更强模型常回退」；具体数值随 E-04 撤回停用。`withdrawn`（原 E-04；状态 contested）
- **收益可能随基线能力升高而缩小。** 旧观察是六点描述性拟合（斜率为负、给不出零交叉阈值）；具体斜率/拟合优度随 E-13 撤回停用。`withdrawn`（原 E-13）
- **审批/分配有前沿，不是单一最优。** CASEL 模拟（20 seeds、120k actions）HSR 14.75%→7.02%、审批 8.7%；最低 HSR 是 Consequence-Menu 4.38%（审批 13.8%），Risk-Menu 5.82%（审批 12.6%）；相对 Risk-Menu，CASEL 少约 30% 审批（12.6%→8.7%，相对降 30.95%），HSR 高 1.2pp（7.02% vs 5.82%）。E-15 把这一权衡概括为「约 30% 更少审批达到相近 harm」；1.2pp 算不算「相近」取决于你的 harm 计价（`推测`），不要读成零代价。`已核`（E-15；模拟、无本体变量、主表 τ=∞）
- **约束形式决定天花板还是护栏。** 限制知识源（curated KG）可能封顶；三值条件 + 假设 revision 可能同时提高成功率与减少无效干预。旧对照数字随 E-16 撤回停用。`withdrawn`（原 E-16；模拟、固定 schema、无真实工厂）

## 4. 拦不住什么 / 失效模式

| 失效 | 说明 | 证据/等级 |
|---|---|---|
| 结构贡献未隔离 | T1-only 接近 blanket veto，增益却不比 full 小 | `withdrawn`（原 E-04） |
| false-veto 未测 | blocked log 没有 harm/授权标签；retail 的 return/exchange 不能判定是否误拦 | `withdrawn`（原 E-04 的缺口） |
| 强模型/retail 回退 | 硬护栏在高基线可能只剩代价 | `withdrawn`（原 E-04/E-13） |
| 阈值错置 | 论文的 τ 参数会让部分域的候选动作被大量剪掉，另一些域几乎不剪（具体比例停用） | `withdrawn`（原 E-04） |
| 判据依赖运行时状态 | 静态本体不够；Layer B 投影不准就失效 | `withdrawn`（原 E-04 的机制） |
| 不验证逆执行 | 「有逆序列」不等于「恢复会成功」 | `withdrawn`（原 E-04 的边界） |
| 只判不记 | 剪枝事件不记录，false-veto 无法算 | `withdrawn`（原 E-04 的缺口） |
| CASEL 的 γ_m 是假设 | 干预后的残余失败比例不是测量；审批疲劳未建模 | `已核`（E-15） |
| 多模式不是单变量 | CASEL-NoRev 是 verify-only，同时去掉 sandbox/approve；15.53% 不能只归因给可逆性路由 | `已核`（E-15） |

## 5. 使能条件

- 动作不可逆且代价高（对外发送、资金、删除唯一数据）；
- 模型能力弱于域要求；强模型 + 高基线先做 shadow，不要直接硬 veto；
- 域规则可被查询成事实；拿得到运行时状态（Layer B）；
- 合法意图不主导；否则先补意图/授权层，再谈可逆性。

## 6. 证据与边界

| 证据 | 等级 | 支持什么 | 不能证明什么 |
|---|---|---|---|
| E-04 | **withdrawn** | 可逆性闸的窄条件收益；回退；T1-only；false-veto 缺口 | 结构判据有效；安全保证；合法意图误拦 |
| E-13 | **withdrawn** | 收益随能力下降的描述性拟合 | 预测曲线；零交叉阈值 |
| E-15 | 已核 | harm–approval–cost 前沿；审批量 | 本体增益；审批疲劳；所有方法同 menu |
| E-16 | **withdrawn** | 条件验证的形式影响；三值 + revision | 安全保证；真实工厂；所有知识源 |

> 四种证据都带强限定：E-04 是单基准/单 gate/6 模型；E-15 是模拟、无本体变量；E-16 是模拟、固定 schema。**不要把任何一个数字当「本体护栏有效」的效应量。**

## 7. 可证伪条件

- **先按 W-03 自测**：shadow 200–500 决策；100 条 blocked 标 harm/授权；同轨迹配对；报 miss–false-block 前沿（不设单点）。

- 同轨迹配对显示 full 相对 T1-only 的 Δ>0 且 CI 不跨零 → 结构贡献成立；
- shadow 标注 false-veto 的 miss–false-block 前沿（不设单点 ≤5%），且 harm 降、task success 不降 >2pp → 窄条件下可试点；
- 强模型上不再回退，或回退可被能力阈值解释 → 收窄 E-13 的边界；
- 复合动作的可逆性可计算且与单步一致 → 扩大可逆性闸的适用范围。

## 8. 上游指针

- 机制：[action-gate/mechanism](../../../topics/01-constraint/action-gate/mechanism.md) · [reasoning-gate/mechanism](../../../topics/01-constraint/reasoning-gate/mechanism.md)
- 判断：[01-constraint/README](../../../topics/01-constraint/README.md) · [conclusions](../../../topics/conclusions.md) E-04/E-13/E-15/E-16
- 施工：[02 R6（recipes）](../../02-engineering-playbook/03-recipes/README.md) · [01 能力 6/11/12](../../01-capability-status/02-sections/02-map.md#22-一张表)
- 长版论证：[附录 §3.4.5](../05-appendix-constraint-spectrum.md#345-action动作前的闸)
