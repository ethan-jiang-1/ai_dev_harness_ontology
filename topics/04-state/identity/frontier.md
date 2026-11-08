# 身份 · 未发现与下一步

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | alias vs registry vs semantic fallback 的分别贡献 | 决定投资哪一层 | 消融实验 | FIRME 后续 | 高 |
| G2 | false merge 检测/回滚 | 污染不可逆 | 审计轨迹 + 回滚机制 | 04 identity / commit-gate | 高 |
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

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| KROMA 线 | 跨源匹配复用 | 候选 | G5 |
| commit gate 实现 | 身份变更授权 | 概念 | G4 |
