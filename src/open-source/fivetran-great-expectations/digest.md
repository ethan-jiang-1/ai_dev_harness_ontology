---
status: draft
updated: 2026-11-10
quality: C
based_on: card.md
commit: 5267a3dd2a36c61eaab76453280f748faa36fe73
claims: []
---

# fivetran/great_expectations：数据质量断言，不是本体 checker

> **自包含**：不假设读者读过 README、card 或论文。代码位置写到 `文件:符号`，不贴大段代码。
> **证据等级**：`已核` = 读过代码并指到文件/函数；`已证` = 仓库外复现；`推测` = 只读 README/文档；`存疑` = 冲突/闭源。
> 本 digest 只读了 `expect_table_row_count_to_be_between.py` 一个核心文件；其他路径标 `待核`。

## 0. 三句话

1. **它是什么**：Python 数据质量框架，用 Expectation Suite 对表/列做断言，Validator/Checkpoint 跑出 `success` 与 `observed_value`。
2. **本体怎么被用**：**没有本体**。它不读 OWL/SHACL/RDF；Expectation 参数就是判据，`table.row_count` 等 metric 是输入。
3. **证据到哪**：`已核`（代码；一个 core expectation）；未跑测试、未接 04 fixture；quality C。

## 1. 项目与维护状态

- **定位**：Fivetran 旗下的开源数据质量框架（原 great-expectations 组织迁到 `fivetran`）；Apache-2.0。
- **活跃度**：`pushed_at 2026-11-09`，`stars 11,922`，`forks 1,882`（扫描 2026-11-10）；不是本体项目，是数据质量/测试工具。
- **谁在用**：数据工程/分析团队；不是 agent 运行时。star 只作影响力，不作质量证明。
- **pin**：commit `5267a3dd2a36c61eaab76453280f748faa36fe73`（develop，2026-11-09）。

## 2. 本体在哪

- **没有本体文件**；没有 OWL/SHACL/RDF 导入。
- Expectation 是 Python 类（`BatchExpectation`/`ColumnExpectation` 等）或 JSON 配置；suite 是 expectation 的集合。
- 与 04 的关系是**输出校验工具**，不是「本体被执行」：`ontology_role: adjunct`，`execution_form: none`。

## 3. 调用链

```
ExpectationSuite（JSON/Python）
  → Validator / Checkpoint
  → ExecutionEngine（pandas/spark/sql…）
  → metric（如 table.row_count）
  → Expectation._validate(...)
  → ExpectationSuiteValidationResult {
       success: bool,
       result: {observed_value, ...},
       exception_info: {raised_exception, ...}
     }
```

**代码锚**：

- `great_expectations/expectations/core/expect_table_row_count_to_be_between.py:ExpectTableRowCountToBeBetween`：`BatchExpectation` 子类；`metric_dependencies = ("table.row_count",)`；`success_keys = ("min_value","max_value","strict_min","strict_max")`；`_validate` 调 `_validate_metric_value_between`。
- 同文件：`row_condition` / `condition_parser` 是 `domain_keys`；`row_condition` 会把 batch 缩到子集（**分母变化**）。
- 同文件文档串：`result_format` 可取 `BOOLEAN_ONLY/BASIC/COMPLETE/SUMMARY`；`catch_exceptions` 把异常收进 `exception_info`；`severity` 是标签。
- `expectations/expectation.py:BatchExpectation`、`validator/validator.py:Validator.validate`、`core/expectation_suite.py:ExpectationSuite`：**未读，待核**。

## 4. 接缝判定

| 问题 | 回答 | 证据 |
|---|---|---|
| 有外部判据（判据来自本体，不是模型自评） | **否**：判据来自 expectation 参数（min/max/值集） | `ExpectTableRowCountToBeBetween` 参数 |
| 有阻断能力（违反可剪动作/拒输出/阻落盘） | **否**：只返回 `success=false`；不阻断 | 同文件文档串；无 gate 调用点 |
| 位置明确（能指到回路某一时刻） | **是**：输出后/落盘前校验 | `seam: checker` |
| 对应六时刻或轴外位置 | `checker`（输出后判定） | 本页 |
| 执行形态 | `none`（不执行 OWL/SHACL；执行的是数据断言） | 无本体 |

**判定**：GE 是 **checker 时刻的工具**，不是「本体闸门」。它可以做 04 的输出校验（schema/cardinality），但不能替代本体判据或策略执行。

## 5. 证据与最小复现

- **读到的代码**：`expect_table_row_count_to_be_between.py`（commit 上）；确认 `BatchExpectation`、`table.row_count`、`success_keys`、`row_condition`、`catch_exceptions`、`result_format`、`success/observed_value`。
- **未跑**：没有安装 GE、没有跑 fixture；没有测 `row_condition`/`mostly`/`catch_exceptions` 的实际行为。
- **能支撑**：GE 的断言模型是「expectation → metric → success 布尔」；它可以表达表行数/列非空/值集等输出校验。
- **不能支撑**：不能证明 GE 能替代 SHACL/本体检查；不能证明 `success=false` 会阻断任何动作；不能证明生产误报率。

## 6. 不能证明什么

- **不是本体校验**：没有 OWL/SHACL；`ontology_role: adjunct`，不能写成「本体被执行」。
- **`success` 是布尔，不是三态**：没有 `undetermined`；`row_condition`/`mostly` 会静默缩小分母；`catch_exceptions=True` 时异常进 `exception_info`，`success` 可能仍为 true（待核）。
- **不阻断**：返回结果，不拒绝写入/不剪动作；gate 要另写。
- **不是 04 的 fixture 验证**：本卡没跑；`success` 语义与 04 的 `pass/violation/undetermined` 不同，需要外层适配。

## 7. 与论文 digest 对照

| digest | 机制 | 代码里对应 | 缺什么 |
|---|---|---|---|
| [E-02](../../../topics/conclusions.md)（Ontology Catch；**已撤回，历史**） | 本体当 checker，报 catch/FA | GE 是数据断言，不是本体检查 | 本体判据、catch/FA |
| [E-27](../../../topics/conclusions.md)（输出校验/传播） | 六类 + 三态 | GE 可覆盖 schema/cardinality；无三态 | cross-field/语义、undetermined |
| [output-validation](../../../topics/02-judgment/checker/output-validation.md) | 6 类 + 三态 | GE 的 expectation 可映射前两类 | 需外层包装三态与 coverage |

## 8. 工程含义

- **接口**：`ExpectationSuite` + `Validator`；结果取 `success`、`result.observed_value`、`exception_info`。
- **数据**：需要 batch/表；04 的 fixture 是 RDF，GE 不直接读 Turtle；要先把结果转成表/JSON。
- **成本**：每条 expectation 一次 metric 计算；全表扫描成本随数据源；本卡未测。
- **什么时候别用**：需要本体语义/OWL 推理/SHACL 约束时；需要阻断时；需要三态 coverage 时。
- **04 用法**：只借「expectation → 结果」的形状，映射到 T5 的 schema/cardinality；不把 GE 当本体 checker。

## 9. 代码地图

见同目录 [code-map.md](./code-map.md)。本页不重复索引。

## 10. 下一步

- 读 `validator/validator.py:Validator.validate` 与 `expectations/expectation.py:BatchExpectation`，确认 `success` 与 `exception_info` 的合并逻辑。
- 在仓库外跑 3 条 expectation（row_count / not_null / in_set），记录 `row_condition`/`mostly`/`catch_exceptions` 的实际分母。
- 回 [output-validation](../../../topics/02-judgment/checker/output-validation.md) 的 GE 映射表，把 `待核` 改成实测/代码锚。
