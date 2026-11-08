# 跨轮记忆 · 未发现与下一步

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | 状态结构能否由本体自动生成 | 冷启动是硬约束 | 从数据/本体自动推导槽位与关系 | FIRME/EvoMemState 后续 | 高 |
| G2 | 冲突应阻塞还是带冲突推进 | 两种产品语义 | 对照实验 + 用户研究 | 记忆系统 | 高 |
| G3 | 记忆压缩与上下文压缩是否同题 | 可共用判据保护 | 统一形式化 | 00-harness/context | 中 |
| G4 | 衰减/强化参数能否按 entity/relation 学习 | 全局 α/γ/N 太粗 | 分层参数 + 数据 | FIRME §6 | 中 |
| G5 | false merge 检测/回滚 | 长期污染不可逆 | 审计轨迹 + 回滚机制 | 04 identity / commit-gate | 高 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变 | 成本 |
|---|---|---|---|---|
| N1 | 自动状态结构 | `ontology-guided memory state induction` | F1/F3 / G1 | 中 |
| N2 | 冲突推进语义 | `memory conflict blocking vs annotate` | F3 / G2 | 中 |
| N3 | false merge 回滚 | `entity resolution false merge rollback` | F2 / G5 | 高 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-08 | FIRME / EvoMemState 深读 | F1–F4 成形；G1–G5 明确 | 先做 G1/G5 |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| 自动状态结构 | 冷启动 | 待扫描 | N1 |
| false merge 回滚 | 污染不可逆 | 待扫描 | N3 |
