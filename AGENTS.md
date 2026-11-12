# AGENTS.md

> **宪章（最高约束）**：[CHARTER](./CHARTER.md)。本仓库是研究档案：只做消化、组织、研究，不做实施；交付物是文档，不是代码。与任何文档冲突时宪章为准；修改宪章需用户明确同意。

本仓库是**持续生长的研究档案**。主干信息流（[ADR 0010](./adr/0010-three-layer-information-flow.md)）：

```
src/（给 Agent 的干货）──digest──▶ topics/（给 Agent+人的判断）──抽取──▶ deliverables/（给人的成品）
```

- `src/`：一篇论文/一个项目一目录；**`digest.md` 是自包含的下游唯一入口**，`card.md` 只作 provenance。
- `topics/`：六派沉淀判断；派内 `L-xx` 升跨派 `E-xx`；素材类型不进 topics。
- `deliverables/`：**只抽不增**，主路径自包含，读者不打开 topics 能完成任务。改/建每份前先读它的 `SCOPE.md`（初心/定性/边界/红线/发挥空间）；共用规矩见 [交付物定位](./meta/deliverables/scope.md)；**答不了初心问题就标 gap，不偷换成更容易的问题**。
- **判断顺流而下，证据逆流而上**：交付物被指错时，先走上游补证，再回写下游——走下面的修复回路。

任何改动都该让某条判断更清楚、更有证据，或更可证伪。

## Fresh agent：动手前先清楚三件事

