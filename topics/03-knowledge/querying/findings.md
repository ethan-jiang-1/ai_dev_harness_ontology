# 查询 · 发现（F）

> 只放已经能站住的判断。`F` 编号是子主题局部编号；跨页引用写 `querying/Fx`。
> 三条路线没有头对头；每条的数字都带条件，不能相加、不能互推。

## 索引
> **2026-11-12 对账（等级以 README 为准）**：本页索引里的「已核」是**撤源前**的记录；支撑它的来源已按 [CHARTER §4](../../../CHARTER.md#4-素材准入material-gate) 移出，这些条目现等级见 [README](./README.md)（多已降 `推测`/`withdrawn`）。**引用请用 README 的等级，不要用本页索引的历史等级。**


| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | GGC 的选择性纠错在 MCQA 单 KG 上把答案集匹配率 90.23→98.33；全量纠错只到 92.34 | `已核`（数字）/ `推测`（跨域） |
| F2 | NLKGQ 把完整 OWL ontology 放进单次上下文，DBLP-QuAD 3.1 上 89.9% Match / 81.3% Exact；单 snapshot | `已核`（单系统）/ `推测`（跨域） |
| F3 | KGVoyager 不依赖 ontology/examples，4 个小型 benchmark 上平均 F1 +3.7pp（64.6 vs 60.9），不是 4× | `已核`（数字）/ `推测`（跨域） |

## 怎么读

- 想看机制：去 [mechanism.md](./mechanism.md)。
- 想看缺口/下一步：去 [frontier.md](./frontier.md)。
- 想看原始材料：各条末尾的 digest 链接；`card.md` 只作 provenance。

## F1 · GGC：先判该不该改，再改

- **判断**：LLM 生成的 SPARQL 大多“能跑但语义错”；GGC 用监督 Gate 在 `(问题, 初始 query)` 上判风险，只把高风险 query 送进 Corrector。MCQA 上答案集匹配率从 90.23% 到 98.33%，但**全量纠错只有 92.34%**——增益来自“选择性”，不是“纠错本身”。
- **数字与条件**：
  - 数据：MCQA，电影域，**单 KG**（iMKG，论文称 based on Wikidata + MovieKG）；训练 119,409 / 验证 15,785 / 测试 31,570；关系/实体靠 `rdfs:label` 匹配，禁用 `wdt:` 直属性。
  - 模型：Generator = Llama-3.2-3B-Instruct LoRA SFT（12,450 样本）；Gate = RoBERTa-base 二分类，输入 `[NLQ; 初始 query]`，标签为初始 query 对/错（gold 离线造），τ=0.5；Corrector 只在这 9.31% 上跑。
  - 指标：`Query Acc.` = 生成 query 与 gold query 的**答案集匹配率**；不是执行成功率，也不是字符串匹配；判等细节未报告。31,570×(1−90.23%)≈3,085，与 Table 3 错例总数对上。
  - 主结果（Table 2, p.6）：Generator-only **90.23%**；全量纠错 **92.34%**；选择性纠错 **98.33%**（默认 W1.0+C0.2）。推理：单跑 ~30h、选择性 ~33h、全量 ~60h；**45% 是相对全量纠错的墙钟**，比单跑多约 10%。
  - Gate（Table 4, p.8）：FPR 0.31%、trigger 9.31%、recall 92.11%；阈值 0.25–0.75 三点 F1 94.24–94.49，未测两端。
  - 改对/改坏：**没有 2×2 配对矩阵**；Table 12 只有子集级（Originally Wrong 85.20%、Originally Correct 99.99%）+ 三个单例（C.1 改对 / C.2 改坏 / C.3 修不动）。空结果没有专门机制、没有测量。
  - 内部不一致（已核，引用前回表）：SciQA 正文 80.70→91.62 与 Table 13b 88.09→94.47 矛盾；Table 5b 与 5c 的“不带反馈/W1.0”行数字相同；Table 12 反推总准确率≈98.54%，Table 2 报 98.33%，差约 65 题未解释。
- **边界**：单域/单 KG/单 3B 骨干/单 seed；无 CI/重复；Gate 依赖分布内监督，跨生成器/跨 KG/跨 schema 未测；45% 是墙钟，不是 FLOPs；没有部署证据。
- **来源**：[GGC digest](../../../src/papers/2607.28082-ggc/digest.md) §3–§5、§8；arXiv:2607.28082v1；[card](../../../src/papers/2607.28082-ggc/card.md) 只作 provenance。
- **等级**：`已核`（数字，Table 2/4/5, p.6–8）/ `推测`（跨域）。

## F2 · NLKGQ：完整 OWL 进上下文

- **判断**：把**完整领域 OWL ontology**（Turtle）与 SPARQL system prompt、domain rider、用户问题一起放进**单次** LLM 调用，零样本生成 SPARQL；原生词汇不透明时用 wrapper ontology + 确定性 runtime rewriter 还原。它把“ontology 表示”单独作为变量，不是 prompt 工程。
- **数字与条件**：
  - 数据：DBLP-QuAD **3.1**（作者修订的确定性参考，1,000 题）；DBLP-QuAD **2.0**（5,000 对，1,000 题测试，确定性协议重算）；SemOpenAlex（100 题）；neuroimaging（21 题，前作）。
  - 模型：主 Qwen3.6-27B；10 个开源权重模型扫描；单次调用、temperature 0.0、无 fine-tune、无 few-shot、无 entity linking；QLever；单一固定 snapshot。
  - 指标：**Match** = 生成结果包含参考结果（允许 superset）；**Exact** = 严格相等；QuAD F1 / SPINACH F1 只作可比性。
  - 主结果：QuAD **3.1** native 74.9% Match / 56.0% Exact → +dblpx wrapper **89.9% Match / 81.3% Exact**；wrapper +15.0 Match / +25.3 Exact（同模型/提示/数据）。QuAD **2.0** 确定性协议 native 52.9/11.3 → wrapper **57.6/20.1**；wrapper 在未修订 2.0 上 +9.9 Match，说明增益不是 3.1 造出来的。SemOpenAlex 98/100；neuroimaging 21/21。
  - 口径：89.9% 是 **Match（允许 superset）**，81.3% 才是 Exact；3.1 是作者修订的参考，不是官方榜；与 2.0 分数不可直接比。
  - 10 模型：Qwen3.6-27B 是主配置；小模型明显更低；完整表在 Table 4，引用带模型/规模。
- **边界**：单作者 preprint、无同行评审、无独立复现；单 snapshot/单 endpoint 为主；完整 ontology 每次进上下文，词汇超窗口时需要选择/缩减，本文未处理；entity linking 不在范围（266 题带 bracketed URI）；闭源模型未测；QuAD 3.1 的修复与所评系统同一作者。
- **来源**：[NLKGQ digest](../../../meta/audits/2026-11-11-source-purge.md#src-2609-14652) §3–§5、§8；arXiv:2609.14652v1；[card](../../../meta/audits/2026-11-11-source-purge.md#src-2609-14652) 只作 provenance。
- **等级**：`已核`（单系统/数字，Table 2–4, p.6）/ `推测`（跨域）。

## F3 · KGVoyager：不依赖 ontology 的 agentic navigation

- **判断**：领域 KG 常没有 ontology、没有 text–SPARQL 例子，只剩 endpoint；KGVoyager 用 think–act–observe + search/exploration/execution 三类工具，运行时把问题词映射到 IRI、探结构、用执行反馈改草稿；只预置一个 KB 级 class index。它在 4 个小型 benchmark 上平均 F1 64.6% vs GRASP 60.9%（**+3.7pp，不是 4×**），成本/墙钟更低。
- **数字与条件**：
  - 数据：4 个 benchmark 共 394 题——Climate Models KG（108）、SOCKG（98）、DREAM-KG（88）、DBLP-QuAD（100，test split 抽样）；前三者题–query 对由各 KG 作者提供。
  - 模型/基线：GPT-6 Sol、GPT-OSS-120B、Nemotron 3 Ultra、Muse Glimmer 30B；主基线 GRASP（被给了 entity index 的“最好情况”），另加仅 SOCKG 的 Grep Ontology 基线。
  - 指标：Spinach row-major F1；成本（$）、迭代数、墙钟、工具调用/执行次数。
  - 主结果（Table 3, p.7）：4 benchmark × 4 骨干 × 3 次运行，平均 F1 **64.6 vs 60.9（+3.7pp，相对 +6.1%）**；成本 **$2.43 vs $3.94（−38.3%）**；迭代 **19.6 vs 23.4**；墙钟 **85.6s vs 112.4s（−23.8%）**。原文摘要说“~4 points”，对应 +3.7pp；不是 4 倍。
  - class index：28 个 okn.us endpoint 扫描，class index 在 Jena 下可建 ~68%；entity index 对多数 endpoint 不可行（GRASP 的前提）。
  - 消融（Table 4）：移除 exploration 在三对比较上掉 1.5–8.6 分；search/execution 工具始终需要；domain/range 搜索工具在 full 与 ablated 都被隐藏（实现细节）。
  - 失败分析：156 例两级分类；主要失败是 schema/词汇不匹配、执行错误、答案格式。
- **边界**：只支持用 `rdf:type` 标注类型的图；Wikidata 那类自有类型体系不直接支持，要 adapter；4 个 benchmark 都小（88–108 题），三个题集同源（Proto-OKN 作者/基础设施），不是 4 个独立域；单系统基线 GRASP；成本口径未报告；preprint/匿名仓库、无独立复现。
- **来源**：[KGVoyager digest](../../../meta/audits/2026-11-11-source-purge.md#src-2609-01780) §3–§5、§8；arXiv:2609.01780v2；[card](../../../meta/audits/2026-11-11-source-purge.md#src-2609-01780) 只作 provenance。
- **等级**：`已核`（数字，Table 3/4, p.7–8）/ `推测`（跨域）。

## 三条路线不能互推

| 路线 | 代表 | 它改变哪一步 | 它不能证明 |
|---|---|---|---|
| 生成后纠错 | GGC | 生成之后、执行之前加 Gate/Corrector | 跨生成器/跨 KG；净收益配对 |
| ontology-in-context | NLKGQ | 生成之前的上下文表示 | 大本体/跨 endpoint/闭源模型 |
| ontology-free navigation | KGVoyager | 生成之前的探索/工具 | 跨图类型体系；大 benchmark |

> 三者没有头对头；把 98.33%、89.9%、64.6 放一张表比较是范畴错误。
