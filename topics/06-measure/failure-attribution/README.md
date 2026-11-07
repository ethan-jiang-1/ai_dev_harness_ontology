---
status: draft
updated: 2026-11-07
rq: [RQ2]
evidence: [E-06]
---

# 尺子二：失败出在哪一环

## 问题

一个任务失败了，最常见的归因是「模型不够强」。这个归因不可证伪，也不可操作——它给不出下一步动作。

Before Blaming the LLM 提出相反的做法：**先诊断工作流。** 它研究 NL → 本体接地 ABox DSL 的语义解析，指出语法有效容易、语义充分很难，而反复出现的难点是结构性的。

## 五角色 + 七变量

**五个角色**（Fig. 1）：

| 角色 | 做什么 | 典型失败 |
|---|---|---|
| Input | 提供意图与上下文 | 歧义、不完整、隐含假设 |
| Generator | grounding 到本体符号，生成候选 | 选错类/关系/模板 |
| Output | DSL 表达式空间 | 模板不规则、覆盖缺口、near-match |
| Validator | 判断是否可接受 | 语法过、语义错；反馈弱 |
| Repairer | 修订/澄清/重生成/升级 | 非局部修复、重复重生成 |

**七个诊断变量**（Table 1）：

| 变量 | 角色 | 高摩擦证据 | 重设计杆 |
|---|---|---|---|
| Input sufficiency | Input | 缺字段/隐含假设/歧义 | intent gate + clarification |
| Context availability | Generator | 缺术语说明/示例/约定 | 知识库精化 |
| Grounding complexity | Generator | 候选符号/模板太多 | 候选排序 |
| Template fit | Output | 断言模式不规则/重叠 | motif 库 |
| Vocabulary coverage | Output | 缺构造、被迫 near-match | 本体扩展 |
| Validation strength | Validator | 语义充分性不可确定性检查 | 分层校验 + 人审 |
| Error observability | Repairer | 失败无法定位 | repair trace |

**用法**：每个 case 填一张 7 行表（变量 / 证据 / 高摩擦？ / 重设计杆 / 负责人）。它不预测准确率，只把「语义不太对」拆成可改设计的位置。

## 例子：Bottom Hole Depth

输入只说了「给 Bottom Hole Depth 钻井信号的语义」。实际输出是 `DynamicDrillingSignal` + `HoleBottomLocation` + `DepthDrillingQuantity` + 两条断言；参考配置还要求 `PhysicalData`、`OneDimensionalCurviLinearReferenceFrame`、`HasDynamicValue`，并把 quantity/frame/location 挂在 physical data 上。

按七变量诊断：

- **Input**：没说要不要 physical data/reference frame——缺的是建模假设，不是一个槽位。
- **Context**：agent 无法从输入推断「Bottom Hole Depth 需要 reference frame」。
- **Grounding**：本体里有大量候选类/关系，要分多步选。
- **Template**：没有稳定 motif，模型每次现发明结构。
- **Vocabulary**：本例词汇够；缺词时会变成 near-match。
- **Validation**：语法/类型能过，语义充分性要专家。
- **Observability**：拒绝输出时，说不清是输入、上下文、grounding、模板还是词汇问题。

## 「非局部修复」值得单独记

校验弱 → 只能发现表面问题 → 修改扩散 → 引入新错误。这是一条**可归因的因果链**，且根因在 harness（校验太弱），不在模型。

它解释了一个常见现象：换更强的判定器往往比换更强的模型更有效。因为模型本来能改对，是判定给了它错误的方向。

## 一个必须带的限定

这是一篇 **position paper**：一个钻井案例、无量化评测、七变量非穷尽且非正交。它的价值是**诊断词汇**，不是效应量。引用时不能写成「七变量已被验证能预测失败」；只能写「提供了一个可操作的诊断框架」。

## 与其它派的关系

- 直接支撑 [00-harness/verification](../../00-harness/verification.md) 的「判定器与被判对象必须不同源」。
- 为 [02 判定](../../02-judgment/README.md) 提供存在理由：判定弱会让修复变成破坏。
- vocabulary gap → 本体扩展，是 [05 生产](../../05-produce/README.md) 的回流；template fit → motif 库，是 [05 生产](../../05-produce/README.md) 的工件。

## 待核 / 开放问题

- [ ] 七个变量的分布比例（本文未给）。
- [ ] 不同实践者对同一 case 的 profile 一致性（inter-rater）。
- [ ] 这套诊断能否预测重设计后的效果？需要前后对照。
- [ ] 能否变成可打分的 rubric，而不是定性判断？
- [ ] 在 Text-to-SQL/API/Workflow 上变量权重是否不同？
