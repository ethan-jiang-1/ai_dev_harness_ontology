---
status: draft
updated: 2026-11-08
rq: [RQ2, RQ4, RQ5]
evidence: [E-02]
---

# 输出后判定：本体当 checker

> 产出已形成、尚未被使用。这里问「用什么本体、以什么方式检查、代价是什么」，不负责动作前拦截（[action-gate](../../01-constraint/action-gate/README.md)）或推理期约束（[reasoning-gate](../../01-constraint/reasoning-gate/README.md)）。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 5 条（[findings](./findings.md)） |
| 未发现 / 开放 | 5 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 输出后的语义/结构检查；不含格式检查与行为测试（见 [00-harness/verification](../../00-harness/verification.md)） |

## 当前判断

- **判定器本身是研究对象。** 不是「有没有本体」，而是「哪种来源、什么代价、漏检/误报怎么换」。`已核`
- **三种来源无单一向优。** curated 抓得多但 FA 高（precision 57.1%）；data-derived FA 低但 catch 8.2%；LLM 生成不稳定。`已核`
- **先超过空结果重试基线。** 空结果重试在人工 fault 上 catch 79.2%、FA 0%；真实答案上 catch 2.5%、FA 0.1%。`已核`
- **同源检查会失效。** 同一 artifact 既做 context 又做 checker，catch 反而下降（探索性）；判定器应与被判对象不同源。`已核`

## 文件地图

| 想知道 | 去 |
|---|---|
| 三种来源/空结果/同源/成本/失效 | [mechanism](./mechanism.md) |
| 每条判断的证据/数字/条件 | [findings](./findings.md) |
| 还缺什么、下一步看什么 | [frontier](./frontier.md) |
| 原始论文 | `src/papers/2610.37809-what-does-an-ontology-catch/` · [digest](../../../src/papers/2610.37809-what-does-an-ontology-catch/digest.md) |

## 边界

- **只查语义/结构，不查格式/行为。** 格式检查管不到语义；测试管不到语义。
- **不保证发现语义错。** 类型都对、关系方向反了/边界划错，结构检查抓不到；需要 LLM judge/人工。
- **不解决「该不该阻断」。** 判定只是信号；阻断/退回/仅标注是策略层。

## 关联

- 派：[02 判定](../README.md) · 结论：[E-02](../../conclusions.md)
- 相邻：[evidence](../evidence/README.md)（证据接地）· [00-harness/verification](../../00-harness/verification.md)
- 成本：[06-measure/feasibility](../../06-measure/feasibility/README.md)
