---
status: draft
updated: 2026-11-07
---

# 结论总表

跨主题的结论索引。**这是流水线唯一允许被 `deliverables/` 直接引用的地方**——交付物引结论编号，不引原始材料。

> 各派的局部判断先写在本派 `claims.md`（`01-Lx` 等）；只有跨派或进 `deliverables/` 时，才升到本页的 `E-xx`。这样改一个派不必动本页。

等级定义见 [conventions](../meta/conventions.md#证据等级)。

## 已证

暂无**可复现**的一手证据（本仓库尚无实验）。下表「已核」指已对原文摘要核验，强于二手转述，但仍不等于独立复现。

## 已核（一手原文摘要）

| 编号 | 结论 | 出处 | 影响 |
|---|---|---|---|
| E-01 | 在足够强的检索 harness 下，结构化工件（本体、图、wiki）在 **FRAMES** 上无可检出的准确率增益；PageIndex 式大纲在同规模下反而退化。作者自述这些工件的回报在**部署层**（治理、跨源集成、上手、时序定向、连续性），而准确率基准看不见；但其部署 ledger 为空，**这是作者主张，不是观测**。限定：单基准、单 compiler/answer model、无 CI | [CAI](../src/papers/2610.41172-context-as-infrastructure/card.md) | **支撑 P1**（价值在约束与控制） |
| E-02 | 三种本体来源（专家 / LLM 生成 / 数据挖掘）在漏检与误报上各有偏向，无单一向优：真实答案上 curated catch/FA/precision 18.9/16.8/57.1%，data-derived 8.2/3.5/72.3%，masked LLM 5.0/1.8/93.7%；curated 精确度**仅略优于随机**（+1.6 点，CI 跨零）；按发布状态使用的 curated schema 可能**与自身数据矛盾**。空结果重试在人工 fault 上 catch 79.2%、FA 0%，是关键基线 | [What Does an Ontology Catch](../src/papers/2610.37809-what-does-an-ontology-catch/card.md) | **支撑 P3**（判定是权衡）；给出判定器评估基线 |
| E-03 | 强制每个答案报告所用作证据的本体观察 + 接地等级（entailed/supported/related/unrelated），在三个大本体、六个医学 QA 任务、2 backbone 上整体最优：平均 50.5%/68.1%；Tests 1–2 +10–15pp；Test 3 同 8k 预算 84.9% vs 66.7%，9.7k vs 96.7k tokens/问。限定：等级是**模型自评**、未校准；检索是主瓶颈（gold evidence 完整检索 MCQ 61.7% vs OQ 23.6%） | [OA-RAG](../src/papers/2610.36335-oa-rag/card.md) | 支撑 P1、P2；接地等级是弱信号 |
| E-04 | 用两层本体对工具调用打可逆性分、执行前剪枝：τ²-bench 上六个模型中四个在 airline 域提升 0.11–0.18；**但 18 个模型-域组合仅 8 个整体改善，retail 与更强模型常回退**；作者声明 reward 不是防止伤害的直接度量。**T1-only 接近 blanket veto，增益却不比 full 小——结构反向组合的贡献未被隔离** | [POLAR](../src/papers/2610.08082-polar/card.md) | **支撑 P3**，**削弱**「护栏总是更好」；也削弱「结构本身有效」 |
| E-05 | 本体在记忆系统中承担**对齐与印证条件**（跨期身份 registry、双模态互证），而非自由推理；克制的用法更易落地。alias memory 让 final-period CMR +7.8–12.1 pp（4 settings），human-audit recall +22.5–29.0 pp，semantic matching token −40.3%。限定：专有数据、3 period、无年度周期；未匹配≠关系结束 | [FIRME](../src/papers/2610.40482-firme/card.md) | 支撑 P1（能力与意图分离）；04 state 的核心一手证据 |
| E-06 | 本体接地类任务的失败多来自**工作流**：输入不足、领域接地弱、模板与词汇缺口、校验弱、非局部修复。作者把它组织成五角色（Input/Generator/Output/Validator/Repairer）+ 七诊断变量；**语法通过不等于语义充分**。限定：position paper、单案例、无量化分布 | [Before Blaming the LLM](../src/papers/2610.35267-diagnose-workflow/card.md) | **直接支撑 P2**；可作 EXP-002 诊断表 |
| E-07 | 形式化器存在 solver-like behavior：轨迹里算出答案，程序只做复述。2,000 generations：85% traces 含 SLB、24% reasoning token 是 SLB；163/1,791 程序继承 reasoning answer；reasoning answer 错时 hardcoded 0/19 正确、independent 32% 正确。伤害有二——成本随实例增长、形式化保证失效 | [SLB](../src/papers/2611.02395-solver-like-behavior/card.md) | 支撑 P2（判据须能看中间） |
| E-08 | 「主张-证据叶子」的导航树是唯一被测出正收益的工件：证据充分时查询 token −91%，不充分时 +1.9%，**平均 −38%**；盈亏平衡充分率 2%，实测约 43%。限定：单基准 FRAMES、单 compiler/answer model、无 CI；平均 −38% 是条件混合，不能当上线依据 | [CAI](../src/papers/2610.41172-context-as-infrastructure/card.md) | 支撑「编译解决预算，不解决准确率」 |
| E-12 | 同一份知识，**投影成文**比 JSON、查询工具、文档检索都更易被使用：element score 投影 0.777 / JSON 0.717 / 查询 0.638 / 检索 0.597；避坑率 0.605→0.802（+19.8pp，OR 5.45，p=6.0×10⁻⁷）。**K0→K1 命名+单位已有 +54.6pp**；9B 带投影 0.737 > 750B 不带 0.672；H2（增益随容量上升）未支持（p=0.85）。限定：n=1 工厂、9 任务、答案基本写在文本里 | [Narrow & Deep](../src/papers/2610.11768-narrow-and-deep/card.md) | 支撑 03 知识派；与 E-01 并列构成 C-04 |
| E-13 | 约束类机制的增益**随模型基线能力升高而缩小**：airline/retail/telecom 斜率约 −0.76/−0.67/−0.31（R² 0.92/0.98/0.65），但这是六点描述性拟合，**给不出零交叉的部署阈值** | [POLAR](../src/papers/2610.08082-polar/card.md) | 强化 E-04，划定 01 约束派的适用边界；不可当预测曲线 |
| E-14 | 编译的盈亏平衡是**条件性**的：无限视野 `p_h > 2%`，有限视野 `p_min = 2% + c/(0.929Q)`；平均 −38% 是 hit/miss 混合，不能当上线依据；证据替换用检索轮次换 token，配对子集时延约 **3×** | [CAI](../src/papers/2610.41172-context-as-infrastructure/card.md) | 支撑 RQ5；把「编译值不值」变成可算的门槛 |
| E-15 | 护栏/分配机制应报 **harm–approval–cost 前沿**，不是单一 HSR：CASEL 模拟（20 seeds、120k actions）HSR 14.75%→7.02%、审批 8.7%；Risk-Menu HSR 5.82% 但审批 12.6%；CASEL 用约 30% 更少审批达到相近 harm。轨迹总账反噬（11.82%）。限定：模拟、γ_m 假设、审批疲劳未建模 | [CASEL](../src/papers/2610.36570-casel/card.md) | 支撑 RQ4/RQ5；把「护栏值不值」变成三维前沿 |
| E-16 | **推理期约束的形式决定它是天花板还是护栏**：限制知识源（curated KG）可能封顶；验证条件（三值 ⊤/⊥/?） + 假设 revision 可同时提高成功率与减少无效干预（Tacit-FLE 78.6–90.0% vs IfR 64.3–65.0%，SI 1.9–2.4 vs 6.4–17.8；Mars 15.92 vs 10.64；ALFWorld 98.5% vs 96.3%）。限定：模拟、固定 schema、无真实工厂 | [OntoAct](../src/papers/2610.21983-ontoact/card.md) | 支撑 P1/P2；refine 01-L3 |
| E-17 | **记忆是状态，不是事实集合**：Persistent Facts + Relational State（有效性/scope/更新/冲突）+ Reasoning State（当前请求怎么用）。EvoMemState 四基准：Complete Retrieval 85.6%（与最好 baseline 相当），但 Acc@complete 70.8/68.5（+11.5/+31.2）；去掉 Relational −8.9/−6.4，去掉 Reasoning −8.0/−15.0，去掉 RL −7.9/−16.4；reasoning state 跨 6 系统 +0.2–4.9。限定：文本 only、需训练信号 | [EvoMemState](../src/papers/2611.03743-evomemstate/card.md) | 支撑 04 状态派；「会用」比「检索到」更关键 |
| E-09 | SLB 的规模与干预：85% traces、24% token、77–89% 程序仍独立重算；SLB 与准确率无关联（ratio +0.1 → +0.007）；placeholders 减 SLB token **97%** 而准确率 +2.6（不降）；cautionary prompts 只减约 1/4；batching 准确率 −5.9。形式语言是最大解释变量（Python > Z3/PDDL，0.03–0.20 ratio）。限定：3 模型/4 CSP/2 FL、单次生成、闭源无 trace | [SLB](../src/papers/2611.02395-solver-like-behavior/card.md) | 支撑 06 trace；把「SLB 可移除」从推测升为已核 |
| E-10 | 本体预测机制上可干预，但无法与类别辅助信息干净分离：MDAS 最好 0.592/0.587（instance of）、0.513/0.542（subclass of）；SAE 0.412/0.371；多任务 Iso +0.081 / Cause −0.052；四层窗口 0.667。正确本体预测本身不意味着干净的内在本体；分离按类别而异 | [MIOE](../src/papers/2610.38326-mioe/card.md) | 支撑 06 mechanism；从「综述转述/推测」升为已核 |
| E-18 | **agent 评测应把配置当系统变量**：4 tasks × 432 cells × 5 runs（8,640 runs；18,240 trajectories）中，**54%** score variance 来自重复同一配置的 run-to-run 噪声；Information 轴影响 > Model > Reasoning > Budget > Verification；信息同时降成本/改善校准；预算只在信息/模型足够时有用；**验证行为靠工具不靠 prompt**（prompt 19→22%，oracle 翻三倍）；agent 99.8% 仍用弱 specialist。限定：4 tasks/2 domains、排除 memory/multi-agent | [Agents are Systems](../src/papers/2610.01618-agents-are-systems/card.md) | 支撑 06 metrics；REPLACE 单次 score 评测 |

> E-06 的论文发现是「已核」；把它推广为「漂移=输入不完备」是仓库推断，标 `推测`。两者不要混。

## 推测（未核原文）

| 编号 | 结论 | 为什么仍是推测 |
|---|---|---|
| E-11 | 训练好的检索嵌入中，前缀维度与分类法粒度对齐 | 仅读综述转述（Peeling the Matryoshka） |
| E-19 | 机制是否值得落地，取决于「位置 × 成本 × 使能条件」，不是本体质量；没有一条适用于所有机制的能力曲线（约束类随能力下降，知识投影不随容量上升） | Wave 4 综合；证据分散在 E-08/E-12/E-13/E-14/E-15/E-16/E-17 |

## 存疑

| 编号 | 结论 | 为什么存疑 |
|---|---|---|
| Q-01 | 「本体越完备效果越好」 | 与 E-01 冲突；完备性与可判定性在工程上反向 |
| Q-02 | 「多智能体优于单体」 | 缺少在同等上下文预算下的对照 |
| Q-03 | 「护栏必然提升任务表现」 | 已被 E-04 直接否证（18 格仅 8 格改善；强模型/retail 回退）；保留作反例索引，不再作为待验假设 |

## 冲突

| 冲突 | 双方 | 当前处理 |
|---|---|---|
| C-01 | 「上本体提准确率」 vs E-01 | 不做平均。假定前者成立的条件是弱 harness + 窄域；强 harness 下后者优先。待 RQ1 实验分离 |
| C-02 | Q-01「越全越好」 vs 领域实践「窄而深」 | 倾向窄而深，但缺跨域对照 |
| C-03 | 度量尺不一致 | E-01 与 E-04 都说「用准确率/reward 度量控制类机制会得出错误结论」。**这不是两个结论，是同一个方法论问题**：需按机制类型选度量 |
| C-04 | 结构化工件无增益（E-01） vs 投影文本有效（E-12） | **不矛盾**，但要说得更准：差别不只在「答案是否写在知识里」，还在**投影什么**——CAI 投影的是**证据**（claim + 逐字 span），N&D 投影的是**领域知识**（本体塔）。证据投影在需要审计/省 token 时有效；领域知识投影在答案即规则/手册时有效。判据见 [03 知识](./03-knowledge/README.md) |

C-03 是当前最有价值的一条：它把「正面证据 vs 负面证据」的文献冲突，重新解释为**度量错配**。若成立，P1 的核心论证就从「本体有用/无用」变成「该用哪把尺子」。

**能力梯度不是一条线（`推测`，Wave 1 综合）。** 约束类收益随基线能力上升而下降（E-13）；知识投影的增益**不随容量上升**（E-12，H2 p=0.85），9B 带投影 0.737 > 750B 不带 0.672。两者不矛盾：护栏**替代**判断，投影**补充**知识。待 Wave 2/3 的 CASEL、OntoAct、Grid Agents 验证。

冲突不消除，保留在表里。
