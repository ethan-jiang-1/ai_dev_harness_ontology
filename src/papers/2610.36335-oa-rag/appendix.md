---
source: 2610.36335-oa-rag.pdf
part: appendix
converted: 2026-11-07
converter: pymupdf4llm
---

# OA-RAG: Ontology-based Agentic RAG for Faithful LLM Reasoning · 附录

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

# **A Implementation Details** 

**Agent and service.** For each item, OA-RAG allows up to 10 tool actions and 5,000 generated tokens across pre-tool reasoning, the ReAct loop, and Step 1 of answering, plus 512 tokens for Step 2. The ontology service decides ASK and SELECT queries over the entailment closure of the ontology, precomputed with the OWL EL reasoner Whelk [5] and stored in Oxigraph [38]; the datasets are built and checked with ELK [25] and HermiT [10]. 

**Cost.** On Test 3 with Qwen, OA-RAG uses 9.7k tokens per question over 5.8 LLM calls on average, including 7.9k input tokens (1.0k from ontology observations) and 1.8k generated tokens. In contrast, i-MedRAGdoc (262k) uses 96.7k tokens over 22.0 calls, including 87.8k input tokens (63.6k from retrieved documents) and 8.9k generated tokens. 

**Tool calls** (Figure 6). Query choice varies systematically with question type and model. On the OQs of Tests 1 and 2, Llama relies almost exclusively on SELECT (97% of calls), whereas Qwen primarily uses DESCRIBE (56%). On the MCQs, Llama divides its calls between ASK and SELECT (40–45% each), while Qwen again favors DESCRIBE (49–53%). On Test 3, Llama averages 4.9 calls per question, 

split evenly between ASK and SELECT (40 and 42%), whereas Qwen averages 2.0 calls and uses DESCRIBE for 84% of them. 

# **B Retrieval and Document Baselines** 

The retrieval baselines differ primarily in their knowledge source: RAGont(text), ReActont, and the ablation search tool retrieve ontology concept cards, whereas RAGdoc(text), MedRAGdoc, and i- MedRAGdoc retrieve medical documents. 

**Ontology retrieval.** Each field of a concept card (§4.2.1) forms a retrieval unit, grouped by type (names, definitions, etc.). Units are retrieved using BM25 [43] and sentence embeddings (all-MiniLM-L6-v2 [42, 51]), with the resulting rankings combined by reciprocal rank fusion [6]; each concept is scored according to its highest-ranked unit. RAGont(text) performs a single retrieval using the question and answer options, then inserts the top-5 concept cards together with the top-5 verbalized axioms retrieved using the same scoring procedure. ReActont uses the same underlying retrieval mechanism as RAGont(text) but each search returns the top-5 concepts, each with only the field that matched rather than its complete concept card, followed by the top-5 matching verbalized axioms. Unlike RAGont(text), ReActont generates search queries dynamically using the LLM. The search tool used in our ablation study follows the same approach. 

**Document baselines.** Following i-MedRAG, we use MedCPT [24] to retrieve from medical textbooks [22] and StatPearls [47]. RAGdoc(text) replaces ontology cards with the top-5 retrieved snippets. Under their standard settings, MedRAGdoc [55] answers from 32 snippets in a single call, while i-MedRAGdoc [56] issues three follow-up queries in each of four rounds. Both are run with the authors’ toolkit using a 7,168-token document budget, with a forced answer when the response reaches the context-window limit [34]. 

**Results by source ontology** (Table 3). OA-RAG achieves the best performance in 19 of the 24 settings, one of them tied. In the other five, it falls behind RAGont(text) (with Llama on the Test 2 GO and FoodOn MCQs, 53.7 vs. 55.7% and 46.8 vs. 51.8%) or ReActont (on three Test 2 OQ settings); the largest gap is on the Test 2 GO OQs with Qwen (22.0 vs. 42.0%), mainly because Qwen’s exact queries rarely retrieve a correct concept there (for 15 of the 200 questions, vs. 106 on Test 1), so it gives no answer to 62.5% of them. 



