---
status: draft
updated: 2026-11-11
parent: README.md
---

# 数据与坏样本

> fixture：5 表 / 13 列 / 5 dataset。数据是合成的，不代表任何真实目录；200 表/5,000 列是本文假设的「中型目录」规模，**不是 Glyph**——Glyph 是 ~98,000 表 / ~3.4M 列（E-22），也不是本 fixture（`O-N28`）。

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

## 坏样本

- `tag_unknown` 与 `col_legacy` 是故意留的：只用于 shape 违反，不参与 CQ1/CQ2。
- **CQ3 会把 `col_legacy` 计入**：它的 `hasTag` 是字面量、没有 level，`FILTER NOT EXISTS` 判为未打标——这是预期，不是数据错。
- `tag_email_1` 是 `:WorkEmail`（`:Email` 子类），CQ1 的 `rdfs:subClassOf*` 因此真正被执行；前提是 TBox 与 ABox 同图。
- 每条 `:columnOfTable` 都同时有 `:hasColumn` 反向三元组；不要依赖 `owl:inverseOf` 推理。

## 相关页

- 文件清单与怎么跑：[README](./README.md)、[run.md](./run.md)。
- 这些数据怎么进 TBox：[A.3](../body/build.md)。
