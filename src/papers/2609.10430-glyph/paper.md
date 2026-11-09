---
source: 2609.10430-glyph.pdf
part: paper
converted: 2026-11-09
converter: pdftotext-layout
---

# Glyph: A Multi-Strategy Agentic System for Column Description and Sensitivity-Ontology Tagging of Enterprise Data Catalogs · 正文

> 由 `pdftotext -layout` 从 PDF 直接转换，保留原页顺序；两栏页面的左右栏在同一行并排出现，逐行读即可，引用前回 PDF 核。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。
>
> **拆分说明**：p.1–7 为整页（双栏并排）。p.8 同页既有正文（左栏 §5.3、§6，右栏 §7 Conclusion）又有参考文献开头，故本文件只留 p.8 的正文部分；p.8 的 References 段与 p.9–10 见 [references.md](./references.md)。PDF 有字体嵌入告警，个别行（如 p.8 末行 "Colvin…"）在转换时落到左栏位置，属版式噪声。

<!-- page 1 -->

                                                  Glyph: A Multi-Strategy Agentic System for Column Description and
                                                       Sensitivity-Ontology Tagging of Enterprise Data Catalogs
                                                                             Kostia Kudriavtsev, Parvez Rafi, Sha Sundaram
                                                                                                       Apple
                                                                                        Seattle, WA and Cupertino, CA, USA
                                                                           k_kudriavtsev@apple.com, p_rafi@apple.com, shas@apple.com


                                                                    Abstract                                 personally identifiable information (PII) is discovered reac-
arXiv:2609.10430v1 [cs.MA] 9 Sep 2026




                                                                                                             tively after incidents rather than proactively, and new engi-
                                          Enterprise data lakes accumulate tables faster than human          neers cannot reason about datasets they did not build.
                                          stewards can document or classify them, leaving columns
                                          with missing descriptions and unassigned governance labels.            One central challenge is the scale of dataset tagging. In
                                          This documentation debt undermines data discovery, access          practice, datasets are not confined to a single storage tech-
                                          control, and regulatory compliance. We present Glyph, a pro-       nology: the same logical catalog may span Apache Ice-
                                          duction system that frames two coupled problems, column            berg tables, relational databases (RDBMS), and Cassandra
                                          description generation and column type annotation for              column-family stores. Consistently tagging metadata across
                                          data classification, as cooperating LLM agents orchestrated        these heterogeneous backends, at the volume encountered
                                          as stateful graphs. The Descriptor grounds generation in the       in a production environment, is intractable by hand. A sin-
                                          pipeline source code that produces each column, retrieved on       gle organization’s production catalog spans ∼3.4M columns
                                          demand from an enterprise GitHub via a reasoning–acting            across ∼98,000 tables, distributed over four lines of business
                                          tool loop (active Retrieval-Augmented Generation). The Tag-
                                          ger assigns labels from a governed 275-leaf Data Classifica-
                                                                                                             and the three storage backends above. At this scale, manual
                                          tion Ontology by running three complementary strategies in         annotation is not merely slow but economically infeasible:
                                          parallel (a description tagger, a line-of-business regex tagger,   even a highly optimistic rate of one column per minute would
                                          and a metadata tagger backed by a fine-tuned contrastive en-       require roughly 30 person-years of expert effort for this cat-
                                          coder over a vector database), then fuses their ranked outputs     alog alone, and the catalog drifts faster than any team can
                                          with Reciprocal Rank Fusion (RRF). We fine-tune a 6-layer          keep pace. This combination of volume and backend hetero-
                                          MiniLM metadata encoder with an in-batch contrastive objec-        geneity, neither of which is addressed by point solutions tied
                                          tive, lifting same-tag retrieval on an in-distribution held-out    to one storage engine, is precisely what motivates an auto-
                                          split from NDCG@10 0.55 to 0.92 (MAP@100 0.19 → 0.90)              mated, learning-based approach: only a system that general-
                                          relative to the stock base encoder. We report end-to-end multi-    izes across backends and improves without per-table human
                                          label tagging quality under a recall-weighted F2 objective
                                          across three evaluation groups, an ablation isolating each
                                                                                                             labeling can bring documentation and sensitivity tagging to
                                          strategy and the RRF fusion, and the engineering decisions         catalog scale.
                                          that distinguish Glyph from prior column-type-annotation               The second task is an instance of column type annotation
                                          work and from commercial value/regex sensitivity scanners:         (CTA), the assignment of a semantic label to a column. It is
                                          value-free and code-grounded design, per-tag provenance, and       a problem studied for over fifteen years, from joint graphical
                                          graceful degradation. Together these make multi-agent LLM          models over web tables (Limaye, Sarawagi, and Chakrabarti
                                          cataloging auditable and operable as a production service.         2010) through supervised deep classifiers (Hulsebos et al.
                                                                                                             2019; Zhang et al. 2020), pre-trained table encoders (Suhara
                                                                                                             et al. 2022; Deng et al. 2021), and, most recently, large lan-
                                                             1     Introduction                              guage models (Korini and Bizer 2023; Feuer et al. 2024;
                                        Modern analytics organizations operate data catalogs con-            Kayali et al. 2024). Glyph differs from this lineage in three
                                        taining tens of thousands of tables and millions of columns.         ways that define its contribution. First, its target is not an
                                        Two questions must be answered for every column before the           open-domain type vocabulary (DBpedia/Schema.org) but a
                                        data can be safely used: what the column means (documen-             governed enterprise sensitivity ontology: 275 leaf anno-
                                        tation) and what category of data it holds (classification and       tations organized by and sensitivity level, where the dom-
                                        governance). In practice both are answered manually, if at           inant class (internal non-sensitive) covers roughly 72% of
                                        all: descriptions are missing or stale, and sensitive-data tag-      columns. Second, Glyph is privacy-preserving by design:
                                        ging, needed for access control and privacy compliance, lags         it never reads cell values. The encoder sees only the structural
                                        discovery by months. The cost is concrete: undocumented              key catalog.database.table.column, and the De-
                                                                                                             scriptor grounds in the producing source code rather than the
                                        Copyright © 2027, Association for the Advancement of Artificial      data. Reasoning about sensitive tables without ever access-
                                        Intelligence (www.aaai.org). All rights reserved.                    ing their data is a first-class capability, not a limitation: it
