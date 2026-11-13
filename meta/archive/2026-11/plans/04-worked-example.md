---
status: draft
type: work-plan
updated: 2026-11-09
target: deliverables/04-worked-example
---

# 04 支撑计划：从“外部信号”到“可引 E”

> **本计划不是 04 正文，也不是 E。** 它把“04 现在靠外部信号”变成“04 能引本轮新升的 2 条 E”的施工顺序；结论仍回 `topics/`，04 只做抽取。
>
> 上游缺口矩阵见 [04-upstream-gaps](../04-upstream-gaps.md)。本版是 2026-11-09 三次收紧后的修订版：新鲜度、来源 scope、可靠性/影响力；改动清单见 §10。

## 0. 一句话与三条硬规则

**04 先保持 field guide 定位。** 本轮只做 **4 个核心 intake + 1 个已有活跃代码项目**，补 **2 个 topics 页面**、**2 条新 E**；**build 章不升级**（没有 in-scope 的 evaluation 来源），只升级 consume B.3 与 govern C.1。**论文线已冻结**：GGC/Glyph/NLKGQ/KGVoyager 是最后一批，不再新找论文；**工程 OSS 升为主线（P2.5）**：论文管机制，OSS 管落地；先扫后选 1–2 个，不硬塞。不新开交付物，不铺 20 个来源。

**硬规则 1（引用）**：`deliverables/` 只引 `E-xx`——[conclusions](../../../../topics/conclusions.md) 的头写明“唯一允许被 deliverables 直接引用的地方”，[loading](../../../workflow/loading.md) 规则 1 与 [checklist](../../../workflow/checklist.md) §3 也禁止引 `L-xx`。路径是：

```text
src digest → 子主题 F → 派 L → 跨派新 E（2 条）→ 04 引 E
```

**硬规则 2（新鲜度）**：新来源只收 **2026-07-01 以后**。论文看首次提交/发表；开源项目看 `last_push`（2026-06 后仍活跃）。规则在 [src/README §0.1](../../../../src/README.md)，`check_repo` 查 `batch: 补给` + `published` / `last_push`。

**硬规则 3（scope + 可靠性）**：新来源 origin 只收 **US / China / Germany / Singapore**；其他地区不要，留着没意义。论文卡写 `region`/`venue`/`reliability`/`impact`；preprint 不能默认 high；`reliability: low` 不入核心。规则在 [src/README §0.2](../../../../src/README.md)。

## 1. 决策

| # | 决策 | 理由 |
|---|---|---|
| D0 | 新来源 ≥ 2026-07-01；旧源删除 | 用户定死；过老材料常误导 |
| D0b | origin 只收 US/China/Germany/Singapore；其他地区删除 | 用户定死；scope 外的来源留着没意义 |
| D0c | 来源要可靠/有影响力；preprint 不默认 high；卡写 `venue`/`reliability`/`impact`/`region` | 用户定死；数字漂亮不等于来源可靠 |
| D1 | 04 暂不标 `stable`，保持 `draft` | 本轮只升级 B.3/C.1；build 章仍是 signal |
| D2 | **4 个核心**：GGC（SG）、NLKGQ（DE）、KGVoyager（US）、Glyph（US）+ trustgraph（已有，last_push 2026-11-08） | 全部 2026-07 后、in-scope、有可靠机构/生产/开源影响 |
| D3 | 新开 **2 个 topics 页面**：`03/querying`、`01/access-control` | 各有 ≥2 来源；evaluation 没有 in-scope 来源，不开 |
| D4 | **新增 2 条 E（一页一条）**；04 只引 E | 进交付物即触发升 E；没有 E 的就留在 signal |
| D5 | **build 章不升级**：A.2/A.3/A.4/A.5 保持 signal | CQ4OE（ES）、OntoExtend（SE/IT）等 out-of-scope，不拿来凑 |
| D6 | 未入库来源继续标 signal；pre-2026-07 的旧信号不再作为新判断依据 | 与 D0 一致；P4 清理 04 evidence 的旧条目 |
| D6b | **工程线**：论文偏学术，04 落地靠活跃 OSS；OSS 按 `last_push` + 采用/标准/生产判，**不套论文 origin scope** | 用户定死；先扫后选，1–2 个，不硬塞 |
| D6c | **论文线冻结**：GGC/Glyph/NLKGQ/KGVoyager 是最后一批，不再新找论文 | 用户定死；论文够用，继续找是边际收益递减 |
| D6d | **Web 讨论线**：2026 年高影响论坛/blog；卡写 `influence` 证据；**不是 E** | 用户定死；补工程现场/失败复盘，不拿营销文凑 |
| D7 | 计数不写死：`check_repo` 动态计数 + 新鲜度/可靠性字段 | 加论文必破 `!= 24`；不修脚本，P5 的 DoD 不可能过 |

