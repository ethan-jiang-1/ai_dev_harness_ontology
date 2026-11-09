# Implementation：从全审到试点

> 全审解决“判断是否站得住”；这一阶段解决“试点能不能开跑、跑完能不能判”。

## 当前状态

- 全审 report：[条件 go（内部试点）/ 对外 no-go](../archive/2026-11/full-audit/report.md)。
- 3 个条件 go 试点：N&D K1 命名+单位、action-gate shadow、Ontology Catch checker。
- `experiments/` 目前只有 EXP-001/002/003 的旧设计，**没有这 3 个试点的可执行协议**。
- `deliverables/` 只有手册大纲，没有“怎么开跑”的 playbook。

## 入口

- 完整计划：[plan.md](./plan.md)
- 状态：`status.md`（Phase 0 建）
- 成本工作簿：`cost-model.md`（Phase 4 建）
- 试点 playbook：[deliverables/pilot-playbook.md](../../deliverables/pilot-playbook.md)（Phase 4 建）

## 原则

- 不扩论文；不新增判断；不编客户数字。
- 每个试点先写“什么结果会推翻什么”，再写设计。
- 实现产物在仓库外，实验编号回链；仓库只放协议与表单。
- 独立人类/客户数据仍缺；本阶段产出是“可开跑”，不是“已跑通”。