satisfies enterprise privacy and data-access policy by con-        for ≈ 0.92. Pham et al. (2016) rank candidate labels by

<!-- page 2 -->

struction. Third, Glyph couples heterogeneous-strategy rank        similarity of an unseen column to labeled examples, and
fusion with an LLM-as-Judge self-refinement loop and per-          Meimei (Takeoka et al. 2019) is one of the few classical
tag provenance, so every label carries the source, score, and      methods that is explicitly multi-label per column.
reasoning behind it, a finer-grained provenance than the rule      Pre-trained table encoders. TURL (Deng et al. 2021),
logs of commercial scanners or the bare labels of academic         TaBERT (Yin et al. 2020), and TABBIE (Iida et al. 2021)
CTA systems.                                                       pre-train structure-aware Transformers over web tables; Do-
   Four requirements shaped the design and distinguish             duo (Suhara et al. 2022) serializes an entire table and fine-
Glyph from a naive “ask the model” prototype: (1) ground-          tunes a single BERT in a multi-task setup to predict col-
ing over guessing. Ambiguous names, such as a column               umn types and relations, reaching ≈ 0.92 micro-F1 on
name that may denote either a PII-sensitive person name            VizNet and remaining the canonical fine-tuned baseline.
or a misnomer for a movie title, must be resolved from             RECA (Sun, Xin, and Chen 2023) enriches a target column
authoritative evidence rather than parametric guesses. (2)         with related tables retrieved by entity-schema matching, and
Defense in depth. Since no single signal suffices, Glyph           Watchog (Miao and Wang 2024) pre-trains column represen-
combines descriptions, structural metadata, historical assign-     tations contrastively for label efficiency. Every system in this
ments, and naming conventions in a principled way. (3) Mea-        family consumes cell values, though Doduo and TURL read
surable, self-improving quality. Output is verified automat-       headers alongside them.
ically against an explicit bar and refined when it falls short.
(4) Production discipline: stateless horizontal scaling, de-       LLM-era CTA. Korini and Bizer (2023) frame CTA as text
terministic decoding, per-request authentication, structured       classification and prompt ChatGPT, finding that few-shot,
tracing, and reproducible training.                                label-narrowing prompts approach fine-tuned baselines on
                                                                   SOTAB. ArcheType (Feuer et al. 2024) maps free-form LLM
Contributions. (a) A two-agent architecture that separates         output back to a fixed vocabulary by label remapping, reach-
meaning generation (Descriptor) from category assignment           ing near-SOTA with open models. CHORUS (Kayali et al.
(Tagger), connected by a shared state and ontology, and,           2024) shows one foundation model can subsume table-class
to our knowledge, the first published account of multi-            detection, CTA, and join discovery via prompt assembly,
strategy CTA targeting a governed enterprise sensitivity on-       and RACOON (Wei, Xiao, and Balazinska 2024) retrieval-
tology with sensitivity levels. (b) A multi-strategy tagger that   augments LLM CTA with a knowledge graph. Table-GPT (Li
fuses dense retrieval, LLM reasoning, and rule-based sig-          et al. 2024) and TableLlama (Zhang et al. 2024) instead
nals with Reciprocal Rank Fusion (RRF) (Cormack, Clarke,           instruction-tune LLMs for table tasks.
and Büttcher 2009) and a candidate-constrained LLM re-
ranker, with full per-tag provenance. (c) A contrastive fine-      How Glyph differs. Glyph’s metadata tagger (Section 4.3.3)
tuning recipe (Henderson et al. 2017) for a metadata-specific      descends from the similarity-to-labeled-examples line but
encoder, improving in-distribution candidate recall of the         uses a fine-tuned neural encoder and ANN search over
metadata tagger (NDCG@10 0.55 → 0.92, MAP@100                      a curated corpus rather than hand-engineered features; its
0.19 → 0.90) on a per-tag, column-level held-out split of          regex tagger (Section 4.3.2) is a T2K-style matcher (Ritze,
the training corpus. (d) An end-to-end evaluation methodol-        Lehmberg, and Bizer 2015); and its description tagger (Sec-
ogy built on steward-curated, per-line-of-business sets under      tion 4.3.1) is a retrieval-constrained, candidate-validated
strict and expanding regimes, plus a strategy ablation, and a      variant of single-prompt LLM CTA (Korini and Bizer 2023)
documented production stack that turns the prototype into a        with ArcheType-style label grounding (Feuer et al. 2024).
reliable service.                                                  Three differences are structural. Generation is constrained to
                                                                   retrieved ontology candidates rather than remapped post hoc.
                                                                   Three heterogeneous strategies are fused by RRF rather than
                    2   Related Work                               one prompt being trusted, a per-column trade against the
