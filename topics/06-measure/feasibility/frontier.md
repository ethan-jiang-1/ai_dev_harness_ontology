# 落地经济学 · 未发现与下一步

## 候选（signal，未过门；不得撑 E/L/交付物）

> 2026-11-12 为 [10 落地现状](../../../deliverables/10-production-landscape/README.md) 找"真实生产证据"时的候选。全部**未过 G3**（缺第二个独立信号），只作线索。

| 候选 | 日期 | 主张什么 | 卡在哪 | 若过门能支撑什么 |
|---|---|---|---|---|
| [AstraZeneca Research Assistant](https://arxiv.org/abs/2608.12395) | 2026-08-06 | 药企内部 LLM + KG 系统；**15,000 名内部用户/首年**；响应 10–30 秒 | 19 作者全属 AstraZeneca（无 I2）；技术报告、无同行评审；无失败/成本披露 | 补到独立采用/社区讨论后可作「企业内 KG 系统规模」的 admitted |
| [Same Context, Different Agents](https://arxiv.org/abs/2610.20959) | 2026-10-14 | 7 模型/1,514 任务/5 benchmark；语义层等三种 context 技术的受控对照；语义层收益依赖 agent 行为 | 学术研究、非生产；无企业部署 | 可作 G6 的学术对照；不撑生产效果 |
| [Auditable by Construction（KDAF）](https://arxiv.org/abs/2608.20661) | 2026-08-21 | 本体驱动 + 证据链的企业金融分析框架；FinanceBench 145 问；有 Zenodo 工件 | **单作者、独立研究者**；只在公开基准上评，无生产部署（G3/G4 不过） | 出现企业部署后重评；现只作 C |
| [小红书 DIBP（QCon 上海 2026 议题）](https://qcon.infoq.cn/2026/shanghai/presentation/7343) | 2026-10-22/24 | 2026-02 起建的 DataAgent Context Layer；覆盖 80%+ 员工、主动会话周活 8,800+；数据/指标/业务语义/代码/血缘统一表征 | 议题摘要，无成本/失败；**不是 OWL 本体**；G3 只 QCon 一个信号 | 中国互联网侧「语义层/Context Layer 在生产」的 B 级采用证据；补到讲稿/视频里的失败与规模后可升 |
| [江西农商 隐性关联图谱](https://www.fintechinchina.com/cases/9803) | 2026-09-29 | 投入 **<50 万元**（上限）；2026-05→08 上线、10 月推广 86 家；6 试点机构/68 用户/3,000+ 隐性关系；三层解耦含「业务语义层」 | 客户自述 + 行业评选；口径未说明（疑不含外部数据采购）；无失败披露；G3 无独立信号 | 中国农商行的**成本上限 + 周期**锚点；出现独立复核可升 admitted |
| [江南农商 新范式知识库](https://www.fintechinchina.com/cases/9766) | 2026-09-22 | **12 个月、3 人核心组**（≈36 人月）；2,000+ 知识页/500+ DAU；文档整理 2.7→0.27 工时/份，年省 ~1,200 工时 | 同上；工时节约为自报估算，非实测账本 | 少见的「团队 × 月数」人月锚点；出现实测工时/审计后可升 |
| [NHS FDP × Palantir（Guardian/Register）](https://www.theguardian.com/technology/2026/nov/02/palantir-unused-nhs-hospital-trusts) | 2026-11-02/03 | £330M 合同；137 家「realising benefits」中 **29 家** FOI 回复未上线/未使用其应用（约 21%）；OSR 介入 | 调查报道 + FOI，不是工程复盘；谈 FDP 使用，不谈 Ontology 深度；G4 媒体 | 「平台宣称 vs 客户使用」落差的证据；补到客户侧工程复盘后可升 |
| [EDM Council「Why Your AI Needs an Ontology: Getting Started with FIBO」](https://edmcouncil.org/wp-content/uploads/2026/08/EDMWebinar_AI-Needs-and-Ontology-FIBO_2026-08-25_FINAL.pdf) | 2026-08-25 | 标准组织在推 FIBO-for-AI；含一组文档抽取成本对比（准确率 76%→95%、每文档 $0.39→$0.14、每查询 $0.21→$0.02） | **G3 只有标准组织自身一个信号**；且那组数字比的是「Claude 单模型 vs 模块化流水线」，**不是本体 vs 无本体**；无生产规模披露 | 2026 年标准组织的活跃度；一组**抽取流水线**成本基准（不可当本体效应） |
| [京东海博 AI 知识库（自称 OKF）](http://stock.10jqka.com.cn/20260924/c680274369.shtml) | 2026-09-24 | 一概念一 md、`type` 唯一必填、index/log、宽容消费；AB 542 秒 vs 967 秒（约 -44%）；编译前移到维护期 | 单一来源、无个人署名；**原文 5 次 “OKF” 从未展开**，“= Google OKF” 是推断 | 拿到京东技术原文 + 第二独立来源后，可作中国第二个 OKF 采用线索 |
| [Kunstenpunt Wikibase](https://tech-news.wikimedia.de/2026/06/02/kunstenpunt-a-whos-who-of-the-flemish-art-scene/) | 2026-06-02 | 100 万页/25 万实体/3 名专职；约束只警告不阻断；**先有 2024 文化参与数据标准（兼容 CIDOC CRM/schema.org），再把三套旧库并进 Wikibase** | 单机构、平台方博客；**与 OKF 无关**（全文 0 次 OKF/ontology）；“数据标准”≠“OWL 本体” | 第二独立报道出现后，可作“数据标准先行的 wiki”反例（不撑 OKF） |
| [Linked.Archi · OKF and Linked.Archi](https://meta.linked.archi/docs/practice/okf-open-knowledge-format/) | 2026-07-17 | OKF 在 DIKW 的 Data→Information；本体→OKF 可机械投影但丢关系类型；OKF→本体 lift 需作者提示/人审；把“关系定型缺口”称为两层的缝；“多数组织会先 OKF、再把高价值域提升到图” | 单项目/自出版文档；GitHub org 仓库 2026-09 起、star 极少；无独立采用（G3 不过） | 作“非对称投影”的工程文档之一（C）；不撑 OKF 采用/迁移 |
| [Atlas · OKF interop spike](https://github.com/AtlasDevHQ/atlas/blob/main/docs/research/okf-interop-spike.md) | 2026-07-02 | 导出“全但丢语义”；导入“有用但有损的草稿生成器”；表白名单/运行时执行无 OKF 对应物；`okf.unverified_sql` 防止未验证 SQL 升格 | 公司工程文档；仓库 1★；spike 未产品化（G3/G4 不过） | 第二份独立实现的映射证据（C） |
| [GMEOW · OKF](https://github.com/Blackcat-Informatics/gmeow-ontology/blob/main/docs/okf.md) | 2026 | OKF = 有损下投影；封闭 `okf:` profile；lift 回 RDF；OWL 公理/RDF-star/对齐留在 canonical 源 | 单项目自出版；无独立采用 | 第三份实现互证（C） |
| [SCIMIN-CRM · Semantic MediaWiki](https://ceur-ws.org/Vol-4293/paper50.pdf) | 2026-10-13 | **本体先行**：OWL 本体 + SMW 标注（category→类、page 属性→对象属性）；LLM 只产候选，自动校验（domain/range、datatype、hallucination）+ 专家 HITL 后才进生产；受控发布 | **承建方（AKKODIS Research）写自己的系统**：G3 的“多机构/I3 采用”都来自同一个 Horizon Europe 项目内部，**不是独立采用**；无量化/规模/成本（论文自述 future work 才做评估） | 出现独立评估（外部用户/规模/失败）后，可作“本体先行 wiki”的 engineering 证据；**现只作线索** |
| Neo4j Aura Agent（ontology-driven agents） | 2026 | 厂商宣称 production-ready | G4 厂商自证；无独立采用 | 只作"有产品在卖"的线索 |
| FAOS 神经符号架构（宣称准确率 +46%） | 2026 | 本体约束推理提升 agent 准确率 | G4 厂商/自媒体；无同行评审、无复现 | 若出现独立复现，可作机制证据 |
| 中文媒体多篇（Palantir 本体论、金融本体落地"十问十答"等） | 2026 | 本体商业化与落地经验 | G4 二手综述/公众号；无一手规模数据 | 只作"国内在讨论"的线索 |

> **判断**：截至目前，窗口内（≥2026-06）**没有找到披露真实规模与失败的生产系统报告**。2026-11-12 复核另加两条判定：① **五家大厂平台 2026-06 后具名客户 = 0**（逐平台检索；能过门的是海致/星环/金山云/中电云/中科世通亨奇与三家农商行自建）；② **没有上线后被关停的本体/KG 项目的第一方复盘**（中国 7 例流标都在授标前，且已重新采购/转谈判）。这不是检索失败，是这类材料本来稀缺——05 的空缺应如实保留，不得用上述候选填充。
>
> **2026-11-12 补记（SCIMIN 判定）**：SCIMIN/SMW 论文最初按 `admitted` 建卡，复核后**降为 `signal` 并移出 `src/`**——它是承建方对自己 demonstrator 的自述，G3 的独立信号不成立（详见 [04b 审计](../../../meta/audits/2026-11-12-04b-okf-provenance.md#7-处置结果2026-11-12-当日关闭)）。
>
> **2026-11-12 补记（OKF/本体映射线）**：另检索到 Zenodo「NKB-OKF-Superset」技术 note（2026-08-08）与 SAP community「Agent Memory in S/4HANA: why we store OKF in Z tables」；两者当日抓取被 403/Cloudflare 拦截，**未核不引**，列为待评估。OKF 的企业采用与“OKF→本体迁移”仍无 admitted 证据；Linked.Archi / Atlas / GMEOW 三份实现只互证“映射非对称”，**不证采用**。

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | 部署层回报 | 治理/上手/审计仍定性 | 部署测量协议 | CAI/N&D | 高 |
| G2 | false-veto / false-defer | 护栏/授权的隐性成本 | 标注 blocked decisions | POLAR/Commit Boundary | 高 |
| G3 | 维护成本 | 本体/投影/registry 长期人工 | 工时测量 | 工程复盘 | 高 |
| G4 | 自有配置方差 | 54% 是别人的估计 | 重复采样 | 自有采样（仓库外） | 中 |
| G5 | 跨域迁移 | 工业/金融/医学/电网边界不同 | 统一对照 | 多域案例 | 中 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变 | 成本 |
|---|---|---|---|---|
| N1 | 部署指标 | `deployment metrics ontology governance` | F1 / G1 | 高 |
| N2 | false-veto 标注 | POLAR block log；`false veto guardrail annotation` | F1/F3 / G2 | 中 |
| N3 | 维护工时 | `ontology maintenance cost case study` | F1 / G3 | 中 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-08 | 22 篇综合 | F1–F6 成形；G1–G5 明确 | 先做 G1/G2/G3 |
| 2026-11-08 | G-X 吸收复核（CAI/POLAR/CASEL） | 单位经济学/NPV、校准协议、γ CI stop 已补进 mechanism/findings；其余机制细节归各派 | 复跑 G-X |

## digest 吸收边界（G-X）

> 本页引用一律写 arXiv 编号或论文名，不用审计矩阵的 D-ID——`absorption-matrix.md` 的 D-03、D-06–D-10 与 [digest-ledger](../../../meta/archive/2026-11/full-audit/digest-ledger.md) 不一致（例：矩阵 D-03=POLAR、D-06=CASEL、D-10=Grid；ledger D-03=CASEL、D-06=FIRME、D-10=POLAR）。矩阵侧待整表对齐，不在本页范围。

| digest 工程发现 | 状态 | 落在哪 / 为什么不进来 |
|---|---|---|
| CAI `p_min`/`c`/`Q`、miss 敏感度、φ 抽样 100→400、3× 时延（仅 7 题） | 吸收 | [mechanism §三个可算的盈亏平衡](./mechanism.md#三个可算的盈亏平衡)、§实施与客户价值 |
| POLAR 人日（Layer A 2–5、Layer B 1–2 人周）、φ/τ 账本字段、false-veto stop | 吸收（成本/账本/stop 视角） | [mechanism §组织/成本](./mechanism.md#组织成本)、[§数据/接口](./mechanism.md#数据接口)、§stop condition |
| POLAR Layer A/B schema、DecisionPolicy 接口、反向搜索参数 | 不重复 | 控制器细节已由 [01/action-gate](../../01-constraint/action-gate/mechanism.md) 吸收 |
| CASEL E4 单位经济学、NPV 决策线 | 吸收 | [mechanism §单位经济学](./mechanism.md#单位经济学e4把单价代进公式)、[findings F5](./findings.md) |
| CASEL 校准协议（Eq(5) 40k/160k、disjoint、one record/trajectory、κ≥0.6） | 吸收 | [mechanism §数据/接口](./mechanism.md#数据接口)、[findings F6](./findings.md) |
| CASEL γ CI stop（±3pp、只上静态 gate、AUC 未显著更低） | 吸收 | [mechanism §stop condition](./mechanism.md#stop-condition) |
| CASEL `c_base` 锚点、动作混合 58/28/14、approve `ĉ≥0.55` | 不重复 | 控制器参数已由 [01/action-gate](../../01-constraint/action-gate/mechanism.md) 吸收；本页只在账本与分母敏感性里用到动作混合 |
| CAI 工具 schema、topN=20/k=100/anchor 20 | 不适用 | 检索参数归 [03/compilation](../../03-knowledge/compilation/mechanism.md) |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| 部署测量协议 | 补治理回报 | 待扫描 | N1 |
| false-veto 标注 | 护栏隐性成本 | 待扫描 | N2 |
