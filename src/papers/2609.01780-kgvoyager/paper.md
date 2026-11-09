---
source: 2609.01780-kgvoyager.pdf
part: paper
converted: 2026-11-09
converter: pdftotext-layout
---

# KGVoyager: Knowledge Graph Agnostic Question Answering via Agentic Navigation · 正文

> 由 `pdftotext -layout` 从 PDF 直接转换，保留原页顺序；两栏页面的左右栏在同一行并排出现，逐行读即可，引用前回 PDF 核。
> 第 9 页只取左栏（Limitations / Ethical Considerations）；该页右栏已是参考文献，见 references.md。表格与图（Fig. 3/4、Table 3/4）横跨两栏，文本表会有版式噪声。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

                                         KGVoyager: Knowledge Graph Agnostic Question Answering via Agentic
                                                                   Navigation

                                                                              Essam Wisam and Chengkai Li
                                                                               University of Texas at Arlington
                                                                               {abdelghanye, cli}@uta.edu

                                                               Abstract                          classes, attributes, relationships, and constraints
                                                                                                 that help models produce semantically valid queries
                                             Knowledge Graph Question Answering
                                                                                                 [12, 24, 26]. In addition to ontologies, example
arXiv:2609.01780v2 [cs.IR] 15 Oct 2026

                                             (KGQA) over RDF graphs remains challenging
                                             in domain-specific settings, where formal           text–SPARQL pairs improve performance of such
                                             ontologies and curated text–SPARQL pairs            natural language interfaces by serving as in-context
                                             are often unavailable. We present KGVoyager,        examples or facilitating fine-tuning [39, 42, 34].
                                             a KG-agnostic agentic architecture that             This dual reliance on ontologies and text–query
                                             generates SPARQL queries from natural               pairs parallels SQL-based DBQA, where systems
                                             language questions by dynamically discovering       depend on the database schema and text–SQL pairs
                                             graph structure and semantics, requiring
                                                                                                 to ground query construction [43].
                                             only a query endpoint of the underlying
                                             graph. Using a think–act–observe loop with             However, the ontologies and example
                                             search, exploration, and execution tools,           text–SPARQL pairs on which these systems
                                             KGVoyager maps terms to graph Internation-          rely are not always available for domain-specific
                                             alized Resource Identifiers (IRIs), uncovers        knowledge graphs. We identify three distinct chal-
                                             structure, and refines queries through execution    lenges. (1) Ontology deficiency: Unlike relational
                                             feedback—all without pre-existing ontologies        databases, which require explicit schemas, RDF
                                             or examples. Unlike the prior state of the art,
                                                                                                 permits a flexible, schema-optional representation.
                                             KGVoyager requires only a lightweight class
                                             index which renders it applicable for far more      Many knowledge graphs lack a formal ontological
                                             real-world endpoints. Across four benchmarks,       structure. They may define entities, classes, and
                                             KGVoyager improves F1 by ∼4 points on               properties without specifying pivotal semantic
                                             average compared to the state of the art while      relationships such as class hierarchies, property
                                             cutting cost by ∼38% and runtime by ∼24%.           characteristics, and other semantic attributes.
                                                                                                 (2) Ontology opacity: Even when knowledge
                                         1   Introduction
                                                                                                 graphs do incorporate ontological structure, they
                                         RDF knowledge graphs (KGs) provide a robust             predominantly lack documentation that exposes or
                                         framework for representing complex, intercon-           explains such structure and related constraints [15].
                                         nected data across diverse domains [16, 35]. How-       (3) Example scarcity: Creating text–SPARQL
                                         ever, utilizing them effectively requires understand-   example pairs for new domain-specific knowledge
                                         ing graph-specific data models and technical query      graphs is both costly and challenging, requiring
                                         languages such as SPARQL [18, 13, 21, 1]. Natu-         human experts with deep domain knowledge,
                                         ral language interfaces that map user questions to      advanced SPARQL proficiency, and a thorough
                                         SPARQL queries lower this barrier and have driven       understanding of the underlying ontology. This
                                         significant research interest in knowledge graph        is corroborated by the pronounced scarcity of
                                         question answering (KGQA) [9, 14, 22, 42, 32, 19].      query examples for domain-specific knowledge
                                            LLM-based KGQA systhems have achieved                graphs [30, 27].
                                         state-of-the-art benchmark performance [9] over            These challenges hinder the development of ef-
                                         earlier machine-learning [6], deep-learning [41,        fective KGQA systems for domain-specific set-
                                         32, 4], template, and rule-based approaches [13].       tings. Most recent natural language to SPARQL
                                         These solutions fundamentally leverage ontolo-          systems [22, 42, 32, 19, 4, 10, 34, 39] avoid these
                                         gies and example text–query pairs for grounding         constraints by focusing on open-domain knowl-
                                         and guiding query generation. Ontologies encode         edge graphs such as Wikidata and DBpedia, which

<!-- page 2 -->

benefit from inherent knowledge in LLMs [14, 39],                 KGVoyager (classes) GRASP (entities)
                                                            KG    Count          Size Count      Size
curated text–SPARQL datasets [11, 36, 37], and              DBLP     35       2.7 KB 140.9M    21 GB
community ontology tooling [22, 42]. These assets           SOCKG    91       5.3 KB   7.1M 1.1 GB
are rarely available for arbitrary domain-specific      Table 1: Indexed items and on-disk size of KGVoyager’s
knowledge graphs.                                       class index vs. GRASP’s entity index for the DBLP and
   As ontologies may be unavailable or opaque and       SOCKG knowledge graphs.