Glyph sits at the intersection of two literatures: se-             collective inference of Limaye, Sarawagi, and Chakrabarti
mantic column type annotation and enterprise meta-                 (2010) and Sato (Zhang et al. 2020) that we revisit in Sec-
data/governance catalogs, which we survey in turn.                 tion 6. And none of these systems targets a governed sensi-
                                                                   tivity taxonomy from metadata alone, without cell values.
2.1   Semantic Column Type Annotation
Classical and supervised CTA. Assigning a category la-             2.2   Benchmarks
bel to a column was pioneered by Limaye, Sarawagi, and             The dominant CTA benchmarks measure open-domain
Chakrabarti (2010), whose graphical model jointly anno-            types: VizNet (Hu et al. 2019) supplies the 78-type Sher-
tates cells, column types, and inter-column relations against a    lock/Sato corpus; SOTAB (Korini, Peeters, and Bizer
knowledge base via collective inference; T2K Match (Ritze,         2022) labels web tables with 91 Schema.org types; Git-
Lehmberg, and Bizer 2015) is the reference unsupervised            Tables (Hulsebos, Demiralp, and Groth 2023) annotates
matcher to DBpedia. Sherlock (Hulsebos et al. 2019) re-            ∼1M repository-mined tables and documents that CTA ac-
framed CTA as supervised learning over character-, word-,          curacy drops on realistic relational tables; SemTab (Jiménez-
and statistics-level features of column values, predicting one     Ruiz et al. 2019) runs the annual CEA/CTA/CPA
of 78 types at support-weighted F1 ≈ 0.89 on VizNet, and           challenge against DBpedia/Wikidata. None measures a
Sato (Zhang et al. 2020) added table context and a CRF             sensitivity/data-classification taxonomy, none is multi-label
in Glyph’s sense, and all treat cell values as the primary sig-   USER_ID, EMAIL_ADDR)1 grouped under classification

<!-- page 3 -->

nal even where headers are present. Because SOTAB and             categories. The categories form a hierarchy from generic
GitTables do ship column headers, they remain a usable            (e.g., the PII category) to specific (e.g., the EMAIL_ADDR
out-of-distribution probe for Glyph’s metadata-only encoder       leaf annotation). Each annotation additionally carries several
(Section 7) — concrete near-term work.                            dimensions, such as a sensitivity-level scale, so the ontology
                                                                  encodes not only what a column is but how sensitive it is and
2.3   Industrial Catalogs and Data-Security                       to whom.
      Posture                                                        This makes Glyph’s target fundamentally unlike the open-
                                                                  domain type vocabularies of VizNet (Hu et al. 2019),
Goods (Halevy et al. 2016) is the canonical account of au-        SOTAB (Korini, Peeters, and Bizer 2022), GitTables (Hulse-
tomatic enterprise metadata enrichment at scale, crawling         bos, Demiralp, and Groth 2023), and SemTab (Jiménez-Ruiz
billions of datasets to infer schema, provenance, and sum-        et al. 2019): the labels are governance decisions, the task
maries, but not LLM-generated descriptions or governed            is multi-label, and the distribution is severely skewed. The
sensitivity labels. Aurum (Castro Fernández et al. 2018) and      internal non-sensitive class (NON_SENSITIVE) alone ac-
Table-Union search (Nargesian et al. 2018) link columns           counts for ≈ 72% of columns. This imbalance is the central
by content signatures for discovery; Glyph’s fine-tuned en-       learning challenge and motivates both class-balanced train-
coder plus ANN search is the neural analogue used for             ing and an evaluation that does not let the majority class
tagging rather than join discovery. Open catalogs such as         mask minority-class errors (Sections 4.4 and 5).
DataHub (LinkedIn 2019) and Amundsen (Grover et al.               Why values are off-limits. Reading cell values to clas-
2020) store column tags and lineage but rely on rule/keyword      sify enterprise columns is, for many of the most sensitive
classifiers and human-authored descriptions, and Apache At-       datasets, precisely the action governance forbids before clas-
las (Apache Software Foundation 2015) propagates sensi-           sification exists, a chicken-and-egg constraint absent from
tivity classifications along lineage without inferring the seed   value-driven CTA (Hulsebos et al. 2019; Zhang et al. 2020;
label. Commercial governance and value-scanning tools (Mi-        Suhara et al. 2022). Glyph therefore operates on metadata
crosoft 2021; Informatica 2018; Microsoft 2018; Google            and code (which engineers may read) rather than data, trading
Cloud 2017; BigID, Inc. 2016; Immuta, Inc. 2015) auto-            a signal for deployability on restricted-access tables where
apply classifications predominantly via regex, dictionaries,      Sherlock/Doduo-style scanners cannot run.
and value-pattern matching over cell values. Glyph is the
enrichment engine that produces the descriptions and seed                                4    Approach
labels those catalogs store and propagate; by reasoning from
the producing source code and structural metadata it can clas-    4.1   System Overview
sify columns whose sensitivity is contextual rather than          Glyph is a graph-structured agent application: each agent
format-detectable — a generic recommendations col-                is a directed graph of nodes (pure functions over a typed
umn holding a list of recommended apps, which a value             state) connected by ordinary and conditional edges, built
scanner sees only as high-entropy noise.                          with LangGraph (Chase and LangChain Inc. 2024). Nodes
                                                                  are produced by a builder pattern that injects dependencies
                                                                  (catalog client, LLM handles, search services) through an
      3   Problem Formulation and the Data                        ApplicationConfig, decoupling node logic from I/O.
               Classification Ontology                            State is a Pydantic (Colvin et al. 2023) model, validated at
                                                                  every hop, and configuration is layered in three tiers (en-
We formalize the two problems Glyph solves, description           vironment defaults → per-deployment AgentConfig →
generation and multi-label sensitivity classification, and then   per-request HyperParams). Fig. 1 depicts the two agents
describe the governed ontology that makes the classification      and their nodes.
task fundamentally unlike open-domain column-type anno-              The two agents are independently deployable REST ser-
tation.                                                           vices but compose naturally: the Descriptor’s generated de-
Task. Let a column be identified by its metadata key              scriptions are the ideal input to the description tagger. Both
                                                                  decode at temperature 0.0 for determinism, cap token usage,
            x = ⟨LOB, database, table, column⟩             (1)    and create LLM handles per request so model choice and
                                                                  credentials can vary by call.
