---
updated: 2026-11-12
---

# deliverables：交付

流水线的第三个工位。把 `topics/` 里已经站得住的判断，重新组织成**对外可用的形态**：手册、Deck、图、讲稿。

> **第一次来？先读 [START.md](./START.md)**（10 分钟）。**宪章**：[CHARTER](../CHARTER.md)——交付物是文档，不以可运行性为标准；示例数据/查询文本是说明材料。
>
> **2026-11-11 证据重置**：按被删源写成的段落重写完成前不得作为结论；撤回清单以 [审计](../meta/audits/2026-11-11-source-purge.md) 为唯一出处。定义已接规范主干（定义句标 `（N: 标准名）` 或 `（local）`）；收口记录见 [_plans 索引](./_plans/README.md)。
>
> **定位权威（[ADR 0014](../adr/0014-deliverable-scope-single-home.md)）**：每份的初心/定性/边界/红线以 [meta/deliverable-scope](../meta/deliverables/scope.md) 为准；改/建任何交付物前先读它。**04 是合成「怎么建」示例；新增 [05 落地现状](./05-production-landscape/README.md) 才是「业界真实怎么样」的实证份（证据待补）。**

## 0. 读者与写法：deliverables 是给人的成品

- **读者**：人（落地团队、评审、决策者），不是 Agent 检索层。
- **写什么**：按任务/问题组织；通俗、步骤、产物、验收、卡住怎么办；把 `topics` 的矩阵/目录消化成读者表。
- **不写什么**：让读者自己拼 `topics`；内部术语堆叠（首次出现要解释）。
- **细节**：可以链 `topics/`，但要标“可选/出处”；**主路径必须自包含**，读者不打开 `topics` 也能完成任务。
- **完成信号**：读者不打开 `topics` 能照着做；要细节时知道去哪。

<img src="./_figures/three-layers.svg" alt="三个层次的阅读顺序" width="100%">

## 抽取规则

1. **主路径面向人，出处可选。** 正文不要求读者打开 `topics/`；细节/出处可在附录引 E-xx 或链 `topics/`，标“可选”。不直接引 `src/`；未经消化的材料不能以成品面貌流出。
2. **不新增判断。** 交付物里不允许出现 `topics/` 中不存在的结论。抽取时发现的缺口，回到 `src/` 或 `frontier`，不在交付物里补。
3. **每条可反查。** 交付物的每个要点都要能指回主题文档或结论编号。做不到，说明它还没被消化。
4. **标注可信度。** 已核与推测必须区分开——对外物最容易犯的错是把推测写成既成事实。
5. **定义引 N，效应引 I，线索只进 frontier。** 规范主干（标准能定义什么/不能定义什么）见 [topics/trunk.md](../topics/trunk.md)；交付物首现的定义要指 N 或标 `local`。
6. **只抽 admitted 源支撑的判断。** 每个要点必须沿 E/L → digest 追到 `admission: admitted`（含 probation）的材料；追不到的删掉或标 `推测`，不能靠“行业普遍认为”补位。源被撤回的，对应段落同步失效；撤回清单以 [审计](../meta/audits/2026-11-11-source-purge.md) 为唯一出处。

## 子目录：01–04 = 3 层 + 1 条生命周期；05 = 落地现状（实证）

前三层回答「判断 / 操作 / 依据」；04 把三者串成「建 → 用 → 治」的落地生命周期。四个子目录之外，还有一份共用的 10 分钟入口 [START.md](./START.md)（不属于任何一层，四份都从它进门）。

```
01-capability-status/     判断层：今天能做成什么、不能承诺什么
        │
        ▼
02-engineering-playbook/  操作层：拿本体做某件事，具体怎么做
        │
        ▼
03-mechanism-reference/   依据层：为什么是这些位置/形态，边界在哪

04-worked-example/ 生命周期：建 → 用 → 治（跨三层）
```

