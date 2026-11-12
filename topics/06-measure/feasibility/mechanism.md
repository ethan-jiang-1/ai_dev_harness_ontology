---
status: draft
updated: 2026-11-12
---

# 落地经济学 · 机制

> 只写「怎么算、怎么选」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。
>
> **2026-11-12 对账**：成本表中 **CASEL / N&D / CAI / FIRME / EvoMemState / CASTON 仍 admitted**（数字保留）；**POLAR / OntoAct / Ontology Catch / OA-RAG / OntoDoc / Grid 已撤回**——其成本/效应数字作历史示例，不作活证据（链接已指 tombstone）。五成本维度与算法框架是设计（`推测`）。

## 五个成本维度

| 维度 | 问什么 | 常见漏算 |
|---|---|---|
| 建设 | 一次性投入多少？谁维护？ | 本体/投影/registry 的人工建模 |
| 运行 | 每次查询/动作多少 token、时延、调用？ | 检索轮次、审批、重试 |
| 维护 | 源/工具/法规变更后怎么更新？ | 增量重抽、版本对账、回归测试 |
| 人审 | 多少比例需要人看？看的成本？ | 审批疲劳、false alarm 的信任损失 |
| 失败 | 机制失效时的代价？ | false veto、错误合并、漏检 |

## 机制成本表

