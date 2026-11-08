# digest 全审 ledger

> E 级定义见 [plan.md](./plan.md) §3.1；Phase 0 基线见 [phase0.md](./phase0.md)。  
> 行在 Phase 1 逐篇补齐；未审行不预填。

| D-ID | 论文 | 当前 E | 到 E3 的缺口 | 到 E4 的缺口 | first sprint | verdict |
|---|---|---|---|---|---|---|
| D-01 | 2610.38326 MIOE | **E4** | 已补接口/训练参数/数据 pair/成本/stop/竞争方案/first sprint；单层 rank 改为 1024/2048；Iso 池与 Cause-Iso 反向已写 | 收益基线（人审工时/false accept）、TCO 金额、复用 RAVEL 的 build/buy 定价 | 20–30 具体类 + 1 属性；500/2,000/8,000 对规模曲线；单层 rank 1024/2048；base-correct retained；随机子空间对照；预写 go/no-go | **Phase 1 pass（E3）**；E4 待收益基线 |
| D-02 | 2610.41172 CAI | **E4** | 已补工具 schema/claim 索引/返回字段；topN=20、k=100、anchor 20；p_h 与 E3 门分离；c/φ 测法；人时 | 已补成本公式/替代方案/V3；金额仍需自己的单价 | 单语料 100–200 问；只做 E2；测 p_h/miss/时延；c 折算；p_h<p_min 停 | **Phase 1 pass（E4）** |
| D-03 | 2610.36570 CASEL | **E4** | 已补控制器接口/γ_m 标定/校准协议/c_base 锚点/first sprint/stop/misspecification | E4 成本公式与两段验证已加；仍缺真实单价/审批人时/伤害货币化 | 2 周 log-only：记录 call+可逆性+c_base+p̂；回放估 γ_verify；画 coverage–risk；预写 go/no-go | **Phase 1 E3 pass**；E4 待单价/基线 |

| D-04 | 2610.11768 N&D | **E4** | 已补投影序列化/工具写接口/任务+rubric 构造/成本伸缩/E4 价值分母 | E4：buy 侧 RFQ、工时价/事故基线、TCO 上限 | 2 周单设备：K0→K1 先测；3 条推导+2 knowledge；45k 投影+node map；K1 vs K2；安全层桩 | **Phase 1 pass（E4）** |
| D-05 | 2610.37809 Ontology Catch | **E4** | 已补 checker 接口/data-derived 参数/成本折算/stop/部署度量/first sprint/V3 | — | 200 题：空结果基线 → data-derived check；增量 catch/FA/成本；预写 go/no-go | **Phase 1 pass（E4）** |
| D-06 | 2610.40482 FIRME | **E4** | 已补 registry/edge schema/match-upsert 契约/$100K 定义/stop/冷启动/first sprint/V3 | — | 2 周单域 1 period shadow：head/alias registry；200–500 文档；200 units 标注；alias on/off | **Phase 1 pass（E4）** |

| D-07 | 2610.21983 OntoAct | **E4** | 已补数据契约/接口/参数/stop/成本/sprint/替代/V3 | E4 成本口径/基线/替代报价仍缺，但决策框架可用 | 2 周单域：schema；30–50 公理；三值求值+report；20–30 episode；预写 go/no-go | **Phase 1 pass（E4）** |
| D-08 | 2611.02395 SLB | **E4** | 已补 placeholders 契约/codebook/sprint/样本量/stop/成本/替代/V3 | E4 成本金额、客户基线、buy 侧审计工具 | 100 题 1 模型：trace+程序；30 条校准；基线；50 题 placeholders；验收 ≤0.02 | **Phase 1 pass（E4）** |
| D-09 | 2611.03534 Grid | **E4** | 已补 citation/study/strict-pass/memory/pause-resume 接口、参数、成本、stop、sprint、替代、V3 | E4 TCO/单价、客户基线、buy 对照 | 2 周 4-bus+3 条款+N-1：citation/契约/strict-pass/签核；20 held-out | **Phase 1 pass（E4）** |
| D-10 | 2610.08082 POLAR | **E4** | 已补 Layer A/B schema、DecisionPolicy 接口、反向搜索细节、成本/stop/sprint/替代/V3 | E4 单价/ESCALATE 人时/blanket veto 对照仍缺，但决策框架可用 | 2 周单域 shadow：T1/T4/T5 本体；只读状态；200–500 回放；100 blocked 标注；配对 A/B | **Phase 1 pass（E4）** |
| D-11 | 2610.35267 Diagnose | **E4** | 已补 case table/repair trace schema、intent gate/validate/repair 接口、参数/stop、成本/sprint/替代/V3 | E4 成本量级、收益基线、buy 对照 | 2 周单域 15–20 case：七变量表；κ；只修 Input/Context；同 batch 重测；预写 go/no-go | **Phase 1 pass（E4）** |
| D-12 | 2611.01276 OntoDoc | **E4** | 已补 prompt/判分规格、DB context ASK 校验、产物 schema、失败路径、发布闸门、成本/sprint/替代/V3 | E4 每 IRI 金额/人工撰写基线、buy 对照 | 2 周 40 术语：naive vs 四阶段；ASK 校验；20 条人工盲评；成本记录；出口判据 | **Phase 1 E3 pass**；E4 待成本 |