example pairs scarce, we treat a SPARQL query           an index covering all entities in the graph can be
endpoint as the sole universally assumable resource.    retrieved from the endpoint. This assumption holds
Our system aims to enable natural language inter-       for only ∼21% of the tested OKN endpoints under
faces for arbitrary knowledge graphs given only         Jena and none under QLever. Other fundamental
query endpoint access. To achieve this goal, our        differences are detailed in Section 2. Even when
system must simulate the exploratory learning pro-      GRASP is given its full entity index, KGVoyager out-
cess a human expert would undertake when encoun-        performs it on average across four domain-specific
tering an unfamiliar knowledge graph. To this end,      benchmarks, with ∼4 points higher F1, ∼38%
we present KGVoyager, an agentic architecture that      lower cost, and ∼24% shorter runtime (Section 4).
uses a suite of KG-agnostic tools to dynamically           In summary, our key contributions are:
discover latent graph structure, semantics, and in-        • KGVoyager, an agentic architecture that lever-
stance data. KGVoyager then uses this discovered in-    ages a suite of KG-agnostic tools to generate
formation to generate SPARQL queries that answer        SPARQL queries that answer user questions with-
user questions. We design a set of searching, sam-      out relying on pre-existing ontologies or curated
pling, and navigation tools that enable systematic      example pairs.
exploration of arbitrary knowledge graphs. Using           • Evaluation of KGVoyager against the cur-
these tools within a think-act-observe loop [40],       rent state-of-the-art across diverse domain-specific
the agent identifies relevant classes and properties,   knowledge graphs, demonstrating superior perfor-
maps local graph structure, and validates query         mance in correctness, efficiency, and applicability.
drafts through execution feedback until it derives         • Open-source release of KGVoyager, enabling
an accurate SPARQL query.                               practitioners to deploy the system against any
   KGVoyager generalizes across endpoints by re-
                                                        SPARQL endpoint with minimal configuration.
lying on two assumptions. First, the knowledge          The codebase, benchmark queries, results, and
graph follows the W3C RDFS standard for defin-          demo recordings are available at https://anonym
ing types [7], so that class discovery and entity       ous.4open.science/r/nl2sparql2-C171.
search can be expressed as agentic tools that run
unchanged on any such endpoint. Second, a               2   Related Work
lightweight class index, containing the list of en-
tity types in the graph, can be retrieved from the      GRASP [38] is the prior work most similar to
endpoint with a single SPARQL query; individual         KGVoyager, employing an LLM agent with KG-
entities are then located on demand within the rel-     agnostic tools for zero-shot SPARQL generation
evant classes. Both assumptions hold broadly in         over arbitrary knowledge graphs. KGVoyager dif-
practice: in a scan of knowledge graph endpoints        fers in three respects: the scale of required index-
from the Open Knowledge Network (OKN) reg-              ing, the inference of property semantics, and the
istry [27], ∼96% of the scanned knowledge graphs        retrieval mechanism. First, GRASP indexes ev-
follow the RDFS typing standard (Appendix B),           ery entity, whereas KGVoyager indexes only classes,
and the class index can be built for ∼68% of the        which scale with the ontology rather than the data.
tested endpoints under the Apache Jena SPARQL           The class index is thus orders of magnitude smaller,
engine and ∼96% under the QLever SPARQL en-             as shown for two benchmark knowledge graphs
gine (Section 4.1).                                     (Table 1). The class index can also be built for far
   To the best of our knowledge, the only prior         more OKN endpoints (Section 4.1).
work sharing a similar endpoint-only, KG-agnostic          Second, GRASP differentiates properties using
objective is GRASP [38], which also targets zero-       ontological domain/range annotations, which are
shot SPARQL generation over arbitrary knowledge         not always present (the ontology-deficiency chal-
graphs. Unlike KGVoyager, which requires only an        lenge discussed in Section 1); KGVoyager infers
index of the graph’s classes, GRASP assumes that        them directly from data via dedicated exploration

<!-- page 3 -->

tools. Third, GRASP uses semantic and keyword           to discover latent graph structure, semantics, and
search as separate signals across its tools, whereas    instances to reflectively generate SPARQL queries
KGVoyager combines them jointly via hybrid re-          from natural language questions. KGVoyager relies
trieval, which has been shown to outperform either      on the minimal assumption that the target knowl-
signal alone in various applications [20, 31].          edge graph adheres to W3C RDFS standards for
   ToG [34] pursues KG-agnostic question answer-        class definitions—a convention adopted across al-
