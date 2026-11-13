---
status: draft
updated: 2026-11-13
---

# _workpapers：交付物工作底稿

> **边界判据（[ADR 0016](../../adr/0016-unify-meta-structure.md)）**：这里放**没有 `plan_status` 的交付物评估底稿**（冷读记录、质量评分、内容审计、精读报告、缺口盘点、接线报告）。它们可以引用 `src/` 与 `topics/`，但不构成 `E`、不新增规则、不进对外阅读路径。
>
> 有 `plan_status`、需要推进的计划放 [meta/plans/](../../meta/plans/README.md)；已执行完毕的历史计划已归档至 [meta/archive/2026-11/plans/](../../meta/archive/2026-11/README.md#2026-11-已归档计划)。常设规则在 [AGENTS](../../AGENTS.md) / [CHARTER](../../CHARTER.md)。

| 文件 | 对应交付物 | 说明 | 性质 |
|---|---|---|---|
| [2026-11-12-content-gap-survey.md](./2026-11-12-content-gap-survey.md) | 全仓 | **内容缺口盘点**：purge 后证据基座、按派缺口、横切缺口、优先级行动清单 | 参考（缺口盘点） |
| [2026-11-12-05-quality-review.md](./2026-11-12-05-quality-review.md) | 10（原 05） | **10 落地现状质量评估（rubric v1.2）** | 参考（评分） |
| [2026-11-11-adr-0011-handoff-to-01.md](./2026-11-11-adr-0011-handoff-to-01.md) | 01 | **跨会话交接**：ADR 0011 生效；K0–K4 按论文实验条件标注 | 日志（已回执） |
| [2026-11-11-cold-read.md](./2026-11-11-cold-read.md) | 01 / START | **代理冷读（第 9 步）**：第一轮 68 → 第二轮 86；真人冷读未做 | 参考（冷读） |
| [2026-11-11-command-board.md](./2026-11-11-command-board.md) | 全仓 | 逐批进度日志：P0–P4 每批改了什么、`check_repo` 结果 | 日志 |
| [2026-11-11-content-audit.md](./2026-11-11-content-audit.md) | 01/02/03 | **内容审计**：硬句/锐句/水句密度；三个税与门口悖论 | 参考（审计） |
| [2026-11-11-content-read.md](./2026-11-11-content-read.md) | 01–04 | **精读报告**：逐页读 41 万字符，判词与证据行号 | 参考（精读） |
| [2026-11-11-content-repair.md](./2026-11-11-content-repair.md) | 01–04 | **内容修复（P0–P2）**：四张 W 表、gap 处补自测协议、03 换叙事 | 参考（修复） |
| [2026-11-11-exp-004-citation-audit.md](./2026-11-11-exp-004-citation-audit.md) | 02 R4 | **EXP-004**：20 条 claim+E 行引文正确性审计 | 历史（审计） |
| [2026-11-11-k-ladder-provenance.md](./2026-11-11-k-ladder-provenance.md) | 01 | **K0–K4 来源核查**：论文条件 vs 行业标准与修正 | 参考（术语核查） |
| [2026-11-11-quality-review.md](./2026-11-11-quality-review.md) | 01–04 | **质量评估（rubric v1.1）**：基线/整改/复评/§12.4 独立评分（01=77 / 02=77 / 03=73） | 参考（评分） |
| [2026-11-11-scan-report.md](./2026-11-11-scan-report.md) | 01–04 | **旧噪声扫描**：撤回 E/旧效应量/借权威/旧计数扫描与干净门 | 参考（扫描） |
| [2026-11-11-score-after-repair.md](./2026-11-11-score-after-repair.md) | 01–04 | **评分（补偿后）**：门槛全过；desk 87/86/83/88 与 §11–§12.3 对比 | 参考（评分） |
| [2026-11-11-status.md](./2026-11-11-status.md) | 01–04 + 术语 | 一页状态快照（2026-11-11）；**现行计数以 [meta/state](../../meta/status/state.md) 为准** | 参考（快照） |
| [2026-11-11-trunk-wiring.md](./2026-11-11-trunk-wiring.md) | 01–04 | **接线报告（第 7 步）**：定义句 `（N: 标准名）`/`（local）` 逐页记录 | 参考（接线） |
| [2026-11-10-gap-assessment-report.md](./2026-11-10-gap-assessment-report.md) | 01/02/03 | **差距评估结果**：27 格评估与三种缺口 | 历史（评估） |
| [2026-11-10-stage-review.md](./2026-11-10-stage-review.md) | 全仓 | **阶段盘点（2026-11-10）**：四层水位与阶段复盘 | 历史（盘点） |

**维护**：新产生的质量评估/冷读/内容审计报告继续落本目录（`YYYY-MM-DD-<slug>.md`），不加 `plan_status`；只读参考，不在本目录另立规则或待办。