## 2. 支撑水位：逐段说清楚“升什么、不升什么”

> 这张表是本计划的核心。它回答“缺东西吗”：querying/access-control 缺，补 4 个；build 章缺 in-scope 来源，**不补、不假装**。

| 04 段 | 现在依赖 | 本轮动作 | 完成后 04 怎么写 | 仍缺 / 不做 |
|---|---|---|---|---|
| A.2 LLM 候选生成 | 2503（已删）；无 in-scope 替代 | **不升** | 保留 signal；不再引 2503 数字 | 没有 2026-07 后 in-scope 生成 benchmark |
| A.3 公理质量 | 2512（已删）；无 in-scope 替代 | **不升** | 保留 signal；不再引 2512 F1 | 公理级 benchmark 缺 |
| A.4 对齐与精化 | Agent-OM（2023，旧信号）；CASTON 是已有语料（UK/SE） | **不升** | 保留 signal；CASTON 只在旧文引用，不新增 E | 无 in-scope 精化来源 |
| A.5 CQ 评估 | 2507（已删）；CQ4OE（ES）已删 | **不升** | 保留 signal | 无 in-scope CQ benchmark |
| B.2 KG 构建 | 3 篇 2024–2025 旧信号 | 不动 | 标“旧信号，不再作为依据” | 全部太老 |
| B.3 Text2SPARQL | GGC（SG）+ NLKGQ（DE）+ KGVoyager（US） | 入 NLKGQ + KGVoyager → `03/querying` F1/F2/F3 → P1 新 E | 引 E；删 SPARQL-LLM/CK25 旧引 | 跨域/跨 KG 未测 |
| B.4 语义层/OBDA | AWS 指南（厂商，旧信号） | 不动 | 保留 signal；“OBDA≠NL→query”仍是边界 | 无 in-scope 一手来源 |
| C.1 访问控制 | VAULT（已删）；Glyph（US）+ trustgraph | 入 Glyph → `01/access-control` F1/F2 → P2 新 E | 引 E + E-20 | 无生产访问控制数据 |
| C.3 输出校验 | 2604（2026-04，早于线） | 不动 | 标旧信号 | 2604 太早 |
| C.4 失败传播 | 2609（2026-09，合线） | 本轮不做；只进 06 frontier 候选 | 保留近期 signal | 2609 未入库 |
| §5 验收 | 外部数字 | 改引 P1/P2 的新 E + 自域协议 | “现在有什么”列改 E / signal | 自域数据仍只能自己量 |

**结论**：本轮升级的是 **B.3/C.1**；**A.2–A.5/B.2/B.4/C.3 保持 signal**；**C.4 保留近期 signal**。04 仍是 field guide，不是“全章都有 E”的 playbook。

## 3. 四个 intake + 一个代码项目

### 3.0 来源可靠性 / 影响力（先筛）

