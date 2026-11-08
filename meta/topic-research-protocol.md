# 主题持续挖掘协议

每个派不是一篇静态综述，而是一个持续生长的研究面。每个派根目录有四个文件，外加可增长的子主题：

- `README.md`：稳定综合。核心主张、边界、硬证据、开放问题。只在判断被改变时改写。
- `frontier.md`：活页。前沿问题、信号源、检索式、候选队列、入档判据、最近扫描。可以频繁更新。
- `claims.md`：本派局部结论（`L-xx`），跨派/交付物才升 `E-xx`。
- `sources.md`：本派卡片索引。

`README` 回答「我们现在信什么」；`frontier` 回答「下一步查什么、为什么」。

派内可以再有子主题：`topics/<派>/<子主题>/README.md`。子主题可以有自己的 `frontier.md`；派 `frontier.md` 只汇总，不重复子主题正文。

## 1. 前沿问题从哪来

- `README.md` 的「开放问题」。
- `conclusions.md` 的「冲突 / 存疑」。
- 相邻派的边界问题（例：02 的误报 vs 01 的过剪枝）。
- 工程侧的真实失败（如果有）。
- 新论文与旧结论的张力（例：E-01 vs E-12 的 C-04）。

每条前沿问题要写成**可判定**的句子：能说清「什么结果会让它前进/后退」。写不成，就还是口号。

## 2. 信号源分三级

| 级别 | 例子 | 用法 |
|---|---|---|
| T1 一手 | 顶会/顶刊论文、官方 benchmark、可复现代码 | 可入卡、可升「已核」 |
| T2 近端 | arXiv 近 6 个月、实验室 blog、工程复盘 | 先入候选；读摘要后可入卡 |
| T3 二手 | 综述、公众号、推文 | 只作索引；引用标「转述 / 待核」 |

**综述摘要不等于论文结论。** T3 只用来找线索，不用来下判断。

## 3. 检索式

每派在 `frontier.md` 写 4-6 条固定查询：核心词 + 机制词 + 评测词。每季度改一次。检索时同时做：

- **关键词**：arXiv / Google Scholar / 会议 proceedings。
- **雪球**：从现有 20 篇的参考文献与引用，往回/往前各一层。
- **Benchmark 反查**：谁在 SOTA，用了什么 harness，失败案例是什么。
- **作者/实验室跟踪**：本派核心作者的新工作。

## 4. 入档判据

一条候选只有满足以下之一才建卡：

1. 会改变某条 `E-xx / Q-xx / C-xx` 或派内 `L-xx` 的可信度。
2. 会填一个 `README.md` 的开放问题。
3. 会推翻一个派的边界判据。

否则只留在 `frontier.md` 的候选队列，不建卡。**不要为「看起来覆盖了」建卡。**

## 5. 入档流程

```
候选 → 卡片（src/）→ 派 sources.md → 派 claims.md → 子主题 README 的 delta
     →（只有跨派/交付物）conclusions 更新 → 交付物重抽
```

- **本地优先**：派内新判断先写 `<派>/claims.md`；不要直接改 `conclusions.md`。
- 卡片的 `provenance` 必须写清：原文正文 / 原文摘要 / 综述转述。
- 卡片修正了旧判断 → 在 `updates:` 列出所有要回改的主题页，并逐页改。
- 派 README 只在判断被改变时改写；否则只更新 `frontier.md` 与 `sources.md`。
- 新派不轻易开：先在 `conclusions.md` 记「悬空结论」，累积三条以上再立派。

## 6. 节奏

- **每周**：每派 30 分钟扫描，更新 `frontier.md` 的「最近扫描」。
- **每月**：把候选队列里 ≥3 条同向的证据合成一次，决定是否改 `claims` / 子主题 README；只有跨派才改 `conclusions`。
- **每季度**：重排优先级，检查是否有派需要拆分/合并；更新检索式。

## 7. 反模式

- 用综述摘要当论文结论。
- 追热点但说不出改变哪条判断。
- 只加卡，不改 `README` / `conclusions`。
- 把 `frontier.md` 写成第二篇综述——它只放「下一步做什么」。
- 为「看起来完整」创建空文件或占位小节。

