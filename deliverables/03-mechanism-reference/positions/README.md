---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# 03 主体：六张位置卡 + 三张横切页

> 本页只做索引；每张卡回答「这个位置怎么跑、能改变什么、拦不住什么、证据到哪」。

| 卡 | 回答 | 入口 |
|---|---|---|
| context | 模型看到什么；供给/投影/编译 | [positions/context.md](context.md) |
| memory | 下一轮记得什么；registry/状态 | [positions/memory.md](memory.md) |
| evidence | 产出带什么依据；grounding | [positions/evidence.md](evidence.md) |
| checker | 产出对不对；三态/漏检/误报 | [positions/checker.md](checker.md) |
| action | 动作能不能做；可逆性/审批 | [positions/action.md](action.md) |
| commit | 证据够不够授权；设计/无实现 | [positions/commit.md](commit.md) |
| outside | 轴外位置：read-path / supply / reasoning / training | [positions/outside.md](outside.md) |

**横切页**：

- [measurement](../across-positions/measurement.md)：每个位置该量什么、不能量什么。
- [coverage](../across-positions/coverage.md)：七类失效 × 八位置的矩阵；组织假设，不是测量。
- [execution-forms](../across-positions/execution-forms.md)：执行链与四种 `engine` 语义。
- [boundaries](../evidence/boundaries.md)：15 条边界；[evidence-ledger](../evidence/ledger.md)：E-xx 台账；[gaps](../evidence/gaps.md)：下一步。
