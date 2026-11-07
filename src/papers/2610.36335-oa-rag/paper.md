---
source: 2610.36335-oa-rag.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# OA-RAG: Ontology-based Agentic RAG for Faithful LLM Reasoning · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

# **OA-RAG: Ontology-based Agentic RAG for Faithful LLM Reasoning** 

Jiaoyan Chen The University of Manchester Manchester, United Kingdom jiaoyan.chen@manchester.ac.uk 

Yongsheng Gao SNOMED International London, United Kingdom yga@snomed.org 

Hui Yang The University of Manchester Manchester, United Kingdom hui.yang-2@manchester.ac.uk 



<!-- Start of picture text -->
(a) Formal Reasoning<br>INPUT / EVIDENCE<br>QUERY Axioms<br>𝐴 ⊑ 𝐵<br>𝐴 ⊑∃ 𝑟.𝐵 Exact<br>Answer<br>Formal Axioms Formal Reasoner<br>(Natural Language)<br>(b) Ontology-Grounded LLM Reasoning<br>WEB<br>ONTOLOGY<br>Axioms<br>Formal Axioms 𝐴𝐴 ⊑∃⊑ 𝑟.𝐵𝐵 + LLM Ontology-Grounded<br>𝐴 ⊑ 𝐵 Answer<br>Formal Informal LLM<br>𝐴 ⊑∃ 𝑟.𝐵 Axioms Annotations Reasoning<br>Informal<br>Annotations (c) Ontology-Assisted LLM Reasoning<br>• Definitions<br>• Comments + LLM LLM Ontology-<br>• Synonyms AssistedAnswer<br>Ontology LLM Parametric LLM<br>Evidence Knowledge Reasoning<br><!-- End of picture text -->

## **Abstract** 

Large language models (LLMs) perform well across many real-world tasks but remain prone to hallucination, limiting their reliability in domains such as biomedicine and healthcare, where answers must be grounded in established knowledge. Retrieval-augmented generation (RAG) mitigates this problem by incorporating external information, but often overlooks logical relationships and relies heavily on the LLM’s own reasoning, which can compromise answer faithfulness. We propose OA-RAG, an agentic framework that integrates formal reasoning with LLM reasoning, drawing on both the logical structure and informal annotations of domain ontologies. For each answer, OA-RAG reports the ontology observations used as evidence and a grounding level ( _entailed_ , _supported_ , _related_ , or _unrelated_ ) that characterises the evidence’s faithfulness. Across benchmarks derived from three large-scale ontologies and six real-world medical question-answering tasks, OA-RAG achieves the best overall performance among the evaluated ontology-finetuned and popular RAG methods, with particularly strong results on reasoning-intensive tasks. The reported grounding levels also offer a useful indication of answer reliability, with stronger grounding generally associated with higher accuracy. Finally, our results demonstrate the value of ontologies as knowledge sources: OA-RAG is competitive with, and sometimes outperforms, domain-specific RAG systems that draw on sources such as textbooks. 

**Figure 1: Three ontology-augmented LLM reasoning patterns, ordered from greatest to least faithfulness to the ontology: (a) the answer is can be inferred from the ontology’s formal axioms; (b) an LLM can infer the answer based on the ontology’s formal axioms and informal annotations; and (c) an LLM generates the answer freely, with optional grounding in relevant ontology content (classic RAG).** 

## **1 Introduction** 

Large language models (LLMs) have demonstrated strong capabilities across a wide range of knowledge-intensive tasks. However, their answers remain constrained by the knowledge encoded in their parameters and may contain hallucinations, that is, plausible but factually incorrect statements [19, 20]. Their reliability is further limited by the lack of transparent reasoning and by gaps in domain- or organization-specific knowledge. 

SNOMED CT [7], encode domain concepts and relations using Description Logic axioms, allowing dedicated reasoners to derive implicit relations soundly and efficiently [3]. Moreover, ontologies can contain rich textual annotations, including definitions and comments, providing informal but relatively important and complementary domain knowledge. This combination of formal semantics and textual annotations motivates our central question: 

Retrieval-augmented generation (RAG) augments LLMs by prompting with external evidence extracted from documents [9], tables [52], and knowledge graphs [31], while tool-using agents enable more adaptive, dynamic and autonomous access to such sources [32, 44, 49, 60]. However, existing methods mainly leverage textual and structured knowledge, leaving explicit logical knowledge under-utilised. Consequently, logical inference still relies heavily on the LLM’s internal reasoning, which can make its conclusions less faithful to the given knowledge. 

_Can ontologies bridge formal reasoning and LLM reasoning to produce more faithful answers to domain-specific questions?_ 

According to the knowledge used, answering domain-specific questions utilisng LLM and ontology may include the following three reasoning patterns, as illustrated in Figure 1: 

- _Formal reasoning_ : the answer is faithful to the ontology’s formal axioms and can be derived by a symbolic ontology reasoner. 

Meanwhile, many scientific and biomedical domains already provide rich shared, explicit and formal knowledge through ontologies in Semantic Web standards like Description Logic underpinned OWL (Web Ontology Language) [18, 46]. These ontologies on the Web, such as the Gene Ontology (GO) [1], FoodOn [8], and 

- _Ontology-grounded LLM reasoning_ : the answer is faithful to the ontology’s formal axioms and informal annotations (e.g., natural language labels and definitions), and requires an LLM for inference based on these ontology’s information.


<!-- page 2 -->

Yang et al. 

- _Ontology-assisted LLM reasoning_ : the answer is not faithful to the ontology, and the LLM reasoning relies on the LLM’s parametric knowledge as well. 

Importantly, the appropriate reasoning pattern is not known in advance and may vary across questions, requiring the system to adaptively select among the three reasoning strategies. 

To address this question, we propose OA-RAG, an agentic framework that combines ontology reasoning with LLM reasoning in three stages (§4): (1) pre-tool reasoning using the LLM’s parametric knowledge; (2) ReAct-based querying, where logical inference results and textual annotations are accessed via SPARQL; and (3) answer generation, which consolidates the evidence, and reports the ontology evidence supporting the answer with a grounding level (§4.1.3). Rather than treating the retrieved evidence as equally informative, the four levels distinguish evidence that logically entails the answer ( _entailed_ ), supports the answer without strictly entailing it ( _supported_ ), is merely relevant ( _related_ ) to the answer, or is irrelevant ( _unrelated_ ) to the answer. This reflects the answer’s faithfulness to the ontology, where entailed, supported and related correspond to formal reasoning, ontology-grounded LLM reasoning and ontology-assisted LLM reasoning in Figure 1, respectively. 

