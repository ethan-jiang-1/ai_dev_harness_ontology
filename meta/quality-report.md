---
status: draft
updated: 2026-11-08
---

# 质量推进报告

> 对应计划：[quality-plan](./quality-plan.md)。按波次记录通过项、未通过项、抽样与下一步；不用“写了多少”当进度。

## 当前波次

**Wave 2 · L2/L1 来源层 + card**（进行中）：L2 6 篇 + L1 4 篇各抽 5 个关键数字回原文，全部命中（格式差异：CASTON 写作 six/100%，Peeling 写作 `._885`，multi-agent 写作 `0._340`）；22 张 card 尚未来源卡化。

**Wave 1 · L3 来源层**（完成，G7 partial）：12 篇 L3 结构复核 + 关键结果补表号/页码；MIOE/CAI/POLAR 15 个数字 + 其余 9 篇各 5 个数字回原文，全部命中（OntoDoc 的 54% 原文写作 54.00%）。`digest-audit` 的 L3 行全部改为 `pass（Wave 1）`。

**Wave 0 · 校准**（完成，G7 partial）：MIOE / CAI / POLAR 三篇 G1/G2 pass；15 个数字回原文；模板/checklist 已补「页码/表号」要求。独立 critic subagent 两次失败/挂起，改用自评双遍；G7 记 partial，Wave 1 继续用数字回原文 + 抽查。

## 质量门

| 门 | 要求 | 当前 |
|---|---|---|
| G1 digest 自包含 | 术语/方法/数字条件/不能证明/工程用法；不靠 card | 22 篇全部结构 pass |
| G2 证据可核查 | 数字带条件；10% 回原文；作者/读者推断分开 | 22 篇数字抽查通过；L3 45+ / L2-L1 约 30 个回原文 |
| G3 card 来源卡 | 40–75 行；只放元数据/索引/局限 | 3/22 样板（CAI/MIOE/POLAR）；19 张待压 |
| G4 子主题 dashboard | 一屏；findings/frontier/mechanism 分文件 | 2/20 已迁 |
| G5 跨页一致 | sources 链 digest；计数/术语/E-L 一致 | 未开始 |
| G6 导航可解析 | 三步到 digest；0 broken links | 基线 969 链接 / 0 broken |
| G7 复核独立 | critic 抽样 ≥30%；不合格不进下一波 | **partial**：subagent 两次失败/挂起；改用自评双遍 + 数字回原文；独立复核待补 |

## Wave 0 抽样

| 论文 | 类型 | G1 | G2 | 主要问题 | 状态 |
|---|---|---|---|---|---|
| MIOE | 机制型 | pass | pass | 缺页码/表号；SAE Iso 需精确；MIOE/residual stream/Entity-Context 未定义 | 已修 |
| CAI | 成本型 | pass | pass | 缺页码/表号；CAI 缩写未定义；75% routing 需标「解析模型」 | 已修 |
| POLAR | 反例型 | pass | pass | 缺页码/表号；Datalog/POLAR 未定义 | 已修 |

## 数字回原文（Wave 0 抽样）

| 论文 | 数字 | 出处 | 核对 |
|---|---|---|---|
| MIOE | MDAS 0.592/0.587；0.513/0.542 | Table 2, p.6 | ✓ |
| MIOE | SAE Iso 0.352/0.344（Disentangle 0.412/0.371） | Table 2, p.6 | ✓ |
| MIOE | 多任务 Iso +0.081 / Cause −0.052 | §4.2, p.6 | ✓ |
| MIOE | DAS 512×4 0.667；MDAS 256×4 0.666；MDAS 512×4 0.565 | Table 3, p.7 | ✓ |
| MIOE | 类级 0.03–0.65 | Fig. 3, p.7 | ✓ |
| CAI | 85% BrowseComp-Plus / 91% FRAMES | §1, §5 | ✓ |
| CAI | 324,479 tokens/问（uncompiled） | Table 4, p.10 | ✓ |
| CAI | −91% / +1.9% / −38% | §5, Table 4 | ✓ |
| CAI | 2% / 43% break-even/measured | §6, Eq. (4) | ✓ |
| CAI | 时延 3×；140→30 s | §8 / §6.4, Fig. 2 | ✓ |
| POLAR | +0.182 / +0.111 / −0.073 / −0.119（airline） | Table 3, p.6 | ✓ |
| POLAR | 18 格仅 8 格改善 | Table 3 / §5 | ✓ |
| POLAR | τ=0.80 保留率 36.6% / 100% / 98.7% | Table 4, p.7 | ✓ |
| POLAR | full 0.080；T1-only 0.087；no-irreversible 0.060 | Table 5, p.7–8 | ✓ |
| POLAR | 1,745 blocked decisions | §5.4 | ✓ |

## 已修复

- 三篇补数字出处（表号/页码/节号）；避免“裸数字”。
- MIOE：把“SAE Iso 0.35 左右”精确为 0.352/0.344，并区分 Disentangle；补 MIOE / residual stream / Entity-Context 术语。
- CAI：补 CAI 缩写；确认“75% routing 是解析模型，不是实测”有原文限定；补成本/时延出处。
- POLAR：补 Datalog / POLAR 术语；补 tier/阈值/block log 出处。
- 全仓链接：969 条，0 broken。

## 未通过 / 待办

- **G7 partial**：subagent 两次失败/挂起；独立 critic 未完成。已在报告注明；Wave 1 用自评双遍 + 数字回原文替代，不假装已独立复核；Wave 2 继续记录此限制。
- Wave 1 已补：N&D / Ontology Catch / CASEL / FIRME / OntoAct / SLB / Grid / OntoDoc 的 `> 出处`（表号/页码/节号）；结构复核 12/12，数字回原文待逐篇完成。

## 下一波

- **Wave 2（进行中）**：L2/L1 数字抽查已完成；3 张来源卡样板（CAI/MIOE/POLAR）已压到 69–72 行；19 张待压；`sources.md` 内容链改 digest。
- Wave 2 出口：22 篇 digest G1/G2 全 pass；22 张 card G3；sources 一致。
- Wave 2 下一步：按 3 张样板压剩余 9 张 L3 card，再压 6 张 L2 + 4 张 L1；card 审计见 [card-audit](./card-audit.md)。
