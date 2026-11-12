---
status: draft
source_type: standard
standing: normative
reading: 摘要级
provenance: 原文正文
updated: 2026-11-11
batch:
source: https://www.w3.org/TR/shacl-af/
author: W3C RDF Data Shapes Working Group（Knublauch / Allemang / Steyskal）
published: 2017-06-08
influence: W3C Working Group Note（不是 REC，自述 work in progress）；SHACL-AF 的 custom target / SPARQL rule 被 trustgraph 的 policy filter 直接使用（E-20）
updates: []
admission: admitted
gate_checked: 2026-11-11
impact_evidence: "I1: W3C Note; trustgraph implementation"
liveness: standard-in-force
provenance_type: standard-body
---

# W3C SHACL Advanced Features（SHACL-AF）

> 标准卡，不是 digest。读的是摘要、§3.1（custom targets）、§8（rules）与附录 B（Security and Privacy）；**未通读全文**。
> 只取读路径用得到的两件事：**不支持 custom target 时行为未定义**，以及**只用可信 shape graph**。

## 它主张什么

1. **SHACL-AF 扩展 SHACL Core**：custom targets（`sh:SPARQLTarget`）、annotation properties、functions、node expressions、rules（`sh:SPARQLRule`）。它是 **Working Group Note**，不是 Recommendation；文档自己写「work in progress」。
2. **不支持 custom target 时行为未定义**：引擎对无法处理的 custom target，「behavior … is left undefined」；只 SHOULD 报 warning。也就是说：**没有「必须拒绝」的规范要求**。
3. **shape graph 必须在信任边界内**：附录 B 的唯一总建议是「only use trusted and controlled shape graphs」；它不提供策略正确性或执行安全的保证。

## 场景与 scope

- **场景**：RDF 图上的 target/rule/函数；常被拿来做策略求值、派生、校验。
- **管什么**：语法与执行语义（在支持的引擎上）。
- **不管什么**：不管访问控制、不管 fail-open/fail-closed、不管策略图是否可信；这些是实现/部署的选择。
- **对读路径的含义**：trustgraph 用 `sh:SPARQLTarget` + `sh:SPARQLRule` 做 post-filter；当 target/rule 异常或不受支持时，SHACL-AF 未定义行为，trustgraph 选择「不命中 → 放行」（fail-open）。**这是实现选择，不是标准要求，也不是标准禁止。**

## 证据强度

- **一手还是转述**：W3C Note 原文（2026-11-11 抓取）；条款号/段落 `待核`。
- **有数据吗**：无实验；规范文本。
- **等级**：两条引文 `已核（原文）`；「trustgraph 选择 fail-open」是 E-20/F6 的代码事实，不是本卡的规范主张。

## 与已有判断的关系

| 结论/判断 | 关系 | 说明 |
|---|---|---|
| read-path 的 fail-open（F6） | **支持（边界）** | SHACL-AF 对不支持 target 的行为未定义；trustgraph 的 fail-open 是实现选择；标准不能拿来当「必须放行」的依据 |
| 02 R8 的「策略图」前提 | 支持 | 只用可信/受控 shape graph；策略图是信任边界的一部分 |
| NIST SP 800-162 ABAC | 对照 | ABAC 的授权判定用 subject/object/action/environment 属性；PEP/PDP 分离；post-filter 只看到结果集，不能替代完整的策略判定 |

## 待核项

- [ ] §3.1 的原文段落号
- [ ] 附录 B 的完整措辞
- [ ] SHACL-AF 在 trustgraph 里的具体调用点（已有 E-20/commit-gate F5–F7）

## 喂到哪个主题

- `topics/01-constraint/commit-gate/read-path.md`（fail-open 的标准边界）
- `deliverables/02-engineering-playbook/03-recipes/06-constraint.md` R8
- `deliverables/03-mechanism-reference/02-sections/95-claim-walkthrough.md`

## 原文摘录

> "The behavior of a SHACL engine that is unable to handle a given custom target is left undefined."（§3.1）

> "The general advice is for users to only use trusted and controlled shape graphs."（附录 B）

> "Publication as a Working Group Note does not imply endorsement by the W3C Membership."（Status of This Document）

## 对照来源（未单独入档）

- NIST SP 800-162, Guide to ABAC：https://csrc.nist.gov/pubs/sp/800/162/upd2/final（ABAC 定义：subject/object/operation/environment 属性对策略求值；PEP/PDP 分离）
