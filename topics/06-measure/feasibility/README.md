---
status: draft
updated: 2026-11-07
rq: [RQ5]
evidence: [E-08, E-13, E-14, E-15, E-16, E-17]
---

# 落地经济学：什么时候值得

> 这一页回答 RQ5：**不是「本体有没有用」，而是「在什么条件下、付多少成本、值不值得」。**
> 它是横切综合，不替代各派 README；证据回各派与 `src/`。

## 问题

同一个机制，在一种配置下是护栏，在另一种配置下是纯开销：

- 强模型 + 高基线：硬护栏可能回退（POLAR）。
- 时延硬约束：省 token 的证据替换可能不值（CAI）。
- 答案不在文本里：投影可能无效（N&D 的限定）。
- 没有训练信号：reasoning-state 策略退化成 prompt 模板（EvoMemState）。

所以「值不值得」不是本体质量问题，是**位置 × 成本 × 使能条件**的问题。

## 五个成本维度

| 维度 | 问什么 | 常见漏算 |
|---|---|---|
| 建设 | 一次性投入多少？谁维护？ | 本体/投影/registry 的人工建模 |
| 运行 | 每次查询/动作多少 token、时延、调用？ | 检索轮次、审批、重试 |
| 维护 | 源/工具/法规变更后怎么更新？ | 增量重抽、版本对账、回归测试 |
| 人审 | 多少比例需要人看？看的成本？ | 审批疲劳、false alarm 的信任损失 |
| 失败 | 机制失效时的代价？ | false veto、错误合并、漏检 |

## 机制成本表

| 机制 | 建设 | 运行 | 维护/人审 | 盈亏平衡/边界 | 证据 |
|---|---|---|---|---|---|
| 01 动作闸门（POLAR） | 每域本体（T1–T5、curator 权重） | 每次候选调用反向搜索；轻量 | 阈值校准；false-veto 未测 | 收益随基线能力下降；T1-only ≈ blanket veto | [POLAR digest](../../../src/papers/2610.08082-polar/digest.md) |
| 01 多模式分配（CASEL） | per-tool consequence 元数据；sandbox/approval | 每次 `p̂ĉ` + J(m) | 审批 8.7–13.8%；γ_m 假设 | harm–approval–cost 前沿；不是最低 HSR | [CASEL digest](../../../src/papers/2610.36570-casel/digest.md) |
| 01 推理闸门（OntoAct） | ontology schema + 世界知识构造 | 每次条件求值 + LLM 提议 | schema/记录维护；构造 token 另算 | 三值条件；固定 schema；模拟 | [OntoAct digest](../../../src/papers/2610.21983-ontoact/digest.md) |
| 02 checker（Ontology Catch） | curated/data-derived/LLM 本体 | curated 66k tokens/46s；data 28k/17s | 审计；false alarm 重试 | 必须先超过空结果重试基线 | [Ontology Catch digest](../../../src/papers/2610.37809-what-does-an-ontology-catch/digest.md) |
| 02 证据契约（OA-RAG） | concept cards + reasoner + SPARQL | 5.8 calls/9.7k tokens（Test 3） | grounding 校准；本体维护 | 同 8k 预算下 84.9% vs 66.7% | [OA-RAG digest](../../../src/papers/2610.36335-oa-rag/digest.md) |
| 03 投影（N&D） | 塔 + 投影（45k 字符） | prompt token；9B 可跑 | 投影/知识节点维护 | 答案在文本里才有效；9B+投影 > 750B 不带 | [N&D digest](../../../src/papers/2610.11768-narrow-and-deep/digest.md) |
| 03 编译（CAI） | 编译成本 `c`（query-equivalent） | 条件性 −91%/+1.9%；平均 −38% | 增量重抽；时延约 3× | `p_h > 2% + c/(0.929Q)` | [CAI digest](../../../src/papers/2610.41172-context-as-infrastructure/digest.md) |
| 04 记忆（FIRME） | registry/alias + 本体 | 每次匹配/更新 | false merge 污染；人审 | alias +7.8–12.1 pp CMR；token −7.2% | [FIRME digest](../../../src/papers/2610.40482-firme/digest.md) |
| 04 状态（EvoMemState） | 本体 + GRPO 训练 | 检索/遍历 + policy | 训练信号；多模态未测 | Acc@complete +11.5/+31.2 | [EvoMemState digest](../../../src/papers/2611.03743-evomemstate/digest.md) |
| 05 生成（OntoDoc） | 4 阶段 pipeline | 每 IRI 多次 LLM/检索 | 人审；假设层信息损失 | completeness 3.43→3.84；无下游 | [OntoDoc digest](../../../src/papers/2611.01276-ontodoc/digest.md) |
| 05 精化（CASTON） | 微调 embedding | 30×10 候选 + LLM | 专家审；medium 全 mixed | high 6/6；pretrained 57.1% | [CASTON digest](../../../src/papers/2610.21466-caston-refinement/digest.md) |
| 证据 + solver（Grid） | 法规语料 + 领域工具 + solver | 每次研究；13.9 s | 人签核；法规更新 | 99.9% vs base 40.8%；optimizer −33–67% | [Grid digest](../../../src/papers/2611.03534-power-system-agentic/digest.md) |

