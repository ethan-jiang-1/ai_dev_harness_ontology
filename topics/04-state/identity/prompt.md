# Prompt: 跨期身份

## 角色

你是本仓库的研究助理。只做证据整理与判断，不写营销文。

## 问题

跨源、跨期身份对齐的最小可用 registry 是什么？它需要哪些字段、哪些决策规则？

## 输入

- 本子主题 [README](./README.md)、派 [claims](../claims.md)、派 [sources](../sources.md)
- 卡片：[FIRME](../../../src/papers/2610.40482-firme.card.md)
- 候选：APEX-MEM（2604.14362，未建卡）；可从摘要开始，标 `待核`
- 允许补充检索：entity resolution / registry / temporal identity

## 输出

1. 3-5 条候选判断，每条带：等级、证据、反例/限定。
2. registry 的最小字段表与对齐策略（规则/嵌入/人工）。
3. 与 `04-L3`（身份是状态的前置）的冲突点。

## 约束

- 不把博客/工程观察当论文结论。
- 没有来源的判断标 `推测`。
- 输出写到 `runs/YYYY-MM-DD-<slug>.md`，不直接改 README。
