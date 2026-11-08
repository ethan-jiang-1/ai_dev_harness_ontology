# 试点就绪计划（Pilot Readiness）

> 一句话：把 3 个“条件 go”变成 **可预注册、可执行、可判 go/no-go** 的 2 周试点包；不扩论文，不编客户数字，不把“设计”写成“已跑通”。

## 0. 起点

- 全审已完成：22/22 digest E3+、12/12 L3 E4、20/20 topic A4、G-X 20/20、8 个 V3 设计。
- 报告：[条件 go（仅内部试点）/ 对外 no-go](../full-audit/report.md)。
- 已选 3 个试点：
  1. N&D：K1 命名+单位（最便宜，先做）。
  2. action-gate：shadow 可逆性路由。
  3. Ontology Catch：data-derived checker。
- `experiments/` 只有 EXP-001/002/003 的旧设计，**这 3 个还没有协议**。

## 1. 目标

| 产物 | 路径 | 判据 |
|---|---|---|
| EXP-004 N&D K1 | `experiments/EXP-004-narrow-deep-k1.md` | 有预注册、变量/对照、样本量、stop、数据表单 |
| EXP-005 action-gate shadow | `experiments/EXP-005-action-gate-shadow.md` | 同上；false-veto 可标 |
| EXP-006 checker | `experiments/EXP-006-ontology-checker.md` | 同上；空结果基线、catch/FA |
| 成本工作簿 | `meta/implementation/cost-model.md` | 公式/输入/敏感性；单价留空，不编 |
| 试点 playbook | `deliverables/pilot-playbook.md` | 90 天路线、角色、数据、go/no-go；只引 E/L |
| 阶段报告 | `meta/implementation/report.md` | 3 个包可否开跑；未跑/未审写明 |

## 2. 不做什么

- 不跑真实试点、不接客户数据、不写“已验证收益”。
- 不扩论文、不改 digest（除非发现事实冲突）。
- 不把 3 个试点写成“全公司路线”；它们只是最便宜的三个验证点。
- 不新增 topics 结论；playbook 只重组已有 E/L。

## 3. 每个 EXP 的必备结构

1. **要回答什么**：一句可判定的话。
2. **会推翻什么**：先写“若 A 则哪条判断降级/改写”；写不出就不做。
3. **变量/对照**：主变量、对照臂、被控混淆项。
4. **度量**：主指标 + 过程指标 + 非对称代价；写清分母。
5. **样本量/功效**：至少给“能分辨多大效应”的算术；稀疏事件给最低样本/窗口。
6. **数据表单**：字段级 schema；谁填、何时填。
7. **go/no-go**：成功/失败/不出结论三档；停止线。
8. **2 周排期**：D1–D10，交付物、角色。
9. **会改变哪个决定**：build/buy/不做，或阈值/流程。
10. **回链**：对应 topics/digest/E/L。

## 4. 三个试点的核心设计

### EXP-004 · N&D K0/K1/K2

- **问题**：K2（塔+投影）相对 K1（命名+单位）的 primary-trap avoidance 是否 ≥15pp；K1 相对 K0 是否已拿到大部分收益？
- **对照**：K0 原样 vs K1 命名/单位 vs K2 塔+45k 投影；三臂同任务/模型/judge。
- **主指标**：K2−K1；次指标：K1−K0、element score、排障工时/次。
- **样本**：3 任务 × 2 模型 × 3 臂 × 3 seeds = 54 trials；有效 n 是 3 任务，trial 不是。
- **go**：K2−K1 ≥ +15pp、≥2/3 任务同向、3 seeds 同向 → 进 **全塔建设**（K2 臂本身是 1/10 试点塔，不是全塔）。
- **stop**：K2−K1 < +5pp → 不建塔，只做 K1；K1−K0 < +5pp 且 K2−K1 < +5pp → 先修数据/任务。
- **关键**：先证明“塔的边际值”，不是拿 K1 的增益替代塔的边际。

### EXP-005 · action-gate shadow

