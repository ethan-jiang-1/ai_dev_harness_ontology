---
status: seed
source_type: open-source
reading: 已读代码
provenance: 一手代码
updated: 2026-11-09
repo: ontop/ontop
url: https://github.com/ontop/ontop
commit: 964dbb79431fb958fce9de0784424f7c0e35f9bf
release:
license: Apache-2.0
scan_date: 2026-11-09
stars_at_scan: 1016
last_push: 2026-11-04
ontology_role: core
seam: supply
execution_form: engine
evidence_role: mechanism-only
home: topics/03-knowledge
subtopic:
also_supports: []
updates: []
---

# ontop/ontop · 来源卡

> 来源卡：只记可定位的事实。调用链与定级在同目录 `digest.md`。

## 一句话

OBDA / 虚拟知识图引擎：用户给 OWL 2 QL 本体 + 关系库映射，Ontop 把 SPARQL 查询重写成 SQL 直接在库上执行。

## 本体在哪

| 项 | 内容 |
|---|---|
| 文件 / 目录 | **不自带本体**；本体与映射由用户提供。映射解析在 `mapping/sql/r2rml/src/main/java/it/unibz/inf/ontop/spec/mapping/parser/impl/R2RMLMappingParser.java`；`.obda` 例在测试资源 |
| 格式 | OWL 2 QL 本体；R2RML / OBDA 映射；SPARQL 查询 |
| 谁生成、谁加载 | 用户提供；`mapping/` 模块解析；`engine/` 做重写与执行 |
| 是否版本化 / 可回滚 | 本体版本由用户管；Ontop 自身按 release 发布 |

## 调用点

- 查询重写：`engine/reformulation/core/src/main/java/it/unibz/inf/ontop/answering/reformulation/impl/QuestQueryProcessor.java`
- 执行：`engine/system/core/src/main/java/it/unibz/inf/ontop/answering/connection/impl/QuestStatement.java`
- 映射解析：`mapping/sql/r2rml/.../R2RMLMappingParser.java`
- 输入 / 输出：SPARQL + 本体 + 映射 → SQL → 结果集
- 失败时降级：未定位（映射不完整/本体超出 QL 时的行为待读）

## 证据入口

- tests：`test/docker-tests/`（`QuestOWLExample_*`、`QuestVirtualParallelScenario` 等）
- benchmark：`test/docker-tests/.../benchmark/`
- issue / 生产案例：2013 年至今；Maven Central + Docker 发布；工业 OBDA 使用（未逐条核）
- 最小复现：Docker 镜像 `ontop/ontop` + 自带示例（待选一个）

## 与哪篇 digest 对照

| 论文 digest | 机制 | 这里对应 / 缺失 |
|---|---|---|
| [CAI](../../papers/2610.41172-context-as-infrastructure/digest.md) | 编译换 token / 预计算 | 形态不同：编译的是查询，不是上下文（只作边界对照） |

## 局限

- 只支持 **OWL 2 QL** profile；不是通用 DL 推理器。
- 执行的是查询重写，不是校验/授权；不能当「约束执行」证据。
- 没有 agent 集成；要当 LLM 工具需要自己包一层。
- 只到模块层，未通读重写调用链。

## 待办

- [x] pin commit（964dbb7…）
- [x] 定位重写与映射解析
- [ ] 跑一个 Docker 最小示例
- [ ] 写 `code-map.md`
- [ ] 写 `digest.md`，判断它在 supply 侧的边界
