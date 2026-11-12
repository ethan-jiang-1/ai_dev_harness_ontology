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

## 关联

- [findings](./findings.md) · [frontier](./frontier.md)
- [metrics](../metrics/README.md) · [trace](../trace/README.md)
