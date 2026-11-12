---
status: draft
source_type: standard
standing: normative
reading: 精读
provenance: 原文正文
updated: 2026-11-11
batch:
source: https://bitol-io.github.io/open-data-contract-standard/v3.1.0/
author: LF AI & Data / Bitol（Open Data Contract Standard 项目）
published: 2025-12-08
influence: LF AI & Data（Bitol）托管的开放 data contract 标准，v3.1.0 于 2025-12-08 批准（APPROVED）；data contract 类工具/平台互操作的参照之一（采用面未核，见待核末条）
updates: []
admission: admitted
gate_checked: 2026-11-11
impact_evidence: "I1: LF AI & Data / Bitol approved"
liveness: standard-in-force
provenance_type: foundation
---

# Open Data Contract Standard (ODCS) v3.1.0

> 本卡读的是**规范正文**（v3.1.0 pinned 文档站，抓取 2026-11-10）：首页 + fundamentals + schema + roles + SLA + servers + data quality + changelog，共 6 个分节；references / pricing / support / team / custom 未读。**未跑任何 validator，未拿真实契约验。** 字段与 Required 列照录（`已核`）；「能不能当消费者契约用」是映射推断（`推测`）；缺项 `待核`。

## 它主张什么

1. **契约的最小核是身份 + 结构，不是访问与服务水平**：顶层只有 5 个字段必填（`apiVersion`/`kind`/`id`/`version`/`status`），`schema` 必填；`servers`/`roles`/`slaProperties`/`quality` 全部可选（`已核`，照录 fundamentals 与各节 Required 列）。
2. **结构层只有两层，关系只有外键**：object（表/主题/文件/API）与 property（列/字段）；v3.1.0 新增的 `relationships` 是外键（支持复合键、嵌套引用、`customProperties`）。没有类层次、没有推理、没有 SPARQL——它描述「数据产品长什么样、在哪」，不是本体 schema（`已核`）。
3. **服务层是两套互不引用的承诺**：SLA 用 `property`/`value`/`unit` 表达交付承诺（`frequency`/`latency`/`retention`/`timeOfAvailability`…）；quality 用「可执行检查」（`library` 指标、`sql` 查询、`custom` 引擎）+ 比较算子（`mustBe`/`mustBeLessThan`/`mustBeBetween`…）表达数据约束。两者都绑到元素/属性，不绑到「某个消费者问什么」（`已核`字段，负向结论的范围见待核 4）。

**字段面（Required 照录）**：

| 节 | Required = Yes | Required = No（含条件必填） |
|---|---|---|
| metadata | `apiVersion`（默认 `v3.1.0`）、`kind`（值 `DataContract`）、`id`、`version`、`status` | `name`、`tenant`、`tags`、`domain`、`dataProduct`、`authoritativeDefinitions`、`description.*`（purpose/limitations/usage/…） |
| schema | `schema`（顶层数组）、元素的 `name` | 元素级 `id`/`physicalName`/`physicalType`/`businessName`/`description`/`quality`/`tags`/`customProperties`；属性级 `logicalType`/`logicalTypeOptions`/`required`/`unique`/`primaryKey`/`primaryKeyPosition`/`partitioned`/`partitionKeyPosition`/`classification`/`encryptedName`/`transformSourceObjects`/`transformLogic`/`transformDescription`/`examples`/`criticalDataElement`/`items`；对象级 `dataGranularityDescription` |
| roles | `roles[].role` | `roles`（顶层）、`roles[].access`、`firstLevelApprovers`、`secondLevelApprovers`、`description`、`id` |
| SLA | `slaProperties[].property`、`slaProperties[].value` | `slaProperties`（顶层）、`element`、`driver`、`description`、`scheduler`、`schedule`；`unit` 与 `valueExt` 标「No - unless needed by property」（按属性条件必填） |
| servers | 条目内 `server`、`type`；类型专属字段（如 postgres `host`+`database`、s3 `location`、local `path`+`format`） | 条目内 `id`/`description`/`environment`/`roles`/`customProperties`；**`servers` 顶层本身 → 待核 1** |
| data quality | 条件必填：`library`→`metric`；`sql`→`query`；`custom`→`engine`+`implementation`；算子（如 `mustBe`）按其分支必填 | `quality`（顶层）、`type`（默认 `library`）、`dimension`/`severity`/`unit`/`businessImpact`/`method`/`arguments`/`scheduler`/`schedule`/`name`/`description`/`tags`/`customProperties` |

