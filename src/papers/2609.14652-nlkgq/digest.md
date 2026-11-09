---
status: draft
updated: 2026-11-09
quality: B
based_on: card.md
claims: []
---

# NLKGQ：把完整 OWL ontology 放进单次上下文，零样本生成 SPARQL

> 自包含消化：不假设你读过论文或 `card.md`。讲清「controlled semantics」指什么、完整 ontology 怎么进上下文，再看 89.9% / 57.6% / 98/100 / 100% 各自的条件，最后说清它不能证明什么。页码为 PDF 页。

## 0. 三句话
1. **问什么**：LLM 做 Text-to-SPARQL 时，领域数据模型怎么传进上下文最有效——非正式描述（schema dump、散文、例子），还是带声明式语义的形式本体？
2. **怎么做**：NLKGQ 在**单次** LLM 调用里放四块：SPARQL 系统提示、**完整领域 OWL ontology（Turtle）**、简短 domain rider、用户问题；零样本生成 SPARQL，剥掉非 SPARQL 文本后执行。原生词汇不透明时，用 **wrapper ontology** 换成可读强类型词，再由**确定性 SPARQL→SPARQL rewriter** 还原。
3. **发现什么**：DBLP-QuAD 3.1（1,000 题、Qwen3.6-27B、t=0、单次调用）**Match 89.9% / Exact 81.3%**；同模型同 prompt 下 wrapper 相对 native **+15.0 Match / +25.3 Exact**。DBLP-QuAD 2.0 在确定性重算协议下 **57.6% / 20.1%**，但 2.0 与 3.1 不可直接比较；另报 SemOpenAlex **98/100**（baseline 86/100）、neuroimaging **21/21**。分数对参考结果是否冻结敏感（52.1–52.9 vs 57.6 Match）；对 endpoint、benchmark 问题措辞、system prompt 措辞**没有干净的隔离实验**。

## 1. 它解决什么问题

Text-to-SPARQL 的难点不是 SPARQL 语法——预训练模型大多会写；难点是**知道这个图里有哪些类、哪些属性、属性连接什么、值是什么类型**。没有这个 domain vocabulary，模型只能从列名、注释、示例里猜；猜错就生成「能跑但语义错」的 query。

已有路线都在用工程复杂度补这块知识：微调（把词汇写进权重）、多轮 agentic 探索（运行时试）、RAG（检索 schema/例子）。作者的主张是：**如果上下文里的词本身带声明式、机器可读的语义，模型就不需要猜**——query 生成退化成「概念转移」。这就是 controlled semantics：不是把 schema 写成散文，而是让每个 token 的 domain/range、类型、层级、注释都在本体里声明好。

论文还有第二条线：**benchmark 质量**。DBLP-QuAD 2.0 的参考 query 大量带 `LIMIT` 且无 `ORDER BY`，参考结果是任意 10 行切片；同一系统在不同运行里 Match 52.1–52.9% 波动。于是作者提出 QuAD 3.1：去掉不确定的 LIMIT、修 122 条 echo query、用 frontier model 重写问题、给 266 题加实体 URI。不理解这条线，就会把 2.0 的 57.6% 和 3.1 的 89.9% 误读成「方法涨了 32 个点」。

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **controlled semantics** | 上下文里的 schema token 带**声明的、机器可读的**含义（domain/range、类型、层级、注释、语义命名），不是靠模型从名字/数据猜。 |
| **system prompt / domain rider** | system prompt 三块：通用 SPARQL 规则 + 完整 OWL（Turtle）+ 一小段领域特定的自然语言指令（rider，只放稳定约定、不做增量概念修补）；用户问题在 user prompt。 |
| **wrapper ontology** | 为不透明原生词汇（如 `dblp:Signature` 像密码学而非署名；`publishedIn` 是 string，`publishedInStream` 是 URI）造的一套干净词表（`dblpx`、`oax`）：可读名、显式 domain/range、单命名空间；模型只看见它。 |
| **runtime rewriter** | 确定性 SPARQL→SPARQL 重写器，把 wrapper 词还原成原生词后交给 endpoint；一个 wrapper 词可展开成多个 triple。 |
| **Match / Exact** | Match：生成结果**包含**参考结果（相等或 superset）即算对；Exact：严格相等，superset 算错。 |

