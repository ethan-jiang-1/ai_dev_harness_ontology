---
status: draft
updated: 2026-11-12
---

# 生成 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。
> 「工程发现 1–4」是从四条 digest 吸收的落地口径（接口/参数/成本/stop/客户指标），不是新增论文结论；本页新增的建议单独标 `推测`，digest 也没给的测算一律标 `推测`。
>
> **2026-11-12 对账**：本页四路线的来源 SFE-O / OntoDoc / ReX-GG / Peeling / Evontree 均已撤回。下列机制描述与数字作**历史/机制参考，不作活证据**；接口/参数/成本等工程口径本就是 digest 配方（`推测`）。生成路线的问题意识保留，证据待新源。

## 问题

多数本体文献默认本体已经存在；真实项目第一步往往是「造一个」。造法不止一种，每条路线的适用边界不同，跨路线的优劣排序目前没有同口径证据。

## 四条路线

| 路线 | 做法 | 代表 | 可核边界（digest 口径） |
|---|---|---|---|
| 专家手工 | 建模 + 工程账本（参数带来源/单位/条件） | SFE-O | 表达力够，瓶颈在执行/集成：数值不在 OWL 求解、约束未落 SHACL 只是文档、热物性/扩散系数靠外部服务、矛盾显式标记（不是「覆盖窄/维护贵」的证据） |
| LLM 生成 | 多 agent 流水线写说明；多模型 + JSON 抽关系 | OntoDoc、ReX-GG | OntoDoc 无下游、简单图 naive 更好；ReX 本体只当标签表（4 种关系）、单任务单语言、互评需人审 |
| 表征挖掘 | 冻结 MRL 嵌入 + 前缀探针解 DAG | Peeling | 只在 MRL 嵌入；零样本迁移只在目标不比源域更深时成立；无下游 |
| 规则引导自演化 | 模型生成本体树 → 规则闭合 → ConfirmValue 选 gap → 训练侧注入 | Evontree | 15 根概念人工种子；规则只覆盖 subclass/synonym；explicit 掉点、implicit/mix 报告有效；两模型单域自评；收益数字仅按报告值引用（+3.1/+3.7 与 +0.9/+1.1 均不可当净增益/相对百分比，表内不可复算，F6） |

「数据挖掘」常被列作第五种，但五条 digest 里没有独立案例（SFE-O 是域本体工程账本，不是挖掘方法）；本页不单列，也不给它编偏向。

## 证据：四篇各自怎么跑

> 下面很多参数/接口来自各 digest 的「工程配方（E3）」；标了「E3」的是工程建议，不是论文报告值，未标的才按 digest §3/§4 的论文口径读。

### OntoDoc：四阶段写 `rdfs:comment`

1. **DB Context Agent**：自适应 SPARQL 探索；5 个工具（digest 只列了 4 个名字：`get_iri_information`、outgoing/incoming、`predicate_usage`、`execute_sparql`）；预算 50 triples / 10 tool calls；四子阶段 Orient → Initial scan → Targeted follow-up → Summarize；class 实例少于 10 个就全取，并看 2–3 个实例属性。
2. **Web Context Agent**：从 IRI 提 label；Wikipedia + Tavily；Cohere Rerank 3.5，k=3，阈值 0.75。
3. **Assumption Generation**：输出 JSON `{items:[{reasoning, assumptions}]}`；DB context 权威，web 只补充；至少一条 assumption 必须引用 DB triple 编号。
4. **Description Generation**：lexicographer 角色；不直接命名 IRI；优先 instance-level、区分性事实。

**校验**：每条 canonical triple 用 SPARQL ASK 回验，不存在/不一致的丢弃，不进 assumption 层。
**失败路径（digest E3 建议）**：SPARQL 失败/空上下文 → 回退 web only + 人工，不编造；web 零命中 → 只用 DB；assumption 与 DB 冲突 → 标 conflict，不让描述层裁决；超时/超预算 → 跳过，不写半成品。

### ReX-GG：七模型 → JSON → 匿名互评 → HTML 图

- 七个模型独立抽关系，每条输出 JSON；聚合、去重后生成交互式 HTML 因果图，供人审。
- 本体只提供四种关系（strong / weak / contrast / composition），不参与判定——它是标签表，不是判据。
- **匿名互评**：候选匿名后由模型互评排序（digest §3 只报告到这一层）；k=3–5、1–5 分、中位数/Borda、分歧 >2 分转人审、去偏四件套是 §6.1 的 E3 建议口径（`推测`）。

