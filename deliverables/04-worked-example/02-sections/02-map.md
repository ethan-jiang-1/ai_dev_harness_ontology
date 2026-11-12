---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# 症状地图：你卡在哪

> 不要从第一页重读。按「你看到什么」查表，直接去对应小节。

## 建（A）

| 你看到什么 | 最可能的原因 | 去哪 |
|---|---|---|
| 不知道消费者是谁、契约填不满 | 没有真实 consumer / moment / refuse | [A.1](../03-body/01-build.md) |
| 不知道自己的表怎么变成 TBox/CQ | 没有推导顺序；在照抄 fixture 的 11 类 | [transfer](92-transfer.md) §2–§3 |
| Turtle 解析失败 | 语法/前缀/文件路径 | [A.3](../03-body/01-build.md) |
| `pyshacl` 报 0 violation，但数据明显有问题 | shape 没有 target；`targeted=0` | [A.4](../03-body/01-build.md)、[A.5](../03-body/01-build.md) |
| shape 报很多无关 violation | target 过宽；缺声明/闭世界 | [A.4](../03-body/01-build.md)、[boundaries](04-boundaries.md) |
| 不知道选词表/结构/逻辑哪档 | 没按消费位置选 | [A.2](../03-body/01-build.md) |
| 建完了不知道能不能用 | 只看 `parsed`，没看三关 | [A.5](../03-body/01-build.md) |
| 契约 principal 对不上（governance 写成 analyst） | CQ3 是 dataset 级治理查询，不能用 analyst；principal 是判定身份，不是 consumer 名字 | [A.1](../03-body/01-build.md)、[C.1](../03-body/03-govern.md)、[transfer §6](92-transfer.md) |

## 用（B）

| 你看到什么 | 最可能的原因 | 去哪 |
|---|---|---|
| 不知道选哪条路线 | 没盘点资产 | [B.0](../03-body/02-consume.md) |
| CQ 返回 0 行 | 覆盖/数据/查询/过滤/版本 | [B.2 空结果分因](../03-body/02-consume.md) |
| CQ 返回太多行 | 缺 `FILTER`/类型约束/superset | [B.2](../03-body/02-consume.md) |
| 纠错后反而变差 | 全量纠错；没有 2×2 | [B.3](../03-body/02-consume.md) |
| OBDA 重写跑通但结果错 | 重写正确 ≠ 查询正确；超 QL 公理 | [B.4](../03-body/02-consume.md) |
| 不知道要不要做纠错/OBDA | 不是必经步骤 | [README §3](00-overview.md#03-四个常见起点) |

## 治（C）

| 你看到什么 | 最可能的原因 | 去哪 |
|---|---|---|
| 有标签，但没有策略 | 标签 ≠ 策略 | [C.1](../03-body/03-govern.md) |
| policy 两条规则都命中，T9 为什么 undetermined | R4/R5 同优先级、effect 不同 | [C.2](../03-body/03-govern.md) |
| 审计 outcome 写成 query 级合计 | per-subject 记录不能代表 query | [C.4](../03-body/03-govern.md) |
| 策略写了但不生效 | 执行层单实现/fail-open；没有执行点 | [C.1](../03-body/03-govern.md)、[C.3](../03-body/03-govern.md) |
| 一列多个 tag，level 不知道取哪个 | 多标签规则没定；policy 的 level 是标量 | [transfer §6.2](92-transfer.md)、[C.2](../03-body/03-govern.md) |
| 表页能看到敏感列 | object 方向泄漏；只删 subject | [C.3](../03-body/03-govern.md) |
| 审计缺字段/不能 replay | 没有版本/快照/`decision_id` | [C.4](../03-body/03-govern.md) |
| 输出校验 0 violation，但结果不对 | `targeted=0` 空转；只查了 schema | [参考表 §6](91-reference.md) |
| 跨段出错，不知道哪一段 | 没有 run_id/snapshot/version | [参考表 §7](91-reference.md) |

## 验收/上线

| 你看到什么 | 去哪 |
|---|---|
| 不知道做完没有 | [acceptance](05-acceptance.md) |
| 要算成本/工期/能不能批 | [decision](06-decision.md) |
| 要空表照填 | [templates](93-templates.md) |
| 被问「这能信吗」 | [boundaries](04-boundaries.md) |
| 被问「和 01/02/03 什么关系」 | [relations](97-relations.md) |
| replay 版本对不上 | [C.4](../03-body/03-govern.md)、[A.5](../03-body/01-build.md)（snapshot 是日期标签、tag/contract 是 fixture 约定、parser 未记） |
