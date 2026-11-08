---
status: seed
updated: 2026-11-08
rq: [RQ2, RQ4]
evidence: [E-05]
---

# 持久化前：推理证据 ≠ 授权证据

> 变更即将落盘或写入外部系统的那一刻。前面都是「推理」，这里是唯一「改变世界」的时刻；这里问「什么证据才有权推动持久化」。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 4 条（[findings](./findings.md)） |
| 未发现 / 开放 | 4 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 落盘前的授权契约；不含动作前（action-gate）与推理期（reasoning-gate） |

## 当前判断

- **推理证据 ≠ 授权证据。** 能支持假设，不等于有权推动持久化变更；`UNVERIFIED` 可进 Planner，但不能当 positive authorization support。`已核`（概念架构）
- **提交条件要显式化。** 证据齐、冲突清、版本有效，三条全过才 commit；不是交给模型自觉。`已核`（设计规范）
- **同源检索不是独立确认。** hypothesis 诱导的多个结果不能互相印证；「没检测到冲突」也不是 positive support。`已核`（概念）
- **只有设计，没有实现。** Commit Boundary 自述无实现、无实证；保证是条件性的，只能作设计提案。`已核`

## 文件地图

| 想知道 | 去 |
|---|---|
| 三条件/状态机/promotion/失效 | [mechanism](./mechanism.md) |
| 四条判断的证据/边界 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始论文 | [Commit Boundary digest](../../../src/papers/2610.37407-commit-boundary/digest.md) |

## 边界

- **不是动作前拦截。** 它管落盘/持久化，不管工具调用是否执行。
- **不是已验证效果。** 无实现、无 false-defer 率；引用时必须标「概念架构」。
- **不控制上游检索。** hypothesis-conditioned retrieval 不在架构内；dependency-aware lineage 是 future work。

## 关联

- 派：[01 约束](../README.md) · 结论：[E-05](../../conclusions.md)
- 相邻：[action-gate](../action-gate/README.md) · [reasoning-gate](../reasoning-gate/README.md)
- 记忆写入：[04 memory](../../04-state/memory/README.md) · [identity](../../04-state/identity/README.md)
