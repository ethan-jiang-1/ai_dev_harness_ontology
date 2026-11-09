---
status: draft
updated: 2026-11-09
type: work-plan
target: deliverables/01-capability-status 的 E1–E9
---

# D1 证据补齐计划：从 E1–E9 倒推 topics / src

> **这是工作计划，不是结论。** 它把 [01 现状](../01-capability-status/README.md) 末尾的 9 条「期待」当成验收规格，倒推：
>
> 1. `topics/` 现在能支持到哪一步；
> 2. 链上断点在哪；
> 3. 哪些能在现有 digest/代码里补，哪些必须新增 `src/`；
> 4. 补完之后 D1 应该变成什么样。
>
> **边界**：只做 desk research 与代码阅读；不设实验、不请求客户资产、不跑模型被试。新增来源只在「会改变某条判断」时入档（AGENTS 的三条入库判定）。

## 0. 一页结论

- D1 的 9 条期待里，**3 条已有可复用证据**（E1/E2/E6），但都限单域/专有数据；**3 条有证据但缺关键数**（E3/E4/E5）；**3 条基本没有证据**（E7/E8/E9）。
- 最该先补的**不是新论文**，而是现有 digest 里没抽出的数：POLAR 的 blocked log/tier、CAI 的 `p_h` estimator、Ontology Catch 的 FP/FN 表、FIRME 的分域表。
- 真正需要新 `src/` 的只有三类：**第二个 read-path 实现**、**commit gate 实现/false-defer**、**跨运行确定性**。前两类可以扫开源；第三类很可能扫不到，保持 `unknown`。
- 预期 3–4 周 desk research；产出：2–4 篇新 digest、1–2 个代码级核对、3–5 条 E 的修订/新增、D1 的 §2/§5/§9 重写。
- **D1 的完成标准不是 9 条都 supported，而是 9 条都有 verdict。** 找不到就写 `unknown`，不把「没找到」写成「无效」。

## 1. 先定义「支持」是什么

| verdict | 含义 | 需要什么 | 不允许写成 |
|---|---|---|---|
| `supported` | 有 ≥1 条一手证据，边界清楚，可反查 | digest/代码 + E 级结论 + 限定 | 「已证」 |
| `supported（限定）` | 有一手证据，但只覆盖单域/单设置 | 同上 + 明确限定 | 跨域规律 |
| `conditional` | 机制/公式成立，但差本地参数 | 公式 + 参数来源 | 「部署有效」 |
| `unknown` | 没有一手证据 | 说明找过哪里 | 「无效」 |
| `contradicted` | 有反例，且能指出限定 | 反例 + 边界 | 「永远不行」 |

每条期待最终必须带四样东西：**verdict + evidence pointer + boundary + what would change it**。这就是 D1 的验收规格。

## 2. 覆盖审计：E1–E9 × topics × src

> 「链」指 `D1 期待 → E-xx → topics 子主题 → digest/代码 → 论文/项目`。断点 = 这条链上缺的那一环。

