# 人类抽检包（5 digest + 5 topic）

> 目的：不是校对全文，只判断“值不值得实施/立项”。  
> 预计 60–90 分钟；每项 5–8 分钟；不需要读论文，读 digest/topic 即可。  
> 记录方式：每项给 `pass / fail / 不确定` + 一句话理由；最后写“是否同意 no-go”。

## 一、5 篇 digest（工程向）

| # | 论文 | 读什么 | 只问三个问题 | 记录 |
|---|---|---|---|---|
| D1 | CAI（2610.41172） | [digest](../../src/papers/2610.41172-context-as-infrastructure/digest.md) §6.5/§6.6 | ① 2% 门/样本量/stop 是否可执行？② 成本能否报批（缺什么）？③ 第一个 sprint 是否排得出？ | pass / fail / 不确定 |
| D2 | N&D（2610.11768） | [digest](../../src/papers/2610.11768-narrow-and-deep/digest.md) §6.5/§6.6 | ① 15/5 出口与 3 任务×2 模型是否匹配？② 投影 2–3 人日 vs 2 天是否可信？③ 可追溯性是否被夸大？ | pass / fail / 不确定 |
| D3 | Evontree（2510.26683） | [digest](../../src/papers/2510.26683-evontree/digest.md) §4.2/§4.3/§6 | ① Table 6 消融后，“规则贡献”是否被说清？② 1 万 raw→90 gap 的规模是否可接受？③ 安全 stop 是否可执行？ | pass / fail / 不确定 |
| D4 | Ontology Catch（2610.37809） | [digest](../../src/papers/2610.37809-what-does-an-ontology-catch/digest.md) §6.5/§6.6 | ① catch/FA 采纳门在你域是否合理？② per-flagged 成本是否够算？③ 空结果基线是否被尊重？ | pass / fail / 不确定 |
| D5 | SLB（2611.02395） | [digest](../../src/papers/2611.02395-solver-like-behavior/digest.md) §6.5/§6.6 | ① placeholders 契约是否可照做？② 50 题验收是否够？③ 闭源无 trace 的 audit-only 是否可接受？ | pass / fail / 不确定 |

## 二、5 个 topic（实施/价值向）

| # | topic | 读什么 | 只问三个问题 | 记录 |
|---|---|---|---|---|
| T1 | action-gate | [mechanism](../../topics/01-constraint/action-gate/mechanism.md) 的“实施与客户价值” | ① 会改变你哪个决策？② false-veto 指标是否可测？③ 你会先做 shadow 吗？ | pass / fail / 不确定 |
| T2 | checker | [mechanism](../../topics/02-judgment/checker/mechanism.md) 的“实施与客户价值” | ① 采纳门与 V3 是否是同一把尺？② per-1k 成本能否算？③ 你会先建空结果基线吗？ | pass / fail / 不确定 |
| T3 | generation | [mechanism](../../topics/05-produce/generation/mechanism.md) 的“实施与客户价值” | ① 可消费性闸门是否可判？② 四条路线是否过度合并？③ 你会先做 40 术语试点吗？ | pass / fail / 不确定 |
| T4 | feasibility | [mechanism](../../topics/06-measure/feasibility/mechanism.md) 的“实施与客户价值” | ① 8 个 V3 是否够立项？② NPV/账本是否可算？③ 你会先买“可算的机制”吗？ | pass / fail / 不确定 |
| T5 | metrics | [mechanism](../../topics/06-measure/metrics/mechanism.md) 的“实施与客户价值” | ① 单一分数评测是否会被替换？② 5 runs/噪声地板是否可执行？③ 你会先改评测口径吗？ | pass / fail / 不确定 |

## 三、四个判断（每项一句话）

1. **工程可实施**：这 10 项里，哪些能让一个工程团队明天列出第一个 sprint？
2. **客户价值**：哪些有可测指标/反事实，哪些只是“机制好听”？
3. **证据诚实**：有没有把 `推测` 写成 `已核`、把作者主张写成观测？
4. **go/no-go**：你同意当前 **对外交付 no-go、研究档案继续用** 吗？

## 四、签核

