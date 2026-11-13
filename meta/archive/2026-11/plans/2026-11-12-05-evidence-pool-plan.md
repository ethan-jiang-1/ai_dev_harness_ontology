---
status: draft
type: execution-plan
updated: 2026-11-12
scope: deliverables/05 + src/papers + topics
current: false
---

# 05 证据池修复计划（2026-11-12，第二轮）

> 现行计划（[_plans 至多一份](../../../../deliverables/_workpapers/README.md)）。前一轮 [缺口补齐计划](./2026-11-12-05-gap-closure-plan.md) 已执行完；本计划针对它暴露出的**新缺口**。
> 判据与准入仍以 [CHARTER §4](../../../../CHARTER.md#4-素材准入material-gate) 和 [05 SCOPE](../../../../deliverables/10-production-landscape/SCOPE.md) 为准；本页只排做什么、按什么算成。

## 0. 诊断：一句话

**05 的证据池与仓库自己的证据库是断开的。** 05 的 5 条 admitted/probation 全部来自 `src/web/`（talk、公司博客、厂商页、采购），**0 条来自 `src/papers/`**——而 `src/papers/` 里已经有一篇 `admitted` 的 **Apple 生产系统**（Glyph：3.4M 列 / 98,000 表 / 275 叶敏感性本体 / 6 周生产 steward 接受率 63.3%→99.8%）和一篇 `admitted (probation)` 的工业本体试验台（Narrow and Deep）。同时，2026-06 后 arXiv 还有一批未评的工业/企业论文，其中 **CoeusBI（百度，VLDB 2026）**有生产规模 + 量化效果 + 失败披露。

所以缺口不是「外部没有」，是：**（a）已过门的论文没接进 05；（b）新论文没扫、没评。**

## 1. 目标（DoD）

| # | 目标 | 完成判据 |
|---|---|---|
| P0-1 | **Glyph（Apple）接入 05** | 06.1 新增一条 A 案例、03.5/00/README/90.1 同步；数字可追到 `src/papers/2609.10430-glyph/digest.md` |
| P0-2 | **Narrow and Deep 定位** | 不作生产案例；进 08/90.3 作「工业侧只有真实试验台、无企业级生产复盘」的证据 |
| P0-3 | **CoeusBI 新准入** | `src/papers/2606.15384-coeusbi/`：card + digest + PDF + manifest 登记；`admission: admitted`（I1 VLDB + I2 多机构）；05 的 04/06/90 回写 |
| P1 | **四篇候选论文评估** | AstraZeneca / UniDataAgent / Auditable by Construction / Same Context：过门建卡，不过门进 frontier，每篇一句判定 |
| P2 | **微观缺口** | QCon PPT 取到/取不到都写清；Medact FOI 原始数据；江西 <50 万口径——拿得到就补，拿不到就标 |
| P3 | **结构缺口** | 05 加「收益侧」一小节；「底座可叠加」补一个真实例子或标推测；欧洲/其他地区标显式 gap |
| 收口 | 记录 | `check_repo` 0 error；state / state-log / `_plans/README` / 质量评估更新；E-28/E-29 若改，先改上游 |

## 2. 执行顺序与判据

### P0-1 Glyph 接入（不改准入，只改覆盖）

- 读 `src/papers/2609.10430-glyph/digest.md` 的 §4–§6，取：规模（3.4M 列/98K 表/4 业务线/3 后端）、效果（接受率 63.3%→99.8%，~24,000 对）、失败/限制（documentation debt、不能读值、标签偏斜、融合只 +0.010、无 OOD）、机制（三策略 + RRF + 275 叶本体）。
- 落点：`06-cases` 主台账新增一条；`03-us` 的「美国证据三条差异」改四条；`00`/`README` 的证据配比从 5 条改 6 条；`90.1` 加一行并链 digest（论文一律链 digest，不链 card）。
- **判断影响**：Glyph 是**治理标签本体**（长在数据目录上），不是「底座 + 薄本体」，也不是 OWL 塔。它**加厚**「本体在生产里以多种薄形态出现」，但**不改变**「企业级通用本体 A 类 = 0」。若要在 02.2 加第六种形态，必须同时改图注并说明图不排序；**本轮先不加形态，只在 02.1 加一句注**。

### P0-2 Narrow and Deep

- 只作「工业侧证据天花板」：真实试验台、9 任务、4 模型、投影 +19.8pp；**不是企业生产部署**。
- 落点：`08 §8.2` 缺口 2/6 的「现状」列、`90.3` 一行。不进 06 主台账。

### P0-3 CoeusBI 新准入

- 先核 PDF（已下 `/tmp/coeus.pdf`）：作者单位、部署规模原文、数据集表、效果数、失败段、作者局限。
- 卡：`src/papers/2606.15384-coeusbi/card.md`（按 [paper-card](../../../templates/src/paper-card.md)）；digest：按 [paper-digest](../../../templates/src/paper-digest.md)，`quality: B`（单公司、单系统、无成本账本）。
- 准入：`admission: admitted`，`impact_evidence: "I1: VLDB 2026 accepted; I2: Baidu + 高校"`；`venue: PVLDB 2026 (accepted; arXiv comment)`，并在卡上标「PDF 里 PVLDB 卷期是模板占位，camera-ready 未核」。
- 回写：`04-china` 的「百度只有厂商材料」句、`06.1` 台账、`90.1`、`90.3`（arXiv 阴性改阳性）、`E-30`/`F10` 的表述（**先改上游**）。
- **判断影响**：CoeusBI 是 BI 语义层（不是 OWL 本体）；它加固「生产里跑的是语义层」，不改变「通用本体 A 类 = 0」。它的失败（JOIN/宽 schema/方言/多轮成本）是**消费侧**失败，不并入 E-29 的语义/权限失败，另立一句。

### P1 四篇候选（每篇 ≤3 个判断）

1. AstraZeneca Research Assistant（2608.12395）——具名药企；看是否给使用规模/限制；无 → frontier。
2. UniDataAgent（2609.27257）——本体接地的企业问报；看客户名/规模。
3. Auditable by Construction（2608.20661）——企业金融本体分析；看是否生产。
4. Same Context（2610.20959）——语义层开关受控研究（7 模型/1,514 任务）；**只作 G6 的学术对照**，不作生产证据。

判据：`admitted` 需 I1–I3 至少一条 + 规模/失败；单公司自述 → `signal` 进 frontier；无量化 → 不建。

### P2 微观

- QCon PPT：`ppt.infoq.cn/list/173` 是 JS 页；找其 XHR/API；取不到就在 90.3 写「页面为 JS 渲染，未能取到」。
- Medact FOI：找 medact.org 的 FOI 数据集/报告；拿到就把 NHS 从「媒体」升到「FOI 一手汇总」。
- 江西口径：找招标/采购需求文件；拿不到就维持「口径未说明」。

### P3 结构

- 05-economics 加 5.7「收益侧：为什么现在算不了」：列已有自报收益（江南 1,200 工时、江西 −90%、京东 94.2%），说明为什么不能当 ROI（无对照/无归因/无审计），并把它接到 5.5b 的 gap。
- 「底座可叠加」：找真实例子（中泰 OKF + 指标/血缘；Snowflake 语义层 + dbt）；找不到就标 `推测`。
- 欧洲/其他地区：90.3 与 08 明确「除采购记录外无案例」。

## 3. 停 / 不做

- 不重画图；不加形态（除非先改图注）；不写代码；不用厂商材料填缺口。
- 论文过不了 G3 的不硬升 `admitted`；单作者/单机构一律 `signal`。
- 同一检索面两轮无增量 → 记阴性收手。

## 4. 预算

- 轮次：60。
- 论文评估：每篇 ≤4 轮；建卡 ≤6 轮。
- 每改一个判断，先改 `topics/` 再改 05。

## 5. 进度

| 阶段 | 状态 | 备注 |
|---|---|---|
| 计划落盘 | done | 2026-11-12 |
| P0-1 Glyph | done | 06.1 #6（A probation）、00/03.5/02.1/90.1；上游 E-28/E-29/L18/L19 加「权限前置限制语义生产」 |
| P0-2 Narrow and Deep | done | 只作工业侧上限：08.2 缺口 6、90.3 一行 |
| P0-3 CoeusBI | done | card+digest+paper+references+appendix+README；manifest #11；05 判 A；04 4.4.8、06.1 #7、90.1 #7、E-30/F10/L20 |
| P1 四篇 | done | UniDataAgent 过门（manifest #12，05 A；复核时补核 ICDM 2026 Demo，由 probation 升 admitted），04 4.4.9、06.1 #8；AstraZeneca → signal（06.1b/frontier）；Same Context → 学术对照（90.3/frontier）；Auditable → frontier（不建卡） |
| P2 微观 | done | QCon PPT：中泰有但需登录、小红书无；Medact 被 Cloudflare 挡；江西采购公告未查到 |
| P3 结构 | done | 05.5c 收益侧；8.2 缺口 8（非中美）；02.1 叠加例子 |
| 收口 | done | check_repo 通过（550 md / 12 论文）；state/state-log/_plans 已更新 |
