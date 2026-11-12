> **历史快照（2026-11-08/09）**：已归档，不再维护。现行规则见 `meta/README.md`，当前状态见 `meta/status/state.md`。文中的计数与结论可能已被后续修复取代。

# 价值链（V2/V3）：8 个 A4

> 只对 8 个 A4 做 V2/V3；其余 A3 保留 V2 方向，不强行编客户数字。  
> 规则：没有基线/单价的，标 `推测`；V3 只要求“能设计、能证伪”，不要求现在跑。

| V-ID | 机制 | 受益者/痛点 | 指标/反事实 | 成本/TCO | 证据 | 实验 | 级 |
|---|---|---|---|---|---|---|---|
| V-01 | action-gate 可逆性路由 | 业务/客服/财务/合规；不可逆动作伤害、事后补救贵 | 每千次调用不可逆伤害、false-veto、审批/千次、task success；不做→事故/补救，blanket veto→误拦 | curator 2–5 人日/域、1–2 人周接入、审批 5–15 分钟/次（推测）；无单价 | POLAR +0.11 / T1-only≈blanket；CASEL 模拟 14.75→7.02（τ=∞） | 单域 shadow 200–500 决策；100 blocked 标注；同轨迹配对 A/B；go/no-go false-veto≤5%、Δ>0 | **V3** |
| V-04 | checker 三源权衡 | KG/agent 平台、数据治理/合规；错误答案上线、人工审核贵 | 每千次产出真实语义错误拦截、误判正确、per-1k token/工时；不做→空结果重试+人工抽检 | per-flagged 66k/28k tokens；setup/维护未记录（推测） | Ontology Catch：curated 18.9/16.8、data 8.2/3.5；空结果 79.2/0（人工 fault） | 200 题：空结果基线→data-derived check；增量 catch≥5pp、FA≤10%、成本≤人工 1/3 | **V3** |
| V-07 | compilation（claim–leaf/树/图/wiki） | agent 平台/检索团队；长程检索 token 贵、窗口浪费 | 每千问 query-equivalent、p95、准确率；不做→BM25/grep+原 harness；代价是 token/时延，不是准确率 | 编译一次性 + 维护；论文无金额；c 用编译 token/平均每问 token | CAI −91%/+1.9%/−38%；p_h 43% 是反推；PageIndex FRAMES 负 | 单语料 100–200 问只做 E2；p_h>p_min 且 p95 不超；token 降≥20%、准确率不降 | **V3** |
| V-08 | projection（固定分节文本） | 工厂运维/领域工程师；误诊、重复排障、误设点 | primary-trap 误判率、误设点/千次、排障工时/次、维护人日；不做→K1 命名+单位/文档检索 | 塔 2–4 人周、投影 2–3 人日、维护 0.5–1 人日/月（推测） | N&D +19.8pp（K1→K2）；K1 +54.6pp；物理推导未测 | 1 台设备 9 任务 K1 vs K2；trap +≥15pp、维护≤2 人周/月；否则停 | **V3** |
| V-09 | memory（registry + 两层状态） | 投研/CRM/客服；跨源碎裂、偏好更新、冲突记忆 | CMR、Acc@complete、冲突解决、每请求 token；不做→每次重识别/固定 prompt | registry/人审/维护人周（推测）；token 按域 | FIRME CMR +7.8–12.1pp；EvoMem Acc@complete 70.8/68.5（各自基准） | 单域 200–500 请求；CMR +10pp、Acc@complete +10pp、冲突漏检≤10% | **V3** |
| V-12 | generation（四路线） | 本体/知识图谱团队、新用户/集成方；术语缺说明、上手慢、集成错 | completeness/accuracy、下游加载成功率、找术语时间；不做→人工/naive | 每 IRI token + 人审 10–20%；setup 1–2 人周；维护 0.5–1 人日/月（推测） | OntoDoc 3.43→3.84（LLM judge）；Evontree 报告值 3.1/3.7 不可复算；Peeling/ReX 各有边界 | 40 术语 naive vs 四阶段；+0.3 completeness、accuracy≥4.0、成本≤人工 1/3；否则停 | **V3** |
| V-19 | metrics（配置当系统变量） | 评测/平台/机制 owner；单次分数误导、配置差异被当机制效应 | run-to-run 方差、CI、决策改变率；不做→单次 score/旧尺子 | 账本 3–5 人日、每机制 0.5 人日、抽检 2–3 人日（推测） | Agents：54% variance（真实尝试/过 hurdle）；Information 轴最大 | 200 题、5 runs/config、两臂；结论与旧尺子不同或 CI 收窄过决策点 | **V3** |
| V-20 | feasibility（位置×成本×使能） | 平台/架构/预算 owner；机制都“有效”但不知先上哪个 | NPV/query-equivalent、p_h、审批占比、HSR；不做→按基准均值/厂商 demo 立项 | 逐机制 TCO；单价/工时/事故成本均缺（推测） | CAI p_min；POLAR/CASEL 模拟；12 机制仅 3 可算 | 组合评审：只对 3 个可算机制做 NPV；其余标“不可算/先测分母” | **V3** |

## V3 共同判据

1. **有反事实**：不做/blanket/静态 gate/纯人工，至少一个同口径对照。
2. **有分母**：年查询量、年判断量、年合并数、年术语数；没有分母先测。
3. **有停止线**：收益 < TCO，或安全/准确率硬约束被破。
4. **有失败判据**：不是“效果不好”，而是“在什么条件下不成立”。
5. **不编单价**：没有报价/工时价，只给公式与敏感性，标 `推测`。

## 当前不能签的

- 8 个 V3 都是**试点设计**，没有一个跑过；不能写“已验证客户收益”。
- 成本侧大多只有人日/量级，没有金额；ROI 仍不可算。
- 客户指标是代理指标（CMR、trap、catch/FA、query-equivalent），不是客户财务报表。
