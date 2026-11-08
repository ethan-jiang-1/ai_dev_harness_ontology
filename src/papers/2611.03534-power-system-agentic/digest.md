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

### 4.3 这些数字之间的逻辑

- **为什么 Grid 99.9% 而 base 40.8%？** base 只有模型知识；Grid 有法规检索 + solver + 领域工具。差距主要来自「工具与求解器」，不是模型参数。
- **为什么 Power-Agent 也 99.4%，但更慢？** 它装了 PowerMCP，却只在 46/519 任务调用；503 个任务仍靠 agent 自己写代码。工具在环境里 ≠ 工具在回路里。
- **为什么 Grid 更快？** 工具覆盖了研究步骤，agent 不用每次从零写代码；13.9 s vs 21.6/16.8 s。
- **为什么人签核？** 不是准确率问题，是责任/合规问题；agent 准备，人决策。
- **strict pass 为什么重要？** 同一个数字可能来自对的研究、记忆、或错的 grid state；重放工具调用才能分辨。

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

### 6.4 最小落地清单

1. **先立三条原则。** 证据先行、solver 算数字、人决策；写进架构，不写进 prompt。
2. **建可检索、可引用的法规库。** 答案必须引用 passage；不能引用就不答。
3. **把研究做成工具。** 潮流/N-1/短路/OPF 包成 agent 真会调用的工具；工具必须到达研究。
4. **数字只从 solver 来。** 模型选择/排序/解释；所有数值由 solver 产生。
5. **strict pass 重放工具调用。** 检查 study 跑在哪个 network state。
6. **人签核是架构的一部分。** 结论并列、决策具名、研究在决策点暂停。
7. **记忆变更需人批准。** semantic/procedural/episodic；共享变更不能静默。
8. **optimizer 在环。** 加固方案不要只靠 agent 设计；solver + optimizer 互补。

## 6.5 工程配方（E3）

### 接口契约

- **citation**：`{doc_id, version, page, span, clause_id, retrieved_at}`；答案的每条法规结论必须带 citation；不能引用就拒答。
- **study tool**：输入 `{study_type, network_model, state_hash, solver_config}`；输出 `{result, solver_version, provenance, warnings}`；每次 study 记录 state_hash，strict pass 重放用。
- **strict-pass log**：`{task_id, tool_calls[], network_state_hash, study_type, pass|fail, reason}`；state 不匹配即 fail。
- **memory**：`{kind: semantic|procedural|episodic, content, source, approved_by, version}`；共享变更人批准。
- **pause/resume**：决策点 `{decision_id, findings, citations, signer, timestamp}`；未签核不继续。

### 参数

- 检索：chunk 大小、top-k、rerank 模型；论文未给，工程上固定并记录。
- 拒答阈值：证据不足/引用缺失的判定规则；45/51 是结果，不是阈值。
- solver：容差、超时、版本；N-1/潮流/短路/OPF 各自配置。
- strict-pass：state_hash 一致 + study_type 匹配 + solver 版本记录；不满足即 fail。
- E-score：任务级 0–100；论文的 99.9% 是结果，不是公式。

### 成本

- 法规语料：27 docs / 6,347 pages；治理/索引约 4–8 人周（`推测`）。
- 领域工具/solver：wrapper 集成 4–8 人周；商用 solver 授权费按厂商。
- 运行：每任务 13.9 s（论文）；token/算力按模型。
- 人签核：每次决策 5–15 分钟（`推测`）；审计/复核另计。
- 维护：法规更新/工具版本/记忆审批；按月变更比例估。

### stop condition

- 没有 solver/领域工具 → 停，不要用 LLM 手算。
- strict-pass 漏报 >0（state 不匹配未发现）→ 停，先修重放。
- citation precision <0.95 或拒答率异常 → 停，先修检索。
- 人签核吞吐 < 业务需求 → 不扩规模，先改流程。
- 法规不可检索/不可引用 → 不做。

### 第一个 sprint

2 周、4-bus 算例 + 3 条法规 + 单一 N-1：

1. citation 对象 + 拒答规则（阈值配置化）。
2. study 工具契约（network model/state hash/solver 版本/provenance）。
3. strict-pass 重放日志 + 判定脚本。
4. 决策点暂停 + 具名签核最小流程。
5. 20 个 held-out 任务：引用精度 ≥0.95、state 不匹配 0 漏报、人审分钟记录。
6. 交付契约 + pass/fail 判据，不追论文分数；第二 sprint 再谈成本/替代方案。

### 替代方案

- 商用并网/规划工具链 + 人审；只做法规检索不碰 solver；do-nothing（人工流程）。
- 论文 baseline 全是 agent harness，没有 buy/do-nothing 对照；build/buy 边界要自己补。

## 6.6 客户价值假设（V2/V3，`推测`）

- **受益者**：电网运营商/开发商/评审方；痛点：并网队列长、法规审查慢、研究返工、审计不可追溯。
- **指标**：申请周期（天）、评审工时/单、返工率、审计发现数、每单加固成本、strict-pass 违规率。
- **反事实**：不上 agent → 人工审查/研究；先测当前周期/工时基线。
- **V3 试点**：单运营商、20–50 单、4-bus/实际算例；成功 = 评审工时降 ≥20%、周期降 ≥10%、strict-pass 违规 0、引用精度 ≥0.95；失败 = 违规 >0 或工时不降；停止线 = 年省工时 < TCO。
- **反例**：真实网络数万 buses；法规版本频繁；人签核瓶颈；solver 授权/集成成本；无形式安全保证。

### E4 决策框架

- **TCO** = 法规语料治理 4–8 人周 + 工具/solver 集成 4–8 人周 + 授权费（RFQ）+ 每任务推理 + 人签核分钟 × 单价 + 维护。
- **收益** = `评审工时下降 × 工时价 + 周期缩短 × 单日价值 + 返工/审计发现减少`；先测当前周期/工时/返工基线。
- **替代**：build（agent+solver）/ buy（商用并网/规划工具 + 人审）/ 只做法规检索 / do nothing。
- **决策线**：12 个月收益 > TCO 且 strict-pass 违规 0 才扩；否则只做法规检索或不做。

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