| 来源 | 机构 / 国家 | venue | reliability | impact | 判定 |
|---|---|---|---|---|---|
| **GGC** | NTU / A*STAR，Singapore | arXiv preprint | medium | medium | 支撑；**不单独撑 E** |
| **NLKGQ** | Max Planck Institute for Biological Cybernetics，Germany | arXiv preprint | medium | medium | 核心：OWL ontology 进上下文；单作者/9 页 |
| **KGVoyager** | University of Texas at Arlington，US | arXiv preprint | medium | medium | 核心：KG-agnostic agentic navigation；4 benchmarks |
| **Glyph** | Apple，US | arXiv preprint（**生产系统**） | high | high | 核心：Apple 生产 + 275-leaf 分类本体 |
| **trustgraph** | 开源，全球 | 2,902★ / 30 contributors / last_push 2026-11-08 | high | high | 核心：唯一读路径代码实现 |
| ~~SPARQL-LLM~~ | SIB/UZH，Switzerland | — | — | — | **out-of-scope，删除** |
| ~~CQ4OE~~ | UPM，Spain | — | — | — | **out-of-scope，删除** |
| ~~OntoExtend~~ | Linköping/Bologna/Bosch，SE/IT/DE | — | — | — | **origin 混合、Lead 非 DE，删除** |
| ~~QRAKEN~~ | Bologna/Harvard/Copenhagen，IT/US/DK | — | — | — | **out-of-scope，删除** |
| ~~PPC~~ | TMU/Flybits/MIT，Canada/US | — | — | — | 框架无实现，且 origin 不合 scope；删除 |

> 读法：scope 是硬门槛，不是先验；例外不设。US/China/Germany/Singapore 内再按 venue/生产/benchmark/强组看 reliability/impact；preprint-only 且无采用的，只做 signal，不单独撑 E。

### 3.1 落点与验收

| # | 来源 | 日期 | src 落点 | topics 落点 | E | 04 段 | 深度 |
|---|---|---|---|---|---|---|---|
| 1 | **GGC** 2607.28082 | 2026-07-30 | `src/papers/2607.28082-ggc/` | `03/querying` F1 | P1 | B.3, B.6 | L2（已落） |
| 2 | **NLKGQ** 2609.14652 | 2026-09-13 | `src/papers/2609.14652-nlkgq/` | `03/querying` F2 | P1 | B.3, B.6 | L1（9 页） |
| 3 | **KGVoyager** 2609.01780 | 2026-09-01 | `src/papers/2609.01780-kgvoyager/` | `03/querying` F3 | P1 | B.3, B.6 | L2（16 页） |
| 4 | **Glyph** 2609.10430 | 2026-09-09 | `src/papers/2609.10430-glyph/` | `01/access-control` F1/F2 | P2 | C.1 | L2（10 页） |
| — | **trustgraph**（已有） | last_push 2026-11-08 | `src/open-source/trustgraph-ai-trustgraph/` | `01/access-control` F2 | P2 | C.1 | 代码（已消化） |

**验收下限**：
1. **GGC（已落）**：MCQA 电影域、单 KG（iMKG）、31,570 题、Llama-3.2-3B 单骨干；`Query Acc.` 是**答案集匹配率**；90.23 = Generator 单跑，92.34 = 全量纠错，98.33 = 选择性纠错；45% 是相对全量纠错的墙钟（比单跑 +10%）；Gate FPR 0.31%、trigger 9.31%。**禁写**：execution accuracy；跨生成器/跨 KG。
2. **NLKGQ**：9 页、Max Planck；OWL ontology 放进单次 LLM 上下文；零样本生成 SPARQL；DBLP-QuAD 2.0；分数依赖 graph snapshot/endpoint/prompt wording。必抽：ontology 规模/域、查询集、指标、结果、失败模式、wrapper ontology/rewrite 的边界。**禁写**：跨 endpoint 通用；把单次 zero-shot 当 SOTA。
3. **KGVoyager**：16 页、UT Arlington；KG-agnostic agentic navigation，think-act-observe + search/exploration/execution 工具；term→IRI、结构发现、执行反馈 refine；不依赖预存 ontology/examples，只要 query endpoint + lightweight class index；4 benchmarks、F1 约 4×。必抽：benchmarks/baselines/指标/增益、class index 的作用、无 ontology 的代价、失败模式。**禁写**：把 4× 当跨域效应量；把 agentic navigation 当 Text2SPARQL 通用解。
4. **Glyph**：Apple 单企业单目录（~3.4M 列/98k 表/4 LOB/3 后端）；275-leaf Data Classification Ontology（~72% NON_SENSITIVE）；不读 cell value，description/LOB regex/metadata+MiniLM 三策略 + RRF(k=60) + tier 重排，per-tag provenance。**只做标签/分类，不产出策略判定、不执行访问控制。** 检索 NDCG@10 0.5497→0.9225、MAP@100 0.1888→0.9009 是**同一 stock MiniLM 微调前后的检索指标**（9,242 query/83,229 corpus、10% 列级留出、同分布上界、未控表内泄漏），不是打标准确率；端到端 F2 fusion 0.890 vs metadata 0.880（RRF 只 +0.010 F2/−0.015 F1；增益主要来自编码器微调）；生产接受率 63.3%→99.8% 是作者报告、对 FN 盲。必抽：标签体系、三策略/RRF、检索 vs 端到端、holdout/CI、生产边界。**禁写**：把 NDCG/MAP 当打标准确率；标签质量=访问控制正确性；跨企业通用。