| # | 期待（简） | topics 现在能给什么 | 链上断点 | src 里已有什么 | 需要新 src？ | 优先级 |
|---|---|---|---|---|---|---|
| E1 | K1 在目标域 ≥ +10pp | E-12；[03/projection](../../topics/03-knowledge/projection/README.md)；N&D | 单工厂、9 任务；无跨域 | N&D digest/paper | 低：先抽分任务表；跨域大概率扫不到 | P2 |
| E2 | 投影 ≥ +5pp、≤60k | E-12；[03/projection](../../topics/03-knowledge/projection/README.md)；N&D | 单工厂；顺序敏感；无多设备 | N&D digest/paper | 低：同 E1；投影粒度候选可看 | P2 |
| E3 | `p_h ≥ p_min` | E-08/E-14；[03/compilation](../../topics/03-knowledge/compilation/README.md)；CAI | 缺自己的 `p_h`/miss/`c`/`Q`；43% 是反推 | CAI digest/paper §8.6 | 中：企业 RAG 复盘；Grep 候选 | P1 |
| E4 | catch ≥5pp、FA ≤15% | E-02；[02/checker](../../topics/02-judgment/checker/README.md)；Catch | 缺自己的故障分布；false-veto | Catch digest/paper Tables 4–6 | 中：LogT / CORE-LLM-Bench / judge 校准 | P1 |
| E5 | false-veto ≤5%、harm 降 | E-04/E-13/E-15；[01/action-gate](../../topics/01-constraint/action-gate/README.md)；POLAR/CASEL | **false-veto 无标签**；T1-only 未配对 | POLAR digest/paper；CASEL digest | 高：What Can Be Enforced? / Safety monitors / 审批疲劳 | **P0** |
| E6 | CMR/Acc@complete +10pp | E-05/E-17；[04/memory](../../topics/04-state/memory/README.md)、[identity](../../topics/04-state/identity/README.md)；FIRME/EvoMem | 专有/文本 only；无跨域 | FIRME/EvoMem digest/paper | 中：APEX-MEM / KROMA | P1 |
| E7 | 读路径 object 方向不泄漏 | E-20；[01/commit-gate](../../topics/01-constraint/commit-gate/README.md)；trustgraph | **只有 1 个独立实现**；fail-open | trustgraph 代码 | 高：扫第二个 SHACL/策略过滤实现 | P1 |
| E8 | 写路径 false-defer ≤20% | E-20 否定证据；[01/commit-gate](../../topics/01-constraint/commit-gate/README.md)；Commit Boundary | **无实现、无 false-defer** | Commit Boundary 概念 | 高：扫 commit gate/写授权实现 | **P0** |
| E9 | 跨运行收敛可度量 | 无 E；[04/determinism](../../topics/04-state/determinism/README.md) | 设计提案；无度量 | 无 | 高：扫重复运行/漂移度量 | P2 |

**先做 P0 的理由**：E5/E8 是 D1 里「B 可试点」和「C 只能设计」的分界；它们的 verdict 一变，§2 能力地图的 A/B/C 就要改。其余 E 更多是补限定，不会改变分层。

## 3. 从现有 digest 里能直接补的（不新增 src）

> 这些是「已经入库、但没抽到 D1 需要的那一栏」的数。先做这一层，成本最低，也最符合「下游倒逼上游」。

| # | 去哪个 digest/正文找 | 抽什么 | 产出 | 验收 |
|---|---|---|---|---|
| H1 | POLAR digest + `paper.md` 附录 B.3 | blocked log 的规模/域/动作类型；tier retention；T1-only 与 full 的差异 | 一页「E5 数据表」：哪些能标 false-veto、哪些不能 | 能回答「false-veto 能否从已发表数据估出」；不能就写 unknown |
| H2 | CAI digest + `paper.md` §8.6 | `p_h` estimator、hit/miss 分布、`c`/`Q` 定义、时延口径 | 一页「E3 数据表」：公式 + 可代入参数 + 不可代入项 | 能算出 `p_min`；能说明 43% 是反推 |
| H3 | Ontology Catch digest + `paper.md` Tables 4–6 / Appendix D | 三源 catch/FA、precision 口径、25% 假设、per-flag 成本、LLM judge 净修复 | 一页「E4 数据表」：prior + 自己的缺口 | 能区分「已发表 prior」与「部署估计」 |
| H4 | FIRME/EvoMem digest + `paper.md` 分表 | CMR/merge precision/Acc@complete 的分域、样本量、口径 | 一页「E6 数据表」：可复用/不可复用 | 能说明跨域为什么不能直接搬 |
| H5 | trustgraph 代码 + 单测 | object 方向、fail-open、首命中、缓存 | 一页「E7 代码核对」：已验证/未验证 | 能指出「读路径 best-effort」的具体边界 |
| H6 | semantica / open-ontologies 代码 | 派生 shapes vs 手写；三态折叠 | 一页「E4/E8 代码旁证」 | 能说明「执行 ≠ 授权」 |

