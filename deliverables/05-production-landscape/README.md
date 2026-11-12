---
status: draft
deliverable_status: draft
updated: 2026-11-12
target: 想知道「本体落地到底靠不靠谱」的决策者 / 架构师 / 研究者
basis: E-28/E-29/E-30/E-31/E-32；8 条 admitted/probation 生产证据（含 Apple Glyph、百度 CoeusBI、联通 UniDataAgent）+ C/signal 类线索
---

# 05 · 落地现状：业界真实做得怎么样，有没有证据说它靠谱

> **读者**：要判断「现在要不要上本体、怎么选底座、怎么不被厂商案例忽悠」的决策者/架构师/研究者。
> **回答**：谁在生产里跑本体/语义层、什么形态、到什么规模、成本收益如何、靠谱与否有没有可靠证据。
> **不回答**：怎么建（去 [04](../04-worked-example/README.md)）、具体怎么做（去 [02](../02-engineering-playbook/README.md)）、凭什么（去 [03](../03-mechanism-reference/README.md)）、值不值得投（去 [01](../01-capability-status/README.md)）。
>
> **定性：现状（描述·实证）**。本份只描述现状与证据，不讲怎么建；定位全文见 [SCOPE](./SCOPE.md)。
>
> **一句话配比**：8 条生产证据里，严格 OWL/对象本体只有 **1 条**（Netflix），语义层/标签层 **6 条**，业务本体试点 1 条。所以本份答的是「**本体在生产里以什么薄形态存在**」，不是「本体塔普及了吗」。

## 先看一个真实问题

券商要按“2026 年某月末的客户资产层级”回看各月“融资利率”——“客户”按哪个时点分层、“资产”含不含未成交委托、“利率”是合同利率还是实际计息、历史月要不要沿用同一分组，四个词各有两种以上口径。查询能跑，业务问题却答不了。这不是假设，是中泰证券在 CCSA TC601 案例里描述的现场。**05 回答的就是：这类东西业界谁在跑、跑到什么规模、有没有证据说它靠谱。**

> **主线**：这份的主线是一条问题链：**① 谁在生产里跑 → ② 坑在哪 → ③ 为什么两国证据长得不一样 → ④ 钱花在哪 → 所以今天该怎么做**。对应关系：① [03 美国](./02-sections/03-us.md) / [04 中国](./02-sections/04-china.md)（底座五选一、本体做多薄）；② [06 案例](./02-sections/06-cases.md)（失败主诉在语义定义/权限）；③ [02 地图](./02-sections/02-map.md) / [04b OKF](./02-sections/04b-okf-wiki.md)（证据不对称、Wiki 只是一种底座）；④ [05 经济](./02-sections/05-economics.md)（有价无账）；最后 [07 决策](./02-sections/07-decision.md) / [08 边界](./02-sections/08-boundaries.md)（90 天四个数、什么时候停）。

> **内码**：E-28–E-32 是上游结论编号，正文都给了要点；想看原文见 [conclusions](../../topics/conclusions.md)（可选，不影响阅读）。

## 30 秒结论

1. **生产里跑的是「底座 + 薄本体/语义层」，不是自建本体塔。** 先看配比：真正是 OWL/对象本体的只有 **Netflix**（领域专用）；中泰是治理语义层已生产、业务本体在试点；Snowflake / Sigma 是 **BI 语义层**。公开可核的 2026 案例绝大多数长在已有底座上：数仓语义层（Snowflake 5,600 员工/320k 查询/月）、dbt/Dagster 语义工程（Sigma 2,883 模型/63 job/6 region）、治理知识库+DataAgent（中泰 9,137 知识目录/6,503 指标文档/12 万+ 血缘）。**另有一类只有产品文档、没有生产案例**：数据库内嵌薄本体（阿里 Context0，类型≤100/关系≤300，C 类）。**例外是领域专用自建**（Netflix QuipuDB；京东 Oxygen 商品本体，signal），不是通用平台；**没有找到从零自建通用本体平台的公开成功案例**（E-28）。
2. **失败不在图引擎，在语义定义与权限。** 影子实体、口径漂移、权限按人特批、聚合泄露、朴素语义视图延迟、预聚合维护爆炸——这些才是生产复盘里的坑（E-29）。
3. **美国公开证据领先在「语义层/上下文层」，中国领先在「大厂平台 + 内部大规模图谱 + 单点行业实践」。** 这是**公开证据的不对称**，不是能力排序；两边都缺「规模+成本+失败+独立印证」齐全的案例（E-30）。一个反直觉的细节：**中国五家大厂平台 2026-06 后没有一条具名客户**；客户自述（三家农商行）与采购集中在海致星图/星环/NebulaGraph/Neo4j/金山云等；五平台之外另有**小红书 DIBP**（覆盖 80%+ 员工、周活 8,800+，议题摘要级，B）。成本拐点降的是启动/抽取成本，不是定义治理/维护成本（E-31，`推测`）；价格锚点已有，**客户自述的投入/人月有两条**（江西 <50 万上限、江南 3 人×12 月），全生命周期账本仍缺。

