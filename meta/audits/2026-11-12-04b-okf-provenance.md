---
status: draft
type: provenance-audit
updated: 2026-11-12
target: deliverables/10-production-landscape/02-sections/04b-okf-wiki.md
plan: deliverables/_plans/2026-11-12-04b-okf-strict-plan.md
---

# 04b 逐句 provenance 审计（2026-11-12）

> **这是什么**：对 4b 现存正文做一次“每句话的上游在哪”的审计。不是评分，是找**无源、越级、伪精度、越界**四类问题。
> **判据**：[CHARTER §4](../../CHARTER.md#4-素材准入material-gate)（五门）、[三档判定](../../CHARTER.md#42-三档判定)（`signal` 不撑交付物）、[修复回路](../../AGENTS.md#修复回路交付物被指错时的常设路径)。
> **结论**：4b 有 **7 处 P0**（必须改）、**9 处 P1**（应改）、**5 处 P2**（顺手改）。P0 集中在“靠向本体”一节（4b.4b/4b.5/4b.6）。

## 0. 分类口径

| 类 | 含义 | 处置 |
|---|---|---|
| `无源` | `src/`、`topics/`、`frontier` 都找不到；或只有记忆/推断 | P0：补 admitted 源，或删/降 `推测` |
| `越级` | 用 `signal`/C 当交付物证据；或把作者主张写成观测 | P0：移出正文，或降为线索 |
| `伪精度` | 看起来像实测的阈值/比例，没有观测或来源 | P0：删数字，或标“示例、未验证” |
| `越界` | 05（现状·实证）写了 recipe/判据 | P1：移 mechanism/07，4b 只留指针 |
| `措辞过强` | “证明/形式化/一步到位/解决”等超过原文 | P1：改成原文动作 |
| `可保留` | 有 admitted 卡/digest 或规范原文 | — |

## 1. P0：必须改（7 处）

| # | 行 | 原文（缩写） | 上游 | 判定 | 改法 |
|---|---|---|---|---|---|
| P0-1 | 54 | “**京东海博**…AB 实验 542 秒 vs 967 秒…” | 仅 [frontier](../../topics/06-measure/feasibility/frontier.md) `signal`；原文 5 次 OKF 未展开 | **越级** | 移出 4b 正文；90.2c 留一行“signal 线索，不撑采用”；4b 只说“另有未经准入的中文线索，见 90” |
| P0-2 | 72–74 | “**SCIMIN** 更典型：SCIMIN CRM ontology 先有，wiki 是标注界面，LLM 只做候选标注，专家复核…” | **无源**（审计时 `src/`/`topics/`/frontier 均无） | **无源** | 新建 SEMANTiCS 2026 论文卡+digest；改写为“本体先行、SMW 作标注界面、LLM 候选+自动校验+专家 HITL、受控发布”；**CRM = critical raw materials，不是客户关系管理** |
| P0-3 | 72 | “Kunstenpunt…**本体驱动的 wiki**…一步到位” | 原文是 2024 **数据标准**先行（兼容 CIDOC CRM/schema.org），不是 OWL 本体；“一步到位”无原文 | **措辞过强/无源** | 改“数据标准先行的 wiki”；删“一步到位”；标 `signal`（不撑结论） |
| P0-4 | 99 | “Linked.Archi（2026-07-17）…可双向投影/上提…‘关系定型缺口’” | 页面真实、日期属实；但**无卡、无 frontier、单项目** | **越级**（C 当证据） | 保留论断但降为 C 级佐证；进 mechanism 的 C 证据表 + frontier；4b 只写“一个开源 EA 本体项目的实践文档（C）与另外两份实现互证” |
| P0-5 | 119 | “**建议阈值（推测）**：≥2 跳/反向查询 >20%；…语料 >10^4…” | **无源**；上游 mechanism 只有 6 条定性信号，没有这 6 个数 | **伪精度** | 删除整段数字；如需保留，写“示例阈值，未经验证，不作为判据” |
| P0-6 | 66 | “GitHub 搜索…**约 501 个仓库**…449★/185★/108★（检索快照 2026-11-12）…” | 无卡/无记录；2026-11-12 复跑为 **477**（同一查询） | **无源/不可复算** | 从正文删除；90.2c 记“检索快照 477（查询式+日期），不等于采用” |
| P0-7 | 64 | “除中泰外…**其余未找到第二家具名组织**把 OKF 跑在生产并披露规模/失败” | 结论方向可能仍成立，但“具名组织”过宽：Atlas/GMEOW/WordPress 站/SAP 帖都是具名或半具名实现 | **措辞过强** | 收窄为“未找到第二家**披露规模+失败+独立印证**的具名生产采用”；单列“实现/教程”不算 |

## 2. P1：应改（9 处）

| # | 行 | 原文 | 问题 | 改法 |
|---|---|---|---|---|
| P1-1 | 12 | “把 Karpathy 的 LLM Wiki 模式**形式化**” | Google 原话是 Karpathy “articulates this idea most crisply”；Linked.Archi 说“specified version of the pattern” | 改“规范化/规格化”；保留原引 |
| P1-2 | 20 | “v0.2 的 sources/verified/status/stale_after 先**解决**‘能不能信’” | 规范原文：记录信号，不给可信度分数；“advisory, not access control” | 改“提供信任信号，不解决真伪” |
| P1-3 | 22 | “把它当**前置层**可以，但别指望 Markdown 自己拦动作” | “前置层”是判断，不是规范词 | 标 `推测（设计判断）` |
| P1-4 | 37 | “它**不解决**什么：…身份/时点” | 身份/时点没有规范原文直接支持（`resource` 给 URI，`timestamp` 给时间）；属于分析 | 拆成“规范明确不解决（查询/存储/分类法）/ 我们的分析（身份粒度、as-of）” |
| P1-5 | 43–52 | 中泰段 | 有卡，但“OKF 当前置层不是纸上谈兵”是判断 | 保留事实，判断句标 `推测`；数字保留 |
| P1-6 | 58–62 | “它**证明** OKF 可以从 git 文件变成组织级目录条目” | Knowledge Catalog 是产品文档（C），示例是合成 | 改“官方文档**展示**了产品能力”；“证明”降为“产品能力，不证采用” |
| P1-7 | 76 | “**OKF 不会自己长成 ontology**” | 机制上正确（links untyped），但“不会”是强断言；无迁移案例≠不可能 | 改“不会自动长成；需要显式的 lift 工程（关系定型+人审）”，标 `已核（机制）/推测（普适）` |
| P1-8 | 96 | “**六类映射不了**：约束/推理/权限/执行/身份/时点” | 约束/推理/执行/权限有规范/实现支持；身份/时点是分析 | 表格分“规范明确没有”“实现中需另建”“我们的分析”三档 |
| P1-9 | 130 | “采用前要锁定版本/镜像” | 建议，不是证据 | 标 `建议（推测）`；或移 07 |

## 3. P2：顺手改（5 处）

| # | 行 | 问题 | 改法 |
|---|---|---|---|
| P2-1 | 30 | “文件路径就是 concept id” | 规范原文 “The file path is the concept's identity”；可保留 |
| P2-2 | 33 | “attestation（数值按约定计算）” | v0.2 原文是 Attested Computation 概念；保留但补“OKF 记录计算与检查方式，不执行” |
| P2-3 | 58 | “13 个字段…**没有 attestation 字段**” | 已核（digest §3）；保留，但补“有 computation/executor/attester” |
| P2-4 | 108 | “W3 不适合多数团队” | 判断，无源 | 标 `推测`；或删 |
| P2-5 | 140 | “Kunstenpunt…B” | 与 06.1 的 A/B/C 口径不符（B = 具名采用+独立信号） | 改为 `signal`，与 frontier 一致 |

## 4. 需要新增的上游（S2 产出）

1. ~~`src/web/semantics-2026-scimin-smw/`~~：初建后复核降 `signal`，**未入库**；论文（CEUR Vol-4293 paper50）只作 frontier 线索，要点：
   - 本体先行：SCIMIN-CRM & MWF Ontology 1.0（OWL/RDF；类/属性）；
   - SMW 映射：category→class、page property→object property、text/number→data property；
   - 工作流：PDF→WikiText→LLM 候选标注→自动校验（domain/range、datatype、结构、hallucination）→专家 HITL→受控同步到生产；
   - 边界：deployed demonstrator；无量化评估、无规模/成本；future work 明说。
2. `frontier.md` 新增/更新：
   - Linked.Archi（signal，单项目、无独立采用）；
   - Atlas OKF interop spike（C/signal，公司工程文档、1★）；
   - GMEOW OKF（C/signal，单项目）；
   - Zenodo NKB note / SAP community（**抓取失败，未核不引**，记“待评估”）。
3. `mechanism.md` OKF 节：新增“三份独立实现的共识/分歧”表；把“六类映射不了”拆三档；把 Kunstenpunt 从“反例”改为“数据标准先行的 signal”。

## 5. 审计后的 4b 结构（建议）

```
4b.1 它解决什么问题（成本/LLM/可加严）        — 分析，标推测处
4b.2 OKF 是什么（规范事实）                    — admitted
4b.3 谁在用（中泰 A；其他线索只指 90）         — admitted + 线索
4b.4 Google 的下一跳（Knowledge Catalog）      — C（产品能力）
4b.5 它和本体是什么关系（本次深挖）
   5a Google 的边界（已核）
   5b 两个方向：投影 vs lift（三实现互证，C/已核工程）
   5c 关系定型缺口与“什么映射不了”（三档）
   5d 生产/试点证据：中泰（OKF 先行，admitted）；SCIMIN（本体先行）与 Kunstenpunt（数据标准先行）均只作 signal
   5e 缺口：没有完成 OKF→本体迁移的公开案例（检索式+日期）
4b.6 什么时候值得升级（判据，推测；只留 3 条信号，指向 mechanism/07）
4b.7 边界/反例（执行/信任/年轻）
4b.8 三句话
```

## 6. 一句话

**4b 不是“内容错”，是“证据层级错位”**：把规范边界（不是本体）、映射机制（可以投影）、采用证据（有人在试）三件事，写成了一条“可以升级”的路。拆层、补证、降级，就能保留它的价值而不越级。

## 7. 处置结果（2026-11-12 当日关闭）

> 行号指**重写前**的 4b（git `18ca218` 版本）；重写后页已改结构，按小节标题对照。

| 项 | 处置 |
|---|---|
| P0-1 京东海博越级 | 移出 4b 正文，只留 [90.2c](../../deliverables/10-production-landscape/02-sections/90-sources.md#902c-okf--wiki-底座选项定义产品案例) 的 `signal` 行与 frontier |
| P0-2 SCIMIN 无源 | 先建卡判 `admitted`，**复核后降 `signal` 并移出 `src/`**（承建方自述、G3 无独立信号）；4b 只留线索、标“不撑任何判断”；正名 `CRM = Critical Raw Materials` |
| P0-3 Kunstenpunt 措辞过强 | 改“数据标准先行（兼容 CIDOC CRM/schema.org）”，删“一步到位”，降 `signal`，只留一句 |
| P0-4 Linked.Archi 越级 | 与 Atlas、GMEOW 一起作 C 级实现互证；入 frontier；不进 05 结论 |
| P0-5 伪阈值 | 整段删除；4b.6 只留 3 条可观测信号，完整判据回 mechanism |
| P0-6 GitHub 501 | 正文删除；90.3 记复跑 477 与查询式 |
| P0-7 “第二家具名组织” | 收窄为“没有第二家同时披露规模+失败+独立印证的具名生产采用” |
| P1-1…P1-9 | 逐条改：规格化、信任信号≠真伪、拆“规范不解决/我们的分析”、“展示”替代“证明”、“不会自动长成”（加机制限定）、映射缺口三档、建议标 推测 |
| P2-1…P2-5 | 保留路径即身份原文；补 Attested Computation 语义；补 13 字段含 computation/executor/attester；W3 不适用标 推测；Kunstenpunt 改 `signal` |

**未关闭**：Kunstenpunt 第二独立信号；SCIMIN 的独立评估（规模/效果/成本）；三份实现是否有生产用户；OKF→本体迁移完成案例（0）。

## 8. 复核教训：什么算“独立信号”

SCIMIN 我最初判 `admitted`，理由是“多机构 Horizon Europe 项目（I2）+ 项目内采纳（I3）”。这只对了一半，错在**把“项目多机构”当成“作者之外的独立信号”**：

| 问 | 松的判法 | 严格判法（本次采用） |
|---|---|---|
| 谁在说？ | 有六个作者、三个机构 → 多主体 | 六个作者同属**承建方** AKKODIS Research；他们在写**自己交付的系统** |
| I2 多主体？ | 项目有多机构 | 参与方是**同一个项目内部**的甲方/伙伴，不是独立于作者的第三方采用或治理 |
| I3 采用？ | 项目里部署了 | 部署者是作者自己；没有外部组织使用，也没有独立评估 |
| 影响外溢？ | — | 无第二篇报道、无外部复现、无社区讨论 |

**可复用的判据（记在这里，不另立规则）**：判断 I2/I3 时先问“这个机构与作者是什么关系、它用这套东西是不是因为作者在建它”；答案若是“同一个项目/同一家公司”，再多的机构也只是一个信号。

**同批复核的另一个例子**：三份实现（Linked.Archi / Atlas / GMEOW）能互证“映射非对称”，但它们的映射细节并不一致（`type` 各落到类 IRI / `rdf:type` / 自家实体类型）；引用时只能写“结构对应一致 + 结论一致”，不能写“映射规则一致”。
