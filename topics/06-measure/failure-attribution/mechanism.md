# 失败归因 · 机制

> 只写「怎么诊断」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 问题

一个任务失败了，最常见的归因是「模型不够强」。这个归因不可证伪，也不可操作——它给不出下一步动作。

Before Blaming the LLM 研究 NL→本体接地 ABox DSL 的语义解析：语法有效容易、语义充分很难，而反复出现的难点是结构性的。

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

**用法**：每个 case 填一张 7 行表（变量 / 证据 / 高摩擦？ / 重设计杆 / 负责人）。它不预测准确率，只把「语义不太对」拆成可改设计的位置。

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

校验弱 → 只能发现表面问题 → 修改扩散 → 引入新错误。这是一条可归因的因果链，根因在 harness（校验太弱），不在模型。

它解释了：换更强判定器往往比换更强模型更有效。模型本来能改对，是判定给了它错误的方向。

## 失效模式

- **把 position paper 当实证。** 单案例、无量化；七变量非正交/非穷尽。
- **profile 不一致。** 不同实践者可能给不同结果。
- **只填表不行动。** 没有负责人/重设计杆，表就只是描述。
- **变量交互。** 低 context 会放大 grounding；弱 template 会与 vocabulary 交互。

## 与本体 / 回路的关系

本体在失败归因里是 **诊断对象/重设计目标**；它不直接执行约束。被违反时通常没有即时信号，需要 trace/人审。

## 关联

- [Diagnose digest](../../../src/papers/2610.35267-diagnose-workflow/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
- [00-harness/verification](../../00-harness/verification.md)
