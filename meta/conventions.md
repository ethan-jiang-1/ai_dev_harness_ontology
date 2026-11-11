---
updated: 2026-11-11
---

# 写作约定

## 证据等级

四个等级，**升不上去就不许写**：

| 等级 | 含义 | 出处要求 |
|---|---|---|
| **已证** | 独立复现（本仓库不设实验目录） | 需仓库外复现记录 + `EXP-xxx` 指针 |
| **已核** | 读过一手原文（至少摘要），引文准确 | 需卡片或原文链接 |
| **推测** | 有线索、未核原文，或来自二手转述 | 标注来源，写清为何未核 |
| **存疑** | 有反例，或证据互相矛盾 | 必须写出反例 |

**默认是推测。** 没标等级的论断，一律按推测看待。

> 不要与「接地等级」混淆：接地等级是 OA-RAG 那套 entailed / supported / related / unrelated，描述输出与本体的关系；证据等级是本仓库对主张的置信度。见 [GLOSSARY](../GLOSSARY.md#证据)。

## 引用

| 情况 | 写法 |
|---|---|
| 一手 | 链接到 `src/` 下的原文件，或 arXiv 编号 |
| 二手转述 | 写「转述自 X」，并加 `待核` |
| 未读原文 | 不许写成事实；写成「某文报告」 |

**综述的一句摘要不是论文结论。** 本仓库已经因此踩过一次坑：三篇论文的转述丢了限定条件，见 [综述卡](audits/2026-11-11-source-purge.md#src-web-weixin-laoliu)。

## 字段与词汇

同一个字段在不同目录不能有不同含义。本仓库用以下字段，各自一套词汇：

| 字段 | 用在哪 | 取值 | 含义 |
|---|---|---|---|
| `status` | 所有文档 | `seed` / `draft` / `stabilized` / `superseded` | 文档成熟度，不代表篇幅 |
| `home` / `subtopic` / `also_supports` | 源卡 / digest | `topics/<派>` / `<子主题>` / `[<子主题>]` | 归位；移动子主题只改 `subtopic`；一篇论文喂多个子主题时，主归位放 `subtopic`，其余放 `also_supports` |
| `evidence_role` | 源卡 | `execution-test` / `mechanism-only` / `harness-evidence` / `boundary-ruler` / `unclear` | 对中心问题提供哪类证据：真的测了本体被执行 / 只提机制 / 提供 harness 证据 / 只做边界与尺子 |
| `execution_form` | 源卡 | `engine` / `compiled` / `context` / `label` / `none` / `unknown` | 本体以什么形态被执行：引擎求值 / 编译成约束 / 作为上下文注入 / 只当标签 / 未执行 / 未判 |
| `source_type` | `src/` 卡片 | `paper` / `preprint` / `blog` / `engineering` / `standard` / `talk` / `survey` / `open-source` | 素材类型；证据天花板见 [source-types](./source-types.md) |
| `standing` | `src/` 标准卡 | `normative` / `informative` | 源位阶：规范性（可定义术语、定合格性）/ 资料性（只能举例、佐证）；`signal` 不是 standing，归 `admission` |
| `reading` | 源卡 `card.md` | 论文/材料：`未读` / `综述级` / `摘要级` / `精读` / `已消化`；代码：`未读` / `已读代码` / `已跑通` | 读到什么程度；**不是证据等级** |
| `provenance` | 源卡 `card.md` | 论文/材料：`原文正文` / `原文摘要` / `综述转述` / `未核`；代码：`一手代码` / `一手文档` / `未核` | 证据来自哪里 |
| `quality` | `digest.md` | `A` / `B` / `C` | 证据强度粗分：A 多基准/真实部署/消融（代码：有测试且有生产/基准）；B 单基准/单域/有限评估（代码：有测试但单路径）；C 概念/模拟/小样本/无量化（代码：只读代码/无测试） |
| `deliverable_status` | `deliverables/` | `draft` / `stable` / `frozen` | 交付阶段 |
| `admission` | `src/` 卡 | `admitted` / `admitted (probation)` / `signal` / `excluded` | 五门结论；没有就是未判；见 [CHARTER §4](../CHARTER.md#4-素材准入material-gate) |
| `gate_checked` | `src/` 卡 | `YYYY-MM-DD` | 最后一次过门日期 |
| `impact_evidence` | `src/` 卡 | `I1: ...; I3: ...` | 逐条列独立信号；`admitted` 必填 |
| `liveness` | `src/` 卡 | 文本 | 最近一次活动及日期 |
| `provenance_type` | `src/` 卡 | `standard-body` / `academic` / `foundation` / `community` / `company` / `individual` | 来源结构，决定 G4 |

**源位阶与术语（ADR 0011）**：

- `normative` 可定义术语、定合格性；`informative` 只能举例、佐证。**术语定义只能引 `normative`。**
- 自造词标 `local`，给出定义与边界，不得写成「业界 / 标准」；交付物首现处解释。
- 标准卡不撑效应量：标准能定「什么叫顶层本体」，不能证明「本体提升 agent 效果」。
- 术语差异判定：`aligned` / `narrower` / `broader` / `divergent` / `local`；`divergent` 与冒充行业词的 `local` 合计超过 1/3 即停，重定基调。执行见 [基线整改计划](../deliverables/_plans/2026-11-11-baseline-correction-plan.md)。

开源卡另有两组字段，只在 `src/open-source/` 使用：

| 字段 | 取值 | 含义 |
|---|---|---|
| `commit` / `release` / `license` | SHA 或 tag / tag / SPDX | 版本与许可；不 pin commit 不算入库 |
| `scan_date` / `stars_at_scan` / `last_push` | 日期 / 数字 / 日期 | 扫描快照；star 只作影响力参考 |
| `ontology_role` / `seam` / `execution_form` | `core/adjunct/none/unclear` / 六时刻 + `read-path/supply/reasoning/training/none` / `engine/compiled/context/label/none/unknown` | 本体地位、接缝/轴外位置、执行形态；只写初判，定级在 digest。旧的 `execution` 字段已由 `execution_form` 取代 |

`status` 的判据：

- `seed` — 结构在，内容已开始，但未交叉核对。
- `draft` — 论证完整，至少经过一次交叉核对；结论可能变。
- `stabilized` — 结论稳定，可被交付物引用；**需要独立复现或外部签核**。当前没有文档达到，是事实，不是遗漏。
- `superseded` — 已被别的文档取代，保留指针。

`updated` 表示「最后一次实质修订」；搬家、改链接、批量重排不算。不要为了显得新而改日期。

**文档状态与笔记进度是两件事。** 一张 `reading: 摘要级` 的卡，其 `status` 通常是 `draft`；不要写 `status: 摘要级`。

正文里的推断句，至少在段末标一次 `已核` / `推测` / `存疑`；引文来源用 `一手摘要` / `一手正文` / `转述`，并按下面的映射读：

| 正文写法 | 对应等级 |
|---|---|
| 一手正文 / 一手摘要 | 已核 |
| 转述 / 待核 | 推测 |
| 反例 / 冲突 | 存疑 |

## 阅读深度（L1/L2/L3）

| 档 | 读到哪 | digest 目标长度 | 用途 |
|---|---|---|---|
| L1 | 摘要 + 结论 + 局限 | 100–240 行 | 一页判断；只作边界/候选证据 |
| L2 | 正文主要节 + 关键表 | 160–260 行 | 标准消化；可进子主题 F |
| L3 | 正文 + 关键表/图 + 附录按需 | 250–360 行 | 深消化；可支撑 E/L 的核心证据 |

长度是目标，不是门：**自包含优先**。L1 的“一页判断”指结论页，不要求整个 digest 只有一页。L1/L2/L3 是阅读深度，不是证据等级，也不是文档 `status`。

## 命名

- 目录：小写短横线；论文目录用 `src/papers/{arxiv_id}-{slug}/`；开源项目目录用 `src/open-source/{org}-{repo}/`（全小写，`/` 换成 `-`，如 `RDFLib/pySHACL` → `rdflib-pyshacl`）
- 论文文件：`<stem>.pdf`（原文，只读）/ `paper.md`（正文 MD）/ `references.md`（参考文献）/ `appendix.md`（附录）/ `card.md`（分解）/ `digest.md`（消化）/ `figures/`（原图）
- 开源文件：`card.md`（来源卡）/ `digest.md`（代码阅读，下游入口）/ `code-map.md`（文件/符号索引，可选）
- 模板统一放 `src/_templates/`：论文、材料、开源各自一套；**源材料子目录不再自带模板**
- 网页卡：`src/web/{来源}/<slug>.card.md`，与原文同名
- 子主题目录：`topics/<派>/<子主题>/README.md`；按子机制命名，不按来源类型。派 README 只做地图，详细论证在子主题
- 结论编号：`E-xx`（结论）/ `Q-xx`（存疑）/ `C-xx`（冲突）
- 仓库外验证编号：`EXP-xxx`（仅指针，不建仓内实验目录）

## 台账纪律

每次动笔后回答三句：

1. 这份材料/这篇文档**改变了哪条判断**？→ 先写本派 `claims.md`；跨派/进交付物才升 [conclusions](../topics/conclusions.md)
2. **喂给了哪个主题**？→ 去改 [src 台账](../src/README.md)
3. 如果修正了旧判断，**哪些主题页要回改**？→ 写进卡片的 `updates:`，逐页改。

三句都答不上来，说明这次动笔没有产生信息。

## 交付物

见 [deliverables/README](../deliverables/README.md)。一句话：**只抽不增。**
