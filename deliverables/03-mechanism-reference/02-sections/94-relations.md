---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# 6. 关系与维护

 > 关系页回答：03 与 01/02 的关系、维护与结构。 ｜ 目标：知道稳定判断在哪、候选在哪。

### 6.1 与另外两份交付物的关系

> 共享的关系表与维护规则见 [deliverables/README §关系与维护](../../README.md#关系与维护)；本页只留 03 自己的结构图与维护规则。

### 6.2 维护规则

- **canonical 在 `positions/` 与 `across-positions/`**；附录是长版论证，不改结论。两者冲突时，以位置卡/横切页为准，并回改附录指针。
- 只从 [conclusions](../../../topics/conclusions.md) 与 [topics/README](../../../topics/README.md) 抽取；**不新增判断**。
- E-xx 变化时，先改 `topics/`，再回改位置卡、台账与边界；不要在这里调和冲突。
- H/D 必须始终带标记；不要因为引用次数多就把它写成 E。
- 原 7 章书稿计划不再维护；没有独立 handbook。


### 6.3 结构怎么长

| 文件 | 回答 | 什么时候读 |
|---|---|---|
| 03 | 三根分类轴、六位置总表、M1–M5 | 第一次进 03 |
| [positions/context.md](../03-positions/01-context.md) | 供给位置为什么不能阻断 | 查知识供给 |
| [positions/memory.md](../03-positions/02-memory.md) | 为什么记忆是状态 | 查跨轮/身份 |
| [positions/evidence.md](../03-positions/03-evidence.md) | 输出契约为什么不是闸门 | 查接地等级 |
| [positions/checker.md](../03-positions/04-checker.md) | 判定器质量曲线与三态 | 查输出后判定 |
| [positions/action.md](../03-positions/05-action.md) | 三种动作前子机制 | 查可逆性/条件/分配 |
| [positions/commit.md](../03-positions/06-commit.md) | 为什么「能推理」不等于「能授权」 | 查落盘前 |
| [positions/outside.md](../03-positions/07-outside.md) | determinism/read-path/supply/reasoning/training 为什么在谱外 | 查第六时刻/轴外 |
| [across-positions/measurement.md](../04-across-positions/03-measurement.md) | 这个位置该量什么 | 设计验收 |
| [across-positions/coverage.md](../04-across-positions/01-coverage.md) | 强度–覆盖率到底是什么 | 查 §4/争论 |
| [across-positions/execution-forms.md](../04-across-positions/02-execution-forms.md) | 形态与执行链 | 查「有引擎」 |
| [evidence-ledger.md](../05-evidence/01-ledger.md) | 每条 E 支持/不支持哪个位置 | 核证据 |
| [boundaries.md](../05-evidence/02-boundaries.md) | 15 条边界 + 12 条反例 + 证伪条件 | 审稿/自查 |
| [gaps.md](../05-evidence/03-gaps.md) | M1–M5、负结果、下一步 | 规划研究 |
| [appendix-constraint-spectrum.md](../09-appendix-constraint-spectrum.md) | 长版论证（历史） | 要完整论证时 |

> 只做入口；稳定判断在位置卡/横切页，证据在台账，缺口在 gaps。位置卡统一 8 字段：机制 / 触发输入输出 / 能改变什么 / 拦不住什么 / 使能条件 / 证据与边界 / 可证伪条件 / 上游指针。
