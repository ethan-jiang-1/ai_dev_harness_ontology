---
status: draft
updated: 2026-11-08
rq: [RQ2]
evidence: [E-06]
---

# 失败出在哪一环：先诊断工作流

> 一个任务失败了，最常见的归因是「模型不够强」。这个归因不可证伪，也不可操作。这里问「失败出在角色/变量的哪一环」。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 7 条（[findings](./findings.md)） |
| 未发现 / 开放 | 4 条（[frontier](./frontier.md)） |
| 下一步 | 4 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | NL→本体接地 DSL 的失败归因；含 D-15 医学鉴别诊断的跨域类比（非迁移证据）；不含机制/过程指标（见同派子页） |

## 当前判断

- **失败多归工作流，不归模型。** 输入不足、上下文缺失、模板/词汇缺口、校验弱、非局部修复都能造成同样表现。`已核`（框架）
- **五角色 + 七变量是可操作的诊断词汇。** 每个 case 填表：变量/证据/高摩擦/重设计杆/负责人。`已核`（框架）
- **校验弱 → 非局部修复 → 新错误。** 根因在 harness，不在模型；换更强判定器可能比换更强模型更有效。`推测`
- **归因前先分桶。** 映射失败、候选截断、本体覆盖缺口、排序错是四类不同失败；混在一起会把「没进池」记成「排错」。`推测`（分桶口径；D-15 实测 8.7% unmapped，D-11 给候选截断 10–20 的工程线）
- **聚合指标会掩盖 case-level。** Top-1、Top-3 与 case-level 必须同报；D-15 的聚合只 +2.5pp，个案 0.340→1.0，50% 完整度下 Top-3 反降 26.3→24.2。`已核`（单基准）
- **这是 position paper。** 单案例、无量化；不能写成「七变量已验证能预测失败」。`已核`

## 文件地图

| 想知道 | 去 |
|---|---|
| 五角色/七变量/钻井例子 | [mechanism](./mechanism.md) |
| 四条判断的证据/边界 | [findings](./findings.md) F1–F4 |
| 映射失败/候选截断/Top-1·Top-3 与 case-level | [findings](./findings.md) F5–F7；[mechanism](./mechanism.md) 的「数据/接口」「客户指标」 |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始论文 | [Diagnose digest](../../../src/papers/2610.35267-diagnose-workflow/digest.md) · [Multi-agent digest](../../../src/papers/2610.36325-ontology-multiagent-diagnosis/digest.md) |

> 编号沿用 [digest ledger](../../../meta/full-audit/digest-ledger.md)：D-11 = Diagnose，D-15 = Multi-agent。

## 边界

- **不是实证。** 单案例、无跨系统实验；七变量非正交/非穷尽。
- **不是可打分 rubric。** 目前靠定性判断；不同实践者可能给不同 profile。
- **不预测重设计效果。** 需要前后对照。
- **口径是本页自定的。** 语义充分率/首次通过率/返工轮次/人审工时/κ 的公式，D-11 只给指标名、没给公式；跨团队比较前先对齐（`推测`）。
- **F5–F7 来自 D-15 单基准与 D-11 工程线**，不是本主题的实测；换算到 NL→本体归因仍需实验。

## 关联

- 派：[06 测量](../README.md) · 结论：[E-06](../../conclusions.md)
- 相邻：[metrics](../metrics/README.md) · [trace](../trace/README.md)
- 判定：[00-harness/verification](../../00-harness/verification.md) · [02 判定](../../02-judgment/README.md)
