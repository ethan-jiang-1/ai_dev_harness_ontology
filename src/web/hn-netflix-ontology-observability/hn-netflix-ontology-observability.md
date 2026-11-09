---
updated: 2026-11-09
source: Hacker News item 50153431
url: https://news.ycombinator.com/item?id=50153431
article_url: https://netflixtechblog.com/ontology-driven-observability-building-an-end-to-end-knowledge-graph-at-netflix-scale-421392cf5adf
title: "Ontology-Driven Observability: Building an End-to-End Knowledge Graph at Netflix"
published: 2026-10-19
points: 131
comments: 32
retrieved: 2026-11-09
note: >
  Top-level comments 摘录（每条截断）；全文在 HN URL。Netflix 原文返回 403（Cloudflare），
  本仓库未存档原文；下面的观点只代表 thread，不代表 Netflix 正文。
---

# HN 讨论：Ontology-Driven Observability at Netflix

> 来源：Hacker News，2026-10-19，131 points / 32 comments。
> 原文：Netflix Tech Blog（本次抓取 403，未读正文）；本文件只记录 thread 的 top-level comments。

## Thread 元数据

- 标题：Ontology-Driven Observability: Building an End-to-End Knowledge Graph at Netflix
- 链接：https://netflixtechblog.com/ontology-driven-observability-building-an-end-to-end-knowledge-graph-at-netflix-scale-421392cf5adf
- HN：https://news.ycombinator.com/item?id=50153431
- 分数/评论：131 / 32

## Top-level comments（摘录）

- **antonvs**：`This agreement has a name: an ontology. Ontology is a formal specification of types, the properties they carry, and the relationships they may have. Its unit is the triple...` 接着纠正：OWL/RDF 只是 ontology 的一种用法，ontology 在更广语境里是“存在及其关系”的哲学分支；不要把 RDF 定义当成全部。
- **j45**：想收集更多 ontology 的学习资源与个人实践。
- **nico**：`Is this like XML and UML all over again?`（怀疑是又一次 schema 潮流）。
- **dominotw**：批评 Netflix 技术栈过度工程；引另一条 HN 讨论“A Staff Engineer's Guide to Inventing Work”。
- **1970-01-01**：`Without actual examples of it working to reduce latency, this is purely academic and not engineering. What happened to the 1.5s problem in the introduction?`（要 latency/效果证据）。
- **threecheese**：担心让机器决定 ontology，会“回归均值”、丢失表达力；人类能读 schema/structure/shape 的 nuance，机器只触发其中一种。
- **smartmic**：企业里 ontology/KG 实验了约 15 年，`it never took off`；关系库仍主导，投入数百万美元，成功故事少见。
- **nout**：集中 identity 仍关键（merge/split/identity shift + 每个 triple 可回源），但**不必把 ontology 强推到所有系统**；给 AI 工具调用/技能 + memory，可能更有效。
- **smithclay**：Netflix 文末的终局是把 observability ontology 接到业务/数据团队的系统，回答“这次变更赚/亏了多少钱”；但这是“in theory”。
- **llmslave**：`Are knowledge graphs still relevant? Agents can grep and fetch on a unix operating system with higher accuracy`（agent 直接 grep/fetch 是否够）。

> 以上为 thread 观点摘录，不是 Netflix 原文；原文未读。
