---
status: draft
source_type: standard
standing: normative
reading: 精读
provenance: 原文正文
updated: 2026-11-11
batch:
source: https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.html
author: OASIS XACML Technical Committee
published: 2013-01-22
influence: OASIS Standard（2013-01-22），ABAC 的参照规范；PAP/PDP/PEP/PIP 与 combining algorithm 已是策略引擎与访问控制文献的通用术语（具体产品采用清单 待核）
updates: []
admission: admitted
gate_checked: 2026-11-11
impact_evidence: "I1: OASIS Standard in force"
liveness: standard-in-force
provenance_type: standard-body
---

# OASIS XACML 3.0 Core（eXtensible Access Control Markup Language）

> 标准卡，不是 digest。全文 HTML（1.2 MB）已抓取；正文节号取自该版目录，可点回原文逐字核对。
> 精读范围限于 §3.1、§3.3、§5.10–5.13、§5.22、§5.39–5.40、§7.2、§7.10–7.11、§7.18、附录 C.1–C.9；数据类型、函数库、各类 profile 未读。

## 它主张什么

1. **策略写、决策、执行、取属性是四个角色，PDP 不做拦截。** PAP 写 policy / policy set 并使其对 PDP 可用；请求方把请求发给 PEP，PEP 交给 context handler，由它向 PIP 取属性、拼成 XACML request context 交 PDP 求值；PDP 只返回 `Permit` / `Deny` / `Indeterminate` / `NotApplicable`（可带 obligation / advice），最后由 PEP 执行访问并履行 obligation（§3.1、§7.2）。
2. **策略是三层套娃，冲突由显式指定的合并算法解决，不是靠规则顺序自然产生。** Rule = target + effect + condition，Policy = rules + rule-combining algorithm，PolicySet = policies + policy-combining algorithm；`deny-overrides` / `permit-overrides` / `first-applicable` / `deny-unless-permit` / `permit-unless-deny` 等算法决定冲突与「不匹配时算什么」（§3.3、附录 C）。
3. **义务按 effect 挂载、版本靠模式匹配，两者都把执行与解析留给实现。** `ObligationExpression` 的 `FulfillOn` 与 `AdviceExpression` 的 `AppliesTo` 取值只能是 `Permit` / `Deny`，只有求值路径的最终结果与之匹配时才上传到 PEP；`Version` 是 Policy/PolicySet 的必填属性，引用侧用 `Version` / `EarliestVersion` / `LatestVersion` 做 `*` / `+` 通配匹配，但版本解析与排序不在规范范围内（§5.10–5.13、§5.39–5.40、§7.18）。

### 机制速查：四个角色（§3.1）

| 角色 | 规范给的职责 | 规范**没**给的 |
|---|---|---|
| PAP | 写 policy / policy set，使其对 PDP 可用 | 谁能写策略、审批流、策略来源 |
| PEP | 发 decision request；执行访问；履行 obligation | 拦在哪个调用点、拦不住怎么办 |
| context handler | 原生请求 ↔ XACML context；向 PIP 要属性 | 部署位置、通信协议（原文：不限制 repository 位置、不规定 data-flow 协议） |
| PIP | 属性值来源 | 属性怎么产生、可不可信 |
| PDP | 求值并返回 decision(+obligations/advice) | **不执行**；`NotApplicable` / `Indeterminate` 时 PEP 的行为由 PEP bias 定（§7.2） |

### 机制速查：Rule → Policy → PolicySet（§3.3）

| 元素 | 组成 | 关键约束 |
|---|---|---|
| Rule | target + effect + condition + obligation/advice 表达式（§3.3.1） | effect 只有 `Permit` / `Deny`（§5.22 `EffectType`）；rule 不能单独在实体间交换，必须包进 policy（§3.3.1） |
| Policy | target + `RuleCombiningAlgId` + rules + obligation/advice 表达式（§3.3.2） | 规则**必须**由该算法合并（§5.14） |
| PolicySet | target + `PolicyCombiningAlgId` + policies / policy sets + obligation/advice 表达式（§3.3.3） | 可嵌套；算法标识必填 |

### 机制速查：合并算法（附录 C）