### Peeling：冻结嵌入 + order-embedding 探针

- **参数（digest E3 建议）**：嵌入 Nomic-embed-text-v1.5（768 维）冻结；wiki-ol 8,033 概念/14,673 边；arXiv-ol 61 类；探针 768→128 线性 + ReLU；margin 4.0；Adam lr 5e-4、batch 512、10 epoch；前缀 d∈{64,128,256,384,512,768}。
- **解码/输出（E3 建议）**：Chu-Liu/Edmonds 最大生成树 → DAG；输出 `{child, parent, confidence}`；对照 = 维度打乱/逆序，确认信号来自前缀顺序而不是模型容量。
- **下游召回**：digest 的 sprint 出口要求「挂一个层级检索下游（parent/child 扩展），看召回是否提升」；Graph F1 ≥0.85 且下游有增益才算成立。论文本身**没有测**下游（§5.3），所以这条是工程闸门，不是论文结果。

### Evontree：本体树 → 规则闭合 → gap → 训练侧注入

- 人工给定 15 个根概念；prompt 生成深度 ≥3 的 JSON 本体树；约 1 万条 raw 三元组用于定阈值。
- `ConfirmValue(t,p) = sign(PPL_False − PPL_True) / min(PPL_True, PPL_False)`；synonym 用 5 个改写 prompt、subclass 用 4 个；所有 prompt 都超过 τ\* 才算 confirmed。
- τ\*：每个模型×prompt 在 [0,1] 扫，最大化 Youden `J=TPR−FPR`。
- 两条规则：subclass 传递、synonym 三角闭合；闭合后 reliable，再向外传递外推得 extrapolated；只保留 `ConfirmValue < τ*` 的 gap。
- 统计（Table 2）：raw synonym 95,814 / subclass 58,309；confirmed 30,532 / 24,276；reliable subclass 14,169；extrapolated 8,661；**gap subclass 只有 1,396 条**（ConfirmValue 均值 0.1595，准确率 74.57，而 confirmed subclass 是 0.4896/72.62）——「事实对、模型不确定」；论文的解读是增益来自选得准，不是加得多（增益本身仅报告值，见下条）。
- 注入：implicit（自蒸馏 Q&A）/ explicit（模板 Q&A）/ mix；LoRA lr 5e-5、3 epoch、fp32、cosine、bs 8、grad accum 2（LLaMAFactory）。
- **结果（§4.2，仅按报告值引用）**：论文报告 Llama3-8B-Evontree(mix) +3.1%、Med42-v2-Evontree(implicit) +3.7%（三个医疗 QA 基准平均），并称相对最强 baseline 为 +0.9/+1.1。**表内均值与 Δ 行不可复算**：Table 3 的 Llama3 raw 62.5 vs mix 61.0 与 +3.1% 对不上，+0.9/+1.1 也是同表绝对分差、不是相对百分比；四个数字都不得当净增益或相对百分比——不要用 +0.9/+1.1 代替 +3.1/+3.7 当「保守净收益」。gap 只有 1,396 条。
- **安全/通用能力（§4.3）**：implicit/mix 没有显著安全下降；通用能力（MMLU/TriviaQA/ARC）平均只降 0.15%，部分还升。掉点的是 explicit：Llama3 Jailbreak Safe 96.35→83.65、Med42 60.19→45.19。

## 核心判断

**生成产出的是候选，不是「完备本体」。** 四篇能证明「能生成可读、部分正确的结构」（OntoDoc 3.43→3.84；ReX 感知准确率 0.778；Peeling Graph F1 0.885/0.931；Evontree 报告 +3.1/+3.7 与 +0.9/+1.1，仅报告值、不可当净增益），不能证明「能被下游判定器直接消费」——四篇都没测。两者之间隔着「可消费性」评估，目前缺（F1/F3）。

**OntoDoc 的可迁移设计**：先写 assumptions（reasoning + triple 引用）再写描述；DB context 权威、web 只补充；自适应 SPARQL 探索而非单跳查询；失败路径显式化（宁可跳过，不写半成品）。

## 失效模式