and (optionally) a natural-language description dx , where           Glyph is assembled from components whose behavior is
LOB stands for line of business (a representation of the com-     well characterized — active retrieval-augmented generation,
pany’s enterprise hierarchy). Glyph solves two problems: (i)      contrastive dense retrieval, multi-label classification, rank fu-
description generation, producing dx from authoritative ev-       sion, and LLM-as-Judge critique. This is a deliberate choice
idence; and (ii) multi-label classification (Tsoumakas and        for a governed sensitivity ontology, where auditable com-
Katakis 2007), assigning a subset Yx ⊆ O of an ontology           ponents with known failure modes matter more than novel
O of sensitivity annotations, each with a confidence and a            1
justification.                                                          Ontology tag names shown throughout this paper (e.g.,
                                                                  USER_ID, EMAIL_ADDR, NON_SENSITIVE) are illustrative
The ontology. O is the Data Classification Ontology, a gov-       placeholders; the production Data Classification Ontology uses dif-
erned taxonomy of 275 leaf annotations (e.g., USER_NAME,          ferent internal codes, which are withheld for confidentiality.
                                                            Descriptor

<!-- page 4 -->

                                        retry w/ feedback



fetch_schema              analyze_batch              grade_results                generate_dataset_                  format_output
                            GitHub RAG                 LLM-as-Judge                  description


                                                              Tagger
                                                    retry failed cols


                                 llm_desc_tagger                  evaluate_metrics
                                   description-based                 LLM-as-Judge




prepare_columns                    regex_tagger
                                      rule-based             merge_all_tags               tag_normalizer             format_output
                                                                RRF k = 60                   tier-weighted


                              llm_metadata_tagger
                                   metadata-only

Figure 1: Glyph as two independently deployable LangGraph agents. The Descriptor grounds column descriptions in the pro-
ducing source code via an active-RAG tool loop, with an LLM-as-Judge refinement cycle. The Tagger runs three complementary
strategies in parallel and fuses their ranked tag lists with Reciprocal Rank Fusion (k = 60), then re-scores them by sensitivity
tier; a separate judge refines the description tagger. Orange boxes are LLM-as-Judge stages, grey boxes are I/O.


machinery. The contribution is the composition: which sig-              ally produces each column.2 A heuristic confidence score is
nals are fused, how they are validated against the ontology,            assigned to each description from observable signals (length,
and what it takes to serve them. Each mechanism is described            presence of technical and business terms, whether the pro-
below with its lineage cited in place.                                  ducing job was identified, and PII awareness), capped at 1.0.
                                                                        PII flagging. A first-class objective: columns such as
4.2   The Descriptor Agent                                              user_id are prefixed with explicit PII warnings, and the
                                                                        autograder scores PII awareness directly. Whereas value-
The Descriptor answers “what does this column mean?” as                 level scanners such as Presidio (Microsoft 2018) and Cloud
a four-stage pipeline (top panel of Fig. 1).                            DLP (Google Cloud 2017) detect PII from recognizable
Schema Discovery. fetch_schema queries the enterprise                   value formats, Glyph reasons about sensitivity from the code
data registry (the organization’s internal metadata catalog) to         and metadata, catching identifiers whose values are opaque
collect table details: column names, types, existing descrip-           hashes that format detectors miss.
tions, etc.                                                             Dataset      description.      A    generate_dataset_
                                                                        description node synthesizes a table-level sum-
Source-grounded generation (RAG). analyze_batch                         mary of business purpose from the per-column results,
is the core. To avoid the latency and inconsistency of per-             giving downstream consumers a self-documenting catalog
column calls, all columns are analyzed in a single LLM                  entry.
invocation, in batches of at most 50 columns. The model is
                                                                        Grading         and       refinement.      When      enabled,
given the schema and a tool, GitHub Enterprise code search,
                                                                        grade_results invokes a judge model over the
that it may call autonomously; the evidence is code, not data
                                                                        descriptions in batches. The judge scores four criteria —
— the Descriptor never reads column values. This realizes
                                                                        plausibility, specificity, completeness, and PII awareness —
active RAG (Lewis et al. 2020; Yao et al. 2023), with the in-
                                                                        aggregated with fixed weights (0.35, 0.25, 0.25, 0.15), and is
terleaved reasoning of chain-of-thought prompting (Wei et al.
                                                                        configured by default to be a different model family from the
2022) and in contrast to a fixed dense retriever (Karpukhin
                                                                        generator, since LLM judges exhibit self-enhancement bias
et al. 2020): the LLM decides which queries to run (a de-
fault budget of 3 tool calls per column, capped per batch                  2
                                                                            Code search is rate-limit aware: a proactive 2 s pause after
with forced finalization), reads context around each match,             25 calls in a 60 s window, plus exponential back-off (30 s initial,
and grounds descriptions in the application code that actu-             doubling, up to 5 attempts).
when scoring their own output (Zheng et al. 2023). Columns       4.3.3 Metadata Tagger The metadata tagger works

<!-- page 5 -->

that fall below threshold are returned to analyze_batch          from structural metadata alone, the fully qualified key
with the judge’s per-criterion feedback; on retry the agent      catalog.database.table.column, without need-
re-searches GitHub for the worst-scoring columns. The loop       ing a human description, a metadata-only descendant of
runs up to a small fixed cap (2 passes by default).              value-feature classifiers (Hulsebos et al. 2019) and similarity-
                                                                 to-example rankers (Pham et al. 2016). It is itself a RAG
4.3   The Tagger Agent                                           system (Lewis et al. 2020): the metadata key is encoded with
                                                                 a fine-tuned sentence encoder (Section 4.4) and searched
The Tagger answers “what category of data is this?” by
                                                                 against an exact inner-product (flat) vector index of veri-
assigning ontology tags (e.g., USER_ID, EMAIL_ADDR)
                                                                 fied training-corpus assignments built from human labeled
with confidence scores and reasoning. Its defining feature
                                                                 corpus. Vectors are L2-normalized so inner product equals
is multi-strategy parallelism with principled fusion: three
                                                                 exact cosine similarity; candidates above a configured simi-
strategies run concurrently over the columns (each fanned out
                                                                 larity S1 carry the tags of their nearest historical neighbors.
into worker batches), and their ranked tag lists are merged
                                                                 Long, deeply nested types are truncated to 200 characters at
by a dedicated fusion node (bottom panel of Fig. 1). The
                                                                 clean delimiter boundaries to match training-time formatting
three are chosen so that their failure modes are uncorrelated,
                                                                 and reduce embedding noise.
allowing fusion to reconcile them.
                                                                    A worker then presents the retrieved candidates, with
4.3.1 Description Tagger The description tagger works            inline similarity attribution, to the LLM, which selects
from the meaning of a column and is retrieval-                   and ranks the final tags from these candidates. Each se-
constrained: for each column it forms the query "{name}:         lected tag carries a reasoning record noting exactly which
{description}" (where the description is the column’s            source contributed at what confidence (e.g., [sources:
human-authored entry in the enterprise data registry when        ann=0.92]). To our knowledge, this per-tag, multi-source
one exists, and the column name alone otherwise), retrieves      provenance is absent from prior CTA systems (Hulsebos et al.
the most similar ontology annotations from semantic search       2019; Zhang et al. 2020; Suhara et al. 2022; Deng et al. 2021;
above a cosine threshold C, and asks the LLM to select and       Yin et al. 2020; Iida et al. 2021; Sun, Xin, and Chen 2023;
rank the best tags from those candidates, with reasoning. Be-    Miao and Wang 2024; Korini and Bizer 2023; Feuer et al.
cause candidates are constrained to real ontology entries and    2024; Kayali et al. 2024; Wei, Xiao, and Balazinska 2024;
validated afterward, hallucinated tags are rejected. This is a   Li et al. 2024; Zhang et al. 2024), which emit labels without
retrieval-constrained, candidate-validated variant of single-    source attribution, and finer-grained than the rule-hit logs
prompt LLM CTA (Korini and Bizer 2023) with ArcheType-           of commercial scanners (Microsoft 2021; Informatica 2018;
style label grounding (Feuer et al. 2024); constraining gener-   Microsoft 2018; Google Cloud 2017; BigID, Inc. 2016; Im-
ation to retrieved candidates (rather than ArcheType’s post-     muta, Inc. 2015).
hoc remapping) is consistent with RACOON’s finding that          4.3.4 Cross-Strategy Fusion with Reciprocal Rank Fu-
retrieval improves LLM CTA (Wei, Xiao, and Balazinska            sion The three strategies produce independent ranked lists
2024).                                                           per column on incomparable score scales (an ANN cosine,
   The ontology annotations (for example, EMAIL_ADDR:            an LLM confidence, a binary rule hit). To combine them
an electronic mail address, typically                            without calibration, merge_all_tags applies Recipro-
written as user@domain)                are    rich    natural-   cal Rank Fusion (Cormack, Clarke, and Büttcher 2009),
language records, so this search uses a general-purpose          which needs no score calibration — and which, unlike self-
all-MiniLM-L6-v2 (Reimers and Gurevych 2019;                     consistency ensembling (Wang et al. 2023), fuses ranked lists
Wang et al. 2020) (384-dim) sentence encoder as-is.              rather than voting over samples. For a tag appearing at rank
Grading and refinement. When grading is enabled, an              ri (1-indexed) in each active source’s list,
evaluate_metrics node scores the description tagger’s                                  X            1
tags with a combination of zero-cost deterministic metrics               rrf(t) =                        ,    k = 60,
and a batched LLM-as-Judge (Zheng et al. 2023); columns                                          k + ri
                                                                                  i ∈ lists containing t
