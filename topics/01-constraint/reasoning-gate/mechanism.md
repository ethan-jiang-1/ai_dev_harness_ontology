# 推理期约束 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 位置

在动作之前、甚至在产出之前：模型正在推理，本体限制它**能用什么结论、能推到哪一步**。它不改变工具调用是否执行，而改变「哪些结论有资格被取用」。

## 两种机制

| 机制 | 做法 | 代表 |
|---|---|---|
| 推理锚定 | 把推理限制在 curated KG 上，拆成可审计步骤；缺证据时追问 | 多 agent 差分诊断 |
| 符号验证 | 把动作空间压到本体概念层，用符号验证器检查条件是否满足 | OntoAct |

共同点：判据来自本体，不是模型自评。区别：前者限制「从什么推」，后者限制「推出来的条件是否成立」。

## OntoAct 的流程

1. 从记录抽候选公理；类型检查 + 来源非空 + 该公理类型的测试通过才进入世界知识。
2. LLM 提出 claims / hypotheses / action。
3. 每个 hypothesis 的每个条件在当前知识下求值：⊤ / ⊥ / ?。
4. 违反 R_W 的条件/禁止 → block；缺读数只报 unresolved，触发观察。
5. 被 block 时给 revision 反馈；新观察/干预结果更新 context 与 hypothesis。

## 多 agent 诊断的流程

1. LLM 只做症状抽取、追问、解释；排序/评分由确定性代码算。
2. 候选病只从 curated KG（SYMP/DOID/HPO）的显式关系来。
3. 追问只问可观察、未报告、能区分候选的症状；Yes/No/unsure。
4. 评分：specificity + coverage + support/conflict；每项回指症状与本体关系。

## 证据

- **OntoAct**：Tacit-FLE 成功率 78.6/83.3/90.0%（IfR 64.3/66.7/65.0）；spurious interventions 1.9/2.4/1.6（6.4/11.9/17.8）；Mars 15.92 vs 10.64；ALFWorld 98.5% vs 96.3%，LLM calls 13.7 vs 28.8。
- **多 agent 诊断**：Q4DX Top-1 18.7→21.2%、Top-3 25.8→27.3%；但 curated KG 没有的诊断（Jaundice/Vertigo 被归为症状）准确率恒 0；作者写「caps benchmark performance」。

## 失效模式

- **覆盖不足。** 本体只覆盖少数关系，推理卡在 KG 边界。
- **封顶表现。** 限制越强，越可能把「本来能推对」的路径剪掉。
- **阻断信号弱。** 推理被限制时，模型往往只是「换个说法」，不报错。
- **与动作闸门重复。** 同一份本体在推理期/动作期各判一次，重复收费。
- **schema 覆盖不足。** 没有适用 axiom 的动作/假设，只能放行/fallback。
- **把 unknown 当 block。** 缺证据应触发观察；直接拒绝会把「不知道」变成「不允许」。

## 与本体 / 回路的关系

本体在推理期以 **typed schema / conditional axioms / curated KG** 出现；约束强度中到强（能限制结论取用），覆盖率取决于 schema/KG。被违反时能报出失败条件/候选；不能报「语义真值」。

## 关联

- [OntoAct digest](../../../src/papers/2610.21983-ontoact/digest.md)
- [多 agent digest](../../../src/papers/2610.36325-ontology-multiagent-diagnosis/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
