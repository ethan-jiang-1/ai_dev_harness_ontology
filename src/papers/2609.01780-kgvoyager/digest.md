---
status: draft
updated: 2026-11-09
quality: B
based_on: card.md
claims: []
---

# KGVoyager：没有 ontology，就让 agent 在 endpoint 上现场探

> 自包含消化：不假设你读过论文或 `card.md`。先讲清「只有 endpoint」这个约束，再看 think–act–observe 三类工具怎么分工、**+3.7 个百分点**（不是 4 倍）是在什么口径与条件下得到的、以及它不能证明什么。
> 论文：KGVoyager, arXiv 2609.01780v2（首次提交 2026-09-01，v2 2026-10-15），Essam Wisam & Chengkai Li，UT Arlington。

## 0. 三句话

1. **它问什么**：领域 KG 常既没有可用的 ontology，也没有 text–SPARQL 例子，只剩一个 SPARQL endpoint——这种条件下还能不能自动把自然语言问题变成可执行 SPARQL？
2. **它怎么做**：把 query 生成当成「探索」：在 think–act–observe 循环里调用三类**与图无关**的工具（search 找类/属性/实例的 IRI，exploration 看属性在数据里实际怎么连，execution 跑草稿拿反馈），只预置一个 KB 级 class index，不预置 ontology、例子或图专用工具。
3. **它发现什么**：4 个领域 benchmark（394 题）× 4 个骨干 × 3 次运行，平均 F1 64.6% vs GRASP 60.9%（**+3.7 个百分点**，相对 +6.1%），成本 $2.43 vs $3.94（−38.3%），每题墙钟 85.6s vs 112.4s（−23.8%）（Table 3, p.7）。GRASP 是在**被给了 entity index 的最好情况**下比的。

## 1. 它解决什么问题

NL→SPARQL 的通行做法是「先给模型看东西」：给 ontology（类、属性、domain/range），或给成对的自然语言–SPARQL 例子（few-shot 或微调）。这两种供给在 Wikidata/DBpedia 这类开放域图上成立——模型见过、社区有数据集和工具。**领域 KG 不成立**，作者把缺口拆成三条（§1, p.1）：**ontology deficiency**（RDF 允许「有类型没层次」，缺类层次与属性特征）、**ontology opacity**（有结构但没文档解释）、**example scarcity**（造成对例子要同时懂领域、SPARQL 与本体）。

作者的应对是把假设压到最小：**SPARQL endpoint 是唯一普遍可假设的资源**，只剩两条前提——① 图用 W3C RDFS 的 `rdf:type` 标注类型；② 能用**一条 SPARQL 查询**取到「类列表」这个轻量索引，实体按需在类内查。第一条在 28 个 okn.us 图里 27 个成立（Appendix B），第二条在 QLever 上 27/28 成立（Table 2, p.6）。

四条路线的输入假设摆在一起（本 digest 归纳，非原文表格）：

| 路线 | 需要先有什么 | 语义从哪来 | 本仓库对应 |
|---|---|---|---|
| 微调 / 少样本 | 成对 text–SPARQL 例子（GGC 用了 119,409 训练对） | 权重 / 上下文例子 | `2607.28082-ggc` |
| ontology-in-context | 完整 OWL 本体 | 本体声明直接进 prompt | `2609.14652-nlkgq`（据其摘要） |
| 预建实体索引 + 工具 | 全实体索引（DBLP 21 GB / SOCKG 1.1 GB） | ontology 的 domain/range 注释 | GRASP（本文基线） |
| **运行时发现** | **只要 endpoint + class index（KB 级）** | **从数据采样出来** | **KGVoyager** |

值得测的理由：如果 agent 能自己探出 schema，「先建本体/先造例子」的前置成本就被摊到每次查询的延迟与 token 上——这是 03/querying 的核心权衡（**前置供给 vs 运行时发现**）。

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **endpoint** | 只接受 SPARQL 查询的 HTTP 服务；本文假设你只有它。 |
| **IRI / term→IRI 映射** | 类、属性、实例的全局标识符。映射 = 把「author」落到 `ds:Creator`、把「Jake Grozdanovski」落到 `dp2:9368`。 |
| **class index / entity index** | 前者是轻量类索引（所有类 + label/alias/实例数），KGVoyager 的全部预置；后者是 GRASP 需要的全实体索引（DBLP 140.9M 条 / 21 GB，SOCKG 7.1M 条 / 1.1 GB，Table 1, p.2）。 |
| **think–act–observe** | ReAct 式循环：想一步 → 调一个工具 → 读返回 → 再想。一次 iteration ≈ 一次工具调用。 |
| **hybrid retrieval** | 语义向量 + BM25，用 RRF 融合再 rerank；search 工具内部即此。配套**自适应过滤 δ**：低于「第一名分数 × δ」的候选砍掉，至少留 3 条，防候选表污染上下文。 |
| **row-major F1** | 主指标，沿用 Spinach。**论文未复述定义**；按名字是对「预测结果表 vs gold 结果表」逐行比对算 F1，不是执行成功率、也不是答案集合的 P/R（`推测`，引用前回 Spinach 核）。 |
| **complete failure** | 某 (模型, 图, 题) 在 3 次运行里 F1 全为 0（Appendix F, p.13）。 |

