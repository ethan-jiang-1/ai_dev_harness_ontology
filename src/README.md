---
updated: 2026-11-07
---

# src：源头池（一篇一目录）

流水线的第一个工位。**一篇论文一个目录**，目录名是 `{arXiv ID}-{题目 slug}`；原文、分解、消化、图都收在里面，打开目录就能从原文走到判断。

```
src/
├── papers/
│   ├── manifest.md
│   ├── manifest-scan.md
│   └── {arxiv_id}-{slug}/
│       ├── {arxiv_id}-{slug}.pdf     # 原文，只读
│       ├── paper.md                  # 正文：PDF 完整转换（保留页码标记）
│       ├── references.md             # 参考文献：单独成文件，默认不读
│       ├── appendix.md               # 附录/补充材料：单独成文件，默认不读
│       ├── card.md                   # 分解：论文说了什么
│       ├── digest.md                 # 消化：工程思路 / 实用意义 / 质量 / 洞察
│       └── figures/                  # 论文原图（有图才建）
├── web/                              # 网页/博客原文 + 同名 .card.md
├── _templates/                       # card / digest / material 卡模板
└── README.md
```

## 规则

1. **原文只读。** `*.pdf` / 网页原文不改写、不摘编；改了就无法回查。修改只发生在 `card.md` / `digest.md`。
2. **一篇一目录。** 论文目录用 `{arxiv_id}-{slug}`，如 `2610.08082-polar/`；PDF 保留原名；卡固定叫 `card.md`，消化固定叫 `digest.md`。
3. **先转 MD，再建卡。** PDF 完整转换为 `paper.md`，并把 `references.md` / `appendix.md` 单独切出；正文保留 `<!-- page N -->`。参考文献与附录默认不读，只有核引文/查细节时打开。转换用 `pymupdf4llm`，公式/表格可能有版式噪声，引用前回 PDF 核。
4. **卡与消化分工。** `card.md` 只记**论文说了什么**（问题、方法、数字、局限、引文、图表索引）；`digest.md` 记**我们怎么用**（工程思路、实用意义、质量评估、洞察、成本与使能条件、何时别用）。判断不进 `card.md`，事实不进 `digest.md` 的引文。
5. **图随论文。** 论文原图放 `figures/`；文件名 `fig-{n}-{slug}.png`；图注写「看什么」、页码、版权。topics 引用时带出处。
6. **登记。** 论文在 [`papers/manifest.md`](./papers/manifest.md) 登记；网页在 [`web/README.md`](./web/README.md) 说明。`_download.log` 保留下载结果。
7. **读没读，看卡。** 原文只回答「有没有」；`card.md` 的 `reading` 回答「读到哪」；`digest.md` 回答「消化成什么判断」。

## 卡片字段

| 字段 | 取值 | 含义 |
|---|---|---|
| `status` | `seed` / `draft` / `stabilized` / `superseded` | 文档成熟度 |
| `source_type` | `paper` / `preprint` / `blog` / `engineering` / `standard` / `talk` / `survey` | 素材类型；证据天花板见 [source-types](../meta/source-types.md) |
| `reading` | `未读` / `综述级` / `摘要级` / `精读` / `已消化` | 读到什么程度 |
| `provenance` | `原文正文` / `原文摘要` / `综述转述` / `未核` | 证据来自哪里 |
| `home` / `subtopic` | `topics/<派>` / `<子主题>` | 卡片归位；移动子主题只改 `subtopic` |
| `quality`（digest） | `A` / `B` / `C` | 证据强度粗分；定义见 [conventions](../meta/conventions.md#字段与词汇) |

正文里的推断句至少标一次 `已核` / `推测` / `存疑`；没有标的按 `推测`。

## 两类材料

| 类型 | 模板 | 用于 |
|---|---|---|
| 论文 card | [_templates/paper-card.md](./_templates/paper-card.md) | 论文/预印本的分解：测了什么、结果、没测什么 |
| 论文 digest | [_templates/paper-digest.md](./_templates/paper-digest.md) | 同一篇的工程消化：机制、成本、质量、洞察 |
| 材料卡 | [_templates/material-card.md](./_templates/material-card.md) | 博客、工程复盘、标准、演讲、综述 |

论文用 `papers/{arxiv_id}-{slug}/`；网页/博客仍平铺在 `web/`，卡与原文同目录 `.card.md`。两类都用 `source_type` 区分。

## 台账

| 材料 | 卡片 / 消化 | 阅读 / 来源 | 已喂到 |
|---|---|---|---|
| 老刘说NLP · 本体4方向20工作（2026-11-04） | [otology.card.md](./web/weixin-laoliu/otology.card.md) | 已消化 / 综述转述 | `topics/conclusions.md`、`topics/README.md`、`topics/05-produce/lifecycle/README.md`、`topics/domains.md` |
| 20 篇基础论文 | [papers/](./papers/)（[manifest](./papers/manifest.md)） | 摘要级 / 原文摘要（8 篇逐条对照，12 篇未逐条对照） | 六派 README 逐篇标注 |
| 2026-11-07 前沿扫描批次（CASEL、Agents Are Systems） | [papers/](./papers/)（[scan](./papers/manifest-scan.md)） | 摘要级 / 原文摘要 | [action-gate](../topics/01-constraint/action-gate/README.md)、[06-measure/README](../topics/06-measure/README.md)（候选，待综合） |
| 22 篇论文（20 基础 + 2 扫描） | [papers/](./papers/) 各目录的 `card.md` / `digest.md` | L3 12 篇 / L2 6 篇 / L1 4 篇 | 六派 README、claims、conclusions（E-01…E-19） |
| CAI（2610.41172） | [card](./papers/2610.41172-context-as-infrastructure/card.md) / [digest](./papers/2610.41172-context-as-infrastructure/digest.md) | 精读 / 原文正文 | 03 compilation、00 context、E-01/E-08/E-14 |

## 什么时候 promote 到 topics

1. 材料改变某条判断或填一个开放问题；
2. ≥2 张卡指向同一子机制；
3. 需要独立 frontier。

路径：`card.md` → `digest.md` → `topics/<派>/sources.md` → `claims.md` / 子主题 README。只在池子里躺着、不改变判断的材料，留在 `src/` 与派 `frontier` 候选队列即可。

## 目录

| 路径 | 内容 |
|---|---|
| [`papers/`](./papers/) | 22 篇：20 基础 + 2 扫描；每篇一个目录；[manifest](./papers/manifest.md) |
| [`web/`](./web/) | 网页/博客原文；同名 `.card.md`；规则见 [web/README.md](./web/README.md) |
| [`_templates/`](./_templates/) | 论文 card、论文 digest、材料卡模板 |

## 已知缺口

- 22 篇全部有 card + digest；L1 4 篇只到一页判断（Peeling/Evontree/SFE-O/ReX-GG），没有深读正文。
- 部署层回报、false-veto/false-defer、维护成本仍缺量化；这是下一阶段（experiments + frontier）的空缺。
- 部分论文有 v2/v3 版本，当前取的是下载当日的最新版本；版本变化可能改变结论。
- `digest.md` 的 `quality` 是粗分，不是同行评审结论；引用时仍看证据等级。
