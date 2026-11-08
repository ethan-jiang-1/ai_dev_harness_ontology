---
id: EXP-001
status: draft
experiment_status: 设计中
updated: 2026-11-08
rq: [RQ1, RQ5]
targets: [E-01, E-08]
artifact: pending（实现产物在仓库外）
---

# EXP-001 · 结构化工件到底有没有用

## 要回答什么

在**同一个 harness** 下，加与不加结构化工件，差异在哪里？

## 会推翻什么

| 若结果为 A | 则 |
|---|---|
| 准确率显著改善 | E-01 必须限定范围（“强 harness 下无增益”不成立） |
| 过程指标也无改善 | 编译派的预算论证失效（E-08/E-12 的成本前提被削弱） |
| 准确率无差异、过程指标显著改善 | 支持 E-01 的“价值在过程/部署层”，但仍不能说准确率有用 |

## 设计

- **变量**：工件有无；工件形式（claim–leaf / 树 / 图 / wiki）。
- **对照**：同 harness、同模型、同任务；只变工件。
- **被控住的混淆项**：上下文预算（必须作为协变量，否则分不清“工件有用”与“工件省预算”）；模型版本；任务集；judge。
- **度量**：主指标 = 任务准确率；过程指标 = token 总量、检索轮次、重复查询率；成本 = 每问 token/时延。
- **分母/口径**：按问；token 按每问总量；不要只报平均。

## 状态与阻塞

- `experiment_status: 设计中`
- 阻塞：需要一个可复现的检索 harness；工件生成器与评测集未定。

## 回链

- 结论：[E-01、E-08](../topics/conclusions.md)
- 主题：[03/compilation](../topics/03-knowledge/compilation/README.md) · [03/projection](../topics/03-knowledge/projection/README.md)
- 相关 digest：[CAI](../src/papers/2610.41172-context-as-infrastructure/digest.md) · [N&D](../src/papers/2610.11768-narrow-and-deep/digest.md)
