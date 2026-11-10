---
status: draft
updated: 2026-11-10
quality: C
based_on: card.md
commit: 48a808df81be1c3abd044c3d1579a57b40032302
claims: []
---

# OpenLineage/OpenLineage：lineage 事件，不是本体

> **自包含**：不假设读者读过 README、card 或论文。代码位置写到 `文件:符号`，不贴大段代码。
> **证据等级**：`已核` = 读过代码/规范并指到文件/字段；`已证` = 仓库外复现；`推测` = 只读 README/文档；`存疑` = 冲突/闭源。
> 本 digest 只读了 `spec/facets/TestRunFacet.json` 与 facet 目录；`spec/OpenLineage.json` 抓取失败，标 `待核`。

## 0. 三句话

1. **它是什么**：开放 lineage 元数据标准；作业运行时发 `RunEvent`（run/job/dataset + facets），后端（如 Marquez）收集成 lineage 图。
2. **本体怎么被用**：**没有本体**。facet 是 JSON Schema 字段；`SchemaDatasetFacet`/`TagsDatasetFacet` 是元数据，不是 OWL/SHACL 类。
3. **证据到哪**：`已核`（规范 JSON；TestRunFacet 的 `status`/`severity`）；未跑事件、未接 04；quality C。

## 1. 项目与维护状态

- **定位**：LF AI & Data 下的开放 lineage 标准；Apache-2.0；`stars 2,755`、`forks 563`、`pushed_at 2026-11-09`（扫描 2026-11-10）。
- **生态**：Spark/Airflow/dbt 等集成端发事件；Marquez 是参考后端；不是 agent 运行时。
- **pin**：commit `48a808df81be1c3abd044c3d1579a57b40032302`（main，2026-11-09）。

## 2. 本体在哪

- **没有本体**；`spec/facets/*.json` 是 JSON Schema。
- 与 04 相关的是 **lineage/审计字段**：`SchemaDatasetFacet`（列/类型）、`TagsDatasetFacet`（标签）、`DataQualityAssertionsDatasetFacet`（断言结果）、`TestRunFacet`（测试状态）、`ParentRunFacet`（父 run）、`SymlinksDatasetFacet`（同实体多标识）。
- `ontology_role: adjunct`，`execution_form: none`；它不是「本体被执行」，是「事件被记录」。

## 3. 调用链

```
instrumented job（Spark/Airflow/dbt…）
  → emit RunEvent {run, job, inputs[], outputs[], facets{}}
  → collector/backend（Marquez 等）
  → lineage graph / API / UI
```

**规范锚**：

- `spec/facets/TestRunFacet.json:TestExecution.status`：描述为 `pass`（no issues）/ `fail`（issues found）/ `skip`（not executed）；`severity`：`error`（blocks pipeline）/ `warn`（warning only，不阻断）。`required: ["name","status"]`。
- `spec/facets/SchemaDatasetFacet.json`：数据集 schema 字段（列名/类型）；**待核**。
- `spec/facets/DataQualityAssertionsDatasetFacet.json`：数据质量断言结果；**待核**。
- `spec/facets/ParentRunFacet.json`：父 run/job；**待核**。
- `spec/OpenLineage.json`：核心 `RunEvent` schema；**抓取失败，待核**。

## 4. 接缝判定

| 问题 | 回答 | 证据 |
|---|---|---|
| 有外部判据（判据来自本体，不是模型自评） | **否**：判据是测试/断言结果，不是本体 | `TestRunFacet` |
| 有阻断能力（违反可剪动作/拒输出/阻落盘） | **否**：`severity=error` 是**约定**，是否阻断由消费方/编排器决定；标准本身不阻断 | spec 描述 |
| 位置明确（能指到回路某一时刻） | **旁路**（观测/审计），不是六时刻 | `seam: none` |
| 对应六时刻或轴外位置 | `none`（outside；审计/观测） | 本页 |
| 执行形态 | `none`（不执行本体） | 无 OWL/SHACL |

**判定**：OpenLineage 是 **审计/lineage 的字段标准**，不是 gate、不是 checker；04 只借它的字段（run_id、parent run、dataset version、test status）来补审计最小单元。

## 5. 证据与最小复现

- **读到的规范**：`TestRunFacet.json`（base64 解码后逐字段读）；facet 目录列表。
- **未跑**：没有发事件、没有起 Marquez、没有接 04 fixture。
- **能支撑**：lineage 事件有 `run/job/dataset/facets`；`TestRunFacet.status` 是 `pass/fail/skip` 三值；`severity` 分 `error/warn`。
- **不能支撑**：不能证明事件完整、不能证明 `skip` 等于 undetermined、不能证明 `severity=error` 会真的阻断。

## 6. 不能证明什么

- **不是本体**：`SchemaDatasetFacet`/`TagsDatasetFacet` 是元数据，不是 OWL/SHACL；不能写「本体被执行」。
- **`skip` ≠ undetermined**：规范说 `skip` = not executed；「跑了但定不了」是另一种状态，04 的三态要自己另立。
- **`severity=error` ≠ 已阻断**：标准只描述「blocks pipeline」，是否执行由编排器/消费方决定。
- **事件齐全 ≠ lineage 正确**：发事件是 producer 的责任；缺失/错报不会自动被标准发现。
- **未跑**：本卡没有生产/测试数据。

## 7. 与论文 digest 对照

| digest | 机制 | 代码/规范里对应 | 缺什么 |
|---|---|---|---|
| [E-06](../../../topics/conclusions.md)（workflow 失败） | 五角色/七变量 | OpenLineage 记录 run/job/dataset 事件 | 失败归因、角色 |
| [E-27](../../../topics/conclusions.md)（输出/传播） | 跨段故障换形态 | `ParentRunFacet`/`SymlinksDatasetFacet` 可追跨段 | 本体语义、注入实验 |
| [04 C.4](../../../deliverables/04-ontology-in-production/body/govern.md) | 审计最小单元 | `run_id`/`parent run`/`dataset version`/`test status` | 与 04 audit schema 的字段映射未做 |

## 8. 工程含义

- **接口**：`RunEvent` + facets；消费方按 facet `_schemaURL` 解析。
- **数据**：需要 producer 集成；没有 producer 就没有 lineage。
- **成本**：事件体积/收集/存储；本卡未测。
- **什么时候别用**：需要阻断/授权时；需要本体语义时；没有 producer 时。
- **04 用法**：借 `run_id`、`parent run`、`dataset version`、`TestRunFacet.status` 四类字段；`skip` 要单独映射成 `undetermined` 的 `reason`，不能直接当 04 三态。

## 9. 代码地图

见同目录 [code-map.md](./code-map.md)。本页不重复索引。

## 10. 下一步

- 读 `spec/OpenLineage.json` 与 `spec/facets/ParentRunFacet.json`，确认 `RunEvent` 必填字段与 parent run 结构。
- 在仓库外发一条 `RunEvent`（不接 Marquez），看 `TestRunFacet.status/severity` 的校验行为。
- 回 [propagation](../../../topics/06-measure/metrics/propagation.md) 与 04 C.4，把 `run_id/parent/version` 映射进 audit schema。
