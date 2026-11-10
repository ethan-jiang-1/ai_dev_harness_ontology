---
status: draft
updated: 2026-11-10
parent: README.md
---

# 04 导读：按你的时间选一条路

> 本页只给阅读路径，不重复正文。第一次来，先读 [README](./README.md) §0–§1。

## 10 分钟：先判断要不要读

适合：只想判断这套东西值不值得投入；只读，不建。

1. [README §1](./README.md#1-30-分钟路径)：8 步，每步一个产物。
2. [A.1 契约](./body/build.md)：看 3 行契约长什么样。
3. [A.5 三关](./body/build.md)：看 `build_report` 该有什么。
4. [B.2 CQ1](./body/consume.md)：跑一条 Email 查询。
5. [C.2 策略表](./body/govern.md)：跑 T1/T2/T7 三条 decision。

**做完你能回答**：这张 fixture 能不能从契约走到一条受控查询。

## 2 小时：建 + 用 + 治各读一遍

适合：要评估落地工作量；读，不跑。

1. [README §2 产物地图](./README.md#2-九件产物地图)：先看 9 件产物。
2. [A · 建](./body/build.md)：契约 → 表示 → 本体 → shapes → 三关。
3. [B · 用](./body/consume.md)：资产表 → 3 条 CQ → 空结果分因 → 纠错/OBDA。
4. [C · 治](./body/govern.md)：三层 → 策略 → 泄漏 → 审计。
5. [example](./example/README.md)：对一遍数据与期望结果。

**做完你能回答**：这条链要几个人、几天、哪些产物必须齐。

## 1 天：按角色走

| 角色 | 先读 | 再读 | 备注 |
|---|---|---|---|
| 数据/本体 | [A.1](./body/build.md)–[A.5](./body/build.md) | [参考表 §1](./sections/reference.md) | 门槛项见 acceptance |
| 应用/agent | [B.0](./body/consume.md)–[B.4](./body/consume.md) | [参考表 §3](./sections/reference.md) | 门槛项见 acceptance |
| 治理/安全 | [C.1](./body/govern.md)–[C.4](./body/govern.md) | [C.2](./body/govern.md) | 门槛项见 acceptance |
| 评审/负责人 | [README §4](./README.md#4-验收6-条) + [acceptance](./sections/acceptance.md) | [boundaries](./sections/boundaries.md) | — |

> **门槛项不能跳**：A1–A4、A5+B1–B3、C1–C5，以及「无未修漏洞」。跳了就只能交 `conditional`，不能交出「最小链」。

## 卡住了

先查 [症状地图](./sections/map.md)：按「你看到什么」定位到章/节，不要从第一页重读。

## 读完之后

- 要判断「值不值得」：回 [01](../01-capability-status/README.md)。
- 要选接缝/recipe：回 [02](../02-engineering-playbook/README.md)。
- 要查机制/边界：回 [03](../03-mechanism-reference/README.md)。
- 要查证据：看 [evidence](./evidence/README.md)（附录）。
