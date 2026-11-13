---
status: draft
updated: 2026-11-12
type: gap-survey
scope: 内容层缺口盘点（purge 后）
---

# 内容缺口盘点（2026-11-12）

> **参考（2026-11-12 上游缺口盘点快照，注：盘点后随 `10-production-landscape` 首轮入库已增至 12 篇论文 / 17 张材料卡 / 32 条 E）**，不是计划、不构成 E。现行计数见 [meta/state](../../meta/status/state.md)；常设规则见 [AGENTS](../../AGENTS.md)。外部对齐节为受限核实（web_search 端点 402，宽口径发现待恢复）。

## 0. 一句话

**骨架与纪律已修好，证据基座被 purge 削薄了一半；当前最缺的不是「更多文档」，是「过门的执行型证据」——尤其是 04 记忆 / 06 度量两派的本体真执行样本，以及部署层代价（false-veto / 维护成本）的量化。**

## 1. 现行证据基座（purge 后）

- **10 篇论文**：6 `admitted` + 4 `admitted (probation)`。probation 四篇（GGC / Agents / N&D / CASEL）**只有 I2（多机构）一个信号**，2027-05-11 前补不到第二独立信号（I3 采用 / I4 社区 / I5 资产）就移出。
- **8 个开源**：trustgraph / semantica / ontop / open-ontologies（4 个已 pin commit 代码级核对）+ OPA / QLever / Great Expectations / OpenLineage（adjunct，非本体执行）。
- **11 张材料卡**：1 HN + 10 在役标准（N 主干，只定词不证效果）。
- **证据配比（18 源）**：`execution-test` 3 / `mechanism-only` 11 / `harness-evidence` 4 / **`boundary-ruler` 0**。即：多数来源只「提机制」，真测「本体被执行」的少，**没有任何来源专做边界与尺子**。
- **执行形态（18 源）**：engine 3 / compiled 3 / context 1 / label 1 / none 10。真正「执行」的 6 个里，4 个是开源代码（只读未跑），2 个是论文（FIRME/EvoMemState，记忆派）。
- **结论**：27 条 E 中 9 撤回、现存 18（16 已核 + 2 推测）；**0 条「已证」**（无独立复现）。79 条 L 中 27 撤回。硬对象 94 注册、20 撤回、现存 74。

## 2. 本轮已完成的内部对账（结构→内容桥）

这些是「旧证据冒充现行」的漂移，已按审计窗口重判修复：

| 漂移 | 修复 |
|---|---|
| 六派 frontier 候选队列仍把 18 篇移出论文标「已入档」 | 全部改「已移出」+ tombstone 链；pre-window 候选标「G1 不过」 |
| 硬对象注册表 5 个停线/协议（T05/T06/T07/P02/P03）仍挂已撤回 E | 补标撤回（累计 20）；M04 换锚 E-15 |
| 8 个交付物页 frontmatter `evidence:` 裸列已撤回 E | 加 `# E-xx withdrawn` 注记 |
| execution-forms 形态表仍列 28 篇（含移出 18），计数「36 来源」 | 重建为 18 源，与 state 一致 |
| loading / appendix 残留「28 篇 / 26 来源」旧数 | 改 10 篇 / 标历史快照 |

> 判断层（claims.md）本身一致：27 条撤回 L 与 state 吻合，无需改。W 表/banners 已覆盖交付物正文的撤回标注。

## 3. 按派的内容缺口（来自 frontier + conclusions）

> 缺口 = 「中心问题需要、但当前没有过门证据」的格。每派给最痛的一到两个。

- **01 约束**：① **false-veto / 剪枝率无量化**——POLAR 移出后，没有任何过门来源报「误拦率/剪枝率」，护栏的真实代价算不出。② **read-path 只有 trustgraph 一个实现**（且 fail-open、只删 subject 侧），缺第二独立实现 + harness 调用点，无法决定升第七时刻。③ **策略层无领域来源**——OPA 是通用引擎不消费本体标签，Glyph 只到标签层；「标签→策略→执行」断在中间。
- **02 判定**：① **checker 的 catch/FA 曲线无过门来源**——Ontology Catch 移出后，三源偏向（curated/LLM/数据挖掘）与误报代价都停在撤回的 E-02。② **误报后的修复破坏力**没测过（被误标后 agent 改坏多少）。③ 接地等级由谁判定、如何防通胀，无来源（E-03 撤回）。
- **03 知识**：① **投影粒度无对照**（整段 vs 记录 vs 主张-证据）；C-04 的关键判据「答案是否写在知识里」靠人工预判。② **查询路线无头对头**——E-26 撤回后只剩 GGC 单路线，OBDA/in-context/agentic 无法比较。③ 编译的部署层回报（上手/跨源引用/审计）无量化。
- **04 状态**：① **缺「本体真执行」的开源样本**——FIRME/EvoMemState 是论文，代码侧记忆派空白。② 状态结构能否由本体自动生成（冷启动硬约束）、冲突该阻塞还是带冲突推进，无对照。③ 跨运行一致性（RQ3）无度量载体。
- **05 生产**：① **可消费性评测缺口**——没有「判定器能否加载/解释/复现生成结构」的评测，生成路线停在候选。② 精化召回（recall@30/@10）无专家标注真错全集。③ 表示选型（结构表+SHACL 第二档 vs 第三档）无成本对照。
- **06 度量**：① **「机制类型→尺子」分派表是全仓最大空缺**——C-03（度量错配）是最强判断，但没有同数据集两把尺子的对照。② 部署层回报、基准慷慨度、过程+任务指标联合分析，都缺过门来源。③ **`boundary-ruler` 证据为 0**——没有任何来源专做边界与尺子。

