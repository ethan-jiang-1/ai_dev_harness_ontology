---
source: 2609.01780-kgvoyager.pdf
part: appendix
converted: 2026-11-09
converter: pdftotext-layout
---

# KGVoyager: Knowledge Graph Agnostic Question Answering via Agentic Navigation · 附录

> 由 `pdftotext -layout` 从 PDF 直接转换，保留原页顺序；两栏页面的左右栏在同一行并排出现，逐行读即可，引用前回 PDF 核。
> 第 11 页只取右栏（附录从这里开始，左栏仍是参考文献 [36]–[43]）；第 12–16 页整页转换，图表与工具 schema 有版式噪声。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 11 -->

Appendix
The appendix is organized as follows. Appendix A
lists implementation details and hyperparame-
ters. Appendix B measures how widely rdf:type
is used across okn.us endpoints, supporting
KGVoyager’s RDF typing assumption. Appendix C
analyzes performance as a function of query com-
plexity. Appendix D examines when the agent
uses each tool group, and Appendix E reports per-
question tool-call and SPARQL-execution counts.
Appendix F presents a failure analysis of KGVoyager,
and Appendix G gives the full system prompt and
tool specification.

A Implementation Details
Table 5 lists the key implementation parameters
used across all experiments.
 Parameter              Value
 Embedding model        BAAI/bge-small-en-v1.5
 Lexical retrieval      BM25 top-k: 20
 Dense retrieval        Dense top-k: 10
 Fusion                 RRF, equal weights, rank constant 61
 Re-ranker              BAAI/bge-reranker-base, top-k: 10
 Adaptive filtering δ   0.125, minimum 3 rows retained
 Property-usage         3000 triples
 sample size
 Vector index           In-memory, cosine similarity
 Caching                Embeddings stored on disk; reused
                        unless metadata changes
          Table 5: Implementation parameters.

B Prevalence of RDFS Typing
KGVoyager makes only one structural assumption:
instances are assigned to classes via the W3C
RDFS predicate rdf:type [7]. Its class index and
tools use this predicate to discover classes. To
check how practical this assumption is, we counted
typing triples and all triples via a SPARQL query
on the 28 okn.us knowledge graphs from our feasi-
bility study (Section 4.1). The wikidata endpoint
returned an error page instead of query results; how-
ever, Wikidata is known not to use rdf:type for
typing entities, as it relies on its own type system.
   We consider a graph to follow the RDFS typing
standard if it contains at least 1,000 typing triples.
Of the 28 graphs, 27 (∼96%) meet this criterion
(median of ∼7.1 million typing triples over the 27
graphs that returned a count; Figure 5), suggesting
that the assumption is reasonable for most knowl-
edge graphs. The only exception is wikidata. This
scan is unlikely to be biased by platform policy,
since okn.us only asks contributors for registry

<!-- page 12 -->

                                                                                 F1 difference (KGVoyager GRASP, points)
                   10        median = 7,118,528            10
                                                                          15
                                                                                                                      49
Knowledge graphs

                    8                                  8                           80   12      27
                                                                                          26 14                            38 46 40
                                                                          10                21                   12
                    6                                                                             3127                                             39
                                                                                                           36                         37
                                                                                                         63 35                             62 37
                    4                                                        5
                                             3    3
                    2                                            2
                                        1                                    0
                    0
                           101        103        105      107      109       5
                        Typing triples (rdf:type) per knowledge graph
                                                                          10
Figure 5: Number of rdf:type triples per okn.us
                                                                                  1-2     3-4 5-6 7+              0         1       2+
knowledge graph (27 graphs that returned a count; bins                                  Triple patterns            Special constructs
are powers of ten).                                                                        Climate Models KG           DREAM-KG
                                                                                           SOCKG                       DBLP
metadata and does not prescribe how entities are                         Figure 6: Mean paired F1 difference (KGVoyager minus
typed [27]. The prevalence of rdf:type instead re-                       GRASP) per benchmark by number of triple patterns
flects its status as the W3C-recommended standard                        (left) and distinct special SPARQL constructs (right) in
for assigning resources to classes [7].                                  the gold query. Points show means with 95% bootstrap
                                                                         confidence intervals over questions; numbers above the
                                                                         intervals are the number of questions; bins with fewer