### 3.2 工程 OSS（可选，P2.5）

- **现有 4 个**：trustgraph / semantica / open-ontologies / ontop，均 last_push 2026-11-04/08；不重复推荐。
- **扫描目标**：策略/授权引擎（补 04 C.1 的“标签→策略→执行”中间层）、SPARQL 运行时（补 B.3 的“生成→执行→验证”）、SHACL/本体校验（补 A.3/C.3）。
- **入选标准**：`last_push ≥ 2026-07-01`；CNCF/Apache/AWS/标准/de facto/生产采用；能定位到 `文件:符号`；不 vendor；pin commit；`ontology_role` 写 adjunct/none 也要诚实。
- **交付**：1–2 个项目，card + digest + code-map；在 01/access-control（策略层）、03/querying（运行时）或 02/checker（校验）加 finding；不新开派。
- **不做**：GraphRAG/纯图检索/闭源/停更；不把 star 当质量证明；不为凑工程线硬塞。

### 3.3 Web 讨论（2026 影响力线）

- **选材**：2026 年（优先 2026-07 后）论坛/blog 讨论；主题围绕 ontology/KG/semantic layer、context engineering、agent authorization、Text2SQL/SPARQL。
- **影响力证据**：HN front page/points/comments、Reddit upvotes、业内引用、标准/厂商采用、作者 reputation；卡写 `influence`，不写形容词。
- **交付**：1–2 篇，`src/web/{source}/` 原文 MD + `.card.md`（自包含，不建 digest）；**不升 E**；改变判断才进 topics。
- **不做**：SEO 农场、纯厂商营销、无日期/2025 及更早、低互动。

## 4. 两个 topics 页面

### 4.1 `03/querying`（新建）

- **成立条件**：GGC（SG）+ NLKGQ（DE）+ KGVoyager（US）= 3 个 2026-07 后、in-scope 来源；三条机制不同（selective correction / ontology-in-context / agentic navigation）。
- **拟写 findings**：
  - `F1` **GGC 的选择性纠错在 MCQA 单 KG 上把答案集匹配率 90.23→98.33**（全量纠错 92.34；45% 是相对全量纠错的墙钟，比单跑 +10%）；净收益依赖分布内 Gate（FPR 0.31%、trigger 9.31%）。`已核`（数字）/`推测`（跨域）。
  - `F2` **NLKGQ 把完整 OWL ontology 放进单次 LLM 上下文，零样本生成 SPARQL**；DBLP-QuAD 2.0 上分数依赖 snapshot/endpoint/prompt wording；wrapper ontology + runtime rewriter 用于 opaque 词汇。`已核`（单系统）/`推测`（跨域）。
  - `F3` **KGVoyager 不依赖预存 ontology/examples，用 agentic navigation 在 4 个 benchmark 上把 F1 提高约 4×**；只需 endpoint + lightweight class index；代价是探索成本/延迟。`已核`（数字）/`推测`（跨域）。
- **frontier**：
  - `G1` 跨域/多 KG：三篇各一个设置，没有独立复现。
  - `G2` 空结果/失败分布：GGC 没有专门机制、没有测量；NLKGQ 依赖 snapshot/endpoint；KGVoyager 用执行反馈 refine。
  - `G3` 纠错净收益：GGC 没有 2×2 配对矩阵，只有子集级 + 单例。
  - `G4` ontology-in-context vs ontology-free：NLKGQ（完整 OWL）vs KGVoyager（无 ontology/只要 class index）不是头对头；谁是默认路线未测。
