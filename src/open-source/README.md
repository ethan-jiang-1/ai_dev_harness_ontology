---
updated: 2026-11-09
---

# src/open-source：真实开源实现

> 第三类源材料：不是论文（[papers](../papers/)），不是博客（[web](../web/)），是**可读代码的真实项目**。
> 目的：回答「论文里的本体机制，在真实 harness 里到底怎么被用 / 被执行，还是只被塞进 prompt」。

## 目录约定

一个项目一个目录：`{org}-{repo}/`（全小写，`/` 换成 `-`）。

```
src/open-source/
├── README.md                  # 本页：候选池 + 选择标准 + 状态表
├── _scan-2026-11-09.md        # 扫描快照：方法、原始数字、未复核项
└── {org}-{repo}/
    ├── card.md                # 来源卡：repo/commit/license/本体在哪/调用点（短）
    ├── digest.md              # 代码阅读正文：自包含，下游唯一入口
    └── code-map.md            # 可选：文件/符号/调用链索引
```

- 模板在 [`../_templates/`](../_templates/)：`open-source-card.md` / `open-source-digest.md` / `open-source-code-map.md`。**本目录不再自带模板。**
- 规则（不 vendor、pin commit、digest 是入口、执行 vs 装饰）见 [src/README §1.1](../README.md#11-开源项目的规则open-source)；本页不重复，避免两处口径。
- **没有 `digest.md` 的项目不算入库**；只有卡的是候选/在读。

## 选择标准（先筛，不先读）

| 维度 | 问什么 |
|---|---|
| 本体中心性 | 本体/schema 是核心对象，还是只是 topic 标签/营销词 |
| 执行 vs 装饰 | 真的跑 SHACL/OWL/约束/查询重写/推理，还是只把本体塞进 prompt |
| harness 接缝 | 能挂到哪个时刻（action-gate / evidence / checker / commit-gate / memory / determinism）；不是接缝就写 `none` |
| 证据 | tests/benchmarks/issues/生产案例，不只看 README |
| 可研究性 | 能否定位到文件/符号；能否与 22 篇 digest 对照 |
| 影响力 | star/采用/标准地位；**star 只作参考，不单独决定入选** |

**排除项**：纯图检索（无 schema 约束/校验/推理）、闭源核心、README 承诺多于代码、star 异常但无提交历史。

## 状态表（2026-11-09 扫描）

扫描快照见 [`_scan-2026-11-09.md`](./_scan-2026-11-09.md)。代码级判断标 `待核` 的表示只看了元数据/README/二手定位，还没自己读过代码。

### 入选（7，按接缝排）

| 项目 | stars | 本体角色 | 接缝 | 选它的理由 |
|---|---:|---|---|---|
| [trustgraph-ai/trustgraph](https://github.com/trustgraph-ai/trustgraph) | 2,902 | core（待核） | action-gate / evidence（待核） | 唯一把 ontology/SHACL/RDF 放在 agent 管道里的活跃项目；要验「运行时 gate 还是离线文档」 |
| [ontodev/robot](https://github.com/ontodev/robot) | 329 | core | commit-gate | reason→validate→diff→release 的真实管线；回答「本体变更/影响面/回滚」到底怎么做（对照 Open Ontologies 的声称） |
| [sib-swiss/sparql-llm](https://github.com/sib-swiss/sparql-llm) | 130† | core | checker | LLM 生成 SPARQL 后，用端点 VoID 逐谓词/类校验，返回 NL 修复提示；自带 MCP server + 生产 chat。**最贴「回路内 schema 检查」的小项目** |
| [RDFLib/pySHACL](https://github.com/RDFLib/pySHACL) | 371 | core | checker | 可嵌入 Python harness 的约束执行；最小可复现；对照 TopBraid SHACL 参考实现 |
| [monarch-initiative/ontogpt](https://github.com/monarch-initiative/ontogpt) | 1,089 | core | evidence（待核） | LinkML schema 约束 + ontology grounding；生物医学有真实使用 |
| [ontop/ontop](https://github.com/ontop/ontop) | 1,016 | core | `none`（供给） | 本体 + R2RML 映射 → SPARQL 重写到 SQL；「本体真被执行」最成熟的形态，可当 LLM 工具 |
| [apache/jena](https://github.com/apache/jena) | 1,501 | core | `none`（控制组） | 标准栈对照组：RDF/SPARQL/SHACL/推理长什么样、为什么难进 agent |

### 依赖 / 对照（不建目录，在 digest 里引用）

| 项目 | stars | 关系 |
|---|---:|---|
| [linkml/linkml](https://github.com/linkml/linkml) | 691 | ontogpt 的 schema 底座；「轻 schema 路线」的对照。若「OWL 太重」成为主线，再单独建卡 |
| [TopQuadrant/shacl](https://github.com/TopQuadrant/shacl) | 248 | SHACL 参考实现，pySHACL 的对照 |
| [INCATools/ontology-development-kit](https://github.com/INCATools/ontology-development-kit) | 391 | ROBOT 的 CI 包装；生命周期流程对照 |
| [owlcs/owlapi](https://github.com/owlcs/owlapi) | 945 | OWL 推理接口，ROBOT/Jena 的依赖 |
| [liveontologies/elk-reasoner](https://github.com/liveontologies/elk-reasoner) | 129 | OWL EL 推理内核 |
| [RDFLib/OWL-RL](https://github.com/RDFLib/OWL-RL) | 181 | OWL2-RL 闭包；pySHACL 的 `-i owlrl` 用 |
| [biolink/biolink-model](https://github.com/biolink/biolink-model) | 269 | ontogpt/Biolink 生态的 schema |
| [neo4j-labs/neosemantics](https://github.com/neo4j-labs/neosemantics) | 972 | RDF/OWL/SHACL 进属性图的一条路 |
| [dice-group/owlapy](https://github.com/dice-group/owlapy) | 115† | Python OWL + HermiT/ELK，回路内一致性检查的候选 |
| [coasys/ad4m](https://github.com/coasys/ad4m) | 103† | SHACL 约束门控图变更 + MCP；license 非标准、LLM 链路未核 |
| [ensaremirerol/shacl-rust](https://github.com/ensaremirerol/shacl-rust) | 5† | `shacl-mcp`：把 SHACL 包成 agent 工具，极小样本 |
| [KRR-Oxford/DeepOnto](https://github.com/KRR-Oxford/DeepOnto) | 328 | 本体补全/嵌入 + DL 推理；学术线候选 |
| [zjunlp/OneKE](https://github.com/zjunlp/OneKE) | 197 | schema 引导抽取的 agent；生成侧对照 |

### 淘汰（不建目录）

| 项目 | stars | 为什么不入选 |
|---|---:|---|
| [microsoft/graphrag](https://github.com/microsoft/graphrag) | 36,593 | 图检索（0 阶形态），本体最多是实体类型提示，不构成约束/校验/推理；一句话对照即可 |
| [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) | 40,608 | 同上；graph 是索引结构 |
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 144,347 | 代码库知识图；star 量级异常，先不投入 |
| [neo4j-labs/llm-graph-builder](https://github.com/neo4j-labs/llm-graph-builder) | 5,301 | schema 引导抽取，但约束停在抽取阶段 |
| [semantica-agi/semantica](https://github.com/semantica-agi/semantica) | 14,475 | 2025-06 建、星数极高；ontology 是核心还是营销**待核**，无代码定位前不建卡 |
| [deeplethe/utopia](https://github.com/deeplethe/utopia) | 8,692 | 2026-08 建，增速异常；「企业世界模型」是否只是图数据库**待核** |
| [fabio-rovai/open-ontologies](https://github.com/fabio-rovai/open-ontologies) | 2,848 | 声称的 blast radius/rollback 是代码还是文档**待核**；研究点已由 ROBOT 覆盖 |
| [HelixDB/helix-foundry](https://github.com/HelixDB/helix-foundry) | 2,082 | 2026-10 建；agent 起草本体，太新，无 issue/使用证据 |
| [FengZhenfei/carrel](https://github.com/FengZhenfei/carrel) | 801 | 2026-09 建、0 open issues；名字命中但证据不足 |
| [getzep/graphiti](https://github.com/getzep/graphiti) | 32,652 | schema-typed 时序记忆，不是形式本体；留作 04 记忆接缝对照 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | 33,135 | 同上；memory graph，不是 ontology |

## 影响力：star 会骗人，采用不会

- **标准/推理类 star 低、采用广**：Jena 是 Apache 顶级项目；ROBOT/ODK 是 OBO Foundry 的发布链；pySHACL 的 PyPI 月下载约 160 万（pypistats，2026-11-09）；sparql-llm 的 star 只有 130，但有 expasy.org/chat 的生产部署。
- **图检索类 star 高一个量级**：GraphRAG 3.6 万、cognee 3.3 万、graphiti 3.3 万。
- 这个落差本身就是证据：**社区注意力在「检索」，不在「执行」**——对应 P1/P2。选项目时按「本体是否被执行」而非 star 排序。

## 先做哪几个

1. **给 7 个入选项目建 `card.md`**（只写可定位事实，不写结论）。
2. **先深读 2 个**：`trustgraph`（最贴题的 agent 内本体）+ `rdflib-pyshacl`（最小可跑、当天能出调用链）。
3. 再补 `ontop`（OBDA）与 `robot`（本体生命周期），这两个是「真执行」的两个极端形态。
4. 每个项目读完回 `topics/<派>/sources.md`；只是「论文机制没找到实现」→ 写进 `frontier.md` 的 G/N。
