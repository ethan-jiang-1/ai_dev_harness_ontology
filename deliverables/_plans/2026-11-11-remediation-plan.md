---
status: draft
type: work-plan
updated: 2026-11-11
target: deliverables 02/01/03
scope: remediation
---

# 整改计划：按 02 → 01 → 03 把三份交付物补到可达的 L2

> 依据 [差距评估报告](./2026-11-10-gap-assessment-report.md)。受 [CHARTER](../../CHARTER.md) 约束：**只做文档层的读、消化、组织、写**；不新增 E/L、不做实验、不写代码、不跑示例。示例与数字只从 `topics/` / `src/` 已有材料里取；取不到就标 `gap` / `untested`。

## 0. 一页结论

**三份的缺口不是同一种东西，所以整改也不是同一套。**

| 顺序 | 交付物 | 缺的那一层 | 主改动 | 验收 |
|---|---|---|---|---|
| 1 | 02 工程 | 参照物（产物包） | 一份填好的 R4 产物包 + 术语页 + canonical 阈值表 + 5 组读者检查 + 三处对账 | 冷读能填完一行契约并说出停线 |
| 2 | 01 现状 | 规则（A/B/C/D） | 有序判定规则（含 undetermined）+ 两份决策记录 + 术语页 + canonical 表 + 9 条「没过怎么办」 | 冷读能给一项能力判 A/B/C/D 并说理由 |
| 3 | 03 机制 | 读者判据 | claim 走查（read-path）+ 5 条读者检查 + 术语页 + 覆盖率/E-22/30-31/M1-M5 修复 | 冷读能判一条 claim 的位置与边界 |

## 1. 四个决定（2026-11-11，按上下文自行拍板）

### D1 · 接受「三种缺口、两张排序」

级差排序 02 = 03 > 01；可补性排序 02 > 01 > 03。**两张都保留**：它们回答不同问题（离 L2 多远 / 补起来要什么）。不合成总分。

### D2 · 01 不改 14 行的 A/B/C/D 标签，只把规则写死

理由：

- 改标签 = 改判断，按 01 自己的规矩要回 `topics/` 改证据；当前证据不够，改了会造出新结论。
- 现有 14 行其实能被一条规则唯一判定，只是规则没写出来。
- #12「审批/多模式分配」的问题是**类别错误**（它不是本体机制），不是成熟度误判；把它标成「非本体（参照）」是纠错，不是改标签。
- README 的「多智能体共享本体」不在矩阵里，是**空白**，不是 C；移到 `undetermined`。

**结果**：14 行标签不变；C 桶统一为 3 行（推理期/落盘/确定性）；#12 单列「非本体」；「多智能体/自动生成」进 undetermined。

### D3 · 03 的 M1/M2 只标 gap，回 frontier

- 不写、不补、不立项。`docs` 层写不出「同本体跨位置」的测量。
- 03 的整改只做读者层：claim 走查、读者检查、术语；外加修硬伤（覆盖率错误、E-22 台账、30/31、M1–M5 重复）。
- 报告与 03 的边界页都保留「M1/M2 未开」；不因补了读者层就暗示它们成立。

### D4 · 顺序 02 → 01 → 03

02 是加法、低风险，先做能验证「产物包」这个参照物类比；01 杠杆最高但需要规则与你的默许（本计划按 D2 执行，不改标签）；03 有硬顶，最后做读者层。

## 2. 三份共用的三个写法

1. **canonical 表**：一个数只写一次，其他页引用。每份新建 `sections/canonical.md`（01/02）或并入现有页（03 用 `evidence/ledger.md`）。
2. **术语页**：每份新建 `sections/glossary.md`；只解释「读这份会用到的码与词」，不重复仓库 `GLOSSARY.md`。
3. **读者检查**：每份的 acceptance 增加 5 组「怎么查 / 通过 / 未通过」，与 04 的 A1–C5 同形。

## 3. 02 的工作包