> 注意 `required` 一词在 ODCS 里有**两个所指**：property 级的 `required` = 该属性允许 null 吗（数据约束）；而 `server`/`type`/`metric` 那层是「契约字段是否必须写」（元数据必填）。与 `load` 在 A.1/A.5 的碰撞同型，见「与已有判断的关系」第 2 行。

## 场景与 scope

- **场景**：data producer 与 data consumer 之间的**单数据集**接口描述，平台无关（RDBMS / 数仓 / 对象存储 / 消息 / API）。`servers` 支持一个契约对多环境（dev/UAT/prod）与多技术（同一数据同时以 Kafka topic 和 BigQuery table 提供）成立。
- **版本位置**：v3.1.0 = 2025-12-08 APPROVED；把 v3.0.2 的单页规范拆成 11 个分页（本卡 6 个）；新增 `relationships`（外键）；`slaDefaultElement` 与 v3.0.x 的 `team` 数组结构标 deprecated（v4 移除）。
- **本卡边界**：只读规范，不读实现、不跑 schema validator、不做契约样例往返。`reading: 精读` 指读到 6 节全部字段表，不等于读完全部 11 节。
- **哪些结论只在这个场景成立**：所有「Required」判断都是**规范文本的声明**，不是被工具执行的实测。ODCS 自述 JSON schema 是伴生件，冲突时以标准为准——所以本卡把 schema 当旁证，不当判据。
- **明确不覆盖**：查询接口 / 结果集契约、消费者的消费时刻、拒绝条件与策略谓词、类层次与推理、权限执行（只到 IAM 角色名与审批人姓名）。

## 证据强度

- **一手还是转述**：一手。v3.1.0 pinned 文档正文；changelog 一手；JSON schema 一手但它是「伴生件」，标准自述优先。
- **有数据吗**：无。规范文本，不含测量、样本、采用率、误报率或延迟。
- **数据规模与场景**：11 节规范 + 示例 YAML（支付/零售表）。本卡未做实现测试，未验证任何字段被工具消费。
- **可复现吗**：字段与 Required 列可逐条回原页复核（`已核`，抓取日 2026-11-10）；「与 A.1 的等价性」「缺哪些格」是映射推断，不能从这里复现（`推测`/`待核`）。
- **证据等级一句话**：字段存在与必填 = `已核`（照录）；ODCS 能否替代 A.1 契约 = `推测`；`servers` 顶层必填、`timeOfAvailability` 合法性、全文有无 answers/refuses = `待核`。
- **不能当**：不能当「ODCS 已被广泛采用」的证明（Vendors 页未读，没有落地数字）；不能当「契约字段够用」的证明（无实现对照）；不能把 `quality` 当 SHACL/shape 的等价物。

## 与已有判断的关系

