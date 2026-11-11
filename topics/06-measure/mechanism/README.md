---
status: draft
updated: 2026-11-08
rq: [RQ3]
evidence: [E-10]
---

# 本体知识真的在模型里吗

> 大量工作默认「模型能答对本体题 ⇒ 它掌握了本体」。这里用因果干预测中间一步：答对是否来自内部结构，还是表面模式。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 5 条（[findings](./findings.md)） |
| 未发现 / 开放 | 5 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 本体预测的内部机制；不含行为/下游任务（[metrics](../metrics/README.md)） |

## 当前判断

- **本体预测机制上可干预。** 换掉内部表示能改变本体层答案；存在可定位的内部表征。`已核`
- **但不能与类别辅助信息干净分离。** 单层最好 MDAS 0.592/0.587（instance-of，Qwen3-8B）；0.59 是 Cause 与 Iso 的平均分，不是「59% 的样本同时做到」；没有方法到 1.0。原因未定（表示纠缠或方法不够强），原文不能区分。`已核`
- **Distributed subspace > SAE/DBM。** SAE 0.412/0.371、DBM 0.425/0.396，DAS 0.584/0.547、MDAS 0.592/0.587（instance-of 单层 Disentangle）；但 **MDAS vs DAS 不宜排序**：instance-of Entity 上，MDAS 的 Iso 更高（0.658 vs 0.579）、DAS 的 Cause 更高（0.589 vs 0.527）；单 seed 无 CI。`已核`
- **多任务与多层都提升分离度，但 Δ 口径不同。** 多任务是 best-vs-best 配对差（Iso +0.081 / Cause −0.052），不是整体平均；四层 DAS 512×4 0.667 的 +0.102 是相对同方法同总维的单层（≈0.565，由 0.667−0.102 反推），不是相对 0.584。`已核`
- **类级差异大，但原文没有可引用的区间。** 类级结果以散点与附录的均值/排名呈现：具体/规则类（airport/country/currency/university）较好，宽泛/异质类（body of water/geographical feature/material）较差；同一类当 base 与当 source 也不同。`已核`

> 口径（`已核`）：各方法按 Entity Disentangle 选配置、Context 复用同一配置；Iso 与 Cause 的评估池不同。小 rank 单层不能套 0.40/0.55 阈值（`推测`，digest 工程线）。

## 文件地图

| 想知道 | 去 |
|---|---|
| 因果抽象、方法、数字、类级与 Δ 口径 | [mechanism](./mechanism.md) |
| 接口、训练参数、成本、stop、第一个 sprint | [mechanism §实施与客户价值](./mechanism.md#实施与客户价值a3a4)、[§stop](./mechanism.md#stop-condition) |
| 五条判断的证据/边界 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始论文 | [MIOE digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-38326) |

## 边界

- **只 Qwen3-4B/8B、两个任务。** 不能外推到其他模型族/本体约束。
- **只 subject-token residual stream。** 其他干预位置未测。
- **机制可干预 ≠ 可精确控制。**
- **无下游/部署评估。**

## 关联

- 派：[06 测量](../README.md) · 结论：[E-10](../../conclusions.md)
- 相邻：[metrics](../metrics/README.md) · [trace](../trace/README.md)
- 判定：[02 checker](../../02-judgment/checker/README.md)
