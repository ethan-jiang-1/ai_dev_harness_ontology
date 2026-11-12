# 输出时证据契约 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `evidence/Fx`。F1–F3 是论文可测结论；F4–F7 是「照它复刻要固定什么」的工程条目——接口存在性与论文给的预算上限 `已核`，参数取值与工期标 `推测`（来自 digest 工程配方，非论文测量）；F8 是论文对比口径的 caveat。

## 索引
> **2026-11-12 对账（等级以 README 为准）**：本页索引里的「已核」是**撤源前**的记录；支撑它的来源已按 [CHARTER §4](../../../CHARTER.md#4-素材准入material-gate) 移出，这些条目现等级见 [README](./README.md)（多已降 `推测`/`withdrawn`）。**引用请用 README 的等级，不要用本页索引的历史等级。**


| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 强制报告本体观察 + 接地等级，平均优于文本 RAG；有 cell 级例外 | 已核 |
| F2 | 等级是模型自评，不是形式保证 | 已核 |
| F3 | 检索是主瓶颈；不是「接地等级不够」 | 已核 |
| F4 | 复刻接口 = 三查询原语 + 固定字段卡 + name linking/fallback | 接口 `已核`；参数取值 `推测` |
| F5 | 预算：≤10 tool actions、≤5,000 generated tokens（Step 2 另 512）；5.8 calls/9.7k 是观察值不是上限 | 论文值 `已核`；闸门处置 `推测` |
| F6 | 覆盖闸先于效果：未知 IRI >20% 停；检索率 <50% 先修检索 | 工程门 `推测` |
| F7 | 成本：1–2 人日/本体、1–2 人周 reasoner 集成；grounding 校准工期论文未给 | `推测` |
| F8 | 预算口径：8,192 全方法统一；262k 仅 i-MedRAGdoc(Qwen)；32k 未测 | 口径 `已核`；32k 外推 `推测` |

## F1 · 显式接地整体最优

- **判断**：每个答案报告本体观察 + grounding level，在三个本体、六个医学 QA 任务上平均最优。**不是每个 cell 都最优**：Test 2 MCQ Llama 52.2 vs RAGont(text) 53.4；Test 2 OQ Qwen 23.2 vs ReActont 32.9。
- **数字**：平均 50.5%（Llama）/ 68.1%（Qwen）；Tests 1–2 比最强基线 +10–15 pp（Llama 44.3 vs 28.9；Qwen 59.7 vs 49.7）；Test 3 同 8k 84.9% vs 66.7%。
- **条件**：GO/FoodOn/SNOMED；Llama-3-8B/Qwen3.5-9B；8k context 对比。
- **边界**：三个本体都是生物医学；grounding 自评；整包（concept card + ReAct + fallback + answering）一起变，不是「本体」单一变量；跨域未测；token/call 对比跨 8k/262k 预算（F8）。
- **来源**：Table 1–3；§6.2；digest §4.2、§5 第 6 条。

## F2 · 等级是自评

- **判断**：grounding level 由模型自己报告，不是独立判定器/形式推导；作者明确不提供形式保证。
- **数字**：entailed+supported 占 70.0%/53.2%；unrelated 0.2%/7.8%；Qwen Test 3 entailed 94.9% / supported 82.1%（单个切片，不是校准曲线）。
- **含义**：等级与正确率同向，但不能当自动放行依据；必须保留「自评」限定。
- **来源**：§4.1.3、§6.2；摘要/结论；digest §4.3。

## F3 · 检索瓶颈

- **判断**：gold evidence 完全检索率 MCQ 61.7% vs OQ 23.6%；检索到后 MCQ 95.1–98.4% 被引用（OQ 更低）。
- **含义**：提升应优先修检索/覆盖，不是加更多推理层（作者原话：retrieval, rather than reasoning over retrieved evidence, is the primary bottleneck）。
- **来源**：§6.3.1；Figure 4；digest §4.4。

## F4 · 复刻接口：三原语 + 固定字段卡

- **判断**：agent 只做三种动作——`DESCRIBE(iri)` 取 concept card；`ASK(s,p,o)` 问 reasoner 是否 entailed（论文正文两值：entailed / not entailed；digest §6.5 多一个 unknown，`推测`）；`SELECT(query)` 取 bindings。精确查询空结果时对 concept cards 做 BM25，取 top-k 候选概念（k 值论文未给）。名字链接三档：精确匹配 → 多义候选 → 未知名字先用 BM25 取 200 候选池、再按字符串相似度重排，给 5 个候选，让 agent 改 query（论文 §4.2.2）。
- **卡字段**：`iri, label, definition, parents[], children[], relations[], comments[], source`（digest §6.5；原文 §4.2.1 为 name/definition/parents/children/stated relations/comments/annotations）。
- **参数（工程配方，非论文测量，`推测`）**：单卡截断 1–2k 字符；BM25 fallback `k=5–10` cards；相似度阈值原文未给——固定并记录，不要一边调阈值一边报效果。
- **条件**：开放世界口径必须写进 prompt（`Not Entailed ≠ false`），否则空结果会被当成「不存在」。
- **边界**：这是接口最小集，不改善 grounding 可靠性；卡质量（字段缺、注释空）是未测量变量。
- **来源**：digest §3.2、§6.5；原文 §4.1.2、§4.2。

## F5 · 交互预算：论文给上限，5.8/9.7k 是观察值

- **判断**：论文给每次交互的硬预算——≤10 tool actions；≤5,000 generated tokens，跨 pre-tool reasoning + ReAct + Answering Step 1；Answering Step 2 另 512 tokens（Appendix A）。到预算即终止；超限后是 abstain、降级还是强制作答，论文定义 limit reached → 强制作答（LLM answering）（`推测`）。5,000 generated 是论文值；digest §6.5 的 `max_total_tokens=12k` 是工程总 token 闸（`推测`），不是同一量，也不与论文冲突。stop 保留两者。
- **数字**：Qwen Test 3 实测平均 5.8 LLM calls / 9.7k tokens 每问（7.9k input，其中 1.0k 来自本体观察；1.8k generated）。注意口径：5.8 是 LLM calls/问；Figure 6 的 tool calls 是另一回事（Qwen Test 3 平均 2.0/问）。对照组 i-MedRAGdoc(262k) 是 22 calls / 96.7k tokens——那是 262k 设置，不是 8k 同预算（F8）。这些均值是**观察值，不是允许上限**；把它当上限会误杀多跳题（`推测`）。
- **条件**：8,192 context 是全方法统一口径；5,000 是 generated tokens 的预算，不是总 token 上限（总 token 9.7k 已含 7.9k 输入）。
- **边界**：设太紧 → 多跳题被误判「证据不足」；设太松 → 等于没闸（`推测`）。论文给值但未做预算敏感性扫描。
- **来源**：Appendix A「Agent and service」「Cost」「Tool calls」；§6.2；digest §4.2、§6.5。

## F6 · 覆盖闸：先决定「能不能用」

- **判断**：三条门在调效果之前先跑：① gold evidence 完全检索率 <50% → 先修检索，不加推理层；② 未知 IRI >20% → 停，先补本体；③ entailed+supported >90% → 抽样校准，不自动放行。
- **数字**：检索率基线来自论文（MCQ 61.7%、OQ 23.6%）；20% 与 90% 是 digest 给的工程阈值，论文未给。
- **含义**：这三条把「本体没覆盖」与「模型推理不行」分开；否则会把覆盖问题误诊成推理问题，越调越差。
- **边界**：未知 IRI 比例要先埋点（name linking 失败率）；没有这个数，20% 就只是口号（`推测`）。
- **来源**：digest §4.4、§6.5；原文 §6.3.1。

## F7 · 成本：一次性集成 + 每问调用

- **判断**：成本分两块——一次性（concept cards + reasoner/SPARQL 接入）与每次（5.8 calls / 9.7k tokens 每问，Qwen Test 3；本体变更重生成 cards）。
- **数字（`推测`）**：concept card 生成 1–2 人日/本体；reasoner/SPARQL 集成 1–2 人周。两项都是 digest 的工程估算，论文未测；**这是 card/集成成本，不是标注成本**，不能挪去当 grounding 校准成本。
- **未给**：grounding 校准的人工样本量与工期，论文与 digest 都没有——不要写「100–400 条 × 1–2 人日」。
- **边界**：单本体一次性的账；多本体协调（第二套 name linking、IRI 冲突）未计。
- **来源**：digest §6.5「成本」；Appendix A「Cost」运行观察值。

## F8 · 预算口径：8k 主比较，262k 只加报，32k 未测

- **判断**：论文主结果是 8,192-token context 下所有方法同口径（匹配 Llama 上限）；262k 只用于 i-MedRAGdoc 在 Qwen 上的加报；32k 论文没有实测。
- **数字**：同 8k 下 Test 3（Qwen）OA-RAG 84.9% vs i-MedRAGdoc 66.7%；96.7k tokens / 22 calls 来自 262k 设置（Appendix A），不是 8k 对照。262k 下 i-MedRAGdoc 的 Test 3 分项仍接近 OA-RAG（Table 1），所以「token 省 10×」不等于「同预算更强」。
- **含义**：跨预算比 token/call 只能说明长上下文方案更贵；同预算只能比准确率。把 96.7k/22 calls 写成 8k 对照，是把两个口径拼在一起。
- **边界**：digest 提「8k/32k/262k 下结论不同」，但 32k 无实测数字——属外推（`推测`），不能当论文结论；8k 也只是 Llama 上限、不是任务最优预算（`推测`）。
- **来源**：§6.1（context 设置）、§6.2（token/call 对比）；Appendix A Cost；Table 1；digest §5 第 3 条、§6.1 第 8 条。
