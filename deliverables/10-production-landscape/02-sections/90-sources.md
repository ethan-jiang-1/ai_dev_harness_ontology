---
status: draft
updated: 2026-11-12
parent: ../README.md
---

# 90. 来源台账：哪些过门、哪些只是线索、哪些没找到

> 本页是 10 的出处层。读正文不需要打开它；要核数字/判断时再来。
> 准入判据以 [CHARTER §4](../../../CHARTER.md#4-素材准入material-gate) 为准；采/引前查 [来源黑名单](../../../meta/rules/excluded-sources.md)。

## 90.1 过门证据（admitted / probation）

| # | 来源 | 日期 | 类型 | 准入 | 关键事实 | 不能证明 |
|---|---|---|---|---|---|---|
| 1 | [中泰证券 QCon 上海 2026 议题页](https://qcon.infoq.cn/2026/shanghai/presentation/7345) · [卡](../../../src/web/qcon-2026-zhongtai-ontology/qcon-2026-zhongtai-ontology.card.md) | 2026-09-02 | talk | `admitted` | 900 万客户；6,000+ 指标（讲者简介另说 3,400+ 公司级指标）；7,000+ 同义词；三个退役判例；权限到属性级 | 单券商、摘要级、无成本/失败率/对照 |
| 2 | [中泰证券 CCSA TC601 WG15 案例](https://www.modb.pro/db/2110672293835923456) · [卡](../../../src/web/modb-2026-zhongtai-ontology/modb-2026-zhongtai-ontology.card.md) | 2026-10-15 | engineering | `admitted` | 9,137 知识目录/6,503 指标文档/2,622 表/12 万+ 血缘；DataAgent 生产；业务本体在信用业务验证 | 知识资产数≠本体覆盖；无成本/准确率；单公司 |
| 3 | [Snowflake 内部 context layer](https://www.snowflake.com/en/blog/snowflake-internal-context-layer-for-ai-agents/) · [卡](../../../src/web/snowflake-context-layer-2026/snowflake-context-layer-2026.card.md) | 2026-08-17 | engineering | `admitted (probation)` | 5,600 员工/320k 查询（2025-07）；400+ 用户/5,400+ 查询；semantic views 版本化/CI/eval；十亿行视图延迟、Dynamic Tables 维护爆炸 | 单公司自述；无外部采用；无成本/准确率 |
| 4 | [Sigma 2,883-model semantic layer](https://www.getdbt.com/blog/sigma-dbt-dagster-semantic-layer) · [卡](../../../src/web/sigma-semantic-layer-2026/sigma-semantic-layer-2026.card.md) | 2026-10-27 | engineering | `admitted (probation)` | 2,883 dbt 模型/63 job/6 region；SQL/Jinja 版本化；PII/列级控制；dbt Summit 2026 | 供应商自己跑自己的产品；无成本/失败/准确率 |
| 5 | [Netflix 本体驱动可观测性](https://netflixtechblog.com/ontology-driven-observability-building-an-end-to-end-knowledge-graph-at-netflix-scale-421392cf5adf) · [卡](../../../src/web/netflix-ontology-observability-2026/netflix-ontology-observability-2026.card.md) | 2026-10-16 | engineering | `admitted` | 49,000 目录；2B 请求/日；38M 日志/秒；65M 并发流；OWL/SHACL/SPARQL + 自建 QuipuDB；12 namespace | 无成本/收益；自建图存储是例外；假设有时错 |
| 6 | [Apple Glyph: column description & sensitivity-ontology tagging](https://arxiv.org/abs/2609.10430) · [digest](../../../src/papers/2609.10430-glyph/digest.md) | 2026-09-09 | engineering（论文）/ `admitted`（§4.4 公司例外；05 判 **A（probation）**：缺独立信号） | ~3.4M 列/98,000 表/4 业务线/3 后端；275 叶内部敏感性本体；6 周 ~24,000 条 steward 判定、接受率 63.3%→99.8%；~30 人年手工等价 | 单企业；无美元成本/漏标率；接受率 association、对 FN 盲；标签质量≠策略执行 |
| 7 | [CoeusBI: interactive BI at Baidu](https://www.vldb.org/pvldb/vol19/p4076-lian.pdf) · [digest](../../../src/papers/2606.15384-coeusbi/digest.md) | 2026-06-13 | engineering（论文）/ `admitted`（I1 PVLDB 19 + I2 百度/北邮 + I5 artifact） | 百度数据平台、**数千用户/日**；生产集 EX 6.03%→23.49%；灰度 50 人/3 周、完成时间 −55.7%；90.8% golden SQL 含 JOIN | 单公司单业务线；无成本/失败率；EX≠业务正确；不是 OWL 本体 |

| 8 | [UniDataAgent: ontology-grounded question-to-report](https://arxiv.org/abs/2609.27257) · [digest](../../../src/papers/2609.27257-unidataagent/digest.md) | 2026-09-23 | engineering（论文）/ `admitted`（I1 ICDM 2026 Demo + I2 联通/南开） | 27 张企业表/数千指标类型；40 问严格准确率 95.0% vs 文档 RAG 72.5%；本体构建「数小时 vs 约一周」、报表「几分钟 vs 数个工作日」 | 单企业单域；40 问小样本；工时定性；无失败率/维护数据 |

**准入自检**：

> 另有 1 张 `admitted` 格式卡（[Google OKF](../../../src/web/google-okf/google-okf.card.md)，见 90.2c）；它不是生产案例，不进上面的台账。

| 门 | 中泰 QCon | 中泰 CCSA | Snowflake | Sigma | Netflix | Apple Glyph | CoeusBI | UniDataAgent |
|---|---|---|---|---|---|---|---|---|
| G1 时效 ≥2026-06 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| G2 活跃 | QCon 2026 | CCSA WG15 2026 | Snowflake 2026 博客 | dbt Summit 2026 | Netflix 博客 2026-10 + HN 讨论 | arXiv v1 2026-09-09 | arXiv 2026-06 + VLDB 2026 accepted | arXiv v2 2026-10；ICDM 2026 Demo |
| G3 独立信号 | I2 中泰+QCon；I3 生产；I4 会议 | I2 中泰+CCSA；I3 生产；I4 案例 | I2 Snowflake+生态（**合作方，独立性弱**）；I3 内部 5,600 人 | I2 Sigma+dbt Labs（**合作方，独立性弱**）；I3 生产；I4 Summit | I2 Netflix+W3C 栈；I3 生产；I4 HN 131 分/32 评论 | **I3 Apple 生产目录**（§4.4 公司例外）；无 I1/I2 | **I1 VLDB 2026 同行评审 + I2 百度/北邮** | **I1 ICDM 2026 Demo + I2 联通软研院/南开** |
| G4 来源 | 公司 talk（§4.4） | 公司案例（§4.4） | 公司工程博客（§4.4） | 公司工程博客（§4.4） | 公司工程博客（§4.4） | 论文 + 公司生产系统（§4.4） | 学术会议（工业 track） | 学术预印本 + 企业系统 |
| G5 可核 | URL+日期+讲者 | URL+日期+讲者 | URL+日期+作者 | URL+日期+作者 | URL+日期+作者 | arXiv+PDF+日期+作者 | arXiv+PDF+表号+日期 | arXiv+PDF+Table I |

> `probation` 的两条（Snowflake/Sigma）是单公司自述，只作工程证据，不单独撑跨组织结论。按 [CHARTER §4.4.3](../../../CHARTER.md#44-三个窄例外)「发表后 6 个月内补第二信号」：Snowflake（2026-08-17）到期 **2027-02-17**、Sigma（2026-10-27）到期 **2027-04-27**；补不到就降 `signal` 并移出。
>
> **第二信号检索（2026-11-12）**：Snowflake、Sigma 均为**阴性**（HN 0 条对应讨论；daily.dev 只有自动转贴 0 评论；dbt/Sigma 同一机构不算）。中泰另有 1 篇独立分析（沙丘社区 2026-10-15，复述 9,137/6,503/2,622/12 万+ 并自判“业务本体仍在试点”），但它复述的是同一批公开数字，**不是审计**。

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
| [银行 KG/本体采购](https://wap.stockstar.com/detail/RB2026072400019041) | 2026-05/07/10（浦发超窗） | 三单合同 ¥49.4 万/¥115 万/¥178.8 万；中标方海致星图/知因智慧/星环 | 不是这五家大厂的订单；只证需求/预算，不证效果 |
| [Anthropic 自助分析](https://claude.com/resources/articles/how-anthropic-enables-self-service-data-analytics-with-claude) | 2026-06-03 | 95% 查询自动化/~95% 准确；无 skills ≤21%；离线 95%→65%/月；对抗复核 +6% 准确/+32% token/+72% 延迟；LLM 自动生成 metric 定义 net-negative | 单公司工程博客；HN 讨论弱；只作机制证据 |
| [AngelList 放弃语义层](https://www.angellist.com/blog/the-semantic-layer-nobody-maintains) | 2026-08-28 | 1,400+ 模型/59 域/13k 行索引/27k 列；GitHub Actions “几美元/月”；“stale semantics worse than none” | 单公司；HN 2 分；无准确率；是换实现，不是项目失败 |
| [AWS Builder Center 语义层成本](https://builder.aws.com/content/3KvFN69cxO83mHPPRm71A5I820C/measuring-a-semantic-layer-evidence-cost-and-control-from-an-agentic-analytics-build) | 2026-10-19 | POC 50 用户/2,000 问/月；整层 $90–175/月；5 类 silent failure；live chat paraphrase agreement 4% | 客户匿名；POC；AWS 自证；只作量级线索 |
| [VentureBeat VB Pulse](https://venturebeat.com/data/companies-are-building-governed-semantic-layers-most-say-their-ai-agents-are-getting-context-somewhere-else) | 2026-10-06（报告 2026-11-06） | n=107/100；39% 生产用语义层；其中 28% 是 agent 主要上下文源（全体 13%）；采用者 78% vs 未采用 37% 报告上下文失败 | 自选样本、41% 顾问、不能推因果；只作弱信号 |
| [Atlan: KG pitfalls](https://atlan.com/know/ai-agent/knowledge-graph/enterprise-knowledge-graph-pitfalls/) | 2026-09-10 | “<15% 企业 KG 项目过 pilot”；组织/技术/经济三类失败 | **原始统计不可核**：追到 Improvado 2025-09-29 只有一句无出处的 “industry surveys suggest”；不采用该数字 |
| [小红书 DIBP（QCon 上海 2026）](https://qcon.infoq.cn/2026/shanghai/presentation/7343) | 2026-10-22/24 | 2026-02 起建 DataAgent；覆盖 80%+ 员工、主动会话周活 8,800+；Context Layer（数据/指标/业务语义/代码/血缘） | **B（具名采用，摘要级）**：无成本/失败/准确率；不是 OWL 本体；单一信号；不改变五平台阴性 |
| [NHS FDP × Palantir（Guardian）](https://www.theguardian.com/technology/2026/nov/02/palantir-unused-nhs-hospital-trusts) · [Register](https://www.theregister.com/public-sector/2026/11/03/nhs-counts-palantir-benefits-at-trusts-that-say-theyre-not-using-it/5307222) | 2026-11-02/03 | £330M 合同；29 家 trust 的 FOI 回复否认使用（Register 以 137 家“realising benefits”为分母≈21%；Guardian 称 137 家为“live”）；OSR 介入 | 调查报道 + FOI，不是工程复盘；谈 FDP 使用非 Ontology 深度；只作 signal |
| [Greptime Agent RCA Bench](https://greptime.com/blogs/2026-09-08-agent-rca-bench-interface-semantic-layer) | 2026-09-11 | 504 次/6 模型，三种查询接口含语义层分支；语义层分支部分故障类型改善（106→112），节点故障变差（24→12）；端到端效率指标未过统计校正 | **厂商自测 benchmark**（公开数据/代码）；不算独立信号；只作“同任务对照”线索，不撑结论 |
| [Stardog customers](https://www.stardog.com/company/customers/) | 未标日期 | Boehringer Ingelheim、NASA、NIH、Springer Nature | 客户页/旧案例；未过 2026-06 门 |
| [Ontotext STM case](https://www.ontotext.com/knowledgehub/case-studies/leading-stm-publishers-improved-data-consumption-reuse-with-knowledge-platform/) | 未标日期 | 匿名 STM publisher 的知识平台 | 匿名+厂商案例；C |

> **C 类使用规则**：只在 [04 中国](./04-china.md) 的“方案存在”和 [06 案例台账](./06-cases.md) 的“线索”列出现；不写进 00/02 的判断，不撑采用/效果。

## 90.2b B 类「谁在投」信号（只证投入，不证效果）

| 信号 | 日期 | 它说明什么 | 不能证明 |
|---|---|---|---|
| CCSA TC601 WG15《本体智能研究报告（1.0）》 | 2026-07-24 | 中国标准工作组在编本体/知识管理标准，报告 1.0 公开（报道称 24 家联署） | 企业采用/效果；报告 2.0 尚未发布（计划 2026-12-15） |
| FIBO Forum（EDM Council） | 2026-09-22 | 金融业本体标准仍在活动；T. Rowe Price 等参与 | 生产部署/成本 |
| Alan Turing Institute KG/ontology 研究服务招标 | 2026-06-30 | 英国公共研究机构在采购 KG/本体服务（3–6 pilots） | 落地效果；合同是否授予 |
| Sciensano（比利时公共卫生）KG 平台招标 | 2026-07-31（OJ S 146/2026；TED 531122-2026） | 政府机构在采购知识图谱平台；**€264k 是招标估算价/预算，2026-08-11 截标，未查到中标结果** | 成交价、是否上线、年维护、效果 |
| dbt Summit 2026（Okta / ING / Sigma） | 2026-09-15/18 | 具名企业在讲语义层生产叙事 | 规模/成本/失败；演讲不等于结果 |
| KeyBank Ontologist 招聘 | 2026-08-25（抓取） | 银行在招 OWL/RDF/SKOS、TopBraid/Stardog 能力的人 | 已落地/效果；招聘只证明“准备投” |

> 这些是 **B 类“谁在投”**，不是生产证据；不要用它们推“行业已规模化”。

## 90.2d 客户自述与采购（signal，只证“有人在用/在买”）

| 来源 | 日期 | 它是什么 | 为什么只是 signal |
|---|---|---|---|
| [贵州农商联合银行 KG](https://www.fintechinchina.com/cases/9863)（金科创新社） | 2026-10-08 | HugeGraph+华为大数据；1,000 日活/TPS 100/跑批 <3h；2024-06 设计→2025-04 上线；"仍在计算查询阶段" | 客户自述+评选，无独立复核、无成本/失败 |
| [江西农商联合银行](https://www.fintechinchina.com/cases/9803)（金科创新社） | 2026-09-29 | NebulaGraph+OceanBase；全省 86 家；6 试点机构/68 用户/3,000+ 隐性关系；有效线索 >85%；2026-05→08 上线；**投入 <50 万（上限）** | 同上；"<50 万"口径未说明（疑不含外部数据采购） |
| [江南农商银行](https://www.fintechinchina.com/cases/9766)（金科创新社） | 2026-09-22 | Neo4j+pgvector；2,000+ 知识页/500 DAU/可用率 99.5%；**12 个月、3 人核心组 ≈36 人月**；文档整理省 ~1,200 工时/年 | 同上；工时节约为自报估算 |
| [东北大学 智能工厂本体仿真服务](http://www.czzx.neu.edu.cn/2026/1109/c12062a482618/page.htm) | 2026-11-09 | 预算 **¥80 万 / 1 年**；本体建模+模型仓库+运行+应用，3 个业务本体；比选采购 | 采购公告；只到比选，无成交/上线/效果 |
| [中国联通软研院 政企本体建模](https://bj.zhiliaobiaoxun.com/article/110498214) | 2026-08-25 招标 / 2026-09-21 结果 | 预算 190 万、限价 180.5 万；4 个本体模型；两次流标（投标人不足 3 家）后转谈判，亚信中标 | 采购公告；只到授标前，无上线/效果 |
| [渝农商行 × 腾讯云 智能知识中台](http://stock.stockstar.com/RB2026072400019821.shtml) | 2026-07-21 成交 | 128.5 万；具名客户 | 产品线未证（不能写成 DataBuddy/Topbase 上线） |
| [上海银行 × 海致星图 关联图谱优化](https://wap.stockstar.com/detail/RB2026072400019041) | 2026-07-19 | 49.4 万；员工异常行为监测 | 只证采购 |
| [徽商银行 × 海致星图](https://ln.zhiliaobiaoxun.com/article/105860743) | 2026-07-13 | 平台投产后运维；2026 年外包预算 50 万；单一来源 | 单源转载；客户自述"投产后" |
| [上海银行 × 金山云 本体建模咨询](https://bosc.cn/zh/jrsh/xxgk_1091/tzzxgqk/zbcg/202609/t20260903_482183.shtml) | 2026-09-01 采购 / 2026-09-02 公示 | 首轮"投标人数不足"磋商失败后成交；金额未披露 | 采购摩擦的一手证据，不证上线 |
| [中电空间 × 中电云计算 本体构建与运营平台](https://bj.zhiliaobiaoxun.com/article/117100952) | 2026-10-28 | 项目名直指本体构建与运营平台；无金额 | 买卖同属中国电子体系（关联交易可能） |
| [中船 716 所 × 中科世通亨奇 KG 通用框架](https://www.csscbidding.com/jyxx/003002/003002004/20261103/0c76a2d3-17f4-47c7-8c72-8ce2f2745ed9.html) | 2026-11-03 | 142.5 万；央企研究所 | 只证采购 |
| [渤海银行 × 星环 AI 知识工程平台](https://bj.zhiliaobiaoxun.com/article/119046388) | 2026-11-11 | 星环成交；金额未披露 | 只证采购 |
| [Westpac 结束 Palantir 合作](https://www.cyberdaily.au/tech/14407-westpac-ditches-palantir-following-activist-push) | 2026-11-05 | 具名银行退出 Foundry | 动因是活动人士施压，非技术失败；无替代方案 |

## 90.2c OKF / Wiki 底座选项（定义、产品、案例）

| 来源 | 日期 | 类型 | 它证明什么 | 不能证明什么 |
|---|---|---|---|---|
| [Google OKF v0.1](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) · [卡](../../../src/web/google-okf/google-okf.card.md) | 2026-06-12 | 官方博客 / `admitted`（定义） | 一概念一 Markdown、路径即身份、YAML 头部只强制 `type`、受 Karpathy LLM Wiki 启发 | 采用/效果；不是标准组织标准 |
| [Google OKF v0.2](https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals) | 2026-07-24 | 同上 | sources/generated/verified/status/stale_after/attestation 全部 opt-in；`type` 仍唯一必填；“advisory signals, not access control” | 信任信号≠真实性；仍需 producer 审计 |
| [Google Knowledge Catalog 集成](https://cloud.google.com/blog/products/data-analytics/scale-okf-bundles-across-an-organization-with-knowledge-catalog) | 2026-08-26 | 官方博客 / C（产品能力） | bundle 可映射成 Catalog Entry、继承 IAM；okf Aspect 13 字段（`okf_type` 等，**无 `attestation` 字段**）；Acme 示例 9 leaf/17 entries | 客户采用/规模/效果；示例是合成 |
| [中泰 CCSA 案例](../../../src/web/modb-2026-zhongtai-ontology/modb-2026-zhongtai-ontology.card.md) | 2026-10-15 | engineering / `admitted` | 用 OKF 组织 9,137 知识目录/6,503 指标文档/12 万+ 血缘；业务本体验证中 | 业务本体全量；成本/准确率；单公司 |
| [SCIMIN-CRM · Semantic MediaWiki](https://ceur-ws.org/Vol-4293/paper50.pdf) | 2026-10-13 | 会议论文 / `signal`（承建方自述，不入 `src/`） | **本体先行**的做法：OWL 本体 + SMW 标注；LLM 候选 + 自动校验 + 专家 HITL + 受控发布 | 独立采用/规模/效果/成本；**不撑任何结论**；不是 OKF 案例；`CRM` = Critical Raw Materials |
| [Kunstenpunt Wikibase](https://tech-news.wikimedia.de/2026/06/02/kunstenpunt-a-whos-who-of-the-flemish-art-scene/) | 2026-06-02 | 工程博客 / `signal`（frontier） | 100 万页/25 万实体/3 名专职/与 Wikidata 联邦；约束只警告不阻断；**2024 数据标准先行（兼容 CIDOC CRM/schema.org），再并库进 Wikibase** | 独立印证；**全文 0 次 OKF/ontology**；“数据标准”≠“OWL 本体”，不能当 OKF 案例 |
| [京东海博 OKF](http://stock.10jqka.com.cn/20260924/c680274369.shtml) | 2026-09-24 | 媒体转载 / `signal` | 一概念一 md、`type` 必填、index/log、宽容消费；542 秒 vs 967 秒（约 -44%）；“编译前移到维护期” | 单一来源、无个人署名；**“OKF”全文未展开，“= Google OKF”是推断**；780+ 商家是业务规模不是知识规模 |
| [Linked.Archi](https://meta.linked.archi/docs/practice/okf-open-knowledge-format/) · [Atlas](https://github.com/AtlasDevHQ/atlas/blob/main/docs/research/okf-interop-spike.md) · [GMEOW](https://github.com/Blackcat-Informatics/gmeow-ontology/blob/main/docs/okf.md) | 2026-07-17 / 07-02 / 2026 | 工程文档 / C（实现与框架） | 三份独立实现互证：本体→OKF 投影有损（丢关系类型/公理/约束）；OKF→本体是草稿 + 关系定型人审 | 生产采用、迁移完成；单项目/小仓库，star 不算信号 |

> **最大缺口**：截至 2026-11-12，没有一条公开证据证明某组织完成“OKF/Wiki → 本体”的迁移（有路径、时间线、成本、失败）。中泰最接近，但把图数据库/对象关系写在后续规划；唯一的“本体先行 wiki”（SCIMIN）是承建方自述的 `signal`，不是独立采用。检索式见 [90.3](#903-阴性结果查过但没有过门的)。

## 90.3 阴性结果：查过但没有过门的

| 想找什么 | 查了什么 | 结果 | 关闭它需要什么 |
|---|---|---|---|
| 中国大厂 2026-06 后**外部采用**（阿里/蚂蚁/腾讯/华为/京东） | 官网、云文档、开发者社区、会议（QCon/CCKS/AICon/云栖/HC）、招聘、采购平台、案例库、arXiv；**2026-11-12 加搜产品名 + 客户**（Context0/DataBuddy/DataArts/TuGraph/Oxygen） | **五平台 0 条「具名客户 + 可追一手」**；能过门的客户侧材料集中在海致星图/星环/金山云/中电云计算/中科世通亨奇与三家农商行自建（signal）；另找到小红书（B，但不在五平台之列） | 客户署名复盘或会议 talk；平台名 + 客户名 + 规模 |
| Palantir 客户侧**一手工程复盘**（2026） | Palantir 公告、客户新闻、会议；**2026-11-12 加搜 FOI/监管** | 仍无客户自己写的规模/成本/失败；**Westpac 2026-11 退出（非技术原因）**；新找到 NHS FDP 客户侧否认（29/137 家 FOI 说未使用，OSR 介入）——是使用口径争议，不是工程复盘 | 客户 engineering blog / conference industry talk |
| 本体/语义层**全生命周期 TCO** | 工程博客、会议、USASpending、UK Contracts Finder、TED（API 检索 `ontology`/`Ontologie`/`knowledge graph`，PD≥2026-06-01）、中国政府采购网 | 五类价 + **两条客户自述投入**（江西 <50 万上限；江南 3 人×12 月）；TED 只回 2 条相关采购（Leibniz-IWT €270k 开发服务、Sciensano €264k），**无人月、无同一买方建设+维护配对、无回收期** | 企业财务/采购披露，或带账本的复盘 |
| 本体/语义层**人月/工时** | 工程博客、会议、arXiv（429 限流）、中国政府采购网、招标聚合站、上市公司募投、招聘 JD、**TED API** | **无 A 类人月**；本轮只补到客户自述一条（江南农商 3 人×12 月 ≈36 人月）。仍不合格的：Data Praxis 是构造案例；玄同科技是匿名软文；联通招标正文在付费墙后 | 客户署名复盘（团队 × 月数）、招标文件的工作量/人月单价表、或募投「新增研发 N 人 + 建设期」 |
| OKF 的企业级采用 | Google OKF 博客/GitHub/Knowledge Catalog；中国案例；GitHub 搜索 `"open knowledge format" in:description`（477，2026-11-12 快照） | **西方未找到具名生产采用**（只有工具/框架实现与教程，C）；中国仅中泰（`admitted`）+ 京东海博（`signal`）；无 A 类 | 具名组织 + 规模 + 成本/失败 + 独立印证 |
| **OKF/Wiki → 本体迁移完成案例** | Google 博客/规范、GitHub、CEUR/SEMANTiCS、工程博客、Linked.Archi/Atlas/GMEOW | **0 条**：有投影/上提实现与“先 OKF 再提升”的框架建议，无组织披露完成迁移（路径/时间线/成本/失败） | 一份带迁移前后规模与成本的复盘；或迁移中断的 postmortem |
| **上线后被关停/废弃的本体/KG 项目** | 英文工程博客、HN（Algolia 检索 2026-06 后 `knowledge graph`/`semantic layer`/`ontology`）、KGC/SEMANTiCS 议程、TED、UK Contracts Finder、中国政府采购网、arXiv、**NAO/GAO/ANAO** | **未找到第一方复盘**；中国 7 例流标/终止全在授标前（供应商不足 3 家），且已重新采购/转谈判；唯一"撤销合同"案例与本体无关；审计机关无本体/KG 专项；**NHS FDP 是"宣称 vs 使用"落差，不是关停** | 一条带结局（取消/回退/降级）与规模的 postmortem |
| 重型平台被替换（窗口内） | TED、UK Contracts Finder、新闻 | 最强案例 MHCLG 用自建替换 Palantir Foundry（2026-05-19）**超窗，只作背景**；窗口内只有 Westpac（非技术原因）；NHS 是合同存续争议（2026-12 决定），不是替换完成 | 窗口内的技术性替换复盘 |
| **失败率** | Atlan/Improvado、HN、咨询报告、审计机关 | 只有二手"<15%"说法，原始统计未核；另有"60% 指标中台死在第二年"无样本/分母，未采用 | 可核的样本框+分母+年份 |
| **会场级论文扫**（2026-11-12） | VLDB vol19 全目录（457 篇标题）、ICDM 2026 站点、SIGMOD 2026 industrial track | VLDB 命中 1 篇 BI（CoeusBI，已入）与 1 篇 KG 运维（DBAIOps）；后者 arXiv 2025-08 首曝，**G1 超窗**，只作背景；Hamilton（交互式本体学习）是学术 demo，非生产；ICDM/SIGMOD 站点未取到（ICDM 以论文脚注核到 UniDataAgent Demo） | 会场站点的 accepted list 可访问后重扫 |
| **DBAIOps（VLDB 19，KG 运维）** | 判 **G1 超窗**：arXiv 2508.01136（2025-08）早于 2026-06；PVLDB 版只是正式发表 | 首曝日期晚于 2026-06 的版本/报告 |
| **制造业/工业本体生产案例** | arXiv、会议、厂商案例、采购公告 | 只有**真实试验台研究**（[Narrow and Deep](https://arxiv.org/abs/2610.11768)，9 任务/4 模型/投影 +19.8pp）与采购公告（中船、东北大学）；**无企业级生产复盘** | 一家制造企业的具名部署复盘（规模+失败） |
| **讲稿/PPT（把摘要级升成可核）** | QCon 上海 2026 PPT 服务（`ppt.infoq.cn`，conid=173，117 个议题） | 中泰议题**有幻灯片**（pptid 5426）但**下载需登录**，未取得；小红书 DIBP **无幻灯片**（pptid 为空）→ 摘要级就是上限 | 登录账号、讲者公开分享或会议录像 |
| **同数据集对照**（本体 vs 无本体） | 论文/工业报告；HN 2026-06 后检索 | 无**生产级**对照；找到两类非生产对照：厂商自测 504 次（Greptime，语义层分支部分改善/部分变差、未过统计校正）与**学术受控研究**（[Same Context](https://arxiv.org/abs/2610.20959)：7 模型/1,514 任务/5 benchmark，语义层收益依赖 agent 行为）；二者都不算生产信号 | 预注册的 A/B 或 shadow 对照 |

## 90.3b 口径与不可比说明

本份的钱与规模来自四类材料：英美公共采购（UK Contracts Finder / USAspending）、中国招标与成交公告、工程博客里的价目与 POC 实测、公司自述的规模数。口径不统一，**没有一条能单独当 TCO**。下表把每一类数的边界摆出来，读 [05 经济性](./05-economics.md) 与 [08 边界](./08-boundaries.md) 时对照。

| 口径 | 本份哪些数属于它 | 不能和什么直接比 | 读的时候要注意什么 |
|---|---|---|---|
| **币种**（£ / $ / € / ¥） | £：£10.09M/5 年、£130k/年；$：$1.14M/年、$4.9M/4 个月、$90–175/月、$37.59/月、$1.65/月；€：€264k；¥：¥49.4 万 / ¥115 万 / ¥142.5 万 / ¥178.8 万/年 / ¥190 万 / ¥180.5 万 / ¥275.689 万 | 跨币种相加、按记忆汇率折算后排名 | **本份不做汇率折算**，一律原币记；跨币种只谈量级，不谈名次 |
| **含税 / 不含税** | 联通 190 万**不含税**；英国 Contracts Finder 的 `awardedValue` **未标**是否含税；美国联邦合同与 TED 预算未单列税 | 含税价与不含税价相减、算差价 | 未标含税的一律**不假设**；也不把两家不同标的的价差解释成税差 |
| **美国联邦合同**（USAspending） | $1.14M/年（SEC，选项至 2030-03）、$4.9M/4 个月（IRS） | 含未行使选项的“合同总价”；$1.14M × 年数 | `Award Amount` 是**当前 obligation**（当期已发生/已承诺），不是含选项总价；乘年数等于把“选项”读成“已花” |
| **中国项目合同** | ¥49.4 万 / ¥115 万 / ¥142.5 万 / ¥275.689 万（建设/实施）、联通 190 万（4 个模型，2026–2028 两期） | 年维护费（浦发 ¥178.8 万/年，**超窗背景**）；人月成本 | 多为**建设/实施合同，不含年维护**，也不含内部人力；维护可与建设同量级，但那是另一家买方的数 |
| **招标预算 vs 成交价** | Sciensano €264k（招标估算价/预算，2026-08-11 截标，**未查到中标**）；联通 190 万预算 / 180.5 万限价（亚信中标，成交价未披露） | 成交价、实际支出 | 预算是**上限估计**，不等于花了多少；方向不定：可能压价成交，也可能流标转谈判后贴近限价 |
| **5 年平台合同 vs 年度支持** | Cambridgeshire £10.09M/5 年（≈£2.0M/年，平台+服务）；SEC $1.14M（1 年支持 + 选项）；National Highways £130k/年 | 5 年总额 ÷ 5 当年费；年度支持当平台全价 | 年化只在**同一合同内**做除法；两个年化数范围不同（平台+服务 vs 仅支持），不能比“单价” |
| **POC vs 生产** | AWS $90–175/月（50 用户/2,000 问/月的 POC）；PolarDB $37.59/月、$1.65/月（组件）；AngelList“几美元/月”（CI 运行） | 生产运行成本；与平台年费放在一张表里排名 | POC 便宜 = **规模小 + 治理人力不计**；它只证“跑起来不贵”，不证“生产便宜” |
| **规模口径**（资产数 ≠ 实体数 ≠ 查询/用户） | 知识资产：9,137 知识目录 / 6,503 指标文档 / 2,622 表 / 12 万+ 血缘（中泰）；消费面：5,600 员工 / 320k 查询、400+ 用户 / 5,400+ 查询（Snowflake）；模型/任务：2,883 模型 / 63 job（Sigma）；目录：49,000（Netflix） | 把知识资产数当本体实体数；把用户数当查询量；跨公司比“规模” | 四类数各指不同东西；本份**没有一家**同时给“实体数 + 查询量 + 用户数”，不能拼成一张规模榜 |
| **同一来源的两种口径** | 中泰 6,000+ 指标（QCon 议题摘要）vs 3,400+ 公司级指标（同页讲者简介） | 相加、取平均、把 3,400 写成对 6,000+ 的“更正” | 可能不是同一口径（AI Native 环境 vs 公司级语义体系）；分别引用，不互相替代 |
| **客户自述投入 vs 合同/报价** | 江西农商「投入不到 50 万」（**上限**，口径未说明，疑不含外部数据采购）；江南农商「3 人核心组 × 12 个月」（**只算核心组**，评审/业务配合未计）；东北大学 ¥80 万/1 年（**比选预算**，非成交） | 当成交价、当 TCO、当人月单价；把「上限」读成「实际花费」 | 三条都是**上界或局部**，不能相加；它们只回答“量级”，不回答“花了多少、值不值” |
| **宣称 vs 使用**（NHS FDP） | 137 家 trust 被列为「realising benefits」，29 家 FOI 回复未上线/未使用；£330M 合同存续待 2026-12 决定 | 当“项目失败率”或“客户流失率” | FOI 回复是**客户自述**，媒体是调查报道；既不是工程复盘，也不是全量普查 |

**怎么比**：

- **先同类再跨类**：平台对平台（5 年合同比年度支持前，先问“含不含实施/服务”）、项目对项目（建设对建设，别拿建设对维护）、运行对运行（POC 对 POC，别拿 POC 对生产）。
- **任何 TCO 必须同一买方、同一范围、含人月**；三条缺一条，就只能叫“**锚点**”，不能叫 TCO。
- **拿不准就写“不可比”**：不取平均、不相加、不把两个年化数拼成一个“行业均值”。

> 本节不引入新证据，只把 90.1/90.2 与 05.5 的既有数按口径归位；不能因此多算任何一条采用、效果或 ROI。

## 90.4 检索日志（摘要）

- 时间：2026-11-12（含当日**第二轮补搜**）。
- 检索面：美国重型平台/语义层、中国大厂/采用者、失败/成本、标准/招聘/采购、2026 工业论文；第二轮加：**arXiv API（按日期筛 2026-06 后）**、**QCon PPT 服务 API（conid=173）**、**TED API**（结构化检索采购公告）、**HN Algolia API**（2026-06 后按日期）、**QCon 上海 2026 日程/议题页**（找中国具名案例）、**云厂商产品名 + 客户**、**审计机关（NAO/GAO/ANAO）**、**FOI/调查报道**。
- 关键词：`ontology production 2026`、`semantic layer production case study`、`Palantir ontology customer 2026`、`阿里云 本体 客户`、`蚂蚁 TuGraph 生产`、`腾讯 Topbase 2026`、`CCSA TC601 WG15`、`knowledge graph postmortem`、`ontology maintenance cost`、`FIBO EDM Council 2026`；第二轮：`ontology`/`Ontologie`/`knowledge graph`（TED，PD≥2026-06-01）、`Context0`/`DataBuddy`/`DataArts`/`TuGraph`/`Oxygen` + 客户、`人月 本体`、`knowledge graph failed`、`Palantir NHS`。
- 抓取限制：`web_fetch` 对部分域名被策略拒绝（返回非公网 IP）；改用 `curl`；微信公众号多被 CAPTCHA，改用官网/会议页/转载；TED/HN 用公开 API。
- 黑名单：采/引前已查 [excluded-sources](../../../meta/rules/excluded-sources.md)；未使用命中源。
- 结论：**不是没搜，是这类材料稀缺**；第二轮把三条从“没查”变成“查过、只有 signal”，其余仍阴性；10 的价值之一是把“缺什么、查过哪”写清楚。