**规则**：H1–H6 只改 `topics/` 的 findings/claims 或 D1 的限定；**不新增 E**，除非抽出的数改变了某条 E 的边界。改变边界才升 E，并按 [conventions](../../meta/conventions.md) 登记。

## 4. 需要新 `src/` 的（按优先级）

> 入档判据：会改变 E1–E9 中至少一条的 verdict，或能关掉一个 P0 断点。只「相关」不入档。

### P0-A｜false-veto / 误拦（E5）

- **要找什么**：报告 false-block/false-veto、blocked log 标注、或「本可合法执行」比例的工作；理论边界也可以，只要能给出可操作的判定。
- **候选**：`What Can Be Enforced?`（2607.22868，摘要已读）、`Safety monitors for agentic systems`（2610.20960，待扫描）、POLAR 引用链、CASEL 部署版、`human approval fatigue agent guardrail`。
- **验收**：有一手 false-veto/误拦数，或给出可复现的标注协议；只有理论 → 入候选，不升 E。
- **停止**：两轮扫描仍无一手数 → E5 的 false-veto 保持 `unknown`，不拿 retention 代算。

### P0-B｜commit gate 实现 / false-defer（E8）

- **要找什么**：单次写/落盘前的授权实现；能报 false-defer 或至少报「正确变更被 defer」的比例。
- **候选**：`commit boundary implementation entity resolution`、`knowledge graph write authorization`、`entity resolution commit gate`、`deferred mutation queue re-entry`；开源侧扫「KG write policy / SHACL write gate / MDM commit gate」。
- **验收**：有实现 + 可指到代码/接口 + false-defer 或审计字段；只有概念 → 保持 `C 只能设计`。
- **停止**：两轮无实现 → E8 写 `unknown/无实现`，D1 不改分层。

### P1-A｜第二个 read-path 实现（E7）

- **要找什么**：独立于 trustgraph 的「检索结果返回前按本体/策略过滤」实现。
- **候选检索式**：`SHACL access control`、`ontology-based access control`、`policy filter SHACL`、`read path authorization knowledge graph`。
- **验收**：≥2 个独立实现；有外部判据 + 阻断 + 位置明确；能测 object 方向。
- **停止**：只有 1 个 → `read-path` 保持轴外，不升第七时刻。

### P1-B｜checker 校准 / 真实错误分布（E4）

- **要找什么**：同时报 catch/FA + 真实 agent 错误分布 + 净修复（fixed − corrupted）的工作。
- **候选**：LogT（2510.01530）、CORE-LLM-Bench（Zenodo 2026）、`Can We Trust LLM Judges`（2609.12002）、`checker false positive deployment trace`。
- **验收**：能给 D1 的 E4 补「真实错误分布」或「净修复」；只有 benchmark 分数 → 候选。
- **停止**：没有真实 trace → E4 保持 `supported（限定）`，不写成部署估计。

### P1-C｜记忆跨域（E6）

- **要找什么**：FIRME/EvoMem 之外的跨域记忆状态证据；最好有 CMR/Acc@complete 同口径。
- **候选**：APEX-MEM（2604.14362）、KROMA（2507.14032）、`registry anchored memory graph`、`temporal entity alignment agent memory`。
- **验收**：能改变 E-05/E-17 的跨域限定；或给出同口径新数。
- **停止**：只有单域 → 保持 `supported（限定）`。

### P2-A｜跨运行确定性（E9）

- **要找什么**：同一输入重复运行的收敛/漂移度量；本体作为锚点的实现。
- **候选**：`agent determinism repeated runs`、`agent output consistency drift`、APEX-MEM、`Time is Not a Label`（2604.11544）、`AriadneMem`（2603.03290）。
- **验收**：有可复算的漂移指标；只有设计 → 保持 `unknown`。
- **停止**：两轮无实证 → E9 保持 `unknown`，D1 不改写。

### P2-B｜K1/投影跨域（E1/E2）

