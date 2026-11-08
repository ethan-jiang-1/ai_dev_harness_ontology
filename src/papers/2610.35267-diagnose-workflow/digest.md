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
