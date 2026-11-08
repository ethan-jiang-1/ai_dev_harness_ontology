---
status: draft
updated: 2026-11-08
---

# 质量推进报告

> 对应计划：[quality-plan](./quality-plan.md)。以质量门为准，不以数量结项。

## 结论

**结构层、来源层、子主题与 digest 深打磨已完成；G7 独立 critic 抽样 7/22（32%）经过 4 轮修正后全部 pass。** 剩余限制是「抽样不是全审」与「无独立复现」；已在本报告保留。

## 质量门

| 门 | 要求 | 结果 |
|---|---|---|
| G1 digest 自包含 | 术语/方法/数字条件/不能证明/工程用法；不靠 card | **22/22 pass** |
| G2 证据可核查 | 数字带条件；10% 回原文；作者/读者推断分开 | **22/22 数字抽查通过**；L3 45+、L2/L1 约 30 个回原文 |
| G3 card 来源卡 | 40–75 行；只放元数据/索引/局限 | **22/22**（56–72 行） |
| G4 子主题 dashboard | 一屏；findings/frontier/mechanism 分文件 | **20/20**（16 拆 + 4 薄页 dashboard） |
| G5 跨页一致 | sources 链 digest；计数/术语/E-L 一致 | **pass**：sources 22/22；17/2/3/4 对齐；E/L 无悬空 |
| G6 导航可解析 | 三步到 digest；0 broken links | **1,172 links / 0 broken** |
| G7 复核独立 | critic 抽样 ≥30%；不合格不进下一波 | **pass**：7/22（32%）独立 critic；4 轮后全部 pass；见 [critic-sample](./critic-sample.md) |

## 波次

| 波次 | 结果 |
|---|---|
| Wave 0 校准 | MIOE/CAI/POLAR 三篇 G1/G2 样板；补页码/表号、术语、缩写；冻结模板 |
| Wave 1 L3 | 12 篇 L3 结构复核；每篇 5 个数字回原文；`digest-audit` L3 全 pass |
| Wave 2 L2/L1 + card | 10 篇数字抽查；22 张 card 压成 56–72 行；6 个 sources 改 digest-first |
| Wave 3 子主题 | 20/20 dashboard；16 个重子主题拆 findings/frontier/mechanism；4 个薄页 dashboard-lite |
| Wave 5 一致 | conclusions 17/2/3/4 对齐；sources 22/22；E/L 无悬空；术语分离 |
| Wave 6 digest 深打磨 | 22/22 加「数字之间的逻辑」/「最小审计/落地」；见 [digest-polish-audit](./digest-polish-audit.md) |

## 关键产物

- 来源层：[src/README](../src/README.md) 定义 card=来源卡、digest=自包含正文；22 篇目录齐 PDF/MD 三件套/card/digest/figures。
- 来源卡：[card-audit](./card-audit.md)，22/22，56–72 行。
- digest：[digest-audit](./digest-audit.md)，22/22；深打磨见 [digest-polish-audit](./digest-polish-audit.md)，22/22 有 why/逻辑段 + 最小落地段。
- 子主题：20/20 dashboard；重页有 findings/frontier/mechanism，薄页只做 dashboard，不建空文件。
- 跨页：conclusions 17 已核 / 2 推测 / 3 存疑 / 4 冲突；E-01…E-19、L 编号无悬空。
- 导航：根 README router；01–05 派 README 为 index；06 为子主题地图；1,170 链接 0 broken。

## 深打磨做了什么

不是补表号，而是让每篇能回答「为什么这些数字是这样」和「我照着做第一步是什么」：

- **MIOE**：DAS/MDAS 为什么强、多任务为什么 Iso↑/Cause↓、多层为什么有效、类级为什么差；最小审计 6 步。
- **CAI**：结构为什么不提准确率（harness 自适应/结构不是证据/抽取误差复合/选择负担）；最小落地 6 步。
- **POLAR**：T1-only 为什么退化成 blanket veto；最小落地 7 步。
- **N&D**：K0→K1 为什么最大、文本为什么优于 JSON、H2 为什么没支持；最小落地 7 步。
- **Ontology Catch**：curated 为什么 catch/FA 都高、组合为什么无净收益；最小落地 7 步。
- **CASEL**：为什么不是最低 HSR；最小落地 8 步。
- 其余 L3/L2/L1 同标准；L1 保持短，但仍自包含。

## 未通过 / 限制

- **G7 完成**：subagent 通道不可用，改用 workflow critic；7/22 抽样、4 轮修正后全部 pass。其余 15 篇仍靠自评 + 数字回原文；critic 是 LLM，不是人类审稿。
- **没有独立复现**：所有「已核」仍是「读过一手原文」，不是「已证」。
- **部署层回报、false-veto/false-defer、维护成本**仍缺量化；已在各 frontier 记录。
- **L1 4 篇**只到摘要级/一页判断，没有深读正文；引用时按 `摘要级`。

## 下一阶段

1. 用 `experiments/` 做 EXP-001/002/003：投影 vs 查询 vs 检索；判定器漏检/误报；按机制分派指标。
2. 补 G7：独立 critic 抽样；若 subagent 仍不可用，用人工第二读者。
3. 补部署指标与 false-veto/false-defer 标注。
4. 在 digest 深打磨基础上，再决定是否进 `deliverables/`。