## 3. 它怎么做

### 3.1 单次调用的四块与执行链

```
system = [SPARQL 规则] + [完整 OWL, Turtle] + [domain rider]；user = [问题]
→ 一次 LLM 调用（t=0.0；无 few-shot/微调/entity linking）
→ 剥非 SPARQL → generated SPARQL → rewriter（仅 wrapper）→ QLever
```

- **一次调用，没有 revision loop、没有工具调用、没有执行反馈**。这与 GGC 的「生成→判→改」和 KGVoyager 的「多轮探索」是三条不同路线。
- **完整 ontology** 指整个领域本体，不是 schema slice；但论文**未报告**本体有多少 triple/token、上下文窗口多大、是否截断。
- **domain rider 只放稳定约定**；作者试过用它做增量概念修补，结论是零和（concept smearing）。wrapper 可选：native 配置直接看 DBLP 原生本体、rewriter 不启用，wrapper 配置只看干净词表、执行前还原。

### 3.2 OWL 比非正式 schema 多什么

| 类别 | 例子 | 对生成的直接作用 |
|---|---|---|
| 显式 domain/range | `dblpx:signatureAuthor` 连接 `Signature` 与 `Person` | 不用从数据推断谁连谁 |
| 类层级 | `rdfs:subClassOf` | 问「publications」时可覆盖 Article/Inproceedings/Book，不必枚举 |
| 属性类型 | `owl:ObjectProperty` vs `owl:DatatypeProperty` | 决定 URI join 还是 literal filter |
| 人类可读注释 | `rdfs:label` / `rdfs:comment` | 把自然语言含义贴在形式词上 |
| 语义命名 | `hasAuthor`、`publishedInStream`、`yearOfPublication` | 名字本身编码方向与关系；`auth_id`/`pub_yr` 做不到 |

作者的解释是：自然语言 token 语义「宽」，会激活大片关联、全局移动生成概率；形式 token 语义「窄」，只参与特定模式。**这是作者的解释，不是本文测量的机制**（`推测`）。本文也没有逐类消融这五类——wrapper 是一次性把五类都换掉。

### 3.3 wrapper + rewriter：一个具体例子（p.3）

问题（QuAD 3.1）："What are the author signatures for publications in venue `<.../conf/pods>` from 2024? Return signature URI and publication URI, sorted by publication."

模型只看见 `dblpx` 词表，生成后由 rewriter 还原：

```sparql
# 前（dblpx）
SELECT DISTINCT ?signature ?pub WHERE { ?pub a dblpx:Publication ;
  dblpx:venue <.../conf/pods> ; dblpx:year "2024"^^xsd:gYear ; dblpx:hasSignature ?signature . }
# 后（native，rewriter 输出）
SELECT DISTINCT ?signature ?pub WHERE { ?pub a dblp:Publication ;
  dblp:publishedInStream <.../conf/pods> ; dblp:yearOfPublication "2024"^^xsd:gYear ; dblp:hasSignature ?signature . }
```

模型**从未见过** `publishedInStream` / `yearOfPublication`；它在一个每个词都为语义精度挑选过的词表里工作，映射回 endpoint 是机械的。`dblpx` 还覆盖 DBLP+OpenCitations 联邦：一个 wrapper 词表同时管两个源的实体与引用。

### 3.4 数据、模型与评测协议

- **DBLP-QuAD 2.0**：5,000 对，1,000 题测试；DBLP 学术书目域（+ OpenCitations 引用数据）；从真实 SPARQL 查询日志派生。查询集特征：998/1,000 带 `LIMIT`（992 条 `LIMIT 10`）、723 条无 `ORDER BY`、122 条 `VALUES` echo、211 条依赖 OpenCitations、28 条 federated `SERVICE`。
- **DBLP-QuAD 3.1**：同样 1,000 题，但去掉 954 条不确定 LIMIT（699 条无 ORDER BY + 255 条排序键并列）、给 305 条加 year/venue/affiliation 约束、保留 44 条确定性 top-k、替换 122 条 echo、逐题修 query、用 Claude 重写问题并给 266 题加 bracketed URI。**2.0 与 3.1 不可直接比较。**
- **SemOpenAlex**：100 题测试集（Bartels et al. 2025），与已发表 baseline 同一测试集。**Neuroimaging**：21 个 competency questions，前作 purpose-built ontology；本文用 Qwen3.6-27B 复跑/继承。
- **模型/协议**：主 Qwen3.6-27B；10 模型扫描见 §4.3；本地 AMD APU，开源权重；未测 proprietary。单次调用、t=0.0、无微调、无 few-shot、无 entity linking；QLever；固定 snapshot（QLever 是 SPARQL 引擎）；失败 case 记 0；重复跑在确定性配置上差 ≤0.1 点（2.0 重算参考除外）。
- **指标**（Table 1, p.5）：Match（二元，containment）、Exact（二元，严格相等）、QuAD F1（graded，cell 摊平）、SPINACH F1（graded，行对齐）。主报 Match；Exact 是更严格的数。

