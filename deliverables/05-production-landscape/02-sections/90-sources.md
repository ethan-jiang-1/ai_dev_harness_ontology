---
status: draft
updated: 2026-11-12
parent: ../README.md
---

# 90. 来源台账：哪些过门、哪些只是线索、哪些没找到

> 本页是 05 的出处层。读正文不需要打开它；要核数字/判断时再来。
> 准入判据以 [CHARTER §4](../../../CHARTER.md#4-素材准入material-gate) 为准；采/引前查 [来源黑名单](../../../meta/rules/excluded-sources.md)。

## 90.1 过门证据（admitted / probation）

| # | 来源 | 日期 | 类型 | 准入 | 关键事实 | 不能证明 |
|---|---|---|---|---|---|---|
| 1 | [中泰证券 QCon 上海 2026 议题页](https://qcon.infoq.cn/2026/shanghai/presentation/7345) · [卡](../../../src/web/qcon-2026-zhongtai-ontology/qcon-2026-zhongtai-ontology.card.md) | 2026-09-02 | talk | `admitted` | 900 万客户；6,000+ 指标（讲者简介另说 3,400+ 公司级指标）；7,000+ 同义词；三个退役判例；权限到属性级 | 单券商、摘要级、无成本/失败率/对照 |
| 2 | [中泰证券 CCSA TC601 WG15 案例](https://www.modb.pro/db/2110672293835923456) · [卡](../../../src/web/modb-2026-zhongtai-ontology/modb-2026-zhongtai-ontology.card.md) | 2026-10-15 | engineering | `admitted` | 9,137 知识目录/6,503 指标文档/2,622 表/12 万+ 血缘；DataAgent 生产；业务本体在信用业务验证 | 知识资产数≠本体覆盖；无成本/准确率；单公司 |
| 3 | [Snowflake 内部 context layer](https://www.snowflake.com/en/blog/snowflake-internal-context-layer-for-ai-agents/) · [卡](../../../src/web/snowflake-context-layer-2026/snowflake-context-layer-2026.card.md) | 2026-08-17 | engineering | `admitted (probation)` | 5,600 员工/320k 查询（2025-07）；400+ 用户/5,400+ 查询；semantic views 版本化/CI/eval；十亿行视图延迟、Dynamic Tables 维护爆炸 | 单公司自述；无外部采用；无成本/准确率 |
| 4 | [Sigma 2,883-model semantic layer](https://www.getdbt.com/blog/sigma-dbt-dagster-semantic-layer) · [卡](../../../src/web/sigma-semantic-layer-2026/sigma-semantic-layer-2026.card.md) | 2026-10-27 | engineering | `admitted (probation)` | 2,883 dbt 模型/63 job/6 region；SQL/Jinja 版本化；PII/列级控制；dbt Summit 2026 | 供应商自己跑自己的产品；无成本/失败/准确率 |
| 5 | [Netflix 本体驱动可观测性](https://netflixtechblog.com/ontology-driven-observability-building-an-end-to-end-knowledge-graph-at-netflix-scale-421392cf5adf) · [卡](../../../src/web/netflix-ontology-observability-2026/netflix-ontology-observability-2026.card.md) | 2026-10-16 | engineering | `admitted` | 49,000 目录；2B 请求/日；38M 日志/秒；65M 并发流；OWL/SHACL/SPARQL + 自建 QuipuDB；12 namespace | 无成本/收益；自建图存储是例外；假设有时错 |

**准入自检**：

| 门 | 中泰 QCon | 中泰 CCSA | Snowflake | Sigma | Netflix |
|---|---|---|---|---|---|
| G1 时效 ≥2026-06 | ✓ | ✓ | ✓ | ✓ | ✓ |
| G2 活跃 | QCon 2026 | CCSA WG15 2026 | Snowflake 2026 博客 | dbt Summit 2026 | Netflix 博客 2026-10 + HN 讨论 |
| G3 独立信号 | I2 中泰+QCon；I3 生产；I4 会议 | I2 中泰+CCSA；I3 生产；I4 案例 | I2 Snowflake+生态；I3 内部 5,600 人 | I2 Sigma+dbt；I3 生产；I4 Summit | I2 Netflix+W3C 栈；I3 生产；I4 HN 131 分/32 评论 |
| G4 来源 | 公司 talk（§4.4） | 公司案例（§4.4） | 公司工程博客（§4.4） | 公司工程博客（§4.4） | 公司工程博客（§4.4） |
| G5 可核 | URL+日期+讲者 | URL+日期+讲者 | URL+日期+作者 | URL+日期+作者 | URL+日期+作者 |

> `probation` 的两条（Snowflake/Sigma）是单公司自述，只作工程证据，不单独撑跨组织结论。按 [CHARTER §4.4.3](../../../CHARTER.md#44-三个窄例外)「发表后 6 个月内补第二信号」：Snowflake（2026-08-17）到期 **2027-02-17**、Sigma（2026-10-27）到期 **2027-04-27**；补不到就降 `signal` 并移出。

## 90.2 C 类 / signal 线索（未过门，只证“有方案/有讨论/有披露”）

| 线索 | 日期 | 它是什么 | 为什么只是 C |
|---|---|---|---|
| [Palantir 2026-10 公告](https://markets.businessinsider.com/news/stocks/palantir-announces-delivery-of-critical-sovereign-ai-outcomes-to-big-customers-1036651855) | 2026-10-21 | Foundry/AIP/Ontology/Apollo 在 L3Harris、McCarthy、Nvidia、Ondas/Regna、Tampa General 等落地 | 公司新闻稿；无规模/成本/失败；客户名单≠效果 |
| [阿里云 PolarDB 本体知识平台](https://www.alibabacloud.com/help/zh/polardb/polardb-for-postgresql/what-is-ontology-knowledge-platform) | 2026-10-21 | 数据库内嵌本体 + LLM 自动生成 + GraphRAG + Agent skills；灰度；按组件计费 | 厂商产品文档；无客户/规模/失败 |
| [阿里云 Context0 本体知识库](https://help.aliyun.com/zh/polardb/polardb-for-xscale/context0-build-ontology-knowledge-base) | 2026-09-23 | 知识库级 schema：类型≤100、关系≤300、每类型≤50 属性；版本/证据/抽取指令 | 同上；且是“薄本体”产品上限 |
| [蚂蚁 TuGraph](https://github.com/TuGraph-family/tugraph-db) | last push 2026-05-11 | 开源图数据库；Apache-2.0；1,768 stars/42 contributors；LDBC FinBench/金融风控 | `last_push`<2026-06-01，G1 失败；图库≠本体平台 |
| [腾讯 Topbase](https://zhuangxiaoyan.blog.csdn.net/article/details/155427520) | 2025-12-02 | 226 类概念/1 亿+实体/22 亿三元组；微信搜一搜/信息流/问答 | G1 超窗；二手技术文；无成本/失败 |
| [京东 Oxygen AIIC](https://arxiv.org/abs/2606.28070) | 2026-06-26 | 数百亿 SKU 商品本体；精度 94.2%/召回 82.8%；承认关系建模未规模化、线上失败、SFT 灾难性遗忘 | 公司自报、无独立采用；只能作 signal（规模+失败齐，但无独立信号） |
| [腾讯 DataBuddy](https://cloud.tencent.com/developer/article/2684075) | 2026-06-05 | 3,000+ 企业试用；两家匿名头部银行；95.9%（厂商口径） | 无具名客户/成本/失败；B-/C+ |
| [华为 DataArts](https://www.huaweicloud.com/product/dap.html) | 2026-10 公测 | 本体为平台底层知识核心；供应链 Agent 场景 | 公测；无客户/规模/失败；C |
| [阿里 UModel/STAROps](https://github.com/alibaba/UnifiedModel) | 2026-06-01 | 开源 + 阿里云内部可观测生产；458 stars/71 forks/6 contributors | 开源版不含控制面/多租户授权；无外部采用；B-/C+ |
| [银行 KG/本体采购](https://wap.stockstar.com/detail/RB2026072400019041) | 2026-05/07/10（浦发超窗） | 三单合同 ¥49.4 万/¥115 万/¥178.8 万；中标方海致星图/知因智慧/星环 | 不是九家大厂；只证需求/预算，不证效果 |
| [Anthropic 自助分析](https://claude.com/resources/articles/how-anthropic-enables-self-service-data-analytics-with-claude) | 2026-06-03 | 95% 查询自动化/~95% 准确；无 skills ≤21%；离线 95%→65%/月；对抗复核 +6% 准确/+32% token/+72% 延迟；LLM 自动生成 metric 定义 net-negative | 单公司工程博客；HN 讨论弱；只作机制证据 |
| [AngelList 放弃语义层](https://www.angellist.com/blog/the-semantic-layer-nobody-maintains) | 2026-08-28 | 1,400+ 模型/59 域/13k 行索引/27k 列；GitHub Actions “几美元/月”；“stale semantics worse than none” | 单公司；HN 2 分；无准确率；是换实现，不是项目失败 |
| [AWS Builder Center 语义层成本](https://builder.aws.com/content/3KvFN69cxO83mHPPRm71A5I820C/measuring-a-semantic-layer-evidence-cost-and-control-from-an-agentic-analytics-build) | 2026-10-19 | POC 50 用户/2,000 问/月；整层 $90–175/月；5 类 silent failure；live chat paraphrase agreement 4% | 客户匿名；POC；AWS 自证；只作量级线索 |
| [VentureBeat VB Pulse](https://venturebeat.com/data/companies-are-building-governed-semantic-layers-most-say-their-ai-agents-are-getting-context-somewhere-else) | 2026-10-06（报告 2026-11-06） | n=107/100；39% 生产用语义层；其中 28% 是 agent 主要上下文源（全体 13%）；采用者 78% vs 未采用 37% 报告上下文失败 | 自选样本、41% 顾问、不能推因果；只作弱信号 |
| [Atlan: KG pitfalls](https://atlan.com/know/ai-agent/knowledge-graph/enterprise-knowledge-graph-pitfalls/) | 2026-09-10 | “<15% 企业 KG 项目过 pilot”；组织/技术/经济三类失败 | **原始统计不可核**：追到 Improvado 2025-09-29 只有一句无出处的 “industry surveys suggest”；不采用该数字 |
| [Stardog customers](https://www.stardog.com/company/customers/) | 未标日期 | Boehringer Ingelheim、NASA、NIH、Springer Nature | 客户页/旧案例；未过 2026-06 门 |
| [Ontotext STM case](https://www.ontotext.com/knowledgehub/case-studies/leading-stm-publishers-improved-data-consumption-reuse-with-knowledge-platform/) | 未标日期 | 匿名 STM publisher 的知识平台 | 匿名+厂商案例；C |

> **C 类使用规则**：只在 [04 中国](./04-china.md) 的“方案存在”和 [06 案例台账](./06-cases.md) 的“线索”列出现；不写进 00/02 的判断，不撑采用/效果。

## 90.2b B 类「谁在投」信号（只证投入，不证效果）

| 信号 | 日期 | 它说明什么 | 不能证明 |
|---|---|---|---|
| CCSA TC601 WG15《本体智能研究报告（1.0）》 | 2026-07-24 | 中国标准工作组在编本体/知识管理标准，报告 1.0 公开（报道称 24 家联署） | 企业采用/效果；报告 2.0 尚未发布（计划 2026-12-15） |
| FIBO Forum（EDM Council） | 2026-09-22 | 金融业本体标准仍在活动；T. Rowe Price 等参与 | 生产部署/成本 |
| Alan Turing Institute KG/ontology 研究服务招标 | 2026-06-30 | 英国公共研究机构在采购 KG/本体服务（3–6 pilots） | 落地效果；合同是否授予 |
| Sciensano（比利时公共卫生）KG 平台招标 | 2026-07-31（OJ S 146/2026） | 政府机构真金白银采购知识图谱平台（约 €264k） | 谁中标、是否上线、效果 |
| dbt Summit 2026（Okta / ING / Sigma） | 2026-09-15/18 | 具名企业在讲语义层生产叙事 | 规模/成本/失败；演讲不等于结果 |
| KeyBank Ontologist 招聘 | 2026-08-25（抓取） | 银行在招 OWL/RDF/SKOS、TopBraid/Stardog 能力的人 | 已落地/效果；招聘只证明“准备投” |

> 这些是 **B 类“谁在投”**，不是生产证据；不要用它们推“行业已规模化”。

## 90.2c OKF / Wiki 底座选项（定义、产品、案例）

| 来源 | 日期 | 类型 | 它证明什么 | 不能证明什么 |
|---|---|---|---|---|
| [Google OKF v0.1](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) | 2026-06-12 | 官方博客/C（定义） | Markdown + YAML 的 concept bundle；受 Karpathy LLM Wiki 启发 | 采用/效果；不是标准组织标准 |
| [Google OKF v0.2](https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals) | 2026-07-24 | 官方博客/C（定义） | provenance/trust/freshness/lifecycle/attestation | 信任信号≠真实性；仍需 producer 审计 |
| [Google Knowledge Catalog 集成](https://cloud.google.com/blog/products/data-analytics/scale-okf-bundles-across-an-organization-with-knowledge-catalog) | 2026-08-26 | 官方博客/B（产品） | OKF bundle 可 push 成 Knowledge Catalog Entry，继承 IAM；Acme Retail 示例 9 leaf/17 entries | 客户采用/规模/效果；示例是合成 |
| [中泰 CCSA 案例](../../../src/web/modb-2026-zhongtai-ontology/modb-2026-zhongtai-ontology.card.md) | 2026-10-15 | engineering/admitted | 用 OKF 组织 9,137 知识目录/6,503 指标文档/12 万+ 血缘；业务本体验证中 | 业务本体全量；成本/准确率；单公司 |
| [Kunstenpunt Wikibase](https://tech-news.wikimedia.de/2026/06/02/kunstenpunt-a-whos-who-of-the-flemish-art-scene/) | 2026-06-02 | 工程博客/B | 100 万页/25 万实体/3 名专职/与 Wikidata 联邦；约束只警告不阻断 | 它是“先有本体/数据标准，再把 wiki 架上去”；单机构 |
| [京东海博 OKF](http://stock.10jqka.com.cn/20260924/c680274369.shtml) | 2026-09-24 | 媒体/B- | 一概念一 md、type 必填、index/log、宽容消费；AB 542 秒/快 44%；“编译前移到维护期” | 单一来源；无成本/失败率；780+ 商家是业务规模不是知识规模 |

> **最大缺口**：截至 2026-11-12，没有一条公开证据证明某组织完成“OKF/Wiki → 本体”的迁移；中泰最接近，但把图数据库/对象关系写在后续规划。

## 90.3 阴性结果：查过但没有过门的

| 想找什么 | 查了什么 | 结果 | 关闭它需要什么 |
|---|---|---|---|
| 中国大厂 2026-06 后**外部采用**（阿里/蚂蚁/腾讯） | 官网、云文档、开发者社区、会议、招聘、采购 | 阿里有产品文档（C）；蚂蚁 TuGraph 2026-05 后无 push；腾讯 Topbase 2025-12；**未找到具名外部客户+规模+失败** | 客户侧工程博客/会议 talk/采购公告；至少一条带规模或失败 |
| Palantir 客户侧**一手工程复盘**（2026） | Palantir 公告、客户新闻、会议 | 只有公司公告/客户名单；无客户自己写的规模/成本/失败 | 客户 engineering blog / conference industry talk |
| 本体/语义层**TCO/ROI** | 工程博客、会议、调研 | 无一条给出人月/金额/回收期；只有工作量代理 | 企业财务/采购披露，或带账本的复盘 |
| OKF 的企业级采用 | Google OKF 博客/GitHub/Knowledge Catalog；中国案例 | 西方 0 个具名生产用户；中国仅中泰、京东海博（后者单一来源）；无 A 类 | 具名组织 + 规模 + 成本/失败 + 独立印证 |
| **失败率** | Atlan/Improvado、HN、咨询报告 | 只有二手“<15%”说法，原始统计未核 | 可核的样本框+分母+年份 |
| **同数据集对照**（本体 vs 无本体） | 论文/工业报告 | 本窗口内未找到生产级对照 | 预注册的 A/B 或 shadow 对照 |

## 90.4 检索日志（摘要）

- 时间：2026-11-12。
- 检索面：美国重型平台/语义层、中国大厂/采用者、失败/成本、标准/招聘/采购、2026 工业论文。
- 关键词：`ontology production 2026`、`semantic layer production case study`、`Palantir ontology customer 2026`、`阿里云 本体 客户`、`蚂蚁 TuGraph 生产`、`腾讯 Topbase 2026`、`CCSA TC601 WG15`、`knowledge graph postmortem`、`ontology maintenance cost`、`FIBO EDM Council 2026`。
- 抓取限制：`web_fetch` 对部分域名被策略拒绝；改用 `curl` 或 `r.jina.ai` 读取；微信公众号多被 CAPTCHA，改用官网/会议页/转载。
- 黑名单：采/引前已查 [excluded-sources](../../../meta/rules/excluded-sources.md)；未使用命中源。
- 结论：**不是没搜，是这类材料稀缺**；05 的价值之一是把“缺什么”写清楚。
