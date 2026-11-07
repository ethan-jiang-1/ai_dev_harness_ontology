---
status: draft
updated: 2026-11-07
rq: [RQ3]
---

# 04 状态派 · 前沿与挖掘

> 活页。稳定判断见 [README](./README.md)；证据见 [notes](../../src_notes/)；时刻位置见 [seams](../seams.md#六个时刻)。

## 这一派现在的前沿问题

1. **状态结构能否由本体自动生成**？若可以，本体必须先于任务存在——这是冷启动的硬约束。
2. **冲突该阻塞推进，还是带冲突推进并标注**？两种产品语义，缺对照。
3. **记忆压缩与上下文压缩是同一问题吗**？若是，可共用“判据保护”机制。
4. **FIRME 的“对齐与印证条件”怎么实现**？确定性状态机的原文细节还没核。
5. **跨运行一致性**（RQ3）如何度量：把产物投影到本体结构后，漂移怎么算、阈值怎么定？

## 信号源

- **Benchmark**：长期对话/记忆使用基准、个人 agent 记忆评测、跨期实体对齐数据。
- **会议/期刊**：ACL、EMNLP、NeurIPS、CIKM、ISWC。
- **实验室/团队**：FIRME（Vanguard）、EvoMemState（厦门大学等）、entity resolution / registry 线。
- **工程侧**：memory layer、CRM/投研知识库、entity resolution 的产品复盘。
- **arXiv**：cs.CL / cs.AI / cs.IR / cs.DB。

## 检索式

- `ontology memory state agent`
- `registry anchored memory graph`
- `temporal entity alignment agent memory`
- `memory conflict resolution LLM`
- `agent determinism repeated runs`

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| FIRME（2610.40482） | 跨期身份 + 来源/时间；克制用法 | 已入档 | 回正文核状态机与“印证条件” |
| EvoMemState（2611.03743） | 关系状态 + 推理状态两层 | 已入档 | 补“检索完整性/grounded 准确率”数字 |
| 记忆一致性基准 | RQ3 的度量载体 | 待扫描 | 用检索式 5 |
| 冲突处理线 | 阻塞 vs 标注 | 待扫描 | 用检索式 4 |
| entity resolution + registry 线 | FIRME 的近邻 | 待扫描 | 雪球一层 |
| APEX-MEM（2604.14362，ACL 2026） | 本体属性图 + append-only + 检索时冲突消解；LOCOMO 88.88%、LongMemEval 86.2% | 摘要已读 | 落盘 + 建卡；对照 FIRME/EvoMemState |
| TRiM-KG（NaNA 2026） | 时序记忆 KG | 待扫描 | 读摘要 |
| Time is Not a Label（2604.11544） | 连续相位旋转的时序 KG/agent memory | 待扫描 | 读摘要 |
| AriadneMem（2603.03290） | 终身记忆 | 待扫描 | 读摘要 |

## 入档判据

- 报告 **冲突处理、身份漂移、重复运行收敛** 中的至少一个。
- 有可复现的记忆结构，而不只是“用了知识图谱”。
- 会改变 E-05 的限定，或给 RQ3 一个可操作的度量。

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-07 | 本地 20 篇复筛 | FIRME 的“不做推理”已修正；“状态机”仍缺出处 | 回正文 + 候选队列 |
| 2026-11-07 | 首轮外部扫描（web） | 4 个候选；APEX-MEM 摘要已读 | 入队；top 1 待落盘/建卡 |

## 本轮计划

> 2026-11-07 首轮外部扫描已完成；下一步从候选队列里选 top 1-2 落盘 + 建卡。

1. 读 FIRME 正文，补状态机/确定性更新规则与“双模态互证”的原文。
2. 用检索式 5 找重复运行/漂移度量。
3. 设计一个最小实验：同一输入跑 N 次，投影到本体结构比差异。
