---
status: draft
updated: 2026-11-10
rq: [RQ2, RQ4]
evidence: [E-20] # 原 E-02 已于 2026-11-11 撤回
---

# 输出校验：把结果对象当判据

> [checker](./README.md) 问「本体能不能判产出」；本页问「查询结果/结构化输出本身能查什么」。
> 同一时刻、不同判据：输入 shape 管「结构对不对」，输出校验管「这次结果可不可信」。

## 0. 三句话

- **输出校验是 checker 的补充，不是替代。** 它查 schema/基数/来源/新鲜度/跨字段/语义合理性，不查「业务上对不对」。
- **必须三态**：pass / violation / undetermined；把 undetermined 合并进 pass 会污染 catch/FA 的分母。
- **先有输入 shape，再谈输出校验**：输入侧没约束，输出侧只能做事后抽样。

## 1. 与输入 shape 的分工

| 层 | 问什么 | 例子 | 失败长什么样 |
|---|---|---|---|
| 输入 shape | 数据/产物的结构对不对 | `Tag` 必须有整数 `sensitivityLevel` | 坏样本被标红 |
| 输出校验 | 这次结果集/回答可不可信 | CQ2 返回 7 列，但有一列缺 level | 空结果、少行、越权、过期 |
| 语义判定 | 业务上对不对 | `col_ssn` 是否真是 SSN | 需要外部判据/人审 |

> 输出校验不能证明语义正确；它只能把「结果不可信」的几种可判定形态标出来。

## 2. 六类校验

| # | 类 | 检查什么 | 失败例 | 误报风险 | 成本 | 工具锚 |
|---|---|---|---|---|---|---|
| 1 | schema | 结果列名/类型/非空 | CQ1 返回 `?col` 为字面量 | 低 | 低 | SPARQL `SELECT` + JSON schema |
| 2 | cardinality | 行数/表数/列数在期望范围 | CQ2 返回 0 行；CQ3 少一个 dataset | 中（数据本来就可能为空） | 低 | `COUNT` / `expect_table_row_count_to_be_between` |
| 3 | provenance | 每行带 `query_id`/`snapshot`/`version` | 结果无法回放到某次快照 | 低 | 低 | 04 audit record；PROV-O |
| 4 | freshness | snapshot 在 SLA 内 | 用了 30 天前的快照 | 中（SLA 未定） | 低 | snapshot 元数据 |
| 5 | cross-field | 字段间一致（level vs tag；policy vs resource） | `col_ssn` level 2 但 tag 是 SSN | 中（规则可能过严） | 中 | SPARQL `FILTER` / 校验脚本 |
| 6 | semantic plausibility | 结果分布/类型是否反常 | 所有列都 level 4；某表列数突增 | 高（无基线） | 中 | 统计基线；人审抽样 |

> 1–4 类可以自动化；5 类要领域规则；6 类只能做「异常提示」，不能当判定。

## 2.5 audit record 的字段（provenance 类校验的落地清单）

> 原 04 走查（已退役，[ADR 0015](../../../adr/0015-retire-04-and-renumber-05-to-10.md)）的 audit schema 搬到这里；**值是构造样例，不是生产记录**。

一次判定要能回放，至少留这些字段：

| 组 | 字段 | 为什么 |
|---|---|---|
| 身份 | `decision_id` `query_id` `who` `action` | 谁、对哪次查询、做了什么动作 |
| 快照 | `snapshot` `policy_version` `tag_version` | 复算要能指回当时的策略与标签版本（严格 replay 还需内容 hash + parser 版本） |
| 判定对象 | `judged_subject` `subject_kind` `judged_triple` `resource_level` | **判定单位是输出行的 subject**；表/dataset 级没有列 subject（见 [policy F4](../../01-constraint/policy/findings.md)） |
| 上下文 | `user_context`（role/clearance） | 输入有、规则不一定消费 |
| 结果 | `decision`（allow/deny/skip/undetermined）`reason` `execution_effect` `obligation` | `skip` 必须带 reason；`obligation: log` 不参与判定 |
| 泄漏观测 | `leaked_object` `leaked_object_level` `outcome` `leak_check` | 判定与「实际返回了什么」分两栏记，否则看不见 skip→leak |

