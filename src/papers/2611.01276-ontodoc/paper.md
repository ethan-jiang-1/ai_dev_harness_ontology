---
source: 2611.01276-ontodoc.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# OntoDoc: Automatically Generating Ontology Resource Descriptions · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

**OntoDoc: Automatically Generating Ontology Resource Descriptions** 

Juan Guajardo Gutierrez, Mike Tran, Nasim Shirvani Mahdavi, Chengkai Li 

University of Texas at Arlington, Arlington TX 76013, US 

**Abstract.** Knowledge graphs and ontologies form the backbone of structured, machine-readable knowledge representation, yet ontology terms often lack natural language descriptions, limiting their accessibility and reuse. Existing ontology verbalization approaches tend to rely on rulebased or template-driven techniques that operate on strict, formal schema axioms, resulting in rigid verbalizations that fail to convey richer contextual semantics. We present OntoDoc, a multi-agent framework for automatically generating natural language descriptions for any Internationalized Resource Identifier (IRI) within a SPARQL endpoint or RDF file. OntoDoc operates through a four-stage pipeline: (1) a Database Context agent that adaptively explores the knowledge graph via SPARQL to collect semantically informative triples about the target IRI; (2) a Web Context agent that retrieves and re-ranks encyclopedic background knowledge from Wikipedia and the open web; (3) an Assumption Generation agent that synthesizes both contexts into a structured, evidencegrounded list of intermediate assumptions; and (4) a Description Generation agent that produces the final natural language description from the grounded assumptions. We evaluate OntoDoc on three knowledge graphs spanning biomedical, agricultural, and cross-domain settings, using both automatic scoring via Large Language Models (LLMs) and human evaluation with 11 annotators. OntoDoc consistently matches or exceeds a naive LLM baseline and a template-based ontology verbalizer in accuracy. Furthermore, it vastly outperforms both baselines in the completeness of the generated descriptions, delivering an average 12% improvement in completeness over the naive baseline across all domains, and improving completeness scores by as much as 2.8 points on a 5-point scale relative to the ontology verbalizer. 

**Keywords:** Ontology verbalization · Knowledge graph documentation · Large language models · LLM agentic framework. 

# **1 Introduction** 

Knowledge graphs have become a foundational framework for representing structured information in scientific, business and governmental applications [9,10], as evidenced by initiatives such as the Proto-OKN program of the U.S. National Science Foundation [16]. Yet the practical utility of such semantic richness is contingent upon users’ ability to comprehend and reuse the data. The semantics of


<!-- page 2 -->

2 J. Guajardo Gutierrez et al. 

a knowledge graph are largely defined by its ontology, which specifies the classes, properties, and relationships used to model the domain. In a typical knowledge graph, the ontology provides the intensional vocabulary, while instance data populates that vocabulary. Because the ontology defines the meaning of every term that appears in the data, it is the primary bottleneck for data comprehension. Users therefore tend to rely on ontology annotations such as `rdfs:comment` [3] to understand what each term means and how it should be used. 

However, in practice, a large fraction of ontology terms carry no humanreadable documentation, a problem visible across many publicly available SPARQL endpoints, where `rdfs:comment` or equivalent annotations are frequently missing. This leaves users and downstream applications without any guidance about the intended meaning or usage of key graph concepts. The standard remedy, where a knowledge graph maintainer or domain expert inspects the graph, examines representative data, and writes a short description for each term, is not scalable. Large knowledge graphs can contain hundreds of distinct classes and properties [25,13], and the expertise required to describe them accurately is often concentrated in a small group of contributors, making systematic manual annotation infeasible. As a result, many knowledge graphs are deployed with incomplete documentation, hindering discovery, integration, and reuse. 

Automatically generating ontology descriptions is therefore an important and practical problem. Existing approaches, however, remain limited. Traditional ontology verbalization systems primarily rely on schema-level axioms and handcrafted linguistic templates to produce descriptions from formal ontology constructs [11,22,23,5,18,1]. While effective for highly structured ontologies with rich logical axiomatization, these methods often generate rigid or overly generic descriptions and struggle when applied to knowledge graphs whose semantics are expressed implicitly through instance data rather than explicit ontology axioms. More recent approaches integrate Large Language Models (LLMs) to improve textual fluency [27]; however, they largely act as semantic translators of existing structure and remain strictly bounded by explicit schema axioms. Conversely, a natural first instinct is to directly prompt an LLM with raw graph triples and ask it to explain the target term. In practice, however, such naive prompting often yields incomplete descriptions because the semantics of ontology terms are rarely recoverable from a single local graph neighborhood. 

To address these challenges, we present OntoDoc, an agentic multi-stage system for automatic ontology description generation. OntoDoc combines adaptive SPARQL-based graph exploration with external web retrieval and an intermediate reasoning stage that synthesizes evidence into structured assumptions before description generation. Rather than relying solely on schema axioms or fixed graph queries, OntoDoc actively explores the knowledge graph to gather semantically informative evidence, supplements sparse graph context with external encyclopedic knowledge, and grounds the final description in explicitly reasoned assumptions derived from both sources. 

