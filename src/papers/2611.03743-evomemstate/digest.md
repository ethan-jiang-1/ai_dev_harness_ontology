---
status: draft
updated: 2026-11-07
quality: A
based_on: card.md
claims: [04-L1]
---

# EvoMemState · 消化

> 事实、数字、页码回 [card.md](./card.md)。这里只写**我们怎么用**、值不值得、哪里会坏。

## 工程思路

**要做「状态化长期记忆」，按这个顺序：**

1. **事实与状态分开存。** Persistent Facts 保留原文/source/timestamp；Relational State 存 validity、scope、更新/冲突/约束。**不要用新事实覆盖旧事实。**
2. **增量建本体。** 每个事实挂到最具体的 concept 下；用 `PARENT_OF`/`CONTAINS` 组织；`CREATE/MERGE/SPLIT` 修订层级；`SUPERSEDES` 记录更新，`CONFLICTS_WITH` 保留冲突。
3. **检索用关系遍历，不用独立 top-k。** 先取 seed facts，再沿 `SUPERSEDES`/`CONFLICTS_WITH`/`CONTAINS` 双向拉齐；否则相关更新/冲突不会一起出现。
4. **Reasoning State 要学，不要写死 prompt。** 固定 self-reflection 在 preliminary 里反而把准确率从 50.5 拉到 48.9；用 GRPO 从「有/无 state 的答案得分差」学。
5. **Reasoning State 只写「怎么用」。** applicability / role / priority；不改写事实，不替代证据。
6. **评估分两层。** Complete Retrieval Rate 与 Acc@complete 分开；否则会把「检索不到」和「不会用」混在一起。
7. **看跨系统迁移。** 同一个 policy 加到 6 个 memory systems 上都有 +0.2–4.9；说明 reasoning state 是可复用的工件，不是绑定某个 memory backend。
8. **承认训练前提。** GRPO 需要参考答案/评分器；真实个人助手没有这个条件时，只能用弱监督/人工反馈替代。

## 实用意义

它解决的操作问题：

- **「用户去年喜欢徒步，今年喜欢海滩，系统还推徒步。」** → `SUPERSEDES` + 当前 preference 的 Reasoning State。
- **「用户说预算 500，又说 900，系统不知道信哪个。」** → `CONFLICTS_WITH` 保留冲突，Reasoning State 标「未解决」。
- **「所有相关记忆都检索到了，模型还是用错。」** → 状态化使用；Acc@complete 70.8 vs baseline 低 11.5–31.2。
- **「记忆越存越碎，关系丢了。」** → ontology + relational traversal。
- **「换个记忆后端，效果就崩。」** → reasoning-state policy 跨 6 个系统迁移 +0.2–4.9。
- **「固定反思 prompt 有用吗？」** → 不一定；本文 preliminary 显示平均下降 1.6 点。

**何时用**：长期个人助手；偏好/约束/经历跨会话变化；冲突需要保留；有答案/评分器可训练策略。

**何时别用**：单次会话；没有训练信号；多模态为主；需要形式可验证的状态；实时低延迟。

## 质量评估

- **证据类型**：实证·基准（`已核`，一手正文；四个基准、9 baselines）。
- **样本与对照**：MemSyco、MemTrap、LoCoMo、LoCoMo-Refined；Qwen3-8B/GPT-4o-mini；ablation；跨系统迁移；代码开源。
- **优点**：多基准；两状态分解清晰；ablation 完整；跨系统迁移；preliminary 研究揭示「检索到 ≠ 会用」。
- **主要威胁**：文本 only；GRPO 训练需要答案/评分器；基准多为记忆使用/对话回忆；本体层级质量依赖抽取；Reasoning State 不可形式验证。
- **`quality: A` 理由**：多基准、多 baseline、ablation、迁移、开源；但训练前提与文本限制是外部效度扣分项。

## 洞察

1. **「检索完整」不等于「会用」。** EvoMemState 的 Complete Retrieval Rate 85.6% 与 MemoryBank 86.4 相当，但 Acc@complete 70.8 vs 36.8；增益在**使用**，不在检索。`已核`
2. **固定 self-reflection 会帮倒忙。** 平均 50.5→48.9；说明「让模型再想想」不是 reasoning state。`已核`
3. **Relational State 对记忆使用任务最关键。** 去掉后 MemSyco −8.9、MemTrap −6.4；LoCoMo 只 −0.3，说明它主要修「关系/冲突」，不是「回忆」。`已核`
4. **Reasoning State 是更大的杠杆（尤其 MemTrap）。** 去掉 −8.0 / −15.0；只生成规则不做 RL 也差不多（−7.9 / −16.4），说明**规则内容不如「从使用反馈学」**。`已核`
5. **Reasoning State 可跨系统迁移。** 6 个 memory backend 加 policy 都有 +0.2–4.9；它是可复用工件。`已核`
6. **两状态分解是可复用的设计模式。** Persistent Facts（是什么）+ Relational State（现在怎么成立/冲突）+ Reasoning State（这次怎么用）。`推测`（设计判断）
7. **训练信号是最大门槛。** GRPO 需要参考答案/评分器；没有它，reasoning state 退化成 prompt 模板。`推测`

## 成本与使能条件

| 成本 | 一次性 / 每次 | 说明 |
|---|---|---|
| 本体构建 | 持续 | 抽取事实、概念挂载、CREATE/MERGE/SPLIT |
| Relational State 维护 | 每次新事实 | 更新/冲突/约束 |
| 策略训练 | 一次性/周期 | GRPO；需要答案/评分器；GPU |
| 推理 | 每次 | 检索 + 遍历 + policy 生成 reasoning state |
| 维护 | 本体/策略变更 | 重新训练/校准 |
| 评估 | 每 benchmark | Complete Retrieval + Acc@complete + judge |

**使能条件**：长期对话数据；答案/评分器；能跑 RL；本体/概念层级可维护。

**2022 年做会卡在哪**：LLM 事实抽取/本体构建不稳；GRPO/RLHF 工具链不成熟；长期记忆基准不成熟。

**反向条件**：单次会话；没有训练信号；多模态；需要形式保证；实时低延迟。

## 与现有判断的关系

| 关联 | 关系 |
|---|---|
| **04-L1** | **一手依据**：记忆是状态，不是事实集合；Relational + Reasoning State 在四个基准上提升。 |
| **E-05** | 支撑「本体承担对齐与印证条件」：本体用于概念挂载/关系，不承担自由推理；Reasoning State 是学出来的策略层。 |
| **P1** | 支撑「价值在结构/约束」：状态结构决定怎么用，不是知识注入。 |
| **P2** | 支撑「harness 不可分离」：同一 memory backend，加 reasoning state 就有 +0.2–4.9。 |
| [memory](../../../topics/04-state/memory/README.md) | 核心文献；机制细节回 card。 |

## 不可迁移

- 文本 only；多模态未测。
- 四个基准都是记忆使用/对话回忆；开放域长期部署未测。
- GRPO 需要参考答案/评分器；真实个人助手没有这个条件。
- 本体层级质量依赖抽取；错误挂载会影响 relational state。
- Reasoning State 是自然语言/结构化规则，不是形式可验证保证。

## 开放问题

- 没有参考答案时，reasoning-state policy 怎么训练？弱监督/偏好反馈可行吗？
- 本体层级（CREATE/MERGE/SPLIT）的自动质量如何评估？
- 多模态扩展：文档/图片/artifact 如何进 relational state？
- 跨域（工作/医疗/金融）是否同样有效？
- Reasoning State 能否形式检查/审计？还是只能是自然语言指导？
- 训练成本 vs 收益：多少用户/多少对话才值得？
