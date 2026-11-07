---
updated: 2026-11-07
---

# src：源头池（原文 + 卡）

流水线的第一个工位。**一处收原文，一处放卡**：原文和它的卡同目录、同 stem，卡用 `.card.md` 后缀。

```
src/
├── papers/          # 原文 PDF + 同名 .card.md + manifest
├── web/             # 网页/博客原文 + 同名 .card.md
├── _templates/      # paper-card.md / material-card.md
└── README.md
```

## 规则

1. **原文只读。** `*.pdf` / 网页原文不改写、不摘编；改了就无法回查。卡的修改只发生在 `.card.md`。
2. **同名配对。** 论文原文 `2610.08082-polar.pdf` 的卡是 `2610.08082-polar.card.md`；网页原文 `otology.md` 的卡是 `otology.card.md`。找卡就看同目录同 stem。
3. **命名。** 论文用 `{arxiv_id}-{slug}.pdf` / `.card.md`；网页用 `{来源}/{slug}.md` / `.card.md`。
4. **登记。** 论文在 [`papers/manifest.md`](./papers/manifest.md) 登记；网页在 [`web/README.md`](./web/README.md) 说明。`_download.log` 保留下载结果。
5. **读没读，看卡。** 原文只回答「有没有」；`.card.md` 才回答「消化到哪」。

## 卡片字段

| 字段 | 取值 | 含义 |
|---|---|---|
| `status` | `seed` / `draft` / `stabilized` / `superseded` | 文档成熟度 |
| `source_type` | `paper` / `preprint` / `blog` / `engineering` / `standard` / `talk` / `survey` | 素材类型；证据天花板见 [source-types](../meta/source-types.md) |
| `reading` | `未读` / `综述级` / `摘要级` / `精读` / `已消化` | 读到什么程度 |
| `provenance` | `原文正文` / `原文摘要` / `综述转述` / `未核` | 证据来自哪里 |
| `home` / `subtopic` | `topics/<派>` / `<子主题>` | 卡片归位；移动子主题只改 `subtopic` |

正文里的推断句至少标一次 `已核` / `推测` / `存疑`；没有标的按 `推测`。

## 卡片分两类

| 类型 | 模板 | 用于 |
|---|---|---|
| 论文卡 | [_templates/paper-card.md](./_templates/paper-card.md) | 单篇论文/预印本。关注「它测了什么、结果是什么、没测什么」 |
| 材料卡 | [_templates/material-card.md](./_templates/material-card.md) | 博客、工程复盘、标准、演讲、综述。关注「作者在什么场景下报告了什么」 |

两类都用 `source_type` 区分，平铺在 `papers/` 或 `web/` 的原文旁边，不再按 `papers/` / `materials/` 分目录。

## 台账

| 材料 | 卡片 | 阅读 / 来源 | 已喂到 |
|---|---|---|---|
| 老刘说NLP · 本体4方向20工作（2026-11-04） | [otology.card.md](./web/weixin-laoliu/otology.card.md) | 已消化 / 综述转述 | `topics/conclusions.md`、`topics/README.md`、`topics/05-produce/lifecycle/README.md`、`topics/domains.md` |
| 20 篇基础论文（摘要+结论+局限） | [papers/](./papers/)（[manifest](./papers/manifest.md)） | 摘要级 / 原文摘要（8 篇逐条对照，12 篇未逐条对照） | 六派 README 逐篇标注 |
| 2026-11-07 前沿扫描批次（CASEL、Agents Are Systems） | [papers/](./papers/)（[scan](./papers/manifest-scan.md)） | 摘要级 / 原文摘要 | [action-gate](../topics/01-constraint/action-gate/README.md)、[06-measure/README](../topics/06-measure/README.md)（候选，待综合） |

## 什么时候 promote 到 topics

1. 材料改变某条判断或填一个开放问题；
2. ≥2 张卡指向同一子机制；
3. 需要独立 frontier。

路径：卡片 → `topics/<派>/sources.md` → `claims.md` / 子主题 README。只在池子里躺着、不改变判断的材料，留在 `src/` 与派 `frontier` 候选队列即可。

## 目录

| 路径 | 内容 |
|---|---|
| [`papers/`](./papers/) | 20 篇基础 + 2 篇扫描 PDF；同名 `.card.md`；[manifest](./papers/manifest.md) |
| [`web/`](./web/) | 网页/博客原文；同名 `.card.md`；规则见 [web/README.md](./web/README.md) |
| [`_templates/`](./_templates/) | 论文卡、材料卡模板 |

## 已知缺口

- 只有摘要级别的核验，正文尚未逐篇精读。
- 部分论文有 v2/v3 版本，当前取的是下载当日的最新版本；版本变化可能改变结论。
