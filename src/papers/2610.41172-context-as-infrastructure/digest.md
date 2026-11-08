---
status: draft
updated: 2026-11-08
quality: B
based_on: card.md
claims: [E-01, E-08, E-14]
---

# CAI：知识编译，省的是预算不是准确率

> 这篇消化不假设你读过论文。先给结论，再解释「编译」是什么、怎么测、数字怎么读、工程上怎么用。

## 0. 三句话

1. **它问什么**：agent 在检索时反复查、反复读、把窗口塞满没用的段落；如果在检索之前先把文档「编译」成结构化工件（带证据的树、图、wiki、本体），值不值得？
2. **它怎么做**：在同一套 BM25/grep harness 下，只变工件与阅读方式；在 FRAMES 多跳问答上测准确率、token、时延；再给一个成本模型。
3. **它发现什么**：结构化工件**不提高准确率**；唯一测出正收益的是「叶子带逐字证据」的 claim–evidence 树——平均省 38% token，但省 token 可能用检索轮次/时延换；盈亏平衡是条件性的（2% 是无限视野，有限视野更高）。

## 1. 它解决什么问题

### 1.1 背景：检索已经变成 agent 循环

传统 RAG 是「一次检索 → 拼上下文 → 回答」。现在越来越多的系统是 **agentic retrieval**：模型自己写查询、读结果、改写查询、决定什么时候停。这套外围循环叫 **harness**。

harness 变强之后，准确率问题被解决了一部分：论文里的基线只用 BM25 + grep（两种词法检索），作答模型 MiniMax M3，在 BrowseComp-Plus 上 85%、多跳 FRAMES 上 91%——**没有任何向量索引、没有任何编译工件**。

但新问题出现了：**上下文成本**。循环会重复查同样的东西、重读同样的文档、把窗口塞满从未被使用的段落。过程消耗 token，但不产出一个答案。

### 1.2 论文的主张

作者把「检索前的整理」叫 **knowledge compilation（知识编译）**：在查询之前，用 LLM 把源文档加工成**不含于任何单一片段的结构**——导航层级、实体图、时间线、wiki、本体、记忆。

关键立场：**编译不需要是更好的检索器**。它可以是供给层：把「读什么、读多少」的成本降下来。准确率由 harness 负责，编译负责预算。

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **CAI** | 本文简称，指 Context as Infrastructure（把上下文当基础设施）。 |
| **agentic retrieval** | 模型在循环里自己查、读、改写、停，而不是一次检索。 |
| **harness** | 包住模型的运行框架：工具、上下文、循环、预算、停止条件。 |
| **BM25 / grep** | 两种词法检索；不依赖向量。 |
| **knowledge compilation** | 在查询之前把文档加工成结构化工件；本文的工件都带 lineage（指回原文 span）。 |
| **claim–evidence pair** | 一条规范化主张（claim）+ 一段逐字证据（span）+ 源 chunk/offset + 时效。 |
| **artifact** | 编译产物：导航树、实体图、wiki、本体、时间线、记忆等。 |
| **FRAMES** | 多跳 Wikipedia 问答基准；本文主实验 N=200。 |
| **gate / p_h** | 决策门；`p_h` 是门接受（认为证据充分）的比例。 |
| **break-even** | 编译成本回本所需的充分率/查询次数。 |

## 3. 它怎么做

### 3.1 三层结构

![Figure 1: Context as infrastructure](../../../src/papers/2610.41172-context-as-infrastructure/figures/fig-1-context-as-infrastructure.png)

> 原图：arXiv:2610.41172, p.4, Figure 1。版权归作者，研究评论用途。

**看什么**：供给（index time 编译）→ 契约（tools）→ 控制（query time harness）。编译发生在检索之前，但「什么进窗口、什么时候停」仍由 harness 决定；所以编译不是「换一个检索器」。

### 3.2 六段流水线

| 段 | 做什么 | 工程要点 |
|---|---|---|
| Parse | PDF/Office/HTML/表格/日志 → 规范表示 | 保留标题、列表、表格、页锚 |
| Chunk | 自然边界切块 | chunker 两臂固定，编译不与 chunking 混淆 |
| Enrich | 模型逐块抽 claim–evidence、实体、事件、本体标签、wiki | 本文抽取器 glm-4-flash |
| Validate | span 逐字比对；实体类型对本体；日期对文档；schema 对模板 | **不合法就丢弃，不让模型修** |
| Assemble | claim 聚类成树、实体成图、事件成时间线 | 内部节点是导航标签，不是摘要 |
| Register | 源版本、offset、抽取器版本、校验状态、ACL | 让审计/fallback/增量更新成立 |

### 3.3 claim 单元与 tree 模板

`(c, e, s, τ)`：规范主张、逐字证据 span、源 chunk + 字符偏移、时效。**没有可定位 span 的 claim 不入库**；表示有损于文、无损于出处。