C                  Query Complexity Analysis                             than 10 questions are omitted.

                                                                         D       Tool-Use Dynamics
To analyze performance as a function of question
complexity and to ensure the benchmarks used                             We analyze whether the agent follows the search–
for evaluation are nontrivial, we parsed the gold                        explore–execute progression described in Section 3.
SPARQL queries corresponding to the benchmark                            For each tool call, we compute its relative step in-
questions and measured the complexity of the un-                         dex, defined as position divided by total run iter-
derlying query subgraph by counting triple pat-                          ations, and pool values across the three KGVoyager
terns in the translated SPARQL algebra, together                         runs per benchmark-model pair.
with the number of distinct special SPARQL con-                             Figure 7 shows all four models. All follow the
structs (aggregation, FILTER, OPTIONAL, UNION,                           intended temporal structure on average: search
MINUS, EXISTS, subqueries, and property paths).                          early, exploration in the middle, and execution later.
We computed paired F1 differences (KGVoyager mi-                         GPT-6 Sol, the best-performing model (78.2% F1),
nus GRASP) for each question, averaging the three                        shows the cleanest phase separation, while GPT-
runs within each backbone model and then averag-                         OSS-120B, the weakest (41.9% F1), shows the
ing across models.                                                       most overlap. The other two models have similar
   The benchmarks differ in the complexity of their                      F1 (68.4% and 69.8% for Nemotron 3 Ultra and
gold queries, measured by the number of triple                           Muse Glimmer 30B) and similar overlap (0.34 and
patterns, which reflects the size of the subgraph                        0.33). This shows that phase mixing can provide
matched by the SPARQL query, and by the num-                             some signal about model performance.
ber of special SPARQL constructs, as shown in
                                                                         E       Tool Invocation Distributions
Figure 6. DBLP contains simpler queries than
other benchmarks, with at most four triple pat-                          Figure 8 reports the distribution of tool invoca-
terns, whereas the other benchmarks mostly con-                          tions per question (top) and the number of explicit
tain queries with five or more. We observe that                          SPARQL executions per question (bottom). Both
KGVoyager’s improvement over GRASP drops for                             analyses pool agent executions across all questions
the most complex queries, on which both systems                          in the four benchmarks, four backbone models, and
perform worse; for example, pooled F1 is 58.8%                           three runs. The distributions show that KGVoyager
for KGVoyager and 57.4% for GRASP on queries                             requires fewer tool invocations (19.2 vs. 22.2 on
with seven or more triple patterns, compared with                        average) and SPARQL executions (7.5 vs. 11.4)
66.7–70.8% and 62.9–67.4% on queries with three                          per question than GRASP, which indicates a more
to six.                                                                  efficient interaction with the knowledge graph.

<!-- page 13 -->

                  GPT-6 Sol                        GPT-OSS-120B                                0.15          KGVoyager (mean=19.2, median=15)
                 (n=11,324)                         (n=17,132)                                               GRASP (mean=22.2, median=17)

                                                                       Fraction of questions
          4         F1 78.2%                           F1 41.9%
                 S X overlap 0.29                   S X overlap 0.45                           0.10
Density

          2
                                                                                               0.05
          0
               Nemotron 3 Ultra                   Muse Glimmer 30B                             0.00
                 (n=23,958)                          (n=40,107)                                       0            10           20          30          40
          4         F1 68.4%
                 S X overlap 0.34
                                                       F1 69.8%
                                                    S X overlap 0.33
                                                                                                           Tool invocations per question (last bin: 40)
Density

          2                                                                                                                    KGVoyager (mean=7.5, median=4)
                                                                                                                               GRASP (mean=11.4, median=6)

                                                                       Fraction of questions
                                                                                               0.15
          0
                                                                                               0.10
           0.00 0.25 0.50 0.75 1.00 0.00 0.25 0.50 0.75 1.00
                  Relative step index (step / total steps)                                     0.05
                Search              Exploration            Execution
                                                                                               0.00
                                                                                                      0         5        10       15        20        25
                                                                                                          SPARQL executions per question (last bin: 25)
