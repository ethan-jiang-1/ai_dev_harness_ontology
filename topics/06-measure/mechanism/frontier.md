# 机制尺子 · 未发现与下一步

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | 跨模型族 | 只 Qwen3；Llama/GPT 未测 | 同协议跨模型 | MIOE 后续 | 高 |
| G2 | 更丰富公理 | disjointness/domain-range 未测 | 新基准 | 本体工程 | 高 |
| G3 | 干预位置 | 只 subject token | attention/MLP/其他 token | 机制实验 | 中 |
| G4 | 表示 vs 方法 | 「部分分离」原因未定 | 更强干预/方法对照 | 机制研究 | 高 |
| G5 | 下游效用 | 机制指标能否筛可信判断 | 下游任务对照 | 02/05 | 高 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变 | 成本 |
|---|---|---|---|---|
| N1 | 跨模型 | `mechanistic interpretability ontology Llama` | F1/F2 / G1 | 高 |
| N2 | 更强干预 | `causal intervention ontology representation` | F2/F3 / G4 | 高 |
| N3 | 下游筛选 | `mechanism metric trustworthy ontology judgment` | F2 / G5 | 中 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-08 | MIOE 深读 | F1–F5 成形；G1–G5 明确 | 先做 G4/G5 |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| 跨模型机制 | 外推 | 待扫描 | N1 |
| 机制指标筛选 | 工程用 | 待扫描 | N3 |
