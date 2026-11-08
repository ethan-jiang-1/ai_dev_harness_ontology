# 生成 · 未发现与下一步

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | 可消费性怎么测 | 生成结构能否被判定器/agent 用 | 加载/解释/复现的评测 | 02 checker / 05 lifecycle | 高 |
| G2 | 最小人工种子 | 冷启动成本 | 种子阶梯实验 | Evontree/OntoDoc | 中 |
| G3 | 来源标记进判定权重 | 专家 vs 模型的约束可信度不同 | 来源标注 + 加权判定 | 02/05 | 高 |
| G4 | 下游任务收益 | 说明更全 ≠ 任务更好 | 生成前后对照 | OntoDoc 后续 | 高 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变 | 成本 |
|---|---|---|---|---|
| N1 | 可消费性评测 | `ontology generation consumability checker` | F1/F3 / G1 | 中 |
| N2 | 来源加权 | `provenance weighted ontology constraint` | F4 / G3 | 中 |
| N3 | 下游对照 | `ontology description downstream task` | F2/F3 / G4 | 高 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-08 | OntoDoc/ReX-GG/Peeling/Evontree | F1–F4 成形；G1–G4 明确 | 先做 G1/G4 |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| 可消费性基准 | 补核心空缺 | 待扫描 | N1 |
| 来源加权判定 | 治理 | 待扫描 | N2 |