| 算法 | 结果（条文的 informative 描述） | 全都不适用时 |
|---|---|---|
| `deny-overrides`（C.2） | 任一 Deny → Deny；否则按 `Indeterminate{DP/D/P}` 回 Indeterminate；否则任一 Permit → Permit | `NotApplicable` |
| `permit-overrides`（C.4） | 任一 Permit → Permit；否则按 Indeterminate 回；否则 Deny | `NotApplicable` |
| `first-applicable`（C.8） | 按列出顺序，第一条 target 匹配且 condition 为 True 的规则立即生效并终止 | `NotApplicable` |
| `deny-unless-permit`（C.6） | 任一 Permit → Permit；否则 Deny | 不产生（刻意消除 Indeterminate / NotApplicable，常用于顶层保证 PDP 一定返回 Permit/Deny） |
| `permit-unless-deny`（C.7） | 任一 Deny → Deny；否则 Permit | 不产生 |
| `ordered-deny-overrides` / `ordered-permit-overrides` / `only-one-applicable`（C.3 / C.5 / C.9） | 前两者按规则顺序取第一个决定性结果（用于需要确定性的场景，§7.18 明确建议）；`only-one-applicable` 仅在恰好一个 policy 适用时返回其结果，多于一个 → Indeterminate | 见各节 |

> 附录 C 每节的条文都写明：算法行为描述是 **non-normative informative**，规范性在后面的伪码；引用行为描述时按说明性材料处理。

### Obligation / Advice（§5.39–5.40、§7.18）

- **Obligation** 是「PEP 在强制执行决定时应执行的动作」；**Advice** 可被 PEP 安全忽略（§3.3.3.3、§5.40）。
- `FulfillOn` 是 `<ObligationExpression>` 的**必填**属性，类型为 `EffectType`，取值只有 `Permit` / `Deny`（§5.22、§5.39）→ **Obligation 可以挂在 Deny 上**，这是规范直接支持的能力，不是推测。
- 上传规则（§7.18）：只有被求值元素的结果与 `FulfillOn` / `AppliesTo` 匹配，obligation 才向上传递；路径上任何一层的结果与最终 decision 不一致，该路径的 obligation 不返回。若匹配的 obligation 里任一 `AttributeAssignmentExpression` 求值为 `Indeterminate`，整个 rule/policy/policy set 变 `Indeterminate`。
- 履行规则（§7.2.1）：决定为 Deny 且带 obligation 时，PEP **只有**在「理解、且能且愿意履行」时才 deny；否则按 PEP bias 处置（§7.2.2 deny-biased：除 Permit 外全部拒；§7.2.3 permit-biased：除 Deny 外全部放行）。
- 规范不定义 obligation 的语义、不定义义务失败的具体后果（只说按 PEP bias）、不给审计字段。

### Version / VersionMatch（§5.10–5.13）

- `Version` 是 `<Policy>` / `<PolicySet>` 的**必填**属性，格式 `(\d+\.)*\d+`（§5.12）。
- `<PolicyIdReference>` / `<PolicySetIdReference>` 可带 `Version` / `EarliestVersion` / `LatestVersion`，三者可任意组合，同时出现时被引用的策略**必须全部匹配**；都不写则任何版本可接受（§5.10）。
- 匹配值同为点分模式 `((\d+|\*)\.)*(\d+|\*|\+)`：数字是直接数值匹配，`*` 匹配任意单个数字，`+` 匹配任意数字及其后所有数字；`1.2.3`、`1.*.3`、`1.2.*`、`1.+` 都能匹配版本串 `1.2.3`（§5.13）。
- 多个版本都可匹配时「most recent」**SHOULD** 被使用（§5.10）——但「most recent 怎么排序」规范没定义；而且 reference → policy 的**解析机制「outside the scope of this specification」**（§5.11）。所以 XACML 给的是版本语法 + 匹配模式，不是版本快照/回放。

## 场景与 scope