We evaluate OntoDoc on three diverse knowledge graphs spanning biomedical, agricultural, and open-domain data. Our evaluation includes both LLM-


<!-- page 3 -->

OntoDoc: Automatically Generating Ontology Resource Descriptions 3 

based and human assessment using four quality dimensions: accuracy, clarity, completeness, and cruciality. Experimental results show that OntoDoc consistently produces more complete and robust descriptions, improving completeness scores by up to 0.6 points on a 5-point Likert scale over the closest baseline while maintaining competitive accuracy and clarity across all domains. 

The main contributions of this work are as follows: 

- We formalize the ontology description generation task for heterogeneous knowledge graphs and define a multi-dimensional evaluation framework grounded in `rdfs:comment` quality criteria. 

- We propose OntoDoc, an agentic multi-stage pipeline that combines adaptive graph exploration, external web retrieval, structured assumption generation, and LLM-based description synthesis. 

- We introduce an intermediate assumption generation stage that improves factual grounding and reduces noise before final description generation. 

- We evaluate OntoDoc across three real-world knowledge graphs and show improvements over existing baselines. 

- All code used to produce this work is available in our anonymous GitHub repository at https://anonymous.4open.science/r/ontodoc/. 

# **2 Related Work** 

**Ontology verbalization.** A substantial body of research has investigated OWL [15] ontology verbalization [11,22,23,5,18,1]. These approaches aim to transform formal OWL axioms into human-readable text, typically focusing on ontology classes or individuals. Most existing methods assume the presence of a well-defined schema graph and operate exclusively on the logical axioms expressed in OWL, rather than considering instance data or external context. Furthermore, they predominantly rely on pre-LLM techniques, including rule-based systems, logical axiom patterning, and Controlled Natural Language (CNL) [12] generation. While structurally precise, such approaches tend to produce rigid descriptions that closely mirror the formal, logical structure of the axioms (e.g., “Class _A_ is a type of Class _B_ and is distinct from Class _C_ )”, and fail to convey the intuitive real-world meaning of a concept. In contrast, OntoDoc generates descriptions grounded in both schema and instance data, and enriched with external knowledge, to produce more fluent and contextually rich explanations. 

Zaitoun et al. [27] introduced an LLM-assisted verbalizer that converts OWL statements from existing ontologies into natural language, with the goal of generating text-to-OWL sentence pairs for fine-tuning ontology learning models. Their system uses a three-stage pipeline: initialization, CNL generation from OWL axioms, and an LLM-based paraphrasing step to improve fluency. The approach has the fundamental limitation of being strictly bounded by the explicit axioms present in a local ontology file. The system functions as a semantic translator of existing schema structure and cannot incorporate instance-level evidence from a live knowledge graph or enrich descriptions with external world knowledge. In contrast, OntoDoc is not limited to OWL ontologies nor constrained by


<!-- page 4 -->

4 J. Guajardo Gutierrez et al. 

predefined schema vocabularies. Rather than solely verbalizing logical axioms, OntoDoc integrates structural signals from the knowledge graph with contextual reasoning capabilities of pretrained LLMs, optionally incorporating relevant webbased information. This generates more informative and semantically enriched descriptions that extend beyond template-based verbalization. 

**LLM-assisted ontology engineering.** Researchers have explored the use of LLMs to support ontology creation and engineering. For example, Lippolis et al. [14] investigated the generation of OWL ontology drafts from user stories and competency questions. Funk et al. [7] proposed a method for constructing concept hierarchies across domains through LLM prompting. Similarly, Val et al. [24] introduced OntoGenix, an LLM-powered pipeline for automating ontology development from complex datasets. While these approaches demonstrate the potential of LLMs in ontology construction, their primary objective is to generate or extend ontology structure. In contrast, OntoDoc focuses on enriching existing knowledge graphs with high-quality natural language descriptions, rather than synthesizing ontology structures from scratch. 

**Graph-to-text generation.** A related but distinct line of research examines the use of LLMs and neural models to generate natural language descriptions from knowledge graphs [20,28,6]. These graph-to-text approaches typically aim to transform subgraphs that are often centered on specific entities into coherent textual summaries. Crucially, these systems focus on describing data instances (e.g., summarizing facts about a specific person or event), whereas OntoDoc is designed to describe ontology terms (classes and properties), abstracting over their instances to define the term’s intended meaning. 

# **3 Problem Formulation, Challenges and Methodology** 

**Problem Definition** . Let _G_ = _{_ ( _s, p, o_ ) _}_ be a knowledge graph represented as a set of RDF triples, where _s_ is the subject, _p_ is the predicate, and _o_ is the object (either an IRI or RDF literal; blank nodes are omitted). The graph is accessible via a SPARQL endpoint or a local RDF file. An IRI _u_ exists in _G_ if it appears as a subject, predicate, or object in at least one triple. 

