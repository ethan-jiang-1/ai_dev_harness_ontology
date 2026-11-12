# 落地经济学 · 未发现与下一步

## 候选（signal，未过门；不得撑 E/L/交付物）

> 2026-11-12 为 [05 落地现状](../../../deliverables/05-production-landscape/README.md) 找"真实生产证据"时的候选。全部**未过 G3**（缺第二个独立信号），只作线索。

| 候选 | 日期 | 主张什么 | 卡在哪 | 若过门能支撑什么 |
|---|---|---|---|---|
| [EDM Council「Why Your AI Needs an Ontology: Getting Started with FIBO」](https://edmcouncil.org/wp-content/uploads/2026/08/EDMWebinar_AI-Needs-and-Ontology-FIBO_2026-08-25_FINAL.pdf) | 2026-08-25 | 标准组织在推 FIBO-for-AI；含一组文档抽取成本对比（准确率 76%→95%、每文档 $0.39→$0.14、每查询 $0.21→$0.02） | **G3 只有标准组织自身一个信号**；且那组数字比的是「Claude 单模型 vs 模块化流水线」，**不是本体 vs 无本体**；无生产规模披露 | 2026 年标准组织的活跃度；一组**抽取流水线**成本基准（不可当本体效应） |
| [京东海博 AI 知识库（自称 OKF）](http://stock.10jqka.com.cn/20260924/c680274369.shtml) | 2026-09-24 | 一概念一 md、`type` 唯一必填、index/log、宽容消费；AB 542 秒 vs 967 秒（约 -44%）；编译前移到维护期 | 单一来源、无个人署名；**原文 5 次 “OKF” 从未展开**，“= Google OKF” 是推断 | 拿到京东技术原文 + 第二独立来源后，可作中国第二个 OKF 采用线索 |
| [Kunstenpunt Wikibase](https://tech-news.wikimedia.de/2026/06/02/kunstenpunt-a-whos-who-of-the-flemish-art-scene/) | 2026-06-02 | 100 万页/25 万实体/3 名专职；约束只警告不阻断；**先有本体/数据标准，再把 wiki 架上去** | 单机构、平台方博客；**与 OKF 无关**（全文 0 次 OKF/ontology） | 第二独立报道出现后，可作“本体驱动 wiki”反例（不撑 OKF） |
| Neo4j Aura Agent（ontology-driven agents） | 2026 | 厂商宣称 production-ready | G4 厂商自证；无独立采用 | 只作"有产品在卖"的线索 |
| FAOS 神经符号架构（宣称准确率 +46%） | 2026 | 本体约束推理提升 agent 准确率 | G4 厂商/自媒体；无同行评审、无复现 | 若出现独立复现，可作机制证据 |
| 中文媒体多篇（Palantir 本体论、金融本体落地"十问十答"等） | 2026 | 本体商业化与落地经验 | G4 二手综述/公众号；无一手规模数据 | 只作"国内在讨论"的线索 |

> **判断**：截至目前，窗口内（≥2026-06）**没有找到披露真实规模与失败的生产系统报告**。2026-11-12 复核另加两条判定：① **五家大厂平台 2026-06 后具名客户 = 0**（逐平台检索；能过门的是海致/星环/金山云/中电云/中科世通亨奇与三家农商行自建）；② **没有上线后被关停的本体/KG 项目的第一方复盘**（中国 7 例流标都在授标前，且已重新采购/转谈判）。这不是检索失败，是这类材料本来稀缺——05 的空缺应如实保留，不得用上述候选填充。

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
