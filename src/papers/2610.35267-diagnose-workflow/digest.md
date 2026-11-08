---
status: draft
updated: 2026-11-08
quality: C
based_on: card.md
claims: [E-06]
---

# Diagnose the Workflow：先别怪模型，先看病流

> 这篇消化不假设你读过论文。先讲清「NL→本体接地 DSL」这项工作，再给五角色/七变量、钻井例子、以及为什么它是 position paper。

## 0. 三句话

1. **它问什么**：把自然语言描述翻译成「本体接地的 ABox 断言」时，失败常被归因于「模型弱」；但输入不足、上下文缺失、模板/词汇缺口、校验弱、非局部修复也会造成同样表现。
2. **它怎么做**：提出一个**角色级难度画像**：五个角色（Input / Generator / Output / Validator / Repairer）× 七个诊断变量；每个变量给「问题 / 高摩擦证据 / 重设计杆」。
3. **它发现什么**：用一个钻井信号 ABox 例子展示「语法对、语义不足」；**没有量化评测**，是 position paper。价值在诊断词汇与重设计映射，不在效应量。

## 1. 它解决什么问题

### 1.1 背景：NL→本体接地 DSL

很多领域要把非正式描述翻译成结构化断言：

- 自然语言 → SQL；
- 自然语言 → API 调用；
- 自然语言 → workflow；
- 自然语言 → 本体接地的 ABox DSL（本文重点）。

**ABox** 是本体里的实例层断言（相对于 TBox 的类/公理）。例如：

> 「给 Bottom Hole Depth 钻井信号一个语义。」

要翻成：`DynamicDrillingSignal` + `HoleBottomLocation` + `DepthDrillingQuantity` + 若干 `hasDynamicValue` 断言。

**语法有效很容易，语义充分很难。** 一个 DSL 可以语法对、类型对、甚至本体接地，但模板错、漏断言、选错本体构造。

### 1.2 论文的立场

失败常被归因于 generator 模型；但反复出现的难点是**结构性的**：

- 输入不足（缺字段、隐含假设、歧义）；
- 上下文缺失（术语说明、示例、建模约定）；
- grounding 复杂（太多候选符号/模板）；
- 模板缺口（断言模式不规则）；
- 词汇缺口（本体没有需要的构造）；
- 校验弱（语义充分性不可确定性检查）；
- 错误可观测性差（失败无法定位）。

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **NL→DSL** | 自然语言 → 领域特定语言。 |
| **ABox / TBox** | ABox 是实例断言；TBox 是类/公理。本文做 ABox。 |
| **ontology-grounded** | 输出必须使用既有本体的词汇。 |
| **role-level** | 按工作流角色（输入/生成/输出/校验/修复）诊断，而不是只看模型。 |
| **difficulty profile** | 七变量组成的诊断表；不是 benchmark，不是评分。 |
| **intent gate** | 生成前先检查输入够不够；不够就澄清。 |
| **motif library** | 常见断言模式的模板库。 |
| **repair trace** | 记录失败定位/修改路径，供后续修复。 |

## 3. 它怎么做

### 3.1 五个角色（Fig. 1）

| 角色 | 做什么 | 典型失败 |
|---|---|---|
| Input | 提供意图与上下文 | 歧义、不完整、隐含假设 |
| Generator | grounding 到本体符号，生成候选 | 选错类/关系/模板 |
| Output | DSL 表达式空间 | 模板不规则、覆盖缺口、near-match |
| Validator | 判断是否可接受 | 语法过、语义错；反馈弱 |
| Repairer | 修订/澄清/重生成/升级 | 非局部修复、重复重生成 |

### 3.2 七个诊断变量

| 变量 | 角色 | 高摩擦证据 | 重设计杆 |
|---|---|---|---|
| Input sufficiency | Input | 缺字段/隐含假设/歧义 | intent gate + clarification |
| Context availability | Generator | 缺术语说明/示例/约定 | 知识库精化 |
| Grounding complexity | Generator | 候选符号/模板太多 | 候选排序 |
| Template fit | Output | 断言模式不规则/重叠 | motif 库 |
| Vocabulary coverage | Output | 缺构造、被迫 near-match | 本体扩展 |
| Validation strength | Validator | 语义充分性不可确定性检查 | 分层校验 + 人审 |
| Error observability | Repairer | 失败无法定位 | repair trace |

### 3.3 钻井例子

输入：`Give the semantics for retrieving the Bottom Hole Depth drilling signal.`

- **实际输出**：`DynamicDrillingSignal` + `HoleBottomLocation` + `DepthDrillingQuantity` + 两条断言。
- **参考配置**：还要求 `PhysicalData`、`OneDimensionalCurviLinearReferenceFrame`、`HasDynamicValue`，并把 quantity/frame/location 挂在 physical data 上。
- **按七变量诊断**：
  - Input：没说要不要 physical data/reference frame——缺的是建模假设，不是一个槽位。
  - Context：agent 无法从输入推断「Bottom Hole Depth 需要 reference frame」。
  - Grounding：本体里有大量候选类/关系，要分多步选。
  - Template：没有稳定 motif，模型每次现发明结构。
  - Vocabulary：本例词汇够；缺词时会变成 near-match。
  - Validation：语法/类型能过，语义充分性要专家。
  - Observability：拒绝输出时，说不清是输入、上下文、grounding、模板还是词汇问题。

