---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# A · 建：从契约到 `build_report`

> **本章回答**：消费者要什么、建到什么程度算可消费。
> **你需要准备**：3 个 consumer、6 项契约、一个能解析 TTL 的环境。
> **做完得到**：契约、`ontology.ttl`、`shapes.ttl`、`build_report`。
> **怎么算做完**：A.5 三关 + A.6 证据与边界；清单见 [acceptance](../sections/acceptance.md)。
>
> 三关 = load / validate / answer；详细判据与 10 个坏样本见 [参考表 §1–§2](../sections/reference.md)。

## A.1 消费者契约（产物）

6 项写不出就停。**怎么找**：UI/agent 的 owner（谁读）、数据 owner（谁能给列）、治理（谁能拒）各拉 1 人；每人给「在什么时刻、要答什么 / 拒什么」。填不出的格就是需求缺口，不要编。

**单人/学习模式**：先用本 fixture 的 3 行读通一条链，再把 consumer 换成你的；不要为了填满而编人。真实立项时，6 项仍要由对应 owner 确认。

本 fixture（[example](../example/README.md)）：

| consumer | principal | moment | answers | refuses | load |
|---|---|---|---|---|---|
| UI | steward | 页面加载 | 答 Email 列 | — | SPARQL endpoint |
| agent | steward | 查询时 | 答 4 表/7 列 | — | SPARQL endpoint |
| governance | governance | 夜间 | 答未打标数据集（4） | 拒列身份/明细 | SPARQL endpoint |

`tag_email_1` 是 `:WorkEmail`（`:Email` 子类），CQ1 用 `?t a/rdfs:subClassOf*` 真正走到子类；拒绝单位 = 列（triple subject）；governance 只拿 dataset 计数，不拿列身份。

**你的表**：

| consumer | principal | moment | answers | refuses | load |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

