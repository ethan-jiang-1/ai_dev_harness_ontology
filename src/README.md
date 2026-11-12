---
updated: 2026-11-12
---

# src：来源层（三类材料，各自一目录）

流水线的第一个工位。三类源材料，落点不同、契约相同：

| 类 | 落点 | 目录粒度 | 原文形态 |
|---|---|---|---|
| 论文 | `papers/` | 一篇一目录 `{arxiv_id}-{slug}/` | PDF + `paper.md` |
| 网页/博客/非 arXiv 论文 | `web/` | 一源一目录 `{来源}/` | 原文 MD；论文另存 PDF |
| 真实代码项目 | `open-source/` | 一个项目一目录 `{org}-{repo}/` | 不 vendor，pin commit + 链接 |

三类都解决三件事：**原文/代码在不在、它说了什么或怎么走、我们消化出了什么**。

## 0. 读者与写法：src 是给 Agent 的干货层

- **读者**：Agent（检索、引用、复用事实）；人不作为第一读者。
- **写什么**：思想、工程实践、事实、数字与条件、`file:symbol`、失败模式；`digest.md` 自包含，不要求读原文。
- **不写什么**：面向人的导读、路线图、总结陈词；这些在 `deliverables/`。
- **完成信号**：Agent 不读原文，就能从 digest 取用一条事实/锚点/条件。
- **边界**：不追求“好读”，追求“可取用”；面向人的重述是 `deliverables/` 的事。

> 非 arXiv 的会议论文/数据集（Zenodo、DLR 等）也落 `web/`，`source_type: paper`；材料卡即消化正文，不另建 digest（见 [web/README](./web/README.md)）。

```
src/
├── papers/
│   ├── manifest.md          # 全仓唯一论文登记（现行 12 篇；历史批次见审计）
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

## 0.1 两个角色 + 一份原文，一句话

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

**反向加载（从交付物倒查）**：不要从 `papers/manifest.md` 顺读。走 `conclusions` 的 E 行 → 该 E 链的 `digest.md` §4/§5 → 只有 digest 不够时才回 `paper.md` 的指定表/节。`card.md` 只在需要 provenance 时读；`references.md` / `appendix.md` 默认不读。三条交付物的具体反向链见 [meta/loading](../meta/rules/loading.md#从交付物倒查反向加载)。

**反向阅读锚点（digest 契约）**：§4「结果：数字与条件」、§5「这些数字不能说明什么」、§6「工程上怎么用」（**本篇价值主体**）、§8「与仓库判断的关系」——这四节编号固定，不重排；新增内容放 §9/§10。§6 必含 6.1 复刻顺序 / 6.2 成本与使能 / 6.3 何时用 / 6.4 三个坑+检测信号 / 6.5 工程配方；frontmatter 必填 `enabler`（为什么以前不行、现在行）。反向读不到 §4/§5 时，才回 `paper.md` 的指定表/节。

## 0.2 素材准入（宪章 §4 的落地，2026-11-11 起）

五道门全部通过才进 `src/`；判定写在卡上。**判据以 [CHARTER §4](../CHARTER.md#4-素材准入material-gate) 为唯一出处**；下表只是按材料类型的操作速查，与宪章冲突时以宪章为准。

**白名单 / 黑名单**：白名单 = 本目录 `admission: admitted`（含 probation）的卡，`check_repo` 强制校验，清单见 [manifest](./papers/manifest.md) / 下方台账 / [规范主干](../topics/trunk.md)；**不另设白名单文件**（避免第二份漂移副本）。黑名单 = [来源黑名单](../meta/rules/excluded-sources.md)（禁读/禁引），采/引前先查。

| 门 | 论文 | 网页/材料 | 开源项目 |
|---|---|---|---|
| G1 时效 | 首次提交/发表 ≥ **2026-06-01** | 发布 ≥ **2026-06-01** | `last_push` ≥ **2026-06-01** |
| G2 活跃 | 2026-06 后有版本/实现/讨论/采用 | 90 天内有新讨论/引用 | 180 天内有提交；≥2 名独立贡献者；有 release/tag |
| G3 影响 | `impact_evidence` 列 ≥2 个独立信号，至少 1 个 I1–I3 | 同左；`influence` 写点数/评论/引用/采用，不写形容词 | 采用/依赖/生产案例；star 只作辅助 |
| G4 来源 | 组织/社区优先；公司过 §4.4 | 同左；厂商文只作 signal | 基金会/社区/标准组织优先；公司项目要有独立采用 |
| G5 可核验 | arXiv/DOI + 日期 + 机构 | URL + 日期 + 作者/机构 + 快照 | commit + license + `file:symbol` |

- `admission: admitted` 才能建卡；`signal` 只进对应派 `frontier.md` 候选队列；`excluded` 不建目录，已入库的移出。
- 卡必填：`admission` / `gate_checked` / `impact_evidence` / `liveness` / `provenance_type`；论文卡另有 `published` / `venue` / `reliability` / `impact` / `region`。
- **区域 scope（沿用，独立于五门）**：新入档论文/项目的 origin 只收 **US / China / Germany / Singapore**；这是选题范围，不是影响门槛。
- **旧口径作废**：2026-07-01 起点、“`batch: 补给` 才查新鲜度”、“历史语料不回填”——全部由本节替代。回溯审计见 [来源清除审计](../meta/audits/2026-11-11-source-purge.md)。

## 0.3 准入字段与复审

字段定义以 [conventions §字段与词汇](../meta/rules/conventions.md#字段与词汇) 为唯一出处。卡必填 `admission` / `gate_checked` / `impact_evidence` / `liveness` / `provenance_type`；写不出两条独立信号就不要写 `admitted`。复审周期、probation 与窄例外以 [CHARTER §4.3/§4.4](../CHARTER.md#43-回溯与退出无-grandfathering) 为准，不另开口子。

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
- **候选与入库分开**：候选池、选择标准在 [open-source/README](./open-source/README.md)；入选项目才建目录。消化顺序与 C/A 闸见 [开源消化计划](../meta/archive/2026-11/open-source-digestion-plan.md)。
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
7. `## 6. 工程上怎么用`（**主角**）：6.1 复刻顺序、6.2 成本与使能（含 `为什么以前不行现在行`）、6.3 何时用/别用、6.4 三个坑+检测信号、6.5 工程配方（数据结构/参数默认值/幂等键/stop 与回滚/第一个 sprint）。
8. `## 7. 质量与边界`：证据类型、强项、威胁、`quality` 理由、引用限定。
9. `## 8. 与仓库判断的关系`：支撑/削弱哪条 E/L/P；没有就写「只作边界证据」。
10. `## 9. 还没解决 / 下一步`：可实验的问题优先。
11. `## 10. 原文`：arXiv/代码链接。

