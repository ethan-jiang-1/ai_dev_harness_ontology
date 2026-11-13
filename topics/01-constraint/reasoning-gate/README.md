---
status: draft
updated: 2026-11-12
rq: [RQ2, RQ4]
evidence: [E-16]  # withdrawn
---

# 推理期约束：筛结论，验条件

> 模型正在推理、动作尚未执行：本体可以限制它能从哪些知识取候选，也可以检查结论/动作的前提条件是否成立。后者在条件不成立时 block 动作；缺证据只转观察。它只拦条件不成立的动作，不是覆盖所有动作的闸门，也不是安全保证。
>
> **2026-11-12 对账**：本页来源 OntoAct（E-16）与 Multi-agent（2610.36325）均已撤回（[tombstone](../../../meta/audits/2026-11-11-source-purge.md#src-2610-21983)）。下列判断作**历史/机制参考，不作活证据**，等级降 `推测`；三值条件/缺证据转观察的设计思想保留作重启参考（对应交付物 01 的 gap 行 / W-05）。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 4 条（[findings](./findings.md)） |
| 未发现 / 开放 | 4 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 推理期的条件验证与知识源限制；与 action-gate 同属动作前（时刻 1），但判据不同，不替代可逆性/审批与输出判定 |

## 当前判断

> 下列出自 OntoAct / Multi-agent（均已撤回）；原标「已核」一律降为 `推测`（历史/机制参考，不作活证据）。

- **它会拦动作，但只拦有适用条件公理的动作。** 条件/禁止被违反 → block；缺读数只报 unresolved、转观察；没有 axiom 的动作只能放行/fallback。`推测`
- **判据来自本体，不是模型自评。** OntoAct 用符号验证器求条件；多 agent 用确定性评分在 curated KG 上排序。`推测`
- **约束形式决定它是护栏还是天花板。** 验证条件（OntoAct）不一定封顶；限制知识源（curated KG）可能封顶（Jaundice/Vertigo 恒 0）。两项任务形态不同，不是头对头。`推测`
- **缺证据应触发观察，不是直接 block。** 三值条件 ⊤/⊥/?；? 走观察/追问，避免把「不知道」变成「不允许」。`推测`
- **覆盖率决定它是不是选择性护栏。** 没有适用 axiom 的动作/假设只能放行或 fallback。`推测`

## 文件地图

| 想知道 | 去 |
|---|---|
| 两种机制/流程/证据/失效 | [mechanism](./mechanism.md) |
| 症状映射/接口/参数/成本/stop/客户指标（工程发现 1–4） | [mechanism](./mechanism.md) 的「工程发现 1–4」 |
| 四条判断的证据/数字 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始论文 | [OntoAct digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-21983) · [多 agent digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-36325) |
| 研究提示词与输出 | [prompt.md](./prompt.md)；run 记在 `runs/`（有 prompt 才建） |

## 边界

- **不是可逆性闸门。** 它不判动作能否撤销、也不分配审批；有适用 axiom 且条件不成立时，它会 block 该动作。可逆性/审批归 [action-gate](../action-gate/README.md)。
- **不是输出判定。** 它看推理过程中的结论与动作前提，不看出厂产物。
- **不是安全保证。** OntoAct 作者明确不声称可部署；它给的是可审计的拒绝理由，不是形式安全证明。
- **不保证覆盖。** curated KG / schema 覆盖不到的地方，约束会失效或封顶。

## 关联

- 派：[01 约束](../README.md) · 结论：[原 E-16（已撤回）](../../conclusions.md)
- 相邻：[action-gate](../action-gate/README.md) · [commit-gate](../commit-gate/README.md)
- 判定：[02 判定](../../02-judgment/README.md)