- **要找什么**：N&D 之外的独立域复现；投影长度/顺序/多设备的对照。
- **候选检索式**：`ontology projection industrial maintenance replication`、`domain ontology projection context`、`ontology tower evaluation`。
- **验收**：独立域 + 同口径 trap/element；否则保持 `supported（限定）`。
- **停止**：找不到 → 明确写「单工厂，跨域未知」，不硬凑。

## 5. 任务分解（WBS）

| ID | 任务 | 输入 | 输出 | 依赖 | 估算 |
|---|---|---|---|---|---|
| W0 | 审计与排期 | D1 §9、topics 六派 README/frontier | 本计划；E1–E9 的 verdict 目标 | — | 1–2 人日 |
| W1 | 现有 digest 回抽 | H1–H4 | 4 张「数据表」；更新 findings/claims | W0 | 4–5 人日 |
| W2 | 代码级核对 | H5–H6 | 2 页代码核对；更新 execution-forms/commit-gate | W0 | 2–3 人日 |
| W3 | P0 源扫描 | E5/E8 候选 | go/no-go 记录；1–2 篇落盘或明确不落 | W1 | 3–5 人日 |
| W4 | P1 源扫描 | E4/E6/E7 候选 | 1–3 篇落盘/建卡/消化 | W1 | 4–6 人日 |
| W5 | P2 源扫描 | E1/E2/E9 候选 | 候选队列更新；不强行入档 | W1 | 2–3 人日 |
| W6 | 综合与升 E | W1–W5 | 3–5 条 E 修订/新增；claims 回写 | W3–W5 | 3–4 人日 |
| W7 | 重写 D1 | W6 | §2/§5/§9 的 verdict + 边界 | W6 | 2–3 人日 |
| W8 | 交叉核对 D2/D3 | W7 | D2 的 stop/验收、D3 的边界同步 | W7 | 1–2 人日 |
| W9 | 自检与台账 | 全仓 | `check_repo.py` 通过；state 更新 | W8 | 1 人日 |

> 估算是 desk research 的量级，不是承诺；如果某个 P0 扫不到，W3 提前结束，把时间让给 W6/W7。

## 6. 排期（建议 3–4 周）

| 周 | 主任务 | 周末交付 | 决策点 |
|---|---|---|---|
| 第 1 周 | W0 + W1 | 4 张数据表 + E1–E9 现状审计 | 哪些 E 只需改限定，哪些必须新源 |
| 第 2 周 | W3 + W2 | P0 go/no-go；代码核对 | E5/E8 是否有可入档来源 |
| 第 3 周 | W4 + W5 | P1/P2 的入档/候选决定 | 是否新增 2–4 篇 digest |
| 第 4 周 | W6 + W7 + W8 + W9 | D1 v2 + 台账 | 9/9 verdict；checker 通过 |

**缓冲**：每个 P0 最多两轮扫描；两轮无果就写 `unknown`，不拖到第 4 周。

## 7. D1 补完之后长什么样

1. **§2 能力地图**：每行加 `verdict`（`supported` / `supported（限定）` / `conditional` / `unknown` / `contradicted`）与 evidence pointer；A/B/C 分层只在 verdict 改变时改。
2. **§5 距离表**：每条缺口标「已关 / 部分关 / 仍开」，并写「关它需要什么」；不再只写「需仓库外」。
3. **§9 期待表**：每行填 verdict + boundary + what would change；`unknown` 不再被读成「无效」。
4. **新增/修订 E**：只有 W6 的综合能升 E；每条带 digest 出处、等级、限定；不把设计提案升 E。
5. **D2/D3 同步**：D2 的 stop/验收表随 verdict 改；D3 的 15 条边界随新证据改；不改就说明「未受影响」。
6. **台账**：`topics/conclusions.md`、各派 `claims.md`、`meta/state.md`、D1/D2/D3 的 `updated` 同步。

**完成判据（DoD）**：

