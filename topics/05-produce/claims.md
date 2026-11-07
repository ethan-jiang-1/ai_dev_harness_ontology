---
status: draft
updated: 2026-11-07
---

# 05 生产派 · 局部结论

> 本页是本派的局部判断账本。跨派/对外引用的结论升到 [conclusions](../conclusions.md) 的 E-xx；`05-Lx` 只在本派内使用。

| ID | 判断 | 等级 | 证据 | 备注 |
|---|---|---|---|---|
| 05-L1 | 来源决定可信度；来源标记要进判定 | 推测 | 分析 | 否则判定器无法继承可信度 |
| 05-L2 | 精化可自动化到小规模：CASTON high-confidence 6/6 接受；pretrained ensemble 57.1%；GPT-4o mini 31.3% | 已核 | CASTON | 单一本体/6 条；medium 全 mixed |
| 05-L3 | 生成产出候选，不是完备本体 | 推测 | 分析 | 缺「可消费性」评估 |
| 05-L4 | 表示不是瓶颈，执行才是 | 推测 | SFE-O | OWL 能表达但跑不起来 |
| 05-L5 | 精化瓶颈是定位与验证：embedding 缩候选 + LLM 局部判断；medium 不可靠 | 已核 | CASTON | 未闭环到下游错误 |
| 05-L6 | 生成说明时，「先写 assumptions 再写描述」显著提升完整性：win 54–61%；completeness 3.43→3.84 | 已核 | OntoDoc | 151 terms/3 KGs；无下游任务 |
| 05-L7 | 说明质量 ≠ 可消费性：OntoDoc 没有测下游任务；文档变好不代表判定器/用户能用 | 推测 | OntoDoc | 作者也未声称 |
