---
status: draft
type: content-read
updated: 2026-11-11
scope: deliverables/01–04 精读与质量判断（代理精读，非真人）
---

# 精读报告：01–04 的内容到底怎么样（2026-11-11）

> **谁读**：要把这套交付物拿去用/评审/继续改的人。
> **回答**：内容强在哪、弱在哪、哪些句子不可信、这一轮改了什么、还剩什么。
> **性质**：这是**代理精读**（我逐页读，不是抽样，也不是真人冷读）；判断带证据行号；处置只做「证据纪律 + 一致性」，不新增 E/L。

## 0. 读了什么

| 交付物 | 规模 | 本轮读到的页 |
|---|---|---|
| 01 | 19 文件 / 7.6 万字符 | README、GUIDE、map、capabilities、decision-record、boundaries、acceptance、canonical、glossary、K 页；data/ 只抽查 |
| 02 | 25 文件 / 12.4 万字符 | README、map、approach、canonical、acceptance、boundaries、R0–R12 全部、operations 的 cost/domains/ledger/evaluation/rollout、interfaces/artifact-pack/case/traceability |
| 03 | 26 文件 / 10.4 万字符 | README、map、glossary、六张位置卡、coverage、measurement、execution-forms、placement、reader-checks、templates、relations、claim-walkthrough、evidence 的 ledger/boundaries/gaps、附录 §3.1–§3.8 |
| 04 | 20 文件 / 10.7 万字符 | README、GUIDE、build、consume、govern、decision、reference、transfer、acceptance、boundaries、glossary、map、journey、relations、templates、worked-example、evidence/ledger、example/README |

**读法**：先按「读者卡 → §0 → 地图 → 主体 → 边界 → 验收」走一遍，再带着「这句话的证据在哪、限定有没有丢」回查；不是通读字数，是逐条判断句读。

> **第二轮补读（2026-11-11 晚）**：把首轮只抽查的页全部读完（02 rollout/traceability/case；03 placement/reader-checks/templates/relations；04 map/journey/relations/templates/worked-example/example）。结论不变；新增 3 处小问题（`02/case` 的旧 79.2%/0% 与 0% 语义检查、01 README 重复 GUIDE 的 5 页路径、02 canonical 双 banner），已修。

## 1. 一句话判断

| 交付物 | 判词 | 一句话 |
|---|---|---|
| **01 现状** | **B+（可作当前真相，需带着「历史数」警告读）** | 决策路径清楚、gap 处置诚实；弱在历史数字残留与篇幅 |
| **02 工程** | **B（骨架最好，被撤回数字污染最重）** | 13 条 recipe 的十字段是硬骨架；但 R5/R12 的正文曾把撤回源的数字当事实，已清 |
| **03 机制** | **B+（概念最锋利，但有「用设计标签洗白证据」的倾向）** | 位置卡与边界页写得好；覆盖率矩阵曾用撤回 E 撑 `●`，已降级 |
| **04 落地** | **B+（最像成品，成本链最弱）** | fixture 自包含、决策页优秀；但成本估算挂在已移出的 SFE-O 上，已改标「工程假设」 |

**总判断**：四份的**结构**是可信的；**证据纪律**在 2026-11-11 重置后仍有一层「数字残留」——不是缺内容，是**该删的数没删干净，且常出现在「这些数已撤回」的句子里**。这一轮把这些句子改成了「停用、不给值」，同时修了 6 处真实的来源误用。

## 2. 逐份详评

### 2.1 01 现状

**强在哪**

- 决策页真的在做决策：§0 一张表给 A/B/C/D/gap，`map §2.1` 给**有序判定规则**（先查源位阶→D→非本体→A→C→B→undetermined），这是全仓最可复用的一页。
- `acceptance §5.2` 把「期待」写成可证伪句 + 数据需求 + 没过怎么办，不是愿望清单。
- `canonical` 是单一真相：计数、阈值、历史数分区清楚；`gap` 与 C 的分野在本轮补了例外说明（#14）。
- K 页是 provenance 纪律的样板：谁定义、是不是标准、哪里过度外推，都写了。

