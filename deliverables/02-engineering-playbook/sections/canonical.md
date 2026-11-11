---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# Canonical：02 的阈值、计数与现役口径

> **阈值与判定口径只在这里定义；其他页引用数值时不另立口径。** 本页只做对账与索引，不新增判断。
>
> **2026-11-11 证据重置**：R4/R5/R6/R12 的原锚已撤回/移出；下表这 4 行只作历史，不再设门槛。R1/R2/R3/R7/R8/R10/R11 的阈值仍有效；R9 只有设计。
>
> 读法：先看 §1 的「现役/历史」两列，再看你那条 recipe 的行。标 `工程建议` 的阈值不是论文结论；标 `gap` 的不进验收。

## 1. 三处已对账的口径

| # | 冲突 | 现役写法 | 历史/别名 | 改动 |
|---|---|---|---|---|
| 1 | false-veto 5% | **不设单点**；在给定 miss 预算下报 miss–false-block 前沿；`5%` 只作示例 | 旧写法 `false-veto ≤5%` 已从 R6/成本页移除；引用旧口径时标「历史」 | `recipes/constraint.md`、`operations/cost.md` |
| 2 | R1 门槛 | **两个不同的门**：绝对 `primary-trap avoidance ≥0.90`（验收）；相对 `K1−K0 ≥ +10pp`（立项工程门）。**预注册选一个**，不要混用 | 90% 是预登记线，不是通用阈值；+10pp 是 N&D 本域工程门 | `sections/acceptance.md`、`appendices/case.md` |
| 3 | 162 vs 149 | **162 节点** = 42 tags + 34 assumptions + 33 bindings + 24 knowledge + 16 derivations + **13 plant elements**；case 原漏了 13 plant elements，已补 | 149 = 漏算 plant elements 的旧相加 | `appendices/case.md` |

## 1.1 撤回与历史（W 表）

> **用途**：把「哪条依据没了、没了之后怎么重启」集中到一处；正文只写 `W-xx`，不再逐句解释撤回。
>
> **`重启前先量` 是测量设计（`工程建议`），不是效应量**：阈值是本仓库的工程默认，不是从论文搬来的结论。
>
> **标注人力（`推测`）**：R5 200 题 × 2 人 + 裁决 ≈ 3–5 人日；R4 四级各 100–200 ≈ 6–10 人日；R6 100 条 blocked ≈ 1–2 人日；R9 20–50 条 ≈ 0.5–1 人日。先算人力再开跑。

<a id="w-table"></a>
| 编号 | 原依据 | 状态 | 不能再用 | 重启前先量（最小自测） | 对应 |
|---|---|---|---|---|---|
| **W-01** | E-02 Ontology Catch | withdrawn | catch/FA、空结果重试、precision、净修复 | **200 题分层**（类型/声明/语义各 ≥50）；catch/FA/净修复分开；per-flagged（token 或人时）。工程建议：catch ≥+5pp、FA ≤15%、净修复 >0 | R5 |
| **W-02** | E-03 OA-RAG | withdrawn | 检索率、引用率、等级校准、调用/token | **200 题**；gold evidence 检索率 ≥50%、引用率 ≥85%；每级 100–200 条独立标注报 precision/recall | R4 |
| **W-03** | E-04/E-13 POLAR | withdrawn | 18 格、T1-only、false-veto、能力梯度 | **shadow 200–500 决策**；100 条 blocked 标 harm/授权；同轨迹配对；报 miss–false-block 前沿（不设单点） | R6 |
| **W-04** | E-16 OntoAct | withdrawn | 三值条件效应、无效干预率 | **≥100 条**带前提的决策；先测三值覆盖率（⊤/⊥/?）；? 比例 >30% 先补状态 | 边界 |
| **W-05** | Grid（2611.03534） | 移出 | 99.9%、citation recall、拒答数、时延 | **20–50 个 held-out**；citation precision ≥0.95（工程建议）、strict-pass 漏报 0、拒答可解释、solver 版本可追 | R12 |
| **W-06** | Commit Boundary | 移出 | promotion 七条、三段式「已核」 | **1 个 mutation class**；20–50 条 false-defer；审计字段齐；无回滚/重入只做影子 | R9 |
| **W-07** | SFE-O | 移出 | 「表达≠执行」的「已核」评级、成本估算出处 | 成本按**你第一个 sprint 的实录工时**；表达≠执行按 R0 检查 4 自己验（约束有无 shape + 负例） | R0 / 04 成本 |

> 每一条撤回都配一个「怎么用你自己的数据重新得到答案」；没有这一列，撤回就只剩免责。

## 2. 阈值（按 recipe）：一张表，带「为什么/什么会推翻」