## 4. 结果：数字与条件

| 数字 | 条件 | 说明 |
|---|---|---|
| ≈2,250 类 / ≈200 对象属性 | DDHub 派生本体快照（原型） | 例子系统规模 |
| 无量化评测 | 全文是框架 + 单案例 | position paper |

**没有准确率/延迟/成本数字。** 论文的价值在诊断词汇与重设计映射，不在效应量。

### 4.1 为什么七变量不是打分卡

- **非正交。** 低 context 会放大 grounding complexity；弱 template fit 会与 vocabulary coverage 交互。
- **非穷尽。** 它是一个诊断词汇，不是完整因果模型；不同任务可能有关键变量缺失。
- **定性。** 不同实践者对同一 case 可能给不同 profile；没有 inter-rater 数据。
- **不预测效应量。** 它能指出「该改哪」，但不能保证改了就一定好；需要前后对照。

这四条决定了它只能当「诊断框架」，不能当「评分卡」。作者自己也把它定位为 position paper。

## 5. 这些数字不能说明什么

1. **不是实证。** 一个案例、无跨系统实验；不能证明「七变量能预测失败」。
2. **不是穷尽。** 七变量非正交、非穷尽；低 context 会放大 grounding complexity，弱 template fit 会与 vocabulary coverage 交互。
3. **不是可打分 rubric。** 目前靠定性判断；不同实践者可能给不同 profile。
4. **不是从零建本体。** 假设本体至少部分可用；TBox 构建不在范围内。
5. **不是「换更强模型就好」。** 作者明确说错误主要来自结构；更强模型不一定修 template/vocabulary gap。

## 6. 工程上怎么用

### 6.1 复刻顺序

1. **先填一张 7 行表。** 每个 case：变量 / 证据 / 高摩擦？ / 重设计杆 / 负责人。
2. **Input 先过 intent gate。** 缺实体/关系/约束/建模假设 → 澄清，不要硬生成。
3. **Context 先补术语/示例/约定。** 用 ontology-aware retrieval 把相关部分带进生成。
4. **Grounding 分阶段。** 先选 entity，再选 relation/template；候选排序，不要一次让模型选全部。
5. **Template 建 motif 库。** 常见断言模式写成模板；不要让模型每次现发明结构。
6. **Vocabulary gap 暴露为本体扩展请求。** 不要静默 near-match。
7. **Validation 分层。** 语法/类型/domain-range/template 先查；语义留人审。
8. **Repair trace 记录。** 检索上下文、候选符号、模板、校验结果、人反馈；否则 repair 退化成重复重生成。

### 6.2 成本与使能

| 成本 | 说明 |
|---|---|
| 本体上下文/示例 | 维护术语说明、建模约定、curated examples |
| Motif 库 | 领域专家把 recurring 结构写成模板 |
| 人审 | 语义充分性不可判定时，专家 review 必需 |
| Repair trace | 记录检索上下文、候选、模板、校验、反馈；存储/工具成本 |
| 本体扩展 | 缺词时评审、加类/关系、版本管理 |

**使能条件**：本体至少部分可用；有领域专家；有 DSL/grammar；能保存生成与校验轨迹。

### 6.3 何时用 / 何时别用

**用**：NL→本体/DSL、语义互操作、数据集成、agent 生成配置、专家评审成本高的域。

**别用**：只需要语法/格式校验；任务有强执行反馈（SQL/求解器）；已经有可量化的失败归因。

### 6.4 最小诊断流程

1. **选一个失败 case。** 保留输入、模型输出、参考输出、拒绝/修复记录。
2. **填 7 行表。** 变量/证据/高摩擦？/重设计杆/负责人；不要只写「模型不行」。
3. **先修 Input/Context。** 这两项成本最低、收益最直接；缺字段/隐含假设先澄清。
4. **再修 Grounding/Template。** 候选排序、motif 库；不要把「选错符号」归因于模型能力。
5. **Validation 分层。** 语法/类型/domain-range 先查；语义充分性留人审。
6. **Repair trace 记录。** 检索上下文、候选符号、模板、校验结果、人反馈；否则 repair 退化成重复重生成。
7. **重测同一 case。** 看是否真的修好；不要只看「换了个说法」。

## 6.5 工程配方（E3）

### 产物 schema

**case table（7 行）**：

