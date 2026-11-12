---
status: draft
source_type: standard
standing: normative
reading: 精读
provenance: 原文正文
updated: 2026-11-11
batch:
source: https://www.w3.org/TR/odrl-model/
author: W3C Permissions & Obligations Expression Working Group（编辑 Renato Iannella、Serena Villata）
published: 2018-02-15
influence: W3C Recommendation（2018-02-15），与同日发布的 ODRL Vocabulary & Expression 共同构成 ODRL 2.2，是「内容/数据使用条款」表达最常被引用的标准基线，数据空间与媒体许可多以 ODRL profile 形式挂靠（具体采用清单 待核）
updates: []
admission: admitted
gate_checked: 2026-11-11
impact_evidence: "I1: W3C Recommendation"
liveness: standard-in-force
provenance_type: standard-body
---

# W3C ODRL 2.2 · Information Model（权利/合约表达，不是执行引擎）

> 读的是 REC 正文（`https://www.w3.org/TR/odrl-model/`）+ 配套 `https://www.w3.org/TR/odrl-vocab/`。
> 抓取限制：REC 页面在 §2.5.6 处被截断，§2.6–§3.3 改读同规范的 W3C 编辑稿（`https://w3c.github.io/poe/model/`，章节号与标题一致）；§2.10 的引文出自编辑稿，REC 逐字未核，见待核项。

## 它主张什么

1. **Policy 是「一条或多条 Rule」的容器，Rule 只有三种**：Permission（可做某 Action）、Prohibition（不可做）、Duty（必须做）；三者再挂 Asset（`target` / 抽象 `relation`）、Party（`assigner` / `assignee` 等抽象 `function`）、Action（可用 `includedIn` / `implies` 组层级）、Constraint（`leftOperand` + `operator` + `rightOperand`，或 `and/or/xone/andSequence` 逻辑组合）。Permission 可挂 `duty` 当前置条件，Policy 可挂 `obligation`（Duty），Prohibition 可挂 `remedy`，Duty 可挂 `consequence`——即它连「违约后怎么办」也有槽位。
2. **冲突不做算法合成，只做声明式选择**：Policy 的 `conflict` 取 `perm` / `prohibit` / `invalid`（可扩展 ConflictTerm），未显式设置时默认 `invalid`；而冲突能否被识别，取决于 Action 的 `includedIn` / `implies` 语义（如 `play ⊆ use`：同一 target 上允许 `play`、禁止 `use` 即冲突），所以「不懂 profile 的 Action 层级，就判不了冲突」。
3. **规范分两层交付，且刻意不碰执行**：本文件只定义逻辑模型（logical view），可实现的 RDF / JSON-LD / XML 序列化交给配套的 Vocabulary & Expression；`ODRL Validator`（查策略表达式本身合规）与 `ODRL Evaluator`（查规则是否被满足）都只是**被定义的角色**，规范不给请求/响应协议、不给 PDP/PEP、不给判定日志格式。

## 场景与 scope

- **场景**：内容、媒体、数据资源的使用条款表达与交换（数字版权、数据空间、隐私/使用政策 profile）。Policy 可挂在资源上（`hasPolicy`），也可独立成文，是「条款文档」而非「判定接口」。
- **Policy 三种档位**：`Set`（默认，泛化规则）/ `Offer`（assigner 提出，**不授予任何权利**）/ `Agreement`（assigner 授予 assignee）；`Offer` 的 assignee 即使写了也 MUST NOT 由此获得特权（词汇表 §3.2.2）。
- **scope 内**：单条 Policy 的规则结构、compact 写法展开为 atomic 规则、跨 Policy 的 `inheritFrom`、同一 Policy 内或 merge 后的冲突策略、profile 机制。
- **scope 外（关键）**：不定义身份与认证，不定义「某张表某列谁能读」，不定义无规则命中时的默认结论，也不定义执行点在哪拦、拦不住怎么办。XACML 的 PDP/PEP + 合并算法在这里没有对应物：ODRL 把「冲突时谁优先」写成 policy 里的一个值，把「要不要执行」留给实现者。
- **使用前提**：只用 Core Vocabulary，或声明 `profile`；处理器不认 profile 标识时 MUST 停止处理该 policy（§3.2）——这使 ODRL 的互操作以「共同 profile」为界，而不是以「都叫 ODRL」为界。

## 证据强度

