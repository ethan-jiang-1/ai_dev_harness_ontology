# 失败归因 · 机制

> 只写「怎么诊断」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。
>
> 编号沿用 [digest ledger](../../../meta/full-audit/digest-ledger.md)：D-11 = [Diagnose digest](../../../src/papers/2610.35267-diagnose-workflow/digest.md)，D-15 = [Multi-agent digest](../../../src/papers/2610.36325-ontology-multiagent-diagnosis/digest.md)。

## 问题

一个任务失败了，最常见的归因是「模型不够强」。这个归因不可证伪，也不可操作——它给不出下一步动作。

Diagnose the Workflow（Before Blaming the LLM…）把 NL→本体接地 ABox DSL 的语义解析作为问题域：语法有效容易、语义充分很难，而反复出现的难点是结构性的。

## 五角色

| 角色 | 做什么 | 典型失败 |
|---|---|---|
| Input | 提供意图与上下文 | 歧义、不完整、隐含假设 |
| Generator | grounding 到本体符号，生成候选 | 选错类/关系/模板 |
| Output | DSL 表达式空间 | 模板不规则、覆盖缺口、near-match |
| Validator | 判断是否可接受 | 语法过、语义错；反馈弱 |
| Repairer | 修订/澄清/重生成/升级 | 非局部修复、重复重生成 |

## 七变量

| 变量 | 角色 | 高摩擦证据 | 重设计杆 |
|---|---|---|---|
| Input sufficiency | Input | 缺字段/隐含假设/歧义 | intent gate + clarification |
| Context availability | Generator | 缺术语说明/示例/约定 | 知识库精化 |
| Grounding complexity | Generator | 候选符号/模板太多 | 候选排序 |
| Template fit | Output | 断言模式不规则/重叠 | motif 库 |
| Vocabulary coverage | Output | 缺构造、被迫 near-match | 本体扩展 |
| Validation strength | Validator | 语义充分性不可确定性检查 | 分层校验 + 人审 |
| Error observability | Repairer | 失败无法定位 | repair trace |

**用法**：每个 case 填一张 7 行表（变量 / 证据 / 高摩擦？ / 重设计杆 / 负责人）。它不预测准确率或重设计效果，只把「语义不太对」拆成可改设计的位置。

## 例子：Bottom Hole Depth

输入只说「给 Bottom Hole Depth 钻井信号的语义」。实际输出 `DynamicDrillingSignal` + `HoleBottomLocation` + `DepthDrillingQuantity` + 两条断言；参考配置还要求 `PhysicalData`、reference frame、`HasDynamicValue`，并把 quantity/frame/location 挂在 physical data 上。

按七变量诊断：

- **Input**：没说要不要 physical data/reference frame——缺的是建模假设，不是一个槽位。
- **Context**：agent 无法推断「Bottom Hole Depth 需要 reference frame」。
- **Grounding**：本体里候选类/关系太多，要分多步选。
- **Template**：没有稳定 motif，模型每次现发明结构。
- **Vocabulary**：本例词汇够；缺词时会 near-match。
- **Validation**：语法/类型能过，语义充分性要专家。
- **Observability**：拒绝时说不清是输入、上下文、grounding、模板还是词汇问题。

## 非局部修复

原文把「非局部修复、重复重生成」列为 Repairer 的典型失败（D-11 digest §3.1）；把「校验弱 → 只能发现表面问题 → 修改扩散 → 引入新错误」串成一条因果链，是本页的推断，原文没有前后对照（`推测`）。

这条链若成立，根因在 harness（校验太弱），不在模型。但「换更强判定器往往比换更强模型更有效」「模型本来能改对，是判定给了它错误的方向」都是本页推断，D-11 未测（`推测`）。D-11 只明确说：错误主要来自结构，更强模型不一定补 template/vocabulary 缺口（digest §5 第 5 条）。

## 失效模式

- **把 position paper 当实证。** 单案例、无量化；七变量非正交/非穷尽。
- **profile 不一致。** 不同实践者可能给不同结果。
- **只填表不行动。** 没有负责人/重设计杆，表就只是描述。
- **变量交互。** 低 context 会放大 grounding；弱 template 会与 vocabulary 交互。

## 与本体 / 回路的关系

本体在失败归因里是 **诊断对象/重设计目标**；它不直接执行约束。被违反时通常没有即时信号，需要 trace/人审（`推测`，本页的架构判断；D-11 未测「有没有即时信号」）。