| 子目录 | 回答什么 | 形态 | 状态 | 依据 |
|---|---|---|---|---|
| [01-capability-status](./01-capability-status/README.md) | 哪些能落地、哪些能试点、哪些只能设计；距离多远 | 判断 + 能力矩阵 | draft | E-01–E-20、C-01–C-04 |
| [02-engineering-playbook](./02-engineering-playbook/README.md) | 选位置/形态、R0–R12、开源与论文指示分级、账本/成本/上线、验收与 stop | 步骤 + 接口 + 验收 | draft | E-xx + 各派 mechanism |
| [03-mechanism-reference](./03-mechanism-reference/README.md) | 为什么是六个位置、三根分类轴怎么分、15 条边界 | 入口 + 六张位置卡 + 谱外页 + 三张横切页 + 证据台账 | draft | E-xx + [topics/README](../topics/README.md) |
| └ [附录：约束强度谱](03-mechanism-reference/05-appendix-constraint-spectrum.md) | 03 的长版论证（约 0.97 万字）；位置细节以卡为准 | Markdown 长文 | draft | E-01–E-05、E-12–E-17、E-20、C-03 |
| [04-worked-example](./04-worked-example/README.md) | 本体怎么建到可消费、怎么查、怎么治 | 建 / 用 / 治三分册 + 验收 | draft | E-xx（含 E-21/E-22）+ 03/querying/01/access-control；未入库 signal |
| [05-production-landscape](./05-production-landscape/README.md) | 业界真实落地现状、成本收益、靠谱与否有无证据 | 实证现状（**证据待补，不编**） | seed | 真实生产/业界证据（待补，CHARTER §4.4） |

> **04 与 05 的分界**：04 是「你可以怎么建」的**合成示例**（fixture 期望值，不证明生产）；05 是「业界实际怎么样」的**实证现状**（须真实生产证据）。定位详见 [meta/deliverable-scope](../meta/deliverables/scope.md)。

> `_plans/` 是[工作底稿](./_plans/README.md)，不是交付物；不进对外阅读路径，也不构成 E。
>
> **2026-11-11 整改**：01/02/03 按 [差距评估报告](./_plans/2026-11-10-gap-assessment-report.md) 与 [整改计划](./_plans/2026-11-11-remediation-plan.md) 补了读者层（01 决策记录/术语/canonical、02 产物包/术语/canonical/读者检查、03 claim 走查/读者检查/术语）。三份仍 `draft`；M1/M2 未关，02 的 citation 正确性仍是 gap。

## 导读：先读哪份、按什么顺序

**一句话**：01 判断值不值得做；02 决定怎么做；03 查凭什么；04 从建到用再到治。

### 按任务

