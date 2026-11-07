# Prompt: 生成的可消费性

## 角色

你是本仓库的研究助理。只做证据整理与判断，不写营销文。

## 问题

生成路线的「可消费性」怎么测：判定器能否加载、解释、稳定复现？

## 输入

- 本子主题 [README](./README.md)、派 [claims](../claims.md)、派 [sources](../sources.md)
- 卡片：[OntoDoc](../../../src_notes/cards/2611.01276-ontodoc.md)、[Peeling](../../../src_notes/cards/2610.41785-peeling-matryoshka.md)、[Evontree](../../../src_notes/cards/2510.26683-evontree.md)、[ReX-GG](../../../src_notes/cards/2610.41901-rex-gg.md)
- 允许补充检索：ontology generation evaluation / downstream utility / consumability

## 输出

1. 3-5 条候选判断，每条带：等级、证据、反例/限定。
2. 「可消费性」的最小指标集（加载、解释、复现）。
3. 与 `05-L3`（生成产出候选，不是完备本体）的冲突点。

## 约束

- 不把博客/工程观察当论文结论。
- 没有来源的判断标 `推测`。
- 输出写到 `runs/YYYY-MM-DD-<slug>.md`，不直接改 README。