ing through an agentic LLM that traverses the           most all RDF knowledge graphs (Appendix B). Un-
knowledge graph hop-by-hop. Unlike KGVoyager,           der this assumption, search and exploration tools
which explores latent structure and semantics to        use KG-agnostic SPARQL queries and run un-
construct an executable SPARQL query, ToG tra-          changed across KGs.
verses instance-level data node-by-node to locate           Given a natural language question, KGVoyager
answers. The two systems differ in three respects.      formulates SPARQL generation as an iterative ex-
First, in access assumptions: adapting ToG to a         ploration problem. The agent operates in a think-
new knowledge graph requires downloading and lo-        act-observe loop [40], reasoning about what to do
cally deploying the entire graph and implementing       next, invoking a tool, and incorporating the result
a graph-specific Python traversal interface, which is   before deciding its next step. Its KG-agnostic tools
infeasible in endpoint-only settings; KGVoyager uses    are organized into three groups: (i) search tools,
a unified tool implementation that works across all     which retrieve candidate classes, node instances,
knowledge graphs that follow the RDFS typing            and properties from natural language cues; (ii) ex-
standard via standard SPARQL. Second, in ground-        ploration tools, which inspect how these candidates
ing: ToG assumes the presence of an initial set         are used and connected in the knowledge graph;
KG entities along with the question from which          and (iii) an execution tool, which runs candidate
exploration will begin; KGVoyager explicitly treats     SPARQL queries and returns feedback. The agent
class, property, and entity grounding as part of the    uses search to map question terms to classes, en-
endpoint-only task. Third, in reasoning efficiency:     tities, and properties, each identified by an IRI.
ToG’s search process grows proportionally with          It then uses exploration to fill gaps in how these
hop distance, the branching factor of intermediate      elements connect. Finally, it uses execution to vali-
neighborhoods, and the cardinality of candidate so-     date and refine query drafts until it determines that
lution nodes, whereas KGVoyager’s tool suite relies     a SPARQL query correctly answers the question.
on SPARQL queries that can express traversals over          Figure 1 summarizes the tool suite. Search
arbitrarily many hops in a single execution while       tools resolve classes, properties, and entities from
yielding results of any cardinality. Finally, ToG’s     natural-language cues. Exploration tools inspect
evaluation covers only open-domain knowledge            entity neighborhoods and property usage to expose
graphs, providing limited evidence of generaliza-       structure not immediately apparent from search
tion to domain-specific knowledge graphs.               results. execute_query validates partial or com-
   Other systems are tailored to a specific knowl-      plete query drafts. The complete KGVoyager system
edge graph or domain. Spinach [22] uses Wikidata-       prompt and tool specification are included in Ap-
specific tools and an in-context learning agent to      pendix G. We prompt the agent to generally fol-
simulate expert exploration for question answering      low a search, exploration, and execution sequence,
over Wikidata, while Expasy [12] presents a bioin-      mirroring the natural workflow of a human expert
formatics text-to-SPARQL system that mitigates          encountering an unfamiliar knowledge graph. Ap-
hallucinations via schema validation, but relies on     pendix D confirms that models typically follow this
curated text–query pairs and KG-specific schemas.       ordering. The agent submits the final query through
Their tight coupling to specific domains limits gen-    a dedicated answer tool to mark task completion.
eralization to arbitrary knowledge graphs without       Following GRASP [38], we also allow the agent to
substantial re-engineering, in contrast to the flexi-   terminate early via a cancel tool when generating a
bility of KGVoyager’s KG-agnostic architecture.         query is unfeasible for a given question under the
                                                        knowledge graph.

3   Methodology                                         3.1   Search Tools
KGVoyager is a KG-agnostic agentic reasoning ar-        Class Search. The search_all_classes tool accepts
chitecture equipped with dynamic exploration tools      a natural language search term and returns a ranked

<!-- page 4 -->

    KG VOYAGER TOOLS
    SEARCH

       🔍 "Model"                                                                     cgi:Model                            🔍 "discuss"
       cgi:Model                                           .252                                                           cgi:PaperMentions                        .042

                                                                  ✂    TaiESM          FIO-ESMv2           ACCESS-CM2
                                                                                                                          cgi:MethodSolves                         .037
       cgi:Method                                          .002
                                                                                          ···                                                                                 ✂

                                                                          🔎 filter: "TaiESM" → ✓
       cgi:Sim.Type                                        .002                                                           cgi:pubYear                              .000

                             CLASS SEARCH                                           INSTANCE LOOKUP                                      PROPERTY SEARCH
                            search_all_classes()                                   lookup_class_instances()                              search_all_properties()

    EXPLORATION                                                                                                         EXECUTION

                                                                               cgi:PaperMentions
                                                           Problem
     Method                                                                                                              SELECT ?meth ?innov WHERE {
               Me
                 tho

                                                                                                                         ?meth UsesModel ?m .
                                                  s
                                               lve
                    dUs

                                             So

                                                                      Domain          Range                Count         ?m cgi:name "TaiESM" .
                       es

                                               Use
                                                                                                                         ?meth HasInnovation ?innov }
                             TaiESM               dIn

                                                              Task    Paper        Experiment               41
                                               Has
                     as

                                                  Res
                 perH

                                                     ult

                                                                      Paper          Project                28
               Pa

     Paper
                                                                                                                                 ?meth                         ?innov
                                                            Result    Paper         Activity                19
                                                                                                                           Deep Convection            New trigger function…

              ENTITY RELATIONS EXPLORATION                                PROPERTY USAGE EXPLORATION                                       EXECUTE QUERY
                       explore_entity_relations()                               explore_property_usage()
                                                                                                                                             execute_query()

Figure 1: The KGVoyager tool suite. Examples are simplified from runs on the Climate Models knowledge graph.