## 3. 它怎么做

### 3.1 循环与两个前提（§3, p.3）

`think → act(一次工具调用) → observe → think …`，出口只有 `answer()`（提交最终查询）与 `cancel()`（判定不可解）。

系统提示词（Fig. 9, p.14）规定 SEARCH → EXPLORE → CONSTRUCT AND TEST，要求「**永不在验证前提交 query**」，最后 `answer()`，不可解则 `cancel()`。`{{ knowledge_graphs }}` 是提示词里按部署替换的槽位——**换图不改代码、不改工具实现**，这是「KG-agnostic」在工程上的实际含义。

### 3.2 三类工具各做什么

| 组 | 工具 | 做什么 / 返回什么 |
|---|---|---|
| search | `search_all_classes(term, limit=10)` | 在**本地缓存的 class index** 上做 hybrid 检索，返回类 IRI + label + 实例数 + 分数；首次调用时才用 SPARQL 拉索引。 |
| search | `lookup_class_instances(class_uri, term, mode)` | 在**指定类内**按 label 找实例（默认 `labels_only`；`all_attributes` 扫全部字面量，更慢）；未命中时用更宽的 `fallback_term` 再按语义相似度筛。 |
| search | `search_all_properties(term, limit=10)` | 在缓存的**属性索引**（枚举全部 distinct predicate）上检索，返回 IRI + label + alias + domain/range（若有）+ 使用计数。 |
| exploration | `explore_property_usage(property_uri, max_sample=5000)` | **采样真实三元组**，聚合主语/宾语所属类、代表实例、计数 → 用数据反推 domain/range。 |
| exploration | `explore_entity_relations(entity_uri, num_ents=3)` | 列出该实体的入边/出边属性 + 每属性的示例邻居。 |
| execution | `execute_query(query)` | 在 endpoint 上跑，返回结果表或错误；既取最终答案，也验证草稿。 |

关键点：**三类工具里没有一个是「读本体」的**。`explore_property_usage` 明确说「从实际数据推断 domain/range，而不是读 ontology 注释（常缺失或不准）」（Fig. 11, p.15）。消融里连「属性 domain/range 搜索」工具都**故意藏掉**，full 与 ablated 都不给（§4.5, p.8）——这是全文对「无 ontology」最硬的操作化。

### 3.3 term→IRI 映射：四步，不是一次 embedding

1. **词 → 类**：`search_all_classes("author")` → `ds:Creator`（Fig. 2 第 1 步）。
2. **词 → 属性**：`search_all_properties("published")` 只返回期刊/图书属性，**漏掉会议边**——同义词搜索靠不住。
3. **名字 → 实例**：先定类再类内找（`ds:Conference` → `dsc:icsoft`；`ds:Creator` → `dp2:9368`），因此**不需要全图实体索引**。
4. **结构补全**：`explore_entity_relations(dsc:icsoft)` 看到入边 `ds:publishedInStream`，再定向搜一次确认是 `Publication → Stream`。

检索栈参数（Table 5, p.11）：embedding `BAAI/bge-small-en-v1.5`；BM25 top-20；dense top-10；RRF 等权、rank constant 61；reranker `bge-reranker-base` top-10；δ=0.125、至少留 3 条。

### 3.4 结构发现：为什么非要有 exploration

search 只能回答「哪个 IRI 像这个词」，回答不了「两类东西在数据里怎么连」。两个 exploration 工具补这一层：**属性用法**看同名属性实际连的是哪些类（论文例子：「located in」连组织→城市，「location」连事件→场馆）；**实体邻居**在属性搜索无结果时，从实体出发看它有哪些边——Fig. 2 第 8 步正是靠这个找到漏掉的属性。这也是与 GRASP 的三处差别之一（§2, p.2）：GRASP 用 ontology 注释区分属性，KGVoyager 从数据推断。

### 3.5 class index 怎么来、多大

