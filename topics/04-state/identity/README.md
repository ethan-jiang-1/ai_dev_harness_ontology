---
status: draft
updated: 2026-11-08
rq: [RQ3]
evidence: [E-05]
---

# 身份：跨源、跨期的同一性

> 记忆系统最先坏的地方往往不是「忘了」，而是「认错了」。这里问「怎么把实体钉住、什么时候有权改」，不负责内容记忆（[memory](../memory/README.md)）。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 4 条（[findings](./findings.md)） |
| 未发现 / 开放 | 5 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 跨源/跨期身份对齐与身份变更授权；不含记忆内容/衰减（memory） |

## 当前判断

- **registry 锚定是当前最可复用的做法。** 固定 product–topic 本体 + 规范身份/持久别名；重复观察定向到同一段历史。`已核`
- **alias memory 是主要增量。** final-period CMR +7.8–12.1 pp；human-audit reattachment recall +22.5–29.0 pp；semantic matching token −40.3%。`已核`
- **身份变更本身是 commit 问题。** 可推理的证据 ≠ 可授权 merge/split；需要 claim-specific promotion、冲突解决、scope/version 检查。`推测`（Commit Boundary 是概念架构，无实现）

## 文件地图

| 想知道 | 去 |
|---|---|
| registry/时序图/commit gate/失效 | [mechanism](./mechanism.md) |
| 四条判断的证据/数字 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始论文 | [FIRME digest](../../../src/papers/2610.40482-firme/digest.md) · [Commit Boundary digest](../../../src/papers/2610.37407-commit-boundary/digest.md) |

## 边界

- **不解决记忆内容。** 身份是前置；内容/衰减/冲突由 [memory](../memory/README.md) 管。
- **不保证合并正确。** merge precision 不等于 CMR；false merge 会长期污染。
- **APEX-MEM 仅摘要级**，数字 `待核`。

## 关联

- 派：[04 状态](../README.md) · 结论：[E-05](../../conclusions.md)
- 相邻：[memory](../memory/README.md) · [commit-gate](../../01-constraint/commit-gate/README.md)
- 生产：[05 refinement](../../05-produce/refinement/README.md)