We developed an automatic procedure for constructing evaluation datasets for the first two patterns—formal reasoning and ontology-grounded LLM reasoning—using three large-scale, realworld ontologies: GO, FoodOn, and SNOMED CT. For the third pattern, we evaluated OA-RAG on six real-world medical questionanswering tasks following the experimental setup of OntoTune [29]. Our main contributions are as follows: 

- We propose trustful LLM reasoning based on ontology’s both formal and informal knowledge, and develop an ontology-based agentic RAG framework OA-RAG, which answers a domainspecific question with evidence and their grounding levels. 

- We formulate ontology-based faithful LLM reasoning in terms of three patterns with ranging faithfulness, and construct a QA benchmark with corresponding datasets for comprehensive evaluation. 

- OA-RAG achieves strong performance across all three reasoning patterns. On the first two patterns, it outperforms the strongest baseline by 10–15 percentage points on average (44.3% vs. 28.9% with Llama-3-8B-Instruct; 59.7% vs. 49.7% with Qwen3.5-9B). On the third pattern, it remains competitive with specialized medical QA methods while using 10× fewer tokens than the strongest baseline with Qwen3.5-9B (9.7k vs. 96.7k per question). 

# **2 Related Work** 

**_LLMs with external knowledge._** Retrieval-augmented generation (RAG) augments LLMs with external knowledge from diverse sources, including unstructured text [9] and structured sources such as tables [52] and knowledge graphs [31]. Domain-specific RAG has also received much attention, particularly in medicine [48, 54– 56, 59]. More recently, growing interest has focused on RAG agents that iteratively retrieve information throughout the reasoning process [21, 50, 56]. For example, in knowledge-base question answering [26], graph agents traverse knowledge graphs step by step [32, 49], often following the reasoning-and-acting paradigm of tool-using LLMs [39, 44, 60]. However, these methods still rely 

primarily on LLMs to reason over retrieved knowledge and may therefore be less faithful and trustworthy than our approach, which additionally incorporates formal reasoning. 

**_LLMs as interfaces to formal reasoning._** A prominent line of work combines LLMs with formal reasoning through neurosymbolic methods, which typically translate natural language into formal representations and delegate inference to symbolic engines. Examples include executing structured queries over knowledge bases [27, 30] and translating problems into logical forms for external solvers [35, 37]. Most existing methods, however, assume a fully symbolic problem representation, where either all premises are explicitly provided or the question is entirely expressible in the vocabulary of a knowledge base. In contrast, we study a hybrid setting in which the relevant premises span formal axioms, informal annotations, and the LLM’s parametric knowledge, and a question cannot necessarily be resolved by formal reasoning alone. 

**_LLMs and ontologies._** Language models have been studied for probing factual and ontological knowledge [16, 61], learning ontology embeddings [17, 57], reasoning over incomplete ontologies [58], and supporting ontology matching and learning [4, 14, 15]. Retrieval-based methods have also begun to exploit ontological structure: OG-RAG [45] and ORT [28] use ontologies to structure or constrain information retrieved from documents and knowledge graphs, respectively. OntoTune [29] and TaxoLLaMA [33] instead incorporate ontology knowledge into model parameters through fine-tuning. However, prior work has largely treated ontologies as sources of structured or textual knowledge, rather than as knowledge bases with both formal and informal knowledge as well as logical reasoning capabilities. To the best of our knowledge, none of the existing works explicitly integrates ontology-based logical reasoning with LLMs within an agentic framework. 

# **3 Preliminaries** 

An OWL ontology [18] represents domain knowledge using concepts (classes), relations (object properties), and logical axioms, whose semantics can be characterised by Description Logics (DLs). For the lightweight DL EL<sup>+</sup> , with concept names _𝐴_ ∈ NC and role names _𝑟_ ∈ NR, concepts are built by 

_𝐶_ ::= ⊤| _𝐴_ | _𝐶_ ⊓ _𝐷_ | ∃ _𝑟.𝐶_ 

and ontologies contain General Concept Inclusions (GCIs) contain General Concept Inclusions (GCIs) _𝐶_ ⊑ _𝐷_ , equivalences _𝐶_ ≡ _𝐷_ , and role inclusions _𝑟_ 1 ◦· · ·◦ _𝑟𝑛_ ⊑ _𝑟_ [2]. We write O |= _𝛼_ when the axiom _𝛼_ can be inferred from ontology O. For example, given Graduate ⊑ Student and Student ⊑∃affiliatedWith _._ Department, we have 

## O |= Graduate ⊑∃affiliatedWith _._ Department _._ 

OWL ontologies may additionally contain _annotations_ , such as rdfs:label and rdfs:comment, which provide lexical and descriptive information, including alternative labels, definitions, and crossreferences. Under OWL direct semantics, annotations do not affect DL entailments and are therefore ignored by DL reasoners. 

Given an OWL ontology, one can construct an RDF graph consisting of ( _subject, predicate, object_ ) triples and execute SPARQL 1.1 [13] queries over the graph to retrieve answers matching specified graph patterns. In particular, an axiom of the form _𝐴_ ⊑∃ _𝑟.𝐵_ , whether


<!-- page 3 -->

OA-RAG: Ontology-based Agentic RAG for Faithful LLM Reasoning 



<!-- Start of picture text -->
1. Pre-Tool Reasoning 2. ReAct with the Ontology Tool (Iterative Loop) 3. Answering<br>No<br>{} Output<br>Action<br>Answer option B<br>LLM reasoning Thought query(SPARQL) limit reached?Answer or Yes LLM answering Evidence E1 E2<br>Query Initial reasoning(without the (with the ontology tool)Planning & Reasoning DESCRIBE “<name>” ASK { ... } evidence digestfrom the clean entailed Grounding level supsu p portedorted ✓<br>ontology tool) SELECT ?x { ... } SELECT ?o / ?r { ... } related unrelated<br>Query fallback for an empty SELECT ?x<br>“An ontology is available<br>“Think step by step briefly toreason about the question...” through the tool below...” Step 1 “The and the tool observations phase is over. below, Using ...” the question<br>Ontology Step 2 “Your it. Now answer state what above it is rests final; on do ...” not change<br>Service Concept Cards Name Linking Formal Axioms Ontology Reasoner<br><!-- End of picture text -->

**Figure 2: Overall framework of OA-RAG: (1) pre-tool reasoning; (2) a ReAct loop of SPARQL queries to the ontology service (name linking, reasoner, query fallback); (3) answering from the evidence digest, with the cited evidence and a grounding level.** 

