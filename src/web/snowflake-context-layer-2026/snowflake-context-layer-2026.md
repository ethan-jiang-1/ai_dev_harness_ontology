# Building an Internal Context Layer for AI Agents at Snowflake

- 来源：Snowflake 官方博客
- URL：https://www.snowflake.com/en/blog/snowflake-internal-context-layer-for-ai-agents/
- 作者：Aniruth Narayanan（Snowflake Product Manager）
- 发布：2026-08-17
- 存档说明：本文件为原文的**摘录**，非全文；引用以原文为准。

## 摘录

Modern enterprises collect and manage millions of data sources and signals across their business. At Snowflake, we use Snowflake internally to monitor our business systems and product telemetry at scale — across every query, warehouse and click. But without a shared understanding, petabytes of raw data become a source of conflicting answers, not a foundation for action.

Take a seemingly simple question such as “What is an active customer?” That question could yield different answers across different tables and varying metric definitions…

Every interface needs consistent meaning, or context, for its data, which can be achieved by using a semantic layer. A semantic view is a top-level object that sits between the downstream consumers and raw data tables, translating governed business language into physical database schemas.

With a semantic-oriented data architecture, returns compound quickly across the stack:
- Increased accuracy: Provide precise business context to models. In AtScale’s benchmark testing, adding semantic context increased text-to-SQL accuracy from 20% to more than 90% across 40 business questions on TPC-DS.
- One source of truth: Replace isolated, tool-specific semantics with a single semantic layer.
- Free governance: Leverage Snowflake’s access controls on semantic views and metric objects natively.
- True self-service: Support ad hoc, natural-language questions for any user on their own.

In July 2025 alone, more than 400 distinct internal users ran over 5,400 queries through the product data science agent and the semantic layer. And in the same time frame, more than 5,600 internal employees across all Snowflake teams and agents ran over 320,000 queries using the broad semantic layer in sales, HR, support and other areas.

The semantic layer needs to be treated with the same rigor as production software. With Snowflake’s native dbt integration, we’re able to fully version control, peer review and apply continuous integration and continuous delivery (CI/CD) to our metrics.

Early on, we tried pointing a semantic view at multiple raw, billion-count event tables. Every time a user asked a question, the view crawled and joined these tables, resulting in massive latency.

Initially, we built and maintained our own preaggregated slices with Dynamic Tables. Each dashboard had the rollup and grain that it needed. However, as we expanded our semantic coverage to support new questions and domains, we had to manually add new pipelines and tables and maintain a rapidly growing estate.

With semantic view materializations, we’re able to model semantic views directly on high-grain source tables and declare which dimension and metric combinations need to be fast. Snowflake intelligently maintains those slices for us in the background, helping reduce response times.