Figure 7: Relative timing of tool use by model: ker-
nel density estimates of the relative step index for the
search, exploration, and execution tool groups. Each                   Figure 8: Distribution of tool invocations (top) and
panel reports the model’s KGVoyager F1 averaged over                   explicit SPARQL executions (bottom) per question.
the four benchmarks and the S–X overlap, the overlap                   Dashed lines indicate means.
coefficient between the search and execution densities
(lower means cleaner phase separation).
                                                                       or using a SELECT query instead of an ASK query
F         Failure Analysis                                             for a yes/no question.
To understand the scenarios in which KGVoyager
breaks down, we analyze complete failures:                                     Group          Definition                           n %
(model, KG, question) triples that scored an F1                                Concept        Agent linked a question concept 29 19
of 0 across all three independent runs. Consider-                              Resolution     to the wrong instance, class, or
ing all the valid gold queries, this criterion yields                                         predicate IRI
156 complete failures across the four models and                               Query          Correct terms, but wrong con- 20 13
                                                                               Construction straints, relation direction, or join
benchmarks. We attribute each failure to a primary                                            path
cause using a two-level taxonomy of five coarse-                               Answer         Semantically analogous answer 28 18
grained error groups, each split into fine-grained                             Representation scored wrong due to not match-
categories.                                                                                   ing result form or shape
   Table 6 summarizes the coarse-grained distribu-                             Query Gen.     No usable final query was pro- 56 36
                                                                               / Execution    duced or a well-formed query
tion. Tables 7–11 detail the fine-grained categories                                          failed to execute
with representative examples.                                                  Other          Cases not fitting the above         23 15
   The largest group, query generation/execution
(36%), consists almost entirely of early stopping, as                  Table 6: Coarse-grained error distribution over 156
                                                                       LLM-classified complete failures (primary label per
seen in Table 10, mostly by smaller models such as
                                                                       case).
GPT-OSS-120B that appear to struggle with long
contexts. Another 31% represent genuine reason-
ing errors (concept resolution and query construc-
tion). As seen in Tables 7 and 8, these are spread                                Category                       n Summarized example
                                                                                  Wrong Class                    11 used c:City instead of c:No_Country_Region
evenly across wrong classes, properties, and enti-
                                                                                  Wrong Property                  9 used dblp:publishedInStream instead of
ties, and across missing constraints and incorrect                                                                  dblp:publishedIn
joins. Answer representation (18%; Table 9) covers                                Wrong Entity                    9 used pid_94:5174 instead of pid_04:1616 (a
                                                                                                                    different author)
answers whose content is analogous to that of the
gold query but whose form or shape differs. For ex-                                            Table 7: Concept resolution errors (29 cases).
ample, returning paper IDs instead of paper names