explicitly stated in the ontology or inferred by a DL reasoner, can be materialised as a class-level triple ( _𝐴,𝑟, 𝐵_ ). Ontology annotations can likewise be represented as triples in the same graph. SPARQL can then query both types of information using graph patterns with variables: SELECT returns variable bindings, ASK tests whether a matching pattern exists, and DESCRIBE returns an RDF description of selected resources. These SPARQL query patterns form the basis of OA-RAG. 

# **4 OA-RAG** 

We now present our main architecture, OA-RAG, illustrated in Figure 2. OA-RAG consists of two main components. The first is the core agentic framework, which follows a standard ReAct [60] architecture to answer a given question through iterative reasoning and tool interaction (§4.1). The second is the ontology service, which provides textual ontology representations and a backend that interfaces LLM-generated queries with ontology reasoners (§4.2). 

# **4.1 Main ReAct Architecture** 

As illustrated in Figure 2, OA-RAG adopts a reasoning-and-acting architecture [60] comprising three stages: (1) pre-tool reasoning, (2) iterative reasoning and acting with access to the ontology, and (3) answer generation. The full prompts are provided in Appendix E. 

_4.1.1 Pre-tool Reasoning._ Before entering the main ReAct loop, OA-RAG prompts the LLM to perform an initial analysis of the input context and question. Given a pre-tool reasoning prompt Ppre and a question _𝑞_ , the model M produces an initial reasoning state 



<!-- Start of picture text -->
ℎ 0 = M(Ppre ,𝑞 ) .<br><!-- End of picture text -->

The purpose of this stage is to encourage the LLM to reason first using only the information already available in the input context and, when that information is sufficient, to form a preliminary answer. In the subsequent stage, the ontology is introduced as an additional source of structured knowledge. The model can then use the ontology to retrieve information missing from the original context and to verify, refine, or revise the preliminary answer when one has been formed. 

_4.1.2 ReAct Loop._ Following the pre-tool reasoning stage, OARAG enters the main ReAct loop, in which the model can interact with an ontology tool to retrieve ontology information and invoke the corresponding reasoner. The loop continues within the same conversation. After producing the initial reasoning state _ℎ_ 0, the model receives an agent prompt Pagent as a new user turn, which introduces the available tool and specifies when it should be used. 

At iteration _𝑡_ , the model generates a single action _𝑎𝑡_ conditioned on the conversation history, including its previous actions and the corresponding observations returned by the ontology service (§4.2). Formally, 



<!-- Start of picture text -->
𝑎𝑡 = M � Ppre ,𝑞,ℎ 0 ,  Pagent ,  {( 𝑎 𝑗,𝑜 𝑗 )} 𝑗 <𝑡 � , 𝑜𝑡 = S( 𝑎𝑡 ) ,<br><!-- End of picture text -->

where S denotes the ontology service. The resulting observation _𝑜𝑡_ is appended to the conversation and becomes part of the context for the next iteration. This process repeats until the model produces a final answer or reaches the per-item interaction budget. 

**Agent Prompt** Pagent **(condensed)** 

An ontology is available through the tool below. Continue from your answer above. You can use tools of the form query(sparql) to execute SPARQL queries over ontology concepts and relations, including DESCRIBE, ASK, and SELECT queries. Use the ontology when the question concerns how its concepts are defined, classified, or related. For questions that do not depend on the ontology, answer using your own knowledge. 

_Action._ In OA-RAG, actions are expressed as SPARQL queries [13]. We support three types of queries: DESCRIBE, which retrieves detailed information about a concept; ASK, which checks whether a subsumption is entailed by the ontology reasoner; and SELECT, which retrieves concepts or relations satisfying specified conditions. The three action types are defined as follows: 

- (1) DESCRIBE "A": Given a concept name _𝐴_ , this query returns the concept card of _𝐴_ (§4.2.1): its names, definition, parents, children, stated relations, and other annotations. 

- (2) ASK {"A" "r" "B"}: This query checks whether the subsumption O |= _𝐴_ ⊑∃ _𝑟.𝐵_ holds. By setting _𝑟_ to "is a" or "subclass of", we can also check subsumptions of the form O |= _𝐴_ ⊑ _𝐵_ . The query returns Entailed if the entailment is verified by the


<!-- page 4 -->

Yang et al. 

ontology reasoner and Not Entailed otherwise. Importantly, under the open-world assumption, Not Entailed does not imply that the corresponding subsumption is false, since the ontology may be incomplete. We explicitly instruct the model about this distinction in the prompt. 

- (3) SELECT ?x WHERE {<conditions>}: This query retrieves concepts or relations that satisfy the specified conditions. For example, a condition of the form {?x " _𝑟_ " " _𝐵_ "} returns concept names _𝐴_ such that O |= _𝐴_ ⊑∃ _𝑟.𝐵_ . Similarly, {"A" "r" ?x} asks for concepts _𝐵_ such that O |= _𝐴_ ⊑∃ _𝑟.𝐵_ , while {"A" ?x "B"} returns relations _𝑟_ such that O |= _𝐴_ ⊑∃ _𝑟.𝐵_ . 

_Query fallback._ An exact SELECT ?x query may return no results, particularly in ontology-grounded LLM reasoning, where relevant information may appear only in informal annotations, which are inaccessible to the exact reasoner. To handle such cases, we introduce a query fallback. When a SELECT ?x query yields no matching concept, we retrieve the top- _𝑘_ candidate concepts by comparing the query against the concept cards (§4.2.1) using BM25 [43]. OARAG can then examine these candidates, inspect their associated information via DESCRIBE, and continue the ReAct loop. 

_4.1.3 Answering._ Finally, we introduce a dedicated answering step that constructs a clean context from the observations gathered during reasoning. It proceeds in two steps (Figure 2, stage 3). 

_Step 1: Answer._ We discard observations produced by failed or uninformative tool calls, such as execution errors and queries that return empty results. If the preceding ReAct loop has already produced a candidate answer, we retain it as a draft, denoted as _𝑦_ ˜ . Let _𝐸_ denote the observations retained after filtering (the _evidence digest_ ). The final answer is 



<!-- Start of picture text -->
M � Pfin ,𝑞, 𝐸, 𝑦 ˜ � if  𝐸 ≠ ∅ ,<br>𝑦 ˆ =<br>�M � Pown ,𝑞 � otherwise.<br><!-- End of picture text -->

We distinguish these two cases using separate prompts. When informative observations remain after filtering ( _𝐸_ ≠ ∅), Pfin instructs the model to answer using the question, the retained observations, and the draft. Otherwise, Pown asks the model to answer from its parametric knowledge. 

