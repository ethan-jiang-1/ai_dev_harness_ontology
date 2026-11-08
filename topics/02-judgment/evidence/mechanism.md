# 输出时证据契约 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 问题

模型生成结论时，判定还没发生，但输出格式可以先被约束：每个结论必须带依据，以及依据与本体的关系强度。这把「不能无根据」从规范变成机制。

## 四个接地等级

| 等级 | 含义 | 期望来源 |
|---|---|---|
| entailed | 答案可由观察里的事实逻辑推出 | formal reasoner / entailment |
| supported | 观察 + 参数知识可合理推断，但不是严格逻辑后承 | ontology-grounded |
| related | 观察相关，但不足以确定答案 | ontology-assisted |
| unrelated | 观察与问题/答案无关 | 有观察但无关；**不是「没检索到」** |

## OA-RAG 的实际做法

1. **Pre-tool reasoning**：先让 LLM 用参数知识分析问题。
2. **ReAct loop**：给 agent 一个 ontology tool；`DESCRIBE` 取 concept card，`ASK` 问 reasoner 是否 entailed（**Not Entailed ≠ false**，开放世界），`SELECT` 检索；精确查询空结果触发 BM25 fallback（取 top-k cards）。
3. **Answering**：过滤失败/空观察，得到 evidence digest；有证据用 `P_fin`，无证据用 `P_own`（**不报 grounding**）；只有 E≠∅ 时才走 `P_att` 报告引用的观察与 grounding level。

**名字链接也要能修**：精确匹配 → 多义候选 → 未知名字先用 BM25 取 200 个候选名、再按字符串相似度重排，给 5 个候选，agent 据此改 query；否则错名会被当成「本体里没有」（机制来自论文 §4.2.2 `已核`；后半句是推断，`推测`）。

**等级是模型自评**：不是独立判定器，也不是形式推导。作者明确写「does not provide a formal guarantee of answer correctness」。

## 接口与预算

> 接口原语、name linking、卡字段与交互预算上限来自论文正文/附录 A（`已核`）；截断长度、BM25 `k` 与超限处置是 digest §6.5 的工程设定（`推测`）。判断见 [findings F4–F8](./findings.md)。

| 项 | 设定 | 备注 |
|---|---|---|
| 卡字段 | `iri, label, definition, parents[], children[], relations[], comments[], source` | 单卡截断 1–2k 字符，避免多本体塞爆 |
| 三原语 | `DESCRIBE(iri)` / `ASK(s,p,o)` / `SELECT(query)` | ASK 返回 entailed / not entailed（论文正文）；unknown 见 digest §6.5，`推测` |
| 空结果兜底 | BM25 取 `k=5–10` cards | 不兜底 → 开放世界被误判「不存在」 |
| 名字链接 | 精确 → 多义候选 → 未知名字 BM25 取 200 候选池 → 相似度重排给 5 个 | 多义候选数论文未给；相似度阈值论文未给，固定并记录 |
| 交互预算（论文） | ≤10 tool actions；≤5,000 generated tokens（跨三阶段，Answer Step 2 另 512） | 实测均值 5.8 calls / 9.7k tokens（Qwen Test 3），不是上限；5k 是生成预算，不是总 token 上限 |
| 输出 | `{answer, observations[], grounding}` | observations 引用卡/ASK 结论/bindings；**无文本 span 规定** |

## 为什么仍然有用

- 把三种情况分开：**没有可用观察（E=∅，过滤后为空，不报等级，走 `P_own`）**、检索到但不足以定答案（`related`）、检索到但无关（`unrelated`）。
- 给答案一个可排序的可靠性字段；比纯文本 RAG 多一个可审计维度（可审计性来自字段设计，论文未把「可审计」单独量化，`推测`）。
- 文档写作层面的论点：格式强制能让无依据结论露馅；论文测的是准确率，没有测「强制格式」本身拦住了多少幻觉（`推测`）。

## 结果（OA-RAG，条件）