An IRI _u_ may play one of three semantic roles in _G_ : class (explicitly declared as `owl:Class` or appearing as the object of `rdf:type` assertions), property (explicitly appearing as a predicate), or instance (typed to a class). OntoDoc makes no assumption about which role _u_ occupies and handles all cases uniformly. 

Given a knowledge graph _G_ and a target IRI _u ∈ G_ , the ontology description generation task is to produce a natural language string _d_ such that _d_ accurately and concisely describes the intended semantics of _u_ within the domain modeled by _G_ , suitable for use in an `rdfs:comment` [3] or similar annotation. 

**Overview of challenges** . Two properties of knowledge graphs make this task non-trivial: the semantics of an IRI are often only partially recoverable from its immediate graph neighborhood (understanding a class may require inspecting its instances and their attributes), and the wide variation in schema richness,


<!-- page 5 -->

5 

OntoDoc: Automatically Generating Ontology Resource Descriptions 



<!-- Start of picture text -->
‘eeooconte owcontestTaba Stem<br>eeaaa 1ratesubcassotduspetstenue)fzrataype,ebolacreseLeage,tertarratin detecomseLegueacecen tg |f | '@passinptionage sinaBescon<br>mm:2ComesSanaeer ptteint Tndpoint a ‘2Rarfeaeee nasumptionseeeer eeteesuecassSporateogeeycoated of<br>dbpedia.org/sparal= Osyeb Context F pence sootjoverns the leaguesdeaeatedto<br>Ameren<br>Owe Zr Atengun2th eancentrascii ore) of !<br>aes @ Description<br>Tey) we<br><!-- End of picture text -->

Fig. 1: OntoDoc System Overview 

instance density, and naming conventions means that no fixed retrieval strategy is reliably informative across domains. 

**System Overview** . OntoDoc is designed to address these challenges through a central intuition: _A good description of any ontology term should be grounded in the actual data it represents, while also offering intuitive guidance for both domain experts and first-time users._ This aligns with the W3C definition of `rdfs:comment` : “A textual comment helps clarify the meaning of RDF classes and properties . . . to indicate the intended meaning of the classes and properties described in an RDF vocabulary” [3]. 

As illustrated in Figure 1, OntoDoc comprises four components that execute in a fixed sequential pipeline: (1) **database context extraction** , (2) **web context retrieval** , (3) **assumption generation** , and (4) **description generation** . To reduce runtime, the database and web context stages run in parallel, and their outputs are then merged and passed downstream. 

Each component is implemented as an autonomous LLM agent. Agents communicate exclusively through a shared session state in the form of a key-value store that persists across the pipeline run. No agent calls another directly, instead, each agent reads its required inputs from session state and writes its output back to a designated key (e.g., `database_context` , `web_context` , `assumptions` , `description` ). This decoupled design allows components to be swapped, ablated, or replaced independently without modifying the rest of the pipeline. Full implementation details are provided in Section 4. 

# **4 Design and Implementation Details** 

## **4.1 Database Context Agent** 

The purpose of the database context agent is to gather the most semantically informative evidence available in the knowledge graph for the target IRI. Because


<!-- page 6 -->

6 J. Guajardo Gutierrez et al. 

Table 1: Agent toolset for ontology exploration and SPARQL <u>querying.</u> 

|**Tool**|**Description**|
|---|---|
|`get_iri_information`|Retrieves rdf:type, rdfs:label, rdfs:comment, dcterms:description, and<br>skos:definition; also checks whether the IRI is used as a predicate.|
|`get_outgoing_triples` <br>`get_incoming_triples` <br>`get_predicate_usage`|Returns triples where the IRI is subject (_⟨iri⟩_?_p_ ?_o_), max 200.<br> Returns triples where the IRI is object (?_s_ ?_p ⟨iri⟩_), max 200.<br>For property IRIs, returns sample triples (?_s ⟨iri⟩_?_o_) and distinct<br>rdf:type values of subjects and objects.|
|`execute_sparql`|Executes SPARQL SELECT/ASK queries with filtering, grouping, ag-<br>gregation, and arbitrary patterns.|



a single predefined SPARQL query cannot capture the diverse shapes of classes, properties, and instances across varying ontologies, we implement the agent as an agentic SPARQL explorer that automatically selects and sequences queries within a configurable budget (default: 50 triples, 10 tool calls). The agent is equipped with five tools, summarized in Table 1. 

The agent follows a four-phase protocol embedded in its system prompt (detailed in Figure 2 in the Annex): 

**Phase 1: Orient.** The agent calls `get_iri_information` on the target IRI to determine its type: _class_ ( `owl:Class` / `rdfs:Class` or many incoming `rdf:type` triples), _property_ (appears as a predicate or declared as `owl:ObjectProperty` / `owl:DatatypeProperty` ), _instance_ (typed to a domain class), or _unknown_ . 

