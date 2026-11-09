# 生成 · 发现（F）

> 只放**已经能站住**的判断。每条带等级、条件、反例/边界、来源。
> `F` 编号是子主题局部编号；跨页引用写 `generation/Fx`。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 四篇都没有交付「下游能直接消费」的本体；生成物只能算候选 | 推测（「四篇均未测下游」已核） |
| F2 | 先写 assumptions 再写描述：completeness 3.43→3.84、win 54–61%（LLM judge） | 已核（限 OntoDoc） |
| F3 | 可消费性（加载/解释/复现）四条路线都没测，是 05 的核心空缺 | 已核（缺口，限四篇） |
| F4 | 四条路线各有可核边界；跨路线的「偏向排序」没有实证 | 分项 已核；排序 推测 |
| F5 | 来源字段是 E3 建议，不是论文产物；生成者身份没有进判定权重 | 已核（流程痕迹）/ 推测（schema、效果） |
| F6 | Evontree：explicit 掉点可核；论文报告 implicit/mix 有增益，但表内均值与 Δ 行不可复算，+3.1/+3.7 与 +0.9/+1.1 都不得当净增益/相对百分比 | explicit 掉点 已核（报告均值，限 Evontree）；implicit/mix 增益 `存疑`（仅报告值） |
| F7 | 生成物→可执行约束的消费路径已有开源实现（semantica：ontology → SHACL → pyshacl）；但生成形状的正确性/覆盖未测 | 已核（代码 + 最小运行） |

## 怎么读

- 想看**四条路线怎么跑、参数/接口/成本/stop/客户指标**：去 [mechanism](./mechanism.md) 的「工程发现 1–4」。
- 想看**缺什么、下一步**：去 [frontier](./frontier.md)。

## F1 · 候选，不是完备本体

- **判断**：生成物只到「可读、部分正确」；没有一篇证明它能被判定器/agent 直接消费。
- **已核（限四篇）**：OntoDoc 只测描述四维（LLM judge + 11 人评估）；ReX-GG 只测用户感知准确率 0.778（摘要级）；Peeling 只测 DAG 的 Graph F1；Evontree 的产物是训练数据（本体树 + 三元组），没有下游加载测试。
- **推测**：「生成产出候选，不是完备本体」是类别判断——「完备」没有操作定义，四篇也没打算交付完整本体。
- **反例/边界**：没有下游任务不等于生成物没用（F2 有 completeness 提升）；可消费性也没有统一评测口径。
- **来源**：OntoDoc digest §4/§5；ReX-GG digest §4.1/§5；Peeling digest §4.1/§5；Evontree digest §5。

## F2 · assumptions 层

- **数字（LLM judge）**：假设阶段 win rate DBpedia 57% / BioBricks 61% / SOCKG 54%；completeness 平均 3.43→3.84（5 分制）；模板 verbalizer 1.20–3.18。
- **条件**：151 terms、3 KGs、11 annotators；无下游任务。LLM judge 做了两类评测：分别和 naive（Table 5）、模板 verbalizer（Table 6）对比打分，以及 assumptions 有/无的强制二选一（Table 4，win 54–61%）；win rate 是 LLM judge 的偏好，不是人工。人工 11 人只评 OntoDoc 输出的绝对分（Table 7），没有 baseline 盲评。
- **反例**：DBpedia 上 naive 的 accuracy 4.30 vs 4.20、clarity 4.73 vs 4.47——简单图上四阶段是过度加工。
- **边界**：假设层是语义瓶颈、漏掉的关键细节后面拿不回来——这是作者对 tradeoff 的自述（digest §4.3/§5.6），不是测量。
- **来源**：OntoDoc digest Table 4/5/6/7；§4.1/§4.2/§4.3；§5.6。

## F3 · 可消费性缺口

- **判断**：判定器能否加载/解释/复现生成结构，四条路线都没有测。
- **含义**：生成质量 ≠ 可消费性；「加载成功」与「一次真实任务成功」两个口径都缺。
- **范围**：只对四条路线/四篇 digest 成立，不外推到整个生成文献。
- **来源**：各 digest 的「这些数字不能说明什么」：OntoDoc §5.1、ReX-GG §5.3、Peeling §5.3；Evontree 产物是训练数据、不是给判定器加载的结构（§5.1）。

## F4 · 路线边界可核，偏向排序不可核

- **判断**：四条路线各有 digest 明确写出的适用边界（汇总见 [mechanism 的四条路线表](./mechanism.md)）；**没有一篇做跨路线同口径比较**，所以「专家覆盖窄/维护贵、LLM 语义漂移、数据挖掘把常见当应然」这类排序是 `推测`，不作依据引用。
- **已核分项**：
  - **专家手工（SFE-O）**：SFE-O 不是生成方法论文，是域本体工程账本；它写的是「表达力够，瓶颈在执行/集成」——OWL 2 不做数值求解、约束没落成 SHACL 就只是文档、热物性/扩散系数靠外部服务、数据矛盾只能显式标记（SFE-O digest §0/§4.1/§5）。
  - **LLM（OntoDoc / ReX-GG）**：OntoDoc 无下游、简单图 naive accuracy/clarity 更高；ReX 本体只当标签表（四种关系）、不参与判定、单任务单语言、互评仍需人审（OntoDoc §5；ReX §4.1/§5）。
  - **表征挖掘（Peeling）**：只在 MRL 嵌入上成立；零样本迁移只在「目标不比源域更深」时验证；明确未测下游（Peeling §4.1/§5）。
  - **规则自演化（Evontree）**：15 根概念人工种子；规则只覆盖 subclass/synonym；explicit 注入掉点、implicit/mix 报告有效（增益仅报告值）；两模型单域自评（Evontree §4/§5；细节见 F6）。
