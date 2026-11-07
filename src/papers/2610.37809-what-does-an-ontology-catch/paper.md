---
source: 2610.37809-what-does-an-ontology-catch.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# What Does an Ontology Catch? Curated, LLM-Generated and Data-Derived Ontologies as Checkers of LLM Agents over Knowledge Graphs · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

# **What Does an Ontology Catch? Curated, LLM-Generated and Data-Derived Ontologies as Checkers of LLM Agents over Knowledge Graphs** 

|Michal Orzechowski<br>ACK Cyfronet AGH|Rund Tawfiq<br>Sano Centre for Computational|Tomasz Kosciolek<br>Sano Centre for Computational|
|---|---|---|
|Krakow, Poland|Medicine|Medicine|
|AGH University of Krakow<br>Krakow, Poland|Krakow, Poland|Krakow, Poland<br>AGH University of Krakow|
|Sano Centre for Computational<br>Medicine<br>Krakow, Poland||Krakow, Poland|



## **Abstract** 

LLM agents that answer questions over Web knowledge graphs are increasingly wrapped in checks derived from the graph’s ontology, on the assumption that a formal schema makes a reliable judge. Yet a checker can be wrong as well: it can miss errors, and it can flag correct answers and push the agent into “fixing” them. Whether a curated ontology is worth its cost as such a judge, and how it compares with an ontology an LLM writes or a schema mined from the data, is unknown. We make the checker itself the object of study. Across curated, LLM-generated and data-derived ontologies, used as prompt context, as a checker, or both, and across open-weight and proprietary agents on public graphs and a private graph of nearly 10<sup>9</sup> triples, we account for what ontology-derived checks catch and what they wrongly flag. We show how each source trades caught errors against false alarms, how a curated schema used as published can contradict its own data, which errors structural checks miss, and whether combining sources or giving the agent the checker’s specific feedback pays off. On UniProt, the curated ontology flags more correct answers than either an ontology derived from the data or one an LLM derives from a summary of the data with masked identifiers. On real agent answers, its flags are only marginally more precise than random flags. 

## **Keywords** 

knowledge graphs, ontologies, LLM agents, verification, SPARQL 

## **1 Introduction** 

Public data across domains is increasingly published as knowledge graphs, which describe entities and the relationships between them so that a single query can traverse many entities; Wikidata [32], DBpedia [19] and UniProt [31], for example, can be queried through SPARQL endpoints [2]. Most graphs are described by an ontology, a machine-readable account of what kinds of entities a graph contains and how they are related. 

Large language models (LLMs) have made knowledge graphs more accessible, as they translate natural language questions into SPARQL queries, run them against the endpoints, and report the retrieved results [16, 20, 29]. However, it is difficult to validate their results. A query can be syntactically valid, execute without error, yet answer a different question from the one asked [7, 21]. One way to assess an answer is to test whether its query fits what the 

graph’s ontology states about its entities and relationships. If the ontology contains, in the Web Ontology Language (OWL) [33], a domain axiom stating that whatever has a birth date is a person and a disjointness axiom stating that no city is a person, a query for the birth date of a city contradicts it. These kinds of checks were built for SPARQL queries written by LLMs, where they are reported to increase accuracy [1], and testing a graph’s data against its ontology with SPARQL is an established method to assess the quality of Linked Data [18]. 

Checks may still permit errors. They may accept incorrect answers or flag correct ones, prompting an LLM agent to revise a correct answer into an incorrect one, as has been observed in text-toSQL refinement [13]. Accuracy alone reveals neither error. Checks based on ontologies are particularly prone to flagging correct answers, because axioms are read as constraints on the data [23] while published ontologies often do not describe all of it: in a crawl of Linked Data, 14.3% of triples used properties that were not defined in any of the crawled vocabularies [11], and a check that requires every property to be declared would reject correct answers that rely on them. Before an ontology can be used to judge an agent’s answer, its suitability for that role must itself be assessed. 

Existing approaches to ontology evaluation do not address this use. Ontologies are typically evaluated by comparison with a gold standard, by expert assessment, or by their coverage of a corpus or dataset [6]. Constraints derived from ontologies were also compared with constraints mined from the data to validate the data [8], where a constraint violation is interpreted as an error in the data. When an ontology is used to check an agent’s answers, however, a violation may instead reflect an error in the ontology, resulting in a correct answer being rejected. We therefore evaluate ontologies in this application directly, measuring both the errors they detect and the correct answers they incorrectly flag. 

This gap has implications for both knowledge graph publishers and agent developers. Publishers would benefit from knowing how expert curated ontologies compare with ontologies generated by LLMs [35], or ontologies derived from data [26] when used to assess agent answers. Developers may benefit from understanding whether an ontology is most useful as context for generating an answer, as a check on the answer, or both. 

In this paper, we evaluate curated, LLM-generated, and dataderived ontologies as checks on agents’ answers. We address three


<!-- page 2 -->

Orzechowski et al. 



<!-- Start of picture text -->
flag: one retry, with the check’s message or a generic one<br>query Knowledge graph results Check derived pass<br>Question LLM agent Answer kept<br>(SPARQL endpoint) from the ontology<br>as context as check<br>Ontology,of three sourcesfrom one curated writtenan LLMby derivedthe datafrom missed,Everythe correctfalseverdictalarm,answer:scoredcorrectcaught,againstpass<br><!-- End of picture text -->

**Figure 1: The setting. An LLM agent answers a question with a SPARQL query; a check derived from an ontology passes the answer or flags it, and a flag triggers one retry. The same ontology can also be the agent’s context.** 

research questions: 

- **RQ1** Which errors do checks from curated, LLM-generated and data-derived ontologies catch, how often do they flag correct answers, and what do they cost to set up and to run? 