**Phase 2: Initial scan.** The agent issues a sequence of queries depending on the type of the IRI. For a _class_ , it retrieves outgoing and incoming triples and executes a `COUNT` of instances; if the count is small ( _<_ 10), all instances are fetched explicitly. Critically, the agent then immediately inspects 2–3 individual instance IRIs via `get_outgoing_triples` to observe the actual attributes and relationships those instances carry. For a _property_ , it calls `get_predicate_usage` to see what subject/object pairs it connects, then inspects a representative subject and object to understand the entities being linked. For an _instance_ , it retrieves outgoing attributes and incoming references. 

**Phase 3: Targeted follow-up.** The agent examines all results accumulated so far and selects semantically significant IRIs (connected classes, frequently occurring properties, shared object values) for further exploration. For each candidate, it calls `get_iri_information` and, for classes, inspects some of their instances. Arbitrary SPARQL queries are used for counts of distinct values and predicate enumerations. 

**Phase 4: Summarize.** The agent compiles a numbered, deduplicated list of triples in the canonical format: _i. ⟨subject⟩⟨predicate⟩⟨object⟩_ , where _i_ denotes the triple index in the list. 

Deduplication rules prevent the output from being overwhelmed by repetitive `rdf:type` assertions; at most two or three representative triples are kept for any structural pattern. Pure ontology axioms ( `rdf:type owl:Class` , `owl:imports` ,


<!-- page 7 -->

7 

OntoDoc: Automatically Generating Ontology Resource Descriptions 

etc.) are omitted. The resulting list is written to the shared pipeline state under the key `database_context` . 

# **4.2 Web Context** 

Ontology terms frequently encode domain concepts whose meaning is not fully recoverable from the graph alone. The web context agent enriches the pipeline with external encyclopedic knowledge sourced from Wikipedia and the open web. The agent first extracts the human-readable label from the target IRI by splitting on the last `/` or `#` character (e.g., `http://dbpedia.org/ontology/LacrosseLeague` _→_ `LacrosseLeague` ). The agent then applies a two-stage filter. First, labels that are trivially unambiguous English words (name, type, id, date, etc.) are rejected immediately without any retrieval call. This rejection is handled via a prompt-embedded heuristic where the agent is given an explicit enumeration of such stopword-like terms and instructed to match against it before proceeding. Second, for all other labels, the agent decomposes the label into searchable keywords and selects from the following two retrieval tools. The agent may invoke one or both, and their outputs are concatenated into a single context string stored in the shared pipeline under `web_context` . 

`fetch_wikipedia_context` is used for general, academic, or common terms likely to have a dedicated Wikipedia article. Results are retrieved via the Wikipedia Search API and then re-ranked by a text embedding model ( `Cohere Rerank 3.5` [4]) via API, keeping at most _k_ results (default _k_ = 3) above a configurable relevance threshold (default: 0 _._ 75). This prevents low-quality, tangentially related articles from polluting the context. 

`fetch_tavily_context` is used for highly technical, niche, or domain-specific terms unlikely to have a Wikipedia entry. It queries the Tavily web search API, which indexes technical documentation, scientific databases, and other nonencyclopedic sources. The choice between tools is determined entirely by the agent’s own judgment about the label’s nature, guided by examples provided in the system prompt (see Figure 3). 

# **4.3 Assumption Generation** 

The assumption generation agent receives the database context, web context, and target IRI, and is instructed to produce a JSON object of the following form: `{ "items": [{reasoning, assumptions}, ...] }` . Table 2 shows an excerpt of the assumptions and their corresponding reasoning as produced by the agent for the DBpedia class `LacrosseLeague` . The extracted assumptions are stored in the shared pipeline under the key `assumptions` and passed to the description generation agent. 

The core idea is to force the model to reason explicitly before it writes. This is directly inspired by chain-of-thought prompting [26], which demonstrates that eliciting intermediate reasoning steps substantially improves factual accuracy in downstream generation. By committing to a structured list of explicitly


<!-- page 8 -->

8 J. Guajardo Gutierrez et al. 

Table 2: Extracted assumptions and reasonings for `dbo:LacrosseLeague` 

|**Assumption**|**Reasoning**<br>i|
|---|---|
|LacrosseLeague is a class representing organized<br>sports leagues specifically for the sport of lacrosse.|The IRI is typed as an OWL Class, specifically a<br>subclass of `SportsLeague`, indicating that it rep-<br>resents a type of sports league focused on lacrosse.<br>This is directly stated in triples 1 and 3.|
|LacrosseLeague is an internationally recognized<br>concept describing leagues, associations, or orga-<br>nizations where lacrosse teams compete.<br>. .|Multiple labels in different languages such as<br>‘lacrosse league’, ‘lacrosse bond’, ‘Lacrosse-Liga’<br>and others indicate the concept is universally rec-<br>ognized as a lacrosse sporting league entity. This<br>is supported by triples 3–9.<br>.|



