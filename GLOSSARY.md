# ai_dev_harness_ontology

本体与 harness 交界处的研究语境。这里的术语用于精确区分「语义层的东西」与「控制层的东西」，因为二者混淆是本领域最常见的误解。

## Language

### 结构

**Harness**:
包裹模型的那一圈工程，承担上下文供给、状态保存、动作放行、结果验证与过程观测。
_Avoid_: 框架、Agent 平台、脚手架

**本体（Ontology）**:
领域概念、关系与约束的显式规范，独立于任何一次具体的模型调用。
_origin_: `standard`（ISO/IEC 21838-1 给 TLO 的要求；我们的定义比 TLO 宽，判 `broader`）｜ _anchor_: ISO/IEC 21838-1（条款号 `待核`）｜ _scope_: 可指 TLO 或领域本体；不要把它当成「一个标准认证的领域本体」。
_Avoid_: 知识图谱（那是实例层）、分类法、词表

**顶层本体（Top-level Ontology, TLO）**:
小、通用、不含领域词的上层本体；BFO 是 ISO/IEC 21838-2 的参考 TLO。
_origin_: `standard`（ISO/IEC 21838-1/-2）｜ _anchor_: ISO/IEC 21838-1/-2（条款号 `待核`）｜ _scope_: 只定 TLO 的合格性；不覆盖领域本体、不构成成熟度分级。
_Avoid_: 通用本体（易与“通用概念库”混）、领域本体

**领域本体（Domain Ontology）**:
面向一个具体领域的概念、关系与约束；ISO/IEC 21838 不定义它。
_origin_: `local`｜ _anchor_: —｜ _scope_: 本仓库工作词；不要写成“标准认证的领域本体”。
_Avoid_: 顶层本体、全域本体

**接缝（Seam）**:
本体与 harness 发生耦合的具体位置，也是本体的语义真正转为控制的位置。
_Avoid_: 集成点、接口层、适配层

**本体塔（Ontology Tower）**:
为单一工业领域构建的窄而深的分层本体，而非跨域的大而全本体。
_Avoid_: 全域本体

**论文条件 K0–K4（不是术语）**:
Narrow & Deep 论文（arXiv:2610.11768）给自己的五个累积实验条件编的号：K0 原始点位、K1 点位语义、K2 知识投影文本、K3 流程摘要、K4 运行记录检索。**它是论文条件，不是专业术语，也不是行业标准/成熟度**；主路径用「点位语义/知识投影文本」，K 只作出处/回查。见 [K0–K4 来源说明](./deliverables/01-capability-status/sections/k-ladder.md)。
_origin_: 论文条件（I 层资料），**不是术语** ｜ _anchor_: arXiv:2610.11768 Table 1 / §2.8 ｜ _scope_: 只描述 N&D 的五个累积条件，不能推成行业层级或成熟度，也不能当本仓库术语。
_Avoid_: 知识层级、本体成熟度、K1 级本体

### 控制

**判定器（Checker）**:
依据本体对 agent 输出或轨迹做一致性判定的组件，其质量由漏检与误报的权衡刻画。
_Avoid_: 校验器、validator（与格式校验混淆）

**闸门（Gate）**:
动作执行或变更持久化之前的放行点，依据判定结果决定通过或阻断。
_Avoid_: 审批、拦截器

**提交边界（Commit Boundary）**:
「推理可用的证据」与「有权推动持久化变更的证据」之间的分界线。
_Avoid_: 审批点、写权限

**确定性锚点（Determinism Anchor）**:
同一输入多次运行时应收敛到同一产物的参照结构，用于度量漂移。
_Avoid_: 基线、ground truth（后者是标注概念）

### 证据

**接地等级（Grounding Level）**:
模型输出与其所引本体证据之间关系强度的分级，如 entailed / supported / related / unrelated。用于约束「这条结论凭什么成立」。
_Avoid_: 证据等级（与仓库的置信度分级混淆）、置信度、准确率

