---
status: draft
updated: 2026-11-13
---

# 协作与交接约定（Working Agreements）

> **本页管什么**：多 Agent / 跨会话改动本仓库时的并发隔离、交接与提交门禁。规则判据仍在 [CHARTER](../../CHARTER.md) 与 [AGENTS](../../AGENTS.md)。

## 1. 动手前：先看现场，不盲目重开

1. **先读 [state.md](../status/state.md#当前目标下一步做什么) 与 [meta/plans/](../plans/README.md)**：确认当前主线目标（A 轨/B 轨）、已知债务与唯一现行计划，不另立新计划或重开已标 `completed` 的历史项。
2. **检查未提交改动（WIP）**：执行 `git status -s`；如看到他人或上一轮的进行中修改，**不要覆盖或回滚**，先沿用现有方向或显式说明冲突。
3. **局部写、按派写**：改一个派只动该派目录（`README.md` / `claims.md` / `sources.md` / `frontier.md` / 子主题）；只改内容不顺手重排全局结构。

## 2. 跨层修改原则（判断顺流、证据逆流）

- **交付物被指错**：禁止只在 `deliverables/` 就地打补丁；必须走 [AGENTS 修复回路](../../AGENTS.md#修复回路交付物被指错时的常设路径) 先核上游 `digest.md` / `claims.md` / `conclusions.md`，再回写交付物。
- **改规则只改唯一出处**：字段/枚举改 [schema.md](../schema.md)；文体/接口改 [information-flow.md](../rules/information-flow.md)；交付物定位改对应 `SCOPE.md` 与 [scope.md](../deliverables/scope.md)。不把规则抄第二份到 README。

## 3. 提交前必须通过的门

1. 过一遍 [checklist.md](./checklist.md) 的人工语义项（宪章边界、黑名单/准入、干货五问、SCOPE 不越界）。
2. 跑只读自检：`python3 meta/tools/check_repo.py`，确保 **0 errors**（有新 warn 要能解释）。
3. 实质性改动同步更新：受影响文档的 `updated`（纯搬家/改链不刷 `updated`）、[state.md](../status/state.md) 的计数与「最后自检」、以及重大结构里程碑到 [state-log.md](../status/state-log.md)。
4. 计划收口：计划完成后立即将 `plan_status` 改为 `completed`（并移入 `meta/archive/<YYYY-MM>/plans/`），不把待办残留在 `meta/plans/`。
