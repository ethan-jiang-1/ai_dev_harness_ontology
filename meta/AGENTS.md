# meta/ —— 治理层入口（agent 先读这一页）

> **这是什么**：`meta/` 放的是**规则本身**，不是内容判断。你在这里改的是"以后怎么写"，不是"某条判断是什么"。
> **本文件只做门牌与指路，不新增规则**：所有规则的唯一出处是 [CHARTER](../CHARTER.md)（准入）、根 [AGENTS](../AGENTS.md)（路由/修复回路）、[rules/](./rules/)（字段/证据/检查）。本文件若与它们冲突，以它们为准。
> **完整文件索引**见 [README](./README.md)。

## 30 秒：你要干什么，去哪个子目录

| 你要做的事 | 去 | 代表性文件 |
|---|---|---|
| 写东西前对齐字段 / 证据等级 / 命名 | [rules/](./rules/) | conventions.md |
| 交稿前自检 | [rules/](./rules/) | checklist.md |
| 判断一个源能不能进来 / 能不能引 | [rules/](./rules/) | excluded-sources.md（黑名单）、source-types.md |
| 开新子主题 / 做前沿扫描 | [rules/](./rules/) | topic-research-protocol.md |
| 改/建交付物 | [deliverables/](./deliverables/) | scope.md（五份总索引）、quality.md（评分卡） |
| 看现在到哪了（计数/阻塞） | [status/](./status/) | state.md（计数唯一权威）、state-log.md |
| 拿模板开新页 | [templates/](./templates/) | note-template.md、subtopic-template/ |
| 查"当时为什么这么定" | [audits/](./audits/) · [archive/](./archive/) | 审计快照、历史计划（**不作现行规则**） |
| 跑只读自检 | [tools/](./tools/) | `python3 meta/tools/check_repo.py` |

## 三个硬约束（判据在上面的出处，这里只提醒）

1. **素材先过门**：≥2026-06-01、活跃、多主体高影响；在役标准须「现行版本 + 2026-06 后维护活动」；采/引前查黑名单 → 判据见 [CHARTER §4](../CHARTER.md#4-素材准入material-gate)。
2. **一条规则只有一个家**：改规则只改一处，别在别处抄第二份 → 见 [根 AGENTS](../AGENTS.md) 与 [ADR 0012](../adr/0012-instruction-layer-single-home.md)。
3. **这里不放内容判断**：判断去 `topics/`，成品去 `deliverables/`，一次性报告去 `audits/` 或 `archive/`。

## 维护约束（防止本文件变成第二个路由器）

- 本文件**不得**复述任何规则条文；只能指路。发现它和规则文件不一致，改它，不改规则。
- 新增规则 → 写进 `rules/` 或 CHARTER，不在本文件加。
- 子目录增删 → 改本文件的表 **和** [README](./README.md) 的索引，两处各改一次。
