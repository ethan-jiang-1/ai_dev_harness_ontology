---
status: draft
updated: 2026-11-11
type: term-baseline
scope: ADR 0011 §S3 v0（10 词）+ v1（29 词 + 06 试点 1 词）
---

# 术语差异表 v0/v1：先标来源，再谈定义

> 依据 [ADR 0011](../../adr/0011-source-standing-and-term-baseline.md) 与 [基线整改计划](../archive/2026-11/plans/2026-11-11-baseline-correction-plan.md)。**本表只做判定与动作，不新增 E/L。**
>
> **v0 范围**：10 个高频词；**v1 范围**：GLOSSARY 里 v0 未判的其余 29 词 + 06-measure 试点发现的 1 个裸词。**未读标准正文的条款号一律写 `待核`**；`local` 不是“错”，是“本仓库自造/限定义”，必须首现解释、不得写成行业标准。
>
> **主干索引**：N（规范性）标准与「能/不能定义什么」见 [topics/trunk.md](../../topics/trunk.md)；本表判词的来源与动作。

## 0. 规则（与 ADR 0011 一致）

- `origin`：`standard` / `academic` / `local`；只有 `standard` 可定术语与合格性。
- 判定五类：`aligned`（换锚）/ `narrower`（标范围）/ `broader`（拆开）/ `divergent`（改名或限定）/ `local`（标自造）。
- **偏移阈值**：`divergent` + **冒充行业词的** `local` 合计 > 1/3 → 停，重定基调；本表 `local` 都显式标注，不算“冒充”。
- 标准卡只定词与合格性，不撑效应量。

## 1. 十词 v0

| 词 | 我们现在的定义 | 标准锚 | origin | 判定 | 动作 | 状态 |
|---|---|---|---|---|---|---|
| **本体** | 领域概念、关系与约束的显式规范 | ISO/IEC 21838-1（TLO 要求；条款号 `待核`） | `standard` | `broader` | 保留通用义；**顶层本体**另列标准义；领域本体标 `local`，不要拿 TLO 标准给领域塔发合格证 | v0 |
| **顶层本体** | 小、通用、不含领域词的上层本体 | ISO/IEC 21838-1/-2（BFO 为参考 TLO；条款号 `待核`） | `standard` | `aligned` | 用标准义；不要与「本体塔 / domain tower」混用 | v0 |
| **领域本体** | 面向一个领域的概念/关系/约束 | ISO/IEC 21838 **不定义**领域本体 | `local` | `local` | 标 local；首现解释；不要写成“标准认证的领域本体” | v0 |
| **知识图谱** | 实例层的事实图，区别于本体（概念层） | 本仓库无 normative 锚 | `local` | `local` | 只作描述词；不要拿它定义“本体”；要定义先引 academic/standard 源 | v0 |
| **语义层** | 把领域语义叠到数据/接口上的那一层 | 本仓库无 normative 锚 | `local` | `local` | 标 local；不与“本体”同义使用 | v0 |
| **成熟度** | 组织能力分级 | 本仓库无 normative 锚；EKGF 判 `excluded` | `local` | `local` | **禁止**写成“行业成熟度标准”；只作组织讨论词 | v0 |
| **知识层级** | 曾用来指 K0–K4 | 论文实验条件，不是标准；见 [K 页](../../deliverables/01-capability-status/02-sections/92-k-ladder.md) | `local` | `local` | 改叫「论文条件」；不写“层级/等级”；**不作为术语，只作出处/回查** | v0 |
| **接地（grounding）** | 输出与本体证据之间的关系强度 | 本仓库无 normative 锚；E-03 已撤回 | `local` | `local` | 只作机制词；不引旧效应量；首现解释 | v0 |
| **数据产品** | 可交付、可治理的数据/知识产物 | 本仓库无 normative 锚 | `local` | `local` | 标 local；不要写成标准术语 | v0 |
| **约束** | 对数据/查询/动作的前置条件 | W3C SHACL（RDF 图约束；SHACL Core 为 W3C Recommendation） | `standard` | `narrower` | 标准义只到 RDF 图约束；动作前授权/闸门另标 local，不能拿 SHACL 证明“会拦动作” | v0 |

## 2. 二十九词 v1（GLOSSARY 剩余词）

> **判定口径同 v0**：`origin` = `standard` / `academic` / `local`；`verdict` = `aligned` / `narrower` / `broader` / `divergent` / `local`。
>
> **`academic` 锚不是 normative 锚**：论文/文献只给「谁这样用」，不能给「行业合格证」；锚未入卡的，按 `local` 用，不得写成标准。