justified assumptions, the model is less likely to conflate evidence from different sources or hallucinate attributes not present in the graph. The reasoning field also makes the final description traceable to specific triples from the database context. The prompting guidelines (reproduced in Figure 4) also enforce several quality constraints: the database context is designated as authoritative, whereas the web context is treated as supplementary background only. Furthermore, at least one assumption must be grounded in a specific triple from the database context, cited by its sequence number. Assumptions are prioritized by semantic value, i.e., assumptions about what the entity is and how it is used in practice are preferred over structural schema axioms, which are only included when they reveal something semantically distinctive. Assumptions supported by instancelevel data are considered the most valuable. 

While structuring intermediate assumptions reduces noise and improves factual traceability, it introduces a theoretical risk of information loss. Because this step acts as a semantic bottleneck between raw retrieval and final generation, any crucial detail omitted by the model during the synthesis phase becomes permanently unavailable to the description generation agent, potentially reducing the completeness of the final output. To empirically evaluate this trade-off between noise reduction and over-summarization, Section 5 reports an ablation study comparing descriptions generated with and without the assumption generation step. In the ablation condition, the description agent receives the raw database and web contexts directly, bypassing assumption generation entirely. 

# **4.4 Description Generation** 

The final stage of the pipeline produces the natural language description. The description generation agent is prompted as a professional lexicographer (see Figure 5) and is given the structured assumption list from the previous stage (or, in the ablation condition, the raw contexts). The agent is instructed to write a concise, accurate description that (i) does not name the IRI directly; (ii) uses specific terminology derived from the database context assumptions where relevant; (iii) omits generic metadata properties (identifiers, dates, status flags) unless they are the defining characteristic of the entity; and (iv) favours


<!-- page 9 -->

OntoDoc: Automatically Generating Ontology Resource Descriptions 9 

rare, distinctive facts that differentiate the entity from similar concepts in the same ontology. The following examples from the Friend of a Friend ontology are provided in the prompt to calibrate expected output style: 

`membershipClass` _→ Indicates the class of individuals that are a member of a Group._ 

`Agent` _→ A resource that acts or has the power to act._ 

Once the description text is composed, the agent calls a `persist_description` tool, which logs the description together with the pipeline configuration metadata (model names and ablation flags) to a database. This logging serves two purposes: it enables post-hoc experiment tracking and supports the ablation analysis reported in Section 5. The agent’s final response consists solely of the description text, which is written to the shared pipeline under the key `description` and returned as the output of the full pipeline. 

# **5 Experiments and Evaluation** 

We evaluate OntoDoc through a sequence of experiments designed to answer four questions: 1) _Which underlying LLM provides the most reliable performance within the OntoDoc pipeline?_ 2) _Does the intermediate assumption generation stage improve description quality?_ 3) _How does OntoDoc compare against existing ontology description generation baselines?_ 4) _Do automatic evaluation trends align with human judgement?_ To answer these questions, we conduct a model selection study, an ablation study on the assumption generation component, automatic evaluation against baseline systems, and human evaluation using domain experts and student annotators. 

## **5.1 Experimental Setup** 

**Datasets** . We evaluate OntoDoc on 151 ontology terms (each an IRI) drawn from three knowledge graphs, covering diverse domains and ontology structures across biomedical, agricultural, and open-domain settings. 

**BioBricks-MeSH** [19] (51 IRIs): A biomedical knowledge graph derived from the Medical Subject Headings (MeSH) vocabulary. The ontology contains 17 classes, 21 object properties, and 28 datatype properties. 

**SOCKG** [21] (70 IRIs identified as semantically important by graph developers and soil scientists): A domain-specific agricultural knowledge graph developed for soil science research using the USDA GRACEnet (Greenhouse gas Reduction through Agricultural Carbon Enhancement Network) dataset. The ontology contains 92 classes, 62 object properties, and 10 datatype properties. 

**DBpedia** [13] (30 randomly sampled IRIs): A large-scale open-domain knowledge graph automatically extracted from Wikipedia. The ontology contains 790 classes, 1167 object properties, and 1857 datatype properties.


<!-- page 10 -->

10 J. Guajardo Gutierrez et al. 

**Evaluation metrics** . We evaluate generated descriptions using four quality dimensions derived from the intended purpose of `rdfs:comment` annotations (full scoring rubrics are provided in Tables 8–11 in the Annex): 

_Accuracy_ : whether the description correctly represents the concept. _Clarity_ : whether the description is readable and accessible to non-experts. _Completeness_ : whether the description captures the important semantic information necessary to understand the term. 

_Cruciality_ : whether the included information is essential and non-redundant. 

**Reference descriptions** . Although DBpedia and Biobricks MeSH contain existing `rdfs:comment` annotations for many terms, we do not treat these annotations as gold-standard reference descriptions. During preliminary inspection, we observed that many comments function primarily as implementation notes or partial usage hints rather than semantically complete descriptions. In some cases, annotations also contradicted information explicitly present in the knowledge graph itself. Instead, evaluation is performed directly on generated descriptions using the four quality dimensions above, with the verified database context serving as the shared factual grounding for both automatic and human judges. 