**长度**：L3 约 250–360 行；L2 约 160–260 行；L1 约 100–240 行。长度是目标不是门；**自包含优先**，L1 的判断可以只有一页，digest 仍可写长。定义见 [conventions](../meta/rules/conventions.md#阅读深度l1l2l3)。

**禁止**：

- 「详见 card」代替术语/方法/数字。
- 裸数字（没有条件/样本量/设置）。
- 把作者结论与读者推断混在一起。
- 用大量链接串起上下文；链接只放原文/代码。

## 4. 字段

字段与取值以 [conventions §字段与词汇](../meta/rules/conventions.md#字段与词汇) 为唯一出处（含开源卡的 commit/seam/ontology_role 三组与 `seam` 取值说明）；`seam` 的时刻/轴外位置定义见 [topics/seams.md](../topics/seams.md)。正文推断句至少标一次 `已核` / `推测` / `存疑`；没有标的按 `推测`。

## 5. 新建的流程

> 先过候选门槛：只有会改变判断/边界/交付物的来源才建卡；候选先记在对应派 `frontier.md`，不预建目录（见 [AGENTS](../AGENTS.md)「任务路由」）。

### 5.1 论文

1. **落原文**：PDF 放 `src/papers/{arxiv_id}-{slug}/`；在 [manifest](./papers/manifest.md) 登记（行格式照表头：`# | 批次 | arXiv | 短标题 | 页 | 方向 | 文件 | 卡片 | 消化`），下载结果记 [_download.log](./papers/_download.log)。
2. **转 MD**：`paper.md` + `references.md` + `appendix.md`；用 `pymupdf4llm` 逐页转，正文保留 `<!-- page N -->`；公式/表格回 PDF 核。
3. **写 card**：用 [paper-card](./_templates/paper-card.md)；元数据 + 一句话 + 问题/设定 + 图表索引 + 作者局限；`reading`/`provenance` 如实，并填 `evidence_role` / `execution_form` / `subtopic`（多归位用 `also_supports`）。
4. **写 digest**：用 [paper-digest](./_templates/paper-digest.md)，按 §3 骨架；先写「三句话」，再补术语/方法/数字/边界/工程。
5. **抽图**：2–3 张承载机制/结果的图；带页码、出处、「看什么」。
6. **落 topics**：更新派 `sources.md`（内容链 digest）→ `claims.md` / 子主题 dashboard；跨派才动 conclusions。
7. **自检**：过 [checklist](../meta/rules/checklist.md) 与 [digest 模板](./_templates/paper-digest.md) 的自包含要求；长度目标见 [conventions](../meta/rules/conventions.md#阅读深度l1l2l3)。

### 5.2 开源项目

1. **先筛**：按 [open-source/README](./open-source/README.md) 的选择标准过一遍；没入选的不建目录。
2. **建目录**：`src/open-source/{org}-{repo}/`，从 `_templates/` 取三份模板。
3. **pin 版本**：`git ls-remote` 或 GitHub API 取 commit SHA；填 license/scan_date/stars。
4. **写 card**：本体在哪、调用点、证据入口；**只写可定位的事实**，执行/装饰的定级留到 digest。
5. **写 code-map**：3–10 个文件/符号，一条调用链；不贴代码。
6. **写 digest**：按 [open-source-digest](./_templates/open-source-digest.md) 的 10 段；每个判断带 `已核/已证/推测/存疑`。
7. **落 topics**：只在改变判断时动 `claims.md`；只是「论文机制没找到实现」→ 写进 `frontier.md` 的 G/N。
8. **自检**：过 [checklist](../meta/rules/checklist.md)。

### 5.3 两类共同

- 入库后更新 [meta/state](../meta/status/state.md) 的计数与 [execution-forms](../topics/execution-forms.md) 的形态分布。
- 改判断：先本派 `claims.md`，跨派才 [conclusions](../topics/conclusions.md)；来源只进 `sources.md`。
- 自检 `check_repo`；失败不提交。

## 6. 台账

| 材料 | 卡 / 消化 | 阅读 / 来源 | 已喂到 |
|---|---|---|---|
| 12 篇过门论文（8 admitted + 4 probation） | 各目录 `card.md` / `digest.md` | 精读/L2/L1 见各卡；4 篇 probation 到 2027-05-11 | E-01/05/07/08/09/12/14/15/17/18/21/22；03/04/05/06 派页 |
| UniDataAgent（中国联通，2026-09-23） | [card](./papers/2609.27257-unidataagent/card.md) / [digest](./papers/2609.27257-unidataagent/digest.md) | 已消化 / 原文正文 | 10 中国；E-28/E-30/E-31 |
| CoeusBI（百度，VLDB 2026，2026-06-13） | [card](./papers/2606.15384-coeusbi/card.md) / [digest](./papers/2606.15384-coeusbi/digest.md) | 已消化 / 原文正文 | 10 中国；E-28/E-30/E-31 |
| 18 篇移出论文 | [tombstone](../meta/audits/2026-11-11-source-purge.md) | — | E-02/03/04/06/10/11/13/16/26 已撤回；主题页待重写 |
| HN · Netflix ontology-driven observability（2026-10-19） | [card](./web/hn-netflix-ontology-observability/hn-netflix-ontology-observability.card.md) | 已消化 / thread 原文 | 10 06.1 与 90.2 的 signal；不升 E |
| 中泰证券 QCon 2026（2026-09-02） | [card](./web/qcon-2026-zhongtai-ontology/qcon-2026-zhongtai-ontology.card.md) | 摘要级 / 议题页 | 10 中国；E-28/E-29/E-30 |
| 中泰证券 CCSA TC601（2026-10-15） | [card](./web/modb-2026-zhongtai-ontology/modb-2026-zhongtai-ontology.card.md) | 已消化 / 报道正文 | 10 中国、OKF；E-28/E-29/E-31/E-32 |
| Snowflake 内部 context layer（2026-08-17） | [card](./web/snowflake-context-layer-2026/snowflake-context-layer-2026.card.md) | 已消化 / 官方博客 | 10 美国；E-28/E-29/E-31 |
| Sigma 2,883-model semantic layer（2026-10-27） | [card](./web/sigma-semantic-layer-2026/sigma-semantic-layer-2026.card.md) | 已消化 / dbt 博客 | 10 美国；E-28/E-29/E-31 |
| Netflix 本体驱动可观测性（2026-10-16） | [card](./web/netflix-ontology-observability-2026/netflix-ontology-observability-2026.card.md) | 已消化 / 官方博客 | 10 美国；E-28/E-29 |
| Google Open Knowledge Format v0.1/v0.2（2026-06/07） | [card](./web/google-okf/google-okf.card.md) | 精读 / 规范正文 + 官方博客 | 10 4b、E-32；Knowledge Catalog 只到 C |
| GB/T 43697-2024 数据分类分级规则 | [card](./web/gbt-43697/gbt-43697.card.md) | 摘要级 / 原文摘要 | 01/policy F3/F4；三级 vs 1–4 是工程映射 |
| GB/T 35273-2020 个人信息安全规范 | [card](./web/gbt-35273/gbt-35273.card.md) | 摘要级 / 原文摘要 | 01/policy；PII 类别，不是 level 表 |
| W3C ODRL 2.2 | [card](./web/w3c-odrl-2.2/w3c-odrl-2.2.card.md) | 精读 / 原文正文 | 01/policy F2；冲突/义务/版本 |
| OASIS XACML 3.0 | [card](./web/oasis-xacml-3.0/oasis-xacml-3.0.card.md) | 精读 / 原文正文 | 01/policy F2；合并算法/obligation |
| W3C SHACL | [card](./web/w3c-shacl/w3c-shacl.card.md) | 摘要级 / 原文摘要 | 05/consumability、02/output-validation §2.5 |
| ODCS v3.1.0 | [card](./web/odcs-v3.1/odcs-v3.1.card.md) | 精读 / 原文正文 | 05/consumability §3、02 附录 D §10.1 |
| W3C OWL 2 Profiles | [card](./web/w3c-owl2-profiles/w3c-owl2-profiles.card.md) | 摘要级 / 原文摘要 | read-path §9 alias 规则；02 R8、03 claim 走查 |
| W3C SHACL-AF | [card](./web/w3c-shacl-af/w3c-shacl-af.card.md) | 摘要级 / 原文正文 | read-path fail-open 的标准边界；02 R8、03 claim 走查 |
| ISO/IEC 21838（顶层本体） | [card](./web/iso-iec-21838/iso-iec-21838.card.md) | 摘要级 / 原文摘要 | 05/representation；TLO 与领域本体边界 |
| OMG Commons 1.3 | [card](./web/omg-commons/omg-commons.card.md) | 摘要级 / 原文摘要 | 05/representation；可复用模块与最小承诺 |
| 开源项目 | 状态与进度见 [open-source/README](./open-source/README.md) | 8 个已消化（4 本体 + OPA/Qlever + Great Expectations + OpenLineage） | `topics/01-constraint`、`02-judgment`、`03-knowledge`、`05-produce` |

> 论文按篇记；开源按项目记在 `open-source/README`；标准按卡记。**一处明细，一处总账。**
> 2026-11-11 起，论文层只保留 10 篇过门来源；被删的 18 篇不再出现在台账内容里，只在 [审计](../meta/audits/2026-11-11-source-purge.md) 留 tombstone。

## 7. 已知缺口

- **第一优先级：重写被删源的段落。** 18 篇论文 + 3 个旧网页已移出，主题页/交付物里仍有按它们写成的数字与判断；链接已指向 tombstone，但段落未改完。重写前不得引用。
- 10 篇过门论文中 4 篇是 `probation`（GGC/Agents/N&D/CASEL）：只有 I2 + 真实评估，缺 I3/I4/I5；2027-05-11 前补不到第二信号就移出。
- 9 条 E 已撤回（E-02/03/04/06/10/11/13/16/26），E-21 改写为 GGC 单路线，E-19 降为 `推测`；交付物引用这些编号的段落同步失效。
- 部署层回报、false-veto/false-defer、维护成本仍缺量化。
- `quality` 是粗分，不是同行评审结论；引用时仍看证据等级。
- 开源侧：8 个已消化；`04 记忆 / 06 度量` 仍缺「本体真执行」的开源样本，语义检索类不计入。
- 硬对象 94 里 20 个已随删论文标「已撤回」（2026-11-12 对账，含 O-T05/T06/T07/P02/P03 五个停线/协议）；换锚待过门新源，见 [objects 变更记录](../topics/objects.md)。