| Recipe | 主指标 | 停线/门槛 | 出处 | 量不出时 | 为什么是这个数 | 什么会推翻 |
|---|---|---|---|---|---|---|
| R0 | 四项检查 pass/flag/unknown | 任一 `unknown` 当 pass | 工程建议（O-T01） | 改人工清单 | 最低准入集；无对照 | 有对照研究 |
| R1 | primary-trap avoidance | 绝对 ≥0.90 **或** 相对 ≥+10pp（预注册） | 工程建议 + E-12（O-T02） | 先做 K0 回放 | 绝对目标 vs 相对增益，两者不等价 | 跨域基线 |
| R2 | primary-trap / element | ≥+5pp；≤60k 字符；≤2 人周/月 | 工程建议 + E-12（O-T03） | 先量 K1 基线 | E-12 投影约 45k；上限是工程留量（`推测`） | 多设备/长文档 |
| R3 | token/问、p95 | `p_h ≥ p_min = 2% + c/(0.929Q)` | E-14 / O-F01（O-T04） | 先量 `p_h` | 成本模型；`c=10,Q=1000` → 3.12% | 自己的 `c`/`Q`/`p_h` |
| R4 **gap** | 检索率、引用率、grounding | **按 W-02 重测；原门槛作废** | E-03 withdrawn | 200 题 + 每级 100–200 标注 | 先修检索，再谈等级 | 新源 + 校准 |
| R5 **gap** | 增量 catch、FA、净修复 | **按 W-01 重测；原门槛作废** | E-02 withdrawn | 200 题分层 + 净修复 | 空结果重试基线要在本域重跑 | 新源 + 故障分布 |
| R6 **gap** | harm、审批、false-veto、task success | **按 W-03 重测；原门槛作废** | E-04/E-13 withdrawn；E-15 仅参照 | shadow 200–500 + 100 blocked | 先标 blocked，再谈阈值 | 新源 + blocked 标签 + 同轨迹配对 |
| R7 | CMR、merge precision、Acc@complete | ≥+10pp；merge precision ≥90% | 工程建议 + E-05（O-T08） | 先量 merge precision | 预登记线；4 settings 85.6–97.5，部分低于线 | 域/数据源变 |
| R8 | 泄漏率、误拦 | 泄漏 0（含 object）；误拦可接受；单实现必须标 | E-20（O-T09） | 标「单实现」 | fail-open/只删 subject 是设计边界，不是 bug | 第二实现/异常注入 |
| R9 | false-defer、unresolved、审计 | ≤20%；≤10%；可追 | 工程建议 / gap（O-T10） | 标 gap；只做设计 | 无实现；阈值是工程建议 | 有实现 + false-defer 标签 |
| R10 | 负例检出、干净误报 | 负例 100%；干净误报 ≤5%；三态 | E-20（O-T11） | 三态报不出就停 | 三态不可折叠；派生 shapes 质量未测 | 三态报不出就停 |
| R11 | 结果一致、时延 | 与手写 SQL 一致；需 DL/事务写入 → 停 | E-20（O-T12） | 需 DL/事务就停 | OWL 2 QL 是范围，不是闸 | 需 DL/事务就停 |
| R12 **gap** | citation precision、strict-pass | **按 W-05 重测；原门槛作废** | Grid 已移出 | 20–50 held-out + 签核记录 | 换域必须重测 | 真实运营商/客户指标 |

> `出处` 只许三类：`E-xx`、`O-xx`、`工程建议`。标 `gap` 的行不进验收。
>
> `为什么` 列是解释层，不是新 E；01 工作底稿的 e4 旧 catch/FA 数字（E-02 撤回）已停用、不再给值，只留 [01 data/e4](../../01-capability-status/data/e4-checker.md) 作历史。**这张表是阈值的唯一定义处**；其他页引用数值，不另立口径。

## 2.2 深度分层（L1/L2/L0）

| 层 | 条 | 说明 |
|---|---|---|
| **L1** | R5、R6、R8 | ≥200 字机制箱：机制链 + 条件 + 反例 + 决策 |
| **L2** | R0、R1、R2、R3、R4、R7、R9、R10、R11、R12 | 一句 why（≤180 字）或阈值来源 |
| **L0** | 无 | — |

> 不再报「13/13 都有 why」；报 **3 L1 / 10 L2 / 0 L0**。

## 3. 计数（其他页引用这里）

| 项 | 值 | 说明 |
|---|---|---|
| recipe | 13 | R0–R12 |
| 停线表 | 13 行 × 7 列 | [acceptance §5.1](./acceptance.md#51-验收与-stop按机制选尺) |
| 反模式 | 18 | [boundaries](./boundaries.md) |
| per-R「不能证明」 | 13 | [traceability §2](../appendices/traceability.md) |
| 缺口 | 9 | [acceptance §5.2](./acceptance.md#52-还缺什么) |
| 读者检查 | 5 组 | [acceptance §5.4](./acceptance.md#54-读者检查5-组) |
| 产物包 | 7 件 | [artifact-pack](../appendices/artifact-pack.md) |

## 4. 高频数（只列口径，不重复解释）

| 值 | 指什么 | 出现处（引用，不复制） |
|---|---|---|
| +54.6pp | K0→K1 primary-trap avoidance，单工厂 | R1 / case / 01 |
| +19.8pp | K1→K2，单工厂 9 任务 | R2 / case / 01 |
| −38% | 编译平均 token 变化的混合值（−91% 与 +1.9%） | R3 |
| 60k | 投影字符上限 | R2 |
| Grid 旧 E score | **历史**：Grid 已移出（W-05），数值不再引用 | R12 |
| R4 旧 token 均值 | **历史**：E-03 撤回（W-02），数值不再引用 | R4 |

## 5. 数字口径（读正文时）

- 正文里的阈值/效应量以本页 §2 为准；没标条件的句子，按本页的条件读。
- 交付物引 E 时，优先「`E-xx` + [evidence-anchors](../../../topics/evidence-anchors.md)」；EXP-004b：只引 E 行 strict 25%，加锚 55–65%。
- 还没逐数标条件的句子：`case` 的 `[待测]`、`boundaries` 的 −38%、`cost` 的单点 5% 已改；剩余标 `待测` 的不算通过。

## 6. 维护规则

1. 改一个阈值：先改本页，再改引用页；引用页只写「见 canonical」。
2. 新增一个数：必须带对象、条件、等级；缺一项不进本页。
3. 发现两页不一致：以本页为准；本页也不确定，标 `undetermined` 并在 §1 登记。
4. 本页不产生 E/L；所有数都来自已有页或 `topics/`。