**Grounding the descriptions** . A key challenge is that the database context is produced via an agentic retrieval process, where outputs depend on modelselected queries. Consequently, retrieved contexts are nondeterministic and may vary across models and runs, introducing potential evaluation bias. To ensure fairness, we standardize this step by running the database context retrieval step as outlined in Section 4.1 using the same model that serves as the LLM judge. We refer to the resulting database contexts outputs as _canonical database contexts_ . Using this setup, for each term in the combined dataset, we construct a single context represented as a numbered list of RDF triples, optionally including instance counts. To ensure factual correctness, we apply an automated cleaning and verification pipeline to each canonical database context. Each context is then automatically cleaned: triples are validated against the knowledge graph via SPARQL ASK queries, instance counts are verified for consistency, and any hallucinated or inconsistent information is discarded, yielding a fully verified canonical context. 

# **5.2 Model Selection and Ablation Study** 

Two preliminary experiments are conducted in a deliberate sequence: model selection first, followed by the ablation study on assumption generation. This ordering is motivated by the need to isolate the contribution of each factor independently. 

**Model selection** . We first evaluate which underlying language model provides the strongest performance within the OntoDoc pipeline. We compare three candidate generation models: GPT-4.1 Mini [17], Gemini 2.5 Flash Lite [8], and GLM-4.7 Flash [29]. Evaluation is conducted using an LLM judge (Kimi K2.5


<!-- page 11 -->

OntoDoc: Automatically Generating Ontology Resource Descriptions 

11 

Table 3: Win Rates with and without Assumptions 

|**Model**|**Win Rate (w/ assumptions)**|**Win Rate (w/o assumptions)**|
|---|---|---|
|gpt-4.1-mini|47.02%|47.68%|
|gemini-2.5-flash-lite|23.18%|19.21%|
|glm-4.7-flash|29.80%|33.11%|



[2]) in a forced-choice preference setting rather than rubric-based scoring. For each IRI, OntoDoc generates two descriptions per candidate model (one description generated using the assumptions step, and one description without). The judge is then presented with the target IRI, the canonical database context, and the three candidate descriptions in randomized order. The judge is then instructed to select the single best description according to the evaluation criteria of accuracy, clarity, completeness, and cruciality in a forced-choice preference setting (see the prompt template in Figure 6). We repeat this step using the descriptions that were generated without the assumptions step. 

Thus, for each ontology term, two independent comparisons are performed: one among three descriptions generated with assumptions (one per model), and one among three descriptions generated without assumptions. Table 3 reports model win rates with and without the assumption generation stage. Across both conditions, GPT-4.1 Mini achieves the highest and most stable win rate, so we use it as the default for all remaining experiments. 

**Assumption generation ablation study** . We next evaluate the contribution of the assumption generation component. Using `gpt-4.1-mini` as the fixed generation model, we compare OntoDoc with and without the assumption generation stage. The evaluation procedure mirrors the model selection setup. For each IRI, the judge receives two candidate descriptions generated under the two configurations together with the canonical database context and selects the stronger description using the ablation prompt template (Figure 7). Table 4 reports the percentage of cases in which the configuration with assumption generation was preferred. The assumption generation stage improves performance consistently across all three knowledge graphs. The largest gains are observed on BioBricks MeSH, suggesting that explicitly reasoning over retrieved evidence is particularly beneficial in highly specialized scientific domains. Based on these results, the assumption generation stage is included in the final OntoDoc configuration. 

Table 4: Assumptions Step Win Rate <u>per</u> Knowledge Graph for <u>gpt-4.1-mini</u> 

|**Knowledge Graph**|**Sample Size (n)**|**Assumptions Step Win Rate**|
|---|---|---|
|DBpedia|30|57.00%|
|BioBricks-MeSH|51|61.00%|
|SOCKG|70|54.00%|


<!-- page 12 -->

12 J. Guajardo Gutierrez et al. 

# **5.3 Automatic Evaluation** 

For end-to-end evaluation, we compare OntoDoc against two baseline systems: 

**Single-Hop Retrieval (Naive).** This baseline simulates the behavior of a user unfamiliar with the knowledge graph who issues a simple outgoing-triple query: `SELECT ?p ?o WHERE { <iri> ?p ?o . }. The exact LLM prompt that was given to gpt-4.1-mini for generating these descriptions is shown in Figure 8.` The retrieved triples are passed directly to an LLM without additional graph exploration, reasoning, or web retrieval. 

**Ontology Verbalizer.** A schema-based verbalization system that generates natural language descriptions from ontology axioms and logical structure. 

Because the ontology verbalizer only supports IRIs that are explicitly typed as `owl:Class` , direct comparison across all three methods is restricted to a subset of ontology terms supported by every approach. We refer to this subset as the _common IRI set_ . 

