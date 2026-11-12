---
status: draft
type: strict-process-plan
result: executed（2026-11-12；S0–S6 已走完，见文末执行回执）
updated: 2026-11-12
target: deliverables/05-production-landscape/02-sections/04b-okf-wiki.md
scope: 05 · 4b（OKF/Wiki 底座）；上游 topics/06 与 src/web
---

# 04b OKF/Wiki 严格化：补证、拆层、收口

> **一句话**：4b 是二期“硬挤进去”的一节——它把**规范边界**、**映射可行性**、**采用/迁移证据**三件事混成了一条“OKF 可以靠向本体”的叙事，并夹带了没有上游、没有过门的源。本计划按[修复回路](../../AGENTS.md)把它拆回三层，逐句补证或降级，再回写。

## 0. 诊断：不是“写得不严谨”，是“三层混一层”

| # | 问题 | 证据 | 后果 |
|---|---|---|---|
| 1 | **无上游的源进了正文** | `SCIMIN` 在 `src/`、`topics/`、`frontier.md` 全无记录；`Linked.Archi` 无卡、无 frontier；`Kunstenpunt` 只是 [frontier](../../topics/06-measure/feasibility/frontier.md) 的 `signal`，却在 4b.4b 当“B 类反例”用；京东海博是 `signal`，却在 4b.3 用 AB 数 | 违反 [CHARTER §4.2](../../CHARTER.md#42-三档判定)：`signal` 不撑交付物 |
| 2 | **三层证据混成一条叙事** | ① Google 规范说“不是本体”（已核）；② 三个映射实现说“投影有损、lift 需人审”（工程文档）；③ 中泰/SCIMIN 说“有人在做”（采用/试点）。4b 把 ①②③ 写成“OKF → 本体”的一条路 | 把“可映射”读成“会自动长成”，把“设计判据”读成“已验证路径” |
| 3 | **伪精度** | 4b.6 的六个阈值（≥2 跳/反向查询 >20%、>10^4 concept、…）在任何上游都没有；“用户可观测的升级信号”也没有观测 | 读者会把它当实测门槛；实际是作者拍的数 |
| 4 | **定位漂移** | 05 的 SCOPE 是“现状·实证”；W0–W3 阶梯与升级判据是 recipe/判断，已在 [mechanism](../../topics/06-measure/feasibility/mechanism.md#okf-2026-11) 有一份 | 同一判断两处维护，且 05 越界替 02/07 回答“怎么做” |

**根因**：这一节没有走“先上游、后下游”。它先写了正文，再回头找材料；找不到的（SCIMIN、Linked.Archi）就用记忆补，找得到的（Kunstenpunt、京东）就越级用。

## 1. 这次要回答的三个真问题

- **Q1 规范边界**：Google 自己把 OKF 的边界划在哪？（已核：SPEC v0.2 的 non-goals、词频、§12.3、无执行/无 ACL）
- **Q2 映射机制**：从 OKF 到本体，实际能自动到哪一步、哪一步必须人审？（**新证据**：三个独立实现 + 一个本体先行的生产型案例）
- **Q3 迁移证据**：有没有组织真的完成“OKF/Wiki → 本体”？没有的话，现有案例是哪个方向？（**新证据**：SCIMIN 是本体先行；中泰是 OKF 先行、本体在验证；没有完成迁移的公开案例）

> Q2/Q3 是用户指出的“靠向本体这一块”。4b 现在把 Q1 的答案（不是本体）和 Q2 的答案（可投影）拼成了 Q3 的答案（可以升级）。**拆开之后，Q3 的答案是“没有已完成案例，只有两个方向的设计与试点”。**

## 2. 已找到的关键材料（2026-11-12 检索，待过门）

| 源 | 日期 | 它回答什么 | 预期判定 | 处置 |
|---|---|---|---|---|
| [Google OKF SPEC v0.2](https://raw.githubusercontent.com/GoogleCloudPlatform/open-knowledge-format/main/SPEC.md) · [卡](../../src/web/google-okf/google-okf.card.md) | 2026-07-24 | Q1：non-goals、0 次 ontology、semantic-layer 仅 §12.3、no execution/ACL | `admitted`（已有） | 保留；补引 §12.3 原文 |
| [中泰 CCSA TC601](../../src/web/modb-2026-zhongtai-ontology/modb-2026-zhongtai-ontology.card.md) | 2026-10-15 | Q3：OKF 作权威源；图数据库/对象关系在后续规划；业务本体在信用业务验证 | `admitted`（已有） | 保留；把“方向不对称”标成我们的概括 |
| [SEMANTiCS 2026 · SCIMIN/SMW 论文](https://ceur-ws.org/Vol-4293/paper50.pdf) | 2026-10-13 | Q2/Q3：**本体先行**，wiki 是协作/标注界面，LLM 只产候选，自动校验 + 专家 HITL 后才进生产 | `signal`（承建方自述；初判 admitted 已复核下调） | **不建目录**；只进 frontier + 90 线索 |
| [SCIMIN-CRM & MWF Ontology 1.0](https://sadeqzougari.github.io/scimin-crm/) | 2026 | 论文的 ontology 本体（OWL/RDF，类/属性） | 支撑材料 | 论文卡内引用，不单独建卡 |
| [Linked.Archi · OKF and Linked.Archi](https://meta.linked.archi/docs/practice/okf-open-knowledge-format/) | 2026-07-17 | Q2：DIKW 分层；双向投影；**关系定型缺口**；何时值得上图 | `signal`/C（单项目、无独立采用、G3 不过） | 只进 frontier + mechanism 的 C 证据表；**不进 05 结论** |
| [Atlas · OKF interop spike](https://github.com/AtlasDevHQ/atlas/blob/main/docs/research/okf-interop-spike.md) | 2026-07-02 | Q2：导出“全但丢语义”、导入“有用但有损的草稿生成器”；权限/白名单无 OKF 对应物 | C（公司工程文档；1★） | 作 Q2 的**独立佐证**（C 级），不进 05 结论 |
| [GMEOW · OKF](https://github.com/Blackcat-Informatics/gmeow-ontology/blob/main/docs/okf.md) | 2026 | Q2：OKF = 有损下投影；封闭 `okf:` profile；lift 回 RDF | C（单项目） | 同上；作第三份实现佐证 |
| [Kunstenpunt Wikibase](https://tech-news.wikimedia.de/2026/06/02/kunstenpunt-a-whos-who-of-the-flemish-art-scene/) | 2026-06-02 | Q3：2024 数据标准先行，再把三套旧库并进 Wikibase；约束只警告 | `signal`（frontier 已有） | 找第二独立信号；找不到就只留 frontier，4b 只留一句“另有线索” |
| [京东海博](http://stock.10jqka.com.cn/20260924/c680274369.shtml) | 2026-09-24 | Q3：自称 OKF 的第二个中国线索；AB 542s vs 967s | `signal`（frontier 已有） | 移出 4b 正文，只进 90.2c 线索与 frontier |

> **黑名单**：上述源均不在 [excluded-sources](../../meta/rules/excluded-sources.md)。Zenodo 的 NKB note、SAP community 帖 2026-11-12 抓取被 403/Cloudflare 拦，**未核不引**，记 frontier 待评估。

## 3. 证据策略：先分级，再决定写在哪

1. **规范/标准事实** → `admitted` 卡的原文摘录（Google OKF、W3C OWL/SHACL、RDF）。
2. **工程实现/映射机制** → 三份独立实现（Linked.Archi / Atlas / GMEOW）作为 **C 级佐证**；结论写成“三份独立工程文档在 X 上一致、在 Y 上分歧”，等级 `已核（工程文档互证）`，不外推为生产规律。
3. **生产/试点采用** → 只有 `admitted`（中泰）能进 05 正文；`signal`（SCIMIN、Kunstenpunt、京东）只进 [90 来源](../05-production-landscape/02-sections/90-sources.md) 与 frontier。
4. **设计判据**（何时升级、W0–W3）→ 留在 [mechanism](../../topics/06-measure/feasibility/mechanism.md#okf-2026-11)，标 `推测`；4b 只保留“三个可观测信号 + 指向 07/mechanism”，**不写数字阈值**。
5. **阴性结论**（没有完成迁移）→ 必须写检索式、日期、渠道；记 [90.3](../05-production-landscape/02-sections/90-sources.md) 与 frontier。

## 4. 执行步骤（S0–S6）

| 步 | 做什么 | 产物 | DoD |
|---|---|---|---|
| **S0 冻结** | 4b 暂停新增；先建逐句 provenance 审计 | `meta/audits/2026-11-12-04b-okf-provenance.md` | 每个正文断言有“上游/无上游”判定 |
| **S1 审计** | 逐句对 `card/digest/E/L/mechanism/frontier`；标 `无源`/`signal 越级`/`伪精度`/`越界` | 同上（P0/P1/P2 分级） | 至少覆盖 4b.1–4b.8 的承重句；给出改法 |
| **S2 补证** | 建 SCIMIN/SMW 卡 + digest；把 Linked.Archi/Atlas/GMEOW 记入 frontier 与 mechanism 的 C 表；Kunstenpunt 找第二信号；Google spec 复核 | `src/web/semantics-2026-scimin-smw/`（卡+digest）；frontier 更新 | 卡有 `admission/gate_checked/impact_evidence/liveness/provenance_type`；不过门的不建目录 |
| **S3 升判断** | 改 [mechanism OKF 节](../../topics/06-measure/feasibility/mechanism.md#okf-2026-11)：拆成“规范边界/映射机制/采用证据”三段；改 [L-22](../../topics/06-measure/claims.md)；校准 [E-32](../../topics/conclusions.md) | mechanism/claims/conclusions 的 diff | 每段等级对档；“没有完成迁移”有检索记录 |
| **S4 回写 4b** | 按新结构重写：删伪阈值；Kunstenpunt/京东降为线索；SCIMIN 正名（critical raw materials，不是 CRM）；加“三实现共识/分歧”表；把“可映射”与“会自动长成”分开 | 4b 新稿 | 每句能指到 admitted 卡/digest，或显式标 C/signal/推测 |
| **S5 一致性** | 90.2c、06.1（如需）、README 证据基座、state/state-log、_plans 索引 | 相关页 diff | 同值同义；计数与 state 一致 |
| **S6 校验** | `python3 meta/tools/check_repo.py`；质量卡复评（D1/D2 为重点）；可选冷读 | 自检输出 + 复评分 | 0 坏链/0 坏锚；质量分 ≥85.6，D1/D2 不降 |

## 5. 预期改动的判断（不是新增结论）

- **E-32**：把“它可以按需升级”改成“它可以按需升级，但**公开证据里没有完成 OKF→本体迁移的案例**；已完成的是本体先行（SCIMIN）与 OKF 先行 + 本体在验证（中泰）”。等级不变（定义已核 / 判据推测）。
- **L-22**：补一句“OKF→本体的 lift 是有损的，关系定型需人审；三份独立实现一致”；仍为 `已核（定义）/推测（判据）`。
- **新增 L（06 派）**：“OKF 与本体之间是**非对称投影**：本体→OKF 可机械投影但丢语义；OKF→本体是有损草稿 + 关系定型人审。三份独立工程文档互证（Linked.Archi / Atlas / GMEOW）。”等级 `已核（工程文档互证）`，不外推生产。
- **不新增 E**：这是对 E-32 的限定，不是新跨派结论。若 S3 发现确需升 E，另议。

## 6. 边界（不做）

- 不写 recipe、不给实施步骤、不加代码/示例引擎（CHARTER §3）。
- 不补“看起来完整”的 W0–W3 第三份；判据只留一处（mechanism）。
- 不把 C 级实现文档写成“生产采用”；不把“没有找到”写成“不存在/不可能”。
- 不引 2026-11-12 抓不到的源（Zenodo NKB、SAP community），只记 frontier 待评估。
- 不为凑“第二个中国案例”把京东海博升格。

## 7. 风险与回退

| 风险 | 触发 | 回退 |
|---|---|---|
| SCIMIN 论文过不了 G3（只有会议 + 项目，缺独立采用） | 建卡时判 `signal` | 不建目录；4b 只写“有一篇会议论文描述该架构（signal）”，不撑结论 |
| Kunstenpunt 找不到第二独立信号 | 检索阴性 | 留在 frontier；4b 删掉 4b.4b 整节，只在 90.2c 留一行 |
| 三份实现其实同源（都抄 Linked.Archi） | 文本比对发现 | 降为“一份框架 + 两份实现”，结论强度降为 `推测` |
| 4b 定位应拆分 | S4 发现“判据”仍越界 | 方案 B：4b 只留现状/证据/缺口；判据移 07 或 02，另开 ADR/计划 |

## 8. 验收（Definition of Done）

1. 4b 的每个数字/判定：能指到 `admitted` 卡的原文节，或显式标 `C`/`signal`/`推测`；**0 处 signal 当证据**。
2. Q1/Q2/Q3 三段分开；“可映射”与“会自动长成”不再混写；无数字阈值。
3. “没有完成迁移”有检索式、日期、渠道、阴性记录。
4. `check_repo` 0 error；质量复评 ≥85.6，D1/D2 不降。
5. 计划归档为 `已执行`，state 记一笔；本页不成为第二份规则。

## 9. 检索日志（2026-11-12）

| 查询 | 渠道 | 结果 |
|---|---|---|
| `SCIMIN CRM ontology wiki LLM annotation` | web_search | 命中 CEUR Vol-4293 paper50；确认真实 |
| `Linked.Archi OKF open knowledge format DIKW` | web_search + curl | 命中官方页；`article:published_time=2026-07-17` |
| `Kunstenpunt Wikibase 250,000` | web_search + curl | 命中原文；数字/约束/3 人/联邦均支持 |
| `"open knowledge format" ontology RDF` | web_search | 命中 Atlas spike、GMEOW、NKB、SAP 帖 |
| `OKF adoption customer case 2026` | web_search | 无具名企业生产案例；多为教程/博客 |
| GitHub `"open knowledge format" in:description` | api.github.com | 477（2026-11-12 快照；不等于采用） |

> 阴性结论只写到“2026-11-12 公开渠道未找到”，不写“不存在”。

## 10. 执行回执（2026-11-12）

| 步 | 状态 | 产物 |
|---|---|---|
| S0 冻结 | 完成 | 本节 |
| S1 审计 | 完成 | [04b provenance 审计](../../meta/audits/2026-11-12-04b-okf-provenance.md)（7 P0 / 9 P1 / 5 P2） |
| S2 补证 | 完成 | [SCIMIN/SMW 论文](https://ceur-ws.org/Vol-4293/paper50.pdf) 读毕后判 `signal`（初判 admitted，复核下调；不入 `src/`）；Linked.Archi/Atlas/GMEOW 入 [frontier](../../topics/06-measure/feasibility/frontier.md)；Kunstenpunt 第二信号检索阴性，维持 `signal`；Zenodo NKB / SAP community 抓取失败记待评估 |
| S3 升判断 | 完成 | mechanism OKF 节重写（两个方向 + 关系定型缺口 + 三档缺口）；E-32 补非对称投影；06-L22 收窄；新增 06-L23 |
| S4 回写 4b | 完成 | 4b 重写为 9 节；删伪阈值与 501 计数；Kunstenpunt/京东降 `signal` 移出正文 |
| S5 一致性 | 完成 | 90.2c/90.3、README 证据基座与导读、state/state-log、_plans 索引 |
| S6 校验 | 完成 | `check_repo`：0 坏链 / 0 坏锚 / 0 未定义 ID / 枚举通过（538 md，L=85，18 材料卡） |

**与计划的偏差**：
1. **SCIMIN 的判定改过两次，最终 `signal`**：初判 `admitted`（理由：多机构 Horizon Europe 项目 + 项目内 adoption）是手松了——G3 要的是**作者之外**的独立信号，而“多机构”和“采用”都在同一个项目内部，作者又是承建方本人。按“尽量严格”复核后**移出 `src/`**，只留 frontier 与 90 线索；这条与计划第 7 节风险表预写的回退路径一致。
2. Kunstenpunt 保持 `signal`（第二独立报道未找到），因此 4b 只留一句，不再有“4b.4b 反例”小节。
3. 新增的不是 E 而是 **06-L23**：非对称投影是派内机制判断，不构成跨派结论。
4. 顺带修 `check_repo` 里过期的结论等级期望（15/3 → 19/4），否则它会一直对当前状态误报。

**未关的缺口**：OKF/Wiki → 本体迁移完成案例仍为 0（写进 [90.3](../../deliverables/05-production-landscape/02-sections/90-sources.md) 阴性行与 frontier）；Kunstenpunt 第二信号、SCIMIN 的规模/效果、三份实现是否有生产用户，都还需外部材料。