<!-- Start of picture text -->
DESCRIBE ASK SELECT<br>Test 1 MCQ 3.6<br>Test 1 OQ 3.8<br>Test 2 MCQ 4.8<br>Test 2 OQ 4.9<br>Test 3 4.9<br>Test 1 MCQ 2.2<br>Test 1 OQ 4.5<br>Test 2 MCQ 3.3<br>Test 2 OQ 6.1<br>Test 3 2.0<br>0 2 4 6<br>Llama<br>Qwen<br><!-- End of picture text -->

**Figure 6: Tool calls of OA-RAG per question by query form (SELECT: all its variants). Test 3 pools its six sets.**


<!-- page 11 -->

OA-RAG: Ontology-based Agentic RAG for Faithful LLM Reasoning 

**Table 3: Test 1 and Test 2 accuracy (%) by source ontology. Red / blue: best / second best per model and test.** 

||||**Tes**|**t 1**|||||**Tes**|**t 2**|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|G|O|Food|On|SNOM|ED CT|G|O|Food|On|SNOME|D CT|
||MCQ|OQ|MCQ|OQ|MCQ|OQ|MCQ|OQ|MCQ|OQ|MCQ|OQ|
||||||_Llama_||||||||
|Direct|50.7|5.0|33.7|12.0|51.0|6.5|50.7|5.0|33.8|12.4|51.9|6.9|
|CoT|47.7|1.0|32.0|6.5|35.0|1.5|47.7|1.0|32.1|6.7|35.6|1.6|
|RAGont(text)|55.0|0.5|53.3|3.5|44.3|5.0|55.7|1.5|51.8|5.7|52.5|6.9|
|RAGont(query)|52.7|13.0|41.0|4.0|42.3|13.0|48.3|1.5|39.8|3.1|39.7|2.6|
|RAGdoc(text)|50.0|0.0|34.0|4.5|45.0|4.0|50.0|0.0|34.1|4.6|45.8|4.2|
|MedRAGdoc|50.7|2.5|31.7|6.5|37.7|8.0|50.7|2.5|31.8|6.7|38.3|8.5|
|ReActont|50.0|10.0|44.7|8.0|40.3|11.5|54.3|13.0|43.8|13.4|46.1|11.1|
|i-MedRAGdoc|46.7|0.0|31.7|1.0|37.7|0.5|46.7|0.0|31.8|1.0|38.0|0.5|
|OA-RAG|63.0|52.0|53.3|18.5|69.7|64.5|53.7|12.5|46.8|17.0|56.3|24.9|
||||||_Qwen_||||||||
|Direct|56.7|4.5|51.7|14.0|61.0|6.5|56.7|4.5|51.8|14.4|61.7|6.9|
|CoT|65.3|13.0|57.0|12.0|61.0|13.0|65.3|13.0|57.2|12.4|61.7|13.8|
|RAGont(text)|71.7|27.0|71.7|15.0|62.7|12.5|73.0|30.0|67.6|12.4|66.8|17.5|
|RAGont(query)|70.3|31.0|61.0|11.0|73.3|36.5|60.0|4.0|53.8|8.2|56.9|5.3|
|RAGdoc(text)|63.3|6.5|59.7|5.5|60.0|4.0|63.3|6.5|59.9|5.7|60.7|3.7|
|MedRAGdoc|61.0|0.0|56.0|0.0|59.7|1.5|61.0|0.0|56.2|0.0|60.3|1.6|
|ReActont|72.7|39.0|71.3|32.0|63.7|23.5|66.7|42.0|61.5|30.9|67.8|25.4|
|i-MedRAGdoc|47.3|0.5|29.7|0.0|43.3|1.0|47.3|0.5|29.8|0.0|44.1|1.1|
|i-MedRAGdoc(262k)|51.0|1.0|27.3|0.0|44.3|2.0|51.0|1.0|27.4|0.0|45.1|2.1|
|OA-RAG|79.7|62.5|78.3|34.0|81.7|89.5|74.0|22.0|74.6|21.1|72.5|26.5|





<!-- Start of picture text -->
Llama Qwen at least one correct and no wrong<br>MCQ: MCQ: OQ:<br>masked slot #Ans conditions  𝑛<br>100<br>75<br>50<br>25<br>0<br>𝐵𝐴 𝑟 𝐵𝐴 𝑟 1 2 3 1 2 3 2 3 4 2 3 4<br>Test 1 Test 2 Test 1 Test 2 Test 1 Test 2<br>accuracy (%)<br><!-- End of picture text -->

