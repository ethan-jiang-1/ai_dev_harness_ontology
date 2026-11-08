# 精化 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 问题

真实项目很少从零建本体；更常见的是「已经有一个，但不够用/有错/过时」。精化的难点不是「加一个概念」，而是**定位该修哪条子类关系/约束**，以及修了之后下游判定器会不会变好。

## 两种做法

| 做法 | 机制 | 代表 | 规模/局限 |
|---|---|---|---|
| 嵌入 + LLM 找高置信修复 | 微调嵌入找候选（30 条可疑公理 × 10 候选父类），LLM 判定，专家复核 | CASTON | 单一本体、6 条高置信修复全部接受；medium 全 mixed |
| 匹配 + 轻量精化 | RAG 检索结构/词法/定义知识，bisimilarity 剪候选，再做轻量精化 | KROMA | 多基准；优于经典与 LLM 基线，开销相当 |

## CASTON 的流程

1. **Candidate generation**：对每条 `A ⊑ B`，用 embedding 给所有候选父类排序；asserted parent 排名很低 → 可疑。
2. 取 top 30 条可疑公理；每条取 top 10 个替代父类。
3. **LLM validation**：给 child/当前父类/候选父类 + label/definition/domain/other axioms；返回 verdict/confidence/替换建议。
4. 只保留 high/medium；专家复核。

**数字**：CASTON 270 classes / 292 subsumption；default（fine-tuned OnT + Qwen3-8B）high 6/6（100%）；pretrained ensemble 4/7（57.1%）；GPT-4o mini 5/16（31.3%）；medium 全 mixed。

## 核心判断

**精化的瓶颈不是生成候选，而是定位与验证。** 给定本体 + 下游错误，能不能自动指出「该修哪条公理」，目前没有通用答案。CASTON 靠 embedding 排序 + 专家复核；KROMA 靠匹配基准；两者都没有把「下游错误 → 该修的公理」闭环。

## 失效模式

- **局部最优。** 只修高置信小问题，大的结构错误不动。
- **修了但没测下游。** 本体更「正确」，判定器不一定更好。
- **无回归测试。** 修一条子类关系，可能破坏另一条约束。
- **来源/版本丢失。** 不知道当前版本是谁改的、为什么改。
- **medium 不可靠。** 全 mixed；confidence 只能粗分。
- **本体层级本身不一致。** 失败案例显示，专家都不一致时方法会错。

## 与本体 / 回路的关系

本体在精化阶段是 **被修改的对象**；约束强度取决于修改后的验证。被违反时通常没有即时信号，需要专家/回归测试。

## 关联

- [CASTON digest](../../../src/papers/2610.21466-caston-refinement/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
- [generation](../generation/README.md)