- **怎么来**：`search_all_classes` **首次被调用时**用 SPARQL 拉一次，之后本地缓存（§3.1, p.4）；内容按输出反推是类 IRI + label + alias + 实例数（Fig. 10, p.15），**具体那条 SPARQL 未报告**。实例数意味着要对每个类做计数，这也解释了它在部分 endpoint 上超时（§4.3）。
- **多大**（Table 1, p.2）：DBLP **35 个类 / 2.7 KB**；SOCKG **91 个类 / 5.3 KB**；同两图 GRASP 的实体索引是 140.9M 条 / 21 GB 与 7.1M 条 / 1.1 GB——差 4–7 个数量级。另有一个**属性索引**（枚举全部 distinct predicate），**规模未报告**。

### 3.6 执行反馈怎么 refine，以及它靠什么停

`execute_query` 是唯一执行入口，双重角色：取最终答案 + 中途验证假设。反馈是**诊断式**的：空结果或报错 → 回退到 search/exploration 换属性或换三元组模式；提示词原话是「If results are unexpected, revisit earlier steps – you may have the wrong property, class, or triple pattern」（Fig. 9, p.14）。

**停止出口只有三个，都不是预算**：`answer()` 提交、`cancel()` 判定不可解、agent 卡住后放弃（Table 10 的 “Agent Gave Up”；它是否走 `cancel()` 论文未说明）。**论文没有报告 max iterations、token 预算或超时阈值**；`execute_query` 只建议「验证查询用 LIMIT」（Fig. 12, p.16）。实践上预算交给模型与外部超时。

### 3.7 一个具体例子（Fig. 2, p.5；§3.4, p.6）

问题：「Count the number of papers that Jake Grozdanovski has published in the International Conference on Software and Data Technologies」，DBLP 图，**10 次工具调用**：

| 步 | 调用 | 得到什么 |
|---|---|---|
| 1–3 | `search_all_classes` × author / paper / conference | `ds:Creator`、`ds:Publication`、`ds:Conference` |
| 4–5 | `search_all_properties` × author / published | `ds:authoredBy`；「published」**漏掉会议边** |
| 6–7 | `lookup_class_instances` × 会议名 / 人名 | `dsc:icsoft`、`dp2:9368` |
| 8 | `explore_entity_relations(dsc:icsoft)` | 入边 `ds:publishedInStream` |
| 9 | `search_all_properties("publishedInStream")` | 确认 `Publication → Stream` |
| 10 | `execute_query(COUNT…)` | `count = 1`，1 行，0.46s |

这个例子同时展示强项（搜索漏掉的边能靠 exploration 补回）与代价（**10 步里 9 步在找 IRI 和边，只有 1 步在生成 query**）。

## 4. 结果：数字与条件

### 4.1 主结果（Table 3, p.7）

条件：4 个 benchmark，每个 benchmark 上 4 个骨干 × 3 次独立运行取平均；GRASP 被给了 entity index（其最好情况）。

| Benchmark（题数） | KV F1 | GRASP F1 | ΔF1 | KV 成本 | GRASP 成本 | Δ成本 | KV 迭代 | GRASP 迭代 | KV 墙钟 | GRASP 墙钟 | Δ时间 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Climate Models KG (108) | 69.8 | 67.2 | +2.6 | $2.66 | $4.57 | −41.8% | 19.6 | 23.1 | 75.1s | 119.7s | −37.3% |
| SOCKG (98) | 71.3 | 68.9 | +2.4 | $2.20 | $4.00 | −45.0% | 19.3 | 25.0 | 57.0s | 108.6s | −47.5% |
| DREAM-KG (88) | 49.7 | 46.9 | +2.8 | $3.06 | $5.06 | −39.5% | 24.2 | 30.5 | 55.9s | 92.8s | −39.8% |
| DBLP-QuAD (100) | 67.5 | 60.8 | +6.7 | $1.79 | $2.13 | −16.0% | 15.1 | 15.1 | 154.2s | 128.7s | **+19.8%** |
| **平均** | **64.6** | **60.9** | **+3.7** | **$2.43** | **$3.94** | **−38.3%** | **19.6** | **23.4** | **85.6s** | **112.4s** | **−23.8%** |