- **mechanism**：`request → schema/ontology or exploration → generate → execute → empty/error → gate/refine → verify`；标出三篇各停在哪。
- **04 改动**：`body/consume.md` B.3/B.6 引 P1 新 E；删 SPARQL-LLM/CK25 旧引；B.1 的“OBDA≠NL→query”保持边界，不挂 E-20。
- **派回写**：`03/README` 子主题地图 + `03/claims.md`（拟新增 03-L）+ `03/sources.md` + `03/frontier.md`。

### 4.2 `01/access-control`（新建）

- **成立条件**：Glyph（Apple，US）+ trustgraph（last_push 2026-11-08）= 2 个独立来源；标签/分类与策略执行是不同层，和 action-gate/commit-gate 是不同机制。**read-path 仍是轴外**（E-20）；本页只是机制之家，不升第七时刻。
- **拟写 findings**：
  - `F1` **标签/分类层是权限的输入，不是执行**：Glyph（Apple 单企业，~3.4M 列/98k 表；275-leaf 分类本体；~72% NON_SENSITIVE）不读 cell value，用 description/regex/metadata+MiniLM 三策略 + RRF(k=60) + tier 重排做列级标签，per-tag provenance；**不产出策略判定、不执行访问控制**。NDCG@10 0.5497→0.9225、MAP@100 0.1888→0.9009 是同一 stock MiniLM 微调前后的**检索**指标（9,242 query/83,229 corpus、10% 列级留出、同分布上界、未控表内泄漏），不是打标准确率；端到端 F2 fusion 0.890 vs metadata 0.880（RRF 只 +0.010 F2/−0.015 F1）。`已核`（一手正文；生产部署为作者报告）/`推测`（跨企业）。
  - `F2` **执行层另有其物**：trustgraph 用 SHACL-AF post-filter 对查询结果做读路径过滤；fail-open、只删 subject、单实现（E-20/commit-gate F5–F7）。`已核`（代码）。
  - `F3` **标签 ≠ 策略 ≠ 执行**：Glyph 的 F2/NDCG 是标签质量（NDCG 还是检索指标、同分布上界），不是策略正确性；trustgraph 的过滤是 best-effort 执行；**策略层本轮没有来源**。`推测`（综合）。
- **frontier**：
  - `G1` 策略冲突/优先级：两个来源都没有。
  - `G2` 审计/策略版本：两个来源都没有。
  - `G3` 第二实现/对象方向：**cross-link commit-gate G1/G4，不复制**。
  - `G4` 标签体系跨企业：Glyph 是单企业，275-leaf 分类本体不外推。
- **mechanism**：`source/column → classification/label (Glyph) → policy → post-filter (trustgraph) → verdict/audit`；标出每个来源停在哪。
- **04 改动**：`body/govern.md` C.1/C.7 引 P2 新 E + E-20；C.1 表的“文档级/节点级/写路径”改成“标签/分类 / 节点级策略过滤 / 写路径”；C.3 旧信号、C.4 近期 signal。
- **派回写**：`01/README` 子主题地图 + `01/claims.md`（拟新增 01-L）+ `01/sources.md` + `01/frontier.md`；**commit-gate 的 F5–F7 不搬家**，只加 cross-link。

### 4.3 为什么本轮不做 `05/evaluation`

没有 in-scope 且可靠的 evaluation 来源：CQ4OE（Spain）、OntoExtend（Sweden/Italy/Bosch）、QRAKEN（Italy/Denmark）都已按 scope 删除；美国/中国/德国/新加坡的 2026-07 后 CQ/本体评估 benchmark 没有找到同等质量的。**不拿 out-of-scope 来源凑页**；04 的 A.2–A.5 保持 signal，等下一轮 in-scope 来源。

### 4.4 为什么本轮不做 `06/failure-attribution` 的新 finding

2609.06391（2026-09）合线，但仍是 12 页综述/蓝图，五个接口契约是**设计提案**，没有实测；把它写成 `F` 会把框架抬成发现。它只进 `06/frontier.md` 的候选队列，04 C.4 保留近期 signal。若以后入库，下一号是 **F8**，等级最多 `已核（框架）`。

