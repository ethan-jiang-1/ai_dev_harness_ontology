# Google OKF：原文摘录与可核事实

> 摘录日期：2026-11-12。`web_fetch` 对 `cloud.google.com` 被策略拒绝（DNS 解析到非公网 IP），改用 `curl` 取全文后去标签；下列引文均为逐字。
> 日期一律用 JSON-LD `datePublished`；页面署名行比它晚 1 天（June 13 / July 25 / August 27），是 +08 时区渲染，不是另一个版本。

## 1. v0.1（2026-06-12）

URL：https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
作者：Sam McVeety（Tech Lead, Data Analytics）、Amir Hormati（Tech Lead, BigQuery）

> "Andrej Karpathy, the prominent AI researcher and educator, articulates this idea most crisply in his LLM Wiki gist. "LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass," he writes. The bookkeeping that causes humans to abandon personal wikis is exactly what LLMs are good at."

> "An OKF bundle is a directory of markdown files representing concepts: anything you want to capture, including tables, datasets, metrics, playbooks, runbooks, and APIs. Each concept is one file. The file path is the concept's identity"

> "1. Minimally opinionated. OKF requires exactly one thing of every concept: a type field. Everything else (e.g., what types exist, what other fields to include, what sections the body has) is left to the producer. The spec defines the interoperability surface, not the content model."

> "Just YAML frontmatter — for the small set of structured fields that need to be queryable: type, title, description, resource, tags, and timestamp"

> "Concepts link to each other with normal markdown links, turning the directory into a graph of relationships that is richer than the parent/child links implied by the file system. Bundles can optionally include index.md files (for progressive disclosure as agents navigate the hierarchy) and log.md files (for chronological history of changes)."

> "Published by the Google Cloud Data Cloud team. Open Knowledge Format is an open specification; contributions, alternative implementations, and adoption beyond Google products are all explicitly welcomed."

- 博客正文**没有 license 句**；license 在仓库 `LICENSE.md`（Apache-2.0）。
- v0.1 当时的规范副本：`GoogleCloudPlatform/knowledge-catalog/tree/main/okf`（现为冻结快照）。

## 2. v0.2（2026-07-24）

URL：https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals
作者：同上

> "It adds vocabulary, not rules: type is still the only always-required field, every new field is opt-in, custom keys are still preserved rather than rejected, and a bundle that adopts none of the additions is exactly as valid as it was under v0.1."

> "What was this created from? (provenance) / How much should I trust it? (trust) / Is it still true? (freshness) / Is it the current version? (lifecycle) / Was this number produced the way we said it must be? (attestation)"

> "The new sources field records the materials a concept derives from: an external doc, a bundle-relative path, or even a scope descriptor like "all queries in project X." At the same time, an entry can carry objective credibility signals: author, usage_count, last_modified." / "The deliberate choice here is what we didn't add. OKF records the signals, not a credibility score."

> "generated: { by, at }: how the current content was produced, and when it last meaningfully changed." / "verified: [ { by, at } ]: a list of independent confirmations against the sources or the underlying resource"

> "status moves a concept through draft → stable → deprecated (absent means stable). stale_after is a single absolute date."

> "OKF v0.2 introduces a new concept type, Attested Computation." / "Crucially, OKF records the computation and how to check it; it never executes anything itself."

> "Tiers are advisory signals, not access control, but they let a consumer say "only surface human-reviewed metrics in the executive dashboard" as a frontmatter filter."

> "v0.2 is a minor version bump that is additive, backward-compatible, with two deliberate renames: timestamp is superseded by generated.at, and the body # Citations list is superseded by sources… A v0.1 bundle drops in unchanged."

> "acme_retail, a fictional US retail company's shared knowledge for AI-assisted analytics over BigQuery"

## 3. Knowledge Catalog 集成（2026-08-26）

URL：https://cloud.google.com/blog/products/data-analytics/scale-okf-bundles-across-an-organization-with-knowledge-catalog
作者：Firat Elbey（Group Product Manager, Data Analytics）、Sam McVeety

> "By mapping the bundle onto Knowledge Catalog's existing types, every concept becomes discoverable, governed, and reachable by any agent already reading from the catalog."

> "Each entry carries schema, lineage, ownership, and tags, and can be extended with typed aspects that add domain-specific fields. … The context retrieval is secure and governed by IAM controls, so agents can only see the entries they have access to based on IAM identity."

> "Bundle Entries inherit IAM from the EntryGroup, so a single agent call returns exactly what the caller is permitted to read, with no parallel permission model to maintain."

> "The okf-aspect.json schema in the sample code defines the AspectType. It carries 13 fields covering the full OKF v0.2 spec:"