**Comparison with naive baseline** . We first evaluate OntoDoc against the naive single-hop baseline across all 151 terms using `kimi-k2.5` as the LLM judge. Each description is independently scored on a 5-point Likert scale for accuracy, clarity, completeness, and cruciality by the LLM judge (see Figure 9 for the grading prompt configuration). Table 5 presents the per–knowledge graph mean scores for both systems. OntoDoc consistently achieves substantially higher completeness across all three graphs: on DBpedia, completeness rises from 3.67 (naive) to 3.97; on BioBricks MeSH from 3.37 to 3.71; and on SOCKG from 3.26 to 3.84. Averaged across all knowledge graphs, OntoDoc attains a mean completeness of 3.84 compared to 3.43 for the naive baseline, confirming that the multi-stage evidence synthesis produces significantly more thorough descriptions. 

Accuracy and clarity follow a slightly different pattern. On DBpedia, the naive baseline yields marginally higher accuracy (4.30 vs. 4.20) and clarity (4.73 vs. 4.47), likely because the simple triples it retrieves are easier to paraphrase without introducing subtle distortions. On the more specialised BioBricks MeSH and SOCKG graphs, however, OntoDoc matches or exceeds the naive baseline in both dimensions (e.g., accuracy 3.76 vs. 3.65 on BioBricks MeSH; 3.91 vs. 3.90 on SOCKG), demonstrating that its adaptive exploration becomes increasingly beneficial as domain complexity grows. Cruciality scores are similar across systems, with OntoDoc maintaining high conciseness (3.79–4.04) while incorporating richer content. Overall, the automatic evaluation shows that OntoDoc delivers a clear advantage in completeness without sacrificing the other quality dimensions, and in domain-specific settings it also equals or improves upon the naive baseline in accuracy and clarity. 

**Comparison with ontology verbalizer** . For the common IRI subset (those unambiguously typed as `owl:Class` ), we additionally compare OntoDoc with the template-based ontology verbalizer. The same LLM judge and scoring protocol are applied. The automatic scores per knowledge graph is shown in Table 6. In terms of accuracy, OntoDoc either matches or slightly exceeds the verbalizer across all three knowledge graphs. The most pronounced difference lies once


<!-- page 13 -->

13 

OntoDoc: Automatically Generating Ontology Resource Descriptions 

Table 5: OntoDoc vs Naive Scores <u>per</u> Knowledge Graph 

|**Knowledge Graph**|**Metric**|**OntoDoc**|**Naive**|
|---|---|---|---|
||Accuracy|4.20|4.30|
|DBedia(n=30)|Clarity|4.47|4.73|
|p|Completeness|3.97|3.67|
||Cruciality|3.90|4.43|
||Accuracy|3.76|3.65|
|BioBricks-MeSH(n=51)|Clarity|4.43|4.24|
||Completeness|3.71|3.37|
||Cruciality|4.04|4.00|
||Accuracy|3.91|3.90|
|SOCKG(n=70)|Clarity|4.49|4.37|
||Completeness|3.84|3.26|
||Cruciality|3.79|3.97|



again in completeness, where OntoDoc vastly outperforms the verbalizer, achieving scores that are often one full point higher on the 5-point scale. This confirms that the template-driven verbalizer, limited to explicit schema axioms, misses much of the semantic information that OntoDoc recovers from instance data and external knowledge. Clarity and cruciality scores are comparable, with OntoDoc maintaining high readability and conciseness despite its richer content. 

Table 6: Rubric Scores <u>(common</u> URIs) <u>per</u> Knowledge Graph 

|**Knowledge Graph**|**Metric**|**Naive**|**OntoDoc**|**Verbalizer**|
|---|---|---|---|---|
||Accuracy|4.20|4.30|1.50|
|DBedia|Clarity|4.80|4.70|1.00|
|p|Completeness|3.40|4.00|1.20|
||Cruciality|4.50|4.10|1.50|
||Accuracy|3.65|4.00|3.41|
|BioBricks-MeSH|Clarity|4.24|4.71|3.94|
||Completeness|3.24|3.88|3.18|
||Cruciality|4.12|4.35|3.65|
||Accuracy|4.00|4.12|3.96|
|SOCKG|Clarity|4.42|4.58|4.58|
||Completeness|3.33|3.96|1.75|
||Cruciality|3.96|3.75|4.96|



# **5.4 Human Evaluation** 

To validate the quality of OntoDoc-generated descriptions in a realistic setting, we conduct a human evaluation study. Unlike the automatic evaluation, which compares OntoDoc against baseline systems, the human evaluation focuses exclusively on assessing the quality of OntoDoc outputs in isolation, providing an absolute measure of description quality from the perspective of real users.


<!-- page 14 -->

14 J. Guajardo Gutierrez et al. 

For SOCKG, annotations are performed by external domain experts in soil science. For DBpedia and BioBricks MeSH, annotations are performed by student evaluators with prior experience working with RDF knowledge graphs. In total, 11 annotators participated in the study. For each ontology term, annotators are presented with the target IRI, the canonical database context, and the generated description. For SOCKG, a screenshot of the relevant section of the AgCROS dataset that the term is modeled after is also provided to aid the domain experts. Descriptions are evaluated independently according to the four evaluation dimensions using the same 5-point Likert scale employed in the automatic evaluation. 

