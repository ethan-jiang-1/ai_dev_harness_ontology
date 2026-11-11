# AGENTS.md

> **宪章（最高约束）**：[CHARTER](./CHARTER.md)。本仓库是研究档案，不是工程项目；我们只做消化、组织、研究，不做实施。任何“把它跑起来/补个实现”的冲动，先读宪章；宪章优先于本文件。

本仓库是**持续生长的研究档案**：材料进来 → 精读成卡 → 沉淀成主题 → 抽成交付物。交付物是文档，不是代码。

任何改动都该让某条判断更清楚、更有证据，或更可证伪。

## 入口

- 流水线全景与目录推导：[README](./README.md)
- 研究问题与假设：[THESIS](./THESIS.md)
- 术语（动笔前先对齐用词）：[GLOSSARY](./GLOSSARY.md)
- 按需加载（渐进披露）：[meta/loading](./meta/loading.md)
- 当前状态与阻塞：[meta/state](./meta/state.md)
- meta 里有什么：[meta/README](./meta/README.md)
- 本地噪音：`.tmp-venv/`、`.pi/` 不是仓库内容；搜索/统计时排除

## 先定位落点

| 你在做什么 | 落点 |
|---|---|
| 存原文 | `src/papers/{arxiv_id}-{slug}/`（论文，一篇一目录）或 `src/web/`（网页）；论文在 [manifest](./src/papers/manifest.md) 登记 |
| 读一篇论文 | 先读同目录 `digest.md`（自包含，下游唯一入口）；要核引文再看 `paper.md` / `references.md` / `appendix.md` |
| 记一篇论文的来源 | 同目录 `card.md`（来源卡：元数据 + 一页索引 + 图表位置）；用 [论文卡模板](./src/_templates/paper-card.md) |
| 消化一篇论文 | 同目录 `digest.md`（自包含长文：术语/方法/数字条件/边界/工程用法）；用 [digest 模板](./src/_templates/paper-digest.md) |
| 存博客/工程材料 | `src/web/`；卡同目录 `<stem>.card.md`，用 [材料卡模板](./src/_templates/material-card.md) |
| 存一个开源项目 | `src/open-source/{org}-{repo}/`；先过 [选择标准](./src/open-source/README.md)，pin commit，不 vendor 代码 |
| 读一个开源项目 | 先读同目录 `digest.md`（自包含，下游唯一入口）；没有 digest 时读 `card.md` + `code-map.md`，并标「未入库」 |
| 记一个开源项目的来源 | 同目录 `card.md`（repo/commit/license/本体在哪/调用点/证据入口）；用 [开源卡模板](./src/_templates/open-source-card.md) |
| 消化一个开源项目 | 同目录 `digest.md`（代码怎么走/执行还是装饰/证据与边界）；用 [开源 digest 模板](./src/_templates/open-source-digest.md) |
| 综合几个来源、形成判断 | `topics/`，用 [机制笔记模板](./meta/note-template.md) |
| 写子机制的详细论证 | `topics/<派>/<子主题>/README.md`；派 README 只留地图 |
| 记本派结论 | `topics/<派>/claims.md`（`L-xx`）；跨派才升 conclusions |
| 列本派证据 | `topics/<派>/sources.md` |
| 跑一个子主题 | `topics/<派>/<子主题>/prompt.md`；输出放 `runs/` |
| 修订跨主题结论 | [topics/conclusions.md](./topics/conclusions.md) |
| 查时刻/接缝 | [topics/seams.md](./topics/seams.md) |
| 查执行形态 | [topics/execution-forms.md](./topics/execution-forms.md) |
| 找某派前沿/候选 | `topics/<派>/frontier.md`，方法见 [topic 协议](./meta/topic-research-protocol.md) |
| 做成对外物 | `deliverables/`，只从 `topics/` 抽取 |

