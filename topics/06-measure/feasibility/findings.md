---
status: draft
updated: 2026-11-12
---

# 落地经济学 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `feasibility/Fx`。
>
> **2026-11-12 对账**：F2（CAI，E-14）/ F3（CASEL，E-15）仍 admitted，保持 `已核`；F4 引用的 POLAR 斜率已撤回（作历史示例），N&D 零结果仍 admitted。横切综合本就是 `推测`。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 值不值得 = 位置 × 成本 × 使能条件，不是本体质量 | 推测 |
| F2 | 编译有可算盈亏平衡；平均 −38% 不能当上线依据 | 已核 |
| F3 | 分配没有单一最优；按 harm–approval–cost 前沿选点（模拟，CASEL 主表 τ=∞） | 已核 |
| F4 | 没有一条适用于所有机制的能力曲线 | 推测 |
| F5 | 护栏 NPV 的分母是 do-nothing；缺单价只给公式与敏感性 | 推测 |
| F6 | 没有 γ 实测，不做多模式；先上静态 gate | 推测 |
| F7 | 生产中的本体/语义层都长在已有底座上，未发现从零自建本体塔的公开成功案例 | 已核（公开案例选择） |
| F8 | 生产失败集中在语义定义/维护/权限，不是图查询性能 | 已核（多案例工程报告） |
| F9 | 成本拐点降的是启动/抽取成本，不是定义治理/维护成本；有两条客户自述投入（<50 万；3 人×12 月），无公开 TCO | 推测 |
| F10 | 公开证据呈美国偏语义层、中国偏大厂平台/内部图谱的不对称；这是证据描述，不是能力排序 | 已核（证据基座）/推测（成熟度） |

## F1 · 位置 × 成本 × 使能

- **判断**：同一机制，在一种配置下是护栏，另一种是纯开销；值不值得不是本体质量。
- **依据**：POLAR 强模型回退；CAI 时延约束；N&D 答案不在文本里；EvoMemState 无训练信号退化成 prompt。
- **等级**：`推测`（横切综合，不是单篇实证）。
- **来源**：本页 + 各派 digest。

## F2 · 编译盈亏平衡

- **数字**：`p_h > 2% + c/(0.929Q)`；Q=1,000、c=10 → 3.12%；p_h=2.5% 仍亏 5.8 query-equivalent。
- **含义**：平均 −38% 不能当上线依据；要看 hit/miss 分布、时延、复用次数。
- **来源**：[CAI digest](../../../src/papers/2610.41172-context-as-infrastructure/digest.md) §4.3/§6.5；E-14。

## F3 · 分配前沿

- **数字**：CASEL 8.7% approvals/7.02% HSR；Risk-Menu 12.6%/5.82%；Consequence-Menu 13.8%/4.38%。都是模拟主表值，**CASEL 的 7.02%/8.7% 在 τ=∞（阈值关闭）下**；阈值规则另测（§VI-E），不能把 7.02% 当「开了阈值」的结果。
- **含义**：没有单一 HSR 最小；审批少 30% vs 多 1.2 点 HSR，是业务选择。
- **来源**：[CASEL digest](../../../src/papers/2610.36570-casel/digest.md) Table 2；E-15。

## F4 · 没有单一能力曲线

- **数字/方向**：POLAR 约束收益随基线能力下降（六点描述性拟合，斜率 −0.76/−0.67/−0.31，不能当阈值）；N&D 投影增益不随容量上升（H2 单向检验 p=0.85，是「未检出」不是「证明无效应」）；9B 带投影 0.737 > 750B 不带 0.672（区间约 0.3 宽）。
- **含义**：不能用一个「能力越强越有用/越没用」的曲线概括所有机制。
- **等级**：`推测`（横切综合；POLAR 斜率已撤回作历史示例，N&D 零结果仍 admitted；「所有机制」是外推，E-19 也把这条列为推测）。
- **来源**：[POLAR digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-08082) §4.2；[N&D digest](../../../src/papers/2610.11768-narrow-and-deep/digest.md) §4；E-12/E-13。

## F5 · 护栏 NPV 的分母是 do-nothing