## 实施与客户价值（A3/A4）

> 读者是「要不要给失败归因立一个预算项」的人。上文的五角色/七变量只是诊断词汇，本身不产出结论；这一节写它改变哪个工程决定、需要什么数据、什么情况下必须停。**诊断框架本身没有效应量**：D-11 是 position paper（单案例、无量化）。带数字的阈值和参数凡出自 [Diagnose digest](../../../src/papers/2610.35267-diagnose-workflow/digest.md) §6.5 的，都是作者的工程线、不是实测；从 [Multi-agent digest](../../../src/papers/2610.36325-ontology-multiagent-diagnosis/digest.md) 引入的数字（映射率、Top-1/Top-3、case-level）是 Q4DX 单基准实测，不能外推到 NL→本体归因。未标来源的推算一律 `推测`。

### 实施决策

1. **模型替换的预算排在七变量表之后。** D-11 的作者明确说错误主要来自结构，更强模型不一定补 template/vocabulary 缺口（D-11 digest §5 第 5 条）；[Multi-agent digest](../../../src/papers/2610.36325-ontology-multiagent-diagnosis/digest.md) 给同向证据：curated 本体没有的诊断恒为 0（§5 第 6 条），本体覆盖封顶。`已核`（作者框架；D-15 只给出「覆盖封顶」的证据，没有错误分布实测，不能写成「诊断错误主要来自 KG」）→ **改变的决定**：模型升级/换 vendor 的评审必须附一张 15–20 例的七变量表；若高摩擦项集中在 Vocabulary/Template，先批本体/模板预算，不批模型预算。
2. **归因结论必须带 `owner` 与 `redesign_lever`，否则不进修复队列。** 「语义不太对」「模型弱」不是工单（F1 已核，框架）；表头字段里只有这两个能变成动作。**改变的决定**：triage/周会的工单准入标准——没有 lever 的 case 只能进观察池，不占修复排期。
3. **修复顺序锁死为 Input/Context → Grounding/Template → Validation 分层，语义留人审。** D-11 digest §6.4 建议先修前两项，理由是「成本最低、收益最直接」；这条理由无前后对照，只算作者判断（`推测`），而「digest 这样建议」本身是 `已核`（引文准确）。因此 **改变的决定**：第一个 sprint 不允许同时改本体、模板和模型；一次只动一组变量，否则同 batch 重测无法归因。
4. **验收看同一 batch 的前后对照，不看「换了个说法」。** D-11 digest §6.4 第 7 步要求重测同一 case，§6.5 要求预写 go/no-go。`已核`（引文准确）→ **改变的决定**：试点立项时先写死成功/失败阈值再开跑；跑完用同一批 case 重算，而不是换一批「看起来更好」的例子。
5. **追问/确定性评分只在「缺失项可枚举、候选集可枚举」时工程化；本体覆盖不足时先扩本体。** 七变量把 Input sufficiency 的杠杆写成 intent gate + clarification，把 Validation strength 写成分层校验 + 人审；Multi-agent 的分工是 LLM 只做语言层（抽取/提问/解释），排序/评分/更新交给确定性代码（D-15 §6.1 第 1 条；`已核` 单基准机制，迁移为 `推测`）。它给了追问接口的可运行版本（Yes/No 追问）和确定性打分（注意：打分是排序，不是接受/拒绝的校验），也给了天花板（本体没有的诊断恒 0；追问在 50% 完整度下把 Top-3 从 26.3 压到 24.2）。`推测`（医学鉴别诊断 → 失败归因的跨域类比，未测）→ **改变的决定**：先做表单式 intent gate 还是先做对话式追问——覆盖不足时不做后者。
6. **归因前先分桶（映射 / 候选截断 / 排序或覆盖），报告同报 Top-1/Top-3/case-level（F5–F7）。** ① 术语/症状映射失败（D-15：91.3% 成功、8.7% unmapped，失败留 trace、不进推理）应单列 `unmapped`，不能记成 Grounding 错；② 候选池截断（D-11 工程线 10–20）要先查「正确答案在不在池里」，再判排序；③ 报告同报 Top-1、Top-3 与 case-level（D-15 的聚合只 +2.5pp，个案 0.340→1.0，50% 完整度下 Top-3 反降）。`推测`（医学鉴别诊断的桶迁到 NL→本体归因，未测）→ **改变的决定**：case 表新增 `failure_bucket`、`pool_size`、`cutoff` 三个字段；没有它们，Top-1 错无法区分「没进池」和「排错」。

