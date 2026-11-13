---
status: draft
updated: 2026-11-13
---

# 仓库状态戳

> 这是全仓**权威的当前计数**。README 只保留结构性摘要，checklist 不再抄数；数字冲突时以本页为准。
> 每次结构性提交前更新；自检命令见文末。历史日志见 [state-log](./state-log.md)。

## 当前状态（2026-11-13）

| 项 | 值 |
|---|---|
| 宪章 | [CHARTER](../../CHARTER.md)：研究档案，不做实施；交付物是文档 |
| 阶段 | 内部研究档案；不做对外客户交付，因此不设客户资产/签核前置 |
| 论文 | 12 个目录（8 `admitted` + 4 `admitted (probation)`）；18 篇已按 [准入审计](../audits/2026-11-11-source-purge.md) 移出 |
| 开源 | 8 个项目（trustgraph / semantica / ontop / open-ontologies + OPA / Qlever + Great Expectations + OpenLineage），已 pin commit、已消化 |
| 材料卡 | 17 张（1 张 HN + 10 张在役标准卡 + 5 张生产证据卡〔10 落地现状用〕 + 1 张 Google OKF） |
| 主题 | 6 派 + 23 个子主题 + 00-harness 七部件 + 6 时刻 + 1 条形态轴 |
| 结论 | 32 条 E：17 已核原文 + 2 已核代码 + 4 推测 + **9 已撤回**（E-25 由已核降推测）；3 条 Q；4 条 C |
| 局部判断 | 86 条 L（01:19 / 02:10 / 03:16 / 04:7 / 05:10 / 06:24）；其中 **28 条 withdrawn**（源移出） |
| 硬对象 | 94 注册（**20 已随源撤回**；现存 74：H3 33 / H2 41）；明细见 [objects](../../topics/objects.md) 变更记录 |
| 证据配比（12 篇 + 8 开源） | 3 execution-test / 13 mechanism-only / 4 harness-evidence / 0 boundary-ruler |
| 执行形态（20 源：12 论文 + 8 开源） | engine 3 / compiled 5 / context 1 / label 1 / none 10 |
| 交付物 | 4 个子目录 + 共用入口 [START](../../deliverables/START.md)：01-capability-status / 02-engineering-playbook / 03-mechanism-reference（一组：判断/做法/机制，谈你的项目）+ **10-production-landscape**（另一组：实证，谈世界）；02 为 README 门厅 + 13 条 recipe（R0–R12）+ 账本/评测/成本/上线/领域 + 附录；03 为四层结构（入口 + 6 位置卡 + 谱外页 + 3 横切页 + 证据台账/边界/缺口）；10 为落地现状·实证（5 条 admitted/probation 生产证据 + 1 张 OKF admitted 格式卡 + 3 家农商行客户自述 signal〔江西 <50 万上限、江南 3 人×12 月〕 + 小红书 DIBP（B） + NHS FDP（signal） + 五类价锚点；五平台外部采用与失败率已判“窗口内不存在”；质量自评 88.8/100；仍缺同一买方建设+维护配对与项目级 postmortem）。**原 04 合成走查已退役（ADR 0015）**；另有 `_workpapers/` 工作底稿（非交付），推进计划已收归 [meta/plans/](../plans/README.md)；原 7 章书稿计划已废弃，没有独立 handbook |
| 模型 | 不本地安装；Yovole 两个：`DeepSeek-V4-Flash` / `qwen3.8-27b`；直连超时；harness override 可调用，但 subagent 会调用工具，**不用于实验**，只做第二意见；见 [models](./models.md) |
| 最后自检 | 2026-11-13，`python3 meta/tools/check_repo.py`：0 errors / 0 warnings（534 个 md；E=32，Q=3，C=4，L=86；12 论文 / 8 开源 / 17 材料卡） |

<a id="当前目标下一步做什么"></a>
## 当前目标（下一步做什么）

> **「现在最该做什么」只看这一节**；README / plans / 各派 frontier 都不另立优先级。拆成**外部守门（A 轨）**与**仓内立即可推（B 轨）**，避免 fresh agent 在等待外部论文期间空转。做完一项就改这一节，并记 [state-log](./state-log.md)。

