---
status: draft
updated: 2026-11-07
rq: [RQ2, RQ3]
---

# Harness：控制回路的七个环节

本层是研究重点。划分不按软件模块，而按**模型在一个回合里被控制的环节**：

> 给它看什么 → 它留下什么 → 谁在做 → 它怎么施力 → 结果是否可接受 → 我们能否看见 → 是否被授权

七个环节对应的分组词是：**供给、留存、分工、施力、判定、看见、授权**。选七个而不是更少，是因为每个环节的中断方式不同；合并会让失效模式混在一起，无法归因。

## 一、本体在这七个位置上的约束强度

这是本仓库最核心的一张表。同一份本体放在不同环节，其约束强度差一个量级：

| 环节 | 本体在此的形态 | 违反时的后果 | 约束强度 |
|---|---|---|---|
| [context](./context.md) 供给 | 检索结果、编译产物、注入片段 | 被忽略、被压缩掉、被后续上下文覆盖 | **弱** |
| [memory](./memory.md) 留存 | 状态结构（约束/失效/冲突关系） | 状态失真，但不阻断动作 | 中 |
| [orchestration](./orchestration.md) 分工 | 共享词表、协作契约 | 协作错配，事后才能发现 | 中 |
| [tools-and-sandbox](./tools-and-sandbox.md) 施力 | 动作的可逆性分级 | 不可逆动作被执行 | 强 |
| [verification](./verification.md) 判定 | 判定器、完成判据 | 不合格产出被放行 | 强 |
| [observability](./observability.md) 看见 | 证据等级、溯源要求 | 无根据的结论进入下游 | 强 |
| [governance](./governance.md) 授权 | 持久化授权判据 | 错误变更落盘，不可撤回 | **最强** |

两条推论：

1. **约束强度与覆盖率反向。** 强度越高的位置，能判定的范围越窄——持久化前的授权只能管少数关键动作，而上下文注入能覆盖一切但什么都管不住。中间的空档（大量中间产物）就是本仓库认为研究不足的区域。
2. **「本体提升准确率」的说法几乎都发生在弱端。** 强端改善的是「是否可用」，用准确率度量它，必然得出「无增益」的结论。这可能解释了文献中正面与负面证据的冲突（推测，见 [thesis](../../THESIS.md) P1）。

## 二、七个机制

| 文档 | 环节 | 一句话 |
|---|---|---|
| [context](./context.md) | 供给 | 预算决定一切；压缩会先杀死语义 |
| [memory](./memory.md) | 留存 | 状态比事实更接近记忆的本质 |
| [orchestration](./orchestration.md) | 分工 | 并行不省总上下文，只改变瓶颈位置 |
| [tools-and-sandbox](./tools-and-sandbox.md) | 施力 | 能力面与权限面必须分开设计 |
| [verification](./verification.md) | 判定 | 判定器与被判对象必须不同源 |
| [observability](./observability.md) | 看见 | 只记结果不记中间，等于没有观测 |
| [governance](./governance.md) | 授权 | 粗粒度审批会退化成橡皮图章 |

## 三、阅读顺序

先 [context](./context.md)（最常见的失效起点）→ [verification](./verification.md)（本仓库的中心）→ [governance](./governance.md)（最硬的约束）→ 其余按需。

若只关心本体，直接跳到 [30-seams](../seams/README.md)。
