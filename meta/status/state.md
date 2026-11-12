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
| 材料卡 | 11 张（1 张 HN + 10 张在役标准卡） |
| 主题 | 6 派 + 23 个子主题 + 00-harness 七部件 + 6 时刻 + 1 条形态轴 |
| 结论 | 27 条 E：13 已核原文 + 2 已核代码 + 3 推测 + **9 已撤回**（E-25 由已核降推测）；3 条 Q；4 条 C |
| 局部判断 | 79 条 L（01:19 / 02:10 / 03:16 / 04:7 / 05:10 / 06:17）；其中 **28 条 withdrawn**（源移出） |
| 硬对象 | 94 注册（**20 已随源撤回**；现存 74：H3 33 / H2 41）；明细见 [objects](../../topics/objects.md) 变更记录 |
| 证据配比（10 篇 + 8 开源） | 3 execution-test / 11 mechanism-only / 4 harness-evidence / 0 boundary-ruler |
| 执行形态（18 源：10 论文 + 8 开源） | engine 3 / compiled 3 / context 1 / label 1 / none 10 |
| 交付物 | 5 个子目录 + 共用入口 [START](../../deliverables/START.md)：01-capability-status / 02-engineering-playbook / 03-mechanism-reference / 04-worked-example；02 为 README 门厅 + 13 条 recipe（R0–R12）+ 账本/评测/成本/上线/领域 + 附录；03 为四层结构（入口 + 6 位置卡 + 谱外页 + 3 横切页 + 证据台账/边界/缺口）；04 为建/用/治生命周期（**合成示例**，E-21/E-22 已升）；**05-production-landscape 落地现状·实证（新增，证据待补，ADR 0014）**；另有 `_plans/` 工作底稿（非交付）；原 7 章书稿计划已废弃，没有独立 handbook |
| 模型 | 不本地安装；Yovole 两个：`DeepSeek-V4-Flash` / `qwen3.8-27b`；直连超时；harness override 可调用，但 subagent 会调用工具，**不用于实验**，只做第二意见；见 [models](./models.md) |
| 最后自检 | 2026-11-12，`python3 meta/tools/check_repo.py`：0 坏链 / 0 坏锚 / 0 未定义 ID / 枚举通过（504 个 md；E=27，Q=3，C=4，L=79；10 论文 / 8 开源 / 11 材料卡） |

<a id="当前目标下一步做什么"></a>
## 当前目标（下一步做什么）

> **「现在最该做什么」只看这一节**；README / _plans / 各派 frontier 都不另立优先级。做完一项就改这一节，并记 [state-log](./state-log.md)。

| # | 目标 | 为什么是它 | 关闭条件 |
|---|---|---|---|
| 1 | **补真实生产/业界证据**，让 [05 落地现状](../../deliverables/05-production-landscape/README.md) 有正文 | 用户最想要的问题（业界到底怎么样）现在答不了；04 当年就是拿合成示例顶替它才跑偏 | 有 ≥1 条过门的真实生产证据（含 §4.4 公司生产报告），能写进 05 且每条可追进 admitted |
| 2 | **P0 四篇 probation 补第二独立信号**（GGC / Agents / N&D / CASEL） | 只靠一条信号，2027-05-11 前补不到就移出，会带走 E-12/E-15/E-18 等锚 | 每篇卡上 `impact_evidence` 出现第二个独立信号（≥1 个 I1–I3） |
| 3 | **M1/M2 承重墙**：同本体跨位置对照、覆盖率测量 | 03 明写「没有这两项，只给分类不给效应量」；这是全仓最大的方法论缺口 | 有 admitted 源做同本体跨位置对照，或明确判定「现有文献不存在」并写进 frontier |

> 不在这张表里的事，默认不做；要做先进这张表（一次至多 3 项，按序）。
>
> **收东西的口径**：只收「能长期保障质量」的做法（可重复 / 自带检测 / 抗腐化），见 [conventions 三条测试](../rules/conventions.md#只收能长期保障质量的做法不是一次性技巧)。一次性技巧记候选，不升 E。

## 已知债务（别当成已完成）

> 这些是**已识别但未做完**的事。每条写清"缺什么、谁能关、判据"，避免下一轮误以为已完成。

| # | 债务 | 现状 | 关闭判据 |
|---|---|---|---|
| D1 | **05 无 A 类证据** | 窗口内只找到媒体/厂商调查/合作 PR；三件套（规模+成本+失败）无一齐备 | 有 ≥1 条 A 类一手复盘过 §4.4，写进 05 且可追到卡 |
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

- **2026-11-12 路线 B 收口 + 二审**：11 条嵌套坏链修复；E-01/E-18 改指正确 mechanism，E-14 的 p_h 标定新增独立锚点并贯通到 compilation/02/01；E-21/E-23/E-07/E-22 的做法按三条测试改写；二审把 01/03/feasibility 残留的点估计判门清成 95% CI 下界；check_repo 把嵌套链接与 active E 缺做法/链接记为 error。细则见 [state-log](./state-log.md#2026-11-12-路线-b-二审p_h-口径清尾--闸门升级)。
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
