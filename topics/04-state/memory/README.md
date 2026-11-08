---
status: draft
updated: 2026-11-08
rq: [RQ3]
evidence: [E-05, E-17]
---

# 跨轮记忆：状态，不是事实集合

> 一个回合结束、下一个回合开始时。这里问「记忆以什么形式存在、怎么对齐/更新/冲突、当前请求怎么用」，不负责哈希链的确定性（[determinism](../determinism/README.md)）。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 4 条（[findings](./findings.md)） |
| 未发现 / 开放 | 5 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 跨会话/跨期记忆；不含单轮上下文压缩（[00-harness/context](../../00-harness/context.md)） |

## 当前判断

- **本体在记忆里是克制的：对齐与印证条件，不是自由推理。** FIRME 用固定 product-topic 本体 + registry 做跨期身份；本体改动只影响槽位/条件。`已核`
- **身份先于内容。** alias memory 让 final-period CMR +7.8–12.1 pp；false merge 会长期污染。`已核`
- **增益在「会用」，不在「检索更多」。** EvoMemState Complete Retrieval 85.6%（MemoryBank 86.4，相当），但 Acc@complete 70.8 vs 36.8。`已核`

## 文件地图

| 想知道 | 去 |
|---|---|
| 事实 vs 状态/两层状态/失效 | [mechanism](./mechanism.md) |
| 四条判断的证据/数字 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始论文 | [FIRME digest](../../../src/papers/2610.40482-firme/digest.md) · [EvoMemState digest](../../../src/papers/2611.03743-evomemstate/digest.md) |

## 边界

- **不定义通用推理规则。** 本体只定义实体/关系/冲突表示与关键印证条件。
- **不把「未匹配」当「关系结束」。** 衰减不是删除；miss 可能是输入缺失。
- **不解决跨模态。** 两篇都是文本记忆；文档/图片/artifact 未测。

## 关联

- 派：[04 状态](../README.md) · 结论：[E-05 / E-17](../../conclusions.md)
- 相邻：[identity](../identity/README.md) · [determinism](../determinism/README.md)
- 上下文：[00-harness/context](../../00-harness/context.md)
