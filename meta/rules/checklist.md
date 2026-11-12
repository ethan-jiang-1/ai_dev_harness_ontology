# 交稿前检查

每次改完跑一遍。任何一条不通过，不要提交。

先跑 `python3 meta/tools/check_repo.py`；它覆盖文件与锚点链接、枚举、E/L 编号、论文/开源清单与计数。下面是脚本查不了的语义项。

## 0. 宪章

- 这次改动是**读/消化/组织/写判断**，还是**建/跑/部署**？后者停；见 [CHARTER](../../CHARTER.md)。
- 没有新增代码、engine、harness、reference filter、可执行套件；示例只作说明。
- 没有把“能跑”当交付标准；没有因为示例不能跑就补实现。
- 例外只有 `meta/tools/` 的只读自检。

## 0.1 素材准入

- 新引源已对 [来源黑名单](./excluded-sources.md) 查过；无命中源的读/引/入库。
- 新卡有 `admission` / `gate_checked` / `impact_evidence` / `liveness` / `provenance_type`；`admitted` 至少两条独立信号，至少一条 I1–I3。
- `signal` 没进 `src/`；`excluded` 没建卡；**历史语料没有“已引用/已消化/名校”豁免**。
- 被删源的引用已改 tombstone；依赖它的 E/L 已撤回、降级或换锚。
- 公司自证、会议主 track、star/浏览不算影响信号；标准走 §4.4 在役例外并写活动证据。

## 1. 链接

- 所有相对链接的文件与 `#锚点` 都存在（`check_repo` 会查）。
- 标签指向正确概念，不只是「能点开」；重点查 `seams.md`、`frontier.md`、`conclusions.md` 的交叉链接。
- 旧结构名（`30-seams`、`src_notes/`、`topics/harness/` 等）不再出现。

## 2. frontmatter

- 文档：`status` ∈ {`seed`, `draft`, `stabilized`, `superseded`}。
- 笔记：`source_type` ∈ {`paper`, `preprint`, `blog`, `engineering`, `standard`, `talk`, `survey`, `open-source`}；`reading` ∈ {`未读`, `综述级`, `摘要级`, `精读`, `已消化`}（代码卡另可用 `已读代码` / `已跑通`）；`provenance` ∈ {`原文正文`, `原文摘要`, `综述转述`, `未核`}（代码卡另可用 `一手代码` / `一手文档`）；`home` 指向 `topics/<派>`，`subtopic` 指向子主题。
- 论文 digest：`quality` ∈ {`A`, `B`, `C`}；`based_on: card.md` 指向同目录的来源卡。
- 开源卡：`commit` 已 pin；`scan_date` / `stars_at_scan` / `last_push` 齐全；`ontology_role` ∈ {`core`, `adjunct`, `none`, `unclear`}；`seam` 取六时刻 + `read-path` / `supply` / `reasoning` / `training` / `none`；`execution_form` ∈ {`engine`, `compiled`, `context`, `label`, `none`, `unknown`}；`evidence_role` ∈ {`execution-test`, `mechanism-only`, `harness-evidence`, `boundary-ruler`}。
- 论文卡：`evidence_role` 与 `execution_form` 齐全；一篇喂多个子主题时，`subtopic` 主归位 + `also_supports` 列出其余。
- 交付：`deliverable_status` ∈ {`draft`, `stable`, `frozen`}。
- `updated` 是最后一次实质修订，不是搬家日期。

## 3. 证据

- 正文引用的 `E-xx / Q-xx / C-xx` 都在 `conclusions.md` 有定义。
- 每个「推测 / 存疑」有未核理由或反例。
- 交付物缺陷走过[修复回路](../../AGENTS.md)：被指的那句话能指到 admitted 源的 digest 节，或已显式标 `推测`/gap 并在 frontier 记「关闭它需要什么」。
- 交付物改动符合该份 `SCOPE.md` 的定性与边界：每句落在它「回答的问题」里，不越界替别的份回答；答不了初心问题已标 gap，**没有偷换成更容易的问题**（合成教程冒充现状之类）。每份交付物必须有 `SCOPE.md`（check_repo 强制）。
- 卡片/消化修正了旧判断 → `updates:` 列全，主题页已回改。
- 派内新判断在 `claims.md`；没有跨派/交付物的理由时，不应改 `conclusions.md`。
- `deliverables/` 引 `E-xx` 作结论；`O-xx` 只作地址（[ADR 0009](../../adr/0009-object-layer.md)），不引 `L-xx`；O 不得替代 E 作主句。