_Step 2: Evidence and grounding level._ When the observation set _𝐸_ is non-empty, we continue the Step 1 conversation with one more turn, the prompt Patt, to identify which observations its answer relies on and to assess the strength of their support: 



<!-- Start of picture text -->
( 𝐶, ˆ 𝑔 ˆ) = M � Step 1,  Patt , 𝐸 � ,<br><!-- End of picture text -->

where _𝐶_<sup>ˆ</sup> ⊆ _𝐸_ denotes the set of cited evidence and _𝑔_ ˆ denotes the grounding level. We distinguish four grounding levels: (1) _entailed_ , when the answer can be logically derived from the facts stated in the observations; (2) _supported_ , when the answer can be reasonably inferred from the observations, possibly in combination with the LLM’s parametric knowledge, but does not follow as a strict logical consequence; (3) _related_ , when the observations are relevant to the question but insufficient to determine the answer; and (4) _unrelated_ , when the observations are irrelevant to the question and the answer. Accordingly, we expect formal reasoning (Figure 1) to produce entailed answers; ontology-grounded LLM reasoning, entailed or supported answers; and ontology-assisted LLM reasoning, mostly 

related answers, although unrelated, supported, and entailed cases may also occur. Although it does not provide a formal guarantee of answer correctness, the reported grounding level reflects the model’s assessment of the extent to which the available evidence supports the answer and the answer is faithful to the ontology. 

# **4.2 Ontology Service** 

_4.2.1 Ontology Concept Cards._ To make the ontology accessible to the agent through standard text-based retrieval, we convert each concept into a _concept card_ , as illustrated below. Each card preserves the information in the ontology, with each item represented as a _key: value_ line using the property’s original label. The fields appear in a fixed order: the name, annotation definition, parents, children, stated relations, comments, and remaining annotations. All values are preserved as stated in the ontology, with three exceptions. The _parents_ and _children_ fields list the concept’s inferred direct parents and children, respectively<sup>1</sup> . The _stated relations_ field lists each pair ( _𝑟, 𝐵_ ) for which the ontology contains an axiom of the form _𝐴_ ⊑ ∃ _𝑟.𝐵_ ⊓ _𝐶_ or _𝐴_ ≡∃ _𝑟.𝐵_ ⊓ _𝐶_ , represented as “r -> B”. 

**Concept card for mitotic chromosome condensation (GO)** 

mitotic chromosome condensation **definition:** The cell cycle process in which chromatin structure is compacted prior to and during mitosis in eukaryotic cells. {database_cross_reference: GOC:mah, ...} **parents:** chromosome condensation; mitotic cell cycle process **children:** mitotic chromosome arm condensation; ... **stated relations:** part of -> mitotic cell cycle; ... **database_cross_reference:** Reactome:R-HSA-2299718 {rdfs:label: Condensation of Prophase Chromosomes}; ... **has_obo_namespace:** biological_process **id:** GO:0007076 

_4.2.2 Name Linking._ For a SPARQL query generated by OA-RAG to be executable by the ontology service, every concept and relation name in the query must be linked to an ontology entity. We first attempt exact matching; if this fails, we retrieve candidate entities for OA-RAG to inspect and use for query repair. The procedure is as follows: 

- _Exact match._ We first normalise each name (e.g., by standardising case, whitespace, and underscores) and match it against every given alternative name. If every name maps uniquely to an ontology entity, the query is executed directly. If a name matches multiple entities, it is marked as ambiguous, and the candidate entities are returned for further disambiguation. If a name cannot be matched to any ontology entity, we proceed to the fallback step. 

- _Unknown-name fallback._ For each concept or relation name that cannot be matched exactly, we return the five closest ontology names as candidate replacements. For concepts, we first retrieve a pool of 200 candidate names using BM25 and then rerank them by string similarity [41]. For relations, we match against the relation vocabulary directly. Given these suggestions, OA-RAG can revise the query using an appropriate ontology name or reformulate the query if none of the candidates is suitable. 

> 1 _𝐵_ is a direct parent of _𝐴_ if O |= _𝐴_ ⊑ _𝐵_ and there is no other concept _𝐵_ ′ such that O |= _𝐴_ ⊑ _𝐵_<sup>′</sup> ⊑ _𝐵_ . Direct children are defined analogously.


<!-- page 5 -->

OA-RAG: Ontology-based Agentic RAG for Faithful LLM Reasoning 

# **5 Dataset Construction** 

We construct evaluation datasets for the two reasoning patterns in which the ontology serves as the primary source of knowledge: _formal reasoning_ (§5.1) and _ontology-grounded LLM reasoning_ (§5.2). For ontology-assisted LLM reasoning, we do not construct a new dataset; instead, we reuse existing domain question answering benchmarks following [29], with details deferred to Section 6. 

# **5.1 Formal Reasoning** 

In the formal reasoning setting, we focus on the case where the answer to a question can be computed directly by ontology reasoning. Specifically, we consider two kinds of questions: (1) multiple-choice questions (MCQ), where options are given and several of them may be correct; and (2) open questions (OQ), which give no options, so that the LLM has to find the answers in the ontology itself. 

_5.1.1 MCQ Construction._ Our central idea is to construct questions directly from valid ontological subsumption statements by masking one component of each statement and treating the masked component as the prediction target. This process can be fully automated using an ontology reasoner. Specifically, given an entailed axiom 



<!-- Start of picture text -->
O |=  𝐴 ⊑∃ 𝑟.𝐵,<br><!-- End of picture text -->

we construct a query by masking either a concept, namely _𝐴_ or _𝐵_ , or the relation _𝑟_ . The masked symbol determines the reference answer, while additional concepts or relations are introduced as candidate options. 

First, we obtain the entailed axioms of the form O |= _𝐴_ ⊑∃ _𝑟.𝐵_ by exhaustively applying the following decomposition rule: 

## _𝐴_ ⊑ _𝐶_ ⊓∃ _𝑟.𝐵_ → _𝐴_ ⊑∃ _𝑟.𝐵, 𝐴_ ⊑ _𝐶_ 

to the asserted axioms in O. Here, _𝐴_ and _𝐵_ denote atomic concepts and _𝐶_ denotes an arbitrary, possibly complex, EL<sup>+</sup> -concept. Then, we mask _𝐴_ , _𝑟_ , or _𝐵_ to obtain questions. For each generated question, we construct six candidate options as follows. 

