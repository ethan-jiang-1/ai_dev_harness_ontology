---
status: draft
updated: 2026-11-07
---

# 01 约束派 · 局部结论

> 本页是本派的局部判断账本。跨派/对外引用的结论升到 [conclusions](../conclusions.md) 的 E-xx；`01-Lx` 只在本派内使用。

| ID | 判断 | 等级 | 证据 | 备注 |
|---|---|---|---|---|
| 01-L1 | 安全是结构问题：问「是否存在可接受的逆操作序列」 | 已核 | E-04 / POLAR | 本派核心 |
| 01-L2 | 约束类机制的增益随模型基线能力升高而缩小 | 已核 | E-13 | 适用边界 |
| 01-L3 | 推理期约束**限制知识源**（curated KG）可能封顶基准表现；**验证条件**（OntoAct）不一定 | 已核 | 多 agent 诊断 / OntoAct | Q4DX 封顶；OntoAct 提升；约束形式决定天花板 vs 护栏 |
| 01-L4 | 把干预拆成多模式比单一剪枝更省代价 | 已核 | CASEL（模拟） | 六模式；模拟 20 seeds/120k actions；不是部署 |
| 01-L5 | 审批量是护栏的隐性成本 | 已核 | CASEL（模拟） | CASEL 8.7% approvals vs Risk-Menu 12.6% / Consequence 13.8% |
| 01-L6 | T1-only 接近 blanket veto，增益却不比 full 小；结构反向组合的贡献未被隔离 | 已核 | E-04 / POLAR | tier ablation；作者自述 |
| 01-L7 | 可逆性 ≠ 安全性 ≠ 授权；零售退货这类合法用户意图会被误拦，需要意图/授权层 | 推测 | POLAR digest | 机制解释，非作者结论 |
| 01-L8 | 护栏评估应报 harm–approval–cost 前沿，不是单一 HSR：CASEL 7.02% HSR / 8.7% approvals；Risk-Menu 5.82% / 12.6% | 已核 | CASEL（模拟） | 模拟；审批疲劳未建模 |
| 01-L9 | 可逆性路由贡献大部分增益；去掉后 HSR 15.53% ≈ uncertainty gate | 已核 | CASEL（模拟） | ablation |
| 01-L10 | 轨迹风险总账会反噬（HSR 11.82%）；只对不可逆动作记账更稳 | 已核 | CASEL（模拟） | 模拟；ledger 前提 54% 失败 |
| 01-L11 | 验证条件式的推理期约束可同时提高成功率与减少无效干预：Tacit-FLE 78.6–90.0% vs IfR 64.3–65.0%，SI 1.9–2.4 vs 6.4–17.8 | 已核 | OntoAct（模拟） | 三环境；合成/固定 schema |
| 01-L12 | Spurious interventions 是被最终成功率掩盖的指标；应单独报 | 已核 | OntoAct / CASEL | 两篇都强调 |
| 01-L13 | 可推理 ≠ 可授权：`UNVERIFIED` 可进 Planner，但不能当 positive authorization support；需 claim-specific promotion | 已核 | Commit Boundary（概念） | 无实现；设计规范 |
| 01-L14 | 同源检索（hypothesis 诱导的多个结果）不算独立确认；「没检测到冲突」也不是 positive support | 已核 | Commit Boundary（概念） | 上游 dependency lineage 未解决 |
