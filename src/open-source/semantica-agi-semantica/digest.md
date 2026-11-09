---
status: draft
updated: 2026-11-09
quality: B
based_on: card.md
commit: 39cf7216d2326b012436efebf8a227e82f37dd3b
claims: []
---

# semantica：本体先被编译成 SHACL，再由 pyshacl 执行——「执行」发生在约束派生之后

> **自包含**：不假设读者读过 README、card 或论文。代码位置写到 `文件:函数`，不贴大段代码。
> **证据等级**（四档）：
> - `已核`：读过代码，能指到文件/函数；或读过一手文档原文。
> - `已证`：不仅跑通，且能用 `EXP-xxx` 在本仓库外复现；**跑通单测不等于机制有效**。
> - `推测`：只读 README/文档/issue，没有代码定位。
> - `存疑`：README 与代码/issue 冲突，或核心闭源。
> `reading: 未读` 指还没通读代码；本页的证据来自调用链阅读 + 最小运行。

## 0. 三句话

1. **它是什么**：Semantica 是一个 Python 语义层框架（14.5k★），`semantica/ontology/` 负责从数据/文本生成本体、导出 OWL、派生 SHACL、校验数据图。
2. **本体怎么被用**：**先编译成 SHACL，再执行校验**。`OntologyEngine.to_shacl()` 从 ontology dict 生成 shapes，`validate_graph()` 调 pyshacl 校验；本体本身在校验时**不做 OWL 推理**（`inference="none"`）。
3. **证据到哪**：调用链已读、两条最小路径跑通（直接校验 + 本体→SHACL→校验）；没有下游任务/漏检误报数据（`已核` 代码，`推测` 效果）。

## 1. 项目与维护状态

- 仓库：`semantica-agi/semantica`，MIT，本次 pin `39cf7216d232`。
- 规模：14,475★，2025-06 建，2026-11-08 仍在推送；API 返回 100+ 贡献者（截断）。
- 结构：`semantica/ontology/`（生成/校验/质量门/版本）、`semantica/kg/`（图算法/社区摘要）、`semantica/change_management/`（版本管理）、`cli.py`（命令）。
- 风险信号：14 个月 1.4 万星、增速异常；贡献者数被 API 截断；少量提交来自 `claude` 账号（复核转述）。**star 只作影响力参考**。

## 2. 本体在哪

| 形态 | 位置 | 格式 | 谁生成/加载 | 用途 |
|---|---|---|---|---|
| 运行时模型 | `semantica/ontology/ontology_generator.py`、`engine.py` | Python dict（classes/properties） | `OntologyEngine.from_data/from_text` | 生成链路的工作表示 |
| OWL 导出 | `owl_generator.py: OWLGenerator.generate_owl()` | OWL/Turtle（rdflib） | `to_owl` / `export_owl` | 导出/交换 |
| SHACL 派生 | `engine.py: to_shacl()` → `ontology_generator.py: SHACLGenerator` | SHACL/Turtle | `to_shacl` | 校验数据图 |
| 词表 | `semantica/ontology/vocabulary/semantica-ns.ttl` | Turtle | 静态 | 框架自身命名空间 |

**关键**：仓库不带领域本体；本体由用户/生成器产生。SHACL 不是手写资产，而是从 ontology dict **派生**出来的。

## 3. 调用链

```
# 路径 A：已有 shapes，直接校验（CLI / 示例）
data.ttl + shapes.ttl
 → cli.py: `semantica validate shacl`
   → run_shacl_validation(data_str, shacl_str)
       import pyshacl（缺 → ImportError：pip install semantica[shacl]）
       rdflib 解析两图
       pyshacl.validate(inference="none", abort_on_first=False)
       → 遍历 sh:ValidationResult，抽 focus/path/severity/message/value/constraint/shape
       → 从 sh:sourceShape 回填 minCount / maxCount / datatype / class
       → SHACLValidationReport(conforms, violations, warnings, infos, raw_report)
       → explain_violations()：按约束类型生成英文解释

# 路径 B：本体 → shapes → 校验（framework 的核心增量）
ontology dict
 → OntologyEngine.to_shacl(ontology, target_namespace=..., quality_tier=...)
     → SHACLGenerator.generate() → serialize()
 → OntologyEngine.validate_graph(data, shacl=shacl_str)
     → _run_pyshacl(data, shacl) → 同上
```

实现细节（可核对）：

- `to_shacl` 的可选参数：`quality_tier`（basic/standard/strict）、`severity`、`include_inherited`、`target_namespace`、`attach_domainless_properties`、`validate_output`。
- `run_shacl_validation` 把 `sh:sourceShape` 回填成 `minCount/maxCount/datatype/class`，用于英文解释；代码注释明确 **`sh:qualifiedMinCount/qualifiedMaxCount` 未处理**，会退化成 `?`。
- `inference="none"`：校验前不做 OWL 演绎；`validate_graph` 没有暴露推理参数。
- 依赖：`pyshacl` 是可选 extra（`semantica[shacl]`）；导入 `semantica.ontology` 会拉 numpy/scipy/pydantic 等重依赖。

## 4. 接缝判定

| 条件 | 是否成立 | 证据 |
|---|---|---|
| 有外部判据（来自本体，不是模型自评） | **成立** | SHACL shapes 由本体派生；pyshacl 按 shapes 判定 |
| 有阻断能力（违反可改变走向） | **成立但由调用方决定** | `validate_graph` 返回 `conforms=False` 的报告；是否拒收/重试由调用方写 |
| 位置明确（能指到回路某一时刻） | **只在「离线/CLI 校验」** | 没有 agent 回路的调用点；CLI 与示例都是显式调用 |