- **RQ2** What causes the false alarms, and which errors do the checks miss? 

- **RQ3** How does the ontology contribute at other stages of the process: as context for answer generation, in combination with another check, or as feedback to the agent after a check is triggered? 

A fair comparison must address three concerns, and each shapes our design. First, executing a query can itself reveal errors, for example when it returns no results, so we distinguish errors caught by a check from those already exposed by query execution. Second, results on artificially introduced faults may not generalize to real errors [14, 24], so we evaluate each check on both real agent answers and faults introduced into correct queries. Third, LLMs may recall identifiers from public knowledge graphs [10], potentially biasing the ontologies they generate. We therefore also have LLMs build ontologies from a masked summary of the graph, in which identifiers are replaced with opaque names. Every check judges the same answers and faults, and each decision is compared with the pre-defined answer (Figure 1). 

This paper makes three contributions: 

- A comparison of curated, LLM-generated and data-derived ontologies as checks on LLM agents built on five openweight and two proprietary models, confirmatory on UniProt and exploratory on other public graphs and a private graph of nearly 10<sup>9</sup> triples. 

- An analysis of why such checks go wrong: where a curated ontology as published disagrees with its own data, and which errors the checks miss. 

- A released set of artificial faults introduced into correct queries, with their pre-defined correct answers, and a protocol that measures any check’s catches and false alarms against a retry on empty results, without running an agent.<sup>1</sup> 

# **2 Related Work** 

LLM agents are increasingly used to interact with knowledge graphs. TogoMCP makes approximately sixty RDF databases accessible to LLMs through the Model Context Protocol (MCP) [16]. Other systems focus on generating and executing queries. SPINACH generates SPARQL queries and revises them based on 

> 1The artificial faults, the code and the pre-registration are available at https:// anonymous.4open.science/r/www-2027-replication-package-36D6; Appendix A lists the contents. 

returned results, empty results, and execution errors [20]. SPARQLLLM generates queries over federated life science endpoints using endpoint metadata and checks them against schema information before execution [29]. 

Beyond query generation, several methods explicitly check or constrain agent behavior. The Ontology-based Query Check flags queries that conflict with an ontology and prompts LLMs to revise them, which is reported to increase accuracy on an enterprise question answering benchmark [1]. NaVQA addresses queries that use ontology terms without mappings to the underlying data, which can silently produce empty results, by restricting the agent to ontology terms represented in the data [34]. These methods differ in what they check and how they intervene, but are typically evaluated by overall response accuracy. We instead vary the source of the ontology and evaluate each flag against the correct answer, distinguishing detected errors from false alarms. 

Ontology axioms can be used to validate data, by interpreting them as constraints rather than only as a means for inference. Motik et al. showed that OWL axioms that resemble integrity constraints do not act as checks under standard first-order semantics, motivating a separate formalization for integrity constraints [23]. The W3C subsequently standardized SHACL for validating RDF data against structural constraints [17], and ShEx offers a comparable language [25]. Kontokostas et al. translated vocabulary axioms such as domain, range, and disjointness into SPARQL tests over Linked Data, and found that domain and range tests identified the most errors [18]. At the query level, Seifer et al. type-check SPARQL queries against an ontology and reject queries whose results must be empty on any database [28]. 

However, ontology-based checks depend on the suitability of the ontology itself. Linked Data uses terms without defined vocabularies [11], while combining widely used vocabularies under a closed-world interpretation can expose conflicting definitions [9]. In the biological domain, ontology-based constraints were used to evaluate annotations, which revealed limitations in the ontology itself [30]. We ask the same question of checks on agents’ answers at query time, where an unsuitable ontology flags correct answers. 

Ontologies and constraints may be generated by LLMs rather than domain experts. LLMs generated shape schemas for Wikidata and YAGO which were evaluated against reference schemas [35]. Shapes mined from large knowledge graphs were filtered according to how frequently the data supports them [26], and constraints extracted from ontologies, mappings, schemas, and data were combined and used to evaluate a dataset [8]. In each case, the constraints are assessed against a reference or the data, not by how they perform as checks on downstream tasks.


<!-- page 3 -->

What Does an Ontology Catch? 

Checks are useful only when their feedback is reliable. LLM self-correction is more effective when guided by reliable external feedback than by the model’s own judgement, except in tasks particularly suited to self-evaluation [15]. Consequences of unreliable checks have also been studied directly, where ErrorLLM measures how often refining a correct SQL query flagged by a detector changes its result [13]. In software engineering, static analyses used in Google’s code review are required to keep effective false positives below 10%, reflecting the risk that false alarms erode developers’ trust [27]. Queries that remain valid while expressing a different question than intended have been catalogued for SQL [7], and LLMs detect them in generated SQL with limited accuracy [21]. 

Evaluating checks requires care in how test cases are constructed. Artificially introduced faults provide controlled test cases, but may not represent the full range of real faults [14], and conclusions drawn from artificial faults do not always generalize to real ones [24]. Evaluation can also be affected by information leakage, where models may recall identifiers from public knowledge graphs even when those identifiers are masked in the input [10]. Building on these lessons from software testing, SQL, and code, we evaluate deterministic, ontology-derived checks for SPARQL agents on both real agent answers and artificial faults. 

# **3 Ontologies as Checks** 

# **3.1 Ontology sources** 

We compare three types of ontologies: A _curated_ ontology is published by the knowledge graph’s authors, and we use it exactly as published to reflect what an agent developer would obtain in practice. A _data-derived_ ontology summarizes the data itself, including the number of instances of each class, and, for each property, the classes of the instances that appear as its subjects and objects. Instances are counted under each of their asserted classes and their superclasses. A pattern is considered allowed only if it occurs at least five times in the data. It states domain and range but no disjointness axioms. An _LLM-generated_ ontology is produced by Claude Opus 5.5 from the same summary used to construct the data-derived ontology, supplemented with a fixed sample of instances per class. Thus, the difference between these data-derived and LLM-generated ontologies is what the LLM adds, given the summary and a sample of instances. We also evaluate a baseline with no ontology. 