| D-13 | 2610.36335 OA-RAG | **E3** | 已补 concept card 字段/工具/name linking/预算/stop/1 周 sprint/成本/替代/V3 | E4 成本/客户基线/替代 | 1 周 FoodOn：concept cards + DESCRIBE/ASK/SELECT；Test1/2 各 200；gold 检索/引用；RAGdoc 对照；预写 go/no-go | **Phase 1 pass（E4）** |
| D-14 | 2610.37407 Commit Boundary | **E3** | 已补 mutation/q_m/evidence/promotion/verdict schema、两阶段时序、失败模式表、stop、2 周 sprint | E4 无实现/成本/价值 | 2 周单 mutation class（person merge）：required claims 表 + 状态机 + fail-closed gate；20 案例回放 | **Phase 1 pass（E4）** |
| D-15 | 2610.36325 Multi-agent | **E3** | 接口契约/停止收敛/复现输入仍可补；不阻塞开工 | E4 成本/客户基线/替代 | 2 周 GraphDB + 症状映射 + 确定性排序；198 case 对齐 Phase-1 | **Phase 1 pass（E4）** |
| D-16 | 2611.03743 EvoMemState | **E3** | 已补 facts/relational/reasoning schema、GRPO 配方、数据构造、stop、2 周 sprint（GRPO 后置） | E4 成本/客户基线/替代 | 先做 facts/relational 分存 + 关系遍历 + 双层评估；GRPO 后置 | **Phase 1 pass（E4）** |
| D-17 | 2610.01618 Agents | **E3** | Information 轴模板/数据与评分常量/sprint 验收仍可补；不阻塞开工 | E4 成本/客户基线/替代 | 单任务固定配置 5 runs 噪声地板；Information none→protocol 单轴；三项读数 | **Phase 1 pass（E4）** |
| D-18 | 2610.21466 CASTON | **E3** | 阈值/召回边界/输入接口仍可补；不阻塞开工 | E4 成本/客户基线/替代 | Sprint1 只闭合 embedding：OnT 微调 + 292 条排序 + 30×10 候选 + 20–30 专家盲标 | **Phase 1 pass（E4）** |
| D-19 | 2610.41785 Peeling | **E3** | 已补编码器/基准/探针超参/DAG I/O/stop/sprint | E4 成本/客户基线/替代 | 冻结 Nomic 768；wiki-ol 8,033 概念；768→128 探针；Graph F1 + 打乱/逆序；挂层级检索 | **Phase 1 pass（E4）** |
| D-20 | 2510.26683 Evontree | **E3** | 已重写：补 3.1/3.7%、ConfirmValue/τ*/两条规则/LoRA 参数/安全反例/E3 配方 | E4 成本/客户基线/替代 | 2 周 Llama3-8B 单域：15 根 → JSON 树；ConfirmValue/τ*；reliable/gap；implicit LoRA；held-out + 安全面 | **Phase 1 pass（重写后 E3）** |
| D-21 | 2610.37123 SFE-O | **E3** | 已补最小 schema/SHACL/外部服务边界/stop/sprint | E4 成本/客户基线/替代 | 3–5 单元流程：三模块 + 参数字段 + 5–10 SHACL；两处矛盾负例；mock 外部服务 | **Phase 1 pass（E4）** |
| D-22 | 2610.41901 ReX-GG | **E3** | 已补 JSON schema/匿名互评/去偏/stop/sprint/成本 | E4 成本/客户基线/替代 | 七模型 JSON + 匿名互评 + 人工 100 条 precision/recall + 下游消费一次 | **Phase 1 pass（E4）** |
