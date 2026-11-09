# Pilot Readiness · status

> 计划：[plan.md](./plan.md)。  
> 状态：Phase 0–5 的 v0 已完成；D0 资产门未过，试点暂不可开跑。3 个 EXP 逐个建，不并行开三个半成品。

## Phase

| Phase | 内容 | 状态 |
|---|---|---|
| 0 | 冻结试点组合/模板/status | **完成** |
| 1 | EXP-004 N&D K0/K1/K2 | **v0 draft** |
| 2 | EXP-005 action-gate shadow | **v0 draft** |
| 3 | EXP-006 checker | **v0 draft** |
| 4 | cost-model + pilot-playbook | **v0** |
| 5 | critic/代办评审 + report | **v0 完成；D0 未过** |

## 质量门

- P-1 预注册：每个 EXP 先写“会推翻什么”+ stop。
- P-2 口径：主指标/过程指标/非对称代价/分母；稀疏事件给样本量。
- P-3 成本：单价留空，不自造费率。
- P-4 回链：EXP ↔ topics/digest/E/L。
- P-5 评审：AI critic + 用户授权代办；独立人类/客户数据 pending。
- P-6 链接：0 broken。

## 当前结论

- 试点组合冻结为 3 个：N&D K1（最便宜）、action-gate shadow、checker。
- D0 gate：[d0-gate.md](./d0-gate.md)（2 天；域/数据/人/单价/评审）。
- 三个协议 v0 已落（含预注册 v0，D0 后冻结）：[EXP-004](../../experiments/EXP-004-narrow-deep-k1.md)、[EXP-005](../../experiments/EXP-005-action-gate-shadow.md)、[EXP-006](../../experiments/EXP-006-ontology-checker.md)。
- 阶段报告：[report.md](./report.md)。结论：**不是今天可开跑**；先过 D0 asset gate（域/日志/题库/3 人/单价）。
- P-5 critic 3 轮；剩余为结构性资产，不是文案。
- P-gate 审计：[gates.md](./gates.md)：P-1 pass(v0)、P-2 partial、P-3 pass、P-4 pass、P-5 partial、P-6 pass。
- 不跑真实试点；产出是“可开跑”的协议与表单。
- 独立人类/客户数据未完成，report 只能写“可开跑/缺口”，不能写“已验证”。

## Blocked（2026-11-09）

- **阻塞条件**：D0 asset gate 未签核——具名域、≥500 条带 state_hash 日志、200 题+gold、K2 的 3 人、单价/人时，均未提供。
- **连带 partial**：P-2 统计功效（n_eff=3、100 blocked、≥80 错误）与 P-5 独立评审（代办评审未覆盖本阶段）。
- **已完成**：3 个 EXP v0（含预注册）、cost-model、pilot-playbook、D0 gate、report、P-gate 审计；链接 1,704/0。
- **解除条件**：用户/团队完成 [d0-gate.md](./d0-gate.md) 并回填；或明确接受“v0 协议作为最终交付”，把 goal 改成“交付 v0”而非“可开跑”。
- **不再做**：没有 D0 资产时，不继续改协议措辞；不伪造日志/题库/单价/人类评审。