- **F1 全胜，但幅度是 2.4–6.7 个百分点**，不是倍数。最大优势在 DBLP（+6.7），而 DBLP 恰好是唯一变慢的（+19.8%）：题面高度模板化、大量人名/论文名实体，GRASP 的实体索引一次查表就解决，KGVoyager 得先定类再类内搜（§4.3, p.7–8）。
- **Δ 列单位混用**：F1/迭代是绝对差，成本/时间是百分比（迭代平均 −3.8 次 ≈ −16.2% 相对）。引用时不要写「迭代 −38%」。
- **平均是「4 个 benchmark 均值的均值」**（macro），不是 394 题 pooled；每行内部还有一层 4 模型 × 3 运行的聚合，**题目层面是宏平均还是汇总未报告**（`推测`：逐题算 F1 再平均）。

### 4.2 「F1 提高约 4 points」的口径与分母（不是 4×）

- 原文（Abstract, p.1）是 "improves F1 by **∼4 points** on average"；对应 Table 3 的 64.6 − 60.9 = **+3.7 个百分点**。若换算成倍数：64.6/60.9 = **1.06×**（相对 +6.1%）。
- **分母**：平均行是 4 个 benchmark 的均值；再往里 4 模型 × 3 运行；题目 108+98+88+100 = **394**。F1 自身的分母是**结果行**（row-major），不是答案实体，也不是执行成功与否。
- 成本 −38.3% = 2.43/3.94；时间 −23.8% = 85.6/112.4。**成本单位与计价方式未报告**（每次运行总花费还是每题？含不含重试与缓存命中？按哪天的价目表？）；**token 数也未报告**，所以无法按单价自己重算。可核的只是同一套计价下的**相对降幅**（`已核`：算术；`未报告`：口径）。

### 4.3 索引可行性：这才是「KG-agnostic」的硬证据（Table 2, p.6；§4.1, p.6）

条件：28 个 okn.us endpoint，两种引擎（各图的 Apache Jena 端点、统一的 QLever 联邦端点）。

| | Jena entity | Jena class | QLever entity | QLever class |
|---|---|---|---|---|
| 成功 | 6/28（21.4%） | 19/28（67.9%） | 0/28（0%） | 27/28（96.4%） |
| 失败形态 | 19 失败（含 3 超时），均为不透明服务端错误 | 8 失败 + 1 超时 | 19 失败，全部内存崩溃 | 1 超时（wikidata） |

- 同一张图、同一个索引查询，**换引擎成功率从 21.4% 变 0%、从 67.9% 变 96.4%**——「能不能建索引」不只看图，还看端点实现。
- 别把两个 96% 混为一谈：Table 2 的 **96.4%** 是「class index 能在 QLever 上建起来」，Appendix B 的 **96%（27/28）** 是「图里有 ≥1,000 条 `rdf:type`」。两件事、两个分母。

### 4.4 逐模型：方法效应小于模型效应（Fig. 7 caption, p.13；Appendix D）

4 个骨干在 4 个 benchmark 上的 KGVoyager 平均 F1：GPT-6 Sol **78.2%**、Muse Glimmer 30B **69.8%**、Nemotron 3 Ultra **68.4%**、GPT-OSS-120B **41.9%**（四者均值 64.6，与 Table 3 对得上，算术已核）。模型间最大差 **36.3pp**，方法间差 **3.7pp**——**换模型比换方法影响大一个数量级**，任何「agentic navigation 提升 F1」的说法都必须先固定骨干。

作者另给一个观察：search 与 execution 的**相位重叠系数**越低（GPT-6 0.29）F1 越高，越重叠（GPT-OSS 0.45）越差（Appendix D）；相关，非因果（`推测`）。

### 4.5 消融：三个组件，没有 class index（Table 4, p.8）

条件：每组至少 2 模型 × 2 benchmark，F1 为 3 次运行 mean±std；「Abl.」= 去掉该组件。

| 去掉什么 | 配对（模型, benchmark） | ΔF1 | 成本/迭代 |
|---|---|---|---|
| `explore_entity_relations` | GPT-OSS/SOCKG 46.9→38.3；GPT-6/SOCKG 85.4→83.9；GPT-OSS/DBLP 58.5→55.1 | **−8.6 / −1.5 / −3.4** | 成本基本不变；迭代 −0.1~+1.7（两组上升） |
| `explore_property_usage` | Nemotron/SOCKG 75.5→74.8；GPT-OSS/Climate 33.9→21.4；Muse/SOCKG 79.9→75.7 | **−0.7 / −12.5 / −4.2** | 除 GPT-OSS/Climate 外，成本与迭代都降 |
| hybrid → keyword-only | GPT-OSS/Climate 41.2→36.3；GPT-OSS/SOCKG 46.9→20.4；Muse/Climate 79.2→78.1；GPT-6/DREAM 67.5→65.7 | **−4.9 / −26.5 / −1.1 / −1.8** | 四组迭代全部上升 |

