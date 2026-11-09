# 查询 · 未发现与下一步

> `G` = gap（还没站住的判断）；`N` = next（下一步看什么）。稳定判断回 [findings](./findings.md)。
> **论文线已冻结**：本页只记录缺口，不再新找论文；新证据优先来自活跃 OSS 的代码/实测。

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | 跨域 / 多 KG 复现 | 三条路线各一个设置，没有独立复现；不能判断哪条是默认路线 | 同一 benchmark/同一骨干上换域、换 KG、换 snapshot 的对照 | 03/querying 三篇的后续；活跃 OSS 的示例图 | 高 |
| G2 | 空结果/失败分布 | GGC 没有空结果机制、没有测量；NLKGQ 依赖 snapshot/endpoint；KGVoyager 用执行反馈 refine，但没有分因 | 把空结果拆成 coverage/query/data 三分因，报分布与处置 | query 日志；OSS 运行时（Qlever/Oxigraph）的错误分类 | 高 |
| G3 | GGC 的净收益 | 没有 2×2 改对/改坏配对，只有子集级 + 单例；“选择性纠错”的净收益未被隔离 | 同轨迹配对：改前对/错 × 改后对/错 + 成本 | 复现 GGC；或换一个 gate 做对照 | 高 |
| G4 | ontology-in-context vs ontology-free | NLKGQ（完整 OWL）与 KGVoyager（无 ontology、只要 class index）没有头对头；谁是默认路线未测 | 同数据/同骨干/同预算的 A/B；加“ontology 大小/质量”变量 | 两篇的后续；OSS 查询运行时 | 高 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变哪条 F/G | 成本 |
|---|---|---|---|---|
| N1 | 三条路线的头对头 | 同 benchmark（如 DBLP-QuAD/GraphQuestions）+ 同骨干；NLKGQ vs KGVoyager vs GGC | F1/F2/F3、G4 | 高 |
| N2 | 空结果分因 | 在 Qlever/Oxigraph 上跑一批查询，按 coverage/query/data 分类；对照 GGC Gate | F1、G2 | 中 |
| N3 | 大本体/context 边界 | NLKGQ 的 ontology 规模 sweep；KGVoyager 的 class index 在更大图上的可行性 | F2/F3、G1 | 中 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-09 | GGC + NLKGQ + KGVoyager 定稿 | 三条路线、各自单 benchmark；无头对头 | 3 F / 4 G / 3 N；论文线冻结 |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| Qlever（OSS 运行时） | 三条路线最终都要在执行层落地；Qlever 是 NLKGQ/挑战赛常用运行时 | 已入档（adjunct） | 核 active/last_push；code-map；与空结果分因对照 |
| Oxigraph（OSS 运行时） | 轻量 SPARQL store，适合做本地复现 | 候选 | 与 Qlever 比部署/延迟 |
| GGC 的 Gate 替代实现 | 检验“选择性”是否依赖监督分布 | 候选 | 用 OSS 分类器/规则做对照 |

> 不再新找论文；候选只从活跃 OSS / 工程讨论里来。
