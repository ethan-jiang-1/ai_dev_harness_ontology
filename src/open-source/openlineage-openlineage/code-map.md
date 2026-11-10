---
status: draft
updated: 2026-11-10
repo: OpenLineage/OpenLineage
commit: 48a808df81be1c3abd044c3d1579a57b40032302
---

# OpenLineage/OpenLineage · 代码地图

> 只做定位：文件 / 符号 / 谁调用谁。**不贴代码、不写判断**；判断在 `digest.md`。
> 不写行号（commit 一动就漂），写 `路径:符号`。

## 入口

| 入口 | 形态 | 说明 |
|---|---|---|
| `spec/OpenLineage.json` | JSON Schema | 核心 `RunEvent`（**未取到，待核**） |
| `spec/facets/*.json` | JSON Schema | run/job/dataset facets |
| 集成端（Spark/Airflow/dbt） | library/integration | 发 `RunEvent` |
| Marquez | server | 参考后端（另一个 repo） |

## 本体相关文件

> **没有本体**。下表是 04 审计/传播用得到的 facet。

| 文件 | 符号/字段 | 作用 | 被谁调用 |
|---|---|---|---|
| `spec/facets/TestRunFacet.json` | `TestExecution.status`（pass/fail/skip）、`severity`（error/warn） | 测试结果与严重度 | producer 写、后端读 |
| `spec/facets/SchemaDatasetFacet.json` | schema/fields | 数据集列/类型 | **待核** |
| `spec/facets/DataQualityAssertionsDatasetFacet.json` | assertions | 数据质量断言结果 | **待核** |
| `spec/facets/ParentRunFacet.json` | parent run/job | 父 run（跨段） | **待核** |
| `spec/facets/SymlinksDatasetFacet.json` | identifiers | 同实体多标识 | **待核** |

## 调用链

```
job → emit RunEvent {run, job, inputs, outputs, facets}
  → collector/backend → lineage graph/API
```

## 测试与示例

| 路径 | 覆盖什么 | 怎么跑 |
|---|---|---|
| `spec/facets/TestRunFacet.json` | `status`/`severity` 字段定义 | 读 schema；未跑 |
| `spec/OpenLineage.json` | 核心 `RunEvent` | **待核**（抓取失败） |

## 未定位

- `RunEvent` 必填字段与 `_schemaURL` 版本机制：**待核**。
- `severity=error` 是否由标准定义「必须阻断」：**待核**（描述是「blocks pipeline」，执行在消费方）。
- 与 04 audit schema 的字段映射：**未做**。
