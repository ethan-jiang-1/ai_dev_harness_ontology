---
status: draft
updated: 2026-11-07
rq: [RQ3]
evidence: [E-05]
---

# 身份：跨源、跨期的同一性

## 问题

记忆系统最先坏的地方往往不是「忘了」，而是「认错了」：同一实体在不同来源、不同时期以不同名字出现，被当成多个实体；或者两个相似实体被合并。身份不稳，后面的状态、冲突、失效都挂不住。

这是 04 派的前置问题：没有身份，就没有可对齐的历史。

## 两种做法

| 做法 | 机制 | 代表 |
|---|---|---|
| registry 锚定 | 固定 product–topic 本体 + 规范身份/持久别名；重复观察定向到同一段历史 | FIRME（2610.40482） |
| 时序属性图 | 领域无关本体把对话组织成带时间的事件；append-only 保留演化；检索时消解冲突 | APEX-MEM（2604.14362，ACL 2026） |

FIRME 的克制之处：本体主要做对齐与印证条件，不承担自由推理（E-05）。**alias memory 让 final-period CMR +7.8–12.1 pp（4 settings），human-audit reattachment recall +22.5–29.0 pp；semantic matching token −40.3%。** APEX-MEM 的量化结果：LOCOMO QA 88.88%、LongMemEval 86.2%（摘要级，`待核`）。

**身份变更本身是一个 commit 问题。** Commit Boundary（概念架构，无实现）把「可推理的证据」与「可授权身份变更的证据」分开：`UNVERIFIED` 可以进推理，但不能授权 merge/split；需要 claim-specific promotion、冲突解决、scope/version 检查。身份系统不只需要「匹配得准」，还需要「什么时候有权改」。

## 为什么它属于 04 而不是 05

05 生产派问「本体从哪来、怎么修」；这里问的是「用本体把身份钉住」。本体是工具，身份是状态问题。两者的失效模式不同：生产派怕来源不可信，身份派怕合并/拆分错误。

## 失效模式

- **合并错误。** 两个相似实体被当成一个，历史被污染。
- **拆分错误。** 同一实体跨期碎裂，证据挂不上新版本。
- **别名漂移。** 规范名与持久别名失配。
- **来源/时间丢失。** 无法判断某条关系属于哪个版本。
- **registry 过时。** 本体升级后，旧身份无法对齐。
- **错误合并的长期污染。** 一个 false merge 会把后续同名观察路由到错误 anchor；merge precision 必须和 CMR 一起看。
- **把「没观察到」当「不是同一实体」。** 未匹配只说明当前证据不足，不是否定。

## 开放问题

- registry 的对齐策略：规则、嵌入、人工，还是混合？
- 身份置信度如何表达？低置信时是合并、挂起，还是双写？
- 跨源身份对齐能否复用本体匹配（KROMA 线）？
- 身份错误如何回滚，而不破坏已挂载的历史？
- commit gate 的 false-defer 率：在 FIRME 这类写入上，多少正确的身份变更会被 UNKNOWN_EVIDENCE 拦住？
- alias memory 与 canonical registry/semantic fallback 的分别贡献？

## 关联

- [04 状态派](../README.md)
- [memory](../memory/README.md)、[determinism](../determinism/README.md)
- [05 生产派的精化](../../05-produce/refinement/README.md)
- 卡片：[FIRME](../../../src/papers/2610.40482-firme/card.md)；候选：APEX-MEM（2604.14362）
