---
status: draft
updated: 2026-11-08
quality: A
based_on: card.md
claims: [01-L3]
---

# OntoAct：LLM 提议，本体验证

> 这篇消化不假设你读过论文。先讲清「本体作为验证器」是什么，再看它在三个环境上的结果、失败边界和工程用法。

## 0. 三句话

1. **它问什么**：工业/维修环境里的知识常常只以日志、笔记、操作记录存在，没写成可复用规则；agent 怎么把「个案经验」变成「下次能用的条件」，并在行动前验证条件是否成立？
2. **它怎么做**：把记录抽象成类型化的世界知识（实体类型、关系、条件公理）；LLM 提出假设/动作，符号验证器按当前证据检查条件，返回真/假/未知；缺证据就去观察，动作被拒就改。
3. **它发现什么**：在 Tacit-FLE（工厂隐藏故障）、Mars、ALFWorld 上，OntoAct 成功率高、无效干预少、LLM 调用/token 少；但它依赖预定义 schema 与合成环境，不是真实工厂。

## 1. 它解决什么问题

### 1.1 背景：tacit operational knowledge

老师傅知道「这个机器停了，先看上游料仓是不是空的」；但这条知识可能只存在于：

- 维护日志：「3 月 12 日，机器停，上游空，清空后恢复。」
- 操作笔记：「转子除湿机 auto self-stop 常和气流低一起出现。」
- 一次性干预记录：「换了过滤器，好了。」

这些记录写了「发生了什么」，但没写「为什么有用、什么时候适用」。论文把这种知识叫 **tacit operational knowledge**：通过观察、干预、结果表达出来，但没有被提升为可复用原则。

### 1.2 两个 gap

1. **抽象**：从个案恢复可迁移的模式（类型/关系角色），而不是记住具体机器。
2. **验证**：判断这些关系/条件在当前情境是否成立；缺证据时知道去观察，而不是猜。

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **Tacit-FLE** | 基于 Factorio Learning Environment 的工业维护基准；现有工厂 + 隐藏故障 + 维护记录。 |
| **world knowledge** | `K_W=(T, A_W, R_W)`：schema T、ground assertions A_W、conditional axioms R_W。 |
| **conditional axiom** | 「动作 X 需要条件 Y 成立」这类规则；带类型/关系。 |
| **symbolic verifier** | 用当前证据检查条件/动作的符号检查器；不靠 LLM 自评。 |
| **三值条件** | 条件在当前证据下是 ⊤（真）/ ⊥（假）/ ?（缺证据）。 |
| **hypothesis** | 对隐藏故障的候选解释；有 required relations + 非空条件集；状态 confirmed/refuted/open。 |
| **spurious intervention** | 没有修好、但消耗了回合的干预；最终成功可能掩盖重复失败。 |
| **Tacit-FLE 三种任务** | chain（跨记录依赖推断）、conjunction（多条件）、elimination（排除）。 |

## 3. 它怎么做

### 3.1 数据/环境

- **Tacit-FLE**：Factorio 环境里的现有工厂；3 种任务类型 × 3 个规模（small/medium/large）；维护记录/运行文档是合成的。
- **Mars**：8 个改机制世界，用 7 个 modified world 平均；测试生存/制作。
- **ALFWorld**：134 个未见 household 任务。

### 3.2 世界知识

`K_W=(T, A_W, R_W)`：

- T：ontology schema（实体类型、关系、可观察属性、允许的公理形式）。
- A_W：ground assertions。
- R_W：conditional axioms（动作要求、诊断模式）。
- 当前证据 A_t 加入后：`K_t=(T, A_W ∪ A_t, R_W)`。

### 3.3 构造：LLM 提议，本体准入

1. LLM 从记录批次提出候选公理 `(x_i, π_i)`（π 是来源记录）。
2. **Admissible**：schema 类型检查 + 来源非空 + 该公理类型的测试 `C_xi` 全过，才进入 A_W/R_W。
3. 最后做 corpus check。

