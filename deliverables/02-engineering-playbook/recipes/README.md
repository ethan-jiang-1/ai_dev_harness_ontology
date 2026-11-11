---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# Recipes：索引与写法

> 13 条 recipe 回答「拿本体做某件事，具体怎么做」。它们不是 E，不证明效果；效应量回 E-xx，细节回 `topics/` 的 mechanism。

## 索引

> **2026-11-11 证据重置**：A=3（R1/R10/R11）/ B=4（R2/R3/R7/R8）/ C=1（R9）/ gap=4（R4/R5/R6/R12）。

| Recipe | 一句话 | 接缝/形态 | 成熟度 | 主证据 |
|---|---|---|---|---|
| [R0 可执行性体检](readiness.md) | 先证明本体能被执行，再选接缝 | 准入 | 配方 | E-12/E-20；E-02/E-03 已撤回 |
| [R1 点位语义](knowledge.md#r1--点位语义k1先把-tag-名和单位对齐) | 先对齐 tag 名/单位/质量码（可加别名/槽位） | 供给 / context | A | E-12 |
| [R2 知识投影文本](knowledge.md#r2--知识投影文本把领域知识写成文本固定分节是工程建议) | 投影成文本；固定分节是工程建议；先 K1 | 供给 / context | B | E-12 |
| [R3 编译](knowledge.md#r3--证据编译只买-claim--逐字-span) | 只买 claim+span，先算 `p_min` | 供给 / compiled | B | E-08/E-14 |
| [R4 证据契约](judgment.md#r4--输出证据契约让答案带依据和接地等级) | 答案带观察与 grounding | 输出时 / compiled | **gap** | E-03 withdrawn |
| [R5 checker](judgment.md#r5--输出后-checker先超过空结果重试) | 先超过空结果重试 | 输出后 / compiled | **gap** | E-02 withdrawn |
| [R6 动作闸](constraint.md#r6--动作前可逆性闸只在不可逆高代价弱模型时试) | 只在不可逆/高代价/弱模型时试 | 动作前 / compiled | **gap** | E-04/E-13 withdrawn；E-15 参照 |
| [R7 身份/记忆](state.md) | 先 registry，再状态 | 跨轮 / compiled | B | E-05/E-17 |
| [R8 读路径](constraint.md#r8--读路径过滤只做可见性不要当授权) | 只做可见性，不当授权 | read-path / engine | B（条件性） | E-20 |
| [R9 落盘授权](constraint.md#r9--落盘前授权现在只能设计不要声称已落地) | 只能设计，不能声称落地 | 落盘前 / 无实现 | C | E-20 |
| [R10 离线/CI SHACL ](offline-and-obda.md#r10--离线ci-shacl把没检查完做成第三态) | 把「没检查完」做成第三态 | 离线/CI / compiled | A | E-20 |
| [R11 OBDA ](offline-and-obda.md#r11--obda-查询重写本体在查询编译时被执行) | 查询时编译，不预存语料 | supply / engine | A | E-20 |
| [R12 受监管供给](regulated.md) | 证据 + solver + 人签核 | 供给+输出+人 | **gap** | Grid 已移出 |

## 每条 recipe 的十字段

1. 目标 / 不适用
2. 前提与使能条件
3. 接缝 / 形态
4. 最小数据契约
5. 实施步骤（两周 sprint 或 30–60 分钟准入）
6. 证据 / 数字 / 限定
7. 成本 / 工时 / 维护
8. 验收指标 / stop line
9. 失效模式 / 反例
10. 可抄锚点（论文/代码）

**填不满的字段，就是上游任务。** 不允许用「行业通常」补；要么有 E/digest，要么标 `推测` 或 `未知`。

## 怎么读

- 第一次：先读 [R0](readiness.md)，再按「你的问题」选一条；不要一次上三条。
- 做方案：读目标 recipe 的 §1–§5 + [interfaces](../appendices/interfaces.md) + [ledger](../operations/ledger.md)。
- 做验收：读 §6–§8 + [evaluation](../operations/evaluation.md)。
- 做预算：读 §7 + [cost](../operations/cost.md)。
- 上线：读 [rollout](../operations/rollout.md)。

## 不做什么

- 不把 recipe 当 E；它们不证明「做了有效」。
- 不把多条 recipe 同时上；先一条 shadow，再扩。
- 不把 `context` 当约束；硬约束另进 R5/R6。
- 不把 R8/R9 当已落地；它们有明确的「不能证明」。
