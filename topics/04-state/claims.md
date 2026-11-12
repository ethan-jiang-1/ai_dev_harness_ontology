---
status: draft
updated: 2026-11-08
---

# 04 状态派 · 局部结论

> 本页是本派的局部判断账本。跨派/对外引用的结论升到 [conclusions](../conclusions.md) 的 E-xx；`04-Lx` 只在本派内使用。

| ID | 判断 | 等级 | 证据 | 备注 |
|---|---|---|---|---|
| 04-L1 | 记忆是状态，不是事实集合；两层状态（Relational + Reasoning）在消融中各有贡献（MemSyco/MemTrap），完整系统在 4 个记忆基准上评测；Acc@complete 70.8（LoCoMo-Refined，+11.5）/ 68.5（MemSyco，+31.2），Complete Retrieval 85.6% 与 MemoryBank 86.4% 相当 | 已核 | E-17 / EvoMemState | 文本 only；需训练信号；Reasoning State 不可形式验证 |
| 04-L2 | 本体在两篇里都不承担自由推理；FIRME 的固定本体只承担对齐/印证条件，「改动只影响槽位」无对照、为推断；EvoMem 的本体则增量构建并修订层级 | 已核（用法）/ 推测（改动范围） | E-05 / FIRME / EvoMemState | FIRME §3.2/6.5；EvoMem §3.1/5.6 |
| 04-L3 | 身份是状态的前置：registry 锚定把跨期观察挂到同一段历史；Full vs LLM-Norm 的 final-period CMR 高 2.3–3.7×，alias 复用再 +7.8–12.1 pp（4 settings） | 已核（对照/增量）/ 推测（无身份对照） | FIRME §5、Table 3/4、Table A2 | 无「完全不做身份对齐」对照组；registry/alias/semantic fallback 分别贡献未拆分；human-audit CMR +9.0–16.5 pp；semantic matching token −40.3%（仅 investor×Opus×final period） |
| 04-L4 | 跨运行一致性可由结构投影度量（**设计提案，不是判断**；未验证） | 推测 | determinism（设计提案） | RQ3；投影覆盖率/归因规则待实测 |
| 04-L5 | 错误合并的「长期污染」是机制推断：false merge 会把后续同名观察路由到错误 anchor；传播幅度论文未测，也无自动回滚。已测的只是 merge precision 85.6–97.5%（4 settings，200 units/setting 抽样） | 推测（污染）/ 已核（precision 口径） | FIRME §5/§9、Table A2 | precision 是「被接受匹配的正确率」，不是污染幅度；与 CMR 同看 |
| 04-L6 | 未匹配 ≠ 关系结束：衰减不删除、Fading 可 Reactivated；但 miss 也可能是输入缺失 | 已核 | FIRME | 作者自述 |
| 04-L7 | 记忆评估分三层：CMR、human audit、抽取保真/round-trip；三层不可互替 | 已核（分层/数字）/ 推测（不可互替） | FIRME | round-trip F1 0.786–0.931（依语料/backend）；幻觉 3.3–7.4%、归一化误差 3.2–22.16%（无 backend 全面占优） |
