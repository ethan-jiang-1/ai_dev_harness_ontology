---
status: draft
source_type: standard
standing: normative
reading: 摘要级
provenance: 原文摘要
updated: 2026-11-11
batch:
source: https://www.w3.org/TR/shacl/
author: W3C Data Shapes Working Group
published: 2017-07-20
influence: W3C Recommendation；SHACL Core 是 RDF 图约束的事实标准，pyshacl / TopBraid / Jena 等实现与 W3C data-shapes test suite 均以它为基线（实现清单与通过率 待核）
updates: []
admission: admitted
gate_checked: 2026-11-11
impact_evidence: "I1: W3C Recommendation; active implementations"
liveness: standard-in-force
provenance_type: standard-body
---

# W3C SHACL（Shapes Constraint Language）

> 标准卡，不是 digest。读的是 REC 目录、§2–§3 的公开摘要与 test suite 页面；**未逐字抓全文**，条款号按公开目录写，逐字核对标 `待核`。
> 重点只取 04 用得到的三件事：target、validation report、conformance；不展开 SHACL-SPARQL/Advanced Features。

## 它主张什么

1. **SHACL 用 shapes 描述 RDF 图应满足的约束**：一个 shape 由 target（对哪些节点生效）与 constraints（要满足什么）组成；Core 覆盖基数、数据类型、节点类型、类成员、值域、字符串/数值比较等。
2. **校验结果是 report，不是一个布尔**：`sh:conforms` 之外，report 里有 `sh:result`，每条带 `focusNode`、`resultPath`、`value`、`sourceShape`、`sourceConstraintComponent`、`resultSeverity`、`resultMessage`；这使「违反哪条、在哪个节点」可定位。
3. **没有 target 的 shape 不会自己产生 focus node**：它只能被其他 shape 引用（如 `sh:node`）；把它当「顶层检查」跑，可能得到 `conforms=true` 而实际没检查任何节点。这是 04 A.4/A.5 的 `targeted=0` 风险来源。

## 场景与 scope

- **管什么**：RDF 图的闭世界约束（cardinality、datatype、class、nodeKind、in、range 等）；可对实例图、shape 图、词汇表做校验。
- **不管什么**：
  - 不定义业务语义/授权策略；`sh:severity` 只是标签，不等于 allow/deny；
  - 不做 OWL 推理；子类/等价类是否生效取决于实现与 `inference` 设置；
  - SHACL-SPARQL 与 SHACL-AF 是扩展，不是 Core；不同实现覆盖不同（open-ontologies 的 verified 路径拒 `sh:sparql`，见 [E-20](../../../topics/conclusions.md)）。
- **test suite**：W3C data-shapes test suite 用 manifest 组织用例；partial 只比 `sh:conforms`，full 要求 report 图同构。通过率依实现与报告日期，`待核`。

## 证据强度

- **一手还是转述**：标准目录/摘要与 test suite 页面；全文未逐字核，`provenance: 原文摘要`。
- **有数据吗**：无实验数据；test suite 的通过数是实现方报告，不是本仓库测量。
- **等级**：
  - 「shape = target + constraints」「report 字段」「无 target 不产生 focus」——`已核（摘要/目录）`；
  - 条款号与逐字定义——`待核`；
  - 「pyshacl/TopBraid 通过率」——`待核`（报告日期旧、未复跑）。
- **不能当**：不能当「校验通过 = 数据可用」；不能当「有 shape 就有覆盖」；不能当「severity = 策略」。

## 与已有判断的关系

| 结论/判断 | 关系 | 说明 |
|---|---|---|
| [consumability](../../../topics/05-produce/representation/consumability.md) F1/A5 | 支持（validate 关） | `violations` 只数 shape 违反；`targeted=0` 时必须 `undetermined`，不是 pass |
| [output-validation](../../../topics/02-judgment/checker/output-validation.md) | 支持（三态/no_target） | report 给 focus/path/sourceShape；`conforms=true` 但在答案图上 target 无实例 → 空转 |
| [E-20](../../../topics/conclusions.md) | 边界 | SHACL 是「执行形态」之一；执行 ≠ 健全、≠ 授权 |
| 04 A.4/A.5 | 一致 | 2 条 shape：TagHasLevel、HasTagClass；`violations=2` 是已声明坏样本，不是覆盖率 |

**不升 E**：标准只证明 SHACL 能表达/报告约束，不证明你的 shapes 覆盖你的域，也不证明误报率。

## 待核项

- [ ] 逐字条款号（§2 targets、§3.5 conformance、§3.6.2 report）
- [ ] 无 target 的 shape 在 pyshacl/TopBraid 下的实际行为（是否报错/静默）
- [ ] `inference=none` 时 `sh:targetClass` 是否含子类；fixture 无 `rdfs:subClassOf`，需另测
- [ ] W3C test suite 的报告日期与实现通过率
- [ ] SHACL-AF 与 Core 的边界（本卡只把 AF 当扩展，不展开）

## 喂到哪个主题

- `topics/05-produce/representation/consumability.md`
- `topics/02-judgment/checker/output-validation.md`

## 原文摘录

> 未逐字摘录；引用时以 `https://www.w3.org/TR/shacl/` 的 §2/§3 为准，条款号 `待核`。