### 数据/接口

- **case 表**：每个 case 七行，字段 `case_id, variable, evidence, friction, redesign_lever, owner`（digest §6.5 的 schema）。`variable` 取七值；`evidence` 必须指到输入/输出/拒绝记录的行号或片段；`friction` 三档（low/medium/high）。本页补五个字段（`推测`，无出处）：`batch_id` 与 `retest_of`（否则决策 4 无法执行），`failure_bucket`（mapping/truncation/coverage/ranking/validation）、`pool_size`、`cutoff`（否则决策 6 无法执行）。
- **repair trace JSON**：`{case_id, retrieved_context[], candidate_symbols[], template_used, validation_results[], human_feedback, change, retest}`（digest §6.5）。没有它，repair 退化成重复重生成。
- **三个接口**：`intent_gate(input) → {sufficient|clarify, missing_slots[], questions[]}`；`validate(dsl) → {syntax, type, domain_range, template, semantic}`（前四层可自动，semantic 留人审）；`repair(trace)`。
- **映射接口（借 D-15，迁移为 `推测`）**：`map(term) → {canonical|fallback|unmapped, trace}`；先 canonical → alternatives → synonym/HPO fallback，映射失败保留 trace、不进推理。D-15 实测 91.3% 成功（77.3% 命中 SYMP + 14.0% HPO fallback）、8.7% unmapped；把 unmapped 当独立失败桶是本页的迁移用法（`推测`，F5）。
- **候选池接口**：`candidates(k=10–20)` + 显式 `cutoff`；阈值宁宽勿严（早期丢掉的候选后面回不来）。候选只从本体关系来、不自由生成；分批选，先 entity 再 relation/template（D-11 §6.1 第 4 步；D-15 §6.4 第 2 条）。两个数都来自作者工程线，不是最优值（D-11 §6.5、D-15 §6.1；`推测`）。归因时必须记录 `pool_size` 与 `cutoff`，否则 Top-1 错分不清是截断还是排序（F6）。
- **词汇缺口接口**：Vocabulary gap 暴露成 `ontology_extension_request`，不静默 near-match（D-11 §6.1 第 6 步；`已核` 框架）。`failure_bucket=coverage` 的 case 不占归因修复排期，进本体扩展队列（本页规则，`推测`）。
- **追问接口（借 Multi-agent，迁移为 `推测`）**：只问用户可观察、未报告、能区分候选的项；回答限 `{yes,no,unsure}`；上限 11 问（D-15 引 MedDialogRubrics：约 10–11 轮达峰，之后下降，不是说上限必须是 10–11）；回答进确定性评分，不进自由对话。
- **确定性排序（只在要建 triage 工具时）**：`composite = raw × (0.5 + 0.5·coverage)`，`score = composite × (1 + α·support_norm − β·conflict_norm)`；α=0.6、β=0.2 是原论文在 Q4DX 上的取值，不是归因场景的调参结果。每个分数必须回指 `evidence` 行与本体关系，否则不可审计（`推测`）。
- **口径（先定后测，换口径即不可比）**：下面五个公式是**本页自定的操作定义**，D-11 只给指标名（语义充分率/首次通过率/返工轮次/人审工时）和 κ 的用法，没给公式（`推测`；跨团队比较前先对齐）：语义充分率 = 通过语义人审的 case / 该 batch 总 case；首次通过率 = 第一轮即过语义人审的比例；返工轮次 = 同一 case 的 repair 次数；人审工时 = 分钟/case；κ = 两名标注者对同一 case 高摩擦项集合的 Cohen's κ。改动前的基线必须先测，否则没有反事实。
- **数据最小集**：输入、模型输出、参考输出、拒绝/修复记录（digest §6.5 第 1 步）。缺参考输出的域做不了语义充分率，只能做「专家是否接受」——要换指标，不硬套（`推测`，本页的工程判断）。

### 组织/成本

