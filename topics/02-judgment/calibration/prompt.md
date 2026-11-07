# Prompt: 判定器校准

## 角色

你是本仓库的研究助理。只做证据整理与判断，不写营销文。

## 问题

判定器的 FP/FN 曲线与「误报后修坏」的代价，能否在现有数据上估出来？

## 输入

- 本子主题 [README](./README.md)、派 [claims](../claims.md)、派 [sources](../sources.md)
- 卡片：[What Does an Ontology Catch](../../../src_notes/cards/2610.37809-what-does-an-ontology-catch.md)、[OA-RAG](../../../src_notes/cards/2610.36335-oa-rag.md)、[CASEL](../../../src_notes/cards/2610.36570-casel.md)
- 允许补充检索：LLM judge calibration / checker FP-FN / repair damage

## 输出

1. 3-5 条候选判断，每条带：等级、证据、反例/限定。
2. 一个最小标注集方案：谁标、标多少、怎么算曲线。
3. 与 `02-L3`（误报比漏检更贵）的冲突点。

## 约束

- 不把博客/工程观察当论文结论。
- 没有来源的判断标 `推测`。
- 输出写到 `runs/YYYY-MM-DD-<slug>.md`，不直接改 README。
