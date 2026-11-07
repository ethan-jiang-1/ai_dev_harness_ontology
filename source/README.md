---
updated: 2026-11-07
---

# source：源头

流水线的第一个工位。**原始材料原样落盘，不改写、不摘编、不整理。** 这里既有论文原文（一手），也有综述/网页（二手）；一手还是转述，按子目录说明与 `notes/` 卡片区分。

整理发生在 `notes/`。这里保持原样，是为了任何时候都能回到原文核对——综述的转述与原文的差别，往往就藏在被省略的限定条件里。

## 规则

1. **原样存档。** 下载什么就存什么，不做改写、不做摘要、不重命名内部内容。
2. **命名带身份。** 论文用 `{arxiv_id}-{slug}.pdf`；博客/网页用 `web/{来源}/` 子目录加原文件名或日期-slug。
3. **登记。** 论文在 [`papers/manifest.md`](./papers/manifest.md) 登记；博客/工程材料在 [`notes/materials/`](../notes/materials/) 建卡；`_download.log` 保留下载结果。
4. **读没读，看 `notes/`。** `source/` 只回答「有没有」，`notes/` 才回答「消化到哪」。

## 目录

| 路径 | 内容 |
|---|---|
| [`papers/`](./papers/) | 20 篇基础 arXiv PDF（源综述）+ 2 篇前沿扫描 PDF |
| [`web/`](./web/) | 博客、网页、工程材料；规则见 [web/README.md](./web/README.md) |
| [`web/weixin-laoliu/`](./web/weixin-laoliu/) | 该综述原文（二手材料；文件名 `otology.md` 是 `ontology` 的笔误，内容是本体综述） |
| [`papers/manifest.md`](./papers/manifest.md) | 20 篇基础清单：编号、页数、方向、文件 |
| [`papers/manifest-scan.md`](./papers/manifest-scan.md) | 2026-11-07 前沿扫描批次（2 篇：CASEL、Agents Are Systems） |
| [`papers/_download.log`](./papers/_download.log) | 下载结果记录 |

## 已知缺口

- 只有摘要级别的核验，正文尚未逐篇精读（`notes/papers/` 与 `notes/materials/` 里的卡片会逐步补）。
- 部分论文有 v2/v3 版本，当前取的是下载当日的最新版本；版本变化可能改变结论，重读时需核对。