| 判断 | 关系 | 说明 |
|---|---|---|
| [consumability §3](../../../topics/05-produce/representation/consumability.md)（契约六项 ↔ `build_report` 不是一一对应）/ [05-L10](../../../topics/05-produce/claims.md) | 支持（字段层） | ODCS 正好落在 §3 说的「`load` 碰撞」上：`servers`（`type`/`host`/`location`/`environment`）是**怎么连**，没有 `parsed`/`violations` 这类**加载结果**字段。`roles`/`slaProperties`/`quality` 里也没有 `answers`/`refuses` 的对应物 → 「契约字段 ≠ `build_report`」再得一个标准侧实例。**但 05-L10 等级不动**：规范文本不是实现证据。 |
| §3 的「三个语义碰撞」（`load` / `violations`≠`refuses` / `missing_fields`≠契约缺字段） | 可加第四个候选 | ODCS 的 `required` 在 property 级 = 「允许 null 吗」，在契约层 = 「字段必须写吗」。同词同型，且比前三个更容易混——因为两处都叫 required、都在写契约时用。 |
| [build.md A.1](../../../deliverables/04-worked-example/03-body/01-build.md)（五格：consumer/principal/moment/answers/refuses/load） | 部分对应，缺 3 格 | consumer←无独立字段（最近 `roles[].role` + `servers[].roles`）；principal←`roles[].role`（IAM 角色名，弱；`tenant` 是「数据主要关联的属性」不是主体）；moment←无（`servers.environment` 是环境不是时刻，`slaProperties.timeOfAvailability` 是承诺交付时点，不是消费时刻）；answers←无；refuses←无（`roles.access` 是 read/write 授予，不是「拒 level≥3」这类谓词）；load←`servers`。`已核`（字段层），整体等价性 → 待核 3。 |
| [build.md A.5](../../../deliverables/04-worked-example/03-body/01-build.md)（`build_report`：`load.violations` / `caught` / `answer`） | 不足替代 | A.5 的 `violations` 带 `focusNode`/`resultPath`/`sourceShape`（shape 违反记录）；ODCS `quality` 产出的是**指标值 + 算子比较**（`nullValues mustBe 0`、`invalidValues mustBeLessThan 5`），不是 violation 记录，也没有「哪个 shape 被违反」。拿 quality 顶 validate 会把「超阈值」当「违反 shape」。`推测`（读两边字段，无实现） |
| [build.md A.2](../../../deliverables/04-worked-example/03-body/01-build.md)（三档：词表/结构表/逻辑表） | 无关 | ODCS 不分表达力档位。`logicalType`（string/date/number/…）与 `logicalTypeOptions`（format/minimum/pattern…）是数据类型与取值域，不是「能推出什么」的档位差。 |
| `topics/conclusions.md` 的 E-xx | 不触 | 本卡不产生 E，也不改任何 E 的等级。 |

**不升 E / 不改判**：本卡只写这一个文件。[consumability §5](../../../topics/05-produce/representation/consumability.md) 里 ODCS 那行（`待核`，网页未入库）现在可以指到本卡，但 §3 的 `推测` 与 05-L10 的等级都不动——读规范≠验实现。要动 topics，需要另起一轮。

## 待核项

- [ ] **`servers` 顶层是否 Required**：servers 分页只给「Common Server Properties」（条目内 `server`/`type` = Yes），**没有顶层必填表**；配套 JSON schema 的顶层 `required` 是 `["version","apiVersion","kind","id","status"]`，不含 `servers`。按 schema 判 No，但标准自述优先于 schema，文本层面无法直接判定 → `待核`。不要写成「servers 必填」或「servers 可选」的定论。
- [ ] **`timeOfAvailability` 是不是合法 `property` 值**：它只在 SLA 示例里出现两次（`value: 09:00-08:00` + `driver: regulatory/analytics`），**不在**「Valid Values for SLA Properties」清单里（清单为 availability / throughput / errorRate / generalAvailability / endOfSupport / endOfLife / retention / frequency / latency / timeToDetect / timeToNotify / timeToRepair）。清单是否穷尽（`slaProperties.property` 类型是 open string）→ `待核`。
- [ ] **与 A.1 六格的等价性**：本卡只做了「最近邻字段」，没有判定 `roles.access: read` 能否算 `answers` 的一部分、`servers.environment` 能否算 `moment`，也没有消费者视角的可执行映射（哪条契约行由谁在什么时刻读）。整体等价性 → `待核`。
- [ ] **是否覆盖查询级 answers/refuses**：读到的 6 节里没有此类字段，但 references / pricing / support / team / custom 未读，**不能断言全标准没有**。要断言需扫完 11 节。
- [ ] **文档 vs 伴生 schema 的冲突实例**：Athena 的 `stagingDir` 文档表标 No、JSON schema 却列入 required；`dataProduct` 文档未标废弃、schema 标 `deprecated`。按「标准优先」应采文档，但需确认是文档 bug 还是 schema bug——这决定 schema 能不能当校验基线。
- [ ] **`quality` → SHACL/LinkML 能否机械生成**：`quality` 是 metric + operator，`schema` 侧没有约束关键字（无 `pattern` 之外的跨行约束）；能否转成 shape/validator 未测。别在 04 里假定「有契约就有校验」。
- [ ] **采用面**：Vendors 页未读；不写市占、不写落地数量。`influence` 只保留「LF AI & Data 托管 + 2025-12-08 批准」这一层。

