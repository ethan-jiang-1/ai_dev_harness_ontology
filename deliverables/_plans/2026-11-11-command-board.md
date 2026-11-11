---
status: draft
updated: 2026-11-11
type: command-board
scope: 交付物证据重置 + ADR 0011 术语基线
---

# 2026-11-11 指挥板：证据重置期间的单一收口

> **一句话**：仓库刚完成“源级”证据重置，但交付物正文还按旧源写着；K0–K4 的命名只是这场重置里最先被看见的一处。**从现在起，交付物（`deliverables/`）的判断、计数与发版口径只由本板收口；`src/`/`meta`/`GLOSSARY` 的术语线继续独立推进，但不得绕开本板改交付物。**

## 1. 现在到底发生了什么

| 线 | 已完成 | 还没完成 | 影响 |
|---|---|---|---|
| **来源准入/清除**（[审计](../../meta/audits/2026-11-11-source-purge.md)） | 28→10 论文、15→11 材料卡、9 条 E 撤回、27 条 L 撤回、15 个对象撤回；tombstone 与横幅已落 | 交付物里仍按被删源写成的数字/判断未重写 | **最高风险**：01 的 A/B/C/D 有一半建立在已撤回的 E 上 |
| **术语基线/ADR 0011**（[ADR](../../adr/0011-source-standing-and-term-baseline.md)、[计划](./2026-11-11-baseline-correction-plan.md)） | `standing` 字段、local 规则、ISO/IEC 21838 + OMG Commons 卡、K 事故入 ADR | `meta/term-baseline.md` v0（10 词）未落；W3C 卡 `standing` 未补；ODM 未核 | 不阻塞 01 的证据重置；但决定“以后怎么定义词” |
| **01 K0–K4 修复**（[K 页](../01-capability-status/sections/k-ladder.md)、[核查笔记](./2026-11-11-k-ladder-provenance.md)） | K0–K4 降为论文实验条件；首屏/术语/02/03/04 首现已改；`local` 与术语基线行已加；`check_repo` 通过 | K 之外的“撤回源”段落未动 | **叫法修好了，证据没修好** |

## 2. 最重要的判断

**这次重置不是“术语事故”，是“证据事故”。**

01 的能力矩阵里，至少 4 行仍把已撤回的 E 当一手证据：

| 行 | 能力 | 原锚 | 现状 | 建议 |
|---|---|---|---|---|
| #4 | 输出证据契约（grounding） | E-03 | withdrawn | 移出 A/B/C → `gap` |
| #5 | 输出后 checker | E-02 | withdrawn | 移出 A/B/C → `gap` |
| #6 | 动作前可逆性闸 | E-04 / E-13 | withdrawn；只剩 CASEL E-15（非本体） | 移出 A/B/C → `gap`；CASEL 另列“非本体参照” |
| #11 | 推理期条件验证 | E-16 | withdrawn | 移出 A/B/C → `gap` |

另外，01 README 的**第 3 条判断**（“约束类机制能改变走向，但 18 个模型-域组合只有 8 个改善”）整条建立在 E-04/E-13 上；它必须改成“该判断的原锚已撤回，今天不能承诺”，不能保留为结论。

**仍然站得住的**：#1/#2 K1/K2（E-12，N&D `admitted (probation)`）、#3 编译（E-08/E-14）、#7 记忆（E-05/E-17）、#8/#9/#10 读路径/OBDA/离线 SHACL（E-20）、#13 commit（E-20 否定性证据）、#14 确定性（设计）。

## 3. 目标矩阵（01 的下一版）

| 桶 | 行 | 计数 |
|---|---|---|
| **A 可先落地** | #1 点位语义（K1）、#9 OBDA、#10 离线/CI SHACL | **3** |
| **B 可试点** | #2 知识投影文本（K2）、#3 证据编译、#7 跨轮记忆、#8 读路径过滤 | **4** |
| **C 只能设计** | #13 落盘授权、#14 跨运行确定性 | **2** |
| **非本体（参照）** | #12 审批/多模式分配（CASEL E-15） | **1** |
| **gap / 待新源** | #4 证据契约、#5 checker、#6 动作闸、#11 推理期 | **4** |
| 合计 | 14 行（不删编号，保留回链） | 14 |

> **不删编号**：#4/#5/#6/#11 移到“gap/待新源”表，保留旧编号与 tombstone 链接；这样旧引用还能回查，但不再计入 A/B/C，也不再有“可试点”暗示。

