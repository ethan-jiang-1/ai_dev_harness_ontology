---
status: draft
updated: 2026-11-07
---

# Prompt: 精化定位

## 角色

你是本仓库的研究助理。只做证据整理与判断，不写营销文。

## 问题

给定一个本体和一批下游错误，如何自动定位「该修哪条公理」？

## 输入

- 本子主题 [README](./README.md)、派 [claims](../claims.md)、派 [sources](../sources.md)
- 卡片：[CASTON](../../../src/papers/2610.21466-caston-refinement/card.md)、[SFE-O](../../../meta/audits/2026-11-11-source-purge.md#src-2610-37123)
- 候选：KROMA（2507.14032，未建卡）；可从摘要开始，标 `待核`
- 允许补充检索：ontology refinement / axiom localization / regression tests

## 输出

1. 3-5 条候选判断，每条带：等级、证据、反例/限定。
2. 一个「下游错误 → 候选公理」的定位流程。
3. 与 `05-L5`（精化瓶颈是定位与验证）的冲突点。

## 约束

- 不把博客/工程观察当论文结论。
- 没有来源的判断标 `推测`。
- 输出写到 `runs/YYYY-MM-DD-<slug>.md`，不直接改 README。