**Figure 7: OA-RAG on Test 1 and Test 2 by item construction (accuracy %; dashed: MCQs scored with at least one correct and no wrong choice).** 

**Table 5: Tests 1 (T1) and 2 (T2): MCQs by the number of correct options (#Ans), and OQs by the number of conditions** _𝑛_ **.** 

|||GO||Food|On|SNOM|ED CT|A|ll|
|---|---|---|---|---|---|---|---|---|---|
|||T1|T2|T1|T2|T1|T2|T1|T2|
||#Ans=1|203|203|230|230|236|235|669|668|
|MCQ|#Ans=2|58|58|43|43|39|39|140|140|
||#Ans=3|39|39|27|26|25|21|91|86|
||_𝑛_=2|67|67|67|67|67|65|201|199|
|OQ|_𝑛_=3|67|67|67|65|67|61|201|193|
||_𝑛_=4|66|66|66|62|66|63|198|191|
|All qu|estions|500|500|500|493|500|484|1,500|1,477|



**Table 4: Sizes of the ontologies (Test 1: source; Test 2: revised).** 

||GO|FoodOn|SNOMED CT|
|---|---|---|---|
|Named concepts|51,986|30,995|374,546|
|Roles|9|69|126|
|Axioms (Test 1)|82,950|44,986|375,261|
|Axioms (Test 2)|65,810|36,881|375,261|



# **C Benchmarks** 

**Table 4** summarizes the sizes of the three ontologies. We use the GO release of 2026-07-26, the FoodOn release of 2022-08-12 (with imports merged), and the SNOMED CT International Edition release of 2025-07-01, converted to OWL using the SNOMED OWL Toolkit. SNOMED CT is in the OWL 2 EL profile (EL<sup>++</sup> ). GO uses only ⊓ and ∃ in its class expressions and lies in EL<sup>++</sup> except for one inverse-object-property axiom relating _part of_ and _has part_ . FoodOn additionally uses ∀, ¬, ⊔, and cardinality restrictions, placing it in SRIQ. The revised ontologies used in Test 2 preserve the signature 

and use a subset of the same constructors. **Table 5** summarizes the sizes of Tests 1 and 2. For each ontology, we construct 300 MCQs by masking the filler, subject, or relation of 100 axioms each, together with 200 OQs. Test 2 uses the same questions as Test 1, except for 23 questions that fail the checks described below. 

**OQ conditions.** We construct the candidate OQ conditions as follows. Let _𝑆_ ( _𝐴_ ) contain the restrictions ∃ _𝑟.𝐵_ that the MCQ decomposition rule (§5.1) yields from the asserted axioms of _𝐴_ and its ancestors, and let the filler be lifted by up to two taxonomy levels: 

_𝑆_ ( _𝐴_ ) = {∃ _𝑟.𝐵_<sup>′</sup> : ∃ _𝑟.𝐵_ ∈ _𝑆_ ( _𝐴_ ) _, 𝐵_<sup>′</sup> ∈{ _𝐵_ } ∪ Parent≤2 ( _𝐵_ )} _._ 

A lifted restriction still holds for _𝐴_ , since _𝐵_ ⊑ _𝐵_<sup>′</sup> . For each _𝐴_ with | _𝑆_ ( _𝐴_ )| ≥ _𝑛_ , we sample _𝑛_ conditions from _𝑆_ ( _𝐴_ ) and resample until none subsumes another (O̸ |= ∃ _𝑟𝑖 .𝐵𝑖_<sup>′⊑∃</sup><sup>_𝑟𝑗.𝐵_′</sup> _𝑗_<sup>for all</sup><sup>_𝑖_≠</sup><sup>_𝑗_).</sup> **Test 2 checks.** We apply two checks to ensure that Test 2 remains in the intended pattern (§5.2). First, the revision may remove information needed to preserve the original answer. In particular, replacing an equivalence ( _⊲⊳_ =≡) with _𝐴_ ⊑ _𝐷_ drops the reverse implication _𝐷_ ⊓<sup>**�**</sup> _𝑖_<sup>∃</sup><sup>_𝑟𝑖.𝐶𝑖_⊑</sup><sup>_𝐴_, which is not preserved by the informal</sup> annotations. We therefore verify that each question retains the


<!-- page 12 -->

Yang et al. 

same gold answer when both the revised axioms and the informal annotations are considered. Second, we require that the gold answer cannot be derived from the revised ontology by an ontology reasoner alone. 

# **D Construction and Difficulty** 

Figure 7 shows how the performance of OA-RAG varies with item construction, including the number of correct MCQ options, the number of OQ conditions, and the masked slot. 

**Correct options.** For Llama on Test 1, accuracy drops from 73.8% on single-answer MCQs to 32.1% and 20.9% with two and three correct options, respectively, because all entailed options must be identified. Despite this drop, OA-RAG remains well above all baselines (at most 14.3%), as it can verify each option independently with an ASK query. 

**Conditions.** On Test 1, OQ accuracy is stable up to _𝑛_ = 3 conditions (46.3% for Llama at both _𝑛_ = 2 and _𝑛_ = 3) and drops to 42.4% only at _𝑛_ = 4, since a single SELECT can evaluate the full conjunction. On Test 2, however, accuracy is far lower throughout and already falls at _𝑛_ = 3 (from 19.6% at _𝑛_ = 2 to 17.1%), as the required conditions must be recovered from separate definition sentences. 

**Masked slot.** For both models, masking the relation is easiest, while masking the filler is consistently hardest, because the filler’s ancestors may also constitute correct answers. 

# **E Prompts** 

OA-RAG uses four prompts, reproduced verbatim below: pre-tool reasoning (Ppre), the ReAct loop (Pagent), final answering (Pfin or Pown, Step 1), and attribution (Patt, Step 2). **Color code.** Black text is fixed; this color marks ontology- or dataset-specific content; and red marks the question block _𝑞_ , including the question, answer options, PubMedQA abstract, and answer format. **Persona.** The persona is prepended to the pre-tool and final-answer prompts. For Tests 1 and 2, SNOMED CT questions use the persona shown in Ppre, and GO and FoodOn questions replace its first sentence with _“You are an expert in molecular biology”_ and _“You are an expert in the science of foods, their ingredients, origins and preparation”_ , respectively. For Test 3, we use the dataset-specific OntoTune header. 

## **Pre-tool reasoning** Ppre **(SNOMED CT persona)** 

System: You are an expert physician in clinical medicine and healthcare terminology, answering questions about how the entities of that field are defined, organized and related. Answer the following question carefully. Think step by step briefly to reason about the question. Use the information provided with the question. Additional records are context; use them only when they bear on the question. A draft is unverified. End your reply with the final answer as a single JSON object matching the answer schema, on its own last line. User: {question block _𝑞_ } 

## **Agent prompt** Pagent **(the user turn after the pre-tool reply)** 

An ontology is available through the tool below. Continue from your answer above: where the ontology decides the question, verify that answer with the tools; then give the final answer in the format below. 

**## Tool** 

query(sparql): exact reasoning over the ontology’s axioms, asked as a short SPARQL query over names: every concept and relation is written as its exact name in double quotes (there are no identifiers or IRIs to use); the relation "is 

a" means classification (a kind of). Inheritance and sub-relations are applied for you. The four query forms, each with a toy example: 

- DESCRIBE "name" – the ontology’s record of one concept: definition, parents, children, the relations it states, annotations. E.g. DESCRIBE "grand piano" 

- ASK { "subject" "relation" "object" } – is every subject related by relation to some object? Verdicts: ENTAILED, NOT ENTAILED, UNKNOWN NAME. E.g. ASK { "grand piano" "part of" "orchestra" } 

- SELECT ?x WHERE { ?x "relation" "object" . ... } – the concepts that satisfy ALL the listed conditions; add VALUES ?x { "name" "name" ... } to test only these candidates, one verdict each. E.g. SELECT ?x WHERE { ?x "part of" "orchestra" . ?x "made of" "brass" } 

- SELECT ?o WHERE { "subject" "relation" ?o } – what the subject is related to by that relation; likewise SELECT ?r WHERE { "subject" ?r "object" } lists the relations that hold between the two. E.g. SELECT ?o WHERE { "grand piano" "part of" ?o } 

**## How to use it** 

Use the ontology when the question is about how its concepts are defined, classified or related to each other: query decides such a question exactly, so verify the candidate answers with it before answering. Answer a question about a situation, a case, a measurement or general knowledge from your own knowledge. Names must be spelled exactly as the ontology spells them; if a name comes back UNKNOWN NAME, retry with one of the similar names it lists. **## What the verdicts mean** 

ENTAILED is certain: the ontology’s axioms derive it. NOT ENTAILED is not a denial: the ontology is incomplete (open world), so a statement it does not derive may still hold. Decide such a statement yourself from the records shown and from what you know, and accept it when it is clearly true. **## Format** 

Thought: reason about the question and about what to do next – take as much room as you need 

Action: one tool call, written as a function call: query(<SPARQL query>) Observation: the tool’s result, given to you – never write one yourself ... (this repeats as often as needed) 

Thought: I now know the answer 

Answer: <ONLY the JSON object in the answer schema the question states> Write a Thought before every Action and before the Answer. A Thought may also stand on its own; the reply after it must be an Action or an Answer. Begin. 

## **Final answer:** Pfin **(non-empty digest) and** Pown **(empty digest)** 

Pfin, System: The tool phase of this session is over. Using the question and the observations below, think step by step briefly, then end your reply with the final answer JSON object that the question’s answer schema requests, on its own last line. ENTAILED is certain: the ontology’s axioms derive it. NOT ENTAILED is not a denial: the ontology is incomplete (open world), so a statement it does not derive may still hold. Decide such a statement yourself from the records shown and from what you know, and accept it when it is clearly true. 

Pfin, User: {persona} {question block _𝑞_ } 

Observations so far: 

{the digest _𝐸_ } 

Draft answer from the tool phase: {draft _𝑦_ ˜} 

- Pown, System: Answer the question from your own knowledge. Think step by step briefly, then end your reply with the final answer JSON on its own last line. 

- Pown, User: {persona} {question block _𝑞_ } 

## **Attribution** Patt **(one more user turn after the reply of** Pfin **; §4.1.3)** 

Your answer above is final; do not change it. Now state what it rests on. The observations you were given, numbered: 

- [E1] {observation _𝑒_ 1} 

- [E2] {observation _𝑒_ 2} ... 

Reply with only this JSON object: 

- {"evidence": [<the ids of the observations your answer relies on, e.g. "E1", "E3"; empty if none>], "grounding": "<one word: entailed, supported, related or unrelated>"} Choose the grounding as the first of these that holds: 

- entailed: your answer follows from the observations by strict logical reasoning: for each option or name in your answer, the facts stated in the observations derive it, with nothing added from your own knowledge. A fact counts whether the tool states it formally (an ENTAILED verdict, a listing of the concepts entailed to satisfy the question’s conditions, a stated relation, parent or child) or a text field states it as explicitly as an axiom would, naming the concepts and the relation (e.g. a definition sentence “Every X is related by R to some Y”).


<!-- page 13 -->

OA-RAG: Ontology-based Agentic RAG for Faithful LLM Reasoning 

Concept names, synonyms and keyword records marked “not verified” state no fact. 

- supported: your answer follows from the observations by sound reasoning that is not such a derivation: it interprets text that does not state the fact explicitly (a paraphrasing definition, a name or synonym match, a “not verified” keyword record), or it combines the facts shown with your own knowledge. 

- related: the observations give some valid information relevant to the question, but not enough to arrive at your answer, or they point to a different answer. 

- • unrelated: the observations are essentially irrelevant to the question and to your answer. 

- NOT ENTAILED or “0 concepts” only means that the axioms do not derive a statement (open world); it does not deny it. So an empty answer (no option selected, an empty list), which claims that nothing satisfies the question, is at most related. 

If the reply holds no such object with one of the four levels, one re-ask follows: _Reply with only the JSON object_ {"evidence": [...], "grounding": "..."} _. The first character of the reply must be ‘{’ and the last must be ‘}’._