<!-- page 14 -->

                                                                         G     KGVoyager System Prompt and Tool
                                                                               Specification

 Category             n Summarized example                                   You are a SPARQL query generation assistant. Your
 Missing Constraint   10 omitted required COUNT(DISTINCT                     job is to generate an accurate SPARQL query that an-
                         ?oceanTopic)
                                                                             swers the user’s question by dynamically discovering
 Incorrect Join       10 used service → schema:audienceType instead
                         of service → schema:category → audience →
                                                                             the knowledge graph’s structure.
                         schema:audienceType                                 You operate in a think-act-observe loop: reason about
                                                                             what you need, invoke a tool, then interpret the re-
    Table 8: Query construction errors (20 cases).                           sults before deciding the next action. Follow this
                                                                             workflow:
                                                                             1. SEARCH: Identify the classes, properties, and
                                                                                entities implied by the question. Search for can-
                                                                                didate class and property URIs using natural-
                                                                                language terms. If the question mentions named
                                                                                entities, resolve them by first finding their class,
                                                                                then looking up instances by name. Use relevance
                                                                                scores and usage counts to select the most likely
                                                                                candidates.
 Category             n Summarized example                                   2. EXPLORE: If the search results do not clearly re-
 Result Shape         20 used ?paper ?paperName ?metricCount instead            veal how properties connect entity types, explore
                         of ?paperId ?metricCount
                                                                                property usage patterns to see actual domain/range
 ASK vs. SELECT        4 used SELECT ?paper ?pid instead of ASK
                                                                                types and example triples. If you need to under-
 IRI vs. Label         4 used "Ammonium Nitrate 34-0-0" instead of              stand the neighborhood of a specific entity, ex-
                         individuals:AmendmentType.30
                                                                                plore its relations.
  Table 9: Answer representation errors (28 cases).                          3. CONSTRUCT AND TEST: Build the SPARQL
                                                                                query incrementally using the discovered URIs.
                                                                                Execute intermediate drafts to verify correctness.
                                                                                If results are unexpected, revisit earlier steps –
                                                                                you may have the wrong property, class, or triple
                                                                                pattern. Once the query returns the expected re-
                                                                                sults, call the answer function. If you cannot find
                                                                                a satisfactory query, call cancel.
                                                                             Keep in mind:
                                                                             • Always strategically decide which tool call to make
 Category             n Summarized example                                     next. Include reasoning about your objective with
 Agent Gave Up        50 Agent gave up after being mostly stuck in the
                                                                               the tool call whenever possible
                         search phase for 20 iterations
                                                                             • Never make a redundant tool call. You will be
 No Valid Query        6 The submitted query used rdfs:label without
                         declaring the rdfs: prefix
                                                                               highly penalized if you repeat a tool call or per-
                                                                               form tool calls of very little value (eg, verifying
Table 10: Query generation/execution errors (56 cases).                        something already obvious). It’s absolutely normal
                                                                               if you only use a subset of the available tools to
                                                                               solve the problem.
                                                                             • Overall solving this with the least amount of tool
                                                                               calls but the perfect accuracy is the ultimate goal.
                                                                             • Never return a SPARQL query before verifying it is
                                                                               correct and returns results that answer the question.
                                                                             • For questions with a “True” or “False” answer the
                                                                               SPARQL query should be an ASK query.
 Category             n Summarized example                                   Available knowledge graphs:
 Ambiguous            10 not clear how to rank the top 5 papers: all         {{ knowledge_graphs }}
 Question                4,482 papers tie at one distinct method
 Top-k / LIMIT         3 used ORDER BY DESC(?methodCount)                          Figure 9: KGVoyager system prompt.
 Tie-Break               ?name instead of ORDER BY
                         DESC(?methodCount)

Table 11: Other errors (23 cases). The remaining 10
cases fall into rare miscellaneous categories (one or two
cases each) that are not shown.

