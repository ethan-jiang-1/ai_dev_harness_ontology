# src/open-source：真实开源实现

> 第三类源材料：不是论文（`src/papers/`），不是博客（`src/web/`），是**可读代码的真实项目**。  
> 目的：回答“论文里的本体机制，在真实 harness 里到底怎么被用/被执行，还是只被塞进 prompt”。

## 目录约定

一个项目一个目录：`{org}-{repo}/`

```
src/open-source/
├── README.md                  # 本页：index + 候选 + 选择标准
├── _template.md               # 项目卡模板
└── {org}-{repo}/
    ├── card.md                # 来源卡：repo/commit/license/本体角色/接缝/证据
    └── code-map.md            # 可选：文件/函数/调用链；只写定位，不贴大段代码
```

- **不 vendor 代码**：不 clone 整仓进仓库；只写 commit/tag + 链接 + 文件路径。
- **一个项目一卡**：`card.md` 是来源卡，不是教程；机制细节写 `code-map.md`。
- **pin 版本**：必须写 commit SHA 或 release tag；`stars_at_scan` 只作影响力参考，不是质量证明。
- **许可**：写 license；不复制受限制代码。

## 选择标准（先筛，不先读）

| 维度 | 问什么 |
|---|---|
| 影响力 | stars/forks/commits/被引用/生产使用；不只看 star |
| 本体中心性 | 本体/schema 是核心，还是只是 topic 标签/营销词 |
| 执行 vs 装饰 | 真的跑 SHACL/OWL/policy/约束，还是只把本体塞进 prompt |
| harness 接缝 | 供给 / 判定 / 授权 / 记忆 / 生成 / 度量，哪一格 |
| 证据 | tests/benchmarks/issues/案例，不只看 README |
| 可研究性 | 能否定位到文件/函数；能否与 22 digest 对照 |

## 候选池（2026-11-09 扫描，stars 会变）

### A. 本体原生 / agent 基础设施

| 项目 | 扫描星数 | 一句话 | 为什么值得看 |
|---|---:|---|---|
| [semantica-agi/semantica](https://github.com/semantica-agi/semantica) | 14,475 | graph-native context / accountable AI | 把 context graph、provenance、ontology 放在 agent 基础设施层；要看它是真执行还是只做检索 |
| [deeplethe/utopia](https://github.com/deeplethe/utopia) | 8,692 | enterprise world model | 世界模型 + 时序 KG + ontology；看“企业世界模型”是否只是图数据库 |
| [trustgraph-ai/trustgraph](https://github.com/trustgraph-ai/trustgraph) | 2,901 | AI governance platform for agents | topics 含 ontology/SHACL/RDF；最接近“本体在 harness 里执行” |
| [fabio-rovai/open-ontologies](https://github.com/fabio-rovai/open-ontologies) | 2,848 | production ontology change/rollback/blast radius | 本体变更/回滚/影响面；对应 commit-gate / lifecycle |
| [HelixDB/helix-foundry](https://github.com/HelixDB/helix-foundry) | 未扫 | agent drafts ontology over company data | “agent 起草本体”的真实管线；看人审/落地在哪 |
| [FengZhenfei/carrel](https://github.com/FengZhenfei/carrel) | 801 | ontology-augmented generation for agents | 名字直接命中；看 ontology 在生成链路里的位置 |

### B. GraphRAG / KG for LLM（高影响，但本体未必中心）

| 项目 | 扫描星数 | 一句话 | 为什么值得看 |
|---|---:|---|---|
| [microsoft/graphrag](https://github.com/microsoft/graphrag) | 36,593 | modular graph-based RAG | 高影响基线；对照“社区摘要”与“本体约束”的区别 |
| [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) | 40,608 | simple/fast graph RAG | 高星；看 graph 是检索结构还是语义约束 |
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 144,347 | codebase → queryable KG | 极高星；code KG，不是本体，但能对照“结构图”与“本体” |
| [neo4j-labs/llm-graph-builder](https://github.com/neo4j-labs/llm-graph-builder) | 5,301 | LLM graph construction | 图构建管线；看 schema/ontology 是否被约束 |

### C. 本体执行 / 校验（控制组）

| 项目 | 一句话 | 为什么值得看 |
|---|---|---|
| [apache/jena](https://github.com/apache/jena) | RDF/OWL/SHACL 工具链 | 真执行/推理的基线；看它为什么难进 agent harness |
| [RDFLib/pySHACL](https://github.com/RDFLib/pySHACL) | SHACL 校验 | 约束执行的“硬控制组” |
| [owlcs/owlapi](https://github.com/owlcs/owlapi) | OWL API | 本体推理的工程接口 |
| [protegeproject/webprotege](https://github.com/protegeproject/webprotege) | 协作本体编辑 | 812 星；看“人维护本体”的真实工作流 |
| [linkml/linkml](https://github.com/linkml/linkml) | schema/ontology as code | 轻量 schema 路线，可能比 OWL 更适合 harness |

### D. Harness / policy（对照接缝）

| 项目 | 一句话 | 为什么值得看 |
|---|---|---|
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | stateful agent graph | 看本体能挂哪个节点/状态；它本身不做本体 |
| [NVIDIA/NeMo-Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) | policy DSL for LLM | 对照“policy engine”与“ontology constraint” |
| [open-policy-agent/opa](https://github.com/open-policy-agent/opa) | policy as code | 对照“可执行约束”的另一种形态 |

## 建议先深读的 5 个

1. **trustgraph**：ontology/SHACL 在 agent 治理里是否真的执行。
2. **semantica**：高星“context graph”是否只是图检索，还是本体/ provenance 真进回路。
3. **open-ontologies**：本体变更/回滚/影响面，直接对应 commit-gate/lifecycle。
4. **microsoft/graphrag**：高影响基线，用来对照“图检索 ≠ 本体约束”。
5. **apache/jena + pySHACL**：控制组，回答“真执行长什么样、为什么少见于 agent”。

## 下一步

- 先给这 5 个建 `card.md`，每个只写：repo/commit/license、本体在哪、接缝、执行/装饰判断、证据、与哪篇 digest 对照。
- 不急着写“结论”；先做代码定位。