> **Wiki/OKF 是底座选项之一**：如果知识还散在 Wiki/文档里，可以选 Google OKF（Markdown + YAML frontmatter；concept/links/来源/信任）统一概念、术语、来源与 owner；也可以选数仓语义层、本体平台、图库或数据库内嵌。OKF **成本低、对 LLM 友好，也不是必经层**，可以长期用。它与本体之间是**两个方向**：本体→OKF 可机械投影但丢语义；OKF→本体是有损草稿 + 关系定型人审；公开证据里**还没有人走完「OKF → 本体」这一跳**——中泰是 OKF 先行、业务本体在验证；“本体先行的 wiki”只有承建方自述的会议论文（`signal`），不撑结论（见 [4b](./02-sections/04b-okf-wiki.md)）。
>
> **一句话**：本体落地已经不是「建不建塔」，而是「底座选谁 + 薄本体怎么治理」。今天能回答「谁在跑、什么形态、公开证据到哪」；还不能回答「哪家最好、ROI 多少」。

## 这份怎么读

| 你手上的问题 | 读 | 得到什么 |
|---|---|---|
| 想先看一张图 | [01 导读 §1.5 图目录](./02-sections/01-GUIDE.md#15-本份的图快速解读用) | 问题链五步 + 6 张图的落点；先速读再进正文 |
| 先看全貌 | [00 一页答案](./02-sections/00-overview.md) | 4 条判断 + 证据天花板 + 一页地图 |
| 我属于哪种情况 | [01 导读](./02-sections/01-GUIDE.md) | 10 分钟/1 小时/深读路径 |
| 到底有哪些形态 | [02 地图](./02-sections/02-map.md) | 底座→本体→应用分层；重→轻谱系；美/中对照 |
| 美国到底谁在跑 | [03 美国](./02-sections/03-us.md) | Palantir / Snowflake / Sigma / Stardog / Ontotext 等 |
| 中国大厂有没有方案 | [04 中国](./02-sections/04-china.md) | 阿里/蚂蚁/腾讯/华为/百度 + 中泰证券 |
| Wiki/OKF 作为底座选项 | [04b OKF/Wiki](./02-sections/04b-okf-wiki.md) | OKF 的价值与边界、中泰采用、两个方向（投影/上提）与“没有完成迁移”的缺口 |
| 成本/收益怎么算 | [05 经济](./02-sections/05-economics.md) | 五项成本、收益点、build vs buy、TCO 缺口 |
| 有哪些案例、各能证明什么 | [06 案例台账](./02-sections/06-cases.md) | A/B/C（+signal）分级 + 规模/失败/限制 |
| 我该先做什么 | [07 决策](./02-sections/07-decision.md) | 5 个选型问题 + 90 天试点 + stop |
| 哪些话不能信 | [08 边界](./02-sections/08-boundaries.md) | 不能回答的问题、反例、什么会改变结论 |
| 出处/检索日志 | [90 来源](./02-sections/90-sources.md) | 来源台账、C 类线索、阴性结果 |

## 证据基座（2026-11-12）

| 类 | 数量 | 说明 |
|---|---|---|
| **admitted / probation 生产证据** | 8 | 中泰 QCon、中泰 CCSA、Snowflake、Sigma、Netflix、Apple Glyph、百度 CoeusBI、联通 UniDataAgent；前五条追到 `src/web/` 卡，后三条追到 `src/papers/` digest |
| **admitted 格式证据** | 1 | Google OKF（格式定义，`admitted`）；它只证格式，不证采用/效果 |
| **C / signal 类线索** | 15+ | Palantir 公告、阿里 PolarDB/Context0、蚂蚁 TuGraph、腾讯 DataBuddy/Topbase、华为 DataArts、京东 Oxygen/海博、Google Knowledge Catalog、Kunstenpunt、SCIMIN/SMW（本体先行自述）、Linked.Archi/Atlas/GMEOW（映射实现）、Atlan、Anthropic、AngelList、AWS、VB Pulse、**小红书 DIBP（B）**、**NHS FDP（FOI 调查）**、**Greptime 504 次对照（厂商 benchmark）**；只证「有方案/有讨论/有披露」，不撑采用/效果 |
| **明确 gap** | 9 | 无「规模+成本+失败+独立印证」四项齐的 A 类；无全生命周期 TCO/ROI（有价目/合同/客户自述投入，无同一买方配对）；五平台无客户侧（已判 0）；无失败率；无生产级同数据集对照；无项目级 postmortem；Snowflake/Sigma/Glyph 第二信号阴性；**无 OKF/Wiki→本体迁移完成案例**；**非中美地区无生产案例**（NHS 是「宣称 vs 使用」落差，不算 postmortem） |

> **读法**：先看等级，再看日期，再看有没有独立信号。厂商案例页/产品文档默认 C；单公司工程博客默认「作者报告」，不默认「行业规律」。

## 维护

- 正文只从 admitted/probation 证据抽取；C/signal 类只进 [90 来源](./02-sections/90-sources.md)、[06 案例台账](./02-sections/06-cases.md) 的「线索」列与 [04 中国](./02-sections/04-china.md) 的「方案存在」段，不撑结论。
- 图在 [`_figures/`](./_figures/)，索引在 [01 §1.5](./02-sections/01-GUIDE.md#15-本份的图快速解读用)。**改正文数字/等级时同步改图**（图内数字都能在正文找到原值）；图只做速读，判断仍以正文/E-xx 为准。
- 新证据先回 `topics/06-measure/feasibility/mechanism.md` 的「生产落地图景」与 `src/web/` 卡，再改本份；不在交付物里新增判断。
- 改了判断 → 回改 E-28–E-32 与 [state](../../meta/status/state.md)；跑 `python3 meta/tools/check_repo.py`。
- 定位改动走 [SCOPE](./SCOPE.md) 与 [ADR 0014](../../adr/0014-deliverable-scope-single-home.md)。