- **owner 四缺一即失效**（`推测`）：平台/评测 owner（表、trace、κ）、本体/领域 owner（Vocabulary 扩展、motif 库）、每个 lever 一个修复 owner、两名标注者（算 κ）。缺领域 owner 时 Vocabulary 行永远填 high 却没人改——这是表最常见的死法。
- **人日**（均 `推测`；前两项出自 D-11 digest §6.5，digest 已自标推测）：诊断 `15–20 case × 2 人 × 1–2 小时`；本体上下文/motif 库 1–2 人周；repair trace 埋点 3–5 人日（本页估算，无出处）；把追问/确定性评分做成系统能力 2–4 人周（本页估算，原论文未报工程成本）。
- **口径警告（`存疑`）**：digest 的 `15–20 case × 2 人 × 1–2 小时` 没说是每例还是总计，两种读法差一个数量级。排预算前先定口径，否则人日表是假的。
- **运行成本**：人审 10–20% case（digest §6.5）；追问约 10 问、上限 11 问/失败 case（D-15 §3.3、§6.2）的用户或专家时间；本体/motif 每次变更后重跑同 batch；κ 只在新增标注者或改定义时重测。
- **成本结构（借 D-15，迁移为 `推测`）**：本体/KG 一次性+持续、症状映射每次、LLM 抽取/提问/解释 3 个 agent、追问约 10 问、评估每 case、本体更新维护（D-15 §6.2）。D-15 同样没给金额；本页只把它当成本项清单，不当报价。
- **单价表目前是空的**：人时价、人审分钟价、返工成本、单次错误成本都要自己填；填不出就只给敏感性区间，不给 ROI 点估计（同 [feasibility](../feasibility/README.md) 的口径）。

### stop condition

- 同一 batch 语义充分率提升 <10pp，或人审工时没降 → 停诊断路线，改走执行反馈/结构化校验（digest §6.5 的工程线，`推测` 非实测）。
- 诊断 2 轮仍无改善 → 停，不继续调 prompt（digest 同处）。
- κ<0.4 → 先改七变量的定义与三档标准，不扩样本、不据此分配预算（digest §6.5 第 3 步）。
- 高摩擦项集中在 Vocabulary/Coverage，且本体扩展排不进本季度 → 停归因工程，转本体扩展；依据是 D-15 的覆盖封顶（Jaundice/Vertigo 被归为症状，准确率恒 0），但「覆盖缺口不是排序或追问能补」是本页推断（`推测`，D-15 未做该消融）。
- 追问不改变排序（Top-1/Top-3 不升，或 Top-3 降）→ 关掉追问，只留 intent gate（本页 stop 规则，`推测`；D-15 只给了 50% 完整度下 Top-3 26.3→24.2 一个观测，没说该关）。
- 连续若干 case 填不出 `owner` 或 `redesign_lever`（条数团队自定）→ 表已退化成描述，停（本页规则，`推测`）。
- 按单价表算出的年省人审工时 < 诊断 + 维护人时 → 停（digest V3 停止线）。
- **硬门槛**：没有改动前基线 → 不出 go 结论，只出测量方案（本页规则，`推测`）。

### 第一个 sprint

2 周、单域、15–20 个失败 case、不接线上写权限、不动模型与本体：

1. **第 1–2 天 · 定口径**：锁死语义充分率、首次通过率、返工轮次、人审工时四个口径（本页操作定义，`推测`）；抽出 15–20 个 case，保留输入/输出/参考输出/拒绝记录；先测基线。
2. **第 3–5 天 · 落 schema**：把七变量落成带 `batch_id/retest_of` 的 case 表与 repair trace JSON；两名标注者独立标 10 例算 κ；κ<0.4 改定义再标，不扩样本。
3. **第 6–8 天 · 只修 Input/Context**：intent gate 澄清 3–5 问 + 补术语/示例；不动模型、不动本体、不动模板。
4. **第 9–10 天 · 同 batch 重测 + 判**：重算充分率/首次通过率/返工/人审工时；填 go/no-go 表。

**交付物**：15–20 例的 case 表 + repair trace JSON + κ + 四指标基线 + 同 batch 前后对照 + 一页 go/no-go memo（含预写的停止线）+ 高摩擦分布（哪几列最多、各归哪个 owner）。

**出口（go/no-go）**（阈值为 digest 的工程线，`推测`，非实测）：

- **go**：充分率 ≥+10pp、人审工时 ≤−10%、κ≥0.6 → 第二 sprint 才允许动 Grounding/Template，或换第二个域复测。
- **no-go**：无提升，或 κ<0.4，或多数 case 落在 Vocabulary 且本季无法扩本体 → 停，结论回写 [frontier](./frontier.md) 的 G1–G4。
- **不出结论**：改动前基线没测，或有效 case <10 → 补数据，不硬判（阈值是本页规则，`推测`）。

### 客户指标/V3

