---
status: draft
updated: 2026-11-13
---

# meta/：治理层入口与索引

> **这是什么**：`meta/` 放**规则、流程、模板、状态、计划与自检工具**，不放内容判断（判断去 `topics/`，成品去 `deliverables/`）。
> **单一权威原则**：本页只做门牌与索引，不复述任何规则条文。最高约束在 [CHARTER](../CHARTER.md)，Agent 路由在 [AGENTS](../AGENTS.md)，字段/枚举在 [schema](./schema.md)。冲突时：**CHARTER > schema / information-flow > AGENTS > 各层 README**。
> 现行工作区只读 `schema.md`、`rules/`、`workflow/`、`deliverables/`、`templates/`、`status/`、`plans/`、`tools/`；`audits/` 与 `archive/` 是历史快照，**不作现行规则**。

## 30 秒：你要干什么，去哪里

| 你要做的事 | 去 | 代表性文件 |
|---|---|---|
| 查机器字段 / 枚举 / 证据阶梯 / 编号 | 根目录 | [schema.md](./schema.md) |
| 对齐写作口径 / 干货五问 / 黑名单 / 信息流 / 复核周期 | [rules/](./rules/conventions.md) | [conventions](./rules/conventions.md) · [information-flow](./rules/information-flow.md) · [excluded-sources](./rules/excluded-sources.md) · [source-types](./rules/source-types.md) · [staleness](./rules/staleness.md) |
| 按任务加载 / 交稿检查 / 子主题协议 / 扩展与并发 | [workflow/](./workflow/loading.md) | [loading](./workflow/loading.md) · [checklist](./workflow/checklist.md) · [topic-research-protocol](./workflow/topic-research-protocol.md) · [extension-points](./workflow/extension-points.md) · [working-agreements](./workflow/working-agreements.md) |
| 改/建交付物的定位与评分 | [deliverables/](./deliverables/scope.md) | [scope](./deliverables/scope.md)（总索引，具体在各份 `SCOPE.md`）· [quality](./deliverables/quality.md)（评分卡） |
| 看现在到哪了（唯一权威计数 / 目标 / 债务） | [status/](./status/state.md) | [state](./status/state.md) · [state-log](./status/state-log.md) · [term-baseline](./status/term-baseline.md) · [models](./status/models.md) |
| 看现行推进计划（`plan_status: active` ≤ 1） | [plans/](./plans/README.md) | [plans/README](./plans/README.md)（非计划的冷读/评分底稿放 [deliverables/_workpapers/](../deliverables/_workpapers/README.md)） |
| 拿模板开新页（来源卡 / digest / 主题 / 子主题） | [templates/](./templates/src/paper-card.md) | [templates/src/](./templates/src/paper-card.md) · [templates/topics/](./templates/topics/note-template.md) |
| 跑只读自检 | [tools/](./tools/README.md) | `python3 meta/tools/check_repo.py`（见 [tools/README](./tools/README.md)） |
| 查准入清除留痕 / 历史计划冷库 | [audits/](./audits/2026-11-11-source-purge.md) · [archive/](./archive/2026-11/README.md) | 准入审计快照、已归档计划（**不作现行规则**） |

## 完整文件索引

### 根目录
- [schema.md](./schema.md)：全仓 frontmatter 字段、枚举、证据阶梯、阅读深度、编号前缀与校验规则的唯一权威。

### rules/ — 静态口径与红线（写之前对齐）
- [rules/conventions.md](./rules/conventions.md)：写作约定、干货三本质与五问、长期质量三测试、引用与台账纪律（字段定义以 `schema.md` 为准）。
- [rules/information-flow.md](./rules/information-flow.md)：`src/` / `topics/` / `deliverables/` 三层读者、文体、层间接口。
- [rules/excluded-sources.md](./rules/excluded-sources.md)：**来源黑名单（禁读/禁引）**，采/引前必查。
- [rules/source-types.md](./rules/source-types.md)：素材类型与证据天花板。
- [rules/staleness.md](./rules/staleness.md)：6 个月重审、观察期转正与过期退场规则。

### workflow/ — 动态流程与检查（按顺序做）
- [workflow/loading.md](./workflow/loading.md)：渐进披露、15 分钟/接手路径、按任务加载与反向倒查。
- [workflow/checklist.md](./workflow/checklist.md)：交稿前人工语义检查。
- [workflow/topic-research-protocol.md](./workflow/topic-research-protocol.md)：派与子主题生长、frontier 与 `runs/` 协议。
- [workflow/extension-points.md](./workflow/extension-points.md)：往哪里加东西不用改结构 + 同步矩阵。
- [workflow/working-agreements.md](./workflow/working-agreements.md)：多 Agent 并发写、交接与提交门禁。

### deliverables/ — 交付物治理
- [deliverables/scope.md](./deliverables/scope.md)：四份交付物定位总索引与共用红线（每份权威在自己的 `SCOPE.md`）。
- [deliverables/quality.md](./deliverables/quality.md)：质量评分卡（12 维 + 5 门槛 + 抽样协议）。

### templates/ — 全仓模板唯一家
- `templates/src/`：[paper-card](./templates/src/paper-card.md) · [paper-digest](./templates/src/paper-digest.md) · [material-card](./templates/src/material-card.md) · [open-source-card](./templates/src/open-source-card.md) · [open-source-digest](./templates/src/open-source-digest.md) · [open-source-code-map](./templates/src/open-source-code-map.md)
- `templates/topics/`：[note-template](./templates/topics/note-template.md) · [subtopic-template](./templates/topics/subtopic-template/README.md)

### status/ · plans/ · tools/ · audits/ · archive/
- [status/state.md](./status/state.md)：**当前计数、目标、已知债务、最后自检**（唯一权威）；[state-log](./status/state-log.md)（历史日志）；[term-baseline](./status/term-baseline.md)；[models](./status/models.md)。
- [plans/README.md](./plans/README.md)：有 `plan_status` 的推进计划（`active` ≤ 1）。
- [tools/README.md](./tools/README.md) · [tools/check_repo.py](./tools/check_repo.py)：只读自检（[ADR 0005](../adr/0005-repo-self-check.md)）。
- [audits/](./audits/2026-11-11-source-purge.md)：准入/术语/指令层审计快照（含不可逆删除 tombstone）。
- [archive/2026-11/](./archive/2026-11/README.md)：已完结的计划（`plans/`）、全审与历史报告；均不作现行规则。

## 维护约束（防止本文件膨胀）

- 本文件**只指路、不复述规则条文**；与 `CHARTER` / `schema.md` / `rules/` / `workflow/` 冲突时，改本文件，不改规则。
- 子目录增删时同步更新上表；不要把 `meta/` 变成第二个内容判断层。