**`principal` 是判定身份，不是 consumer 名字**：consumer 是调用方，principal 是 policy 判定用的用户/角色/服务，`user_context` 是请求带的 role/clearance。fixture 的 CQ1 同时出现 `steward` 与 `analyst` 两个 principal，但契约只写了 steward——这层没写死。落地时先选 A/B/C，见 [transfer §6.1](../sections/transfer.md#p-principal)。标签/等级从哪来、没有怎么停：见 [label-source](../sections/label-source.md)。

> `refuses` 写 `—` 表示「明确不拒」，不算空；契约本身带 `contract_version`（第 7 项，A.5 回填），不在 6 列里。

**契约六项与 `build_report` 只部分对应**：`violations` ≠ `refuses`，`missing_fields` ≠ 契约缺字段；覆盖表见 [参考表 §0](../sections/reference.md)。


### CQ 只是模板词：须在契约行可执行

①`?col :hasTag ?t . ?t a/rdfs:subClassOf* :Email`（UI）；②`sensitivityLevel ≥ 3` + `columnOfTable` 反查（agent）；③`FILTER NOT EXISTS { ?col :hasTag ?t }`（治理）。

## A.2 表示档位：按消费者选

| 消费者要什么 | 选 | 判据 |
|---|---|---|
| 只把知识拼进 prompt / 检索 | 词表 | 不需要判定，形式化只占预算 |
| 要跑 shape / 查询 / 授权判定 | 结构表 | 有可判定的关系与约束 |
| 要从公理推出隐含分类 | 逻辑表 | 需要 reasoner；解释成本高 |

本例选结构表（`推测`）：三条契约无隐含分类。**薄层优先**：原始点位（K0）→ 点位语义（K1）→ 知识投影文本（K2）；K0→K1 是 **54.6 个百分点**（占两层总增益 74.4pp 的 73.4%），K1→K2 再加 19.8pp（26.6%，`O-F14`）。这是文本投影的点位语义效应（单工厂、9 任务），不是三档对照；K 是 N&D 实验条件代号，定义见 [01 K 页](../../01-capability-status/sections/k-ladder.md)。

三档 × 四位置矩阵见 [参考表 §1](../sections/reference.md)：结构表是唯一三关都 `supported` 的档；词表 validate/explain 弱；逻辑表 explain 无可移植路径。能力矩阵，不是效应量；薄层优先的 +54.6pp 不是三档对照。

## A.3 最小本体（11 类 / 5 属性）

只建契约用得到的；等级挂 `Tag`，不挂 `Column`。

**一列一个 tag 是 fixture 的约定，不是模型约束**：Glyph 是列级多标签（`已核`，Glyph digest；单企业，E-22），fixture 的 shape 没有 `maxCount 1`，policy 的 `level` 是标量。多标签列怎么取 level，见 [transfer §6.2](../sections/transfer.md#p-multitag)；不选就先别写 shape。标签源是否可信、覆盖多少、漏标多少，见 [label-source](../sections/label-source.md)。

TBox：[ontology.ttl](../example/ontology.ttl)（11 类/5 属性；`SELECT (COUNT(DISTINCT ?c) WHERE { ?c a owl:Class })` = 11）；ABox：[catalog.ttl](../example/catalog.ttl)。

> **词源**：TBox / ABox 是 `local` 描述词（DL 文献常用，未入卡 normative 源）；类与属性的语义边界可对到 `N: W3C OWL 2 Profiles`（profile 只定语义子集，不证明推理效果）；shape 与三态见 `N: W3C SHACL`。**「建多少类算够」是工程判断，不是标准条款。**

11 类 = Tag 层级 8（Tag/PII/Email/WorkEmail/Phone/Name/Financial/SSN）+ Dataset/Table/Column 3。`WorkEmail` 是 `Email` 子类，`tag_email_1` 挂在它上面，CQ1 的 `rdfs:subClassOf*` 因此不是装饰；`Address` 已删，避免“未用类”。

`owl:inverseOf` 只是文档：执行层不 entail，ABox 两侧显式写 `columnOfTable`/`hasColumn`。

**标签层独立**：Glyph 275 叶标签，不产策略、不执行。

## A.4 约束与负例（产物：shape + 负例表）

每条约束 = shape/检查 + 已知违反 + 干净样本。从 CQ 反推 shape 的三步见 [transfer §4](../sections/transfer.md)。

Shapes：[shapes.ttl](../example/shapes.ttl)（2 条：TagHasLevel、HasTagClass）。

| 约束 | 检查 | 已知违反 | 干净样本 |
|---|---|---|---|
| Tag 有 1–4 的整数等级 | `TagHasLevel` | `tag_unknown` 缺等级 | `tag_email_1` |
| hasTag 非字面量 | `sh:nodeKind sh:IRI` | `col_legacy` 指字面量 | `col_email`→WorkEmail |
| 未打标可发现（CQ3，不是 shape） | `FILTER NOT EXISTS` | `col_order_id` 等 4 列无 tag | `col_email` |

范围 1–4 已写进 shape；fixture 没有 level 0 坏样本，所以仍是 2 violations。0/负数不在合法域（见 [boundaries](../sections/boundaries.md)）。

**10 个坏样本里，现有闸门只稳定抓住 2 个**（完整表见 [参考表 §2](../sections/reference.md)）：

| # | 坏样本 | 现在抓住？ |
|---|---|---|
| S4 | 缺 load | 否（假阳性） |
| S6 | shape 缺 target | 否（0 focus → `conforms=true`） |
| S7 | tag 是字面量 | **是**（violation） |
| S8 | level 缺失 | **是**（violation） |

其余 6 个（S1/S2/S3/S5/S9/S10）分别缺 principal/moment/refuse/version、无 dataset 边、版本不一致；现状均为 silent 或 answer undercoverage。

SFE-O 与 Ontology Catch 已移出；checker 的 catch/FA 不再引用（W 表见 [02 canonical §1.1](../../02-engineering-playbook/sections/canonical.md#w-table)），PPV 只保留复算方法（O-F08）。

## A.5 可消费性闸门（产物：`build_report`）

三关记录，不是一个 `parsed` 布尔：

```json
{"_note":"fixture 期望，非实测","load":{"parsed":true,"missing_fields":[]},"validate":{"violations":2,"targeted":2,"declared_shape_samples":2,"caught":2,"contract_bad_samples":10,"contract_caught":2,"clean_fp":"未测"},"answer":{"CQ1":"2 列/2 表（steward）","CQ2":"7 列/4 表（steward）","CQ3":"4 数据集（governance）"},"classes":11,"properties":5,"policy_version":"0.4.0","ontology_version":"0.1.0","tag_version":"0.1.0","contract_version":"0.1.0","snapshot":"example/ 2026-11-10（日期标签，不是 hash）","parser":"rdflib+pyshacl（版本未记）","provenance":{"source":"synthetic"}}
```

- **load**：rdflib 解析 [ontology.ttl](../example/ontology.ttl)/[shapes.ttl](../example/shapes.ttl)/[catalog.ttl](../example/catalog.ttl)；`parsed`=语法/前缀，`missing_fields`=产物必填。
- **validate**：pyshacl 跑 shapes；`targeted`=有目标且实际被检查的 shape 数；`violations`=shape 违反；`caught`=已声明 shape 坏样本被抓住数；`clean_fp` 未测。**两个分母不要混**：`2/2` 是 shape 声明样本；10 个契约坏样本只抓 2 个（`contract_caught/contract_bad_samples`）。分子就是 S7/S8，别把它当第二个独立测试。
- **answer**：CQ1 2 列 / 2 表、CQ2 7 列 / 4 表、CQ3 4 数据集；查询文本在 [B.2](./consume.md)；0 行必须分因。这些是 **raw**，不是 policy 后的结果；governed 见 C.4。

**版本来源**：

| 字段 | 来源 | 说明 |
|---|---|---|
| `policy_version` | [policy.json](../example/policy.json) | 0.4.0 |
| `ontology_version` | [ontology.ttl](../example/ontology.ttl) 的 `owl:versionInfo` | 0.1.0 |
| `tag_version` | `ontology.ttl` 的 `:tagVersion` | fixture 约定；不是独立 tag 文件 |
| `contract_version` | A.1 契约表 | fixture 约定 0.1.0；没有独立文件 |
| `snapshot` | `example/ 2026-11-10` | 日期标签，不是内容 hash；真 replay 需 hash |
| `parser` | 环境 | 本次未记版本；跨版本重跑可能不同 |

三关是记录，不是产物属性；`targeted=0` 不是 pass。

> 空表见 [templates TPL-7](../sections/templates.md#tpl-7-build_report)；从 CQ 到三关的推导见 [transfer §7](../sections/transfer.md)。

**交接**：`build_report` 的 `targeted/violations`→B 的先决条件；`query_id`→C.4；`policy_version`→A.5。

**停**：`violations` ≠ 已声明坏样本数（2）或落在已知清单外；`targeted=0`（shape 无目标）当 pass；`answer` 0 行不分因；无契约/版本/来源；下游不加载。

## A.6 证据与边界

> 证据见 [evidence](../evidence/ledger.md)。

- **能加载 ≠ 可用**：`parsed=true` 只到语法；S4（endpoint 假阳性）、S6（无 target 静默）都可能在「加载成功」后发生。
- **`violations=2` ≠ 干净**：只证明两个已声明坏样本被抓住，不证明干净数据无误报。
- **三关过 ≠ 生产**：没有真数据误报率、延迟、权限、规模、版本回滚；fixture 是合成 5 表/13 列。
- **版本不可精确 replay**：`snapshot` 是日期标签，`tag_version`/`contract_version` 是 fixture 约定；没有内容 hash 和 parser 版本。要 replay，先把这三件事补齐。

