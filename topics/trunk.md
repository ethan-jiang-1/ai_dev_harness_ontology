---
status: draft
updated: 2026-11-11
---

# 规范主干：标准能定义什么，不能定义什么

> **这不是第七派。** 它是给六派判断提供**规范锚**的横切索引：哪些词有标准可依，哪些只是本仓库的工作词，哪些只能是线索。
>
> **三层来源**（避免再造新词）：
> - **N 规范性（normative）**：标准、规范、权威本体；**只能定义词与合格性**，不撑效应量。
> - **I 资料性（informative）**：论文、工程报告、开源代码；**给证据、数据、示例**，不定义词。
> - **S 线索（signal）**：只在 `frontier.md` 的候选队列；**不撑 E/L/交付物**。
>
> 我们平时说的「主干 / 支持补充 / 线索」，对应的就是 **N / I / S**；正式文件里用 N/I/S，避免再造一套私词。

## 1. 主干上有哪些标准

只列已入 `src/`、`admission: admitted` 且 `standing: normative` 的卡。**标准只定词与合格性，不证明效果。**

| 标准 | 定什么 | 不能定什么 | 接到哪 |
|---|---|---|---|
| **ISO/IEC 21838-1/-2**（TLO 要求；BFO 为参考 TLO） | 顶层本体（TLO）的范围、要求、合格性 | 不定义领域本体；不给成熟度分级；不证明「用了本体 agent 更准」 | 「本体」「顶层本体」；01/03/04 的定义段 |
| **OMG Commons 1.3** | 可复用本体模块、最小承诺（minimal commitments） | 不是 TLO；不定义领域语义；不保证跨库对齐 | 「可复用模块」「最小承诺」；03/04 的建模范畴 |
| **W3C SHACL** | RDF 图约束、校验、三态（通过/违反/未检查完）的语义基础 | 不定义动作授权；不保证语义正确；不证明 catch/FA 效应 | 「约束」「校验」；02 R10、03 checker 的接口层 |
| **W3C SHACL-AF** | 规则、target、扩展机制 | 不是执行点；不保证「会拦」；不撑效果量 | 读路径/策略过滤的**表达层**；02 R8、03 checker |
| **W3C OWL 2 Profiles** | profile 语义、RL 规则表 | 不定义实现；不证明推理效果；不覆盖所有 OWL | 「推理」「查询重写」的语义边界；02 R11、03 supply |
| **W3C ODRL 2.2** | 策略表达（permission/prohibition/duty 等） | 不定义身份/认证；不定义「谁读哪列」；不定义默认结论；不定义执行点 | 策略层/授权讨论；01 commit、03 action 的**边界** |
| **OASIS XACML 3.0** | 访问控制策略与判定的架构（PDP/PEP 等） | 不定义 obligation 语义；不定义义务失败后果；不给审计字段 | 访问控制/审批的**架构参照**；01 commit、04 治理 |
| **GB/T 43697-2024** | 数据分类分级的原则、框架、流程；核心/重要/一般三级 | 不定义策略语言；不给 principal×action→effect 映射；不管国家秘密/军事数据 | 数据分级/治理词表；04 治理 |
| **GB/T 35273-2020** | 个人信息处理的组织要求（收集/保存/使用/共享/删除） | 不是数据机密性分级；不是策略语言；不定义执行点 | 个人信息/合规边界；04 治理 |
| **ODCS v3.1.0** | data contract 的结构、SLA、质量检查字段 | 不是本体 schema；不定义访问控制；不保证运行时执行 | 「数据契约」字段；02/04 的数据契约 |

> **读法**：标准卡能回答「这个词是什么意思、什么叫合格」；不能回答「用了它效果好不好」。后者只能由 I 层（论文/代码/数据）回答。

## 2. 六派/六时刻，主干覆盖到哪

