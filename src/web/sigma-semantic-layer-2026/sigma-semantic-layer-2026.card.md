---
status: draft
source_type: engineering
reading: 已消化
provenance: 原文正文
updated: 2026-11-12
admission: admitted (probation)
gate_checked: 2026-11-12
liveness: 2026-10-27 dbt Labs 博客在线
impact_evidence: "I2: Sigma + dbt Labs 两个独立机构；I3: Sigma 生产 2,883 个 dbt 模型 / 6 个 region；I4: dbt Summit 2026 议题"
provenance_type: company
source: https://www.getdbt.com/blog/sigma-dbt-dagster-semantic-layer
author: Daniel Poppy（dbt Labs），报道 Matt Senick（Sigma Computing）
published: 2026-10-27
updates: []
---

# Sigma：2,883 个 semantic model 跑在 dbt + Dagster 上

> dbt Labs 报道 Sigma 的 lead data platform engineer 在 dbt Summit 2026 的 session。Sigma 既卖语义层，也自己用；本文是“供应商自己跑自己的产品”的工程证据。

## 它主张什么

1. **规模**：Sigma 的 dbt 项目有 **2,883 个 dbt 模型、63 个 Dagster job、6 个数据 region**；semantic objects 用 SQL/Jinja 版本化，映射到仓库表，列级控制暴露给业务用户。
2. **做法**：语义层按业务职能拆分（销售/市场/客户成功/产品等）；用 dbt 包编译成 Sigma data model、Snowflake semantic view、Cortex agent；Dagster 下载 dbt manifest、state-aware build、回写 Sigma API、再上传 manifest。
3. **AI 用途**：把 PII 限制、SQL 格式规则、同义词、verified queries 写进 model-level instructions，让每个 AI surface 拿到同一套定义；目标是从“text-to-SQL 猜”变成“调用一个已定义指标函数”。
4. **边界**：文章没有成本、失败率、查询量；Sigma 是语义层厂商，不能把“自己用自己的产品”当成客户效果证据。

## 场景与 scope

- Sigma Computing 内部数据平台；6 个 region、2,883 个模型；不是客户案例，也不是本体推理系统。
- 语义层是“指标/维度/同义词/verified query”层，不是 OWL/RDF；它证明的是**轻语义层可以在生产规模上版本化运行**。
- dbt Labs 是独立机构（报道方/工具方），但它与 Sigma 有生态关系，不是独立采用者。

## 证据强度

- 一手/转述：dbt Labs 编辑的工程报道，引用 Sigma 工程师的 session；一手成分高，但不是 Sigma 官方审计。
- 有数据吗：有模型数/job 数/region 数；无成本、无准确率、无失败率。
- 可复现吗：部分可（dbt + Dagster + Sigma 的 pipeline 结构可对照）；效果不可复现。
- 证据等级：作为“Sigma 报告了 X”是 `已核`；作为“语义层普遍有效”是 `推测`。
- 准入：`admitted (probation)`；G3 有 I2/I3/I4，但缺成本/失败，2027-05-11 前补第二信号或降级。

## 与已有判断的关系

| 结论编号 | 关系 | 说明 |
|---|---|---|
| E-28（平台承载） | 支持 | 语义层长在 dbt/Dagster/仓库底座上，不是从零建本体 |
| E-29（失败模式） | 旁证 | 需要版本化、PII/格式 guardrail、列级暴露控制；否则 AI surface 会各自为政 |
| E-30（成本拐点） | 旁证 | 2,883 模型的持续 build/deploy 说明维护是长期工程；无金额 |

## 待核项

- [ ] Sigma 的查询量/用户数/准确率/返工率。
- [ ] 2,883 个模型里有多少是 semantic model、多少是普通 transform。
- [ ] 成本：Dagster 运行成本、dbt/Sigma 许可、维护人力。

## 喂到哪个主题

- `topics/06-measure/feasibility/mechanism.md` §生产落地图景
- `deliverables/05-production-landscape/02-sections/03-us.md`
- `deliverables/05-production-landscape/02-sections/05-economics.md`

## 原文摘录

> “Dagster orchestrates the whole thing: 63 jobs continuously build and deploy across 2,883 dbt models and 6 data regions, downloading the dbt manifest from S3, running a state-aware dbt build, syncing the resulting Sigma data models back through Sigma’s API, and re-uploading the manifest for the next run.”

> “Senick framed the semantic layer's job in the age of LLMs around three things: giving AI applications guardrails, like PII restrictions and SQL formatting rules, baked directly into model-level instructions; giving every AI surface in the company the same definitions for a given metric so they never disagree with each other; and giving agents enough model context, synonyms, and verified queries to move past generic text-to-SQL guessing.”