list of classes whose IRIs or labels are semanti-                                                 Searches using abbreviations, alternative spellings,
cally or lexically related to the term. Each result                                               or overly specific names may return no results be-
includes the class label, aliases, and instance count.                                            cause matching relies on lexical SPARQL string
On first invocation, the tool fetches a lightweight                                               filters. To handle such cases, the tool supports a
class index via SPARQL and caches it locally for                                                  broader fallback_term to retrieve a larger candidate
all subsequent searches. To retrieve and rank re-                                                 set when the exact_term search fails. These can-
sults, we employ a hybrid approach that combines                                                  didates are then filtered by the semantic similarity
dense vector similarity with sparse BM25 lexical                                                  of their labels to the exact_term. Separately, for
scoring via reciprocal rank fusion [8], which has                                                 knowledge graphs that store useful names or identi-
been shown to consistently outperform either signal                                               fiers in literal-valued attributes rather than standard
alone in various applications [20, 31].                                                           labels, the lookup_class_instances tool also sup-
   Each result is returned with a relevance score.                                                ports an all_attributes mode that further extends
To prevent low-quality candidates from polluting                                                  the search to all literal values of class instances, at
the agent’s context, a phenomenon known as con-                                                   the cost of slower execution. These class-scoped
text rot [17], we apply an adaptive filtering mech-                                               mechanisms enable precise entity resolution with-
anism. This mechanism prunes candidates whose                                                     out an exhaustive entity index over the entire graph,
relevance score relative to the top-ranked result                                                 which is infeasible for most endpoints.
falls below a ratio δ, while always retaining the top                                                Property Search. The search_all_properties
three candidates. We manually tune this hyperpa-                                                  tool searches for properties using an approach sim-
rameter and set δ = 0.125.                                                                        ilar to that used for class search. Given a search
   Instance Lookup. The lookup_class_instances                                                    term, it returns a ranked list of property IRIs along
tool retrieves instances of a given class, option-                                                with labels, aliases, usage counts as well as do-
ally filtered by an exact_term. After identifying                                                 mains and ranges, if available. As with class search,
a candidate class IRI via search_all_classes, the                                                 the property index is fetched and cached on first
agent uses this tool to verify that the class con-                                                use by enumerating all distinct predicates from the
tains the expected content or locate entities men-                                                endpoint. Subsequent searches apply the hybrid
tioned in the question. The default lookup matches                                                retrieval and adaptive filtering methods used for
the exact_term against instance labels and IRIs.                                                  class search to the locally cached property index.

<!-- page 5 -->

3.2   Exploration Tools                                                                                  QUESTION
                                                           Count the number of papers that Jake Grozdanovski has published in International
                                                                          Conference on Software and Data Technologies.
While the search tools resolve natural language
                                                            ① SEARCH
terms to candidate class, property, or instance IRIs,
they do not reveal how those IRIs are structurally          1      search_all_classes( "author" )

embedded and connected in the graph. To under-                  psc:AuthorSelfCitation                                                                    0.0249

                                                                ds:AuthorSignature                                                                        0.0066
stand the interaction of properties and the neigh-              ds:Creator                                                                               0.0008

borhoods of entities, the agent requires tools that
                                                            2      search_all_classes( "paper" )
inspect the graph directly.
                                                                psc:JournalSelfCitation                                                                   0.0004

   Property Usage Exploration. Many knowl-                      ds:Publication                                                                           0.0003

                                                                psc:Citation                                                                              0.0001

edge graphs lack explicit or accurate domain and
range annotations, leading to ambiguity in prop-            3      search_all_classes( "conference" )

                                                                ds:Conference                                                                            0.4207
erty interpretation. The explore_property_usage                 psc:Citation                                                                              0.0002

tool bridges this gap by examining how a property               psc:AuthorSelfCitation                                                                    0.0001

is actually used. Given a property IRI, it samples          4      search_all_properties( "author" )

triples with that property and aggregates the subject           ds:authoredBy (Publication -> Creator)                                                   0.0010

and object classes involved, along with represen-               ds:creatorNote (Creator -> string)

                                                                ds:publishedInBook (Publication -> string)
                                                                                                                                                          0.0009

                                                                                                                                                          0.0008

tative instances and their labels. This allows the
                                                            5      search_all_properties( "published" )
agent to verify that a candidate property empiri-
                                                                ds:publishedInSeriesVolume (Publication -> string)                                        0.4299

cally connects the kinds of entities expected by the            ds:publishedInBook (Publication -> string)                                                0.4264

                                                                ds:publishedAsPartOf (Publication -> Publication)
question, before committing it to the query as well             ds:publishedInJournal (Publication -> string)
                                                                                                                                                          0.3110

                                                                                                                                                          0.2815

as to disambiguate properties with similar labels.
                                                            6      lookup_class_instances( ds:Conference, "Software and Data Technologies" )
For instance, while a property labeled “located in”
connects organizations and companies to cities, a                 dsc:icsoft       International Conference on Software and Data Technologies (ICSOFT)
different property “location” may connect events
to venues.                                                  7      lookup_class_instances( ds:Creator, "Jake Grozdanovski" )

   Entity Relation Exploration. The tool ex-                      dp2:9368       Jake Grozdanovski

plore_entity_relations inspects the local neighbor-
hood of a given entity. From an entity IRI, it re-          ② EXPLORE
trieves the incoming and outgoing properties along
with example subjects or objects reached through            8      explore_entity_relations( dsc:icsoft )

each, including labels when available. This helps               Property

                                                                rdfs:label
                                                                                             Dir

                                                                                             out
                                                                                                       Example neighbor

                                                                                                       International Conference on Software and Data
                                                                                                       Technologies (ICSOFT)