- [x] E1–E9 每条都有 verdict，且 verdict 后有 evidence pointer。
- [x] 所有 `unknown` 都写了「找过哪里、为什么没找到」。
- [x] 新增 E 都有 digest/代码出处 + 限定；没有「概念升 E」。
- [x] D1 §2 的 A/B/C 与 §9 的 verdict 不矛盾。
- [x] D2 的 stop 线、D3 的边界与 D1 一致。
- [x] `python3 meta/tools/check_repo.py` 通过；`meta/state.md` 更新。

> **2026-11-09 第一轮完成**：E5 false-veto / E8 commit gate 仍 `unknown`，但已从「没有评测方法」推进到「有授权 benchmark + false-block/miss 前沿」；E7 仍缺第二个 read-path；E9 仍缺本体锚点实现。下一轮可继续这些 P1/P2，不阻塞 D1 的 verdict。

## 8. 停止规则与反模式

- **没找到 ≠ 无效。** `unknown` 是合法 verdict；不要用「没有证据」推「没有效果」。
- **不要用 retention/block count 代算 false-veto。** 没有 harm/授权标签就是没有。
- **不要把概念架构升 E。** Commit Boundary、determinism 目前都停在设计。
- **不要为填表加论文。** 先问「它会改变哪条判断」；答不出就不入档。
- **不要跑模型实验、不要请求客户资产。** 本仓库只做 desk research 与代码阅读；需要实验的，标 `仓库外`。
- **不要为了「完整」把 D1 写成 9 条都 supported。** 那样会重演「把推测写成既成事实」。
- **两轮无果就停。** P0 扫不到就记录「无一手来源」，把时间让给能关的 E。

## 9. 未来 3 天的具体动作

1. **H1**：读 POLAR digest + `paper.md` 附录 B.3，抽 blocked log/tier；写「E5 数据表」，回答「false-veto 能不能从已发表数据估」。
2. **H2**：读 CAI `paper.md` §8.6，抽 `p_h` estimator、hit/miss、`c`/`Q`；写「E3 数据表」。
3. **H3**：读 Ontology Catch Tables 4–6/Appendix D，抽三源 FP/FN、成本、judge 净修复；写「E4 数据表」。
4. **H4**：读 FIRME/EvoMem 分表，抽 CMR/merge precision/Acc@complete 的域与样本；写「E6 数据表」。
5. **P0 扫描**：`What Can Be Enforced?`（2607.22868）+ `commit boundary implementation` 两条检索；各写 5 行 go/no-go。
6. 把 1–5 的结果贴回本计划 §3/§4 的对应行，更新 verdict 目标；不要先改 D1 正文。

> 3 天后的检查点：4 张数据表是否都能回答「这条期待现在是什么 verdict」；P0 是否有一条可入档来源。若否，进入「两轮无果」分支。

## 10. 缺口 → frontier（支持层指针）

> 这一节把 D1 的期待接到 `topics/` 的缺口页。反向链走完 E → digest 后，缺的数在这里找；**不要新开索引**，`frontier.md` 的 G/N 就是缺口账本。

| 期待 | 缺口 | 去哪 |
|---|---|---|
| E1 / E2 | 跨域、投影长度/顺序、多设备 | [03/projection/frontier](../../topics/03-knowledge/projection/frontier.md) G1/G2/G5；[03/frontier](../../topics/03-knowledge/frontier.md) |
| E3 | 企业 `p_h`/miss、φ、维护成本 | [03/compilation/frontier](../../topics/03-knowledge/compilation/frontier.md) G1/G2/G4 |
| E4 | 真实错误分布、净修复、校准 | [02/checker/frontier](../../topics/02-judgment/checker/frontier.md) G1/G3；[02/calibration/frontier](../../topics/02-judgment/calibration/frontier.md) G1/G2 |
| E5 | false-veto、T1-only 配对、审批疲劳 | [01/action-gate/frontier](../../topics/01-constraint/action-gate/frontier.md) G1/G3/G4 |
| E6 | 跨域、false merge 传播/回滚 | [04/memory/frontier](../../topics/04-state/memory/frontier.md) G5；[04/identity/frontier](../../topics/04-state/identity/frontier.md) G1/G2 |
| E7 | 第二个 read-path 实现、object 方向 | [01/commit-gate/frontier](../../topics/01-constraint/commit-gate/frontier.md) G1；[src/open-source/README](../../src/open-source/README.md) 状态表 |
| E8 | 实现、false-defer、重入协议 | [01/commit-gate/frontier](../../topics/01-constraint/commit-gate/frontier.md) G1/G3/G4 |
| E9 | 跨运行收敛度量 | [04/determinism/README](../../topics/04-state/determinism/README.md) 开放问题 |

