---
status: draft
updated: 2026-11-11
parent: ../README.md
basis: E-20；evidence & checker mechanism（E-02/E-03 已撤回）
---

# R4–R5 · 判定：输出时带依据，输出后查结构

> 两条 recipe 都在「产出」侧，但强度不同：R4 只约束格式与声明，**不改变走向**；R5 能 flag/阻断，**改变走向**。不要把它们混成一个「更懂业务的校验层」。
>
> **词源**：「约束/校验/三态」取 RDF 图约束语义（`N: W3C SHACL`），规则与 target 见 `N: W3C SHACL-AF`；「接地（grounding）/ 接地等级」和「checker 的 catch/FA」是 `local` 工作词，没有标准锚——E-03/E-02 已撤回，本节只保留机制描述，不给效应量。

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

> **W-02**：原锚 E-03 撤回；R4 转 gap。机制保留，效应量按 [W-02](../02-sections/91-canonical.md#w-table) 重测；不再逐句解释撤回。

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

**预算**：按 W-02 先记每次答案的调用数与 token（这是你的基线）；工具调用上限按你的 harness 设，不沿用论文值。

### 做法

1. **生成 concept cards**（1–2 人日/本体）；接 `DESCRIBE`/`ASK`/`SELECT`；空结果走 BM25 fallback。
2. **名字链接**：精确 → 多义候选 → 未知名字先 BM25 取 200 候选池 → 相似度重排给 5 个；让 agent 改 query，而不是把错名当「本体里没有」。
3. **200 题回放**：报检索率、引用率、每问 calls/tokens；grounding 等级单独校准。
4. **校准 grounding**（见下）；未校准前只做排序/人工分流，不自动放行。
5. **预算闸**：tool actions >10 或 generated tokens >5,000 → 停/降级到纯 concept card。

### grounding 校准协议（工程配方，`推测`）

> 原 E-03 已于 2026-11-11 撤回（历史注记：其等级是**模型自评**、未校准，无形式正确性保证）。下面的协议是工程兜底补丁，不是论文方法。
>
> 注意：公开的 conformal/faithfulness 方法多是**二值**（supported/not），不是 entailed/supported/related/unrelated 四级；不要假设有现成库能直接校准四级，需自建标注与阈值。

1. 从 200 题里分层抽 **100–200 条/等级**（entailed/supported/related/unrelated），独立人工标注「这个等级是否成立」。
2. 对每个等级算 precision/recall；报 Wilson CI；不要只报总体准确率。
3. 若某等级 precision < 0.7（工程建议），把该等级降级为「提示」，不参与自动路由。
4. 若 `entailed+supported > 90%`（等级通胀），抽样复核；通胀时不要用等级做门槛。
5. 每季度/本体大版本变更后重标；阈值与标注版本入档。

**没有独立标注 → 只做提示，不做自动路由/放行。**

### 证据

**W-02；R4 没有 admitted 效应量。** 重启按 W-02 协议（200 题、检索率/引用率、每级 100–200 独立标注）；没有独立标注前不设门槛、不做自动路由。

### 成本

| 项 | 量级 | 等级 |
|---|---|---|
| concept card 生成 | 1–2 人日/本体 | 推测 |
| reasoner/SPARQL 集成 | 1–2 人周 | 推测 |
| 运行 | 按 W-02 记 per-answer 调用/token | 工程记录 |
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
- **等级未校准。** 要当阈值依据，先按 W-02 每级做 100–200 条独立标注。
- **等级通胀。** 全标 supported，字段存在但无区分度。
- **引用形式化。** 引用了观察，但结论与观察无关。
- **格式开销。** 每条结论都带证据会增加输出 token；论文没有单列这项开销。
- **把等级当形式证明。** 最常见的误用。

### citation 正确性（R4 不覆盖）

> R4 只测「有没有引用」；不测「引用是否支持结论」。这一节是边界 + 最小协议，**不是新 E**。
>
> 外部依据：[ALCE 卡](../../../meta/audits/2026-11-11-source-purge.md#src-web-alce)（EMNLP 2023）；AIS 的「According to P, s」判定式与 AttributionBench 的「自动判官约 80% macro-F1 上限」作对照（转述，待核）。

- **两个概念**：citation presence（答案带 observations/span）≠ citation correctness（引用支持结论）。R4 的「引用率 ≥85%」是前者。
- **判 P，不判真**：把句子还原成去语境的独立命题（补代词/时间/指代）；问「According to P, s 是否成立」，而不是「s 对不对」。
- **20 条小样**：按句抽 20 个「陈述—引用」对，每句固定取 1 条引用；风险分层——多跳、数字/日期、比较级、否定/限定各 ≥3 条。
- **三值 + 不可判**：`S`（仅凭该引用可推出）/ `P`（需与其它引用合并，或只部分支持）/ `N`（不支持，或只话题相关/断章取义）/ `U`（句子不可解读，单列，不计入分子分母）。
- **两个数**：citation recall = `S` 占比（严格版只算 S；宽松版算 S+P，两版都报）；citation precision = 每条引用 `S=1 / P=0.5 / N=0`。ALCE 式反事实「去掉该引用后是否仍成立」单独标**冗余引用**，不混进 N。
- **人评先行**：两人独立标注，报 κ；κ < 0.6 或 precision < 0.9 → 只做提示，不自动放行。
- **LLM judge 只做预标注**：先在这 20 条上测与人一致率；AttributionBench 的经验上限约 80% macro-F1，达不到就不得替代人评。
- **停**：没有标签 → 标 `gap`；不要把 presence 的 85% 当 correctness 的通过线。
- **EXP-004（2026-11-11）**：抽 20 条交付物 claim + 所引 E 行，两个 agent 标 S/P/N，κ=1.0；strict S=5/20（25%），宽松 57.5%，N=2/20。结论：**E 行单独只支持 1/4 的 claim**；多数是 E 行摘要掉了具体数字/条件，细节在 digest。E-xx 是地址，不是自足 warrant。**EXP-004b**：同一 20 对改用「E 行 + [evidence-anchors](../../../topics/evidence-anchors.md) 锚」后，strict 25% → **55–65%**，N 2 → **0**；剩余 P 多是处方/解释，应标 `工程建议`，不要挂 E。见 [exp-004](../../_workpapers/2026-11-11-exp-004-citation-audit.md)。

### 可抄锚点

> **源已移出**：OA-RAG 已按 §4 移出；下面只作历史读法，不要照抄。
- [evidence 机制](../../../topics/02-judgment/evidence/mechanism.md) 的「实际做法」「接口与预算」「stop」——当历史模板读。
- 三原语、name linking、E=∅ 处理只作结构参考；**不要抄「等级=保证」**。

---

## R5 · 输出后 checker：先超过空结果重试

> **W-01**：原锚 E-02 撤回；R5 转 gap。机制保留，catch/FA 按 [W-01](../02-sections/91-canonical.md#w-table) 重测。

### 目标

用本体当外部判据，查出**结构/声明/模式**错误；把「通过/违反/没检查完」三态显式化。

> **机制（L1）**：checker 把答案/查询送进 reasoner 或 SPARQL，检查类型/声明/domain-range；它只能判「结构上说不通」，判不了「意义变了」。**条件**：有声明/闭世界；**反例**：语义错为主时越查越误；**决策**：先在本域建空结果基线，再谈 checker。

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

`data_summary` = 可用的数据摘要（表/列/范围/空值/样例），**不是全量数据**；用于判断 checker 有没有足够事实判。

**三态不可折叠**：`unknown` 不阻断，也不能并进 `pass`；否则 catch/FA 的分母被污染（checker F7）。

### 做法

1. **先建本域基线**：空结果重试要自己重跑（W-01）；curated/data-derived 的 catch/FA 也在本域重测，不沿用旧值。
2. **只有能抓「有结果但答错」的增量，才建 checker**；增量门槛要由新源/本域回放重定，不沿用旧 +5pp。
3. **来源选择**：curated / data-derived / masked LLM 的偏向是机制假设（`推测`）；没有新源前不做默认推荐，也不盲目组合。
4. **200 题回放**：报 catch / FA / precision / per-1k cost；人工抽 50 条；**这些是测量项，不是旧结论**。
5. **三态显式化**：pass/flag/unknown；unknown 不阻断（E-20 的接口层面仍成立）。
6. **feedback 默认 generic**：specific 可能修好也可能修坏；没有新源前先 generic（工程默认，不是安全结论）。

### LLM judge 分支（不是免费升级）

- 输入：问题 + 查询 + 结果 + 答案；每条答案一次模型调用。
- **旧观察方向（W-01）**：judge 能抓结构检查抓不到的语义错，但「修坏」可能多于「修好」；用净修复协议自己测。
- 规则：先测 **净修复（fixed − corrupted）**、每条答案模型调用成本、稳定性；不能只看 catch，也不能默认 judge 更好。

### 证据

**W-01；R5 没有 admitted 效应量。** 重启按 W-01：200 题分层、catch/FA/净修复分开、per-flagged 成本；空结果重试基线在本域重建。


### 成本

```text
per-1k cost = flag_rate × per-flagged cost × 1000
```

先量 `flag_rate`；per-flagged 成本按 W-01 记账。LLM judge 按每条答案一次调用计，单位成本要自己测。

### 验收 / 停

| 指标 | 通过线（工程建议） | 停 |
|---|---|---|
| 增量 catch | 旧线 ≥5pp；**只作测量项**（新源前不设线） | 量不出 → 停 |
| FA | 旧线 ≤15%；**只作测量项**（新源前不设线） | 量不出 → 停 |
| 净修复 | >0（judge 分支） | ≤0 → 不用 judge |
| per-1k 成本 | ≤人工审核 1/3 | 超过 → 停 |
| 语义错为主 | 换 judge/人工 | 结构 checker 抓不到 → 不要硬上 |
| 三态 | checked/passed/undetermined 都报 | 只报 pass/fail → 不可比 |

### 失效模式

- **误报导致修坏。** 正确答案被 flag，agent 去修，把对的改成错的。
- **漏检语义错误。** 类型都对、关系方向反了/边界划错；结构检查抓不到这类（机制判断，`推测`）。
- **判定器不可解释。** 只说错、不说哪条约束，模型只能换姿势重试。
- **串联放大误报。** 前一级误报引发下游大量无效工作。
- **把 curated 当权威。** 常见 FA 源是缺声明/闭世界（机制假设，待新源验证）；先审计/补声明。
- **把 LLM judge 当更好替代。** 旧观察提示「修坏可能多于修好」（E-02 已撤回）；先测净修复。
- **用 accuracy 评估 checker。** catch 与 FA 混在一起，会得出反向结论。
- **同源 context+checker。** catch 下降是探索性观察；机制未定，不要写成部署规则。

### 可抄锚点

- [checker 机制](../../../topics/02-judgment/checker/mechanism.md) 的「三种来源」「判定回路」「成本」「stop」。
- Ontology Catch 已移出：口径可读，数值按 W-01 重测；不要抄「curated 权威」。
- [open-ontologies 的三态 ](10-offline-and-obda.md#r10--离线ci-shacl把没检查完做成第三态)；第三态是接口设计，不是效果证据。

**出处**：[evidence 机制](../../../topics/02-judgment/evidence/mechanism.md) · [checker 机制](../../../topics/02-judgment/checker/mechanism.md) · [E-02/E-03（均已撤回，历史配方参考）](../../../topics/conclusions.md)