## 4. 结果：数字与条件

### 4.1 主 progression（Table 2, p.6；Qwen3.6-27B，procedural prompt，t=0.0，1,000 题，%）

| QuAD | Ontology | Match | Exact | QuAD F1 | SPINACH F1 |
|---|---|---|---|---|---|
| 2.0 | native | 43.0 | 10.7 | 23.2 | 23.0 |
| 2.0 | wrapper | 52.9 | 11.3 | 17.6 | 17.5 |
| 2.1 | wrapper | 57.6 | 20.1 | 16.7 | 17.3 |
| 3.1 | native | 74.9 | 56.0 | 63.8 | 62.3 |
| 3.1 | **wrapper** | **89.9** | **81.3** | **80.7** | **79.0** |

- **89.9 是 3.1 + wrapper + Qwen3.6-27B + 单次零样本**；**2.0 的 57.6 是 2.1 测量协议 + wrapper**（参考结果冻结一次），摘要写成「DBLP-QuAD 2.0 57.6%」时没提 wrapper/协议，引用要补。
- **2.0 native 43.0 → 3.1 native 74.9**：+31.9 Match 来自 benchmark 修复，不是模型或本体改进；**3.1 native 74.9 → wrapper 89.9**：+15.0 Match / +25.3 Exact 来自 wrapper（同模型、同 prompt、同数据），Exact 涨得更多，说明不是 Match 的 superset 容忍在起作用。
- **2.0 上 wrapper 只 +9.9 Match / +0.6 Exact，且 F1 下降**（QuAD F1 23.2→17.6，SPINACH 23.0→17.5）：参考是任意 10 行切片，wrapper 返回更完整的结果反而被 F1 罚。这是「F1 在 2.0 上测的是参考，不是系统」的直接证据（作者结论）。

### 4.2 跨域（Table 3, p.6；Qwen3.6-27B，t=0.0）

| 域 | 题数 | Match % | Exact % | SPINACH F1 | Baseline |
|---|---|---|---|---|---|
| DBLP（QuAD 3.1，dblpx） | 1,000 | 89.9 | 81.3 | 79.0 | 51.0 F1（GRASP，50 题原版 DBLP-QuAD，GPT-4.1，多轮） |
| SemOpenAlex（oax） | 100 | 98.0 | 98.0 | — | 86/100（Bartels et al.，123B，few-shot + entity mappings） |
| Neuroimaging（purpose-built） | 21 | 100.0 | 100.0 | — | — |

- **SemOpenAlex 98/100 vs 86/100 不是受控比较**：baseline 是 123B + few-shot + entity mappings，本文是 27B + 零样本；只共享测试集。100 题里 2 题作者判为 ambiguous（UNION vs co-authorship），2 个 miss 都来自这种歧义。**Neuroimaging 21/21** 是前作 purpose-built ontology 的结果，题量 21，不是独立公共 benchmark。
- **GRASP 的 51.0 是在原版 DBLP-QuAD 的 50 题上**，不是 3.1 的 1,000 题；作者自己写明「not a same-benchmark ranking」，并预期 GRASP 在 3.1 上也会更高。这个比较只能说明「去掉 2.0 的混淆后，query 生成能到 79 F1」，不能说明 NLKGQ 比 GRASP 强 28 点。

### 4.3 模型扫描（Table 4, p.6；QuAD 3.1 + wrapper，t=0.0，procedural prompt，1,000 题，%）