Tree 模板：`extract.unit=claim_evidence`、`require_verbatim_span=true`、`validate=span_match`、`leaves=evidence_units`、`internal_nodes=embedding_clusters`、`summary_nodes=false`、`serve.default=evidence_substitution`、`fallback=raw_chunk`。

### 3.4 三种服务模式

| 模式 | 做什么 | 代价 |
|---|---|---|
| E1 evidence-first | 直接在证据索引上词法检索 | 少一跳；优于「先找文档再下树」 |
| E2 substitution（默认） | 照常检索原文，定位到 chunk 后用 claim–evidence 替换 | 省 token，但增加检索轮次 |
| E3 decision-gated | 小决策模型判断是否值得深读 | 控制读不读；无证据时省约 30% token |

**树是 carrier，不是 retriever。** 检索始终是词法的；语义步由 agent 改写查询完成。

### 3.5 一个具体例子

问题：某条法规的例外条款是什么？

- 未编译：agent 先搜文档，读整段，可能读 3–5 个 chunk 才找到条款。
- 编译后：claim–evidence 叶子直接给出「例外条款：X；证据：原文第 12 段，逐字」；E2 只把这一段替换进上下文。
- 如果证据不足：叶子为空，agent 继续检索；miss 的代价是 +1.9% token（因为还要读原文）。

## 4. 结果：数字与条件

### 4.1 结构化工件没有准确率增益

| 工件 | FRAMES 准确率 | token |
|---|---|---|
| 无编译 BM25/grep 基线 | 91.0% | 324,479/问 |
| Claim–evidence 树 | acc. neutral | 平均 **−38%** |
| RAPTOR 摘要树（去 claim） | acc. neutral | — |
| PageIndex 大纲（去 claim） | neutral → 大规模负面 | — |
| 实体图 | acc. neutral | — |
| LLM wiki | acc. neutral | — |
| 本体 | **not measured** | — |

条件：FRAMES N=200；BM25/grep harness；MiniMax M3；glm-4-flash 抽取；单次运行、无 CI/重复种子。

> 出处：§5 主结果 / Table 4（FRAMES 各行）；基线 85%/91% 在 §1 与 §5；token 端点 §5。

### 4.2 token 收益是条件性的

| 条件 | 总查询 token 变化 |
|---|---|
| 证据充分（gate hit） | **−91%** |
| 证据不充分（gate miss） | **+1.9%** |
| FRAMES 平均 | **−38%** |
| 决策门（有证据，arm mean） | −52% |
| 决策门（无证据，arm mean） | −30% |

**平均会骗人**：−38% 是 −91% 与 +1.9% 的混合；不上报 hit/miss 分布，不能做上线决策。

> 出处：§6 成本模型 / Table 4；决策门 140→30 s 在 §6.4 与 Fig. 2。

### 4.3 成本模型

- 无限视野：`p_h > 2.0%`（`0.019/(0.91+0.019)`）。
- 有限视野：`p_min = 2.0% + c/(0.929Q)`；`c` 是编译成本（query-equivalent），`Q` 是查询次数。
- 例子：`Q=1,000, c=10` → `p_min=3.12%`；若 `p_h=2.5%`，仍亏 5.8 query-equivalent。
- 回本：`p_h≈0.43, c=10` → 约 26 次查询。
- 时延：证据替换用轮次换 token；配对子集 token 约减半，端到端时延约 **3×**；决策门把时延从 140 s 降到 30 s。

![Figure 2: token and latency](../../../src/papers/2610.41172-context-as-infrastructure/figures/fig-2-token-latency.png)

> 原图：arXiv:2610.41172, p.6, Figure 2。版权归作者，研究评论用途。

**看什么**：上图是条件性 token 变化（hit −91%、miss +1.9%、平均 −38%）；下图是决策门把时延从 140 s 降到 30 s。平均 −38% 掩盖了两端，时延代价在平均值里看不见。

> 出处：Fig. 2, p.6；配对子集时延 3× 在 §8/§6.4。

## 5. 这些数字不能说明什么

1. **不是「编译无用」。** 它说明在强词法 harness + FRAMES 上，结构化工件没有可检出的准确率增益；企业语料可能不同（但作者没测）。
2. **不是「本体无用/有用」。** ontology 一行的 FRAMES 结果是 `not measured`；作者把本体价值放在部署层（治理、集成），但 Table 2 的部署 ledger 没有任何一行达到预登记目标——**这是作者主张，不是观测**。
3. **不是「零效应」。** 样本量不足以区分小效应与零；「无可检出」不等于「没有」。
4. **不能外推到企业语料。** FRAMES 是英文 Wikipedia；表格/扫描/行话会降低抽取质量、抬高 miss、减少节省。
5. **PageIndex 的负面是规模观察**，不是普遍规律；75% routing 是解析模型，不是实测。
6. **`p_h` 是 gate 接受率，不是正确率。** 门放行了多少，不等于放对了多少；false-accept rate φ 没测。
7. **平均 −38% 不能当上线依据。** 必须看条件分布、时延、复用次数。

