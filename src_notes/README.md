---
updated: 2026-11-07
---

# src_notes：粗读卡池

流水线的第二个工位。每份材料一张卡，卡片回答：**它说了什么、有多可信、喂给哪个主题。**

**定位**：`src_notes` 是粗糙源头池的卡片层。卡片先粗读、可互不关联；只有发现好材料后，才 promote 到 `topics/` 做深度研究。

这是整个仓库的盘点表。想知道「读了多少」看这里，不看 `src_raw/`。

## 台账

| 材料 | 卡片 | 阅读 / 来源 | 已喂到 |
|---|---|---|---|
| [老刘说NLP · 本体4方向20工作](./cards/2026-11-04-ontology-20-papers.md)（2026-11-04） | [cards/](./cards/) | 已消化 / 综述转述 | `topics/conclusions.md`、`topics/README.md`、`topics/05-produce/lifecycle/README.md`、`topics/domains.md` |
| └ 其中 20 篇论文（摘要+结论+局限） | [cards/](./cards/) | 摘要级 / 原文摘要（8 篇逐条对照，12 篇未逐条对照） | 六派 README 逐篇标注 |
| └ 2026-11-07 前沿扫描批次（CASEL、Agents Are Systems） | [cards/](./cards/) | 摘要级 / 原文摘要 | [action-gate](../topics/01-constraint/action-gate/README.md)、[06-measure/README](../topics/06-measure/README.md)（候选，待综合） |

## 阅读进度（`reading`）

| 值 | 含义 |
|---|---|
| `未读` | 只登记了来源，没打开 |
| `综述级` | 只读了综述/二手转述，未对原文 |
| `摘要级` | 读过论文摘要与首页，知道它做了什么、没做什么 |
| `精读` | 读过正文，能复述方法与结果 |
| `已消化` | 已提炼为可引用判断，并写入 `topics/` |

## 来源（`provenance`）

| 值 | 含义 |
|---|---|
| `原文正文` | 读过论文正文 |
| `原文摘要` | 读过论文摘要/首页 |
| `综述转述` | 只来自综述或二手材料 |
| `未核` | 尚未核对来源 |

## 素材类型（`source_type`）

论文卡用 `paper` / `preprint`；材料卡用 `blog` / `engineering` / `standard` / `talk` / `survey`。它回答「素材是什么」，与「读到哪」（`reading`）和「从哪来」（`provenance`）正交。证据天花板见 [source-types](../meta/source-types.md)。

**文档 `status` 与阅读 `reading` 是两件事。** 卡片本身是文档，`status` 用 `seed / draft / stabilized / superseded`；`reading` 才表示读到哪。定义见 [conventions](../meta/conventions.md#字段与词汇)。

**卡片状态与 `src_raw/` 的下载状态无关。** 下载只代表「拥有」，不动笔记账。

## 卡片归位（`home` / `subtopic`）

`home` 指向 `topics/<派>`；`subtopic` 指向子主题目录。移动/改名子主题时只改 `subtopic`，不动 `home`；这样 `topics/` 内部调整不会牵连卡片。

## 卡片分两类，平铺在 `cards/`

| 类型 | 模板 | 用于 |
|---|---|---|
| 论文卡 | [cards/_template-paper.md](./cards/_template-paper.md) | 单篇论文/预印本。关注「它测了什么、结果是什么、没测什么」 |
| 材料卡 | [cards/_template-material.md](./cards/_template-material.md) | 博客、工程复盘、标准、演讲、综述。关注「作者在什么场景下报告了什么」 |

两类最大的差别：论文卡必须有**结果数字**与**未测范围**两栏；材料卡必须写**场景与 scope**。综述最容易省略的正是这两样。两类都用 `source_type` 区分，不再按 `papers/` / `materials/` 分目录。

## 什么时候 promote 到 topics

1. 材料改变某条判断或填一个开放问题；
2. ≥2 张卡指向同一子机制；
3. 需要独立 frontier。

路径：卡片 → `topics/<派>/sources.md` → `claims.md` / 子主题 README。只在库里躺着、不改变判断的材料，留在 `src_notes` 与派 `frontier` 候选队列即可。

## 一条纪律

卡片写完，必须回答三句：

1. **这份材料改变了哪条判断？** 改变了 → 先写该派 `claims.md` / 子主题；跨派或进交付物才升 [conclusions](../topics/conclusions.md)；没改变 → 只增来源，不动正文。
2. **它喂给了哪个主题？** → 更新上面的台账。
3. **它修正了旧判断吗？** 修正了 → 在卡片 `updates:` 列出所有要回改的主题页，逐页改。

如果一份材料既不改变判断、也不提供来源，它就不该有卡片——它只是 `src_raw/` 里的一个文件。