### 3.4 推理与行动

- LLM 每轮提出 claims / hypotheses / action。
- claims 经 `f_admit` 检查类型、结构证据、引用模式；进入 A。
- 每个 hypothesis 有必需关系与非空条件集 Φ(h)；每个条件 `(u,p,op,z)` 在当前知识下求值：**⊤ / ⊥ / ?**。
- 状态：任一条件 ⊥ → refuted；全部 ⊤ → confirmed；否则 open。
- **动作验证**：违反 R_W 的条件/禁止 → block；**缺读数本身不 block**（只报 unresolved）。需要解释支持的动作要求 confirmed hypothesis；观察动作不需要。
- 被 block 时，LLM 可改 claims/hypotheses/action；新观察/干预结果更新 context 与 hypothesis。

### 3.5 一个具体例子

现象：机器停了，上游料仓空。

- 日志里学到：`machine_stopped ← upstream_storage_empty`（conditional axiom）。
- 当前观察：`machine_stopped=true`，`upstream_storage_empty=?`（没读数）。
- 验证器：条件 `?` → 不 block，建议「去看上游料仓」。
- 观察后：`upstream_storage_empty=true` → hypothesis confirmed；动作「清空料仓」允许。
- 如果读数显示 `false` → hypothesis refuted；去看别的条件。

## 4. 结果：数字与条件

### 4.1 Tacit-FLE

| 规模 | 方法 | 总成功率 | spurious interventions | turns |
|---|---|---|---|---|
| small | IfR | 64.3% | 6.4 | 17.4 |
| small | **OntoAct** | **78.6%** | **1.9** | **11.8** |
| medium | IfR | 66.7% | 11.9 | 31.7 |
| medium | **OntoAct** | **83.3%** | **2.4** | **19.4** |
| large | IfR | 65.0% | 17.8 | 42.6 |
| large | **OntoAct** | **90.0%** | **1.6** | **17.2** |

- 最优势在 chain 任务（跨记录依赖推断）：small 69.2%、medium 57.1%、large 82.4%；IfR 38.5/28.6/23.5。
- elimination 上 IfR 匹配或超过 OntoAct。

### 4.2 诊断收窄

| 指标 | OntoAct | WALL-E | IfR |
|---|---|---|---|
| distinct candidates/episode | **3.36** | 5.14 | 9.00 |
| fault in candidate set | **32/36** | 17/36 | 24/36 |
| fault in first 3 | **25/36** | 10/36 | 4/36 |

- target-aligned hypotheses 保留 71.4–90.0%；off-target 被 refute 95.6–99.6%。

### 4.3 其他环境

- Mars：平均 Score **15.92 vs 10.64**（ReAct*）；每环境步 evaluation tokens **0.84k vs 1.54k**。
- ALFWorld：success **98.5% vs 96.3%**（WALL-E）；LLM calls **13.7 vs 28.8**；tokens **32.16k vs 47.70k**。
- 共享资源条件：OntoAct 70/70 违规候选在执行前被重定向；发出命令 0/136 违规；IfR 只重定向 0/20，发出命令 20/107 违规。

> 出处：Table 1, p.6（Tacit-FLE）；Table 2, p.7（诊断收窄）；Table 3, p.8（Mars）；ALFWorld 在 §5.3。

## 5. 这些数字不能说明什么

1. **不是真实工厂。** Tacit-FLE 是合成环境；维护记录是生成的。
2. **schema 固定。** 评估用预定义 ontology schema 与世界机制；schema 学习未解决。
3. **verifier 是 auditability，不是 safety guarantee。** 作者明确不声称可部署。
4. **ALFWorld 134 任务有限；Mars 7 个 modified world。**
5. **知识构造成本不在 eval token 里。** 构造世界知识的 LLM 调用不低。
6. **elimination 上 IfR 匹配/超过。** 不同任务形态对机制有利/不利。

## 6. 工程上怎么用

### 6.1 复刻顺序