- 规范对象是 ABAC 的**通用策略语言 + 求值模型**，刻意与传输协议、存储、策略管理流程解耦：§3.1 明说不限制 repository 位置、不规定 data-flow 的通信协议；§5.11 明说引用解析不在范围内。
- 覆盖「策略怎么求值」；不覆盖「策略从哪来」「属性可不可信」「执行点布在哪」「义务怎么真做到」——这四件事在本仓库正是 04 C.1 的三层分离要处理的部分。
- 04 的场景（单企业、**假设** 200 表 / 5,000 列；Glyph 的真实量级是 ~98k 表 / ~3.4M 列，E-22；读路径 post-filter、一条会 fail-open 的查询改写）比 XACML 的模型窄：XACML 预设存在独立 PDP 和一个**能履行 obligation 的 PEP**，04 的执行层没有这两个前提。
- 本卡只对「规范条文怎么写」作判断；对「某实现/某产品是否照此实现」不作判断。

## 证据强度

- **一手还是转述**：一手正文（OASIS 官方 HTML，OASIS Standard，2013-01-22）。
- **有数据吗**：没有，也不该有——标准是规范文本，不是效果证据。
- **数据规模与场景**：N/A（无实现、无部署、无对照实验）。
- **可复现吗**：条文可逐字复核，节号可点回原文；附录 C 的规范性部分是可执行的伪码。**不可**由此推出任何实现行为。
- **等级**：条文本身 `已核`（逐字引原文、节号真实）；「XACML 语义能直接套到 04 policy 表」`待核`（见下）；「某产品按 XACML 语义」本卡不写，`推测`。
- 标准的「新」不作为证据：2013 年发布不削弱条文有效性，但也不提供任何采用/落地证据。

## 与已有判断的关系

| 结论/判断 | 关系 | 说明 |
|---|---|---|
| policy **F2** | 支持，并把一半 `待核` 收窄 | F2 说四种语义不能混。本卡给出 XACML 一侧的原文依据（合并算法是显式标识符、obligation 有 `FulfillOn`、effect 只有两种）。ODRL / Rego / OpenFGA 一侧仍 `待核`，F2 整体不宜直接升 `已核` |
| policy F2 / mechanism 对照表的算法清单 | 补正 | 规范里还有 `ordered-deny-overrides`、`ordered-permit-overrides`、`only-one-applicable`（C.3 / C.5 / C.9）。只列 5 个不算错，但不全 |
| 04 **C.2** 的「deny-overrides / 默认 deny」 | **需要改措辞** | `deny-overrides` 在无子项适用时返回 `NotApplicable`，不是 `Deny`（C.2 第 7 条）。「无命中 → deny」来自顶层用 `deny-unless-permit`（C.6）或 PEP 采用 deny-biased（§7.2.2）。把 04 的默认 deny 说成「XACML deny-overrides 的默认」是错的；说成「我们的 PEP bias 选择」是对的 |
| 04 C.2 的 obligation 列（每行都带 `log`，含 deny 行） | 支持 | `FulfillOn` 可取 `Deny`，所以「deny 也带 obligation」在 XACML 里成立。但 §7.2.1 要求 PEP「理解且能且愿意履行」才执行决定——04 执行层是否履行未测 |
| mechanism.md 的 `skip` | 支持，且更硬 | Rule 的值只有 `Permit` / `Deny` / `NotApplicable` / `Indeterminate`（§7.11 Table 4），`EffectType` 只枚举 Permit/Deny（§5.22）：XACML 没有第 4 种 effect。`skip` 最接近 `NotApplicable`，但 04 把 `skip` 当带 reason 的 decision 返回，语义不同 |
| mechanism.md 的「版本一定可回放」 | 支持（原怀疑更成立） | §5.11 明说 reference 解析在规范外，§5.10 的 `most recent` 只是 SHOULD 且无排序定义。XACML 不提供回放能力 |
| **E-22**（三层不能互推） | 旁证 | XACML 把「求值 / 执行 / 属性供给 / 策略作者」拆成四个角色，正是三层分离的规范版本；但它是应然模型，不是落地证据 |
| **01-L19** | 支持前半句 | 「策略层有可判定的冲突/默认/义务语义」现在有 XACML 一手条款；「领域标准不给 principal/action 映射」本卡不涉及，仍 `推测` |

**不升 E**：单一标准的应然条文，没有实现/部署/对照证据。它能把 F2 的 XACML 列从 `待核` 变成 `已核`，不能把 F2 整体升 `已核`。

## 待核项