**证据等级（Evidence Level）**:
本仓库对一条主张的置信度分级：已证 / 已核 / 推测 / 存疑。定义见 [conventions](./meta/conventions.md#证据等级)。
_Avoid_: 接地等级、置信度

**上下文编译（Context Compilation）**:
在检索之前把原始材料预整理成结构化产物的做法，其收益可能落在上下文预算而非检索准确率上。
_Avoid_: 预计算、摘要、索引

**记忆状态（Memory State）**:
把长期记忆表示为事实之间的约束、失效与冲突关系，而非彼此独立的事实集合。
_Avoid_: 长期记忆、知识库

### 工程路径

**蒸馏（Distillation）**:
从既有 IT 系统或数据中抽取业务能力，产出可挂载能力单元的过程。
_Avoid_: 抽取、迁移

**技能包（Skill Package）**:
可被 agent 安装并调用的业务能力单元，是对模型的一次能力外挂。
_Avoid_: 插件、工具（工具粒度更细）

### 流水线

**工位（Station）**:
流水线的三个产出入库位置：`src/`（吸纳 + 精读）、`topics/`（沉淀）、`deliverables/`（交付）。吸纳与精读是 `src/` 内的两步，不是独立工位；AGENTS 的「落点」表是任务，不是工位。
_Avoid_: 阶段、环节、chapter

**台账（Ledger）**:
记录「已有什么、消化到哪、喂给了谁」的索引表，是盘点入口而非内容本身。
_Avoid_: 清单、目录、索引（与导航混淆）

**评测账本（Evaluation Ledger）**:
按每次查询或每次决策记录 token、时延、命中、审批、回滚等字段的数据表；用于计算 `p_h`、false-veto、审批成本。它记的是机制运行，不是仓库盘存。
_Avoid_: 台账（那是仓库盘点）、日志（未结构化）、指标（账本是原始记录，指标是汇总）

**消化（Digest）**:
把材料从「读过」提炼为「可被引用的判断」的过程，产物是带证据等级的结论。
_Avoid_: 总结、摘要、整理

**转述（Secondhand）**:
来自综述、二手介绍而非原文的表述，引用时必须标注并标 `待核`。
_Avoid_: 引用、参考、来源

**接缝权重（Seam Weight）**:
本仓库用于排序研究优先级的判断：某个接缝位置能改变多少条结论。权重高者先做。
_Avoid_: 优先级、重要性

**执行形态（Execution Form）**:
本体被机器使用的方式：引擎求值（engine）、编译成约束（compiled）、作为上下文注入（context）、只当标签（label）、未执行（none）。与「位置」正交。
_Avoid_: 执行方式、接入方式

**证据角色（Evidence Role）**:
一个来源对中心问题提供哪类证据：真的测了本体被执行（execution-test）、只提机制（mechanism-only）、提供 harness 证据（harness-evidence）、只做边界与尺子（boundary-ruler）。
_Avoid_: 证据等级（那是置信度）、来源类型

**失效类别（Failure Class）**:
按坏结果的类型划分的类（如不可逆动作、语义错误产出、错误落盘），不按机制、来源或论文。用于把「覆盖率」拆成可逐格反驳的分类，而不是合成百分比。见 [coverage](./topics/06-measure/metrics/coverage.md)。
_Avoid_: 失效模式（那是单个机制的失败方式）、错误类型（太泛）

**覆盖率（Coverage）**:
某个位置能碰到的失效类别集合；本仓库只做分类（`●` 能阻断 / `◐` 能发现或部分影响 / `○` 碰不到 / `?D` 只有设计），不合成单一百分比。它是组织假设的操作化，不是测量。
_Avoid_: 召回率、命中率、覆盖率百分比

**执行链（Enforcement Chain）**:
本体在 harness 里的五层工序：求值（evaluate）→ 决策（decide）→ 执行（enforce）→ 授权（authorize）→ 审计（audit）。用于区分「机器算出了什么」与「机器有没有权改变世界」；见 [execution-forms](./topics/execution-forms.md#执行链求值决策执行授权审计)。
_Avoid_: 调用链（那是代码路径）、流水线（那是仓库工位）

**工程配方（Recipe）**:
`deliverables/02-engineering-playbook` 里的 R0–R12：回答「怎么做」，不回答「做了有没有用」。它不是 E；效应量仍以 `E-xx` 为准。
_Avoid_: 结论、最佳实践

**Primary-trap avoidance**:
在预先标出的「最常掉进去的坑」上不犯错的 trial 比例；与 element score 分开报，避免总分掩盖 trap 没动。见 [R1/R2](./deliverables/02-engineering-playbook/recipes/knowledge.md)。
_Avoid_: 准确率、总分

**False veto / false denial**:
被 gate 拦下、但本可合法执行且低 harm 的动作比例；没有授权/伤害标签就不能算。与 retention、block count 区分。见 [R6](./deliverables/02-engineering-playbook/recipes/constraint.md)。
_Avoid_: 误报率（那是 checker 口径）、拦截率

**`p_h` / `p_min`**:
`p_h` 是证据充分、可替换的查询比例；`p_min = 2% + c/(0.929Q)` 是编译的盈亏平衡。`p_h` 不是答对率（φ 另算）。见 [R3](./deliverables/02-engineering-playbook/recipes/knowledge.md)。
_Avoid_: 命中率、准确率


**证据锚（Evidence anchor）**:
`E-xx` 行之外的「承重数/条件 + digest 节」地址，集中放 [topics/evidence-anchors](./topics/evidence-anchors.md)。它不产生结论；用途是让交付物引 E 时能落到具体节，而不是只写 `E-xx`。EXP-004b：只引 E 行时 citation strict support 25%，加锚后 55–65%。
_Avoid_: 新 E、digest 摘要