whose tags fall below the configured threshold are returned to
llm_desc_tagger for another attempt, a bounded Self-             normalized by the theoretical maximum nactive /(k + 1) (the
Refine (Madaan et al. 2023; Shinn et al. 2023) loop. The         score of a tag ranked #1 by every active source), yield-
refined output then joins the regex and metadata taggers at      ing a confidence in [0, 1] that equals 1.0 only under unan-
fusion (Section 4.3.4); only the description tagger passes       imous top agreement. When several strategies nominate the
through this judge.                                              same tag, a fixed priority order (llm_desc_tagger >
                                                                 llm_metadata_tagger > regex_tagger) selects
4.3.2 Regex Tagger The regex tagger encodes institu-             whose provenance fields (reasoning, ontology, grades) are
tional knowledge by applying domain expert defined line-         inherited, while the confidence is the cross-strategy RRF
of-business-specific pattern rules over column names; for        score. The fused list is deduplicated by annotation name,
example, a column email has a hardcoded rule that assigns        with the priority order above deciding which source’s prove-
the tag EMAIL_ADDR. The strategy provides high-precision         nance is retained, and sorted with a deterministic tie-break
anchors in the T2K matching lineage (Ritze, Lehmberg, and        on the annotation name.
Bizer 2015) that complement the learned signals.                   Finally, tag_normalizer re-scores the fused list
Source               INTERNAL COUNTRY NON_SENSITIVE                   Metric           Pre-tuning      Post-tuning             ∆

<!-- page 6 -->

Regex tagger            ✓                                             NDCG@10               0.5497           0.9225    +0.3728
Description tagger                    ✓                               MRR@10                0.7875           0.9469    +0.1594
Metadata tagger                       ✓                ✓              Accuracy@1            0.7138           0.9229    +0.2091
RRF score              0.333        0.667            0.328            Accuracy@5            0.8812           0.9797    +0.0986
                                                                      MAP@100               0.1888           0.9009    +0.7121
Table 1: Tagger votes and fused confidence for a country
column — “The 2-letter ISO 3166-1 alpha-2 country                   Table 2: In-distribution retrieval quality of the metadata
code.” The fused row is the normalized RRF confidence               candidate-generation encoder on a per-tag, column-level
(k = 60); the metadata tagger ranks COUNTRY above                   held-out split of the training corpus, before and after con-
NON_SENSITIVE.                                                      trastive fine-tuning. These are retrieval, not tagging, metrics.


against the governed sensitivity tiers of Section 3: it blends      Evaluation. A per-tag random 10% column-level held-out
the RRF confidence c with the annotation’s ontology tier            query set, with each tag’s contribution capped at 500 keys
weight w as α c + (1 − α) w, where untiered and higher-             to bound memory (9,242 queries against an 83,229-entry
sensitivity annotations are unweighted (w = 1.0) and lower-         corpus), is scored with an Information-Retrieval evalua-
sensitivity tiers (levels 2, 3, 4) carry weights 0.75, 0.5, 0.25,   tor (Reimers and Gurevych 2019; Järvelin and Kekäläinen
respectively. Tags below a minimum normalized score are             2002) using NDCG, MRR, MAP, and Accuracy@k. Be-
dropped and the remainder re-sorted, so the final ranking re-       cause the hold-out is at column granularity, columns from
flects both cross-strategy agreement and governed sensitivity       the same table may appear in both the query set and the
level.                                                              corpus, so these numbers are an in-distribution upper bound
   Table 1 works this scoring through for a single column.          that does not control for within-table leakage (Kaufman et al.
                                                                    2012). Table-disjoint splitting, at (catalog, db, table) gran-
4.4   Domain-Specific Embedding Fine-Tuning                         ularity, with floors of ≥ 30 test / ≥ 90 train samples per
The metadata tagger’s ANN search (Section 4.3.3) is the             tag, is applied separately to the training corpus, to index the
one component of the Tagger that a general-purpose en-              vector-search corpus; the encoder fine-tuning itself uses the
coder cannot serve well. Its queries are metadata keys that         column-level hold-out described above. Table 2 quantifies
are terse, abbreviation-laden, and non-linguistic, and a stock      how well the encoder surfaces same-tag historical neighbors
model does not know that uat.core_db.users.uid                      and therefore upper-bounds the candidate recall of the meta-
and prod.analytics.events.user_id denote the                        data tagger; end-to-end tagging accuracy on unseen tables
same concept; abbreviations, catalog prefixes, and type vari-       (Section 5) and out-of-distribution generalization (Section 7)
ants are opaque to it, and the off-the-shelf model leaves sub-      are addressed separately. The relevant set for a query is all
stantial same-tag recall unrealized in our training-corpus re-      same-tag corpus entries, so its size varies enormously by tag:
trieval diagnostic (MAP@100 ≈ 0.19; Table 2, pre-tuning).           huge for NON_SENSITIVE, a handful for rare tags. This is
We therefore fine-tune a compact all-MiniLM-L6-v2                   why recall@k is small while accuracy@k stays high (≥ 0.92
encoder (a 6-layer distillation of BERT (Devlin et al. 2019),       post-tuning). MAP@100 is the most informative line because
a Transformer (Vaswani et al. 2017) with 384 hidden units,          it rewards recovering the full same-tag pool regardless of its
∼90 MB) with an in-batch contrastive objective. This en-            size: its +0.71 gain shows the model surfaces far more of
coder is specific to the metadata index; the description tag-       the relevant neighbors that the metadata tagger’s LLM then
ger’s ontology search uses a stock encoder unchanged (Sec-          re-ranks.
tion 4.3.1).                                                            Both the encoder and the vector index are versioned
Training        data.      A       training     corpus      of      and published to S3-compatible object storage under times-
metadata_key → tags assignments is extracted                        tamped paths; the vector index is rebuilt from the same train-
from a production system and represents already tagged              ing corpus (embedding the metadata_key without the tag
and verified assignments. Pairs are constructed within tag          suffix to avoid train/serve skew) and loaded read-only on con-
groups: any two columns sharing a tag form an (anchor, pos-         tainer cold start. We use an exact inner-product (flat) index
itive) pair. Because a few tags (notably NON_SENSITIVE,             because the metadata tagger runs as a stateless, ephemeral
≈72%) dominate, we cap pairs per tag (3 000 for the reported        container at modest scale (102 –105 vectors); scaling past
encoder) and require a minimum group size, yielding 70 948          ∼106 vectors would require a quantized or graph-based in-
balanced training pairs.                                            dex.
Objective. We use MultipleNegativesRanking
Loss (Henderson et al. 2017) (scale 20, cosine similar-
                                                                                 5    End-to-End Evaluation
ity): for each (anchor, positive) pair, all other positives in      Table 2 measures retrieval, not tagging. This section reports
the batch act as negatives, pulling same-tag columns to-            the metric that is comparable in spirit to the CTA literature:
gether and pushing different-tag columns apart — the in-            end-to-end multi-label tagging quality of the full Tagger (all
batch-negatives recipe that also underpins dense passage re-        three taggers plus RRF) against curated expectations.
trieval (Karpukhin et al. 2020).                                    Harness and metrics. Glyph ships a tag-evaluation harness
                                                                         F1                                                     F2

<!-- page 7 -->

        Configuration                                    G1       G2          G3            Overall          G1          G2          G3   Overall       p50 (s)
        Regex tagger only                               0.062    0.103    0.128                 0.077       0.040       0.067    0.085    0.050           0.30
        Description tagger only, Claude Sonnet 4.5†     0.122    0.326    0.411                 0.205       0.250       0.325    0.590    0.238          47.31
        Metadata tagger only                            0.890    0.969    0.956                 0.912       0.853       0.957    0.937    0.880          40.41
        Fusion, Claude Sonnet 4.5                       0.878    0.951    0.932                 0.897       0.878       0.961    0.938    0.890          57.80
   †
       The description tagger is evaluated only over columns that carry a description; columns without one are out of scope for this strategy.

Table 3: Measured micro-averaged F1 and F2 per curated dataset group, overall F1 /F2 , and p50 request latency for each
configuration (higher F1 /F2 / lower latency is better). All runs cover the same 4 evaluation files. Per-group F1 /F2 is aggregated
from per-file confusion counts. The best F2 per group is in bold.


that compares predicted tags against curated expectations per                  dependent, and deliberately so: the three metrics disagree on
column over the universe of candidate tags, computing the                      which system to ship — under F1 the fusion and the meta-
confusion quantities and the derived accuracy, precision,                      data tagger are tied, and under F0.5 the single strategy leads
recall, and the Fβ family (Manning, Raghavan, and Schütze                      — so the choice of β is a deployment decision, not a cos-
2008). While we report precision, recall, F0.5 , and F1 for                    metic one. Third, quality trades against latency: fusion’s
completeness, we adopt F2 as the primary selection met-                        F2 comes at a p50 of 57.8 s. The description tagger is the
ric. The choice of β in Fβ = (1 + β 2 ) β 2PPR+R encodes a                     outlier: at 47.3 s it spends 82% of fusion’s latency to reach
cost model, and sensitivity tagging has a sharply asymmetric                   only 0.238, below the metadata tagger’s 0.880, so it is not a
one. A false negative, a sensitive or PII-bearing column left                  viable standalone configuration and earns its place only as
untagged, silently defeats access control and privacy com-                     an input to the fusion. The operative deployment choice is
pliance and is typically discovered only reactively, after an                  therefore metadata-only versus full fusion.
incident. A false positive, an over-applied tag, is cheap to
remediate and dismissed by a data steward during review.                       5.2              Deployed Impact: Steward Acceptance
We therefore select on F2 (β=2), which weights recall twice                    Glyph runs in production behind the governance workflow:
as heavily as precision and aligns the headline number with                    human stewards adjudicate its suggestions, and each accepted
the governance reality that missing a sensitive column is far                  or rejected column–tag pair is written back to a data store.
costlier than over-tagging a benign one.                                       The training pipeline re-exports that store, re-fine-tunes the
Evaluation sets. These sets are curated by line of business                    metadata encoder (Section 4.4) — a human-feedback loop
and span multiple LOBs, each a collection of {column                           that closes on a weekly cadence.
metadata, expected-tags} cases authored with
data stewards. The evaluation sets are table-disjoint from                                       100
                                                                                                                                                        99.8%
the training corpus of Section 4.4: none of their 1,905 ta-
bles appears in the 15,205-table vector index, though the two
                                                                                   accepted %




draw on overlapping catalogs and databases, so no evaluated
column was seen at training or indexing time.                                                     75


5.1      Per-Dataset Tagging Quality (F2 )                                                                  63.3%
Table 3 reports measured, micro-averaged F2 per curated                                           50
dataset group (Group 1–3) for four end-to-end configura-                                                1           2           3         4         5             6
tions, isolating (i) each strategy in isolation, and (ii) the full                                                            consecutive week
multi-strategy fusion. Per-group figures are micro-averaged
from the per-file confusion counts within each group (F2 =                     Figure 2: Weekly steward acceptance of Glyph’s tag sugges-
5 TP/(5 TP + 4 FN + FP)); the table also reports the over-                     tions over six consecutive weeks of production operation.
all F2 and the p50 request latency of each configuration.                      The vertical axis begins at 50%.
We lead with F2 (Section 5): the ranking of configurations
by F2 is the ranking that minimizes missed sensitive-data                         Figure 2 plots every steward decision to date: acceptance
classifications.                                                               rises from 63.3% to 99.8% across ∼ 24, 000 adjudicated
   Three findings stand out. First, no single strategy is suffi-               pairs. Decision volume grows 21× over the same window
cient: the regex tagger alone collapses to near-zero F2 across                 and the population under review broadens alongside it, so
every group (it fires on almost nothing outside its hand-                      we report the trend as an association rather than a causal
written patterns), and the strongest lone strategy, the meta-                  effect. Because a steward only ever sees tags the system
data tagger, reaches only 0.880 overall. Second, fusion ranks                  emitted, acceptance is a precision-like measure and is blind
above every single strategy under F2 : the best fused con-                     to false negatives; it complements rather than replaces the
figuration lifts overall F2 to 0.890. This ordering is metric-                 recall-weighted F2 of Table 3.
Dimension           Glyph (this work)      Sherlock                Sato                     Doduo                   Korini & Bizer

<!-- page 8 -->

Input signal      Metadata only; no cell Cell values               Values + table topic     Serialized table values Values + name
                  values
Learning paradigm Fine-tuned contrastive Supervised deep           DNN + CRF                Fine-tuned PLM          Zero-/few-shot LLM
                  encoder + rules +      neural network                                     (multi-task)
                  commercial LLM         (DNN)
Target taxonomy   275 curated tags       78 open types             78 open types            78 open types           SOTAB types
Fusion            RRF                    none                      CRF joint                multi-task head         none
Deployment        commercial             research                  research                 research                research
Reported eval     F1 ≈ 0.897 and F2 ≈ F1 ≈ 0.89 (VizNet)           F1 ≈ 0.92                micro-F1 ≈ 0.92         F1 ≈ 0.85 (SOTAB)
                  0.890

Table 4: Positioning of Glyph against representative CTA systems. Systems, in column order: Sherlock (Hulsebos et al. 2019),
Sato (Zhang et al. 2020), Doduo (Suhara et al. 2022) and Korini and Bizer (2023).


5.3   Positioning Against the CTA Literature
These numbers are not directly comparable to published CTA
F1 (Sherlock (Hulsebos et al. 2019), Sato (Zhang et al. 2020),
Doduo (Suhara et al. 2022), and the near-fine-tuned accu-
racy of ArcheType (Feuer et al. 2024) with open models
across several label spaces), because the taxonomy (a cu-
rated enterprise list of tags with sensitivity levels vs. 78–91
open-domain types without sensitivity levels), the label car-
dinality (multi-label, dominated by a few specific tags), and
the information available (metadata + code vs. cell values)
all differ; prior-work figures are reproduced from each pa-
per’s best-reported configuration and serve only as in-spirit
reference points.
   Table 4 positions Glyph against representative CTA sys-
tems and commercial sensitivity scanners across the dimen-
sions that matter for enterprise deployment.

          6    Discussion and Future Work
Glyph’s central bet is that redundancy plus principled fu-
sion beats any single clever signal: a rule engine that is pre-
cise but brittle, a dense retriever that generalizes but drifts,
and an LLM that reasons but hallucinates, reconciled by
RRF and an ontology validator, with an autograder convert-
ing open-ended generation into a measurable, self-improving
task. We are candid about what this paper does and does not
establish.
Operational lessons. Two design choices proved decisive
in production and generalize beyond Glyph. (1) Value-free,
code-grounded design (Section 1) lets Glyph run at all on
restricted-access tables that value/regex scanners (Microsoft
2021; Informatica 2018; Microsoft 2018; Google Cloud
2017; BigID, Inc. 2016; Immuta, Inc. 2015) cannot touch.
(2) Batching for cost: analyzing a whole table’s columns in
one LLM call rather than one call per column is the ratio that
dominates latency and cost at catalog scale.

Future work. Two directions to extend Glyph. (1) Collec-
tive inference. Glyph fuses per-column signals and ignores
the inter-column and inter-tag correlation exploited since Li-
maye, Sarawagi, and Chakrabarti (2010), Sato (Zhang et al.
2020), and Meimei (Takeoka et al. 2019); evaluating such
joint models under our NON_SENSITIVE tag dominance is
a promising direction. (2) A reinforcement-learning loop for

the Tagger: treating tag selection as a learned policy (Schul-
man et al. 2017) optimized against a reward model (Chris-
tiano et al. 2017; Ouyang et al. 2022), so that a persistent
policy learns to rank rare tags, attacking class imbalance, and
internalizes steward feedback rather than re-deriving quality
per request.
                      7    Conclusion
Glyph shows that automated, auditable data cataloging at en-
terprise scale is achievable by composing well-understood
techniques inside a disciplined agentic framework, and by
adapting the column-type-annotation tradition to a governed
sensitivity ontology under an enterprise privacy constraint
that forbids reading values. By grounding descriptions in
source code, fusing complementary value-free tagging sig-
nals, validating against an authoritative ontology, and grading
its own output, Glyph produces descriptions and tags that are
not only useful but explainable and auditable: every tag car-
ries its provenance, confidence, and reasoning. We have been
deliberate about the boundary between what is demonstrated
(strong in-distribution retrieval, a deployed multi-strategy
system) and what remains to be shown (public-benchmark
generalization, judge–human agreement), and we see clos-
ing that gap as the natural next step toward substantially
reducing the manual stewardship burden of enterprise data
governance.
