---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# 02 运行：账本、评测、成本、上线、领域

> 本目录回答「怎么把 recipe 跑起来、怎么验收、怎么上线」，不重复 recipe 的机制。

| 文件 | 回答 | 什么时候读 |
|---|---|---|
| [ledger.md](./ledger.md) | 记什么字段、怎么算 `p_h`/false-veto/审批成本 | 开工前 |
| [evaluation.md](./evaluation.md) | 噪声地板、样本量、预注册、shadow/A-B | 设计验收 |
| [cost.md](./cost.md) | 五维成本、盈亏平衡、TCO、单价空表 | 做预算 |
| [rollout.md](./rollout.md) | shadow→advisory→enforce、回滚、审批队列 | 上线前 |
| [domains.md](./domains.md) | 五域约束、哪些阈值必须重标 | 换域时 |

**读法**：先 `ledger` 定口径，再 `evaluation` 定样本，最后 `cost`/`rollout` 做 go/no-go。
