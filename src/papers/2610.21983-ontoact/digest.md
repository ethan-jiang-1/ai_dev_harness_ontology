---
status: draft
updated: 2026-11-07
quality: A
based_on: card.md
claims: [01-L3]
---

# OntoAct · 消化

> 事实、数字、页码回 [card.md](./card.md)。这里只写**我们怎么用**、值不值得、哪里会坏。

## 工程思路

**要做「推理期验证」，按这个顺序：**

1. **先定 schema。** 实体类型、关系、可观察属性、允许的公理形式。没有 schema，抽象会退化成自由文本规则。
2. **从记录里抽候选公理。** LLM 提议 `(axiom, sources)`；每条必须带来源记录，不能凭空写。
3. **准入检查，不是全收。** 类型检查 + 来源非空 + 该公理类型的测试全过，才进入世界知识；否则丢弃。
4. **条件用三值逻辑。** 每个条件在当前证据下是 ⊤ / ⊥ / ?；**? 触发观察/干预，不直接 block**。
5. **假设是一等对象。** 每个 hypothesis 有必需关系 + 非空条件集；状态 confirmed / refuted / open；后续证据可推翻。
6. **动作验证只看条件。** 违反 R_W 的条件/禁止 → block；缺读数只报 unresolved，不 block。需要解释支持的动作要求 confirmed hypothesis。
7. **block 后给 revision 反馈。** 不是简单拒绝；告诉 agent 哪条条件失败/未解析，让它改 claims/hypotheses/action。
8. **测 spurious interventions。** 只看最终成功率会被“重复失败后终于成功”骗；SI 是更敏感的指标。
9. **把知识构造与 evaluation 成本分开。** OntoAct 的 eval token 低，但构造世界知识的 LLM 调用不低；要算总账。

## 实用意义

它解决的操作问题：

- **「老师傅的维修日志在，但 agent 不会用。」** → 从日志抽 typed axioms + sources；LLM 提出假设，验证器检查条件。
- **「agent 反复换零件，最后碰巧修好。」** → 看 spurious interventions；OntoAct 1.9–2.4 vs IfR 6.4–17.8。
- **「缺一个读数，agent 就卡住或乱猜。」** → 三值条件：? 去观察，不 block。
- **「动作被拒，但不知道为什么。」** → condition report + revision；不是黑箱 veto。
- **「换了设备/型号，规则要重写。」** → 类型化抽象：规则写在类型/关系角色上，具体实体实例化。
- **「LLM 调用太贵。」** → 符号检查替代部分 LLM 推理；ALFWorld calls 13.7 vs 28.8，Mars tokens 0.84k vs 1.54k/step。

**何时用**：有可读的运行记录/日志；领域有稳定类型/关系；动作有前置条件；需要可审计的拒绝理由。

**何时别用**：没有 schema；环境机制频繁变化；记录质量差；需要实时低延迟；安全性要求形式保证（OntoAct 只给 auditability）。

## 质量评估

- **证据类型**：实证·基准（`已核`，一手正文；三个模拟环境）。
- **样本与对照**：Tacit-FLE 3 类型 × 3 规模；Mars 8 世界（7 modified 平均）；ALFWorld 134 unseen tasks；7 个 baseline；ablation/分析；human？无。
- **优点**：三环境；强 baseline；SI/turns/tokens 多指标；tacit knowledge benchmark 新；代码将开源；诚实写「不是 safety guarantee」。
- **主要威胁**：固定 schema/world mechanics；合成数据；无真实工厂；ALFWorld 任务数有限；知识构造成本未进 eval token；elimination 上 IfR 匹配/超过。
- **`quality: A` 理由**：多环境、多 baseline、多指标、机制清晰；但外部效度受合成/固定 schema 限制。

## 洞察