## 三个可算的盈亏平衡

1. **编译**：`p_h > 2% + c/(0.929Q)`。Q=1,000、c=10 → 3.12%；p_h=2.5% 仍亏。**平均 −38% 不能当上线依据。**
2. **分配**：没有单一 HSR 最小；按 harm–approval–cost 前沿选点。CASEL 8.7% approvals / 7.02% HSR；Risk-Menu 12.6% / 5.82%。**审批少 30% 是否值得多 1.2 点 HSR，是业务问题。**
3. **能力**：约束类收益随基线能力下降（POLAR）；知识投影的增益不随容量上升（N&D，H2 p=0.85）；9B 带投影 > 750B 不带。**没有一条适用于所有机制的「能力曲线」。**

## 使能条件（为什么现在才出现）

- **长上下文**：45k 字符投影、concept cards、法规语料可进 prompt。
- **工具调用/结构化输出**：agent 能查 SPARQL、调 solver、写 JSON；否则编译/验证接不上。
- **便宜的小模型**：claim 抽取、checker、投影生成不必用 frontier（CAI 用 glm-4-flash）。
- **可接的 solver/validator**：Grid 的潮流/N-1/OPF；OA-RAG 的 reasoner；SLB 的 solver。
- **可观测的 token/时延/审批**：没有 per-query ledger，就算不出 2%/3.12%。

**但本体编写、投影生成、memory registry 仍是人工成本**；这些论文没有把建模成本降到零。

## 决策规则（先问这五个）

1. **答案在知识里，还是要从语料里找？** 在 → 投影/说明；不在 → 编译/检索/solver。
2. **时延是硬约束吗？** 是 → 不要用「省 token 但加轮次」的替换；考虑 E1/决策门。
3. **能接受多少误报/审批？** 低 → data-derived checker + 空结果基线；高 → curated/多模式。
4. **复用次数够吗？** 编译/投影需要 `Q` 足够大；一次性任务不值得建。
5. **有训练信号/参考答案吗？** 没有 → 不要上 GRPO reasoning-state；用检索/规则。

## 问题 → 机制目录

| 操作问题 | 机制 | 证据 | 成本/边界 |
|---|---|---|---|
| 跨源实体同一性 | registry + alias；commit gate | FIRME；Commit Boundary | false merge；无实现 |
| 不可逆动作防护 | 可逆性 gate；多模式分配 | POLAR；CASEL | 能力反向；T1-only ≈ veto |
| 证据不足时授权 | claim-specific promotion；三态 | Commit Boundary；CASEL | 无实现；审批 |
| 大语料重复检索 | claim–evidence 编译 | CAI | `p_h` 门槛；时延 3× |
| 判定器误报/漏报 | 空结果基线 + data-derived checker | Ontology Catch | false alarm；无正确答案 |
| 本体维护/描述缺失 | 生成 + 精化 | OntoDoc；CASTON | 无下游；单一本体 |
| 评测方差/失败归因 | 配置轴；角色画像；trace | Agents are Systems；Diagnose；SLB | 4 tasks；position paper；闭源无 trace |

## 还不知道的

- **部署层回报**：治理、上手、审计通过率，仍只有定性断言（CAI/N&D）。
- **false veto / false defer**：POLAR 1,745 blocked decisions 无标签；Commit Boundary 无实现。
- **维护成本**：本体/投影/registry 的长期人工成本没有一篇量化。
- **配置方差**：54% 是 Agents are Systems 的估计；本仓库自有实验还没有测。
- **跨域迁移**：工业/金融/医学/电网各自的边界；没有统一对照。

## 关联

- 结论：[E-08](../../conclusions.md) / [E-13](../../conclusions.md) / [E-14](../../conclusions.md) / [E-15](../../conclusions.md) / [E-16](../../conclusions.md) / [E-17](../../conclusions.md)
- 派：[01](../../01-constraint/README.md) / [02](../../02-judgment/README.md) / [03](../../03-knowledge/README.md) / [04](../../04-state/README.md) / [05](../../05-produce/README.md)
- 方法：[metrics](../metrics/README.md)、[trace](../trace/README.md)、[mechanism](../mechanism/README.md)
- 实验：[EXP-003](../../../experiments/README.md)
