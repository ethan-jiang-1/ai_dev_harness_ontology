# P-gate 审计（Pilot Readiness）

> 对象：EXP-004/005/006、cost-model、pilot-playbook、report。  
> 判据：P-1 预注册、P-2 口径、P-3 成本不编价、P-4 回链、P-5 AI critic+代办评审、P-6 链接。

## 总结

| 门 | 结果 | 说明 |
|---|---|---|
| P-1 预注册 | **pass（v0）** | 3 个 EXP 都有 H1/H0、主分析、不做分析、偏离记录、冻结件；`frozen_at` 仍 pending D0 |
| P-2 口径 | **partial** | 主/过程/非对称/分母都写了；但 n_eff、blocked、错误数、FA 带的统计功效仍不足，已标“方向性/不出结论” |
| P-3 成本 | **pass** | cost-model 单价全空；无自造费率；公式/输入/敏感性可复算到“缺项即不出结论” |
| P-4 回链 | **pass** | EXP ↔ topics/digest/E/L 全可追；playbook 只重组已有 E/L |
| P-5 评审 | **partial** | AI critic 3 轮（含结构性缺口）；用户授权代办评审只覆盖全审 5+5，**未覆盖本阶段 3 个试点**；独立人类 pending |
| P-6 链接 | **pass** | 全仓 1,701 / 0 broken |

**结论**：协议可评审；**执行 no-go，直到 D0 资产签核**。P-2/P-5 的 residual 是“样本/评审”，不是文案。

## P-1 预注册

- EXP-004：H1 K2−K1 ≥15pp；H0 <5pp；主分析 pooled + 逐任务/逐模型 + 3 seeds；不做 K1−K0 判塔。
- EXP-005：H1 false-veto Wilson 上界 ≤5%、保留率 20–95%；H0 上界 >5%；shadow 不测 task success。
- EXP-006：H1 错误子集增量 catch ≥5pp、FA ≤10%、per-1k ≤人工 1/3；H0 <5pp 或 FA >15%。
- 冻结件：协议 + 任务卡/题库 + 预注册表 + 代码/配置 hash；`frozen_at` 待 D0。

## P-2 口径（residual）

| 试点 | 已写 | 仍不足 |
|---|---|---|
| EXP-004 | 主/次/过程/非对称/分母；n_eff=3 | 15pp 只是方向；单任务可拉 33pp；无 CI/MDE |
| EXP-005 | false-veto Wilson；保留率；blocked 分母 | 100 blocked 在 95% 保留率需扩到 ~2,000；扩样预算/周次未排 |
| EXP-006 | 错误子集 5pp；FA 三档；Wilson | ≥80 错误在 200 题需 40% 错误率；20% 需扩到 400–800，排期未排 |

## P-3 成本

- cost-model：CAI `p_min/C_total/B`、action-gate `NPV/TCO`、feasibility 3 个可算；单价全空。
- 规则：缺单价/人时/事故成本 → 只给 token 账 + 敏感性，不给 build/buy 结论。
- residual：真实费率、审批分钟、事故成本仍需组织数据。

## P-4 回链

- EXP-004 → 03/projection、06/feasibility、N&D、E-12/03-L1。
- EXP-005 → 01/action-gate、06/feasibility、POLAR/CASEL、E-15/E-04。
- EXP-006 → 02/checker、02/calibration、Ontology Catch、E-02/02-L6。
- playbook → E-12/E-15/E-02/E-18/C-03；不新增 E。

## P-5 评审（residual）

- AI critic 3 轮：
  - 轮 1：K1−K0 判塔、shadow task success、50 条判 FA、B 公式错。
  - 轮 2：plan/playbook 口径、5pp 分母、C_total 量纲、K2 重复。
  - 轮 3：K2 构建工序/角色、D0/抽样框、题库/预注册、NPV 周期。
- 已修到 v0；**结构性 residual 仍在**：K2 建设人、日志/题库、统计功效。
- 用户授权代办评审此前只覆盖全审 5+5，**不覆盖本阶段**；独立人类 pending。

## P-6 链接

- 最近一次：**1,701 / 0 broken**。
- 修过：EXP 文件 `../../` → `../`；report `../experiments` → `../../experiments`。

## 最终判

- **可评审**：三个协议、cost-model、playbook、report。
- **不可开跑**：D0 资产未签核；P-2/P-5 residual。
- **不可对外**：无客户数据、无独立人类、无试点结果。