# **3.2 Ontology uses** 

Each ontology is used in three ways. _As context_ , the ontology is rendered as text in the agent’s prompt. All ontology sources use the same rendering procedure where classes and hierarchy are provided first, followed by domain and range, disjointness, and labels, all within a common token budget. _As a check_ on the agent’s answer, each ontology is compiled using the same compiler, so differences between sources do not reflect differences in implementation. _Both_ : the same ontology is supplied as context in the prompt and used as a check on the answer. 

and infer, from its triple patterns, the types required of each variable and constant, which they test against the ontology. The subject of a property must be an instance of the property’s declared domain or one of its subclasses, its object must be an instance of the declared range or one of its subclasses, and no variable may be required to belong to two classes declared disjoint. A heuristic check, on in every condition, also flags a variable required to belong to two classes that share no subclass in the ontology, a closed-world counterpart of a missing disjointness axiom. A separate declaration check requires every class and property named by the query to be declared in the ontology. A datatype check flags a literal outside the datatype a property declares as its range. The data-derived ontology adds pattern checks on co-occurrence: they flag a property used with a class the data never combines with it, and a join of two triple patterns that no class supports at least five times. 

Binding checks re-evaluate the query’s graph pattern with every variable projected, collect the resulting bindings, and test the asserted types of the bound resources against the same axioms. Collection is limited to 10,000 triples per answer. 

# **3.4 Axiom interpretation** 

We interpret ontology axioms as constraints on the data as it stands, following the closed-world reading of OWL axioms as integrity constraints [23]. A flag therefore indicates that the asserted data violates an axiom as written. Under OWL’s open-world semantics [33], the same data might instead entail a class membership that has not been explicitly asserted. We do not resolve this difference between interpretations, and instead quantify it by attributing each false alarm to its cause (RQ2, Section 5). 

We distinguish _contradictions_ from _mismatches_ . A contradiction is a violation under both readings, where the data witnesses an explicit logical clash, such as an instance belonging to two disjoint classes, a value violating a declared datatype, or a functional property with two distinct literal values for the same subject. A mismatch is a violation under the closed-world reading only, such as a subject with no asserted type in a property’s declared domain, which OWL would instead use to infer that type. 

# **3.5 Check verdicts** 

A check _passes_ when the available evidence satisfies the constraint, and flags when it detects a violation. It returns _unknown_ when the evidence needed to decide is unavailable, for example because the value is untyped, retrieval reaches its limit, or the query contains a construct outside the supported SPARQL fragment (Appendix B.1). A check is _not applicable_ when there is no relevant axiom to test against the terms used in the query. 

An answer is flagged if any check flags it. If none flags the answer but at least one returns unknown, the answer is classified as unknown; otherwise, it is passed. Unknown answers are not flagged and therefore do not trigger a retry. They count as unflagged in every rate, and their share is reported separately. 

# **3.6 Scoring checks** 

# **3.3 Check types** 

Checks examine either the query or its bindings, the solution mappings of its graph pattern. Query checks parse the SPARQL query 

There is a pre-defined correct answer for each question, and each check decision therefore falls into one of four categories. A _caught_ answer is a flagged wrong answer. A _missed_ answer is an unflagged


<!-- page 4 -->

Orzechowski et al. 

|**Curated ontology (excerpt)**<br>ex:birthDate rdfs:domain ex:Person .<br>ex:Person owl:disjointWith ex:City .<br>ex:birthPlace rdfs:domain ex:Person .<br>ex:birthPlace rdfs:range ex:Place .<br>ex:populationis used by the data but not declared.<br>**Data (excerpt)**<br>ex:Dublin rdf:type ex:City .|
|---|
|**Caught.**_“When was Dublin founded?”_<br>SELECT ?d WHERE { ex:Dublin ex:birthDate ?d }<br>Dublin is a city, and a city cannot have a birth date: flag. Running the query also<br>returns nothing.|
|**False alarm.**_“What is the population of Dublin?”_<br>SELECT ?p WHERE { ex:Dublin ex:population ?p }|
|The query is right, but the ontology does not declareex:population: flag. A data-<br>derived ontology passes it.|
|**Missed.**_“Who founded Dublin?”_<br>SELECT ?p WHERE { ?p ex:birthPlace ex:Dublin }<br>The query returns the people born in Dublin. Every type fits the ontology, so every<br>check passes a wrong answer.|



## **Figure 2: Three answers checked against one curated ontology, in an invented vocabulary.** 

wrong answer. A _false alarm_ (a false positive) is a flagged correct answer. A _correctly passed_ answer is an unflagged correct answer. Figure 2 shows a caught answer, a false alarm and a missed answer. We report the _catch rate_ (recall) as the proportion of wrong answers that are flagged, and the _false-alarm rate_ as the proportion of correct answers that are flagged. 

# **3.7 Retries** 

A flag triggers one retry. The agent resumes its conversation, and a fixed instruction tells it that its earlier answer has been set aside and asks for a final answer. It receives one of two messages: a _specific_ message, which identifies the failed constraint and the part of the query that violated it without revealing the ontology source, or a _generic_ message, “Please re-check your answer.” The two messages are alternative conditions applied from the same state, so the message is the only difference between them. The retry has the same tools and limits as the first attempt, and its answer is final. A retry that fails or abstains counts as wrong. 

We classify a wrong answer that becomes correct after retry as _fixed_ , and a correct answer that becomes wrong as _corrupted_ . These outcomes measure both the benefit of a flag and the risk of acting on a false alarm. 

