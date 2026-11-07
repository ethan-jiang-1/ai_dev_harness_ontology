---
status: draft
updated: 2026-11-07
---

# 论文消化验收报告（2026-11-07）

> 对应计划：[digestion-plan](./digestion-plan.md)。范围：`src/papers/` 22 篇（20 基础 + 2 扫描）。

## 1. 完成了什么

| 项 | 数量 | 说明 |
|---|---|---|
| 论文目录 | 22 | `src/papers/{arxiv_id}-{slug}/` |
| PDF → MD | 22 × 3 | `paper.md`（正文）/ `references.md` / `appendix.md`（无附录写说明） |
| 分解卡 | 22 | `card.md`；`reading`/`provenance` 已更新 |
| 消化卡 | 22 | `digest.md`；L3 12、L2 6、L1 4（一页判断） |
| 论文图 | 35 | 18 篇有图；`figures/`；带出处/页码/看什么 |
| 自绘/综合图 | 0（本阶段） | 图主要集中在论文原图；综合图在 Wave 4 未单独绘制，文字表格替代 |
| 结论 | 17 已核 / 2 推测 / 3 存疑 / 4 冲突 | E-01…E-19；见 [conclusions](../topics/conclusions.md) |

**证据升级**：E-09（SLB 数字）与 E-10（MIOE 机制）从「综述转述/推测」升为「已核」；新增 E-14（编译盈亏平衡）、E-15（harm–approval–cost 前沿）、E-16（推理期约束形式）、E-17（记忆是状态）、E-18（agent 配置方差）、E-19（落地经济学，`推测`）。

## 2. 最有价值的判断变化

1. **能力梯度不是一条线。** 约束类收益随基线能力上升而下降（POLAR，E-13）；知识投影的增益不随容量上升（N&D，H2 p=0.85），9B 带投影 0.737 > 750B 不带 0.672（E-12）。两者不矛盾：护栏**替代**判断，投影**补充**知识。
2. **投影 vs 编译的分界更清楚。** 不是「结构 vs 文本」，而是**投影什么**：CAI 投影证据（claim + span），N&D 投影领域知识（本体塔）。C-04 已改写。
3. **闸门的形态决定代价。** POLAR 二值 veto 的收益可能主要来自「保守拒绝」（T1-only ≈ blanket veto）；CASEL 多模式分配的价值是 harm–approval–cost 前沿，不是最低 HSR；推理期**验证条件**（OntoAct 三值逻辑）不一定封顶，**限制知识源**（multi-agent curated KG）才封顶（E-16）。
4. **记忆的关键是身份与状态，不是检索更多。** FIRME：alias memory +7.8–12.1 pp CMR，false merge 会长期污染；EvoMemState：Complete Retrieval 85.6% 与最好 baseline 相当，但 Acc@complete 70.8/68.5（E-17）。
5. **度量必须能读中间。** SLB：85% 轨迹有 solver-like behavior、24% token，输出评估区分不出 hardcoded 与 independent；Agents are Systems：54% 方差是 run-to-run 噪声，信息轴影响 > 模型/预算；验证靠工具不靠 prompt（E-09/E-18）。
6. **落地经济学。** 值不值得 = 位置 × 成本 × 使能条件；三个可算盈亏平衡（编译/分配/能力）；见 [feasibility](../topics/06-measure/feasibility/README.md)。

## 3. 各派更新

| 派 | 主要更新 |
|---|---|
| 01 约束 | action-gate 加 POLAR/CASEL；reasoning-gate 加 OntoAct/多 agent；commit-gate 加 Commit Boundary；claims 01-L6…01-L14 |
| 02 判定 | checker 加 Ontology Catch 三源/空结果基线；evidence 加 OA-RAG 接地等级（自评限定）；claims 02-L5…02-L9 |
| 03 知识 | compilation 加 CAI 成本模型 + Grid 法规系统；projection 加 N&D 数字；claims 03-L5…03-L9 |
| 04 状态 | memory 加 FIRME/EvoMemState；identity 加 alias/false merge/commit gate；claims 04-L5/L6 |
| 05 生产 | generation 加 OntoDoc 假设层；refinement 加 CASTON；claims 05-L6/L7；L1 四篇一页判断 |
| 06 测量 | mechanism/trace/metrics/failure-attribution 全部升级；新增 feasibility；claims 06-L6…06-L14 |
| 00 harness | context 回答「编译省预算不提准确率」；verification 与 02 的判定器相接 |

## 4. 质量与边界

- **L3 12 篇**：card + digest + 2–3 图；数字带页码/表号；作者自述局限与读者推断分开。
- **L2 6 篇**：card + digest；OA-RAG/Commit Boundary/多 agent/EvoMemState/Agents are Systems/CASTON。
- **L1 4 篇**：只到卡 + 一页判断（Peeling/Evontree/SFE-O/ReX-GG）；**没有深读正文**，引用时按 `摘要级`。
- **无独立复现**：所有「已核」仍是「读过一手原文」，不是「已证」；本仓库尚无实验。
- **部署层回报**：CAI/N&D 的治理/上手/审计回报仍是作者主张，未量化。
- **false-veto / false-defer**：POLAR 1,745 blocked decisions 无标签；Commit Boundary 无实现。
- **维护成本**：本体/投影/registry 的长期人工成本没有一篇量化。

## 5. 未完成与下一步

1. **EXP-001/002/003**：投影 vs 查询 vs 检索；判定器漏检/误报；按机制分派指标。
2. **false-veto / false-defer 标注**：优先用 POLAR 的 blocked decisions 与 Commit Boundary 的规范做小规模标注。
3. **部署指标**：上手时间、跨源引用率、审计通过率；目前只有定性断言。
4. **L1 四篇**：只有在需要 05 生产派细节时才升 L2/L3；否则保持一页判断。
5. **综合图**：本阶段用表格替代；若做交付物，再补 3–5 张自绘图（能力梯度、成本前沿、闸门四形态）。

## 6. 验收清单

- [x] 22 个论文目录，均含 PDF / `paper.md` / `references.md` / `appendix.md` / `card.md` / `digest.md`。
- [x] `paper.md` 保留 `<!-- page N -->`；references/appendix 单独成文件。
- [x] 所有相对链接可解析（950 条，0 broken）。
- [x] 22 张卡有 `reading` / `provenance`；18 篇 `精读`，4 篇 L1 `摘要级`。
- [x] 22 篇 digest 有 `quality` / `based_on`。
- [x] conclusions：17 已核 / 2 推测 / 3 存疑 / 4 冲突；README 与 checklist 计数一致。
- [x] manifest 的「消化」列 22 篇全部 ✓。
