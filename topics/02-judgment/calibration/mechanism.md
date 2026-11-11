# 校准 · 机制与实施

> 只写「怎么定阈值、怎么算、怎么停」。判断回 [findings](./findings.md)，gap/next 回 [frontier](./frontier.md)。

## 校准对象

判定回路（Ontology Catch 的口径）：

`产出 → 判定器分数/等级 → 阈值 → pass / flag → 修复/重试 → 复判`

- 每个 verdict 记四类：caught（错被 flag）、missed（错过）、false alarm（对被 flag）、correct pass（对通过）；重试后记 fixed / corrupted。
- 校准不是重训判定器，而是**在部署错误率 p 下选阈值**：阈值变 → catch/FA 变 → precision、重试成本、修复破坏一起变。
- 两篇 digest 只给单点/切片：Ontology Catch 是 checker on/off（不是阈值扫描）；OA-RAG 是四级序数（不是连续曲线）。要画曲线，得自己扫判定器分数（工程配方，`推测`）。
- 对 binary checker（Ontology Catch），阈值只是 on/off；对 scored judge / OA-RAG 等级，才是分数或等级的切点。

## 口径与公式

- `catch = caught / (caught + missed)`
- `FA = false_alarm / (false_alarm + correct_pass)`
- `precision(p) = p·catch / (p·catch + (1−p)·FA)`
- `flag_rate(p) = p·catch + (1−p)·FA`
- `per-1k cost = flag_rate × per-flagged cost × 1000`
- `增量 catch = catch(checker) − catch(空结果重试)`，同题同口径；优先看「有结果但答错」子集。

> p 是部署集错答案占比。论文只给 p=25% 假设下的人工故障 precision（57.1/72.3/93.7）；真实答案 precision 未直接给。报告必须带 p、catch、FA、n，否则 precision 不可比。公式假设同一判定器、同一错误构成下 catch/FA 不变；换域/换错误构成要重测。

## 数据/接口

- **审计集**：100–400 条分层抽样（digest 部署度量配方）；每条记 `truth`、`verdict/level`、`flag`、`repair_result`、`cost`。
- **输出记录**：`{threshold, p, catch, FA, precision, flag_rate, incremental_catch, fixed, corrupted, per_flagged_tokens, per_flagged_seconds, n}`；报 Wilson CI。
- **阈值**：按 FA 预算选，不按 accuracy 选；FA 预算示例 ≤10% 来自 digest 的采纳门/静态分析预算，agent 场景要自己定（`推测`）。
- **等级**：OA-RAG 的 entailed/supported/related/unrelated 当序数路由信号，不当概率；entailed 94.9%、supported 82.1%（Qwen Test 3 切片）只说明方向，不足以为每级定阈值。
- **反馈**：specific 28.3% fixed / 1.0% corrupted，generic 20.2% / 0.2%；C5 最终准确率差异未确立（0.2，CI −3.2~3.1）。未验证前先 generic 是风险默认，不是安全结论（`推测`）。

## 实施决策

- 先跑空结果重试基线，再叠 checker；只对「有结果但答错」算增量。
- 先定 FA 预算，再在预算内选 catch 最高的阈值；不追单一 accuracy。
- 报 precision 必须带 p；真实答案口径与人工故障 25% 口径不拼表。
- 接地等级只当路由/抽检触发器，不自动放行（`推测`）。
- 同一 artifact 既做 context 又做 checker 时，digest 只给探索性观察（catch 下降，机制未定）；不能据此写「同源 = 只能路由」的部署规则。要保守可降为弱信号 + 抽样复核（`推测`）。

## 组织/成本

- **运行**：per-flagged tokens/time；FA 触发重试，修复可能改坏正确答案。
- **标注/审计**：100–400 条分层抽样；人日未测，按团队实际记（不套用未测的人日估算）。
- **维护**：模型/域/本体变更后重测阈值；digest 配方是每季度重抽；是否适用未测（`推测`）。
- **修复破坏**：curated specific 1.0% corrupted vs generic 0.2%（flagged correct）；judge 分支修坏多于修好（checker/F6；数字见 Table 11）；工时未测。
- **误报 vs 漏检的贵贱**：02-L3 仍是 `推测`；digest 只有 corrupt 比例，没有工时/损失折算。不要写成已核。

## stop condition

- 空结果重试基线未测或未超过 → 不接 checker。
- 增量 catch <5pp（同题、有结果但答错子集）→ 停（digest 工程配方）。
- 采纳门：真实/人工混合集 catch ≥30% 且 FA ≤10%，per-1k 成本 ≤ 人工审核 1/3（digest 工程配方；`推测`）；FA >15% → 停。
- 接地等级通胀（entailed+supported >90%）→ 抽样校准，不自动放行（OA-RAG digest 配方）。
- 标注量不足以把 FA 的 CI 压到可接受范围 → 不自动放行（工程规则，`推测`）。
- 修复破坏的代价 > 拦下错误的收益 → 停（方向性判断；未测，`推测`）。
- 换域/换模型后未重测 → 不沿用原阈值（`推测`）。

## 第一个 sprint

2 周、单域 200 题（Ontology Catch 配方）：

1. 只上空结果重试，记 catch/FA/token/延迟基线。
2. 加 checker（或 grounding level），同题测增量 catch / 增量 FA / flag_rate。
3. 抽 50 条人工复核，记 fixed/corrupted 与工时。
4. 按 FA 预算与增量 catch 预写 go/no-go；增量 <5pp 或 FA >10% 则停。

> 200/50 是 digest 的配方；人日按团队实测，不套用未测数字。

## 客户指标/V3（`推测`）

- **受益者/痛点**：KG/agent 平台团队、数据治理/合规；痛点是误报导致返工、人工复核贵、阈值靠猜。
- **指标**：每千次产出的漏检/误报数、误报修复工时、人工复核率、per-1k token。
- **反事实**：不做校准 → 固定阈值/单一 accuracy；先测空结果基线。
- **V3**：200 题；成功 = 增量 catch ≥5pp、FA ≤10%、per-1k 成本 ≤ 人工审核 1/3；失败 = 增量 <5pp 或 FA >15%；停止线 = 年省复核 < 标注/维护。
- **反例**：错误率 p 未知；域移；等级自评；类别不平衡；级联放大（后两条未测）。

## 不适用/未吸收（G-X）

| 来源 | 本页吸收/处理 | 状态 |
|---|---|---|
| Ontology Catch（D-05） | 空结果基线 79.2/0（人工 fault）、2.5/0.1（真实答案）；增量 catch <5pp 停；per-flagged 成本；catch/FA 口径；p=25% precision 条件 | absorbed |
| OA-RAG（D-13） | 四级 grounding；94.9/82.1 切片；自评/未校准；>90% 通胀 stop | absorbed |
| ECE/可靠性图/isotonic/temperature scaling | 两篇 digest 均未测；本页不采用，不据此设门 | explained-not-applicable |
| 同源「只做路由」 | digest 仅有探索性观察（catch 下降，机制未定）；不写成部署规则 | explained-not-applicable |

## 关联

- [README](./README.md) · [findings](./findings.md) · [frontier](./frontier.md)
- [Ontology Catch digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-37809) · [OA-RAG digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-36335)
- [checker](../checker/README.md) · [evidence](../evidence/README.md) · [06 metrics](../../06-measure/metrics/README.md)
