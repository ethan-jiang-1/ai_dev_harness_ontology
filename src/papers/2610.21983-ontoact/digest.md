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

### 4.4 这些数字之间的逻辑

- **为什么「验证条件」比「限制知识源」更少封顶？** 前者只检查动作/假设的条件是否成立，不限制模型从哪些知识推理；后者把候选限制在 curated KG，KG 没有的诊断永远出不来。
- **三值条件为什么重要？** ⊤/⊥/? 把「缺证据」与「不允许」分开；? 触发观察/追问，而不是直接 block。直接 block 会把「不知道」变成「不允许」。
- **为什么 spurious interventions 降得比成功率多？** 验证器在动作前拦掉不满足条件的干预，并给 revision 反馈；成功率是最终结果，SI 更直接反映「少做无效动作」。
- **schema 覆盖率为什么决定它是选择性护栏？** 没有适用 axiom 的动作/假设只能放行或 fallback；覆盖率低时，它只覆盖一小部分动作。

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

### 6.4 最小落地清单

1. **先定 schema。** 实体类型、关系、可观察属性、允许的公理形式；没有 schema，抽象会退化成自由文本规则。
2. **从记录抽候选公理。** 每条带来源；不能凭空写。
3. **准入检查。** 类型检查 + 来源非空 + 该公理类型的测试全过，才进入世界知识。
4. **条件用三值逻辑。** ⊤/⊥/?；? 触发观察/干预，不直接 block。
5. **假设是一等对象。** 每个 hypothesis 有必需关系 + 非空条件集；状态 confirmed/refuted/open。
6. **动作验证只看条件。** 违反 R_W 的条件/禁止 → block；缺读数只报 unresolved。
7. **block 后给 revision 反馈。** 告诉 agent 哪条条件失败/未解析。
8. **测 spurious interventions。** 只看最终成功率会被「重复失败后终于成功」骗。

## 6.5 工程配方（E3）

### 数据契约

| 对象 | 字段 |
|---|---|
| condition | `(u, p, op, z)`：实体/关系、属性、比较符、值；求值 ⊤/⊥/? |
| axiom | `{id, type, action, conditions[], sources[], created_by, version}` |
| claim | `{id, subject, predicate, object, source, confidence}` |
| hypothesis | `{id, required_relations[], conditions[], state}` |
| block payload | `{action, failed_conditions[], unresolved[], evidence_refs[]}` |

- 公理准入：类型检查 + 来源非空 + 每类 2–3 条测试（C_xi）+ corpus check（至多一条矛盾 transition）；不过不进入世界知识。
- `f_admit` 字段级规则要写死：类型/来源/引用模式/时间范围；不能只写「测试全过」。

### 接口

- `verify(action, K_t)` → `{allowed|blocked, failed_conditions[], unresolved[]}`；`?` 触发观察/追问，不 block。
- `revise(block_payload)` → 更新 claims/hypotheses/action；回传结构固定，agent 才能学。
- `observe(reading)` → 更新 A_t；`corpus_check(axioms)` → 矛盾/覆盖报告。

### 参数与 stop

- turn budget 20–40；block 后重试 ≤3；`?` 累积 3 条转人工；axiom 覆盖率 <40% → 停（选择性护栏）。
- false-block >10% 或 unresolved >30% → 降级到纯 LLM 基线 + 事后审计。
- corpus check：至多一条矛盾 transition；schema 变更后重跑。

### 成本

- schema 建设：5–10 专家人日（`推测`）。
- corpus 知识构造：每 1,000 条记录约 20–50 次 LLM 调用 + 人工抽检（`推测`）；eval token 不含构造。
- 运行：符号求值轻量；LLM 提议调用为主。
- 维护：schema/环境变更重跑；规则过期复审。

### 第一个 sprint

2 周、单域单故障类、10–15 人日：

1. 从 20–40 条维护记录定 schema（3 实体 + 2 关系 + 可观察属性 + 公理形式）。
2. LLM 抽 30–50 条带来源候选公理，实现准入门 + 每类 2–3 测试；人工抽检 20 条。
3. 实现三值求值 + condition report + block→revision；先用记录脚本回放，不接真 LLM 循环。
4. 20–30 个历史 episode 回放；报 SI/成功率/block 率/? 比例/公理覆盖率。
5. 预写 go/no-go：覆盖率 <40% 或 false-block >10% 停，退回纯 LLM 基线。

### 替代方案

- 纯 LLM + 事后审计；curated KG/规则引擎；买 CMMS/知识图谱产品；开源 ontology + tool-calling。
- 论文只与 IfR/WALL-E/ReAct* 比；没有与这些工程替代做成本-效果。

## 6.6 客户价值假设（V2/V3，`推测`）

- **受益者**：工厂维护/值班班组；痛点：误诊、无效干预、专家工时、停机。
- **指标**：MTTR、每千次干预的无效干预数、专家工时/次、false-block 率、停机分钟。
- **反事实**：不上验证器 → 纯 LLM 诊断；先测当前 MTTR/SI 基线。
- **V3 试点**：单域 20–30 episode；成功 = SI 降 ≥30% 且 false-block ≤10%、专家工时降 ≥10%；失败 = 覆盖率 <40% 或 SI 不降；停止线 = 年省专家工时 < 维护成本。
- **反例**：schema 覆盖低；真实传感器噪声；环境机制频繁变化；无专家维护。

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
