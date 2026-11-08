# 输出时证据契约 · 未发现与下一步

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | 每个 level 的 precision/recall | 自评等级不能自动放行 | 独立标注 + 校准曲线 | OA-RAG 后续；人工审计 | 高 |
| G2 | 等级通胀的检测 | 全标 supported 会让字段失效 | 等级分布 + 抽样 | 生产 trace | 中 |
| G3 | 证据粒度（句/结论） | 句子级更准但成本高 | 同任务粒度对照 | 输出契约实验 | 中 |
| G4 | 谁来做等级判定 | 自评 vs 独立判定器 | 独立 reasoner / judge / 人工对照 | 02 checker 线 | 高 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变 | 成本 |
|---|---|---|---|---|
| N1 | 独立等级判定 | `grounding level calibration ontology RAG` | F2 / G1/G4 | 中 |
| N2 | 等级分布作为健康度 | `grounding inflation LLM citation` | F2 / G2 | 低 |
| N3 | 检索覆盖修复 | OA-RAG §6.4；`ontology concept card retrieval coverage` | F3 / G3 | 中 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-08 | OA-RAG 深读 | F1–F3 成形；G1–G4 明确 | 先做 G1/G4 |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| 独立 grounding judge | 把自评变成可校准信号 | 待扫描 | N1 |
| concept card 检索 | 补主瓶颈 | 待扫描 | N3 |
