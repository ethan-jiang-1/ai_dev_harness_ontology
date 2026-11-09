---
status: seed
updated: 2026-11-09
repo: trustgraph-ai/trustgraph
commit: 184f6228e9ebfa0e54f87e0e66f190549dfbd162
---

# trustgraph-ai/trustgraph · 代码地图

> 只做定位：文件 / 符号 / 谁调用谁。不贴代码、不写判断；判断在 `digest.md`。
> 路径相对仓库根；commit `184f622`。

## 入口

| 入口 | 形态 | 说明 |
|---|---|---|
| `trustgraph-flow/trustgraph/policy/triples/service.py: Processor.on_message` | 流服务（FlowProcessor） | 策略过滤版的 triples-query；flow config 选择它而非 `triples-query` |
| `trustgraph-flow/trustgraph/extract/kg/ontology/extract.py` | 抽取管线 | 本体作为抽取 schema 的入口 |
| `trustgraph-cli/trustgraph/cli/load_knowledge.py:216` | CLI | `--graph` 可指向 `urn:graph:policy`，用于装策略 |

## 本体相关文件

| 文件 | 符号 | 作用 | 被谁调用 |
|---|---|---|---|
| `specs/ontology/trustgraph.ttl` | OWL 本体（`owl:versionInfo "2.3"`） | provenance / extraction metadata / explainability 词表 | 规格，不被运行时直接解析 |
| `trustgraph-flow/.../extract/kg/ontology/ontology_loader.py` | `OntologyLoader` / `OntologyClass` | 从配置服务读 OWL-like 类/属性 | `extract.py`、`ontology_selector.py` |
| `.../ontology/ontology_selector.py` | `OntologySelector` | 选相关类 | `extract.py` |
| `.../ontology/triple_converter.py` | `TripleConverter` | 抽取结果转三元组 | `extract.py` |
| `.../policy/policy_filter.py` | `PolicyFilter` | SHACL-AF 求值：加载策略、hydrate、SELECT target、CONSTRUCT rule、决定 block | `policy/triples/service.py` |
| `.../policy/policy_filter.py` | `PolicyEvaluation` | 单节点判定结果（determination/blocks/reason） | `PolicyFilter.apply` → `on_evaluation` |
| `.../policy/policy_filter.py` | `QueryCache` / `SparqlCache` / `NodeDeterminationCache` | 三层缓存（30s / 64 条 / 60s） | `PolicyFilter` |
| `trustgraph-base/trustgraph/schema/user_context.py` | `UserContext` | 用户上下文（roles/assignments/entitlements/override/delegation） | 请求字段；`_build_context_graph` |

## 调用链

```
TriplesQueryRequest（含 user_context）
  → service.on_message
    → _needs_policy：从 urn:graph:policy 数 NodeShape（缓存 60s）
        ├─ 有策略 + 无 user_context → 返回 policy-enforcement-error
        ├─ 无策略 → _passthrough（原样转发）
        └─ 有策略 + 有 context → _filtered_query
              → 后端 triples 流式返回，逐批 PolicyFilter.apply
                    → 候选 IRIs = 本批三元组的 subject/object
                    → _hydrate_node：按策略 SELECT 里可达谓词逐条取数（并发）
                    → _build_context_graph：UserContext → rdflib triples
                    → 每个候选节点按 sh:order 依次：
                         _run_sparql_target（SELECT ?this）
                         → 命中则 _run_sparql_rule（CONSTRUCT ValidationResult）
                         → 解析 sh:resultSeverity / sh:resultMessage / tg-pol:blocks
                         → 第一个命中策略生效（break）
                    → blocked 节点的 subject 三元组被剔除（_triple_blocked 只看 subject）
              → 过滤后批次回送；策略事件发布（PolicyEventPublisher）
```

## 测试与示例

| 路径 | 覆盖什么 | 怎么跑 |
|---|---|---|
| `tests/unit/test_policy/test_policy_filter.py` | 判定/缓存/并发/无策略直通 | 见下方运行记录 |
| `docs/tech-specs/policy-test-data/aerosentinel-policies.ttl` | 真实策略样例（信息屏障、范围过滤） | 装入 `urn:graph:policy` |
| `docs/tech-specs/policy-filtering.md` | 设计说明（enforcement mode、SHACL-AF 理由） | 阅读 |

## 运行记录（C2）

```bash
# 环境：python3.13 + venv；rdflib 7.6.0 / pytest / pytest-asyncio
# 仓库自带 pytest 会加载 tests/conftest.py，它 patch trustgraph.base（需 pulsar 等重依赖）
# 因此单独把测试模块拷出运行（不改仓库代码）：
cp tests/unit/test_policy/test_policy_filter.py /tmp/tgtest/
PYTHONPATH=/tmp/tgmerge /tmp/tgvenv/bin/python -m pytest /tmp/tgtest/test_policy_filter.py -q
# 结果：31 passed in 0.13s
```

- `trustgraph.schema` 在 `trustgraph-base/` 是不带 `__init__.py` 的命名空间包；与 `trustgraph-flow/trustgraph/__init__.py` 同路径冲突，需合并目录树（本次在 `/tmp/tgmerge` 合并，未改仓库）。
- 未跑：仓库完整 pytest（需 `trustgraph.base` + pulsar-client 等）。

## 未定位

- 默认容器/flow config 是否启用 `triples-policy`（grep 只找到 service 自身）。
- 策略装填的完整运维路径（`load_knowledge --graph` 之外有没有专用命令）。
- 策略事件（`PolicyEventPublisher`）落到哪个审计组件。