| 模型 | 类型 | Match | Exact | F1Q | F1S | Fail |
|---|---|---|---|---|---|---|
| Gemma-4-31B | dense | 90.3 | 75.1 | 79.4 | 76.9 | 3.5 |
| Qwen3.6-27B-FP8 | dense/q | 90.0 | 81.4 | 81.3 | 79.4 | 2.5 |
| Qwen3.6-27B | dense | 89.9 | 81.4 | 80.8 | 79.1 | 3.4 |
| Qwen3-Coder-30B | MoE/code | 81.1 | 62.3 | 69.6 | 67.9 | 4.0 |
| Mistral-Small-24B | dense | 80.6 | 65.2 | 68.0 | 64.3 | 4.7 |
| Llama3.3-70B | dense | 74.3 | 59.4 | 63.6 | 61.7 | 5.0 |
| Qwen3-8B | dense | 66.2 | 50.6 | 53.5 | 51.3 | 13.2 |
| Qwen3.6-35B-FP8 | MoE/q | 64.9 | 52.6 | 55.1 | 52.7 | 25.3 |
| Qwen3.6-35B* | MoE | 50.4 | 40.3 | 42.4 | 40.3 | 41.5 |
| Qwen3-14B* | dense | 24.8 | 19.1 | 19.3 | 18.4 | 68.6 |

\* partial：Qwen3-14B 实际跑 593/1,000，Qwen3.6-35B 730/1,000；百分比按实际跑完题数计。Fail 是「无 query 或执行错」的比例；常见失败是 query 超时。

- 顶部两个不同家族、同尺寸的 dense 模型都到 ~90 Match（Gemma 90.3、Qwen 90.0/89.9），但 **Gemma 的 Exact 只有 75.1，Qwen 是 81.4**：Gemma 更多给出「包含参考但多行」的结果。**Match 收敛不等于 Exact 收敛。** 模型间差异仍然很大（24.8–90.3 Match）；「ontology 比模型家族更重要」是作者从顶部收敛做的解释，**不是 factorial 实验**（`推测`）。
- 规模有效：Qwen3-8B 50.6 Exact → Qwen3.6-27B 81.4 Exact（+30.8，3.4× 参数）；跨家族 8B→70B 只 +8.8 Exact。FP8 与全精度基本持平（27B-FP8 90.0/81.4 vs 27B 89.9/81.4，差 0.1）。通用 MoE 失败率高（35B 25.3%、35B* 41.5%），但 code-specialized MoE（Qwen3-Coder-30B）只有 4.0% 失败——作者说稀疏激活本身不解释失败，代码训练可能补偿；这是相关性，不是因果（`推测`）。

### 4.4 错误分析（progression run，899 Match → 101 个非 Match；p.6–7）

- **citation 24**：参考返回 OMID（OpenCitations Meta Identifier）侧实体，wrapper 把 citation endpoint 解析成 DBLP URI；OMID→DBLP 映射只覆盖 71%。
- **federated 22 + aggregation 23 + introspection 3 + 异质 29**：22 条 `SERVICE` 调 DBpedia/Wikidata/FactGrid，dblpx 不覆盖（另 6 条只用 FOAF 等常见词表，能 match）；23 条聚合（结构 18 + 执行失败/超时 5）；3 条「有哪些类」；29 条 venue info dump、type/label listing 等。101 条里 30 条是「无 query 或执行错」：10 federated、11 异质、5 aggregation、3 citation、1 introspection。

作者结论：**主要失败模式是 data coverage 和 federation scope，不是 vocabulary confusion**。这是对「词汇是瓶颈」的重要限定：wrapper 解决命名/类型后，剩下的错更多是数据覆盖与联邦边界。

### 4.5 敏感性：到底对什么敏感、差多少