**弱在哪（本轮已修）**

1. `acceptance §5.1` 把**已移出**的 2610.16838、2607.22868 写成「已入档」「校准理论」——读者会以为这两篇还可用。已改为「候选也按 §4 移出，待新源」。
2. 同页「28 篇论文 + 6 个开源」是旧计数；已改 10 + 8。
3. 同页「entailed 94.9%/supported 82.1%」来自已撤回的 E-03；已删值。
4. `canonical §3` 的「历史数」表仍列 8/18、1,745、15/26；已改成「值停用」。
5. `README` 的换词检查段（26 源/15/3）与 `glossary §6` 同数；已改成「计数停用」。
6. `boundaries §4.2` 写「旧 catch 79.2%/FA 0% 不能再用」——句子在否定它，但数字还活着；已删值。
7. `map §2.2` 的「等级」列混装 `已核`/`gap`/`设计`，冷读会读成「gap=C」；已拆列并在注里写清。

**还剩什么**

- **篇幅**：01 自称「5 页约 30 分钟」，实际按 GUIDE 走到验收约 10 页；冷读代理也卡在这。要么改口径，要么砍页（C2 项）。
- **历史数的「只读区」**：`data/` 与 `_plans/` 仍有旧数，已标历史；这是有意的，但新人可能翻到。

### 2.2 02 工程

**强在哪**

- 13 条 recipe 统一十字段（目标/前提/接缝/契约/步骤/证据/成本/验收/失效/锚点），是全仓最工程化的一份；R0 的 30–60 分钟准入流程可直接照做。
- `evaluation` 页把「先量噪声地板、预注册、非对称代价分开报」写成硬规则，比多数评测文档扎实。
- `canonical` 的三处对账（false-veto 5%、R1 双门、162 vs 149）说明作者知道自己的口径冲突并处理过。

**弱在哪（本轮已修，问题最重）**

1. **R5 的「LLM judge 分支」把撤回源的效应量当事实写**：`judgment.md` 原文列了 catch 40.3%、FA 16.2%、40 修好/83 修坏，而 R5 已判 gap。这是本轮最严重的一处「证据越级」。已改成定性描述 + 「数字停用」。
2. **R12 整页 ~50% 是 Grid 数字**，而 R12 已判 gap：0.967、99.9%、45/51、46/519、9,241 buses、13.9s。已全部改为定性读法，只留「工具在环境里 ≠ 工具在回路里」这类机制判断。
3. **SFE-O 已被移出（quality C），却仍在支撑判断**：`readiness` 把「表达 ≠ 执行」标成 `已核（限 SFE-O）`，并用 61.7%/23.6% 的检索瓶颈数；`decision`（04）的成本估算直接写「SFE-O digest 的推测估算」。已改为「工程经验/假设，原源已移出」。
4. `operations/domains.md`、`cost.md`、`ledger.md`、`evaluation.md`、`artifact-pack.md` 都有撤回源的数字残留（Grid、OA-RAG、E-02 per-flagged、9.7k tokens）；已逐条删值。
5. `approach §3.2` 说 sparql-guard「未在仓库内复跑」，与 state-log 的 EXP-001「仓库外复跑 76/76 通过」矛盾；已统一为「仓库外复跑，仍未入卡」。
6. `acceptance §5.2` 写「20 条 E 无已证」，与 01 的 27 条不一致；已改为「本份所引 E-01–E-20 无一为已证」。

**还剩什么**

- 清理后 02 的**可执行面变窄**：13 条里 4 条是 gap（R4/R5/R6/R12），实际「今天可照做」的是 R0/R1/R2/R3/R7/R8/R10/R11 + R9（设计）。这不是退步，是诚实；但读者需要一眼看到这个比例（recipe 索引已有计数）。
- `operations/rollout.md`、`appendices/traceability.md`、`case.md` 只读了关键段；下一轮可再逐句核。

### 2.3 03 机制

**强在哪**

