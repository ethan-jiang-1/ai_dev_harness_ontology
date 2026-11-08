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
3. **它发现什么**：curated 本体抓得多、但误报也多；真实答案上它的 precision 只比随机高 1.6 点（CI 跨零）。数据派生本体在「人工故障 + 25% 错答案」假设下 precision 更高（72.3%），但只抓到 8.2% 的真错；**空结果重试**是很强的基线（人工故障 catch 79.2%、FA 0%）。没有单一向优的来源。

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
| **type swap** | 把类/属性/常量替换成 co-occurrence 图上 2 或 4 步外的**不同类型**项；用来测 domain/range 等结构检查能抓的类型错误。**不是「类型都对、关系错」**；后者是 changes of meaning（语义错）。 |
| **domain / range** | 属性允许的主语类 / 宾语类；违反会产生结构误报。 |
| **disjointness** | 两个类不能有共同实例；本文发现它几乎不贡献 flag。 |
| **triple / binding** | RDF 的三元组 / 查询结果变量的绑定；binding check 是对结果重新求值。 |
| **C1–C5** | 预注册比较：C1 context 准确率、C2 人工故障 FA/type-swap、C3 LLM 对照 FA、C4 组合净收益、C5 feedback。 |
| **confirmatory / exploratory** | 前者是预注册检验、有权重；后者是描述性/事后比较，不能当确认证据。 |

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

| 来源 | catch（真实答案） | FA（真实答案） |
|---|---|---|---|
| curated | **18.9%** | **16.8%** |
| data-derived | **8.2%** | **3.5%** |
| LLM-generated（masked，三个） | 5.0% | 1.8% |
| 空结果重试 | 2.5% | 0.1% |

- **precision 不是真实答案口径**：57.1/72.3/93.7/100 是用人工故障的 catch/FA、在「错答案占 25%」假设下算的。若把同一公式套到真实答案 18.9/16.8，会得到约 27.3%，但**论文没有直接给这个数**；只能当反推。表里只放真实答案 catch/FA，precision 单独看。
- **C2（人工故障上的确认性比较，per-question controls）**：curated − data-derived：FA **+8.6**（6.0,11.2），type-swap catch **−22.3**（−23.5,−21.0）；两个方向都超过 5 点 margin。注意：type-swap 故障是从 **data-derived 自己的 co-occurrence graph** 生成的，设计上偏向 data-derived；−22.3 只由 4 步 swap 驱动，2 步 swap 的差异未确立（−1.3，CI 跨零，exploratory）。这不是干净的普遍优势。
- **C3（人工故障）**：curated − masked LLM：FA **+15.7**（13.7,17.9）。
- **C1a（context 用法，pooled）**：data-derived 作上下文比 curated 准 **2.1 点**（curated−data −2.1，CI −3.4~−0.9，p*=0.003）。但同一 C1 的 **C1b** 在 Qwen3.8 / Sonnet 上 ±3 等价未确立（−1.1 [−4.2,1.9]、−0.8 [−2.7,0.9]）；不能把这个 pooled 优势说成跨模型稳健。

> 出处：Table 2, p.7；Table 3, p.7；§5 RQ1。**precision（人工故障、25% 错答案假设）：curated 57.1、data 72.3、LLM masked 93.7、空结果 100。**

### 4.2 人工故障

| 来源 | catch（all） | catch（rows returned） | FA（人工故障/control） |
|---|---|---|---|
| curated | 60.1% | 54.3% | **15.0%** |
| data-derived | 75.6% | 62.1% | **9.7%** |
| 空结果重试 | 79.2% | 0.0% | 0% |

**空结果基线在人工故障上已经很强**：很多故障会让查询返回空；ontology check 的增量价值主要在「查询仍有结果」的错误。

> 出处：Table 2, p.7；§5 RQ1。注意：16.8%/3.5% 是真实答案的 FA，15.0%/9.7% 是人工故障/control 的 FA；不能跨表拼接。

### 4.3 组合与反馈

- 组合 curated + data-derived：真实答案 catch 19.5%、FA 17.8%；比 curated 单用只多 0.6 点 catch，却多 1.0 点 FA。C4 的注册检验在人工故障/25% 错答案上：combined−curated **−0.5**（CI −1.5~0.4），combined−data-derived **−10.6**（CI −12.2~−9.2）；组合不比 curated 好，且显著差于 data-derived。
- specific feedback：修复 28.3% 的 flagged wrong，但 corrupt 1.0% 的 flagged correct；generic 是 20.2% / 0.2%。specific 的净修复更高；C5 的最终准确率差异未确立，不是「generic 更安全」。

> 出处：Table 2（fixed/corrupted）、Table 3（C4/C5）；§5 RQ3；Table 4 是人工故障类别，不是组合/反馈。

### 4.4 成本

- curated check：每**被 flag 的答案** 65,976 tokens / 46.0 s（median）。
- data-derived：28,076 tokens / 17 s（同为 per answer flagged，不是 per answer checked）。
- LLM ontology 生成：<$1/个（Claude Opus 5.5）；data-derived 的 setup 成本/时间**未记录**（论文 Table 8 的 Setup 列是「—」）。

