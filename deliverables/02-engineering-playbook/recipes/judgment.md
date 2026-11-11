---
status: draft
updated: 2026-11-09
parent: ../README.md
basis: E-02/E-03/E-20；evidence & checker mechanism
---

# R4–R5 · 判定：输出时带依据，输出后查结构

> 两条 recipe 都在「产出」侧，但强度不同：R4 只约束格式与声明，**不改变走向**；R5 能 flag/阻断，**改变走向**。不要把它们混成一个「更懂业务的校验层」。

## 0. 先选哪一条

| 你的问题 | 选 | 不要选 |
|---|---|---|
| 答案没有依据、无法审计、不知道是否检索到 | R4 | R5 不能补检索 |
| 答案有依据，但类型/关系/模式经常错 | R5 | R4 不检查语义 |
| 需要「通过/违反/没检查完」三态 | R5 | R4 没有 verdict |
| 需要形式正确性保证 | 直接 reasoner | R4 的等级是模型自评 |
| 主要错是「意思反了/边界划错」 | R5 的 LLM judge 分支（先测净修复） | 结构 checker 抓不到 changes of meaning |

---

## R4 · 输出证据契约：让答案带依据和接地等级

### 目标

把「无根据的结论」变成可审计的字段：每条结论带观察依据 + 接地等级；把「没检索到」「检索到但不够」「检索到但无关」分开。


> **为什么（机制）**：answer 不带 observations 时，模型分不清「没检索到/检索到但不够/检索到但无关」；契约把三态变成字段，让「无根据」可见——但不阻断、不保证真值，grounding 是模型自评。
### 适用 / 不适用

| 适用 | 不适用 |
|---|---|
| 有 OWL reasoner / SPARQL endpoint，能跑 `ASK`/`SELECT` | 没有 reasoner/SPARQL，只剩概念卡 |
| 领域本体覆盖问题所需概念 | 问题超出本体覆盖；未知 IRI 高 |
| 答案主要靠本体/证据，不是纯文本阅读或计算 | 答案主要靠 reading comprehension/calculation |
| 需要审计字段，不要求形式保证 | 需要「形式正确性保证」 |

### 前提

- concept card 能生成（1–2k 字符/卡）。
- 有 `DESCRIBE(iri)` / `ASK(s,p,o)` / `SELECT(query)` 三原语。
- 有 BM25 fallback：精确查询空结果时取 5–10 张候选卡。
- 能记录 tool actions / generated tokens；有预算闸。

### 接缝 / 形态

输出时 / `compiled` 或 `context`。它约束格式与声明，不保证语义真值；类别上属于「弱到中」约束。

### 最小数据契约

```text
output: {answer, observations[], grounding: entailed|supported|related|unrelated}
```

- `observations` 引用三类观察：`DESCRIBE` 的 concept card、`ASK` 的 entailed/not-entailed/unknown、`SELECT` 的 bindings。
- **E=∅ 时不报 grounding**：过滤失败/空观察后没有证据，走 `P_own`，不编造等级。
- `unrelated` 只用于「有观察但与问题/答案无关」，不是「没检索到」。

**concept card 字段**：`iri, label, definition, parents[], children[], relations[], comments[], source`；单卡截断 1–2k 字符。

**预算**：≤10 tool actions；≤5,000 generated tokens（Answer Step 2 另 512）；实测均值 5.8 calls / 9.7k tokens（Qwen Test 3），不是上限。

### 做法

1. **生成 concept cards**（1–2 人日/本体）；接 `DESCRIBE`/`ASK`/`SELECT`；空结果走 BM25 fallback。
2. **名字链接**：精确 → 多义候选 → 未知名字先 BM25 取 200 候选池 → 相似度重排给 5 个；让 agent 改 query，而不是把错名当「本体里没有」。
3. **200 题回放**：报检索率、引用率、每问 calls/tokens；grounding 等级单独校准。
4. **校准 grounding**（见下）；未校准前只做排序/人工分流，不自动放行。
5. **预算闸**：tool actions >10 或 generated tokens >5,000 → 停/降级到纯 concept card。

