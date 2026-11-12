> **历史快照（2026-11-08/09）**：已归档，不再维护。现行规则见 `meta/README.md`，当前状态见 `meta/status/state.md`。文中的计数与结论可能已被后续修复取代。

# G-X 失败清单（20/20）

> 2026-11-08，20 个 topic 并发反向核对结果。A4 段落已写，但 G-X 未过：unsupported claim 与 orphan digest findings 仍在。  
> 修法：先修“与 digest 冲突/把推测写成已核”，再补 orphan；每 topic 复跑 G-X。

| T-ID | topic | 关键 unsupported（与 digest 冲突/无源） | 关键 orphan（digest 工程发现未吸收） |
|---|---|---|---|
| T-01 | 01/action-gate | F5“同等成本优于不确定性”沿旧卡；F6“可逆性路由贡献大部分”把 NoRev=verify-only 当单变量；ESCALATE 5–15 分钟/curator 2–5 人日被写成事实 | CASEL 4 条 stop、Prop 1 条件/40k 校准/τ_g=0.2/approve ĉ≥0.55/c_base 锚点；CASEL 控制器接口/E4 公式；POLAR admissibility/curator rubric |
| T-02 | 01/commit-gate | “一次批准覆盖整个会话”与 digest 相反；scope 变更频繁反例无源 | verdict 缺 scope_valid/versions_valid/failed_claims[]/unresolved[]；promotion 缺 shadow/eligible/promoted_by；持续审计成本 |
| T-03 | 01/reasoning-gate | “不阻止工具调用/不是动作闸门”与 OntoAct block 冲突；“阻断信号弱/重复收费”无源 | 症状映射管线（91.3%/8.7%）；verifier 非 safety guarantee/别用；turn budget 20–40/重试 3/? 转人工 |
| T-04 | 02/checker | 同源结论标已核；“generic 更安全”与 digest 相反；57.1 precision 与真实答案混用；“curated 审计 1–2 人日”无源 | per-flagged 成本公式/LLM ontology <$1 记错行/部署期 100–400 抽样+Wilson+A/B/data-derived 重建频率/disjointness 不贡献/30% 绝对 catch 门 |
| T-05 | 02/evidence | output 带 span 无源；校准 100–400 条与 1–2 人日无源（实为 card 成本） | call>10/token>12k abstain；未知 IRI>20% 停；concept card 字段/BM25 k/name linking 200 池/1–2 人日/card、1–2 人周 reasoner；RAGdoc 对照/1 周 FoodOn |
| T-06 | 02/calibration | ECE/isotonic/temperature 整机制无源；precision 条件丢；同源“只做路由”无源 | 空结果重试基线 79.2/2.5；增量 catch ≥5pp；OA-RAG grounding 94.9/82.1 |
| T-07 | 03/compilation | F6“RAPTOR/PageIndex neutral”与 PageIndex 负面矛盾；六条不变量/工具六类不在 CAI digest | Grid memory/pause-resume 契约、solver 容差/超时/版本、strict-pass study_type/solver_version、每单加固成本/审计发现数；CAI miss-penalty 敏感度 |
| T-08 | 03/projection | “投影 > JSON/查询”无条件；24–68% 丢“仅 GLM”；“教训写进提示也被用”无 digest 条目 | 写接口 propose_setpoint/readback；build 成本伸缩式；buy/CMMS RFQ |
| T-09 | 04/memory | Acc@complete 70.8 vs 36.8 跨基准拼接；“检查点回滚点”无源 | 五态 N=3 边界；$100K/Rule 3/4；GRPO 配方/60K/≥3 seeds |
| T-10 | 04/identity | “alias 是主要增量”未拆分；false merge“长期污染”未测量；“CMR 奖励少匹配”与 CMR=MMR×precision 相反 | Commit 写侧字段 hypothesis_id/source_id/failed_claims/promoted_by；冷启动历史 alias 不泄漏 |
| T-11 | 04/determinism | “漂移=输入不完备”挂 D-16 错配（实为 E-06 类比）；README 9% 仍标待核 | SLB zero result（+0.007/+0.005）；形式语言 0.03–0.20/方差 0.123；EvoMem stop 门 |
| T-12 | 05/generation | 专家手工“覆盖窄/维护贵”归 SFE-O 无源；LLM“语义漂移/方向错”无源；“把常见当应然”无源；“四条路线均未实现增量”过度概括；“无来源标记”未标推测 | OntoDoc DB 5 工具/50 triples/10 calls/四子阶段/Web Tavily+Rerank/失败路径；ReX 匿名互评 k=3–5/median/Borda/去偏；Evontree gap 1,396/ConfirmValue/成本；Peeling 探针参数/下游召回；客户指标只吸收 OntoDoc |
| T-13 | 05/refinement | “瓶颈是定位与验证”循环引证；“medium 全 mixed”与 1/4、1/5 不符；“更大 LLM 不能补”混淆两变量 | recall@30/@10 与“真错父类在候选池”；别用 5 条只吸收 2 条（本体很小/无专家/关系限制） |
| T-14 | 05/representation | 消费位置表/成本差 1–2 数量级/多数团队/第三档得不偿失均无源；2–4 人周口径被放宽 | 第三处矛盾（床体积缺几何因子）；SHACL 能否当判定器/矛盾进置信度 |
| T-15 | 05/lifecycle | recall@10 与 CASTON“排除已断言父类”互斥；“四组 medium 全 mixed”无源；Evontree 2–3 人日被写成每人 | FIRME observation 级契约/source_indicator/幂等键/CMR=MMR×precision；OntoAct axiom 准入/覆盖率 stop/schema 5–10 人日 |
| T-16 | 06/mechanism | 类级 0.03–0.65 无源；多任务 +0.081/−0.052 当整体平均 | 小 rank 阈值作废；Entity 选配置/Context 复用；+0.102 基线 0.565 不是 0.584 |
| T-17 | 06/failure-attribution | “换人复算同一结论”无源；语义充分率等操作定义自定未标 | 症状映射管线；候选截断 10–20/阈值宁宽；Top-1/Top-3+case-level |
| T-18 | 06/trace | “审计默认 shadow”无源；成本随实例增长写成普遍规律（2/4 数据集才有） | codebook 排除“题面限制不算 SLB”；buy 臂/闭源出局；低延迟/无需 solver 的别用 |
| T-19 | 06/metrics | 57.1 precision 与真实 catch/FA 拼接；单轴“会误判”是推断未标 | GAP_CLOSED/hurdle/54% 真实尝试限定；五轴档位；效率≠结果 |
| T-20 | 06/feasibility | “先买 miss/false-veto”false-veto 无测量；CASEL 8.7/7.02 未带 τ=∞；D-ID 矩阵与 ledger 错位 | CASEL 单位经济学公式/校准协议/γ CI stop；NPV 公式 |

## 修复顺序

1. **P0 冲突/错标**：T-01 F5/F6、T-02 批准继承、T-03 不阻止动作、T-04 同源/ generic、T-06 ECE、T-07 F6、T-09 36.8、T-10 alias/false merge、T-12 来源归因、T-13 medium、T-15 recall/四组、T-16 0.03–0.65、T-19 precision。
2. **P1 orphan 工程发现**：每 topic 补 2–4 条最关键的接口/参数/stop/成本。
3. **P2 复跑 G-X**：20 个并行；全 pass 才进 Phase 3。

## 当前状态

- A4：20/20（段落已写）。
- G-X：**0/20**（本清单）。
- 结论：不能签 G-X，不能进 Phase 3。

## 复跑状态（2026-11-08 checkpoint）

**20/20 pass**（2026-11-08）：全部 T-01…T-20。

**未过 0 个。**

**下一步**：A/C/D/E 跨页 claims/README/conclusions 回写；Phase 3 只对 8 个 A4 做 V2/V3；Phase 4 双 critic + 人类抽检；Phase 5 report。
