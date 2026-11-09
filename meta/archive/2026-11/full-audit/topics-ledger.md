> **历史快照（2026-11-08/09）**：已归档，不再维护。现行规则见 `meta/README.md`，当前状态见 `meta/state.md`。文中的计数与结论可能已被后续修复取代。

# topics 全审 ledger

> A 级定义见 [plan.md](./plan.md) §3.2；Phase 0 基线见 [phase0.md](./phase0.md)。  
> 行在 Phase 2 逐页补齐；未审行不预填。

| T-ID | 子主题 | 当前 A | 核心判断 | 改变哪个决策 | 实施缺口 | 客户指标 | 到 A4 的缺口 | verdict |
|---|---|---|---|---|---|---|---|---|
| T-01 | 01 action-gate | A2 | 安全是结构问题；T1-only≈blanket veto；收益随基线下降；验收应用 harm–approval–cost–task success 前沿 | 验收口径；弱基线硬 veto / 强模型 advisory（后者推测） | 数据契约/日志字段/TCO/组织职责/stop/first sprint；false-veto 未测；F5/01-L9 有失真 | 未定义（候选：不可逆伤害/千次、false-veto、审批/千次、task success） | 受益者/基线/反事实/V3/反例；TCO | Phase 0 基线 A2 |
| T-02 | 02 checker | A2 | checker 先超过空结果重试与随机 flag 基线；curated precision 只略优；catch/FA 分开报 | 建/不建；选 curated/data-derived；验收口径 | 标注规模/成本/FA 预算/catch 目标/停止；per flagged 单位；同源/feedback 等级 | 未定义（候选：拦下真实错误/千次 vs 误判正确/千次） | 受益者/现状/反事实/V3/TCO/反例 | Phase 0 基线 A2 |
| T-03 | 06 feasibility | A2 | 价值是位置×成本×复用×基线能力的属性；编译算 p_h>p_min；分配选前沿；无单一能力曲线 | 上线评审从均值改为盈亏平衡；按审批预算选点；投影只在答案在文本里时建 | 度量契约/ledger 字段/p_h 抽样/c 折算/组织口径；12 机制仅 3 可算；φ/false-veto 无数字；EXP-003 错挂 | 未定义（候选：query-equivalent/千次、p95 时延、审批占比、HSR） | 受益者/基线/反事实/V3/反例；TCO | Phase 0 基线 A2 |
