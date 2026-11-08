---
status: draft
updated: 2026-11-08
---

# 01 约束派 · 局部结论

> 本页是本派的局部判断账本。跨派/对外引用的结论升到 [conclusions](../conclusions.md) 的 E-xx；`01-Lx` 只在本派内使用。

| ID | 判断 | 等级 | 证据 | 备注 |
|---|---|---|---|---|
| 01-L1 | 安全是结构问题：问「是否存在可接受的逆操作序列」，而不是让模型给安全标签 | 已核 | E-04 / POLAR | 本派核心；只到「有逆序列」，不保证逆执行成功，也不判意图/授权 |
| 01-L2 | 约束类机制的增益随模型基线能力升高而缩小 | 已核 | E-13 / POLAR | 六点描述性拟合，给不出零交叉阈值；证据仅 POLAR 三域六模型，不能当所有约束机制的能力曲线 |
| 01-L3 | 推理期约束的形式决定天花板/护栏：限制知识源（curated KG）可能封顶（Q4DX 上 Jaundice/Vertigo 恒 0）；验证条件（OntoAct 三值逻辑）不一定封顶 | 已核 | OntoAct / 多 agent 诊断 | 两项任务形态不同，不是头对头；elimination 上 IfR 匹配/超过 OntoAct |
| 01-L4 | 多模式分配不是单轴更省：CASEL 相对 Uncertainty-Menu 审批更多（8.7% vs 6.9%）、task success 低 1.78 pp；相对 Risk-Menu 是「相近 harm、审批少约 30%」 | 已核（模拟） | CASEL | 20 seeds/120k actions；主表 τ̂=∞；γ_m 假设；不是部署 |
| 01-L5 | 审批量是护栏的隐性成本：CASEL 8.7% vs Uncertainty 6.9% / Risk 12.6% / Consequence 13.8% | 已核（模拟） | CASEL | 审批疲劳未建模；不能只看 HSR |
| 01-L6 | T1-only 接近 blanket veto，增益却不比 full 小；结构反向组合的贡献未被隔离 | 已核 | E-04 / POLAR | 作者自述；需同轨迹配对 |
| 01-L7 | retail return/exchange 在 block log 里最多（150/103 次），但没有 harm/授权标签，不能判定是否误拦；合法意图需要意图/授权层 | 推测 | POLAR digest | 机制解释，非作者结论；false-veto 未测 |
| 01-L8 | 护栏评估应报 harm–approval–cost 前沿，不是单一 HSR：CASEL HSR 7.02% / 审批 8.7%；Uncertainty 14.75% / 6.9%；Risk 5.82% / 12.6%；Consequence 4.38% / 13.8% | 已核（模拟） | CASEL | 主表 τ̂=∞；不是所有方法同 menu/cost；task success 也要报 |
| 01-L9 | CASEL-NoRev 是 verify-only，同时去掉 sandbox/approve；15.53% 不能单归因给「可逆性路由」，其贡献未被隔离 | 已核（模拟；消融口径） | CASEL | 旧读「可逆性路由贡献大部分增益」作废 |
| 01-L10 | full ledger 在 harm–compute 面被支配，但在低审批端（4.3% approvals / 11.82% HSR）仍是前沿点；「只对不可逆动作记账」未验证 | 已核（模拟） | CASEL | 54% 直接执行步骤 p_t c_t > r̄_t，ledger 前提失败 |
| 01-L11 | 验证条件式推理期约束在 Tacit-FLE 三个规模上同时提高成功率、减少无效干预：small 78.6 vs IfR 64.3、medium 83.3 vs 66.7、large 90.0 vs 65.0；SI 1.6–2.4 vs IfR 6.4–17.8 | 已核（模拟） | OntoAct | Tacit-FLE 三个规模；Mars/ALFWorld 同向；合成/固定 schema；elimination 上 IfR 匹配/超过，不能推广为「验证条件总是更好」 |
| 01-L12 | Spurious interventions 是被最终成功率掩盖的指标；应单独报 | 已核 | OntoAct / CASEL | 两篇都强调；CASEL 另报 approvals/coverage |
| 01-L13 | 可推理 ≠ 可授权：`UNVERIFIED` 可进 Planner，但不能当 positive authorization support；需 claim-specific promotion | 已核（概念） | Commit Boundary | 无实现；设计规范，不是效果证据；未升 E |
| 01-L14 | 同源检索（hypothesis 诱导的多个结果）不算独立确认；「没检测到冲突」也不是 positive support | 已核（概念） | Commit Boundary | 上游 dependency lineage 未解决；未升 E |
| 01-L15 | 推理期条件闸门只拦有适用 axiom 的动作；缺证据转 unresolved/观察，不是覆盖所有动作的安全保证 | 已核 | OntoAct / 多 agent 诊断 | 覆盖率是缺口（reasoning-gate F4/G1）；三环境模拟；作者明确不声称可部署 |

> **跨页缺口（本次不动 conclusions）**：Commit Boundary 仍是概念架构，未升 E；`conclusions` 的 E-05 属 FIRME，不属于本派，`src/papers/2610.37407-commit-boundary/digest.md` 的 `claims: [E-05]` 是错挂。`E-16` 仍写 Tacit-FLE `64.3–65.0%` / SI `1.9–2.4`，与 OntoAct digest 的 `64.3/66.7/65.0`、SI `1.6–2.4` 不一致；01-L11 已按 digest 校正。