- 最难看的数在 hybrid 那行：**GPT-OSS 在 SOCKG 上 46.9 → 20.4**（−26.5）。检索融合对弱模型是命门。
- 唯一「噪声内」是 Nemotron 的 property-usage（−0.7，作者自己说落在 run-to-run 波动里）。
- **没做的消融**：class index（结构性依赖，用 28 endpoint 的可行性代替）、迭代/token 预算（没有预算）、search 与 execution 工具（作者说 endpoint-only 系统不能去掉）。

### 4.6 给 ontology 的对照：只有 SOCKG 上的 grep 基线（Fig. 4, p.8；§4.3, p.8）

SOCKG 作者提供了 Turtle 本体，作者据此造了 **Grep Ontology** 基线：同一骨干、只有两个工具（整份本体上 `grep` + 执行 SPARQL）；KGVoyager 不给本体文件。

平均 F1 **71.3% vs 63.2%**（**+8.1pp**），成本 −36.4%、墙钟 −18.7%。分模型增益：GPT-OSS-120B **+19.6**、Muse Glimmer 30B **+9.5**（两个小模型最大），作者归因于 grep 输出过长导致 context rot。**这条基线不是「ontology 进上下文」**：grep 一个 Turtle 文件 ≠ 把完整 OWL 放进 prompt 让模型直接用（NLKGQ 那条路线）。它能说明「拿着本体乱 grep 不如现场探」，**不能**说明「无 ontology 优于 ontology-in-context」。

### 4.7 复杂度与成本结构（Appendix C/E, p.12；Fig. 6, 8）

- **复杂度**：按 gold query 的三元组模式数分箱，配对 F1 差（KGVoyager − GRASP，先按模型平均再跨模型平均，带 95% bootstrap CI）在 **7+ 个模式**时几乎消失（pooled F1 **58.8% vs 57.4%**，+1.4pp），**3–6 个模式**时 66.7–70.8% vs 62.9–67.4%。Fig. 6 标出每箱题数、**<10 题的箱被省略**；DBLP 的 gold query 最多 4 个模式，是四个 benchmark 里最简单的。
- **工具与成本**：每题工具调用 KGVoyager **19.2**（中位 15）vs GRASP **22.2**（中位 17），每题 SPARQL 执行 **7.5**（中位 4）vs **11.4**（中位 6）。「便宜」主要不是少调模型，而是**少调工具、少打 endpoint**；但 DBLP 的墙钟 +19.8% 说明成本结构依题面形态变。

### 4.8 失败模式（Appendix F, p.13–14；Table 6）

「complete failure」= 某 (模型, 图, 题) 在 3 次运行里 F1 全 0，共 **156 例**（4 模型 × 394 题 = 1,576 个三元组，若 gold 全有效则约 9.9%；**有效 gold 的分母未报告**，9.9% 是 `推测`）。

| 组 | n | 占比 | 典型形态 |
|---|---|---|---|
| Query generation / execution | 56 | 36% | 几乎全是**提前放弃**（Table 10：50/56 是 gave up，例「在 search 里卡了 20 步后放弃」）；另 6 例 query 写错（如用了 `rdfs:` 没声明前缀） |
| Concept resolution | 29 | 19% | 类错 11、属性错 9、实体错 9（Table 7） |
| Answer representation | 28 | 18% | 语义等价但形状不同：返回 paper ID 而非 name、yes/no 该用 ASK 却用 SELECT（Table 9） |
| Query construction | 20 | 13% | 缺约束 10（漏 COUNT(DISTINCT)）、连接路径错 10（Table 8） |
| Other | 23 | 15% | 问题本身歧义 10、top-k 平局 3、其余罕见（Table 11） |

- **真正的语义/结构错是 concept resolution + construction 共 49 例（31%）**；36% 是「跑不完/放弃」，属成本与稳定性问题，不是语义能力问题。
- **18% 的失败是评测口径造成的**（答案对但形状不同）——真实语义正确率比 F1 显示的高，也说明 F1 对「返回 ID 还是 label」这类实现选择敏感。
- 表里 19+13+18+36+15 = 101%（四舍五入）；正文写「another 31%」= 49/156 = 31.4%，与表内舍入一致。

### 4.9 补充：RDFS 假设有多普适（Appendix B, p.11–12；Fig. 5）

判定标准是图里 `rdf:type` 三元组 **≥1,000 条**：28 个 okn.us 图里 **27 个（96%）** 达标，27 个图的 typing 三元组中位数 **≈7,118,528**。唯一例外是 wikidata，但它的端点统计时**返回了错误页**，并没有真测出「它没有 rdf:type」；作者是按「Wikidata 用自己的类型体系」这一既有事实把它算作例外。1,000 条是作者选的阈值，**没有敏感性分析**：一个只用 `rdf:type` 标了 900 条的小图会被判为「不符合」。

