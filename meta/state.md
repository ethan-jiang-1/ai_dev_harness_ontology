---
status: draft
updated: 2026-11-09
---

# 仓库状态戳

> 这是全仓**权威的当前计数**。README 只保留结构性摘要，checklist 不再抄数；数字冲突时以本页为准。
> 每次结构性提交前更新；自检命令见文末。

## 当前状态（2026-11-09）

| 项 | 值 |
|---|---|
| 阶段 | 内部研究档案；不做对外客户交付，因此不设客户资产/签核前置 |
| 论文 | 24 个目录（20 基础 + 4 扫描），全部有 PDF + 三份 MD + card + digest |
| 开源 | 6 个项目（trustgraph / semantica / ontop / open-ontologies + OPA / Qlever），已 pin commit、已消化 |
| 主题 | 6 派 + 22 个子主题 + 00-harness 七部件 + 6 时刻 + 1 条形态轴 |
| 结论 | 22 条 E：19 已核原文 + 1 已核代码 + 2 推测；3 条 Q；4 条 C |
| 局部判断 | 73 条 L（01:18 / 02:9 / 03:15 / 04:7 / 05:9 / 06:15） |
| 证据配比（28 篇 + 6 开源） | 9 execution-test（8 回路上 + 1 训练侧）/ 14 mechanism-only / 8 harness-evidence / 3 boundary-ruler |
| 执行形态（34 源） | engine 4 / compiled 7 / context 3 / label 2 / none 18 |
| 交付物 | 4 个子目录：01-capability-status / 02-engineering-playbook / 03-mechanism-reference / 04-ontology-in-production；02 为 README 门厅 + 13 条 recipe（R0–R12）+ 账本/评测/成本/上线/领域 + 附录；03 为四层结构（入口 + 6 位置卡 + 谱外页 + 3 横切页 + 证据台账/边界/缺口）；04 为建/用/治生命周期（README + GUIDE + 3 body + sections + evidence，E-21/E-22 已升、未入库 signal 另列）；另有 `_plans/` 工作底稿（非交付）；原 7 章书稿计划已废弃，没有独立 handbook |
| 模型 | 不本地安装；Yovole 两个：`DeepSeek-V4-Flash` / `qwen3.8-27b`；直连超时；harness override 可调用，但 subagent 会调用工具，**不用于实验**，只做第二意见；见 [models](./models.md) |
| 最后自检 | 2026-11-10 08:38，`python3 meta/tools/check_repo.py`：0 坏链 / 0 未定义 ID / 枚举通过（467 文件；E=22，Q=3，C=4，L=73；28 论文 / 6 开源） |

## 当前边界（不是阻塞）

