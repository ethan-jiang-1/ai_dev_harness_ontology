---
status: draft
updated: 2026-11-07
quality: C
based_on: card.md
claims: [E-06]
---

# Before Blaming the LLM, Diagnose the Workflow · 消化

> 事实、数字、页码回 [card.md](./card.md)。这里只写**我们怎么用**、值不值得、哪里会坏。

## 工程思路

**模型「不够强」之前，先走一遍这七问：**

1. **Input sufficiency**：输入够不够明确？缺实体/关系/约束/建模假设吗？→ 加 intent gate，缺就澄清，不要硬生成。
2. **Context availability**：generator 拿得到术语说明、示例、建模约定吗？→ 精化知识库 + ontology-aware retrieval。
3. **Grounding complexity**：候选符号/模板是不是太多？→ 候选生成 + 排序，分阶段选 entity/relation/template。
4. **Template fit**：这类输入有没有稳定的断言模式？→ 建 motif 库；不要让模型每次现发明结构。
5. **Vocabulary coverage**：本体有需要的类/关系/单位吗？→ 缺就暴露为本体扩展请求，不要静默 near-match。
6. **Validation strength**：能不能确定性检查语义充分性？→ 分层：语法/类型/domain-range/template 先查，语义留人审。
7. **Error observability**：失败能不能定位到上面六项？→ 保存 repair trace：检索上下文、候选符号、模板、校验结果、人反馈。

**记录方式**：每个 case 填一张 7 行表（变量 / 证据 / 高摩擦？ / 重设计杆 / 负责人）。这比「模型不行，换个更大的」更能指导下一步。

## 实用意义

它解决的操作问题：

- **「模型生成的本体断言语法都对，专家说语义不对。」** → 先分 workflow 角色，不要直接换模型。
- **「同一个输入，模型每次生成的结构都不一样。」** → template fit 差；建 motif 库，而不是加 temperature 约束。
- **「本体里没有这个词，模型硬凑了一个近义类。」** → vocabulary coverage；暴露为本体扩展请求。
- **「校验器说通过，专家说不行。」** → validation strength；语义充分性需要人审或更强的外部判据。
- **「修了一次，别的地方又坏了。」** → 非局部修复；需要 repair trace + 跨断言一致性检查。
- **「不知道该不该上人审。」** → 看 validation strength 与 error observability：语义不可判定时，人审是设计的一部分，不是失败。

**何时用**：NL→本体/DSL、语义互操作、数据集成、agent 生成配置、专家评审成本高的域。

**何时别用**：只需要语法/格式校验；任务有强执行反馈（SQL/求解器）；已经有可量化的失败归因。

## 质量评估

- **证据类型**：立场/经验框架（position paper），单案例，无量化评测。
- **样本与对照**：一个钻井 ABox 系统；约 2,250 类 / 200 对象属性；一个 diagnostic case（实际 vs 参考配置）。
- **优点**：诊断词汇清晰；五角色 + 七变量可操作；把「模型弱」拆成可改设计；与 Text-to-SQL/API/Workflow 做了对照定位。
- **主要威胁**：没有量化验证；七变量非正交、非穷尽；单案例；评估者差异；不能预测重设计效果。
- **`quality: C` 理由**：概念框架，不是实证；价值在诊断，不在效应量。

## 洞察

1. **「模型弱」是默认归因，但往往不是根因。** 输入不足、上下文缺失、模板缺口、词汇缺口、校验弱、可观测性差，都会表现成「模型不行」。`已核`（作者立场；本仓库认同）
2. **语法有效是弱成功标准。** ABox DSL 可以语法对、类型对、甚至本体接地，但模板错/漏断言/选错构造；用语法通过率评估会高估系统。`已核`
3. **Template fit 是输出侧属性，换更强模型修不好。** 如果领域没有稳定 motif，模型只能每次现发明结构；需要 motif 库。`推测`（设计判断）
4. **Vocabulary gap 会变成 near-match。** 缺构造时，模型不是报错，而是塞进一个相近的类；这比报错更危险，因为看起来通过了。`已核`（例子）
5. **Error observability 是一等设计变量。** 失败不能定位，repair 就退化成重复重生成；repair trace 不是调试附属品，是系统组件。`推测`
6. **语义充分性通常需要人审。** Validation strength 决定自动化上限；不要把「LLM judge 能打分」当成「语义可判定」。`推测`
7. **非局部修复是本体接地的常态。** 一个类型/关系错会沿链接传播；单点修补不够，需要跨断言一致性检查。`已核`（作者观察）

## 成本与使能条件

| 成本 | 说明 |
|---|---|
| 本体上下文/示例 | 需要维护术语说明、建模约定、curated examples |
| Motif 库 | 需要领域专家把 recurring 结构写成模板 |
| 人审 | 语义充分性不可判定时，专家 review 是必需 |
| Repair trace | 记录检索上下文、候选、模板、校验、反馈；存储/工具成本 |
| 本体扩展 | 缺词时评审、加类/关系、版本管理 |

**使能条件**：本体至少部分可用；有领域专家；有 DSL/grammar；能保存生成与校验轨迹。

**2022 年做会卡在哪**：LLM 生成本体断言的稳定性更差；没有 agent/工具调用；本体上下文与检索不成熟；但诊断框架本身不依赖模型版本。

**反向条件**：任务有强执行反馈；只需要语法校验；没有专家可审；本体完全从零构建。

## 与现有判断的关系

| 关联 | 关系 |
|---|---|
| **E-06** | **直接支撑**：本体接地类任务的失败多来自工作流（输入不足、领域接地弱、模板/词汇缺口、校验弱、非局部修复）。 |
| **P2** | 支撑「harness 是不可分离的一半」：同一模型，换 input/context/template/validator，难度不同。 |
| [failure-attribution](../../../topics/06-measure/failure-attribution/README.md) | 核心文献；七变量可作为 EXP-002 的诊断表。 |
| [00-harness/verification](../../../topics/00-harness/verification.md) | 语义充分性需要外部判据/人审，与 02 判定派相接。 |
| [05-produce/lifecycle](../../../topics/05-produce/lifecycle/README.md) | vocabulary gap → 本体扩展，是生产侧的回流。 |

## 不可迁移

- 一个钻井 ABox 系统、一个案例；不能外推到所有 NL→DSL。
- 定性框架，没有效应量；不能用来预测准确率或比较模型。
- 七变量非正交；不同评估者可能给出不同 profile。
- 假设本体至少部分可用；从零构建本体不在范围内。

## 开放问题

- 七变量能否变成可打分的 rubric？评分者一致性如何？
- 这套诊断能否预测重设计后的效果？需要前后对照。
- 在 Text-to-SQL/API/Workflow 上是否同样适用？哪些变量权重不同？
- 能否把 repair trace 自动化为结构化日志，喂给下一次生成？
- 语义充分性的人审成本能否用「分层校验 + 抽样」降下来？