## 5. 这些数字不能说明什么

1. **不能说明「无 ontology 优于 ontology-in-context」。** 唯一的「给 ontology」对照是 SOCKG 上的 grep 基线（§4.6），不是全 OWL 进 prompt。全文没有与 NLKGQ 比较，甚至没有引用它——两者**未头对头**。
2. **不能把 +3.7pp 当跨域效应量。** 四个 benchmark 都小（88–108 题）、三个题集由各 KG 作者提供（非社区标准 benchmark）、第四个只是 100 题抽样；域虽不同，**供给方式同源**（同一批 Proto-OKN 作者与基础设施），不能读成「4 个独立域」。单看 SOCKG 的 +2.4pp：同类格子的实验 std 能到 ±5.3（GPT-OSS/DBLP，Table 4），2.4 不能当稳。
3. **不能把「−38% 成本」当生产节省。** 成本口径未报告；且 GRASP 是在被给了 entity index 的最好情况下比的——现实里该索引只有 21.4%（Jena）/ 0%（QLever）的 endpoint 建得起来（Table 2），**样本被选择过**，真实部署差距无法从 F1 差推出。反过来，这也说明 −38% 是在对 GRASP 有利的设置下取得的。
4. **不能说明方法无关模型。** GPT-OSS 41.9% vs GPT-6 78.2%（§4.4）；失败里 36% 是提前放弃，作者称其集中在弱模型。
5. **不能说明「语义对齐解决了」。** 31% 的 complete failure 是真语义/结构错，而这只统计「3 次全 0」的题——**单次失败被定义排除**，真实失败率被低估。
6. **不能说明有时间/预算保证，也不能说明可复现。** 无 max iterations、无 token 预算；DBLP 每题 154.2s，没报 P95 或超时率；代码在匿名仓库、未 pin commit；三个 domain 题集非公开标准 benchmark。
7. **作者结论与我的推断分开。** 「exploration 工具贡献 0.7–12.5pp（含一对噪声内）」「hybrid 检索贡献 1.1–26.5pp」是作者结论且有 Table 4；「弱模型上 agentic 探索更不稳定」是作者的 context-rot 解释 + 我的推断（`推测`）；「18% 的失败只是指标问题」是作者分类 + 我的读法，未做人工复核。

## 6. 工程上怎么用

**复刻顺序（从可行性开始，不从 prompt 开始）**

1. **先量索引可行性**：在你的 endpoint 上跑「枚举类 + 每类实例数」与「枚举全部 predicate」，记录耗时/超时。**这是 adopt/no-adopt 的闸门**——Table 2 说 class index 在 4%–32% 的 endpoint 上建不起来（§4.3）。
2. **落四件套工具 + 缓存**：class search / instance lookup / property search / execute_query，加两个 exploration。class 与属性索引首次拉取后缓存到磁盘，embedding 也缓存（Table 5：向量索引在内存、embedding 存盘复用，metadata 变了才重建）。
3. **照抄检索栈参数**（Table 5, p.11）：bge-small-en-v1.5 + BM25 top-20 + dense top-10 + RRF(k=61) + bge-reranker-base top-10 + δ=0.125（至少留 3 条）。这层在消融里贡献最大，别省。
4. **自己补预算**（他们没有）：设 max iterations（均值 19.6、中位 15，可先取 30–40）、每题工具调用上限、墙钟超时；把「提前放弃」当显式失败码记录，别让它变成 0 分。
5. **按 query 复杂度分层验收**：3–6 个三元组模式上优势明显，7+ 上几乎没有（§4.7）。题以复杂 join 为主时别期待这套的增益。

**关键参数/接口**

| 项 | 默认/观测值 | 备注 |
|---|---|---|
| class index 规模 | 35–91 类、2.7–5.3 KB | 随本体规模增长，不随数据量增长 |
| 属性采样量 | Table 5 写 3000 triples；工具 spec 默认 `max_sample=5000` | **两处不一致**，实际用哪个未说明（`存疑`） |
| 每题工具调用 / SPARQL 执行 | 均值 19.2 / 7.5（中位 15 / 4） | 按这个估 token 与端点 QPS |
| 每题墙钟 | 57–154s（四 benchmark 均值 85.6s） | 不是交互式延迟 |

**何时用 / 何时别用**

