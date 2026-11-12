---
status: draft
updated: 2026-11-12
rq: [RQ2, RQ5]
evidence: [E-12]
---

# 可消费性：三关记录，不是产物属性

> 回答：一个本体/生成物「能被消费」怎么判定；三档表示在四类消费上的能力差；契约字段与 `build_report` 怎么对。
> 不回答：本体怎么建（[README](./README.md)）、生成路线怎么选（[generation](../generation/README.md)）、判定器质量（[02/checker](../../02-judgment/checker/README.md)）。
>
> **口径**：本页所有 `A.1/A.5/S1–S10/CQ1–CQ3/fixture` 都指**原 04 的合成构造例**（5 表/13 列）。该构造例已随 [ADR 0015](../../../adr/0015-retire-04-and-renumber-05-to-10.md) 退役，这里保留的是判据与坏样本清单，**仓库内不再有可跑的样例**。

## 0. 三句话

- **可消费不是产物属性，是三关记录**：load（拿到声明的图/模式）、validate（对已知坏样本与干净样本给出预期报告）、answer（对声明的 CQ 给出可核对答案，0 行能分因）。缺一关只能写「只测了 X」。
- **现有 `build_report` 只覆盖 load/validate 的一部分**：A.1 六项里只有 `load` 有对应物，且语义从「加载方式」漂移成「加载结果」；`violations` 不是 `refuses`，`missing_fields` 不是契约缺字段。
- **结构表是唯一三关都 supported 的档**；词表 load/query 可用、validate/explain 弱；逻辑表 load 可、validate/query partial、explain not，成本最高。证据只到标准/代码/单域，不证明生产可用。

## 1. 三关判据

| 关 | 可测判据（最小） | 通过例 | 失败例 | 未测例 |
|---|---|---|---|---|
| **load** | pinned parser 下 `parsed=true`；`classes/properties/shapes` 与 manifest 一致；每个 shape 有 target；consumer 的 endpoint/auth 可达 | fixture 三文件解析；`{parsed:true, classes:11, properties:5}`；shapes 2 | Turtle 语法错；shape 缺 target；endpoint 不可达 | consumer 真 endpoint/auth/timeout；第二 parser；规模 |
| **validate** | 已知坏样本每条 ≥1 violation（`focusNode/resultPath/sourceShape/sourceConstraintComponent`）；干净样本 0；`violations=|B|`；shapes 过 shacl-shacl | `violations=2`（字面量 tag、缺 level） | 删一条 shape → 少 1；target 过宽 → 干净样本被标 | 真数据 FP/FN；跨 validator；severity→决策 |
| **answer** | `query_id` + query hash + expected 集；actual 匹配（无序）；0 行分因；记录 executor/snapshot/version | CQ1 2 列/2 表；CQ2 4 表/7 列；CQ3 4 数据集 | 删 dataset 边 → CQ3 3；子类缺失 → CQ1 0；超时 | 自由问句/agent；生产延迟；跨域 |

**记录字段**（建议，不是标准）：`{gate, artifact, consumer, principal, moment, query_id, expected, actual, parser_version, ontology_version, policy_version, provenance, result}`。`未测 ≠ 通过；0 行 ≠ 失败，先分因。`

## 2. 三档 × 四消费位置

> 状态：`supported` = 有标准/可运行产物且演示过；`partial` = 只覆盖一部分或需第二机制；`not` = 本仓库证据内无可移植路径。均不表示生产可用。

| 档 \ 消费 | load | validate | query | explain | 成本 |
|---|---|---|---|---|---|
| **词表** | supported（A.3/A.5 解析） | partial（只能查 IRI/必填；基数/范围要 shape） | supported（CQ1 `rdfs:subClassOf*`） | partial（label/comment + 直接 source；无推导链） | 低（估算） |
| **结构表** | supported（Turtle/YAML；LinkML `gen-shacl`） | supported（SHACL core；fixture 2/2） | supported（3 CQ 期望集） | partial（报告有 focus/path/sourceShape；无业务理由） | 中（估算；2–4 人周建模 + 3–5 人日 shapes，`推测`） |
| **逻辑表** | supported（OWL 2 可解析；profile 另计） | partial（一致性/包含可推；闭世界数据约束不在 OWL） | partial（断言可查；推断需物化/重写；OWL 2 QL only） | not（无标准 justification 记录；个别 reasoner 有解释，未测） | 高（估算；结构表 + reasoner/profile/解释） |

