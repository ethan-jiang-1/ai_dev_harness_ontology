---
status: draft
updated: 2026-11-12
---

# 交付物定位（scope）：总索引与共用规矩

> **每份交付物的定位权威在它自己的 `SCOPE.md`**（改/建前必读）；本页是五份的**总索引 + 共用规矩**，不重复每份内容。决策依据 [ADR 0014](../../adr/0014-deliverable-scope-single-home.md)。
> 层级：宪章 > AGENTS > 本页（共用规矩）> 各份 SCOPE.md > README 读者钩子。

## 为什么有这套（04 的教训，血的教训）

04 曾名 *ontology-in-production*，却长成「不证明生产」的合成教程——因为没定义它「是什么/答什么/边界/红线」，模型拿不到真实生产证据时，擅自用更容易的问题（怎么建）偷换了原问题（落地现状）。**定位不钉死，跑着跑着就偏。** 现在每份有 SCOPE.md，fresh agent 一进来就知道奔哪个目标、干哪些事、边界在哪、有多大发挥空间。

## 三条总规矩（五份共用）

1. **先读 SCOPE 再动手**：改/建交付物前读它的 `SCOPE.md`；写下的每句话都要落在它「回答的问题」里。
2. **答不了就标 gap，不偷换问题**：admitted 证据答不了初心问题 → 显式标 gap + frontier 写「关闭它需要什么」；**禁止改答一个更容易的问题**（合成教程、理想化做法）冒充回答了原问题。
3. **定性不混**：描述（是什么）与规定（怎么做）分开；实证（真实证据）与合成（编的例子）分开。一份只承担一种定性，越界即漂移。

## 五份定性一览（权威在各份 SCOPE.md）

| 份 | 定性 | 回答的问题 | SCOPE |
|---|---|---|---|
| 01 现状 | 判断（描述·分级） | 值不值得做？今天能做到哪？ | [01/SCOPE](../../deliverables/01-capability-status/SCOPE.md) |
| 02 工程 | 做法（规定） | 具体怎么做？ | [02/SCOPE](../../deliverables/02-engineering-playbook/SCOPE.md) |
| 03 机制 | 机制（描述·参考） | 凭什么？边界在哪？ | [03/SCOPE](../../deliverables/03-mechanism-reference/SCOPE.md) |
| 04 示例 | 示例（规定·**合成**） | 一条最小建用治链长什么样？ | [04/SCOPE](../../deliverables/04-worked-example/SCOPE.md) |
| 05 现状 | 现状（描述·**实证**） | 业界真实落地如何？靠谱与否有无证据？ | [05/SCOPE](../../deliverables/05-production-landscape/SCOPE.md) |

> **04 与 05 的分界是要点**：04 是「你可以怎么建」的**合成示例**；05 是「业界实际怎么样」的**实证现状**。04 不证明生产；05 必须真实生产证据，缺证据标 gap，不许拿合成例子冒充。

## 入口质量门（五份共用的前提）

任何支撑交付物的素材，先过 [CHARTER §4](../../CHARTER.md#4-素材准入material-gate)：**≥2026-06-01、活跃、多主体高影响**；在役标准例外须「现行版本 + 2026-06 后维护活动」；采/引前查[来源黑名单](../rules/excluded-sources.md)。**孤证/过期/厂商自证/二手综述不进**——这是 purge 的血泪教训，预防比事后对账便宜百倍。

## 维护

- 新增/重定位一份交付物：先建/改它的 `SCOPE.md`，再更新本页一览与 [loading](../rules/loading.md)；走 [ADR](../../adr/README.md) 判据。
- 发现内容与 SCOPE 定性不符：按[修复回路](../../AGENTS.md)处理——改内容回 scope，或走 ADR 重定位；**不允许内容偷偷越界**。
- `check_repo` 强制：每份交付物必须有 `SCOPE.md`。
- 本页只管定位索引与共用规矩；计数归 [state](../status/state.md)、质量打分归 [rubric](./quality.md)、字段归 [conventions](../rules/conventions.md)。