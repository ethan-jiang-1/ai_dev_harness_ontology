---
id: EXP-003
status: draft
experiment_status: 未开始
updated: 2026-11-08
rq: [RQ2, RQ3]
targets: [E-04, C-03]
artifact: pending（实现产物在仓库外）
---

# EXP-003 · 接缝位置对照

## 要回答什么

同一份本体放在不同时刻（上下文 / 判定 / 授权），行为差异有多大？

## 会推翻什么

| 若结果为 A | 则 |
|---|---|
| 拦截率不随位置后移上升 | “强度/覆盖反向”被削弱 |
| 覆盖率不降 | 该假设被推翻 |
| 拦截率上升且覆盖率下降 | 支持 C-03：按机制类型选度量，不用单一准确率 |

## 设计

- **变量**：同一本体三种投放位置（上下文 / 判定 / 授权）。
- **对照**：同任务、同模型、同本体；只换位置。
- **被控住的混淆项**：本体内容、任务集、模型、预算；重复运行测收敛（RQ3）。
- **度量**：主指标 = 不可逆错误拦截率；过程指标 = 覆盖率、false-veto、审批/千次；不用准确率替代。
- **分母/口径**：按决策/轨迹；拦截率与覆盖率分开报。

## 状态与阻塞

- `experiment_status: 未开始`
- 阻塞：需要一个可控的投放位置实验台；授权位置要有写路径/回滚。

## 回链

- 结论：[E-04、C-03](../topics/conclusions.md)
- 主题：[01/action-gate](../topics/01-constraint/action-gate/README.md) · [02/checker](../topics/02-judgment/checker/README.md)
- 相关 digest：[POLAR](../src/papers/2610.08082-polar/digest.md) · [CASEL](../src/papers/2610.36570-casel/digest.md)