- **用**：领域 KG、`rdf:type` 标注、没有可用本体或例子、能容忍每题分钟级延迟、endpoint 能跑类枚举查询。
- **别用**：Wikidata 式自有类型体系（要 adapter，作者未做）、强交互延迟预算、endpoint 会因类计数查询超时、弱模型（41.9% 那一档）、需要**保证**正确性（这套没有 soundness 保证，只有 F1）。

## 7. 质量与边界

- **证据类型**：preprint 实证（4 benchmark × 4 骨干 × 3 运行）+ 28 endpoint 可行性扫描 + 三组件消融 + 156 例失败分析 + 完整 prompt/工具 schema。
- **强项**：① 把「没有 ontology 怎么办」做成可运行系统，而不只提机制；② Table 1/2 这种「索引规模 vs endpoint 可行性」的账，同类论文基本不报，对工程决策最有用；③ 失败分析诚实——最大一类是「提前放弃」，没有藏；④ 消融带 ±std，且把「不给 domain/range 注释」写进设置。
- **主要威胁**：① 主结果只有**一个**系统基线（GRASP），没有 NLKGQ、没有微调 SOTA、没有非 agent 的 zero-shot 基线；② 每个 benchmark 只有 88–108 题，Table 3 的 +3.7 没有题目层面 CI（只有 Fig. 6 的分箱 CI）；③ 成本口径完全未报告；④ row-major F1 是转引，本文未复述定义；⑤ preprint、匿名仓库、无独立复现。
- **`quality: B` 的理由**：多 benchmark、多骨干、3 次运行、消融与失败分析都齐（有 A 的骨架），但**每 benchmark 题量小、主结果只有一个系统基线、成本口径缺失、无同行评审与独立复现**——按仓库定义属「有限评估」的强 B，不到 A。
- **引用时必须带上的限定**：4 个领域 benchmark（394 题，三个题集由 KG 作者提供）、4 个骨干、GRASP 最好情况（给了 entity index）、row-major F1、成本口径未报告、`rdf:type` 前提。

## 8. 与仓库判断的关系

**F3 的最终措辞（建议）**

> KGVoyager 不依赖预存 ontology 或 text–SPARQL 例子，只要求 SPARQL endpoint + 一个 KB 级 class index（DBLP 35 类 / 2.7 KB，SOCKG 91 类 / 5.3 KB），用 think–act–observe 循环调用 search/exploration/execution 三类通用工具在运行时发现 schema；在 4 个领域 benchmark（394 题）× 4 个骨干 × 3 次运行的**宏平均**上，F1 64.6% vs GRASP 60.9%（**+3.7 个百分点，相对 +6.1%，不是 4 倍**），成本 −38.3%、每题墙钟 −23.8%（Table 3）。增益随 query 复杂度收窄（7+ 三元组模式：58.8 vs 57.4）；GRASP 被给了 entity index 的最好情况，而该索引现实中只有 21.4%（Jena）/ 0%（QLever）的 endpoint 建得起来（Table 2）。成本口径与迭代预算未报告。
> 等级：**已核（数字，Table 1–4, p.2–8）/ 推测（跨域与外推）**。

