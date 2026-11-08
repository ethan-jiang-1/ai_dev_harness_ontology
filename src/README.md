---
updated: 2026-11-08
---

# src：来源层（一篇一目录）

流水线的第一个工位。**一篇论文一个目录**，目录名是 `{arXiv ID}-{题目 slug}`。这里解决三件事：**原文在不在、论文说了什么、我们消化出了什么**。

```
src/
├── papers/
│   ├── manifest.md
│   ├── manifest-scan.md
│   └── {arxiv_id}-{slug}/
│       ├── {arxiv_id}-{slug}.pdf     # 原文，只读
│       ├── paper.md                  # 正文全文 MD（保留页码标记）
│       ├── references.md             # 参考文献（默认不读）
│       ├── appendix.md               # 附录/补充材料（默认不读）
│       ├── card.md                   # 来源卡：元数据 + 论文说了什么（短）
│       ├── digest.md                 # 消化正文：自包含，下游唯一入口
│       └── figures/                  # 论文原图（有图才建）
├── web/                              # 网页/博客原文 + 同名 .card.md
├── _templates/                       # card / digest / material 模板
└── README.md
```

## 0. 三个角色，一句话

| 文件 | 角色 | 谁读 |
|---|---|---|
| `paper.md` / PDF | **原文**：完整、未消化 | 核引文、查细节时 |
| `card.md` | **来源卡**：这篇是什么、读没读、原文/图在哪 | 需要 provenance 时 |
| `digest.md` | **消化正文**：自包含的判断与细节 | **topics / 下游默认只读这个** |

**信息流**：

```
PDF ──▶ paper.md（原文，保真）
          │
          ├──▶ card.md（来源卡：元数据 + 一页索引）
          │
          └──▶ digest.md（自包含消化）──▶ topics/sources.md ──▶ claims / 子主题
```

`card.md` 与 `digest.md` 都从原文来，但**不是上下游关系**：card 是来源登记，digest 是消化正文。下游不需要先读 card。

## 1. 规则

1. **原文只读。** `*.pdf` / 网页原文不改写、不摘编；修改只发生在 `card.md` / `digest.md`。
2. **一篇一目录。** 目录用 `{arxiv_id}-{slug}`；PDF 保留原名；来源卡固定 `card.md`，消化固定 `digest.md`。
3. **先转 MD，再建卡。** PDF 完整转 `paper.md`，把 `references.md` / `appendix.md` 单独切出；正文保留 `<!-- page N -->`。转换用 `pymupdf4llm`；公式/表格可能有版式噪声，引用前回 PDF 核。
4. **card 短，digest 长。** `card.md` 不承载机制细节与判断；`digest.md` 承载全部下游需要的信息。**不要用「详见 card」代替内容**。
5. **digest 自包含。** 不假设读者读过论文或 card：定义术语、解释方法、数字带条件、说明不能证明什么、给出工程用法。链接只放原文/代码，放在最后。
6. **topics 引 digest，不引 card 作为内容。** `sources.md` 可同时给 card（provenance）与 digest（内容），但内容判断只从 digest 来。
7. **图随论文。** 原图放 `figures/`；文件名 `fig-{n}-{slug}.png`；图注写「看什么」、页码、版权。
8. **登记。** 论文在 [`papers/manifest.md`](./papers/manifest.md) 登记；`_download.log` 保留下载结果；网页规则见 [`web/README.md`](./web/README.md)。

## 2. `card.md` 的定位：来源卡，不是消化

`card.md` 只回答「这篇是什么、我从哪读的、原文/图在哪」。建议 40–70 行：

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

`digest.md` 是**自包含消化正文**。读者可能只读这一篇，不读 card/paper；所以它必须能独立成立。

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

**长度**：L3 约 150–250 行；L2 约 100–200 行；L1 约 50–100 行。L1 可以短，但仍要自包含。

**禁止**：

- 「详见 card」代替术语/方法/数字。
- 裸数字（没有条件/样本量/设置）。
- 把作者结论与读者推断混在一起。
- 用大量链接串起上下文；链接只放原文/代码。

## 4. 字段

| 字段 | 取值 | 含义 |
|---|---|---|
| `status` | `seed` / `draft` / `stabilized` / `superseded` | 文档成熟度 |
| `source_type` | `paper` / `preprint` / `blog` / `engineering` / `standard` / `talk` / `survey` | 素材类型；证据天花板见 [source-types](../meta/source-types.md) |
| `reading` | `未读` / `综述级` / `摘要级` / `精读` / `已消化` | 读到什么程度（写在 card） |
| `provenance` | `原文正文` / `原文摘要` / `综述转述` / `未核` | 证据来自哪里（写在 card） |
| `home` / `subtopic` | `topics/<派>` / `<子主题>` | 归位；移动子主题只改 `subtopic` |
| `quality` | `A` / `B` / `C` | 证据强度粗分（写在 digest）；定义见 [conventions](../meta/conventions.md#字段与词汇) |

正文推断句至少标一次 `已核` / `推测` / `存疑`；没有标的按 `推测`。

## 5. 新建一篇的流程

1. **落原文**：PDF 放 `src/papers/{arxiv_id}-{slug}/`，在 manifest 登记。
2. **转 MD**：`paper.md` + `references.md` + `appendix.md`；检查页码标记。
3. **写 card**：元数据 + 一句话 + 问题/设定 + 图表索引 + 作者局限；`reading`/`provenance` 如实。
4. **写 digest**：按 §3 骨架；先写「三句话」，再补术语/方法/数字/边界/工程。
5. **抽图**：2–3 张承载机制/结果的图；带页码、出处、「看什么」。
6. **落 topics**：更新派 `sources.md`（内容链 digest）→ `claims.md` / 子主题 dashboard；跨派才动 conclusions。
7. **自检**：过 [checklist](../meta/checklist.md) 与 [digest-audit](../meta/digest-audit.md) 标准。

## 6. 台账

| 材料 | 卡 / 消化 | 阅读 / 来源 | 已喂到 |
|---|---|---|---|
| 老刘说NLP · 本体4方向20工作（2026-11-04） | [otology.card.md](./web/weixin-laoliu/otology.card.md) | 已消化 / 综述转述 | `topics/conclusions.md`、`topics/README.md`、`topics/05-produce/lifecycle/README.md`、`topics/domains.md` |
| 22 篇论文（20 基础 + 2 扫描） | 各目录 `card.md` / `digest.md` | L3 12 篇 / L2 6 篇 / L1 4 篇 | 六派 README、claims、conclusions（E-01…E-19） |

## 7. 已知缺口

- 22 篇都有 card + digest；**digest 已全部重写为自包含版本**（L3 150–250 行、L2 100–200、L1 50–100）；审计表见 [digest-audit](../meta/digest-audit.md)。
- L1 4 篇只到一页判断（Peeling/Evontree/SFE-O/ReX-GG），没有深读正文。
- 部署层回报、false-veto/false-defer、维护成本仍缺量化。
- 部分论文有 v2/v3 版本，当前取下载当日最新版；版本变化可能改变结论。
- `quality` 是粗分，不是同行评审结论；引用时仍看证据等级。
