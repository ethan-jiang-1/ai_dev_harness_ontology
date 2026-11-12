---
status: draft
updated: 2026-11-09
---

# 结论总表

跨主题的结论索引。**这是流水线唯一允许被 `deliverables/` 直接引用的地方**——交付物引结论编号，不引原始材料。

> 各派的局部判断先写在本派 `claims.md`（`01-Lx` 等）；只有跨派或进 `deliverables/` 时，才升到本页的 `E-xx`。这样改一个派不必动本页。

等级定义见 [conventions](../meta/rules/conventions.md#证据等级)。

> **反向阅读**：E 行 → [evidence-anchors](./evidence-anchors.md)（承重数/条件 + digest 节）→ digest §4（数字与条件）→ §5（不能说明什么）；缺的数去对应派 `frontier.md`。不要在 E 表里补新判断。

## 已证

暂无**可复现**的一手证据（本仓库尚无实验）。下表「已核」指已对原文摘要核验，强于二手转述，但仍不等于独立复现。

> **E 层的证据类型**：E-01/E-07/E-08/E-09/E-14/E-15/E-18 是 harness/度量证据，不是本体专属；E-20 是代码级形态分类。引用前先看 impact 列，不要把“结构化上下文”读成“本体”。

## 已撤回（源未过准入）

> 编号保留，供旧引用回链；**结论不再成立**，不得作为判断或交付物依据。依据见 [来源清除审计](../meta/audits/2026-11-11-source-purge.md)。

| 编号 | 原锚 | 撤回理由 | 替代 |
|---|---|---|---|
| E-02 | Ontology Catch | 唯一锚移出（单机构、无代码/采用） | 无；判定器来源偏向待新源 |
| E-03 | OA-RAG | 唯一锚移出（单机构） | 无；接地等级待新源 |
| E-04 | POLAR | 唯一锚移出（单机构） | 无；护栏权衡只保留 CASEL（E-15） |
| E-06 | Diagnose | position paper | 无；工作流归因待新源 |
| E-10 | MIOE | 唯一锚移出（单机构） | 无 |
| E-11 | Peeling | 单作者 / L1 | 无 |
| E-13 | POLAR | 同 E-04 | 无 |
| E-16 | OntoAct | 唯一锚移出（单机构） | 无 |
| E-26 | 四条查询路线 | 只剩 GGC 一条，无法比较 | 无 |

## 已核（一手原文摘要）

> 状态为 `withdrawn` 的行不再成立；见上节。

| 编号 | 结论 | 出处 | 影响 | 状态 |
|---|---|---|---|---|
| E-01 | 在足够强的检索 harness 下，**被测量的**结构化工件（摘要树、PageIndex 大纲、wiki、entity graph）在 **FRAMES** 上无可检出的准确率增益；PageIndex 式大纲在同规模下反而退化。**本体、timeline、mind map、session memory 在 Table 1 是 not measured，不能算进这个结论。** 作者自述这些工件的回报在**部署层**（治理、跨源集成、上手、时序定向、连续性），而准确率基准看不见；但其部署 ledger 为空，**这是作者主张，不是观测**。限定：单基准、单 compiler/answer model、无 CI | [CAI digest](../src/papers/2610.41172-context-as-infrastructure/digest.md) | 支撑 P1a/P1c（价值在约束/注入有条件）；**不支撑 P1b**（ontology 在原文是 not measured） | active |
| E-02 | 三种本体来源（专家 / LLM 生成 / 数据挖掘）在漏检与误报上各有偏向，无单一向优：真实答案 catch/FA 为 curated 18.9/16.8、data-derived 8.2/3.5、masked LLM 5.0/1.8；precision（**人工故障、25% 错答案假设**）为 57.1/72.3/93.7；curated 精确度**仅略优于随机**（+1.6 点，CI 跨零）；按发布状态使用的 curated schema 可能**与自身数据矛盾**。空结果重试在人工 fault 上 catch 79.2%、FA 0%，是关键基线 | [What Does an Ontology Catch digest](../meta/audits/2026-11-11-source-purge.md#src-2610-37809) | 支撑 P3a/P3b（判定权衡 + 来源偏向）；给出判定器评估基线 | withdrawn |
| E-03 | 强制每个答案报告所用作证据的本体观察 + 接地等级（entailed/supported/related/unrelated），在三个大本体、六个医学 QA 任务、2 backbone 上整体最优：平均 50.5%/68.1%；Tests 1–2 +10–15pp；Test 3 同 8k 预算 84.9% vs 66.7%，9.7k vs 96.7k tokens/问。限定：等级是**模型自评**、未校准；检索是主瓶颈（gold evidence 完整检索 MCQ 61.7% vs OQ 23.6%） | [OA-RAG](../meta/audits/2026-11-11-source-purge.md#src-2610-36335) | 支撑 P1a/P2；接地等级是弱信号（P1c 的边界） | withdrawn |
| E-04 | 用两层本体对工具调用打可逆性分、执行前剪枝：τ²-bench 上六个模型中四个在 airline 域提升 0.11–0.18；**但 18 个模型-域组合仅 8 个整体改善，retail 与更强模型常回退**；作者声明 reward 不是防止伤害的直接度量。**T1-only 接近 blanket veto，增益却不比 full 小——结构反向组合的贡献未被隔离** | [POLAR](../meta/audits/2026-11-11-source-purge.md#src-2610-08082) | 支撑 **P3a**（判定/护栏权衡）；**不支撑 P3b**（未测来源）、不支撑「结构已被证明有效」；削弱「护栏总是更好」 | withdrawn |
| E-05 | 本体在记忆系统中承担**对齐与印证条件**（跨期身份 registry、双模态互证），而非自由推理；克制的用法更易落地。alias memory 让 final-period CMR +7.8–12.1 pp（4 settings），human-audit recall +22.5–29.0 pp，semantic matching token −40.3%。限定：专有数据、3 period、无年度周期；未匹配≠关系结束 | [FIRME](../src/papers/2610.40482-firme/digest.md) | 支撑 P1a（能力与意图分离）+ P2（同一抽取器，换状态结构效果不同）；04 核心证据 | active |
| E-06 | 本体接地类任务的失败多来自**工作流**：输入不足、领域接地弱、模板与词汇缺口、校验弱、非局部修复。作者把它组织成五角色（Input/Generator/Output/Validator/Repairer）+ 七诊断变量；**语法通过不等于语义充分**。限定：position paper、单案例、无量化分布 | [Before Blaming the LLM](../meta/audits/2026-11-11-source-purge.md#src-2610-35267) | 支撑 **P2**（同一模型，换工作流结果不同）；可作诊断表（仓库外验证） | withdrawn |
| E-07 | 形式化器存在 solver-like behavior：轨迹里算出答案，程序只做复述。2,000 generations：85% traces 含 SLB（BlocksWorld PDDL 例外 51%）、24% reasoning token 是 SLB；163/1,791 程序继承 reasoning answer；reasoning answer 错时 hardcoded 0/19 正确、independent 32% 正确。伤害有二——token 成本只在 2/4 数据集随规模上升（Meeting 3,873→10,971、Zebra 532→4,148；Calendar/BlocksWorld 不增；Qwen Calendar 约 3×/+54%、GPT-OSS −31%），不是普遍规律；形式化保证失效 | [SLB digest](../src/papers/2611.02395-solver-like-behavior/digest.md) | 支撑 P2/C-03（判据须能看中间）；不直接支撑本体增益 | active |
| E-08 | 「主张-证据叶子」的导航树是唯一被测出正收益的工件：证据充分时查询 token −91%，不充分时 +1.9%，**平均 −38%**；盈亏平衡充分率 2%，实测约 43%。限定：单基准 FRAMES、单 compiler/answer model、无 CI；平均 −38% 是条件混合，不能当上线依据 | [CAI](../src/papers/2610.41172-context-as-infrastructure/digest.md) | 支撑 RQ5/P1a（编译省预算，不解决准确率）；**工件/编译证据，不是本体形态或本体增益** | active |
| E-12 | 同一份知识，**投影成文的 pooled element score 最高**（0.777 > JSON 0.717 > 查询 0.638 > 检索 0.597），但**不是普适排序**：GLM-5.2 的 JSON 0.900 反超文本 0.891；Qwen 的工具 0.407 低于文档检索 0.538；工具是事后描述性条件、非受控。避坑率 0.605→0.802（+19.8pp，OR 5.45，p=6.0×10⁻⁷），但**K0→K1 命名+单位已有 +54.6pp**，塔只再加 +19.8pp；物理深度未测，H3（事故记录）K4 0.644 vs K4x 0.645 未支持。限定：n=1 工厂、9 任务、答案基本写在文本里 | [N&D digest](../src/papers/2610.11768-narrow-and-deep/digest.md) | 支撑 P1b/P1c（薄语义层先起量、条件性）；不支撑 P1a（这是知识供给）；与 E-01 并列构成 C-04 | contested |
| E-13 | 约束类机制的增益**随模型基线能力升高而缩小**：airline/retail/telecom 斜率约 −0.76/−0.67/−0.31（R² 0.92/0.98/0.65），但这是六点描述性拟合，**给不出零交叉的部署阈值** | [POLAR](../meta/audits/2026-11-11-source-purge.md#src-2610-08082) | 强化 E-04；P1a 的适用边界；六点描述性拟合，不可当预测曲线 | withdrawn |
| E-14 | 编译的盈亏平衡是**条件性**的：无限视野 `p_h > 2%`，有限视野 `p_min = 2% + c/(0.929Q)`；平均 −38% 是 hit/miss 混合，不能当上线依据；证据替换用检索轮次换 token，配对子集时延约 **3×** | [CAI](../src/papers/2610.41172-context-as-infrastructure/digest.md) | 支撑 RQ5（编译经济学）；**不是本体增益** | active |
| E-15 | 护栏/分配机制应报 **harm–approval–cost 前沿**，不是单一 HSR：CASEL 模拟（20 seeds、120k actions）HSR 14.75%→7.02%、审批 8.7%；最低 HSR 是 Consequence-Menu 4.38%（审批 13.8%），Risk-Menu 5.82%（审批 12.6%）；CASEL 用约 30% 更少审批达到相近 harm。**主表 CASEL 在 τ=∞（阈值关闭）下；不是所有方法同 menu/cost**。full ledger 在 harm–compute 面被支配，但在低审批端（4.3% approvals / 11.82% HSR）是前沿点。限定：模拟、γ_m 假设、审批疲劳未建模 | [CASEL digest](../src/papers/2610.36570-casel/digest.md) | 支撑 P3a（harm–approval–cost 权衡）+ RQ4/RQ5；**harness 证据，无本体变量** | contested |
| E-16 | **推理期约束的形式决定它是天花板还是护栏**：限制知识源（curated KG）可能封顶；验证条件（三值 ⊤/⊥/?） + 假设 revision 可同时提高成功率与减少无效干预（Tacit-FLE **78.6/83.3/90.0%** vs IfR 64.3/66.7/65.0%，SI **1.6–2.4** vs 6.4–17.8；Mars 15.92 vs 10.64；ALFWorld 98.5% vs 96.3%）。限定：模拟、固定 schema、无真实工厂 | [OntoAct digest](../meta/audits/2026-11-11-source-purge.md#src-2610-21983) | 支撑 P1a/P2；refine 01-L3 | withdrawn |
| E-17 | **记忆是状态，不是事实集合**：Persistent Facts + Relational State（有效性/scope/更新/冲突）+ Reasoning State（当前请求怎么用）。EvoMemState 四基准：Complete Retrieval 85.6%（与最好 baseline 相当），但 Acc@complete 70.8/68.5（+11.5/+31.2）；去掉 Relational −8.9/−6.4，去掉 Reasoning −8.0/−15.0，去掉 RL −7.9/−16.4；reasoning state 跨 6 系统 +0.2–4.9。限定：文本 only、需训练信号 | [EvoMemState](../src/papers/2611.03743-evomemstate/digest.md) | 支撑 P1a/P2（同一 memory backend，加 reasoning state 效果变）；04 核心 | active |
| E-09 | SLB 的规模与干预：85% traces、24% token、77–89% 程序仍独立重算；SLB 与准确率无关联（ratio +0.1 → +0.007）；placeholders 减 SLB token **97%** 而准确率 +2.6（不降）；cautionary prompts 只减约 1/4；batching 准确率 −5.9。形式语言是最大解释变量（Python > Z3/PDDL，0.03–0.20 ratio）。限定：3 模型/4 CSP/2 FL、单次生成、闭源无 trace | [SLB](../src/papers/2611.02395-solver-like-behavior/digest.md) | 支撑 06 trace；把「SLB 可移除」从推测升为已核；不直接支撑本体增益 | active |
| E-10 | 本体预测机制上可干预，但无法与类别辅助信息干净分离：单层 Disentangle 点估计 MDAS 0.592 vs DAS 0.584，但单 seed、无 CI，不宜当稳定排序；MDAS 的 Cause 0.527/Iso 0.658 与 DAS 0.589/0.579 反向。SAE 0.412/0.371；多任务 +0.081 Iso / −0.052 Cause 是 **best-vs-best 配对差**，不是整体平均；四层 DAS 512×4 0.667，Δ 基线是单层同总维 0.565，不是 0.584。正确本体预测本身不意味着干净的内在本体；分离按类别而异 | [MIOE digest](../meta/audits/2026-11-11-source-purge.md#src-2610-38326) | 支撑 06 mechanism（内部本体不干净）；不直接支撑 P1/P2 | withdrawn |
| E-18 | **agent 评测应把配置当系统变量**：4 tasks × 432 cells × 5 runs（8,640 runs；18,240 trajectories）中，**54%** score variance 来自重复同一配置的 run-to-run 噪声（限定为**真实尝试/过 hurdle**；不排除 hurdle 失败为 39.4%、排除后 46.1%）；Information 轴影响 > Model > Reasoning > Budget > Verification；信息同时降成本/改善校准；预算只在信息/模型足够时有用；**验证行为靠工具不靠 prompt**（prompt 19→22%，oracle 翻三倍）；agent 99.8% 仍用弱 specialist。限定：4 tasks/2 domains、排除 memory/multi-agent | [Agents digest](../src/papers/2610.01618-agents-are-systems/digest.md) | 支撑 P2（配置轴）+ 06 metrics；**无本体变量，是评测证据**；REPLACE 单次 score 评测 | active |
| E-21 | **Text2SPARQL 的单条路线只在单设置上成立**：GGC 的选择性纠错在 MCQA（电影域、iMKG、31,570 题、Llama-3.2-3B 单骨干）把答案集匹配率 90.23→98.33（全量纠错 92.34；45% 是相对全量纠错的墙钟，比单跑 +10%；Gate FPR 0.31%、trigger 9.31%）。限定：单 benchmark、单 snapshot、单系统、单模型；Match 允许 superset；不能当业务正确或跨域效应量；原“三条路线”中的 NLKGQ/KGVoyager 已移出，不再比较 | [GGC digest](../src/papers/2607.28082-ggc/digest.md) | 支撑 03/querying 的单路线机制；**不支撑路线排序**、不支撑业务正确 | contested |
| E-22 | **访问控制至少分三层，层间不能互推**：标签/分类有生产级来源（Glyph，Apple 单企业，~3.4M 列/98k 表、275-leaf 分类本体、列级标签；NDCG/MAP 是检索指标、生产接受率是作者报告且对 FN 盲；**不产策略判定、不执行访问控制**）；策略层没有 ontology/KG 领域来源（OPA 只是通用策略引擎候选）；执行层只有 trustgraph 的单实现读路径 SHACL-AF post-filter（fail-open、只删 subject，E-20）。因此「有敏感标签」不能推出「有策略」或「执行正确」；读路径≠写授权。限定：Glyph 单企业/标签层；trustgraph 单实现/只读代码；无跨企业、无漏标率、无领域策略来源、无生产效果；OPA adjunct 未集成 | [Glyph digest](../src/papers/2609.10430-glyph/digest.md) · [trustgraph digest](../src/open-source/trustgraph-ai-trustgraph/digest.md) · E-20 | 支撑 04 C.1/C.7；**不支撑端到端访问控制** | active |
| E-24 | **策略层可以纸面判定，但领域映射不是标准给的**：XACML 3.0 给合并算法（deny-overrides 等）/obligation/version；ODRL 2.2 给 permission/prohibition/duty/conflict；GB/T 43697 只分核心/重要/一般三级，GB/T 35273 只定义个人信息/敏感个人信息；04 的 1–4 + 2/3 阈值是工程映射。11 条测试 10 条有唯一期望；T9（steward+table）R4/R5 优先级未定；`clearance` 未被 8 条规则消费；`skip` 是 XACML/ODRL 都没有的第 4 种效果。限定：标准材料卡为摘要/精读混合，条款与 API 待核；11 条测试未跑；无领域策略来源；不证明执行 | [policy mechanism](../topics/01-constraint/policy/mechanism.md) · [GB/T 43697 卡](../src/web/gbt-43697/gbt-43697.card.md) · [XACML 卡](../src/web/oasis-xacml-3.0/oasis-xacml-3.0.card.md) · [ODRL 卡](../src/web/w3c-odrl-2.2/w3c-odrl-2.2.card.md) · E-22 | 支撑 04 C.2；**不支撑「策略正确」或「执行可授权」** | active |
| E-25 | **可消费性不是产物属性，是三关记录**：load（parsed + 每个 shape 有 target + consumer endpoint）、validate（坏样本 caught + 干净样本 FP + shacl-shacl）、answer（CQ expected + 0 行分因）；三档里结构表是唯一三关 supported；10 个坏样本里现有 `build_report` 只稳定抓住 2 个（字面量 tag、缺 level）；`targeted=0` 必须是 undetermined，不是 pass。限定：fixture + 标准材料卡；S1–S6/S9/S10 未跑；无真数据/跨域/生产误报率 | [consumability](../topics/05-produce/representation/consumability.md) · [SHACL 卡](../src/web/w3c-shacl/w3c-shacl.card.md) · [ODCS 卡](../src/web/odcs-v3.1/odcs-v3.1.card.md) · E-12 | 支撑 04 A.1/A.5；**不支撑「建完就能用」** | active |

> E-06 的论文发现是「已核」；把它推广为「漂移=输入不完备」是仓库推断，标 `推测`。两者不要混。
>
> **出处纪律（2026-11-09）**：本页 E-xx 出处一律链 `digest.md`；`card.md` 只用于 `src` 台账的 provenance，不再作为结论出处。影响列的 P1a/P1b/P1c/P2/P3a/P3b 定义见 [THESIS](../THESIS.md#工作假设与反驳条件)。

## 已核（代码）

> 这一节是代码级核对，不是论文摘要。按 [ADR 0004](../adr/0004-open-source-source-type.md)，定位到 `文件:符号` 可到 `已核`；只读代码、未跑测试，不等于 `已证`。

| 编号 | 结论 | 出处 | 影响 | 状态 |
|---|---|---|---|---|
| E-20 | 「本体被执行」不是单一形态：同一 `engine` 至少覆盖 OWL 2 QL 查询重写（ontop）、SHACL-AF 策略求值（trustgraph）、SHACL 校验（semantica）、SHACL→SPARQL/verified Core（open-ontologies）四种语义；执行不保证健全（trustgraph target/rule 异常 fail-open，且只删 subject 侧），也不等于写授权（open-ontologies 只做影响报告与 CI 规则门，不对单次写签发授权）。限定：4 个开源项目、pin commit、只读代码未跑测试；不能外推为所有 `engine` 实现 | [execution-forms 代码核对](../topics/execution-forms.md#代码级核对2026-11-09) · [trustgraph](../src/open-source/trustgraph-ai-trustgraph/digest.md) · [semantica](../src/open-source/semantica-agi-semantica/digest.md) · [ontop](../src/open-source/ontop-ontop/digest.md) · [open-ontologies](../src/open-source/fabio-rovai-open-ontologies/digest.md) | 支撑「形态是独立变量」这一前提；**不支撑效应量**（未跑对照）；把 `engine` 从强度刻度拆成语义类别；`read-path` 仍只有 1 个实现，保持轴外 | active |

| E-23 | **读路径策略过滤的 10 条用例：1 条正常，4 类漏洞**：trustgraph 只在 subject 命中时删三元组；object 方向不删（只查 `triple.s`）、target 异常 fail-open、无策略 open mode、判定缓存 60s 且不含 policy_version。唯一 fail-closed 是「有策略 + 缺 `user_context`」。**没有合格第二实现**：sparql-guard 方向相反但单作者/1★/3 周龄/无 harness 调用点；Jena `jena-permissions` 已退役；Fuseki 是端点级 ACL。限定：trustgraph 单实现、pin `184f622`、只读代码；10 条里 6 条已核、4 条 `待核`；不证明泄漏率/生产效果 | [read-path](../topics/01-constraint/commit-gate/read-path.md) · [trustgraph digest](../src/open-source/trustgraph-ai-trustgraph/digest.md) · E-20 | 支撑 04 C.3；**不支撑「读路径可授权」**、不支撑通用行为 | active |

> E-20 是代码级综合，不是单篇 digest：四个 digest 提供逐项目证据，[execution-forms](../topics/execution-forms.md#代码级核对2026-11-09) 提供跨项目矩阵。引用时写「已核（代码）」，不要写成「已证」。

## 推测（未核原文）

| 编号 | 结论 | 为什么仍是推测 | 状态 |
|---|---|---|---|
| E-11 | 训练好的检索嵌入中，前缀维度与分类法粒度对齐 | 仅读综述转述（Peeling the Matryoshka） | withdrawn |
| E-19 | 机制是否值得落地，取决于「位置 × 成本 × 使能条件」，不是本体质量；没有一条适用于所有机制的能力曲线（约束类随能力下降，知识投影不随容量上升） | 横切综合；证据分散在 E-08/E-12/E-14/E-15/E-17（E-13/E-16 已撤回） | active |
| E-26 | **四条查询路线按资产条件选，不按总分排**：有关系库 → OBDA；有 KG 且本体进得了 context → ontology-in-context；有 KG 无本体 → agentic navigation；有生成器 + 可标注错例 → gate/correction。4×8 矩阵、17 类失败与「不可比」清单见 [compare](../topics/03-knowledge/querying/compare.md)；98.33 / 89.9 / 64.6 不能互比；OBDA 无 LLM、无 benchmark | 跨源综合；三条路线无头对头；P1/P2 空 | withdrawn |
| E-27 | **输出校验要六类 + 三态，跨段故障会换形态**：同一 0 行可来自缺 tag/错 join/超时/真答案为空；同一 allow 可来自错 level/skip/版本；单段指标（violations/accuracy）看不见。六类 = schema/cardinality/provenance/freshness/cross-field/plausibility；`pass` 只在 `targeted>0` 且 `skipped=0` 时给 | 无跨段注入实验；六类里只有前两类成本低；生产误报未测 | active |

## 存疑

| 编号 | 结论 | 为什么存疑 |
|---|---|---|
| Q-01 | 「本体越完备效果越好」 | 与 E-01 冲突；完备性与可判定性在工程上反向 |
| Q-02 | 「多智能体优于单体」 | 缺少在同等上下文预算下的对照 |
| Q-03 | 「护栏必然提升任务表现」 | E-04 在 τ²-bench/单 gate/6 模型上否证了「护栏必然提升 reward」；不能外推为所有护栏/所有度量；保留作反例索引 |

## 冲突

| 冲突 | 双方 | 当前处理 |
|---|---|---|
| C-01 | 「上本体提准确率」 vs E-01 | 不做平均。假定前者成立的条件是弱 harness + 窄域；强 harness 下后者优先。待 RQ1 实验分离 |
| C-02 | Q-01「越全越好」 vs 领域实践「窄而深」 | 倾向窄而深，但缺跨域对照 |
| C-03 | 度量尺不一致 | E-01 与 E-04 都说「用准确率/reward 度量控制类机制会得出错误结论」。**这不是两个结论，是同一个方法论问题**：需按机制类型选度量 |
| C-04 | 结构化工件无增益（E-01） vs 投影文本有效（E-12） | **不矛盾**，但要说得更准：差别不只在「答案是否写在知识里」，还在**投影什么**——CAI 投影的是**证据**（claim + 逐字 span），N&D 投影的是**领域知识**（本体塔）。证据投影在需要审计/省 token 时有效；领域知识投影在答案即规则/手册时有效。判据见 [03 知识](./03-knowledge/README.md) |

C-03 是当前最有价值的一条：它把「正面证据 vs 负面证据」的文献冲突，重新解释为**度量错配**。若成立，P1 的核心论证就从「本体有用/无用」变成「该用哪把尺子」。

**2×2 证据（2026-11-10）**：约束类在任务账上混合/负、在风险账上前沿更优；知识供给在准确率上 neutral、在 token 上正收益（E-01/E-04/E-12/E-15；[06-L16](./06-measure/claims.md)；[03 measurement](../deliverables/03-mechanism-reference/04-across-positions/03-measurement.md#25-机制类型与尺子分派)）。**逐格已核，方向翻转仍是跨来源综合**——没有同数据集两把尺子的对照。

**能力梯度不是一条线（`推测`，Wave 1 综合）。** 约束类收益随基线能力上升而下降（E-13）；知识投影的增益**不随容量上升**（E-12，H2 p=0.85），9B 带投影 0.737 > 750B 不带 0.672。两者不矛盾：护栏**替代**判断，投影**补充**知识。待 Wave 2/3 的 CASEL、OntoAct、Grid Agents 验证。

冲突不消除，保留在表里。

## 生命周期

E-xx 不是一次写死。每条有一个 `状态` 列；改 E 之前先读对应 digest 的 §5（不能说明什么）。

| 状态 | 含义 | 当前 |
|---|---|---|
| `active` | 未被反例推翻；按限定使用 | 除下列外默认 |
| `contested` | 主结论可站，但某个读法/外推被削弱 | E-04（“结构有效”的读法被 T1-only 削弱）、E-12（排序非普适）、E-15（模拟，非部署） |
| `withdrawn` | 源未过准入，结论撤回；编号保留供回链 | E-02/03/04/06/10/11/13/16/26 |
| `superseded` | 被新证据取代；保留编号与指针 | 暂无 |

“什么会改变它”写在每条 digest 的 §5 与 §9；本页不重复。**不要把 `contested` 当成降级**：它表示限定条件已经写清，仍可引用。

## 悬空结论（未归派）

当前无。

新派成立前，把“跨派、但暂时没有归属”的判断先记在这里；同一方向累计 ≥3 条，再按 [topic 协议](../meta/rules/topic-research-protocol.md) 立派。不要把单条判断直接写成新派。