| 字段 | 取值 |
|---|---|
| `case_id` | 失败样本 id |
| `variable` | Input sufficiency / Context availability / Grounding complexity / Template fit / Vocabulary coverage / Validation strength / Error observability |
| `evidence` | 指向输入/输出/拒绝记录的行号或片段 |
| `friction` | low / medium / high |
| `redesign_lever` | intent gate / 知识库精化 / 候选排序 / motif 库 / 本体扩展 / 分层校验 / repair trace |
| `owner` | 产品/本体/平台/标注 |

**repair trace JSON**：`{case_id, retrieved_context[], candidate_symbols[], template_used, validation_results[], human_feedback, change, retest}`。

### 接口

- `intent_gate(input)` → `{sufficient|clarify, missing_slots[], questions[]}`；输入不够先澄清，不硬生成。
- `validate(dsl)` → `{syntax, type, domain_range, template, semantic}`；前三层可自动，semantic 留人审。
- `repair(trace)` → 修订/重生成/升级；回灌下一次生成。

### 参数与 stop

- 候选符号截断 10–20；人审抽样 10–20%；单轮诊断 15–20 case。
- stop：语义充分率提升 <10pp 或人审工时没降 → 换执行反馈/结构化校验路线。
- 诊断 2 轮仍无改善 → 停，不继续调 prompt。

### 成本

- 标注/诊断：15–20 case × 2 人 × 1–2 小时（`推测`）。
- 本体上下文/motif 库：1–2 人周（`推测`）。
- 人审：10–20% case；按每小时审成本算。
- 维护：本体/motif 变更后重跑。

### 第一个 sprint

2 周、单域、15–20 个失败 case：

1. 保留 input/模型输出/参考输出/拒绝记录。
2. 把七变量落成带字段 + 三档 + 证据链接的 case 表与 repair trace JSON（这步就是缺失的规格）。
3. 两名标注者独立打 10 例，测 κ；κ<0.4 先改定义。
4. 按 §6.4 只修 Input/Context：intent gate 澄清 3–5 问 + 补术语/示例；同 batch 重测。
5. 预写 go/no-go：语义充分率提升 <10pp 或人审工时没降 → 改走执行反馈/结构化校验。

### 替代方案

- 执行反馈（SQL/求解器报错）、schema 校验器、宿主平台校验；do-nothing。
- 论文无量化；替代方案无同口径对照。

## 6.6 客户价值假设（V2/V3，`推测`）

- **受益者**：本体/数据集成团队；痛点：NL→本体断言反复失败、人工 review 贵、修来修去。
- **指标**：语义充分率、返工轮次、人审工时/case、首次通过率。
- **反事实**：不诊断 → 继续换模型/调 prompt；成本高且不可归因。
- **V3 试点**：单域 15–20 case；成功 = 语义充分率 +10pp、人审工时 −10%、κ≥0.6；失败 = 无提升或 κ<0.4；停止线 = 年省工时 < 诊断/维护成本。
- **反例**：七变量非正交；profile 不一致；单案例；换任务形态权重不同。

### E4 决策框架

- **TCO** = 诊断/标注 `15–20 case × 2 人 × 1–2 小时` + 本体上下文/motif `1–2 人周` + 人审 + 维护。
- **收益** = `语义充分率提升 × 返工成本 + 人审工时下降 × 工时价`；先测当前充分率/返工/人审基线。
- **替代**：build（诊断框架）/ buy（现成 schema 校验/抽取工具）/ 执行反馈 / do nothing。
- **决策线**：语义充分率 +10pp 且人审工时 −10% 才继续；否则改走执行反馈/结构化校验。

## 7. 质量与边界

- **证据类型**：立场/经验框架（position paper），单案例，无量化评测。
- **强项**：诊断词汇清晰；五角色 + 七变量可操作；把「模型弱」拆成可改设计；与 Text-to-SQL/API/Workflow 做了对照定位。
- **主要威胁**：没有量化验证；七变量非正交/非穷尽；单案例；评估者差异；不能预测重设计效果。
- **`quality: C`**：概念框架，不是实证；价值在诊断，不在效应量。

## 8. 与仓库判断的关系

- **E-06（已核）**：本体接地类任务的失败多来自工作流；五角色 + 七变量；语法通过不等于语义充分。
- **P2**：同一模型，换 input/context/template/validator，难度不同。
- **06 failure-attribution**：七变量可作为 EXP-002 的诊断表。
- **05 生产**：vocabulary gap → 本体扩展；template fit → motif 库。

## 9. 还没解决 / 下一步

- **七变量能否变成可打分的 rubric？** 评分者一致性如何？
- **能否预测重设计后的效果？** 需要前后对照。
- **在 Text-to-SQL/API/Workflow 上是否同样适用？** 哪些变量权重不同？
- **repair trace 能否自动化为结构化日志，喂给下一次生成？**
- **语义充分性的人审成本能否用「分层校验 + 抽样」降下来？**

## 10. 原文

- arXiv:2610.35267
- PDF：`src/papers/2610.35267-diagnose-workflow/`
- 代码/数据：论文未给公开仓库。