- 3 个本体（GO/FoodOn/SNOMED）、6 个医学 QA 任务、2 个 backbone。
- 平均准确率 50.5%（Llama）/ 68.1%（Qwen）；Tests 1–2 比最强基线 +10–15 pp。
- Test 3 同 8k context（Qwen）：84.9% vs 66.7%（i-MedRAGdoc）。
- 预算账另算：OA-RAG 8k 下 9.7k tokens / 5.8 calls；i-MedRAGdoc **262k** 下 96.7k / 22 calls——跨预算，不是同预算效率对照。
- grounding：entailed+supported 占 70.0%（Llama）/ 53.2%（Qwen）；unrelated 0.2% / 7.8%；部分答案没有 grounding 标注（论文举例：无证据可用），故占比不足 100%。
- Qwen Test 3：entailed 94.9% 正确、supported 82.1% 正确（切片，不是校准曲线）。
- 检索瓶颈：gold evidence 完全检索 61.7% MCQ vs 23.6% OQ。
- 不是单一变量：concept card、ReAct、fallback、answering step 都在变；去掉 answering step 平均掉 2.9–5.8 点。

> 预算口径 caveat：8,192 是全方法统一 context；262k 只给 i-MedRAGdoc(Qwen) 加报；32k 论文未测（digest 的「8k/32k/262k 结论不同」是外推，`推测`）。见 [findings F8](./findings.md)。

> 出处：Table 1/2/3、§6.1–6.3、Appendix A；OA-RAG digest §4、§5 第 6 条。

## 失效模式

- **等级自评**（`已核`）：模型给自己打分；作者写明不提供形式正确性保证。
- **等级未校准**（`已核`）：entailed/supported 的 precision/recall 未知；94.9/82.1 只是 Qwen Test 3 一个切片，不能当阈值依据。
- **等级通胀**（`推测`）：全标 supported，字段存在但无区分度；论文给了等级分布（entailed+supported 70.0%/53.2%，unrelated 0.2%/7.8%），但没测「通胀/校准」。
- **引用形式化**（`推测`）：引用了观察，但结论与观察无关；论文没有单独测量这类失败。
- **格式开销**（`推测`）：每条结论都带证据会增加输出 token；论文没有单列这项开销，且每问 9.7k tokens（Qwen Test 3）是含证据摘要的总账，看不出它是否拖累。
- **等级当形式证明**（`已核`）：作者自述无形式保证；把它写成「已验证」是最常见的误用。

## 与本体 / 回路的关系

本体在输出时以 **concept card / entailment / 注释** 出现；约束强度弱到中——能约束格式与声明，不能保证语义真值（`推测`：这是对约束强度的判断，论文只测了准确率与等级相关性）。被违反时通常没有自动信号，需要 checker/人审。

## 实施与客户价值（A3/A4）

### 实施决策

- 输出必须带证据 + grounding level；等级只做排序与人工分流，不能自动放行（`已核`：作者自述无形式保证；「用来排序/分流」是工程用法，`推测`）。
- 没有保留观察（E=∅）时走 `P_own`，不报 grounding，也不编造；`unrelated` 只用于「有观察但与问题/答案无关」。先修检索，不加推理层（`已核`：作者对 E=∅ 与检索瓶颈的表述）。
- 高等级（entailed）与低等级（related）可走不同审核路径（`推测`：等级未校准，分流阈值要自己标）。
- 替代方案：纯文本 RAG、只 ASK、只 concept card、人工审核；论文没有与这些同口径的成本-效果（digest §6.5）。

### 何时别用（前提不满足就别上）

> 第一条是方法依赖（`已核`）；其余条件来自 digest §6.3 与论文对前提/边界的表述，「因此别用」的选型判断是 `推测`。

- **没有 OWL reasoner / SPARQL endpoint。** `ASK`/`SELECT` 与 entailment closure 跑不起来；只剩 concept card，效果向普通文本 RAG 靠拢（论文的 service 建在 Whelk 预计算闭包 + Oxigraph 上；等价程度 `推测`）。
- **问题超出本体覆盖。** 未知 IRI 高时先补本体，否则等级只反映覆盖缺口（F6）。
- **答案主要靠文本阅读/计算。** 论文对 unrelated 的解释是：部分题主要依赖 reading comprehension 或 calculation，而不是本体推理；这类题不体现机制，等级也不可比（作者解释 `已核`；据此说「别用」是 `推测`）。
- **需要形式正确性保证。** 等级是模型自评，作者明确无形式保证（F2）；要形式保证直接用 reasoner，不要用这个输出契约。
- **多本体协调复杂。** 多本体是论文 future work；第二套 name linking、IRI 冲突未计（`推测`）。

