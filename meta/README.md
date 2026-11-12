---
status: draft
updated: 2026-11-12
---

# meta：文件索引

> **怎么用这一层**：先看 [AGENTS](./AGENTS.md)（30 秒入口：你要干什么去哪个子目录）。本页只做**文件索引**，不复述规则、不重复用法。
> 现行规则 vs 历史：只读 `rules/` `deliverables/` `status/` `templates/`；`audits/` 与 `archive/` 是快照，**不作现行规则**。

## rules/ — 现行规则（写之前读）

| 文件 | 作用 |
|---|---|
| [rules/conventions.md](./rules/conventions.md) | 证据等级、字段、命名、台账纪律 |
| [rules/checklist.md](./rules/checklist.md) | 交稿前检查（脚本查不了的语义项） |
| [rules/excluded-sources.md](./rules/excluded-sources.md) | **来源黑名单（禁读/禁引）**，采/引前必查 |
| [rules/source-types.md](./rules/source-types.md) | 素材类型与证据天花板 |
| [rules/topic-research-protocol.md](./rules/topic-research-protocol.md) | 派与子主题怎么长、frontier 怎么用 |
| [rules/loading.md](./rules/loading.md) | 按任务加载（渐进披露）与阅读路径 |

## deliverables/ — 交付物治理

| 文件 | 作用 |
|---|---|
| [deliverables/scope.md](./deliverables/scope.md) | **交付物定位总索引**（五份的定性/边界/共用规矩；每份权威在它自己的 `SCOPE.md`） |
| [deliverables/quality.md](./deliverables/quality.md) | 质量评分卡（12 维 + 5 门槛 + 抽样协议） |

## status/ — 状态与台账（"现在到哪了"）

| 文件 | 作用 |
|---|---|
| [status/state.md](./status/state.md) | **当前计数、阻塞、最后自检**（计数唯一权威） |
| [status/state-log.md](./status/state-log.md) | 历史日志（快照，不是现行计数） |
| [status/term-baseline.md](./status/term-baseline.md) | 术语差异表（ADR 0011） |
| [status/models.md](./status/models.md) | 可用模型与本地约束（不装本地模型） |

## templates/ — 模板

| 文件 | 作用 |
|---|---|
| [templates/note-template.md](./templates/note-template.md) | 主题笔记模板 |
| [templates/subtopic-template/](./templates/subtopic-template/README.md) | 子主题四件套模板 |

## tools/ — 只读自检

| 文件 | 作用 |
|---|---|
| [tools/check_repo.py](./tools/check_repo.py) | 链接/锚点/枚举/ID/清单/计数/交付物 SCOPE 自检；见 [ADR 0005](../adr/0005-repo-self-check.md) |

## audits/ · archive/ — 历史（不要当现行规则）

- [audits/](./audits/)：准入/术语/指令层审计快照（如 [来源清除](./audits/2026-11-11-source-purge.md)）。tombstone 在这里。
- [archive/2026-11/](./archive/2026-11/README.md)：已完成的计划、质量报告、digest/card 审计、开源消化计划/吸收矩阵；均标 `status: superseded`，只用于追溯"当时怎么判的"。

## 一条规则

meta 只放**现行规则、模板、状态与台账**；一次性的计划/审计/报告完成后移入 `audits/` 或 `archive/<YYYY-MM>/` 并在本页登记。**不要把 meta 变成第二个内容层。**
