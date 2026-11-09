---
status: seed
source_type: open-source
reading: 已读代码
provenance: 一手代码
updated: 2026-11-09
repo: semantica-agi/semantica
url: https://github.com/semantica-agi/semantica
commit: 39cf7216d2326b012436efebf8a227e82f37dd3b
release:
license: MIT
scan_date: 2026-11-09
stars_at_scan: 14475
last_push: 2026-11-08
ontology_role: core
seam: checker
execution_form: compiled
evidence_role: mechanism-only
home: topics/03-knowledge
subtopic:
also_supports: []
updates: []
---

# semantica-agi/semantica · 来源卡

> 来源卡：只记可定位的事实。调用链与定级在同目录 `digest.md`。

## 一句话

graph-native context / accountable AI 平台；本体模块负责生成 OWL、推断类、跑能力问题，并用 pyshacl 做 SHACL 校验。

## 本体在哪

| 项 | 内容 |
|---|---|
| 文件 / 目录 | `semantica/ontology/`：`owl_generator.py`、`class_inferrer.py`、`competency_questions.py`、`ontology_validator.py`、`module_manager.py`、`naming_conventions.py`；词表 `semantica/ontology/vocabulary/semantica-ns.ttl` |
| 格式 | OWL/Turtle（生成与导出）；SHACL 校验输入；Python 内部模型 |
| 谁生成、谁加载 | `owl_generator.py` / `llm_generator.py` 生成；`engine.py` 编排；`ontology_validator.py` 校验 |
| 是否版本化 / 可回滚 | 24 releases（复核转述，待核）；`ontology_provenance.py` 记录来源；回滚机制未定位 |

## 调用点

- 公共 API：`semantica/ontology/ontology_validator.py:148 run_shacl_validation()`，由 `semantica/ontology/__init__.py` 导出
- 生成：`owl_generator.py`、`class_inferrer.py`、`competency_questions.py`
- 编排：`engine.py`；LLM 生成：`llm_generator.py`
- 输入 / 输出：数据/文档 → OWL 本体 + SHACL 报告
- 失败时降级：`pyshacl` 是可选依赖（测试里 `import pyshacl` 失败会 skip），缺依赖时行为未核

## 证据入口

- tests：`tests/ontology/test_ontology_advanced.py`（`test_public_run_shacl_validation_api`、conforming graph 用例）
- benchmark：未定位
- issue / 生产案例：README 声称 accountable AI；真实部署未核
- 最小复现：`pip install pyshacl` + `pytest tests/ontology/test_ontology_advanced.py -k shacl`

## 与哪篇 digest 对照

| 论文 digest | 机制 | 这里对应 / 缺失 |
|---|---|---|
| [OntoDoc](../../papers/2611.01276-ontodoc/digest.md) | 本体生成/文档化 | 有 OWL 生成器与文档模块；生成质量未独立评测（待核） |
| [What Does an Ontology Catch](../../papers/2610.37809-what-does-an-ontology-catch/digest.md) | 本体作为判定器 | pyshacl 校验是「判定」，但没有漏检/误报的测量 |

## 局限

- 14 个月做到 14,475 星，增速异常；贡献者 100+（API 截断），commit 数不代表人力。
- `pyshacl` 是可选依赖：**不装 pyshacl 时，校验路径可能根本跑不到**。
- 本体生成质量（OWL 是否正确、能力问题是否真被回答）没有独立基准；README 与代码要分开看。
- 只到模块/测试层，未通读调用链。

## 待办

- [x] pin commit（39cf721…）
- [x] 定位本体生成与校验入口
- [ ] 跑 `run_shacl_validation` 最小示例
- [ ] 写 `code-map.md`
- [ ] 写 `digest.md`，回链 `topics/03-knowledge` 与 `02-judgment/checker`
