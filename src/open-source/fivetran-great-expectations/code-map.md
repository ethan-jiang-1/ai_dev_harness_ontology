---
status: draft
updated: 2026-11-10
repo: fivetran/great_expectations
commit: 5267a3dd2a36c61eaab76453280f748faa36fe73
---

# fivetran/great_expectations · 代码地图

> 只做定位：文件 / 符号 / 谁调用谁。**不贴代码、不写判断**；判断在 `digest.md`。
> 不写行号（commit 一动就漂），写 `路径:符号`。

## 入口

| 入口 | 形态 | 说明 |
|---|---|---|
| `great_expectations` CLI / Python API | CLI + library | 本卡只读 Python 库路径 |
| `Validator` / `Checkpoint` | library | 跑 suite、出 validation result |

## 本体相关文件

> **没有本体**。下表是「输出校验」相关文件；不是 OWL/SHACL/RDF。

| 文件 | 符号 | 作用 | 被谁调用 |
|---|---|---|---|
| `great_expectations/expectations/core/expect_table_row_count_to_be_between.py` | `ExpectTableRowCountToBeBetween` | 表行数区间断言；`metric_dependencies=("table.row_count",)` | Validator / Checkpoint |
| 同文件 | `_validate` | 调 `_validate_metric_value_between` | Validator |
| 同文件 | `row_condition` / `condition_parser` | 把 batch 缩到子集 | 调用方传参 |
| `great_expectations/expectations/expectation.py` | `BatchExpectation` | expectation 基类 | 所有 batch expectation（**待核**） |
| `great_expectations/validator/validator.py` | `Validator.validate` | 跑 suite、合并结果 | Checkpoint/用户（**待核**） |
| `great_expectations/core/expectation_suite.py` | `ExpectationSuite` | suite 容器 | Validator（**待核**） |

## 调用链

```
ExpectationSuite → Validator/Checkpoint → ExecutionEngine
  → metric（table.row_count）→ Expectation._validate
  → ExpectationSuiteValidationResult {success, result, exception_info}
```

## 测试与示例

| 路径 | 覆盖什么 | 怎么跑 |
|---|---|---|
| 同文件 docstring | passing/failing 例（`observed_value: 3`, `success: true/false`） | 未跑 |
| `tests/` | 项目自测（未定位具体文件） | **待核** |

## 未定位

- `Validator.validate` 的 `success` 合并与 `catch_exceptions` 交互：**待核**。
- `mostly` / `row_condition` 对分母的影响：**待核**。
- 与 RDF/Turtle 的连接：**不存在**；04 fixture 需先转表/JSON。