| 位置 | 有 N 锚吗 | 锚是什么 | 缺什么 / 只能标 local |
|---|---|---|---|
| **context / 供给** | 部分 | ISO 21838、OMG Commons、OWL 2 定义「本体/模块/推理」 | 没有标准定义「投影文本」「上下文供给」；靠 I 层（N&D/CAI） |
| **memory / 跨轮** | 无 | — | 没有标准定义「agent 记忆/状态」；只能 local + I 层（FIRME/EvoMemState） |
| **evidence / 输出契约** | 无 | — | 没有标准定义「接地等级」；E-03 已撤回，只能 local/gap |
| **checker / 输出后** | 部分 | SHACL/SHACL-AF/OWL 2 定义约束语义 | 没有标准定义「checker 的 catch/FA」；效应靠 I 层（E-20 代码） |
| **action / 动作前** | 部分 | ODRL/XACML 定义策略表达/判定架构 | 没有标准定义「可逆性」「动作闸」；E-04 已撤回，只能 local/gap |
| **commit / 落盘前** | 部分 | XACML/ODRL 给策略/判定架构 | 没有标准定义「commit gate」；E-20 只有否定性代码证据；只能 local/gap |

> 结论：**主干只覆盖「词与合格性」的一半，覆盖不了「效应」。** 这是正常的：标准不负责效果。不要把标准卡拿去撑「本体提升 agent 效果」。

## 3. N / I / S 怎么用

| 层 | 可以做什么 | 不可以做什么 | 放在哪 |
|---|---|---|---|
| **N 规范性** | 定义术语、定合格性、写边界 | 证明效果、给阈值、替代实验 | `src/web/*` 标准卡；本页 |
| **I 资料性** | 给效应量、数据、代码锚、失败模式 | 定义术语（定义必须回到 N 或标 local） | `src/papers/*`、`src/open-source/*`；`topics/*/sources.md` |
| **S 线索** | 提示「有人在说/可能在动」 | 写进 claims/README/交付物；当证据 | 各派 `frontier.md` 候选队列 |

**四条硬规则**：

1. **专业术语只能来自 N。** 没有 N 就标 `local`，首现解释；不得写成“行业标准/共识”。
2. **论文只能给证据，不能定义术语。** 论文里的条件编号（如 K0–K4）是**实验条件**，不是术语；主路径不用，只能出现在出处/回查。
3. 效应量只能指 I；I 的限定必须一起写。
4. S 只能进 `frontier.md`；不得出现在 `claims.md`、派 README、交付物。

> 例子：K0–K4 是一篇论文的五个实验条件，**不是“知识层级”**；本仓库只在 [K 页](../deliverables/01-capability-status/sections/k-ladder.md) 作来源说明，不拿它当术语。专业术语如“顶层本体/约束/策略/数据分级”才去 ISO 21838、SHACL、ODRL、GB/T 找 N。

## 4. 现在的主干缺口

这些词**没有** normative 锚，当前只能标 `local`：

- 知识图谱（实例层）——本仓库只作描述词；
- 语义层——没有标准定义；
- 成熟度——没有标准分级；EKGF 已判 `excluded`；
- 知识层级 / K0–K4——论文实验条件，不是标准；
- 接地（grounding）/ 接地等级——没有标准；E-03 已撤回；
- 动作可逆性 / 动作闸——没有标准；
- commit gate / 落盘授权——没有标准；
- agent 记忆 / 跨轮状态——没有标准。

> 这些不是「永远没有标准」，是**今天没有入卡的 normative 源**。要用，先按 CHARTER §4 找标准/权威本体，入卡后改本页；找不到就继续标 local。

## 5. 接到哪里

- 术语表：[meta/term-baseline.md](../meta/term-baseline.md) v0（10 词）+ v1（29 词 + 06 试点 1 词）与本页对齐；K 行见 [K 页](../deliverables/01-capability-status/sections/k-ladder.md)。
- 各派来源：`topics/<派>/sources.md` 顶部加「N/I/S 三层读法」，N 指本页，I/S 在各自表里。
- 交付物：01/02/03/04 的定义段与边界，只引 N；效应引 I；S 不出现。
- 维护：新增标准卡必须 `admission: admitted` + `standing: normative`；厂商页、社区成熟度模型、单机构白皮书不进主干。

### 5.1 实际接线（2026-11-11，第 7 步）

四个交付物各有一个「§0 名词从哪来（N / local）」术语页；正文定义句用 `（N: 标准名）` / `（local）` 标注。逐页：

