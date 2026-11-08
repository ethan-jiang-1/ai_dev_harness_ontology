---
status: draft
updated: 2026-11-08
rq: [RQ2, RQ3]
evidence: [E-05]
---

# 生成：本体从哪来

> 多数本体文献默认本体已经存在；真实项目第一步往往是「造一个」。这里问「来源怎么决定可信度、生成物怎么被消费」，不负责精化（[refinement](../refinement/README.md)）。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 4 条（[findings](./findings.md)） |
| 未发现 / 开放 | 4 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 本体/说明的生成路线；不含精化、表示、生命周期 |

## 当前判断

- **生成产出候选，不是完备本体。** 现有证据能证明「能生成可读、部分正确的结构」，不能证明「能被下游判定器直接消费」。`推测`
- **先写 assumptions 再写描述，显著提升完整性。** OntoDoc：win 54–61%，completeness 3.43→3.84；但没有下游任务。`已核`
- **来源决定系统性偏向。** 专家手工覆盖窄/维护贵；LLM 生成语义漂移；表征挖掘只限特定嵌入；规则自演化要人工种子。`推测`
- **可消费性评估缺失。** 判定器能否加载/解释/复现生成结构，目前没有一篇测。`已核`（缺口）

## 文件地图

| 想知道 | 去 |
|---|---|
| 四条路线/证据/失效 | [mechanism](./mechanism.md) |
| 四条判断的证据/边界 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始论文 | [OntoDoc digest](../../../src/papers/2611.01276-ontodoc/digest.md) · [ReX-GG digest](../../../src/papers/2610.41901-rex-gg/digest.md) · [Peeling digest](../../../src/papers/2610.41785-peeling-matryoshka/digest.md) · [Evontree digest](../../../src/papers/2510.26683-evontree/digest.md) |

## 边界

- **不保证可消费。** 说明/结构生成后，判定器能否加载未测。
- **不保证来源可信。** 来源标记目前是文档层，不进判定权重。
- **不解决维护。** 生成后的同步/版本管理在 [lifecycle](../lifecycle/README.md)。

## 关联

- 派：[05 生产](../README.md) · 结论：[E-05](../../conclusions.md)
- 相邻：[refinement](../refinement/README.md) · [representation](../representation/README.md)
- 判定：[02 checker](../../02-judgment/checker/README.md)