构造样例（table 级 subject 判 skip、object 方向仍返回 `col_ssn`）：

```json
{"decision_id":"dec-0002","query_id":"LEAK-T1","judged_subject":":t_hr","subject_kind":"table",
 "resource_level":null,"user_context":{"role":"analyst","clearance":2},
 "decision":"skip","reason":"table_subject_not_judged","execution_effect":"returned",
 "obligation":"log","leaked_object":":col_ssn","leaked_object_level":4,
 "outcome":"returned t_hr/col_ssn","leak_check":"object_direction_failed"}
```

> 读法：`decision=skip` 与 `leak_check=object_direction_failed` 并存，就是「未判定被当成了不拦」。字段名是 `local` 约定，不对应任何标准。

## 3. 三态 verdict

```json
{
  "verdict": "pass | violation | undetermined",
  "query_id": "CQ2",
  "snapshot": "2026-11-10",
  "policy_version": "0.3.0",
  "checks": [
    {"id": "schema", "state": "pass", "detail": "?table, ?col 均非空"},
    {"id": "cardinality", "state": "pass", "detail": "4 表 / 7 列"},
    {"id": "provenance", "state": "undetermined", "detail": "缺 snapshot 字段"}
  ],
  "coverage": {"checked": 2, "total": 3}
}
```

**语义**：

- `pass`：所有 check 都跑了且通过；不是「没发现问题」。
- `violation`：至少一个 check 失败；带 `detail` 与证据。
- `undetermined`：check 没跑/跑不完/样本不足；不能当 pass。
- `coverage`：`checked/total`；没有它，catch/FA 不可比。

开源侧已有实现把 undetermined 做成独立状态：open-ontologies 的 verified 路径用 exit code 3，默认路径会 skip 不支持的约束（`skipped_constraints`）；外层 `gate_exit_code` 会把 `conforms:null` 映射为 exit 2，与解析失败同码。引用时必须说明是哪一层。

依据：[checker F7](./findings.md)；[open-ontologies digest](../../../src/open-source/fabio-rovai-open-ontologies/digest.md) §3–§5。

## 4. 示例 8 条检查（原 04 fixture，已退役）

> 下表来自原 04 的合成 fixture（5 表/13 列），**数字只作形状示范，不再是可跑的样例**；fixture 已随 [ADR 0015](../../../adr/0015-retire-04-and-renumber-05-to-10.md) 退役。

| # | 检查 | 查询/规则 | 期望 | 失败时 |
|---|---|---|---|---|
| 1 | CQ1 schema | 返回 `?col ?table`，两列均 IRI | 2 行 / 2 表 | violation |
| 2 | CQ2 基数 | `COUNT(DISTINCT ?col)` = 7；`COUNT(DISTINCT ?table)` = 4 | 7 / 4 | violation 或 undetermined |
| 3 | CQ3 覆盖 | 4 个 dataset 各 1 行 | 4 | undetermined（可能缺 dataset 边） |
| 4 | T1 泄漏 | `SELECT ?col WHERE { :t_hr :hasColumn ?col }` | 含 `col_ssn` → violation | violation（object 方向） |
| 5 | provenance | 每行带 `query_id/snapshot/policy_version` | 全有；fixture 无 PROV → undetermined | undetermined |
| 6 | freshness | `snapshot` 在 SLA 内 | 有 `xsd:dateTime` 且在 SLA；无时间戳 → undetermined | undetermined |
| 7 | cross-field | `col_ssn` 的 `sensitivityLevel` = 4；`tag_ssn` 的 level 一致 | 一致 | violation |
| 8 | 语义合理性 | 等级分布不应全 4；某表列数不应突增 | 正常 | undetermined（仅提示） |

