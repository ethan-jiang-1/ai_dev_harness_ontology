# 持久化前 · 未发现与下一步

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | 授权判据由谁执行 | 本体/独立判定器/硬编码流程，可维护性不同 | 三种实现对照 | 01/02/05 | 高 |
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

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| 实现版 commit gate | 从概念到 false-defer | 待扫描 | N1 |
| 冲突降级语义 | 域差异 | 待扫描 | N2 |
