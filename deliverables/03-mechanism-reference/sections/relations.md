---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# 6. 关系与维护

### 6.1 与另外两份交付物的关系

| 交付物 | 回答 | 读者 | 形态 |
|---|---|---|---|
| [01 现状](../../01-capability-status/README.md) | 今天能做成什么、不能承诺什么 | 决策者/工程负责人 | 判断 + 矩阵 |
| [02 工程实施](../../02-engineering-playbook/README.md) | 拿本体做某件事，具体怎么做 | 工程负责人/架构师 | 步骤 + 接口 + 验收 |
| **03（本份）** | 为什么是这些位置/形态，证据边界在哪 | 架构师/研究者 | 参考 + 边界 |

**一句话**：01 告诉你「值不值得做」，02 告诉你「怎么做」，03 告诉你「凭什么这么说、说到哪为止」。

### 6.2 维护规则

- **canonical 在 `positions/` 与 `across-positions/`**；附录是长版论证，不改结论。两者冲突时，以位置卡/横切页为准，并回改附录指针。
- 本页只从 [conclusions](../../../topics/conclusions.md) 与 [topics/README](../../../topics/README.md) 抽取；**不新增判断**。
- E-xx 变化时，先改 `topics/`，再回改本页、位置卡、台账与边界；不要在本页调和冲突。
- H/D 必须始终带标记；不要因为引用次数多就把它写成 E。
- 原 7 章书稿计划不再维护；没有独立 handbook。


### 6.3 本目录怎么长

| 文件 | 回答 | 什么时候读 |
|---|---|---|
| 本页 | 三根分类轴、六位置总表、M1–M5 | 第一次进 03 |
| [positions/context.md](../positions/context.md) | 供给位置为什么不能阻断 | 查知识供给 |
| [positions/memory.md](../positions/memory.md) | 为什么记忆是状态 | 查跨轮/身份 |
| [positions/evidence.md](../positions/evidence.md) | 输出契约为什么不是闸门 | 查接地等级 |
| [positions/checker.md](../positions/checker.md) | 判定器质量曲线与三态 | 查输出后判定 |
| [positions/action.md](../positions/action.md) | 三种动作前子机制 | 查可逆性/条件/分配 |
| [positions/commit.md](../positions/commit.md) | 为什么「能推理」不等于「能授权」 | 查落盘前 |
| [positions/outside.md](../positions/outside.md) | determinism/read-path/supply/reasoning/training 为什么在谱外 | 查第六时刻/轴外 |
| [across-positions/measurement.md](../across-positions/measurement.md) | 这个位置该量什么 | 设计验收 |
| [across-positions/coverage.md](../across-positions/coverage.md) | 强度–覆盖率到底是什么 | 查 §4/争论 |
| [across-positions/execution-forms.md](../across-positions/execution-forms.md) | 形态与执行链 | 查「有引擎」 |
| [evidence-ledger.md](../evidence/ledger.md) | 每条 E 支持/不支持哪个位置 | 核证据 |
| [boundaries.md](../evidence/boundaries.md) | 15 条边界 + 可证伪条件 | 审稿/自查 |
| [gaps.md](../evidence/gaps.md) | M1–M5、负结果、下一步 | 规划研究 |
| [appendix-constraint-spectrum.md](../appendix-constraint-spectrum.md) | 长版论证（历史） | 要完整论证时 |

> 本页只做入口；稳定判断在位置卡/横切页，证据在台账，缺口在 gaps。位置卡统一 8 字段：机制 / 触发输入输出 / 能改变什么 / 拦不住什么 / 使能条件 / 证据与边界 / 可证伪条件 / 上游指针。