**读法**：这张表是能力矩阵，不是效应量。E-12 的 +54.6pp 是**文本投影**的命名/单位效应（n=1 工厂、9 任务），不是三档对照；不能拿来证明「词表够用」。SFE-O（已撤回）只证明「逻辑档表达 ≠ 执行」（历史参考），不能证明结构表覆盖多数场景。

依据：E-12；[SFE-O digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-37123) §4.1；[SHACL 材料卡](../../../src/web/w3c-shacl/w3c-shacl.card.md)、[LinkML docs](https://linkml.io/linkml/)（待入库）。

## 3. 契约六项 ↔ `build_report`

| `build_report`（A.5） | consumer | principal | moment | answers | refuses | load |
|---|---|---|---|---|---|---|
| `load.parsed` | — | — | — | — | — | ✓（仅本地解析） |
| `load.violations` | — | — | — | — | —（shape 违反 ≠ 拒绝） | ✓（shape） |
| `load.missing_fields` | — | — | — | — | — | ✓（产物必填，非契约） |
| `classes`/`properties` | — | — | — | — | — | ✓ |
| `policy_version`/`tag_version` | — | 弱（产物版本，非主体） | — | — | 弱（非拒绝谓词） | — |
| `provenance.source` | — | —（`synthetic` 不是 principal） | — | — | — | — |

**三个语义碰撞**：

1. **`load` 是碰撞**：A.1 的 load 是「怎么加载」（endpoint/格式），A.5 的 load 是「加载结果」（parsed/violations）。不拆就会拿「本地解析成功」冒充「消费者能加载」。
2. **`violations` ≠ `refuses`**：前者 shape 违反，后者策略拒绝；A.5 没有 `refused`。
3. **`missing_fields` ≠ 契约缺字段**：A.5 的必填是产物字段，不读 A.1；`missing_fields=[]` 不能证明六格完整。

**应新增**：`consumer`、`principal{role,tenant}`、`moment/as_of`、`answers{query_id,expected}`、`refuses{policy_id,condition}`、`contract_version`/`ontology_version`；`load_target` 与 `load_result` 拆开。

依据：原 04 的 build A.1/A.5（已退役，[ADR 0015](../../../adr/0015-retire-04-and-renumber-05-to-10.md)）；[ODCS 材料卡](../../../src/web/odcs-v3.1/odcs-v3.1.card.md)。

## 4. 十个坏样本

| # | 坏样本 | 失败类型 | 最小复现 | 期望 / 现状 | 等级 |
|---|---|---|---|---|---|
| S1 | 缺 principal | `missing_fields`（应）；silent（现状） | A.1 删 `principal` 格；跑 build gate | 期望 `["principal"]`；现状无字段 | `推测` |
| S2 | 缺 moment | 同上 | 删 `moment`；同一 artifact 供 UI/agent/governance | 期望拒绝；现状无时刻 | `推测` |
| S3 | 缺 refuse | 同上；全放行 | governance 行删「拒列身份/明细」；跑 level=4 用例 | 期望 deny；现状 refuses 无 | `推测` |
| S4 | 缺 load | `load.parsed=false`（应）；假阳性 | 把 load 改成不存在的 endpoint；只跑本地解析 | 期望 fail；现状 `parsed=true` | `推测` |
| S5 | 缺 version | `missing_fields`（应）；silent | 删契约 version + `owl:versionInfo` | 期望 missing；现状 tag/policy version 仍在 | `推测` |
| S6 | shape 缺 target | `missing_fields`（应）；silent | 删 `sh:targetClass :Tag`；跑 pyshacl | 期望 gate fail；现状 `conforms=true`, 0 results | `待核` |
| S7 | tag 是字面量 | `load.violations` | 保留 `:col_legacy :hasTag "email"`；跑 `HasTagClass` | 期望 1 violation | `已核`（A.5 示例） |
| S8 | level 缺失 | `load.violations` | 保留 `:tag_unknown a :Tag`；跑 `TagHasLevel` | 期望 1 violation | `已核`（A.5 示例） |
| S9 | 无 dataset 边 | `answer undercoverage`（非 violation） | 删 `:t_legacy :tableInDataset :ds_legacy`；跑 CQ3 | 期望 4；现状 3；parsed/violations 不变 | `推测` |
| S10 | 版本不一致 | `version skew`（silent） | 改 `owl:versionInfo`，保留 tag/policy version；跑 CQ1 | 期望 mismatch；现状无 `ontology_version` | `推测` |

**结论**：10 个里只有 S7/S8 被现有 `violations` 稳定抓住；S6/S9 需新增 target/边检查；S1–S5/S10 需契约/版本 schema。`推测`（读 A.5 + 文件，未跑 S1–S6/S9/S10）。

**范围补充**：`sensitivityLevel` 的合法域是 1–4；构造例的 shape 曾加 `minInclusive 1`/`maxInclusive 4`，但没有 0/负数坏样本，所以仍是 2 violations。S11 未入构造例；真实数据要加，否则 0/负数会绕过策略（fail-open）。

## 5. 来源与边界

| 来源 | 用到的锚 | 等级 |
|---|---|---|
| [ODCS v3.1.0](../../../src/web/odcs-v3.1/odcs-v3.1.card.md) | `version/status`、`servers`、`roles`、`slaProperties`、`quality` | `已核`（材料卡；Required 待核） |
| [W3C SHACL](../../../src/web/w3c-shacl/w3c-shacl.card.md) | targets、conformance、result 字段、shacl-shacl | `已核`（材料卡；条款待核） |
| W3C SHACL test suite | `core/property/minCount-001`、`core/node/nodeKind-001` 等 | `待核`（页面；未入库） |
| LinkML | `gen-shacl`（Beta）、`linkml-validate` | `待核`（文档；未入库） |
| CASTON | high 6/6、medium 0–25%；无下游 | `已核`（digest 转述；admitted） |
| OntoDoc（已撤回） | completeness 3.43→3.84；无下游 | 推测（源撤回，历史示例） |
| SFE-O（已撤回） | OWL 2 表达力够；约束未落 SHACL；无 agent 评测 | 推测（源撤回，历史示例） |

**不能证明**：

- **能加载 ≠ 可用**：`parsed=true` 只到语法；S4（endpoint 假阳性）、S6（无 target 静默）都可能在「加载成功」后发生。
- **文档质量 ≠ 可消费**：OntoDoc 的 completeness、CASTON 的专家接受率，都没有下游任务。
- **单域 ≠ 跨域**：SFE-O 一个萃取域；CASTON 单一本体/公理类型；fixture 5 表/13 列。
- **三关过 ≠ 生产**：没有真数据误报率、延迟、权限、规模、版本回滚。
- **`violations=2` ≠ 干净**：只证明两个已声明坏样本被抓住，不证明干净数据无误报。

## 6. 下一步

1. **跑 fixture**：parse + pyshacl + 3 CQ，记录原始输出；给 S6/S9/S10 加检查（shape target 必填、dataset 边 `ASK`、版本对账）。`待核`
2. **契约 schema**：六格 + version 做成可校验 schema，让 `build_report` 读契约；`missing_fields` 拆 `contract_missing`/`artifact_missing`。`推测`
3. **跨 validator**：pySHACL vs TopBraid 同 shapes/坏样本；SHACL test suite 121 例只当合规基线。`待核`
4. **P5/EXP**：找下游评估论文或仓库外实验；没有之前，本页只写「闸门与停」，不写「建完就能用」。
