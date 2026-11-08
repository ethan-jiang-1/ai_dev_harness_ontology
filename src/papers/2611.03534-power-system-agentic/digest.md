---
status: draft
updated: 2026-11-08
quality: A
based_on: card.md
claims: [E-06]
---

# Grid Agents：受监管工程里的 agent，证据 + solver + 人

> 这篇消化不假设你读过论文。先讲清并网评估这项工作、Grid Agents 的三条原则，再看 519 个任务上的结果、成本与边界。

## 0. 三句话

1. **它问什么**：并网评估需要两种稀缺技能——按不断变化的法规核查申请；跑潮流/N-1/短路等 network studies。agent 能不能同时做这两件事，而且答案可审计？
2. **它怎么做**：Grid Ontology 承载法规/标准/工程知识（27 docs / 6,347 pages）+ 记忆；Grid Studio 把领域研究做成工具，所有数字由成熟 solver 算；人做最终决策；评估不仅看答案，还重放工具调用检查「工作」。
3. **它发现什么**：519 个任务/8 个 benchmark 家族上，Grid Studio **99.9%** 端到端、中位 **13.9 s**，比所有 baseline 又快又准；法规证据 recall **0.967 vs 0.856**；optimizer 让加固方案便宜 **33–67%**。

## 1. 它解决什么问题

### 1.1 背景

把新能源/负荷接到电网，先要做两件事：

- **法规**：申请要对照法律、grid code、标准（几千页，且不断改革）。
- **工程**：决定接在哪、需要什么加固；跑 power flow、N-1 contingency、short circuit、OPF 等研究。

这两件事都稀缺、都专家密集。agent 的三种典型失败：
1. 流畅但无来源的法规解释；
2. 大网络上的不可信算术；
3. 答案对，但「背后的工作」不可验证（跑错 network state、用错研究）。

### 1.2 论文的立场

受监管工作不能靠「更强模型」解决；要靠三件事：**证据引用、solver 算数字、人决策**。

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **并网评估（grid connection assessment）** | 新项目能不能接、接在哪、要做什么加固。 |
| **power flow** | 给定负荷/发电/拓扑，算各节点电压/潮流。 |
| **N-1 contingency** | 任一单一元件故障后，系统是否仍安全。 |
| **short circuit** | 故障电流水平。 |
| **OPF** | 最优潮流：在约束下找最小成本调度。 |
| **Grid Ontology** | 法规/标准/工程知识 + 记忆的知识系统；不是形式 OWL 本体。 |
| **Grid Studio** | 跑电力系统研究的 agent 系统；领域工具 + solver + optimizer。 |
| **strict pass** | 不只答案对，还要重放工具调用，检查研究跑在正确 network state。 |
| **E score** | 端到端任务得分（0–100）。 |
| **agent work time** | 每个任务的 agent 工作时间（秒）。 |

## 3. 它怎么做

### 3.1 三条设计原则

1. **Evidence before answers**：每个答案/发现都锚定到源文档或申请人提交的段落。
2. **Computation by established solvers**：模型选择/排序/解释研究，所有数字由 solver 产生。
3. **Human decision authority**：agent 准备，人决策；结论并列、决策需具名签核、研究在决策点暂停。

### 3.2 Grid Ontology

- **GB corpus**：27 个文档、6,347 页（含图表）。
- 检索/引用：只从找到的证据回答，必须引用 passage。
- **Memory**：semantic（领域/operator/project 事实、规则）、procedural（skill，如 connection study）、episodic（经验/教训）；共享变更需人批准。
- 作者明确：这里的「ontology」是 **organized body of domain knowledge，不是 formal specification**。

### 3.3 Grid Studio

- 把电力系统研究做成工具：agent 选研究/选 network state/读结果，solver 算。
- **Reinforcement planning**：需要加固时调用 optimizer 提 least-cost package。
- **Strict pass**：重放工具调用，检查 grid state 与研究是否匹配；不是只看最终数字。

### 3.4 一个具体例子

申请人提交并网申请：

1. Grid Ontology agent 检索法规，回答「需要哪些研究、哪些条款适用」，每条带引用。
2. Grid Studio 选择 network state，跑 power flow / N-1；数字由 solver 算。
3. 发现 overload → 调 optimizer 提加固 package。
4. Reviewer/Planning engineer 看 findings + 引用 + solver 结果，签核。
5. strict pass 重放工具调用，确认研究跑在正确的 state 上。

## 4. 结果：数字与条件

### 4.1 法规证据

| 指标 | Grid Ontology | 对照 |
|---|---|---|
| GB Regulation Set evidence recall | **0.967** | Claude Code 0.856 |
| LegalBench-RAG F1 | **0.980** | — |
| Enterprise RAG Challenge | **124.5**（第一） | 123.7 |
| ViDoRe V3 nDCG@10 | **70.23**（第一） | 70.01 |
| 正确拒答不可回答问题 | 45/51 | — |

### 4.2 端到端