| 你手上是什么 | 先读 | 再读 | 不用读 |
|---|---|---|---|
| 只有一个模糊想法 | [01 §0](./01-capability-status/02-sections/00-overview.md#0-一页结论) + 本页图 | [01 地图](01-capability-status/02-sections/02-map.md) | 02 `recipes/`、03 `positions/` |
| 有一个具体任务 | [01 地图](01-capability-status/02-sections/02-map.md)（A/B） | [02 地图](02-engineering-playbook/02-sections/02-map.md) → [02 主体](02-engineering-playbook/02-sections/03-approach.md)（R0 + 一条 recipe） | 03 附录、`src/` |
| 要评审/说服别人 | [03 地图](03-mechanism-reference/02-sections/02-map.md) + [证据边界](03-mechanism-reference/02-sections/04-boundaries.md) | [01 验收](01-capability-status/02-sections/05-acceptance.md) + [02 边界](02-engineering-playbook/02-sections/04-boundaries.md) | `src/` 原文 |
| 要落地一个接缝 | [02 地图](02-engineering-playbook/02-sections/02-map.md) → [R0 + recipe](02-engineering-playbook/02-sections/03-approach.md) | [02 运行](02-engineering-playbook/04-operations/01-ledger.md) + [02 验收](02-engineering-playbook/02-sections/05-acceptance.md) | 01 全篇 |
| 要建/查/治一个本体应用 | [04 地图](04-worked-example/02-sections/02-map.md) | [04 建/用/治](04-worked-example/03-body/01-build.md) | 01/03 全篇 |
| 要查某条判断的边界 | [03 地图](03-mechanism-reference/02-sections/02-map.md) + 对应 position | [03 证据](03-mechanism-reference/05-evidence/01-ledger.md) | 02 全篇 |

### 按时间

| 时间 | 读什么 | 得到什么 |
|---|---|---|
| 10 分钟 | 本页图 + [01 §0](./01-capability-status/02-sections/00-overview.md#0-一页结论) + [02 §0](./02-engineering-playbook/02-sections/00-overview.md#0-一页结论) | 知道四份分工与「先做什么」 |
| 1 小时 | 01 地图 + 02 地图 + 02 主体（R0） | 能选一个接缝/一条 recipe |
| 半天 | 四份 0–6 | 能写 go/no-go 与边界评审 |

### 每份的阅读顺序

- **01**（[GUIDE](01-capability-status/02-sections/01-GUIDE.md)）：0 → [地图](01-capability-status/02-sections/02-map.md) → [能力条目](01-capability-status/03-capabilities/README.md)（A→B→C→D）→ [边界](01-capability-status/02-sections/04-boundaries.md) → [验收](01-capability-status/02-sections/05-acceptance.md) → [关系](#关系与维护)。
- **02**（[GUIDE](02-engineering-playbook/02-sections/01-GUIDE.md)）：0 → [地图](02-engineering-playbook/02-sections/02-map.md) → [R0 + 一条 recipe](02-engineering-playbook/02-sections/03-approach.md) → [边界](02-engineering-playbook/02-sections/04-boundaries.md) → [验收](02-engineering-playbook/02-sections/05-acceptance.md) → [关系](#关系与维护)。
- **03**（[GUIDE](03-mechanism-reference/02-sections/01-GUIDE.md)）：0 → [地图](03-mechanism-reference/02-sections/02-map.md) → [位置卡](03-mechanism-reference/03-positions/README.md)（context→…→commit→outside）→ [横切页](03-mechanism-reference/04-across-positions/03-measurement.md) → [边界](03-mechanism-reference/02-sections/04-boundaries.md) → [验收](03-mechanism-reference/02-sections/05-acceptance.md) → [关系](03-mechanism-reference/02-sections/94-relations.md)。
- **04**（[GUIDE](04-worked-example/02-sections/01-GUIDE.md)）：0 → [地图](04-worked-example/02-sections/02-map.md) → [建](04-worked-example/03-body/01-build.md) → [用](04-worked-example/03-body/02-consume.md) → [治](04-worked-example/03-body/03-govern.md) → [边界](04-worked-example/02-sections/04-boundaries.md) → [验收](04-worked-example/02-sections/05-acceptance.md) → [关系](04-worked-example/02-sections/97-relations.md)。

**反向加载**：从 [01 §5.2](01-capability-status/02-sections/05-acceptance.md#52-期待与数据需求验收规格)/[plan](./_plans/01-capability-status.md)、[02 §3.1](02-engineering-playbook/02-sections/03-approach.md#31-十二条工程做法r0r12)、[03 §2.3](03-mechanism-reference/02-sections/02-map.md#23-六个位置一页表) 出发，按 [meta/loading 的三条反向链](../meta/rules/loading.md#从交付物倒查反向加载) 走；不要从 `src/papers/manifest.md` 开始扫。

## 统一阅读结构

四份交付物内容不同，但**对读者的骨架是同一套**。每份开头都有一张同样的读者卡（读者 / 回答 / 不回答），然后从同一层进入：

| 节 | 回答什么 | 01 现状 | 02 工程 | 03 机制 | 04 落地 |
|---|---|---|---|---|---|
| **0 一页结论** | 这份东西一句话是什么、给谁、最重要三句 | `02-sections/00-overview.md` | 同左 | 同左 | 同左 |
| **1 导读** | 先读哪份、按任务/时间怎么走 | `02-sections/01-GUIDE.md` | 同左 | 同左 | 同左 |
| **2 地图** | 本份的核心框架（矩阵 / 五步法 / 四轴六位置 / 生命周期） | `02-sections/02-map.md` | 同左 | 同左 | 同左 |
| **3 主体** | 逐项：能力 / recipe / 位置卡 / 建用治 | `03-capabilities/` | `03-recipes/` + `02-sections/03-approach.md` | `03-positions/` | `03-body/` |
| **4 边界** | 证据等级、不能证明、反例/反模式 | `02-sections/04-boundaries.md` | 同左 | 同左 | 同左 |
| **5 验收** | 指标、stop、缺口、期待与数据需求 | `02-sections/05-acceptance.md` | 同左 | 同左 | 同左 |
| **6 关系与维护** | 与另外两份的关系、附录、更新规则 | [本页](#关系与维护) | 同左 | 同左 | 同左 |

**同构不等于同文**：01 的主体是「能力条目」，02 是「recipe 条目」，03 是「位置卡」，04 是「建/用/治三分册」；前三类条目都必须有 **一句话 / 适用 / 证据等级 / 边界 / 去哪** 这五个字段。

### 目录契约

| 角色 | 01 现状 | 02 工程 | 03 机制 | 04 落地 |
|---|---|---|---|---|
| 索引 | `README.md`（只放 0/目录/关注） | 同左 | 同左 | 同左 |
| 导读 | `02-sections/01-GUIDE.md` | 同左 | 同左 | 同左 |
| 分节 | `02-sections/`（00-overview / 02-map / 04-boundaries / 05-acceptance） | 同左（多 03-approach） | 同左 | 同左（多 06-decision） |
| 主体 | `03-capabilities/` | `03-recipes/`；总览在 `02-sections/03-approach.md` | `03-positions/` | `03-body/`（01-build / 02-consume / 03-govern） |
| 支撑 | — | `04-operations/` | `04-across-positions/` | — |
| 证据/工作底稿 | `09-data/` | `05-appendices/02-traceability.md` | `05-evidence/` | `04-evidence/` |
| 附录/查阅 | `90+` 查阅页 | `05-appendices/` | `09-appendix...` + `90+` | `05-example/` + `90+` |

## 关系与维护

**一句话**：01 告诉你「值不值得做」，02 告诉你「怎么做」，03 告诉你「凭什么这么说、说到哪为止」，04 把三者串成一条能跑的链。

| 交付物 | 回答 | 读者 | 形态 |
|---|---|---|---|
| [01 现状](./01-capability-status/README.md) | 今天能做成什么、不能承诺什么 | 决策者/工程负责人 | 判断 + 矩阵 |
| [02 工程实施](./02-engineering-playbook/README.md) | 拿本体做某件事，具体怎么做 | 工程负责人/架构师 | 步骤 + 接口 + 验收 |
| [03 机制参考](./03-mechanism-reference/README.md) | 为什么是这些位置/形态，证据边界在哪 | 架构师/研究者 | 参考 + 边界 |
| [04 落地](./04-worked-example/README.md) | 怎么建、怎么查、怎么治 | 落地小团队 | 生命周期 + 验收 |
| [05 落地现状](./05-production-landscape/README.md) | 业界真实落地如何、靠谱与否有无证据 | 决策者/研究者 | 实证现状（证据待补） |

**维护规则（四份共用）：**

- 新判断先回 `topics/` 的 claims/E，再改交付物；交付物不新增判断。结构性修改后跑 `python3 meta/tools/check_repo.py`。
- 01：A/B/C/D 是交付层排序，不是 E；`09-data/` 与 `_plans/` 是工作底稿，不构成稳定判断。
- 02：先改 `03-recipes/`，再回 README 索引；02 不新增 E。
- 03：canonical 在 `03-positions/` 与 `04-across-positions/`；`09-appendix...` 是长版论证；`H`/`D` 必须始终带标记。
- 04：不重复 01 的排序、02 的 recipe、03 的机制论证；04 不新增 E。

**规则**：README 只做索引；正文按「02-sections / 03-主体 / 04-支撑 / 05-附录 / 09-工作底稿 / 90+ 查阅」放，不把长文塞回 README。目录与文件编号规则见 [IA 整改计划](./_plans/2026-11-12-deliverable-ia-plan.md)。导航图统一在 [`_figures/`](./_figures/README.md)，用 SVG；每份 `02-sections/01-GUIDE.md` 嵌本份图，README 不再嵌图。

## 期待 → 数据（验收规格）

四份交付物的 `02-sections/05-acceptance.md` 都有一节「期待与数据需求」：把交付物要回答的问题写成**可证伪的期待**，再倒推「支持它需要什么数据、现在有什么、缺什么」。

它的作用不是承诺结果，而是让缺口显形：**量不出「支持它需要的数据」，就说明这条期待还停在推测。** 这是交付物的验收规格（非 E），不是新结论；数据回 `topics/` 或 `frontier` 补，不在交付物里补。

01 的详细执行计划见 [plan.md](./_plans/01-capability-status.md)；04 的 topics/src 支撑计划见 [04-worked-example.md](./_plans/04-worked-example.md)。历史的上游订货与对象产线记录（reverse-gap-plan / hard-objects-plan / wiring-plan，均已执行）见 [_plans 索引](./_plans/README.md)；其中的倒查补证方法已升为常设[修复回路](../AGENTS.md)。

## handbook 的去留（2026-11-09）

**没有独立的 handbook。** 原《本体在 harness 里如何被执行》7 章、4–6 万字的书稿计划已废弃：

- 书稿没有独立角色——01–04 已经把「判断/操作/依据/落地」分开，再写一本会把它们混回去。
- 第四章缺一手失败复盘、第六章缺按机制分派的度量方案、第七章是案例不是对照；按仓库规则，写不动的地方是研究没做完，不应在交付物里绕过去。
- 主线「价值不在知道更多，而在让不该发生的事不发生」接近 P1a，但 E-01 的 ontology 是 `not measured`、E-04 的结构贡献未隔离；附录已把它收窄为「强端不是更好，是更窄」。

唯一保留的是**论证资产**：原第三章成为 [03 的长版附录](03-mechanism-reference/05-appendix-constraint-spectrum.md)。原大纲与规划已删除，git 历史保留；不再有第四个 `handbook/` 目录。

## 质量评估（维护者用）

评估 01–04 时**只用一套口径**：[交付物质量评分卡](../meta/deliverables/quality.md)（十二维 + 五条硬门槛 + 测量协议 + 使用纪律；维度定义不在本页复述）。评分不自动改 `status`；报告落 `_plans/YYYY-MM-DD-quality-review.md`，同维度比上次 ±1 才写 delta。

**最近一次**：[2026-11-11 质量评估](./_plans/2026-11-11-quality-review.md)——§12.2 接线后 01=85 / 02=82 / 03=83 / 04=87（非冷读）；残留 C2 冗余/体量与真人冷读。

## 待做

| 交付物 | 形态 | 状态 | 依据 |
|---|---|---|---|
| 一页图：约束强度谱 | 图 | 待画 | [03 §2.4](03-mechanism-reference/02-sections/02-map.md#24-强度覆盖率直线是摘要矩阵是操作定义) + [coverage 矩阵](03-mechanism-reference/04-across-positions/01-coverage.md)（H/D，不是 E 结论） |
| Deck：给工程团队的 30 分钟 | 幻灯片 | 待做 | 02 §0 一页结论、§3.1 R 索引、§3.4 参考架构 |
| 案例页：一个端到端示例 | Markdown | 示意已写；真实场景待补 | [02 附录 C](02-engineering-playbook/05-appendices/03-case.md)；标 illustrative，不是部署 |

## 交付阶段（`deliverable_status`）

| 状态 | 含义 |
|---|---|
| `draft` | 结构在改 |
| `stable` | 结构冻结，可对外 |
| `frozen` | 内容冻结，仅随新证据被动修订 |

文档本身的 `status` 仍用 `seed / draft / stabilized / superseded`；`deliverable_status` 只表示交付阶段。见 [conventions](../meta/rules/conventions.md#字段与词汇)。

## 一条判据

交付物做不出来的地方，就是研究没做完的地方。

如果某一章反复卡住，说明 `topics/` 里对应结论还是「推测」——回去补证据，而不是在交付物里绕过去。