## 4. 推进顺序（单一关键路径）

### P0 冻结与收口（本轮）
- 本板生效；01/02/03/04 不再新增判断；一个文件一个 writer。
- K 页/回执/`check_repo` 已收口；不再改 K 的命名（除非发现事实错误）。
- 交付物顶部只保留一条“证据重置”横幅，指向本板与审计。

### P1 01 证据重置（最高优先，先做）
1. `sections/map.md`：加“撤回源 → gap”判定步；#4/#5/#6/#11 移到 gap 表；§2.4 的 X4/X5 verdict 改 `unknown`。
2. `README.md`：§0 的 A/B/C 清单与计数；第 3 条判断改写；第一轮 verdict 计数。
3. `sections/canonical.md`：A=3 / B=4 / C=2 / 非本体=1 / gap=4；X4/X5 门槛改“待新源，不设门槛”。
4. `sections/decision-record.md`：记录 3/4（checker/action）改成“撤回→gap”的决策记录；不再写“为什么是 B”。
5. `sections/acceptance.md`：X4/X5 改 `unknown/gap`；删除“支持它需要的数据”里假装可验收的部分，改成“先找新源”。
6. `sections/boundaries.md`：§4.1 第 3/4 条、§4.3 第 2–5 条改为“原锚撤回，待新源”；不保留 E-04/E-02/E-03 的结论语气。
7. `capabilities/README.md`：3.4/3.5/3.6/3.9 的“能做什么/不能做什么”加撤回标记；不删机制描述，但不作为证据。

### P2 术语基线（并行，只动 `src/`、`meta/`、`GLOSSARY`）
- 基线线：`meta/term-baseline.md` v0 十词；K 行用本板 §2 的 `local` 判定；W3C 卡补 `standing`；ODM 死活核查。
- 本板只审“与交付物冲突”的词；不抢写 `src/`。

### P3 02/03/04 重写（01 完成后）
- 顺序：02（R5/R6/约束 recipe 重灾区）→ 03（action/checker/outside 位置卡）→ 04（证据台账）。
- 原则：先删/降撤回源，再谈质量分；不重写结构、不新增判断；`signal` 不进交付物。

### P4 收口
- `check_repo` + 质量评分 + 冷读；给出一页状态：哪些行还 gap、哪些源待新、哪些计数已对齐。
- **不擅自 commit**；当前工作区 300+ 项未提交，建议在 01 重置完成、check 通过后由用户决定 checkpoint。

## 5. 指挥关系与冲突规则

| 线 | 谁 | 能改什么 | 不能改什么 |
|---|---|---|---|
| 交付物证据重置 | 本线（01） | `deliverables/` 的 01–04 证据/计数/首屏/术语首现 | 不改六派结构、不新增 E/L、不恢复已删源 |
| 术语基线 | 基线线 | `src/` 标准卡、`meta/` 规则、`GLOSSARY` | 不写交付物；不把标准卡当效应量 |
| 来源清除 | 源整改线 | `src/` 删除/tombstone、`meta/audits/` | 不再写交付物；不再新增 source |
| 最终验收 | 本线 | 合并判断、计数、发版口径 | 不在未过 check 时标 stable |

**硬规则**：
1. 同一文件只允许一个 writer；遇到 `file changed since it was read` 先重读。
2. 每批改动跑 `check_repo`；计数只认 `meta/state.md`。
3. 撤回源只能出现在“撤回/待新源”语境；不得作为结论引用。
4. 术语定义只能引 `normative`；`local` 首现解释；标准卡不撑效应量。
5. 不在本板之外另起“第二套计划”。

## 6. 完成标准（这一轮）

- [ ] 01 的 A/B/C/D 表 0 行依赖 withdrawn E；4 行已进 gap 表。
- [ ] 01 的 A/B/C 计数与 README/ canonical/ decision-record/ acceptance/ boundaries 一致。
- [ ] 02/03/04 不再把 E-02/03/04/06/10/11/13/16/26 当结论（可保留 tombstone 说明）。
- [ ] `meta/term-baseline.md` v0 有 K 行；`GLOSSARY` 十词有 `origin`/`anchor`/`scope`。
- [ ] `check_repo` 通过；质量评分重跑；未决项一页可查。
- [ ] 未擅自 commit；checkpoint 建议已写在本板。