| 词 | 我们的定义 | 锚 | origin | 判定 | 动作 |
|---|---|---|---|---|---|
| **Harness** | 包住模型的那圈工程：上下文供给、状态保存、动作放行、结果验证、过程观测 | 无标准；社区工程词 | `local` | `local` | 首现解释；不写成「平台/框架」的标准名 |
| **接缝（Seam）** | 本体与 harness 耦合、语义转为控制的位置 | 无标准锚 | `local` | `local` | 首现解释；不与「接口/集成点」混 |
| **本体塔（Ontology Tower）** | 为单一工业领域构建的窄而深分层本体 | N&D 论文用语（arXiv:2610.11768，章节 `待核`） | `academic` | `local` | 写「一台设备的窄而深结构」；不写成行业分级 |
| **判定器（Checker）** | 依据本体判定 agent 输出/轨迹一致性的组件，质量由漏检与误报刻画 | SHACL 只定「图校验」，不定 checker 的效应 | `local` | `narrower` | 标准义只到约束/校验；catch/FA 是 `local` 口径 |
| **闸门（Gate）** | 动作执行或持久化前的放行点 | XACML 的 PEP 是最近的标准概念，但不等价 | `local` | `local` | 不把 gate 写成 XACML 术语；机制义首现解释 |
| **提交边界（Commit Boundary）** | 「可推理证据」与「有权推动持久化证据」的分界 | 原论文已 `excluded` | `local` | `local` | 只作机制词；不引已删源 |
| **确定性锚点（Determinism Anchor）** | 同一输入多次运行应收敛到的参照结构 | 无标准 | `local` | `local` | 首现解释；不与 baseline/ground truth 混 |
| **接地等级（Grounding Level）** | 输出与本体重证据的关系强度分级 | 无标准；原 E-03 锚已撤回 | `local` | `local` | 只作机制词；不引旧效应量；等级是模型自评 |
| **证据等级（Evidence Level）** | 本仓库置信度分级：已证/已核/推测/存疑 | 本仓库规则（conventions） | `local` | `local` | 不与 var/置信度/接地等级混 |
| **上下文编译（Context Compilation）** | 检索前把原始材料预整理成结构化产物 | 无标准；OBDA 的 query compilation 不同义 | `local` | `local` | 首现解释「检索前预整理」；不与查询编译混 |
| **记忆状态（Memory State）** | 长期记忆表示为事实间约束/失效/冲突 | 无标准 | `local` | `local` | 首现解释；不与「知识库」同义 |
| **蒸馏（Distillation）** | 从既有 IT 系统/数据抽取可挂载能力单元 | ML 的 knowledge distillation（不同义） | `academic` | `divergent` | **改名或限定**：首现写「能力蒸馏（从系统抽能力）」；不写成模型蒸馏 |
| **技能包（Skill Package）** | 可被 agent 安装调用的业务能力单元 | 社区词（Agent Skills），未入卡 | `local` | `local` | 首现解释；不写成行业标准/插件市场规范 |
| **工位（Station）** | `src/`→`topics/`→`deliverables/` 三个入库位置 | 无标准 | `local` | `local` | 只在本仓库流水线语境用；不写成「阶段」 |
| **台账（Ledger）** | 「已有什么/消化到哪/喂给谁」的索引表 | 无标准 | `local` | `local` | 与「评测账本」分写；不是会计台账 |
| **评测账本（Evaluation Ledger）** | 按 query/decision 记录 token、时延、命中、审批、回滚的数据表 | 无标准 | `local` | `local` | 首现解释；账本是原始记录，指标是汇总 |
| **消化（Digest）** | 从「读过」提炼为「可引用的判断」 | 无标准 | `local` | `local` | 首现解释；不是摘录/总结 |
| **转述（Secondhand）** | 来自综述/二手介绍的表述，引用须标 `待核` | 无标准 | `local` | `local` | 首现解释；与「引用/来源」区分 |
| **接缝权重（Seam Weight）** | 某接缝能改变多少条结论（排序用） | 无标准 | `local` | `local` | 首现解释；不是优先级/重要性 |
| **执行形态（Execution Form）** | engine / compiled / context / label / none | 无标准；与「位置」正交 | `local` | `local` | 首现解释五种；不把 context 当 engine 低配 |
| **证据角色（Evidence Role）** | execution-test / mechanism-only / harness-evidence / boundary-ruler | 无标准；本仓库字段 | `local` | `local` | 与「证据等级」分开；字段定义见 conventions |
| **失效类别（Failure Class）** | 按坏结果类型分类（不可逆动作、语义错、错落盘…） | 无标准 | `local` | `local` | 与「失效模式」分开：类别 vs 单机制失败方式 |
| **覆盖率（Coverage）** | 某位置能碰到的失效类别集合（`●/◐/○/?D`） | 无标准；与测试覆盖率不同义 | `local` | `local` | 只作分类，不合成百分比；不写成召回率 |
| **执行链（Enforcement Chain）** | 求值→决策→执行→授权→审计五层工序 | 无标准 | `local` | `local` | 与「调用链」分开；见 execution-forms |
| **工程配方（Recipe）** | `02` 的 R0–R12：回答怎么做，不回答有没有用 | 无标准 | `local` | `local` | 不是 E；不写成最佳实践 |
| **Primary-trap avoidance** | 预注册「主要坑」上不犯错的 trial 比例 | N&D 论文（arXiv:2610.11768 Table 1/§2.8） | `academic` | `aligned` | 引论文条件；中文写「避坑率」；单工厂 9 任务 |
| **False veto / false denial** | 被 gate 拦下、但本可合法执行且低 harm 的比例 | 原 POLAR（E-04 已撤回） | `academic` | `local` | 锚已撤回；无 harm/授权标签就写 `unknown`，不算比例 |
| **`p_h` / `p_min`** | 可替换查询比例 / 编译盈亏平衡 `2% + c/(0.929Q)` | 本仓库公式（E-08/E-14） | `local` | `local` | 自己的 `c/Q` 没量不能套；不是答对率 |
| **证据锚（Evidence Anchor）** | `E-xx` 之外的「承重数/条件 + digest 节」地址 | 本仓库机制（ADR 0009） | `local` | `local` | 不产生结论；只让引用落节 |

