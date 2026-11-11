---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# 例子数据（fixture）：索引

> 5 表 / 13 列 / 5 dataset。**断言式三元组存储，无 entailment**；`:hasColumn` 与 `:columnOfTable` 两侧显式写入；`owl:inverseOf` 只是文档。**决策单位 = triple subject（列）**。
> `tag_email_1` 是 `:WorkEmail`（`:Email` 子类），CQ1 的 `rdfs:subClassOf*` 因此真正被执行；前提是 TBox 与 ABox 同图。200 表/5,000 列是本文假设的中型目录，不是 Glyph 参照（Glyph ~98k 表 / ~3.4M 列，E-22），也不是本 fixture。

## 怎么用

- 要跑命令、看期望输出：见 [run.md](./run.md)。
- 要看表/列/标签与坏样本：见 [data.md](./data.md)。
- 要对照产物：见 [A](../body/build.md)/[B](../body/consume.md)/[C](../body/govern.md)。

## 文件清单

| 文件 | 是什么 | 对应产物 |
|---|---|---|
| [ontology.ttl](./ontology.ttl) | TBox：11 类 / 5 属性 | ② Turtle |
| [catalog.ttl](./catalog.ttl) | ABox：5 表 / 13 列 / 标签 | ② Turtle |
| [shapes.ttl](./shapes.ttl) | 2 条 SHACL shape | ③ shapes |
| [policy.json](./policy.json) | 8 条策略规则 | ⑤ policy 表 |
| [policy_tests.json](./policy_tests.json) | 11 条输入 → 期望 decision | ⑥ 策略测试 |
| [leak_cases.json](./leak_cases.json) | 12 条泄漏用例 | ⑦ 泄漏用例 |
| [audit.schema.json](./audit.schema.json) | audit record JSON Schema | ⑧ audit schema |
| [audit_records.json](./audit_records.json) | 3 条 audit 记录（deny + skip/leak + allow） | ⑧ audit record |
| [fault_matrix.json](./fault_matrix.json) | 10 类故障 × 3 段；注入骨架，不是实测 | ⑨ 故障矩阵 |

> 支持页：[run.md](./run.md)（可选跑）· [data.md](./data.md)（数据/坏样本）。

## 文件怎么用（没有引擎）

- [policy_tests.json](./policy_tests.json)：11 条输入 → 期望 decision。用任意 JSON/脚本按 `policy.json` 的 8 条规则判；T9 故意留成 `undetermined`，不要强行给 allow/deny；T11 是 governance 的 dataset 级 allow。
- [leak_cases.json](./leak_cases.json)：12 条查询与期望；`expected_rows` 只对 filter/allow 用例有意义，deny/withhold 看 `expected_absent`；`trustgraph` 列是 pin `184f622` 的已知行为，不是实测。`object_direction_failed` 是预期缺口，不是用例写错。
- [audit.schema.json](./audit.schema.json)：用 `jsonschema` 校验 [audit_records.json](./audit_records.json) 的三条记录（对应 [C.4](../body/govern.md)）；`policy_version/tag_version/snapshot` 必须能回放。
- [fault_matrix.json](./fault_matrix.json)：10 类 × 3 段骨架；没有注入实验，不要当结果。

## 注意

- 坏样本是故意的：`tag_unknown` / `col_legacy` 只用于 shape 违反；**CQ3 会把 `col_legacy` 计入**（字面量 tag 判为未打标）。详见 [data.md](./data.md)。
- 需要 `ontology.ttl` 与 `catalog.ttl` 同图，CQ1 的 `subClassOf*` 与 shape 的 target 才成立；只加载 ABox 会少行。
