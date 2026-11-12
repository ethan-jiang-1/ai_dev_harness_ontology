---
status: draft
updated: 2026-11-12
---

# 仓库状态戳

> 这是全仓**权威的当前计数**。README 只保留结构性摘要，checklist 不再抄数；数字冲突时以本页为准。
> 每次结构性提交前更新；自检命令见文末。历史日志见 [state-log](./state-log.md)。

## 当前状态（2026-11-12）

| 项 | 值 |
|---|---|
| 宪章 | [CHARTER](../../CHARTER.md)：研究档案，不做实施；交付物是文档 |
| 阶段 | 内部研究档案；不做对外客户交付，因此不设客户资产/签核前置 |
| 论文 | 10 个目录（6 `admitted` + 4 `admitted (probation)`）；18 篇已按 [准入审计](../audits/2026-11-11-source-purge.md) 移出 |
| 开源 | 8 个项目（trustgraph / semantica / ontop / open-ontologies + OPA / Qlever + Great Expectations + OpenLineage），已 pin commit、已消化 |
| 材料卡 | 17 张（1 张 HN + 10 张在役标准卡 + 5 张 05 生产证据卡 + 1 张 Google OKF） |
| 主题 | 6 派 + 23 个子主题 + 00-harness 七部件 + 6 时刻 + 1 条形态轴 |
| 结论 | 32 条 E：17 已核原文 + 2 已核代码 + 4 推测 + **9 已撤回**（E-25 由已核降推测）；3 条 Q；4 条 C |
| 局部判断 | 85 条 L（01:19 / 02:10 / 03:16 / 04:7 / 05:10 / 06:23）；其中 **28 条 withdrawn**（源移出） |
| 硬对象 | 94 注册（**20 已随源撤回**；现存 74：H3 33 / H2 41）；明细见 [objects](../../topics/objects.md) 变更记录 |
| 证据配比（10 篇 + 8 开源） | 3 execution-test / 11 mechanism-only / 4 harness-evidence / 0 boundary-ruler |
| 执行形态（18 源：10 论文 + 8 开源） | engine 3 / compiled 3 / context 1 / label 1 / none 10 |
| 交付物 | 5 个子目录 + 共用入口 [START](../../deliverables/START.md)：01-capability-status / 02-engineering-playbook / 03-mechanism-reference / 04-worked-example；02 为 README 门厅 + 13 条 recipe（R0–R12）+ 账本/评测/成本/上线/领域 + 附录；03 为四层结构（入口 + 6 位置卡 + 谱外页 + 3 横切页 + 证据台账/边界/缺口）；04 为建/用/治生命周期（**合成示例**，E-21/E-22 已升）；**05-production-landscape 落地现状·实证（5 条 admitted/probation 生产证据 + 1 张 OKF admitted 格式卡 + 3 家农商行客户自述 signal + 五类价锚点；五平台外部采用与失败率已判“窗口内不存在”；质量自评 85.6/100；仍缺人月与项目级 postmortem，ADR 0014）**；另有 `_plans/` 工作底稿（非交付）；原 7 章书稿计划已废弃，没有独立 handbook |
| 模型 | 不本地安装；Yovole 两个：`DeepSeek-V4-Flash` / `qwen3.8-27b`；直连超时；harness override 可调用，但 subagent 会调用工具，**不用于实验**，只做第二意见；见 [models](./models.md) |
| 最后自检 | 2026-11-12，`python3 meta/tools/check_repo.py`：0 坏链 / 0 坏锚 / 0 未定义 ID / 枚举通过（537 个 md；E=32，Q=3，C=4，L=85；10 论文 / 8 开源 / 17 材料卡） |

<a id="当前目标下一步做什么"></a>
## 当前目标（下一步做什么）

> **「现在最该做什么」只看这一节**；README / _plans / 各派 frontier 都不另立优先级。做完一项就改这一节，并记 [state-log](./state-log.md)。

| # | 目标 | 为什么是它 | 关闭条件 |
|---|---|---|---|
| 1 | **P0 四篇 probation 补第二独立信号**（GGC / Agents / N&D / CASEL） | 只靠一条信号，2027-05-11 前补不到就移出，会带走 E-12/E-15/E-18 等锚 | 每篇卡上 `impact_evidence` 出现第二个独立信号（≥1 个 I1–I3） |
| 2 | **M1/M2 承重墙**：同本体跨位置对照、覆盖率测量 | 03 明写「没有这两项，只给分类不给效应量」；这是全仓最大的方法论缺口 | 有 admitted 源做同本体跨位置对照，或明确判定「现有文献不存在」并写进 frontier |