| 机制 | 建设 | 运行 | 维护/人审 | 盈亏平衡/边界 | 来源 |
|---|---|---|---|---|---|
| 01 动作闸门（POLAR） | 每域本体（T1–T5、curator 权重） | 每次候选调用反向搜索；轻量 | 阈值校准；false-veto 未测 | 收益随基线能力下降（六点描述性拟合，不是部署阈值）；T1-only ≈ blanket veto | [POLAR](../../../meta/audits/2026-11-11-source-purge.md#src-2610-08082) |
| 01 多模式分配（CASEL） | per-tool consequence 元数据；sandbox/approval | 每次 `p̂ĉ` + J(m) | 审批 8.7–13.8%（模拟，主表 τ=∞）；γ_m 假设 | harm–approval–cost 前沿；不是最低 HSR | [CASEL](../../../src/papers/2610.36570-casel/digest.md) |
| 01 推理闸门（OntoAct） | ontology schema + 世界知识构造 | 每次条件求值 + LLM 提议 | schema/记录维护；构造 token 另算 | 三值条件；固定 schema；模拟 | [OntoAct](../../../meta/audits/2026-11-11-source-purge.md#src-2610-21983) |
| 02 checker（Ontology Catch） | curated/data-derived/LLM 本体 | curated 66k tokens/46s；data 28k/17s（每被 flag 的答案，不是每答案） | 审计；false alarm 重试 | 必须先超过空结果重试基线 | [Catch](../../../meta/audits/2026-11-11-source-purge.md#src-2610-37809) |
| 02 证据契约（OA-RAG） | concept cards + reasoner + SPARQL | 5.8 calls/9.7k tokens（Test 3） | grounding 校准；本体维护 | 同 8k 预算下 84.9% vs 66.7% | [OA-RAG](../../../meta/audits/2026-11-11-source-purge.md#src-2610-36335) |
| 03 投影（N&D） | 塔 + 投影（45k 字符） | prompt token；9B 可跑 | 投影/知识节点维护 | 答案在文本里才有效；9B+投影 > 750B 不带 | [N&D](../../../src/papers/2610.11768-narrow-and-deep/digest.md) |
| 03 编译（CAI） | 编译成本 `c`（query-equivalent） | 条件性 −91%/+1.9%；平均 −38% | 增量重抽；时延约 3×（7 题配对） | `p_h > 2% + c/(0.929Q)` | [CAI](../../../src/papers/2610.41172-context-as-infrastructure/digest.md) |
| 04 记忆（FIRME） | registry/alias + 本体 | 每次匹配/更新 | false merge 污染；人审 | alias +7.8–12.1 pp CMR；token −7.2% | [FIRME](../../../src/papers/2610.40482-firme/digest.md) |
| 04 状态（EvoMemState） | 本体 + GRPO 训练 | 检索/遍历 + policy | 训练信号；多模态未测 | Acc@complete +11.5/+31.2 | [EvoMem](../../../src/papers/2611.03743-evomemstate/digest.md) |
| 05 生成（OntoDoc） | 4 阶段 pipeline | 每 IRI 多次 LLM/检索 | 人审；假设层信息损失 | completeness 3.43→3.84；无下游 | [OntoDoc](../../../meta/audits/2026-11-11-source-purge.md#src-2611-01276) |
| 05 精化（CASTON） | 微调 embedding | 30×10 候选 + LLM | 专家审；medium 接受 0/2（default）、1/4（pretrained）、1/5（GPT-4o mini） | high 6/6；pretrained 57.1% | [CASTON](../../../src/papers/2610.21466-caston-refinement/digest.md) |
| 证据 + solver（Grid） | 法规语料 + 领域工具 + solver | 每次研究；13.9 s | 人签核；法规更新 | 99.9% vs base 40.8%；optimizer −33–67% | [Grid](../../../meta/audits/2026-11-11-source-purge.md#src-2611-03534) |

## 三个可算的盈亏平衡

1. **编译**：`p_h > 2% + c/(0.929Q)`。Q=1,000、c=10 → 3.12%；p_h=2.5% 仍亏。**平均 −38% 不能当上线依据。**
2. **分配**：没有单一 HSR 最小；按 harm–approval–cost 前沿选点。CASEL 8.7% approvals / 7.02% HSR；Risk-Menu 12.6% / 5.82%（模拟；CASEL 主表在 τ=∞，阈值关闭）。**审批少 30% 是否值得多 1.2 点 HSR，是业务问题。**
3. **能力**：约束类收益随基线能力下降（POLAR；六点描述性拟合，不识别 causal headroom，不能当阈值）；知识投影增益不随容量上升（N&D，H2 p=0.85 是「未检出」，不是「证明无效应」）；9B 带投影 > 750B 不带（区间约 0.3 宽）。**没有一条适用于所有机制的能力曲线。**

其余 9 个机制本页只给成本项与定性边界，没有 break-even 公式；不要把 3 条可算门槛和 9 条定性边界合成一个总分。

## 使能条件（为什么现在才出现）

- **长上下文**：45k 字符投影、concept cards、法规语料可进 prompt。
- **工具调用/结构化输出**：agent 能查 SPARQL、调 solver、写 JSON。
- **便宜的小模型**：claim 抽取、checker、投影生成不必用 frontier。`推测`（CAI 只对抽取器说「质量由 validation 保证」；其余是外推）
- **可接的 solver/validator**：Grid 的 solver；OA-RAG 的 reasoner；SLB 的 solver。
- **可观测的 token/时延/审批**：没有 per-query 账本，就算不出 `p_h` 与 miss 分布，2%/3.12% 只是纸面门槛。

**但本体编写、投影生成、memory registry 仍是人工成本**；这些论文没有把建模成本降到零。

## 决策规则（先问五个）

1. **答案在知识里，还是要从语料里找？** 在 → 投影/说明；不在 → 编译/检索/solver。
2. **时延是硬约束吗？** 是 → 不要用「省 token 但加轮次」的替换；考虑 E1/决策门。
3. **能接受多少误报/审批？** 低 → data-derived checker + 空结果基线；高 → curated/多模式。
4. **复用次数够吗？** 编译/投影需要 `Q` 足够大；一次性任务不值得建。
5. **有训练信号/参考答案吗？** 没有 → 不要上 GRPO reasoning-state；用检索/规则。

## 问题 → 机制目录

| 操作问题 | 机制 | 证据 | 成本/边界 |
|---|---|---|---|
| 跨源实体同一性 | registry + alias；commit gate | FIRME；Commit Boundary | false merge；无实现 |
| 不可逆动作防护 | 可逆性 gate；多模式分配 | POLAR；CASEL | 能力反向；T1-only ≈ veto |
| 证据不足时授权 | claim-specific promotion；三态 | Commit Boundary；CASEL | 无实现；审批 |
| 大语料重复检索 | claim–evidence 编译 | CAI | `p_h` 门槛；时延 3× |
| 判定器误报/漏报 | 空结果基线 + data-derived checker | Ontology Catch | false alarm；无正确答案 |
| 本体维护/描述缺失 | 生成 + 精化 | OntoDoc；CASTON | 无下游；单一本体 |
| 评测方差/失败归因 | 配置轴；角色画像；trace | Agents are Systems；Diagnose；SLB | 4 tasks；position paper；闭源无 trace |

## 与本体 / 回路的关系

成本不在回路的任何单点；它决定「这个机制在回路里值不值得存在」。同一机制换位置/模型/预算，成本结构会变。

## 实施与客户价值（A3/A4）

> 读者是「批不批预算的人」。本节不重复各派机制（见 [01](../../01-constraint/README.md)–[05](../../05-produce/README.md)），只回答这张尺子改变哪个决定、要什么数据、何时必须停。单价与部署层回报仍是空洞（[G1–G3](./frontier.md)）；**带 `已核` 的只指 digest 里核过的数字/公式/契约；sprint、阈值、组织建议属于本页工程配方，一律 `推测`。**

### 实施决策

1. **上线审批看盈亏平衡，不看平均收益。** 编译类用 `p_h` 的 95% CI 下界对 `p_min = 2% + c/(0.929Q)`；护栏类用 harm–approval 前沿点。「平均 −38%」「HSR 降 7.7 点」都不构成上线依据。`已核`（E-14/E-15；两个数都是模拟/条件值：−38% 是 hit/miss 混合，7.73 pp 是 CASEL 主表 τ=∞ 下相对 Uncertainty-Menu 的模拟差）→ 改变的是**审批材料里必须出现的分布项**（hit/miss、审批率、false-veto），不是机制选型。
2. **评测预算先买 miss；false-veto 不在现成可买清单里。** miss penalty ±1.5pp 会让 `p_h*` 在 0.4–3.6% 间移动，hit saving ±1.5pp 只动 2.0–2.1%（[CAI digest](../../../src/papers/2610.41172-context-as-infrastructure/digest.md) §6.5）；false-veto 在现有 digest 里**没有可用的测量**——POLAR 的 1,745 条 blocked decisions 没有 harm/authorization 标签，CASEL 的 approvals 也不含「本可合法执行」的标注。所以 false-veto 要先建标注能力（抽 blocked decisions 人工标），不是向供应商买一个数。`已核`（CAI 敏感度、POLAR 无标签）＋`推测`（先标 blocked decisions 的预算顺序）→ 标注预算按「拦错了多少」而不是「省了多少」立项。
3. **先建账本，再建本体。** 没有 per-query / per-decision ledger，`p_h`、审批率、hit/miss 分布都算不出来（`c` 能从编译日志单算，但没法按 hit/miss 分摊；φ 还要另抽标签审计），五维成本表只能填「未知」。`推测`（三篇 digest 的共同接口要求，不是任一论文结论）→ 决定工具链顺序：埋点先于建模。
4. **按「基线能力 × 不可逆性」排部署顺序，不按机制先进度。** 约束类收益随基线能力上升而下降（E-13），强模型与 retail（用户意图主导的域）常回退（E-04）；**合法意图是否导致回退未测**。编译类只在答案本就在语料里、复用次数够高时回本（E-14）。`已核`（E-04/E-13/E-14 的方向；E-04 未测合法意图）＋`推测`（把它当排序规则；E-13 是六点描述性拟合，作者明确不能当部署阈值）→ 决定先修弱模型那条链路，还是先修语料供给。
5. **商业论证的分母是「什么都不做」，不是「换个更好的机制」。** CASEL 模拟把 do-nothing 记为 HSR 32.76%、审批 0%、task success 29.48%（Table 2，`已核`：模拟基线）；把 Risk-Menu/Uncertainty-Menu 当参考臂、只让 do-nothing 进 NPV 分母，是 CASEL digest 的 E4 建模约定，不是论文结论（`推测`）。→ 改变的是采购 memo 里「省了多少伤害」的减法基准。

### 数据/接口

- **评测账本（最小字段集）**：`query_id, arm, hit/miss, token_in/out, latency, rounds, gate_verdict, citations`。缺这张表就算不出 `p_h`、φ、`p_min`（CAI §6.5）。
- **决策账本（护栏侧）**：`trajectory_id, tool, entity, tier, phi, tau, c_base, p̂, ĉ, ρ, g, d, J(m), mode, decision, approval(人/分钟), rollback, reason`——POLAR 的 `{tool,entity,tier,phi,tau,decision,reason}` 与 CASEL 的 `{mode,p̂,ĉ,ρ,g,d,J(m)}` 取并集，再补 `trajectory_id`（HSR 按轨迹、校准一条轨迹一个记录）和审批人/时长/回滚（CASEL 的日志要求）。只抄一边会丢另一边的分母：只有 POLAR 字段就算不出 `J(m)`/审批成本，只有 CASEL 字段就丢了 φ/τ 和 veto 理由。false-veto 只能从它标。
- **成本模型输入**：`c`（编译总 token ÷ 平均每问 token = query-equivalent）、`Q`、`p_h`、p95 时延；护栏侧为 `γ_m`、`k`、`q`、`c_base` rubric。`c` 与 `Q` 必须自己实测，不要套论文的 `c=10`。
- **单价表（当前全空）**：人周价、审批分钟价、单次事故成本、token 单价、审批队列基线。**填不出就只给公式与敏感性，不给结论**；表里每个数都要带出处，否则不许进 memo。
- **协议**：G1/G2 的测量一律 shadow/回放，不接线上写权限；按 collection hash 或 trajectory 分桶，主指标预登记；φ 的审计样本 100 条（区间约 4–16%）→ 400 条（7–13%）的扩样路径要预写（CAI Eq(11)）。`推测`（工程约定）
- **校准/标注协议（G2）**：CASEL 的 Eq(5) 认证要求 40,000 条校准轨迹、20 点网格、δ=0.1；ε=0.014 时 20/20 seed 绑定（coverage 62.3%、risk 0.0035），160,000 条才够 ε=0.009（`已核`：论文条件）。校准记录必须与拟合 `f_cal` 的数据 **disjoint**、**one record per trajectory**，否则 Prop 1 不成立（`已核`）。落地最小量是 digest 的工程建议（论文未给，`推测`）：2,000–10,000 条轨迹、20% 双标、κ≥0.6、第三人裁决、每季度重标；达不到就用静态 gate，不要声称覆盖率保证。
- **口径固定**：HSR 按轨迹、token 按每问总量、审批按分钟/次；换口径即不可比（C-03）。

### 组织/成本

- **owner 三缺一即失效**（`推测`）：平台/评测 owner 拥有账本与单价表（本页交付物）；域 owner 拥有本体/投影与 curator 权重；财务/风控提供事故成本与审批人时口径。缺第三项，E4 退化成公式。
- **人日**（全为 `推测`）：动作本体（POLAR Layer A）每域 2–5 curator 人日，接真实状态投影（Layer B）1–2 人周（[POLAR digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-08082) §6.5 的估算，论文未测）；控制器 + 校准 + `c_base` 审计 + sandbox/审批集成 2–4 人周（[CASEL digest](../../../src/papers/2610.36570-casel/digest.md) §6.5 的估算）；账本 + 单价表 3–5 人日（本页首次提出，无出处）。三档不能相加当 TCO——它们分属不同 owner，且都只有量级精度。
- **运行**：编译一次性 `c` + 每次查询条件性变化（hit −91% / miss +1.9%）；证据替换的配对子集时延约 3×（46.7 s → 140 s，**仅 7 题**，不是 N=200 的时延）。
- **人审**：审批 8.7%（CASEL，模拟，τ=∞）到 13.8%（Consequence-Menu）——是各臂比例，不是同一机制的区间；每次审批的真实人时未测（G2/G3）——没有本人群实测前，NPV 里只能放区间敏感性，不能放点估计。
- **维护**：增量重抽、`c_base`/`γ_m` 重标、本体修订；G3 未关，按季度复盘人时并录入账本。

### 单位经济学（E4）：把单价代进公式

> 公式来自 [CASEL digest](../../../src/papers/2610.36570-casel/digest.md) §6.5 的工程配方，不是论文结果：论文只给模拟的 HSR/审批/compute（0.486），没有金额。公式本身 `推测`（建模约定），代入的模拟基线 `已核`；控制器/参数细节见 [01/action-gate](../../01-constraint/action-gate/mechanism.md)。

**统一反事实 = 不上护栏（do nothing）**：HSR 32.76%、approvals 0%、task success 29.48%（Table 2，模拟）；不是 Uncertainty-Menu/Risk-Menu。

- 伤害节省/千次 = `(32.76% − HSR) × (1000/L) × incidents_per_harmful_trajectory × cost_per_incident`（L=20 动作/轨迹；HSR 按轨迹）。
- 审批成本/千次 = `approval_rate × 1000 × minutes_per_approval / 60 × hourly_rate`；对 do-nothing，审批从 0 增到 8.7%（CASEL 主表，τ=∞），是成本不是节省。
- task success 收益/千次 = `(47.01% − 29.48%) × (1000/L) × value_per_success`（可选；业务不能货币化就不进 NPV）。
- 12 个月 TCO = 建设（控制器 + 校准 + `c_base` 审计 + sandbox/审批集成，按 2–4 人周估）+ 运行（`0.58 × 基线算力成本`；0.486 是论文匹配的公共 compute，不是部署单价）+ 审批人时 + 维护（γ/阈值/`c_base` 重标）。
- 决策线：`NPV_build = Σ(伤害节省 − 审批成本 + task success 收益)/(1+r)^t − TCO`；`NPV_buy` 同口径（RFQ 报价 + 集成 + 迁移/退出）；`NPV_do_nothing = 0`。取 argmax；硬约束 `task success 下降 ≤2pp`、`false-veto ≤5%`。
- **缺口**：`minutes_per_approval`、`hourly_rate`、`cost_per_incident`、`value_per_success`、`r` 全空（G1–G3）。填不出来时只给公式与敏感性，不给 build/buy 结论。

### stop condition

- `p_h` 的 95% CI 下界 ≤ `p_min`（用本人群实测的 `c`、`Q`）→ 停编译，转 harness 侧：收紧读预算、改停止策略、缓存重复查询。
- 复用太少：以论文示例参数（`c=10`、`p_h≈0.43`）计，回本约 26 次查询；`Q` 低于这个量级 → 不建编译。
- 编译后 p95 时延超预算（证据替换约 3×；3× 是 7 题配对观测，不是 p95）→ 只在 token 是硬成本的一小片流量灰度，不全量。
- 护栏侧：shadow 回放 false-veto >5%，或审批率 >15%（示例上限）→ 降级 advisory/always-verify 或停。`推测`（digest 提的工程线，非论文实测；15% 是 CASEL digest 的示例，不是业务上限）。
- `γ_verify` 的 CI 宽到分不开 direct/verify 的 `J` 差 → 只上静态 `p̂ĉ` gate，不做多模式。`推测`
- 校准量不足以把 `γ_verify` 压到 ±3pp → 停，先补标注；达不到 Eq(5) 的 40,000 条校准轨迹，就不要声称覆盖率保证。`推测`（门槛是工程线；40,000 条是论文的模拟条件）
- `p̂ĉ` 的 selective-risk AUC 未显著低于 `p̂` → 机制不迁移，停。`推测`
- 同轨迹配对 Δ≤0 且 T1-only 与 full 无差异 → 结构贡献不成立，停。
- 维护人时 > 省下的 token/伤害价值 → 停；按季度重算（G3）。
- 拿不到真实状态投影 → 不做硬 veto（POLAR）。
- 无法校准 `p̂` → 不做阈值门、不算 `J(m)`（CASEL：`p̂` 不校准，阈值和账本都没有意义）。
- 没有 `γ_m` 实测 → 只上静态 `p̂ĉ` gate（`p̂` 仍要校准），不做多模式。
- **硬门槛**：没有 per-query 账本或单价表 → 不出 build 结论，只出公式与敏感性。

### 第一个 sprint

2 周、单语料 + 单工具集、不接线上写权限、只做一条机制（编译或可逆性门，二选一）：

1. **第 1–3 天 · 定口径**：锁 token（每问总量）、伤害（轨迹级 HSR 或 prevented harm）、审批（分钟/次）三个口径；把单价表建出来，缺项标「待填」。
2. **第 4–6 天 · 埋点**：接 per-query 或 per-decision 账本，回放 7 天历史流量（或 200–500 条历史决策），出动作混合与基线 token/时延/轮次。
3. **第 7–8 天 · 量分布**：编译侧抽 100–200 问 smoke 估 `p_h` 与 miss penalty，判门另按 1,600–2,000 条 shadow 的 95% CI 下界（见 [compilation §p_h](../../03-knowledge/compilation/mechanism.md#p_h-calibration)）；护栏侧统计保留率/审批率，抽 100 条 blocked 标 false-veto。
4. **第 9–10 天 · 算数**：算 `p_min`（用自己实测的 `c`、`Q`）或画 harm–approval 前沿；悲观/基准/乐观三列敏感性表替代点估计。

**交付物**：一页账本 schema + 基线分布（`p_h`/miss、时延、审批、动作混合）+ `p_min` 对照表 + 单价表（含缺口清单）+ build/buy/不做 memo 草稿。

**出口（go/no-go）**（下面前两条的阈值是工程门槛，不是论文实测，`推测`）：
- **go**：`p_h` 的 95% CI 下界 > `p_min` 或前沿点优于现状，时延/审批在预算内，单价表缺口 ≤2 项 → 进第二 sprint（shadow/A-B）。
- **no-go**：`p_h` 的 95% CI 下界 ≤ `p_min`，或 `p̂ĉ` 的 selective-risk AUC 未显著低于 `p̂`，或 false-veto >5% → 停，结论回写 [frontier](./frontier.md) 的 G1–G3。
- **不出结论**：单价缺项 >2，或样本量不足以判 HSR（稀疏事件，2 周 log-only 不够）→ 补数据，不硬判。
- **样本未到**：编译侧 shadow <1,600–2,000 条 → 只出 smoke 与采样计划，不判 go/no-go；护栏侧按 200–500 shadow 的预登记门槛另判。

### 客户指标/V3

- **受益者**：负责批预算的人（平台/经费 owner）与业务线（少审批、少事故）。痛点不是「本体不好」，是**无法证明投入回本**，于是要么全上、要么全不上。
- **指标（两类）**：
  - 机制收益：每千问 query-equivalent、p95 时延、审批/千次、false-veto、prevented harm。
  - 尺子本身：**误上线率**——上线后一个季度内被回退或停用的机制数（目标 0，`推测`）；**决策返工率**——因口径/单价缺失而重开的 build 评审次数（`推测`）。
- **反事实**：不做账本 → 继续用「平均 −38%」或单一 HSR 决策；不做实验 → 由 vendor demo 决定采购。
- **试点成功**：2 周内对一个机制给出**可复算**的 go/no-go 材料（样本未到 1,600–2,000 时只出 smoke 结论，不判 go/no-go）——账本、`p_h` 抽样、公式、单价表同档，同一口径能重算出同一区间，且事后一个季度无回退。`推测`（「可复算」是本页定义，无外部出处）
- **试点失败**：sprint 结束时仍拿不出 `p_h`/审批率分布，或单价缺项多到结论只能靠假设。
- **停止线**：账本维护人时 > 它避免的返工/事故价值（`推测`，无实测；按季度重估）。

### 反例

- **公式精度可能不如直觉。** `c` 和 `Q` 都要自己测，miss penalty ±1.5pp 就让门槛在 0.4–3.6% 间移动；若真实 `p_h` 落在 5–20%，门槛根本不 binding，算出来的只是一层数学装饰（CAI 自己说 43% 是反推值）。
- **`J(m)` 算不动。** CASEL 的 `γ_m` 是假设，不是测量；没有 γ 就没有 `J(m)`，「按前沿选点」退化成「按审批率选点」——仍是判断，不是计算。
- **账本本身可能不划算。** 只跑 1–2 个机制时，埋点 + 单价表 + 标注的人日可能高于它避免的一次错误采购；本页价值随机制数量增长，不随单个机制增长。
- **F1 是事后解释，不是事前预测。** 「位置 × 成本 × 使能」能解释某机制为何回退，但不能在开跑前判断哪个机制值得；拿它做选型只会得到「都对」的结论。
- **可能只是三篇论文的共同偏差。** CAI 是作者评自家 RAGFlow，CASEL 是模拟，POLAR 是单一合成基准，三者的部署层观测都是空的（G1）；尺子建在这三篇上，会继承同样的乐观或悲观偏差。

<a id="landscape-2026-11"></a>
## 生产落地图景（2026-11）

> 2026-11-12 为 [05 落地现状](../../../deliverables/05-production-landscape/README.md) 补的实证页。问题不是「本体有没有用」，而是「谁在生产里跑、什么形态/规模、成本收益、靠谱与否有无证据」。
>
> **证据分级**（沿用 05 README 的方法，但准入仍按 CHARTER §4）：A = 一手工程复盘/公司生产报告，披露规模 + 成本或失败/限制；B = 具名组织在生产中使用/采用，有独立信号；C = 厂商产品页/白皮书/赞助调查/二手转述，只作线索。**只有 `admitted`（含 probation）能进「发现」；C 只进「供给面线索」，不撑判断。**

### 证据台账（截至 2026-11-12）

| 来源 | 日期 | 类型 / 准入 | 它证明什么 | 它不能证明什么 |
|---|---|---|---|---|
| [中泰证券 QCon 2026](../../../src/web/qcon-2026-zhongtai-ontology/qcon-2026-zhongtai-ontology.card.md) | 2026-09-02 | talk / `admitted` | 900 万客户、6,000+ 指标的券商环境；本体语义层（指标五要素、7,000+ 同义词）；生成/执行分离；三个退役判例；权限到属性级 | 单券商；议题页只有摘要，无成本/失败率/对照；不能外推全行业 |
| [中泰证券 CCSA TC601 案例](../../../src/web/modb-2026-zhongtai-ontology/modb-2026-zhongtai-ontology.card.md) | 2026-10-15 | engineering / `admitted` | 9,137 知识目录、6,503 指标文档、2,622 表、12 万+ 血缘；DataAgent 生产；业务本体仍在信用业务验证 | 规模是知识资产数，不是本体实体/查询量；无成本/准确率；单公司 |
| [Snowflake 内部 context layer](../../../src/web/snowflake-context-layer-2026/snowflake-context-layer-2026.card.md) | 2026-08-17 | engineering / `admitted (probation)` | 5,600 员工、320k 查询/月；semantic views 版本化/CI；朴素语义视图延迟与预聚合维护爆炸 | 单公司自述；无外部采用；准确率/成本缺失 |
| [Sigma 2,883-model semantic layer](../../../src/web/sigma-semantic-layer-2026/sigma-semantic-layer-2026.card.md) | 2026-10-27 | engineering / `admitted (probation)` | 2,883 dbt 模型、63 job、6 region；语义层版本化/列级暴露/PII guardrail；dbt Summit 2026 | 供应商自己跑自己的产品；无成本/失败/准确率；不是本体推理 |
| [Netflix 本体驱动可观测性](../../../src/web/netflix-ontology-observability-2026/netflix-ontology-observability-2026.card.md) | 2026-10-16 | engineering / `admitted` | OWL/SHACL/SPARQL + 自建 QuipuDB；49,000 目录/2B 请求/日/38M 日志/秒；12 namespace | 无成本/收益；自建图存储是例外；假设有时错 |

**证据配比（谁在证明什么）**：5 条 admitted/probation 里，严格意义的 OWL/对象本体只有 **Netflix**（可观测性领域、自建图存储）；**中泰**是治理语义层已生产、业务本体在信用业务**试点**；**Snowflake / Sigma** 是 BI/数仓语义层（指标、维度、verified query），不是本体推理。所以「本体在生产」的 A 类证据是 **1 条领域专用 + 1 条试点**，不是 4 条。把「语义层落地」读成「本体落地」会高估现状；这也是 05 必须先讲清配比、再讲形态的原因。

**供给面线索（C，未过门，只作「有方案」的证据，不撑采用/效果）**

| 线索 | 日期 | 它是什么 | 为什么不能撑结论 |
|---|---|---|---|
| [Palantir 2026-10 公告](https://markets.businessinsider.com/news/stocks/palantir-announces-delivery-of-critical-sovereign-ai-outcomes-to-big-customers-1036651855) | 2026-10-21 | Foundry/AIP/Ontology/Apollo 在 L3Harris、McCarthy、Nvidia、Ondas/Regna、Tampa General 等落地 | 公司新闻稿；无规模/成本/失败；客户名单不等于效果 |
| [阿里云 PolarDB 本体知识平台](https://www.alibabacloud.com/help/zh/polardb/polardb-for-postgresql/what-is-ontology-knowledge-platform) | 2026-10-21 | 数据库内嵌本体建模 + LLM 自动生成 + GraphRAG + Agent skills；灰度；按组件规格计费 | 厂商产品文档；无客户/规模/失败；只证产品存在 |
| [阿里云 Context0 本体知识库](https://help.aliyun.com/zh/polardb/polardb-for-xscale/context0-build-ontology-knowledge-base) | 2026-09-23 | 知识库级 schema：类型≤100、关系≤300、每类型≤50 属性；版本、证据、自然语言抽取指令 | 同上；且是「薄本体」产品上限，不是企业级本体 |
| [腾讯 Topbase](https://zhuangxiaoyan.blog.csdn.net/article/details/155427520) | 2025-12-02 | 226 类概念、1 亿+实体、22 亿三元组；微信搜一搜/信息流/问答 | **G1 超窗**（2025-12），只能作背景；无成本/失败；二手技术文 |
| [Ant TuGraph](https://github.com/TuGraph-family/tugraph-db) | last push 2026-05-11 | 开源图数据库；Apache-2.0；1,768 stars/42 contributors；LDBC FinBench/金融风控 | `last_push` < 2026-06-01，G1 失败；图数据库≠本体平台；无 2026 生产报告 |
| [Atlan: KG pitfalls](https://atlan.com/know/ai-agent/knowledge-graph/enterprise-knowledge-graph-pitfalls/) | 2026-09-10 | 「<15% 企业 KG 项目过 pilot」；组织/技术/经济三类失败 | 厂商二手综述，引用 Improvado 2026 synthesis；原始统计未核；只能当线索 |

### F7 · 生产中的本体以「底座 + 薄本体」为主，不是自建本体塔

**判断**：在我们能核到的 2026 生产/试点案例里，本体/语义层都跑在已有底座上——数仓语义层（Snowflake）、dbt/Dagster 语义工程（Sigma）、治理知识库/DataAgent（中泰）。阿里 PolarDB/Context0 与 Palantir 只有产品文档/客户名单（C），不计入生产案例。**没有发现「从零自建通用本体平台」的公开成功案例；唯一例外是 Netflix 自建 QuipuDB（领域专用图存储，不是通用平台，且无成本数）。**

**证据**：
- 中泰明确写「本体建设不必从零开始，指标治理、元数据与血缘是本体最重要的输入」；生产先用治理语义层，业务本体仍在信用业务验证。
- Snowflake 的 semantic views 长在数仓/BI 上；Sigma 的语义层长在 dbt/Dagster/仓库上；阿里的本体平台长在 PolarDB 上，且 Context0 把本体限制在知识库级（类型≤100、关系≤300）。
- Palantir 是重型平台路径：客户买的是 Foundry/Ontology/AIP，不是自己造本体引擎。

**限定**：这是**公开案例的选择**，不是行业普查；「底座」包括公司自研平台（中泰的 DataAgent、腾讯 Topbase），所以不能把「平台承载」读成「一定买商业产品」。反例搜索（自建本体塔的成功案例）未找到，不等于不存在。

**等级**：`已核`（公开证据的选择）；推广到「所有企业」是 `推测`。

### F8 · 失败模式集中在语义定义、权限与维护

**判断**：生产案例披露的坑，集中在**语义定义、维护、权限**，不是图查询性能：影子实体（表→实体自动映射）、口径漂移（同名不同源/全半角）、权限按人特批、聚合结果定位到个人、朴素语义视图延迟、预聚合管线维护爆炸。

**证据**：
- 中泰：三个退役判例（指标值顶点、万能组织类、任职承接）；「数据库表一键转实体」产出影子实体，源表一变全错且无人知道；权限按人特批、聚合泄露。
- Snowflake：把 semantic view 指向十亿行原始事件表，每次提问 crawl/join，延迟巨大；自建 Dynamic Tables 预聚合后维护量爆炸。
- Sigma：语义层要版本化、PII/SQL guardrail、列级暴露控制，否则每个 AI surface 各说各话。
- 反例线索：Atlan 的「<15% 过 pilot」把失败归为组织/技术/经济三类（ontology drift、schema rigidity、entity resolution、ontology tax），但它是厂商二手综述，只能作线索，不能当统计。

**限定**：这些是工程报告里的失败形态，不是失败率；不能推出「图引擎不重要」，只能说「公开复盘里它不是主诉」。

**等级**：`已核`（多案例工程报告）；「多数项目失败于此」是 `推测`。

### F9 · 成本拐点降的是启动/抽取成本，不是定义治理/维护成本

**判断**：LLM 让「从数据/文档里抽本体、生成候选 schema、写摘要/别名/问法」变便宜；但没有降低「口径由谁定、同义词谁维护、权限怎么算、版本怎么退役」的成本。**真正的重活从建模前移到语义治理。**

**证据**：
- 中泰：6,503 个指标文档、9,137 份知识目录、12 万+ 血缘；7,000+ 同义词；LLM 只补充业务摘要/别名/问法，技术事实由程序整理，模型解释必须过来源证据核验。
- Snowflake：5,600 员工/320k 查询的语义层要版本控制、peer review、CI/CD、eval、materialization；早期预聚合管线越扩越难维护。
- Sigma：2,883 个模型、63 个 job、6 个 region 持续 build/deploy；语义层是长期软件工程，不是一次性建模。
- 阿里：PolarDB/Context0 用 LLM 自动分析数据结构、样本发现生成候选 schema，把「建」的门槛降下来；但 Context0 仍要求显式版本、应用、权限、证据。

**限定**：没有一条来源给出 TCO/人月/金额；这些都是**工作量代理**（文档数、模型数、job 数、同义词数），不能当成本曲线。成本拐点是 `推测`。

**等级**：`推测`（方向有多个工程信号，缺成本数）。

### F10 · 公开证据呈「美国偏语义层/上下文层、中国偏大厂平台/内部图谱」的不对称

**判断**：2026-06 后的公开生产写作里，美国更多是**语义层/上下文层**的规模与失败披露（Snowflake、Sigma、dbt/AtScale、Palantir 客户公告）；中国更多是**大厂平台产品**（阿里 PolarDB/Context0、蚂蚁 TuGraph/GraphRAG、腾讯 Topbase）和**单点金融实践**（中泰），公开的独立生产复盘、成本/失败披露更少。

**证据**：
- 美国：Snowflake/Sigma 给出用户数/模型数/失败形态；Palantir 给出客户名单；dbt/AtScale 给出生态讨论。
- 中国：阿里有 2026-09/10 的产品文档（C）；中泰有 2026-09/10 的会议+标准工作组案例（A）；腾讯 Topbase 的规模数是 2025-12（G1 超窗）；蚂蚁 TuGraph 的 `last_push` 是 2026-05（G1 失败）。**逐平台检索（2026-11-12）：阿里 Context0 / 蚂蚁 TuGraph / 腾讯 DataBuddy / 华为 DataArts / 京东 Oxygen 五家，2026-06 后 0 条「具名客户 + 可追一手」**；能过门的客户侧材料集中在海致星图/星环/NebulaGraph/Neo4j 与三家农商行自述（signal）。
- 中国不是没有东西：CCSA TC601 WG15 已立项《本体建模技术要求》《本体智能平台技术要求》《知识管理能力成熟度模型》等标准，说明生态在制度化；但标准只定词/合格性，不证效果。

**限定**：这是**公开证据的描述**，不是产业能力排序；中国材料受公开意愿、语言、渠道影响，不能把「没公开」读成「没做」。

**等级**：`已核`（证据基座描述）；「美国更成熟/中国更落后」是 `推测`，且不是本页要回答的问题。

### 对 05 的四句话

1. **形态**：生产里跑的是「底座 + 薄本体/语义层」，不是自建本体塔；重型平台（Palantir）与轻语义层（Snowflake/Sigma/dbt）是两端，中间是行业平台（阿里 PolarDB/Context0、中泰 DataAgent）。
2. **规模**：公开可核的规模从「2,883 个语义模型/6 个 region」到「5,600 员工/320k 查询/月」到「900 万客户/6,000+ 指标/7,000+ 同义词」，但都缺同一口径的成本与效果。
3. **靠谱**：有条件——定义有 owner、执行确定、权限可计算、证据不足能停；失败形态是影子实体/口径漂移/权限旁路/延迟，不是图查询。
4. **缺口**：没有一条同时披露「规模 + 成本 + 失败 + 独立印证」的 A 类全量案例；中国大厂缺 2026-06 后的外部采用/成本/失败证据。05 应把这个缺口写成主线，而不是用厂商材料填满。


<a id="okf-2026-11"></a>
## OKF / Wiki 底座选项（2026-11）

> 2026-11-12 补。问题：直接上完整本体太贵，能不能把 Wiki/OKF 当底座选项之一、需要时再衔接本体？本节只做**定义、证据与升级判据**，不写实施 recipe。
>
> **一句话**：OKF 是 Google 的开放知识格式（v0.1 2026-06-12，v0.2 2026-07-24），把 Karpathy 的 LLM Wiki 模式规格化为可交换的 Markdown bundle；它是**知识容器**，不是本体——能解决可读/可审/可版本化/可溯源，不解决约束、推理、查询执行、策略/权限。它与本体之间是**非对称投影**：本体→OKF 可机械投影但丢语义；OKF→本体是有损草稿 + 关系定型人审。

### 它是什么（Google 官方定义）

- **格式，不是服务**：一个 OKF bundle 是“一个目录的 markdown 文件”；一个 concept 一个文件，文件路径就是 concept 的 id；不需要 SDK/runtime。
- **frontmatter**：v0.1 必填只有 `type`，约定 `title`/`description`/`resource`/`tags`/`timestamp`；正文是 markdown；concept 之间用普通 markdown 链接，链接图就是知识图；`index.md` 做渐进披露，`log.md` 做历史。
- **v0.2 信任信号**（2026-07-24，全部 opt-in）：`sources`（含 author/usage_count/last_modified）、`generated`/`verified`（谁生成、谁独立确认）、`status`/`stale_after`（生命周期/过期）、`attestation`（数值是否按约定计算）。它记录信号，不给“可信度分数”。
- **来源**：Google Cloud 博客 2026-06-12 / 2026-07-24；规范与示例在 `GoogleCloudPlatform/open-knowledge-format`；Karpathy 的 LLM Wiki gist 被官方明确引用（AK = Andrej Karpathy）。

### 它不是什么

| 它像 | 但它不是 |
|---|---|
| 目录 + 文件 + 链接 | 不是 OWL/RDF 本体：没有 class/property 的公理语义 |
| frontmatter 有 type/tags | 不是 schema：不保证类型/基数/关系约束 |
| 链接成图 | 不是可查询的 KG：没有 SPARQL/图查询执行 |
| v0.2 有 verified/freshness | 不是策略/权限：不执行 allow/deny，不做行/列/属性级授权 |
| 可被 agent 读 | 不是推理：不做 entailment/一致性检查 |

**关键区分**（社区 ADR 的说法）：OKF concepts 是**声明性知识**，很多消费者读；本体/语义层是**可执行语义**，机器要求值/校验/拦。两者可以组合，不能互相替代。

### 证据台账

| 来源 | 日期 | 类型/准入 | 它证明什么 | 它不能证明什么 |
|---|---|---|---|---|
| [Google OKF v0.1](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) · [卡](../../../src/web/google-okf/google-okf.card.md) | 2026-06-12 | 官方博客 / `admitted`（定义） | OKF 是开放的 markdown+YAML 格式；一概念一文件；受 Karpathy LLM Wiki 启发 | 采用/效果；不是标准组织标准 |
| [Google OKF v0.2](https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals) | 2026-07-24 | 官方博客 / `admitted`（定义） | 加 provenance/trust/freshness/lifecycle/attestation，全部 opt-in；“advisory signals, not access control” | 信任信号≠真实性；仍需 producer 审计 |
| [Knowledge Catalog 集成](https://cloud.google.com/blog/products/data-analytics/scale-okf-bundles-across-an-organization-with-knowledge-catalog) | 2026-08-26 | 官方博客 / C（产品能力） | OKF bundle 可映射成 Catalog Entry，继承 IAM；okf Aspect 13 字段；Acme 9 leaf/17 entries | 客户采用/规模/效果；sample 是合成 |
| [中泰证券 CCSA 案例](../../../src/web/modb-2026-zhongtai-ontology/modb-2026-zhongtai-ontology.card.md) | 2026-10-15 | engineering / `admitted` | 用 OKF 组织 9,137 知识目录/6,503 指标文档/2,622 表/12 万+ 血缘；三泳道+证据门禁；业务本体验证中 | 业务本体全量；成本/准确率；单公司 |
| [社区 ADR：不把 OKF 用于 skills](https://github.com/laurigates/claude-plugins/blob/main/docs/adrs/0021-open-knowledge-format-mapping-not-adopted.md) | 2026-07-12/11-02 | 工程决策 / C | 声明性知识 vs 可执行能力的区分；OKF 适合多消费者知识，不适合单 runtime 过程 | 不是生产采用；单项目 |
| [OKF interop 批评](https://raw.githubusercontent.com/chrisgagne/grounded-forge/refs/heads/main/docs/architecture/okf-interop.md) | 2026-07 | 工程文档 / C | OKF 标准化容器，不标准化 producer/审计；“conformant bundle of confabulated claims validates cleanly” | 不是采用/效果；单项目 |

### 从 OKF 到本体：两个方向、一条缝

> 2026-11-12 重写。旧版把“可映射”写成“可以升级”，并混入了无源材料。新版按**方向**拆开：投影（本体→OKF）与上提（OKF→本体），只写有来源的部分。

**方向一：本体 → OKF（投影，可机械完成、有损）**

- 映射规则：`type` → 类名、`resource`/IRI → 资源链接、`tags` → SKOS 词、typed property → 未命名 Markdown 链接（关系类型在正文里丢失）。
- 三份独立实现的说法：
  - [Linked.Archi](https://meta.linked.archi/docs/practice/okf-open-knowledge-format/)（2026-07-17，C）：投影 “mildly lossy”，`am:realizes` 压成 untyped link；但 “for retrieval and progressive disclosure that is exactly enough”。
  - [Atlas](https://github.com/AtlasDevHQ/atlas/blob/main/docs/research/okf-interop-spike.md)（2026-07-02，C）：导出 “near-total”，但 “what foreign consumers **lose is semantics, not data**”；表白名单/运行时执行没有 OKF 对应物。
  - [GMEOW](https://github.com/Blackcat-Informatics/gmeow-ontology/blob/main/docs/okf.md)（2026，C）：OKF 是 “**LOSSY down-projection**”，只带 flat term surface；OWL 公理/RDF-star/对齐图留在 canonical 源。
- 结论：投影可以全量，但**丢的正好是语义**（关系类型、公理、约束、执行）。等级 `已核（三份工程文档一致）`；不外推为生产规律。

**方向二：OKF → 本体（上提，有损草稿 + 关系定型人审）**

- `type` → OWL class、`resource` → IRI、`tags` → SKOS concept 可以机械映射。
- **Markdown 链接没有类型**：要把 `[Customer Management]（…）` 变成 `am:realizes`，必须“作者提示或人审确认的推断”（Linked.Archi 原话：author-supplied hint or a human-confirmed inference）。Atlas 的 import 直接叫 “useful but genuinely **lossy draft generator**”，并把导入的 metric SQL 标 `okf.unverified_sql`，不让它静默升格为权威 metric；GMEOW 的 lift 要求封闭 `okf:` profile，未知键硬失败。
- 结论：上提是**草稿生成 + 人工定型**，不是读一遍就得到本体。等级 `已核（三份工程文档一致）`。

**这条缝：关系定型**

- 三份实现都指向同一处：OKF 的链接只断言“有关系”，不断言“什么关系”；关系类型/基数/方向在正文里。Linked.Archi 把它命名为 “the **relationship-typing gap**”，并说这是 Information 层到 Knowledge 层的缝。
- 这不是 OKF 的缺陷，是它的设计（consumer 不得因未知 type/坏链拒绝）。但它是**上提成本的主要来源**：文档越多，需要人审的链接越多。

**什么映射不了（分三档，不再一句“六类”）**

| 档 | 项 | 依据 | 能否补 |
|---|---|---|---|
| 规范明确不做 | 固定类型分类法、存储/查询基础设施、替代领域 schema | SPEC v0.2 non-goals（已核） | 要另建 ontology/semantic layer |
| 规范明确没有 | 执行（OKF 记录计算与检查方式，**never executes**）、ACL/策略（“advisory signals, not access control”） | SPEC v0.2 / v0.2 博客（已核） | 要另接执行/策略层 |
| 实现/分析 | 形式约束（SHACL/OWL 公理）、推理、关系类型/基数、身份粒度、as-of 时点 | 三份实现（C）+ W3C 标准卡（已核） | 要建模 + 人审 + 版本化 schema |

**迁移证据：两个方向都有人做，但没有“完成迁移”的案例**

- **本体先行（只有 `signal`）**：[SCIMIN-CRM/SMW](https://ceur-ws.org/Vol-4293/paper50.pdf) 描述 OWL 本体 + Semantic MediaWiki；LLM 只产候选标注，自动校验（domain/range、datatype、hallucination）+ 专家 HITL 后才同步生产。**判 `signal`**：承建方写自己的 demonstrator，G3 无独立信号，无量化/规模/成本。Kunstenpunt 是“数据标准先行、再并库进 Wikibase”（`signal`，单机构）。
- **OKF 先行（有生产，但下一跳未完成）**：中泰用 OKF 作权威源/交换格式，图数据库/对象关系写在后续规划，业务本体仍在信用业务验证（[卡](../../../src/web/modb-2026-zhongtai-ontology/modb-2026-zhongtai-ontology.card.md)，`admitted`）。
- **完成迁移**：截至 2026-11-12，公开渠道**没有找到**任何组织披露“OKF/Wiki → 本体”的完成案例（有路径、时间线、成本、失败）。这是检索阴性，不是“不存在”。

**“OKF 会自己长成 ontology”是错的**：它不会自动长；要显式的上提工程（关系定型 + 人审 + 版本化 schema）。Linked.Archi 也明说两者 “neither is an evolution of the other”，只是同一阶梯的相邻层；它给出的路径是“先 OKF 捕获，再把高价值域提升到图”，这是**设计建议**，不是观测到的迁移。

### 毕业判据：W0 → W1 → W2 → W3（设计判据，`推测`）

> 这一节是**设计判据**，不是观测到的“毕业路径”；没有一条公开案例按这个阶梯走完。05 只引用 3 条信号，不复制整表，也不要把“判据”写成“已验证路线”。

| 层 | 形态 | 能做什么 | 典型失败 | 升级信号 |
|---|---|---|---|---|
| **W0** | 纯 Wiki/文档 | 人读、搜索、审阅 | stale、无 owner、口径漂移 | 同一概念多页面；开始要跨页关系 |
| **W1** | OKF/结构化 Markdown | 多消费者读、版本化、来源/信任/新鲜度 | 链接成图但无约束；agent 写库 trust 崩 | 需要约束/权限执行；多 agent 要稳定 schema；跨页关系查询 |
| **W2** | 轻本体/语义层 | 概念/关系/约束/版本/权限；可查询/校验 | 维护成本；影子实体；权限旁路 | 跨系统对象/动作；高价值应用；重型平台 |
| **W3** | 重型本体平台 | 对象/关系/动作/权限/应用一体 | 平台费/实施重/锁定 | 不适合多数团队 |

**可观测的毕业信号**（命中 2 条以上再升级）：
1. 同一概念在 ≥3 个页面/文档里重复，且已有两个“官方版本”。
2. 业务问题需要**跨页关系查询**（不是关键词/向量检索）。
3. 约束/权限**必须执行**（不能只在 prompt 里提醒）。
4. ≥2 个 agent/应用需要**同一套稳定 schema**。
5. 维护人时持续上升，而问答质量不升（stale/冲突）。
6. 审计要求“这个数怎么算出来的”可追溯，而 OKF 只有来源/验证信号，没有计算链。

**Wiki/OKF 就够的场景**：文档/制度/runbook/术语表/来源索引；单团队、低冲突、只读；agent 只需要上下文，不需要执行。

### 反例与边界

- **OKF 不是“便宜的本体”**：它把“知识可读/可审/可版本化”做便宜了，但没把“语义可执行”做便宜；把 OKF 当本体买，最后还是要补约束/权限/查询。
- **agent 写库的信任问题**：v0.2 的 `verified` 是信号，不是保证；没有独立 producer/审计，conformance 不等于正确。
- **规模不是毕业信号**：本份没有可引用的规模基准；文件数能很大，但真正触发升级的是**语义/执行/权限**，不是文件数。
- **标准只定词**：Google 是公司，不是标准组织；OKF 是开放规范，不是 ISO/W3C 标准。引用时写“Google OKF”，不要写“行业标准”。

### 对 05 的用法

05 应把 OKF/Wiki 写成**底座选项之一**，不是本体的替代；可以是过渡，也可以长期并行。**只写证据，不写 recipe**：

- **写什么**：OKF 是什么（`admitted` 规范）；谁在用（中泰 `admitted`；京东海博/Kunstenpunt 只作 `signal` 线索，进 90 来源）；Google 的下一跳（Knowledge Catalog，C 级产品能力）；两个方向（投影有损、上提需人审，三份工程文档 C 级互证）；**没有完成 OKF→本体迁移的公开案例**（检索阴性，写日期与渠道）。
- **不写什么**：W0–W3 整表、6 条成绩信号、任何数字阈值——判据留本节（`推测`），05 只留 3 条可观测信号并指向本页/07。
- **不要写**：把 C 级实现文档写成生产采用；把“可映射”写成“会自动长成”；把“没找到”写成“不存在”。
- **对读者的唯一动作**：先用 OKF 统一“概念/术语/来源/owner/版本”；出现跨页关系查询、约束/权限要执行、多 agent 共用稳定 schema 时，再考虑本体/语义层；没有这些信号，长期停在 OKF 是合理选择（`推测`）。
- **对厂商的问题**：不要只问“支持 Markdown/OKF”，要问“能不能导出/映射到本体？关系类型谁定？能不能执行约束/权限？”

## 关联

- [findings](./findings.md) · [frontier](./frontier.md)
- [metrics](../metrics/README.md) · [trace](../trace/README.md)
