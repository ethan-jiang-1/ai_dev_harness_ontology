---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# 03 主体：六张位置卡 + 四张横切页

> 本页只做索引；每张卡回答「这个位置怎么跑、能改变什么、拦不住什么、证据到哪」。

| 卡 | 回答 | 入口 |
|---|---|---|
| context | 模型看到什么；供给/投影/编译 | [positions/context.md](01-context.md) |
| memory | 下一轮记得什么；registry/状态 | [positions/memory.md](02-memory.md) |
| evidence | 产出带什么依据；grounding | [positions/evidence.md](03-evidence.md) |
| checker | 产出对不对；三态/漏检/误报 | [positions/checker.md](04-checker.md) |
| action | 动作能不能做；可逆性/审批 | [positions/action.md](05-action.md) |
| commit | 证据够不够授权；设计/无实现 | [positions/commit.md](06-commit.md) |
| outside | 轴外位置：read-path / supply / reasoning / training | [positions/outside.md](07-outside.md) |

**横切页**：

- [measurement](../04-across-positions/03-measurement.md)：每个位置该量什么、不能量什么。
- [coverage](../04-across-positions/01-coverage.md)：七类失效 × 八位置的矩阵；组织假设，不是测量。
- [execution-forms](../04-across-positions/02-execution-forms.md)：执行链与四种 `engine` 语义。
- [boundaries](../05-evidence/02-boundaries.md)：15 条边界 + 12 条反例；[evidence-ledger](../05-evidence/01-ledger.md)：E-xx 台账；[gaps](../05-evidence/03-gaps.md)：下一步。
