---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# 04 证据：本仓库 E + 外部信号

> 本目录只做来源索引；**外部来源未入库、未升 E**。正式引用仍走 `topics/conclusions.md` 的 E-xx 或对应 digest。

## 1. 本仓库已用的 E / 主题

| 来源 | 用在哪 | 等级 |
|---|---|---|
| [E-02](../../../topics/conclusions.md) | checker 的 catch/FA；建/用的验收基线 | 已核 |
| [E-03](../../../topics/conclusions.md) | 检索/接地；query 前先修检索 | 已核 |
| [E-04](../../../topics/conclusions.md) | 动作前的 false-veto；治理的代价 | 已核 |
| [E-12](../../../topics/conclusions.md) | 薄语义层/投影；建的优先级 | 已核 |
| [E-20](../../../topics/conclusions.md) | engine 的四种语义；执行 ≠ 授权 | 已核（代码） |
| [05 生产派](../../../topics/05-produce/README.md) | 生成/精化/表示/生命周期 | 研究页 |
| [03 知识派](../../../topics/03-knowledge/README.md) | 编译/投影；query 的供给侧 | 研究页 |
| [01 约束派](../../../topics/01-constraint/README.md) | action/commit/读路径 | 研究页 |

## 2. 外部信号（摘要/指南级，未入库）

| 来源 | 类型 | 用在哪 | 状态 |
|---|---|---|---|
| [Ontology Generation](https://arxiv.org/abs/2503.05388) | 论文 | build：CQ→候选 | 摘要级 |
| [Axiom Benchmark](https://arxiv.org/abs/2512.05594) | 论文 | build：公理质量 | 摘要级 |
| [LLM-assisted Ontology Evaluation](https://arxiv.org/abs/2507.14552) | 论文 | build：CQ 评估 | 摘要级 |
| [Agent-OM](https://arxiv.org/abs/2312.00326) | 论文 | build：对齐 | 摘要级 |
| [CASTON](https://arxiv.org/abs/2610.21466) | 论文 | build：精化 | 摘要级 |
| [Industrial KG](https://arxiv.org/abs/2609.31663) | 论文 | consume：schema-guided extraction | 摘要级 |
| [Legal KG](https://arxiv.org/abs/2607.24551) | 论文 | consume：法规本体/闭式抽取 | 摘要级 |
| [CK25](https://zenodo.org/records/16912605) | benchmark | consume：企业 Text2SPARQL | 摘要级 |
| [GGC](https://arxiv.org/abs/2607.28082) | 论文 | consume：选择性纠错 | 摘要级 |
| [SAGA](https://arxiv.org/abs/2607.14494) | 论文 | consume：schema grounding | 摘要级 |
| [SchemaForge](https://arxiv.org/abs/2508.01815) | 论文 | consume：异构 KG | 摘要级 |
| [Build2SPARQL](https://arxiv.org/abs/2610.00224) | benchmark | consume：building KGQA | 摘要级 |
| [Researcher Agents](https://arxiv.org/abs/2608.07700) | 论文 | consume：predicate selection | 摘要级 |
| [VAULT](https://elib.dlr.de/214536/) | 论文 | govern：访问控制 | 摘要级 |
| [Graph-Agentic RAG assurance](https://arxiv.org/abs/2609.06391) | 论文 | govern：失败传播/契约 | 摘要级 |
| [Enterprise Agentic Systems](https://arxiv.org/abs/2604.00555) | 预印本 | govern：输出校验 | 摘要级 |
| [AWS 语义层指南](https://docs.aws.amazon.com/prescriptive-guidance/latest/semantic-layer-agentic-ai-ontology-reasoning-virtual-knowledge-graph/semantic-layer-agentic-ai-ontology-reasoning-virtual-knowledge-graph.html) | 厂商指南 | consume：语义层/MCP | 行业信号 |
| [Gartner/Stardog](https://info.stardog.com/adopt-a-data-semantic-approach-to-drive-business-value-with-genai) | 厂商转载 | 行业在关心什么 | 行业信号 |
| [Progress 博客](https://www.progress.com/blogs/details/the-resurgence-of-ontologies-ontology-driven-ai) | 厂商博客 | 治理/成本/组织 | 行业信号 |

## 3. 怎么升 E（如果以后要做）

1. 先落 `src/papers/{id}-{slug}/` 或 `src/web/...`，写 card + digest；
2. 再写 `topics/05-produce` / `topics/03-knowledge` / `topics/01-constraint` 的 claims；
3. 只有跨派、且要进交付物时才升 `E-xx`；
4. 04 正文只引 E-xx；外部信号留在本页。

**没有 1–3，04 不把外部数字写成结论。**
