---
status: draft
source_type: blog
reading: 精读
provenance: 原文正文
updated: 2026-11-12
admission: admitted
gate: standard-in-force
gate_checked: 2026-11-12
impact_evidence: "I2: v0.2 博客记外部贡献者提交扩展提案与样例；I3: 中泰证券在生产中用 OKF 作知识载体（admitted 卡）；I5: Apache-2.0 规范 + samples/tests + reference agent 公开"
liveness: "v0.2 2026-07-24；Knowledge Catalog 集成 2026-08-26；规范仓 main 最新 commit 2026-08-21；PR #63（2026-11-06，未合并）称迁往新组织"
provenance_type: company
source: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
author: Sam McVeety（Tech Lead, Data Analytics）；Amir Hormati（Tech Lead, BigQuery）；Firat Elbey（Knowledge Catalog 篇）
published: 2026-06-12（v0.1）；2026-07-24（v0.2）；2026-08-26（Knowledge Catalog）
updates: ["2026-11-12 补 gate 字段：按 CHARTER §4.4.1 在役例外记录（现行版本 + 2026-06 后维护 + ≥2 活跃实现），并声明证据天花板只到“定义”，不撑采用/效果/迁移"]
---

# Google Open Knowledge Format（OKF v0.2）

> 本卡覆盖一组同源材料：v0.1 发布博客（2026-06-12）、v0.2 博客（2026-07-24）、Knowledge Catalog 集成博客（2026-08-26）、规范正文 `SPEC.md`（v0.2，2026-11-12 抓取）。日期以 JSON-LD `datePublished` 为准；三篇博客的署名行比它晚一天，是本地时区渲染，不是另一个版本。
> **它是什么**：一个把「一份 Markdown = 一个 concept」组织成 bundle 的**开放规范**；不是 W3C/ISO 标准，不是本体语言，也不是执行引擎。

## 它主张什么

1. **一个 concept 一个文件，路径就是身份**：bundle 是一个目录的 Markdown；YAML frontmatter 只强制 `type`，其余字段由生产者定；链接用普通 Markdown，链接图就是知识图；`index.md`（渐进披露）与 `log.md`（变更历史）可选。
2. **v0.2 加的是「判断信号」，不是「规则」**：`sources` / `generated` / `verified` / `status` / `stale_after` / `attestation` 全部 opt-in；`type` 仍是唯一必填；不采纳任何新字段的 bundle 与 v0.1 一样合规。信任分级原文写明是 **advisory signals, not access control**；规范只记录计算与校验方式，**从不执行**。
3. **它刻意不碰语义执行**：Non-goals 明确包括「定义固定的概念类型分类法」「规定存储/服务/查询基础设施」「替代领域 schema（Avro/Protobuf/OpenAPI）」。规范要求消费者**不得**因缺可选字段、未知 type、未知键、坏链、缺 `index.md` 而拒绝 bundle。

## 场景与 scope

- **作者场景**：Google Cloud Data Cloud 团队，面向「多个生产者写的 wiki 要被多个 agent 消费」的互操作问题；示例用 BigQuery 数据集（`acme_retail` 是**虚构**美国零售商）。
- **Knowledge Catalog 集成**（2026-08-26）：把 bundle 的每个 concept 映射成 Catalog Entry，继承 EntryGroup 的 IAM；`okf` Aspect 13 个字段（`okf_type, generated, sources, verified, status, stale_after, usage_window, runtime, parameters, computation, executor, attester, extra`）——**没有名为 `attestation` 的字段**，也没有 `type`（叫 `okf_type`）。示例 9 个 leaf concept / 17 个 Entry（auto 多 1 个，共 18 行）。
- **规模与边界**：格式侧没有采用规模可披露；产品侧只有「能力」，示例是合成的。**不要把 Knowledge Catalog 的 IAM 继承读成 OKF 自带权限**——权限来自 Catalog，不来自格式。

## 证据强度