| 系统 | E score | median work time |
|---|---|---|
| **Grid Studio** | **99.9%** | **13.9 s** |
| Codex CLI | 99.4% | 21.6 s |
| Power-Agent | 99.4% | 16.8 s |
| Claude Code | 85.4% | 22.0 s |
| GPT-6.1 sol（base） | 40.8% | 58.2 s |
| Fable 5.1（base） | 28.3% | 162.5 s |

- 519 tasks / 8 个 benchmark 家族；516/519 工作被验证通过。
- >2,000 bus 任务：Grid 108/109；Power-Agent 106；Codex 90；Claude 74；base 0。
- **工具必须到达研究**：PowerMCP 只在 46/519 任务被调用，16 个单独解决；503 个仍靠 agent 自己写代码。
- optimizer：加固方案平均便宜 **33–67%**。

> 出处：Table 3, p.6（法规证据）；Table 4, p.7（端到端/时间）；Table 5, p.7（optimizer）；§5.2。

## 5. 这些数字不能说明什么

1. **不是真实运营商规模。** 最大 9,241 buses；真实电网可达数万。
2. **不是完整 connection study。** benchmark 是单个研究任务；真实流程会串联多个研究。
3. **不是形式安全保证。** 人签核是流程保证；strict pass 是工作验证，不是证明。
4. **GB corpus 特定。** 其他法规体系未测。
5. **技术报告。** 系统/数据不完全公开；长期维护成本未量化。
6. **base model 对比受工具影响。** 40.8% 是 base model；agent+solver 才是 99.9%。

## 6. 工程上怎么用

### 6.1 复刻顺序

1. **先立三条原则，不是先选模型。** 证据先行、solver 算数字、人决策；写进架构，不写进 prompt。
2. **把法规/标准做成可检索、可引用的知识系统。** 答案必须引用 passage；不能引用就不答。
3. **把领域研究做成工具。** 不是「给 agent 一个环境」，而是把它真的会调用的研究包成工具；**工具必须到达研究**。
4. **数字只从 solver 来。** 模型选择/排序/解释研究；所有数值由成熟 solver 产生。
5. **验证「工作」，不只验证答案。** 重放工具调用，检查 study 跑在哪个 network state。
6. **人签核是架构的一部分。** 结论并列、决策需具名、研究在决策点暂停。
7. **记忆要有人批准。** semantic/procedural/episodic；共享变更经人审批。
8. **reinforcement 用 optimizer。** 不要只靠 agent 设计；solver + optimizer 互补。
9. **同时报分数与时间。** 只看分数会漏掉「慢且不可验证」。

### 6.2 成本与使能

| 成本 | 一次性/每次 | 说明 |
|---|---|---|
| 法规语料/索引 | 一次性/持续 | 27 docs/6,347 pages；更新/版本 |
| 领域工具/solver | 集成一次性 | 潮流/N-1/短路/OPF；工具 wrapper |
| 工作验证 | 每次 | 重放工具调用；日志/状态 |
| 人签核 | 每次决策 | 具名、暂停、审计 |
| 记忆管理 | 持续 | semantic/procedural/episodic；人批准 |
| Optimizer | 集成 | reinforcement planning；成本模型 |

**使能条件**：成熟 solver；可检索法规；领域工具；人可签核；能记录 study 状态。

### 6.3 何时用 / 何时别用

**用**：受监管工程；有成熟 solver；法规/标准可检索；需要审计；人可签核。

**别用**：没有 solver/工具；法规不可检索；需要完全自动无人决策；网络规模远超工具能力；需要形式安全保证。

## 7. 质量与边界

- **证据类型**：实证·部署/基准（技术报告；工业系统）。
- **强项**：真实工业系统；证据+solver+人三原则；工作验证；速度/分数/成本都报；optimizer 结果。
- **主要威胁**：技术报告/系统不完全公开；benchmark 单研究；最大 9,241 buses；GB corpus 特定；无形式安全；长期维护未量化。
- **`quality: A`**：工业部署 + 多 benchmark + 公开 leaderboard + 工作验证；外部效度受规模/域限制。

## 8. 与仓库判断的关系

- **E-06（已核）**：失败多归工作流；工具是否到达研究、工作是否可验证，比模型大小更决定结果。
- **P1**：价值在约束/证据/求解器，不在知识注入。
- **P2**：同一模型，换工具/验证/人签核，结果与速度都变。
- **03-L9**：受监管知识供给三原则；工具必须到达研究（PowerMCP 仅 46/519）。
- **domains**：电网域：法规硬约束、数字由 solver 算、人决策。

## 9. 还没解决 / 下一步

- **数万 buses / 多研究串联** 是否保持？
- **法规更新/版本管理** 的长期成本？
- **人签核的吞吐/负担？**
- **工具集成的可迁移性**：换域（金融/医疗）要重做多少？
- **strict pass 能否自动化** 到不需要人工检查？
- **「ontology 是知识系统」与形式本体（OWL/SHACL）如何结合？**

## 10. 原文

- arXiv:2611.03534
- PDF：`src/papers/2611.03534-power-system-agentic/`
- 系统/数据：技术报告，部分不公开。