## 5. 现场数据，不进 src

| 04 要的数字 | 怎么量 | 写在哪 | 不能写成 |
|---|---|---|---|
| CQ 覆盖 | 目标消费者 3–10 个 CQ，逐条执行/人审 | `sections/acceptance.md` 5.1 | “CQ 通过 = 语义正确” |
| execution accuracy | 100–200 问题 + SPARQL + 答案；同一 schema/模型 | 5.2 | “benchmark 数字” |
| 权限覆盖/泄漏 | 20–50 条 policy 用例 + object 方向 | 5.3 | “有策略 = 策略正确” |
| 输出校验 verdict | 20–50 条高风险输出 | 5.3 | “校验 = 形式保证” |

**这些不进 topics，也不进 src；04 只写协议与 stop。** `false-defer` 是 01/commit-gate 的数，不塞进 04 的验收表。

## 6. 阶段与 DoD

| 阶段 | 时间 | 做什么 | DoD |
|---|---:|---|---|
| P0 基础设施/清理 | 已完成 | 新鲜度 + scope + 可靠性规则；删除 out-of-scope/旧源；`check_repo` 动态计数；P0 映射 | 旧源目录/manifest/log 清理；`check_repo` 不再因旧源报错 |
| P1 querying | 2–3.5 天 | NLKGQ + KGVoyager 落盘；GGC 已落；`03/querying` 四件套；03 claims/sources/frontier/README；P1 新 E | 04 consume 引 E；SPARQL-LLM/CQ4OE/OntoExtend/QRAKEN 不再出现；`check_repo` 过 |
| P2 access-control | 1.5–2.5 天 | Glyph 落盘；`01/access-control` 四件套；01 claims/sources/frontier/README；P2 新 E | 04 govern 引 E + E-20；不重复 commit-gate F5–F7；`check_repo` 过 |
| P2.5 工程 OSS（主线，论文后） | 1–2 天 | scan GitHub；shortlist；选 1–2 个（策略引擎/查询运行时/SHACL 校验）；card/digest/code-map；补 01/03/02 finding | 1 个项目 pin commit；digest 能回答“真执行还是装饰”；不 vendor；不拖 P3/P4 |
| P2.6 Web 讨论（2026 影响力线） | 0.5–1 天 | scan 2026 HN/Reddit/blog；选 1–2 篇；原文 MD + card（`influence`）；不升 E；改变判断才进 topics | 有 URL/日期/影响力证据；卡自包含；不拿 SEO/营销凑 |
| P3 04 回写 | 1.5–2.5 天 | body/consume/govern；sections/acceptance/boundaries/map/relations；evidence；README `basis`；deliverables/README | 已入库来源不再标“外部信号（未入库）”；旧/out-of-scope 明标；04 仍 draft |
| P4 台账/计数 | 0.5–1 天 | `state` 当前计数；`loading`；顶层 README；`src/README`；manifest 顶部说明；01 acceptance 的 E 数；`check_repo` | `check_repo` 0 错；计数以脚本输出为准；04 draft |

**路径**：P0+P1+P2+P3+P4 ≈ **6–10 天**；加 P2.5/P2.6 ≈ **8–12 天**（量级，不是承诺）。build 章不升级，省掉 evaluation 阶段。

## 7. 风险与处置

