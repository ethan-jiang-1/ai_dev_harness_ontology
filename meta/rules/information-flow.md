---
status: draft
updated: 2026-11-13
---

# 信息流：三层分工、文体与层间接口

> **本页是三层分工的唯一权威**（依据 [ADR 0010](../../adr/0010-three-layer-information-flow.md) 与 [ADR 0012](../../adr/0012-instruction-layer-single-home.md)）。各层 README 与根 [README](../../README.md) 只做摘要与指针，冲突以本页与 [CHARTER](../../CHARTER.md) 为准。

## 0. 一句话

**`src/` 存干货，`topics/` 把干货组织成判断，`deliverables/` 把判断抽成给人用的成品。** 判断顺流而下，证据逆流而上；同一事实只在一层展开，上层引用下层，不复制。

## 1. 三层分工

| 层 | 读者 | 放什么 | 文体 | 完成判据 | 不该出现 |
|---|---|---|---|---|---|
| [`src/`](../../src/README.md) | **Agent**（研究员/写作者）为主；人按需溯源 | 原文、`card.md`（来源卡）、`digest.md`（自包含干货：条件/数字/边界/工程用法/`file:symbol`） | **干货**：短句、表、锚点；自包含 | 另一个 Agent 不读原文，仅靠 `digest.md` 就能写出 `topics/` 判断 | 面向人的科普导读、总结陈词、未核推测 |
| [`topics/`](../../topics/README.md) | **Agent + 人**（查判断与边界） | 六派 `claims.md`（`L-xx`）、跨派 `conclusions.md`（`E/Q/C`）、子主题 `findings`/`mechanism`/`frontier`、四轴、硬对象 `O-xx` | **组织**：一句判断 + 等级 + 条件/反例 + 回 `src` 的锚 | 每条判断引得出（进交付物）、复核得了（回得到 digest） | 无出处的断言、科普铺垫、复制 `src/` 原文 |
| [`deliverables/`](../../deliverables/README.md) | **人**（决策者/架构师/工程团队）；**不假设读过 `topics/`** | 按 `SCOPE.md` 定位抽取的四份成品（01 现状 / 02 工程 / 03 机制 / 10 落地现状）与 `_workpapers/`（底稿） | **通俗自包含**：先问题后判断、术语首现解释、主路径不跳层 | 没读过 `topics/` 的人能完成该份 `SCOPE.md` 的问题；细节可链 `topics/` | `topics/` 没有的新判断、未升 `E` 的 `L-xx`、偷换问题（拿合成教程冒充现状） |

## 2. 四条流规则

1. **只抽不增**：`deliverables/` 只从 `topics/` 抽取并组织，不新增 `topics/` 没有的判断；发现交付物缺口或错误，必须走 [AGENTS 修复回路](../../AGENTS.md#修复回路交付物被指错时的常设路径) 回上游补证后再回写。
2. **E 只做索引，做法住在 `mechanism`**：`conclusions.md` 保持窄表，每条现役 `E-xx` 只放一句「做法」并链接到对应 `mechanism.md` 等详细程序页；交付物涉及「怎么做」时须同时给 `mechanism` 链接（放「出处/可选」即可，主路径仍自包含）。
3. **交付物主路径自包含，但按 `SCOPE.md` 守边界**：概念、边界与操作步骤在交付物内讲完，`topics/` 链接只作「可选/出处」；答不了 `SCOPE.md` 的初心问题就标 gap + 记 `frontier`，禁止偷换成更容易的问题（[ADR 0014](../../adr/0014-deliverable-scope-single-home.md)）。
4. **底稿不进阅读路径**：`deliverables/_workpapers/`（冷读、评分、缺口盘点）和 `meta/plans/` 不构成 E、不新增规则、不进对外阅读路径。

## 3. 层间接口

| 接口 | 从 → 到 | 形式 | 纪律 |
|---|---|---|---|
| 消化入口 | `src/` → `topics/` | `digest.md`（§4 数字条件 / §5 边界 / §6 工程用法 / §8 关系） | `card.md` 只作 provenance，不承载判断；没有 digest 不算入库 |
| 局部 → 跨派 | `topics/<派>/claims.md` → `topics/conclusions.md` | `L-xx` 升 `E-xx` | 派内解决的留 `claims.md`；跨派或进交付物才升 `E-xx` |
| 结论与地址 | `topics/` → `deliverables/` | `E-xx`（主句）+ `O-xx`（地址） | 不引 `L-xx`；`O-xx` 只作地址，不替代 `E-xx` 作主句 |
| 定位契约 | `meta/deliverables/` → `deliverables/` | `meta/deliverables/scope.md` + 各份 `SCOPE.md` | 改/建交付物前必读对应 `SCOPE.md` |