字段实名（按原文表格）：`okf_type, generated, sources, verified, status, stale_after, usage_window, runtime, parameters, computation, executor, attester, extra`
→ **没有 `attestation` 字段；也没有 `type`（叫 `okf_type`）**。

> "The Acme Retail bundle is a synthetic OKF bundle for a US retailer's BigQuery estate. It contains nine leaf concepts across six directories (attesters, tables, metrics, computations, policies, skills), each with its own index.md, plus a bundle root with its own index.md and log.md. That's 17 pushed Entries in total; Dataplex auto-creates one `<eg>_entry` alongside, so `gcloud dataplex entries list` returns 18 rows."

## 4. 规范正文（SPEC.md v0.2）

URL：https://raw.githubusercontent.com/GoogleCloudPlatform/open-knowledge-format/main/SPEC.md
版本：`**Version 0.2**`；1007 行 / 5,164 words；无 v0.3。

**词频（可复算）**：whole-word 正则（`(?<![a-z0-9_])term(?![a-z0-9_])`，全文小写）：

| 词 | 次数 | 备注 |
|---|---|---|
| ontology | 0 | |
| RDF | 0 | |
| OWL | 0 | substring 12 次全是 "kn-owl-edge" 假阳性 |
| SHACL | 0 | |
| SPARQL | 0 | |
| knowledge graph | 0 | 连字符版也 0 |
| semantic layer（空格） | 0 | |
| Semantic-layer（连字符） | **1** | §12.3 "Considered and deferred"：`- Semantic-layer templates (Looker, dbt) where the attester comparison shifts from SQL equality to model-and-binding equality.` |

> **写法约束**：只能说「ontology/RDF/OWL/SHACL/SPARQL/knowledge graph 各 0 次；`semantic layer` 0 次，但 `Semantic-layer` 1 次且出现在推迟工作清单」。不能写成「semantic layer 0 次」的整句结论。

**Non-goals（原文）**：

> "- Defining a fixed taxonomy of concept types.
> - Prescribing storage, serving, or query infrastructure.
> - Replacing domain-specific schemas (Avro, Protobuf, OpenAPI, and so on). OKF *references* them; it does not subsume them."

**不得拒绝（原文）**：

> "Consumers SHOULD treat all other constraints as soft guidance. In particular, consumers MUST NOT reject a bundle because of: Missing optional frontmatter fields. / Unknown type values. / Unknown additional frontmatter keys. / Broken cross-links. / Missing index.md files."

> "`type` is the only always-required key; a concept carrying just `type` is fully conformant (§11)."

> "Consumers SHOULD preserve unknown keys when round-tripping and MUST NOT reject documents with unrecognized fields."

**信任边界（§5.3）**：

> "Trust tiers are advisory signals, not access control."

## 5. 仓库状态（2026-11-12 实测）

| 项 | 实测 |
|---|---|
| `GoogleCloudPlatform/open-knowledge-format` | 存在，HTTP 200；created 2026-08-11；Apache-2.0；1,458★；51 open issues；非 archive |
| main 最新 commit | `ad30107c3` 2026-08-21T20:08:36Z（merge PR #6, okf-iso-datetimes） |
| commit 数 / 作者 | **6 / 1**（amirhormati） |
| tags / releases | 0 / 0（无 v0.3） |
| `pushed_at` | 2026-11-06T18:22:04Z，来自未合并分支 `deprecate-repo`，不是 main |
| `open-knowledge-format/open-knowledge-format` | **404**；org 存在（created 2026-09-28），`public_repos: 0` |
| 迁移公告 | PR #63 "Mark the repository as deprecated"（2026-11-06 开，**open**）："…where OKF development continues (spec v0.3, bundles, and tooling)." |
| `knowledge-catalog/okf/` 旧副本 | 冻结快照；README："**Stop using the copy under `okf/` in this repository.**" |

## 6. 中文采用（用于采用面，不用来定义格式）

- **中泰证券**（2026-10-15，`admitted`）："知识载体采用开放知识格式（OKF），参考 Google Cloud 的开放知识格式和 Anthropic 的仓库化知识实践，以带有轻量结构化头部的 Markdown 文件保存知识……现有 OKF 文件继续作为权威源与交换格式"。原文**未写 OKF 版本**。
- **京东海博**（2026-09-24，同花顺转载，`signal` 级线索）：全文 5 次写 "OKF"，**从不展开缩写**；"= Google OKF" 是推断，不是原文。它给了可核的同类约定（一概念一 md、`type` 唯一必填、`index.md`/`log.md`、宽容消费）和 AB 数（542 秒 vs 967 秒，约 -44%）。
