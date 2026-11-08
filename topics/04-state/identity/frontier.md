# 身份 · 未发现与下一步

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | alias vs registry vs semantic fallback 的分别贡献 | 决定投资哪一层 | 消融实验 | FIRME 后续 | 高 |
| G2 | false merge 检测/回滚 | 污染传播幅度未测、无自动回滚（机制推断） | 审计轨迹 + 回滚机制 + 传播测量 + 域内 merge-precision 基线（论文 85.6–97.5% 跨 4 settings，90% 停线不是通用阈值） | 04 identity / commit-gate | 高 |
| G3 | 身份置信度怎么表达 | 低置信时合并/挂起/双写 | 置信度校准 + 产品语义 | 生产 trace | 中 |
| G4 | commit gate 的 false-defer 率 | 正确变更被 UNKNOWN 拦住 | 在 FIRME 写入上标注 | commit-gate | 中 |
| G5 | 跨源本体匹配复用 | 降低成本 | KROMA 线 + 本体匹配 | 05 refinement | 低 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变 | 成本 |
|---|---|---|---|---|
| N1 | alias/registry 消融 | `alias memory entity resolution ablation` | F2 / G1 | 中 |
| N2 | false merge 回滚 | `entity resolution false merge rollback` | F3 / G2 | 高 |
| N3 | 身份置信度 | `entity resolution confidence calibration` | F1 / G3 | 中 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-08 | FIRME + Commit Boundary 深读 | F1–F4 成形；G1–G5 明确 | 先做 G1/G2 |
| 2026-11-08 | G-X 反向核对（对照两篇 digest） | 修正「alias 是主增量」「false merge 长期污染」「CMR 奖励少匹配」；补写侧字段与冷启动 | alias 增量标条件、污染降为 `推测`；G1/G2 仍是高优先 |
| 2026-11-08 | T-10 二级残留复核（04-L5 / 90% 停线 / period 口径 / Commit 失败表） | 04-L5 降为 `推测`；`merge precision <90%` 停线改标预登记；10 个月度 period 与 S&P 3 个 reporting period 拆开；补 Commit 失败模式表 | G1/G2 仍开；停线要在目标域重标 |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| KROMA 线 | 跨源匹配复用 | 候选 | G5 |
| commit gate 实现 | 身份变更授权 | 概念 | G4 |