- **判断**：分配/护栏机制也能写成 NPV；统一反事实只能是「不上护栏」，不是 Uncertainty-Menu/Risk-Menu。缺单价时只能给公式与敏感性，不能给点估计。
- **公式**（[CASEL digest](../../../src/papers/2610.36570-casel/digest.md) §6.5 E4，建模约定）：伤害节省/千次 `= (32.76% − HSR) × (1000/L) × incidents_per_harmful_trajectory × cost_per_incident`（L=20 动作/轨迹）；审批成本/千次 `= approval_rate × 1000 × minutes_per_approval/60 × hourly_rate`；12 个月 TCO = 建设 + 运行（`0.58 × 基线算力成本`）+ 审批人时 + 维护；`NPV_build = Σ(伤害节省 − 审批成本 + task success 收益)/(1+r)^t − TCO`；`NPV_buy` 同口径（RFQ + 集成 + 迁移/退出），`NPV_do_nothing = 0`，取 argmax；硬约束 task success 降 ≤2pp、false-veto ≤5%。
- **边界**：公式与决策线是工程配方，不是 CASEL 论文结果——论文只给模拟 HSR/审批/compute（0.486），没有金额。`minutes_per_approval`、`hourly_rate`、`cost_per_incident`、`value_per_success`、`r` 全空（G1–G3）。
- **等级**：`推测`（公式与决策线）；代入的模拟基线 32.76%/0%/29.48% 为 `已核`（Table 2，模拟）。
- **来源**：CASEL digest §6.5 E4、Table 2；[frontier](./frontier.md) G1–G3。

## F6 · 没有 γ 实测，不做多模式

- **判断**：多模式分配按 `J(m)` 选模式，前提是 `γ_m` 可估；γ 只有假设值、或 CI 分不开模式时，先上静态 `p̂ĉ` gate，不做 verify/sandbox/approve 路由。
- **依据**：CASEL 的 γ 是模拟假设（direct/verify/sandbox/approve = 1.00/0.42/0.15/0.04），审批疲劳也未建模；其工程 stop 是：`γ_verify` 的 CI 宽到分不开 direct/verify 的 `J` 差 → 只上静态 gate；校准量不足以把 `γ_verify` 压到 ±3pp → 停、补标注；`p̂ĉ` 的 selective-risk AUC 未显著低于 `p̂` → 停。
- **等级**：`推测`（门槛是工程线；γ 是假设、论文未实测，`已核` digest 自述）。
- **来源**：CASEL digest §4.1/§6.5 stop；[mechanism §stop](./mechanism.md#stop-condition)。

## F7 · 底座 + 薄本体

- **判断**：公开可核的 2026 生产/试点案例里，本体/语义层都跑在已有底座上；未发现从零自建本体塔的公开成功案例。
- **依据**：中泰「本体建设不必从零开始」；Snowflake semantic views 长在数仓；Sigma 长在 dbt/Dagster；阿里 Context0 把本体限制在知识库级（类型≤100/关系≤300）；Palantir 卖 Foundry/Ontology。
- **等级**：`已核`（公开案例的选择）；行业普查是 `推测`。
- **来源**：[mechanism §生产落地图景](./mechanism.md#landscape-2026-11)。

## F8 · 失败在语义层

- **判断**：公开复盘里的坑是影子实体、口径漂移、权限按人特批、聚合泄露、朴素语义视图延迟、预聚合维护爆炸；不是图查询性能。
- **依据**：中泰三个退役判例/影子实体；Snowflake 十亿行视图延迟与 Dynamic Tables 维护；Sigma 的版本化/PII/列级控制。
- **等级**：`已核`（多案例工程报告）；「多数项目失败于此」是 `推测`。
- **来源**：[mechanism §生产落地图景](./mechanism.md#landscape-2026-11)。

## F9 · 成本拐点在语义治理

- **判断**：LLM 降低抽取/候选 schema/摘要/别名/问法的成本；没有降低口径、同义词、权限、版本的治理/维护成本。
- **依据**：中泰 6,503 指标文档/9,137 知识目录/12 万+ 血缘/7,000+ 同义词；Snowflake 5,600 员工/320k 查询 + 版本/CI/eval/materialization；Sigma 2,883 模型/63 job/6 region。
- **等级**：`推测`（工作量代理，无 TCO/人月）。
- **来源**：[mechanism §生产落地图景](./mechanism.md#landscape-2026-11)。

## F10 · 公开证据不对称

- **判断**：2026-06 后美国更多是语义层/上下文层的规模与失败披露；中国更多是大厂平台产品与单点金融实践，独立复盘/成本/失败披露更少。
- **依据**：Snowflake/Sigma/Palantir 的公开材料；阿里 2026-09/10 产品文档；中泰 2026-09/10 会议+CCSA 案例；腾讯 2025-12、蚂蚁 TuGraph 2026-05 均 G1 超窗。
- **等级**：`已核`（证据基座描述）；产业成熟度排序是 `推测`。
- **来源**：[mechanism §生产落地图景](./mechanism.md#landscape-2026-11)。