### grounding 校准协议（工程配方，`推测`）

> E-03 明确：等级是**模型自评**、未校准，作者不提供形式正确性保证。下面的协议是补丁，不是论文方法。
>
> 注意：公开的 conformal/faithfulness 方法多是**二值**（supported/not），不是 entailed/supported/related/unrelated 四级；不要假设有现成库能直接校准四级，需自建标注与阈值。

1. 从 200 题里分层抽 **100–200 条/等级**（entailed/supported/related/unrelated），独立人工标注「这个等级是否成立」。
2. 对每个等级算 precision/recall；报 Wilson CI；不要只报总体准确率。
3. 若某等级 precision < 0.7（工程建议），把该等级降级为「提示」，不参与自动路由。
4. 若 `entailed+supported > 90%`（等级通胀），抽样复核；通胀时不要用等级做门槛。
5. 每季度/本体大版本变更后重标；阈值与标注版本入档。

**没有独立标注 → 只做提示，不做自动路由/放行。**

### 证据

- 三个大本体、六个医学 QA、2 backbone：平均 **50.5%/68.1%**；Tests 1–2 **+10–15pp**；Test 3 同 8k 预算 **84.9% vs 66.7%**；9.7k vs 96.7k tokens/问（E-03）。
- grounding 分布：entailed+supported 70.0%/53.2%；unrelated 0.2%/7.8%；部分答案无 grounding（E=∅）。
- Qwen Test 3：entailed 94.9% 正确、supported 82.1% 正确；这是切片，不是校准曲线。
- 检索是主瓶颈：gold evidence 完整检索 MCQ 61.7% vs OQ 23.6%。
- 不是单一变量：concept card、ReAct、fallback、answering step 都在变；去掉 answering step 平均掉 2.9–5.8 点。

### 成本

| 项 | 量级 | 等级 |
|---|---|---|
| concept card 生成 | 1–2 人日/本体 | 推测 |
| reasoner/SPARQL 集成 | 1–2 人周 | 推测 |
| 运行 | 5.8 calls / 9.7k tokens 每问（Qwen Test 3） | 已核（观测） |
| 校准标注 | 100–200/等级；人日未测 | 推测 |

### 验收 / 停

| 指标 | 通过线（工程建议） | 停 |
|---|---|---|
| gold evidence 检索率 | ≥50% | <50% → 先修检索 |
| 未知 IRI | <20% | >20% → 先补本体 |
| 引用率 | ≥85% | 低于线 → 先修 name linking/检索 |
| grounding 校准 | 每级 precision/recall 可报 | 无独立标注 → 只做提示 |
| 预算 | ≤10 actions / ≤5,000 generated | 超限 → 停/降级 |

### 失效模式

- **等级自评。** 模型给自己打分；作者写明不提供形式正确性保证。
- **等级未校准。** 94.9/82.1 是一个切片，不能当阈值依据。
- **等级通胀。** 全标 supported，字段存在但无区分度。
- **引用形式化。** 引用了观察，但结论与观察无关。
- **格式开销。** 每条结论都带证据会增加输出 token；论文没有单列这项开销。
- **把等级当形式证明。** 最常见的误用。

### citation 正确性（R4 不覆盖）

> R4 只测「有没有引用」；不测「引用是否支持结论」。这一节是边界 + 最小协议，**不是新 E**。
>
> 外部依据：[ALCE 卡](../../../src/web/alce/alce.card.md)（EMNLP 2023）；AIS 的「According to P, s」判定式与 AttributionBench 的「自动判官约 80% macro-F1 上限」作对照（转述，待核）。