- 六张位置卡每张都有「为什么不是相邻位置」「拦不住什么」「可证伪条件」，这是防过度承诺的好结构。
- `claim-walkthrough` 用一条 claim 走完「资金/证据/边界」，比抽象矩阵更有说服力。
- `evidence/boundaries` 的 N01–N12 反例集带条件与 O 地址，可逐条反驳。

**弱在哪（本轮已修）**

1. **覆盖率矩阵用撤回证据撑 `●`**：`action × A` 的理由是「POLAR 有代码级实现」（E-04 已撤回），`checker × B` 的理由是 E-02。矩阵是 D（设计），但 `●` 的判据写着「有实现或强机制证据」——用撤回源撑 `●` 是证据越级。已改：`action × A` → `?D`（机制设计、无实现），`checker × B` → `◐`（只碰结构错），并同步 §2.4、§4 的计数与叙述。
2. **位置卡正文仍列旧效应量**：checker §3 的 18.9/16.8、79.2/0、40.3/16.2；action §3 的 0.11–0.18、8/18、Tacit-FLE 数字。已全部改成定性 + 「数值停用」；这符合核心计划「旧数字不出现」。
3. `evidence/ledger` 的 E-04 行、`appendix` 多处「18 格/8 改善」；已改成「格数/改善数」。
4. `outside.md` 的 E-16 行、`checker` 的「同源检查」观察未标撤回；已标。

**还剩什么**

- 03 的**长版附录**（约 0.97 万字）仍是四份里最重的阅读负担；它是「为什么」的论证，不适合新人在 10 分钟路径读。建议保留但明确「只给评审/研究者」。
- 矩阵修正后，**全仓只剩 `memory × D` 一个 `●`**；这个结论很强（「今天没有哪一格能稳定阻断」），值得在 03 首屏或 01 里更醒目，而不是埋在矩阵里。

### 2.4 04 落地

**强在哪**

- 04 是**最像成品**的一份：9 件产物、5 组门槛、3 条 CQ、11 条策略测试、3 条 audit，读者能照着填。
- `decision.md` 的「`not enough data`」处置是四份里最成熟的：缺项 >2 不出点估计；成本公式 + 最小测量；`conditional` 不是失败。
- `boundaries` 的 17 条边界与「读者版三条」双切法，比单列清单好用。

**弱在哪（本轮已修）**

1. **成本链最弱**：`decision §2.2` 的「2–4 人周 / 3–5 人日」写成「SFE-O digest，`推测`」，而 SFE-O 已移出。已改成「工程假设（`推测`），原 SFE-O 已移出」；`transfer` 与 §7 误判同改。
2. `evidence/ledger` 的 O-F08 用 E-02 的 Se/FA 复算 PPV（57.2%），把撤回源的输入带进对象层；已改成「公式保留、旧输入停用」。
3. `boundaries` 引用三条路线的旧分数（98.33/89.9/64.6，后两者来自已移出的 NLKGQ/KGVoyager）；已删值。
4. `build.md` 的「旧 catch/FA（18.9/16.8）」仍在正文；已删值。
5. `glossary` 把 SFE-O 写成「本体工程做法」，未标已移出；已标。

**还剩什么**

- **fixture 数字的「实测感」**：04 的 2/2、7/4、4 dataset 都是**期望值**，不是运行记录；页面已说明，但新读者容易把它们当实测。建议在首屏用一行「这些数是 fixture 期望，不是跑出来的」再压一次。
- `worked-example`、`templates` 只抽查；模板里的示例数（如 13 列、50 列）是算术示例，风险低。

## 3. 横切发现（比单份问题更值得记）

