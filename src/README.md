---
updated: 2026-11-09
---

# src：来源层（三类材料，各自一目录）

流水线的第一个工位。三类源材料，落点不同、契约相同：

| 类 | 落点 | 目录粒度 | 原文形态 |
|---|---|---|---|
| 论文 | `papers/` | 一篇一目录 `{arxiv_id}-{slug}/` | PDF + `paper.md` |
| 网页/博客/非 arXiv 论文 | `web/` | 一源一目录 `{来源}/` | 原文 MD；论文另存 PDF |
| 真实代码项目 | `open-source/` | 一个项目一目录 `{org}-{repo}/` | 不 vendor，pin commit + 链接 |

三类都解决三件事：**原文/代码在不在、它说了什么或怎么走、我们消化出了什么**。

> 非 arXiv 的会议论文/数据集（Zenodo、DLR 等）也落 `web/`，`source_type: paper`；材料卡即消化正文，不另建 digest（见 [web/README](./web/README.md)）。

```
src/
├── papers/
│   ├── manifest.md          # 全仓唯一论文登记（28 篇，含批次列）
│   └── {arxiv_id}-{slug}/
│       ├── {arxiv_id}-{slug}.pdf     # 原文，只读
│       ├── paper.md                  # 正文全文 MD（保留页码标记）
│       ├── references.md             # 参考文献（默认不读）
│       ├── appendix.md               # 附录/补充材料（默认不读）
│       ├── card.md                   # 来源卡：元数据 + 论文说了什么（短）
│       ├── digest.md                 # 消化正文：自包含，下游唯一入口
│       └── figures/                  # 论文原图（有图才建）
├── web/                              # 网页/博客原文 + 同名 .card.md
├── open-source/
│   └── {org}-{repo}/
│       ├── card.md                   # 来源卡：repo/commit/license/本体在哪/调用点（短）
│       ├── digest.md                 # 代码阅读正文：自包含，下游唯一入口
│       └── code-map.md               # 可选：文件/符号/调用链索引
├── _templates/                       # 三类源材料的模板都在这里，子目录不再自带模板
└── README.md
```

## 0. 两个角色 + 一份原文，一句话

| 文件 | 角色 | 谁读 |
|---|---|---|
| 原文（PDF / 网页 MD / 代码） | **完整、未消化** | 核引文、查细节、追调用链时 |
| `card.md` | **来源卡**：这是什么、读到哪、原文/图/代码在哪 | 需要 provenance 时 |
| `digest.md` | **消化正文**：自包含的判断与细节 | **topics / 下游默认只读这个** |

三种原文形态对应三种卡与 digest 模板，但角色关系不变：

| 类 | 原文 | 来源卡模板 | 消化模板 | 额外 |
|---|---|---|---|---|
| 论文 | `paper.md` / PDF | [paper-card](./_templates/paper-card.md) | [paper-digest](./_templates/paper-digest.md) | `figures/` |
| 网页 | 原文 MD | [material-card](./_templates/material-card.md) | 同卡（材料卡含判断） | — |
| 代码 | commit + 链接 | [open-source-card](./_templates/open-source-card.md) | [open-source-digest](./_templates/open-source-digest.md) | `code-map.md` |

**信息流**（论文为例，另两类同构）：

```
原文（PDF/代码/网页）
     │
     ├──▶ card.md（来源卡：元数据 + 一页索引）
     │
     └──▶ digest.md（自包含消化）──▶ topics/sources.md ──▶ claims / 子主题
```

`card.md` 与 `digest.md` 都从原文来，但**不是上下游关系**：card 是来源登记，digest 是消化正文。下游不需要先读 card；**没有 digest 的源材料，不算进过流水线**。

