---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# Canonical：02 的阈值、计数与现役口径

> **一个数只写在这里；其他页引用，不复制。** 本页只做对账与索引，不新增判断。
>
> 读法：先看 §1 的「现役/历史」两列，再看你那条 recipe 的行。标 `工程建议` 的阈值不是论文结论；标 `gap` 的不进验收。

## 1. 三处已对账的口径

| # | 冲突 | 现役写法 | 历史/别名 | 改动 |
|---|---|---|---|---|
| 1 | false-veto 5% | **不设单点**；在给定 miss 预算下报 miss–false-block 前沿；`5%` 只作示例 | 旧写法 `false-veto ≤5%` 已从 R6/成本页移除；引用旧口径时标「历史」 | `recipes/constraint.md`、`operations/cost.md` |
| 2 | R1 门槛 | **两个不同的门**：绝对 `primary-trap avoidance ≥0.90`（验收）；相对 `K1−K0 ≥ +10pp`（立项工程门）。**预注册选一个**，不要混用 | 90% 是预登记线，不是通用阈值；+10pp 是 N&D 本域工程门 | `sections/acceptance.md`、`appendices/case.md` |
| 3 | 162 vs 149 | **162 节点** = 42 tags + 34 assumptions + 33 bindings + 24 knowledge + 16 derivations + **13 plant elements**；case 原漏了 13 plant elements，已补 | 149 = 漏算 plant elements 的旧相加 | `appendices/case.md` |

## 2. 阈值（按 recipe）

| Recipe | 主指标 | 停线/门槛 | 出处 | 量不出时 |
|---|---|---|---|---|
| R0 | 四项检查 pass/flag/unknown | 任一 `unknown` 当 pass | 工程建议（O-T01） | 改人工清单；不宣称 pass |
| R1 | primary-trap avoidance | 绝对 ≥0.90 **或** 相对 ≥+10pp（预注册） | 工程建议 + E-12（O-T02） | 先做 K0 回放；量不出停在 K1 |
| R2 | primary-trap / element | ≥+5pp；且 ≤60k 字符；≤2 人周/月 | 工程建议 + E-12（O-T03） | 先量 K1 基线；<+5pp 就停 |
| R3 | token/问、p95 | `p_h ≥ p_min = 2% + c/(0.929Q)` | E-14 / O-F01（O-T04） | 先量 `p_h`；量不出不编译 |
| R4 | 检索率、引用率、grounding | 检索 ≥50%；引用 ≥85%（**分子/分母未定义 = gap**）；grounding 未校准 → 不自动路由；预算按 **generated** tokens，9.7k 是 total，不可直接比 | 工程建议 + E-03（O-T05） | 先量检索率；<50% 先修检索 |
| R5 | 增量 catch、FA、净修复 | catch ≥5pp；FA ≤15%；净修复 >0 | 工程建议 + E-02（O-T06） | 先建空结果基线；超不过就停 |
| R6 | harm、审批、false-veto、task success | **不设 false-veto 单点**；报前沿；task success 降 ≤2pp | E-04 + 2607.22868（O-T07） | 标 gap；只 shadow，不承诺 |
| R7 | CMR、merge precision、Acc@complete | ≥+10pp；merge precision ≥90% | 工程建议 + E-05（O-T08） | 先量 merge precision；<90% 停 |
| R8 | 泄漏率、误拦 | 泄漏 0（含 object）；误拦可接受；单实现必须标 | E-20（O-T09） | 标「单实现」；不升第七时刻 |
| R9 | false-defer、unresolved、审计 | ≤20%；≤10%；可追 | 工程建议 / gap（O-T10） | 标 gap；只做设计 |
| R10 | 负例检出、干净误报 | 负例 100%；干净误报 ≤5%；三态 | E-20（O-T11） | 三态报不出就停 |
| R11 | 结果一致、时延 | 与手写 SQL 一致；需 DL/事务写入 → 停 | E-20（O-T12） | 需 DL/事务就停 |
| R12 | citation precision、strict-pass | ≥0.95；违规 0 | 工程建议 + Grid（O-T13） | 0.95 不可达就停 |

> `出处` 只许三类：`E-xx`、`O-xx`、`工程建议`。标 `gap` 的行不进验收。

### 2.1 阈值从哪来（不是「行业通常」）

| 阈值 | 来源类型 | 为什么是这个数 | 什么会推翻 |
|---|---|---|---|
| R5 catch ≥5pp / FA ≤15% | D1 工程阈值，不是 E-02 结论 | e4：data-derived 在 UniProt 真实答案 +5.7pp/FA 3.5%；curated 真实答案 FA 16.8% 超线 | 换数据源/故障分布 → 重标 |
| R6 不设 false-veto 单点 | E-04/E-15 的前沿 | block-all 零 miss 但零可用性；单点 5% 会逼出「全拦」 | 有 blocked 标签 + 同轨迹配对 |
| R1 0.90 vs +10pp | 预登记线 / 本域工程门 | 90% 是绝对目标；+10pp 是相对增益；两者不等价 | 跨域基线 |
| R7 merge ≥90% | 预登记线 | 4 settings 85.6–97.5%，部分低于 90% | 域/数据源变 |
| R3 `p_min` | 成本模型 | `2% + c/(0.929Q)`；`c=10,Q=1000` → 3.12% | 自己的 `c`/`Q`/`p_h` |
| R2 60k 字符 | 工程上限 | E-12 的投影约 45k；60k 是工程留量（`推测`），不是测量阈值 | 多设备/长文档 |

**读法**：这张表回答「凭什么用这个数」，不回答「这个数对不对」；每个数都带一个「什么会推翻」。

## 3. 计数（其他页引用这里）

| 项 | 值 | 说明 |
|---|---|---|
| recipe | 13 | R0–R12 |
| 停线表 | 13 行 × 7 列 | [acceptance §5.1](./acceptance.md#51-验收与-stop按机制选尺) |
| 反模式 | 17 | [boundaries](./boundaries.md) |
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
| 99.9% | Grid benchmark E score，不是部署 | R12 |
| 9.7k tokens | R4 的 Qwen Test 3 每问均值 | R4 |

## 5. 数字口径（读正文时）

- 正文里的阈值/效应量以本页 §2 为准；没标条件的句子，按本页的条件读。
- 交付物引 E 时，优先「`E-xx` + [evidence-anchors](../../../topics/evidence-anchors.md)」；EXP-004b：只引 E 行 strict 25%，加锚 55–65%。
- 还没逐数标条件的句子：`case` 的 `[待测]`、`boundaries` 的 −38%、`cost` 的单点 5% 已改；剩余标 `待测` 的不算通过。

## 6. 维护规则

1. 改一个阈值：先改本页，再改引用页；引用页只写「见 canonical」。
2. 新增一个数：必须带对象、条件、等级；缺一项不进本页。
3. 发现两页不一致：以本页为准；本页也不确定，标 `undetermined` 并在 §1 登记。
4. 本页不产生 E/L；所有数都来自已有页或 `topics/`。
