# How Sigma runs a 2,883-model semantic layer on dbt and Dagster

- 来源：dbt Labs Blog
- URL：https://www.getdbt.com/blog/sigma-dbt-dagster-semantic-layer
- 作者：Daniel Poppy（dbt Labs）；受访：Matt Senick（Sigma Computing, lead data platform engineer）
- 发布/最后编辑：2026-10-27
- 存档说明：本文件为原文的**摘录**，非全文；引用以原文为准。

## 摘录

Matt Senick, lead data platform engineer at Sigma Computing, spent his dbt Summit 2026 session walking through how Sigma runs its own semantic layer, the same kind of layer it sells to customers, as versioned code inside a dbt project orchestrated by Dagster.

Senick framed the semantic layer's job in the age of LLMs around three things: giving AI applications guardrails, like PII restrictions and SQL formatting rules, baked directly into model-level instructions; giving every AI surface in the company the same definitions for a given metric so they never disagree with each other; and giving agents enough model context, synonyms, and verified queries to move past generic text-to-SQL guessing.

Inside Sigma's own dbt project, semantic objects are defined and version-controlled directly in SQL and Jinja, mapped to specific warehouse tables, with explicit column-level control over what gets exposed to business users.

Sigma splits its semantic models by business function (sales, marketing, customer success, product, and more) and relies on a small set of dbt packages, including dbt-sigma-data-model, dbt-semantic-view, and dbt-cortex-agent, to compile those definitions into Sigma data models, Snowflake semantic views, and Cortex agents respectively, all as ordinary dbt nodes.

Dagster orchestrates the whole thing: 63 jobs continuously build and deploy across 2,883 dbt models and 6 data regions, downloading the dbt manifest from S3, running a state-aware dbt build, syncing the resulting Sigma data models back through Sigma's API, and re-uploading the manifest for the next run.

Senick also previewed Open Semantic Interchange, an effort nicknamed Ossie that aims to let teams convert between a Snowflake semantic view, a dbt metric, and a Sigma data model without locking into any single vendor's format.
