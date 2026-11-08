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

- **本体预测机制上可干预。** 说明存在可定位的内部表征；但**不能与类别辅助信息干净分离**（MDAS 最好 0.592/0.587）。`已核`
- **没有方法到 1.0。** 「部分分离」可能是表示纠缠，也可能是方法不够强；本文不能区分。`已核`
- **Distributed subspace > SAE/DBM。** SAE Disentangle 0.412/0.371；DAS 0.584/0.547；MDAS 最强。`已核`
- **多任务 Iso↑/Cause↓；多层窗口更好。** 四层 DAS 512×4 0.667（+0.102）。`已核`
- **类级差异大。** 具体/规则类好；宽泛/异质类差；聚合分数掩盖。`已核`

## 文件地图

| 想知道 | 去 |
|---|---|
| 因果抽象/方法/数字/边界 | [mechanism](./mechanism.md) |
| 五条判断的证据/边界 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始论文 | [MIOE digest](../../../src/papers/2610.38326-mioe/digest.md) |

## 边界

- **只 Qwen3-4B/8B、两个任务。** 不能外推到其他模型族/本体约束。
- **只 subject-token residual stream。** 其他干预位置未测。
- **机制可干预 ≠ 可精确控制。**
- **无下游/部署评估。**

## 关联

- 派：[06 测量](../README.md) · 结论：[E-10](../../conclusions.md)
- 相邻：[metrics](../metrics/README.md) · [trace](../trace/README.md)
- 判定：[02 checker](../../02-judgment/checker/README.md)
