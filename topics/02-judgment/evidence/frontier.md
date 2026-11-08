# 输出时证据契约 · 未发现与下一步

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | 每个 level 的 precision/recall | 自评等级不能自动放行 | 独立标注 + 校准曲线；**样本量/工期论文未给**（02/checker 的 100–400 条是 checker 部署抽样口径，不能直接搬） | OA-RAG 后续；人工审计 | 高 |
| G2 | 等级通胀的检测 | 若全标 supported，字段就失去区分度（`推测`） | 等级分布 + 抽样；阈值（>90%）目前是工程猜测 | 生产 trace | 中 |
| G3 | 证据粒度（句/结论/整卡） | 论文的 observation 是整卡/绑定，没有文本 span 规定；粒度越细越可核，但标注/引用成本更高（`推测`） | 同任务粒度对照 + 引用单元定义 | 输出契约实验 | 中 |
| G4 | 谁来做等级判定 | 自评 vs 独立判定器 | 独立 reasoner / judge / 人工对照 | 02 checker 线 | 高 |
| G5 | 8k/32k/262k 预算敏感性 | 论文只测 8,192 统一口径 + 262k 下的 i-MedRAGdoc(Qwen)；32k 无实测，digest 的「结论不同」是外推（`推测`） | 同任务三档 context 对照，固定检索与交互预算 | OA-RAG 后续；自测 | 中 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变 | 成本 |
|---|---|---|---|---|
| N1 | 独立等级判定 | `grounding level calibration ontology RAG` | F2 / G1/G4 | 中 |
| N2 | 等级分布作为健康度 | `grounding inflation LLM citation` | F2 / G2 | 低 |
| N3 | 检索覆盖修复 | OA-RAG §6.3.1；`ontology concept card retrieval coverage` | F3 / G3 | 中 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-08 | OA-RAG 深读 | F1–F3 成形；G1–G4 明确 | 先做 G1/G4 |
| 2026-11-08 | G-X 修复（digest 反核） | 删「observations 带 span」「100–400 条校准 × 1–2 人日」；1–2 人日改回 concept card 生成（每本体）、1–2 人周 reasoner；sprint 改 1 周 FoodOn + RAGdoc 对照；V3 改检索率 ≥60%/引用率 ≥85%/准确率 +10pp | 补 F4–F7；span 与校准样本量进 G1/G3 |
| 2026-11-08 | G-X 复修（Appendix A 反核） | 12k → 5,000 generated（Step 2 另 512）/9.7k total；96.7k/22 calls 标 262k 口径；E=∅→`P_own` 不报等级；补 F8 预算 caveat、别用条件、V1 | F5/F8 更新；README 边界 +3 条；G5 |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| 独立 grounding judge | 把自评变成可校准信号 | 待扫描 | N1 |
| concept card 检索 | 补主瓶颈 | 待扫描 | N3 |