## 6. 工程上怎么用

### 6.1 复刻顺序

1. **先量基线。** 用 BM25/grep + 现有 agent 跑目标语料，记录准确率、token/问、时延、轮次。
2. **先选目标成本。** 省 token 还是省时延？两者在这篇论文里是反向的。
3. **保留原检索器。** 默认 E2；不要一上来换 dense/树路由。
4. **只编译证据，不编译散文。** 每个 claim 带逐字 span；span 对不上就丢弃。
5. **抽取器可以用小模型。** 质量由 validation 保证，不由模型大小保证。
6. **树只做 carrier。** 内部节点用聚类标签；叶子是证据。
7. **先算账再上线。** 用 `p_h`、miss penalty、`c`、`Q`、时延预算算 `p_min`。
8. **把审计和交付门分开。** `p_h` 是接受率；φ 要单独估。
9. **按 collection 做部署测量。** shadow/A-B 用 collection hash 分桶；目标预登记；null 报 null。

### 6.2 成本与使能

| 成本 | 一次性/每次 | 说明 |
|---|---|---|
| Parse + chunk | 一次性 | 便宜；chunker 与基线固定 |
| Enrich | 一次性 | 小模型逐块并行；与查询无关 |
| Validate + register | 一次性 | 逐字比对；offset/版本/ACL |
| 查询 token | 每次 | 条件性：hit −91%、miss +1.9%、平均 −38% |
| 检索轮次/时延 | 每次 | 替代用轮次换 token；配对子集 3× |
| 人工审计 | 一次性/周期 | 100–400 条标注估 φ；本文未跑 |
| 维护 | 变更时 | 增量重抽；registry/版本管理 |

**使能条件**：强词法 harness + 会改写查询的 agent；便宜的小抽取器；逐字 span 校验；可增量、带 lineage 的工件注册；能观测 token/时延。

**2022 年做会卡在哪**：抽取模型更贵更弱；claim-level span 校验不成熟；agent 循环/工具调用不稳；没有「harness 固定、只变工件」的对照意识。

### 6.3 何时用 / 何时别用

**用**：语料相对稳定、查询复用高、token 是主要成本、审计要求高、文本为主可抽取。

**别用**：时延硬约束；查询视野小；表格/扫描/行话导致抽取质量差；没有审计/版本管理；`p_h` 低于 `p_min`。

## 7. 质量与边界

- **证据类型**：实证·基准 + 成本模型（一手正文）。
- **强项**：对照干净（只变工件/服务模式）；同时给反证；成本模型可复用；局限写得诚实（无 CI、单基准、部署 ledger 为空）。
- **主要威胁**：单基准、单 compiler、单 answer model；无置信区间/重复种子；FRAMES 是英文 Wikipedia；PageIndex 负面是规模观察；φ 未测；部署层无观测。
- **`quality: B`**：机制与成本模型强、内部对照干净；但外部效度、复现次数、部署观测不足。

## 8. 与仓库判断的关系

- **E-01（已核）**：强 harness 下结构化工件无可检出准确率增益；PageIndex 大规模负面。补充：基线 91%、单基准、无 CI；部署价值是作者主张。
- **E-08（已核）**：claim-leaf tree 是唯一测出正收益的工件；−91%/+1.9%/−38%；2%/43%。
- **E-14（已核）**：有限视野 `p_min=2%+c/(0.929Q)`；平均 −38% 不能当上线依据；时延约 3×。
- **C-04**：CAI 投影的是**证据**（claim+span），N&D 投影的是**领域知识**（本体塔）；两者都是「投影」，但 payload 不同。
- **P1**：支撑「价值在部署/治理」——但 CAI 的部署价值是作者定位，ledger 为空；只能标「作者这么说」，不能标「已证」。
- **RQ5**：提供最可操作的「何时值得」公式。

## 9. 还没解决 / 下一步

- **企业语料的 `p_h`/miss**：FRAMES 的 43% 不能外推；表格/扫描/行话会改变盈亏平衡。
- **φ（false-accept rate）**：`p_h` 不是正确率；需要 100–400 条标注审计。
- **时延代价**：证据替换的 3× 时延能否用并行/预算控制压下来？
- **增量维护成本**：文档频繁变更时，registry/重抽/聚类更新会不会吃掉 token 收益？
- **部署层回报**：治理/上手/审计通过率仍没有量化。
- **投影 vs 编译边界**：C-04 仍靠人工预判「答案在不在文本里」。

## 10. 原文

- arXiv:2610.41172
- PDF：`src/papers/2610.41172-context-as-infrastructure/`
- 代码/数据：论文未给独立仓库；实现细节见附录与正文。
