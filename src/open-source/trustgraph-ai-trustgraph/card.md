---
status: seed
source_type: open-source
reading: 已读代码
provenance: 一手代码
updated: 2026-11-09
repo: trustgraph-ai/trustgraph
url: https://github.com/trustgraph-ai/trustgraph
commit: 184f6228e9ebfa0e54f87e0e66f190549dfbd162
release:
license: Apache-2.0
scan_date: 2026-11-09
stars_at_scan: 2902
last_push: 2026-11-08
ontology_role: core
seam: read-path
execution_form: engine
evidence_role: mechanism-only
home: topics/01-constraint
subtopic:
also_supports: []
updates: []
admission: admitted
gate_checked: 2026-11-11
impact_evidence: "I2+I3: 30 contributors, 1603 commits, 2902 stars"
liveness: last_push 2026-11-08
provenance_type: company
---

# trustgraph-ai/trustgraph · 来源卡

> 来源卡：只记可定位的事实。调用链与「执行还是装饰」的定级在同目录 `digest.md`。

## 一句话

AI governance platform for agents；本体有两个用途——抽取阶段的类/属性 schema，以及查询结果返回前的 SHACL-AF 策略过滤。

## 本体在哪

| 项 | 内容 |
|---|---|
| 文件 / 目录 | 词表规格 `specs/ontology/trustgraph.ttl`（OWL 2，`owl:versionInfo "2.3"`，覆盖 provenance / extraction metadata / explainability）；抽取用的本体由配置服务下发 |
| 格式 | OWL/Turtle（规格）；运行时是 OWL-like 的类/属性结构（`OntologyClass` / `OntologyProperty`）；策略是 SHACL-AF NodeShape（`sh:SPARQLTarget` + `sh:SPARQLRule`） |
| 谁生成、谁加载 | `extract/kg/ontology/ontology_loader.py` 从配置服务读；`ontology_selector.py` 选类；`triple_converter.py` 转三元组 |
| 是否版本化 / 可回滚 | TTL 有 `owl:versionInfo`；策略图 `urn:graph:policy` 由服务加载，回滚机制未定位 |

## 调用点

- 抽取入口：`trustgraph-flow/trustgraph/extract/kg/ontology/extract.py`（`OntologyLoader`）
- 本体选择 / 嵌入 / 归一化：同目录 `ontology_selector.py`、`ontology_embedder.py`、`entity_normalizer.py`
- 查询解释：`trustgraph-flow/trustgraph/query/ontology/query_explanation.py`
- 策略过滤（运行时）：`trustgraph-flow/trustgraph/policy/policy_filter.py`（`PolicyFilter`，SHACL-AF 求值：Hydrate → SPARQLTarget → Rule → ValidationResult → 移除 `blocks=true` 的节点）；服务装配在 `policy/triples/service.py`
- 输入 / 输出：三元组 + UserContext → 只返回允许看见的三元组
- 失败时降级：未定位（策略缺失 / 求值异常的行为待读）

## 证据入口

- tests：`tests/unit/test_extract/test_ontology/*.py`（加载、选择、URI 展开、三元组转换、抽取）；`tests/unit/test_policy/test_policy_filter.py`
- benchmark：未定位
- issue / 生产案例：README 与 docs 声称 agent governance；真实部署未核
- 最小复现：`pytest tests/unit/test_extract/test_ontology tests/unit/test_policy`（Python 环境待建）

## 与哪篇 digest 对照

| 论文 digest | 机制 | 这里对应 / 缺失 |
|---|---|---|
| [Commit Boundary](../../../meta/audits/2026-11-11-source-purge.md#src-2610-37407) | 授权判据：可推理 ≠ 可授权 | 读路径的可见性判定；写路径的 commit gate 未定位（待核） |
| [POLAR](../../../meta/audits/2026-11-11-source-purge.md#src-2610-08082) | 动作执行前按本体剪枝 | 形态不同：这里过滤查询结果，不是剪动作 |

## 局限

- **没有用 pyshacl**：SHACL-AF 是自研求值器（`policy_filter.py`），别用「grep pyshacl」判断它有没有执行。
- 策略是**读路径**（返回结果过滤），不是写路径的 commit gate；也不能直接当「动作前拦截」证据。
- **不属于六时刻**：位置在「查询结果返回前」，最接近 checker 但对象是检索结果，不是模型产出；见 digest §4 与 `topics/01-constraint/frontier.md`。
- 本体从配置服务加载，不是直接解析 `specs/ontology/trustgraph.ttl`。
- 只读到入口与 docstring，调用链未通读；「是否真在 LLM 提议的动作上生效」未核。

## 待办

- [x] pin commit（184f622…）
- [x] 定位本体加载与调用点
- [ ] 跑 `tests/unit/test_extract/test_ontology` 与 `test_policy`
- [ ] 写 `code-map.md`
- [ ] 写 `digest.md`，回链 `topics/01-constraint`
