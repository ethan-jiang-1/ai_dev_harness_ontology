---
status: draft
updated: 2026-11-13
---

# plans：推进计划（现行唯一）

> **边界判据（[ADR 0016](../../adr/0016-unify-meta-structure.md)）**：有 `plan_status`、有目标与验收条件、需要推进的计划放这里；没有状态机的评估报告、冷读记录、缺口盘点、评分结果放 [deliverables/_workpapers/](../../deliverables/_workpapers/README.md)。计划不构成判断（判断进 `topics/`），不进对外阅读路径。

## 规则

1. **现行至多一份**：全仓同时只能有一份 `plan_status: active` 的计划（由 [check_repo.py](../tools/check_repo.py) 强校验）。开新计划前，先把旧计划收口为 `completed` 或 `abandoned`。
2. **完成后进冷库**：状态变为 `completed` / `abandoned` 后，在收口批次将其移入 [meta/archive/YYYY-MM/plans/](../archive/2026-11/README.md)，不在本目录堆满历史计划。
3. **不另立“现在该做什么”**：全局优先级看 [state.md](../status/state.md#当前目标下一步做什么)，常设规则看 [AGENTS](../../AGENTS.md) 与 [CHARTER](../../CHARTER.md)，不在计划正文里新增常设规则。

## 命名与必填字段

文件名：`YYYY-MM-DD-<slug>.md`

| 字段 | 取值 | 说明 |
|---|---|---|
| `plan_status` | `active` / `completed` / `abandoned` | 计划专用状态；**不要用文档 `status`** |
| `updated` | `YYYY-MM-DD` | 最后一次实质修订 |
| `scope` | 短标签 | 覆盖范围 |

## 当前计划

| 计划 | 状态 | 范围 | 说明 |
|---|---|---|---|
| [2026-11-12-deliverable-ia-plan](./2026-11-12-deliverable-ia-plan.md) | `active` | deliverables 01–04 | IA 整改（01 已落地，02–03 对齐待续；对应 `state.md` B 轨 #3） |

> 2026-11-09 至 2026-11-12 已完成的 22 份历史计划已归档至 [archive/2026-11/plans/](../archive/2026-11/README.md#2026-11-已归档计划)。