- When the masked answer is a concept, we randomly select 1–3 semantically valid concepts as correct options. If _𝐴_ is masked, the correct options are sampled from _𝐴_ and its descendants; if _𝐵_ is masked, they are sampled from _𝐵_ and its ancestors. To avoid selecting concepts that are overly general or overly specific, we restrict these candidates to those within a taxonomy distance of at most two from _𝐴_ or _𝐵_ , respectively. The remaining options are sampled from sibling concepts of _𝐴_ or _𝐵_ , with randomly sampled concepts used when there are insufficient siblings. 

- When the masked answer is a relation, the original relation is used as the correct option, and five distractors are sampled randomly from the other relations appearing in existential restrictions in the ontology. 

Finally, to ensure the correctness of the constructed query–answer pairs, we verify each candidate option with an ontology reasoner and replace any incorrectly labeled option. 

_5.1.2 OQ Construction._ We construct an OQ _𝑄_ by specifying _𝑛_ ≥ 2 conditions and asking for concepts that satisfy all of them. We restrict the search to the taxonomy branch rooted at a designated 

### **Example 1: A generated multiple-choice item (GO, filler masked)** 

**Source axiom.** _mesoderm formation_ ⊑∃ _part of . mesoderm morphogenesis_ . **Question.** _Which concept completes this statement about “mesoderm formation”: is part of [?]? Select the option or options that this ontology supports, and no option that is merely plausible._ **Options.** A mesoderm morphogenesis B tissue morphogenesis C morphogenesis of an epithelium D cartilage morphogenesis E fibrous ring of heart morphogenesis F muscle tissue morphogenesis **Gold.** A and B: the asserted filler and its parent _tissue morphogenesis_ 

### **Example 2: A generated open question (GO,** _𝑛_ = 2 **)** 

**Concept.** _negative regulation of receptor signaling pathway via STAT_ **Question.** _Find one or more biological processes in this ontology that satisfy all of these conditions: negatively regulates signaling; regulates cell surface receptor signaling pathway via STAT._ **Answer set.** _negative regulation of receptor signaling pathway via STAT_ ; _negative regulation of receptor signaling pathway via JAK-STAT_ ; _negative regulation of tyrosine phosphorylation of STAT protein_ . 

general concept _𝐴_ 0, that is, to concepts _𝐴_ such that O |= _𝐴_ ⊑ _𝐴_ 0.<sup>2</sup> An answer must additionally satisfy the relation restrictions ∃ _𝑟𝑖 .𝐵𝑖_ , for _𝑖_ = 1 _, . . . ,𝑛_ . Thus, _𝐴_ is an answer to _𝑄_ if 



<!-- Start of picture text -->
O |=  𝐴 ⊑ 𝐴 0 ⊓∃ 𝑟 1 .𝐵 1 ⊓· · · ⊓∃ 𝑟𝑛.𝐵𝑛.<br><!-- End of picture text -->

We generate OQs by first selecting a concept _𝐴_ in the target branch and then constructing query conditions that _𝐴_ is known to satisfy. Specifically, for each concept _𝐴_ such that O |= _𝐴_ ⊑ _𝐴_ 0, we first collect relation restrictions known to hold for _𝐴_ , and then sample _𝑛_ mutually non-subsuming restrictions as the query conditions. Since all selected conditions hold for _𝐴_ , the resulting OQ is guaranteed to have at least one answer. Appendix C gives the details. 

# **5.2 Ontology-Grounded LLM Reasoning** 

Ontology-grounded LLM reasoning targets questions that can be answered using information contained in the ontology but cannot be solved by an ontology reasoner alone. In such cases, part of the information required to answer the question is not represented as formal axioms, but instead appears in other forms, such as annotations of natural language comments and definitions. Answering these questions therefore requires combining textual evidence with the remaining logical structure of the ontology. 

To construct a dataset for this setting, we reuse the same questions, options, gold answer sets, answer schemas, and sample identifiers, while replacing the original ontology with a deterministically revised version, as described below. The key idea is to move part of the information encoded in logical axioms into the concepts’ natural-language definitions. As a result, the revised ontology still contains sufficient information to answer the questions when both its textual and logical content are considered, while an ontology reasoner operating only on the remaining formal axioms can no longer recover all required information. 

The ontology is revised as follows. For every asserted axiom with a named concept on the left-hand side, we remove its existential 

> 2For example, _𝐴_ 0 is _biological process_ in GO, _food product_ in FoodOn, and _Clinical finding_ in SNOMED CT.


<!-- page 6 -->

Yang et al. 

**Table 1: Overall accuracy (%). Average: mean across the three tests after within-test averaging.**<sup>†</sup> **: from OntoTune [29]. (262k): full 262k-token context. Red / blue: best / second best.** 