understand how the entity is embedded in the graph,             ds:primaryStreamTitle        out       International Conference on Software and Data
                                                                                                       Technologies (ICSOFT)

particularly when property search has not surfaced              ds:streamTitle               out       International Conference on Software and Data
                                                                                                       Technologies (ICSOFT)
                                                                ds:publishedInStream         in        drci:0001BR24; drci:0001CM0T21; ...
the property needed for the question. Given a lit-
eral instead, the tool returns the entities with that       9      search_all_properties( "publishedInStream" )

value and the corresponding data properties.                    ds:publishedInStream (Publication -> Stream)                                             0.9178

                                                                ds:publishedInSeriesVolume (Publication -> string)                                        0.0072

                                                                ds:publishedInSeries (Publication -> string)                                              0.0043

3.3   Execution Tools
                                                            ③ EXECUTION
The execute_query tool runs a SPARQL query                  10     execute_query( query )

against the endpoint and returns the results. It
                                                            PREFIX ds: <https://dblp.org/rdf/schema#>

serves a dual role: providing execution-based feed-         PREFIX dsc: <https://dblp.org/streams/conf/>
                                                            PREFIX dp2: <https://dblp.org/pid/297/>

back from intermediate queries throughout the rea-          SELECT (COUNT(DISTINCT ?paper) AS ?count) WHERE {
                                                                 ?paper a ds:Publication ;
soning process, and executing the final query to                       ds:authoredBy dp2:9368 ;
                                                                       ds:publishedInStream dsc:icsoft .

obtain the answer. The agent can run intermediate           }

queries to test hypotheses about graph structure,          Results count = 1                                                                             1 row · 0.46s

verify that queries produce non-empty results, and
diagnose errors in partial queries. This iterative      Figure 2: A complete KGVoyager example. Numbered
                                                        blocks indicate tool calls in the order they were invoked
feedback is central to the agent’s ability to self-
                                                        by the agent. Abbreviations such as ‘ds:’ denote names-
correct and converge on accurate queries.               pace prefixes used in the underlying graph.

<!-- page 6 -->

3.4    End-to-End Example                                                             Jena       QLever
                                                       Knowledge Graph            Entity Class Entity Class
 Figure 2 shows KGVoyager resolving the question       biobricks-aopwiki            ✓      ✓    ×      ✓
                                                       biobricks-ice                ×      ×    ×      ✓
“Count the number of papers that Jake Grozdanovski     biobricks-mesh               ×      ×    ×      ✓
 has published in the International Conference on      biobricks-pubchem-
                                                                                    ×      ✓    ×      ✓
 Software and Data Technologies” in ten tool calls,    annotations
                                                       biobricks-tox21              ✓      ✓    ×      ✓
 over the DBLP knowledge graph. During Search,         biobricks-toxcast            ×      ×    ×      ✓
 the agent decomposes the question into seman-         biohealth                    ×      ✓    ×      ✓
 tic search terms and resolves them to KG ele-         climatemodelskg              ✓      ✓    ×      ✓
                                                       dream-kg                     ✓      ✓    ×      ✓
 ments. The agent infers author, implied by “Jake      fio-kg                       ×      ×    ×      ✓
 Grozdanovski has published” though not a lit-         gene-expression-atlas-okn    ×      ✓    ×      ✓
 eral query keyword, and maps it to ds:Creator         geoconnex                    ×      ✓    ×      ✓
                                                       hydrology-kg                 Â      ✓    ×      ✓
 (step 1), then maps paper to ds:Publication           nasa-gesdisc-kg              ×      ✓    ×      ✓
 (step 2) and conference to ds:Conference (step 3).    nde                          ×      ✓    ×      ✓
 It reuses author to surface the authorship prop-      neighborhood-information-kg ✓       ✓    ×      ✓
                                                       rural-kg                     ✓      ✓    ×      ✓
 erty ds:authoredBy (step 4), while a search on        sawgraph                     ×      ×    ×      ✓
“published” (step 5) returns only journal/book prop-   scales                       ×      ✓    ×      ✓
 erties, leaving the property linking publications     secure-chain-kg              ×      ✓    ×      ✓
                                                       semopenalex                  ×      ×    ×      ✓
 to conference venues unresolved. The agent then       sockg                        ×      ✓    ×      ✓
 grounds the two named entities: the conference        spatial-kg                   Â     Â     ×      ✓
 name to dsc:icsoft (step 6) and the person name       spoke-genelab                ×      ✓    ×      ✓
                                                       sud-okn                      ×      ×    ×      ✓
 to dp2:9368 (step 7). In the Explore phase, the       ubergraph                    ×      ✓    ×      ✓
 agent inspects dsc:icsoft directly, which reveals     uf-okn                       Â      ✓    ×      ✓
 the incoming relation ds:publishedInStream.           wikidata                     ×      ×    ×      Â
                                                       Success Rate               21.4% 67.9% 0% 96.4%
 A targeted follow-up search confirms it is the
                                                       Table 2: Indexing feasibility (✓: Success, ×: Failed,
 Publication → Stream property required for the        Â: Timeout) across 28 KG SPARQL endpoints from
 publication-conference relationship. In Execu-        okn.us under two settings.
 tion, the agent has fully resolved the triple
 pattern ?paper ds:authoredBy dp2:9368;                (27/28), while entity indexing failed on all 28, with
 ds:publishedInStream dsc:icsoft, executes             failures manifesting as server memory crashes—an
 the COUNT query, and obtains the answer 1.            interpretable outcome given the size of entity in-
                                                       dices. These results show that the feasibility of