## 7. 立即可执行的三件事

1. 01 `map.md` 加“撤回源 → gap”判定步，并移动 4 行。
2. 01 `README.md` 改 §0 计数与第 3 条判断。
3. 01 `canonical.md` 改计数与 X4/X5 门槛。

> 本板是唯一指挥源；两个交接文件（[ADR 0011 交接](./2026-11-11-adr-0011-handoff-to-01.md)、源清除 handoff）只作背景与回执，不再各自发指令。

## 8. 进展记录

### 2026-11-11 · P0 + P1 第一批

- **已完成**：本板生效；01 的 [map §2.1/§2.2/§2.2b/§2.4](../01-capability-status/sections/map.md)、[README §0](../01-capability-status/README.md)、[canonical](../01-capability-status/sections/canonical.md)、[decision-record 6](../01-capability-status/sections/decision-record.md)、[acceptance X4/X5](../01-capability-status/sections/acceptance.md)、[boundaries §4.1–§4.4](../01-capability-status/sections/boundaries.md)、[capabilities 3.4/3.5/3.6 + 索引](../01-capability-status/capabilities/README.md)、[glossary §2](../01-capability-status/sections/glossary.md) 已按“源撤回 → gap”重写。
- **当前 01 计数**：A=3 / B=4 / C=2 / 非本体=1 / gap=4；#4/#5/#6/#11 保留编号，移入 gap 表。
- **数据表**：[e4-checker](../01-capability-status/data/e4-checker.md)、[e5-false-veto](../01-capability-status/data/e5-false-veto.md) 已加“只作历史”横幅。
- **自检**：`check_repo` 通过（434 md；10 论文 / 8 开源 / 11 材料卡）。
- **下一批**：01 的残留扫描（`capabilities`、`data/`、`GUIDE`、`templates` 中不再把 E-02/03/04/13/16 当结论）→ 02/03/04 引用撤回源的段落 → 术语线 `term-baseline v0` 的 K 行。

### 2026-11-11 · P3 第一批（02/03/04）

- **02**：README 首屏/判断、`sections/approach.md`、`recipes/README.md`、`sections/map.md`、`sections/acceptance.md`、`sections/canonical.md`、`sections/boundaries.md`、`recipes/judgment.md`（R4/R5）、`recipes/constraint.md`（R6）、`recipes/regulated.md`（R12）、`recipes/readiness.md`（R0 证据基础）、`appendices/traceability.md`、`appendices/case.md`、`appendices/artifact-pack.md` 已加撤回/ gap 标注。当前 02 计数：A=3 / B=4 / C=1 / gap=4（不含 R0）。
- **03**：README、`sections/map.md`、`positions/checker.md`、`positions/action.md`、`positions/evidence.md`、`positions/outside.md`、`evidence/ledger.md`、`evidence/boundaries.md` 已加撤回/ gap/历史标注。
- **04**：README、`evidence/ledger.md` 已标 E-02/E-04/E-06/E-26 撤回；其余生命周期内容不动。
- **START / deliverables README**：已改“约束/判定不能承诺”与当前收口状态。
- **自检**：`check_repo` 通过（434 md）。
- **下一批**：01/02 的残留数字清理（R4/R5/R6 正文里的旧效应量），03 的 `appendix-constraint-spectrum.md` 与 `sections/placements` 残留，04 的 build/consume 引用；然后 `term-baseline v0` 的 K 行与最终质量评分。

### 2026-11-11 · P3 第二批（残留标注）

- **02**：`recipes/judgment.md` 的 R4/R5 证据段、`recipes/constraint.md` 的 R6 证据段、`appendices/case.md` 的 R5 Week、`appendices/artifact-pack.md` 的 R4 模板、`sections/approach.md` 协议表、`sections/acceptance.md` 的 evidence/checker/action/受监管行、`sections/canonical.md` 的 99.9/9.7k、`operations/*` 的 basis 已标“历史/撤回”；`check_repo` 通过。
- **03**：`positions/action.md` 等位置卡的 `已核（E-04/02/03）` 已改 `withdrawn`；`evidence/gaps.md`、`sections/boundaries.md` B3、`across-positions/measurement.md`、`appendix-constraint-spectrum.md` 的 E-04 行/开头已标撤回。
- **04**：`evidence/ledger.md` 的 propagation/A.4/B 路线已标 E-06/E-02/E-26 撤回/移出。
- **未做**：02/03 正文里仍有旧数字（已加“历史”标注，但未逐句删）；03 附录的长版论证还需要一次逐节重写；术语线 `term-baseline v0` 尚未落。
- **自检**：`check_repo` 通过（434 md）。

