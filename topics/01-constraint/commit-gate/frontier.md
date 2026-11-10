# 持久化前 · 未发现与下一步

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | 授权判据由谁执行 | 本体/独立判定器/硬编码流程，可维护性不同；**读路径有三个执行点（post-filter/rewrite/scan），写路径仍空** | 三种实现对照（读/写/审批） | 01/02/05 | 高 |
| G2 | 冲突清 vs 冲突已标注的降级条件 | 医疗/金融语义不同 | 域策略 + 用户研究 | 域案例 | 高 |
| G3 | 被阻塞变更如何重新进入 | 待定队列不可见会被静默丢弃 | 队列/重入协议 | 工程实现 | 中 |
| G4 | false-defer 率 | 正确变更被 UNKNOWN 拦住 | 在 FIRME 写入上标注 | commit-gate + identity | 高 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变 | 成本 |
|---|---|---|---|---|
| N1 | 实现/实证 | `commit boundary implementation entity resolution` | F4 / G4 | 高 |
| N2 | 冲突降级语义 | `conflict resolution commit gate annotation` | F2 / G2 | 中 |
| N3 | 重入协议 | `deferred mutation queue re-entry` | F2 / G3 | 中 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-08 | Commit Boundary 深读 | F1–F4 成形；G1–G4 明确 | 先做 G4 |
| 2026-11-09 | trustgraph（读路径策略过滤） | G1 读侧有答案；F5 入档；写路径仍空 | 补 fail-open/对象方向 |
| 2026-11-11 | sparql-guard / holosdb（EXP-001） | 第二/第三执行点成形；sparql-guard 76/76 tests 复跑通过；仍无泄漏率 | F8 入档；不建卡，等评测 |
| 2026-11-11 | sparql-guard 10 用例（EXP-002） | 7 pass、1 alias leak、0 false-block；trustgraph/holosdb 未跑同协议 | 协议可执行；下一步补两列 |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| 实现版 commit gate | 从概念到 false-defer | 待扫描 | N1 |
| trustgraph 读路径策略引擎 | 授权判据的独立执行者；不是 commit gate | 已核（代码） | 验证 fail-open 与对象方向 |
| 冲突降级语义 | 域差异 | 待扫描 | N2 |
| [Matdata-eu/sparql-guard](https://github.com/Matdata-eu/sparql-guard) | 第二 read-path 执行点（rewrite）：fail-closed、subject+object、**76/76 tests 复跑通过（EXP-001）**；**10 用例实跑 7 pass、1 alias leak、0 false-block（EXP-002）**；仍单作者/1★/3 周/无独立采纳 | 候选（未入库） | 不建卡；等独立评测或采纳 |
| [pwin/triplestore](https://github.com/pwin/triplestore) | 第三 read-path 执行点（scan）：predicate/graph 级、默认 deny、fail-closed；`holos-engine/src/view.rs` 有调用点；20 security tests（未复跑）；无 Subject/Object scope | 候选（未入库） | 只作执行点对照，不进 01/02 主证据 |