**用法**：如果某个期待找不到 frontier 指针，说明它的缺口还没被登记；先补 `frontier.md` 的 G/N，再谈补 `src/`。这是「支持层先落地」的顺序。

## 11. 进度（2026-11-09 第一轮）

| 项 | 状态 | 产出 |
|---|---|---|
| H1 POLAR | 完成 | [e5 数据表](../01-capability-status/data/e5-false-veto.md)：1,745 blocked 无标签；false-veto `unknown`；保留率/tier 已抽 |
| H2 CAI | 完成 | [e3 数据表](../01-capability-status/data/e3-compilation.md)：`p_min` 公式、43% 是反推、φ 未测、门实现不一致 |
| H3 Catch | 完成 | [e4 数据表](../01-capability-status/data/e4-checker.md)：data-derived 在 UniProt 真实答案上过 +5pp/FA≤15%；curated FA 16.8% 超线 |
| H4 FIRME/EvoMem | 完成 | [e6 数据表](../01-capability-status/data/e6-memory.md)：alias +7.8–12.1pp；非全部设置过 +10pp/90%；跨域未知 |
| H5/H6 代码 | 完成（只读，未重跑） | [e7/e8 代码](../01-capability-status/data/e7-e8-code.md)：trustgraph 只删 subject、fail-open；四项目无写授权 |
| P0 源扫描 | 完成（摘要级） | [P0 扫描](../01-capability-status/data/p0-source-scan.md)：2610.16838（授权 benchmark，go）、2607.22868（false-block/miss 前沿，go）；无 commit gate 实现 |
| P0 入档 | 完成 2 篇 | [2610.16838 digest](../../src/papers/2610.16838-same-operation-different-permission/digest.md)（L2；harness-evidence / none）；[2607.22868 digest](../../src/papers/2607.22868-what-can-be-enforced/digest.md)（L2；harness-evidence / none）；均不升 E；manifest 24 篇 |
| E5 校准理论 | 完成（已入档 L2） | [e5 校准理论](../01-capability-status/data/e5-calibration-theory.md)：NP false-block/miss 前沿；δ=.05 时每个 judge 都 block-all；δ=.10 false block .78；false-veto 应报前沿不是单点 |
| P1/P2 源扫描 | 完成（摘要级） | [P1/P2 扫描](../01-capability-status/data/p1-p2-source-scan.md)：无第二个 read-path；E9 有 Suite v0 候选（harness 级）；E1/E2 无跨域复现 |
| D1 verdict | 完成第一轮 | [01 §2.4](../01-capability-status/README.md#24-e1e9-verdict2026-11-09-第一轮) 与 [§9](../01-capability-status/README.md#9-期待与数据需求验收规格)：5 条 `supported（限定）`、1 条 `conditional`、3 条 `unknown` |

**下一步（按 P0）**：

1. 落盘 2610.16838，建卡 + L2 digest；抽 false-block/authorized-pass；决定是否改 E5/E8 的 verdict。
2. 读 2607.22868 正文的 false-block/miss 前沿与校准；若可复用，写进 E5 的边界，不急着升 E。
3. 继续扫第二个 read-path 实现（P1）；没有就保持 `unknown`。
4. 把新证据回写 `topics/` 的 frontier/claims，再回改 D1/D2/D3 与 `meta/state`。
