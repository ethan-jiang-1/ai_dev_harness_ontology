# 全审报告（条件式）

> 日期：2026-11-08  
> 结论：**条件 go（仅内部试点/研究）；对外交付 no-go。**  
> 原因：digest G-X 20/20、topic A4 20/20；Phase 4 抽样 4/5 digest pass + CAI explained-residual；用户授权 AI 代办 5+5 评审，结论为条件 go，但**不是独立人类 sign-off**；客户价值 V3 全部是试点设计，未跑。

## 一、硬指标

| 项 | 结果 | 说明 |
|---|---|---|
| digest E3+ | **22/22** | 全部有工程配方/成本/stop/first sprint |
| L3 E4 | **12/12** | 有成本/收益公式、替代方案、V3 |
| topic A3+ | **20/20** | 全部有实施含义 |
| topic A4 | **20/20** | 全部有客户指标/反事实/V3 |
| G-X 吸收 | **20/20 pass** | 每 topic 核心 claim 可追 digest；无 orphan |
| 8 个 A4 V3 | **8/8 设计** | 未跑，全部 `推测` |
| 链接 | **1,628 / 0 broken** | 全仓 |
| 人类抽检 | **代办 10/10；独立人类 0/10** | 用户授权 AI 代办，不能写 human sign-off |

## 二、Phase 4 抽样（5 digest + 5 topic）

### digest（工程向）

| 论文 | verdict | 关键 residual |
|---|---|---|
| CAI | **fail → explained-residual** | 门/样本量/stop 已修；仍缺 $/文档/人日费率、sprint 工时、E3 决策门经济性；token 侧只有算例，不能报批 |
| N&D | **pass** | 已补 15/5 出口、功效 caveat、成本对齐、可追溯限定 |
| Ontology Catch | **pass** | stop 的混合集比例/unknown 率未定义；setup 预算缺 |
| Evontree | **pass** | 已补 Table 6 消融、产率/规模、三档安全 stop |
| SLB | **pass** | placeholders 防泄漏条款缺；50 题准确率 ≤2pp 功效不足；audit-only 无内容 |

### topic（实施/价值向）

5/5 **pass**，但都有补强项：action-gate（NPV 量纲/ vs Risk 的 HSR +1.2pp）、checker（采纳门 vs V3 两把尺）、generation（可消费性闸门不可判）、feasibility（V3 单臂/缺基线）、metrics（稀有事件样本量不足）。

## 二点五、代办评审（用户授权，2026-11-08）

- 性质：**AI delegated review，不是独立人类审稿**；用户明确授权我代办。
- 范围：5 digest + 5 topic（见 [human-review.md](./human-review.md) §七）。
- 结果：D1 CAI 条件 pass；D2 N&D pass；D3 Evontree 条件 pass；D4 Ontology Catch pass；D5 SLB 条件 pass；5 topic 全 pass（带条件）。
- 关键修正：action-gate / feasibility 的 task-success 收益分母从 `×1000` 改为 `×1000/L`，避免 20 倍高估。
- 限制：仍建议在对外交付前做一次真正的人类 spot-check；代办评审不能替代。

## 三、Go / No-go

### 条件 go（仅内部试点/研究）

只启动 3 个试点，不对外承诺客户收益：

1. **action-gate shadow**：200–500 决策、100 blocked 标注、同轨迹配对；false-veto ≤5% 才继续。
2. **N&D K1→K2**：1 台设备、3 任务、先做 K1 命名+单位；K2−K1 ≥15pp 才建塔。
3. **Ontology Catch checker**：200 题、空结果基线 + data-derived check；增量 catch ≥5pp、FA ≤10% 才继续。

其余：digest 的工程配方、G-X 20/20、8 个 V3 可支撑选题/实验设计；结论账本已收 E-07/E-10/E-12/E-16/E-18 的限定。

### No-go（对外交付/客户承诺）

1. **CAI 未过工程 critic，已标 explained-residual**：不是措辞，是 $/文档/人日费率、sprint 工时、E3 决策门经济性缺失；N&D/Evontree 已修过。
2. **代办评审不是独立人类**：5+5 由 AI 按用户授权完成；对外交付前仍建议人类 spot-check。
2. **人类 5+5 抽检未做**；LLM critic 不能替代。
3. **V3 全部未跑**：客户指标是代理指标，没有金额/基线；不能写“已验证收益”。
4. **成本侧仍缺单价/工时/事故成本**；ROI 不可算。
5. **Phase 4 是抽样，不是全审**：5 digest/5 topic，不能外推到 22/20。

## 四、明确 residual（下一步只修这些）

### R-1 CAI

- 把 2% 门改为“shadow 流量标定后再用”；p_h 样本量按 1,600–2,000 问或生产累计。
- sprint 先编译、再算 p_h、再 A/B；补准确率非劣效边界。
- 成本加 $/文档、token/文档、人日。

### R-2 N&D

- sprint 出口改为 ≥15pp / <5pp（与 V3 一致），不用无阈值“K2>K1”。
- 投影 2–3 人日 vs 2 天排期对齐；评估预算含 ground-truth/trap/rubric。
- “可追溯”从采用理由删除，或改为“查询工具可追溯、但调用率低”。

### R-3 Evontree

- 补 Table 6 消融：full implicit 60.0、w/o gap 59.7、w/o reliable 59.8、w/o ontology 59.4；gap/reliable 边际 ~0.3–0.5pp，不能把 +2.1pp 全归规则。
- sprint 规模：1 万 raw≈90 gap，低于 gap<500 停线；要么 3–6 万 raw，要么改小样本停线。
- stop 统一：安全 >5pp 停、sprint 出口 ≤2pp、V3 失败 >5pp 三处冲突要合成一张表；+1pp 出口要写参照与 seeds/CI。

### R-4 人类抽检

- 5 digest + 5 topic；重点 CAI/N&D/Evontree 与 action-gate/checker/feasibility。
- 只判断“是否值得实施”，不替 AI 校对全文。

## 五、下一步

1. 按 R-1/R-2/R-3 修 3 篇（一个子领域批次，不再逐条开循环）。
2. 人类 5+5 抽检。
3. 重跑 Phase 4 这 3 篇 + 3 topic；全 pass 才把 report 改成“交付 go”。
4. 否则保持 no-go，把 residual 写进 `frontier`，不硬签。

## 六、文件

- [status.md](./status.md)
- [subdomains/](./subdomains/README.md)
- [gx-issues.md](./gx-issues.md)
- [absorption-matrix.md](./absorption-matrix.md)
- [value-trace.md](./value-trace.md)
- [plan.md](./plan.md)