4     Experiments                                      entity-level indexing is highly sensitive to the un-
                                                       derlying SPARQL engine and knowledge graph.
4.1    Feasibility Analysis
We assessed the feasibility of GRASP’s entity in-      4.2   Benchmarks and Models
dex and KGVoyager’s class index by attempting to       We evaluated question answering on four domain-
build each over 28 KG SPARQL endpoints from            specific benchmarks: Climate Models KG [2]
okn.us [27], a catalog of graphs developed under       (108 questions on climate-science literature),
the U.S. NSF Proto-OKN initiative. For GRASP,          SOCKG [33] (98 questions on soil-carbon mod-
we used its official entity index query. We com-       eling), DREAM-KG (88 questions on local govern-
pared two settings: (i) the individual Apache Jena     ment service data), and DBLP-QuAD (100 ques-
endpoints of okn.us and (ii) its unified federated     tions on scholarly metadata). The first three are as-
QLever endpoint [5], which okn.us plans to adopt       sociated with okn.us [27], with question–SPARQL
in place of Jena for performance reasons.              pairs supplied by the respective KG developers.
   Table 2 reports the results. Under Jena, class      DBLP-QuAD is a public question–SPARQL bench-
indexing succeeded for ∼68% of endpoints while         mark; we randomly sampled 100 questions from
entity indexing succeeded for only ∼21%, con-          its test split [3]. For brevity, we refer to each bench-
firming the impracticality of GRASP’s entity-index     mark by the name of its knowledge graph. The
requirement; the Jena entity-indexing failures re-     question–SPARQL pairs used in our evaluation are
turned opaque server errors with no actionable diag-   available through our repository and in the supple-
nostic information. The gap widens under QLever:       mentary data file accompanying this manuscript.
class indexing succeeded for ∼96% of endpoints            Although Section 4.1 shows that constructing

<!-- page 7 -->

                                 F1 (%)              Cost ($)                Iterations             Time (s)
        Benchmark         KGVoyager GRASP ∆ KGVoyager GRASP          ∆ KGVoyager GRASP ∆ KGVoyager GRASP            ∆
        Climate Models KG      69.8     67.2 +2.6 2.66     4.57 −41.8%      19.6      23.1 −3.5  75.1   119.7 −37.3%
        SOCKG                  71.3     68.9 +2.4 2.20     4.00 −45.0%      19.3      25.0 −5.7  57.0   108.6 −47.5%
        DREAM-KG               49.7     46.9 +2.8 3.06     5.06 −39.5%      24.2      30.5 −6.3  55.9     92.8 −39.8%
        DBLP                   67.5     60.8 +6.7 1.79     2.13 −16.0%      15.1      15.1 0.0  154.2   128.7 +19.8%
        Average                64.6     60.9 +3.7 2.43     3.94 −38.3%      19.6      23.4 −3.8  85.6   112.4 −23.8%
Table 3: Performance by benchmark, averaged across four backbone models. GRASP is evaluated under its best-case
setting (entity index available).

             Climate Models KG                                             SOCKG                                             DREAM-KG                                                DBLP

                      82.8                           100                   79.8                           100                                                 100
 100                              75.0      79.6                                                 77.9                                                                              69.4
                   84.6                                                 85.4           73.3                                                                                                    62.3
                               74.3      79.2                                                 79.6                             53.0                                                                      66.4
                                                                                    73.1                                                                                44.8    75.2        71.9
  75                                                  75                                                   75               67.5           53.7      54.5      75                                     64.4
                                                                                                                                                                     58.5
           31.4                                                 44.4                                                                    54.4      55.8
        41.2                                                 46.9                                                                                              50
  50                                                  50                                                   50       26.3
                                                                                                                 21.0
  25                                                  25                                                   25                                                  25

   0                                                   0                                                    0                                                   0
        $0.12                                               $0.098                                               $0.11                                               $0.13
           $0.14                                                $0.12                                               $0.13                                               $0.14
                                                    $1.58                                                $2.01                                               $0.81
$1.92

                                                    $3.17                                                $4.02                                               $1.63
$3.84
                                         $3.23                                                $2.62      $6.02                                               $2.44                                    $1.99
$5.76                                               $4.75                                                                                         $3.62
                                            $4.51                                                $4.17                                                                                                   $2.19
                              $4.34                                                                                                                  $5.52
                                                                        $2.52                                               $2.82                                               $1.87
                                                                                                         $8.03                                               $3.25
$7.68                            $5.94              $6.33                  $5.38                                               $6.54                                               $2.96
                   $2.95                                                           $3.56                                               $5.71                                               $3.19
                      $7.68                                                           $6.33                                               $8.03                                               $3.25

        GPT-OSS     GPT-6     Nemotron 3  Muse              GPT-OSS      GPT-6     Nemotron 3  Muse              GPT-OSS     GPT-6     Nemotron 3  Muse              GPT-OSS     GPT-6     Nemotron 3  Muse
         120B        Sol        Ultra Glimmer 30B            120B         Sol        Ultra Glimmer 30B            120B        Sol        Ultra Glimmer 30B            120B        Sol        Ultra Glimmer 30B

                                                             KG Voyager F1              GRASP F1           KG Voyager cost               GRASP cost

