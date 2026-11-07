---
status: draft
updated: 2026-11-07
quality: A
based_on: card.md
claims: [E-06]
---

# Grid Agents · 消化

> 事实、数字、页码回 [card.md](./card.md)。这里只写**我们怎么用**、值不值得、哪里会坏。

## 工程思路

**要做受监管工程工作的 agent，按这个顺序：**

1. **先立三条原则，不是先选模型。** 证据先行（每个答案锚定源文）、solver 算数字、人做决策。三条都写进架构，不写进 prompt。
2. **把法规/标准做成可检索、可引用的知识系统。** 27 docs/6,347 pages；答案必须引用 passage；不能引用就不答。
3. **把领域研究做成工具。** 不是「给 agent 一个 pandapower 环境」，而是把潮流/N-1/短路/OPF 包成它真的会调用的工具；**工具必须到达研究**。
4. **数字只从 solver 来。** 模型选择/排序/解释研究；所有数值由成熟 solver 产生；不要让它手算大网络。
5. **验证「工作」，不只验证答案。** 重放工具调用，检查 study 跑在哪个 network state；同一个数字可能来自记忆/错状态/对的研究。
6. **人签核是架构的一部分。** 结论并列、决策需具名、研究在决策点暂停；不要把它当免责声明。
7. **记忆要有人批准。** semantic/procedural/episodic 三类；共享变更经人审批，避免一个工程师的会话悄悄改同事的 agent。
8. **reinforcement 用 optimizer，不要只靠 agent 设计。** 33–67% 更便宜；solver + optimizer 是互补，不是替代。
9. **同时报分数与时间。** Grid Studio 99.9% / 13.9 s；base model 40.8% / 58.2 s；只看分数会漏掉「慢且不可验证」。

## 实用意义

它解决的操作问题：

- **「法规几千页，审查员看不过来。」** → Grid Ontology 检索 + 引用；recall 0.967 vs 0.856。
- **「agent 算的数是错的。」** → solver 算；模型只选研究/读结果。
- **「答案对，但不知道跑的是哪个 grid state。」** → strict pass 重放工具调用；516/519 工作被验证。
- **「agent 有 domain tools，但不用。」** → PowerMCP 只被调用 46/519；工具必须接进研究路径，不是放在旁边。
- **「加固方案太贵。」** → optimizer 在环，33–67% 更便宜。
- **「一个工程师改的记忆影响所有人。」** → 共享变更人批准。
- **「base model 能不能直接做？」** → 最好 40.8%，大网络 0；agent+solver 才到 99.9%。

**何时用**：受监管工程；有成熟 solver；法规/标准可检索；需要审计；人可签核。

**何时别用**：没有 solver/工具；法规不可检索；需要完全自动无人决策；网络规模远超工具能力；no formal safety。

## 质量评估

- **证据类型**：实证·部署/基准（`已核`，一手技术报告；工业系统）。
- **样本与对照**：8 benchmark families/519 tasks；4–9,241 buses；多个 coding agent、retrieval pipeline、base model；strict pass；public leaderboards。
- **优点**：真实工业系统；证据引用 + solver + 人决策三原则；工作验证；速度/分数/成本都报；optimizer 结果。
- **主要威胁**：技术报告/系统不完全公开；benchmark 单研究；最大 9,241 buses；GB corpus 特定；无形式安全；长期维护未量化。
- **`quality: A` 理由**：工业部署 + 多 benchmark + 公开 leaderboard + 工作验证；外部效度受规模/域限制。

## 洞察

1. **受监管工作的正确架构是「证据 + solver + 人」，不是「更强模型」。** 三条原则同时约束答案、数字、决策权。`已核`
2. **工具必须到达研究。** Power-Agent 装了 PowerMCP，但只在 46/519 任务被调用，16 个单独解决；503 个仍靠 agent 自己写代码。**工具在环境里 ≠ 工具在回路里。** `已核`
3. **验证工作，不只验证答案。** 同一个数字可能来自对的研究、记忆、或错的 grid state；重放工具调用是唯一能分辨的方式。`已核`
4. **Base model 的上限很低。** 最好 40.8%，>2,000 buses 全 0；agent+solver 99.9%。**领域工作不是靠模型参数，是靠工具/求解器。** `已核`
5. **Optimizer 是「solver + agent」的下一层。** 33–67% 更便宜；agent 设计 package 会贵，因为不做全局优化。`已核`
6. **速度和准确率可以同时要。** Grid Studio 13.9s / 99.9%，比其他系统都快且准；关键是工具真正接进研究。`已核`
7. **记忆需要人批准。** 在 regulated work 里，共享记忆的变更不能静默；这是 P3 在 learning 上的延伸。`已核`
8. **这里的「ontology」是知识系统，不是 OWL 本体。** 作者明确说「organized body of domain knowledge, not a formal specification」。**别把它的成功当成形式本体的成功。** `已核`

## 成本与使能条件

| 成本 | 一次性 / 每次 | 说明 |
|---|---|---|
| 法规语料/索引 | 一次性/持续 | 27 docs/6,347 pages；更新/版本 |
| 领域工具/solver | 集成一次性 | 潮流/N-1/短路/OPF；工具 wrapper |
| 工作验证 | 每次 | 重放工具调用；日志/状态 |
| 人签核 | 每次决策 | 具名、暂停、审计 |
| 记忆管理 | 持续 | semantic/procedural/episodic；人批准 |
| Optimizer | 集成 | reinforcement planning；成本模型 |

**使能条件**：成熟 solver；可检索法规；领域工具；人可签核；能记录 study 状态。

**2022 年做会卡在哪**：长程 agent/工具调用不成熟；没有 519-task 统一 benchmark；solver wrapper/MCP 不成熟；但三原则本身不依赖模型版本。

**反向条件**：没有 solver；法规不可检索；需要完全自动；网络规模过大；无审计/签核。

## 与现有判断的关系

| 关联 | 关系 |
|---|---|
| **E-06** | 支撑「失败多归工作流」：工具是否到达研究、工作是否可验证，比模型大小更决定结果。 |
| **P1** | 强支撑：价值在约束/证据/求解器，不在知识注入。 |
| **P2** | 强支撑：同一模型，换工具/验证/人签核，结果与速度都变。 |
| [03 知识](../../../topics/03-knowledge/README.md) | 知识系统 + 引用；不是投影文本，而是可检索法规库 + solver。 |
| [02 判定](../../../topics/02-judgment/README.md) | strict pass 是「工作验证」的判定器；比答案准确率更强。 |
| [domains](../../../topics/domains.md) | 电网域：法规硬约束、数字由 solver 算、人决策。 |

## 不可迁移

- 技术报告；系统/数据不完全公开。
- 519 tasks 是单个研究；真实 connection study 串联多个研究。
- 最大 9,241 buses；真实运营商数万。
- GB corpus 特定；其他法规体系未测。
- 无形式安全保证；人签核是流程保证。

## 开放问题

- 数万 buses / 多研究串联是否保持？
- 法规更新/版本管理的长期成本？
- 人签核的吞吐/负担？
- 工具集成的可迁移性：换域（金融/医疗）要重做多少？
- strict pass 能否自动化到不需要人工检查？
- 「ontology 是知识系统」与形式本体（OWL/SHACL）如何结合？