## 4. 计数

**当前计数只看 [meta/state](../status/state.md)**；本节只列结构性不变量，不再抄数字。

- 论文目录数 = manifest 行数；每目录一个 `<stem>.pdf`、`paper.md` / `references.md` / `appendix.md`、`card.md`、`digest.md`。
- 开源：磁盘目录数 = 有 `card.md` 的项目数；有 `digest.md` 的才是「已消化」；没有 digest 的不计入。
- 6 派 / 6 个 `frontier.md` / 6 个 `claims.md` / 6 个 `sources.md` / 6 个硬时刻 + 轴外位置。
- 06 有 5 个子主题（mechanism / failure-attribution / trace / metrics / feasibility）。
- 标题里的「N 种读法」与下面的条目数一致。
- 自检脚本能数的（论文/开源/ID/枚举/链接/锚点），以脚本输出为准。

## 5. 术语

- `证据等级` 只指四档置信度；OA-RAG 的 entailed/... 用 `接地等级`。
- `接缝`（概念）/ `时刻`（六个位置）/ `派`（分类）不混用。
- 新术语进 `GLOSSARY.md`。

## 6. 结构

- `01-04` 问时刻，`05` 问来源，`06` 问尺子。
- 时刻表在 [topics/seams.md](../../topics/seams.md)；派表在 [topics/README.md](../../topics/README.md)；部件表在 [00-harness/README.md](../../topics/00-harness/README.md)。
- 稳定判断在 `README.md`；活页在 `frontier.md`；局部结论在 `claims.md`；证据索引在 `sources.md`；详细论证在 `topics/<派>/<子主题>/README.md`。
- **子主题 README 是 index/dashboard**：一屏以内；发现/证据在 `findings.md` + `findings/`，gap/next 在 `frontier.md`，机制在 `mechanism.md`。
- 改一个派只动该派目录；跨派结论才动 `topics/conclusions.md`。
- 论文一篇一目录：`src/papers/{arxiv_id}-{slug}/`，内含 `<stem>.pdf` / `paper.md` / `references.md` / `appendix.md` / `card.md` / `digest.md` / `figures/`。
- 开源一个项目一目录：`src/open-source/{org}-{repo}/`，内含 `card.md` / `digest.md` / `code-map.md`；**没有 digest 的不算入库**；不 vendor 代码。
- **模板只有一处**：`src/_templates/`（paper / material / open-source 各一套）；源材料子目录不再自带 `_template.md`。
- **card 是来源卡，digest 是消化正文**：card 只放元数据 + 一页索引 + 图表位置 + 作者局限；digest 自包含（术语/方法/数字条件/边界/工程用法），不靠「详见 card」。
- 图在论文目录的 `figures/`；topics 引用时带出处、页码、看什么。
- 博客/工程原文在 `src/web/`，卡与原文同目录 `.card.md`；不放进 `topics/`。
- 子主题有 `prompt.md` 才建 `runs/`；run 带 `prompt` / `model` / `sources` / `claims_changed`。
- run 不直接改 README；结论先过 `claims.md` / README。

## 7. digest 自包含

- 有「三句话 / 问题 / 术语 / 方法 / 数字与条件 / 不能说明什么 / 工程用法 / 质量边界 / 与仓库判断 / 未解决」。
- 每个数字带数据、模型、样本量、设置；没有裸数字；关键数字带表号/页码。
- 不靠「详见 card」补上下文；链接只放原文/代码。
- 长度：L3 250–360 行；L2 160–260；L1 100–240（目标，不是门；自包含优先）。
- 过 [digest 模板](../../src/_templates/paper-digest.md) 的自包含要求；长度目标见 [conventions](./conventions.md#阅读深度l1l2l3)。