| 变量 | 论文报了什么 | 差多少 | 不能说明什么 |
|---|---|---|---|
| **参考结果是否冻结**（同一 snapshot） | 2.0 wrapper 重算参考：52.1–52.9 Match（五次）；冻结参考：57.6 | **+4.7–5.5 Match；Exact 11.3→20.1（+8.8）** | 不是「不同 graph snapshot」的差；snapshot 始终是同一个 |
| **graph snapshot** | 所有 DBLP 结果跑在单一固定 snapshot（DBLP 2025-07-02 + OpenCitations DBLP 子集） | **未报告**跨 snapshot 对照 | 不能从本文推出换 snapshot 会差多少 |
| **endpoint** | QLever；28 条 federated `SERVICE` 依赖第三方 endpoint；22/101 错来自未覆盖的 federation | **未报告**同一 query 跨 endpoint 的 A/B；22 条是定性归因 | 不能把 22 条当 endpoint 效应的估计 |
| **benchmark 问题措辞** | 2.0 用 LLaMA-3.1-8B 生成问题；3.1 用 Claude 重写，547 题补列/排序/范围，266 题加 URI | 与参考修复混在一起：2.0→3.1 native 是 43.0→74.9（+31.9 Match），**未单独消融** | 不能把 +31.9 全算成「问题措辞」；也不是 system prompt |
| **system prompt 措辞** | 前作：三版 system prompt 在词汇正确后打平；本文：任何 token 改动会移动许多未目标 query（concept smearing），rider 增量修补零和 | **未报告**本文的 numeric delta | 不能把摘要里的「wording of machine-generated questions」读成 system prompt 措辞 |
| **wrapper vs native** | 3.1：74.9→89.9 Match、56.0→81.3 Exact；2.0：43.0→52.9 Match、10.7→11.3 Exact，F1 下降 | **+15.0/+25.3（3.1）；+9.9/+0.6（2.0）** | 不是「OWL vs 散文/schema dump/examples」的对照；两边都是 OWL |

**这是 F2 措辞的关键**：摘要的「scores depend on the graph snapshot, the endpoint used, and the wording of its machine-generated questions」把三件事混在一句里；本文真正有数字的是「参考结果冻结 vs 重算」，其余两项是定性/未隔离。

### 4.6 前作数字（本文引用，不是本文重跑）

这些数字来自 Fitch & Kurtz 2026（arXiv:2607.18029，本仓库未入档），本文用它们做动机，不是本文实验：Neuroimaging purpose-built ontology 上 SPARQL 100%（21 competency questions）vs 同一 ontology 自动生成 SQL 的 43%，把 ontology 注释带进 SQL 列注释后 57%；去掉 `rdfs:comment` 使 SPARQL 100%→81%，把 ontology 缩减成 bare graph structure 使 100%→5%；三版 system prompt 在词汇正确后打平；35B MoE 峰值 57%，dense 27B 100%。**这些是「controlled semantics 比 informal 好」的主要经验依据，但它们是前作、单域、21 题；本文没有重复这些消融。**

## 5. 这些数字不能说明什么

1. **不是「OWL 一定赢 schema dump / 散文 / few-shot」的对照实验。** 本文的 wrapper vs native 两边都是 OWL；wrapper 换掉的是命名、注释、namespace、domain/range 完整性，不是「形式 vs 非形式」。要支持「controlled semantics 优于散文/例子」，主要靠前作的注释/裸结构消融和跨论文比较，不是本文的单因子实验（`已核` 实验设计；`推测` 一般结论）。
2. **不是「完整 ontology 总能塞进上下文」。** 论文没报本体 triple/token 数、上下文窗口大小、截断率；作者自己把「词汇超出上下文需要选择/缩减」列为未解决。DBLP 能塞下，不代表 Wikidata/企业本体能塞下。
3. **不是「2.0→3.1 是方法增益」。** 3.1 同时改了参考确定性、query、问题、实体 URI；57.6 与 89.9 之间隔着 benchmark 修复，不是同一把尺子。
4. **Match 不是业务正确率。** Match 允许 superset；Exact 81.3 才是严格数。两者都不是人工评审，也没有下游任务。
5. **不是跨 endpoint / 跨模型结论。** 单 QLever、单固定 snapshot；28 条 federated 只是定性依赖；wrapper-vs-native 消融只跑 Qwen3.6-27B；10 模型扫描只覆盖 wrapper 配置；没有 proprietary 模型；没有 8B native / 70B wrapper 的 factorial。
6. **不是「ontology 比 scale 重要」的因果排序。** 作者给的是「formal concept transfer > architecture > scale > prompt」的解释；实际数据里模型间 Match 24.8–90.3，scale 从 8B→27B 有 +30.8 Exact，说明 scale 仍然很大。这个 hierarchy 是 `推测`，不是测出来的排序。
7. **不是「词汇是唯一瓶颈」。** 101 个非 Match 里 46 个是 citation/federation 覆盖，23 个是 aggregation，29 个异质；作者自己说主因是 data coverage / federation scope。wrapper 修不了数据覆盖。
8. **不是独立复现。** 单作者 preprint；QuAD 3.1 的修复者与所评系统同一作者；修复没有第三方审计；3.1 论文发表时「将发布」，未给代码链接。作者提供的检查是逐题日志与修复前 margin（2.0 上 +9.9 Match）。
9. **不是成本或部署结论。** 没有 token 数、上下文长度、延迟、吞吐、GPU 小时；「单次调用」是调用次数，不是成本。也没有生产流量、人工评审、失败回滚；不要写「部署有效」。
10. **不是 entity resolution 结论。** 3.1 的 266 题带 bracketed URI；未加括号的实体提及仍未解。系统在「实体已给定」的条件下评测 query 构造，不是端到端 KGQA。