- **没有下游消费证据。** 四篇都没让判定器/agent 真正加载并完成任务；completeness、用户感知、Graph F1、held-out 增益都不能替代「可消费」（F1/F3）。
- **结构分数 ≠ 语义真值。** Peeling 的 Graph F1 0.885/0.931 只说明抽出的 DAG 与金标结构接近，不说明每个类定义正确。
- **模板式注入掉点，implicit/mix 未报告显著掉点。** Evontree explicit：Llama3 平均 56.1 vs raw 62.5，Jailbreak Safe 96.35→83.65；Med42 62.3 vs 63.5，60.19→45.19。implicit/mix 没有显著安全下降，通用能力平均只降 0.15%。注入口径比注入量更关键（F6）。
- **简单域上复杂流水线过度加工。** DBpedia 上 naive accuracy 4.30 vs 4.20、clarity 4.73 vs 4.47。
- **假设层是不可逆瓶颈（作者自述）。** OntoDoc 漏掉的关键细节后面拿不回来；重写 prompt 会丢 assumptions 层前提，复刻只能到「看起来像」。
- **生成者身份不进判定权重。** 流程里有证据痕迹（OntoDoc 的 assumption 引用 DB triple 编号、ReX 互评匿名化、Evontree 的 `ConfirmValue` 分级），但 `provenance_triples`/`generator_version`/`evidence_span` 是 digest E3 建议 schema（`推测`），不是论文报告的产物字段；也没有一篇测过按来源加权会不会减少误判（F5）。
- **两条常被引用的「失效」在 digest 里没有测量**：「LLM 语义漂移/关系方向易错」「把常见当应然」。前者只能追到 ReX 对「关系类型混乱」的问题陈述（工程观察，不是本体级测量），后者见 [frontier G5](./frontier.md)；二者均按 `推测` 处理，不写进依据。

## 与本体 / 回路的关系

本体在生成阶段是 **产物**；约束强度取决于生成后的校验。生成物的错误通常没有即时信号——说明写歪、DAG 边错、三元组不可靠，都要等 checker 加载或人审才暴露。这一点是 `推测`（四篇均未抓运行期信号）。

## 实施与客户价值（A3/A4）

