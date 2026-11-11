---
status: draft
updated: 2026-11-11
---

# meta：规则、模板与历史

> 这一页回答「meta 里有什么、哪个是现行、哪个只是历史」。**先看本页，不要直接 `ls`。**

## 现行规则（写之前读）

| 文件 | 作用 | 什么时候读 |
|---|---|---|
| [../CHARTER.md](../CHARTER.md) | **全仓宪章**：研究档案，不做实施 | 进入仓库先读 |
| [conventions.md](./conventions.md) | 证据等级、字段、命名、台账纪律 | 动笔前必读 |
| [checklist.md](./checklist.md) | 交稿前检查 | 每次改完 |
| [deliverable-quality.md](./deliverable-quality.md) | **交付物质量评分卡**（12 维 + 5 门槛 + 抽样协议） | 评估/打磨 `deliverables/` 时 |
| [source-types.md](./source-types.md) | 素材类型与证据天花板 | 引入新类型/博客/开源时 |
| [topic-research-protocol.md](./topic-research-protocol.md) | 派与子主题怎么长、frontier 怎么用 | 开新子主题/做扫描时 |
| [loading.md](./loading.md) | 按任务加载（渐进披露） | 接手时 |
| [state.md](./state.md) | **当前计数、阻塞、最后自检**；历史日志见 [state-log](./state-log.md) | 想知道“现在到哪了” |
| [models.md](./models.md) | **可用模型与本地约束**（不装本地模型；只用 Yovole 两个） | 要跑任何模型依赖的实验时 |

## 模板与工具

| 文件 | 作用 |
|---|---|
| [note-template.md](./note-template.md) | 主题笔记模板 |
| [subtopic-template/](./subtopic-template/README.md) | 子主题四件套模板 |
| [tools/check_repo.py](./tools/check_repo.py) | 只读自检（链接/枚举/ID/清单/计数）；见 [ADR 0005](../adr/0005-repo-self-check.md) |

## 现行计划与台账

| 文件 | 作用 | 状态 |
|---|---|---|
| [term-baseline.md](./term-baseline.md) | ADR 0011 的术语差异表 v0（10 词）：origin/判定/动作 | 现行 v0（2026-11-11） |
| [执行计划](../deliverables/_plans/README.md) | 核心计划、进度板、一页状态、术语/标准子计划 | 现行（2026-11-11） |
| [open-source-digestion-plan.md](./open-source-digestion-plan.md) | 开源项目怎么吸收进 topics | 现行（2026-11-09） |
| [open-source-absorption.md](./open-source-absorption.md) | 代码发现 → topics 的吸收矩阵 | 现行（2026-11-09） |

## 历史归档（不要当现行规则）

[archive/2026-11/](./archive/2026-11/README.md) 存放 2026-11-07～09 的消化计划、质量计划/报告、digest/card 审计、critic 抽样与全审（full-audit）。这些文件已标 `status: superseded`，只用于追溯“当时怎么判的”，**不要用来指导现在的写入**。

## 一条规则

meta 根只放**现行**规则、模板、台账与状态；一次性的计划/审计/报告在完成后移入 `archive/<YYYY-MM>/`，并在本页登记。不要把 meta 变成第二个内容层。