- **必须改的一处**：`topics/03-knowledge/querying/README.md` 现有句「在 4 个 benchmark 上把 F1 提高约 4×」——原文是 "∼4 points"，即 **+3.7pp**；「4×」是把 points 读成倍数。同页「KGVoyager 的 4× 是 4 个 benchmark 上的报告值」也要一起改。
- **`execution_form` 我判 `none`。** 这篇论文里**根本没有本体出现**——没有 OWL/RDFS 本体被读入、求值、编译，也没有被注入 prompt。运行时发现的是「数据里的类名/属性名/实例」（`rdf:type` 三元组与 predicate 枚举），是**数据词表**而非本体公理；class index 是检索索引（2.7 KB 类清单），不是本体上下文。次选是 `context`（发现到的类/属性确实以工具返回形式进了 prompt），但那会把「运行时采样的数据」与「预置本体进上下文」混成一档；`label` 更不成立（它不止当标签）。若仓库将来要单列「运行时发现 schema」，这篇可作第一个样本（`已核`：按 prompt/tool spec；分档判断 `推测`）。同理**不计入 E-20 的 `engine`**：E-20 的四种 `engine` 都要求本体被求值，这里 SPARQL 执行只是**数据检索**，正确性由 row-major F1 定义。
- **`evidence_role: mechanism-only`**：它证明「无 ontology 的 endpoint 上 agentic 探索能到某个水平」，但没测本体是否被执行（没有本体变量），所以不是 `execution-test`；28 endpoint 扫描有点 `boundary-ruler` 味道，但主证据是机制。
- **与 NLKGQ：互补，不是替代，未头对头。** 两者都指向 DBLP-QuAD，但 NLKGQ 用 2.0/3.1 + **Match**（2.0 57.6%、3.1 89.9% @1,000 题），KGVoyager 用 test split 抽 **100 题** + **row-major F1**（67.5%）。**版本、样本、指标三者都不同，不能相减**。可说的是：NLKGQ 证明「有本体时把完整 OWL 放进上下文」是低成本高分的路；KGVoyager 证明「没本体时运行时探」能超过同样没本体的 GRASP。两者覆盖**本体在不在**这两个互斥前提（`推测`：都有本体时谁更好，无人测）。
- **与 GGC：假设相反，互补。** GGC 要求同一 KG 上有 119,409 条 NLQ–SPARQL 训练对来训 Gate/Corrector，把纠错压到 9.31% 样本；KGVoyager 的前提恰恰是「例子不存在」。GGC 适合「有数据、要便宜、要稳」，KGVoyager 适合「没数据、要能跑起来」。**两者都没解决对方的失败模式**：GGC 修不动逻辑组合错，KGVoyager 的 36% 失败是跑不完。
- **对 `04` B.3 的可用结论（三条 + 一条反向）**：
  1. B.3 的「先做 schema slice，不做全库检索」应改成**条件句**：有本体 → 先切 slice；无本体 → 运行时发现（KGVoyager 路线），代价是每题 57–154s 与 19 次工具调用。
  2. B.3 的验收清单「execution accuracy + 空结果率 + 纠错净收益」——KGVoyager **一个都没报**（只有 F1/成本/迭代/墙钟）。这说明该清单目前没有一篇来源能填满（`已核`：按原文表格核对）。
  3. 「瓶颈在 grounding」得到支持：10 步例子里 9 步在找 IRI/边（§3.7），失败里 19% 概念解析错 + 13% 构造错。工程量应落在**类/属性/实例的定位与验证**上，不是 prompt 措辞。
  4. 反向证据：本文「给本体」的 grep 基线反而更差（63.2 vs 71.3），说明**把本体丢给模型 ≠ 本体有用**。这与 B.3 引 SchemaForge 的「schema-aware 过滤提升 F1」不矛盾，但提醒 B.3 别把「有本体」当充分条件。
- **没有改变任何跨派 E 判断**：本篇只作 03/querying 的机制证据与 04 B.3 的条件边界，**只作边界证据**，不升 conclusions。

## 9. 还没解决 / 下一步

- **头对头**：同一 endpoint、同一题集、同一骨干，比「完整 OWL 进上下文（NLKGQ 式）」vs「运行时发现」。这是 03/querying 目前最大的空洞。NLKGQ 提出了 DBLP-QuAD 3.1（1,000 题、确定性重打分；是否公开**未核**），KGVoyager 的 100 题可直接在它上面重跑——**最省力的一步**。
- **预算-精度曲线**：固定 max iterations ∈ {10, 20, 40}，看 F1 与「提前放弃率」怎么换。他们没有预算，所以这条曲线不存在；对工程来说它比 +3.7pp 更重要。
- **class index 的失败分层**：为什么 Jena 上 32% 的 endpoint 建不起来（类计数太贵？超时？权限？）。按图规模/引擎分层重跑，才能判断「96% 可用」是否只在 QLever 上成立。
- **空结果率与执行成功率**：两个数都没报，却是 B.3 验收清单的硬项；用 156 例失败反推也不够（只覆盖 3 次全 0）。
- **跨 endpoint 一致性**：同一题在 Jena 端点与 QLever 联邦端点上答案是否一致？Table 2 显示同图两引擎成功率差异巨大，答案一致性无人测。
- **「Answer representation」18% 需人工复核**：若这 28 例多数其实答对，F1 与真实正确率的差就有 2pp 量级（`推测`），会影响与 NLKGQ 的 Match 指标对照。成本口径也需要 token 数、单价、缓存命中率与重试次数，否则 −38% 只能当相对信号。

## 10. 原文

- arXiv:2609.01780v2（2026-10-15；首次提交 2026-09-01，cs.IR）
- PDF：`src/papers/2609.01780-kgvoyager/2609.01780-kgvoyager.pdf`；正文 [paper.md](./paper.md)；参考文献 [references.md](./references.md)；附录 [appendix.md](./appendix.md)
- 代码/数据：https://anonymous.4open.science/r/nl2sparql2-C171 （匿名仓库，未 pin commit；benchmark 题–query 对随仓库提供）