| 轨道 | # | 目标 | 为什么是它 | 关闭条件 |
|---|---|---|---|---|
| **A 轨（外部守门）** | 1 | **P0 四篇 probation 补第二独立信号**（GGC / Agents / N&D / CASEL） | 只靠 I2 一条信号，2027-05-11 前补不到就移出，会带走 E-12/E-15/E-18 等锚 | 每篇卡上 `impact_evidence` 出现第二个独立信号（≥1 个 I1–I3）；如命中先查黑名单 |
| **B 轨（仓内可推）** | 2 | **补 `04-state` / `06-measure` 开源执行样本 + `read-path` 第二独立实现** | 不等新论文即可推进：目前仅 trustgraph 1 个 `read-path` 实现（`ontology-rag-firewall`/`sparql-guard` 仍为候选），04/06 缺代码级本体执行样本 | 在 [选择标准](../../src/open-source/README.md) 五门下入库可 pin commit 的代码读码（或明确记录本轮候选排除结论） |
| **B 轨（结构收口）** | 3 | **完成 `02/03` 信息架构对齐（见 [IA 整改计划](../plans/2026-11-12-deliverable-ia-plan.md)）+ D4（02 R3 extractor 规格）** | 把 02/03 与 10 一样收紧读径字数与可检入口，并补齐 R3 唯一缺的下游消费接口契约 | 02/03 对齐评分过线，R3 写出输入/输出契约 + offset 校验 + 降级路径 |