# **4 Study Design** 

Every confirmatory claim concerns one public graph, UniProt, and was registered with its test and margin before any test answer was examined (Section 4.6). The other graphs, the human-written questions and every analysis not registered in advance are exploratory. 

# **4.1 Graphs** 

Table 1 lists the five graphs used in the study. We use the SwissProt subset from UniProt [31] r2026_03 for all confirmatory claims. The curated ontology of this graph declares domain, range, and disjointness axioms, which allows all three kinds of checks to be evaluated. We use Rhea [3], which declares a class hierarchy but no domain, range or disjointness axioms in its curated ontology, for class membership checks. We also use a masked copy of Rhea, 

**Table 1: The graphs: size, what the curated ontology declares, and role.** 

|Graph|Triples|Curated ontology declares|Role|
|---|---|---|---|
|UniProt|4_._0×10<sup>8 </sup><br>|domain, range, disjointness<br>|confirmatory|
|Rhea<br>|5_._5×10<sup>6 </sup><br>|class hierarchy only<br>|exploratory|
|Rhea, masked|5_._5×10<sup>6 </sup><br>|as Rhea<br>|exploratory|
|Corporate|2_._7×10<sup>4 </sup><br>|domain, range; no disjointness<br>|exploratory|
|Private|∼10<sup>9 </sup>|not described|rates only|



in which we replace class, property, and instance identifiers and labels with opaque identifiers, to test whether agents and LLMgenerated ontologies rely on recognising a familiar vocabulary. We also use a corporate graph from outside the life sciences [22] and a private graph of nearly 10<sup>9</sup> triples with its own curated ontology. Each graph is served from a triple store that answers queries over its asserted triples without reasoning, and the public graphs from QLever [4]. Results on graphs other than UniProt are exploratory, and we only report rates on the private graph. 

# **4.2 Ontologies** 

Each graph has the three ontology sources defined in Section 3.1, and a baseline without an ontology. For UniProt, every ontology fits within the common token budget and is given to the agent in full. We draw three LLM-generated ontologies per graph; on the masked copy of Rhea they are drawn from its masked data summary. On UniProt we draw three more _masked_ ontologies from a copy of the data summary in which identifiers are renamed and string values masked; they are used only as checks. C3 uses these masked draws, so that agreement with the curated ontology does not merely reflect recall of familiar identifiers; masking reduces the cues for recalling UniProt’s published ontology, but it cannot establish that the model has never seen it (closed-book probes, Appendix D.3). Their domain and range axioms are a subset of the data-derived ontology’s, and the LLM adds disjointness, so C3 compares the curated axioms with data-derived domain and range plus LLM-added disjointness. The properties of these draws are described in Appendix B.2. 

Each ontology source can be used as context, as a check, or in both roles (Section 3.2). On UniProt, every model answers with no ontology, the curated or the data-derived ontology in its prompt, and Sonnet and Qwen3.8 also with the first LLM-generated one. The checks of every source, including the masked ontologies and the combined check, are applied to the first answers of every prompt condition. Retries are run on the answers given with no ontology: after a curated flag, once with the specific message and once, from the same state, with a generic request to re-check, and after each comparator’s flags (Section 4.7). 

# **4.3 Questions and correct answers** 

Questions are generated from each graph’s structure using seven templates, ranging from single lookups to compositional questions involving joins, filters and, aggregation. Each question is paired with the SPARQL query that answers it on the graph. The result of that query is the question’s pre-defined correct answer. Agent answers are scored mechanically by exact match using scorer rules fixed in advance. A guard rejects ambiguous questions: for each template, plausible alternative readings, such as including narrower classes or transitive membership, are run against the graph, and


<!-- page 5 -->

What Does an Ontology Catch? 

a question whose answer changes under one must state its scope or is not generated. Each correct query is re-executed against the graph. An independent LLM agent, given only the question text and not its paired query, produced queries matching the correct answers for all 30 questions in a sample from an earlier version of the set. 

Because agents answered simple lookups almost perfectly on development data, the compositional tier was made harder in at most two rounds, each raising every compositional template one step along one axis, aiming at an accuracy of about 50–80% for Sonnet without an ontology on the development questions. For each graph, questions are divided into development (30%) and test (70%) sets within each template, resulting in 210 test questions on UniProt, 70 lookups and 140 compositional. In addition, we use 173 UniProt and 124 Rhea question–query pairs from a published collection [5] as a reference set that models may have seen during training, run for two models (Appendix C.3). 

# **4.4 Agents** 

Seven models answer the questions: two proprietary models, Claude Sonnet 5.5 and Claude Haiku 5.5, and five open-weight models, Qwen3.8-27B, Qwen3-Coder-30B-A3B, GLM-5.3-Flash, Gemma-431B and DeepSeek-V4-Flash. Each agent queries the graph through a SPARQL tool and submits its answer as rows of identifiers and values. Each question is attempted three times per model and condition, as independent runs, subject to turn and time limits held constant across models. 

# **4.5 Artificial faults** 

Agent errors are sparse and unevenly distributed, so we also introduce artificial faults in correct queries to measure checks independently of agent behaviour. Each fault applies a single operator to the correct query of a UniProt test question or of an additional question generated with the same templates, resulting in 1,260 questions. The operators form three classes: (1) invented identifiers absent from the graph. (2) swaps of a class, property, or constant for an item of a different type, drawn from the data-derived ontology’s co-occurrence graph, whose nodes are properties and the classes and datatypes the data uses with them at least five times, and whose edges join a property to such a class or datatype. A swap replaces a class or property with a node of the same kind exactly two or four steps away, so that at two steps two classes share a property or two properties share a class; a constant is replaced by a member of a class at that distance from its own classes. (3) meaning changes that preserve the query form, such as replacing COUNT with COUNT DISTINCT, MIN with MAX, or dropping a grouping key. Swaps of a constant for another constant of the same type are reported as a separate stratum, which accounts for the four rows in Table 4. 