> 出处：Table 8 / Appendix B.3；§5 RQ2/RQ3。

### 4.5 这些数字之间的逻辑

- **为什么 curated catch 高、FA 也高？** 它检查的约束多（domain/range/disjointness），能抓到更多类型/声明错误；但 schema 与数据漂移时，它会把大量正确答案标错。
- **为什么 data-derived FA 低、catch 也低？** 它从数据总结模式，不会 flag 数据里出现≥5 次的模式；它抓的是「数据里没见过的组合」，不是语义错误。
- **为什么 curated 会与自己的数据矛盾？** 发布状态的本体可能缺声明、与实例数据不一致；14.3% 的 Linked Data triples 使用未声明属性（这是论文引用的外部 crawl 统计，不是本文测量）。每个缺失声明都会误报用到它的正确答案。
- **为什么空结果重试这么强？** 很多人工 fault 会让查询返回空；空结果重试不需要本体。但真实 agent 的「有结果但答错」它抓不到（真实答案 catch 2.5%）。
- **为什么组合没有净收益？** 组合只有 curated + data-derived 两源，覆盖重叠；curated 的 FA 抵消了 data-derived 的增量 catch；真实答案上只多 0.6 点 catch、多 1.0 点 FA。

## 5. 这些数字不能说明什么

1. **不是「本体无用」。** curated 在真实答案上 precision 只略高于随机（+1.6，CI 跨零）；**data-derived 的真实答案 precision 是 29.9%，比同率随机 flag 高 +14.4 点**——它 catch 低，但 precision 不差。curated 的明显优势在 invented identifier（77.4% vs 随机 48.1%）；type swap 只略高于随机（55.3% vs 48.0），且低于 data-derived（78.4%）。
2. **不是「data-derived 更好」。** data-derived 的 precision 高，但 catch 只有 8.2%；它抓不到语义错误（类型都对、问错问题）。
3. **不是「空结果重试就够了」。** 它在真实答案上只抓 2.5%；对「查询仍有结果」的错误，ontology check 才有增量。
4. **UniProt 是唯一 confirmatory。** 其他图 exploratory；private 只报率。
5. **人工故障可能不代表真实错误。** 真实 agent 错误稀疏且分布不均。
6. **知道正确答案。** 真实部署没有这个条件；precision/recall 无法直接算。
7. **curated/data-derived setup 成本未测。** `<$1` 是 LLM ontology 的生成成本，不是 data-derived，也不是维护成本。

## 6. 工程上怎么用

### 6.1 复刻顺序

1. **先建空结果重试基线。** 不加本体，先看执行结果本身能暴露多少错。
2. **做 data-derived summary 审计 curated 本体。** false alarm 主要来自 domain/range 与 declaration check；「curated schema 与自身数据矛盾」是 Table 5 的观察，不是 false-alarm 来源（Table 6 里 data clash=0）。
3. **按错误类型选 checker。** 类型/声明/模式错 → data-derived / declaration check；语义错 → 本体检查抓不到，换 LLM judge 或人工。
4. **同时报 catch 与 FA。** 只看 accuracy 会把「多抓错、多杀对」混在一起。
5. **同源 context+checker 的 catch 下降是探索性观察**，不要写成部署规则；机制（确认偏差 vs 信息冗余）未定。
6. **不要盲目组合。** 组合往往增加 FA 而不增加净收益。
7. **把 FA 当预算。** Google 的静态分析要求 effective FP <10%；agent 场景要自己定。
8. **specific feedback 要验证。** specific 修复 28.3% / corrupt 1.0%，generic 20.2% / 0.2%，specific 净修复更高；C5 的最终准确率差异未确立（0.2，CI −3.2~3.1），不能默认 generic 更安全。

### 6.2 成本与使能

| 成本 | 一次性/每次 | 说明 |
|---|---|---|
| curated 本体 | 发布方一次性（未测） | 可能缺声明/与数据矛盾；维护成本高 |
| data-derived summary | 一次性，成本未记录 | 从数据总结类/属性/模式；可自动生成 |
| LLM-generated 本体 | 一次性，<$1/个 | 不稳定；需多个 draw + 评估 |
| check | 每**被 flag 的答案** | curated 66k tokens / 46 s；data 28k / 17 s；不是 per answer checked |
| 重试 | 每次 flag | 由 false alarm 触发；成本随 FA 上升 |
| 人工标注 | 评估期 | 需要正确答案/抽样标注；部署时通常没有 |

**使能条件**：可执行 schema（OWL/SHACL/SPARQL）、能读数据生成 summary、有 SPARQL endpoint、能拿到正确答案或抽样标注。

### 6.3 何时用 / 何时别用

**用**：知识图谱有可执行 schema；任务主要是类型/声明/模式错误；有正确答案或能人工标注；false alarm 预算明确。

**别用**：语义错误为主；没有正确答案、无法估 precision；curated 本体与数据不一致且没人维护；查询大量使用 UNION/subquery；false alarm 会直接损害用户信任。

### 6.4 最小落地清单

