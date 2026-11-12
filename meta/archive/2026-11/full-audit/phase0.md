---
status: superseded
updated: 2026-11-08
---

> **历史快照（2026-11-08/09）**：已归档，不再维护。现行规则见 `meta/README.md`，当前状态见 `meta/status/state.md`。文中的计数与结论可能已被后续修复取代。


# Phase 0 · 校准记录

> 目的：用 3 篇 digest + 3 个 topic 校准 E/A 量表，判断“E3/A3 是否可操作”，并记录基线缺口。  
> 人类 sign-off：静默模式下暂缓；以 AI 双视角校准替代，最终 Phase 4 再请人类抽检。

## 样本

| 类型 | 样本 |
|---|---|
| digest | MIOE（2610.38326）、CAI（2610.41172）、CASEL（2610.36570） |
| topic | action-gate（01）、checker（02）、feasibility（06） |

## E 分（digest 工程度）

| 论文 | 当前 | 到 E3 的主要缺口 | 到 E4 的主要缺口 |
|---|---|---|---|
| MIOE | **E2** | 缺 stop condition；缺训练超参（epoch/batch/lr/seed/卡）；缺 hook/仓库接口；缺数据规模外推；Cause/Iso 反向权衡未写；Iso 可评估池未量化；pair 构造易误读 | 无 GPU 小时/人日/金额；无下游收益；无替代方案；无客户价值假设/失败判据；0.59 无参照线 |
| CAI | **E2** | 接口只到功能描述（缺工具 schema/claim 索引/返回字段）；缺 topN=20、k=100、anchor 20；p_h 与 E3 决策门混名；c/φ 的测法缺失；缺人时 | 无受益者/业务指标；无绝对成本；无替代方案（改 harness/压缩/缓存/更便宜模型）；无 build/buy 边界；无 V3 |
| CASEL | **E2** | 缺控制器接口/返回结构；缺 γ_m/k/q 的标定程序；缺校准集数据契约；c_base 无 rubric；无 first sprint；无运行时 stop condition；缺 misspecification 数字 | 成本无单位；无受益者/KPI；无 build/buy/不做边界；无验证实验；无“审批率超过多少不值”的门槛 |

**共同缺口**：不是“机制讲不清”，而是**接口契约、参数标定、成本单位、stop condition、first sprint**这五样没写。E3 的门是有效的。

## A 分（topic 吸收度）

| 子主题 | 当前 | 核心判断 | 改变哪个决策 | 到 A3/A4 的主要缺口 |
|---|---|---|---|---|
| action-gate | **A2** | 安全是结构问题；T1-only≈blanket veto；收益随基线下降；验收应用 harm–approval–cost–task success 前沿 | 验收口径；弱基线硬 veto/强模型 advisory（后者仍是推测） | 缺数据契约/日志字段/TCO/组织职责/stop condition/first sprint；false-veto 未测；F5 的“同等成本”与 01-L9 的归因有失真 |
| checker | **A2** | checker 要先超过空结果重试和随机 flag 基线；curated precision 只略优于随机；catch/FA 必须分开报 | 建/不建 checker；选 curated/data-derived；验收口径 | 缺标注规模/成本/FA 预算/catch 目标/停止条件；成本单位 per flagged 误写；同源/feedback 的证据等级与 digest 冲突 |
| feasibility | **A2** | 价值是位置×成本×复用次数×基线能力的属性；编译要算 p_h>p_min；分配是前沿选点；没有单一能力曲线 | 上线评审从基准均值改为盈亏平衡；按审批预算选点；投影只在答案在文本里时建 | 缺度量契约（ledger 字段/p_h 抽样/c 折算）；缺组织口径；12 机制只有 3 个可算；false-veto/φ 无数字；无 first sprint；EXP-003 错挂 |

**共同缺口**：topic 有判断，但没有**客户指标/反事实/TCO/first sprint**；A3 的“实施含义”与 A4 的“客户价值”都缺。

## 校准决定

1. **E3/A3 门不放宽**。样本是 E2/A2，说明门有效；Phase 1/2 修内容，不降标准。
2. **E3 必须新增两节**：`## 工程配方`（接口/数据/参数/步骤/失败/stop）与 `## 第一个 sprint`；没有就不算 E3。
3. **E4 必须新增**：成本单位（人时/机时/金额或可换算）、替代方案、客户价值假设（可标推测）、go/no-go 判据。
4. **A3 必须新增**：数据/接口/组织/成本/风险/stop/first sprint。
5. **A4 必须新增**：受益者/痛点、客户指标、反事实、V3 试点设计、至少一条反例。
6. **人类 sign-off 延后**到 Phase 4；Phase 0 以 AI 双视角校准为准，并在最终报告标注。

## 对排期的影响

- 22 篇 digest 大多需要补“工程配方/成本/stop/first sprint”，不是小修；Phase 1 按 2 篇/轮，预计 11–15 轮。
- 20 个 topic 大多需要补“实施含义/客户价值”，Phase 2 按 2 个/轮，预计 10–12 轮。
- 总轮次仍在 120 内；Phase 1 先做 L3 12 篇，再做 L2/L1。

## 下一步

- 建 `digest-ledger.md` / `topics-ledger.md` 的 Phase 0 基线行。
- 进 Phase 1：从 MIOE 开始，补工程配方与 first sprint，目标 E3；L3 有条件的冲 E4。