|**Method**|**Know**<br>**So**|**ledge**<br>**urce**|**Tes**<br>(**for**|**t 1**<br>**mal**)|**T**<br>(**ontolog**|**est 2**<br>**y-grounde**|**d**)||**Test**<br>(**ontology-**|**3**<br>**assisted**)|||**Average**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||ont|doc|MCQ|OQ|MCQ|OQ|PubMedQA|MedQA|MedMCQA|USMLE 1|USMLE 2|USMLE 3||
||||||||_Base LLMs_|||||||
|Llama-3-8B-Instruct|–|–|45.1|7.8|45.4|8.1|70.3<sup>†</sup>|51.7<sup>†</sup>|51.7<sup>†</sup>|57.4<sup>†</sup>|52.3<sup>†</sup>|58.2<sup>†</sup>|36.7|
|Qwen3.5-9B|–|–|56.4|8.3|56.7|8.6|72.2|78.3|68.1|86.2|82.6|89.3|48.2|
|||||_O_|_ntology Fi_|_ne-Tuned L_|_LMs (Backbone: L_|_lama-3-8B_|_-Instruct)_|||||
|OntoTune-sft|–|–|44.4|11.2|44.7|11.5|72.0<sup>†</sup>|51.5<sup>†</sup>|56.7<sup>†</sup>|57.4<sup>†</sup>|54.1<sup>†</sup>|60.7<sup>†</sup>|38.2|
|OntoTune-dpo|–|–|46.4|6.5|46.8|6.7|65.5<sup>†</sup>|53.3<sup>†</sup>|57.2<sup>†</sup>|58.5<sup>†</sup>|51.4<sup>†</sup>|59.0<sup>†</sup>|36.9|
|OntoTune-sft+dpo|–|–|45.6|9.8|45.9|10.1|66.3<sup>†</sup>|51.9<sup>†</sup>|56.7<sup>†</sup>|53.2<sup>†</sup>|54.1<sup>†</sup>|63.1<sup>†</sup>|37.8|
|TaxoLLaMA<sup>∗</sup>|–|–|–|–|–|–|73.4<sup>†</sup>|50.5<sup>†</sup>|46.1<sup>†</sup>|42.6<sup>†</sup>|39.4<sup>†</sup>|47.5<sup>†</sup>|–|
|||||_Pr_|_ompting an_|_d RAG Me_|_thods (Backbone:_|_Llama-3-8_|_B-Instruct)_|||||
|CoT|–|–|38.2|3.0|38.5|3.1|67.7|55.6|55.3|64.9|64.2|64.8|34.5|
|RAGont(text)|✓|–|50.9|3.0|53.4|4.6|65.5|51.7|51.8|56.4|56.9|57.4|37.5|
|RAGont(query)|✓|–|45.3|10.0|42.6|2.4|64.8|55.6|54.5|62.8|57.8|63.9|36.7|
|RAGdoc(text)|–|✓|43.0|2.8|43.3|2.9|61.6|54.0|55.5|56.4|55.0|55.7|34.1|
|MedRAGdoc|–|✓|40.0|5.7|40.3|5.8|77.0|55.1|55.7|64.9|55.0|59.0|35.7|
|ReActont|✓|–|45.0|9.8|48.1|12.5|67.6|54.8|53.3|63.8|51.4|63.9|38.9|
|i-MedRAGdoc|–|✓|38.7|0.5|38.8|0.5|66.0|61.6|56.2|78.7|64.2|61.5|34.6|
|**OA-RAG**|✓|–|62.0|45.0|52.2|18.0|71.6|57.6|57.4|66.0|56.9|67.2|50.5|
||||||_Promptin_|_g and RAG_|_Methods (Backb_|_one: Qwen_|_3.5-9B)_|||||
|CoT|–|–|61.1|12.7|61.4|13.0|76.4|82.4|69.0|89.4|87.2|90.2|52.2|
|RAGont(text)|✓|–|68.7|18.2|69.1|20.1|72.6|84.4|70.4|91.5|82.6|89.3|56.6|
|RAGont(query)|✓|–|68.2|26.2|56.9|5.8|75.5|84.8|71.2|91.5|88.1|86.9|53.8|
|RAGdoc(text)|–|✓|61.0|5.3|61.3|5.3|74.5|82.6|71.5|91.5|81.7|84.4|49.1|
|MedRAGdoc|–|✓|58.9|0.5|59.2|0.5|79.3|81.1|70.5|94.7|79.8|82.8|47.0|
|ReActont|✓|–|69.2|31.5|65.3|32.9|75.4|84.7|72.1|91.5|88.1|86.9|60.9|
|i-MedRAGdoc|–|✓|40.1|0.5|40.4|0.5|71.2|69.8|66.4|73.4|65.1|54.1|35.8|
|i-MedRAGdoc(262k)|–|✓|40.9|1.0|41.2|1.0|77.2|88.6|72.9|94.7|91.7|86.1|42.4|
|<br>**OA-RAG**|✓|–|79.9|62.0|73.7|23.2|77.0|86.3|71.7|94.7|91.7|87.7|68.1|



restrictions from the logical layer. Specifically, 



<!-- Start of picture text -->
𝐴 ⊲⊳ 𝐷 ⊓ � 𝑚 𝑖 =1 ∃ 𝑟𝑖 .𝐶𝑖 with ⊲⊳ ∈{⊑ ,  ≡} , ↦−→ 𝐴 ⊑ 𝐷.<br><!-- End of picture text -->

If no logical content remains, i.e., _𝐷_ = ⊤, the revised axiom is removed entirely. Each removed restriction ∃ _𝑟𝑖 .𝐶𝑖_ is then verbalised [16] and appended to the annotation definition of _𝐴_ (a definition is added if _𝐴_ has none). We further verify that each question from Section 5.1 is answerable from the revised axioms combined with the informal annotations, but not from the axioms alone, and exclude 23 questions that fail these criteria (detailed in Appendix C). 

# **6 Evaluation** 

# **6.1 Experimental Setup** 

**Benchmarks.** We apply the procedure of Section 5 to three widely used ontologies that differ in scale, terminology, and modeling conventions: GO [1], FoodOn [8], and SNOMED CT [7], and created 300 MCQs and 200 OQs per ontology (see Appendix C for details). **Test 1** 

(formal reasoning) asks these 1,500 questions against the source ontologies. **Test 2** (ontology-grounded LLM reasoning) ask 1,477 questions against the revised ontologies. **Test 3** (ontology-assisted LLM reasoning) follows OntoTune [29]: 6,781 single-answer test questions from MedQA [22], USMLE Step 1/2/3 [12], MedMCQA [36], and PubMedQA [23], with SNOMED CT as the underlying ontology. 

**Baselines.** Besides the base LLMs, Llama-3-8B-Instruct [11] and Qwen3.5-9B [40] (hereafter Llama and Qwen, respectively), we evaluate the following two categories of baselines: 

- _Ontology fine-tuned LLMs._ We include the three released OntoTune variants (sft, dpo, and sft+dpo) and TaxoLLaMA<sup>∗</sup> , OntoTune’s non-public re-implementation of TaxoLLaMA [33]; all four are fine-tuned to integrate SNOMED CT knowledge into Llama, and the Test 3 results of the Llama-based models (marked with †) are quoted from OntoTune. 

- _Prompting and retrieval methods._ We consider standard chainof-thought (CoT) prompting [53] and four retrieval-augmented methods: RAG, ReAct [60], MedRAG [55], and i-MedRAG [56]. We consider two retrieval sources: **(1)** ont, the ontology concept cards introduced in Section 4.2.1, and **(2)** doc, comprising the


<!-- page 7 -->

OA-RAG: Ontology-based Agentic RAG for Faithful LLM Reasoning 



<!-- Start of picture text -->
entailed supported related unrelated entailed supported related unrelated<br>Llama Llama<br>Test 1 Test 1 61.8 (m=1251) 24.8 (m=117) 7.7 (m=13) 0.0 (m=1)<br>Test 2 Test 2 45.3 (m=811) 29.6 (m=402) 5.4 (m=37) 50.0 (m=2)<br>Test 3 Test 3 61.3 (m=2843) 58.2 (m=1408) 45.5 (m=44) 52.6 (m=19)<br>Qwen Qwen<br>Test 1 Test 1 83.0 (m=1257) 34.5 (m=116) 0.0 (m=19) 33.3 (m=3)<br>Test 2 Test 2 75.1 (m=924) 40.7 (m=209) 0.0 (m=133) 0.0 (m=23)<br>Test 3 Test 3 94.9 (m=59) 82.1 (m=2630) 54.3 (m=35) 66.4 (m=738)<br>0 25 50 75 100<br>(a) Grounding level percentage (%) (b) Answer accuracy (%)<br><!-- End of picture text -->

