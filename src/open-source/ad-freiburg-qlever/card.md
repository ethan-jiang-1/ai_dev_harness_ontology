---
status: draft
source_type: open-source
reading: 已读代码
provenance: 一手代码
updated: 2026-11-09
repo: ad-freiburg/qlever
url: https://github.com/ad-freiburg/qlever
commit: 0998359ab0a569a12eae22050c694b6aa46bdda4
release:
license: Apache-2.0
scan_date: 2026-11-09
stars_at_scan: 940
last_push: 2026-11-09
ontology_role: none
seam: none
execution_form: none
evidence_role: mechanism-only
home: topics/03-knowledge
subtopic: querying
also_supports: []
updates:
  - topics/03-knowledge/querying/README.md
  - topics/03-knowledge/claims.md
  - topics/03-knowledge/sources.md
---

# ad-freiburg/qlever · 来源卡

> 来源卡：只记可定位的事实。调用链与「执行还是装饰」的定级在同目录 [digest.md](./digest.md)。

## 一句话

高性能 RDF/SPARQL 引擎：完整 SPARQL 1.1、单机可查千亿级 triples；**不做 OWL 推理、不做策略**，但能把 04 B.3 的“生成 → 执行 → 验证”里的执行层做成可部署的运行时（NLKGQ/挑战赛都用它）。

## 本体在哪

- **没有 OWL/SHACL 推理**。它加载 RDF triples、建索引、执行 SPARQL；ontology 只能作为普通 triples 存进去，不会被 entailment/约束求值。
- `ontology_role: none`：它是查询运行时 adjunct，不是本体引擎。
- 对 04 的用法：把生成的 SPARQL 交给它执行；空结果/错误/延迟从它这里拿；不要指望它校验本体或策略。

## 调用链（文件:符号）

| 步 | 位置 | 做什么 |
|---|---|---|
| 建索引 | `src/index/IndexBuilderMain.cpp`、`src/index/Index.cpp` | 加载 RDF、建 permutation/统计 |
| 启动 | `src/ServerMain.cpp` → `src/engine/Server.cpp` | HTTP 服务/endpoint |
| 解析 | `src/parser/SparqlParser.cpp` | SPARQL 1.1 解析 |
| 规划 | `src/engine/QueryPlanner.cpp` | 选 join 顺序/算子 |
| 执行 | `src/engine/QueryExecutionTree.cpp` | 算子树求值 |
| 结果 | `src/engine/ExportQueryExecutionTrees.cpp` | JSON/CSV/TSV 等 |
| 更新 | `src/engine/ExecuteUpdate.cpp` | SPARQL Update |
| 嵌入 | `src/libqlever/` | 进程内使用 |

## 接缝判定

| 问题 | 回答 | 证据 |
|---|---|---|
| 有外部判据（判据来自本体） | 否（只按 SPARQL 查 triples） | `src/parser/`、`src/engine/` |
| 有阻断能力 | 否（执行查询；不拦动作/不拒输出） | `src/engine/Server.cpp` |
| 位置明确 | 否（B.3 的执行层，不是本体接缝） | 本文 §6 |
| 失败处理 | 返回 SPARQL 错误/空结果；分类在调用方 | `src/engine/` |

## 维护与采用

- 940★；最后 push 2026-11-09；commit `0998359`；Apache-2.0；活跃开发；有 Docker/原生包。
- 被 Text2SPARQL/QLever demos、QRAKEN 等使用（论文侧证据，不是本仓库实测）。
- 只读代码，未在本仓库跑 Qlever；`reading: 已读代码`，`quality: B`。

## 原文

- Repo：https://github.com/ad-freiburg/qlever
- 文档：https://docs.qlever.dev
- pin commit：`0998359ab0a569a12eae22050c694b6aa46bdda4`