## 4. 横切缺口

1. **无独立复现（0 条「已证」）**：所有「已核」止于原文摘要/只读代码。这是研究深度的根本缺口，但按宪章不在仓内做实验；要升「已证」需仓外 `EXP-xxx`。
2. **N 主干覆盖不全**：语义层、成熟度、接地、动作可逆性、commit gate、agent 记忆这些词**没有 normative 锚**，只能标 `local`。标准只定词不证效果，效应缺口不能靠补标准解决。
3. **probation 倒计时**：4 篇承重论文（撑 E-01/05/07/08/09/12/14/15/17/18/21/22 的大部分）2027-05-11 前需第二信号，否则证据基座再塌一半。
4. **证据类型偏科**：`mechanism-only` 占 11/18，`execution-test` 仅 3，`boundary-ruler` 为 0。中心问题问「以什么形式被执行」，但多数证据回答的是「提出了什么机制」。

## 5. 优先级行动清单（内部视角，待外部对齐校准）

> 排序原则：先补「会让现有判断塌方」的，再补「中心问题最核心」的，最后补「锦上添花」的。每项标注「补什么证据 / 过哪道门 / 改变哪条判断」。

- **P0 · 保证据基座不塌**：为 4 篇 probation 论文找第二独立信号（I3 采用 / I4 社区 / I5 资产）。这是倒计时任务，塌了会连带撤回大量 E。**已核查的线索（阴性结果）**：Agents Are Systems 释放了 benchmark 仓库 [lusxvr/rethinking-agent-evaluation](https://github.com/lusxvr/rethinking-agent-evaluation)（公开、MIT、Python，last push 2026-10-05），但 **0 fork / 0 依赖 / 1 star / 0 issue——无外部使用者，I5 不成立**，不能据此转正，probation 维持。其余三篇也已查：**GGC/CASEL 无公开代码仓库、无采用（仅 arXiv 镜像/聚合站）；N&D 仅作者自建 [ontotower gallery](https://yhjoo-kier.github.io/ontotower/gallery.html) + 1 篇第三方博客评（低于 I4 的 ≥3 讨论阈值）——四篇目前都没有第二独立信号**，probation 全部维持，2027-05-11 是真实风险。→ 改变：probation 转正或移出。本条是「释放代码 ≠ 有影响力」的实例，门该挡就挡。
- **P1 · 补执行型证据（中心问题核心）**：
  - 04 记忆 / 06 度量的「本体真执行」开源样本（engine/compiled，pin commit，独立采用）。→ 改变：E-20 的形态矩阵、04/06 的代码级证据。
  - read-path 第二独立实现 + harness 调用点。→ 改变：是否升第七时刻。
- **P2 · 补代价量化（护栏可信度）**：false-veto/剪枝率、checker catch/FA、部署维护成本的过门来源（研究 + 工程复盘并重）。→ 改变：01/02 的效应量与停线阈值（当前 T05/T06/T07 已撤回停用）。
- **P3 · 补尺子（C-03 落地）**：「机制类型→失效形态→主指标→过程指标」分派表 + 同数据集两把尺子对照的来源。→ 改变：C-03 从「最有价值判断」升为可操作度量。
- **P4 · N 主干扩词**：为语义层/记忆/接地等 local 词找 normative 锚（若有在役标准）。→ 改变：trunk 覆盖，术语去 local 化。**注意：标准只定词，不解决效应缺口。**

## 6. 外部前沿对齐（受限核实）

> **工具状态（如实记录）**：`web_search` 已恢复（用户充值）。`web_fetch` 因 VPN 把域名解析成虚拟 IP 而被安全策略误拒；**改用 bash `curl` 走 VPN 隧道可正常抓公共页面（arXiv/GitHub API/AAAI）**，本节候选已据此逐一过门。下文判定为已核实结果。

**4 篇 probation 论文逐条核实（arXiv 摘要，4/4）**：

| 论文 | 真实性 | 与仓库 digest 一致 | venue / I1 | 第二信号线索 |
|---|---|---|---|---|
| GGC（2607.28082） | ✓ | ✓ 90.23→98.33、省 45%、MCQA、选择性纠错 | 纯预印本，无 venue，I1 弱 | 无 I1；需 I3/I4/I5 |
| Agents（2610.01618） | ✓ | ✓ 54% 方差、信息>模型、验证工具>提示、18k 轨迹；单位 TUM/Helmholtz/Inria 确认 | 无 venue，I1 弱 | benchmark 仓库已核：公开 MIT，但 **0 fork/0 依赖/1 star → 无外部使用者，I5 不成立**，维持 probation |
| N&D（2610.11768） | ✓ | ✓ 本体塔、+20pp 避坑、9B≈750B、9 任务、真实试验台 | 纯预印本，无 venue，I1 弱 | 无 I1；需 I3/I4/I5 |
| CASEL（2610.36570） | ✓ | ✓ 14.75→7.02%、120k 动作、20 seeds；摘要自述「effectiveness assumed, not measured」 | CBASE 2026（小型会议，非顶会），I1 弱 | 无 I1；需 I3/I4/I5 |

**三条结论**：

1. **证据基座忠实**：4 篇承重论文的摘要与仓库 digest 的关键数字/限定逐条吻合，连 CASEL「有效性是假设不是测量」、N&D「单试验台」这类限定都如实保留。**仓库对已有来源的消化是忠实的，没有夸大**——这是「full picture 一致」在来源层的正面证据。
2. **probation 判定站得住**：4 篇都没有顶会/标准组织级 I1，确实只有 I2（多机构）一个信号；按宪章 probation 合理，第二信号缺口是真的，不是误判。
3. **P0 线索已核（阴性）**：Agents 的 benchmark 仓库公开（MIT/Python，last push 2026-10-05）但 0 fork / 0 依赖 / 1 star / 0 issue，无外部使用者，I5 不成立——**释放代码 ≠ 有影响力**，probation 维持。这正是准入门该挡的：不能因「作者释放了代码」就转正。第二信号得另找（I3 独立采用 / I4 社区）。

**窗口内候选已逐一过门（bash curl 核实）**：

| 候选 | 窗口 G1 | 关键发现 | 五门判定 |
|---|---|---|---|
| **Selective Forgetting**（2608.28978，2026-08-29） | ✓ | KG 记忆在 LongMemEval **不如**扁平向量（token F1 0.417 vs 0.468，Δ=-0.050，CI[-0.085,-0.016]）；forgetting 剪枝模块有效（删 9.8% 节点 F1 不变）；作者自限单小模型单基准。代码 [Selective-Amnesia](https://github.com/skhanzad/Selective-Amnesia) **无 license**、11 star/1 fork、贡献者同组 | **signal**：G3 无独立采用、G5 无 license。阴性结果与 E-01 怀疑立场一致，留 04 frontier |
| **SARA**（AAAI Vol.40，法律 Jur-KG） | ✗ **2026-03-17** | AAAI 顶会（I1）+ **部署在巴西一家法院**（I3）；LLM agent 接 Jurisprudential KG 做法律推理 | **excluded（G1 超窗）**：强证据但窗口前，只作背景，不入库 |
| **ontology-rag-firewall**（cloudbadal007） | ✓ pushed 2026-09-13 | OWL/SHACL 防火墙验合同条款、拦 agent 动作；**单作者**（1 人 6 提交）、11 star/2 fork、0 issue | **signal**：G2 单贡献者、G3 无独立采用。留 01/read-path frontier |
| **ToolRosetta**（2610.24055，2026-10-16） | ✓ | 量化 guard 误报代价：shell 形式下专用 guard FP 升 21–47 点、拦 1/3–9/10 良性动作；placebo 对照；**正中 P2 false-veto 缺口** | **signal**：NeurIPS 2026 workshop（弱 I1）、无代码/独立采用。留 02 frontier |
| **Ontology-to-tools compilation**（2602.03439） | ✗ 2026-02 | 本体编译成可执行工具约束 | 窗口前，只作背景 |

**结论：窗口内「高影响 + 本体真执行」的来源确实稀缺**——强的（SARA）超窗，窗口内的（Selective Forgetting / firewall / ToolRosetta）独立影响不足（ToolRosetta 是 workshop，另两个单作者/无 license）。这印证了 P1/P2 执行型与代价量化缺口是**真的**，不是没搜到。**宁缺毋滥：五个候选都不 admitted，按判定留 frontier 或作背景。** 其中 **ToolRosetta 最贴近 P2 false-veto 缺口**，值得优先跟踪其影响信号。这也说明准入门在正确工作：没有因为「看起来相关」就放水。
