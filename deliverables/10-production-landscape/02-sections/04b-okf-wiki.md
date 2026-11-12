---
status: draft
updated: 2026-11-12
parent: ../README.md
---

<a id="4b-okf"></a>
# 4b. Wiki/OKF：底座选项之一，但“靠向本体”要拆成三件事

> 本页回答：直接上完整本体太贵，Wiki/OKF 能不能作为一条更便宜的路？它可以长期用，还是只在某些阶段用？ ｜ 读完你能：判断你的场景该停在 OKF、长期并行，还是值得另建本体/语义层。
>
> **先说结论**：OKF/Wiki 是**底座选项之一**，可以长期并行，也可以按需另建语义层；但它**不是一条“会自动长成本体”的路**。OKF 是 Google 的开放知识格式（v0.1 2026-06-12，v0.2 2026-07-24；[卡](../../../src/web/google-okf/google-okf.card.md)），把“一概念一 Markdown”的 LLM Wiki 模式**规格化**为可交换格式；它把“知识可读、可审、可版本化、可溯源”做便宜了，执行侧的约束/权限要另接。它与本体之间是**两个方向**：本体→OKF 可机械投影但丢语义；OKF→本体是有损草稿 + 关系定型人审。截至 2026-11-12，**没有找到任何组织完成“OKF/Wiki → 本体”迁移的公开案例**；能看到的相邻形态都只是**自述或规划**：中泰是 OKF 先行、业务本体在验证（`admitted`）；“本体先行的 wiki”只有一篇承建方会议论文（`signal`，见 4b.5.4）。

## 4b.1 它解决什么问题

不要先问“它算不算本体”，先问“它把哪段成本降下来了”。OKF 的价值在三件事（分析，非规范原文）：

1. **生产成本低**：一份 Markdown 就是一个 concept；不需要 SDK/runtime，git 就能版本化；人可读、agent 可读，改一处不用动整套系统。
2. **对 LLM 友好**：concept 一文件、frontmatter 少量结构化字段、链接成图；LLM 可以读、写、补交叉引用、批量改十几个文件——这正好是 Wiki 最容易烂掉、而 LLM 最擅长的记账工作。
3. **可逐步加严**：v0.2 的 `sources`/`verified`/`status`/`stale_after` 先提供**信任信号**（不是真伪保证）；需要执行约束/权限/跨页关系时，再接语义层/本体。

**边界**：它负责“把知识组织好、让人和 agent 都能用”，不负责执行/约束/权限；这些要语义层/策略引擎。把它当前置层可以，但别指望 Markdown 自己拦动作（`推测`，设计判断）。

## 4b.2 OKF 到底是什么

| 项 | 内容 |
|---|---|
| **提出者** | Google Cloud（开放规范，Apache-2.0；不是 W3C/ISO 标准） |
| **版本** | v0.1 2026-06-12；v0.2 2026-07-24（加信任信号） |
| **形态** | bundle = 一个目录的 Markdown 文件；一个 concept 一个文件；文件路径就是 concept id |
| **必填** | v0.1 只有 `type`；约定 `title`/`description`/`resource`/`tags`/`timestamp` |
| **图** | concept 之间用普通 Markdown 链接；链接图就是知识图；`index.md` 做渐进披露，`log.md` 做历史 |
| **v0.2 信任信号** | `sources`（来源/作者/使用量/更新时间）、`generated`/`verified`（谁生成、谁独立确认）、`status`/`stale_after`（生命周期/过期）、`attestation`（Attested Computation：记录计算与检查方式） |
| **运行** | 不需要 SDK/runtime；可在 git、Obsidian、Notion、MkDocs、静态文件服务器里读 |

**它解决什么**：知识碎片化、不可移植、不可审、不可版本化、agent 读不到；它让“同一份知识”同时被人读、被 agent 读、被 git 管。
**它不解决什么**：概念/关系的公理语义、约束/基数、推理、查询执行、策略/权限。身份粒度与 as-of 时点属于**我们的分析**（规范给 `resource` URI 与时间戳，但不定义实体同一性与有效期语义）。

> **规范原文的硬证据**（SPEC.md v0.2，2026-11-12 抓取；[卡](../../../src/web/google-okf/google-okf.card.md)）：whole-word 统计全文 **0 次**出现 ontology / RDF / OWL / SHACL / SPARQL / knowledge graph；`semantic layer`（空格）0 次，`Semantic-layer`（连字符）只在 §12.3「Considered and deferred」出现 **1 次**，是 attester 的未来工作目标。non-goals 明确放弃“固定概念类型分类法”“规定存储/服务/查询基础设施”“替代领域 schema”。这不是我们解读，是 Google 自己划的边界。v0.2 原文还写：`Crucially, OKF records the computation and how to check it; it never executes anything itself.`；信任分级 `advisory signals, not access control`。