## 3. 计数与风险

| 判定 | v0 | v1 | 合计 | 备注 |
|---|---|---|---|---|
| `aligned` | 1 | 1 | 2 | 顶层本体；避坑率（论文原义） |
| `narrower` | 1 | 1 | 2 | 约束；判定器 |
| `broader` | 1 | 0 | 1 | 本体（比 TLO 标准宽） |
| `divergent` | 0 | 1 | 1 | 蒸馏（与 ML 蒸馏不同义） |
| `local` | 7 | 26 | 33 | 均显式标注；不冒充行业词 |

> **v0/v1 的结论**：40 词里只有 2 词有 `standard` 锚（本体、顶层本体），另 2 词有 `narrower` 的标准义（约束、判定器）；其余是本仓库工作词或已撤回的 academic 锚。这不代表“没救”，代表**它们只能作本仓库的工作词**：交付物首现处必须解释；对外文档不要把它们写成行业共识。
>
> **风险点**：`divergent` 只有 1 个（蒸馏），但真正危险的是「看起来像标准词、实际是自义」的 `local`——**判定器、闸门、覆盖率、执行形态**最容易被人当成行业术语。对外时一律带「本仓库」或改用描述句。

## 4. 与交付物的接口

- 01 的 K0–K4 已按 `local` 处理（[K 页](../../deliverables/01-capability-status/02-sections/92-k-ladder.md)）；**K0–K4 本身不是术语，不列入词表**；本表「知识层级」行只用于回查旧说法。
- 01/02/03/04 的术语页与首现定义已按 v0/v1 判定改：四个术语页都有「§0 名词从哪来（N / local）」表；正文定义句用 `（N: 标准名）` 或 `（local）` 标注。**只改定义段/首现/锚点，不重写结构。**（04 的术语页已随 [ADR 0015](../../adr/0015-retire-04-and-renumber-05-to-10.md) 退役，其余三份不变。）
- 标准卡 `standing` 已补到 10 张标准卡；HN 是 `engineering`，不标 `standing`。

## 5. 06-measure 试点与冲突记录

> 试点对象：[06-measure README](../../topics/06-measure/README.md)、[claims](../../topics/06-measure/claims.md)、[metrics/coverage](../../topics/06-measure/metrics/coverage.md)。**只查术语用法，不改判断。**

| 位置 | 用法 | 判定 | 动作 |
|---|---|---|---|
| 06-L1 / 06-L6 | 「本体预测」「本体接地失败」 | 「接地」= `local`（无标准锚；E-03 已撤回） | 保留机制词；首现已由 03 evidence/glossary 解释；**不引旧效应量** |
| 06-L6 / 06-L7 | 「五角色 + 七变量」 | 本仓库框架（`local`） | L6/L7 已 `withdrawn`；不得当术语或预测器 |
| 06-L15 | 「覆盖率」按七类失效 × 八位置分类、不合成百分比 | 与 GLOSSARY 的 `local` 定义一致（`aligned`） | 保留；对外链 [coverage](../../topics/06-measure/metrics/coverage.md) |
| 06-L16 / 03 measurement | 「任务账 / 风险账」 | **裸词**：GLOSSARY 无此条，但 14 处使用 | **v1 补判**：`local`，无标准锚；首现解释「用任务成功率记账 vs 用 harm/风险记账」；已写入 §6 |
| 06 README §双重身份 | 「判定器」 | 与 v1 判定一致：`narrower`（SHACL 只定图校验） | 保留；不写成「SHACL 判定器」 |
| 06-L13 | 「落地经济学」 | 本仓库综合词（`local`） | 只在本仓库语境用；不写成学科名 |

> **试点结论**：06-measure 没有把 `local` 词冒充行业标准；真正需要补的是「任务账/风险账」这条裸词（已补）。术语冲突 0 条，**不新建审计整改项**；逐条记录见 [术语审计](../audits/2026-11-11-term-baseline.md)。

## 6. 待核 / 下一版

- [ ] ISO/IEC 21838-1/-2 的具体条款号（当前只到目录摘要）。
- [ ] 知识图谱、语义层、数据产品、接地：是否值得引 academic 源；若引，改 `origin` 并给 anchor。
- [ ] 「任务账 / 风险账」补进 GLOSSARY（v1 已判 `local`，词条待写）。
- [ ] 术语冲突再扫：`topics/*/claims.md` 的裸词（下一轮用同一 06 试点方法，按派抽样）。

> 本表是工作稿，不是标准；引用时带「本仓库术语基线 v0/v1」。
