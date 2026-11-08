---
status: draft
updated: 2026-11-08
quality: A
based_on: card.md
claims: [E-02]
---

# What Does an Ontology Catch?：本体当 checker，自己也会错

> 这篇消化不假设你读过论文。先讲清「用本体检查 agent 的 SPARQL 答案」是什么，再看三种本体来源的漏检/误报、空结果基线、工程上怎么选。

## 0. 三句话

1. **它问什么**：LLM agent 在知识图谱上写 SPARQL 答题；用图的本体做 checker，能不能可靠地抓错？curated / LLM 生成 / 数据派生三种来源，哪种更值得？
2. **它怎么做**：在 5 个知识图、7 个模型上，比较三种本体来源 × 三种用法（prompt 上下文 / checker / 两者）；用「真实答案 + 人工故障」分别量 catch 与 false alarm。
3. **它发现什么**：curated 本体抓得多、但误报也多；真实答案上它的 precision 只比随机高 1.6 点。数据派生本体 precision 更高（72.3%）但只抓到 8.2% 的真错；**空结果重试**是很强的基线（人工故障 catch 79.2%、FA 0%）。没有单一向优的来源。

## 1. 它解决什么问题

### 1.1 背景

知识图谱（KG）用 SPARQL 查询。LLM agent 把自然语言问题翻成 SPARQL，执行，返回答案。一个查询可以**语法有效、执行无错、却答错**：选错类、关系方向反了、把「相关」当「同一」、漏掉约束。

一种常见做法：用图的**本体（ontology）**做 checker——本体规定类、属性、domain/range、disjointness；如果查询违反这些约束，就 flag，让 agent 修。

问题：**checker 自己也会错**。它可能：
- **漏检**：错误答案通过了检查；
- **误报**：正确答案被 flag，agent 被逼着去「修」一个本来正确的答案；
- 误报的破坏力被低估：它会产生新的、更隐蔽的错误。

### 1.2 论文的立场

不要假设「正式 schema = 可靠 judge」。要把 checker 本身当研究对象：它到底抓到了什么、误报了什么、代价是什么。

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **知识图谱（KG）** | 实体 + 关系的图；本文用 UniProt、Rhea、企业图、私有图等。 |
| **本体（ontology）** | 图的 schema：类、属性、domain/range、disjointness 等。 |
| **checker** | 从本体编译出来的检查器；对查询/答案给 pass / flag / unknown。 |
| **curated** | 图作者发布、按原样使用的本体。 |
| **data-derived** | 从数据总结出来的 schema：类、属性、常见模式；没有 disjointness。 |
| **LLM-generated** | 让 LLM 从数据 summary + 实例样本写出本体。 |
| **catch** | 错误答案被 flag 的比例。 |
| **false alarm（FA）** | 正确答案被 flag 的比例。 |
| **precision** | flag 里有多少是真的错；catch 高但 FA 高，precision 就低。 |
| **empty-result retry** | 查询返回空就重试；不需要本体，是很强的基线。 |
| **UniProt** | 本文唯一 confirmatory 的图（约 4×10⁸ triples）。 |

## 3. 它怎么做

### 3.1 数据与模型

- **5 个图**：
  - UniProt：4.0×10⁸ triples，confirmatory；curated 声明 domain/range/disjointness。
  - Rhea：5.5×10⁶ triples，exploratory；只有类层级。
  - Rhea-masked：把类/属性/实例标识符替换成不透明 id，防记忆泄漏。
  - Corporate：2.7×10⁴ triples。
  - Private：约 10⁹ triples；只报率。
- **7 个模型**：Claude Sonnet 5.5、Haiku 5.5；Qwen3.8-27B、Qwen3-Coder-30B-A3B、GLM-5.3-Flash、Gemma-4-31B、DeepSeek-V4-Flash。
- **规模**：210 个 UniProt 测试题 × 3 attempts × 7 模型 = 4,410 条真实答案；其中 3,383 可检查。人工故障：9,753 个改变答案的 fault + 3,630 个正确 control。

### 3.2 三种本体来源

| 来源 | 怎么来 | 关键差异 |
|---|---|---|
| curated | 图作者发布，按原样用 | 可能有 domain/range/disjointness；也可能缺声明、与数据矛盾 |
| data-derived | 从数据总结：类实例数、属性 subject/object 类；模式≥5 次才允许 | 无 disjointness；不会 flag 数据中出现≥5 次的模式 |
| LLM-generated | Claude Opus 5.5 从同一 summary + instance sample 写 | 可能加 disjointness；不同 draw 差异大；masked 变体防记忆 |

