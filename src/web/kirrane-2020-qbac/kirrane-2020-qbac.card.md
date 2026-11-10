---
status: draft
source_type: paper
reading: 摘要级
provenance: 原文摘要
updated: 2026-11-11
batch:
source: https://arxiv.org/abs/2007.00461
author: Sabrina Kirrane, Alessandra Mileo, Axel Polleres, Stefan Decker
published: 2020-07-01
influence: arXiv 预印本（未见同行评审版本，待核）；Linked Data 访问控制里少见的「查询重写 vs 结果过滤」形式化对照；被后续 read-path 讨论引用（采用清单 待核）
updates: []
---

# Query Based Access Control for Linked Data：重写 vs 结果过滤

> **arXiv 论文卡，不是 digest，也不入 `papers/`**（未存 PDF/paper.md）；只作外部参照，引用时按「摘要级/待核」对待。
> 只取读路径用得到的三件事：两种执行点怎么比、FILTER 式重写哪里会错、失败往哪边倒。

## 它主张什么

1. **把「查询重写」与「结果过滤」放在同一策略下对照**：用 secure / sound / maximum 三个判据比较；两者不是同一个安全语义。
2. **FILTER 式重写在否定/子查询下不正确**：把策略写成 `FILTER` 追加到查询上，会在 `NOT EXISTS`/`MINUS`/子查询/聚合等算子上漏；这是「重写忘了某个 operator」的形式化版本。
3. **选择「像未授权数据不存在」的语义**：失败/越权时不是「返回部分结果」，而是让请求方无法区分「不存在」与「无权」；这倾向于 fail-closed，而不是 post-filter 的「删掉可见行、其余照返」。

## 场景与 scope

- **场景**：Linked Data / SPARQL 端点；策略用图/三元组模式表达。
- **管什么**：两种执行点的安全性差异；重写在哪些算子上不可靠。
- **不管什么**：不提供 RDF 上的泄漏率 benchmark；不覆盖 SHACL-AF 的具体实现；不证明某个产品安全。
- **不外推**：结论是形式化/设计层；具体实现的泄漏率仍需实测。

## 证据强度

- **一手还是转述**：arXiv 摘要/正文（2026-11-11 检索）；未逐字通读全文，定理与实验 `待核`。
- **有数据吗**：形式化对照 + 示例；不是 benchmark。
- **等级**：两种执行点可对照 `已核（摘要）`；FILTER 在否定/子查询下不正确 `已核（摘要，待核定理）`；fail-closed 倾向 `推测/设计`。

## 与已有判断的关系

| 结论/判断 | 关系 | 说明 |
|---|---|---|
| read-path 的 10 用例矩阵 | **支持（形式化）** | 聚合/否定/子查询是 post-filter 与 rewrite 的分歧点；不是只有「方向」一个维度 |
| 02 R8「只做可见性，不当授权」 | 支持 | 结果过滤的语义是「删可见行」，不等于「像不存在」；后者更接近授权 |
| 03 claim 走查「聚合/异常」 | 支持 | 为「聚合会漏」提供形式化依据，不只是工程猜测 |

## 待核项

- [ ] secure / sound / maximum 的形式定义
- [ ] FILTER 在 `NOT EXISTS`/`MINUS`/子查询下的反例
- [ ] 是否有同行评审版本
- [ ] 与 XACML §9.1.6（NotApplicable 被当 Permit）的关系

## 喂到哪个主题

- `topics/01-constraint/commit-gate/read-path.md` §3/§4/§10
- `deliverables/02-engineering-playbook/recipes/constraint.md` R8
- `deliverables/03-mechanism-reference/sections/claim-walkthrough.md`

## 原文摘录

> "the requester will be aware that data exists which they do not have access to, and could potentially infer unauthorised information"（摘要）

## 对照来源（未单独入档）

- Kirrane, Mileo, Decker, *Access Control and the RDF: A Survey*, Semantic Web 8(2), 2017：https://www.semantic-web-journal.org/system/files/swj1084.pdf
- OASIS XACML 3.0 §9.1.6：NotApplicable 被当作 Permit 会导致越权（本仓库已有 [XACML 卡](../oasis-xacml-3.0/oasis-xacml-3.0.card.md)）
- Plaintext Recovery 2026（RLS/DLS 场景）：post-filter 的侧信道实证，非 RDF；未入档