1. **无外部资产请求**：D0/试点线已于 2026-11-09 删除；不再需要具名域、日志、题库、人或单价。
2. **独立复现仍是空缺**：不影响 desk research；若要升「已证」，需要独立复现，但不在本仓库做；不设实验目录，也不再用模型做实验被试。
3. **独立人类抽检**：只在对外交付时需要；内部研究不阻塞。
4. **开源执行线**：4 个项目已在 pin commit 上完成只读代码核对；矩阵进 [execution-forms](../topics/execution-forms.md#代码级核对2026-11-09)；`read-path` 已入库仍只有 1 个实现（外部扫描另见 sparql-guard 候选，未入库），需第二实现 + harness 调用点才能决定是否升第七时刻。

## 2026-11-10 交付物接线（M/R/X）

- **ADR**：[0009](../adr/0009-object-layer.md) 状态改为**接受（方案 A）**；[checklist](./checklist.md) §3、[loading](./loading.md) 规则 1、[objects](../topics/objects.md) 头部三处同步：O 可作地址，主句仍落 E。
- **M**：[02 §5.1](../deliverables/02-engineering-playbook/sections/acceptance.md#51-验收与-stop按机制选尺) 13 行 × 7 列；13/13 有出处，11 行挂 E/公式，2 行 `工程建议/gap`（R0、commit）。
- **R**：[03 boundaries §0](../deliverables/03-mechanism-reference/evidence/boundaries.md#0-反例集r-table) 12 条反例，带数/条件/`O-Rxx`；B1–B15 原表保留。
- **X**：[03 execution-forms §3](../deliverables/03-mechanism-reference/across-positions/execution-forms.md) 5 行加 `O` 列，补 OPA；Qlever 标「无代码锚」。
- **冷读**：3 条路径（编译/checker/read-path）均 2–3 跳到 digest 锚；0 断链，0 交付物 L 引用；1 个误读风险（O 是地址不是结论）已在 M-table 脚注写明。
- **计划**：[wiring-plan](../deliverables/_plans/2026-11-10-wiring-plan.md) 全部验收勾选；check_repo 通过（467 文件；objects 91 / H3 33 / H2 58）。

## 2026-11-09 硬对象层（O-xx，R1–R5）

- **新增** [topics/objects.md](../topics/objects.md)：地址层，不是结论层；**91 个对象**（C15 代码 / F13 公式 / T13 停线 / M3 矩阵 / N29 数值 / R12 反例 / P6 协议），H3 33 / H2 58；10 条承重 E 各 ≥3；**E 级 H3 8/10**；锚点 25 处（`path#anchor`）全部打开。
- **执行对比**：R1 C+F 22 个（H3 18，E 覆盖 2/10）→ R2 +T 35（22，2/10）→ R3 +M 38（**25，2/10**）→ R4 +N 67（27，**10/10**）→ R5 +F6/R12/P6 91（33，10/10；**E 级 H3 2/10 → 8/10**）。**R3 已到 25 个 H3 但覆盖只有 2/10**：H3 是手段，E 覆盖是目的。详见 [plan §12](../deliverables/_plans/2026-11-09-hard-objects-plan.md#12-执行对比四轮以及达到目的是什么意思)。
- **偏差/收口**：F 9/13 到 H3（F03–F06 缺 γ/单价/样本量实测，保持 H2）；承重 E 的 H3 覆盖 8/10（E-01/E-02/E-04/E-05/E-14/E-15/E-17/E-20），超过计划 ≥7/10；E-03/E-12 无可复算量；R12/P6 已补完。
- **待决**：[ADR 0009](../adr/0009-object-layer.md)（O 能否进交付物）状态为**提议**；在定案前按方案 B，交付物不引 O。
- **首轮抓到的偏差**：`O-F01` 复算 digest §4.3「Q=1,000、c=10 → 3.12%」得 3.08%（差 0.04pp），`c`/`Q` 疑为 rounded。
- **自检**：`check_repo.py` 已加 O 检查（warn-only）：对象字段/重复 ID/硬度/锚点/未定义引用；输出 `objects: 91 (H3 33 / H2 58 / H1 0)`，0 warning。

## 2026-11-09 交付物逆向补齐 + 硬对象产线

- **新增**：[reverse-gap-plan](../deliverables/_plans/2026-11-09-reverse-gap-plan.md)：从四份交付物反扫 topics/src，诊断四种薄法（17/22 单源、31/73 推测、13 行停线 0 出处、5 个门无第二实现/标签），给三条硬杠、旗舰三件（门槛表 / 反例集 / 执行矩阵）、上游订货单（TB/CA/FC/QP/S2/LB）与 WP0–WP8。
- **新增**：[hard-objects-plan](../deliverables/_plans/2026-11-09-hard-objects-plan.md)：把判断做成可引用/可复算/可核对的对象（O-xx）；H0–H3 分级、六字段 schema、`topics/objects.md` 注册表、五条产线（C/F/N/T/M+R/P/L）、10 天 60–80 个对象；O 能否进交付物待 ADR 0009。
- **定位**：工作底稿，不产生 E/L；与 [01 计划](../deliverables/_plans/01-capability-status.md)（E1–E9 证据）、[04 计划](../deliverables/_plans/04-ontology-in-production.md)（intake/scope）分工，不重复。
- **口径**：desk research + 只读代码；不向用户要资产/人/价/签核（ADR 0007）；停线出处标不出就标 gap，不编。

## 2026-11-09 D1 第一轮证据回抽

- **数据表**：[e3](../deliverables/01-capability-status/data/e3-compilation.md) / [e4](../deliverables/01-capability-status/data/e4-checker.md) / [e5](../deliverables/01-capability-status/data/e5-false-veto.md) / [e6](../deliverables/01-capability-status/data/e6-memory.md) / [e7-e8](../deliverables/01-capability-status/data/e7-e8-code.md) / [P0 扫描](../deliverables/01-capability-status/data/p0-source-scan.md)。
- **D1 verdict**：5 条 `supported（限定）`、1 条 `conditional`、3 条 `unknown`；见 [01 §2.4](../deliverables/01-capability-status/sections/map.md#24-e1e9-verdict2026-11-09-第一轮) 与 [§9](../deliverables/01-capability-status/sections/acceptance.md#52-期待与数据需求验收规格)。
- **关键结论**：E5 false-veto 仍 `unknown`（1,745 blocked 无标签）；E8 无写授权实现；E4 的 data-derived 在 UniProt 真实答案上过 +5pp/FA≤15%，curated FA 16.8% 超线；E6 只有部分设置过 +10pp/90%。
- **P0 候选**：2610.16838（授权 benchmark，go）、2607.22868（false-block/miss 前沿，go）；尚无 commit gate 实现。
- **topics 回写**：[02/checker F9](../topics/02-judgment/checker/findings.md#f9-用-d1-的5pp--fa15-阈值套-e-02) 已落账（data-derived 在 UniProt 真实答案上过 +5pp/FA≤15%；curated FA 超线）；其他数据表结论仍留在 deliverables 工作底稿，待第二轮决定是否升。
- **下一步**：落盘 2610.16838；读 2607.22868 正文；复核 sparql-guard 候选（是否建卡/是否有 harness 调用点）。

## 2026-11-09 D3 机制参考 v1.0 结构

- **四层结构**：[03 README](../deliverables/03-mechanism-reference/README.md)（主张类型 E/C/H/D/G + 四轴 crosswalk + 六位置表）→ `positions/`（context/memory/evidence/checker/action/commit + outside）→ `across-positions/`（measurement/coverage/execution-forms）→ `evidence-ledger` / `boundaries` / `gaps`。
- **上游合成件**：[execution-forms 执行链](../topics/execution-forms.md#执行链求值决策执行授权审计)（求值→决策→执行→授权→审计）；[metrics/coverage](../topics/06-measure/metrics/coverage.md)（七类失效 × 八位置矩阵）；[metrics/mechanism 八行分派](../topics/06-measure/metrics/mechanism.md#按位置分派八行设计)。
- **关键修正**：「强度–覆盖率反向」保留为 H（摘要），矩阵为 D（操作定义）；矩阵显示位置是专门化的，**不能排成一条强度线**；`checker` 4 个 `●/◐`、`action` 3 个，不能按格子数排强弱。
- **未新增 E；新增 1 条 L**：只抽取现有 E-01–E-20 与 C-03/C-04；分类设计记为 06-L15；commit 写路径、false-veto、M1 同本体跨位置仍标缺口。
- **页码/主证据**：position 卡的 8 字段（机制/触发/能改变/拦不住/使能/证据/可证伪/上游）统一；六位置表与附录互链，附录降为长版论证。
- 自检：`python3 meta/tools/check_repo.py` 通过（426 文件；E=20，Q=3，C=4，L=66；24 论文 / 4 开源）。

## 2026-11-09 交付物重构

- **三个子目录 = 三种交付物**：新增 [01 现状](../deliverables/01-capability-status/README.md)（能力矩阵：A 可先落地 / B 可试点 / C 只能设计 / D 反向；可当工作前提/不能当工作前提；距离表）、[02 工程实施](../deliverables/02-engineering-playbook/README.md)（五步法、R1–R9、4 个开源参考、论文/开源指示分级、参考架构、最小落地路线、验收表）、[03 机制参考](../deliverables/03-mechanism-reference/README.md)（三层分工、三条轴、六位置一页表、15 条边界）。
- **没有独立 handbook**：原 7 章、4–6 万字书稿计划废弃；唯一保留的是原第三章，现为 [03 的长版附录](../deliverables/03-mechanism-reference/appendix-constraint-spectrum.md)。原 outline / planning-notes / handbook README 已删除，git 历史保留。理由：书稿无独立角色、后四章缺证据、主线过强。
- **E-16 数字口径修正**：conclusions、ch03、01-constraint/sources、01-constraint/claims 的注记原来写成 `Tacit-FLE 64.3/66.7/65.0% vs IfR 64.3–65.0%`，与 OntoAct digest（Table 1）不符；改为 `78.6/83.3/90.0% vs IfR 64.3/66.7/65.0%`。这是转写错误，不是新判断；01-L11 原本就是对的。
- **交付物 README**：清单改为三个子目录（01 判断 / 02 操作 / 03 依据）+ 03 的附录；新增「handbook 的去留」与待做（图/Deck/案例页）。
- **01 证据计划**：新增 [plan.md](../deliverables/_plans/01-capability-status.md)：E1–E9 的覆盖审计、现有 digest 回抽（H1–H6）、新 `src/` 来源（P0/P1/P2）、WBS、排期、DoD 与停止规则。定位是工作计划，不是结论。
- **反向加载**：[meta/loading](./loading.md#从交付物倒查反向加载) 新增「从交付物倒查」三条链（01 期待→plan→digest；02 recipe→mechanism→digest；03 边界→E→附录）；三份 README 加「加载集」表；[topics/README](../topics/README.md) 与 [src/README](../src/README.md) 加反向读法指针。
- **支持层契约**：[meta/loading](./loading.md) 加「支持层契约」；[conclusions](../topics/conclusions.md) 加反向阅读规则（E→digest §4/§5→frontier）；[topics/README](../topics/README.md) 加反向路由表；[src/README](../src/README.md) 加 digest 四节锚点；[plan](../deliverables/_plans/01-capability-status.md) 加 E1–E9 → frontier 指针。目的：先保证 E→digest→frontier 可走，再开始倒逼。
- **验收规格**：三份 README 末尾各加「期待与数据需求」：把期待写成可证伪句，列出「支持它需要的数据 / 现在的证据 / 缺口」。作用是逆向暴露证据缺口，不是新结论。
- **术语**：GLOSSARY 新增「评测账本（Evaluation Ledger）」，与「台账」区分；交付物里的 `p_h`/false-veto/审批成本都指前者。
- 自检：`python3 meta/tools/check_repo.py` 通过（329 文件 / 22 论文 / 4 开源；E=20，Q=3，C=4，L=65）。

## 2026-11-09 手册第三章初稿

- 原第三章现为 [03 的长版附录](../deliverables/03-mechanism-reference/appendix-constraint-spectrum.md)：9 节、约 0.97 万中文字符；12 条 E + C-03；强度/覆盖率反向标组织假设；六个位置逐节；E-20 放 3.3。
- 原 planning-notes / outline 已删除（git 历史保留）；第三章证据行、图法与「准确率说法集中在弱端」的收窄记录不再有文件指针。
- 更新 [deliverables/README.md](../deliverables/README.md) 清单。
- 写作检验：topics 够用；六位置逐节未出现必须回写的判断缺口；已知缺口仍是 commit 写路径无实现、false-veto 未测、E-20 非效应量。
- 自检：`python3 meta/tools/check_repo.py` 通过（327 文件 / 22 论文 / 4 开源；E=20，Q=3，C=4，L=65）。

## 扫描状态（全局视图）

候选队列分散在各派 `frontier.md`；本表只汇总“最后一次扫描”，不复制候选。每周扫描后更新一行。

| 派 | 最后扫描 | 下一步 | 入口 |
|---|---|---|---|
| 01 约束 | 2026-11-09（开源 trustgraph） | false-veto/剪枝率；Commit Boundary 实现 | [frontier](../topics/01-constraint/frontier.md) |
| 02 判定 | 2026-11-07（首轮外部） | LogT / CORE-LLM-Bench 待落盘 | [frontier](../topics/02-judgment/frontier.md) |
| 03 知识 | 2026-11-07（首轮外部） | Grep 候选；投影粒度 | [frontier](../topics/03-knowledge/frontier.md) |
| 04 状态 | 2026-11-07（首轮外部） | APEX-MEM 候选；determinism 设计 | [frontier](../topics/04-state/frontier.md) |
| 05 生产 | 2026-11-08（G-X 回写） | KROMA 候选；可消费性 | [frontier](../topics/05-produce/frontier.md) |
| 06 测量 | 2026-11-07（首轮外部） | AgentDebugX 候选；机制→尺子表 | [frontier](../topics/06-measure/frontier.md) |

## 2026-11-09 删除 D0/试点线

按用户决定，“D0 资产门 + 内部试点”整条线删除：

- 删除 `meta/implementation/`（7 个文件：plan/status/gates/cost-model/d0-gate/report/README）。
- 删除 `deliverables/pilot-playbook.md`。
- 删除 `experiments/EXP-004-narrow-deep-k1.md`、`EXP-005-action-gate-shadow.md`、`EXP-006-ontology-checker.md`、`_pilot-template.md`。
- 不再请求具名域、日志、题库、人或单价；外部客户试点不是本仓库的路径。
- git 历史保留；若以后真要做企业试点，可从历史恢复，但不在门厅出现。

## 执行形态代码核对（2026-11-09）

在 card 所 pin 的 commit 上读代码（未跑测试；不改结论等级为「已证」）：

| 项目 | commit | `seam` | `execution_form` | 核对要点 |
|---|---|---|---|---|
| trustgraph | `184f622` | `read-path` | `engine` | SHACL-AF 策略求值；fail-open；只删 subject 侧；31 条策略测试存在 |
| semantica | `39cf721` | `checker` | `compiled` | 本体→SHACL；pyshacl `inference="none"`；CLI 校验 |
| ontop | `964dbb7` | `supply` | `engine` | TBox 饱和 + 查询重写 → SQL；不是 gate |
| open-ontologies | `375fbc4` | `none` | `engine` | SHACL→SPARQL / verified Core；影响报告 + CI 规则门；不是单次写授权 |

写入位置：[topics/execution-forms.md](../topics/execution-forms.md#代码级核对2026-11-09)（矩阵 + 4 条代码级判断）、[seams](../topics/seams.md#轴外位置可记录但不是六时刻)、4 个 digest 的「2026-11-09 代码核对」段、checker F7 的接口边界。

关键发现：`engine` 不是一种语义（OWL 重写 / SHACL-AF / SHACL 校验）；执行 ≠ 健全（trustgraph fail-open）；执行 ≠ 授权（open-ontologies 只做 CI/报告）；三态在 JSON 保留、在 shell 退出码被折叠。已升 [E-20](../topics/conclusions.md)（`已核（代码）`，不是 `已证`）。

## 冷启动复测（2026-11-09）

只读新 agent 复测：实际加载约 2,100 行 / 27 个文件；结论「能读懂，不能 15 分钟改仓」。首轮发现 4 处入口问题（loading 的 E-19/EXP/ADR 计数、README/state 的 18+2+3+4 计数、manifest 21–22 行断裂、topics/README updated），均已修复；复核 4/4 pass。`experiments/` 已无目录，D0/试点只在 ADR/归档/state 删除记录中。15 分钟路径已补 `meta/state`，并明确「只够读懂，不够改仓」。

## 薄页合并审计（2026-11-09）

15 个独立来源 <2 的子主题逐页审计：全部有独立机制或独立判断，**本轮 0 个合并**；`determinism` / `lifecycle` 列为下轮复核。规则与审计表见 [ADR 0008](../adr/0008-thin-subtopics-merge-audit.md)。「薄」是来源计数，不是冗余信号。

## 本轮修复（2026-11-09）

- E 层：全部 E-xx 出处改链 digest（17 条）；E-04 去掉“支撑 P3”的范畴错误，改标 P3a，并新增“E-04 能/不能支撑什么”范围框；Q-03 收窄到单基准/单 gate；outline 第 6 章去掉“reward 低估”的方向断言；合法意图归因降回 `推测`。E-04 共 37 处引用，4 类过度解读（结构有效 / P3b / reward 低估 / 合法意图）已修。
- 硬矛盾：E-05 错挂回改；02-L2 改为“模型自评”；开源接缝改为 `read-path` / `supply` / `none`；manifest 合并为 22 篇单账；GLOSSARY 工位改为 3 个；P3 拆 P3a/P3b。
- 结构：新增 `execution_form` 轴（[topics/execution-forms.md](../topics/execution-forms.md)，[ADR 0006](../adr/0006-execution-form-axis.md)）、`evidence_role`、`also_supports`；26 个来源全部落字段（9/4/6/3；engine 4 / compiled 7 / context 2 / label 1 / none 12）；E 行影响列改用 P1a/P1b/P1c/P2/P3a/P3b；15 个薄子主题标记；L1/L2/L3 定义与长度门重写。
- 账本：meta 索引 + 归档（8 个一次性文档 + full-audit）；state.md（本页）；可执行自检（ADR 0005）；ADR 索引（含 0006）；manifest 合并为 22 篇单账（含批次列），删除 manifest-scan。

## 2026-11-09 02 工程手册 v2

- **结构**：02 改为「README 门厅 + `recipes/`（R0–R12）+ `operations/`（账本/评测/成本/上线/领域）+ `appendices/`（接口/追溯/案例）」；README 保留决策图与 R 索引，细节下沉到分片，避免单页继续膨胀。
- **三份同构**：01/02/03 统一为 `0 一页结论 / 1 怎么读 / 2 地图 / 3 主体 / 4 边界 / 5 验收 / 6 关系与维护`；顶层 [deliverables/README](../deliverables/README.md) 做总导读；每份另有 `GUIDE.md` 做本份导读，子 README 只做索引，`sections/` 放 2/4/5/6，主体分别是 `capabilities/` / `recipes/` / `positions/`，条目字段统一为「一句话/适用/证据等级/边界/去哪」。01 的旧 `plan.md` 移到 [`deliverables/_plans/`](../deliverables/_plans/README.md)，不占交付正文章节。
- **新增**：R0 本体可执行性体检（四项准入：名字/单位、声明、覆盖、执行落点）；R10 离线/CI SHACL；R11 OBDA 查询重写；R12 受监管供给（citation + solver + 人签核）。R1–R9 保留编号，避免 01/03 的 R 引用漂移。
- **R8 第二实现**：外部扫描发现 `Matdata-eu/sparql-guard`（Apache-2.0，HEAD `6b68d769`）：TS 代理 + 查询重写，fail-closed、subject+object 两侧、有一组 vitest 用例（外部复核 76/76 通过，未在仓库内复跑）；**未按仓库标准入库**（单作者/1★/无 harness 调用点/无泄漏率）。它只说明 read-path 是 family（post-filter vs query rewrite），不升第七时刻，也不改 01 的 B 评级。候选记在 [commit-gate frontier](../topics/01-constraint/commit-gate/frontier.md)。
- **证据边界**：false-veto、grounding 校准、commit 写路径、第二 read-path 调用点仍缺；02 只写测量协议与 stop，不写「已解决」。
- 自检：`python3 meta/tools/check_repo.py` 通过（426 文件；E=20，Q=3，C=4，L=66；24 论文 / 4 开源）。

## 2026-11-09 04 落地生命周期

- **新增 [04-ontology-in-production](../deliverables/04-ontology-in-production/README.md)**：README 索引 + `GUIDE.md` 本份导读 + `sections/`（map/boundaries/acceptance/relations）+ `body/`（build/consume/govern）+ `evidence/`；按 0–6 与前三份同构。
- **读者**：本体/数据工程师（建）、应用/agent 工程师（用）、治理/安全（治）；决策者仍走 01，工程负责人走 02，架构师走 03。
- **证据边界**：外部来源（Ontology Generation、Axiom Benchmark、CK25、GGC、SAGA、SchemaForge、Build2SPARQL、VAULT、Graph-Agentic RAG、Enterprise Agentic Systems、AWS 指南）只作“信号/候选”，**未入库、未升 E**；04 正文只引 E-xx + 这些信号，不把厂商/摘要数字写成结论。
- 自检：`python3 meta/tools/check_repo.py` 通过（426 文件；E=20，Q=3，C=4，L=66；24 论文 / 4 开源）。

## 2026-11-09 04 支撑执行（E-21/E-22）

> 取代上一节的“外部信号未升 E”状态。

- 论文线冻结：GGC（SG）、Glyph（US）、NLKGQ（DE）、KGVoyager（US）入库；2512/2507/2503/CK25/VAULT/SPARQL-LLM/CQ4OE/OntoExtend/QRAKEN/PPC 删除。
- 页面/E：`03/querying`、`01/access-control`；E-21/E-22；04 B.3/C.1 引 E，build 保持 signal。
- 工程线：OPA、Qlever 入档；Web：HN Netflix 材料卡（不升 E）。
- 自检：`check_repo` 通过（462 文件；E=22，L=73；28 论文/6 开源）。

## 怎么刷新

```bash
python3 meta/tools/check_repo.py
```

- 通过：更新本页的“最后自检”日期与计数。
- 失败：先修，不提交。
- 本文的计数是**手工维护的唯一副本**；如果脚本能数，优先信脚本输出的数字。
