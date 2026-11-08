# 输出时证据契约 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 问题

模型生成结论时，判定还没发生，但输出格式可以先被约束：每个结论必须带依据，以及依据与本体的关系强度。这把「不能无根据」从规范变成机制。

## 四个接地等级

| 等级 | 含义 | 期望来源 |
|---|---|---|
| entailed | 由本体约束必然推出 | formal reasoner / entailment |
| supported | 有直接证据支撑，但非必然 | 本体注释 + LLM 推理 |
| related | 仅有相关材料，非直接支撑 | 检索到但不足 |
| unrelated | 无支撑 | 检索失败/无关 |

## OA-RAG 的实际做法

1. **Pre-tool reasoning**：先让 LLM 用参数知识分析问题。
2. **ReAct loop**：给 agent 一个 ontology tool；`DESCRIBE` 取 concept card，`ASK` 问 reasoner 是否 entailed，`SELECT` 检索；空结果触发 BM25 fallback。
3. **Answering**：过滤失败/空观察，得到 evidence digest；有证据用 `P_fin`，无证据用 `P_own`；再一轮 `P_att` 报告引用的观察与 grounding level。

**等级是模型自评**：不是独立判定器，也不是形式推导。作者明确写「does not provide a formal guarantee of answer correctness」。

## 为什么仍然有用

- 把「没检索到」与「检索到但没用」分开：`unrelated` vs `related`。
- 给答案一个可排序的可靠性字段；比纯文本 RAG 多一个可审计维度。
- 强制结构改变产出本身：没有依据的结论无法通过格式这一关。

## 结果（OA-RAG，条件）

- 3 个本体（GO/FoodOn/SNOMED）、6 个医学 QA 任务、2 个 backbone。
- 平均准确率 50.5%（Llama）/ 68.1%（Qwen）；Tests 1–2 比最强基线 +10–15 pp。
- Test 3 同 8k context：84.9% vs 66.7%；9.7k vs 96.7k tokens/问；5.8 vs 22 calls。
- grounding：entailed+supported 占 70.0%（Llama）/ 53.2%（Qwen）；unrelated 0.2% / 7.8%。
- Qwen Test 3：entailed 94.9% 正确、supported 82.1% 正确（切片，不是校准曲线）。
- 检索瓶颈：gold evidence 完全检索 61.7% MCQ vs 23.6% OQ。

> 出处：Table 2/3、§6.2–6.3；OA-RAG digest §4。

## 失效模式

- **等级自评**：模型给自己打分；相关性是经验观察，不是保证。
- **等级通胀**：全标 supported，字段存在但无区分度。
- **引用形式化**：引用了文档，但结论与文档无关。
- **格式开销**：每个结论都带证据，长输出里成本可观。
- **等级未校准**：不知道 entailed 的 precision/recall；不能自动放行。
- **把等级当形式证明**：作者自己说没有形式保证。

## 与本体 / 回路的关系

本体在输出时以 **concept card / entailment / 注释** 出现；约束强度弱到中（能约束格式与声明，不能保证语义真值）。被违反时通常没有自动信号，需要 checker/人审。

## 关联

- [OA-RAG digest](../../../src/papers/2610.36335-oa-rag/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
- [checker](../checker/README.md)