- **问题**：可逆性路由在 shadow 中能否把 false-veto 控制在 5% 内？task success 留到 Stage 2。
- **对照**：无门（记录）vs 门（shadow veto，不执行）；同轨迹配对。
- **主指标**：false-veto（blocked 中本可合法执行的比例）；次指标：保留率、审批/千次、prevented harm（若有标签）。
- **样本**：200–500 决策；100 条 blocked 人工标；稀疏事件不判 HSR。
- **go**：false-veto 的 Wilson 95% 上界 ≤5%、保留率 20–95%、100 条 blocked、κ≥0.6。task success 不在 shadow 判。
- **stop**：false-veto >5%、保留率 <20%/>95%、状态投影不可得。
- **关键**：不接线上写权限；没有 false-veto 标签就不算过关。

### EXP-006 · Ontology Catch checker

- **问题**：data-derived checker 能否在空结果重试之上，提供 ≥5pp 增量 catch 且 FA ≤10%？
- **对照**：空结果重试 vs 空结果重试 + data-derived check；同 200 题。
- **主指标**：增量 catch（有结果但答错）；次指标：FA、per-1k token/工时、告警处置。
- **样本**：目标 500 条决策，blocked 过采样到 100 条；复核 100–200 条正确题；混合集比例预注册。
- **go**：增量 catch ≥5pp、FA ≤10%、per-1k ≤人工 1/3；否则停。
- **stop**：增量 <5pp 或 FA >15%；语义错为主 → 换 LLM judge/人工。
- **关键**：先建空结果基线；不要把 curated 的 precision 与真实 catch 拼在一起。

## 5. 成本工作簿（不编价）

`cost-model.md` 只做三件事：

1. **CAI**：`p_min=2%+c/(0.929Q)`；输入 `T_doc, T0, D, Q, c, p_h, δ`；敏感性：miss ±1.5pp、T0 5k–20k。
2. **action-gate**：`NPV_build = Σ(伤害节省 − 审批成本 + task success 收益)/(1+r)^t − TCO`；输入 `cost_per_incident, minutes_per_approval, hourly_rate, value_per_success, r`；全空，只给公式/敏感性。
3. **feasibility**：12 机制里 3 个可算（CAI/POLAR/CASEL）；其余标“不可算/先测分母”。

规则：**任何单价没有出处就留空**；工作簿里出现自造费率即 fail。

## 6. Playbook（只重组，不新增）

`deliverables/pilot-playbook.md`：

- 90 天路线：第 1–2 周 N&D K1；第 3–4 周 action-gate shadow；第 5–6 周 checker；第 7–12 周复盘/扩展。
- 每个试点：owner、数据、指标、stop、交付物、决策会。
- “不要做”清单：CAI 全量编译、Evontree 训练、generation 四路线全做。
- 只引 E-xx/L-xx；不新增判断；标注 `推测`/未跑。

## 7. 质量门

| 门 | 要求 |
|---|---|
| P-1 预注册 | 每个 EXP 先写“会推翻什么”+ stop；没有就不做 |
| P-2 口径 | 主指标/过程指标/非对称代价/分母写清；稀疏事件给样本量 |
| P-3 成本 | 单价留空；无自造费率；敏感性可复算 |
| P-4 回链 | EXP ↔ topics/digest/E/L 可追；playbook 不新增判断 |
| P-5 评审 | AI critic + 用户授权代办评审；独立人类/客户数据仍标 pending |
| P-6 链接 | 0 broken |

## 8. 排期

| Phase | 内容 | 轮次 |
|---|---|---|
| 0 | 冻结试点组合、模板、status | 2–3 |
| 1 | EXP-004 N&D K0/K1/K2 | 4–6 |
| 2 | EXP-005 action-gate shadow | 4–6 |
| 3 | EXP-006 checker | 4–6 |
| 4 | 成本工作簿 + playbook | 4–6 |
| 5 | critic/代办评审 + report | 3–4 |
| 合计 | | 21–31，留 buffer 到 50 |

## 9. 完成定义

- 3 个 EXP 都有预注册、样本量/功效、数据表单、go/no-go、2 周排期。
- 成本工作簿可代入，但**不编单价**；敏感性可复算。
- playbook 可给工程负责人直接排期；只引已有 E/L。
- `meta/implementation/report.md` 明确：可开跑 / 仍缺什么 / 未跑未审。
- 独立人类与客户数据未完成 → 仍不能写“已验证收益”。

## 10. 与全审的关系

- 全审回答“判断是否站得住”；本阶段回答“试点能不能开跑”。
- 不重开全审；除非 EXP 发现 digest 事实错误，才回 `src/` 修。
- 试点结果出来前，report 保持“条件 go（内部试点）/ 对外 no-go”。
