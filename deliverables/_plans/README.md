# _plans：工作底稿

> 这里放**交付物的执行计划/工作底稿**，不是交付正文。它们可以引用 `src/` 与 `topics/`，但不构成 E，也不保证稳定。

| 文件 | 对应交付物 | 说明 |
|---|---|---|
| [2026-11-10-04-content-supply.md](./2026-11-10-04-content-supply.md) | [04 建用治](../04-ontology-in-production/README.md) | **内容供给**：12 条承重句 → 6 张矩阵/目录 → 12 个 M 来源 + 1 个论文槽位；W0–W3，8 条靠整理/标准、4 条靠新证据；停止线=并进 02 R13。**2026-11-10 已执行 W0–W3 主体**：6 页落 topics、04 九件产物；6 个标准卡已入（GB/T 43697/35273、ODRL、XACML、SHACL、ODCS）；M5–M7/M10 按 D7 降为候选；Great Expectations / OpenLineage 已入；E23–E27 全部已升、body 14.9k（修订 ≤15k） |
| [2026-11-10-04-matrix-skeletons.md](./2026-11-10-04-matrix-skeletons.md) | [04 建用治](../04-ontology-in-production/README.md) | **W0 矩阵骨架**：12 条承重句 × 12 张表；B1/B2/C2 已满，其余部分；空格=订单 |
| [2026-11-10-04-deep-plan.md](./2026-11-10-04-deep-plan.md) | [04 建用治](../04-ontology-in-production/README.md) | **04 深挖**：按 04→topics→src→外部 走依据链；三链（可消费性/查询/治理）、18 行依据表、W0–W5；§6 是 workflow/subagent 执行编排；**D1–D6 已定并执行完**：正文 11,995/12k、导航 8.5%、5 件产物（TBox/shapes/ABox/3 SPARQL/policy/audit）；4 轮冷读，P0 定向复核 PASS；kill criterion 不 kill；剩余 P2 与输出校验/端到端失败传播 |
| [2026-11-10-04-remediation-plan.md](./2026-11-10-04-remediation-plan.md) | [04 建用治](../04-ontology-in-production/README.md) | **04 内容整改（不做实现）**：新人冷读 6 组问题 → S/N/E/R/H 五类发现；C0 口径 → C1 读源/证据对齐 → C2 语义内容 → C3 新人内容 → C4 一致性 → C5 冷读；9 件产物不变，不加 engine/harness/reference filter/EXP；`topics/`、`src/`、`meta/` 只补条件与出处。**2026-11-10 已执行（内容层）**：04 raw/governed + 8 规则/11 测试 + 3 audit + journey/glossary；未跑示例/未做实验；check 499 文件 |
| [2026-11-11-quality-lift-plan.md](./2026-11-11-quality-lift-plan.md) | 01/02/03 | **总体提拉**：先合并（02 双表/D1）→ 01 补 5 why → 03 补 5 why/降框架税 → 共同收口；DoD=10/14、10/13、7/7、本页≤20、同数≤1；3.5–5 人日；只提内容层 |
| [2026-11-11-01-lift-plan.md](./2026-11-11-01-lift-plan.md) | 01 | 01 分计划：补 memory/离线 SHACL/推理/commit/确定性 5 条 why；去重 |
| [2026-11-11-02-lift-plan.md](./2026-11-11-02-lift-plan.md) | 02 | 02 分计划：合并双阈值表、链 D1、补 R4/R9/R10/R11/R12 why |
| [2026-11-11-03-lift-plan.md](./2026-11-11-03-lift-plan.md) | 03 | 03 分计划：补 memory/evidence/commit/outside why；`本页` 61→≤30；零硬页 5→5（不硬塞） |
| [2026-11-11-content-audit.md](./2026-11-11-content-audit.md) | 01/02/03（基准 04） | **内容审计**：硬句/锐句/水句密度；01 短而硬、02 手册体、03 概念锐框架重、04 单点深；三个税（框架/程序/边界）与门口悖论；只评内容，不评流程 |
| [2026-11-11-exp-004-citation-audit.md](./2026-11-11-exp-004-citation-audit.md) | 02 R4 | **EXP-004**：20 条 claim+E 行，两个 agent 标 S/P/N，κ=1.0；strict S=5/20；**EXP-004b** 加 evidence-anchors 后 55–65%，N 0；E 行是地址不是自足 warrant |
| [2026-11-11-remediation-plan.md](./2026-11-11-remediation-plan.md) | 02/01/03 | **整改**：四个决定（不改 01 标签、03 M1/M2 只标 gap、顺序 02→01→03、接受两张排序）；02 产物包/术语/canonical/读者检查，01 规则/决策记录/术语/canonical，03 claim 走查/读者检查/术语；**2026-11-11 已执行**，冷读 01=yes、02/03=partial（真 gap） |
| [2026-11-10-gap-assessment.md](./2026-11-10-gap-assessment.md) | 01/02/03（基准 04） | **差距评估**：04 的四层（供给/参照物/判据/自足）与三条会被误用的指标；10 维评分卡（L0/L1/L2）；P0–P5 探索计划；初读 02 最近、01/03 更远但远法不同；**只评估，不修** |
| [2026-11-10-gap-assessment-report.md](./2026-11-10-gap-assessment-report.md) | 01/02/03（基准 04） | **评估结果**：27 格里只有 1 格到 L2（03 D8）、2 格到 L1+（02 D4/D8）；级差 02=03>01，可补性 02>01>03；三种缺口（规则型/装配型/判据型）；冷读 01=yes、02/03=partial；粗估 21–32 人日 |
| [2026-11-10-wiring-plan.md](./2026-11-10-wiring-plan.md) | 01–04 | **接线**：ADR 0009 方案 A → 02 门槛表加出处 → 03 反例集 → 03 执行矩阵加 O 列 → 冷读；2026-11-10 已执行完 |
| [2026-11-10-stage-review.md](./2026-11-10-stage-review.md) | 全仓 | **阶段盘点**：四层水位（src/topics/objects/deliverables）、三个闭合、三个仍开、下一步三选一 |
| [2026-11-09-hard-objects-plan.md](./2026-11-09-hard-objects-plan.md) | 01–04 全四份 | **硬对象产线**：把判断做成可引用/可复算/可核对的对象（O-xx）；H0–H3 分级、六字段 schema、`topics/objects.md` 注册表、五条产线（C/F/N/T/M+R/P/L）、10 天 60–80 个对象；**已入库 91 个（H3 33 / H2 58；10 条承重 E 各 ≥3；E 级 H3 8/10）**；R/P 已补完；O 引用待 ADR 0009（提议，暂按方案 B） |
| [2026-11-09-reverse-gap-plan.md](./2026-11-09-reverse-gap-plan.md) | 01–04 全四份 | 逆向补齐（力度版）：17/22 单源、31/73 推测、13 行停线 0 出处的诊断；硬杠、旗舰三件（门槛表/反例集/执行矩阵）、上游订货单（TB/CA/FC/QP/S2/LB）、WP0–WP8 |
| [01-capability-status.md](./01-capability-status.md) | [01 现状](../01-capability-status/README.md) | D1 证据回抽计划：E1–E9 的覆盖审计、H1–H6、P0/P1/P2 来源、WBS、DoD、停止规则 |
| [04-ontology-in-production.md](./04-ontology-in-production.md) | [04 建用治](../04-ontology-in-production/README.md) | 4+1 intake（US/China/Germany/Singapore，≥2026-07）、2 个 topics 页面、2 条新 E（P1/P2 分配）、P2.5 工程 OSS + P2.6 Web 讨论线、验收/stop 与 P0–P4 |

**维护**：计划只在推进时更新；结论回 `topics/` 或 01/04 正文，不在计划里落判断。