| # | 改动 | 文件 | 验收 |
|---|---|---|---|
| 2.1 | 填好的 R4 产物包（契约/概念卡/查询/账本行/停线记录/未测清单） | 新 `appendices/artifact-pack.md` | 读者能照着填自己的一行；每个值有出处或标 `untested` |
| 2.2 | 术语页（R0–R12、K0–K2、p_h/p_min、FA、CMR、O 码、5pp/15%/90%/60k） | 新 `sections/glossary.md` | 正文内码 100% 有定义或链 |
| 2.3 | canonical 阈值表（false-veto 前沿、R1 绝对/相对、5pp、15%、90%、60k、2 人周、0.95、20%/10%） | 新 `sections/canonical.md` | 其他页不再各写一套 |
| 2.4 | 5 组读者检查（R0 / 选 recipe / 接口 / 停线 / 边界） | `sections/acceptance.md` | 每组有 pass/fail |
| 2.5 | 对账：false-veto 5%、R1 0.90 vs +10pp、162 vs 149 | `recipes/constraint.md`、`operations/cost.md`、`sections/acceptance.md`、`appendices/case.md` | 三处只剩一个现役写法，另加「历史口径」注 |
| 2.6 | 修悬空锚；README/GUIDE 接入新页 | `sections/boundaries.md`、`README.md`、`GUIDE.md` | `check_repo` 0 断链 |

**162 的事实**：`topics/03-knowledge/projection/mechanism.md:104` 与 `src/papers/2610.11768-narrow-and-deep/digest.md:66` 都写 42 tags + 34 assumptions + 33 bindings + 24 knowledge + 16 derivations + **13 plant elements** = 162。`case.md:18` 漏了 13 plant elements，相加 149。改 case 补上，不改 162。

## 4. 01 的工作包

| # | 改动 | 文件 | 验收 |
|---|---|---|---|
| 1.1 | A/B/C/D 有序判定规则（D → 非本体 → A → C → B → undetermined），每步给判据与例子 | `sections/map.md` §2.1 | 14 行逐行能唯一判定；#12 标非本体；一个 undetermined 案例 |
| 1.2 | 两份决策记录：K1→A、read-path→B；附 OBDA→A 的对照 | 新 `sections/decision-record.md` | 每份有 证据→门槛→判定→缺什么→停在哪 |
| 1.3 | 术语页（E1–E9 vs E-01–E-20、T1–T5、K0–K2、pp、p_h、FA、CMR、D1 底稿） | 新 `sections/glossary.md` | 正文内码有定义或链 |
| 1.4 | canonical 表（14 能力、9 期待、E 条数、C 桶 3、D 反向 6） | 新 `sections/canonical.md` | README/map/acceptance 引用不复制 |
| 1.5 | 9 条期待加「没过怎么办」 | `sections/acceptance.md` | 9/9 有处置 |
| 1.6 | C 桶 3 vs 4、`human-audit` vs `reattachment`、Q-01 链 | `README.md`、`sections/map.md`、`capabilities/state.md`、`sections/boundaries.md` | 三处一致；Q-01 链到 `topics/conclusions.md` |

**不改标签**：14 行判定保持原样；#12 从 C 移到「非本体（参照）」是类别纠错（理由见 D2）。

## 5. 03 的工作包

| # | 改动 | 文件 | 验收 |
|---|---|---|---|
| 3.1 | claim 走查：「读路径过滤能防止敏感数据泄漏吗？」 | 新 `sections/claim-walkthrough.md` | 有位置/成立程度/四条不成立条件/缺什么 |
| 3.2 | 5 条读者检查（定位、证据、边界、形态、判不了） | 新 `sections/reader-checks.md` | 每条 pass/fail |
| 3.3 | 术语页（E/C/H/D/G、O/C/M/B/R/T/K/Q/RQ/P、seams、强度、覆盖率、B/R、●◐○?D） | 新 `sections/glossary.md` | 12 类内码至少 10 类有定义或链 |
| 3.4 | 修覆盖率：C/E/F/G 四类没有 ●，不是「只有 G」；统一「覆盖率 = 类别集合，不是百分比」 | `across-positions/coverage.md`、`evidence/gaps.md`、`appendix-constraint-spectrum.md` | 两处说法一致；矩阵自证成立 |
| 3.5 | E-22 台账行（按 `topics/conclusions.md:44` 摘，不新增判断） | `evidence/ledger.md` | E-22 可查；R07 不再是悬空出处 |
| 3.6 | 30% vs 31% 统一；M1–M5 表只留一处 canonical，另一处链接 | `positions/action.md`、`across-positions/measurement.md`、`sections/acceptance.md`、`evidence/gaps.md` | 一处写、两处引 |

