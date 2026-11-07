---
status: draft
updated: 2026-11-07
quality: B
based_on: card.md
claims: [05-L2, 05-L5]
---

# CASTON · 消化

> 事实、数字、页码回 [card.md](./card.md)。这里只写**我们怎么用**、值不值得、哪里会坏。

## 工程思路

**要做本体层级精化，按这个顺序：**

1. **先用 embedding 缩小搜索空间。** 对每条 `A ⊑ B` 给所有候选父类排序；只把 asserted parent 排名很低的 30 条拿出来。
2. **每条只给 10 个替代父类。** 不要把整个本体塞给 LLM；局部候选才能让判断可追溯。
3. **fine-tune embedding 到目标本体。** Default 100% vs pretrained ensemble 57.1%；这一步不是可选的。
4. **LLM 只做局部 yes/no/替换判断。** 给 child、当前父类、候选父类 + label/definition/domain/other axioms；返回结构化 JSON。
5. **用 confidence 做 triage。** High 可信（本文 6/6）；medium 全 mixed，必须人审；不要把人审预算花在 high 上。
6. **不要信任模型的 confidence 校准。** GPT-4o mini 的 high-confidence 只有 31.3% 被接受；Qwen3-8B 是 100%。换模型要重测校准。
7. **案例要看语义类型。** `chromite_sand` 从 `green_sand_molding`（工艺）改到 `foundry_sand`（材料）——embedding 抓的是语义关系，不是词面相似。
8. **本体本身不一致时，方法会失败。** `semisolid_metal_processing` 的层级本身有争议；专家都不一致。先修本体结构，再谈自动精化。

## 实用意义

它解决的操作问题：

- **「本体里有隐蔽的父类错误，人工看不过来。」** → embedding 排序 + LLM 局部验证，先看 30 条。
- **「LLM 直接看整个本体，既贵又不准。」** → 缩到 30×10 候选。
- **「微调 embedding 值不值？」** → 值：100% vs 57.1% 高置信接受率。
- **「模型的 high confidence 能不能信？」** → 取决于模型；GPT-4o mini 只有 31.3%，Qwen3-8B 100%。
- **「medium confidence 怎么办？」** → 人审；本文 medium 全 mixed。
- **「本体层级本身有争议。」** → 自动精化不能替代领域专家裁决。

**何时用**：有中等规模本体；有 embedding/LLM；有专家可审 high/medium；目标是父类替换。

**何时别用**：本体很小；层级本身不一致；需要关系限制/复杂公理；没有专家；需要大规模跨本体。

## 质量评估

- **证据类型**：实证·专家评估（`已核`，一手正文；小样本）。
- **样本与对照**：CASTON 270 classes/292 subsumption；3 设置；2 专家；5 分制；40 建议。
- **优点**：两阶段分工清晰；fine-tune vs ensemble 对照；模型对照；案例具体；代码开源。
- **主要威胁**：单一本体；6 条高置信；preliminary；medium 全 mixed；无下游；无跨本体。
- **`quality: B` 理由**：机制与对照干净，专家评估可信；但样本小、单一本体、初步结果。

## 洞察

1. **「缩小搜索空间」比「更强 LLM」更重要。** 30×10 候选让 LLM 只做局部判断；全本体审查既贵又不准。`已核`
2. **Embedding fine-tune 是主要增益来源。** 100% vs 57.1%；pretrained ensemble 的召回有，但 precision 不够。`已核`
3. **Confidence 校准是模型特定的。** Qwen3-8B high 100%；GPT-4o mini high 31.3%；换模型必须重测。`已核`
4. **High/medium 的分层有用。** High 可信任；medium 全 mixed；不要一视同仁。`已核`
5. **语义关系 ≠ 词面相似。** `chromite_sand` 是材料，`green_sand_molding` 是工艺；embedding 能抓这种区别。`已核`
6. **本体结构不一致时，自动精化会失败。** 失败案例的层级本身有争议；方法不能替代专家。`已核`
7. **小样本不能外推。** 6 条高置信、单一本体；需要更大规模验证。`已核`（作者自述）

## 成本与使能条件

| 成本 | 一次性 / 每次 | 说明 |
|---|---|---|
| Embedding fine-tune | 每本体一次性 | OnT + CASTON；GPU |
| Candidate generation | 每本体 | 292 条排序；轻量 |
| LLM validation | 每可疑公理 | 30 条 × 10 候选；Qwen3-8B |
| 专家评审 | high/medium | 2 专家；5 分制 |
| 维护 | 本体版本 | 重新排序/验证 |

**使能条件**：本体 + embedding 模型；LLM；领域专家；可微调。

**2022 年做会卡在哪**：本体 embedding/LLM 工具链不成熟；OnT 等 hyperbolic embedding 未普及；但两阶段思路可手写。

**反向条件**：本体很小；层级本身不一致；关系限制公理；无专家；跨本体规模大。

## 与现有判断的关系

| 关联 | 关系 |
|---|---|
| **05-L2** | 支撑「精化可自动化到小规模」：6/6 高置信接受；单一本体/少量修复。 |
| **05-L5** | 支撑「精化瓶颈是定位与验证」：embedding 定位候选，LLM/专家验证；medium 不可靠。 |
| **P3** | 支撑「判定是权衡」：high/medium 分层；precision 与召回权衡。 |
| [refinement](../../../topics/05-produce/refinement/README.md) | 核心文献；机制细节回 card。 |
| [representation](../../../topics/05-produce/representation/README.md) | 本体表示不是瓶颈；定位/验证才是。 |

## 不可迁移

- 单一本体（CASTON）、单一公理类型（subsumption）、6 条高置信修复。
- Preliminary；没有大规模/跨本体。
- Medium 全 mixed；confidence 只能粗分。
- 无下游任务；修复是否让应用变好不好说。
- 失败案例显示层级本身不一致时方法会错。

## 开放问题

- 更大本体/更多公理类型是否同样？
- Medium-confidence 能否通过更强验证/人审降级？
- 跨本体 fine-tune 的迁移成本？
- 下游任务是否因修复变好？
- 多层/关系限制公理能否用同一 pipeline？
- 能否把专家评审变成可学习的 reward？