| 标准 | 实际接到哪（页面级） |
|---|---|
| ISO/IEC 21838-1/-2 | [START](../deliverables/START.md) 三词表；[01 术语](../deliverables/01-capability-status/sections/glossary.md#term-sources)；[01 README](../deliverables/01-capability-status/README.md)；[03 术语](../deliverables/03-mechanism-reference/sections/glossary.md#term-sources)；[04 术语](../deliverables/04-ontology-in-production/sections/glossary.md#term-sources)；[04 build A.3](../deliverables/04-ontology-in-production/body/build.md) |
| OMG Commons 1.3 | [03 术语](../deliverables/03-mechanism-reference/sections/glossary.md#term-sources)；[02 术语](../deliverables/02-engineering-playbook/sections/glossary.md#term-sources) |
| W3C SHACL | [01 术语](../deliverables/01-capability-status/sections/glossary.md#term-sources)、[01 map §2.2](../deliverables/01-capability-status/sections/map.md#22-一张表)、[01 capabilities §3.8](../deliverables/01-capability-status/capabilities/README.md#read-path)；[02 术语](../deliverables/02-engineering-playbook/sections/glossary.md#term-sources)、[R10/R11](../deliverables/02-engineering-playbook/recipes/offline-and-obda.md)、[R4/R5](../deliverables/02-engineering-playbook/recipes/judgment.md)；[03 checker](../deliverables/03-mechanism-reference/positions/checker.md)；[04 术语](../deliverables/04-ontology-in-production/sections/glossary.md#term-sources)、[04 build A.3](../deliverables/04-ontology-in-production/body/build.md) |
| W3C SHACL-AF | [01 capabilities §3.8](../deliverables/01-capability-status/capabilities/README.md#read-path)；[02 R10/R11](../deliverables/02-engineering-playbook/recipes/offline-and-obda.md)、[R8](../deliverables/02-engineering-playbook/recipes/constraint.md#r8--读路径过滤只做可见性不要当授权)；[03 checker](../deliverables/03-mechanism-reference/positions/checker.md)；[04 govern C.1](../deliverables/04-ontology-in-production/body/govern.md) |
| W3C OWL 2 Profiles | [01 map §2.2](../deliverables/01-capability-status/sections/map.md#22-一张表)、[01 capabilities §3.8](../deliverables/01-capability-status/capabilities/README.md#read-path)；[02 R10/R11](../deliverables/02-engineering-playbook/recipes/offline-and-obda.md)；[03 术语](../deliverables/03-mechanism-reference/sections/glossary.md#term-sources)；[04 术语](../deliverables/04-ontology-in-production/sections/glossary.md#term-sources)、[04 build A.3](../deliverables/04-ontology-in-production/body/build.md) |
| W3C ODRL 2.2 | [01 README 词源](../deliverables/01-capability-status/README.md)、[decision-record](../deliverables/01-capability-status/sections/decision-record.md)；[02 术语](../deliverables/02-engineering-playbook/sections/glossary.md#term-sources)、[R6/R8/R9](../deliverables/02-engineering-playbook/recipes/constraint.md)；[03 action](../deliverables/03-mechanism-reference/positions/action.md)、[03 commit](../deliverables/03-mechanism-reference/positions/commit.md)；[04 govern C.1/C.2](../deliverables/04-ontology-in-production/body/govern.md) |
| OASIS XACML 3.0 | 同 ODRL 的页面（成对出现，表达 vs 判定架构） |
| GB/T 43697-2024 | [01 术语](../deliverables/01-capability-status/sections/glossary.md#term-sources)；[02 术语](../deliverables/02-engineering-playbook/sections/glossary.md#term-sources)；[04 术语](../deliverables/04-ontology-in-production/sections/glossary.md#term-sources)、[04 govern C.1](../deliverables/04-ontology-in-production/body/govern.md) |
| GB/T 35273-2020 | 同 GB/T 43697 的页面 |
| ODCS v3.1.0 | [02 术语](../deliverables/02-engineering-playbook/sections/glossary.md#term-sources)、[02 接口附录](../deliverables/02-engineering-playbook/appendices/interfaces.md)；[04 术语](../deliverables/04-ontology-in-production/sections/glossary.md#term-sources) |

> **接线口径**：`N:` 只出现在「定义/合格性」句；效应句仍引 E-xx。`local` 词（动作闸、commit gate、接地、记忆、读路径、六位置、执行形态等）一律首现解释，不借标准抬高。完整记录与验收命令见 [接线报告](../deliverables/_plans/2026-11-11-trunk-wiring.md)。

> 本页是索引，不是新 E；不改变任何已有判断，只把「词从哪来」摆清楚。
