---
status: draft
updated: 2026-11-07
rq: [RQ2, RQ3]
---

# 00 harness：被接入的那台机器

六派都是往这台机器上接。本目录讲机器的七个部件**各自如何工作、在哪失效**；本体具体怎么接、效果如何，去对应的派。

## 七个部件

划分不按软件模块，而按**模型在一个回合里被控制的环节**：

> 给它看什么 → 它留下什么 → 谁在做 → 它怎么施力 → 结果是否可接受 → 我们能否看见 → 是否被授权

## 七个部件与六派的接口

| 部件 | 一句话失效 | 接哪一派 |
|---|---|---|
| [context](./context.md) 供给 | 压缩会先杀死语义（判据和冗余长得一样） | [03 知识](../03-knowledge/README.md) |
| [memory](./memory.md) 留存 | 状态比事实更接近记忆的本质 | [04 状态](../04-state/README.md) |
| [orchestration](./orchestration.md) 分工 | 并行不省总上下文，只挪瓶颈位置 | **无**（见下） |
| [tools-and-sandbox](./tools-and-sandbox.md) 施力 | 能力面与权限面必须分开设计 | [01 约束](../01-constraint/README.md) |
| [verification](./verification.md) 判定 | 判定器与被判对象必须不同源 | [02 判定](../02-judgment/README.md) |
| [observability](./observability.md) 看见 | 只记结果不记中间，等于没有观测 | [02 判定](../02-judgment/README.md) |
| [governance](./governance.md) 授权 | 粗粒度审批会退化成橡皮图章 | [01 约束](../01-constraint/README.md) |

> **「分工」是唯一没有对应流派的部件。** 多智能体协作中的共享本体，目前只有零散的「协作契约」提法，缺可判定的设计与证据。这是本仓库记录的一个空白，不是遗漏。

## 约束强度谱

同一份本体放在不同部件上，强度差一个量级（完整图见 [topics/README](../README.md#强度与覆盖率反向)）：

```
弱 ── context ── memory ── orchestration ── tools ── verification ── governance ── 强
     被忽略      状态失真    协作错配        动作被执行   产出被放行      变更落盘
```

两条推论：

1. **强度与覆盖率反向。** 强端管得硬但管得少；弱端管得广但什么都管不住。中间空档（大量中间产物）是研究不足区。
2. **「本体提升准确率」的说法几乎都发生在弱端。** 用准确率量强端机制，必然得出「无增益」——见 [度量错配](../06-measure/metric-mismatch.md)。

## 阅读顺序

[context](./context.md)（最常见的失效起点）→ [verification](./verification.md)（最容易被做错）→ [governance](./governance.md)（最硬的约束）→ 其余按需。

只关心本体用法，可跳过本目录，直接进六派。