## 4b.3 谁在用：一个 A 类案例，其余都还只是线索

**中泰证券 2026-10-15 的 CCSA TC601 WG15 案例**（[卡](../../../src/web/modb-2026-zhongtai-ontology/modb-2026-zhongtai-ontology.card.md)，`admitted`，本份口径 A 类）明确写：知识载体采用**开放知识格式（OKF）**，参考 Google Cloud 的开放知识格式和 Anthropic 的仓库化知识实践，以**带轻量结构化头部的 Markdown** 保存知识；一份文档既能供人读/审，也能被检索、供 agent 上下文、支持后续 SQL 校验。注意：这是 **Google OKF 的本地化变体**（同时混了 Anthropic 仓库实践），不是 Google 官方客户/认证案例。

它做到了什么：

- **规模**：9,137 份知识目录、6,503 个指标文档、2,622 张可检索表、12 万余条物理血缘。
- **生产分工**：三泳道——字段/公式/血缘等技术事实由程序整理；模型只补业务摘要/别名/常见问法；模型解释必须过来源证据核验；没有依据的语义内容剔除。
- **门禁**：检索依据不足继续查；口径不明向用户澄清；核心字段缺证据返回缺口清单；校验不通过不交付 SQL。
- **演进边界**：数据领域的治理语义层已在生产；**业务本体仍在信用业务经营分析场景验证**（“已启动业务本体演进探索”），不是全公司本体生产系统。原文：`现有 OKF 文件继续作为权威源与交换格式，后续规划引入图数据库支持血缘穿透和对象关系计算`——**“写模型/读模型”是我们的概括，原文只写“继续作权威源与交换格式”**。

**这说明**：OKF 当前置层不是纸上谈兵；中泰用它把“指标/元数据/血缘/业务解释”组织成可检索、可追溯的知识，再往业务本体走。**但它也说明**：OKF 只走到“知识可调用”，业务本体是下一层，还没全面上线。

**其余线索（不撑结论）**：