**Figure 3: Grounding levels reported by OA-RAG. (a) Percentage of all questions at each level; note that a part of answers have no grounding levels. (b) Answer accuracy within each grounding level;** _𝑚_ **is the number of corresponding questions.** 

medical textbooks [22] and StatPearls [47] used by MedRAG and i-MedRAG. For RAG, we evaluate both doc and ont as retrieval sources with textual retrieval, RAGdoc(text) and RAGont(text), as well as a structured query variant, RAGont(query), which replaces textual retrieval with a single SPARQL query as in OARAG. ReActont uses ont, while MedRAGdoc and i-MedRAGdoc use doc. In particular, i-MedRAG can be viewed as a medically specialized variant of ReAct. Implementation details are provided in Appendices A and B. 

For a fair comparison, we use an 8,192-token context window for all methods, matching the maximum supported by Llama. We also report i-MedRAGdoc on Qwen with a 262k-token window, as its performance degrades markedly under the shorter context. 

**Metrics.** We report accuracy (%) of the all tested questions. An MCQ question is correct if the predicted set of options exactly matches the gold set. An OQ is correct if the response is non-empty and entirely correct. 

# **6.2 Main Results** 

The overall results are shown in Table 1. For methods that do not use the ontology, the Test 2 results are directly reused from Test 1. The slight performance differences are due to the 23 excluded questions described in Section 5.2. 

OA-RAG achieves the best average accuracy with both backbones (50.5% and 68.1%). On **Tests 1 (formal reasoning)** and **Tests 2 (ontology-grounded LLM reasoning)** , OA-RAG outperforms all baselines in every setting except two: the Test 2 MCQs with Llama (RAGont(text), 53.4% vs. 52.2%) and the Test 2 OQs with Qwen (ReActont, 32.9% vs. 23.2%). This is consistent with the fact that these tasks are constructed directly from ontologies and require reasoning over explicit ontological knowledge. Notably, two of the ontology fine-tuning methods, OntoTune-sft and OntoTunesft+dpo, slightly improve over their base model on the OQs (e.g., from 7.8% to 11.2% on Test 1 for OntoTune-sft), indicating that ontology knowledge can be partially internalised through finetuning. In contrast, medical RAG methods such as MedRAGdoc and i-MedRAGdoc fall below the base model on the OQs with both backbones, and on the MCQs too, except for MedRAGdoc with Qwen. These results suggest that existing medical RAG methods may struggle when questions require explicit logical reasoning and to be answered with high faithfulness to the ontology rather than primarily retrieving relevant evidence. 

On **Test 3 (ontology-assisted LLM reasoning )** , OA-RAG remains competitive with the best-performing baseline, i-MedRAGdoc. However, with Qwen, i-MedRAGdoc (262k) requires a substantially larger retrieval and generation budget (about 4× the LLM calls and 10× the tokens per question of OA-RAG: 22 vs. 5.8 calls and 96.7k vs. 9.7k tokens, counting the input and generated tokens of all LLM calls of a question). Most of the difference lies in the retrieved text that the model reads, which is about 66× larger for i-MedRAGdoc, and i-MedRAGdoc also generates about 5× as many tokens (Appendix A). Moreover, when restricted to the same 8,192-token context window as OA-RAG, its average Test 3 accuracy drops markedly to 66.7%, compared with 84.9% for OA-RAG. We further find that RAGont(text) outperforms RAGdoc(text) on Test 3 with both backbones, and outperforms MedRAGdoc with Qwen. These findings highlight the potential of ontologies as retrieval sources: compared with medical textbooks, ontologies provide more concise and structured knowledge, which may also benefit real-world QA tasks in related domains. 

Beyond answer accuracy, OA-RAG reports the **grounding level** of each answer (§4.1.3). **Figure 3a** shows the distribution of grounding levels in the final outputs. Because some answers lack grounding annotations (e.g., when no evidence is available), the percentages do not sum to 100%. Entailed and supported answers dominate, accounting for 70.0% of all questions for Llama and 53.2% for Qwen, whereas unrelated answers are rare, comprising only 0.2% for Llama and 7.8% for Qwen. **Figure 3b** shows that, among answers labeled _entailed_ , _supported_ , or _related_ , stronger reported grounding is generally associated with higher accuracy. For example, with Qwen on Test 3, 94.9% of _entailed_ and 82.1% of _supported_ answers are correct (together accounting for 39.7% of the questions), compared with 72.1% of the remaining answers. The reported grounding level therefore provides a useful signal of answer reliability beyond the answer itself. Note that _unrelated_ answers are unsuitable for direct comparison, as they tend to arise from questions that are less closely aligned with the scope of the ontology. For example, some may depend primarily on reading comprehension or calculation rather than ontology-based reasoning, making their accuracy more reflective of the LLM’s general capabilities. 

# **6.3 Analysis** 

_6.3.1 Evidence Retrieval and Selection._ Unlike the grounding level, the _gold evidence_ can be traced directly from the ontology for Tests 1 and 2, allowing us to evaluate exactly whether the required evidence


<!-- page 8 -->

Yang et al. 



<!-- Start of picture text -->
Gold evidence retrieved: completely partly not at all<br>Retrieved evidence output: fully not fully<br>MCQ 64.1 29.6 31.7 13.3 55.0<br>OQ 36.8 8.0 55.2 99.0<br>MCQ 81.3 14.1 69.6 18.7 11.7<br>OQ 47.2 22.5 30.3 9.3 24.7 66.0<br>Test 1 (formal reasoning) Test 2 (ontology-grounded LLM reasoning)<br>Llama<br>Qwen<br><!-- End of picture text -->

**Figure 4: Ratio of questions whose gold evidence is retrieved and selected (%).** 

is retrieved and subsequently cited (Figure 4). The results suggest that retrieval, rather than reasoning over retrieved evidence, is the primary bottleneck. MCQs achieve a substantially higher rate of fully retrieved gold evidence than OQs (61.7 vs. 23.6% over all items), which is reasonable as the candidate answer options provide additional cues that constrain retrieval. Moreover, once the relevant evidence is retrieved, it is usually among the observations cited for the answer (95.1–98.4% of the MCQs and at least 77.8% of the OQs). Qwen also demonstrates a substantially stronger ability than Llama to retrieve useful evidence. Nevertheless, both models perform poorly on Test 2 OQs. This is expected because much of the relevant information in Test 2 is encoded in definitions and is therefore less directly accessible to the retrieval process. The absence of candidate options in OQs further increases the difficulty of identifying the relevant evidence. 