Each faulty query is labelled according to whether it changes the answer. Unmodified correct queries and rewrites that preserve the answer are controls used to count false alarms. To evaluate any check without running an agent, the check is applied to each faulty query and each control. A flag on a faulty query counts as a catch only if the fault changes the answer, and a flag on a control counts as a false alarm. Since a query that returns no rows already signals a problem, rates are also reported separately for faults whose queries 

still return rows, and compared with retrying only when a query returns no rows. Table 4 reports the composition of the fault set. 

# **4.6 Claims and statistics** 

The claims, outcomes, tests, and margins were registered and frozen in a timestamped commit before any test question was run. Each claim answers one of the research questions, as labelled below. **RQ1, C2** As checks, compare the curated and data-derived ontologies on (i) false-alarm rate for correct queries and (ii) catch rate for type swap faults. C2 requires both differences in the same direction, each with a five-percentage-point margin. 

**RQ1, C3** As checks, compare the curated ontology with the mean over the three masked LLM-generated ontologies on false-alarm rate, with a five-percentage-point margin. This is the central comparison. 

**RQ3, C1** As context, compare curated and data-derived ontologies on agents’ first-answer accuracy: C1a tests for a difference, pooled over the seven models, and C1b tests equivalence within ±3 accuracy points on Qwen3.8 and Sonnet, the two models fixed for it in advance, because a pooled equivalence could hide opposite effects in different models. 

**RQ3, C4** Compare the combined curated and data-derived checks with each check alone on net detection gain when wrong answers make up 25% of answers. 

**RQ3, C5** After a flag, compare the check’s specific message with a generic request to re-check on accuracy after one retry. C1a, C2 and C3 are two-sided tests, and C4 and C5 test for a gain. The margins are the smallest differences of interest; for C1b, and for C3 when read from its interval, they are equivalence bounds. 

We control the family-wise error rate at _𝛼_ = 0 _._ 05 with a weighted Holm procedure [12], with the most weight on C3, fixed in the preregistration from simulations without any test data and after an independent statistical review. A claim is significant by the weightedHolm decision on its calibrated _𝑝_ -value, written _𝑝_<sup>∗</sup> ; the unadjusted bootstrap _𝑝_ -values are in Appendix C.1. Non-significance establishes neither equivalence nor the absence of a benefit. Each test is a paired cluster bootstrap whose nominal level was calibrated on simulated data before the freeze, with the question as the unit of analysis. From the same simulations, C1b, C4 and C5 were declared in advance as expected to be inconclusive at their margins; we report them as bounds. Every other analysis is exploratory and labelled as such. Inference is conditional on the seven frozen question templates, the frozen artificial faults and the recipe for generating ontologies. Changes made after the freeze preserve comparisons within each model and graph and leave every registered decision unchanged; the Ontology-based Query Check, registered also on the artificial faults, was run on real answers only. 

# **4.7 Baselines** 

In addition to retrying when a query returns no rows, four comparators run in the same harness: (1) an LLM judge given the question, query, results, and answer, implemented by the agent’s own model for agent answers and by Claude Sonnet 5.5 and Haiku 5.5 for artificial faults; (2) SPARQL-LLM query validation [29], as published; (3) the Ontology-based Query Check rules [1], run from its paper’s printed rules; and (4) trivial checks that always or never flag. Results


<!-- page 6 -->

Orzechowski et al. 

are reported in the appendix. 

# **5 Results** 

We address the three research questions in turn, using the UniProt knowledge graph unless stated otherwise. The real answer analysis includes the first answers to 210 test questions from seven LLM models, with three attempts per question, involving 4,410 answers. Of these, 3,383 contained a query that could be checked. We calculate exploratory rates per answer, pooled across models. For artificial faults, we pool rates across 9,753 artificial faults that change the answer, and 3,630 correct queries. Confirmatory comparisons weigh questions equally with 95% confidence intervals from a paired cluster bootstrap over questions. 

# **RQ1: Curated checks raise more false alarms than data-derived and masked LLM-generated checks** 

RQ1 examines which errors each type of ontology catches when used as a check, how often it flags correct answers, and at what cost. The curated ontology raises more false alarms than both the data-derived ontology and the LLM-generated ontologies built from a summary with masked identifiers. On real agent answers, its flags are only marginally more precise than random flags. Table 2 reports catch and false alarm rates for each ontology on real agent answers and artificial faults. The first row shows a baseline that retries any query that returns no rows and does not require an ontology. Ontology-based checks only add value where they catch errors beyond this baseline. All checks read about the same number of triples per answer, so their costs mainly differ due to retries after a flag. The curated ontology check triggers more retries than the data-derived ontology check, incurring greater token usage and runtime (Appendix B.3). 

Exploratory results on real answers reveal trade offs between catching errors and flagging correct answers. The curated ontology catches more wrong answers than the data-derived and masked LLM-generated ontologies, but most of its flags concern correct answers, and its flags are right hardly more often than those of a random flag at the same rate (Table 3). The data-derived and masked ontologies flag fewer correct answers and are more likely to be right when they flag an answer, but each catches fewer than one in ten wrong answers. The three LLM-generated ontologies written from the original summary vary from one generation to the next: two catch few wrong answers, whereas the third catches more than the curated ontology but also flags far more correct answers (Table 2). 

All ontologies catch a smaller proportion of errors in real answers than in artificial faults. Most artificial faults produce empty query results, whereas almost all wrong agent answers return plausible results. Consequently, the empty result baseline catches few real wrong answers. Retrying flagged answers with the curated check’s specific feedback corrects more than a quarter of the flagged wrong answers but corrupts about one in a hundred flagged correct answers (Table 2). 

