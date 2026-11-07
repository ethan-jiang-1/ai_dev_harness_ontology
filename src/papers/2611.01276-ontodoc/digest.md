---
status: draft
updated: 2026-11-07
quality: B
based_on: card.md
claims: [05-L6]
---

# OntoDoc · 消化

> 事实、数字、页码回 [card.md](./card.md)。这里只写**我们怎么用**、值不值得、哪里会坏。

## 工程思路

**要给知识图谱补术语说明，按这个顺序：**

1. **先做自适应 SPARQL 探索，不要单跳查询。** 先判 IRI 类型（class/property/instance），再按类型扫 outgoing/incoming/实例；class 少于 10 个实例就全取，并看 2–3 个实例的属性。
2. **加网页背景，但只作补充。** Wikipedia 适合通用词；Tavily 适合技术/小众词；rerank + 阈值；DB context 是权威。
3. **先写 assumptions，再写描述。** 每条 assumption 带 reasoning 和 triple 引用；至少一条引用 DB triple；这能把推断前提摆到台面上。
4. **描述要 lexicographer 风格。** 不直接命名 IRI；优先 instance-level、区分性事实；省略 id/date/status 等通用元数据。
5. **四个 agent 用共享 state 解耦。** 每个阶段读/写固定 key；可替换/消融，不互相调用。
6. **评估四维分开。** accuracy / clarity / completeness / cruciality；只看一个会掩盖 tradeoff。
7. **先和 naive 比，再和模板比。** Naive 在简单图上 accuracy/clarity 可能更高；模板 verbalizer 的 completeness 可能低到 1.2。
8. **承认没有下游评估。** 说明写得完整 ≠ 用户/agent 更能用；需要后续任务测。

## 实用意义

它解决的操作问题：

- **「本体里一半术语没有 rdfs:comment。」** → 自动生成说明；151 个术语上 completeness 3.43→3.84。
- **「模板 verbalizer 写出来的话像机器翻译。」** → 用实例数据 + 网页背景 + assumptions 生成更自然的说明。
- **「模型直接看 triples 写说明，漏关键信息。」** → 自适应探索 + 假设层；DB 权威、web 补充。
- **「知识图谱文档维护不起。」** → 四阶段 pipeline 可批量跑；但人工复核仍必要。
- **「说明写得好，但下游任务没变好。」** → 本文没测；不要假设文档质量 = 任务收益。
- **「专业域 vs 开放域。」** → SOCKG/BioBricks 上 accuracy/clarity 不差；DBpedia 上 naive 略高，说明简单图不需要复杂 pipeline。

**何时用**：本体术语缺说明；有 SPARQL endpoint；有实例数据；需要批量补文档。

**何时别用**：本体很小/很简单；没有实例数据；需要形式公理说明（模板更合适）；需要下游任务保证。

## 质量评估

- **证据类型**：实证·基准（`已核`，一手正文；151 terms，3 KGs，11 annotators）。
- **样本与对照**：3 KGs；naive + template verbalizer；assumption ablation；model selection；LLM judge + human。
- **优点**：多本体；assumption 中间层；人工评估；可复现代码；诚实写「语义瓶颈」。
- **主要威胁**：151 terms；无下游任务；LLM judge；人工只评 OntoDoc；跨语言/本体有限；描述质量 ≠ 本体质量。
- **`quality: B` 理由**：机制清晰、多本体、有人工评估；但无下游任务、样本有限、评估口径偏描述质量。

## 洞察

1. **自适应探索 > 单跳检索。** Completeness 3.43→3.84；专业域提升更大（SOCKG 3.26→3.84）。`已核`
2. **假设层是真正的贡献。** 先写 reasoning + assumptions，再写描述；win rate 54–61%。**把推断前提显式化，比直接让模型写更完整。** `已核`
3. **模板 verbalizer 只能覆盖显式公理。** Completeness 1.2–3.2 vs OntoDoc 3.9–4.0；实例数据里的语义它读不到。`已核`
4. **Accuracy/clarity 不是总赢。** DBpedia 上 naive 的 accuracy 4.30 vs 4.20、clarity 4.73 vs 4.47；简单图上复杂 pipeline 可能过度加工。`已核`
5. **DB 权威、web 补充是重要约束。** 网页能补背景，但也会引入噪声；本文明确把 web 当 supplementary。`已核`
6. **假设层是语义瓶颈。** 漏掉的关键细节后面拿不回来；作者自己指出这是 tradeoff。`已核`
7. **没有下游评估。** 描述质量提升不等于用户/agent 更能用；这是最大的空缺。`推测`（作者也未声称）
8. **人工与 LLM judge 趋势一致。** 但人工只评 OntoDoc 输出，没做 baseline 盲评；一致性证据有限。`已核`（有限）

## 成本与使能条件

| 成本 | 一次性 / 每次 | 说明 |
|---|---|---|
| SPARQL 探索 | 每 IRI | 50 triples / 10 tool calls 预算；可调 |
| Web 检索 | 每 IRI | Wikipedia/Tavily + rerank；API 成本 |
| LLM 调用 | 每 IRI | 4 个 agent；GPT-4.1 Mini 默认 |
| 人工复核 | 抽样 | 11 annotators；专业域需专家 |
| 维护 | 本体变更 | 增量重生成；未实现 |

**使能条件**：SPARQL endpoint/RDF；实例数据；网页检索 API；LLM API。

**2022 年做会卡在哪**：LLM 代理式 SPARQL 探索不成熟；网页 rerank/工具调用不成熟；但 pipeline 思路可手写。

**反向条件**：本体很小/简单；无实例数据；需要形式公理；需要下游任务保证。

## 与现有判断的关系

| 关联 | 关系 |
|---|---|
| **05 生产** | 生成路线之一：把本体变成人能读的说明；不是造本体结构。 |
| **03 知识** | 说明文本是投影的原料；与 concept card 相接。 |
| **P2** | 支撑「harness 不可分离」：同一 LLM，换自适应探索/假设层，completeness 提升。 |
| [generation](../../../topics/05-produce/generation/README.md) | 核心文献；机制细节回 card。 |
| [03/projection](../../../topics/03-knowledge/projection/README.md) | 生成的说明可视为一种投影产物。 |

## 不可迁移

- 151 terms / 3 KGs；跨更多本体/语言未测。
- 没有下游任务；不能声称「文档变好 → 任务变好」。
- LLM judge 可能偏好冗长；人工只评 OntoDoc 输出。
- 描述质量 ≠ 本体质量；生成说明不能替代本体修正。
- 假设层的信息损失未量化。

## 开放问题

- 描述变好后，下游任务/用户理解是否变好？
- 假设阶段最容易丢哪类事实？能否量化？
- 跨本体/多语言是否同样？
- LLM judge 与人工的偏好是否一致（需要 baseline 盲评）？
- 本体变更后如何增量更新说明？
- 能否把「说明质量」纳入本体发布流程？
