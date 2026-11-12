---
status: draft
updated: 2026-11-10
rq: [RQ2, RQ4]
evidence: [E-22]
---

# 策略层：标签怎么变成 allow/deny

> **薄页（<2 篇独立来源）**：本页判断只作候选/边界，**不承担稳定判断**；引用时必须带「单来源」限定。

> 回答：敏感标签/等级怎么映射成 principal/action/condition/effect，冲突怎么解，默认怎么定，审计留什么。
> 不回答：标签怎么产（[access-control](../access-control/README.md)）、读路径怎么执行（[commit-gate/read-path](../commit-gate/read-path.md)）、写授权（[commit-gate](../commit-gate/README.md)）。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 3 条（[findings](./findings.md)） |
| 未发现 / 开放 | 3 条（[frontier](./frontier.md)） |
| 下一步 | 3 个（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-10 |
| 覆盖 | 标签/等级 → 策略 → 决定 → 审计；不含标签生产、读路径执行、写路径授权 |
| 来源 | GB/T 43697/35273、XACML 3.0、ODRL 2.2（已入材料卡）；Atlas/Ranger/OpenFGA（待入库）；OPA（已入库，adjunct） |

## 当前判断

- **策略层是独立层，不能从标签推出。** `E-22`：标签有、策略无、执行单实现；「有敏感标签」推不出「有策略」或「执行正确」。`已核`（综合）。[F1](./findings.md)
- **策略语言能表达冲突/默认/义务，但语义不同。** XACML 有 deny-overrides 等合并算法；ODRL 有 `perm/prohibit/invalid` 冲突策略与 duty；Rego 默认 deny、规则序；OpenFGA 是 ReBAC，没有「冲突」概念。不能把四种语义混成一张表。`已核`（标准卡；条款待核）。[F2](./findings.md)
- **领域标准给等级/处置，不给 principal/action 映射。** GB/T 43697 给分类分级框架与级别，GB/T 35273 给 PII 类别与处理规则；「level 4 → 哪些角色 deny」仍是工程选择。`已核`（GB/T 摘要）/ `推测`（映射）。[F3](./findings.md)
- **11 条测试里 10 条有唯一期望，T9 暴露优先级空洞。** 04 policy.json 的 `skip` 是 XACML/ODRL 都没有的第 4 种效果；`clearance` 在 input 里但 8 条规则均未消费；steward+table 时 R4 与 R5 谁先没写。`已核`（逐行读 policy.json）。[mechanism](./mechanism.md)
- **标准给三级，政策给 1–4，是工程映射。** GB/T 43697 只分核心/重要/一般；GB/T 35273 只定义个人信息/敏感个人信息；04 用 1–4 数值 + 2/3 阈值，没有标准条款支撑。`已核`（标准范围/摘要；条款待核）。[mechanism](./mechanism.md)

## 文件地图

| 想知道 | 去 |
|---|---|
| 三条判断的证据/条件/边界 | [findings](./findings.md) |
| 7 列 schema、冲突消解、7–11 条测试 | [mechanism](./mechanism.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 标签/执行层 | [access-control](../access-control/README.md) · [read-path](../commit-gate/read-path.md) |
| 原始标准/实现 | 见 [01 sources](../sources.md) 的 policy 行；入库后补 digest |

## 边界

- **不是领域策略来源**：GB/T 43697 是分类分级标准，不是「谁能读哪列」的策略标准；Atlas/Ranger 是标签→策略的工程架构，不是本体。
- **不是执行证明**：本页只到 decision；读路径的 fail-open/object 方向在 [read-path](../commit-gate/read-path.md)。
- **不是写授权**：写路径 commit gate 仍无实现。
- **不能外推**：标准/实现都未入库；条款号与 API 在入库前标 `待核`。
- **不把 OPA 当本体策略引擎**：OPA 不解析 OWL/SHACL、不消费 Glyph 标签；它是 adjunct。

## 关联

- 派：[01 约束](../README.md) · 本派 claims：01-L16–L19
- 相邻：[access-control](../access-control/README.md) · [commit-gate](../commit-gate/README.md) · [read-path](../commit-gate/read-path.md)
- 结论：[E-22](../../conclusions.md)（三层不能互推）