Table 7 summarizes the average human evaluation scores across datasets. Human evaluators rated OntoDoc descriptions highly across all dimensions and knowledge graphs. On DBpedia and BioBricks MeSH, mean scores for clarity and accuracy comfortably exceed 4.0 on the 5-point scale, while completeness and cruciality also receive strongly positive ratings. The pattern mirrors the automatic evaluation: clarity and accuracy tend to be the highest-scored dimensions, followed by cruciality and completeness, which reflects the inherent difficulty of packing all essential information into a concise description without introducing any extraneous detail. Scores on SOCKG are slightly lower overall, consistent with the increased domain specificity and terminological complexity of agricultural and soil science concepts; nonetheless, all mean ratings remain in the favourable range, demonstrating that OntoDoc produces high-quality descriptions even for highly specialised scientific terms. 

The alignment between human and automatic evaluation trends confirms that the LLM-based judge captures the same quality perceptions as human evaluators, supporting the reliability of the automatic scoring protocol used in the preceding experiments. 

Table 7: Average Human Annotation Scores by Knowledge Graph 

|**KG**|**Accuracy**|**Clarity**|**Completeness**|**Cruciality**|
|---|---|---|---|---|
|DBpedia|4.43|4.36|4.36|4.20|
|BioBricks-MeSH|4.51|4.49|4.43|4.34|
|SOCKG|3.93|3.65|3.72|3.74|



# **6 Discussion** 

Our experiments reveal a consistent pattern: OntoDoc’s primary advantage lies in the completeness of its generated descriptions. Adaptive graph exploration combined with external contextual grounding allows it to recover semantic information that fixed-query and schema-only approaches miss. This is most visible in comparisons against the ontology verbalizer, whose reliance on explicit schema axioms leaves it unable to surface semantics expressed implicitly through instance data.


<!-- page 15 -->

OntoDoc: Automatically Generating Ontology Resource Descriptions 

15 

These gains carry a trade-off. The cruciality metric rewards descriptions in which every detail is strictly necessary and since OntoDoc retrieves substantially more evidence than the baselines, it is more likely to include secondary details that are informative but not absolutely essential. This is particularly visible on SOCKG, where the verbalizer achieves high cruciality despite poor completeness due to its tendency to produce structurally generic outputs (e.g., “Planting management is a type of measurable entity.”) that contain little opportunity for irrelevant content. High cruciality in this case reflects brevity, not quality. 

The DBpedia results point to a boundary condition: when concepts are already well represented in a model’s pretraining data, the additional context OntoDoc gathers offers marginal benefit and can occasionally introduce detail that slightly harms clarity or cruciality. OntoDoc is most valuable in specialized domains where underlying model knowledge is sparse. 

Finally, the lower SOCKG scores in human evaluation reflect annotator composition as much as system performance. Domain experts in agricultural soil science apply stricter standards of scientific precision than general RDFexperienced annotators, so the gap between SOCKG and the other datasets is best interpreted as a difficulty effect rather than a system failure. The alignment between human and automatic evaluation trends across all three graphs confirms that LLM-based scoring reliably tracks human quality perception. 

# **7 Conclusion** 

We presented OntoDoc, a multi-agent framework for automatically generating natural language descriptions for ontology terms in heterogeneous knowledge graphs. By combining adaptive SPARQL-based graph exploration, external web retrieval, and an intermediate assumption generation stage, OntoDoc produces descriptions that are substantially more complete than naive single-hop retrieval or template-based ontology verbalization, while maintaining competitive accuracy and clarity across biomedical, agricultural, and open-domain settings. Our evaluation across 151 ontology terms demonstrates that the assumption generation stage consistently improves description quality, particularly in specialized scientific domains. Human evaluation by both domain experts and student annotators corroborates the trends observed in automatic scoring, confirming the reliability of LLM-based assessment for this task. 

_Supplemental Material Statement:_ Source code is available at `https:// anonymous.4open.science/r/ontodoc/` . Prompt templates and evaluation scoring rubrics are located in the annex. System demo videos, the raw data used to generate Tables 3, 4, 5, 6, and 7, and the ontology files and SPARQL endpoints used as input to OntoDoc are attached with the submission in EasyChair and, if accepted, will be made publicly available via a GitHub repository.


<!-- page 16 -->

16 J. Guajardo Gutierrez et al. 

# **8 Declaration of use of Generative AI** 

We used generative AI to improve the clarity, grammar, and readability of portions of the text. All AI-suggested changes were reviewed and finalized by the authors. In addition, we used Claude to assist in writing and refactoring sections of the code used in this research. The authors verified, tested, and assume full responsibility for all generated code. 

No generative AI tool is listed as a co-author, nor was any AI used to create figures, tables, or citations. All use described above complies with the conference’s disclosure requirements, and the authors remain fully responsible for the originality, accuracy, and integrity of the entire work.