> **方法论开放墙（M1/M2）**：同本体跨位置对照、覆盖率实测是全仓最大的方法论缺口（决定 `03` 能否从分类走向效应量）。若外部有 admitted 新源立即收入；若要通过仓外实验验证升「已证」，须经用户明确同意并在仓库外运行、以 `EXP-xxx` 回链（[CHARTER](../../CHARTER.md) 禁止在仓内写代码/建实验）。
>
> **10 四期已收口到 [D1](#已知债务别当成已完成)**：二轮补搜后公开证据能拿的都拿了（五类价 + 江西 <50 万/江南 36 人月两条客户自述、3 家农商行 signal、小红书 B、NHS「宣称 vs 使用」、7 例采购流标、五平台 0 客户、无项目级 postmortem），剩下是"等外部材料"，不再占目标位；出现材料即回填。
>
> **收东西的口径**：只收「能长期保障质量」的做法（可重复 / 自带检测 / 抗腐化），见 [conventions 三条测试](../rules/conventions.md#只收能长期保障质量的做法不是一次性技巧)。一次性技巧记候选，不升 E。

## 已知债务（别当成已完成）

> 这些是**已识别但未做完**的事。每条写清"缺什么、谁能关、判据"，避免下一轮误以为已完成。

| # | 债务 | 现状 | 关闭判据 |
|---|---|---|---|
| D1 | **10 仍无“四项齐全”A 类** | 5 条 admitted/probation + 3 家农商行 signal + 小红书 B + NHS signal；成本有五类价，**2026-11-12 补到两条客户自述投入**（江西 <50 万上限、江南 3 人×12 月），仍无同一买方建设+维护配对、无人月单价、无回收期；失败只有运行中的坑 + NHS「宣称 vs 使用」，无项目级 postmortem；五平台客户侧 0（已判定“窗口内不存在”，见 [frontier](../../topics/06-measure/feasibility/frontier.md) 与 05 的 90.3） | 出现任一条：带人月的审计复盘、项目级失败 postmortem、五平台任一客户署名复盘；写进 05 且可追到卡 |
| D2 | **坏样本清单无实测入口** | 原 04 fixture 的 8 条未跑坏样本 + clean FP 随 fixture 退役（ADR 0015）；清单留在 [consumability §4](../../topics/05-produce/representation/consumability.md)，是设计检查表、不是实测 | 不关：需要新的可跑样例（新份立项或仓库外 EXP），不在退役文档里补跑 |
| D4 | **02 R3 缺 extractor 规格** | 只有"span 对不上就丢"；谁抽 claim、怎么保 offset 未定 | 写出 extractor 的输入/输出契约 + offset 校验 + 抽不出的降级路径 |
| D5 | **03 施工细节未补（有意为之）** | T1–T5、Layer B、τ 无定义 | **不关**：需先有新的 admitted 源；现在补=把 withdrawn 装成手册 |
| D6 | **9 条 E 无做法（全是 withdrawn）** | 已撤回行不需要做法 | 不关；重新 admitted 时一并补 |
| D7 | **P0 四篇 probation 缺第二信号** | GGC/Agents/N&D/CASEL 各只有 I2 | 2027-05-11 前每篇卡上出现第二个 I1–I3 信号 |

## 当前边界（不是阻塞）

1. **无外部资产请求**：D0/试点线已于 2026-11-09 删除；不再需要具名域、日志、题库、人或单价。
2. **独立复现仍是空缺**：不影响 desk research；若要升「已证」，需要独立复现，但不在本仓库做；不设实验目录，也不再用模型做实验被试。
3. **独立人类抽检**：只在对外交付时需要；内部研究不阻塞。
4. **素材准入重置（2026-11-11）+ 叙述页对账（2026-11-12）**：18 篇论文 + 3 个旧网页材料已移出；9 条 E 撤回、E-21 改写、E-19 降为推测。**topics 对账：判断层（README/claims/mechanism）已完成；证据层（findings 索引）2026-11-12 补对账，8 处旧「已核」已声明作废，派 README 补撤源横幅**；admitted 源（CASTON/FIRME/CAI/CASEL/N&D/SLB/Agents/E-20 等）内容保留。交付物正文经扫描**无撤回源当活证据**。剩余长尾：个别历史 run 日志（`runs/`）为 pre-purge 快照，不作现役判断。
5. **开源执行线**：4 个项目已在 pin commit 上完成只读代码核对；矩阵进 [execution-forms](../../topics/execution-forms.md#代码级核对2026-11-09)；`read-path` 已入库仍只有 1 个实现（外部扫描另见 sparql-guard 候选，未入库），需第二实现 + harness 调用点才能决定是否升第七时刻。

## 最近改动

> 仅保留最新 3 条里程碑摘要；全量历史快照见 [state-log](./state-log.md)（其中 `04` 已退役、`05` 已按 [ADR 0015](../../adr/0015-retire-04-and-renumber-05-to-10.md) 改名为 `10-production-landscape`）。

- **2026-11-13 `meta/` 治理结构与工作底稿对齐（[ADR 0016](../../adr/0016-unify-meta-structure.md)）**：合并 `meta/AGENTS.md` 到 [meta/README.md](../README.md)；抽离 [meta/schema.md](../schema.md) 为全仓字段/枚举唯一权威；拆分 `rules/`（静态口径，补 `information-flow.md`、`staleness.md`）与 `workflow/`（动态流程，移入 `loading`/`checklist`/`topic-research-protocol`，补 `extension-points.md`、`working-agreements.md`）；模板全收归 `meta/templates/{src,topics}/`；撤销 `deliverables/_plans/`，推进计划归 [meta/plans/](../plans/README.md) 与 `archive/2026-11/plans/`，冷读/评分底稿留 `deliverables/_workpapers/`；补 `meta/tools/README.md` 并强化 `check_repo` 对 `plan_status` 唯一性检验。
- **2026-11-13 fresh-agent 防跑偏校准与闸门加固**：修正 `THESIS` / `01` / `02` / `03/compilation` / `05-produce` / `06/feasibility` / `01/09-data` 中残余的撤回源旧「已核」标号、死 `src/` 路径与退役 `04` / 旧计数错标；补全 `iso-iec-21838`、`omg-commons` 的 `provenance_type`；将 `check_repo` 升级覆盖 `10-*` `SCOPE`、动态比对 `结论` 计数、`src/web` 门禁字段、黑名单防复入、死 `src/` 路径与未标注撤回 `E-xx`；`当前目标` 改为「外部守门 + 仓内可推」双轨。详见 [state-log](./state-log.md#2026-11-13-fresh-agent-防跑偏校准与闸门加固)。
- **2026-11-12 交付物重排（ADR 0015）**：04 合成走查退役（判据打捞至 `policy F4`、`output-validation §2.5`、`02 附录 D §10`），删除 fixture 与 35 个文件；05 改名 **10-production-landscape**，交付物收拢为 `01 / 02 / 03 / 10` 四份。

## 怎么刷新

```bash
python3 meta/tools/check_repo.py
```

- 通过：更新本页的“最后自检”日期与计数；一次性的改动记录写 [state-log](./state-log.md)，不写回本页。
- 失败：先修，不提交。
- 本文的计数是**手工维护的唯一副本**；`check_repo` 会比对“最后自检”里的文件数，脚本能数的优先信脚本。
