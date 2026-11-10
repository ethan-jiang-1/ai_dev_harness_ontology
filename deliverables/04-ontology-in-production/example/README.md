---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# 例子数据（fixture）

> 5 表 / 13 列，页内可复现。TBox：[ontology.ttl](./ontology.ttl) ｜ shapes：[shapes.ttl](./shapes.ttl) ｜ ABox：[catalog.ttl](./catalog.ttl) ｜ 策略测试：[policy_tests.json](./policy_tests.json) ｜ 审计 schema：[audit.schema.json](./audit.schema.json) ｜ 泄漏用例：[leak_cases.json](./leak_cases.json) ｜ 故障矩阵：[fault_matrix.json](./fault_matrix.json)。**断言式三元组存储，无 entailment**；`:hasColumn` 与 `:columnOfTable` 两侧显式写入；`owl:inverseOf` 只是文档。**决策单位 = triple subject（列）**。200 表/5,000 列只作 Glyph 量级参照，不是本 fixture。

## 数据

| table | column | tag | level |
|---|---|---|---|
| t_users | col_email | Email | 3 |
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

## 期望结果

- **CQ1**：2 列（`col_email`、`col_customer_email`）/ 2 表。
- **CQ2**：4 表 / 7 列（users: email/phone；orders: amount/customer_email；hr: ssn/salary；sales: revenue）。
- **CQ3**：ds_orders 1、ds_hr 1、ds_sales 1、ds_legacy 1（按「无 level-bearing tag」）。
- **shape violations**：2（`tag_unknown` 缺 `sensitivityLevel`；`col_legacy` 的 `hasTag` 是字面量）；`violations` 只数 shape 违反。
- **版本**：`policy_version: 0.3.0`、`tag_version: 0.1.0`；`query_id: CQ1|CQ2|CQ3`。

## 说明

- 坏样本是故意留的：`tag_unknown` 与 `col_legacy` 只用于 shape 违反，不参与 CQ1/CQ2；**CQ3 会把 `col_legacy` 计入**（它的 `hasTag` 是字面量、没有 level，`FILTER NOT EXISTS` 判为未打标）——这是预期，不是数据错。
- 每条 `:columnOfTable` 都同时有 `:hasColumn` 反向三元组；不要依赖推理。
- 数据是合成的，不代表任何真实目录；规模参照见 `O-N28`。
