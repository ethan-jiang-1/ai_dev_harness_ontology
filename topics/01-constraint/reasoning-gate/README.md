---
status: draft
updated: 2026-11-08
rq: [RQ2, RQ4]
evidence: [E-16]
---

# 推理期约束：拦结论，不拦动作

> 在动作之前、甚至在产出之前：本体限制模型**能用什么结论、能推到哪一步**。它不改变工具调用是否执行，而改变「哪些结论有资格被取用」。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 4 条（[findings](./findings.md)） |
| 未发现 / 开放 | 4 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 推理期：验证条件 / 限制知识源；不含动作前与落盘前 |

## 当前判断

- **推理期约束是 01 派的第三个位置。** 比动作闸门更早，比输出判定更深；判据来自本体，不是模型自评。`已核`
- **约束形式决定它是护栏还是天花板。** 验证条件（OntoAct 三值逻辑）可同时提成功率、降无效干预；限制知识源（curated KG）会封顶（Jaundice/Vertigo 恒 0）。`已核`
- **缺证据应触发观察，不是直接 block。** 三值条件 ⊤/⊥/?；? 走观察/追问，避免把「不知道」变成「不允许」。`已核`
- **覆盖率决定它是不是选择性护栏。** 没有适用 axiom 的动作/假设只能放行或 fallback。`推测`

## 文件地图

| 想知道 | 去 |
|---|---|
| 两种机制/证据/失效 | [mechanism](./mechanism.md) |
| 四条判断的证据/数字 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始论文 | [OntoAct digest](../../../src/papers/2610.21983-ontoact/digest.md) · [多 agent digest](../../../src/papers/2610.36325-ontology-multiagent-diagnosis/digest.md) |

## 边界

- **不是动作闸门。** 它不阻止工具调用；只限制结论/推理依据。
- **不是输出判定。** 它看推理链，不看出厂产物。
- **不保证覆盖。** curated KG / schema 覆盖不到的地方，约束会失效或封顶。

## 关联

- 派：[01 约束](../README.md) · 结论：[E-16](../../conclusions.md)
- 相邻：[action-gate](../action-gate/README.md) · [commit-gate](../commit-gate/README.md)
- 判定：[02 判定](../../02-judgment/README.md)