- **一手还是转述**：一手。规范正文（`SPEC.md` v0.2，5,164 words）与三篇官方博客全文均逐字读过。
- **有数据吗**：有可核的**文本事实**（字段、必填项、Non-goals、词频），没有采用/效果数据。
- **数据规模与场景**：规范层；唯一生产采用证据来自**中泰证券**（admitted 卡，OKF 作权威源/交换格式，版本未披露）。
- **准入走的是哪条例外（2026-11-12 补）**：**§4.4.1 在役标准例外**——① 现行版本 v0.2（SPEC.md 明确 `Version 0.2`，无 v0.3）；② 2026-06 后仍有维护活动（v0.2 2026-07-24、Knowledge Catalog 集成 2026-08-26、规范仓 main 2026-08-21 的 commit、51 个 open issue）；③ **≥2 个活跃独立实现**（Atlas 的 `okf import/export`、GMEOW 的 `gmeow okf` / `transpile`、Linked.Archi 的读写投影，均 2026-07 后）。**限定**：Google 是公司不是标准组织（SDO），所以这里只借 §4.4.1 的**实质条件**（现行 + 维护 + 多实现）判格式的“在役”，不等于承认它是行业标准；卡片用 `gate: standard-in-force` 记录这一判定，`standing` 仍按资料性处理。**证据天花板：只到“格式/字段/边界是什么”，不撑采用、效果、迁移。**
- **可复现吗**：词频可复算——对 `SPEC.md` 做 whole-word 统计：`ontology`/`RDF`/`OWL`/`SHACL`/`SPARQL`/`knowledge graph` 各 **0** 次；`semantic layer`（空格）**0** 次，`Semantic-layer`（连字符）**1** 次，在 §12.3「Considered and deferred」把 Looker/dbt 模板列为未来工作。**「0 次」不能写成包含 semantic layer 的整句。**

## 与已有判断的关系

| 结论编号 | 关系 | 说明 |
|---|---|---|
| E-32 | 支持 | 提供「OKF 是什么/不是什么」的定义与边界；采用面由中泰卡支撑，不由本卡单独支撑 |
| E-28 | 支持（弱） | OKF 作为「底座选项」之一；本身不证明生产规模 |

> **G4 判定（写在明处）**：这是 Google 发布的开放规范 + 公开仓库，不是产品页或营销文，故按「组织/社区产出的技术规范」过门；但它仍是公司出版物，所以本卡**只用于格式定义类事实，不用于采用/效果类结论**。采用类结论另由 [中泰 CCSA 卡](../modb-2026-zhongtai-ontology/modb-2026-zhongtai-ontology.card.md)（`admitted`）支撑。

## 待核项

- [ ] 中泰用的是 OKF 哪个版本、是否用了 v0.2 的信任字段——原报道未写。
- [ ] `open-knowledge-format/open-knowledge-format`（官方 PR #63 指定的新家）截至 2026-11-12 仍是 404；org 存在但 `public_repos: 0`。**不能写「v0.3 已发布」**。
- [ ] 规范仓 main 只有 6 个 commit、1 位作者、无 tag/release；`pushed_at` 2026-11-06 来自未合并的 `deprecate-repo` 分支，不是 main 的更新。
- [ ] OKF 的 license 只写在仓库 `LICENSE.md`（Apache-2.0）；三篇博客正文没有 license 句。

## 喂到哪个主题

- `topics/06-measure/feasibility/mechanism.md` §OKF / Wiki 底座选项
- `deliverables/05-production-landscape/02-sections/04b-okf-wiki.md`

## 原文摘录

完整逐字摘录见 [google-okf.md](./google-okf.md)。最短的三句：

> "OKF requires exactly one thing of every concept: a type field. … The spec defines the interoperability surface, not the content model."

> "It adds vocabulary, not rules: type is still the only always-required field, every new field is opt-in…"

> "Tiers are advisory signals, not access control."