| 项 | 结论 | 理由（一句话） |
|---|---|---|
| 5 digest | pass __ / fail __ / 不确定 __ | |
| 5 topic | pass __ / fail __ / 不确定 __ | |
| 对外交付 | go / no-go / 条件 go | |
| 人类 reviewer | （姓名/日期） | |

## 五、怎么用结果

- 任何一项 `fail`：回到该子领域的 `frontier` 登记 residual，不阻塞其他项。
- 多数 `pass` 且有 3 个以上“会改变决策”：可把 report 从 no-go 改成**条件 go**（先做 1–2 个 V3 试点）。
- 人类抽检完成前，报告保持 **no-go**，不冒充已审。

## 六、当前建议

优先看 **CAI、N&D、Evontree** 和 **action-gate、feasibility**：这 5 项是当前 residual 与价值假设最集中的地方。

## 七、代办评审结果（2026-11-08）

> **性质**：用户授权 AI 代办评审，不是独立人类审稿；不能写“human sign-off”。  
> 判断依据：逐项读 digest §6.5/§6.6 与 topic 的“实施与客户价值”，并核关键数字。

| # | 项 | 结论 | 一句话理由 | 条件/缺口 |
|---|---|---|---|---|
| D1 | CAI | **条件 pass（仅试点）** | 门/样本量/stop 已可执行；但 `$/文档`、人日费率、judge 成本仍需自填，不能报批 | 先在 shadow 标定门；固定样本 1,600–2,000 条；补单价表 |
| D2 | N&D | **pass** | 15/5 出口、功效 caveat、成本/排期对齐、可追溯已限定；2 周试点可做 | 评估集构造人日需记实耗；3 任务只作方向性 |
| D3 | Evontree | **条件 pass** | Table 6 消融已收，gap 产率/规模已对齐；但 stop 的覆盖率分母、+1pp 噪声仍弱 | 先 3 seeds 标噪声；gap<300 才停；先跑 rule-free 基线 |
| D4 | Ontology Catch | **pass** | 空结果基线、catch/FA、per-flagged 成本、200 题试点都可执行 | 混合集比例/unknown 率需在试点定义 |
| D5 | SLB | **条件 pass** | placeholders/ codebook/样本量已写；但防泄漏条款、50 题功效仍不足 | 加“编号打乱/不得覆盖 VALUES/输出映射”；50 题只作方向 |
| T1 | action-gate | **pass（已修量纲）** | 实施决策/接口/成本/stop/V3 齐全；NPV 的 task success 项已改为 per-1k 调用 | false-veto 仍无标签；E4 单价缺 |
| T2 | checker | **条件 pass** | 空结果基线、catch/FA、per-1k、V3 都可执行 | 采纳门（30%）与 V3（+5pp）需统一成一把尺 |
| T3 | generation | **条件 pass** | 按消费位置选路线、40 术语试点、成本公式可执行 | 可消费性闸门比例阈值未定；客户结果未测 |
| T4 | feasibility | **条件 pass** | 账本/公式/8 个 V3 能支撑预算讨论 | V3 单臂；false-veto 无测量；单价表空 |
| T5 | metrics | **条件 pass** | 配置当系统变量、5 runs、噪声地板可执行 | 稀有事件样本量不足；分派表未验证 |

## 八、代办评审的 go/no-go

### 条件 go（仅内部试点/研究）

只启动 3 个试点，不对外承诺客户收益：

1. **action-gate shadow**：200–500 决策、100 blocked 标注、同轨迹配对；false-veto ≤5% 才继续。
2. **N&D K1→K2**：1 台设备、3 任务、先做 K1 命名+单位；K2−K1 ≥15pp 才建塔。
3. **Ontology Catch checker**：200 题、空结果基线 + data-derived check；增量 catch ≥5pp、FA ≤10% 才继续。

### No-go（对外交付/客户承诺）

- 没有客户现场基线、单价、事故成本；ROI 不可算。
- 人类独立抽检仍未做；本结果是“代办评审”，不能替代 human sign-off。
- CAI 全量编译、Evontree 训练、generation 四路线全做：暂不启动。

### 建议

- 先把 3 个试点跑成“可复算的 go/no-go”，再谈对外交付。
- 如果只能选一个：**先做 N&D 的 K1 命名+单位**——最便宜，且 K1 已拿最大一层增益（+54.6pp）。
