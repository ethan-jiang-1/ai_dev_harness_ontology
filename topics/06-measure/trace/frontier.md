# 过程有效性 · 未发现与下一步

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | 闭源模型的 SLB | 大多数部署用闭源 API，无完整 trace | 可观测接口/代理 trace | API 供应商 | 高 |
| G2 | 定理证明/优化是否同样 | 任务类型有限 | 扩展 benchmark | 形式化任务 | 中 |
| G3 | Placeholders 的适用边界 | 值与结构不可分时失效 | 交互式规划实验 | SLB 后续 | 高 |
| G4 | Batching 损失能否避免 | 批处理是常见成本优化 | 批内隔离/独立上下文 | 工程实验 | 中 |
| G5 | 训练模型不 SLB | 外部约束不是唯一解 | 训练目标/数据 | 训练侧 | 低 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变 | 成本 |
|---|---|---|---|---|
| N1 | 闭源 trace | `closed model reasoning trace solver behavior` | F1 / G1 | 高 |
| N2 | placeholders 边界 | `placeholder value structure separation planning` | F4 / G3 | 中 |
| N3 | 训练侧 | `train model not precompute solver` | F3 / G5 | 高 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-08 | SLB 深读 + G-X 修复 | F1–F8 成形；G1–G5 明确；吸收 codebook/buy/低延迟边界 | 先做 G1/G3；E-07 成本条件待 digest 修正 |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| 闭源 trace 代理 | 部署可见性 | 待扫描 | N1 |
| 交互式 placeholder | 推广边界 | 待扫描 | N2 |