## 6. 工程上怎么用

**复刻顺序（先别改模型）**

1. **先量本体预算**：把目标域的 OWL 导成 Turtle，数 triple 与 token；确认在目标模型上下文里放得下，并留出问题/输出预算。论文没给这个数，必须自己量。
2. **先做 native vs wrapper 的小对照**：抽 50–100 题，同一模型、同一 prompt、t=0，只换词表；同时报 Match 与 Exact。若 Exact 不动、只有 Match 动，先查是不是 superset/参考切片问题。
3. **wrapper 只包「模型必须知道」的词**：类、属性、domain/range、枚举；不要把整个数据实例塞进去。一个 wrapper 词可以展开成多个 triple，rewriter 要可测试。
4. **rider 只放稳定约定**：输出格式、排序、单位、必须用的前缀。不要用 rider 做逐 case 修补——作者的实验显示零和。
5. **评测协议先冻结**：参考结果算一次、存下来；报告 Match 与 Exact；失败 case 记 0；记录模型、t、prompt 版本、snapshot、endpoint；执行前剥掉 code fence/reasoning/解释。

- **调用/温度 + ontology/rider**：1 次/题，t=0.0；近确定性，重复跑差 ≤0.1 点。完整领域本体 Turtle（大小未报告；超出上下文需选择/缩减，未解决）；rider 短、稳定，增量修补零和。
- **wrapper/rewriter**：dblpx/oax，手工；确定性 SPARQL→SPARQL；一个 wrapper 词可展开多 triple，要单测。
- **执行/指标**：QLever，单 snapshot；Match + Exact + 两个 F1；federated `SERVICE` 是覆盖缺口，Match 允许 superset。

**何时用 / 何时别用**：用——schema 相对稳定、本体能塞进上下文、原生词不透明（需要 wrapper）、没有训练数据/不想微调、要单次低交互、能接受结果集匹配口径。别用——本体大到放不下；需要 entity resolution（未加括号的实体）；大量 federation 到未覆盖的 endpoint；聚合/introspection 为主；需要 soundness 保证；需要成本/延迟硬指标（本文没报）。

## 7. 质量与边界

- **证据类型/强项**：单作者 preprint；主 benchmark（DBLP-QuAD 2.0/3.1，1,000 题）+ 两个小集（100、21）；wrapper 消融单模型；10 模型扫描；无独立复现。机制写得清楚（四块 prompt、wrapper、rewriter、worked example）；benchmark 审计具体（998 LIMIT、122 echo、211 citation、71% 覆盖）并给出确定性协议；作者把单模型消融、上下文溢出、Match superset、同作者修 benchmark、手工 wrapper、entity resolution 不在范围都写进了 Limitations。
- **主要威胁**：① 单作者 + preprint + benchmark 修复者与系统作者同一人，存在利益冲突；② 核心因果 claim（ontology 表示 > 模型/prompt）只有单模型 wrapper 消融，10 模型扫描不覆盖 native；③ 没有同内容的散文/schema dump/few-shot 对照；④ 本体大小/上下文预算未报告；⑤ 2.0 与 3.1 的对比容易被误读；⑥ 无 CI、无独立复现、无成本数据。
- **`quality: B` 的理由**：有单 benchmark 主结果 + wrapper 消融 + 多模型扫描 + 跨域小集，属于「单基准/单域为主、评估有限」；不到 A（没有多基准独立复现、没有真实部署、核心消融单模型），也不是 C（有量化、有对照、有错误分析）。
- **引用时必须带上的限定**：DBLP-QuAD 3.1、1,000 题、Qwen3.6-27B、单次调用、t=0、无微调/few-shot/entity linking、dblpx wrapper、固定 QLever snapshot、Match 允许 superset；2.0 的 57.6 是 2.1 协议 + wrapper；SemOpenAlex 98/100 是 100 题、baseline 非受控；neuroimaging 21 题是前作 purpose-built。

