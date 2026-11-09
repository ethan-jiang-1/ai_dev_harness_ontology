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

## 状态表（2026-11-09 扫描 + 一轮代码复核）

扫描快照见 [`_scan-2026-11-09.md`](./_scan-2026-11-09.md)。**复核说明**：六个高星项目做过一轮 tarball/代码检查（由研究 agent 完成，本仓库尚未自己复核），结论已折进下表；标 `待核` 的路径要等我自己读过代码才升 `已核`。

### 本轮消化（4，≥1,000★）

本轮临时门槛：**stars ≥ 1,000**（2026-11-09 起，可撤销）。消化顺序与 C/A 闸见 [开源消化计划](../../meta/open-source-digestion-plan.md)。4 个均已建卡并写 `digest.md`（见下表与状态行）。

| 项目 | stars | 本体在代码里做什么 | 接缝 | 为什么选它 / 要小心什么 |
|---|---:|---|---|---|
| [trustgraph-ai/trustgraph](https://github.com/trustgraph-ai/trustgraph) | 2,902 | 两处：`extract/kg/ontology/`（loader/selector/triple_converter，从配置服务加载 OWL-like 结构）+ `specs/ontology/trustgraph.ttl`；**`policy/policy_filter.py` 是自研 SHACL-AF 求值器**，对查询结果做策略过滤 | checker（读路径）/ commit-gate（未定位） | 唯一成规模的「agent + 本体」平台（30 贡献者、1,603 commits、28 个月）。**SHACL 是真执行，但不是 pyshacl**——grep 库名会漏，要读 `policy_filter.py` |
| [semantica-agi/semantica](https://github.com/semantica-agi/semantica) | 14,475 | `semantica/ontology/`（owl_generator / class_inferrer / competency_questions）；`run_shacl_validation()` 调 pyshacl；24 releases + strict-xfail CI | evidence / checker（**待核**） | 影响最大，用来回答「高星是否真本体」；已核：pyshacl 与 OWL 生成是真代码。贡献者 100+（API 截断），承诺要逐条回代码 |
| [fabio-rovai/open-ontologies](https://github.com/fabio-rovai/open-ontologies) | 2,848 | `src/shacl.rs` + `shacl_verified.rs`；314 个 `.ttl`、54 个 SHACL；W3C SHACL 测试套件；16 releases | commit-gate | 真 SHACL 引擎 + 本体变更/回滚的声称，直接对应 commit boundary。12 贡献者、680/1,080 提交来自 `claude` 账号——AI 辅助，非造假，但别把 commit 数当人力 |
| [ontop/ontop](https://github.com/ontop/ontop) | 1,016 | OWL 2 QL 本体 + R2RML 映射 → SPARQL 重写成 SQL | `none`（供给） | 2013 年至今的 OBDA 参考实现；「本体真被执行」的成熟形态，也可当 LLM 查询工具 |

**状态（2026-11-09）**：4 个本轮项目全部已消化（trustgraph、semantica、ontop、open-ontologies）；矩阵 `absorbed`×3 + `partial`×1（ontop 只进 frontier）。低于 1,000★ 的三个（pySHACL 371 / ROBOT 329 / sparql-llm 130）已删除目录，只在 [`_scan-2026-11-09.md`](./_scan-2026-11-09.md) 保留元数据；撤销门槛时重新建卡。

### 对照 / 依赖（不建目录，在 digest 里引用）

| 项目 | stars | 关系 |
|---|---:|---|
| [apache/jena](https://github.com/apache/jena) | 1,501 | 标准栈控制组（RDF/SPARQL/SHACL/推理）；「为什么难进 agent」的参照 |
| [monarch-initiative/ontogpt](https://github.com/monarch-initiative/ontogpt) | 1,089 | LinkML + ontology grounding，生成侧对照；约束的是抽取结构，不是执行判据 |
| [linkml/linkml](https://github.com/linkml/linkml) | 691 | 「轻 schema 路线」；ontogpt 的底座。若「OWL 太重」成主线，再升卡 |
| [owlcs/owlapi](https://github.com/owlcs/owlapi) | 945 | OWL 推理接口，ROBOT/Jena 的依赖 |
| [liveontologies/elk-reasoner](https://github.com/liveontologies/elk-reasoner) | 129 | OWL EL 推理内核（ROBOT 的 reasoner） |
| [RDFLib/OWL-RL](https://github.com/RDFLib/OWL-RL) | 181 | OWL2-RL 闭包；pySHACL `-i owlrl` 的 entailment 源 |
| [TopQuadrant/shacl](https://github.com/TopQuadrant/shacl) | 248 | SHACL 参考实现，pySHACL 的对照 |
| [INCATools/ontology-development-kit](https://github.com/INCATools/ontology-development-kit) | 391 | ROBOT 的 CI 包装；生命周期流程对照 |
| [biolink/biolink-model](https://github.com/biolink/biolink-model) | 269 | ontogpt/semantica 生态的 schema |
| [dice-group/owlapy](https://github.com/dice-group/owlapy) | 115† | Python OWL + HermiT/ELK，回路内一致性检查的候选 |
| [coasys/ad4m](https://github.com/coasys/ad4m) | 103† | SHACL 门控图变更 + MCP；license 非标准、LLM 链路未核 |
| [ensaremirerol/shacl-rust](https://github.com/ensaremirerol/shacl-rust) | 5† | `shacl-mcp`：把 SHACL 包成 agent 工具；样本极小 |
| [zazuko/rdf-validate-shacl](https://github.com/zazuko/rdf-validate-shacl) | 126† | 纯 JS SHACL 引擎，可做输出闸门 |
| [neo4j-labs/neosemantics](https://github.com/neo4j-labs/neosemantics) | 972 | RDF/OWL/SHACL 进属性图的一条路 |
| [KRR-Oxford/DeepOnto](https://github.com/KRR-Oxford/DeepOnto) | 328 | 本体补全/嵌入 + DL 推理；学术候选 |
| [zjunlp/OneKE](https://github.com/zjunlp/OneKE) | 197 | schema 引导抽取的 agent；生成侧候选 |

### 候选待核（真实，但先不进第一批）

| 项目 | stars | 为什么先不进 |
|---|---:|---|
| [deeplethe/utopia](https://github.com/deeplethe/utopia) | 8,692 | `crates/utopia-ingest/src/ontology_rdf.rs` 真解析 OWL 构造；但 3 个月做到 8.7k 星、536/929 提交来自 `claude`——先看稳定性与真实用户 |
| [HelixDB/helix-foundry](https://github.com/HelixDB/helix-foundry) | 2,082 | `backend/ontology/` 是自建 Go schema，不是 RDF/OWL；1 个月，无独立使用证据 |
| [FengZhenfei/carrel](https://github.com/FengZhenfei/carrel) | 801 | `app/kb_pipeline/ontology.py` 是 680 行 LinkML 子集；0 个 `.ttl/.owl`，OWL/SHACL 被推到「plugin side」；2 人 |

### 淘汰（不建目录）

| 项目 | stars | 为什么不入选 |
|---|---:|---|
| [microsoft/graphrag](https://github.com/microsoft/graphrag) | 36,593 | 图检索（0 阶形态），本体最多是实体类型提示，不构成约束/校验/推理；一句话对照即可 |
| [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) | 40,608 | 同上；graph 是索引结构 |
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 144,347 | 代码库知识图；star 量级异常，先不投入 |
| [neo4j-labs/llm-graph-builder](https://github.com/neo4j-labs/llm-graph-builder) | 5,301 | schema 引导抽取，但约束停在抽取阶段 |
| [getzep/graphiti](https://github.com/getzep/graphiti) | 32,652 | schema-typed 时序记忆，不是形式本体；留作 04 记忆接缝对照 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | 33,135 | 同上；memory graph，不是 ontology |

## 影响力：star 会骗人，采用不会

- **标准/推理类 star 低、采用广**：Jena 是 Apache 顶级项目；ROBOT/ODK 是 OBO Foundry 的发布链；pySHACL 月下载约 160 万；sparql-llm 只有 130 星，但有 expasy.org/chat 的生产部署与论文。
- **图检索类 star 高一个量级**：GraphRAG 3.6 万、cognee 3.3 万、graphiti 3.3 万。
- 这个落差本身就是证据：**社区注意力在「检索」，不在「执行」**——对应 P1/P2。
- 三个反信号：① `claude` 账号在多个高星本体项目里占大量提交（open-ontologies 680/1,080、utopia 536/929）；② 新项目 star 增速异常（utopia 3 个月 8.7k）；③ **SHACL 可以自研**——trustgraph 不用 pyshacl，而是在 `policy/policy_filter.py` 里自己实现 SHACL-AF 求值；只 grep `pyshacl` / `shacl.rs` 会误判。判断标准是「有没有 shape 求值 + 是否影响返回」，不是依赖清单。

## 先做哪几个

按 [开源消化计划](../../meta/open-source-digestion-plan.md) 的波次走，一次只动 1–2 个派：

1. **Wave 1（01 / 02）**：`trustgraph`（读路径策略链 + `tests/unit/test_policy`）。
2. **Wave 2（03）**：`semantica`（`run_shacl_validation` 最小示例）→ `ontop`（Docker 最小示例 + 查询重写）。
3. **Wave 3（05 / 01）**：`open-ontologies`（W3C SHACL 一条用例 + 变更/影响面）。
4. **Wave 4**：`jena` / `ontogpt` 只做对照段；跨派结论只在两个以上来源同向时动 `conclusions`；吸收矩阵记一行。
