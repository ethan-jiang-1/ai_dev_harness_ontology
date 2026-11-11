---
status: draft
source_type: standard
standing: normative
reading: 摘要级
provenance: 原文摘要
updated: 2026-11-11
batch:
source: https://www.w3.org/TR/owl2-profiles/
author: W3C OWL Working Group
published: 2012-12-11
influence: W3C Recommendation；OWL 2 RL 的 eq-rep-s/p/o 是「sameAs 必须替换」的可实现规则表；GraphDB / Virtuoso / RDF4J 的实现差异见下（文档级，待核）
updates: []
admission: admitted
gate_checked: 2026-11-11
impact_evidence: "I1: W3C Recommendation; active implementations"
liveness: standard-in-force
provenance_type: standard-body
---

# W3C OWL 2 Profiles：sameAs 的替换规则

> 标准卡，不是 digest。读的是 Profiles §4.3 与 Direct Semantics 的相关段（经 2026-11-11 检索摘要）；**未逐字通读全文**，条款号 `待核`。
> 只取读路径用得到的一件事：**已断言的 sameAs 是否强制替换、未断言时能不能推定同一。**

## 它主张什么

1. **sameAs 是等价关系**：自反、对称、传递；在 OWL 2 RL 下，`eq-rep-s/p/o` 要求在主语/谓语/宾语三个位置做替换并做对称+传递闭包。只匹配到一个别名的查询，在 RL 语义下是**不完整**的。
2. **SameIndividual 是语义承诺**：Direct Semantics 要求所有被命名个体指称同一个域元素；身份不是标签/字符串相似度。
3. **未断言时不得推定同一**：RDF 1.1 Semantics §2 明确不规范「IRI 在现实中如何被赋予指称」；因此不能从相似性推出身份。

## 场景与 scope

- **条件性**：上述替换只在声明 OWL 2 RL / DL 蕴含时成立；SPARQL 默认 simple entailment 下 sameAs 完全不生效。
- **不管什么**：不规定访问控制、不规定「解析必须先于过滤」、不规定 canonical ID 怎么选。
- **工程证据（非规范）**：GraphDB 关闭 `FROM onto:disable-sameAs` 后只返回等价类代表；Virtuoso 的 sameAs 只在查询指定 inference context 时生效；RDF4J 默认不用 reasoner——三处都说明「不解析就漏」是真实工程行为，但**不是规范强制**。

## 证据强度

- **一手还是转述**：W3C REC 摘要/相关段；GraphDB/Virtuoso/RDF4J 为厂商文档（转述，待核）。
- **有数据吗**：无实验；工程行为是文档描述，不是本仓库测量。
- **等级**：`eq-rep`/`SameIndividual`/RDF 1.1 §2 的规范主张 `已核（摘要）`；「必须先于过滤」`推测（工程推论）`；「canonical ID 选谁」`推测`。

## 与已有判断的关系

| 结论/判断 | 关系 | 说明 |
|---|---|---|
| read-path 的 alias 规则 | **支持（条件性）** | 已断言 sameAs → 必须展开；未断言 → 不得推定同一；**「先于过滤」没有规范依据**，只能写成工程要求 |
| R07「读路径 ≠ 写授权」 | 支持（边界） | 别名解析保匹配完整性，不等于授权；合并身份可能扩权，需单独授权 |
| 02 R8 / 03 claim 走查 | 支持 | 把「解析」与「授权」解耦：解析按 alias 逐个判，合并单独判 |

## 待核项

- [ ] `eq-rep-s/p/o` 的具体条款号
- [ ] OWL 2 Direct Semantics 的 `SameIndividual` 原文页
- [ ] GraphDB / Virtuoso / RDF4J 文档的版本与日期
- [ ] Kirrane 等 2017 综述中「sameAs 传播」原句（转述 Qin & Atluri，二手）

## 喂到哪个主题

- `topics/01-constraint/commit-gate/read-path.md` §9（alias 前置）
- `deliverables/03-mechanism-reference/sections/claim-walkthrough.md`
- `deliverables/02-engineering-playbook/recipes/constraint.md` R8

## 原文摘录

> "it defines the equality relation owl:sameAs as being reflexive, symmetric, and transitive, and it axiomatizes the standard replacement properties of equality"（OWL 2 Profiles §4.3 摘要）

> "SameIndividual( a1 ... an ) | (aj)I = (ak)I for each 1 ≤ j ≤ n and each 1 ≤ k ≤ n"（OWL 2 Direct Semantics §2.3.6）

> "It is not normative for many aspects of RDF meaning ... including social issues of how IRIs are assigned meanings in use"（RDF 1.1 Semantics §2）

## 对照来源（未单独入档）

- Kirrane, Mileo, Decker, *Access Control and the RDF: A Survey*, Semantic Web 8(2), 2017：https://www.semantic-web-journal.org/system/files/swj1084.pdf（唯一把 sameAs 放进访问控制传播的同行评审综述；关键句为转述，二手）
- GraphDB sameAs optimization：https://graphdb.ontotext.com/documentation/11.2/sameas-optimisation.html
- Stardog named graph security / entity resolution：https://docs.stardog.com/
- PROV-O：https://www.w3.org/TR/prov-o/（`alternateOf`/`specializationOf` 提供弱于同一的词汇）
