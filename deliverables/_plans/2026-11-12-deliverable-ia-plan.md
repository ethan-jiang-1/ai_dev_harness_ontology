---
status: draft
type: ia-plan
updated: 2026-11-12
scope: deliverables 01–04 的 README 索引化、目录/文件编号、阅读体验整改
---

# 交付物 IA 整改计划：索引、序号与阅读体验

> **一句话**：把四份交付物从「README 当第一章 + 文件树无序 + 故事化叙述」改成「README 当索引 + 章号进文件名 + 第三人称技术叙述」，并保证链接在任何查看器里都有兜底路径。

## 1. 三个诉求与根因

| 诉求 | 现象 | 根因 |
|---|---|---|
| **README 应该是索引** | 01 README 同时承担案例、三条判断、A/B/C/D 表、阅读路径、数据表 | 违反仓库自己的契约：「README 只做索引；不把长文塞回 README」（[deliverables/README.md:143](../README.md)） |
| **目录没有顺序** | 文件树按字母排：acceptance、boundaries、canonical…；读者不知道先读哪个 | 章号只存在于正文标题（「§4 边界」），没有进入文件名；目录按「类型」而非「阅读顺序」命名 |
| **阅读体验差** | 故事化第二人称（「你带 3 个人」「先看一个决定」）；内码前置；相对链接在部分查看器里点不开 | 把 explanation/tutorial 的语气混进 reference；链接依赖查看器的 base path，没有纯文本兜底 |

## 2. 目标（Definition of Done）

### 2.1 README（四份统一）

- ≤ 60 行，只含六块：读者卡、状态、**30 秒结论**（≤5 条，每条一句 + 链接）、**目录**（用途 / 入口 / 路径列）、**阅读顺序**、**维护**。
- 不出现：完整案例、完整判断论证、A/B/C/D 全表、数据表清单、多段内码说明。
- 首屏 10 秒内能回答：这是什么、给谁、先读哪、去哪查。

### 2.2 正文第 0 章

- 新增 `<份>/02-sections/00-overview.md`：案例框、三条判断、A/B/C/D 表、第一个动作。
- 旧锚点（如 `#0-一页结论`、`#6-如果只做一件事`）用显式 `<a id="...">` 保留，避免入链断裂。

### 2.3 命名（B 方案：章号对齐 + 两位数字）

- `02-sections/`：正文（第 2–5 章）；`01-GUIDE`、`00-overview` 在首位。
- `03-…/`：主体（capabilities / recipes / positions / body）。
- `04-…/`：支撑（operations / across-positions / evidence）。
- `05-…/`：附录（appendices / example）。
- `09-…/`：工作底稿、长版历史附录（data / appendix）。
- `90+`：查阅页（glossary / canonical / k-ladder / templates / reference / transfer / placement / reader-checks…）。
- **README 不编号**；`START.md` 不动。
- 两位数字：避免 `10-` 排到 `2-` 前面；与仓库既有 `01-constraint`、`01-capability-status` 一致。

### 2.4 链接

- 正文用**相对链接**；目录表加「路径」列，值为仓库相对路径（纯文本，`deliverables/…`）。
- 关键首现链接后附 `（路径：…）`，例：链接文字「K0–K4 来源说明」+ 目标 `02-sections/92-k-ladder.md` + 括注 `路径：deliverables/01-capability-status/02-sections/92-k-ladder.md`。
- 不用根绝对路径（`/deliverables/...`）；不改 README/START 文件名。
- 验收：`check_repo` 0 坏链/坏锚；另跑一次「所有 md 内相对链接目标存在」的脚本。

### 2.5 语气

- 默认**第三人称陈述**：「01 的判断是…」「案例：某工厂…」。
- 案例压缩为 `> 案例：…` 事实框（4–6 行，带条件与数字），不写「先看一个决定/你带 3 个人」。
- 步骤可用第二人称，但只限操作句（「先量 X，再量 Y」），不用于场景设定。
- 保留 E/W 编号与限定；不因改语气删条件。

### 2.6 冷读

- 每份改完做一次代理冷读：10 分钟内能说出「这是什么、先读哪、下一步」。
- 真人冷读仍是人工步骤，不阻塞。

## 3. 命名映射

### 3.1 01（已完成，commit `95ca558`）

