# AGENTS.md

本仓库是**持续生长的研究档案**：材料进来 → 精读成卡 → 沉淀成主题 → 抽成交付物。交付物是文档，不是代码。

任何改动都该让某条判断更清楚、更有证据，或更可证伪。

## 入口

- 流水线全景与目录推导：[README](./README.md)
- 研究问题与假设：[THESIS](./THESIS.md)
- 术语（动笔前先对齐用词）：[GLOSSARY](./GLOSSARY.md)
- 按需加载（渐进披露）：[meta/loading](./meta/loading.md)

## 先定位工位

| 你在做什么 | 落点 |
|---|---|
| 存原文 | `src/papers/{arxiv_id}-{slug}/`（论文，一篇一目录）或 `src/web/`（网页）；论文在 [manifest](./src/papers/manifest.md) 登记 |
| 读一篇论文 | 先读同目录 `digest.md`（自包含，下游唯一入口）；要核引文再看 `paper.md` / `references.md` / `appendix.md` |
| 记一篇论文的来源 | 同目录 `card.md`（来源卡：元数据 + 一页索引 + 图表位置）；用 [论文卡模板](./src/_templates/paper-card.md) |
| 消化一篇论文 | 同目录 `digest.md`（自包含长文：术语/方法/数字条件/边界/工程用法）；用 [digest 模板](./src/_templates/paper-digest.md) |
| 存博客/工程材料 | `src/web/`；卡同目录 `<stem>.card.md`，用 [材料卡模板](./src/_templates/material-card.md) |
| 综合几个来源、形成判断 | `topics/`，用 [机制笔记模板](./meta/note-template.md) |
| 写子机制的详细论证 | `topics/<派>/<子主题>/README.md`；派 README 只留地图 |
| 记本派结论 | `topics/<派>/claims.md`（`L-xx`）；跨派才升 conclusions |
| 列本派证据 | `topics/<派>/sources.md` |
| 跑一个子主题 | `topics/<派>/<子主题>/prompt.md`；输出放 `runs/` |
| 修订跨主题结论 | [topics/conclusions.md](./topics/conclusions.md) |
| 查时刻/接缝 | [topics/seams.md](./topics/seams.md) |
| 找某派前沿/候选 | `topics/<派>/frontier.md`，方法见 [topic 协议](./meta/topic-research-protocol.md) |
| 做成对外物 | `deliverables/`，只从 `topics/` 抽取 |
| 设计验证 | `experiments/`，用 [实验模板](./experiments/_template.md) |

`topics/` 内按**本体凭什么起作用**分六派：`01-constraint`（拦动作）、`02-judgment`（验产出）、`03-knowledge`（喂上下文）、`04-state`（跨轮记忆）、`05-produce`（造与修）、`06-measure`（量它有没有用），底座是 `00-harness`（控制回路七部件）。

六派是 **4+1+1**：`01-04` 是回路内的四个介入点，`05` 是回路前（来源），`06` 是回路外（尺子）。归派一句话：**01-04 问时刻，05 问来源，06 问尺子；跨派按主效应归派并标双重身份。** 时刻轴见 [seams](./topics/seams.md)。

卡片与主题页的字段：`status`（文档成熟度）/ `source_type`（素材类型）/ `reading`（读到哪）/ `provenance`（一手/转述），定义见 [conventions](./meta/conventions.md#字段与词汇)。

**派内可以再有子主题**：`topics/<派>/<子主题>/README.md`。派 README 只做地图与硬证据；详细机制在子主题。子主题按子机制命名，不按来源类型；成立条件见 [ADR 0003](./adr/0003-subtopics-and-source-types.md)。

**改一个派只动该派目录**：`README.md` / `claims.md` / `sources.md` / `frontier.md` / 子主题。只有跨派结论或进 `deliverables/` 时，才改 [conclusions](./topics/conclusions.md) 的 `E-xx`。

**素材类型不进 topics**：论文的 `card.md` / `digest.md` 在 `src/papers/{arxiv_id}-{slug}/`，网页卡在 `src/web/`；用 `source_type` 区分论文/预印本与博客/工程/标准/演讲/综述。**topics 引用内容时链 `digest.md`；`card.md` 只用于 provenance/阅读状态。** 证据天花板见 [source-types](./meta/source-types.md)。

## 三条硬规矩

1. **每个主张带证据等级。** 已证 / 已核 / 推测 / 存疑，四选一。没写就是推测。定义见 [conventions](./meta/conventions.md#证据等级)。
2. **区分一手与转述。** 读原文就引 `src/` 下的文件或 arXiv 编号；读综述就在卡片里写「转述自」并标 `待核`。**综述摘要不等于论文结论**——转述常丢限定条件，本仓库已因三处转述失真修正过结论。
3. **反例与正例同权重。** 与结论冲突的证据照样入库，并在 conclusions 里保留冲突条目。

## 写之后

- 问一句「这次动笔改变了哪条判断」：改了 → 先写本派 `claims.md`；跨派或进交付物才升 [conclusions](./topics/conclusions.md)；没改 → 只补来源。
- 如果修正了旧判断，回改所有引用它的主题页，并在 `card.md` / `digest.md` 的 `updates:` 登记。
- 更新被改文件的 `updated` 与 `status`，并在 [src 台账](./src/README.md) 记一笔。
- 新术语进 [GLOSSARY](./GLOSSARY.md)；改了术语含义，扫一遍引用它的文档。
- 新候选先放 `frontier.md` 的候选队列；只有会改变判断时才建卡，入档时先更新本派 `sources.md`。
- 交稿前过一遍 [checklist](./meta/checklist.md)。

## 不要做

- 不为「看起来完整」创建空文件或占位小节。
- 不把综述的一句话扩散到多篇文档——那会把一次误读放大成仓库共识。
- 不在 `deliverables/` 里新增 `topics/` 没有的判断。
- 不把 `frontier.md` 写成第二篇综述——它只放「下一步做什么」，稳定判断回 `README.md`。
- 不为候选建 `card.md` / `digest.md` 而没有「改变哪条判断」的理由。
- 不把博客/工程观察当论文结论；一般性结论默认 `推测`。
- 不按来源类型（papers/blogs）建子主题；子主题按子机制。
- 不把派内局部判断直接写进 `conclusions.md`；先写本派 `claims.md`。
- 不把 `runs/` 里的输出直接当 README 结论；先审 run，再升 `claims.md` / README。
- 不用 `card.md` 当消化正文；`digest.md` 必须自包含，下游不需要先读 card。
- 不引入代码目录。验证性实现放仓库外，靠 `EXP-xxx` 编号回链。
