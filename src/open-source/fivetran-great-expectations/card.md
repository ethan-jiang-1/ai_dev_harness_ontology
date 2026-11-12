---
status: draft
source_type: open-source
reading: 已读代码
provenance: 一手代码
updated: 2026-11-10
repo: fivetran/great_expectations
url: https://github.com/fivetran/great_expectations
commit: 5267a3dd2a36c61eaab76453280f748faa36fe73
release:
license: Apache-2.0
scan_date: 2026-11-10
stars_at_scan: 11922
last_push: 2026-11-09
ontology_role: adjunct
seam: checker
execution_form: none
evidence_role: mechanism-only
home: topics/02-judgment
subtopic: checker
also_supports: []
updates:
  - topics/02-judgment/checker/output-validation.md
  - deliverables/04-worked-example/body/govern.md
admission: admitted
gate_checked: 2026-11-11
impact_evidence: "I3: production adoption"
liveness: last_push 2026-11-09
provenance_type: company
---

# fivetran/great_expectations · 来源卡

> **这是来源卡，不是消化正文。** 只记能定位到文件/链接的事实：它是什么、本体在哪、从哪调、证据入口在哪。
> 调用链、执行/装饰的定级、与论文机制的对照，都在同目录 `digest.md`；文件索引在 `code-map.md`。

## 一句话

Python 数据质量框架：用 Expectation Suite 对表/列做断言，Validator 跑出 `success` 与 `observed_value`；不是本体/OWL/SHACL 校验器。

## 本体在哪

| 项 | 内容 |
|---|---|
| 文件 / 目录 | 无本体文件；Expectation 是 Python 类 / JSON 配置 |
| 格式 | Python expectation + JSON suite；不是 OWL/SHACL/RDF |
| 谁生成、谁加载 | 数据团队写 suite；Validator/Checkpoint 加载并执行 |
| 是否版本化 / 可回滚 | suite 可版本化；本卡未核版本机制 |

## 调用点

- 入口（文件:符号）：`great_expectations/expectations/core/expect_table_row_count_to_be_between.py:ExpectTableRowCountToBeBetween`（`BatchExpectation` 子类）
- 本体在哪一步被读入：**没有本体**；只读 expectation 参数与 batch metrics（`table.row_count`）
- 输入 / 输出：输入 batch + suite；输出 `ExpectationSuiteValidationResult`（`success` / `result.observed_value` / `exception_info`）
- 失败时降级（拒绝 / 重试 / 忽略）：只返回 `success=false`；不阻断、不拒绝写入；`catch_exceptions` 把异常收进结果，**不是 gate**

> 只写「代码里发生了什么」；「算不算接缝、是执行还是装饰」的定级放 `digest.md`。
