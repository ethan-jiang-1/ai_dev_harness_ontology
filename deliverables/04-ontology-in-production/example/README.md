---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# 例子数据（fixture）：5 分钟跑通

> 5 表 / 13 列。**断言式三元组存储，无 entailment**；`:hasColumn` 与 `:columnOfTable` 两侧显式写入；`owl:inverseOf` 只是文档。**决策单位 = triple subject（列）**。`tag_email_1` 是 `:WorkEmail`（`:Email` 子类），CQ1 的 `rdfs:subClassOf*` 因此真正被执行。200 表/5,000 列只作 Glyph 量级参照，不是本 fixture。

## 文件清单

| 文件 | 是什么 | 对应产物 |
|---|---|---|
| [ontology.ttl](./ontology.ttl) | TBox：11 类 / 5 属性 | ② Turtle |
| [catalog.ttl](./catalog.ttl) | ABox：5 表 / 13 列 / 标签 | ② Turtle |
| [shapes.ttl](./shapes.ttl) | 2 条 SHACL shape | ③ shapes |
| [policy.json](./policy.json) | 7 条策略规则 | ⑤ policy 表 |
| [policy_tests.json](./policy_tests.json) | 11 条输入 → 期望 decision | ⑥ 策略测试 |
| [leak_cases.json](./leak_cases.json) | 12 条泄漏用例 | ⑦ 泄漏用例 |
| [audit.schema.json](./audit.schema.json) | audit record JSON Schema | ⑧ audit schema |
| [audit_records.json](./audit_records.json) | 3 条 audit 记录（deny + skip/leak + allow） | ⑧ audit record |
| [fault_matrix.json](./fault_matrix.json) | 10 类故障 × 3 段 | ⑨ 故障矩阵 |

## 5 分钟跑通查询子集（可选）

> 需要 `rdflib` + `pyshacl`（`pip install rdflib pyshacl`）。以下命令在本目录跑；下面的数字是 fixture 期望，不是运行记录。

```bash
# 1. 解析三个 TTL（期望 3/3 parsed）
python3 - <<'PY'
import rdflib
for f in ["ontology.ttl", "shapes.ttl", "catalog.ttl"]:
    g = rdflib.Graph(); g.parse(f); print(f, len(g), "triples")
PY

# 2. 跑 shapes（期望 2 violations：tag_unknown / col_legacy）
python3 - <<'PY'
from pyshacl import validate
conforms, _, text = validate("catalog.ttl", shacl_graph="shapes.ttl",
                             inference="none", advanced=False)
print("conforms:", conforms); print(text[-800:])
PY

# 3. 跑 CQ1（期望 2 列 / 2 表）
python3 - <<'PY'
import rdflib
g = rdflib.Graph(); g.parse("catalog.ttl")
q = """PREFIX : <https://ex.org/c#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?col ?table WHERE {
  ?col :hasTag ?t ; :columnOfTable ?table .
  ?t a/rdfs:subClassOf* :Email .
}"""
for row in g.query(q): print(row)
PY
```

**期望**（与 [A.5](../body/build.md)/[B.2](../body/consume.md) 一致）：

- 解析：3/3；TBox 11 类/5 属性；shapes 2。
- `pyshacl`：`conforms=false`，2 violations（`tag_unknown` 缺 `sensitivityLevel`；`col_legacy` 的 `hasTag` 是字面量）。
- CQ1：2 行（`col_email`、`col_customer_email`）/ 2 表。
- CQ2：4 表 / 7 列；CQ3：4 个 dataset 各 1。

**跑不通时**：先看 [症状地图](../sections/map.md)；`0 violation` 可能是 shape 没有 target，不是数据干净。

## 策略与泄漏（没有引擎，怎么用）

- [policy_tests.json](./policy_tests.json)：11 条输入 → 期望 decision。用任意 JSON/脚本按 `policy.json` 的 8 条规则判；T9 故意留成 `undetermined`，不要强行给 allow/deny；T11 是 governance 的 dataset 级 allow。
- [leak_cases.json](./leak_cases.json)：12 条查询与期望；`expected_rows` 只对 filter/allow 用例有意义，deny/withhold 看 `expected_absent`；`trustgraph` 列是 pin `184f622` 的已知行为，不是实测。`object_direction_failed` 是预期缺口，不是用例写错。
- [audit.schema.json](./audit.schema.json)：用 `jsonschema` 校验 [audit_records.json](./audit_records.json) 的三条记录（对应 [govern C.4](../body/govern.md)）；`policy_version/tag_version/snapshot` 必须能回放。

## 数据

| table | column | tag | level |
|---|---|---|---|
| t_users | col_email | WorkEmail（Email 子类） | 3 |
| t_users | col_phone | Phone | 3 |
| t_users | col_name | Name | 2 |
| t_orders | col_order_id | — | — |
| t_orders | col_amount | Financial | 3 |
| t_orders | col_customer_email | Email | 3 |
| t_hr | col_ssn | SSN | 4 |
| t_hr | col_salary | Financial | 4 |
| t_hr | col_dept | — | — |
| t_sales | col_region | — | — |
| t_sales | col_revenue | Financial | 3 |
| t_sales | col_rep | Name | 2 |
| t_legacy | col_legacy | `"email"`（字面量，坏样本） | — |

## 说明

- 坏样本是故意留的：`tag_unknown` 与 `col_legacy` 只用于 shape 违反，不参与 CQ1/CQ2；**CQ3 会把 `col_legacy` 计入**（它的 `hasTag` 是字面量、没有 level，`FILTER NOT EXISTS` 判为未打标）——这是预期，不是数据错。
- 每条 `:columnOfTable` 都同时有 `:hasColumn` 反向三元组；不要依赖推理。
- 数据是合成的，不代表任何真实目录；规模参照见 `O-N28`。