- **一手还是转述**：一手（W3C REC 正文 + 配套 REC 词汇表）。§2.10 与 §2.6.5–§3.3 因页面截断改读同规范编辑稿，标「编辑稿」；不是二手综述。
- **有数据吗**：标准本身无实验数据；有实现报告（implementation report，本轮未读），所以「有多少实现通过」未知。
- **规范强度**：规范用 MUST/SHOULD 明确到属性基数（Policy MUST 有 `uid`、MUST 至少一条 Rule；Asset/Party 的 `uid` 是 SHOULD；`conflict` 是 SHOULD 取三值之一 + 默认值），这类条款可逐条引用。
- **可复现吗**：条款可逐条核；但**行为不可复现**——Evaluator 的判定过程、日志、无命中默认都没规定，两个实现可以都「合规」而给出不同处置。
- **证据等级**：本文所述条款内容 `已核`（正文）；「实现会照此执行」「采用很广」是 `推测`/`待核`；本卡未做任何实现对照，不给「ODRL 好用/不好用」的结论。
- **存档状态**：原文未落盘，本目录只有本卡；台账（`src/README.md`）未登记——本轮只允许写这一个文件。

## 与已有判断的关系

| 结论编号 | 关系 | 说明 |
|---|---|---|
| policy F2（策略语言语义不同） | **支持并收紧** | 原文坐实「ODRL 没有 XACML 式合并算法」：只有 `perm`/`prohibit`/`invalid` 三个声明值 + 默认 `invalid`；冲突触发条件还依赖 Action 层级（`includedIn`/`implies`）。F2 的说法可从 `待核`（标准未入库）上移到「条款已核」，但 F2 整体仍含 XACML/Rego/OpenFGA 三方未入库，不因本卡单独升级。 |
| policy mechanism.md 冲突消解表「ODRL 默认：未指定」 | **修正** | 可填 `invalid`（§2.10 编辑稿原文：未显式设置时默认 `invalid`）。另需补一行：ODRL 的冲突可能由 Action 语义触发，不只是 action 字符串相同。 |
| policy mechanism.md「版本 → ODRL = profile」 | **修正** | `profile` 是「Policy 遵循的 ODRL Profile 标识」（词汇表 §3.1.3），不是版本号；版本语义在 Policy Metadata 的 `dc:replaces` / `dc:isReplacedBy`（§2.8：声明 `dc:isReplacedBy` 时处理器 MUST 视旧 Policy 为 void 并取新 Policy）与 `inheritFrom`（§2.9）。把 profile 当版本列会误导 04 的 `policy_version` 对照。 |
| 04 C.2 策略表（effect 列含 `skip`） | **支持 + 需标注** | ODRL 的三种 Rule 不是 effect 取值：`Duty` 是义务不是「第三种判定」，`skip` 在 ODRL 里没有对应物。04 的 `skip` 与「无命中 deny」都是工程选择，若表要自称 ODRL 语义须改写；这与 04 现有注「skip 是第 4 种效果」一致，本卡只补条款级依据。 |
| 04 C.2 义务列（`log`/`mask`/`approve`） | **旁证（更细的槽位）** | ODRL 把义务分成 duty（前置）、obligation（Policy 级）、consequence（不履行后的新义务）、remedy（禁令已被违反后的补救）。04 表只有一列 obligation，表达不了「违反后补救」；这是 04 与标准的结构差，不是 04 的错误。 |
| E-22（访问控制三层不能互推） | **支持** | ODRL 停在「策略层」：它能把条款写成机器可读、能查合规、能声明冲突优先级，但不产生执行点、不产判定日志、不回答「拦在哪」。正好是 E-22 里「策略层」的形态证据（且仍**没有** ontology/KG 领域的策略来源）。 |
| E-20（执行 ≠ 授权） | **旁证** | `Evaluator` 只被定义为「判定规则是否被满足」的角色，规范不规定它如何记录、是否阻断；「ODRL 被执行」不能从标准文本推出。 |

**不升 E**：这是单一标准的条款核对，没有落地对照、没有实现行为数据；它改变的是 policy 派内部的措辞与一张对照表，不动 conclusions。

## 待核项

- [ ] **REC 版 §2.10 逐字**：本次 REC 页面在 §2.5.6 截断，`perm`/`prohibit`/`invalid` 与默认值引自编辑稿；需取 REC 快照逐字比对（编辑稿可能与 REC 有措辞差）。
- [ ] **2.10 默认冲突策略是否被 errata 改动**：已读到「未显式设置 → 默认 `invalid`」；`https://www.w3.org/2016/poe/errata/` 未读。
- [ ] **是否定义 audit / decision log**：已读 §1–§3 未见 audit、decision log、evaluation record 之类术语；§2.8 只有 `dc:creator/description/issued/modified/coverage/replaces/isReplacedBy`。§4 Privacy Considerations 与附录 B–E 未读，不能断言「全篇没有」。
- [ ] **条款号**：W3C 规范用章节号，无「第 X 条第 Y 款」；本卡只写 `§x.y`，未编造条号。若要引用到具体 MUST 列表，需再对一遍段落锚点。
- [ ] **XML 编码细节**：词汇表 §5 分 RDF / JSON-LD / XML 三节，本轮只核到「RDF 序列化 + JSON-LD context + 备选 XML 序列化」的存在与并列关系（词汇表 §1、§5 目录），§5.3 正文未读。
- [ ] **§2.6.1–§2.6.4（Permission/Prohibition/Duty 类属性、Policy 级 obligation）与 §3.4（Core Profile）未逐段读**：本卡的 Rule 结构描述来自 §1.3 术语表 + §2 总览 + §2.6.5–§2.10，缺这几段的细节。
- [ ] **实现报告**（`https://w3c.github.io/poe/test/implementors`）未读：实现数量、互操作测试结论未知，「采用广」目前只是印象。
- [ ] **原文未落盘、台账未登记**：`src/web/w3c-odrl-2.2/` 缺 `<slug>.md` 原文与 `src/README.md` 台账行（本轮文件权限只到本卡）。