## 8. 子主题与素材类型

- **子主题**：派 README 只做地图；子主题 README 只做 index/dashboard；详细机制、发现、路线分别放 `mechanism.md` / `findings.md` / `frontier.md`。成立条件（满足其一）：有自己的判断与边界；≥2 张卡片共享同一子机制；需要自己的 frontier。不预建空子目录。见 [ADR 0003](../adr/0003-subtopics-and-source-types.md) 与 [§10](#10-readme-是-index不是正文)。
- **素材类型**：论文在 `src/papers/{arxiv_id}-{slug}/`，目录内含 `<stem>.pdf` / `card.md` / `digest.md` / `figures/`；网页在 `src/web/`，卡与原文同名 `.card.md`。都用 `source_type` 区分。
- **证据天花板**：博客/工程的 `已核` 只指「作者报告了 X」；一般规律默认 `推测`。见 [source-types](./source-types.md)。

## 9. 子主题的 prompt / run

- 子主题可以有一个 `prompt.md`：问题、输入、输出格式、证据规则。
- 每次运行把输出写到 `runs/YYYY-MM-DD-<slug>.md`，不要直接改 README。
- run 必须带 `prompt` / `model` / `sources` / `claims_changed`。
- 审 run 后，结论才进 `claims.md` / README；run 保留作审计轨迹。
- 模板见 [subtopic-template](./subtopic-template/README.md)。

## 10. README 是 index，不是正文

内容一多，README 会同时变成索引、正文、证据表和路线图，结果是：**看不见「发现了多少」「还缺什么」「下一步看什么」**。所以三类 README 各司其职：

| README | 角色 | 只放 |
|---|---|---|
| 根 `README.md` | 门厅 / router | 这是什么、从哪开始、当前状态；细节全链走 |
| `topics/<派>/README.md` | 派地图 | 子主题表 + 每页状态 + 本派 top claims；不展开机制 |
| `topics/<派>/<子主题>/README.md` | dashboard | 覆盖范围、已发现/未发现/下一步计数、当前判断、文件地图 |

### 子主题四件套

```
topics/<派>/<子主题>/
├── README.md       # index：dashboard + 当前判断 + 文件地图（一屏以内）
├── findings.md     # 发现索引：F1… 一行一条，带等级与链接
├── findings/       # 可选：每条/每组发现的详细证据（超过 ~5 行就拆）
├── frontier.md     # 未发现（G）+ 下一步（N）+ 候选/检索式
├── mechanism.md    # 可选：机制怎么跑（稳定综合）
├── prompt.md       # 可选：常驻研究 prompt
└── runs/           # 可选：按日期输出
```

**判断放哪**：

- `findings.md`：已经能站住的判断。每条带 `F` 编号、等级、条件、反例/边界、来源。
- `frontier.md`：还没站住的判断 + 下一步。`G` 是 gap（缺什么、为什么重要、关闭它需要什么、去哪找、优先级）；`N` 是 next（候选论文/检索式/来源、预期改变哪条 F/G、成本）。
- `mechanism.md`：机制的结构化描述；不写“我们信什么”，只写“它怎么跑”。

**编号是局部的**：`F1` / `G1` / `N1` 只在当前子主题内唯一；跨页引用带路径，例如 `action-gate/F3`。

**长度纪律**：README 一屏以内（约 60–80 行）。超过就说明内容该下沉到 `findings/` 或 `mechanism.md`，不要靠加长 README 解决。

**迁移规则**：

1. 先迁“重”页（有 ≥3 条判断或 ≥2 个未解决 gap 的页）；薄页只加 dashboard，不硬拆。
2. `findings.md` 先做索引；某条发现超过 ~5 行或需要独立证据表，再拆到 `findings/<slug>.md`。
3. 不预建空 `findings/`、`mechanism.md`、`runs/`。
4. 迁完一页，回改派 README 的子主题表与 `sources.md`，并在卡片 `updates:` 登记（如果判断变了）。
