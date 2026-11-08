# 试点 playbook：90 天，只做三个

> 依据：全审 [report](../meta/full-audit/report.md) 的“条件 go（内部试点）/ 对外 no-go”。  
> 本 playbook 只重组已有 E/L，不新增判断；设计/阈值标 `推测`。  
> 实现产物在仓库外；实验协议见 [experiments](../experiments/README.md)。

## 0. 一句话

**别全线铺开。** 先做 N&D 的 K1 命名+单位，再做 action-gate shadow，再做 Ontology Catch checker；三个都跑出可复算的 go/no-go，再谈对外交付。

## 1. 90 天路线

| 周 | 试点 | 关键动作 | 出口 |
|---|---|---|---|
| 1–2 | N&D K1 | 3 任务、K0 vs K1、2 模型、3 seeds；单位/命名审计 | K1 ≥15pp → 不建塔；<5pp → 只说明命名不够 |
| 3–4 | action-gate shadow | 200–500 决策；100 blocked 盲标；同轨迹配对 | false-veto 上界 ≤5%、保留率 20–95% |
| 5–6 | checker | 200 题；空结果重试 vs +data-derived；50 条复核 | 增量 catch ≥5pp、FA ≤10%、成本 ≤人工 1/3 |
| 7–8 | 成本/决策 memo | 用 [cost-model](../meta/implementation/cost-model.md) 代公式；单价缺就只出 token 账 + 缺口 | 三个试点各一页“能算/不能算”；单价齐才 build/buy/不做 |
| 9–12 | 复盘/扩展 | 只扩跑通的；失败写 frontier；给失败项留重跑/扩样槽 | 是否进第二 sprint/对外 |

## 2. 三个试点的最小包

### N&D K1（最便宜，先做）

- **问题**：只做 K1，能否解决 primary trap？
- **数据**：3 个“答案在文本里”的任务；K0/K1 同设备、同 prompt、同 judge。
- **主指标**：primary-trap avoidance；次指标：element score、排障工时/次。
- **go**：K1 ≥ +15pp，≥2/3 任务同向、3 seeds 同向 → **不建塔**。
- **stop**：< +5pp → 命名不够；不据此说塔无效，下一步才测 K2。
- **协议**：[EXP-004](../experiments/EXP-004-narrow-deep-k1.md)

### action-gate shadow

- **问题**：可逆性路由的 false-veto 能否 ≤5%？
- **数据**：目标 500 条历史决策；blocked 过采样到 100 条双人盲标；只读状态投影。若保留率 95%，blocked 只有 25 条，必须扩 N 或补 logging，不能硬抽 100。
- **主指标**：false-veto（Wilson 95% 上界）；次指标：保留率、审批/千次。**shadow 不测 task success**；Stage 2 才测。
- **go**：false-veto 上界 ≤5%、保留率 20–95%、100 blocked、κ≥0.6。
- **stop**：false-veto >5% → 降 advisory/停；无状态投影 → 不做硬 veto。
- **协议**：[EXP-005](../experiments/EXP-005-action-gate-shadow.md)

### checker

- **问题**：data-derived checker 能否在空结果重试上提供 ≥5pp 增量 catch？
- **数据**：200 题；空结果重试基线；data-derived summary + declaration/pattern check。
- **主指标**：增量 catch（错误子集，不是 200 题）；次指标：FA、per-1k token/工时。
- **go**：增量 catch ≥5pp、FA ≤10%、成本 ≤人工 1/3；错误数 ≥80、复核 100–200 条、κ≥0.6。
- **stop**：增量 <5pp 或 FA >15%；语义错为主 → 换 LLM judge/人工。
- **协议**：[EXP-006](../experiments/EXP-006-ontology-checker.md)

## 3. 角色

| 角色 | 负责 | 不能兼 |
|---|---|---|
| 试点 owner | 协议、排期、决策 memo | 不能兼评分 |
| 领域专家 | 任务卡、ground truth、盲评 | 不能兼模型调参 |
| 平台 | 日志、状态投影、回放 | 不能兼业务结论 |
| 财务/风控 | 单价、事故成本、审批人时 | 不能兼技术选型 |
| 独立复核 | 抽检、κ、false-veto 仲裁 | 不能是试点 owner |

## 4. 数据与评审节奏

- 每周一次 30 分钟 gate review：只看主指标 + 缺口，不展开新 scope。
- 每 pilot 结束写 1 页 memo：go/no-go/不出结论 + 缺口 + 下一步。
- 所有数字带分母；所有 `推测` 标注；没有 CI 的收益不进 memo。
- 失败也登记：失败原因写进对应 `frontier`，不删。

## 5. 不要做

- **CAI 全量编译**：`$/文档`、人日费率、judge 成本没填，预算报不出；先 shadow 标定。
- **Evontree 训练**：3 seeds 噪声没标，+1pp 出口可能落在噪声内；先做 rule-free 基线。
- **generation 四路线全做**：只有 OntoDoc/Evontree 有 V3 形态；ReX/Peeling 客户结果未测。
- **对外承诺收益**：没有客户现场基线/单价/事故成本；V3 全部未跑。
- **把代办评审当独立人类**：本 playbook 的 go 是内部试点，不是 external sign-off。

## 6. 可引用的判断（不新增）

- 投影/知识供给：E-12（K1 最大层、H3 未支持、物理深度未测）；E-01（被测量的结构化工件无准确率增益）。
- 护栏：E-15（harm–approval–cost 前沿；τ=∞；NoRev=verify-only）；E-04（结构判据/能力反向）。
- 判定器：E-02（三源权衡；空结果基线；precision 口径）。
- 度量：E-18（配置当系统变量；54% 限定真实尝试）；C-03（按机制类型选尺）。
- 全部证据等级见 [conclusions](../topics/conclusions.md)；本 playbook 不升 E。

## 7. 回链

- 全审：[report](../meta/full-audit/report.md) · [value-trace](../meta/full-audit/value-trace.md)
- 试点计划：[meta/implementation/plan.md](../meta/implementation/plan.md)
- 成本：[cost-model](../meta/implementation/cost-model.md)
- 实验：[experiments](../experiments/README.md)