### 3.3 三种用法

- **as context**：把本体渲染进 prompt，让 agent 自己参考。
- **as check**：编译成 checker，对查询/答案做结构检查。
- **both**：两者都用。

### 3.4 判定回路

`Question → LLM agent → SPARQL → KG → answers → check → pass/flag → answer kept`。

- flag 触发**一次重试**；消息是 specific（指出失败约束/查询片段）或 generic（"Please re-check"）。
- 每个 verdict 对正确答案打分：**caught**（错误被 flag）、**missed**（错误通过）、**false alarm**（正确被 flag）、**correct pass**（正确通过）。
- 重试后：**fixed**（错→对）、**corrupted**（对→错）。

### 3.5 检查类型

- **Query checks**：解析 SPARQL，推断每个变量的类型；检查 term 是否存在、class membership、domain/range、disjointness、datatype range。
- **Binding checks**：对结果绑定重新求值；检查类/属性/数据类型。
- **data-derived 额外 pattern checks**：属性与数据从未共现的类、没有类支持≥5 次的 join。
- 不支持的 fragment（UNION、subquery）返回 **unknown**，不是 pass/flag。

### 3.6 空结果基线

查询返回空就重试；不需要本体。它在人工故障上 catch **79.2%**、FA **0%**；在真实答案上 catch 2.5%、FA 0.1%。

**ontology check 只有超过这个基线才有价值**；否则只是多一次重试。

## 4. 结果：数字与条件

### 4.1 真实答案（UniProt，4,410 条，3,383 可检查）

| 来源 | catch | false alarm | precision |
|---|---|---|---|
| curated | **18.9%** | **16.8%** | **57.1%** |
| data-derived | **8.2%** | **3.5%** | **72.3%** |
| LLM-generated（masked，三个） | 5.0% | 1.8% | 93.7% |
| 空结果重试 | 2.5% | 0.1% | 100% |

- curated precision 相对随机 flag 只高 **+1.6 点**（CI −2.3~+6.3）；LLM judge 比随机高 +15.8。
- 确认性比较（C2）：curated − data-derived：FA **+8.6**（6.0,11.2），type-swap catch **−22.3**（−23.5,−21.0）。
- C3：curated − masked LLM：FA **+15.7**（13.7,17.9）。

> 出处：Table 2, p.7；Table 3, p.7；§5.3。

### 4.2 人工故障

| 来源 | catch（all） | catch（rows returned） | FA |
|---|---|---|---|
| curated | 60.1% | 54.3% | 16.8% |
| data-derived | 75.6% | 62.1% | 3.5% |
| 空结果重试 | 79.2% | 0.0% | 0% |

**空结果基线在人工故障上已经很强**：很多故障会让查询返回空；ontology check 的增量价值主要在「查询仍有结果」的错误。

> 出处：Table 2, p.7；§5.4。

### 4.3 组合与反馈

- 组合 curated + data-derived：catch 19.5%、FA 17.8%；比 curated 单用只多 0.6 点 catch，却多 1.0 点 FA；C4 无净收益。
- specific feedback：修复 28.3% 的 flagged wrong，但 corrupt 1.0% 的 flagged correct；generic 是 20.2% / 0.2%。C5 无显著差异。

> 出处：§5.5；Table 4（组合/反馈）。

### 4.4 成本

- curated check：每答案 65,976 tokens / 46.0 s（median）。
- data-derived：28,076 tokens / 17 s。
- 生成一个 data-derived ontology：<$1。

> 出处：Table 8, p.10；§5.7。

## 5. 这些数字不能说明什么

1. **不是「本体无用」。** 它说明「把本体当 checker」在真实答案上 precision 只略高于随机；特定错误类型（type swap）curated 仍然有用。
2. **不是「data-derived 更好」。** data-derived 的 precision 高，但 catch 只有 8.2%；它抓不到语义错误（类型都对、问错问题）。
3. **不是「空结果重试就够了」。** 它在真实答案上只抓 2.5%；对「查询仍有结果」的错误，ontology check 才有增量。
4. **UniProt 是唯一 confirmatory。** 其他图 exploratory；private 只报率。
5. **人工故障可能不代表真实错误。** 真实 agent 错误稀疏且分布不均。
6. **知道正确答案。** 真实部署没有这个条件；precision/recall 无法直接算。
7. **curated setup 成本未测。** data-derived <$1 是生成成本，不是维护成本。