**反向加载（从交付物倒查）**：不要从 `papers/manifest.md` 顺读。走 `conclusions` 的 E 行 → 该 E 链的 `digest.md` §4/§5 → 只有 digest 不够时才回 `paper.md` 的指定表/节。`card.md` 只在需要 provenance 时读；`references.md` / `appendix.md` 默认不读。三条交付物的具体反向链见 [meta/loading](../meta/loading.md#从交付物倒查反向加载)。

**反向阅读锚点（digest 契约）**：§4「结果：数字与条件」、§5「这些数字不能说明什么」、§6「工程上怎么用」、§8「与仓库判断的关系」——这四节编号固定，不重排；新增内容放 §9/§10。反向读不到 §4/§5 时，才回 `paper.md` 的指定表/节。

## 0.1 来源新鲜度（2026-11-09 起，硬规则）

- **论文**：新入档论文的**首次提交/发表**必须 **≥ 2026-07-01**。2025 年及更早的材料不再新入档；已有 24 篇是历史语料，不回填，也不据此新开判断。
- **开源项目**：新入档项目的 `last_push` 必须 **≥ 2026-07-01**（2026 年 6 月之后仍活跃）。只有 star/README、没有近期提交的不算。
- **登记**：新论文卡带 `batch: 补给` + `published: YYYY-MM-DD`；新开源卡带 `last_push`；`check_repo` 机械校验（论文只查 `补给` 批，避免误伤历史卡）。
- **理由**：在快速变化的 ontology/agent 工程里，2025 的材料经常把过时假设带进来；宁可少一条，不拿旧结论撑新判断。

## 0.2 来源可靠性 / 影响力（2026-11-09 起，硬规则）

- **scope**：新来源 origin 只收 **US / China / Germany / Singapore**；其他地区不新入档（已有历史语料不回填）。scope 内再按 `venue` / 生产 / benchmark 采用 / 强组 track record 看 reliability / impact。
- **论文**：卡上写 `region`（机构/国家）、`venue`、`reliability`（high/medium/low）、`impact`（high/medium/low），并给一句依据。preprint 不能默认 high。
- **降级**：preprint-only + 无采用 + 无强组 = signal，不单独撑 E；`reliability: low` 不入核心。
- **开源**：`stars` / contributors / commits / 生产采用 + `last_push ≥ 2026-07-01`；低星/单作者/停更只作候选。
- **理由**：来源本身不可靠，数字越漂亮越误导。

## 1. 论文的规则（`papers/`）

网页的规则见 [web/README](./web/README.md)；开源项目的规则见 §1.1。三类共用的是 §0 的角色关系与 §4 的字段纪律。

1. **原文只读。** `*.pdf` / 网页原文不改写、不摘编；修改只发生在 `card.md` / `digest.md`。
2. **一篇一目录。** 目录用 `{arxiv_id}-{slug}`；PDF 保留原名；来源卡固定 `card.md`，消化固定 `digest.md`。
3. **先转 MD，再建卡。** PDF 完整转 `paper.md`，把 `references.md` / `appendix.md` 单独切出；正文保留 `<!-- page N -->`。转换优先用 `pymupdf4llm`；不可用时用 `pdftotext -layout` 并在 `paper.md` frontmatter 记 `converter: pdftotext-layout`。公式/表格可能有版式噪声，引用前回 PDF 核。
4. **card 短，digest 长。** `card.md` 不承载机制细节与判断；`digest.md` 承载全部下游需要的信息。**不要用「详见 card」代替内容**。
5. **digest 自包含。** 不假设读者读过论文或 card：定义术语、解释方法、数字带条件、说明不能证明什么、给出工程用法。链接只放原文/代码，放在最后。
6. **topics 引 digest，不引 card 作为内容。** `sources.md` 可同时给 card（provenance）与 digest（内容），但内容判断只从 digest 来。
7. **图随论文。** 原图放 `figures/`；文件名 `fig-{n}-{slug}.png`；图注写「看什么」、页码、版权。
8. **登记。** 论文在 [`papers/manifest.md`](./papers/manifest.md) 登记；`_download.log` 保留下载结果；网页规则见 [`web/README.md`](./web/README.md)；开源项目规则见 [`open-source/README.md`](./open-source/README.md)。

## 1.1 开源项目的规则（`open-source/`）

`src/open-source/` 放 GitHub/GitLab 上可读代码的项目，不是论文、不是博客。**一个项目一个目录**：

```
open-source/{org}-{repo}/
├── card.md        # 来源卡：repo/commit/license/本体在哪/调用点/证据入口（短）
├── digest.md      # 代码阅读正文：自包含，下游唯一入口
└── code-map.md    # 可选：文件/符号/调用链索引，只做定位
```

规则：

- **不 vendor 代码**：只写 commit/tag + 链接 + 文件路径，不把整仓搬进仓库。
- **pin 版本**：必须写 commit SHA 或 release tag；stars 只作影响力参考，不是质量证明。
- **digest 是下游唯一入口**：topics 引开源证据时链 `digest.md`；`card.md` 只作 provenance，`code-map.md` 只做索引。
- **执行 vs 装饰**要在 digest 里定级：真的跑 SHACL/OWL/约束检查，还是只把本体塞进 prompt；只有 README 说法的标 `推测`。
- **命名**：目录全小写，`{org}-{repo}`，`/` 换成 `-`（如 `RDFLib/pySHACL` → `rdflib-pyshacl`）。
- **候选与入库分开**：候选池、选择标准在 [open-source/README](./open-source/README.md)；入选项目才建目录。消化顺序与 C/A 闸见 [开源消化计划](../meta/open-source-digestion-plan.md)。
- 模板：[open-source-card](./_templates/open-source-card.md) / [open-source-digest](./_templates/open-source-digest.md) / [open-source-code-map](./_templates/open-source-code-map.md)。

## 2. `card.md` 的定位：来源卡，不是消化（以论文为例）

`card.md` 只回答「这是什么、我从哪读的、原文/图/代码在哪」。建议 40–70 行；材料卡与开源卡是同一角色，字段不同（见 `_templates/` 对应模板）。

| 内容 | 要求 |
|---|---|
| frontmatter | `status` / `source_type` / `reading` / `provenance` / `arxiv` / `title` / `authors` / `pdf` / `home` / `subtopic` / `updates` |
| 一句话 | 论文自己的主张，不是我们的判断 |
| 问题与设定 | 任务/数据/模型/基线，3–5 行 |
| 机制/数字索引 | 只列「有哪些节/表/图」，不展开；详细数字进 digest |
| 图表索引 | 图/表编号、页码、是否已提取 |
| 作者自述局限 | 作者承认的边界 |
| 原文 | PDF/arXiv/代码链接 |

**不要放**：长机制复述、完整证据表、我们的工程建议、与其它论文的比较。这些都在 `digest.md`。

## 3. `digest.md` 的定位：下游唯一入口

`digest.md` 是**自包含消化正文**。读者可能只读这一篇，不读 card/原文；所以它必须能独立成立。以下骨架以论文为例；开源 digest 用 [open-source-digest](./_templates/open-source-digest.md)，要求相同（自包含、不靠「详见 card」）。

固定骨架：

1. `## 0. 三句话`：问什么、怎么做、发现什么。
2. `## 1. 它解决什么问题`：用大白话讲背景与为什么值得测。
3. `## 2. 术语`：读数字前必须懂的词。
4. `## 3. 它怎么做`：数据/模型/方法/指标 + 一个具体例子。
5. `## 4. 结果：数字与条件`：每个数字带数据、模型、样本量、设置、比较对象。
6. `## 5. 这些数字不能说明什么`：外推边界、指标混淆、作者限定、读者推断。
7. `## 6. 工程上怎么用`：复刻第一步、关键参数/成本、何时用/别用。
8. `## 7. 质量与边界`：证据类型、强项、威胁、`quality` 理由、引用限定。
9. `## 8. 与仓库判断的关系`：支撑/削弱哪条 E/L/P；没有就写「只作边界证据」。
10. `## 9. 还没解决 / 下一步`：可实验的问题优先。
11. `## 10. 原文`：arXiv/代码链接。

**长度**：L3 约 250–360 行；L2 约 160–260 行；L1 约 100–240 行。长度是目标不是门；**自包含优先**，L1 的判断可以只有一页，digest 仍可写长。定义见 [conventions](../meta/conventions.md#阅读深度l1l2l3)。

**禁止**：

- 「详见 card」代替术语/方法/数字。
- 裸数字（没有条件/样本量/设置）。
- 把作者结论与读者推断混在一起。
- 用大量链接串起上下文；链接只放原文/代码。

## 4. 字段

| 字段 | 取值 | 含义 |
|---|---|---|
| `status` | `seed` / `draft` / `stabilized` / `superseded` | 文档成熟度 |
| `source_type` | `paper` / `preprint` / `blog` / `engineering` / `standard` / `talk` / `survey` / `open-source` | 素材类型；证据天花板见 [source-types](../meta/source-types.md) |
| `reading` | 论文/材料：`未读` / `综述级` / `摘要级` / `精读` / `已消化`；代码：`未读` / `已读代码` / `已跑通` | 读到什么程度（写在 card） |
| `provenance` | 论文/材料：`原文正文` / `原文摘要` / `综述转述` / `未核`；代码：`一手代码` / `一手文档` / `未核` | 证据来自哪里（写在 card） |
| `home` / `subtopic` / `also_supports` | `topics/<派>` / `<子主题>` / `[<子主题>]` | 归位；移动子主题只改 `subtopic`；一篇喂多个子主题时，主归位放 `subtopic`，其余放 `also_supports` |
| `evidence_role` | `execution-test` / `mechanism-only` / `harness-evidence` / `boundary-ruler` | 对中心问题提供哪类证据 |
| `execution_form` | `engine` / `compiled` / `context` / `label` / `none` / `unknown` | 本体以什么形态被执行；见 [execution-forms](../topics/execution-forms.md) |
| `quality` | `A` / `B` / `C` | 证据强度粗分（写在 digest）；定义见 [conventions](../meta/conventions.md#字段与词汇) |

开源卡另有三组字段（不进论文卡）：

| 字段 | 取值 | 含义 |
|---|---|---|
| `commit` / `release` / `license` | SHA/tag / tag / SPDX | 版本与许可；**不 pin 不算入库** |
| `scan_date` / `stars_at_scan` / `last_push` | 日期 / 数字 / 日期 | 扫描快照；star 只作影响力参考 |
| `ontology_role` / `seam` / `execution_form` | `core/adjunct/none/unclear` / 六时刻 + `read-path/supply/reasoning/training/none` / `engine/compiled/context/label/none/unknown` | 本体地位、接缝/轴外位置、执行形态；**只写初判，定级在 digest**；旧 `execution` 字段已由 `execution_form` 取代 |

`seam` 的取值来自 [topics/seams.md](../topics/seams.md)：六个硬时刻（`action-gate` / `evidence` / `checker` / `commit-gate` / `memory` / `determinism`）+ 四个轴外位置（`read-path` / `supply` / `reasoning` / `training`）+ `none`。不是接缝写 `none`，并在 digest 里说明是“回路外”还是“尚未判定”。

正文推断句至少标一次 `已核` / `推测` / `存疑`；没有标的按 `推测`。

## 5. 新建的流程

### 5.1 论文

1. **落原文**：PDF 放 `src/papers/{arxiv_id}-{slug}/`，在 manifest 登记。
2. **转 MD**：`paper.md` + `references.md` + `appendix.md`；检查页码标记。
3. **写 card**：元数据 + 一句话 + 问题/设定 + 图表索引 + 作者局限；`reading`/`provenance` 如实，并填 `evidence_role` / `execution_form` / `subtopic`（多归位用 `also_supports`）。
4. **写 digest**：按 §3 骨架；先写「三句话」，再补术语/方法/数字/边界/工程。
5. **抽图**：2–3 张承载机制/结果的图；带页码、出处、「看什么」。
6. **落 topics**：更新派 `sources.md`（内容链 digest）→ `claims.md` / 子主题 dashboard；跨派才动 conclusions。
7. **自检**：过 [checklist](../meta/checklist.md) 与 [digest-audit](../meta/archive/2026-11/digest-audit.md) 标准。

### 5.2 开源项目

1. **先筛**：按 [open-source/README](./open-source/README.md) 的选择标准过一遍；没入选的不建目录。
2. **建目录**：`src/open-source/{org}-{repo}/`，从 `_templates/` 取三份模板。
3. **pin 版本**：`git ls-remote` 或 GitHub API 取 commit SHA；填 license/scan_date/stars。
4. **写 card**：本体在哪、调用点、证据入口；**只写可定位的事实**，执行/装饰的定级留到 digest。
5. **写 code-map**：3–10 个文件/符号，一条调用链；不贴代码。
6. **写 digest**：按 [open-source-digest](./_templates/open-source-digest.md) 的 10 段；每个判断带 `已核/已证/推测/存疑`。
7. **落 topics**：只在改变判断时动 `claims.md`；只是「论文机制没找到实现」→ 写进 `frontier.md` 的 G/N。
8. **自检**：过 [checklist](../meta/checklist.md)。

## 6. 台账

| 材料 | 卡 / 消化 | 阅读 / 来源 | 已喂到 |
|---|---|---|---|
| 老刘说NLP · 本体4方向20工作（2026-11-04） | [otology.card.md](./web/weixin-laoliu/otology.card.md) | 已消化 / 综述转述 | `topics/conclusions.md`、`topics/README.md`、`topics/05-produce/lifecycle/README.md`、`topics/domains.md` |
| HN · Netflix ontology-driven observability（2026-10-19） | [card](./web/hn-netflix-ontology-observability/hn-netflix-ontology-observability.card.md) | 已消化 / thread 原文 | 04 C.5/B.2 signal；不升 E |
| 24 篇历史论文（20 基础 + 4 扫描） | 各目录 `card.md` / `digest.md` | L3 12 篇 / L2 8 篇 / L1 4 篇 | 六派 README、claims、conclusions（E-01…E-22） |
| 4 篇补给（GGC / Glyph / NLKGQ / KGVoyager） | 各目录 `card.md` / `digest.md` | 精读；L2/L1 见各 card | `topics/03-knowledge/querying`、`topics/01-constraint/access-control`、conclusions（P1/P2 新 E） |
| 开源项目 | 状态与进度见 [open-source/README](./open-source/README.md)；未建卡的不算入库 | 6 个本轮已消化（4 本体 + OPA/Qlever 工程线）；3 个 <1,000★ 仍不建卡 | `topics/01-constraint`（commit-gate F5–F7、access-control）、`topics/02-judgment`（checker F7–F8）、`topics/05-produce`（generation F7、lifecycle 判断 4）、`topics/03-knowledge`（querying） |

> 论文按篇记；开源按项目记在 `open-source/README` 的状态表里，本页只留总账——**一处明细，一处总账，不重复**。

## 7. 已知缺口

- 28 篇都有 card + digest；**digest 已全部重写为自包含版本**（L3 250–360 行、L2 160–260、L1 100–240）；4 篇补给按 L1/L2 落（见各卡）；历史审计表见 [digest-audit](../meta/archive/2026-11/digest-audit.md)。
- L1 4 篇只到一页判断（Peeling/Evontree/SFE-O/ReX-GG），没有深读正文。
- 部署层回报、false-veto/false-defer、维护成本仍缺量化。
- 部分论文有 v2/v3 版本，当前取下载当日最新版；版本变化可能改变结论。
- `quality` 是粗分，不是同行评审结论；引用时仍看证据等级。
- 开源侧：本轮 4 个（≥1,000★）全部已消化（trustgraph、semantica、ontop、open-ontologies）；3 个 <1,000★ 已删除目录（元数据留在扫描快照）。**04 记忆 / 06 度量** 还没有「本体真执行」的开源样本，语义检索类项目不计入。这是缺口，不硬凑。
