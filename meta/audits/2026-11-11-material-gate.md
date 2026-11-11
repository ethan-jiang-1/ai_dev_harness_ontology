---
status: draft
type: material-gate-audit
updated: 2026-11-11
scope: 2026-11-11 新增的 4 个 web/talk 材料
---

# 2026-11-11 素材准入审计（新增材料）

> 依据 [CHARTER §4](../../CHARTER.md#4-素材准入material-gate)。审计窗口 2026-11-11 → 2026-12-11；本页只审本轮新增的 4 个材料，旧材料全量重审另列。
>
> **结论**：4 个新增材料都**不能**作 `admitted`。3 个判 `signal`（G3/G4 未过），1 个判 `excluded`（G1 未过，且不是 in-force 标准）。对应的 原 03 知识派第 17 条、原 05 生产派第 11 条、06 失败归因 signal 与交付物里的 signal 段落已撤回；**没有 E 依赖它们**。

## 1. 判定表

| 材料 | G1 时效 | G2 活跃 | G3 影响 | G4 来源 | G5 可核 | 判定 | 原因 |
|---|---|---|---|---|---|---|---|
| Emil Eifrem（Neo4j），AI Engineer 2026-07-22 | 过（2026-07-22） | 过（companion essay 2026-07-24） | **不过**：会议主 track 不算信号；Neo4j 是作者公司；无独立采用/社区讨论 | **不过**：公司高管演讲 | 过（官方 transcript） | `signal` | 除作者自述外，没有第二个独立信号；company self-report |
| ZS Associates，AI Engineer 2026-07-23 | 过（2026-07-23） | 过（talk + transcript） | **不过**：会议主 track 不算信号；ZS 是作者公司；无独立复现/采用 | **不过**：公司案例 | 过（官方 transcript） | `signal` | 单公司案例，自报 20–30 分钟 vs 3–4 周，无评测/成本 |
| 叶小钗，人人都是产品经理 2026-08-31 | 过（2026-08-31） | 过（作者持续更新） | **不过**：984 浏览/1 评论不算信号；无独立引用/采用 | **不过**：个人经验文 | 过（原文 URL） | `signal` | 从业者经验，无样本/口径/审计 |
| EKGF EKG Maturity（OMG Managed Community） | **不过**：页脚 2022-01-31 / 2026-01-14，无法证明首版 ≥2026-06-01 | 过（社区仍在动） | 部分：OMG 社区页 + GitHub 14★（stars 不算）；无 I1–I3 | 过（OMG Managed Community） | 过（官网 + GitHub） | `excluded` | G1 未过；成熟度模型不是 in-force 标准，不能走 §4.4 例外 |

## 2. 处理

| 材料 | 动作 | 去向 |
|---|---|---|
| Eifrem | 删除 `src/web/aie-2026-eifrem-ontology-layer/`；撤回 原 03 知识派第 17 条、03 README signal、03 context signal、04 A.1/A.3 signal、04 sources 行 | 候选队列：`topics/03-knowledge/frontier.md`（只作线索） |
| ZS | 删除 `src/web/aie-2026-zs-multi-agent/`；撤回 06 失败归因 signal、02 反模式 #18、04 B.0 signal、04 sources 行 | 候选队列：`topics/06-measure/frontier.md`（只作线索） |
| 叶小钗 | 删除 `src/web/woshipm-ontology-cost-2026/`；撤回 原 05 生产派第 11 条、01 验收成本 signal、02 成本 signal、04 decision 成本 signal、04 sources 行 | 候选队列：`topics/05-produce/frontier.md`（只作线索） |
| EKGF | 删除 `src/web/ekgf-ekg-maturity/`；从 `src/README` 台账移除；k-ladder 只保留官网 URL 作外部对照，不引卡 | 不建卡；不升 L/E |

## 3. 受影响判断

- 原 03 知识派第 17 条（共享本体语义层）：**撤回**；03 README 与 context 卡的 signal 段落删除。
- 原 05 生产派第 11 条（成本结构）：**撤回**；01/02/04 的成本 signal 段落删除。
- 06 `failure-attribution` 的 ZS signal：**撤回**；02 反模式 #18 删除。
- 没有 `E-xx` 引用这 4 个材料；`E-19`/`E-12` 等原结论不受影响。

## 4. 备注

- 这次审计不改变结构整改（术语、首屏、合并、C3）——那些只动表达，不依赖这 4 个材料。
- 如果后续要恢复这些内容，先补 G3：找 ≥2 个独立信号，至少 1 个 I1–I3（独立采用、同行评审、标准组织、≥2 个独立机构参与），再按 `admitted` 重审；不要用浏览量/会议主 track 当信号。