1. **「这些数字已撤回」的句子，最常把数字留着。** 四份里至少 20 处是「旧 X%（不能再用）」的句式。读者会记住数字，不会记住否定。**处置**：全部改成「停用、不给值」；这也符合核心计划「旧数字不出现」。
2. **被移出的源仍在当「工程经验」用。** SFE-O（R0/成本）、Grid（R12/域）、OA-RAG（R4/评测样本量）、Commit Boundary（R9）都以「方法/量级」的名义留在正文。规则只写了「不得当结论」，没写「不得当做法来源」。**建议**：在 CHARTER §4 或 conventions 补一句——被移出的源只能出现在 tombstone/历史语境，不能作为 practice 或 estimate 的出处；本轮已按此执行（改标工程假设）。
3. **「设计」标签会洗白证据。** 03 的矩阵是 D，但 `●` 的判据要求「有实现或强机制证据」；用撤回 E 撑 `●`，等于用 D 的壳装 E 的数。**处置**：矩阵两格降级（`?D`/`◐`），并要求所有 D 类表格的每格写清「证据/设计」。
4. **C2 的真问题不是「跨份重复」，是「同一份内多层复述」。** 四份各自需要自包含（G3），所以术语表/横幅跨份重复是合理的；真正的冗余是同一份里「banner + §0 + 地图 + 边界」各说一遍同一组计数。本轮删了 01 的 2 处重复横幅；**不建议大砍**——会伤主路径自包含，收益小于风险。
5. **01/02 的「页数/时间」口径不一致**：01 说 5 页 30 分钟，实际路径约 10 页；GUIDE 说 10 分钟到 §0。**建议**：统一成「10 分钟到决策、30 分钟到验收」，本轮未改（属文案口径，下一轮统一）。

## 4. 修复清单（本轮，按文件）

| 位置 | 问题 | 处置 |
|---|---|---|
| `01/sections/acceptance.md` | 已移出源写成「已入档」；旧计数；E-03 数值 | 改「待新源」、10+8、删值 |
| `01/sections/canonical.md` | 历史数表保留 8/18、1,745、15/26 | 改成「值停用」 |
| `01/sections/boundaries.md` | 「79.2%/0% 不能再用」仍带值；26/15/3 | 删值，改「计数停用」 |
| `01/README.md`、`01/glossary.md` | 换词检查 26/15/3 重复 | 改「计数停用」 |
| `02/recipes/judgment.md` | R5 judge 效应量当事实；R4/R5 多处旧值 | 全改定性 + 停用 |
| `02/recipes/regulated.md` | R12 整页 Grid 数字 | 改定性读法；删 0.967/99.9/45/51/46/519/9,241/13.9s |
| `02/recipes/readiness.md` | SFE-O 当已核；61.7/23.6；curated 证据 | 改工程经验/历史；删值 |
| `02/operations/{domains,cost,ledger,evaluation}.md` | Grid/OA-RAG/E-02 数字残留 | 删值/标历史 |
| `02/appendices/{artifact-pack,case}.md` | 9.7k tokens；E-02 出处 | 改 `<实测>`/标撤回 |
| `02/sections/{approach,acceptance,canonical,boundaries}.md` | 参数级引用移出源；20 条 E；99.9%；sparql-guard 复跑矛盾 | 逐条改 |
| `03/across-positions/coverage.md` | 2 个 `●` 用撤回 E 撑 | action→`?D`、checker→`◐`，同步叙述与计数 |
| `03/positions/{checker,action}.md` | 旧效应量列在正文 | 改定性 + 停用 |
| `03/evidence/{ledger,boundaries}.md`、`appendix` | 「18 格/8 改善」等 | 改「格数/改善数」 |
| `03/positions/{outside,checker}.md` | E-16/E-02 观察未标撤回 | 标撤回 |
| `03/sections/map.md` | 「各只对 1 类 ●」与矩阵不一致 | 同步为 memory 1 个 `●` |
| `04/sections/decision.md`、`transfer.md` | 成本挂 SFE-O | 改「工程假设，原源移出」 |
| `04/evidence/ledger.md` | O-F08 用 E-02 输入复算 PPV | 保留公式、停用旧输入 |
| `04/sections/boundaries.md` | 三条路线旧分数；checker 边界；输入 gate 观察 | 删值/标撤回 |
| `04/body/build.md`、`sections/glossary.md` | 旧 catch/FA 值；SFE-O 未标移出 | 删值/标移出 |
| 四份 glossary §0 + 正文定义页 | 定义来源 | 上一轮已接线；本轮补 03 map/03 placement/02 approach/04 reference 四处 |
| `02/case.md` | 旧 79.2%/0%、结构检查 0% | 改定性；预注册门槛标「旧口径停用」 |
| `01/README.md`、`02/canonical.md` | 5 页路径与双 banner 重复 | 改为 GUIDE 指针 / 合并 banner（C2） |