`topics/` 内按**本体凭什么起作用**分六派：`01-constraint`（拦动作）、`02-judgment`（验产出）、`03-knowledge`（喂上下文）、`04-state`（跨轮记忆）、`05-produce`（造与修）、`06-measure`（量它有没有用），底座是 `00-harness`（控制回路七部件）。

六派是 **4+1+1**：`01-04` 是回路内的四个介入点，`05` 是回路前（来源），`06` 是回路外（尺子）。归派一句话：**01-04 问时刻，05 问来源，06 问尺子；跨派按主效应归派并标双重身份。** 时刻轴见 [seams](./topics/seams.md)；形态轴见 [execution-forms](./topics/execution-forms.md)。

卡片与主题页的字段：`status`（文档成熟度）/ `source_type`（素材类型）/ `reading`（读到哪）/ `provenance`（一手/转述）/ `evidence_role`（对中心问题提供哪类证据）/ `execution_form`（以什么形态被执行），定义见 [conventions](./meta/conventions.md#字段与词汇)。

**派内可以再有子主题**：`topics/<派>/<子主题>/README.md`。派 README 只做地图与硬证据；详细机制在子主题。子主题按子机制命名，不按来源类型；成立条件见 [ADR 0003](./adr/0003-subtopics-and-source-types.md)。

**改一个派只动该派目录**：`README.md` / `claims.md` / `sources.md` / `frontier.md` / 子主题。只有跨派结论或进 `deliverables/` 时，才改 [conclusions](./topics/conclusions.md) 的 `E-xx`。

**三层信息流（ADR 0010）**：`src/` 写给 Agent 的干货（事实/锚点/条件）；`topics/` 写给 Agent + 人的判断（findings/compare/边界）；`deliverables/` 写给人的成品（通俗、按任务、可照着做）。**成品主路径必须自包含**，不要求读者打开 `topics`；细节可以链 `topics`，但要标“可选/出处”。细则见 [ADR 0010](./adr/0010-three-layer-information-flow.md)。

**素材类型不进 topics**：论文的 `card.md` / `digest.md` 在 `src/papers/{arxiv_id}-{slug}/`，网页卡在 `src/web/`，开源项目的 `card.md` / `digest.md` / `code-map.md` 在 `src/open-source/{org}-{repo}/`；用 `source_type` 区分论文/预印本/博客/工程/标准/演讲/综述/开源项目。**topics 引用内容时链 `digest.md`；`card.md` 只用于 provenance/阅读状态。** 证据天花板见 [source-types](./meta/source-types.md)。

## 三条硬规矩

1. **每个主张带证据等级。** 已证 / 已核 / 推测 / 存疑，四选一。没写就是推测。定义见 [conventions](./meta/conventions.md#证据等级)。
2. **区分一手与转述。** 读原文就引 `src/` 下的文件或 arXiv 编号；读综述就在卡片里写「转述自」并标 `待核`。**综述摘要不等于论文结论**——转述常丢限定条件，本仓库已因三处转述失真修正过结论。
3. **反例与正例同权重。** 与结论冲突的证据照样入库，并在 conclusions 里保留冲突条目。

## 素材准入（先过门，再建卡）

任何新材料进 `src/` 前，先按 [CHARTER §4](./CHARTER.md#4-素材准入material-gate) 过五道门；**这是建卡的前置，不是建卡后的评分**。

| 门 | 一分钟问法 | 卡上记什么 |
|---|---|---|
| G1 时效 | 首次公开 ≥ 2026-06-01？开源 `last_push` ≥ 2026-06-01？ | `published` / `last_push` |
| G2 活跃 | 180 天内还有提交/版本/讨论/采用吗？ | `liveness` |
| G3 影响 | 除作者外，至少两个独立信号？至少一个 I1–I3？ | `impact_evidence`（逐条列 I1–I5） |
| G4 来源 | 组织/社区/标准，还是公司自证？公司过 §4.4 了吗？ | `provenance_type` |
| G5 可核验 | URL + 日期 + 机构 + 版本/commit 齐吗？ | `source` / `commit` |

- 五门全过 → `admission: admitted`，建 `card.md` / `digest.md`。
- G1/G5 过、G2/G3 未证 → `admission: signal`，只写进 `frontier.md` 候选队列，**不建目录、不进 topics/deliverables**。
- G1/G4/G5 失败 → `admission: excluded`，不建目录；已入库的移出，并在 `meta/audits/` 登记。
- **没有 `impact_evidence` 的卡不算 admitted；`check_repo` 会查。**
- 标准走 §4.4 的在役例外；公司生产报告走 §4.4 的窄例外，最高只作 `engineering` 证据。

**回溯**：旧材料不豁免。审计窗口（2026-11-11 → 2026-12-11）内只做重判，不再拿旧材料开新判断；窗口结束按 [论文/旧网页审计](./meta/audits/2026-11-11-source-purge.md) 与 [新增材料审计](./meta/audits/2026-11-11-material-gate.md) 的判定执行。

## 写之后

- 跑 `python3 meta/tools/check_repo.py`；失败不提交。
- 新卡先填 `admission` / `gate_checked` / `impact_evidence` / `liveness`；不合格的不要用 `updates:` 洗白。
- 问一句「这次动笔改变了哪条判断」：改了 → 先写本派 `claims.md`；跨派或进交付物才升 [conclusions](./topics/conclusions.md)；没改 → 只补来源。
- 如果修正了旧判断，回改所有引用它的主题页，并在 `card.md` / `digest.md` 的 `updates:` 登记。
- 更新被改文件的 `updated` 与 `status`，并在 [src 台账](./src/README.md) 记一笔。
- 新术语进 [GLOSSARY](./GLOSSARY.md)；改了术语含义，扫一遍引用它的文档。
- 新候选先放 `frontier.md` 的候选队列；只有会改变判断时才建卡，入档时先更新本派 `sources.md`。
- 交稿前过一遍 [checklist](./meta/checklist.md)。
- 改 `deliverables/` 用 [交付物质量评分卡](./meta/deliverable-quality.md) 打分，别临时另起维度；报告落 `deliverables/_plans/`。

## 不要做

- 不为「看起来完整」创建空文件或占位小节。
- 不把综述的一句话扩散到多篇文档——那会把一次误读放大成仓库共识。
- 不在 `deliverables/` 里新增 `topics/` 没有的判断。
- 不把 `frontier.md` 写成第二篇综述——它只放「下一步做什么」，稳定判断回 `README.md`。
- 不为候选建 `card.md` / `digest.md` 而没有「改变哪条判断」的理由。
- 不把博客/工程观察当论文结论；一般性结论默认 `推测`。
- 不为没有 `impact_evidence` 的材料建卡；不把公司自证、会议主 track、star/浏览当影响信号。
- 不用“历史语料/已经引用过/作者是名校”给旧材料续命；质量或影响不达标，立即移出。
- 不把 `signal` 写进 `claims.md` / 派 README / 交付物；它只配待在 `frontier.md` 候选队列。
- 不按来源类型（papers/blogs）建子主题；子主题按子机制。
- 不把派内局部判断直接写进 `conclusions.md`；先写本派 `claims.md`。
- 不把 `runs/` 里的输出直接当 README 结论；先审 run，再升 `claims.md` / README。
- 不用 `card.md` 当消化正文；`digest.md` 必须自包含，下游不需要先读 card。
- 不引入代码目录。验证性实现放仓库外，靠 `EXP-xxx` 编号回链。**唯一例外**是 `meta/tools/` 的只读自检（[ADR 0005](./adr/0005-repo-self-check.md)），不承载研究逻辑。
- 不自行设置要求用户提供资产/人/价/签核的 gate。要设必须先经用户明确同意（[ADR 0007](./adr/0007-no-external-asset-gate.md)）。
