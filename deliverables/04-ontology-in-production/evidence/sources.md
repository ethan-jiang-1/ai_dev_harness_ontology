---
status: draft
updated: 2026-11-10
parent: README.md
---

# 标准材料卡与外部 signal

> 标准卡只证明「标准说了什么」，不证明「你的实现/映射正确」；外部 signal 未入库，只作旁证，不作依据。

## 1. 标准材料卡（不是 E，条款待核）

| 标准 | 用在哪 | 读法 |
|---|---|---|
| [GB/T 43697-2024](../../../src/web/gbt-43697/gbt-43697.card.md) | C.1/C.2：三级 vs 1–4 | 摘要级；三级名称转述 |
| [GB/T 35273-2020](../../../src/web/gbt-35273/gbt-35273.card.md) | C.2：PII 类别 | 摘要级；正文未取 |
| [W3C ODRL 2.2](../../../src/web/w3c-odrl-2.2/w3c-odrl-2.2.card.md) | C.2：冲突/义务 | 精读；§2.10 待核 |
| [OASIS XACML 3.0](../../../src/web/oasis-xacml-3.0/oasis-xacml-3.0.card.md) | C.2：合并算法/obligation | 精读；FulfillOn 待核 |
| [W3C SHACL](../../../src/web/w3c-shacl/w3c-shacl.card.md) | A.4/A.5、C.5 | 摘要级；条款待核 |
| [ODCS v3.1.0](../../../src/web/odcs-v3.1/odcs-v3.1.card.md) | A.1/A.5 | 精读；Required 待核 |

> 材料卡只证明「标准说了什么」，不证明「你的实现/映射正确」；不升 E。

## 2. 外部信号（未入库，只作旁证）

| 来源（signal） | 用在哪 |
|---|---|
| Industrial KG 2609.31663 | 建：schema 抽取 |
| SAGA 2607.14494 | 建：grounding |
| Legal KG 2607.24551 | 用：法规本体 |
| Build2SPARQL 2610.00224 | 用：building KGQA |
| Researcher Agents 2608.07700 | 用：predicate |
| Graph-Agentic 2609.06391 | 治：失败传播 |
| AWS 语义层指南 | 用：语义层/MCP |
| HN: Netflix ontology | 治：observability |

> 这些来源没有入库 digest/card；引用时标 `signal`，不作「已核」。

> 回 [04 目录](../README.md) ｜ 回 [证据台账](./ledger.md)