| 风险 | 表现 | 处置 |
|---|---|---|
| in-scope 窗口太窄 | 2026-07 后 US/China/Germany/Singapore 的 evaluation 来源找不到 | 不拿 out-of-scope 凑；A.2–A.5 保持 signal，写清“没有 in-scope 来源” |
| 来源拿不到 | PDF/网页 403 | 换官方 PDF/arXiv HTML；拿不到就留 signal，不硬编 |
| 单来源太薄 | querying 只有 GGC / access-control 只有 Glyph | NLKGQ/KGVoyager、trustgraph 必进；否则标“薄页”，不承担稳定判断 |
| E 升不上去 | 判断只属一派、没有跨派性 | 不硬升；04 保留 signal，等第二轮 |
| 04 引 F/L 的诱惑 | 图省事直接链 findings | 规则禁止；只引 E-xx；F/L 留在 topics |
| `check_repo` 失败 | 加论文后 `!= 24`；新鲜度/可靠性字段不认 | P0 已改：动态计数 + `补给` 正则 + 新鲜度 + 可靠性字段 |
| 旧/out-of-scope 残留 | 04 还在引 2025/CH/ES/SE 的数字 | P3 清理 04 evidence；旧条目标“旧信号（不再作为依据）”，不保留数字 |
| 重复 read-path | access-control 又写一遍 fail-open/subject-only | F5–F7 留在 commit-gate，access-control 只写标签/执行点/强度 |
| OSS 扫描无高影响候选 | 只有低星/停更/纯图检索 | 不硬塞；留在 frontier 候选；工程线可以为空 |
| Web 讨论营销/轶事 | 只有厂商文/SEO 农场/低互动 | 只做 card/signal，不升 E；没有影响力证据就跳过 |

## 8. 不做

- 不补 20 个来源；只做 4+1。
- **不再新找论文**；论文线冻结在 GGC/Glyph/NLKGQ/KGVoyager；后续主线是 OSS 工程线 + 04 回写。
- **不再新入档 2026-07-01 前或 origin 不在 US/China/Germany/Singapore 的论文/项目**；旧源删除。
- 不新开 05/06/07 交付物；不开 `05/evaluation`；不开 `06/failure-attribution` 新子主题。
- 不在 04 引 `F`/`L`；只引 `E-xx`。
- 不把 signal 升 E 而没有 digest；不把综述/蓝图当 finding。
- 不为“看起来完整”建空子主题；先有 2 个来源再开。
- 不把 2604.00555/AWS/SAGA/SchemaForge 升 E；它们不是旧就是厂商信号。
- 不把 `false-defer` 塞进 04 的验收表；它属 01/commit-gate。
- 不把 04 正文改成“待引”占位——那是破坏性 churn；映射只放本计划。
- 不为过 `check_repo` 写死数字；把脚本改成动态。
- 不为凑工程线收 GraphRAG/纯图检索/闭源/停更项目；OSS 不套论文 origin scope，但必须活跃 + 有采用。
- 不收 SEO/厂商营销/低互动 blog；web 讨论不是 E，只做 card/signal。

## 9. 下一步（P0 产物）

**P0 映射一页**（每行都要能回答“升哪条 E、04 哪句变、哪句仍留 signal”）：

| 04 句（段） | 来源 | 子主题 F | E | 04 改法 |
|---|---|---|---|---|
| A.2–A.5 “LLM 只做候选/公理/CQ” | 无 in-scope 来源 | — | 不升 | 保留 signal；删 2503/2512/2507 数字 |
| B.3 “瓶颈在 grounding / 选择性纠错” | GGC + NLKGQ + KGVoyager | `03/querying` F1/F2/F3 | P1 新 E | 引 E；删 SPARQL-LLM/CK25 |
| C.1 “标签/节点级/写路径” | Glyph + trustgraph | `01/access-control` F1/F2 | P2 新 E | 引 E + E-20；改表 |
| §5.1/5.2/5.3 “现在有什么” | 上述 | F/E | P1/P2 新 E | 改“现在有什么”列；自域数据另测 |

1. **P0 已完成**：脚本、src 规则、旧/out-of-scope 源删除、映射。
2. **先开 P1（querying）与 P2（access-control）**；P3/P4 收口。
3. **P2.5（主线）**：OSS scan → 选 1–2 个补策略/执行/校验；不拖 P3/P4。
4. **P2.6（可选）**：2026 高影响 blog/forum → 1–2 篇 card；不升 E。
5. 做完 P0–P4 再评估 04 是否值得升 `stable`；**现在不改**。

## 10. 本版修正（2026-11-09 复审 + 新鲜度 + scope）

