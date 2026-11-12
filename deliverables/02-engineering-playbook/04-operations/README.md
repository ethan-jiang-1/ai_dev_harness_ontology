# 02 · 运维五件（04-operations）

> **本目录是什么**：把一条 recipe 真正跑起来需要的账本、评测、成本、上线、领域适配。上级回 [02/README](../README.md)。

| 文件 | 是什么 | 什么时候读 |
|---|---|---|
| [01-ledger](./01-ledger.md) | **评测账本**：per-query/per-decision 记什么字段 | 动手前就建 |
| [02-evaluation](./02-evaluation.md) | 评测：基线、方差、CI 怎么报 | 要验收时 |
| [03-cost](./03-cost.md) | 成本：单价、公式、敏感性 | 报预算时 |
| [04-rollout](./04-rollout.md) | 上线：shadow → 灰度 → 全量 | 要上线时 |
| [05-domains](./05-domains.md) | 领域适配注意事项 | 换域时 |

**顺序**：账本 → 评测 → 成本 → 上线。没有账本，后面四个都算不出。
