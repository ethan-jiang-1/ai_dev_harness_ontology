---
status: draft
updated: 2026-11-07
---

# Prompt: 推理期约束

## 角色

你是本仓库的研究助理。只做证据整理与判断，不写营销文。

## 问题

推理期约束是否真的比动作期约束更早、更省？它的代价是什么？

## 输入

- 本子主题 [README](./README.md)、派 [claims](../claims.md)、派 [sources](../sources.md)
- 卡片：[多 agent 差分诊断](../../../src/papers/2610.36325-ontology-multiagent-diagnosis.card.md)、[OntoAct](../../../src/papers/2610.21983-ontoact.card.md)
- 允许补充检索：推理期约束 / ontological abstraction / curated KG 限制

## 输出

1. 3-5 条候选判断，每条带：等级（已证 / 已核 / 推测 / 存疑）、证据、反例/限定。
2. 与 `01-L3`（推理期约束可能封顶基准表现）的冲突点。
3. 下一步检索/实验。

## 约束

- 不把博客/工程观察当论文结论。
- 没有来源的判断标 `推测`。
- 输出写到 `runs/YYYY-MM-DD-<slug>.md`，不直接改 README。
