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
| 已发现 | 5 条（[findings](./findings.md)） |
| 未发现 / 开放 | 5 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 跨会话/跨期记忆；不含单轮上下文压缩（[00-harness/context](../../00-harness/context.md)） |

## 当前判断

- **本体不承担自由推理；但「给定且改动不扩散」只对 FIRME 成立。** FIRME 用 product–topic 本体（product/topic + `CONTAINS`/`PARENT_OF`）把 topic 讨论关联到 product，跨期身份由 registry 负责；本体只供给槽位、关系与印证条件 `已核`（FIRME §3.2/§6.5；digest §8）。「本体改动只影响槽位/条件、不扩散」没有改动对照、维护/变更流程未定，是架构推断 `推测`。
- **EvoMem 的本体是长出来的，不是现成的。** 事实挂到最具体 concept，增量建 concept/fact 图；`CREATE/MERGE/SPLIT` 修订层级。层级错误会传进 relational state，自动质量评估仍开放 `已核`（机制）/ `推测`（错误幅度未测）——它仍然只组织状态，不做自由推理；「本体克制」不能推成「本体稳定」。
- **身份先于内容（净效应未单独识别，见 [identity/F1](../identity/findings.md)）。** alias memory 让 final-period CMR +7.8–12.1 pp（4 settings）`已核`（增量条件见 [identity/F2](../identity/findings.md)）；false merge 会把后续同名观察路由到错误 anchor，但「长期污染」是机制推断、论文未测量 `推测`。
- **增益在「会用」，不在「检索更多」。** EvoMemState Complete Retrieval 85.6%（MemoryBank 86.4，相当），但 Acc@complete 只有 70.8%（LoCoMo-Refined，较最强 baseline +11.5）/ 68.5%（MemSyco，+31.2）；两个数分属不同基准，只能各自与同基准 baseline 比。`已核`
- **评估分三层，抽取保真不能省。** CMR、human audit（reattachment recall / merge precision）、extraction faithfulness（round-trip F1 0.786–0.931，依语料/backend）分开报；抽取幻觉 3.3–7.4%、归一化误差 3.2–22.16%，没有 backend 全面占优。任何一层都不能替代另一层。`已核`（数字）/ 跨层外推 `推测`

## 文件地图

| 想知道 | 去 |
|---|---|
| 事实 vs 状态/两层状态/失效 | [mechanism](./mechanism.md) |
| 五态边界（N=3）· $100K 与 Rule 3/4 · GRPO 配方/60K/seeds | [mechanism](./mechanism.md) 的「五态、融合阈值与训练配方」 |
| stop 门 / 成本 / 客户指标 | [mechanism](./mechanism.md) 的 stop-condition、组织/成本、客户指标/V3 |
| 五条判断的证据/数字 | [findings](./findings.md) |
| 三层评估（CMR / human audit / round-trip） | [findings](./findings.md) F5 · [mechanism](./mechanism.md) 的「数据/接口」 |
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