> 不在这张表里的事，默认不做；要做先进这张表（一次至多 3 项，按序）。
>
> **05 三期已收口到 [D1](#已知债务别当成已完成)**：公开证据能拿的都拿了（五类价锚点、3 家农商行 signal、7 例采购流标、五平台 0 客户、无项目级 postmortem），剩下三项是"等外部材料"，不再占目标位；出现材料即回填。
>
> **收东西的口径**：只收「能长期保障质量」的做法（可重复 / 自带检测 / 抗腐化），见 [conventions 三条测试](../rules/conventions.md#只收能长期保障质量的做法不是一次性技巧)。一次性技巧记候选，不升 E。

## 已知债务（别当成已完成）

> 这些是**已识别但未做完**的事。每条写清"缺什么、谁能关、判据"，避免下一轮误以为已完成。

| # | 债务 | 现状 | 关闭判据 |
|---|---|---|---|
| D1 | **05 仍无“四项齐全”A 类** | 5 条 admitted/probation + 3 家农商行 signal；成本有五类价（平台/服务/建设/维护/运行）但无人月、无同一买方建设+维护配对；失败只有运行中的坑，无项目级 postmortem；五平台客户侧 0（已判定“窗口内不存在”，见 [frontier](../../topics/06-measure/feasibility/frontier.md) 与 05 的 90.3） | 出现任一条：带人月的复盘、项目级失败 postmortem、五平台任一客户署名复盘；写进 05 且可追到卡 |
| D2 | **04 有 8 个坏样本未跑** | `bad_samples.json` 里 tested=false 共 8 条（S1–S5/S6/S9/S10） | 逐条施加 mutation 跑出 `build_report`，把 tested 改 true 并填实测值 |
| D3 | **04 clean FP 未测** | `clean_fp_set.status = 未测` | 5–10 个干净快照跑同一 shapes，报 FP 条数与分母 |
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

- **2026-11-12 04b OKF 严格化（拆层/补证/降级）**：4b 被指“硬挤进去、未走严格流程”，尤其“靠向本体”把规范边界/映射机制/采用证据混成一条路。走[修复回路](../../AGENTS.md)：逐句审计（7 P0/9 P1/5 P2，见 [provenance 审计](../audits/2026-11-12-04b-okf-provenance.md)）→ SCIMIN/SMW 论文先建卡后**复核降为 `signal` 并移出 `src/`**（承建方自述、G3 无独立信号，只进 frontier）→ 上游重写 mechanism OKF 节（两个方向 + 关系定型缺口；映射缺口分三档）、E-32 补非对称投影、新增 06-L23、frontier 收三份 C 实现 → 4b 重写 9 节（删伪阈值、Kunstenpunt/京东降 `signal`、加“没有完成迁移的案例”）。计划见 [04b strict plan](../../deliverables/_plans/2026-11-12-04b-okf-strict-plan.md)。
- **2026-11-12 05 三期（可读性收口）**：03.5/04.5 台账去掉、指向 06.1 canonical；07 加 7.5b 填好的决策卡（示例值）；README/00 加问题链主线；01 加产品名一句话 + 四条类比；06.1 加证据类型图例（观测/主张/采购记录/媒体转述/厂商材料）；90 加 90.3b 九类口径与不可比说明。自评从 77 → **85.6**（C2 仍 3：主路径约 3 万字 > 2 万字档；A1/A3/D3 仍 4：缺人月/项目级 postmortem/五平台客户）。
- **2026-11-12 05 缺口收口（二期）**：C 层一致性 7 项 + E-28/E-29/E-30 措辞修正（本体 vs 语义层配比 / 失败表述 / 窗口外源）；OKF 建 `admitted` 卡并修三处事实偏差（semantic-layer 词频、Knowledge Catalog 13 字段、京东海博 OKF 推断）；成本章从“无金额”升级为五类价锚点（£10.09M/5 年、$1.14M/年、¥49–276 万、¥178.8 万/年、$37–175/月）；补 3 家农商行 signal、7 例采购流标（供给薄）、Westpac 退出；失败率与五平台外部采用判“窗口内不存在”写入 frontier/90.3。评分见 [05 质量评估](../../deliverables/_plans/2026-11-12-05-quality-review.md)。
- **2026-11-12 05 落地现状成稿（一期）**：5 条 admitted/probation（中泰×2、Snowflake、Sigma、Netflix）+ 10+ C/B 线索；新增 E-28–E-32（平台承载 / 失败在语义层 / 公开证据不对称 / 成本拐点 / OKF 前置层）、L-18–L-22；新增 5 张源卡；05 共 11 节 + 1 张 SVG；仍缺 TCO、中国大厂 2026-06 后外部采用、失败率。- **2026-11-12 路线 B 收口 + 二审**：11 条嵌套坏链修复；E-01/E-18 改指正确 mechanism，E-14 的 p_h 标定新增独立锚点并贯通到 compilation/02/01；E-21/E-23/E-07/E-22 的做法按三条测试改写；二审把 01/03/feasibility 残留的点估计判门清成 95% CI 下界；check_repo 把嵌套链接与 active E 缺做法/链接记为 error。细则见 [state-log](./state-log.md#2026-11-12-路线-b-二审p_h-口径清尾--闸门升级)。
- **2026-11-12 meta 目录重组 + meta/AGENTS.md 门牌**：meta 根从 14 个平铺文件收成 **README（索引）+ AGENTS（30 秒入口）+ 子目录**：`rules/`（现行规则）、`deliverables/`（交付物治理）、`status/`（状态台账）、`templates/`（模板）、`audits/`、`archive/`、`tools/`；归档 2 个已完成开源计划；`meta/AGENTS.md` 只做门牌与指路、**不新增规则**（守住单一路由 ADR 0012）。
- **2026-11-12 治理体系化（fresh-agent 契约 + SCOPE）**：AGENTS 加「Fresh agent 三件事」（目标/质量门/边界）；每份交付物立 `SCOPE.md`（初心/定性/边界/红线/发挥空间/答不了怎么办）；check_repo 强制每份有 SCOPE.md；**04 改名 ontology-in-production → worked-example**（名实不符，合成示例非生产现状）；质量门重申 ≥2026-06-01 + 活跃 + 在役标准须现行版本+维护活动。
- **2026-11-12 交付物定位系统（ADR 0014）**：[meta/deliverables/scope](../deliverables/scope.md) 为五份总索引；各份 `SCOPE.md` 为权威；01–04 定性钉死；新开 [05-production-landscape](../../deliverables/05-production-landscape/README.md)（落地现状·实证，证据待补、不编）。硬规矩：**答不了初心问题就标 gap，不偷换成更容易的问题**——治 04 式漂移。
- **2026-11-12 topics 撤回源叙述页对账（11 提交）**：01-constraint（action-gate/reasoning-gate/reversibility）、02-judgment（evidence/checker/calibration）、05-produce（README/claims/generation/representation/lifecycle）、06-measure（metrics/mechanism/failure-attribution/feasibility/claims）把撤回源数字降 `推测`/历史示例并加对账横幅；admitted 源保留；06-L2、05-L1/L8 等级修正；01 capabilities 补 frontmatter。交付物正文扫描无漂移；最重要的 01-capability-status 经逐页冷读确认自包含、判定口径/计数/W 表一致。
- **2026-11-12 指令层结构整改（ADR 0012）** → [ADR](../../adr/0012-instruction-layer-single-home.md) / [审计](../audits/2026-11-12-instruction-layer-audit.md)；AGENTS 唯一路由 + 常设修复回路；规则单一出处；_plans 现行唯一；修 3 处漂移。细则见 [state-log](./state-log.md#2026-11-12-指令层结构整改adr-0012)。
- **2026-11-12 内容层 purge 对账 + 缺口盘点**：六派 frontier 队列 / 硬对象注册表（20 撤回）/ execution-forms（18 源）/ frontmatter 卫生对齐；[内容缺口盘点](../../deliverables/_plans/2026-11-12-content-gap-survey.md)（外部前沿对齐待补）。
- **2026-11-12 来源黑名单（ADR 0013）**：[excluded-sources](../rules/excluded-sources.md) 常设禁引清单（21 源）；白名单=admitted 卡不另设文件；采/引前查黑名单接进 AGENTS/协议/checklist；P0 四篇 probation 第二信号核实为阴性。
- **2026-11-11 素材准入重置** → [审计](../audits/2026-11-11-source-purge.md)；宪章 §4 + 18 篇论文/3 个旧网页移出 + 9 条 E 撤回。
- **2026-11-11 规范主干接线 + 术语 v1**：01–04 定义段接 N/local（[接线报告](../../deliverables/_plans/2026-11-11-trunk-wiring.md)）；[term-baseline](./term-baseline.md) v1 29 词 + [术语审计](../audits/2026-11-11-term-baseline.md)。
- **2026-11-11 撤回补偿（W 表 + 自测协议）**：[content-repair](../../deliverables/_plans/2026-11-11-content-repair.md)；02 免责密度 −43%，术语表 57→33 行，质量分以 [§12.4 独立修正](../../deliverables/_plans/2026-11-11-quality-review.md) 为现行口径（01=77/02=77/03=73/04=88）；§12.2/§12.3 已作废。
- **2026-11-11 内容精读 + 长尾清理**：[content-read](../../deliverables/_plans/2026-11-11-content-read.md)；清 40+ 处撤回源数值、修 2 个覆盖率格子、2 处排除源误用。
- **2026-11-11 代理冷读 + checkpoint**：[cold-read](../../deliverables/_plans/2026-11-11-cold-read.md)（68→86，修 5 处口径/裸词）；质量 §12.2 01=85/02=82/03=83/04=87。

## 怎么刷新

```bash
python3 meta/tools/check_repo.py
```

- 通过：更新本页的“最后自检”日期与计数；一次性的改动记录写 [state-log](./state-log.md)，不写回本页。
- 失败：先修，不提交。
- 本文的计数是**手工维护的唯一副本**；`check_repo` 会比对“最后自检”里的文件数，脚本能数的优先信脚本。