1. **本体在推理期最好的角色是「验证器」，不是「知识库」。** LLM 提议，符号检查条件；这比把本体塞进 prompt 更硬。`已核`
2. **三值条件（⊤/⊥/?）是关键设计。** 缺证据不是失败，是“去观察”的信号；这避免了「不知道就拒绝」和「不知道就放行」两个极端。`已核`
3. **假设必须可被推翻。** confirmed 不是永久；后续读数/干预结果可以 refute。**没有 revision 的验证只是静态规则。** `已核`
4. **Spurious interventions 是被低估的指标。** 最终成功率可以掩盖重复失败；OntoAct 的 SI 1.9–2.4 vs IfR 6.4–17.8。`已核`
5. **类型化抽象让经验可迁移。** 个案事实保留，规则写在类型/关系角色上；chain 任务 +31 pp 是最大优势。`已核`
6. **符号验证能省 LLM 调用。** ALFWorld 13.7 vs 28.8 calls；Mars 0.84k vs 1.54k tokens/step。**验证不是纯开销。** `已核`
7. **推理期约束不一定封顶表现。** 01-L3 的「推理限制在 curated KG 会封顶」是多 agent 诊断的设计；OntoAct 的「验证条件 + 假设 revision」反而提升。**约束的形式决定它是天花板还是护栏。** `推测`（跨论文综合）
8. **Auditability ≠ safety。** 作者明确说 verifier 是审计一步，不是安全保证；不能把「有验证器」当成「不会错」。`已核`

## 成本与使能条件

| 成本 | 一次性 / 每次 | 说明 |
|---|---|---|
| Ontology schema | 每域一次性 | 类型/关系/可观察属性/公理形式；需领域专家 |
| 世界知识构造 | 每 corpus 一次性 | LLM 抽候选 + admission + corpus check；成本不低 |
| 条件求值 | 每次 | 符号检查；轻量 |
| LLM 提议 | 每次/每轮 | 比 baseline 少 calls（ALFWorld 13.7 vs 28.8） |
| 记录/语料 | 一次性 | 维护日志/操作文档；质量决定上限 |
| 维护 | schema/环境变更 | 新类型/新条件；schema 学习未解决 |

**使能条件**：可读的记录；稳定的类型/关系；有前置条件的动作；能接受「验证器不是安全保证」。

**2022 年做会卡在哪**：LLM 抽公理/假设不稳；没有 FLE/Mars/ALFWorld 这类可交互环境；符号验证与 LLM 循环的工具链不成熟。

**反向条件**：没有 schema；环境机制频繁变化；记录质量差；需要形式安全保证；elimination 型任务（IfR 可匹配/超过）。

## 与现有判断的关系

| 关联 | 关系 |
|---|---|
| **01-L3** | **反例/ refinement**：多 agent 诊断把推理限制在 curated KG，可能封顶；OntoAct 用符号验证条件 + 假设 revision，反而提升。**推理期约束的形式决定它是天花板还是护栏。** |
| **P1** | 强支撑：本体作为验证器，直接约束动作/假设；不是知识注入。 |
| **P2** | 强支撑：同一 LLM，换「验证 + revision」harness，成功率/SI/token 都变。 |
| [reasoning-gate](../../../topics/01-constraint/reasoning-gate/README.md) | 核心文献；机制细节回 card。 |
| [00-harness/verification](../../../topics/00-harness/verification.md) | 三值条件 + 条件报告是「判定器」的一种实现。 |

## 不可迁移

- Tacit-FLE 是合成环境；不是真实工厂。
- ontology schema 与世界机制在评估中固定；schema 学习未解决。
- Mars/ALFWorld 的收益依赖 corpus 与环境；ALFWorld 134 个任务有限。
- 知识构造的 LLM 成本未进 eval token；总账可能不同。
- Verifier 是 auditability，不是 safety guarantee；不能用于安全关键认证。

## 开放问题

- schema 学习：能否从记录自动扩展 T，而不只是实例化？这是 05 生产的子问题。
- 真实工厂的传感器噪声/缺失数据下，三值条件是否仍可用？
- 知识构造成本 vs evaluation 成本的平衡；什么规模下值得？
- elimination 任务上 Why IfR 匹配/超过 OntoAct？是记录设计还是机制差异？
- 条件公理的覆盖率：多少动作没有适用 axiom？没有 axiom 时是放行还是 fallback？
- 能否把 verifier 的 condition report 做成标准审计格式？