> 本节除引用 D-15/D-11 的数字外，都是 V2/V3 假设（`推测`），不能当已核结论。

- **受益者**：本体/数据集成团队（NL→本体断言反复失败）、平台/预算 owner（批不批模型升级）、领域专家（人审工时）；间接受益是下游数据消费者（`推测`，V2 假设）。
- **痛点不是「本体质量差」**，是**失败无法归因**：每次换模型都复现同一批错，却说不清该改哪里，于是预算只能押在「更强的模型」上（`推测`，V2 假设）。
- **指标（三层）**：
  - 结果：语义充分率、首次通过率、返工轮次/case、下游断言返修率（本页加，`推测`）。
  - 成本：人审分钟/case、从失败到定位变量的 lead time（本页加，`推测`）、每 case 诊断人时（本页加，`推测`）。
  - 尺子本身：κ（profile 一致性）、**误归因率**（按表改了变量、case 仍失败的比例，`推测` 口径）、**归因闭环率**（有 owner 且设计已改的 case 占比）。
- **报告口径**：Top-1、Top-3、case-level 三者同报（D-15 实测：聚合 +2.5pp 掩盖个案 0.340→1.0 与 50% 完整度 Top-3 反降；`已核`，单基准；F7）。
- **反事实**：不诊断 → 继续换模型/调 prompt，同一批 case 大概率复发（G3 未关，`推测`）；只有表没有 trace → 归因变事后叙事，无法验证；直接买现成 schema 校验/抽取工具 → 能解决语法/类型层，语义充分性仍在人审（digest §3.3 的钻井例子：语法/类型能过，语义要专家）。
- **试点成功**：单域 15–20 case、2 周内，充分率 +10pp、人审工时 −10%、κ≥0.6（D-11 的三条）。D-11 没有「换人复算同一结论」这条，本页删掉；要表达复算性就用两名标注者的 κ（本页口径，`推测`）。
- **试点失败**：无提升，或 κ<0.4，或表填完仍指不出下一个动作；若 Top-1 升、Top-3 降，先看 case-level 再判，不直接算失败（D-15 的聚合会打架）。
- **停止线**：按单价表算，年省人审工时 < 诊断 + 维护成本（`推测`，单价需先填）。
- **外推边界**：只对 NL→本体/DSL 类任务成立；Text-to-SQL/求解器有执行反馈、失败可直接报错，归因优先级不同（digest §6.3）。

### 反例

- **七变量可能只是更长的「模型弱」。** 变量非正交：同一 case 可以同时在 Input 和 Context 打 high，没有正交性就没法把预算分给某一列；填完表若仍不知道该改哪个 lever，它只是把不可证伪换了个说法（G3 未关）。
- **Multi-agent 的证据是类比，不是迁移证据。** 医学鉴别诊断、99 cases/29 diagnoses、模拟患者；追问的聚合收益只有 Top-1 +2.5pp，Top-3 在 50% 完整度下反降。搬到失败归因，收益方向和量级都未知（`推测`）。
- **覆盖缺口会吃掉归因收益。** 本体没有的构造只能被记成 Vocabulary high，改不动；这时先扩本体可能比先归因更值（`推测`；依据是 D-15 的覆盖封顶，但「先扩本体更值」没有做对照）。
- **只诊断「被记录的失败」会系统性低估 Vocabulary。** near-match 与静默通过不进失败集（F1 的「语义不太对」常常没人拒绝），表越依赖拒绝记录，越看不见最贵的那类错（`推测`，本页推断；D-11 未测）。
- **截断会把「没进池」伪装成「排错」。** 候选截断 10–20 是 D-11 的工程线，D-15 没做截断消融；正确答案不在池里时，七变量表会把它记成 Grounding/Validation 错，改了也不见效（`推测`）。
- **映射失败会被记成模型/本体错。** D-15 的 8.7% unmapped 被排除在推理外；归因表若没有 `unmapped` 桶，会系统性高估 grounding 与 vocabulary 的问题（`推测`，迁移用法；单基准数字本身 `已核`）。
- **成本可能摊不薄。** 单域 15–20 例只覆盖一个季度的一种任务形态；本体/motif 的 1–2 人周与 trace 埋点是固定成本，失败率低时 do-nothing 更便宜（`推测`，无实测）。

## 关联

- [Diagnose digest](../../../src/papers/2610.35267-diagnose-workflow/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
- [00-harness/verification](../../00-harness/verification.md)