## 喂到哪个主题

- [consumability §3](../../../topics/05-produce/representation/consumability.md)：补 ODCS 侧锚点——`servers` 落在 A.1 的 `load`、`quality` 不产出 `violations`、`answers`/`refuses` 无对应物、`required` 是第四个碰撞候选。§5 来源表的 ODCS 行可从「网页；未入库」改为指本卡，等级仍按「规范文本」记（不是实现证据）。
- [build.md A.1](../../../deliverables/04-worked-example/03-body/01-build.md)：说明五格**不能从 ODCS 直接抄**——ODCS 稳定只供 `load`（servers）与被动的角色名，consumer/moment/answers/refuses 仍须自造。**只读不改表。**
- [build.md A.5](../../../deliverables/04-worked-example/03-body/01-build.md)：`quality`（metric+operator）≠ `violations`（shape 违反记录）的外部佐证。
- 同目录没有 `digest`（web 材料卡即消化正文，见 [web/README](../README.md)），故下游引用本卡；本卡未改 topics/deliverables/meta，也未在 [src 台账](../README.md) 登记。
- 不升 [conclusions.md](../../../topics/conclusions.md)；不给 04 添新判断。

## 原文摘录

> "The provided JSON schemas are companions to the standards (ODCS or ODPS), it means that they do not define the standards and may include bugs. In case of conflict between the standard and the JSON Schema, the standard takes precedence."
>
> — 首页 · Notes

> "The `servers` element describes where the data protected by this data contract is _physically_ located. That metadata helps to know where the data is so that a data consumer can discover the data and a platform engineer can automate access."
>
> — Infrastructure & Servers · 开头

> "**Objects** are a structure of data: a table in a RDBMS system, a document in a NoSQL database, and so on. **Properties** are attributes of an object: a column in a table, a field in a payload, and so on. **Elements** are either an object or a property."
>
> — Schema · 开头

> "This section lists the roles that a consumer may need to access the dataset, depending on the type of access they require."
>
> — Roles · 开头

> "Use the `Object.Element` to indicate the number to do the checks on, as in `SELECT txn_ref_dt FROM tab1`."
>
> — SLA · 开头

> "Data quality rules support different levels/stages of data quality attributes: **Text**: A human-readable text that describes the quality of the data. **Library** : A maintained library of commonly used quality metrics such as `rowCount`, `nullValues`, `invalidValues`, and more. **SQL**: An individual SQL query that returns a value that can be compared. **Custom**: Quality attributes that are vendor-specific, such as Soda, Great Expectations, dbt tests, dbx, or Montecarlo monitors."
>
> — Data Quality · 开头

> "v3.1.0 - 2025-12-08 - APPROVED" … "**Splits** Main specification document into several smaller documents."
>
> — Changelog

> `- id: reg_toa` / `property: timeOfAvailability` / `value: 09:00-08:00` / `element: tab1.txn_ref_dt` / `driver: regulatory`
>
> — SLA · Example（`timeOfAvailability` 只出现在示例，见待核 2）

出处：`https://bitol-io.github.io/open-data-contract-standard/v3.1.0/`（及 `/fundamentals/`、`/schema/`、`/roles/`、`/service-level-agreement/`、`/infrastructure-servers/`、`/data-quality/`、`/changelog/`），抓取 2026-11-10。Required 列与 schema 顶层 `required` 取自
`https://raw.githubusercontent.com/bitol-io/open-data-contract-standard/main/schema/odcs-json-schema-v3.1.0.json`（伴生件，冲突时以标准为准）。