On the artificial faults, no single ontology catches as many faults as the retry on empty results, which raises no false alarm (Table 2). The two confirmatory comparisons for RQ1 are decided on the artificial faults, per question (Table 3). As checks, the data-derived 

ontology raises fewer false alarms on the control queries than the curated ontology and catches more type swaps, both by more than the registered 5-point margin (C2). The curated ontology also raises more false alarms than the mean of the masked LLM-generated ontologies, by more than the margin (C3). 

Two features of the design favour the data-derived ontology in C2. It is built from the graph on which the checks run, so it cannot flag a pattern that occurs at least five times in the data. The type swaps were also generated from its co-occurrence graph, so nearly all of them form patterns absent from the data, which executing the query would also reveal (Table 2). The difference in type swap catch rate arises from swaps four steps apart on the co-occurrence graph; for swaps two steps apart it is not established (exploratory; Table 3). A lower false-alarm rate does not by itself make a better check: the masked ontologies also catch fewer of the faults whose queries still return rows than either the curated or the data-derived ontology. 

Sonnet and Qwen3.8 are far less accurate on the human-written questions than on the generated ones, so these leave checks much more to catch. On the UniProt questions Sonnet’s curated check beats a random flag; on the Rhea questions it does no better than one (Appendix C.3). Among the comparators (Appendix C.2), an LLM judge, the agent’s own model reading the question, the query, the results and the answer, catches more wrong answers than either the curated or the data-derived ontology at a false-alarm rate similar to the curated check’s, and its flags are right more often than a random flag’s (Table 3). Acting on its flags was not beneficial: retries informed by the judge’s reason corrupted more flagged correct answers than they fixed wrong ones, unlike the curated check’s. Results per model and on the other graphs are in Appendices C.1 and C.4. 

Table 4 shows the distribution of artificial faults by class. The classes differ in how often the faulty query still returns rows, and so in how much a check can add to running the query. Invented identifiers and type swaps mostly do not return rows, so a retry on empty results already catches most of them; the ontologies differ mainly on type swaps. Constants swapped for others of the same type and changes of meaning mostly still return rows, and every ontology catches far fewer of them than a random flag at the curated check’s rate would. 

# **RQ2: Domain, range and declaration checks raise the curated ontology’s false alarms, and ontology checks miss changes of meaning** 

RQ2 asks what causes the false alarms and which errors the checks miss. The curated ontology’s false alarms come from its domain and range axioms and its requirement that every term be declared, and each curated ontology we studied disagrees with its own data; the curated, data-derived and masked ontologies catch none of the changes of meaning among the artificial faults. Evaluating the curated ontology one axiom type at a time (Table 2, the curated rows) shows that class membership and subsumption alone produce almost no false alarms; adding rdfs:domain and rdfs:range axioms raises them, and requiring every class and property in the query to be declared raises them the most. On real answers, domain and range checks flag correct and incorrect answers at similar rates,


<!-- page 7 -->

What Does an Ontology Catch? 

**Table 2: Each ontology as a check on UniProt, in %: real answers of seven models, and artificial faults. Bold, per column: the highest catch rate, precision and share fixed; the lowest false-alarm rate, share unknown and share corrupted.** 

|||Real answer|s||Artifi|icial faults|||
|---|---|---|---|---|---|---|---|---|
|Check from|catch|false alarm|unknown|catch, all|catch, rows returned|false alarm|precision at 25% wrong|fixed / corrupted|
|Retry on empty result (reference)|2.5|**0.1**|—|79.2|—|**0.0**|**100**|15.4 /**0.0**|
|Curated ontology, specific message|18.9|16.8|1.8|60.1|54.3|15.0|57.1|28.3 / 1.0|
|same flags, generic message|18.9|16.8|1.8|60.1|54.3|15.0|57.1|20.2 / 0.2|
|class checks only|3.1|0.6|—|17.0|—|1.1|83.4|—|
|class, domain and range|8.0|8.8|—|26.8|—|6.1|59.5|—|
|Data-derived ontology|8.2|3.5|1.6|75.6|62.1|9.7|72.3|7.0 / 1.0|
|LLM-generated, draw 1|6.7|3.2|2.0|54.5|46.7|1.2|93.7|11.4 / 24.2|
|LLM-generated, draw 2|8.6|6.6|1.9|57.1|47.5|6.3|75.3|13.3 / 12.7|
|LLM-generated, draw 3|**43.4**|24.3|1.5|69.6|53.7|29.4|44.1|**30.8**/ 6.0|
|LLM-generated, masked (three)|5.0|1.8|2.0|55.2–56.4|47.2–48.5|1.2–1.3|93.4–93.7|not run|
|Curated and data-derived combined|19.5|17.8|**1.4**|**80.0**|**67.3**|23.6|53.1|29.4 / 1.0|



**Table 3: Registered claims and exploratory comparisons on UniProt, in points, with 95% intervals; for the claims, the margin and the adjusted** _𝑝_ **(** _𝑝_<sup>∗</sup> **). Bold: established.** 