> 本节回答「改变哪个实施决策、客户哪个指标会动、怎么验证」。数字出自四条 digest（[OntoDoc](../../../meta/audits/2026-11-11-source-purge.md#src-2611-01276) / [ReX-GG](../../../meta/audits/2026-11-11-source-purge.md#src-2610-41901) / [Peeling](../../../meta/audits/2026-11-11-source-purge.md#src-2610-41785) / [Evontree](../../../meta/audits/2026-11-11-source-purge.md#src-2510-26683)）；digest 没给的成本/比例标 `推测`。

### 实施决策

- **先定消费位置，再选生成路线。** 要人读的说明 → LLM 四阶段（assumptions + ASK 回验）；要短文本关系 → 结构化 JSON + 匿名互评；要层级候选 → 嵌入探针（仅 MRL 嵌入、目标不比源域更深时成立）；要改模型行为 → 训练侧自蒸馏，不当运行时约束。按产物怎么被消费选，不按「哪个更先进」排序。
- **发布闸门用可消费性，不用 completeness。** 四篇证据只到「可读、部分正确」（F1/F3）；生成物先被下游判定器/检索加载一次，再允许进本体。description completeness 从发布依据降为内部质量指标。（本页建议，四条路线都没做，`推测`）
- **assumptions 中间层与最终文本一同落盘。** 只存最终描述 = 不可审计、无法解释重跑差异；OntoDoc 的 win 54–61% 是 assumptions 层消融（Table 4，LLM judge）的结果，重写 prompt 会丢掉这层前提。
- **来源字段随生成物入库，但先别串进判定。** digest E3 建议的 `provenance_triples[] + generator_version`、`evidence_span`、`ConfirmValue/reliable/gap` 可以先记录（`推测`，论文未报告这些字段名）；`source`（expert/llm/mining）作为附加字段。F5：没有一篇测过按来源加权，先并联记录、不进判定权重（`推测`）。
- **不做一次性全量生成。** 按域/术语类型分批，每批过闸门再扩。**增量重生成只有 OntoDoc 明确写「未实现」**；其余三篇未报告增量机制（未报道 ≠ 已证不可行，见 frontier G6）。

### 工程发现 1｜接口：输入什么、落什么

> **schema 的来源**：下面的字段是 digest 的 E3 建议（OntoDoc §6.5、ReX-GG §6.1、Peeling/Evontree §6）加本页整理；四篇论文都没有报告带来源权重的成品 schema，E3 字段名一律按工程建议读（`推测`），不要当论文产物或已核字段。

- **输入**：`iri_list` + SPARQL endpoint/本体文件 + 实例数据 + 网页检索（可缺）+ 冻结嵌入（仅表征挖掘）。没有实例数据就不走 LLM 路线（OntoDoc 的实例语义靠数据），退模板 verbalizer 或人工。
- **说明产物**：`{iri, description, lang, provenance_triples[], generator_version, reviewed_by, generated_at}`，落库为 `rdfs:comment` + 语言标签。
- **关系产物**：`{cause, effect, relation: strong|weak|contrast|composition, confidence, evidence_span}`；没有 `evidence_span` 的条目丢弃。
- **层级产物**：`{child, parent, confidence}`（Chu-Liu/Edmonds 解码输出）。
- **自演化产物**：`(head, relation, tail, ConfirmValue, reliable, gap)`。
- **批处理**：`generate(iri_list, endpoint, config)`；幂等键 `(iri, ontology_version, generator_version)`；自演化 `extract(root_concepts, depth≥3) → confirm(triples, prompts) → close_rules → select_gap(τ*) → inject(gap, mode=implicit|mix)`。
<a id="可消费性闸门"></a>

- **可消费性闸门（本页新增，四条路线均未做，`推测`）**：`load(artifact) → {parsed, violations, missing_fields}` + 一次真实任务（checker 加载判定 / 层级检索 / agent 消费），记成功/失败与失败原因。
- **日志**：每 IRI 记路线、token、检索命中、ASK 结果、人审结论；没有日志算不出每术语成本与 reject 率。

### 工程发现 2｜参数：能抄的是条件，不是值

| 路线 | digest 给的可抄参数 | 换域时必须重标 |
|---|---|---|
| OntoDoc | DB：5 个工具（digest 列名 4 个）、50 triples / 10 tool calls、四子阶段；class 实例 <10 全取；Web：Wikipedia+Tavily、Cohere Rerank 3.5 k=3 τ=0.75；每条 assumption 至少 1 条 DB triple；生成 gpt-4.1-mini、判分 kimi-k2.5 | tool 预算、rerank 阈值、判分模型与 prompt |
| ReX-GG | 7 模型；匿名互评（E3 建议：k=3–5、1–5 分、中位数/Borda、分歧 >2 分转人审；去偏=随机顺序+隐藏模型名+不自评+双向顺序） | 关系 schema（本文 4 种）、k、分歧阈值 |
| Peeling | （E3 参数）Nomic-embed-text-v1.5 768 冻结；探针 768→128 + ReLU、margin 4.0、Adam lr 5e-4、bs 512、10 epoch；d∈{64,128,256,384,512,768}；Chu-Liu/Edmonds 解码 | 嵌入族（参数只在 MRL 上验证）、源/目标深度、d 网格 |
| Evontree | 15 根概念、深度 ≥3；synonym 5 个 / subclass 4 个改写 prompt；τ\* 用 Youden 扫；LoRA lr 5e-5、3 epoch、fp32、cosine、bs 8、grad accum 2 | 根概念、τ\*（每模型×prompt 单独定）、关系类型 |

- **参数不是常量。** 上表多数是论文设置，标 E3 的是 digest 工程建议（ReX 互评、Peeling 探针超参）；跨域照搬阈值（尤其 τ\*、rerank 0.75、k）会改判定行为，需要在自己的抽检集上重扫。
- **prompt 是资产。** OntoDoc 的假设层收益绑定在这套四阶段 prompt 上（win 54–61%）；重写 prompt 会丢掉 assumptions 层前提，复刻只能到「看起来像」。
- **互评排序不是放行证据。** ReX 的 k、Borda、去偏（E3 建议）只能把候选排好序，仍需人工 precision 才谈自动放行。

来源：[OntoDoc digest](../../../meta/audits/2026-11-11-source-purge.md#src-2611-01276) · [ReX-GG digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-41901) · [Peeling digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-41785) · [Evontree digest](../../../meta/audits/2026-11-11-source-purge.md#src-2510-26683)

### 工程发现 3｜成本：四篇都没有金额

- **owner**：本体/知识工程 owner（口径、闸门；1 人，`推测`）+ 平台工程（SPARQL/检索/批处理；1 人，`推测`）+ 领域专家（按域抽检）。
- **人日**（digest E3 的工程估算，均 `推测`）：OntoDoc setup 1–2 人周、人审抽检 10–20% 且每条 2–5 分钟、维护 0.5–1 人日/月；ReX 人工标 100 条约 1–2 人日；Peeling 金标 taxonomy 校验 1–2 人日；Evontree 15 根概念 + 规则/τ\* 复核 2–3 人日。
- **运行成本**（论文无金额，只给规模；分钟–小时级为 `推测`）：OntoDoc 每 IRI 4 个 agent 调用 + 检索；ReX 50 篇 × 7 模型 + 互评 k=3 × 候选数（50 篇/k 为 digest E3 设定）；Peeling 8,033 概念嵌入单卡分钟级、探针 10 epoch 分钟–小时；Evontree 抽本体 15 根 × 深度 3 约 1–3 小时 GPU、1,396 gap × 3 epoch LoRA 数小时–1 天。
- **金额**：四篇都没给。要报价先测自己的 token/GPU 单价，不套别人的数字。
- **维护**：OntoDoc 明确未实现增量重生成；其余三篇未报告。0.5–1 人日/月只是 OntoDoc 的工程估算（`推测`），不要当四条路线的通用值。
- **决策口径（OntoDoc digest E4，工程建议，`推测`；digest 未给金额，也不是论文测算）**：`TCO = N × 每 IRI 成本 + setup + 12 × 月维护`。N 为术语数；每 IRI 成本含 token/检索/4 个 agent + 人审 10–20%；setup 1–2 人周、月维护 0.5–1 人日（digest E3 估算，`推测`）。替代项要列全：build（四阶段）/ buy（商业本体文档工具）/ 通用 LLM 批量 / 人工写 / do nothing。TCO 只用自己测的 token/GPU 单价，不套论文（四篇都无金额）。

### 工程发现 4｜stop 与客户指标

#### stop condition（按路线）

> 这些停线来自各 digest 的 E3 工程配方，不是论文报告的门槛；一律按 `推测` 用，需在自己的数据上校准。

| 路线 | 停线 | 来源 |
|---|---|---|
| OntoDoc | 人审 reject >20% 或 accuracy <4.0/5 → 不发；SPARQL 失败/超预算 → 跳过，不写半成品 | OntoDoc digest §6.5 |
| ReX-GG | reviewer α（Krippendorff）<0.6；人工 100 条 precision <0.7；七模型成本 > 单模型+人审 2×；下游无法消费 → 只做可视化 | ReX digest §6.1 |
| Peeling | Graph F1 <0.85；打乱/逆序对照无差异；目标本体比源域更深；DAG 无法被下游加载 → 只做结构分析 | Peeling digest §6.1 |
| Evontree | 规则覆盖率 <50%；gap <500 条或 confirmed/gap 区分不显著；held-out 增益 <1pp；explicit 安全面掉 >5pp | Evontree digest §6 |
| 通用（本页） | 生成 + 人审 > 人工撰写同量术语 → 不做（`推测`，需先测人工基线） | — |

#### 客户指标/V3（按路线）

- **受益者**：本体/知识图谱团队（维护者）、新用户/集成方（读者）、下游 agent/checker 开发者（消费者）。痛点：术语缺说明、上手慢、集成错误。
- **指标（按路线分开，不要拼成一个数）**：
  - **OntoDoc**：找术语时间、集成错误率、人工撰写工时/术语、description completeness/accuracy、reject 率、每 IRI 成本。**收益口径（digest E4，`推测`）**：`收益 = 撰写工时下降 × 工时价 + 集成错误率下降 × 修复成本`；先测当前人工撰写工时/术语。决策线 `NPV_build > max(NPV_buy, 0)`，且 completeness +0.3、人工 accuracy ≥4.0；buy 按商业工具报价 + 集成人周算，商业工具覆盖 <70% 术语类型则不买。
  - **ReX-GG**：人工 precision/recall、互评一致性 α、感知准确率 0.778（用户研究，摘要级）、单篇成本。
  - **Peeling**：Graph F1 + 层级检索召回（sprint 出口要求「下游有增益」）；**没有客户指标**——因为它没测下游。
  - **Evontree**：held-out 准确率、安全面（Jailbreak Safe）、标注/训练成本、专家复核工时。
- **反事实**：OntoDoc 不生成 → 人工写或空着（先测当前人工工时/术语）；只跑 naive → 简单图上 accuracy/clarity 更高；ReX 单模型+人审 → 成本更低，幻觉是否更多论文没测（`推测`）；Peeling 不抽 → 手工建或 LLM 抽；Evontree 不注入 → 直接 SFT/RAG。
- **V3 试点（只有两篇给了可抄的成功线）**：
  - OntoDoc：40 术语、naive vs 四阶段；成功 = completeness +0.3、人工 accuracy ≥4.0、成本 ≤ 人工撰写 1/3（`推测`，需先测人工基线）、下游能加载并完成一次任务。
  - Evontree：单域、Llama3-8B、1,396 gap；成功 = held-out +≥1pp、安全掉点 ≤2pp、成本 < 人工标同量数据。
- **失败/停止线**：OntoDoc completeness 无提升或成本超人工 → 降级为「只生成草稿」；Evontree 增益 <1pp 或安全掉点 >5pp → 停；ReX precision <0.7 或 α <0.6 → 停；Peeling 下游无增益 → 停。
- **级别**：A3+ / V3（试点设计可执行）。只有 OntoDoc/Evontree 到了 V3 形态；ReX 有感知准确率但无价值测算；Peeling 无下游，客户价值只能到 V1/V2。所有金额/工时基线与价值陈述均 `推测`，不进 deliverables。

### 第一个 sprint

2 周、单域单语言、只跑 LLM 路线（四阶段）与 naive 基线；表征挖掘/自演化消费位置不同，另立 sprint（Peeling 1 周、Evontree 2 周，见各自 digest），不混做。

1. 取 40 个缺 `rdfs:comment` 的术语（20 class / 10 property / 10 instance），先跑 naive 单跳基线。
2. 四阶段：共享 state `database_context → web_context → assumptions → description`；每条 canonical triple 用 SPARQL ASK 回验；assumptions JSON 落盘。
3. 产物按 digest E3 建议 schema 落库（含 `provenance_triples`、`generator_version`；`推测`，论文未给这些字段名），幂等重跑不重复写。
4. 评测：四维 rubric + 20 条人工盲评（naive vs 四阶段）；记每 IRI token / 分钟 / 美元。
5. 可消费性抽查：把描述与结构给下游 checker 或检索加载一次，记 `load` 结果与一次任务成败。
6. **交付物**：40 条带 triple 引用与 assumptions 的描述；naive vs 四阶段四维对比表；每 IRI 成本表；可消费性记录；build/buy/不做 memo。
7. **出口**：completeness 相对 naive ≥+0.3、人工 accuracy ≥4.0、每 IRI 成本在预设上限内，且下游至少完成一次加载 + 一次真实任务（比例阈值待校准，`推测`）。不达标即停在该路线，不写入本体。

### 反例

- **naive 可能更好。** DBpedia 上 naive accuracy 4.30 vs 4.20、clarity 4.73 vs 4.47；简单本体上四阶段是过度加工。
- **质量提升不等于可消费。** 四篇都没测下游任务；completeness 与用户感知 0.778 都不能证明 checker 能加载。
- **结构分数不等于语义正确。** Peeling 的 Graph F1 只衡量 DAG 与金标结构的接近程度。
- **自演化的硬反例。** Evontree explicit 模板注入平均分低于 raw（Llama3 56.1 vs 62.5），安全面 96.35→83.65；implicit/mix 报告有效（增益仅报告值，表内不可复算，F6）。把「本体注入」笼统当有效或笼统当有害都会错。
- **假设层是不可逆瓶颈。** OntoDoc 假设层漏掉的关键事实后面拿不回来（作者自述）；重写 prompt 即丢前提。
- **变更频率可能吃掉收益。** 增量重生成只有 OntoDoc 明确未实现，其余未报道；频繁变更时维护成本可能吃掉全部节省（`推测`，无增量成本数据）。

## 关联

- [OntoDoc digest](../../../meta/audits/2026-11-11-source-purge.md#src-2611-01276)
- [ReX-GG digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-41901)
- [Peeling digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-41785)
- [Evontree digest](../../../meta/audits/2026-11-11-source-purge.md#src-2510-26683)
- [findings](./findings.md) · [frontier](./frontier.md)