<!-- page 15 -->

    SEARCH                                                                                    EXPLORATION

               Class Search           search_all_classes(search_term, limit)                            Property Usage Exploration
                                                                                                         explore_property_usage(property_uri, limit, max_sampl
                                                                                                         e, include_class_prefixes)
     Search for classes in the Knowledge Graph by name or concept. Uses
     hybrid retrieval (semantic + keyword) to find relevant classes. Low-
     relevance results are automatically pruned.                                              Analyze how a property is actually used in the graph by sampling real
                                                                                              triples. Infers domain and range from actual data rather than ontology
     Purpose: Use natural-language terms from the question to find candidate                  annotations (which are often missing or inaccurate).
     class URIs.
                                                                                              Purpose: Differentiate between linguistically similar properties by seeing
      INPUT SCHEMA                                                                            which entity types they actually connect, and verify that a candidate
                                                                                              property relates the expected types before committing it to the query.
     search_term     string REQ
     The concept, keyword, or class name to search for. Utilizes semantic search                INPUT SCHEMA
     to find relevant matches.
                                                                                              property_uri       string REQ
     limit     number OPT
     Maximum number of results to return (default: 10).                                       The full absolute URI of the property to analyze. Do not use
                                                                                              prefixed/abbreviated URIs.
                                                                                              limit     number OPT
      OUTPUT FORMAT
      ▤ TABLE WITH COLUMNS:
                                                                                              Number of example usage patterns to return (default: 10).
                                                                                              max_sample      number OPT
      class_uri      label        count   score
                                                                                              Maximum number of triples to sample for type analysis (default: 5000).
                                                                                              Reduce if the endpoint times out.
               Instance Lookup                                                                include_class_prefixes          string[] OPT
                lookup_class_instances(class_uri, search_term, limit,                         Optional list of URI prefixes to restrict the domain/range types shown. Useful
                mode)                                                                         to filter out noise when the knowledge graph spans many namespaces.
     Retrieve instances of a specific class, optionally filtered by name.                       OUTPUT FORMAT
                                                                                               ▤ TABLE WITH COLUMNS:
     Purpose: The primary way to resolve named entities mentioned in the
     question (e.g., 'France', 'Albert Einstein') to their URIs. First identify the            Domain      Domain Label        Range   Range Label    Example Subject
     entity's class via class search, then use this tool with the entity name as
     search_term.                                                                              Subject Label          Example Object   Object Label     Count

      INPUT SCHEMA
                                                                                                        Entity Relations Exploration
     class_uri     string REQ
     The full absolute URI of the class. Do not use prefixed/abbreviated URIs.                           explore_entity_relations(entity_uri, num_ents, limit)

                     string OPT
     search_term
                                                                                              Explore the relationships of a specific entity by listing all its incoming and
     Optional keyword to filter entities by label/name.                                       outgoing connections.
               number OPT
     limit
                                                                                              Purpose: Useful when search alone has been inconclusive for resolving a
     Maximum number of entities to return (default: 10).                                      relation mentioned in the question, as it reveals the full local graph
     mode    string OPT                                                                       structure around the entity.
     Result mode: 'labels_only' (default) searches only entity label; 'all_attributes'
     searches across all literal values.                                                        INPUT SCHEMA
                                                                                              entity_uri      string REQ
      OUTPUT FORMAT                                                                           The full absolute URI of the entity to explore. Do not use prefixed/abbreviated
      ▤ TABLE WITH COLUMNS:                                                                   URIs.
      entity      displayLabel        searchProp   searchVal                                  num_ents     number OPT
                                                                                              Number of sample neighbors to show per property (default: 3). Keep low to
                                                                                              avoid large outputs.
               Property Search                                                                limit     number OPT
                search_all_properties(search_term, limit)
                                                                                              Total number of results to return from query.
     Search for properties in the Knowledge Graph by name or concept. Uses                      OUTPUT FORMAT
     hybrid retrieval (semantic + keyword) to find relevant properties. Low-
     relevance results are automatically pruned.                                               ▤▤ 2 TABLES WITH COLUMNS:
                                                                                              Attributes (literals)
     Purpose: Find candidate property URIs. Use the domain and range
     columns to understand how the property connects different entity types.                   property       direction       example_neighbors

                                                                                               example_neighbors_labels

      INPUT SCHEMA                                                                            Relations (URIs)
     search_term     string OPT                                                                property       direction       example_neighbors

     The concept, keyword, or property name to search for. Utilizes semantic                   example_neighbors_labels
     search to find relevant matches.
     limit     number OPT
     Maximum number of results to return (default: 10).                                  Figure 11: KGVoyager tool specification: exploration
      OUTPUT FORMAT                                                                      tools.
      ▤ TABLE WITH COLUMNS:
      property_uri        label      aliases   domain     range    count     score

Figure 10: KGVoyager tool specification: search tools.

<!-- page 16 -->

    EXECUTION

              Execute Query                               execute_query(query)

     Executes a SPARQL query against the Knowledge Graph and returns the
     results.
     Purpose: Serves a dual role: running the final query to obtain the answer,
     and providing iterative feedback throughout reasoning. Use it to test
     intermediate query drafts and diagnose errors in partial queries.
     Use LIMIT to prevent fetching too much data for verification queries. After
     verification, the final query you return should be consistent with the
     question on whether LIMIT is needed.
     Output Format: Table with the query result columns, or an error message if
     the query fails.
      INPUT SCHEMA
     query    string REQ
     The valid SPARQL query string to execute.
      OUTPUT FORMAT
     Table with the query result columns, or an error message if the query fails.

    FINISH

              Answer Question                     answer(kg, sparql, answer)

     Provide your final SPARQL query and answer to the user question based on
     the query results. This function will stop the generation process.
      INPUT SCHEMA
     kg   string REQ
     The knowledge graph on which the final SPARQL query needs to be executed
     sparql    string REQ
     The final SPARQL query
     answer    string REQ
     The answer to the question based on the SPARQL query results
      OUTPUT FORMAT
     Stops the generation process and returns the final answer.

Figure 12: KGVoyager tool specification: execution
tools.