| 旧 | 新 |
|---|---|
| `GUIDE.md` | `02-sections/01-GUIDE.md` |
| `sections/map.md` | `02-sections/02-map.md` |
| `sections/boundaries.md` | `02-sections/04-boundaries.md` |
| `sections/acceptance.md` | `02-sections/05-acceptance.md` |
| `sections/decision-record.md` | `02-sections/09-decision-record.md` |
| `sections/glossary.md` | `02-sections/90-glossary.md` |
| `sections/canonical.md` | `02-sections/91-canonical.md` |
| `sections/k-ladder.md` | `02-sections/92-k-ladder.md` |
| `sections/templates.md` | `02-sections/93-templates.md` |
| `capabilities/` | `03-capabilities/` |
| `data/` | `09-data/` |
| — | `02-sections/00-overview.md`（新） |

### 3.2 02

| 旧 | 新 |
|---|---|
| `GUIDE.md` | `02-sections/01-GUIDE.md` |
| `sections/map.md` | `02-sections/02-map.md` |
| `sections/approach.md` | `02-sections/03-approach.md` |
| `sections/boundaries.md` | `02-sections/04-boundaries.md` |
| `sections/acceptance.md` | `02-sections/05-acceptance.md` |
| `sections/glossary.md` | `02-sections/90-glossary.md` |
| `sections/canonical.md` | `02-sections/91-canonical.md` |
| `recipes/README.md` | `03-recipes/README.md`（不编号） |
| `recipes/readiness.md` | `03-recipes/00-readiness.md` |
| `recipes/knowledge.md` | `03-recipes/01-knowledge.md` |
| `recipes/judgment.md` | `03-recipes/04-judgment.md` |
| `recipes/constraint.md` | `03-recipes/06-constraint.md` |
| `recipes/state.md` | `03-recipes/07-state.md` |
| `recipes/offline-and-obda.md` | `03-recipes/10-offline-and-obda.md` |
| `recipes/regulated.md` | `03-recipes/12-regulated.md` |
| `operations/*` | `04-operations/01-ledger` … `05-domains` |
| `appendices/*` | `05-appendices/01-interfaces` … `04-artifact-pack` |

### 3.3 03

| 旧 | 新 |
|---|---|
| `GUIDE.md` | `02-sections/01-GUIDE.md` |
| `sections/map.md` | `02-sections/02-map.md` |
| `sections/boundaries.md` | `02-sections/04-boundaries.md` |
| `sections/acceptance.md` | `02-sections/05-acceptance.md` |
| `sections/glossary.md` | `02-sections/90-glossary.md` |
| `sections/placement.md` | `02-sections/91-placement.md` |
| `sections/reader-checks.md` | `02-sections/92-reader-checks.md` |
| `sections/templates.md` | `02-sections/93-templates.md` |
| `sections/relations.md` | `02-sections/94-relations.md` |
| `sections/claim-walkthrough.md` | `02-sections/95-claim-walkthrough.md` |
| `positions/README.md` | `03-positions/README.md` |
| `positions/context.md` … `outside.md` | `03-positions/01-context.md` … `07-outside.md` |
| `across-positions/*` | `04-across-positions/01-coverage` … `03-measurement` |
| `evidence/*` | `05-evidence/01-ledger` … `03-gaps` |
| `appendix-constraint-spectrum.md` | `05-appendix-constraint-spectrum.md` |

### 3.4 04

| 旧 | 新 |
|---|---|
| `GUIDE.md` | `02-sections/01-GUIDE.md` |
| `sections/map.md` | `02-sections/02-map.md` |
| `sections/boundaries.md` | `02-sections/04-boundaries.md` |
| `sections/acceptance.md` | `02-sections/05-acceptance.md` |
| `sections/decision.md` | `02-sections/06-decision.md` |
| `sections/glossary.md` | `02-sections/90-glossary.md` |
| `sections/reference.md` | `02-sections/91-reference.md` |
| `sections/transfer.md` | `02-sections/92-transfer.md` |
| `sections/templates.md` | `02-sections/93-templates.md` |
| `sections/worked-example.md` | `02-sections/94-worked-example.md` |
| `sections/journey.md` | `02-sections/95-journey.md` |
| `sections/label-source.md` | `02-sections/96-label-source.md` |
| `sections/relations.md` | `02-sections/97-relations.md` |
| `body/build.md` | `03-body/01-build.md` |
| `body/consume.md` | `03-body/02-consume.md` |
| `body/govern.md` | `03-body/03-govern.md` |
| `evidence/*` | `04-evidence/01-ledger` … `02-sources` |
| `example/*` | `05-example/`（README 不编号，JSON/TTL 原名） |

## 4. README 模板