### 2026-11-11 · Goal Round 1（补写与术语 K 行）

- **02 实际重写（不只横幅）**：`recipes/judgment.md` 的 R4/R5 证据段、`recipes/constraint.md` 的 R6 证据段已删旧数字，改为“原锚撤回；要重启先找新源”。
- **03 收口**：`positions/action.md` 的“能改变什么”与证据表、`positions/checker.md`/`positions/evidence.md` 的证据表已把 E-02/E-03/E-04/E-13/E-16 行标 `withdrawn`。
- **术语基线 K 行**：已写入 [baseline-correction-plan §S3](./2026-11-11-baseline-correction-plan.md)，判定 `local`；完整 10 词 v0 仍待基线线。
- **自检**：`check_repo` 通过（434 md）。
- **剩余**：02/03 长版附录仍有未逐句删的旧数字（已标历史）；`meta/term-baseline.md` 未建；质量评分/冷读未重跑；352 项未提交。

### 2026-11-11 · Goal Round 2（03 附录重写）

- **03 附录**：`appendix-constraint-spectrum.md` 的 §3.1.3（E-01/E-04）、§3.4.3 evidence、§3.4.4 checker、§3.4.5 action、§3.6.2 决策表、§3.7 限制、§3.8 证据表已从“旧数字+已核”改为“原锚撤回/历史”；旧 ID 锚点已保留。
- **03 位置卡**：action 的“能改变什么”与证据表、checker/evidence 的证据表、outside 的 E-16 行已标 `withdrawn`。
- **02 残留**：cost 的 E-13 段、domains 的 basis/出处、artifact-pack 的 `已核` 说明已改历史；R4/R5/R6 证据段已删旧数字。
- **自检**：`check_repo` 通过（434 md）。
- **仍剩**：02/03 个别长文段落仍可能带旧数字（已标历史）；`meta/term-baseline.md` v0 未建；质量评分/冷读未重跑。

### 2026-11-11 · Goal Round 3（术语 v0 + 03 附录）

- **术语 v0**：新建 [meta/term-baseline.md](../../meta/term-baseline.md)，10 词判定（aligned 1 / narrower 1 / broader 1 / divergent 0 / local 7；local 均显式标注）；补 GLOSSARY 的「本体」origin、「顶层本体」「领域本体」；给 8 张标准卡补 `standing: normative`。
- **03 附录**：§3.1.3、§3.4.3/4/5、§3.6.2、§3.7、§3.8 已重写为“原锚撤回/历史”，旧锚点保留。
- **02**：R4/R5/R6 证据段删旧数字；cost/domains/artifact-pack 残留已标历史。
- **自检**：`check_repo` 通过（435 md；10 论文 / 8 开源 / 11 材料卡）。
- **仍剩**：02/03 少数长尾旧数字；质量评分/冷读未重跑；353 项未提交。

### 2026-11-11 · Goal Round 4（长尾清理）

- **02**：`recipes/judgment.md` 的 R4 预算/成本、R5 机制/步骤，`operations/domains.md` 的 OA-RAG 数字、`operations/cost.md` 的 E-13 段已删/标历史；R4/R5 的旧数字不再作为做法依据。
- **03**：`positions/checker.md` 开头与口径注、`positions/action.md` 开头、`appendix-constraint-spectrum.md` 的 3.5/3.6 证据与成本行已改“撤回/历史”。
- **自检**：`check_repo` 通过（435 md）。
- **仍剩**：少量长尾旧数字（已标历史）；质量评分/冷读未重跑；checkpoint 未做。

### 2026-11-11 · Goal Round 4（一页状态）

- 新增 [一页状态](./2026-11-11-status.md)：01/02/03/04/术语的当前状态、不能信什么、未决项、checkpoint 建议。
- 继续清 02/03 长尾旧数字：R4/R5 预算与成本、domains OA-RAG、03 checker/action 开头、appendix 3.5/3.6、evidence 9.7k 注均已标历史。
- 自检：`check_repo` 通过（436 md）。
- **仍剩**：质量评分/冷读未重跑；术语 v1 未做；checkpoint 未做。

### 2026-11-11 · Goal Round 5（桌面复评）