Figure 3: Per-model F1 and monetary cost by benchmark. F1 bars extend above the baseline, cost (hatched) below;
error bars indicate run-to-run standard deviation across three independent runs.

GRASP’s entity index from endpoint access is in-                                                           open-weight mixture-of-experts reasoning model
feasible for most knowledge graphs, we evaluate                                                            with 117B total and 5.1B active parameters, built
GRASP under its best-case conditions by provid-                                                            with tool calling support [28]. Nemotron 3 Ul-
ing the required entity index. We obtained this                                                            tra (NVIDIA, 2026) is an open hybrid Mamba–
index through one of three routes: (i) building it                                                         Transformer mixture-of-experts model with 550B
directly on relatively small KGs whose Jena end-                                                           total and 55B active parameters, targeting reason-
point can serve the entity-index query, as for Cli-                                                        ing and agentic workflows [25]. Muse Glimmer
mate Models KG and DREAM-KG; (ii) locally                                                                  30B (Meta, 2026) is an open 30B-parameter dense
redeploying the knowledge graph and extracting                                                             model distilled from Muse Spark for local agentic
the index from the deployment, as for SOCKG,                                                               tasks with failure recovery [23]. The three open
whose okn.us endpoint fails entity index creation                                                          models were accessed via OpenRouter. Full imple-
(Section 4.1); or (iii) using a pre-built index, as                                                        mentation hyperparameters are in Appendix A.
provided by GRASP’s authors for DBLP-QuAD.
   KGVoyager assumes only endpoint access. For                                                             4.3        QA Performance
SOCKG, the KG’s authors provided the ontology                                                              We compared KGVoyager against the prior state of
as a Turtle file, which we use to construct an ad-                                                         the art, GRASP [38], on the benchmarks and mod-
ditional Grep Ontology baseline. This baseline is                                                          els above. For each combination of method, bench-
built on the Unix grep command, which coding                                                               mark and model, we average three independent
agents commonly use to search code. It uses the                                                            runs and report F1, monetary cost, agent iterations,
same backbone models with only two tools: grep                                                             and wall-clock time. Following GRASP, we adopt
over the ontology file and SPARQL query execu-                                                             the row-major F1 metric of Spinach [22].
tion. KGVoyager uses its standard tool suite and is                                                           Table 3 reports results averaged across runs
not given the ontology file. This comparison tests                                                         and models; Figure 3 shows per-model results.
whether KGVoyager, using only endpoint access, can                                                         KGVoyager improves F1 on all four benchmarks,
outperform a baseline given the full ontology.                                                             with gains ranging from 2.4 percentage points on
   We ran our experiments on these benchmarks                                                              SOCKG to 6.7 points on DBLP. It also reduces cost
with four backbone models spanning closed and                                                              on every benchmark and requires fewer agent itera-
open systems of varying size and agentic capability.                                                       tions on all benchmarks except DBLP, where the
GPT-6 Sol (OpenAI, 2026) is a cost-efficient closed                                                        two systems tie. Runtime is lower by 37–48% on
model built for complex coding and agentic work-                                                           three benchmarks; DBLP is the exception (19.8%
flows [29]. GPT-OSS-120B (OpenAI, 2025) is an                                                              higher) because its template-based questions fo-

<!-- page 8 -->

                                             SOCKG                                                             F1 (%)             Cost ($)         Iter.
                                          82.5
                                                                                  Model, benchmark           Full        Abl.    Full Abl.      Full Abl.
      100                                                 72.9            70.1
                                  85.4
                                                  73.1            79.6             Entity-relation exploration (w/o explore_entity_relations)
      75               27.3
      50
              46.9                                                                GPT-OSS, SOCKG         46.9±.6 38.3±1.1 .098 .098             15.9   15.8
      25                                                                          GPT-6 Sol, SOCKG       85.4±.8      83.9±.6 2.52 2.74         10.7   11.4
       0                                                                          GPT-OSS, DBLP         58.5±5.3 55.1±1.3 .128 .081             10.8   12.5
              $0.098
  $1.42                $0.085
                                                                                   Property-usage exploration (w/o explore_property_usage)
  $2.85

  $4.27                                                           $2.62           Nemotron 3, SOCKG 75.5±2.0 74.8±3.3 4.46 5.09                 20.9   22.4
                                  $2.52                                   $3.52
  $5.69                                   $4.53                                   GPT-OSS, Climate     33.9±3.8 21.4±3.7 .116 .094              16.6   14.7
                                                  $3.56
                                                          $5.69
                                                                                  Muse 30B, SOCKG 79.9±1.0 75.7±1.3 2.72 2.94                   28.5   31.3
                GPT-OSS              GPT-6        Nemotron 3          Muse
                 120B                 Sol           Ultra         Glimmer 30B
                                                                                   Hybrid retrieval (keyword-only instead of hybrid)
                                                                                  GPT-OSS, Climate      41.2±7.7 36.3±2.1 .122          .115    16.1   18.6
                           KG Voyager F1          KG Voyager cost                 GPT-OSS, SOCKG         46.9±.6 20.4±2.3 .098          .094    15.9   19.7
                           Grep Ontology F1       Grep Ontology cost
                                                                                  Muse 30B, Climate 79.2±1.8         78.1±.9 3.23       3.86    30.7   33.9
Figure 4: Per-model F1 (top) and monetary cost                                    GPT-6 Sol, DREAM 67.5±3.0 65.7±1.2 2.82               3.13    12.8   13.6