- **两个概念**：citation presence（答案带 observations/span）≠ citation correctness（引用支持结论）。R4 的「引用率 ≥85%」是前者。
- **判 P，不判真**：把句子还原成去语境的独立命题（补代词/时间/指代）；问「According to P, s 是否成立」，而不是「s 对不对」。
- **20 条小样**：按句抽 20 个「陈述—引用」对，每句固定取 1 条引用；风险分层——多跳、数字/日期、比较级、否定/限定各 ≥3 条。
- **三值 + 不可判**：`S`（仅凭该引用可推出）/ `P`（需与其它引用合并，或只部分支持）/ `N`（不支持，或只话题相关/断章取义）/ `U`（句子不可解读，单列，不计入分子分母）。
- **两个数**：citation recall = `S` 占比（严格版只算 S；宽松版算 S+P，两版都报）；citation precision = 每条引用 `S=1 / P=0.5 / N=0`。ALCE 式反事实「去掉该引用后是否仍成立」单独标**冗余引用**，不混进 N。
- **人评先行**：两人独立标注，报 κ；κ < 0.6 或 precision < 0.9 → 只做提示，不自动放行。
- **LLM judge 只做预标注**：先在这 20 条上测与人一致率；AttributionBench 的经验上限约 80% macro-F1，达不到就不得替代人评。
- **停**：没有标签 → 标 `gap`；不要把 presence 的 85% 当 correctness 的通过线。
- **EXP-004（2026-11-11）**：抽 20 条交付物 claim + 所引 E 行，两个 agent 标 S/P/N，κ=1.0；strict S=5/20（25%），宽松 57.5%，N=2/20。结论：**E 行单独只支持 1/4 的 claim**；多数是 E 行摘要掉了具体数字/条件，细节在 digest。E-xx 是地址，不是自足 warrant。**EXP-004b**：同一 20 对改用「E 行 + [evidence-anchors](../../../topics/evidence-anchors.md) 锚」后，strict 25% → **55–65%**，N 2 → **0**；剩余 P 多是处方/解释，应标 `工程建议`，不要挂 E。见 [exp-004](../../_plans/2026-11-11-exp-004-citation-audit.md)。

### 可抄锚点

- [evidence 机制](../../../topics/02-judgment/evidence/mechanism.md) 的「OA-RAG 实际做法」「接口与预算」「stop」。
- OA-RAG 的三原语、name linking、E=∅ 处理；不要抄「等级=保证」。

---

## R5 · 输出后 checker：先超过空结果重试

### 目标

用本体当外部判据，查出**结构/声明/模式**错误；把「通过/违反/没检查完」三态显式化。

### 适用 / 不适用

| 适用 | 不适用 |
|---|---|
| 输出是 SPARQL/结构化答案，能对查询/绑定做检查 | 输出是自由文本，无法解析 |
| 错误类型是类型/声明/domain-range/模式 | 错误类型是 changes of meaning（意思反了） |
| 有 200 题 + 空结果重试基线 | 没有基线，只想「加个校验」 |
| 能接受 per-flagged 成本 | 要求零误报 |

### 前提

- 有本体/schema + 数据 summary。
- 有 SPARQL 查询与结果绑定（或等价结构化输出）。
- 能跑空结果重试基线。
- 有 200 题标注集；能人工抽 50 条。

### 接缝 / 形态

输出后 / `compiled`（本体→SHACL/checker）或 `engine`。它能 flag/阻断，但不保证语义正确。

### 最小数据契约

```text
input:  {query, bindings, ontology|schema, data_summary}
output: {verdict: pass|flag|unknown,
         constraint_id, query_fragment, message, evidence}
```

**三态不可折叠**：`unknown` 不阻断，也不能并进 `pass`；否则 catch/FA 的分母被污染（checker F7）。

### 做法

1. **先建空结果重试基线**：查询空就重试，不需要本体；人工 fault 上 catch 79.2%、FA 0%（E-02）。
2. **只有能抓「有结果但答错」的增量，才建 checker**；增量 <5pp 不建。
3. **选来源**：
   - data-derived：FA 低（3.5%）、catch 低（8.2%）；适合先上。
   - curated：catch 高（18.9%）、FA 高（16.8%）；先审计/补声明。
   - masked LLM：不稳定；不要当默认。
   - **不要盲目组合**：curated+data-derived 的 catch 只多 0.6pp、FA 多 1.0pp（F4）。
