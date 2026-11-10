---
status: draft
deliverable_status: draft
updated: 2026-11-10
target: 要落地一个小型本体查询应用的团队
basis: E-02/E-04/E-06/E-12/E-19/E-20/E-21/E-22/E-23/E-24/E-25/E-26/E-27；工程产物；未测
---

# 04 · 从本体到应用：建、用、治

> **单读者**：一个落地团队（本体/数据、应用/agent、治理/安全 三种角色，同一套产物）。
> **回答**：一张消费者契约能不能走到可加载的 Turtle、能跑的查询、策略表与审计记录。
> **治理是最后一关**：C 章不过，A/B 的产物不算可用。
> **不回答**：值不值得做（01）、接缝怎么落（02）、为什么是这些位置（03）。

## 三条链

| 链 | 走法 | 产物 | 依据 |
|---|---|---|---|
| 建 | 契约 → 表示档位 → shape + 负例 → 三关闸门 | 消费者契约 + `build_report` | T:05/representation（含 consumability）；工程产物；未测 |
| 用 | 路线 → query → 空结果分因 → 选择性纠错 | 3 条 SPARQL | E-21 单设置；T:03/querying；S:Qlever digest |
| 治 | 标签 → 策略 → 泄漏 → 审计 | policy 表 + 测试 + audit schema | E-22：三层不能互推；E-20；T:01/policy、commit-gate/read-path；S:trustgraph digest |

依据：建=T:05/representation（含 consumability 三关）+ 模板；用=E-21 + T:03/querying compare + S:Qlever digest；治=E-22（三层不能互推）+ E-20（代码级）+ T:01/policy；共同 gap=输出校验生产误报、端到端失败传播。

## 五件主产物 + 四件测试/清单 = 9 件

① 消费者契约 ② Turtle（11 类/5 属性）③ 3 条 SPARQL ④ policy 表 ⑤ audit record；另加 ⑥ [policy_tests.json](./example/policy_tests.json)（10 条输入→decision）⑦ [audit.schema.json](./example/audit.schema.json) ⑧ [leak_cases.json](./example/leak_cases.json)（12 条泄漏用例）⑨ [fault_matrix.json](./example/fault_matrix.json)（10 类故障 × 3 段）。同一 [fixture](./example/README.md)（5 表/13 列；200/5,000 只作量级参照）。

依据：工程产物（合成例子）· E-22 + O-N28（规模只作量级参照）

## 证据不对称

建=工程产物（无 in-scope 建本体评估；E-02/E-12 只补局部两处）；用=E-21（三路线各单设置、无头对头）；治=E-22/E-20（强：原文+代码，但单企业、单实现）。

依据：E-20/E-21/E-22 的限定列；未测：跨域、部署效果

## kill criterion

若 04 只是 02 的 playbook + 03 的机制页拼接，并进 02。判据：拿掉 04，读者仍能从 02/03 拼出这条端到端链、跑通同一例子 → kill。

依据：未测（D2 立项判据）

## 目录

[build](./body/build.md) · [consume](./body/consume.md) · [govern](./body/govern.md) · [boundaries](./sections/boundaries.md) · [evidence](./evidence/README.md)

定位：[example](./example/README.md) · [GUIDE](./GUIDE.md) · [分节索引](./sections/README.md) · [关系](./sections/relations.md) · [验收](./sections/acceptance.md)
