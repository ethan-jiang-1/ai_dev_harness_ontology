---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# 状态：跨轮身份/记忆

> **一句话**：先建 registry，再谈状态。 ｜ **适用**：跨期实体、冲突/失效要保留。 ｜ **证据**：E-05/E-17。 ｜ **边界**：专有数据；false merge 传播未测。

## 3.7 跨轮身份/记忆：能试，但先锚身份

本体在记忆系统里克制到只做对齐与印证条件：alias memory 让 final-period CMR（跨期匹配率）+7.8–12.1pp（4 settings）、reattachment recall +22.5–29.0pp、human-audit CMR +9.0–16.5pp、semantic matching token −40.3%（E-05）。EvoMemState 把记忆分成 Persistent Facts + Relational State + Reasoning State：Complete Retrieval 85.6%（与最好 baseline 相当），但 Acc@complete（完整答案准确率）70.8/68.5（+11.5/+31.2）；去掉状态层掉点（E-17）。

**能做什么**：跨会话、跨期实体知识；需要保留冲突/失效；下游判断依赖历史一致性。

**不能做什么**：不保证跨运行确定性；文本 only、需训练信号；false merge 的长期污染未测；未匹配 ≠ 关系结束。

**距离**：先建 registry，再谈内容/检索；merge precision 与 CMR 一起看；没有自动回滚。