## 5. 还没解决（诚实清单）

1. **真人冷读**：仍是人工步骤；代理两轮（68→86）不能替代。
2. **C2 体量**：四份合计约 41 万字符；02/03 的长版是主要负担。本轮只做保守去重，没有大砍——原因是 G3（主路径自包含）与「不重写结构」的约束。
2.1 **清理后 02 的可执行面变窄**：13 条里 4 条 gap；读者需要看 recipe 索引的计数，不要拿 gap 行当配方。
3. **逐句 N/local**：做到「页级 + 定义句就地标」；没有给每个术语的每次出现都加标记（会伤 B3）。四个术语页 §0 是查询面。
4. **ISO/IEC 21838 条款号**：仍 `待核`；仓库只有摘要级卡，读不到正文条款，不能编。
5. **02/03 的 data/ 与 _plans**：旧数仍在，已标历史；不参与主路径。
6. **未读页**：02 rollout/traceability/case 部分、03 placement/reader-checks/templates、04 templates/worked-example/journey 只抽查；下一轮可补。

## 6. 与自动审计的关系

本轮另起两个只读审计代理（02 一个、03/04 一个），按「撤回源数字」清单扫全文。03/04 审计返回 **23 条**（数值残留 13、未标注 3、结论级未标注 7），**已全部处置**：

| 审计项 | 处置 |
|---|---|
| `03/positions/evidence.md` 的 E-03 六处数值（50.5/68.1、84.9/66.7、5.8/9.7k、94.9/82.1、61.7/23.6、9.7k/96.7k） | 改定性 + 「数值停用」 |
| `checker.md` 的「结构检查 0%」「corrupt 1.0%」 | 改机制判断/定性 |
| `action.md`、`ledger.md` 的 E-13 斜率 | 改「斜率为负、数值停用」 |
| `appendix` 的 50.5/68.1、9.7k/96.7k、E-03 当现役证据 | 改定性/标撤回 |
| `execution-forms`、`measurement`、`gaps` 把 E-02/E-03/E-04/E-16 当代表/现役 | 标撤回 |
| `04/reference` 的 NLKGQ/KGVoyager 分数（89.9/81.3、64.6/60.9、98.33 并列） | 标「源已移出、数值停用」 |
| `04/consume` 的两条已移出路线描述 | 标「原论文已移出，只作路线形态」 |
| `03/positions/commit.md` 的 promotion 契约未点名来源 | 加 banner 点名 Commit Boundary 已移出；证据表改历史 |

02 的审计代理超时未返回（已停）；02 的清理由主代理按同一标准逐页完成并复核：`grep` 只剩 E-05（admitted）的数值。若后续代理清单与本文有出入，以文件当前内容为准。

**定义句的机械代理检查**（第三轮）：所有含「定义为 / 是指 / 指的是 / 所谓」的页面，都已带「词源」或 `term-sources`；没有定义段落在无来源页上。

**复核命令**（应只剩 admitted 源）：

```bash
grep -rn "50\.5\|68\.1\|94\.9\|82\.1\|9\.7k\|40\.3\|18\.9\|16\.8\|79\.2\|99\.9\|0\.967\|18 格\|8 改善" \
  deliverables/01-capability-status deliverables/02-engineering-playbook \
  deliverables/03-mechanism-reference deliverables/04-ontology-in-production \
  --include=*.md | grep -v "/data/\|_plans\|withdrawn\|撤回\|历史\|停用\|待新源\|旧"
```

> 本页是工作底稿，不是交付正文；不构成 E/L。判断只到「内容与证据纪律」，不替读者做 domain 决策。
