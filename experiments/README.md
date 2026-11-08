---
status: draft
updated: 2026-11-08
---

# experiments：验证（index）

流水线的旁路。这里只放**实验设计/协议**，实现产物在仓库外，靠实验编号回链（见 [ADR 0001](../adr/0001-research-repo-over-code.md)）。

## 为什么需要

目前全仓库最强的结论等级是「已核原文摘要」——**没有一个结论是独立复现的**。所有判断都继承他人的实验条件，我们无法确认这些条件是否是我们的条件。

## 实验清单

| 编号 | 要回答什么 | 状态 | 会改变 | 文件 |
|---|---|---|---|---|
| EXP-001 | 同一 harness 下，结构化工件有没有用 | 设计中 | E-01 / E-08 | [EXP-001](./EXP-001-structured-artifacts.md) |
| EXP-002 | 判定器的漏检/误报曲线，而非单一 accuracy | 未开始 | E-02 | [EXP-002](./EXP-002-checker-fp-fn.md) |
| EXP-003 | 同一本体放在不同接缝（上下文/判定/授权）的差异 | 未开始 | E-04 / C-03 | [EXP-003](./EXP-003-seam-position.md) |
| EXP-004 | 只做 K1 命名+单位，能否解决 primary trap | 设计中 | E-12 / 03-L1 | [EXP-004](./EXP-004-narrow-deep-k1.md) |
| EXP-005 | 可逆性路由 shadow 的 false-veto 能否 ≤5% | 设计中 | E-15 / E-04 | [EXP-005](./EXP-005-action-gate-shadow.md) |
| EXP-006 | data-derived checker 能否在空结果重试上提供增量 catch | 设计中 | E-02 | [EXP-006](./EXP-006-ontology-checker.md) |

## 状态

| 状态 | 含义 |
|---|---|
| 未开始 | 只有问题，没有协议 |
| 设计中 | 有协议草稿，未冻结 |
| 运行中 | 协议冻结，正在跑 |
| 已完成 | 有结果/失败记录，已回链结论 |
| 已放弃 | 写清为什么不做 |

## 怎么加一个实验

1. 复制 [_template.md](./_template.md)（通用）或 [_pilot-template.md](./_pilot-template.md)（2 周试点）。
2. 先写「会推翻什么」和 go/no-go；写不出就不做。
3. 写清主指标/过程指标/非对称代价/分母；稀疏事件给最低样本。
4. 在本页表格加一行；实现产物只写“仓库外 + 编号”，不放进仓库。
5. 实验失败也登记：失败原因本身就是结论。

## 纪律

- 实验失败照样登记，写清失败原因。
- 每个实验必须预先写明「哪种结果会推翻哪条假设」；没写就别做。
- 实现产物在仓库外，编号与本文档一致；产物丢失时，对应结论降级。
- 交付物不得引用未跑的实验当“已验证”；只能引 `topics/` 的 E/L。

## 相关

- 试点就绪计划：[meta/implementation/plan.md](../meta/implementation/plan.md)
- 试点状态：[meta/implementation/status.md](../meta/implementation/status.md)