**M1/M2 不碰**：只把「未开」写清，不写新证据。

## 6. 验收（每份都要过）

1. `python3 meta/tools/check_repo.py` 通过（0 断链 / 0 未定义 ID）。
2. **新的独立冷读**：起一个没读过评分卡、没读过 `_plans` 的 agent，只读该份做一次任务；记录 finished / 卡点 / 是否开 `topics/`。通过线：`finished = yes`，或 `partial` 且卡点全是「材料里确实没有的 gap」（不是「找不到」）。
3. **一致性抽查**：改过的数在 canonical 表与正文一致；没有新增 `E-xx` / `L-xx`；没有把 `推测` 写成 `已核`。
4. **不新增判断**：每处新文字要么是已有 E 的展开，要么标 `gap` / `untested` / `工程建议`。

## 7. 不做什么

- 不改 04；不改 `topics/` 的 E/L（只读）；不新增 E/L。
- 不为「凑 L2」造数字；不把 fixture 复制给 01/03。
- 不做外部读者测试；冷读是代理自审，报告里标清。
- 不把 M1/M2 写进 03 的正文当结论。

## 8. 风险

| 风险 | 处理 |
|---|---|
| 01 规则写死后，某行按规则判出的标签与原标签不一致 | 以原标签为准，反查规则漏了哪条判据；不悄悄改标签 |
| 02 的产物包被读成「实测结果」 | 每个值标 `已核` / `推测` / `untested`；页首写「这是填好的样例，不是运行记录」 |
| 03 的 claim 走查被读成新结论 | 页首写「这是读法，不是新 E」；每个判断挂 E-20/E-22/R07 |
| 冷读 agent 太慢 | 等；不中断、不用结构核对替代 |


## 9. 执行记录（2026-11-11）

- **02**：新增 [artifact-pack](../02-engineering-playbook/appendices/artifact-pack.md)、[glossary](../02-engineering-playbook/sections/glossary.md)、[canonical](../02-engineering-playbook/sections/canonical.md)、[acceptance §5.4](../02-engineering-playbook/sections/acceptance.md) 5 组读者检查；对账 false-veto（改为报前沿）、R1（绝对/相对两个门）、162（补 13 plant elements）。冷读 `partial`：卡点 = citation 正确性无 recipe、引用率口径未定义、无 R4 专属两周表——都是真 gap；顺手修了 9.7k total vs 5,000 generated 的口径。
- **01**：A/B/C/D 改为 [map §2.1](../01-capability-status/sections/map.md) 的六步有序规则；新增 [decision-record](../01-capability-status/sections/decision-record.md)（K1→A、读路径→B、离线 SHACL→A、OBDA 对照）、[glossary](../01-capability-status/sections/glossary.md)、[canonical](../01-capability-status/sections/canonical.md)；9 条期待补「没过怎么办」；C 桶统一 3；#12 标非本体；`human-audit` 改名；Q-01 加链。**冷读：第一轮 `partial`（发现 3 处内部矛盾）→ 修复后第二轮 `yes`**（判对 B/A/source，并复述理由）。
- **03**：新增 [claim-walkthrough](../03-mechanism-reference/sections/claim-walkthrough.md)、[reader-checks](../03-mechanism-reference/sections/reader-checks.md)、[glossary](../03-mechanism-reference/sections/glossary.md)；修 coverage「只有 G 没有 ●」→ C/E/F/G、覆盖率两套定义、E-22 台账行、30%→31%、M1–M5 去重（acceptance 只留状态）。冷读 `partial`：位置/程度/四条条件/未修清单都答对；卡点是「强读法需实测」——属真 gap。
- **验收**：`check_repo` 通过（520 文件）；04 未改；没有新增 E/L；M1/M2 仍标 gap。
