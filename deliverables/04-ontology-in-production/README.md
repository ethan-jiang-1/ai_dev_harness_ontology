---
status: draft
deliverable_status: draft
updated: 2026-11-09
target: 本体/数据工程师；应用/agent 工程师；治理/安全
basis: E-02/E-03/E-04/E-12/E-20/E-21/E-22；05/03/01 topics；未入库 signal（不是 E）
---

# 04 · 从本体到应用：建、用、治

> **读者**：本体/数据工程师、应用/agent 工程师、治理/安全/合规 ｜ **回答**：本体怎么从 CQ 变成可消费的 KG，再被 agent 查得动、治得住 ｜ **不回答**：值不值得做（去 01）、具体接缝怎么做（去 02）、为什么是这些位置（去 03）。

> **怎么用**：本页只做索引；先读本份 [GUIDE.md](./GUIDE.md)。

## 0. 一页结论

**04 是 01–03 的“落地生命周期”：建 → 用 → 治。**

1. **先定 CQ 和消费者**：没有 CQ、没有负例、没有下游消费者，不要开始“建本体”。
2. **LLM 只做候选**：生成、公理、对齐、精化都只到“候选 + 人审”；已测来源是单域/单 benchmark，不是跨域效应量。**build 章本轮不升级**（没有 in-scope evaluation 来源）。
3. **“能查”是独立工程面**：Text-to-SPARQL 有三条路线（选择性纠错 / ontology-in-context / ontology-free navigation），没有头对头；OBDA 不等于 NL→query。
4. **治理不是最后补的**：权限、来源、时效、审计、输出校验要在接口里；只在输入侧拦，等于不治输出。
5. **材料分两类**：已入库来源通过 E-21/E-22 引用；未入库的留在 `evidence/` 的 signal 表。04 不新增 E。

## 目录

| 节 | 文件 | 内容 |
|---|---|---|
| 导读 | [GUIDE.md](./GUIDE.md) | 先读哪一页、按角色/时间怎么走 |
| 2 地图 | [sections/map.md](./sections/map.md) | 生命周期、三段的问题、产出与 owner |
| 3 主体 | [body/README.md](./body/README.md) | 建 / 用 / 治 三分册 |
| 4 边界 | [sections/boundaries.md](./sections/boundaries.md) | 外部信号、不能证明什么、反模式 |
| 5 验收 | [sections/acceptance.md](./sections/acceptance.md) | 每段的期待、数据、stop |
| 6 关系 | [sections/relations.md](./sections/relations.md) | 与 01/02/03/05 的关系、维护 |
| 证据 | [evidence/README.md](./evidence/README.md) | E-21/E-22 + 未入库 signal |

## 关注什么 / 需要什么材料

| 项 | 内容 |
|---|---|
| 关心 | 本体怎么建到“可消费”；自然语言怎么查 KG；权限/来源/审计怎么进接口 |
| 需要材料 | E-21/E-22、03/querying、01/access-control、02 的 R0/R5/R8/R9；未入库 signal 只作旁证 |
| 不做什么 | 不写“本体导论”；不把厂商 ROI 当 E；不把单点 benchmark 当跨域效应量 |
