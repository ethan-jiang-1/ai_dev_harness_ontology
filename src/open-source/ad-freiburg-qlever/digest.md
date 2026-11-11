---
status: draft
updated: 2026-11-09
quality: B
based_on: card.md
commit: 0998359ab0a569a12eae22050c694b6aa46bdda4
claims: []
---

# ad-freiburg/qlever：把生成的 SPARQL 真正跑起来

> **自包含**：不假设读者读过 README、card。代码位置写到 `文件:符号`，不贴大段代码。
> `已核` = 读过代码、能指到文件/函数；`推测` = 只读 README/文档。

## 0. 三句话

1. **它是什么**：高性能 RDF/SPARQL 引擎；完整 SPARQL 1.1；单机可查千亿级 triples；有 Docker/原生包/嵌入式库。
2. **本体怎么被用**：**没有**。只加载 RDF triples、执行 SPARQL；OWL/SHACL 不会被 entailment/约束求值。
3. **证据到哪**：读到调用链（`ServerMain` → `Server` → `SparqlParser` → `QueryPlanner` → `QueryExecutionTree` → `Index`）；未跑 Qlever、未测延迟/内存。`quality: B`。

## 1. 项目与维护状态

- **定位**：RDF/SPARQL 查询引擎；不是本体引擎、不是策略引擎、不是 LLM。
- **维护**：940★；最后 push 2026-11-09；commit `0998359`；Apache-2.0；活跃；有 CI/benchmark/Docker。
- **能力面**：SPARQL 1.1（federated、named graphs、Graph Store HTTP、updates）、materialized views、text search、spatial、autocompletion、嵌入式。
- **不把它当**：OWL reasoner、SHACL validator、policy engine、Text2SPARQL 生成器。

## 2. 本体在哪

- **没有**。`src/parser/SparqlParser.cpp` 解析 SPARQL；`src/index/Index.cpp` 建 RDF 索引；`src/engine/` 执行算子。没有 OWL entailment、没有 SHACL。
- ontology 可以作为 triples 加载，但不会被“执行”；如果要推理/约束，要在上游做或换引擎。
- 对 04 的用法：它是 **B.3 的执行层**，不是本体层。

## 3. 调用链

| 步 | 文件:符号 | 做什么 |
|---|---|---|
| 建索引 | `src/index/IndexBuilderMain.cpp`、`src/index/Index.cpp` | 加载 RDF、建 permutation/统计 |
| 启动 | `src/ServerMain.cpp` → `src/engine/Server.cpp` | HTTP endpoint/服务 |
| 解析 | `src/parser/SparqlParser.cpp` | SPARQL 1.1 解析 |
| 规划 | `src/engine/QueryPlanner.cpp` | join 顺序/算子选择 |
| 执行 | `src/engine/QueryExecutionTree.cpp` | 算子树求值 |
| 结果 | `src/engine/ExportQueryExecutionTrees.cpp` | JSON/CSV/TSV |
| 更新 | `src/engine/ExecuteUpdate.cpp` | SPARQL Update |
| 嵌入 | `src/libqlever/` | 进程内使用 |

**失败处理**：解析/执行错误返回给调用方；空结果是正常结果，不区分 coverage/query/data——这个分因要在 04 B.5 的 `empty_reason` 里自己做。

## 4. 接缝判定

| 问题 | 回答 | 证据 |
|---|---|---|
| 有外部判据（判据来自本体） | **否**：只按 SPARQL 查 triples | `src/parser/`、`src/engine/` |
| 有阻断能力 | **否**：执行查询，不拦动作/不拒输出 | `src/engine/Server.cpp` |
| 位置明确 | **否**：B.3 的执行层，不是本体接缝 | 本文 §6 |
| 与本体执行的关系 | 无：不 entail/不校验 | `src/index/`、`src/engine/` |

## 5. 真执行还是装饰

- **真执行**：SPARQL 解析、规划、算子求值、索引扫描都是真代码；有 benchmark/CI/生产 demos。不是“把查询塞进 prompt”。
- **但不是本体执行**：没有 OWL entailment/SHACL；它执行的是**查询**，不是本体。
- **不能证明**：换 Qlever 就能提高 Text2SPARQL 准确率；准确率在生成/grounding，执行层只决定“跑不跑得动、快不快”。

## 6. 对 04 B.3 的用法

B.3 的链是 `生成 → 执行 → 空结果/错误 → 纠错/验证`；Qlever 只填**执行**：

```
question → LLM 生成 SPARQL (GGC/NLKGQ/KGVoyager)
        → Qlever 执行 (endpoint/snapshot)
        → 空结果/错误/延迟
        → 纠错/验证 (GGC/调用方)
```

- **能补的**：真执行、SPARQL 1.1 覆盖、性能、Docker/嵌入式部署、结果格式。
- **不能补的**：生成质量、schema grounding、空结果分因、策略/权限。
- **接线要点**：pin snapshot/version；记录 endpoint；空结果分因在调用方；不要把 Qlever 的“快”当“准”。

## 7. 成本 / 运维

- **形态**：C++ 二进制；Docker/原生包；索引构建与查询分离；内存/磁盘随数据量。
- **成本**：未在本仓库测；索引构建时间/内存是主要成本；查询延迟取决于图/查询。
- **风险**：索引/snapshot 漂移；SPARQL 方言差异；更新/事务语义要另核。

## 8. 与 E-21 的关系

- **E-21** 说三条生成路线各单设置；它们都需要一个执行层。Qlever 是**执行层的候选实现**，不是 E-21 的证据。
- NLKGQ/QRAKEN 论文用 QLever；这能说明“工程上可接”，不能说明“换了引擎准确率会变”。
- 如果要把 Qlever 写进 E-21，需要另做代码级/实测核对；本页只是候选。

## 9. 还没解决 / 下一步

- 空结果分因：Qlever 返回空结果，但 coverage/query/data 要调用方分；未做。
- 与 GGC 的 Gate 集成：执行结果/错误能不能作为 Gate 特征？未做。
- 性能基准：在目标图/查询分布上的 p50/p99、内存；未测。
- OWL/SHACL：不在 Qlever；要不要上游接 ontop/pySHACL？未做。

## 10. 代码位置

- 入口：`src/ServerMain.cpp`、`src/engine/Server.cpp`
- 解析/规划/执行：`src/parser/SparqlParser.cpp`、`src/engine/QueryPlanner.cpp`、`src/engine/QueryExecutionTree.cpp`
- 索引：`src/index/Index.cpp`、`src/index/IndexBuilderMain.cpp`
- 结果/更新：`src/engine/ExportQueryExecutionTrees.cpp`、`src/engine/ExecuteUpdate.cpp`
- 嵌入：`src/libqlever/`
- 代码地图：[code-map.md](./code-map.md)（文件/符号索引）
- 文档：https://docs.qlever.dev
- pin：`0998359ab0a569a12eae22050c694b6aa46bdda4`
