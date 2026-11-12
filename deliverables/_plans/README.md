# _plans：工作底稿

> 这里放**交付物的执行计划/工作底稿**，不是交付正文。它们可以引用 `src/` 与 `topics/`，但不构成 E、不新增规则、不进对外阅读路径。常设规则在 [AGENTS](../../AGENTS.md) / [CHARTER](../../CHARTER.md)。
>
> **现行计划至多一份**（当前：无（05 收口计划 2026-11-12 执行完毕）；[缺口补齐计划](./2026-11-12-05-gap-closure-plan.md) 已执行完；04b OKF 严格化已执行完，IA 整改暂停）。其余是日志或参考：日志记当时改了什么，参考是被引用的报告/快照；都不指导新的写入。当前计数与阻塞看 [meta/state](../../meta/status/state.md)。结构决策见 [ADR 0012](../../adr/0012-instruction-layer-single-home.md)。

| 文件 | 对应交付物 | 说明 | 状态 |
|---|---|---|---|
| [2026-11-12-05-closeout-plan.md](./2026-11-12-05-closeout-plan.md) | 05 | **收口**：会场扫（VLDB/ICDM）、补读、联通与 Glyph 一致性、主路径压缩 33.6k→28.1k、首屏配比 | 已执行（2026-11-12） |
| [2026-11-12-05-evidence-pool-plan.md](./2026-11-12-05-evidence-pool-plan.md) | 05 | **证据池修复**：接通 `src/papers/`（Glyph、Narrow and Deep）、新准入 CoeusBI / UniDataAgent、评估 AstraZeneca / Same Context / Auditable、补收益侧与欧洲 gap | 已执行（2026-11-12） |
| [2026-11-12-05-gap-closure-plan.md](./2026-11-12-05-gap-closure-plan.md) | 05 | **缺口补齐**：七条 gap 的二轮补搜（TED API / HN / QCon / 云厂商 / 审计机关 / FOI）+ 上游回写 + 05 回写 + 冷读；命中江西 <50 万、江南 36 人月、小红书 B、NHS 29/137；仍阴性清单见 90.3 | 已执行（2026-11-12） |
| [2026-11-12-04b-okf-strict-plan.md](./2026-11-12-04b-okf-strict-plan.md) | 05 · 4b | **04b 严格化**：拆规范边界/映射机制/采用证据三层；SCIMIN 复核降为 signal（不入库）、Kunstenpunt/京东降为线索、删伪阈值；上游改 E-32/L-22 + 新增 L-23 | 已执行（2026-11-12） |
| [2026-11-12-deliverable-ia-plan.md](./2026-11-12-deliverable-ia-plan.md) | 01–04 | **IA 整改计划**：README 索引化、B 方案编号（02/03/04/05/09/90+）、链接路径兜底、第三人称语气；01 已落地，02–04 待执行 | 参考（暂停） |
| [2026-11-12-content-gap-survey.md](./2026-11-12-content-gap-survey.md) | 全仓 | **内容缺口盘点**：purge 后证据基座、按派缺口、横切缺口、优先级行动清单；外部对齐受限核实（web_search 402，宽口径发现待恢复） | 参考（缺口盘点） |
| [2026-11-11-core-plan.md](./2026-11-11-core-plan.md) | 全仓 | **收口交接快照**：证据重置 + ADR 0011 术语基线 + 01→04 收口的 P0–P6 记录；常设规则以 AGENTS/CHARTER 为准，本文件不再新增规则 | 日志（收口记录） |
| [2026-11-11-command-board.md](./2026-11-11-command-board.md) | 全仓 | 逐批进度日志：P0–P4 每批改了什么、`check_repo` 结果 | 日志 |
| [2026-11-11-scan-report.md](./2026-11-11-scan-report.md) | 01–04 | **旧噪声扫描**：撤回 E/旧效应量/借权威/旧计数；干净门结论与保留为历史的文件 | 参考（第 5 步已完成） |
| [2026-11-11-trunk-wiring.md](./2026-11-11-trunk-wiring.md) | 01–04 | **接线报告（第 7 步）**：定义句 `（N: 标准名）`/`（local）` 的逐页记录、可复跑验收命令、审计结果与限制 | 参考（第 7 步已完成） |
| [2026-11-11-score-after-repair.md](./2026-11-11-score-after-repair.md) | 01–04 | **评分（补偿后）**：门槛全过；desk 87/86/83/88；与 §11–§12.3 的对比；短板 C2/B3 | 参考（评分） |
| [2026-11-11-content-repair.md](./2026-11-11-content-repair.md) | 01–04 | **内容修复（P0–P2）**：四张 W 表、gap 处补自测协议、03 换叙事、术语表瘦身；修复前后指标 | 参考（修复） |
| [2026-11-11-content-read.md](./2026-11-11-content-read.md) | 01–04 | **精读报告**：逐页读 41 万字符，判词与证据行号；撤回源数值清理清单、覆盖率矩阵修正、仍未解决项 | 参考（精读） |
| [2026-11-11-cold-read.md](./2026-11-11-cold-read.md) | 01 / START | **代理冷读（第 9 步）**：第一轮 68 → 第二轮 86；修 5 处（START/01 口径冲突、map 等级列、gap 定义、START 裸词）；真人冷读未做 | 参考（第 9 步已完成） |
| [2026-11-11-status.md](./2026-11-11-status.md) | 01–04 + 术语 | 一页状态快照（2026-11-11）：当时计数、不能信什么、未决项；**现行计数以 [meta/state](../../meta/status/state.md) 为准** | 参考（快照） |
| [2026-11-11-baseline-correction-plan.md](./2026-11-11-baseline-correction-plan.md) | 术语/标准线 | S0–S5：标准卡、10 词差异表、06-measure 试点；进度见 [term-baseline](../../meta/status/term-baseline.md) 与 [术语审计](../../meta/audits/2026-11-11-term-baseline.md) | 参考（进度见审计） |
| [2026-11-11-adr-0011-handoff-to-01.md](./2026-11-11-adr-0011-handoff-to-01.md) | 01 | **跨会话交接**：ADR 0011 生效；K0–K4 按论文实验条件标注；不得把成熟度模型当行业标准 | 日志（已回执） |
| [2026-11-11-quality-review.md](./2026-11-11-quality-review.md) | 01–04 | **质量评估（[rubric v1](../../meta/deliverables/quality.md)）**：基线 02/04 78、01 71、03 64；§10 冷读 04 84 / 02 80 / 01 76 / 03 74；**§11 整改后 02 86 / 04 86 / 03 84 / 01 82**；**§12.1 证据重置桌面复评 01 84 / 02 81 / 03 82 / 04 86**、**§12.2 接线后 01 85 / 02 82 / 03 83 / 04 87**（非冷读）；02/03 下降来自 gap 行扩大，不是文笔；残留长尾与真人冷读 | 参考（基线+收口+冷读+复评） |
| [2026-11-11-k-ladder-provenance.md](./2026-11-11-k-ladder-provenance.md) | 01 | **K0–K4 来源核查**：论文条件 vs 行业标准；OpenAlex 0 引用；K 记号撞车（K0–K6）；三处过度外推（K0 地址级、K1 别名/槽位、K2 整塔/固定分节）与修正 | 参考（术语核查） |
| [2026-11-10-04-content-supply.md](./2026-11-10-04-content-supply.md) | 04 建用治 | **内容供给**：12 条承重句 → 6 张矩阵/目录 → 12 个 M 来源 + 1 个论文槽位；W0–W3，8 条靠整理/标准、4 条靠新证据；停止线=并进 02 R13。**2026-11-10 已执行 W0–W3 主体**：6 页落 topics、04 九件产物；6 个标准卡已入（GB/T 43697/35273、ODRL、XACML、SHACL、ODCS）；M5–M7/M10 按 D7 降为候选；Great Expectations / OpenLineage 已入；E23–E27 全部已升、body 14.9k（修订 ≤15k） | 已执行 |
| [2026-11-10-04-matrix-skeletons.md](./2026-11-10-04-matrix-skeletons.md) | 04 建用治 | **W0 矩阵骨架**：12 条承重句 × 12 张表；B1/B2/C2 已满，其余部分；空格=订单 | 已执行（W0） |
| [2026-11-10-04-deep-plan.md](./2026-11-10-04-deep-plan.md) | 04 建用治 | **04 深挖**：按 04→topics→src→外部 走依据链；三链（可消费性/查询/治理）、18 行依据表、W0–W5；§6 是 workflow/subagent 执行编排；**D1–D6 已定并执行完**：正文 11,995/12k、导航 8.5%、5 件产物（TBox/shapes/ABox/3 SPARQL/policy/audit）；4 轮冷读，P0 定向复核 PASS；kill criterion 不 kill；剩余 P2 与输出校验/端到端失败传播 | 已执行 |
| [2026-11-10-04-remediation-plan.md](./2026-11-10-04-remediation-plan.md) | 04 建用治 | **04 内容整改（不做实现）**：新人冷读 6 组问题 → S/N/E/R/H 五类发现；C0 口径 → C1 读源/证据对齐 → C2 语义内容 → C3 新人内容 → C4 一致性 → C5 冷读；9 件产物不变，不加 engine/harness/reference filter/EXP；`topics/`、`src/`、`meta/` 只补条件与出处。**2026-11-10 已执行（内容层）**：04 raw/governed + 8 规则/11 测试 + 3 audit + journey/glossary；未跑示例/未做实验；check 499 文件 | 已执行 |
| [2026-11-11-depth-lift-plan.md](./2026-11-11-depth-lift-plan.md) | 01/02/03 | **深度提拉**：D1 3 条/份（≥200 字，机制+条件+反例+决策），其余 D2（≤120 字）；不追覆盖率；4–5 人日；D1 候选：01 K1/动作/read-path，02 R5/R6/R8，03 action/checker/commit | 已执行 |
| [2026-11-11-quality-lift-plan.md](./2026-11-11-quality-lift-plan.md) | 01/02/03 | **总体提拉**：先合并（02 双表/D1）→ 01 补 5 why → 03 补 5 why/降框架税 → 共同收口；DoD=10/14、10/13、7/7、meta 句≤60（当前页，不含 appendix；不许换词）、同数≤1；3.5–5 人日；只提内容层 | 已执行 |
| [2026-11-11-01-lift-plan.md](./2026-11-11-01-lift-plan.md) | 01 | 01 分计划：补 memory/离线 SHACL/推理/commit/确定性 5 条 why；去重 | 已执行 |
| [2026-11-11-02-lift-plan.md](./2026-11-11-02-lift-plan.md) | 02 | 02 分计划：合并双阈值表、链 D1、补 R4/R9/R10/R11/R12 why | 已执行 |
| [2026-11-11-03-lift-plan.md](./2026-11-11-03-lift-plan.md) | 03 | 03 分计划：补 memory/evidence/commit/outside why；`本页` 61→≤30；零硬页 5→5（不硬塞） | 已执行 |
| [2026-11-11-content-audit.md](./2026-11-11-content-audit.md) | 01/02/03（基准 04） | **内容审计**：硬句/锐句/水句密度；01 短而硬、02 手册体、03 概念锐框架重、04 单点深；三个税（框架/程序/边界）与门口悖论；只评内容，不评流程 | 历史 |
| [2026-11-11-exp-004-citation-audit.md](./2026-11-11-exp-004-citation-audit.md) | 02 R4 | **EXP-004**：20 条 claim+E 行，两个 agent 标 S/P/N，κ=1.0；strict S=5/20；**EXP-004b** 加 evidence-anchors 后 55–65%，N 0；E 行是地址不是自足 warrant | 历史 |
| [2026-11-11-remediation-plan.md](./2026-11-11-remediation-plan.md) | 02/01/03 | **整改**：四个决定（不改 01 标签、03 M1/M2 只标 gap、顺序 02→01→03、接受两张排序）；02 产物包/术语/canonical/读者检查，01 规则/决策记录/术语/canonical，03 claim 走查/读者检查/术语；**2026-11-11 已执行**，冷读 01=yes、02/03=partial（真 gap） | 已执行 |
| [2026-11-10-gap-assessment.md](./2026-11-10-gap-assessment.md) | 01/02/03（基准 04） | **差距评估**：04 的四层（供给/参照物/判据/自足）与三条会被误用的指标；10 维评分卡（L0/L1/L2）；P0–P5 探索计划；初读 02 最近、01/03 更远但远法不同；**只评估，不修** | 历史 |
| [2026-11-10-gap-assessment-report.md](./2026-11-10-gap-assessment-report.md) | 01/02/03（基准 04） | **评估结果**：27 格里只有 1 格到 L2（03 D8）、2 格到 L1+（02 D4/D8）；级差 02=03>01，可补性 02>01>03；三种缺口（规则型/装配型/判据型）；冷读 01=yes、02/03=partial；粗估 21–32 人日 | 历史 |
| [2026-11-10-wiring-plan.md](./2026-11-10-wiring-plan.md) | 01–04 | **接线**：ADR 0009 方案 A → 02 门槛表加出处 → 03 反例集 → 03 执行矩阵加 O 列 → 冷读；2026-11-10 已执行完 | 已执行 |
| [2026-11-10-stage-review.md](./2026-11-10-stage-review.md) | 全仓 | **阶段盘点**：四层水位（src/topics/objects/deliverables）、三个闭合、三个仍开、下一步三选一 | 历史 |
| [2026-11-09-hard-objects-plan.md](./2026-11-09-hard-objects-plan.md) | 01–04 全四份 | **硬对象产线**：把判断做成可引用/可复算/可核对的对象（O-xx）；H0–H3 分级、六字段 schema、`topics/objects.md` 注册表、五条产线（C/F/N/T/M+R/P/L）、10 天 60–80 个对象；**首轮入库 91 个（H3 33 / H2 58；E 级 H3 8/10）；现行 94 / H3 36 / 10/10**；R/P 已补完；O 引用待 ADR 0009（提议，暂按方案 B） | 已执行 |
| [2026-11-09-reverse-gap-plan.md](./2026-11-09-reverse-gap-plan.md) | 01–04 全四份 | 逆向补齐（力度版）：17/22 单源、31/73 推测、13 行停线 0 出处的诊断；硬杠、旗舰三件（门槛表/反例集/执行矩阵）、上游订货单（TB/CA/FC/QP/S2/LB）、WP0–WP8。其中的倒查补证方法已升为常设[修复回路](../../AGENTS.md) | 历史 |
| [01-capability-status.md](./01-capability-status.md) | [01 现状](../01-capability-status/README.md) | D1 证据回抽计划：E1–E9 的覆盖审计、H1–H6、P0/P1/P2 来源、WBS、DoD、停止规则 | 历史 |
| [04-worked-example.md](./04-worked-example.md) | 04 建用治 | 4+1 intake（US/China/Germany/Singapore，≥2026-07）、2 个 topics 页面、2 条新 E（P1/P2 分配）、P2.5 工程 OSS + P2.6 Web 讨论线、验收/stop 与 P0–P4 | 历史 |

**维护**：计划只在推进时更新；结论回 `topics/` 或 01/04 正文，不在计划里落判断。新危机不新开“先读我”——改常设文档（AGENTS/CHARTER/meta），这里只留日志。

> 状态：`现行` = 唯一还在指导后续工作的计划；`参考` = 已完成的报告/快照，可被引用，不指导写入；`日志` = 过程记录；`已执行` = 结论已回写、保留追溯；`历史` = 只追溯。
