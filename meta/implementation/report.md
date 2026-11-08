# Pilot Readiness 报告（v0）

> 日期：2026-11-09  
> 结论：**三个试点协议是 v0 draft，不是“今天可开跑”。**  
> 下一步不是继续改文案，而是过 **D0 asset gate**（2 天）：定域/日志/本体 owner/题库/K2 建设人。  
> D0 checklist：[d0-gate.md](./d0-gate.md)。  
> 没有跑真实试点，没有客户数据；所有“可开跑”判断都受此限制。

## 一、产出

| 产物 | 状态 | 说明 |
|---|---|---|
| [experiments/README.md](../../experiments/README.md) | **index** | 6 个实验清单；不再把正文塞 README |
| [EXP-001](../../experiments/EXP-001-structured-artifacts.md) | 设计中 | 从旧 README 拆出 |
| [EXP-002](../../experiments/EXP-002-checker-fp-fn.md) | 未开始 | 从旧 README 拆出 |
| [EXP-003](../../experiments/EXP-003-seam-position.md) | 未开始 | 从旧 README 拆出 |
| [EXP-004](../../experiments/EXP-004-narrow-deep-k1.md) | **v0 draft** | K0/K1/K2；主判 K2−K1；54 trials |
| [EXP-005](../../experiments/EXP-005-action-gate-shadow.md) | **v0 draft** | shadow；false-veto Wilson 上界；不测 task success |
| [EXP-006](../../experiments/EXP-006-ontology-checker.md) | **v0 draft** | 空结果基线；错误子集 5pp；FA 10–15% 不判 |
| [cost-model](./cost-model.md) | **v0** | 公式/输入/敏感性；单价全空；不编价 |
| [pilot-playbook](../../deliverables/pilot-playbook.md) | **v0** | 90 天路线；只重组 E/L；标注条件 |

## 二、三个包的真实状态

### EXP-004 N&D K0/K1/K2

- **能做**：问题、三臂、54 trials、数据表单、go/no-go、2 周排期（含 3 人 D3–4 建 1/10 塔 + 45k 投影）。
- **卡点**：
  1. K2 的 1/10 塔/投影需要 **1 curator + 1 后端 + 1 领域工程师**；没有这 3 个人，2 周跑不出 K2。
  2. n_eff=3 任务；15pp 只作方向性，不能当统计结论；单任务可拉 33pp。
  3. 构建/投影人日无实耗；成本侧仍空。
- **结论**：协议可评审，**不能承诺“2 周一定判 build/no-build”**；先过 D0（人 + 设备 + 任务卡）。

### EXP-005 action-gate shadow

- **能做**：shadow 不执行、false-veto Wilson 上界、blocked 过采样、D0 gate、pair/rater 字段。
- **卡点**：
  1. 需要 **≥500 条带 state_hash 的历史决策**；只有当前态 → 不能回放，先补 logging。
  2. 需要 Layer A v0 owner + legal codebook；没有 → 本 2 周只做本体。
  3. 100 blocked 在保留率 95% 时需扩到 ~2,000 条；协议写了“扩 N”，但没给预算/周次。
- **结论**：协议可评审；**没有日志/本体 owner 就不开跑**。

### EXP-006 checker

- **能做**：空结果基线、错误子集 5pp、FA 三档、100–200 复核、D0 gate。
- **卡点**：
  1. 需要 **200 题题库 + gold + 分层比例**；没有 → 本 2 周只建题库。
  2. 目标 ≥80 错误；200 题若错误率 20% 只有 40 个，需扩到 400–800；排期没排扩样。
  3. 成本门 `per-1k ≤人工 1/3` 需要单价/人时价，当前留空 → 只能判“不出结论”。
- **结论**：协议可评审；**没有题库/单价就不判 go**。

## 三、Critic 的三轮结果

| 轮 | 主要发现 | 已修 |
|---|---|---|
| 1 | EXP-004 用 K1−K0 判建塔；EXP-005 shadow 测 task success；EXP-006 50 条判 FA；cost B 公式错 | 改 K2−K1；去 task success；100–200 复核；B=Q(0.929p_h−0.019)−c |
| 2 | plan/playbook 仍写 K1−K0；EXP-006 5pp 分母；cost C_total 量纲；K2 重复“1/10/全塔” | 统一三臂；错误子集；C_total/T0；K2 是 1/10、go 是全塔 |
| 3 | K2 无构建工序/角色；EXP-005 D0/抽样框；EXP-006 题库/预注册；NPV 周期 | 加 D3–4 三人建塔；D0 gate；题库 D0；Σ_t/N_12 |

**未解决（结构性，非文案）**：
- D0 资产（域/日志/本体 owner/题库/3 人）。
- n_eff=3 / 80 错误的统计功效。
- 单价/人时/事故成本全空。
- 独立人类/客户数据未做。

## 四、Go / No-go

### No-go：今天开跑

- 三个 D0 gate 都未签核；没有域、日志、题库、K2 建设人。
- 样本量只够方向性；不能承诺“2 周判 build/no-build”。
- 成本门多数只能判“不出结论”。

### Go：2 天 D0 asset gate

先做这 5 件事，再决定是否开跑：

1. **定域**：N&D 一台设备；action-gate 一个工具集；checker 一个 KG。
2. **定数据**：N&D 任务卡/描述记录；action-gate ≥500 条带 state_hash 日志；checker 200 题 + gold。
3. **定人**：N&D 1 curator + 1 后端 + 1 领域；action-gate 本体 owner；checker 题库 owner。
4. **定单价**：至少拿到人日价、token 单价、事故成本中 2 项；拿不到就只做 token 账。
5. **定评审**：谁签 D0、谁做盲评、谁仲裁。

D0 全过 → 按 playbook 第 1–2 周开 EXP-004；不过 → 本阶段只交付协议，不跑。

## 四之二、P-gate 审计

| 门 | 结果 |
|---|---|
| P-1 预注册 | pass（v0） |
| P-2 口径 | partial（n_eff/blocked/错误数/FA 功效） |
| P-3 成本 | pass（不编价） |
| P-4 回链 | pass |
| P-5 评审 | partial（AI critic 3 轮；代办评审未覆盖本阶段） |
| P-6 链接 | pass（0 broken） |

详见 [gates.md](./gates.md)。

## 五、文件

- [plan.md](./plan.md)
- [status.md](./status.md)
- [gates.md](./gates.md)
- [cost-model.md](./cost-model.md)
- [pilot-playbook.md](../../deliverables/pilot-playbook.md)
- [experiments/README.md](../../experiments/README.md)
