---
status: draft
updated: 2026-11-13
---

# 2026-11 归档

> 2026-11-07～12 的已完成计划、审计与全审快照。**不要当现行规则读**；现行规则见 [meta 索引](../../README.md)，当前状态见 [state](../../status/state.md)，现行计划见 [meta/plans](../../plans/README.md)。

## 2026-11 早期审计与全审（11-07～11-09）

| 文件/目录 | 当时是什么 | 为什么归档 |
|---|---|---|
| [digestion-plan.md](./digestion-plan.md) | 22 篇从摘要级到工程判断的消化计划 | 已完成，结论进 digest/topics |
| [digestion-report.md](./digestion-report.md) | 消化验收报告（2026-11-07） | 一次性验收 |
| [quality-plan.md](./quality-plan.md) / [quality-report.md](./quality-report.md) | 质量推进计划与报告 | 已完成，后续由 full-audit 接替 |
| [card-audit.md](./card-audit.md) / [digest-audit.md](./digest-audit.md) / [digest-polish-audit.md](./digest-polish-audit.md) | 来源卡/digest 审计 | 快照，行数与计数已过时 |
| [critic-sample.md](./critic-sample.md) | 独立 critic 抽样 | 一次性抽样 |
| [full-audit/](./full-audit/README.md) | 全审（E0–E4 / A0–A4 / V0–V3）与条件 go/no-go | 已出报告；D0 阻塞已关闭 |
| [ontology-llm-landscape.md](./ontology-llm-landscape.md) | 外部「本体 × LLM 应用」问题扫描（2026-11） | 工作底稿；未入 topics，不构成 E |
| [04-upstream-gaps.md](./04-upstream-gaps.md) | 04 的 topics/src 支撑矩阵与 intake 优先级 | 工作底稿；04 已退役（ADR 0015） |

<a id="2026-11-已归档计划"></a>
## 2026-11 已归档计划（`plans/`，原 `deliverables/_plans/`）

> 按 [ADR 0016](../../../adr/0016-unify-meta-structure.md) 迁入；以下计划均已执行完毕或作历史留痕，不指导新的写入。

| 文件 | 原目标 | 状态 |
|---|---|---|
| [01-capability-status.md](./plans/01-capability-status.md) | 01 现状 D1 证据回抽（E1–E9 规格/H1–H6） | 历史 |
| [04-worked-example.md](./plans/04-worked-example.md) | 原 04 支撑计划（04 已按 ADR 0015 退役） | 历史 |
| [2026-11-09-hard-objects-plan.md](./plans/2026-11-09-hard-objects-plan.md) | 硬对象产线（O-xx） | 已执行 |
| [2026-11-09-reverse-gap-plan.md](./plans/2026-11-09-reverse-gap-plan.md) | 逆向补齐（方法已升为常设修复回路） | 历史 |
| [2026-11-10-04-content-supply.md](./plans/2026-11-10-04-content-supply.md) | 原 04 内容供给（W0–W3） | 已执行 |
| [2026-11-10-04-deep-plan.md](./plans/2026-11-10-04-deep-plan.md) | 原 04 深挖计划 | 已执行 |
| [2026-11-10-04-matrix-skeletons.md](./plans/2026-11-10-04-matrix-skeletons.md) | 原 04 W0 矩阵骨架 | 已执行 |
| [2026-11-10-04-remediation-plan.md](./plans/2026-11-10-04-remediation-plan.md) | 原 04 内容整改 | 已执行 |
| [2026-11-10-gap-assessment.md](./plans/2026-11-10-gap-assessment.md) | 01/02/03 差距评估计划 | 历史 |
| [2026-11-10-wiring-plan.md](./plans/2026-11-10-wiring-plan.md) | O-xx 接线计划 | 已执行 |
| [2026-11-11-01-lift-plan.md](./plans/2026-11-11-01-lift-plan.md) | 01 分计划提拉 | 已执行 |
| [2026-11-11-02-lift-plan.md](./plans/2026-11-11-02-lift-plan.md) | 02 分计划提拉 | 已执行 |
| [2026-11-11-03-lift-plan.md](./plans/2026-11-11-03-lift-plan.md) | 03 分计划提拉 | 已执行 |
| [2026-11-11-baseline-correction-plan.md](./plans/2026-11-11-baseline-correction-plan.md) | ADR 0011 术语基线整改 | 已执行 |
| [2026-11-11-core-plan.md](./plans/2026-11-11-core-plan.md) | 证据重置收口交接快照 | 日志 |
| [2026-11-11-depth-lift-plan.md](./plans/2026-11-11-depth-lift-plan.md) | 01/02/03 深度提拉 | 已执行 |
| [2026-11-11-quality-lift-plan.md](./plans/2026-11-11-quality-lift-plan.md) | 01/02/03 总体提拉 | 已执行 |
| [2026-11-11-remediation-plan.md](./plans/2026-11-11-remediation-plan.md) | 02→01→03 整改 | 已执行 |
| [2026-11-12-04b-okf-strict-plan.md](./plans/2026-11-12-04b-okf-strict-plan.md) | 10 · 4b OKF/Wiki 严格化 | 已执行 |
| [2026-11-12-05-closeout-plan.md](./plans/2026-11-12-05-closeout-plan.md) | 10（原 05）收口计划 | 已执行 |
| [2026-11-12-05-evidence-pool-plan.md](./plans/2026-11-12-05-evidence-pool-plan.md) | 10（原 05）证据池修复 | 已执行 |
| [2026-11-12-05-gap-closure-plan.md](./plans/2026-11-12-05-gap-closure-plan.md) | 10（原 05）七条 gap 补齐 | 已执行 |

**保留原因**：这些文件记录了“当时为什么这么判”，对追溯有用；但其中的计数、链接与判断可能已被后续修复取代。