|Comparison|Estimate (95% CI)|Margin|_𝑝_<sup>∗</sup>|
|---|---|---|---|
|_RQ1: as checks, on artificial faults_||||
|C2: false alarms on controls, curated−data-derived|**+**8_._6**(6.0, 11.2)**<br>|5|0.013|
|type-swap catches, curated−data-derived|**−22.3 (−23.5, −21.0)**<br>|5||
|C3: false alarms on controls, curated −masked LLM-|**15.7 (13.7, 17.9)**|5|0.025|
|generated||||
|_RQ3: accuracy, and net detection for C4_||||
|C1a: context, curated−data-derived<br>|**−2.1 (−3.4, −0.9)**<br>|—|0.003|
|C1b: the same, Qwen3.8|−1.1 (−4.2, 1.9)<br>|±3|1.000|
|Sonnet|−0.8 (−2.7, 0.9)|±3||
|C4: combined−curated check<br>combined−data-derived check|−0.5 (−1.5, 0.4)<br>−10.6 (−12.2,−9.2)|1<br>1|1.000|
|C5: specific−generic message, per flagged answer|0.2 (−3.2, 3.1)|10|1.000|
|_Exploratory, no test_||||
|C2’s type swaps two steps apart|−1_._3(−2_._6, 0.1)|||
|C5 weighted by each model’s flags|+0_._7(−1_._2, 3.0)|||
|Real answers: precision−random flag, curated|+1_._6(−2_._3, 6.3)|||
|the same, LLM judge|+15_._8(12.5, 19.3)<br>|||
|Curated check: curated−data-derived in the prompt|−14_._3(−19_._9,−9_._3)|||
|Data-derived check: data-derived−curated in the prompt|−4_._8(−8_._7,−1_._0)|||



**Table 4: Catch rates by class of artificial fault on UniProt, in %. LLM-m: masked LLM-generated, mean of three; rand.: a random flag at the curated check’s rate. Bold: a random flag catches more than every ontology.** 

|Class|_𝑛_|no rows|cur.|data|LLM-m|rand.|
|---|---|---|---|---|---|---|
|Invented identifier|2,986|80.5|77.4|77.5|74.5|48.1|
|Type swap|6,413|80.0|55.3|78.4|49.9|48.0|
|Same-type constant|1,554|46.8|3.1|5.8|0.0|**47.9**|
|<br>Change of meaning|245|41.2|0.0|0.0|0.0|**44.9**|
|Correct items (false alarm)|3,630|0.0|15.0|9.7|1.2–1.3|—|



# **Table 5: Where a curated ontology, as published, disagrees with its own data.** 

|Graph<br>Disagreement|
|---|



UniProt Contradictions: up:maximum is declared xsd:float, but all 139 of its values are integers; 5 data properties declared functional have two distinct values for some subjects (82 entries for one property, 3,859 citations for four others). No instance of two disjoint classes. Rhea Omissions: 4 properties the data uses (between 15,032 and 90,295 times each) are not declared. Private 94.2% of triples use an identifier other than the ontology’s own, mostly renamings of declared terms; 19.9% use a term with no counterpart in it; 1.46% have a subject typed outside the property’s declared domain (a mismatch). 

**Table 6: Why checks go wrong, in a blind audit of a sample: the curated check’s false alarms by judged cause (top) and missed wrong answers by kind of error (bottom), counted where both annotators gave the same code, out of 32 and 64 items; Cohen’s** _𝜅_ **0.77 and 0.54.** 

|False alar|m undecl<br>term|ared<br>|closed<br>world|data clash|schem<br>too<br>narro|a<br>w<br>checker<br>defect|other|
|---|---|---|---|---|---|---|---|
|Curated|17||11|0|0|0|0|
|Missed|aggre-|wrong|filter or|path|shape|gold or<br>scorer|other|
||gation|con-<br>stant|scope|||ques-<br>tion||
|Answers|0|2|13|21|3|1<br>1|0|



so their flags are right no more often than random ones, while the flags from class membership and term declarations do better than random (Appendix D.1). In the curated and masked ontologies, disjointness axioms do not contribute to flags: neither the seven pairs of the curated ontology nor the 73 to 759 pairs added by the LLM in the masked ontologies flag any answer not already flagged by another axiom type. C3’s difference therefore rests on domain and range axioms and term declarations. The data-derived ontology’s checks are analysed in the same way in Appendix D.1. 

Table 5 shows where each curated ontology disagrees with its own data: with logical contradictions in UniProt, with omissions of properties the data uses extensively and the graph’s documentation describes in Rhea, and mostly through naming on the private graph, whose curated checks flag most correct answers (Appendix C.4). 

In a blind audit of a sample of the curated check’s false alarms, two annotators judged the cause of each (Table 6, top; Appendix D.2). Most came from a term the ontology does not declare and most of 

the rest from a closed-world reading, and every audited false alarm was indeed a correct answer. 

On the artificial faults, the curated, data-derived and masked ontologies catch none of the changes of meaning in Table 4 and few of the constants swapped for others of the same type, whereas a random flag at the curated check’s rate would catch many of both. One LLM-generated ontology built from the original summary catches 25.7% of the changes of meaning and 17.2% of the sametype swaps, but it also flags the most correct items (Table 2). An LLM judge, given the question, catches all 41 changes of meaning it judged (Appendix C.2). On real answers, two annotators blind to the model, the condition and the checks’ verdicts, coded a sample of the wrong answers that no check flagged (Table 6, bottom). Most missed wrong answers took a wrong path through the graph or a wrong filter or scope, and almost none could be flagged by a structural check even over a correct schema.


<!-- page 8 -->

Orzechowski et al. 

# **RQ3: Data-derived context does better; combining and specific messages show no gain** 

RQ3 asks whether the ontology improves performance beyond its use as a single check, and we examine three uses: providing the ontology as context to the agent, combining checks derived from two ontology sources, and including the check’s specific message when the agent retries a flagged answer. As context, the data-derived ontology gives higher accuracy than the curated one; combining the two checks shows no net gain in detection, and passing the check’s specific message to the agent no gain in accuracy, with intervals that bound any gain at a few points. Table 3 gives each estimate with its interval and registered margin. 