- **LLM 不会写 SPARQL**：先验证 DESCRIBE/ASK/SELECT 三原语；写不出 query 时，检索率低不是覆盖问题，先补提示/示例/工具。
- **临床/生产使用**：论文没有真实病历/对话，也没有安全评估；本页的医学域只是 benchmark，不能当临床验证。

### 数据/接口

- 输出 `{answer, observations[], grounding: entailed|supported|related|unrelated}`（工程 schema，论文只规定内容不规定键名，`推测`）；**E=∅ 时没有 grounding 字段**（论文：部分答案缺 grounding 标注，故占比不足 100%）。
- `observations` 引用三类本体观察：`DESCRIBE` 的 concept card、`ASK` 的 entailed / not-entailed / unknown、`SELECT` 的 bindings。**论文没有规定文本 span 级定位**（卡是整卡引用）；句子级粒度是缺口，见 [frontier G3](./frontier.md)。
- 校准：每个 level 的 precision/recall 要独立标注；**样本量/工期论文未给**——不要沿用 [02/checker](../checker/mechanism.md) 的 100–400 条抽样（任务口径不同，`推测`）。
- 检索指标：gold evidence 检索率、引用率（论文口径）。
- 运行埋点：每次交互记 tool actions/generated tokens；按论文预算 ≤10 actions / ≤5,000 generated（Step 2 另 512）设闸（论文值 `已核`；超限 abstain/降级是工程处置，`推测`，见 [findings F5](./findings.md)）。

### 组织/成本

- 一次性：concept card 生成 1–2 人日/本体；reasoner/SPARQL 集成 1–2 人周（digest 工程估算，`推测`）。
- 运行：5.8 calls / 9.7k tokens 每问（Qwen Test 3；观察值，不是上限）。
- 维护：本体变更重生成 cards；grounding 校准的人工量未定，不要拍数。

### stop condition

> 阈值是 digest 工程门，论文未对这些门扫参；门背后的方向（检索是瓶颈、等级未校准）有论文支撑。

- 检索率 <50% → 先修检索，不做等级（「检索是主瓶颈」`已核`：作者结论；50% 是 digest 工程门，`推测`）。
- 未知 IRI >20% → 停，先补本体（工程门，`推测`）。
- tool actions >10 或 generated tokens >5,000（Step 2 另 512）→ 停/降级到纯 concept card 回答（论文预算 `已核`；降级处置是工程门，`推测`）。
- grounding 通胀（entailed+supported >90%）→ 抽样校准，不自动放行（工程门，`推测`）。
- 无独立标注 → 只做提示，不做自动路由/放行（`推测`）。

### 第一个 sprint

1 周、FoodOn 单本体（digest §6.5）：生成 concept cards（1–2k 字符/卡）→ 接 DESCRIBE/ASK/SELECT + 空结果 BM25 fallback → Test 1/2 各 200 题，记 gold evidence 检索率、引用率、calls/tokens → 与 RAGdoc 对照 → 预写 go/no-go：检索率 ≥50% 且引用率 ≥80% 才进第二阶段。不做 Test 3 全量、不做多本体协调。

### 客户价值（V1–V3，`推测`）

- **V1 受益者/痛点**：受益者是医学/生物本体问答产品（已有 OWL 本体、要答案可追溯）；痛点是答案无依据、术语歧义、检索不到，且检索失败与推理失败分不开，容易把「加推理层」当解法（前三条来自 digest §6.6；最后一条是检索瓶颈的工程推论，`推测`）。
- 指标：gold evidence 检索率、引用率、grounding 校准、每问 token/时延、人工复核率。
- 反事实：不做 → 纯文本 RAG；无 grounding 字段；先测检索率基线。
- V3：单本体 200 题；成功 = 检索率 ≥60%、引用率 ≥85%、准确率 ≥RAGdoc +10pp；失败 = 检索率 <50% 或 grounding 通胀；停止线 = 年省复核 < 维护成本。
- 反例：检索瓶颈；等级自评；本体覆盖不足；Test 3 只在 8k 同预算占优（262k 下 i-MedRAGdoc 仍有竞争力）；整包一起变、不是本体单变量。

## 关联

- [OA-RAG digest](../../../src/papers/2610.36335-oa-rag/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
- [checker](../checker/README.md)