_6.3.2 Ablation Study._ To analyse the contribution of each component, we report an ablation study in Table 2. Across both backbones, adding the ReAct loop and the final answering step consistently improves over pre-tool reasoning alone, with the largest gains on the first two test patterns (59.7 vs. 36.5% on Tests 1–2, with Qwen). This highlights the importance of ontology-grounded reasoning through SPARQL queries when the answer depends on structured ontology knowledge. The final **answering step** provides a further consistent gain (68.1 vs. 65.2% on average, with Qwen), showing that synthesizing the intermediate reasoning and retrieved evidence remains important even after tool use. The **query fallback** exhibits a more nuanced trade-off. While it improves overall performance (68.1 vs. 67.7% on average, with Qwen), removing it can benefit some settings, such as Test 1 MCQs, likely because doing so avoids introducing less targeted retrieval when the structured ontology is already sufficient. 

_6.3.3 Case Study._ Figure 5 illustrates a common correction pattern: the model’s pre-tool answer is plausible but based on a loose association, whereas the ontology provides an explicit relation that directly supports the correct option. In case (a), the model attributes the liver injury to hemolysis after the transfusion, whereas the ontology describes _Halothane hepatitis_ as a drug-induced hepatitis whose causative agent is halothane, leading to A. In case (b), the model associates _blind staggers_ with molybdenum, while the ontology identifies it as an alternative name for _Selenium poisoning_ and directly links the condition to selenium, leading to C. These cases show that the tool phase is most useful when the ontology 

**Table 2: Ablation of OA-RAG (accuracy %): each indented row changes one component;** ↓ **: drop of percentage points over the original OA-RAG.** 

|**Variant**|**Tes**|**t 1**|**Te**|**st 2**|**Test 3**|**Ave**|**rage**|
|---|---|---|---|---|---|---|---|
||MCQ|OQ|MCQ|OQ||||
|_Backbo_|_ne: Lla_|_ma-3-_|_8B-Inst_|_ruct_||||
|OA-RAG|62.0|45.0|52.2|18.0|62.8|50.5||
|pre-tool reasoning only|43.4|4.8|43.8|4.5|61.9|36.7|↓13.8|
|w/o answering step|57.3|38.7|48.0|7.9|58.1|44.7|↓5.8|
|w/o query fallback|62.1|42.7|52.6|9.3|62.8|48.7|↓1.8|
|_Ba_|_ckbone:_|_Qwe_|_n3.5-9B_|||||
|OA-RAG|79.9|62.0|73.7|23.2|84.9|68.1||
|pre-tool reasoning only|63.6|9.2|63.9|9.4|84.7|52.6|↓15.5|
|w/o answering step|78.0|54.0|73.3|16.5|84.7|65.2|↓2.9|
|w/o query fallback|80.4|61.7|75.8|17.8|85.1|67.7|↓0.4|





<!-- Start of picture text -->
(a) The ontology names halothane as the causative agent MedQA<br>Q:  Five days after undergoing an emergency appendectomy under general inhalational<br>anesthesia ... she received a transfusion of 1 unit of packed red blood cells ... Examination<br>shows jaundice ... Eosinophils 13% ... A biopsy of the liver shows massive centrilobular<br>necrosis. Which of the following is the most likely underlying cause ...?<br>(A) Adverse effect of anesthetic (B) Gram negative bacteria in the bloodstream<br>(C) Trauma to the bile duct (D) Acalculous inflammation of the gallbladder<br>(E) Excessive lysis of red blood cells<br>Pre-tool:  “... The hemolysis releases free hemoglobin, which is toxic to the liver ...” ⇒ E ✗<br>Tool phase  (call 4 of 4):<br>4. DESCRIBE "Halothane hepatitis"<br>→ Halothane hepatitis . . . parents: Drug-induced hepatitis; Poisoning<br>caused by halothane . . . stated relations: . . . ; Causative agent -><br>Halothane; Finding site -> Liver structure<br>Answer:  “... is diagnostic of Halothane hepatitis, which is an adverse effect of the anesthetic” ⇒<br>A ✓<br><!-- End of picture text -->



<!-- Start of picture text -->
(b) The ontology maps blind staggers to selenium MedMCQA<br>Q:  Poisoning by which of these elements causes blind staggers alkali disease in livestock?<br>(A) Magnesium (B) Manganese<br>(C) Selenium (D) Molybdenum<br>Pre-tool:  “... Molybdenum: Toxicity (or high levels relative to sulfur/copper) is the direct cause<br>of the condition described as alkali disease leading to blind staggers” ⇒ D ✗<br>Tool phase  (calls 1 and 3 of 3):<br>1. DESCRIBE "blind staggers"<br>→ Selenium poisoning . . . stated relations: Causative agent -> Selenium;<br>skos:altLabel: Alkali disease; Blind staggers<br>3. ASK { "blind staggers" "Causative agent" "Selenium" }<br>→ every Selenium poisoning is related by Causative agent to some Selenium:<br>ENTAILED<br>Answer:  “... The provided observations explicitly link ‘Selenium poisoning’ with the alternative<br>labels ‘Alkali disease’ and ‘Blind staggers’ and identify Selenium as the causative agent” ⇒ C ✓<br><!-- End of picture text -->

## **Figure 5: Two Test 3 trajectories of OA-RAG (Qwen), with intermediate reasoning omitted for brevity.** 

contains a direct, question-relevant relation that can override an incorrect model association. 

# **7 Conclusion** 

We presented OA-RAG, which, to our knowledge, is the first agentic RAG framework that combines LLM reasoning with formal OWL ontology reasoning. It can adaptively address three distinct


<!-- page 9 -->

OA-RAG: Ontology-based Agentic RAG for Faithful LLM Reasoning 

reasoning patterns: formal reasoning, ontology-grounded LLM reasoning, and ontology-assisted LLM reasoning. Experiments across all three patterns with QA over three large-scale real-world ontologies demonstrate its strong and consistent performance. They also show that ontologies provide an effective and efficient knowledge resource, with competitive performance but substantially fewer input and generated tokens in comparison with textual resources. 

For future work, we plan to extend OA-RAG toward agentic web that coordinates knowledge across multiple ontologies, supporting more complex questions that require reasoning across domains.