> **负控制**：每条 check 都要有一个「已知违反」样本；否则 `0 violation` 可能只是 `targeted=0` 的空转。`sh:targetClass` 在答案图上没有实例时，pyshacl 会返回 `conforms=true`，这不是 pass，是 `no_target` → undetermined。

**SPARQL 片段（5/7）**：

```sparql
# 5 provenance：结果行必须能回放到某次快照
SELECT ?col ?table ?snapshot WHERE {
  ?col :hasTag ?t ; :columnOfTable ?table .
  ?t a/rdfs:subClassOf* :Email .
  BIND("2026-11-10" AS ?snapshot)
}

# 7 cross-field：tag 与 column 的 level 不一致
SELECT ?col ?tagLevel ?colLevel WHERE {
  ?col :hasTag ?t ; :sensitivityLevel ?colLevel .
  ?t :sensitivityLevel ?tagLevel .
  FILTER(?tagLevel != ?colLevel)
}
```

> 第 5 条是模板：真实实现里 `snapshot` 来自执行器元数据，不是 `BIND`。这里只示范「结果行要带版本」的字段，不把 `BIND` 当生产写法。

## 5. 与 expectations 的映射

| 输出校验类 | Great Expectations（已入库，部分） | 说明 |
|---|---|---|
| schema | `expect_column_values_to_not_be_null` / `expect_column_to_exist` | 列存在与非空 |
| cardinality | `expect_table_row_count_to_be_between` | 行数区间 |
| cross-field | `expect_column_values_to_be_in_set` / 自定义 expectation | 等级/枚举一致 |
| provenance | 无现成 expectation | 需要自定义；字段清单见 [§2.5](#25-audit-record-的字段provenance-类校验的落地清单) |

> Great Expectations 已入 [digest](../../../src/open-source/fivetran-great-expectations/digest.md)：确认的是 `ExpectTableRowCountToBeBetween` 的 `success`/`table.row_count` 模型（一个 core expectation）；`validator.py`/`ExpectationSuite` 路径待核。它是数据质量工具，不是本体校验器。
>
> **三个坑**：`success` 是布尔，`mostly`/`row_condition` 会静默缩小分母（与 undetermined 同一种污染）；`catch_exceptions=True` 时异常进 `exception_info`，`success` 可能仍为 true；GE 没有 undetermined，最接近的是 OpenLineage `TestRunFacet.status: pass/fail/skip`，但 `skip` = 未执行，不等于「跑了但定不了」。

## 6. 边界

- **校验 ≠ 语义正确**：schema/基数/来源都对，不代表业务对；语义错要 checker/人审。
- **三态 ≠ 覆盖率**：报 pass/violation/undetermined 三个数，不等于知道漏了什么。
- **输出校验不能替代输入 shape**：输入侧没约束，输出侧只能抽样。
- **`0 violation` 不等于检查有效**：先看 `targeted>0` 且 `skipped=0`；否则是空转。
- **golden count（2/4/7）只在 fixture 成立**：生产没有 ground truth，只能基线 + 分层抽样。
- **CQ3 的文档矛盾**：原 04 的 `example/README`（已退役）写「CQ3 不把 `col_legacy` 算作未打标」，但期望结果是 4 个 dataset 各 1（含 `ds_legacy`）；按图计算，`col_legacy` 的 `hasTag` 是字面量、无 level，会被 CQ3 计入。**该改的是说明，不是数据**（`已核`：读图对账，未跑）。
- **误报/成本未测**：6 类里只有 schema/cardinality 的成本低；cross-field 与 semantic plausibility 的误报没有本仓库数据。
- **不要写「输出校验能拦住越权」**：它只能标出「结果与策略不一致」；执行层语义见 [policy F4](../../01-constraint/policy/findings.md)（skip ≠ allow）。

依据：原 E-02（已撤回，历史对照）；[checker F7/F8](./findings.md)；[open-ontologies digest](../../../src/open-source/fabio-rovai-open-ontologies/digest.md)；gap：误报/成本、生产数据。