**结论**：它是 **checker 组件**（输出后判定），不是 in-loop 执行。它提供的增量不是「在 agent 里跑」，而是「**shapes 从本体编译而来**」——把 checker 的约束作者成本从手写转移到了本体建模。

## 5. 证据与最小复现

**路径 A（直接校验）**

```python
from semantica.ontology.ontology_validator import run_shacl_validation
data = "@prefix ex: <http://example.org/> . ex:alice a ex:Person ."
shacl = """... ex:PersonShape ... sh:property [ sh:path ex:name ; sh:minCount 1 ] ..."""
r = run_shacl_validation(data, shacl)
# conforms: False, violations: 1
# explanation: Node <.../alice> is missing required property <.../name>. At least 1 value(s) are required.
```

**路径 B（本体 → SHACL → 校验）**

```python
engine = OntologyEngine()
shacl = engine.to_shacl(onto, target_namespace="http://example.org/ns#")  # 1,729 chars，54ms
r = engine.validate_graph(data, shacl=shacl)
# conforms: False, violations: 1 → ns:rex 缺 ns:owner (MinCountConstraintComponent)
```

- 环境：Python 3.13 + venv；`pyshacl`、`rdflib`、`numpy`、`scipy`、`pydantic`、`dateutil`。
- 失败记录：不装 pyshacl 时 `run_shacl_validation` 抛 `ImportError`（明确提示 `semantica[shacl]`）；`OntologyEngine()` 初始化打印 `openai library not installed`（LLM 路径可选）。
- **quality: B 的理由**：有最小运行、有代码定位、有派生链路；但没有基准/生产数据，生成形状的质量未测。

## 6. 不能证明什么

1. **不能证明生成的 shapes 正确**：只证明「能生成 + 能跑」，没有漏检/误报率；派生错误会静默变成「检查通过」。
2. **不能证明装进 agent 回路**：所有调用都是显式 CLI/库调用；没有输出后自动校验、没有拒绝/重试策略。
3. **不能证明本体被推理**：`inference="none"`；subClassOf/等价类不会在校验前展开（除非显式加推理）。
4. **不能证明生成的本体质量**：`from_data` / `from_text` 的产出没有独立评测；`quality_gate` 的门槛未核。
5. **不能证明 14.5k★ 代表采用**：star 增速异常；真实用户/生产部署未核。
6. **不能证明它替代手写 SHACL**：派生 shapes 与手写 shapes 的覆盖差异没有对照。
7. **不能证明 `explain_violations` 的解释正确**：文本模板是按约束类型拼的，`qualifiedMinCount` 等未覆盖。

## 7. 与论文 digest 对照

| digest | 论文机制 | 代码里对应 | 缺什么 / 差异 |
|---|---|---|---|
| [OntoDoc](../../../src/papers/2611.01276-ontodoc/digest.md) | 先写 assumptions 再生成描述；生成物只到说明 | 有 `from_data` / `from_text` 生成路径 + OWL 导出 | 生成质量未测；没有 assumptions 步骤 |
| [What Does an Ontology Catch](../../../src/papers/2610.37809-what-does-an-ontology-catch/digest.md) | 本体当 checker；漏检/误报是核心指标 | 有 checker 执行器（pyshacl）+ 派生 shapes | 没有 catch/FA 测量；没有真实错误分布 |
| [生成 subtopic 的判断](../../../topics/05-produce/generation/README.md) | 「四篇都没有交付下游能直接消费的本体；可消费性没测」 | **代码侧提供了消费路径**：ontology → SHACL → 校验 | 只证明管线能跑，不证明生成物可消费；不能反推论文 |

**一句话**：它把「本体 → 可执行约束」这段路修通了，但没有测「修出来的约束对不对」。

## 8. 工程含义

- **接口**：`to_shacl(ontology, quality_tier=..., target_namespace=...)` → shapes 字符串；`validate_graph(data, shacl=...)` → 结构化报告。
- **成本**：小本体派生 54ms；校验成本由 pyshacl + 图规模决定；依赖重（numpy/scipy/pydantic），不适合塞进轻量工具。
- **失败模式**：shapes 派生过度/不足都会静默；`inference=none` 让子类实例不匹配父类 shapes（除非数据里显式断言类型）；`qualifiedMinCount` 解释退化。
- **什么时候别用**：需要 OWL 推理、需要 in-loop 自动拒收、需要可审计的「为什么允许」时，这个组件不够。

## 9. 代码地图

见同目录 [`code-map.md`](./code-map.md)：入口、本体相关符号、两条调用链、运行记录、未定位项。

## 10. 下一步

- **G**：派生 shapes vs 手写 shapes 的 catch/FA 对照（可接 [checker G1](../../../topics/02-judgment/checker/frontier.md)）。
- 用 `examples/fibo-lei` 跑一次真实记录校验，看 shapes 覆盖与失败分布。
- 检查 `quality_gate` 是否度量生成质量；若没有，直接把「生成物质量未测」写进 05/generation 的 F。
- 回 topics：`05/generation` 加 F7（消费路径有实现、质量未测）；`02/checker` 加 G6（派生 vs 手写）。
