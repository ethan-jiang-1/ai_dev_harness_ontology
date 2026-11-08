---
status: draft
updated: 2026-11-08
rq: [RQ5]
evidence: [E-08, E-13, E-14, E-15, E-16, E-17]
---

# 落地经济学：什么时候值得

> 这一页回答 RQ5：**不是「本体有没有用」，而是「在什么条件下、付多少成本、值不值得」。** 横切综合，不替代各派 README。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 4 条（[findings](./findings.md)） |
| 未发现 / 开放 | 5 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 机制落地的成本/盈亏平衡/使能条件；不含具体机制实现（见各派） |

## 当前判断

- **值不值得 = 位置 × 成本 × 使能条件**，不是本体质量。`推测`
- **编译有可算的盈亏平衡**：`p_h > 2% + c/(0.929Q)`；平均 −38% 不能当上线依据。`已核`
- **分配没有单一最优**：按 harm–approval–cost 前沿选点；CASEL 8.7% approvals/7.02% HSR vs Risk-Menu 12.6%/5.82%。`已核`
- **没有一条适用于所有机制的能力曲线**：约束类随能力下降；知识投影不随容量上升。`已核`

## 文件地图

| 想知道 | 去 |
|---|---|
| 五成本/机制成本表/三盈亏/决策规则 | [mechanism](./mechanism.md) |
| 四条判断的证据/边界 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 问题→机制目录 | [mechanism §问题→机制](./mechanism.md) |

## 边界

- **不是部署实测。** 多数数字来自论文/模拟；维护/审批成本未量化。
- **不是单一评分卡。** 三个盈亏平衡各自适用，不能合成一个总分。
- **不覆盖所有域。** 工业/金融/医学/电网边界不同；没有统一对照。

## 关联

- 结论：[E-08 / E-13 / E-14 / E-15 / E-16 / E-17](../../conclusions.md)
- 派：[01](../../01-constraint/README.md) / [02](../../02-judgment/README.md) / [03](../../03-knowledge/README.md) / [04](../../04-state/README.md) / [05](../../05-produce/README.md)
- 方法：[metrics](../metrics/README.md)、[trace](../trace/README.md)、[mechanism](../mechanism/README.md)
- 实验：[EXP-003](../../../experiments/README.md)