4. **200 题回放**：报 catch / FA / precision / per-1k cost；人工抽 50 条。
5. **三态显式化**：pass/flag/unknown；unknown 不阻断。
6. **feedback 默认 generic**：specific 修复 28.3% 但 corrupt 1.0%；generic 20.2%/0.2%；未验证前先 generic（工程默认，不是安全结论）。

### LLM judge 分支（不是免费升级）

- 输入：问题 + 查询 + 结果 + 答案；每条答案一次模型调用。
- 收益：UniProt 真实答案 catch 40.3%、FA 16.2%、precision 31.3；能抓 changes of meaning（结构检查 0%）。
- 代价：把 flag 当行动信号后 **40 条修好 / 83 条修坏**；人工故障上会 flag 30–38% 答案仍正确的查询。
- 规则：先测 **净修复（fixed − corrupted）**、每条答案模型调用成本、稳定性；不能只看 catch，也不能默认 judge 更好。

### 证据

- curated 18.9/16.8；data-derived 8.2/3.5；masked LLM 5.0/1.8；空结果重试 2.5/0.1（真实答案，UniProt，3,383 可检查；E-02）。
- precision（人工故障 + 25% 错答案假设）：curated 57.1、data-derived 72.3、LLM masked 93.7；**不能与真实答案口径拼接**。
- curated precision 仅略优于同率随机（+1.6 点，CI −2.3~+6.3）。
- 成本：curated **65,976 tokens / 46.0 s per flagged**；data-derived **28,076 / 17 s per flagged**；不是 per checked。
- 空结果重试 catch 79.2%/FA 0% 是强基线；真实答案 catch 2.5%/FA 0.1%。

### 成本

```text
per-1k cost = flag_rate × per-flagged cost × 1000
```

先量 `flag_rate`；66k 不是每答案成本。LLM judge 按每条答案一次调用计，单位成本未测。

### 验收 / 停

| 指标 | 通过线（工程建议） | 停 |
|---|---|---|
| 增量 catch | ≥5pp | <5pp → 停 |
| FA | ≤15% | >15% → 停 |
| 净修复 | >0（judge 分支） | ≤0 → 不用 judge |
| per-1k 成本 | ≤人工审核 1/3 | 超过 → 停 |
| 语义错为主 | 换 judge/人工 | 结构 checker 抓不到 → 不要硬上 |
| 三态 | checked/passed/undetermined 都报 | 只报 pass/fail → 不可比 |

### 失效模式

- **误报导致修坏。** 正确答案被 flag，agent 去修，把对的改成错的。
- **漏检语义错误。** 类型都对、关系方向反了/边界划错；结构检查 0%。
- **判定器不可解释。** 只说错、不说哪条约束，模型只能换姿势重试。
- **串联放大误报。** 前一级误报引发下游大量无效工作。
- **把 curated 当权威。** FA 主源是缺声明/闭世界，不是「与数据矛盾」；先审计/补声明。
- **把 LLM judge 当更好替代。** 检错更多，但修坏多于修好；先测净修复。
- **用 accuracy 评估 checker。** catch 与 FA 混在一起，会得出反向结论。
- **同源 context+checker。** catch 下降是探索性观察；机制未定，不要写成部署规则。

### 可抄锚点

- [checker 机制](../../../topics/02-judgment/checker/mechanism.md) 的「三种来源」「判定回路」「成本」「stop」。
- Ontology Catch 的 catch/FA 口径、空结果基线、per-flagged 成本；不要抄「curated 权威」。
- [open-ontologies 的三态 ](offline-and-obda.md#r10--离线ci-shacl把没检查完做成第三态)；第三态是接口设计，不是效果证据。

**出处**：[evidence 机制](../../../topics/02-judgment/evidence/mechanism.md) · [checker 机制](../../../topics/02-judgment/checker/mechanism.md) · [E-02/E-03](../../../topics/conclusions.md)