1. **先建空结果重试基线。** 不加本体，记录 catch/FA/成本。
2. **做 data-derived summary。** 从数据总结类/属性/模式；生成成本未记录；先审计 curated 的缺声明/矛盾。
3. **按错误类型选 checker。** 类型/声明/模式错 → data-derived/declaration；语义错 → LLM judge/人工。
4. **同源 context+checker 的 catch 下降是探索性观察**；不要写成「判定器必须不同源」的部署规则。
5. **不要盲目组合。** 组合通常增加 FA；先证明净收益。
6. **同时报 catch/FA/成本。** 只看 accuracy 会反向。
7. **specific feedback 要验证。** specific 净修复更高；C5 最终准确率差异未确立，不能默认 generic 更安全。

## 6.5 工程配方（E3）

### 接口

- **输入**：SPARQL 查询、结果绑定、本体/schema、数据 summary。
- **输出**：`{verdict: pass|flag|unknown, constraint_id, query_fragment, message, evidence}`；flag 要能指出「哪条约束/哪个 triple」，否则 agent 只会换姿势重试。
- **挂载点**：agent 执行前（query check）或执行后（binding check）；unknown 不阻断，只记录并降级到「空结果重试 + 人工抽检」。
- **specific vs generic**：specific 带 constraint_id/片段；generic 只说「请重查」。specific 的 corrupt 更高，默认先 generic，验证后再 specific。

### data-derived 建库参数

- 模式阈值：属性/类共现 ≥5 次才允许；低于 5 次不 flag，避免把长尾当异常。
- summary 规模：类/属性/模式列表；论文未给上限；工程上按 1–2 万实体估，超过就分域重建。
- 重建频率：数据变更/本体变更触发；全量重建按周/月，增量按日。
- curated 缺声明：先自动补声明（domain/range），补不了的进人工队列；**disjointness 不贡献 flag，别把它当主检查**。

### 成本

- 论文只给 per **flagged** answer：curated 65,976 tokens/46s，data 28,076/17s；不是 per checked。
- 折算：`per-1k cost = flag_rate × per-flagged cost × 1000`；curated FA 16.8% 时，per-1k 成本约是 per-flagged 的 0.168 倍；别把 66k 当每答案成本。
- setup：LLM ontology <$1/个；data-derived setup 未记录，按 1–2 人日估（`推测`）。
- 维护：curated 缺声明/矛盾审计、data summary 重建、告警处置；按 0.5–1 人日/月估（`推测`）。

### stop condition

- 空结果重试基线：人工 fault catch 79.2%/FA 0%；真实答案 catch 2.5%/FA 0.1%。**本体 checker 必须先超过它**。
- 采纳门：真实/人工混合集上 catch ≥30% 且 FA ≤10%，per-1k 成本 ≤ 人工审核的 1/3；否则不做。
- 只看「有结果但答错」的增量：若增量 catch <5pp，停；语义错（changes of meaning）结构检查 0%，不要指望它。
- 同源 context+checker、generic/specific 的结论是 exploratory/未定；不要写进上线门。

### 部署度量

- 没有 ground truth 时 precision 不可算；用 100–400 条分层抽样人工审计，报 Wilson CI；每季度重抽。
- 在线 A/B：同一流量分「空结果重试」vs「空结果重试 + data-derived check」；主指标 catch/FA、per-1k token、告警处置工时。
- LLM judge 分支：需另测 precision/成本/稳定性；本文说 judge 检错更多但修坏多于修好，不能默认更好。

### 第一个 sprint

2 周、本方 KG、200 题：

1. 只上空结果重试，记录 catch/FA/token/延迟基线。
2. 生成 data-derived summary + declaration/pattern check；同一批题测增量 catch/增量 FA。
3. 记录 setup 人日与 per-flagged 成本；抽 50 条人工复核。
4. 出口：FA ≤ 自定预算（如 10%）且增量 catch ≥5pp → 进第二阶段；否则停，不接 curated、不组合。

### 替代方案

- 空结果重试（最便宜）；LLM judge（语义错更强，但成本/稳定性未定）；人工审核；采购 SHACL/校验服务；curated 本体（需先审计）。
- 论文没有与 LLM judge/人工/SHACL 服务的头对头成本；build/buy 只能给公式。

## 6.6 客户价值假设（V2/V3，`推测`）

- **受益者**：KG/agent 平台团队、数据治理/合规；痛点：错误答案上线、人工审核贵、告警疲劳。
- **指标**：每千次产出的真实语义错误拦截数、误判正确数、per-1k token/工时、告警处置时长。
- **反事实**：不做 checker → 空结果重试 + 人工抽检；先测这个基线。
- **V3 试点**：200 题、data-derived check vs 空结果重试；成功 = 增量 catch ≥5pp 且 FA ≤10%、per-1k 成本 ≤ 人工 1/3；失败 = 增量 <5pp 或 FA >15%；停止线 = 年省审核工时 < 维护成本。
- **反例**：语义错为主；没有 ground truth；curated 与数据矛盾；FA 导致修坏超过拦下的错。

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
- PDF：同目录 `2610.37809-what-does-an-ontology-catch.pdf`
- 代码/数据：论文提供 replication package；正文链接。