- **降级**：「覆盖窄/维护贵」「语义漂移/关系方向易错」「把常见当应然」在 digest 中没有测量；前两条是从工程常识借来的，第三条见 [frontier G5](./frontier.md)，均不再作为判断。
- **边界**：这是四条路线，不是全部来源；「数据挖掘」没有独立 digest 案例，本页不单列。
- **来源**：SFE-O / OntoDoc / ReX-GG / Peeling / Evontree digest，见上。

## F5 · 来源字段是建议，生成者身份没有进判定

- **判断**：四篇论文都没有把「生成者身份（expert/llm/mining）」作为判定权重。`provenance_triples[]`、`generator_version`、`evidence_span` 这三个字段出自 digest 的 E3 建议（OntoDoc §6.5、ReX-GG §6.1），是工程建议，不是论文产物；ReX 论文侧能核的只是 JSON 输出含证据 span（digest §0/§3）。
- **已核（流程痕迹，不是 schema）**：OntoDoc 的每条 assumption 至少一条引用 DB triple 编号，描述可追溯到 triple；ReX 的匿名互评把候选匿名/隐藏模型名（去偏设计），刻意抹掉来源；Evontree 的三元组按 `ConfirmValue` 分 confirmed/reliable/extrapolated/gap（Table 2）。这些说明流程里有证据痕迹，不等于产物带来源权重。
- **推测（字段设计）**：`provenance_triples[]`/`generator_version`/`evidence_span` 可作为工程字段先记，但论文没有给出这些字段名；标 `推测`，不算「已核字段」。
- **未核（效果）**：四篇都没有测过按来源加权会不会降低误判。所以「判定器不知道约束是谁写的」是 `推测`，且与「产物带来源字段」不是一回事——字段可加，加权效果没测。
- **含义**：来源标记是可加的字段设计，不是已验证的收益；进权重前先测 false-accept/false-reject。
- **来源**：OntoDoc digest §3.1（assumption 引用 triple）/§6.5（E3 schema）；ReX-GG digest §3/§6.1（匿名化与 E3 schema）；Evontree digest §4.1（Table 2）/§6（E3 三元组表）。

## F6 · 训练侧注入：explicit 是硬反例，implicit/mix 只到报告值

- **判断**：论文报告 implicit/mix 有增益、explicit 掉点；能对上的是 explicit 更差（Llama3 56.1 vs 62.5、Med42 62.3 vs 63.5），implicit/mix 的增益只到报告值（Table 3 的 Llama3 mix 均值 61.0 反而低于 raw 62.5）。所以不能概括成「本体注入有效」，也不能用 explicit 的掉点概括成「本体注入有害」。
- **数字（仅按报告值引用）**：论文报告 Llama3-8B-Evontree(mix) +3.1%、Med42-v2-Evontree(implicit) +3.7%（三个医疗 QA 基准平均），并称相对最强 baseline 为 +0.9/+1.1。**这些数字不得当净增益/相对百分比**：digest Table 3 的均值列（Llama3 raw 62.5、mix 61.0）与 Δ 行（+3.1%）对不上，+0.9/+1.1 也是同表绝对分差、不是相对百分比；表内均值与 Δ 行不可复算。gap 只有 1,396 条。
- **条件**：两个模型（Llama3-8B、Med42-v2）、单医疗域、自评/自建 benchmark；15 根概念人工种子；规则只覆盖 subclass/synonym。
- **反例（explicit）**：explicit 变体低于 raw（Llama3 平均 56.1 vs 62.5；Med42 62.3 vs 63.5）；安全面 Jailbreak Safe 96.35→83.65 / 60.19→45.19。
- **安全/通用能力（implicit/mix）**：没有显著安全下降；通用能力（MMLU/TriviaQA/ARC）平均只降 0.15%，部分还升。
- **边界**：不能外推到推理时约束、其他关系类型/模型族。**收益表述**：Evontree 数字一律「仅按报告值引用」；表内均值与 Δ 行不可复算（Llama3 raw 62.5 vs mix 61.0 与 +3.1% 对不上），+3.1/+3.7 与 +0.9/+1.1 都不得当净增益/相对百分比——也不得用 +0.9/+1.1 代替 +3.1/+3.7 充作「更保守的净收益」。`存疑`（表内复算）。
- **来源**：Evontree digest §4.2/§4.3/§5/§6。

## F7 · 消费路径有实现，质量未测

- **判断**：开源侧已有「生成本体 → 派生 SHACL → 校验数据」的完整路径（semantica `OntologyEngine.to_shacl` + `validate_graph`），最小跑通（1,729 chars / 54ms / 1 violation）。但这只证明管线能跑；派生 shapes 的漏检/误报、覆盖度没有测。
- **等级**：已核（代码 + 最小运行）。
- **含义**：F3 的「可消费性没测」对四篇论文仍成立，但不能再说「没人做消费」——工程侧有实现，缺口转移到「质量/覆盖」。
- **来源**：[semantica digest](../../../src/open-source/semantica-agi-semantica/digest.md) §3–§5。