As context, the data-derived ontology yields higher accuracy than the curated ontology pooled over the seven models (C1a). Equivalence within 3 points is not established for Qwen3.8 and Sonnet, the two models fixed for it in advance (C1b). 

A net detection gain from combining the curated and dataderived checks is not established (C4). The combination catches more faults than either check alone but also raises more false alarms than either (Table 2), so it does no better than the curated check alone and worse than the data-derived check alone. 

The check’s specific message does not detectably improve on a generic request to re-check (C5), whether the seven models are weighted equally or by their flags. The specific message fixed more of the flagged wrong answers than the generic request, but also corrupted more of the flagged correct ones (Table 2). C1b, C4 and C5 were declared in advance as expected to be inconclusive, and we interpret them as bounds on the size of the effects, not as evidence that the effects are absent. 

A setting an agent developer is likely to deploy uses the dataderived ontology as context and the curated ontology as the check. On this configuration, the retry resulted in a small gain in accuracy, or none, for each of the seven models (exploratory; Appendix C.4). On the other graphs where retries were run the change was smaller or negative (Appendix C.4). 

Using the same ontology as context and as the check is associated with fewer catches (exploratory). The curated check catches fewer of the wrong answers produced with the curated ontology in the prompt than of those produced with the data-derived ontology in the prompt; the data-derived check shows the same pattern with the roles reversed, more weakly (Table 3). 

# **6 Discussion** 

_Implications for knowledge graph publishers._ Published, curated ontologies are not necessarily reliable as checks. On the published UniProt knowledge graph, ontologies derived from the data, either summarized directly or written by an LLM from masked identifiers at a cost of under one US dollar each (Appendix B.3), raised fewer false alarms than the curated ontology. These curated ontologies often disagree with the published data and knowledge graphs (Table 5), and these disagreements have direct consequences. Because checks require every class and property used in a query to be declared, each property missing from the ontology produces a false alarm on every correct answer that uses it. An ontology is a reliable check only if it declares every term its data uses and its axioms are satisfied by that data. The curated ontologies used in this study 

do not meet this standard, and a summary derived from the data itself is sufficient to reveal where they fall short. Publishers could therefore release summaries alongside the ontology, or directly use the summary to validate the ontology before each release. 

_Implications for agent developers._ For developers of agents, a check earns its place only on errors that running the query does not already reveal, so any check should be compared with a retry on empty results before it is deployed. False alarms deserve the same scrutiny as catches: static analyses at Google are required to keep effective false positives below 10% to retain developers’ trust [27], and a check that sends an agent to revise correct answers reduces trust in the same way. Measured comparably, as the proportion of a check’s flags that fall on correct answers, every ontology check and the LLM judge exceed this threshold by a wide margin on the agents’ answers to the generated questions, most of which are correct. On questions written by humans, where most answers are wrong, most flags fall on wrong answers. This proportion therefore depends on how often the agent errs, which is why we compare each check with a random check that flags the same proportion of answers. In the configuration a developer is most likely to deploy, with the data-derived ontology as context and the curated ontology as the check, retries improved accuracy slightly on UniProt, and yielded smaller gains or losses on the other graphs on which they were run (Section 5). An LLM judge detected more errors than either the curated or the data-derived ontology, but acting on its flags corrupted more correct answers than it fixed, and it requires a model call for every answer it checks, whereas an ontology-derived check requires none. 

_Limitations._ The confirmatory claims apply for UniProt’s frozen questions, artificial faults and ontologies. The other graphs show how far they extend. The LLM-generated ontologies were produced by a single model. Ontologies written by two open-weight models flag substantially more correct queries on average and vary widely between draws (Appendix B.2). On Rhea, whose curated ontology declares no domain, range or disjointness axioms, the curated check flags far more correct answers than on UniProt, whereas the dataderived ontology flags few (Appendix C.4). We do not report results on Rhea’s artificial faults, which were provisional and partly inspected during development. The difference between ontologies used as context that we observed on UniProt was not replicated on Rhea. Finally, the private graph is not publicly available, so its results cannot be independently reproduced, and no conclusion rests on it alone. 

# **7 Conclusion and Future Work** 

An ontology used to check an LLM agent’s answers is itself a judge that can be wrong, and we measured how: on the same answers and the same artificial faults, for a curated ontology, an LLM-generated one and one derived from the data, with every comparison fixed before any test answer was seen. The curated ontology raised more false alarms than the data-derived one and the LLM-generated ones written from masked names, and on real answers its flags were right hardly more often than random ones. Beyond checking, the dataderived ontology served the agents better as context, and neither combining the two checks nor passing the check’s specific message


<!-- page 9 -->

What Does an Ontology Catch? 

to the agent showed a gain. Our artificial faults let anyone measure a new check’s catches and false alarms without running an agent. 

Our measurements rely on knowing the correct answer to every question, and real use does not. We will apply these checks to agents that help biologists analyse a large knowledge graph of genomes, proteins and the computational predictions made about them, where no correct answer is known in advance and a flag is the only automatic sign that an answer may be wrong. The rates measured here will decide which checks such an agent runs, beside a new check that every value traces back to its source. 

# **Acknowledgments** 

This work is co-financed by the project of the Minister of Science and Higher Education (MEiN/2023/DIR/3796) and by the subvention assigned to AGH University of Krakow. We acknowledge ACK Cyfronet AGH (PLGINT/2026/020157, Gaia/AIF/101314359, LAIF/AIF/101234208) for providing computational resources. T.K. and R.T. are supported by the National Science Centre, Poland grant 2023/05/Y/NZ2/00080. 

Large language models are the subject of this study: they serve as the agents and the LLM judge, and they write the LLM-generated ontologies (Sections 3 and 4). They were also used as tools for experiment orchestration and design, data analysis, and copy-editing of the manuscript. All content was reviewed and validated by the authors.
