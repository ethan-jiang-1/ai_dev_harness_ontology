---
status: draft
updated: 2026-11-10
parent: README.md
---

# 04 导读：按你的时间选一条路

> 本页只给阅读路径，不重复正文。第一次来，先读 [README](./README.md) §0–§1；术语卡在 [glossary](./sections/glossary.md)。

## 10 分钟：先判断要不要读

适合：只想判断这套东西值不值得投入；只读，不建。

1. [README §1](./README.md#1-30-分钟读路径不要求跑)：8 步读路径。
2. [A.1 契约](./body/build.md)：看 3 行契约长什么样，governance 用哪个 principal。
3. [A.5 三关](./body/build.md)：看 `build_report` 该有什么，版本从哪来。
4. [B.2 CQ1](./body/consume.md)：看一条 raw 查询和它的 principal。
5. [C.2 策略表](./body/govern.md)：看 T1/T2/T7/T9/T11 怎么复算。

**做完你能回答**：这张 fixture 能不能从契约走到一条受控查询；哪些数字是 raw，哪些是 governed。

## 2 小时：建 + 用 + 治各读一遍

适合：要评估落地工作量；读，不跑。

1. [README §2 产物地图](./README.md#2-九件产物地图)：先看 9 件产物。
2. [A · 建](./body/build.md)：契约 → 表示 → 本体 → shapes → 三关。
3. [B · 用](./body/consume.md)：资产表 → 3 条 CQ → 空结果分因 → 纠错/OBDA。
4. [C · 治](./body/govern.md)：三层 → 策略/判定顺序 → skip/leak → 审计/query log。
5. [journey](./sections/journey.md) + [example](./example/README.md)：把一条查询从头到尾走一遍。

**做完你能回答**：这条链要哪些产物、哪些字段、哪些门槛。**具体工期看下面的工作量口径，不是 2 小时能估出来的。**

## 工作量口径（`推测`，不是报价）

| 项 | 量级 | 说明 |
|---|---|---|
| 建模（结构表） | 2–4 人周 | 5 表/13 列的小域；来自 `topics/consumability` 的单域估算 |
| shapes | 3–5 人日 | 2 条 shape + 负例；不含跨 validator |
| 实现/集成 | 未估 | 查询、policy、audit、replay 的工程胶水；04 不报价 |

> 这是 `推测`，不是承诺；你的域/规模/现有栈会改变它。04 不给报价。

## 1 天：按角色走

| 角色 | 先读 | 再读 |
|---|---|---|
| 数据/本体 | [A.1](./body/build.md)–[A.5](./body/build.md) | [参考表 §0/§2](./sections/reference.md)、[acceptance](./sections/acceptance.md) |
| 应用/agent | [B.0](./body/consume.md)–[B.4](./body/consume.md) | [参考表 §3](./sections/reference.md)、[journey](./sections/journey.md) |
| 治理/安全 | [C.1](./body/govern.md)–[C.4](./body/govern.md) | [参考表 §5–§7](./sections/reference.md)、[boundaries](./sections/boundaries.md) |
| 评审/负责人 | [README §4](./README.md#4-验收5-组门槛) + [acceptance](./sections/acceptance.md) | [boundaries](./sections/boundaries.md) + 工作量口径 |

> **门槛 5 组见 acceptance**：A1–A4 / A5+B1–B3 / C1–C3 / C4–C5 / 无未修漏洞。别把 GUIDE 的阅读路径当门槛数。

## 卡住了

先查 [症状地图](./sections/map.md)：按「你看到什么」定位到章/节，不要从第一页重读。

## 读完之后

- 要判断「值不值得」：回 [01](../01-capability-status/README.md)。
- 要选接缝/recipe：回 [02](../02-engineering-playbook/README.md)。
- 要查机制/边界：回 [03](../03-mechanism-reference/README.md)。
- 要查证据：看 [evidence](./evidence/README.md)（附录）。