1. **目标**：产出可信判断（不是软件）。你这次奔哪份交付物/哪个派，就先读它的 `SCOPE.md` / 派 README——目标、该干什么、边界、发挥空间都在那。
2. **质量门**：素材必须过 [CHARTER §4](./CHARTER.md#4-素材准入material-gate)——**≥2026-06-01、活跃、多主体高影响**；在役标准须「现行版本 + 2026-06 后维护活动」；采/引前查 [黑名单](./meta/rules/excluded-sources.md)。孤证/过期/厂商自证/二手综述不进（purge 的血泪教训）。
3. **边界**：宪章硬约束（不写代码/不实施）+ 该份 SCOPE 红线。答不了标 gap，不偷换问题。

## 入口

- 研究问题与假设：[THESIS](./THESIS.md) · 术语（动笔前对齐）：[GLOSSARY](./GLOSSARY.md)
- 加载集与阅读路径：[meta/loading](./meta/rules/loading.md) · 当前计数与阻塞：[meta/state](./meta/status/state.md)（计数唯一权威）
- meta 怎么用：[meta/AGENTS](./meta/AGENTS.md)（30 秒入口）· 文件索引：[meta/README](./meta/README.md) · 结构决策：[adr/README](./adr/README.md)
- 本地噪音：`.tmp-venv/`、`.pi/` 不是仓库内容；搜索/统计时排除

## 任务路由（唯一表）

| 你在做什么 | 落点 | 加载 |
|---|---|---|
| **交付物被指错/有缺口** | **修复回路（下节）** | 被指页 + 对应 E 行 + digest |
| 论文入库/精读/消化 | `src/papers/{arxiv_id}-{slug}/`；在 [manifest](./src/papers/manifest.md) 登记 | [src/README §5](./src/README.md) + [论文卡](./src/_templates/paper-card.md)/[digest 模板](./src/_templates/paper-digest.md) |
| 网页/标准/博客入库 | `src/web/{来源}/`；卡为同目录 `<stem>.card.md` | [src/README](./src/README.md) + [材料卡模板](./src/_templates/material-card.md) |
| 开源项目入库/读码 | `src/open-source/{org}-{repo}/`；pin commit，不 vendor | [选择标准](./src/open-source/README.md) + [开源卡](./src/_templates/open-source-card.md)/[digest 模板](./src/_templates/open-source-digest.md) |
| 综合来源、形成判断 | `topics/<派>/`；[机制笔记模板](./meta/templates/note-template.md) | 该派 README + claims + sources + frontier |
| 写子机制详细论证 | `topics/<派>/<子主题>/README.md`；按子机制命名，不按来源类型 | [ADR 0003](./adr/0003-subtopics-and-source-types.md) |
| 记本派判断/证据 | 该派 `claims.md`（`L-xx`）/ `sources.md`；改一个派只动该派目录 | [conventions](./meta/rules/conventions.md) |
| 跑一个子主题 | 子主题 `prompt.md`；输出放 `runs/`，先审 run 再升 claims | [topic 协议 §9](./meta/rules/topic-research-protocol.md) |
| 修订跨派结论 | [topics/conclusions.md](./topics/conclusions.md)（`E-xx`，唯一 E 表） | 对应派 claims + digest |
| 查时刻/形态/对象/承重数 | [seams](./topics/seams.md) / [execution-forms](./topics/execution-forms.md) / [objects](./topics/objects.md) / [evidence-anchors](./topics/evidence-anchors.md) | — |
| 找某派前沿/候选 | 该派 `frontier.md`；候选只放这里，建卡须有「改变哪条判断」的理由 | [topic 协议](./meta/rules/topic-research-protocol.md) |
| 做成对外物 | `deliverables/`；只从 topics 抽取，**先读该份 SCOPE.md** | 该份 `SCOPE.md` + [定位总索引](./meta/deliverables/scope.md) + [deliverables/README](./deliverables/README.md) + [质量评分卡](./meta/deliverables/quality.md) |

六派按**本体凭什么起作用**分：`01-constraint` 拦动作、`02-judgment` 验产出、`03-knowledge` 喂上下文、`04-state` 跨轮记忆、`05-produce` 造与修、`06-measure` 量有没有用；底座 `00-harness`（控制回路七部件）。**4+1+1**：01-04 问时刻，05 问来源，06 问尺子；跨派按主效应归派并标双重身份。地图与归派三问见 [topics/README](./topics/README.md)。

## 修复回路（交付物被指错时的常设路径）

用户指出交付物里某句话/数字/判断不对或缺失时，按顺序走；**修复先走上游，不在交付物里直接补判断**：

1. **定位**：在被指页找到承重句与它背后的 `E-xx`。没有 E → 它是新判断，从第 3 步开始。
2. **核证**：读 E 行链的 `digest.md` §4/§5。digest 足够 → 错在抽取或表述，跳第 5 步。
3. **补证**：digest 不足或源不合格 → 先查 [来源黑名单](./meta/rules/excluded-sources.md)（命中即弃），再按 [CHARTER §4](./CHARTER.md#4-素材准入material-gate) 找权威材料（研究论文与工程落地并重；标准只定词，不证效果）。过五门 → 建 card/digest；不过 → 记入该派 `frontier.md` 候选队列。
4. **升判断**：先写该派 `claims.md`（L）；跨派或进交付物才升 `conclusions.md`（E）。修正旧判断的，回改所有引用页，并在 card/digest 的 `updates:` 登记。
5. **回写**：按新的 E/digest 重写交付物段落，对照该份 `SCOPE.md` 不越界；主路径保持自包含，细节链 topics 标「可选/出处」。
6. **收口**：跑 `python3 meta/tools/check_repo.py`，过 [checklist](./meta/rules/checklist.md)，更新 [state](./meta/status/state.md)。

**完成判据**：被指的那句话能指到 `admitted` 源的 digest 节，且数字/条件与原文一致；指不到，就在页面显式标 `推测` 或 gap，并在 frontier 写明「关闭它需要什么」。两者都做不到，修复未完成。

## 三条硬规矩

1. **每个主张带证据等级**：已证 / 已核 / 推测 / 存疑，没写就是推测。定义见 [conventions](./meta/rules/conventions.md#证据等级)。
2. **区分一手与转述**：引 `src/` 文件或 arXiv 编号；转述写「转述自 X」+ `待核`，且只进一处，不扩散到多篇文档。综述摘要不等于论文结论——转述常丢限定条件。
3. **反例与正例同权重**：与结论冲突的证据照样入库，conclusions 保留冲突条目。

## 素材准入（先过门，再建卡）

新材料进 `src/` 前，先过 [CHARTER §4](./CHARTER.md#4-素材准入material-gate) 的五道门 G1–G5——**判据以宪章为唯一出处，本页不复述**。这是建卡的前置，不是建卡后的评分。**采/引任何源之前先查 [来源黑名单](./meta/rules/excluded-sources.md)：命中的源一律不读、不引、不入库**（防调研时复见已剔除源、把判断带偏）。结果写在卡上：

- 五门全过 → `admission: admitted`，建 card + digest；卡必填 `admission` / `gate_checked` / `impact_evidence` / `liveness` / `provenance_type`（字段定义见 [conventions](./meta/rules/conventions.md#字段与词汇)）。
- G1/G5 过、G2/G3 未证 → `signal`，只进 `frontier.md` 候选队列，不建目录、不进 topics/deliverables。
- G1/G4/G5 失败 → `excluded`，不建目录；已入库的移出并在 `meta/audits/` 登记。旧材料不豁免。
- 只有 `admitted`（含 probation）能撑 E/L/交付物；在役标准与公司生产报告走宪章 §4.4 窄例外。证据天花板见 [source-types](./meta/rules/source-types.md)。

## 写之后

- 跑 `python3 meta/tools/check_repo.py`；失败不提交。交稿前过 [checklist](./meta/rules/checklist.md)。
- 问「这次动笔改变了哪条判断」：改了 → 先写本派 `claims.md`，跨派/进交付物才升 E；没改 → 只补来源。
- 更新被改文件的 `updated` 与 `status`，在 [src 台账](./src/README.md) 记一笔；新术语进 [GLOSSARY](./GLOSSARY.md)，改术语含义要扫引用。
- 改 `deliverables/` 用 [质量评分卡](./meta/deliverables/quality.md) 打分，报告落 `deliverables/_plans/`。
- `_plans/` 是工作底稿：现行计划至多一份，其余是日志/参考；不构成判断，不进对外阅读路径，不新增规则。

## 护栏（看到就停）

- 写代码/引擎/demo/CI → 停。唯一例外是 `meta/tools/` 只读自检（[ADR 0005](./adr/0005-repo-self-check.md)）；验证放仓库外，`EXP-xxx` 回链，需用户同意。
- 为「看起来完整」建空文件/占位小节 → 停。
- 给用户提供资产/人/价/签核的 gate → 停，除非用户明确同意（[ADR 0007](./adr/0007-no-external-asset-gate.md)）。
