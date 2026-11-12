# Ontology-Driven Observability: Building an End-to-End Knowledge Graph at Netflix Scale

- 来源：Netflix Technology Blog
- URL：https://netflixtechblog.com/ontology-driven-observability-building-an-end-to-end-knowledge-graph-at-netflix-scale-421392cf5adf
- 作者：Prasanna Vijayanathan, Renzo Sanchez-Silva
- 发布：2026-10-16
- 存档说明：本文件为原文的**摘录**，非全文；引用以原文为准。

## 摘录

When Jake Paul and Mike Tyson stepped into the ring in November 2024, we delivered the fight to roughly 65 million concurrent streams. On an ordinary day our infrastructure takes in more than 2 billion requests and handles upwards of 38 million real-time logging events every second.

The difficulty is that they do not agree on what they are talking about. A thing that is an application in one system is a service in a second and a cluster in a third, with names differing by a suffix, a casing convention, or a rename only a couple of people remember.

We built it on the W3C stack for this: RDF for the data model, OWL for the ontology, SHACL for validation, and SPARQL for querying. These standards are well specified and widely implemented, which keeps the model portable across graph stores.

The data from the ontology itself, is stored as a knowledge graph, persisted to QuipuDB, our homegrown RDF graph database, a distributed quad store based on redb, a Rust-based embedded key value db.

Our ontology is organized into twelve namespaces, each owning one operational domain.

We refused a generic Service type. “Service” means four different things across our tooling, so applications resolve to exactly one type, ops:Application, and every one of them is validated against our software catalog of roughly 49,000 entries before the entity is created. Unvalidated strings like usernames, team names, dependency names scraped from network topology, never become applications. We also cap dependency edges in both directions, because one popular service can carry thousands of reverse dependencies and would otherwise dominate the graph.

The enrichment pipeline runs sequentially — load the graph, add triples, and save. This sequencing removes an entire category of race conditions at a cost in wall-clock time we are happy to pay.

We are early enough that the ranked hypotheses are sometimes wrong, which is why each one carries the evidence that produced it. But when the engineer now starts the investigation, they are already holding the picture that used to take half an afternoon to assemble.

## 相关讨论

- HN 50153431（2026-10-19）：131 分 / 32 评论；已有仓库卡 [hn-netflix-ontology-observability](../hn-netflix-ontology-observability/hn-netflix-ontology-observability.card.md)。
- 讨论中从业者反证：“15 年、花了数百万美元、从没起飞”（匿名观感，不能当统计）；也有反方向：本地 KG 把读侧 token 从总支出 30% 降到 2%、单次图遍历 ~25ms（匿名，未核）。