## 8. 与仓库判断的关系

### 8.1 对 `03/querying` F2 的最终措辞

主题页草案需要改三点：① 主结果不是 2.0，而是 3.1 的 89.9/81.3；2.0 的 57.6 是 2.1 协议 + wrapper；② 「prompt wording」在摘要里指 **benchmark 的机器生成问题**，不是 system prompt；③ 要写清 2.0 与 3.1 不可直接比较，以及 wrapper 在 2.0 上 F1 反而下降。

**建议 F2（短版，可直接进主题页）**：

> NLKGQ 把**完整领域 OWL ontology（Turtle）+ SPARQL 系统提示 + 简短 domain rider + 用户问题**放进**单次** LLM 调用，零样本生成 SPARQL；原生词汇不透明时用 **wrapper ontology** 换成可读强类型词，再由**确定性 rewriter** 还原。DBLP-QuAD 3.1（1,000 题、Qwen3.6-27B、t=0、无微调/few-shot/entity linking、固定 QLever snapshot）**Match 89.9% / Exact 81.3%**；同模型同 prompt 下 wrapper 相对 native **+15.0 Match / +25.3 Exact**。DBLP-QuAD 2.0 在确定性重算协议下 **57.6% / 20.1%**，但 2.0 与 3.1 不可直接比较（3.1 修了 954 条 LIMIT、122 条 echo、重写问题并给 266 题加 URI）；2.0 上 wrapper 只 +9.9 Match / +0.6 Exact，F1 反而下降。分数对**参考结果是否冻结**敏感（52.1–52.9 vs 57.6 Match）；对 endpoint、benchmark 问题措辞、system prompt 措辞**没有干净的隔离实验**。`已核`（单系统/单 benchmark 主结果与 wrapper 对照）/ `推测`（跨域、跨 endpoint、本体超出上下文）。

**等级**：`已核`（数字与实验设定，一手正文）/ `推测`（跨域、跨 endpoint、上下文溢出、把「controlled semantics」推广到所有 schema）。不要写「部署有效」，也不要写「ontology 一定优于 schema dump」——本文没有这个对照。

### 8.2 与 GGC 的关系

- **GGC**：生成后**选择性纠错**——Generator 出 query，Gate 判是否要改，Corrector 只改高风险；监督训练、单 KG（MCQA/iMKG）、答案集匹配口径；`execution_form: none`（本体不进 prompt，关系名进权重）。**NLKGQ**：生成前**供概念**——完整 OWL 进上下文，零样本单次；`execution_form: context`；wrapper 处理不透明词。
- 两者不是同一阶段的替代品：GGC 假设你已有能生成 query 的模型，补的是「错了怎么改」；NLKGQ 假设你还没有领域词汇，补的是「怎么让模型第一次就写对」。可以串：先用 NLKGQ 的 ontology/wrapper 做生成，再用 GGC 式的 gate 做后验纠错；**这个组合没人测**（`推测`）。
- 数字不可比：GGC 的 98.33% 是 MCQA 31,570 题的 query-level accuracy（答案集匹配）；NLKGQ 的 89.9% 是 QuAD 3.1 1,000 题的 Match（containment）。不同 benchmark、不同指标、不同模型。

### 8.3 与 KGVoyager 的关系

- **KGVoyager**（同批来源，本目录未读原文）：agentic navigation、ontology-free，多轮 think-act-observe，靠 endpoint + lightweight class index 探索；不预存 ontology/examples。**NLKGQ**：单次、ontology-in-context、零样本；不探索。这是第三条线：**ontology-in-context**。三条线（selective correction / agentic navigation / ontology-in-context）**没有同 benchmark、同模型、同预算的头对头**；「谁是默认路线」未测。
- KGVoyager 的报告值（本仓库 `03/querying` 草案记为 4 个 benchmark、约 4× F1，本目录未核原文）不能与 NLKGQ 的 89.9 相减或相比；两者指标、数据、调用预算都不同（`推测`：若按 token/调用次数归一，排序可能变；未测）。

