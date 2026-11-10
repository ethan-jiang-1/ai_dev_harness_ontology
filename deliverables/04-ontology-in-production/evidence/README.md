---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# 04 证据

> 已入库走 E；未入库只标 signal，不作依据；旧源已删。

## 1. 已入库 E

| E | 用在哪 | 等级 |
|---|---|---|
| E-02 | 建：负例/验收 | 已核 |
| E-04 | 边界：输入 gate≠输出校验 | 已核 |
| E-06 | 边界：失败在 workflow | 已核 |
| E-12 | 建：薄层优先 | 已核 |
| E-19 | 全篇：位置×成本 | 推测（综合） |
| E-20 | 用/治：执行形态 | 已核（代码） |
| E-21 | 用：三路线 | 已核（原文） |
| E-22 | 治：三层访问 | 已核（原文+代码） |
| E-23 | 治：读路径 10 用例 / 第二实现 | 已核（代码） |
| E-24 | 治：策略层语义 / 10 测试 / 优先级空洞 | 已核（标准摘要+文件） |
| E-25 | 建：三关 / 10 坏样本 / 2 抓 2 | 已核（标准卡+文件） |
| E-26 | 用：四路线按资产选 | 推测（综合） |
| E-27 | 治：输出六类 + 跨段传播 | 推测（综合） |

依据：[conclusions](../../../topics/conclusions.md)；不新增 E。

## 1b. topics 支撑页（不是 E，只作证据组织）

| 页 | 用在哪 | 组织什么 |
|---|---|---|
| [consumability](../../../topics/05-produce/representation/consumability.md) | 建：三关 + 10 坏样本 | SHACL/ODCS/LinkML + SFE-O/CASTON/OntoDoc |
| [querying/compare](../../../topics/03-knowledge/querying/compare.md) | 用：4×8 矩阵 + 17 类失败 | GGC/NLKGQ/KGVoyager/Ontop + E-21 |
| [policy](../../../topics/01-constraint/policy/README.md) | 治：策略 schema + 10 测试 | GB/T/XACML/ODRL/Atlas/Ranger/OpenFGA（待入库） |
| [read-path](../../../topics/01-constraint/commit-gate/read-path.md) | 治：10 条用例 + 第二实现 | trustgraph + sparql-guard/Jena（候选/退役） |
| [output-validation](../../../topics/02-judgment/checker/output-validation.md) | 治：六类 + 三态 | pyshacl/open-ontologies/PROV/GE |
| [propagation](../../../topics/06-measure/metrics/propagation.md) | 治：10 类 × 3 段 | E-06/E-05 + 三段 artifacts |

> 这些页不是 E；04 的主句仍落 `E-xx`。页只回答「证据怎么排成表」，不新增判断。三关协议、10 条策略测试、12 条泄漏用例、10×3 故障矩阵是**工程产物**，标「工程产物 / 待核」，不升 E；引用时写 `工程产物`，不写成「已验证」。

## 1c. 标准材料卡（不是 E，条款待核）

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
