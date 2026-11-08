---
status: draft
updated: 2026-11-08
rq: [RQ2, RQ5]
evidence: [E-04, E-13, E-15]
---

# 动作前拦截

> 模型决定调用工具、尚未真正调用之前：这里问「这个动作有没有可接受的逆路径/该分配多少审查」，不负责落盘后的提交契约。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 6 条（[findings](./findings.md)） |
| 未发现 / 开放 | 4 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选/检索式（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 动作前的可逆性判定、多模式分配、审批/成本；不含落盘前（[commit-gate](../commit-gate/README.md)）与推理期（[reasoning-gate](../reasoning-gate/README.md)） |

## 当前判断

- **可逆性可以做成结构化判据。** POLAR 用 T1–T5 类型化关系 + 反向搜索 + 最弱一步分数，比 LLM judge 可审计。`已核`
- **收益与基线能力反向。** 强模型/retail 经常回退；硬护栏可能只剩代价。`已核`
- **「结构」还没被证明。** T1-only ≈ blanket veto，增益却不比 full 小；结构反向组合的贡献未隔离。`已核`
- **多模式分配的价值是 harm–approval–cost 前沿**，不是最低 HSR。CASEL 用约 30% 更少审批达到相近 harm。`已核`（模拟）

## 文件地图

| 想知道 | 去 |
|---|---|
| POLAR/CASEL 的机制怎么跑 | [mechanism](./mechanism.md) |
| 每条判断的证据/数字/条件 | [findings](./findings.md) |
| 还缺什么、下一步看什么 | [frontier](./frontier.md) |
| POLAR 原卡 | `src/papers/2610.08082-polar/card.md` · [digest](../../../src/papers/2610.08082-polar/digest.md) |
| CASEL 原卡 | `src/papers/2610.36570-casel/card.md` · [digest](../../../src/papers/2610.36570-casel/digest.md) |

## 边界

- **只拦动作，不验产出。** 产出后的语义判定归 [02 判定](../../02-judgment/README.md)。
- **只判可逆性，不判意图/授权。** 合法用户意图（retail 退货）可能被误拦；需要意图/授权层。
- **不保证逆操作能执行。** 「有逆序列」不等于「恢复成功」；本文不模拟完整 s′。

## 关联

- 派：[01 约束](../README.md) · 结论：[E-04 / E-13 / E-15](../../conclusions.md)
- 相邻：[commit-gate](../commit-gate/README.md)（落盘前）· [reasoning-gate](../reasoning-gate/README.md)（推理期）
- 成本/可行性：[06-measure/feasibility](../../06-measure/feasibility/README.md)
