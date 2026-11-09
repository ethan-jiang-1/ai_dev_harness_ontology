---
status: seed
updated: 2026-11-09
repo: semantica-agi/semantica
commit: 39cf7216d2326b012436efebf8a227e82f37dd3b
---

# semantica-agi/semantica · 代码地图

> 只做定位：文件 / 符号 / 谁调用谁。不贴代码、不写判断；判断在 `digest.md`。
> 路径相对仓库根；commit `39cf721`。

## 入口

| 入口 | 形态 | 说明 |
|---|---|---|
| `semantica/cli.py`（`validate shacl`） | CLI | `semantica validate shacl data.ttl --shapes shapes.ttl` |
| `semantica/ontology/engine.py: OntologyEngine` | Python API | 生成、导出、SHACL 派生、图校验、版本比较 |
| `examples/fibo-lei/run.py` | 示例 | 用 SHACL 校验 FIBO 记录，含 `check_record()` |

## 本体相关文件

| 文件 | 符号 | 作用 | 被谁调用 |
|---|---|---|---|
| `semantica/ontology/engine.py` | `OntologyEngine.to_shacl()` | 从 ontology dict 派生 SHACL shapes | CLI / 示例 / 用户代码 |
| `semantica/ontology/engine.py` | `OntologyEngine.validate_graph()` | 校验数据图（shacl 或 ontology 二选一） | 用户代码 |
| `semantica/ontology/ontology_generator.py` | `SHACLGenerator.generate/serialize` | 实际生成 shapes（quality_tier/severity/继承） | `to_shacl` |
| `semantica/ontology/owl_generator.py` | `OWLGenerator.generate_owl()` | ontology dict → OWL（rdflib） | `to_owl` / `export_owl` |
| `semantica/ontology/ontology_validator.py` | `run_shacl_validation()` | pyshacl 包装：结构化报告 + 英文解释 | CLI、示例、`validate_graph` |
| `semantica/ontology/ontology_validator.py` | `_run_pyshacl()` | 兼容别名 | `validate_graph` |
| `semantica/ontology/ontology_validator.py` | `OntologyValidator` | 结构/一致性校验（可选 reasoner） | `quality_gate` |
| `semantica/ontology/quality_gate.py` | `OntologyQualityGate` | 质量门（结构 + 评测） | `OntologyEngine` |
| `semantica/change_management/ontology_version_manager.py` | `VersionManager` | 版本/比较 | `OntologyEngine` |

## 调用链

```
# 路径 A：直接校验（CLI / 示例）
data.ttl + shapes.ttl
  → cli.py: validate shacl
    → run_shacl_validation(data_str, shacl_str)
        import pyshacl（缺 → ImportError: pip install semantica[shacl]）
        rdflib 解析两张图
        pyshacl.validate(inference="none", abort_on_first=False)
        → 遍历 sh:ValidationResult，抽出 focus/path/severity/message/value/constraint/shape
        → 从 sourceShape 回填 minCount/maxCount/datatype/class
        → SHACLValidationReport（conforms / violations / warnings / infos）
        → explain_violations()：按约束类型生成英文解释
  → 输出 JSON（conforms / violation_count / violations）

# 路径 B：本体 → shapes → 校验
ontology dict
  → OntologyEngine.to_shacl()：SHACLGenerator.generate → serialize
  → OntologyEngine.validate_graph(data, shacl=shacl_str)
        → _run_pyshacl(data, shacl) → 同上
```

## 测试与示例

| 路径 | 覆盖什么 | 怎么跑 |
|---|---|---|
| `tests/ontology/test_ontology_advanced.py` | 报告结构、约束参数回填、公共 API、conforming graph | `pytest tests/ontology/test_ontology_advanced.py` |
| `tests/ontology/test_shacl_target_namespace.py` | target namespace / closed / ignoredProperties | 同上 |
| `examples/fibo-lei/run.py` | 真实 FIBO 记录 + shapes；`check_record()` | `python examples/fibo-lei/run.py`（需示例数据） |
| `semantica/cli.py` | `validate shacl` | `semantica validate shacl data.ttl --shapes shapes.ttl` |

## 运行记录（C2）

```bash
# 环境：/tmp/tgvenv（Python 3.13），pip install pyshacl numpy networkx scipy pydantic python-dateutil
PYTHONPATH=. python - <<'PY'
from semantica.ontology.ontology_validator import run_shacl_validation
data = "@prefix ex: <http://example.org/> . ex:alice a ex:Person ."
shacl = """... ex:PersonShape ... sh:property [ sh:path ex:name ; sh:minCount 1 ] ..."""
r = run_shacl_validation(data, shacl)
print(r.conforms, r.violation_count)   # False 1
PY
# → conforms: False, violations: 1；explain_human:
#   Node <.../alice> is missing required property <.../name>. At least 1 value(s) are required.

# 路径 B：最小 ontology dict
#   to_shacl(target_namespace="http://example.org/ns#") → 1,729 chars，54ms
#   validate_graph(data) → conforms False, 1 violation: ns:rex 缺 ns:owner (MinCount)
```

- 依赖链：导入 `semantica.ontology` 会拉 `engine → quality_gate → kg`，需要 numpy/scipy/pydantic/dateutil；不装 `pyshacl` 时 `run_shacl_validation` 抛 ImportError。
- `OntologyEngine()` 初始化时打印 `openai library not installed` 警告（LLM 生成是可选路径）。

## 未定位

- `inference="none"` 之外是否提供 OWL 推理选项（`validate_graph` 没有暴露该参数）。
- 生成 shapes 的质量门（`quality_gate`）是否度量漏检/误报。
- 24 releases / strict-xfail CI 的原始证据（复核转述，未逐条核）。