(hatched, bottom) of KGVoyager and the Grep Ontology                              Table 4: Ablation study (Abl. = component removed).
baseline on SOCKG; error bars show standard deviation                             F1 is mean ± std. over three independent runs; cost and
over three runs.                                                                  iterations are means.

cus heavily on specific entity instances (e.g., paper                             ing explore_entity_relations reduces F1 in all
and author names), which GRASP resolves with                                      three pairs (by 1.5 to 8.6 points). Removing ex-
a single lookup in its pre-supplied entity index,                                 plore_property_usage lowers F1 by 12.5 points on
whereas KGVoyager must first identify the relevant                                Climate Models KG with GPT-OSS-120B and 4.2
class and then search within it. Overall, KGVoyager                               points on SOCKG with Muse Glimmer 30B, while
also makes fewer tool calls and SPARQL execu-                                     the 0.7-point drop for Nemotron 3 Ultra on SOCKG
tions per question (Appendix E). We also verify                                   falls within run-to-run variability. Only GPT-OSS-
that the benchmarks are nontrivial and analyze per-                               120B on Climate Models KG pays more cost and
formance by query complexity (Appendix C). Fi-                                    iterations with the tool; for the other two pairs, the
nally, we categorize KGVoyager’s failure cases in a                               tool lowers both. Both the full and ablated variants
detailed failure analysis (Appendix F).                                           hide the property domain/range search tool, be-
   Beyond GRASP, we compared KGVoyager against                                    cause, per the ontology deficiency challenge (Sec-
the Grep Ontology baseline on SOCKG (Sec-                                         tion 1), we assume such annotations are generally
tion 4.2). The results in Figure 4 show that, despite                             absent, even though some of these KGs may have
having direct access to the ontology, the baseline                                them. This shows that property-usage exploration
trails KGVoyager by 8.1 points of F1 on average                                   recovers useful semantic information directly from
(63.2% vs. 71.3%), while KGVoyager also reduces                                   graph data when ontological annotations are un-
cost by 36.4%. We also observed an 18.7% de-                                      available. Finally, hybrid retrieval improves F1
crease in runtime. The largest F1 gains are ob-                                   over keyword-only search in all four pairs (+1.1
served for the two smaller models, GPT-OSS-120B                                   to +26.5 points) and reduces iterations in all four,
(+19.6 points) and Muse Glimmer 30B (+9.5). We                                    showing that combining semantic and lexical sig-
attribute these differences to context rot [17], as                               nals improves search robustness.
repeated grep calls return long outputs that accu-
mulate in the context, which raises token cost and
                                                                                  5     Conclusion
tends to degrade smaller models more.                                             We presented KGVoyager, a KG-agnostic frame-
                                                                                  work that answers natural language questions
4.4         Ablation Study                                                        over arbitrary RDF knowledge graphs given only
We ablate three components of KGVoyager: entity-                                  SPARQL endpoints. Our feasibility study shows
relation and property-usage exploration, which we                                 that KGVoyager’s lightweight class index succeeds
remove, and hybrid retrieval, which we replace                                    on ∼96% of okn.us endpoints under QLever,
with keyword-only retrieval in class and property                                 compared to 0% for the entity index required by
search. Search and execution tools are always re-                                 GRASP. Across four domain-specific benchmarks
tained, as an endpoint-only system cannot ground                                  and four backbone models, KGVoyager improves F1
terms or test queries without them. Each compo-                                   over GRASP while generally reducing cost, run-
nent is evaluated on at least two models and two                                  time, and iterations, showing that endpoint-only
benchmarks.                                                                       KGQA is viable where curated resources are un-
   Table 4 reports the ablation results. Remov-                                   available.

<!-- page 9 -->

 Limitations
 Although KGVoyager requires no KG-specific ontol-
 ogy, text–query examples, or graph-specific tools
 and assumes that the knowledge graph follows
 the RDF standard for defining types (rdf:type),
 which is broadly adopted in practice (Appendix B),
 knowledge graphs that use their own typing con-
 ventions, such as Wikidata, are not directly sup-
 ported. Supporting them would require adapter
 tools, which we leave for future work.
   A second limitation is data availability: domain-
 specific text–SPARQL benchmarks remain scarce,
 and despite reaching out to many KG authors and
 maintainers, we could not gather larger datasets.
 More public domain-specific KGQA benchmarks
 are needed and we envision that automated bench-
 mark generation could be promising.

 Ethical Considerations
 All knowledge graphs endpoints and benchmarks
 used in this work are publicly available (see links
 in our repository 1 ), and no private or personal data
 was collected or processed in any part of our ex-
 periments. We use existing artifacts only for their
 intended research and benchmarking purposes. Re-
 leased artifacts are intended for research, evalua-
 tion, and reproducibility, with third-party resources
 remaining subject to their original terms.
    Users of KGVoyager should be aware that, like
 any LLM-based system, it may generate syntacti-
 cally valid SPARQL queries that are nonetheless
 semantically incorrect. In domains where query
 results inform decisions, such as scientific or pol-
 icy contexts, outputs should be verified rather than
 trusted uncritically.
    Finally, LLM inference carries an environmental
 cost. We note, however, that KGVoyager reduces
 monetary cost by ∼38% and wall-clock runtime by
 ∼24% relative to the prior state-of-the-art system,
 partially mitigating this concern.