| # | 原计划的问题 | 本版修法 |
|---|---|---|
| 1 | 让 04 引 `F1/F2`、`F1–F3`，与“deliverables 只引 E”冲突 | 改为 **2 条新 E（P1/P2 各一条）**；04 只引 E；F/L 留在 topics |
| 2 | §2 说 A/B/C 三段升级，§3 只补 5 个来源，口径对不上 | 改为 §2 逐段矩阵：只升 B.3/C.1，A.2–A.5 保持 signal |
| 3 | 旧源 2512/2507/2503/CK25/VAULT 太老（2025） | **全部删除**；替换为 GGC/NLKGQ/KGVoyager/Glyph，全部 ≥ 2026-07-01 |
| 4 | 04 改动只列 body，漏 acceptance/boundaries/map/relations/README | P3 列全 04 的落点（body 2 + sections 4 + evidence + 2 个 README） |
| 5 | CASTON 已在 src，却在 04 evidence 里标“未入库/摘要级” | P0 先把 CASTON 挪到 §1；A.4 不新增 E |
| 6 | 把 E-20 当成“OBDA≠NL→query”的出处 | E-20 只讲 engine 形态/执行≠授权；“OBDA≠NL→query”保持 04 边界，不挂 E-20 |
| 7 | 06 拟加 `F9/F10`；把 2609 的五契约当 finding | 本轮不做；若做，下一号是 **F8**，且只能标 `推测/已核（框架）` |
| 8 | access-control 的 F1–F3 与 commit-gate F5–F7 重复 | 重划为标签/执行/证据强度；F5–F7 不搬家，只 cross-link |
| 9 | 落点规则与 `src/web`/`check_repo`/manifest 契约不合 | web 用材料卡不建 digest；`check_repo` 动态计数 + 新鲜度；manifest 批次 `补给` |
| 10 | 时间估算偏乐观；P0 要把 04 改成“待引” | 改为 6–10 天（量级）；P0 只做映射，不改 04 正文 |
| 11 | 用户定死“只找 2026-06 以后”（论文 + 开源项目活跃） | 新来源 ≥ 2026-07-01；开源 `last_push ≥ 2026-07-01`；`check_repo` 机械校验 |
| 12 | 2503 可选槽失效 | A.2–A.5 改由“没有 in-scope 来源”解释；不补生成单篇 |
| 13 | 来源可靠性/影响力未设门槛；PPC 是框架无实现 | 卡加 `venue`/`reliability`/`impact`/`region`；只收 US/China/Germany/Singapore；Glyph（Apple 生产）替换 PPC |
| 14 | origin 不在建议 scope 的来源（CH/ES/SE/IT/DK）被收进来 | 全部删除：SPARQL-LLM、CQ4OE、OntoExtend、QRAKEN、PPC；只留 GGC（SG）、Glyph（US）、trustgraph；补 NLKGQ（DE）、KGVoyager（US）；evaluation 降 signal |
| 15 | 论文偏学术，工程落地缺 OSS | 加 P2.5 工程线：scan GitHub；选 1–2 个（策略/运行时/校验）；按 last_push + 采用/标准/生产判，不套论文 origin scope |
| 16 | 论文继续找边际收益递减；工程落地缺 OSS | 论文线冻结；P2.5 工程 OSS 升主线；选 1–2 个 active/高采用项目，补策略/执行/校验 |
| 17 | 论文/OSS 之外缺工程现场讨论 | 加 P2.6 Web 讨论线：2026 高影响 HN/Reddit/blog；卡写 `influence`；不升 E |

## 11. 执行结果（2026-11-09）

- **论文**：GGC（SG）、Glyph（US）、NLKGQ（DE）、KGVoyager（US）落 card+digest；旧/out-of-scope 的 2512/2507/2503/CK25/VAULT/SPARQL-LLM/CQ4OE/OntoExtend/QRAKEN/PPC 全部删除或未入库。
- **页面**：`03/querying`（F1–F3 / G1–G4）、`01/access-control`（F1–F3 / G1–G4）；派账本 03-L12–L15、01-L16–L18。
- **E**：E-21（querying）、E-22（access-control）；04 B.3/C.1 引 E；build A.2–A.5 保持 signal。
- **工程线**：OPA（策略层候选）、Qlever（执行层候选）入 card+digest+code-map；开源 6 个项目。
- **Web**：HN Netflix ontology observability（131 pts/32 comments）材料卡；不升 E。
- **自检**：`check_repo` 通过（462 文件；E=22，L=73；28 论文/6 开源）；04 仍 `draft`。
