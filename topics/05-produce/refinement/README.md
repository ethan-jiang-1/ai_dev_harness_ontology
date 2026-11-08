---
status: draft
updated: 2026-11-08
rq: [RQ2, RQ3]
evidence: [E-05]
---

# 精化：在既有本体上修

> 真实项目很少从零建本体；更常见的是「已经有一个，但不够用/有错/过时」。这里问「怎么定位该修哪条、怎么验证」，不负责生成（[generation](../generation/README.md)）。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 4 条（[findings](./findings.md)） |
| 未发现 / 开放 | 4 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 既有本体的子类/约束精化；不含从零生成、生命周期 |

## 当前判断

- **精化可以自动化到小规模。** CASTON high-confidence 6/6 被两位专家接受；pretrained ensemble 57.1%；GPT-4o mini 31.3%。`已核`
- **瓶颈是定位与验证，不是生成候选。** 先缩到 30 条可疑公理 × 10 候选父类，再让 LLM 做局部判断。`已核`
- **fine-tune embedding 是主要增益来源。** 100% vs 57.1%；不是「换个更大 LLM」能补的。`已核`
- **medium-confidence 不可靠。** 全 mixed，必须人审；confidence 校准是模型特定的。`已核`

## 文件地图

| 想知道 | 去 |
|---|---|
| 两种做法/CASTON 数字/失效 | [mechanism](./mechanism.md) |
| 四条判断的证据/边界 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始论文 | [CASTON digest](../../../src/papers/2610.21466-caston-refinement/digest.md) |

## 边界

- **不是大规模。** 单一本体、单一公理类型、6 条高置信修复。
- **不是下游闭环。** 修复是否让判定器/应用变好，没测。
- **不是通用 confidence。** 换模型要重测校准。

## 关联

- 派：[05 生产](../README.md) · 结论：[E-05](../../conclusions.md)
- 相邻：[generation](../generation/README.md) · [lifecycle](../lifecycle/README.md)
- 判定：[02 checker](../../02-judgment/checker/README.md)