- [x] **能否把 Obligation 挂到 Deny 上**：已核销。`FulfillOn` 必填、类型 `EffectType`（只有 Permit/Deny），§7.18 按 effect 匹配上传，§7.2.1 直接描述「决定是 Deny 且带 obligation」的情形 → 可以挂。可回改 mechanism.md 的那句 `待核`。
- [x] **条款号**：本文引用的节号均取自该版目录，可逐字复核；未引用的条文不写号。
- [ ] **版本匹配的具体行为**：模式语义已核（§5.13），但「多个匹配版本时怎么排序、怎么取」规范只给 SHOULD，且解析机制明文在范围外。需要实现文档/案例才能判「版本可回放」。
- [ ] **附录 C.7 疑似编辑错误**：`permit-unless-deny` 的描述写「where a deny decision should have priority over a permit decision」，但算法是「任一 Deny → Deny，否则 Permit」，默认是 Permit。文本自相矛盾；引用时只引伪码。是否有 OASIS errata 更正在 待核。
- [ ] **是否有 3.0 后续 errata / 修订**改变上述节号或条文（本卡只按 2013-01-22 单版）。
- [ ] **实现侧**：是否有实现真的区分 extended `Indeterminate` 与 PEP bias；04 若要写 `deny-overrides`，需说明它只覆盖「有命中规则」的部分。
- [ ] **ODRL 2.2 / Rego / OpenFGA** 的对应条款（F2 的另一半仍是 `待核`）。

## 喂到哪个主题

- `topics/01-constraint/policy/findings.md` F2：XACML 列由「标准待入库」→ 本源卡；补 `ordered-*` / `only-one-applicable`；可核销「obligation 能否挂 Deny」。
- `topics/01-constraint/policy/mechanism.md`「冲突消解对照」：XACML 列可去 `待核`，并把「默认」一格改为 `deny-overrides → NotApplicable；默认 deny 由 PEP bias 或 deny-unless-permit 给`。
- `topics/01-constraint/access-control/frontier.md` G1（策略冲突/优先级）：XACML 给出可命名的冲突消解原语，可作为 G1 的术语底座。
- `topics/01-constraint/sources.md`：OASIS XACML 3.0 由「待入库」→ 本源卡。
- `deliverables/04-worked-example/body/govern.md` C.2：`deny-overrides` / 默认 deny 的措辞需分开写（算法 vs PEP bias）。
- 不升 `topics/conclusions.md` 的 E：标准条文不是落地证据。

## 原文摘录

> "PAPs write policies and policy sets and make them available to the PDP. These policies or policy sets represent the complete policy for a specified target." — §3.1

> "The PEP fulfills the obligations." — §3.1（data-flow 最后一步）

> "If the decision is 'Deny', then the PEP SHALL deny access. If obligations accompany the decision, then the PEP shall deny access only if it understands, and it can and will discharge those obligations." — §7.2.1（Base PEP）

> "the obligation or advice expression SHALL be evaluated to an obligation or advice respectively, which SHALL be passed up to the next level of evaluation … only if the result of the rule, policy, or policy set being evaluated matches the value of the FulfillOn attribute of the obligation or the AppliesTo attribute of the advice." — §7.18

> "The 'Deny-unless-permit' combining algorithm is intended for those cases where a permit decision should have priority over a deny decision, and an 'Indeterminate' or 'NotApplicable' must never be the result. It is particularly useful at the top level in a policy structure to ensure that a PDP will always return a definite 'Permit' or 'Deny' result." — C.6

> "If any decision is 'Deny', the result is 'Deny'." — C.2 第 1 条
>
> "Otherwise, the result is 'NotApplicable'." — C.2 第 7 条（无子项适用时）

> "If none of these attributes is present, then any version of the policy set is acceptable. In the case that more than one matching version can be obtained, then the most recent one SHOULD be used." — §5.10

> "However, the mechanism for resolving a policy reference to the corresponding policy is outside the scope of this specification." — §5.11

> "A '*' means that any single number is valid. A '+' means that any number, and any subsequent numbers, are valid. In this manner, the following four patterns would all match the version string '1.2.3': '1.2.3', '1.*.3', '1.2.*' and '1.+'." — §5.13