## 6. 工程上怎么用

### 6.1 复刻顺序

1. **先建空结果重试基线。** 不加本体，先看执行结果本身能暴露多少错。
2. **做 data-derived summary 审计 curated 本体。** 缺声明、矛盾 axiom 是最便宜的 false alarm 来源。
3. **按错误类型选 checker。** 类型/声明/模式错 → data-derived / declaration check；语义错 → 本体检查抓不到，换 LLM judge 或人工。
4. **同时报 catch 与 FA。** 只看 accuracy 会把「多抓错、多杀对」混在一起。
5. **不要同源。** 同一个本体既做 context 又做 checker，catch 反而下降（探索性）；判定器应与被判定对象不同源。
6. **不要盲目组合。** 组合往往增加 FA 而不增加净收益。
7. **把 FA 当预算。** Google 的静态分析要求 effective FP <10%；agent 场景要自己定。
8. **specific feedback 要验证。** 它修复更多，但 corrupt 也更多；没有验证前 generic 更安全。

### 6.2 成本与使能

| 成本 | 一次性/每次 | 说明 |
|---|---|---|
| curated 本体 | 发布方一次性（未测） | 可能缺声明/与数据矛盾；维护成本高 |
| data-derived summary | 一次性，<$1 | 从数据总结类/属性/模式；可自动生成 |
| LLM-generated 本体 | 一次性，<$1/个 | 不稳定；需多个 draw + 评估 |
| check | 每次答案 | curated 66k tokens / 46 s；data 28k / 17 s |
| 重试 | 每次 flag | 由 false alarm 触发；成本随 FA 上升 |
| 人工标注 | 评估期 | 需要正确答案/抽样标注；部署时通常没有 |

**使能条件**：可执行 schema（OWL/SHACL/SPARQL）、能读数据生成 summary、有 SPARQL endpoint、能拿到正确答案或抽样标注。

### 6.3 何时用 / 何时别用

**用**：知识图谱有可执行 schema；任务主要是类型/声明/模式错误；有正确答案或能人工标注；false alarm 预算明确。

**别用**：语义错误为主；没有正确答案、无法估 precision；curated 本体与数据不一致且没人维护；查询大量使用 UNION/subquery；false alarm 会直接损害用户信任。

## 7. 质量与边界

- **证据类型**：实证·基准（UniProt confirmatory）。
- **强项**：把 checker 本身当对象；catch/FA 分开；真实答案 + 人工故障双轨；同一 compiler；成本表；代码/数据公开。
- **主要威胁**：只有 UniProt confirmatory；人工故障可能不代表真实错误；真实错误稀疏；private 图只报率；curated setup 成本未测；部分注册分析未跑。
- **`quality: A`**：预注册 + 多模型 + 多图 + 真实/人工双轨 + 成本 + 可复现；但外部效度受「知道正确答案」限制。

## 8. 与仓库判断的关系

- **E-02（已核）**：三种来源在漏检/误报上各有偏向；curated precision 仅略优于随机；curated schema 可能与自身数据矛盾；空结果重试是关键基线。
- **P3（判定是权衡）**：不存在单一向优的来源；curated 高 catch/高 FA，data-derived 低 FA/低 catch，LLM 不稳定。
- **02-L5**：ontology check 必须先超过空结果重试基线。
- **02-L6**：没有单一向优来源。
- **C-03（度量错配）**：只看 accuracy 会把 catch 与 FA 混在一起；必须分开报。

## 9. 还没解决 / 下一步

- **真实 agent 错误的 catch**：curated 18.9% 是真实答案；能不能 >30% 且 FA <10%？
- **语义错误**：类型都对、问错问题，用什么 checker？LLM judge precision 更高，但成本/稳定性如何？
- **空结果 + ontology 的组合净收益**：本文没给组合相对空结果基线的增益。
- **false alarm 的信任成本**：Google 10% 预算是否适用于 agent？
- **curated 维护成本**：与 data-derived 自动生成的长期对比。
- **同源 context+checker 的 catch 下降**：确认偏差还是信息冗余？

## 10. 原文

- arXiv:2610.37809
- PDF：`src/papers/2610.37809-what-does-an-ontology-catch/`
- 代码/数据：论文提供 replication package；正文链接。