### 8.4 对 04 B.3 / B.4 的可用结论

**B.3 Text2SPARQL**：B.3 现在写「先做 schema slice，不做全库检索」。NLKGQ 是**边界反例**：DBLP 上完整 ontology 进上下文可行，且比 native 不透明词表好；但 NLKGQ **没测本体大小/溢出**，不能反过来说「全量总是可行」。B.3 应改成「先量本体 token 预算；能放下且词表可读时，全量 ontology 是已测选项；放不下再 slice」。B.3 的「选择性纠错」是 GGC 的后验路线，NLKGQ 提供**生成前**路线（ontology/wrapper），两条可并列；验收应同时报 **Match 与 Exact** 并冻结参考结果。

**B.4 语义层 / OBDA**：NLKGQ 的 wrapper + rewriter 是**确定性的概念词表→原生 schema 映射**，与 semantic layer/OBDA 同源（作者自己引 OBDA 谱系），但**不是 OBDA**：没有 virtual KG、没有推理/entailment、没有权限、没有治理；只服务 query 生成。所以 B.4 的「OBDA ≠ NL→query」仍然成立；它能支持「干净概念词表 + 确定性映射」这个模式，以及「语义层不是更懂业务的 prompt」——wrapper 是代码/映射，不是散文。不要写成「语义层已能替代 OBDA」或「ontology 进 prompt 就等于执行本体」。

### 8.5 与 E-20 / execution_form

- `execution_form: context`：本体以 Turtle 文本进 system prompt，**没有被求值、没有 entailment、没有约束校验**；SPARQL 在数据上执行，不是在 ontology 上推理。所以它**不应计入 E-20 的 `engine`**，也不支撑「本体被执行」的效应量。它是 E-20 的边界样本：**「本体在上下文里」≠「本体被执行」**；只证明「context 能提升 query 生成」，不证明「context 能替代 engine」。
- 与 `03/projection` 的关系：NLKGQ 也是「把本体投影进上下文」，但投影的是**形式 Turtle**，不是散文；它可以作为 projection 的对照样本（形式投影 vs 文本投影），但本文没有做这个对照（`推测`）。

## 9. 还没解决 / 下一步
- **本体大小 + 同内容表示**：多少 triple/token 开始掉点？固定模型按 25/50/75/100% 截断，报 Match/Exact；同一本体分别以 Turtle、散文、schema dump、few-shot 例子给出，同模型同 prompt 对照。本文没有这个 arm。
- **wrapper 消融跨模型**：8B/27B/70B 各跑 native vs wrapper，看 +25.3 Exact 是否随规模变。现在只有 27B 一个点。
- **跨 endpoint A/B**：同一 snapshot 在 QLever/Virtuoso/Blazegraph 上跑同一批 query，量 endpoint 差异；现在只有 QLever。
- **prompt 措辞的隔离消融**：固定 ontology，只改 system prompt 的三版/五版，报每版 Match/Exact；现在只有前作「三版持平」的定性说法。
- **entity resolution**：266 题 bracketed URI 是「给定实体」；未 bracketed 的实体提及怎么解？这是端到端 KGQA 的门。
- **aggregation / introspection / 成本**：18+5+3 个失败说明这些 query 形态还没解；另需 token、延迟、吞吐、GPU 小时（「单次调用」不等于便宜）。
- **独立复现 + 三路线头对头**：修 QuAD 3.1 的修复清单、逐题日志、release 是否公开；同一 benchmark/模型预算比较 NLKGQ（ontology-in-context）、GGC（selective correction）、KGVoyager（agentic navigation）。

## 10. 原文

- arXiv:2609.14652v1（2026-09-13，cs.DB）；PDF：`src/papers/2609.14652-nlkgq/2609.14652-nlkgq.pdf`；正文 [paper.md](./paper.md)；参考文献 [references.md](./references.md)；附录 [appendix.md](./appendix.md)（本文无附录）
- 代码/数据：论文未给代码链接；QuAD 3.1 称将发布（GitHub），发表时未见