```markdown
# <份号> · <一句话定位>

> 读者：… ｜ 回答：… ｜ 不回答：…（去 0x）
> 状态：draft ｜ 计数：…（详见 91-canonical）
> 证据重置：…（W 表见 91-canonical §…）

## 30 秒结论
1. …（一句）→ 详见 [overview §…](02-sections/00-overview.md#…)
2. …
3. …

## 目录
| 你要 | 读 | 路径 |
|---|---|---|
| … | [00-overview](02-sections/00-overview.md) | `deliverables/…` |

## 阅读顺序
| 时间 | 读什么 |

## 维护
- 计数以 91-canonical 为准；改判定先改 02-map §2.1。
```

## 5. 执行顺序（每批一个 commit）

| 批 | 内容 | 验收 |
|---|---|---|
| **P0（已完成）** | 01：README 索引化 + 00-overview + 重命名 + 链接重写 | `check_repo` 通过（446 md）；提交 `95ca558` |
| **P1** | 02：同 P0 + 语气改写 + 路径列 | 0 坏链；代理冷读 ≥80 可用性 |
| **P2** | 03：同 P1（位置卡/横切页按序编号） | 同上 |
| **P3** | 04：同 P1（body 按 1/2/3；example 不编号） | 同上 |
| **P4** | 全局：`deliverables/README.md` 入口表更新；`_plans/README` 索引；状态页 | `check_repo`；四份 README ≤60 行 |

每批步骤固定：

1. `git mv` 目录/文件（保留 git 历史）。
2. 链接重写脚本：按「旧路径→新路径」映射，从**旧位置**解析相对链接，重算**新位置**的相对路径；锚点不变。
3. 人工补：目录表「路径」列、首现路径注、README/overview 改写。
4. `check_repo` + 自定义链接脚本 + 坏链清零。
5. 代理冷读 10 分钟；记录判词。
6. `git commit`。

## 6. 验收清单

- [ ] 四份 README ≤60 行，只含六块；无案例/无完整判断/无数据表清单。
- [ ] 每份有 `02-sections/00-overview.md`，旧锚点保留。
- [ ] 文件树按 B 方案排序：`00-` → `02-` → `03-` → `04-` → `05-` → `09-` → `90+`。
- [ ] `check_repo` 0 坏链/坏锚；自定义链接脚本 0 缺失。
- [ ] 目录表每行有「路径」列；关键首现链接带路径注。
- [ ] 语气：无「你带…」「先看一个…」开场；案例为第三人称事实框。
- [ ] 代理冷读：能说出「这是什么 / 先读哪 / 下一步」。

## 7. 风险与回滚

| 风险 | 处置 |
|---|---|
| 重命名导致链接断裂 | 先 `git mv`，再跑映射脚本，再 `check_repo`；每批独立 commit，可单独 revert |
| README 信息量下降 | 全文进 `00-overview`；README 保留 3 条结论 + 链接 |
| 评分波动（B1/C1/C2 先降后升） | 以冷读和「读者 10 分钟能做什么」为准，不追单次分数 |
| 目录号与章号重复（`04-boundaries` vs `04-operations`） | 不同层级，允许；在计划与 README 里写明规则 |
| 查看器仍不解析链接 | 路径列 + 路径注兜底；不改文件名去迁就查看器 |

## 8. 不做

- 不重写论证、不改 E/L、不动 `topics/` 与 `src/`。
- 不把章节平铺到根目录。
- 不重命名 `README.md` / `START.md`。
- 不做静态站点、不引入构建工具（仓库是研究档案，不是软件项目）。

> 本计划是工作底稿，不是交付正文；不构成 E/L。

---

## 9. 执行记录

| 批 | 状态 | 提交 | 结果 |
|---|---|---|---|
| P0 01 | 完成 | `95ca558` | README 索引化 + 00-overview + 02/03/09 编号；`check_repo` 通过 |
| P1 02 | 完成 | `ad14c08` | 02-sections/03-recipes/04-operations/05-appendices；README 56 行；`check_repo` 通过（448 md） |
| P2 03 | 完成 | `5927a9b` | 02-sections/03-positions/04-across-positions/05-evidence/09-appendix；README 56 行；`check_repo` 通过（449 md） |
| P3 04 | 完成 | `136db9a` | 02-sections/03-body/04-evidence/05-example；README 61 行；`check_repo` 通过（450 md） |
| P4 全局 | 完成 | `02ef8ac` + 本批 | 入口表/结构表更新；README 表头改「用途」；01-GUIDE 重编号；锚点改名；10 分钟路径补下一步；路径列说明修正；`check_repo` 通过（450 md） |

> 每批都重写了旧路径链接（脚本从旧位置解析、按新位置重算），锚点未变；`check_repo` 0 坏链/坏锚。