## 喂到哪个主题

- [policy F2](../../../topics/01-constraint/policy/findings.md)：F2 的 ODRL 一行的条款级证据；可把「标准未入库 → 待核」的限定收窄到「XACML/Rego/OpenFGA 未入库」。
- [policy mechanism.md 冲突消解对照](../../../topics/01-constraint/policy/mechanism.md)：改「ODRL 默认：未指定 → `invalid`」；改「版本 = profile → `dc:replaces`/`dc:isReplacedBy` + `inheritFrom`」；补「冲突由 Action `includedIn`/`implies` 触发」。
- [01-constraint/sources.md](../../../topics/01-constraint/sources.md)：ODRL 行仍写「待入库」，可改为指向本卡（本轮不改）。
- [04 C.2 策略表](../../../deliverables/04-worked-example/03-body/03-govern.md)：`effect` 与 `obligation` 两列的语义对照；`skip`、`无命中 deny` 标为工程选择。
- 不升 `topics/conclusions.md`，不改 `claims.md`：本卡没有改变「策略层是独立层」这一级判断，只补条款与一处对照表错误。

## 原文摘录

> **§2.10 Policy Conflict Strategy（W3C 编辑稿，章节号与 REC 一致）**
> "The `conflict` property SHOULD take one of the following Conflict Strategy Preference values (instance of the ConflictTerm class): `perm`: the Permissions MUST override the Prohibitions; `prohibit`: the Prohibitions MUST override the Permissions; `invalid`: the entire Policy MUST be void if any conflict is detected."
> "If the `conflict` property is not explicitly set, the default of `invalid` will be used."
> "If a Policy has multiple `conflict` property values … and there are conflicting Rules then the entire Policy MUST be void."

> **§2.4 Action Class**（冲突如何被触发）
> "…if the `play` Action is defined as `includedIn` with `use` then if `play` is permitted in a Policy and `use` is prohibited in the same Policy - and both Actions apply to the same target Asset - then because of this asserted relationship between the two, there is conflict in the Policy."

> **§2.1 Policy Class**（最小合规）
> "A Policy _MUST_ have one `uid` property value (of type IRI) to identify the Policy."
> "A Policy _MUST_ have at least one `permission`, `prohibition`, or `obligation` property values of type Rule."

> **§2.9 Policy Inheritance**
> "Inheritance MUST NOT be circular."
> "No constraint `status` information is transferred from the parent Policy to the child Policy."

> **§2.8 Policy Metadata**（版本语义在这里，不在 profile）
> "If a Policy has the `dc:isReplacedBy` property, then a processor MUST consider the first Policy void and MUST retrieve and process the identified Policy."

> **§3.2 ODRL Profile Conformance**
> "If the ODRL Processing system does not recognise the ODRL Profile identifier(s) then it MUST stop processing the policy."

> **§2 Note**（逻辑模型 vs 可实现模型）
> "The ODRL Information Model provides a _logical view_ of the components of the Policy model. The _implementable view_ … is provided by various encoding serialisations as normatively described in the ODRL Vocabulary & Expression document."

> **§1.1 Aims of the Model**
> "While the ODRL Information Model is built using Linked Data principles, the design is intended to allow non-graph-based implementations."

> **词汇表 §1 Introduction**（编码清单）
> "In addition to supported RDF serialisations, the ODRL Vocabulary and Expression provides the JSON-LD Context and profile definitions needed to use the ODRL JSON serialisation in a Linked Data context, and includes an alternate XML serialisation."

> **词汇表 §3.1.2 / §3.1.3**（uid / profile）
> "Unique Identifier — Definition: An unambiguous identifier. Note: Used by the Policy, Rule, Asset, Party, Constraint, and Logical Constraint Classes."
> "Profile — Definition: The identifier(s) of an ODRL Profile that the Policy conforms to. Note: The profile property is mandatory if the Policy is using an ODRL Profile."

> **词汇表 §3.2.2 Offer**（Offer ≠ 授予）
> "The Offer Policy _MAY_ contain a Party with Assignee function, but _MUST_ not grant any privileges to that Party."

> **词汇表 §1.3 术语（模型文档）**（Evaluator 只是角色；原文 "have meet" 如此）
> "ODRL Evaluator — A system that determines whether the Rules of an ODRL Policy expression have meet their intended action performance."