- **京东海博**（2026-09-24，`signal`）：媒体转述称其用 OKF 建“项目—角色—Skill”知识体系，并给了 AB 时间数；但**单一来源、无个人署名、原文 5 次写“OKF”从未展开缩写，“= Google OKF”是推断**。细节只放 [90 来源](./90-sources.md#902c-okf--wiki-底座选项定义产品案例)，本页不拿它当采用证据。
- **工具/框架实现**（Atlas、GMEOW、Linked.Archi，均 C）：它们证明“有人在做 OKF ↔ 图/RDF 的导入导出”，**不证明企业采用**；见 [4b.5](#4b5-okf-和本体是什么关系两个方向一条缝)。
- **教程/专栏**（2026 年多篇，C）：证明“有人在教”，不证明“有人在生产用”。

> **截至 2026-11-12**：除中泰外，**没有找到第二家同时披露规模、失败/限制、且有独立印证的具名生产采用**。这个缺口要如实写，不能拿“Google 发布”当“企业采用”，也不能拿“有工具实现”当“有人上线”。

## 4b.4 Google 的下一跳：OKF → Knowledge Catalog

Google 2026-08-26 的博客（[原文](https://cloud.google.com/blog/products/data-analytics/scale-okf-bundles-across-an-organization-with-knowledge-catalog)）给了 OKF 的“组织级”路径：把 OKF bundle push 进 **Knowledge Catalog**，每个 concept 变成一个 Entry，继承 IAM；`index.md` 变成可浏览层级，`okf` Aspect 带 13 个字段（`okf_type`/`generated`/`sources`/`verified`/`status`/`stale_after`/`usage_window`/`runtime`/`parameters`/`computation`/`executor`/`attester`/`extra`——**没有 `attestation` 字段**），可被搜索/过滤/权限控制。

- **它展示**：OKF 可以从“git 里的文件”变成“组织级可治理的目录条目”——这是**产品能力**（C），不是客户采用。
- **它不证明**：客户采用/规模/效果；官方示例 `acme_retail` 是**合成**的美国零售商 bundle（9 个 leaf concept/17 个 Entry），不是客户案例。
- **关键边界**：Knowledge Catalog 给的是**目录/治理/检索 + IAM**；要推理/约束/执行，还得另接语义层。权限来自 Catalog，不来自 OKF 格式本身。

## 4b.5 OKF 和本体是什么关系：两个方向、一条缝

> 这是本页最容易被写错的一段。旧稿把“可映射”写成“可以升级”，把“有人做”写成“有人迁移完成”。下面按**方向**拆开，只写有来源的部分；分级见段末。

### 5.1 Google 自己划的边界

- 规范全文 **0 次** ontology/RDF/OWL/SHACL/SPARQL/knowledge graph；`semantic layer` 只在 §12.3“Considered and deferred”出现 1 次（Looker/dbt 模板，未来工作）。
- non-goals 明确：不定义固定概念类型分类法、不规定存储/服务/查询基础设施、不替代领域 schema。
- “never executes anything itself”；信任分级是“advisory signals, not access control”。
- **结论（已核）**：OKF 不是本体，也不是语义层；Google 没有把“升级为本体”写进规范或路线图。

### 5.2 两个方向：投影 vs 上提

**方向一：本体 → OKF（投影，可机械完成、有损）**

- **映射细节并不统一**（这点旧稿写错了）：同为 `type`，Linked.Archi 把它落到 ArchiMate/BPMN 的类 IRI，GMEOW 把 `Class`/`Property`/`Individual` 字面量翻成 `rdf:type`，Atlas 则落到自己的实体类型（table/view/metric）并强调 `type` 是自由文本。三者真正一致的是**结构对应**：`resource` → IRI、`tags` → 词表概念、**无类型的 Markdown 链接 → 有向边（关系种类丢失）**。
- 三份独立实现的原文：
  - [Linked.Archi](https://meta.linked.archi/docs/practice/okf-open-knowledge-format/)（2026-07-17，C）：“The projection is mildly lossy — `am:realizes` flattens to an untyped markdown link — but for retrieval and progressive disclosure that is exactly enough.”
  - [Atlas](https://github.com/AtlasDevHQ/atlas/blob/main/docs/research/okf-interop-spike.md)（2026-07-02，C）：“export is easy and total”；但 “what foreign consumers **lose is semantics, not data**”；表白名单/运行时执行没有 OKF 对应物。
  - [GMEOW](https://github.com/Blackcat-Informatics/gmeow-ontology/blob/main/docs/okf.md)（发布日未标；2026-11-12 抓取，C）：OKF 是 “**LOSSY down-projection**”，只带 flat term surface；OWL 公理/RDF-star/对齐图留在 canonical 源。
- **结论**：投影可以全量，但**丢的正好是语义**（关系类型、公理、约束、执行）。`已核（三份工程文档一致）`；不外推为生产规律。

**方向二：OKF → 本体（上提，有损草稿 + 关系定型人审）**

- `type` → OWL class、`resource` → IRI、`tags` → SKOS concept 可以机械映射。
- **Markdown 链接没有类型**：要把 `[Customer Management]（…）` 变成 `am:realizes`，必须“作者提示或人审确认的推断”。Linked.Archi 原话：“requires either an author-supplied hint or a human-confirmed inference.”
- Atlas 的 import 直接叫 “a useful but genuinely **lossy draft generator**”，并把导入的 metric SQL 标 `okf.unverified_sql: true`，不让它静默升格为权威 metric；GMEOW 的 lift 要求封闭 `okf:` profile，未知键硬失败。
- **结论**：上提是**草稿生成 + 人工定型**，不是读一遍就得到本体。`已核（三份工程文档一致）`。

**这条缝：关系定型（relationship-typing gap）**

- 三份实现都指向同一处：OKF 的链接只断言“有关系”，不断言“什么关系”；关系类型/基数/方向在正文里。Linked.Archi 把它命名为 “the relationship-typing gap”，并说这是 Information 层到 Knowledge 层的缝。
- 这不是 OKF 的缺陷，是它的设计（consumer 不得因未知 type/坏链拒绝）。但它是**上提成本的主要来源**：文档越多，需要人审的链接越多。

### 5.3 什么映射不了（分三档，不再一句“六类”）

| 档 | 项 | 依据 | 能否补 |
|---|---|---|---|
| **规范明确不做** | 固定类型分类法、存储/查询基础设施、替代领域 schema | SPEC v0.2 non-goals（已核） | 要另建 ontology/semantic layer |
| **规范明确没有** | 执行（OKF 记录计算与检查方式，never executes）、ACL/策略（advisory signals, not access control） | SPEC v0.2 / v0.2 博客（已核） | 要另接执行/策略层 |
| **实现/分析** | 形式约束（SHACL/OWL 公理）、推理、关系类型/基数、身份粒度、as-of 时点 | 三份实现（C）+ W3C 标准卡（已核） | 要建模 + 人审 + 版本化 schema |

### 5.4 证据：两个方向都有人做，但没有“完成迁移”的案例

- **本体先行（只有 `signal`，不撑结论）**：[SCIMIN-CRM · Semantic MediaWiki](https://ceur-ws.org/Vol-4293/paper50.pdf)（SEMANTiCS 2026 / CEUR Vol-4293 paper50，2026-10-13）描述了一套 OWL 本体 + Semantic MediaWiki 的做法：`Category` 对齐类、`page` 属性对齐对象属性、`text/number` 属性对齐数据属性；LLM 只产候选标注，先过 domain/range、datatype、hallucination 校验，再由领域专家 HITL 复核，两关都过才同步到生产。**为什么只算线索**：这是**承建方（AKKODIS Research）写自己的 demonstrator**，G3 的“多机构/采用”都在同一个 Horizon Europe 项目内部，不是独立采用；无量化/规模/成本，论文自述评估是 future work。`CRM = Critical Raw Materials`（关键原材料），不是客户关系管理。
- **数据标准先行（signal）**：Kunstenpunt 先用 2024 年 Flemish 文化参与数据标准（兼容 CIDOC CRM/schema.org）统一三套旧库，再并进 Wikibase；约束只警告不阻断（[原文](https://tech-news.wikimedia.de/2026/06/02/kunstenpunt-a-whos-who-of-the-flemish-art-scene/)，`signal`，单机构）。
- **OKF 先行（有生产，但下一跳未完成）**：中泰用 OKF 作权威源/交换格式，图数据库/对象关系写在后续规划，业务本体仍在信用业务验证（`admitted`）。
- **完成迁移**：截至 2026-11-12，公开渠道**没有找到**任何组织披露“OKF/Wiki → 本体”的完成案例（有路径、时间线、成本、失败）。这是检索阴性，不是“不存在”。检索式与渠道见 [90 来源](./90-sources.md#902c-okf--wiki-底座选项定义产品案例)。

### 5.5 这意味着什么

- **“OKF 会自己长成 ontology”是错的**：它不会自动长；要显式的上提工程（关系定型 + 人审 + 版本化 schema）。Linked.Archi 也明说两者 “neither is an evolution of the other”，只是同一阶梯的相邻层。
- **“先 OKF、后本体”是设计建议，不是观测路径**：Linked.Archi 说 “Most organizations will not choose once… start with OKF-style markdown… then promote the specific, high-value domains”；这是 C 级框架作者的判断，不是迁移完成记录。中泰的方向与它一致，但中泰自己也还没走完。
- **可行的组合是“OKF 捕获/交换 + 本体推理/治理”**：这是三份实现与本页分析的共同指向（`推测`，设计判断）；它要求你在 W1 就定义“哪些概念/关系会进本体、谁负责、用什么约束”，而不是等文档堆到几万份再回头补。

## 4b.6 什么时候才值得上本体：3 条信号（设计判据，`推测`）

> 下面是**设计判据**，不是实测门槛；没有一条公开案例按它走完。完整判据（W0–W3）在 [mechanism](../../../topics/06-measure/feasibility/mechanism.md#okf-2026-11)，本页只留可观测的三条。

1. **业务问题需要跨页关系查询**（不是关键词/向量检索）：例如“停掉这个系统，哪些能力会断”。
2. **约束/权限必须执行**（不能只在 prompt 里提醒）：违规会进对外报表、或权限要按任职关系计算。
3. **≥2 个 agent/应用需要同一套稳定 schema**：同一概念在不同 agent 里开始出现两个“官方版本”。

命中两条以上，再考虑本体/语义层；**没有这些信号，长期停在 OKF 是合理选择，不是落后**。不要把“文件多了”当升级信号——文件数不是语义/执行信号。

## 4b.7 四个反例/边界

1. **OKF 不负责执行**：它把“知识可读/可审/可版本化”做便宜了；约束/权限/查询要另接语义层，别指望 Markdown 自己拦。
2. **agent 写库的信任问题**：v0.2 的 `verified` 是信号，不是保证；没有独立 producer/审计，conformance 不等于正确。“一个充满编造内容的合规 bundle，和一个经过审计的 bundle，验证结果一样干净”是工程社区的批评（C 级，[grounded-forge](https://raw.githubusercontent.com/chrisgagne/grounded-forge/refs/heads/main/docs/architecture/okf-interop.md)），不是规范结论。
3. **规模不是升级信号**：本份没有可引用的规模基准；文件数可以很大，但真正触发升级的是**语义/执行/权限**，不是文件数。
4. **格式还很年轻，别当稳定标准**：2026-06 发布后五个月两次搬家（`knowledge-catalog/okf/` 冻结 → `GoogleCloudPlatform/open-knowledge-format` → 官方 PR #63 指向中立组织，但目标仓库 2026-11-12 实测 **404**）；**没有 v0.3**（无 tag/release，SPEC 仍是 v0.2）；canonical 仓 main 只有 **6 commits、1 位作者、51 个 open issue**（2026-11-12 抓取），main 最新 commit 是 **2026-08-21**。采用前要锁定版本/镜像，不要把“Google 发布”当“长期治理已稳”。

> **标准提醒**：Google 是公司，不是标准组织；OKF 是开放规范，不是 W3C/ISO 标准。引用时写“Google OKF”，不要写“行业标准”。

## 4b.8 给读者的三句话

1. **把 OKF 当底座选项之一**：统一概念/术语/来源/owner/版本，让同一份知识被人和 agent 共读；这比一上来建本体塔便宜得多。它可以长期用，也可以按需另建语义层；不是每个团队都必须走。
2. **把“OKF 靠向本体”拆成两件事**：投影（本体→OKF）可以机械做，但会丢关系类型/公理/约束；上提（OKF→本体）是有损草稿 + 关系定型人审。**没有“自动长成”这回事**；要本体，就在 W1 定义目标概念/关系/约束/owner。
3. **用信号而不是感觉决定要不要上本体**：跨页关系查询、约束/权限要执行、多 agent 共用稳定 schema——命中两条，再上本体/语义层；不命中，就长期用 OKF。**公开证据里还没有人走完“OKF → 本体”这一跳**，所以这是设计判断，不是已验证路线。

## 4b.9 证据台账（本页只认这些）

| 证据 | 日期 | 等级 | 能证明 | 不能证明 |
|---|---|---|---|---|
| [Google OKF 规范 v0.1/v0.2](../../../src/web/google-okf/google-okf.card.md) | 2026-06-12 / 07-24 | `admitted`（定义） | 格式、字段、non-goals、词频；不是本体/语义层 | 采用、效果、迁移 |
| [中泰 CCSA TC601](../../../src/web/modb-2026-zhongtai-ontology/modb-2026-zhongtai-ontology.card.md) | 2026-10-15 | `admitted` / A 类 | OKF 承载 9,137 知识目录；业务本体在验证 | 本体全量、成本、准确率 |
| [SCIMIN/SMW 论文](https://ceur-ws.org/Vol-4293/paper50.pdf) | 2026-10-13 | `signal`（承建方自述；不入 `src/`） | 有一篇会议论文描述“本体先行的 wiki”做法 | 采用、规模、效果、成本；**不撑本页任何判断** |
| [Knowledge Catalog 集成](https://cloud.google.com/blog/products/data-analytics/scale-okf-bundles-across-an-organization-with-knowledge-catalog) | 2026-08-26 | C（产品能力） | bundle→Entry、IAM、13 字段；示例是合成 | 客户采用、规模、效果 |
| [Linked.Archi](https://meta.linked.archi/docs/practice/okf-open-knowledge-format/) · [Atlas](https://github.com/AtlasDevHQ/atlas/blob/main/docs/research/okf-interop-spike.md) · [GMEOW](https://github.com/Blackcat-Informatics/gmeow-ontology/blob/main/docs/okf.md) | 2026-07-17 / 07-02 / 日期未标 | C（实现/框架） | 映射非对称、关系定型缺口、投影有损 | 生产采用、迁移完成 |
| [Kunstenpunt Wikibase](https://tech-news.wikimedia.de/2026/06/02/kunstenpunt-a-whos-who-of-the-flemish-art-scene/) | 2026-06-02 | `signal` | 数据标准先行、约束只警告、3 人维护 | 独立印证；与 OKF 无关 |
| [京东海博](http://stock.10jqka.com.cn/20260924/c680274369.shtml) | 2026-09-24 | `signal` | “有人在说” | 采用、效果；OKF 缩写未展开 |

> **最大的 gap**：截至 2026-11-12，**没有找到任何组织公开完成“OKF/Wiki → 本体”的迁移**（有路径、时间线、成本、失败）。中泰最接近，但它把“图数据库 + 对象关系计算”写在后续规划里；唯一的“本体先行 wiki”是承建方自述的 `signal`，不是独立采用。所以本节的“升级判据”是**设计判据（推测）**，不是已被验证的路径；写方案时不要把“可以衔接”写成“已经衔接”。而且**这不等于每家公司都必须走**：没有升级信号，长期停在 OKF 完全合理。