- 按同一 12 维对 01–04 做桌面复评（非冷读）：**01=84 / 02=81 / 03=82 / 04=86**；02/03 下降主要来自可执行面缩小（R4/R5/R6/R12 转 gap），不是文笔退步。见 [quality review §12.1](./2026-11-11-quality-review.md)。
- 最后一批旧数字：02 canonical 的 e4 注、regulated 的 Grid 对照已标历史；02/03 不再把旧效应量当现役门槛。
- 更新 [一页状态](./2026-11-11-status.md) 的分数与未决项。
- 自检：`check_repo` 通过（436 md）。
- **仍剩**：真人冷读、术语 v1、checkpoint。

### 2026-11-11 · 第 7–10 步（规范主干接线 / 术语 v1 / 冷读 / checkpoint）

- **第 7 步（01→02→03→04 接线）**：四份术语页各新增「§0 名词从哪来（N / local）」；正文定义句标 `（N: 标准名）`/`（local）`。逐页：01 README/map/capabilities/decision-record/K 页；02 README/R4–R5/R6–R9/R10–R11/接口附录；03 README/checker/action/commit/memory/evidence；04 README/build A.3/govern C.1–C.2；共用入口 START。记录与验收命令见 [接线报告](./2026-11-11-trunk-wiring.md)。
- **第 8 步（术语 v1）**：[term-baseline](../../meta/term-baseline.md) 增 29 词（+06 试点补「任务账/风险账」1 词）；GLOSSARY 39 条全部有 `_origin_/_anchor_/_scope_`（v0 的 5 个漏条也补上）；计数 aligned 2 / narrower 2 / broader 1 / divergent 1 / local 33。06-measure 试点结论：0 术语冲突，1 条裸词已补判，见 [术语审计](../../meta/audits/2026-11-11-term-baseline.md)。
- **第 9 步（冷读）**：代理冷读第一轮 68/100，抓 2 处口径冲突（START「只记一句」说「让某些事不发生」，与 01「动作前的拦不能承诺」相反；map §2.2「等级」列混装 `gap`/`设计`，读成「gap=C」）；已修。第二轮复核 86/100，再补 3 处：`gap` 收窄为「曾有 E 被撤回」、#14 的例外写明、START 两个裸词就地解释。见 [cold-read](./2026-11-11-cold-read.md)。**真人冷读仍未做。**
- **第 10 步（checkpoint）**：`check_repo` 通过（442 md；0 坏链 / 0 坏锚 / 未定义 ID）；质量桌面复评 §12.2：01=85 / 02=82 / 03=83 / 04=87（非真人冷读）；提交最终 checkpoint（用户授权「一口气做完」）。
- **仍剩**：真人冷读、C2 冗余/体量、02/03 长尾旧数字逐句删、ISO 21838 条款号。

### 2026-11-11 · 精读 + 长尾清理（用户要求「替我读内容并判断」）

- **精读**：[content-read](./2026-11-11-content-read.md) 逐页读 01–04（约 41 万字符），判词 01 B+ / 02 B / 03 B+ / 04 B+；四个强项（决策页、recipe 骨架、位置卡、fixture 自包含）与四个弱项（历史数残留、排除源当工程经验、D 标签洗白证据、C2 体量）都写了证据行号。
- **清理**：撤回源（E-02/03/04/13/16/26、Grid、OA-RAG、OntoAct、Commit Boundary、SFE-O）的具体数值从 01–04 主路径删除或改定性，共 40+ 处；涉及 01 acceptance/canonical/boundaries/README/glossary、02 R5/R12/R0/cost/domains/ledger/evaluation/artifact-pack、03 evidence/checker/action/appendix/execution-forms/measurement/gaps、04 decision/transfer/build/reference/consume/boundaries/ledger。
- **两处判断修正**：① 03 覆盖率矩阵 `action×A` `●`→`?D`、`checker×B` `●`→`◐`（原用撤回 E 撑 `●`）；② 04/02 的成本不再挂 SFE-O，改「工程假设（`推测`），原源已移出」。
- **审计**：只读审计代理返回 23 条（数值残留 13 / 未标注 3 / 结论级 7），全部处置；复核 grep 只剩 admitted 源。
- **自检**：`check_repo` 通过（443 md）。
- **仍剩**：真人冷读、C2 体量、ISO 条款号、02 rollout/traceability 未逐句核。