1. **先定 schema。** 实体类型、关系、可观察属性、允许的公理形式；没有 schema，抽象会退化成自由文本规则。
2. **从记录抽候选公理。** LLM 提议 `(axiom, sources)`；每条带来源，不能凭空写。
3. **准入检查，不是全收。** 类型检查 + 来源非空 + 该公理类型的测试全过，才进入世界知识。
4. **条件用三值逻辑。** ⊤/⊥/?；? 触发观察/干预，不直接 block。
5. **假设是一等对象。** 每个 hypothesis 有必需关系 + 非空条件集；状态 confirmed/refuted/open；后续证据可推翻。
6. **动作验证只看条件。** 违反 R_W 的条件/禁止 → block；缺读数只报 unresolved。需要解释支持的动作要求 confirmed hypothesis。
7. **block 后给 revision 反馈。** 告诉 agent 哪条条件失败/未解析，让它改 claims/hypotheses/action。
8. **测 spurious interventions。** 只看最终成功率会被「重复失败后终于成功」骗；SI 更敏感。
9. **把知识构造与 eval 成本分开。** eval token 低，但构造世界知识的 LLM 调用不低。

### 6.2 成本与使能

| 成本 | 一次性/每次 | 说明 |
|---|---|---|
| Ontology schema | 每域一次性 | 类型/关系/可观察属性/公理形式；需领域专家 |
| 世界知识构造 | 每 corpus 一次性 | LLM 抽候选 + admission + corpus check |
| 条件求值 | 每次 | 符号检查；轻量 |
| LLM 提议 | 每次/每轮 | 比 baseline 少 calls（ALFWorld 13.7 vs 28.8） |
| 记录/语料 | 一次性 | 维护日志/操作文档；质量决定上限 |
| 维护 | schema/环境变更 | 新类型/新条件；schema 学习未解决 |

**使能条件**：可读记录；稳定类型/关系；有前置条件的动作；能接受「验证器不是安全保证」。

### 6.3 何时用 / 何时别用

**用**：有可读运行记录/日志；领域有稳定类型/关系；动作有前置条件；需要可审计的拒绝理由。

**别用**：没有 schema；环境机制频繁变化；记录质量差；需要实时低延迟；安全性要求形式保证。

## 7. 质量与边界

- **证据类型**：实证·基准（三个模拟环境）。
- **强项**：三环境；强 baseline；SI/turns/tokens 多指标；tacit knowledge benchmark 新；代码将开源；诚实写「不是 safety guarantee」。
- **主要威胁**：固定 schema/world mechanics；合成数据；无真实工厂；ALFWorld 任务数有限；知识构造成本未进 eval token；elimination 上 IfR 匹配/超过。
- **`quality: A`**：多环境、多 baseline、多指标、机制清晰；但外部效度受合成/固定 schema 限制。

## 8. 与仓库判断的关系

- **01-L3**：推理期约束**限制知识源**（curated KG）可能封顶；**验证条件**（OntoAct 三值逻辑）不一定。约束形式决定天花板 vs 护栏。
- **E-16（已核）**：验证条件 + 假设 revision 可同时提高成功率与减少无效干预。
- **P1/P2**：本体作为验证器，不是知识注入；同一 LLM，换验证+revision，成功率/SI/token 都变。
- **00-harness/verification**：三值条件 + condition report 是「判定器」的一种实现。

## 9. 还没解决 / 下一步

- **schema 学习**：能否从记录自动扩展 T，而不只是实例化？
- **真实工厂**：传感器噪声/缺失数据下，三值条件是否仍可用？
- **知识构造成本 vs eval 成本**：什么规模下值得？
- **elimination 任务**：为什么 IfR 匹配/超过 OntoAct？
- **条件公理覆盖率**：多少动作没有适用 axiom？没有 axiom 时放行还是 fallback？
- **verifier 的 condition report 能否标准化为审计格式？**

## 10. 原文

- arXiv:2610.21983
- PDF：`src/papers/2610.21983-ontoact/`
- 代码/数据：论文称 camera-ready 发布。
