---
status: draft
source_type: open-source
reading: 已读代码
provenance: 一手文档
updated: 2026-11-10
repo: OpenLineage/OpenLineage
url: https://github.com/OpenLineage/OpenLineage
commit: 48a808df81be1c3abd044c3d1579a57b40032302
release:
license: Apache-2.0
scan_date: 2026-11-10
stars_at_scan: 2755
last_push: 2026-11-09
ontology_role: adjunct
seam: none
execution_form: none
evidence_role: mechanism-only
home: topics/06-measure
subtopic: metrics
also_supports: []
updates:
  - topics/06-measure/metrics/propagation.md
  - deliverables/04-worked-example/body/govern.md
admission: admitted
gate_checked: 2026-11-11
impact_evidence: "I1+I3: LF AI & Data, production adoption"
liveness: last_push 2026-11-09
provenance_type: foundation
---

# OpenLineage/OpenLineage · 来源卡

> **这是来源卡，不是消化正文。** 只记能定位到文件/链接的事实：它是什么、本体在哪、从哪调、证据入口在哪。
> 调用链、执行/装饰的定级、与论文机制的对照，都在同目录 `digest.md`；文件索引在 `code-map.md`。

## 一句话

开放 lineage 元数据标准：作业运行时发 `RunEvent`（run/job/dataset + facets），后端收集成 lineage 图；不是本体、不是 gate。

## 本体在哪

| 项 | 内容 |
|---|---|
| 文件 / 目录 | `spec/facets/*.json`（JSON Schema）；核心 `spec/OpenLineage.json` |
| 格式 | JSON Schema facets；不是 OWL/SHACL/RDF |
| 谁生成、谁加载 | 集成端（Spark/Airflow/dbt…）发事件；Marquez 等后端收集 |
| 是否版本化 / 可回滚 | facet 有 `_schemaURL`/版本；本卡未核版本机制 |

## 调用点

- 入口（文件:符号）：`spec/facets/TestRunFacet.json:TestExecution.status`（`pass`/`fail`/`skip`）；`severity`（`error` 阻断 / `warn` 只警告，按 spec 描述）
- 本体在哪一步被读入：**没有本体**；facet 是 JSON 字段，不是本体类
- 输入 / 输出：输入 job run 元数据；输出 `RunEvent`（run/job/datasets/facets）
- 失败时降级（拒绝 / 重试 / 忽略）：发事件失败通常不阻断作业；没有授权/门禁

> 只写「代码里发生了什么」；「算不算接缝、是执行还是装饰」的定级放 `digest.md`。
