---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# 04 证据：本仓库 E + 未入库 signal

> 本目录只做来源索引。**已入库来源通过 E-21/E-22 引用；未入库的留 signal，不写成 E。**
> 旧于 2026-07 或 origin 不在 US/China/Germany/Singapore 的来源已删除，不再引用。

## 1. 本仓库已用的 E / 主题

| 来源 | 用在哪 | 等级 |
|---|---|---|
| [E-02](../../../topics/conclusions.md) | checker 的 catch/FA；建/用的验收基线 | 已核 |
| [E-03](../../../topics/conclusions.md) | 检索/接地；query 前先修检索 | 已核 |
| [E-04](../../../topics/conclusions.md) | 动作前的 false-veto；治理的代价 | 已核 |
| [E-12](../../../topics/conclusions.md) | 薄语义层/投影；建的优先级 | 已核 |
| [E-20](../../../topics/conclusions.md) | engine 的四种语义；执行 ≠ 授权；读路径单实现 | 已核（代码） |
| [E-21](../../../topics/conclusions.md) | Text2SPARQL 三条路线（GGC/NLKGQ/KGVoyager）；各单设置 | 已核（原文）/推测（跨域） |
| [E-22](../../../topics/conclusions.md) | 访问控制三层（Glyph 标签/无策略/trustgraph 执行） | 已核（原文+代码）/推测（部署） |
| [OPA digest](../../../src/open-source/open-policy-agent-opa/digest.md) | C.1 策略层候选；不解析本体、不消费标签 | 已核（代码） |
| [Qlever digest](../../../src/open-source/ad-freiburg-qlever/digest.md) | B.3 执行层候选；不做 OWL 推理 | 已核（代码） |
| [CASTON digest](../../../src/papers/2610.21466-caston-refinement/digest.md) | 精化；high 6/6、medium 0–25% | 旧文引用，不新增 E |
| [03/querying](../../../topics/03-knowledge/querying/README.md) | E-21 的出处；三条路线 | 研究页 |
| [01/access-control](../../../topics/01-constraint/access-control/README.md) | E-22 的出处；标签/策略/执行 | 研究页 |
| [05 生产派](../../../topics/05-produce/README.md) | 生成/精化/表示/生命周期 | 研究页 |

## 2. 外部信号（未入库，只作旁证）

| 来源 | 类型 | 用在哪 | 状态 |
|---|---|---|---|
| [Industrial KG](https://arxiv.org/abs/2609.31663) | 论文（2026-09） | consume：schema-guided extraction | signal |
| [HN: Netflix ontology observability](https://news.ycombinator.com/item?id=50153431) | 论坛讨论（2026-10） | govern：observability/ontology 价值争论 | signal（131 pts/32 comments） |
| [Legal KG](https://arxiv.org/abs/2607.24551) | 论文（2026-07） | consume：法规本体/闭式抽取 | signal |
| [SAGA](https://arxiv.org/abs/2607.14494) | 论文（2026-07） | consume：schema grounding | signal |
| [Build2SPARQL](https://arxiv.org/abs/2610.00224) | benchmark（2026-10） | consume：building KGQA | signal |
| [Researcher Agents](https://arxiv.org/abs/2608.07700) | 论文（2026-08） | consume：predicate selection | signal |
| [Graph-Agentic RAG assurance](https://arxiv.org/abs/2609.06391) | 论文（2026-09） | govern：失败传播/契约 | signal（未入库） |
| [AWS 语义层指南](https://docs.aws.amazon.com/prescriptive-guidance/latest/semantic-layer-agentic-ai-ontology-reasoning-virtual-knowledge-graph/semantic-layer-agentic-ai-ontology-reasoning-virtual-knowledge-graph.html) | 厂商指南 | consume：语义层/MCP | 行业信号 |
| [Gartner/Stardog](https://info.stardog.com/adopt-a-data-semantic-approach-to-drive-business-value-with-genai) | 厂商转载 | 行业在关心什么 | 行业信号 |
| [Progress 博客](https://www.progress.com/blogs/details/the-resurgence-of-ontologies-ontology-driven-ai) | 厂商博客 | 治理/成本/组织 | 行业信号 |

> 2025 与 2026 上半年的旧 signal（2503/2512/2507/Agent-OM/CK25/VAULT/SchemaForge/2604）已删除；不再用它们撑判断。

## 3. 怎么升 E

1. 先落 `src/papers/{id}-{slug}/` 或 `src/web/...`，写 card + digest；**补给批必须 ≥ 2026-07-01 + in-scope origin**；
2. 再写 `topics/03-knowledge` / `topics/05-produce` / `topics/01-constraint` 的 claims；
3. 只有跨派、且要进交付物时才升 `E-xx`；
4. 04 正文只引 E-xx；未入库的留在本页 signal 表。

**本轮已按此升 E-21/E-22。没有 1–3，04 不把外部数字写成结论。**
