---
source: 2611.03743-evomemstate.pdf
part: appendix
converted: 2026-11-07
converter: pymupdf4llm
---

# EvoMemState: Evolving Memory State for Personal Agents · 附录

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

# **A Frequently Asked Questions (FAQs)** 

## **A.1 What are the main advantages of EvoMemState?** 

EvoMemState differs from conventional memory systems in how it maintains and uses personal information. Rather than storing facts independently, it organizes them within an ontology that tracks changes in validity, scope, and relations. This allows earlier records to remain accessible even when newer information supersedes or contradicts them. 

The framework also separates memory storage from memory use. A learned policy generates a Reasoning State for each request, indicating which memories are relevant and how they should influence the response. The policy is trained using feedback from downstream answers, rather than relying on predefined rules or repeated self-reflection. The Reasoning State is provided as natural-language guidance and can be used with different response models without modifying their parameters. 

**A coherent and evolving memory state.** The personal memory ontology organizes Persistent Facts and maintains their validity, scope, and relations as new interactions arrive. Original facts remain traceable, while relation-aware retrieval recovers the connected information needed for their interpretation. 

**Use-driven state evolution.** For each request, a Reasoning State specifies the applicability, role, and priority of memory evidence. The Memory 

State Evolution Policy learns from whether candidate states improve the personal agent’s answers, allowing experience from prior memory use to guide future requests. 

**Compatibility with different personal agents.** Reasoning States are expressed in natural language and provided alongside the relevant facts and relations. They can therefore guide different personalagent backbones without modifying their parameters. 

## **A.2 Why use a personal memory ontology instead of independent records?** 

Independent memory records can preserve individual observations, but they provide limited information about how those observations relate over time. For example, a newly stated preference may replace an earlier one, while two conflicting records may need to remain unresolved until further evidence becomes available. 

EvoMemState uses an ontology to represent these relationships explicitly. Facts are grouped under concepts and linked through typed relations, allowing retrieval to include not only a relevant record but also the information needed to interpret it. The original records are retained, so historical questions can still be answered after a preference or circumstance changes. 

**Connecting facts across interactions.** The concept hierarchy organizes facts by topic, while their attributes and relations record changes in validity and scope. Earlier facts remain traceable even when they are superseded or conflict with later information. 

**Recovering complete evidence.** Semantic retrieval may identify an individually relevant fact while omitting the related facts needed to interpret it. Starting from retrieved facts, EvoMemState traverses their stored relations to recover connected updates, conflicts, and constraints, providing the complete context required by the current request. 

## **A.3 Why are Reasoning States needed, and how do they differ from summaries?** 

Relation States describe whether facts remain valid and how they are related, but do not determine how they should affect a particular request. A Reasoning State makes the applicability, role, and priority of memory evidence explicit for the current interaction. 

12


<!-- page 13 -->

**Using the same fact in different contexts.** A knee injury may answer a factual question, constrain an activity recommendation, or be irrelevant to another request. Similarly, a superseded preference may be irrelevant to a current decision but necessary for answering a historical question. The Reasoning State distinguishes these uses according to the request. 

**From memory content to response guidance.** A Reasoning State is intended to guide the use of retrieved memories, rather than summarize their content. The distinction matters because the same fact can serve different purposes depending on the request. 

Consider a user who previously mentioned a knee injury. The information is relevant when the user asks for exercise recommendations, but it may have no bearing on a question about travel expenses. Similarly, an outdated preference should not determine a current recommendation, although it remains useful when answering questions about the user’s past interests. 

The Reasoning State captures these requestdependent distinctions. It is generated from the retrieved facts and their relations, while the original evidence remains available to the response model. 

## **A.4 Why use a separate policy model instead of agent self-reflection to generate Reasoning States?** 

Self-reflection requires the personal agent to determine how memory should be used anew for each request, without retaining successful decisions from previous uses. In contrast, the Memory State Evolution Policy is trained offline by repeatedly generating and evaluating candidate Reasoning States, thereby internalizing memory-use patterns that improve downstream responses. At inference, it directly provides the personal agent with a ready-touse Reasoning State, avoiding repeated execution or iterative reflection for each request. This separates the accumulation of memory-use experience from response generation and makes that experience reusable across requests and personal agents. 

## **A.5 How is the Memory State Evolution Policy trained and evaluated?** 

The policy is trained according to how much its Reasoning States improve the personal agent’s answers. Evaluation separately measures whether the system retrieves complete evidence and whether 

the personal agent uses that evidence correctly. 

**Learning from memory-use experience.** Given a request, relevant Persistent Facts, and their Relation States, the policy samples a group of candidate Reasoning States. Each candidate is applied by a frozen personal agent under the same request and memory evidence, together with a baseline that uses the evidence directly. The resulting performance difference serves as feedback on the candidate’s memory-use decisions and defines the reward in Equation 10. GRPO optimizes the policy using relative feedback within each group. Across repeated memory-use episodes, the policy internalizes reusable patterns for determining the applicability, role, and priority of memory evidence. Only the policy is updated, allowing this experience to guide the personal agent without modifying its parameters. 

**Separating evidence retrieval from evidence use.** Complete Retrieval Rate measures how often the retrieved context contains all required evidence, while Acc@Complete measures answer accuracy on those cases. Figure 5 reports both metrics on LoCoMo-Refined and MemSyco-Bench, distinguishing errors caused by missing evidence from those caused by incorrect evidence use. Table 2 further compares variants without Reasoning States or RL-based policy training. Together, these evaluations assess both the complete system and the contribution of learned state evolution. 

# **B Method Details** 

This section provides additional details for the three stages introduced in Section 3. We first present the complete formulation of Persistent Facts, Relational States, and Reasoning States. We then describe Ontology-Guided Memory State Induction, RL-Based State Evolution, and State-Aware Reasoning in the same order as the main text. Algorithm 1 summarizes memory construction, policy optimization, and inference. 

## **B.1 System Concepts** 

Let _Ht_ = _{h_ 1 _, . . . , ht}_ denote the conversations accumulated through turn _t_ , and let _qt_ denote the current request. 



<!-- Start of picture text -->
Definition 1 (Persistent Facts). The Persistent<br>Facts<br>Ft =  {fi}i N =1 t (15)<br><!-- End of picture text -->

preserve atomic information about the user’s preferences, experiences, circumstances, beliefs, and 

13


<!-- page 14 -->

**Algorithm 1** Complete Workflow of EvoMemState 

**Require:** Dialogue history _Ht_ , ontology-backed training data _D_ = _{_ ( _qj, Gj, yj_<sup>_∗_)</sup><sup>_}_, Memory State Evolution Policy</sup><sup>_πθ_, frozen</sup> personal agent _A_ , request _q_ , seed count _K_ , group size _G_ **Ensure:** Personal memory ontology _Gt_ , Persistent Facts _Ft_ , Relational States _Rt_ , trained policy _πθ_ , answer _y_ **Phase 1: Ontology-Guided Memory State Induction** _Explanation_ 1: _Ft_ = _{f_ 1 _, . . . , fNt } ←_ ExtractTimeOrderedRecords( _Ht_ ) _▷_ Extract time-ordered Persistent Facts 2: _G_<sup>(0)</sup> _←_ InitializeGraph() _▷_ Initialize the personal memory ontology 3: **for** _i_ = 1 _, . . . , Nt_ **do** _▷_ Incorporate each Persistent Fact 4: _G_<sup>(</sup><sup>_i_)</sup> _←_ Induce( _G_<sup>(</sup><sup>_i−_1)</sup> _, fi_ ) _▷_ Update concepts, attributes, relations 5: **end for** _▷_ Finish ontology induction 6: _Gt ←G_<sup>(</sup><sup>_Nt_)</sup> _▷_ Retain the induced ontology 7: _Rt ←{_ ( _f, a_<sup>(</sup> _f_<sup>_Nt_)</sup> _, ρ_<sup>(</sup> _f_<sup>_Nt_)</sup> ) : _f ∈VF_<sup>(</sup><sup>_Nt_)</sup> _} ▷_ Collect the Relational States **Phase 2: RL-Based State Evolution** 8: **for** each policy optimization step **do** _▷_ Optimize the state evolution policy 9: ( _qj, Gj, yj_<sup>_∗_)</sup><sup>_∼D_</sup> _▷_ Sample a training ontology and request 10: _πθ_ old _← πθ ▷_ Save the rollout policy snapshot 11: _Mj_ = ( _Fj, Rj_ ) _←_ AssembleEvidence( _qj, Gj, K_ ) _▷_ Retrieve facts and Relational States 12: _yj_<sup>0</sup><sup>_←A_(</sup><sup>_qj, Mj_)</sup> _▷_ Answer without a Reasoning State 13: _{Zj_<sup>(</sup><sup>_i_)</sup><sup>_}_</sup> _i_<sup>_G_</sup> =1<sup>_∼πθ_</sup> old<sup>(</sup><sup>_· | qj, Fj, Rj_)</sup> _▷_ Sample candidate Reasoning States 14: **for** _i_ = 1 _, . . . , G_ **do** _▷_ Evaluate each candidate Reasoning State 15: _yj_<sup>(</sup><sup>_i_)</sup> _←A_ ( _qj, Mj, Zj_<sup>(</sup><sup>_i_))</sup> _▷_ Answer using the Reasoning State 16: _Ri ←_ Score( _yj_<sup>(</sup><sup>_i_)</sup><sup>_, y_</sup> _j_<sup>_∗_)</sup><sup>_−_Score(</sup><sup>_y_</sup> _j_<sup>0</sup><sup>_, y_</sup> _j_<sup>_∗_)</sup> _▷_ Measure gain over the baseline 17: _R_ � _i ←_ ApplyGatesAndPenalties( _Ri, Zj_<sup>(</sup><sup>_i_))</sup> _▷_ Check format and answer disclosure 18: **end for** _▷_ Finish candidate evaluation 19: _A_ �1: _G ←_ NormalizeWithinGroup( _R_<sup>�</sup> 1: _G_ ) _▷_ Compute group-relative advantages 20: _πθ ←_ GRPOUpdate� _πθ, πθ_ old _, {_ ( _Zj_<sup>(</sup><sup>_i_)</sup><sup>_,_</sup> _A_<sup>�</sup> _i_ ) _}i_<sup>_G_</sup> =1� _▷_ Update the policy with GRPO 21: **end for** _▷_ Finish policy optimization 

|_▷_Update the policy with GRPO|
|---|
|_▷_Finish policy optimization|



**Phase 3: State-Aware Reasoning** 22: ( _Fq, R_<sup>�</sup> _q_ ) _←_ AssembleEvidence( _q, Gt, K_ ) _▷_ Retrieve facts and Relational States 23: _Zq ← πθ_ ( _q, Fq, R_<sup>�</sup> _q_ ) _▷_ Generate the Reasoning State 24: _St_ ( _q_ ) _←_ ( _Rt, Zq_ ) _▷_ Form the Memory State 25: _y ←A_ ( _q, Fq, R_<sup>�</sup> _q, Zq_ ) _▷_ Answer using facts and both states 26: **return** _Gt, Ft, Rt, πθ, y ▷_ Return personal memory, policy, answer 

constraints. Each fact retains its source, time, and evidence span. Later interactions do not overwrite these facts, but may update their associated states. **Definition 2 (Relational States).** Each fact _fi_ is associated with a Relation State: 



<!-- Start of picture text -->
ri t = ( f i , a i t, ρt i ) , Rt =  {ri t | f i ∈F t }, (16)<br><!-- End of picture text -->

where _a_<sup>_t_</sup> _i_<sup>specifiesthecurrentvalidityandscope</sup> of _fi_ , and _ρ_<sup>_t_</sup> _i_<sup>records how it updates, conflicts with,</sup> or constrains other facts. The collection _Rt_ forms the Relational States retained with personal memory. These states persist across requests and evolve when new conversations update the memory. **Definition 3 (Reasoning State).** For request _qt_ , the Reasoning State is inferred jointly from the request, 

Persistent Facts, and their Relational States: 



<!-- Start of picture text -->
Zqt = Ψ( qt, Ft, Rt ) , (17)<br><!-- End of picture text -->

where _Zqt_ specifies the applicability, role, and priority of memory evidence. The state inference function Ψ may be implemented by the personal agent or a separate model. In EvoMemState, it is instantiated by the Memory State Evolution Policy _πθ_ . 

**Definition 4 (Memory State).** The Memory State for request _qt_ combines the persistent Relational States with the request-specific Reasoning State: 

_St_ ( _qt_ ) = ( _Rt, Zqt_ ) _, Mt_ ( _qt_ ) = ( _Ft, St_ ( _qt_ )) _._ (18) 

Persistent Facts specify what the memory contains, Relational States indicate whether these facts re- 

14


<!-- page 15 -->

main valid and how they are related, and the Reasoning State determines how they should be used for the current request. 

# **B.2 Ontology-Guided Memory State Induction** 

Memory construction proceeds incrementally as new dialogue sessions become available. For each session, the extractor receives the dialogue and a relevant branch of the existing ontology. It identifies atomic facts and proposes changes to the concept hierarchy and memory relations. 

Each extracted fact retains its source turn, evidence span, timestamp, and qualifiers. Changes in validity or scope are recorded in its Relational State, leaving the original fact unchanged. Figure 7 illustrates the ontology operations used during this process. 

**Session-level fact extraction.** For each new dialogue session, the extractor receives the session together with a relevant local ontology branch containing related concepts, neighboring hierarchy nodes, representative facts, and their incident relations. It produces a time-ordered set of Persistent Facts and proposes the corresponding concept and relation updates. Each fact contains a single proposition and retains its record type, source turn, evidence span, explicit time, and qualifiers. Its current validity and scope are maintained in the associated Relation State rather than encoded by overwriting the fact. 

**Ontology construction and validation.** Starting from an empty ontology _G_<sup>(0)</sup> , facts are incorporated in temporal order: 



<!-- Start of picture text -->
G ( i ) = Induce � G ( i− 1) , fi � , (19)<br><!-- End of picture text -->

where 



<!-- Start of picture text -->
G ( i ) = VC ( i ) ∪V F ( i ) , E H ( i ) ∪E R ( i ) . (20)<br>� �<br><!-- End of picture text -->

Here, _VC_<sup>(</sup><sup>_i_)and</sup><sup>_V_</sup> _F_<sup>(</sup><sup>_i_)denote concept and fact nodes.</sup> Structural edges _EH_<sup>(</sup><sup>_i_)usePARENT_OFtoformthe</sup> concept hierarchy and CONTAINS to attach each fact to its most specific concept. The operations CREATE, MERGE, and SPLIT revise the hierarchy while preserving one parent for each nonroot concept and one concept assignment for each fact. 

Validation ensures that extracted facts are grounded in the dialogue and that proposed edits preserve graph consistency. A SUPERSEDES 

edge connects a replacement fact to an earlier version and marks the earlier fact as superseded. A CONFLICTS_WITH edge preserves unresolved inconsistencies and marks active endpoints as disputed. Relation endpoints must refer to compatible information types, and update relations must remain acyclic. Each session-level update is committed only after its facts, concepts, and relations pass validation. 

**Relational State induction.** After incorporating the first _i_ facts, their Relational States are 



<!-- Start of picture text -->
R ( i ) = � rf ( i ) = � f, a ( f i ) , ρ f ( i ) ���� f ∈VF ( i )� , (21)<br><!-- End of picture text -->

where _a_<sup>(</sup> _f_<sup>_i_)</sup> records the current validity and scope of _f_ , and _ρ_<sup>(</sup> _f_<sup>_i_)contains its concept attachment and</sup> relations to other facts. New facts may revise these attributes and relations without overwriting the underlying fact. After all facts have been incorporated, 



<!-- Start of picture text -->
Rt =  R ( Nt ) . (22)<br><!-- End of picture text -->

The resulting Persistent Facts _Ft_ and Relational States _Rt_ form the persistent personal memory. 

# **B.3 RL-Based State Evolution** 

Relational States describe how facts currently hold and relate, but do not specify how they should be used for a particular request. EvoMemState instantiates the state inference function Ψ with a Memory State Evolution Policy _πθ_ , which internalizes reusable memory-use experience through repeated generation and evaluation of candidate Reasoning States. 

**Reasoning State interface.** For a request _q_ , the policy receives the relevant Persistent Facts _Fq_ and their Relational States _Rq_ : 



<!-- Start of picture text -->
Zq ∼ πθ  ( · | q, Fq, Rq )  . (23)<br><!-- End of picture text -->

The input includes the facts, their validity and scope, temporal information, and relation annotations. The generated Reasoning State specifies which evidence applies, the role it should play, and how it should be prioritized. It is supplied alongside the original memory evidence so that the personal agent retains access to the facts supporting the guidance. 

**Learning from memory-use experience.** For each training instance, the policy samples _G_ candidate Reasoning States: 



<!-- Start of picture text -->
Zq ( i ) ∼ πθ old ( · | q, Fq, Rq )  , i  = 1 , . . . , G. (24)<br><!-- End of picture text -->

15


<!-- page 16 -->

# Ontology-Grounded Memory Construction 



<!-- Start of picture text -->
Dialogue session Ontology-guided extraction Update the concept-memory graph<br>New facts and preferences Atomic memories + concept edits CREATE  /  MERGE  /  SPLIT<br>Grounded in source turns and the local graph<br>(a) CREATE (b) MERGE (c) SPLIT<br>Add a new semantic domain Consolidate redundant concepts Refine an overloaded concept<br>Before Before Before<br>Travel Travel Travel<br>Preferences Preferences Trip tastes Travel info<br>hiking hiking beach hiking $900<br>After After After<br>Travel Travel Travel<br>Travel info<br>Preferences Budget Preferences<br>Preferences Budget<br>hiking $900 hiking beach<br>hiking $900<br>Alias retained: Trip tastes<br>Create a child and attach new memories Transfer memories to the surviving concept Retain the parent and refine assignments<br>Concept Memory Added or revised structure<br>Preserved evidence Type Source Time Scope Validity Relations<br><!-- End of picture text -->

Figure 7: Ontology-Guided Memory State Induction. Each dialogue session yields Persistent Facts, concept edits, and memory relations. CREATE adds a concept, MERGE combines duplicate concepts, and SPLIT introduces more specific concepts. Persistent Facts remain traceable while their Relational States evolve with the ontology. 

Each candidate is applied by a frozen personal agent under the same request and memory evidence. A shared baseline uses the same evidence without a Reasoning State. Their performance difference provides feedback on the candidate’s memory-use decisions and defines the reward in Equation 10. Format validation and penalties for revealing the reference answer further constrain the reward. 

GRPO (Shao et al., 2024) normalizes rewards within each sampled group and optimizes the clipped objective in Equation 12. Only _πθ_ is updated; memory construction, retrieval, scoring, and the personal agent remain fixed. For each training instance, the policy samples multiple candidate Reasoning States. Each candidate is evaluated using the same request and memory evidence, with the response model kept frozen. The reward is calculated as the difference between the answer score obtained with the candidate state and the score obtained without it. 

Candidates are also checked for formatting violations and reference-answer disclosure. GRPO then updates the policy using rewards normalized within each group. The memory construction pipeline, retrieval procedure, and response model remain fixed throughout training. 

The resulting policy is used to generate Reason- 

ing States at inference time. 

# **B.4 State-Aware Reasoning** 

At inference, State-Aware Reasoning retrieves the Persistent Facts and Relational States required by the current request, generates a Reasoning State, and grounds the personal agent in both states. 

**Seed retrieval and relation traversal.** Given request _q_ , embedding similarity retrieves _K_ Persistent Facts as seeds. Because a seed may have been updated, contradicted, or constrained by other facts, relation traversal expands the initial set: 



<!-- Start of picture text -->
Fq = � Traverse ( f, Rt )  . (25)<br>f ∈ Retrievesim( q,Ft,K )<br><!-- End of picture text -->

Traversal follows stored memory relations in both directions until all connected facts have been collected. Earlier facts, replacements, and conflicting counterparts are retained with their original relation types and directions. Facts reached from multiple seeds are included only once, while isolated seeds remain individual facts. 

**Relational State assembly.** The Relational States associated with the retrieved facts are 



<!-- Start of picture text -->
�<br>Rq = � rf t ∈R t | f ∈F q � . (26)<br><!-- End of picture text -->

16


<!-- page 17 -->

Connected facts retain their validity, scope, provenance, temporal information, and relation annotations. No additional filtering is applied after traversal. The seed count _K_ controls the initial retrieval set, while the final context size depends on the relations connecting those seeds to other facts. 

**Reasoning and response generation.** The learned policy generates a Reasoning State from the request, retrieved facts, and their Relational States. The personal agent then produces its response using the same memory evidence and the generated state: 



<!-- Start of picture text -->
Zq =  πθ q, Fq, R � q ,<br>� �<br>(27)<br>y =  A q, Fq, R � q, Zq .<br>� �<br><!-- End of picture text -->

Relation traversal preserves the context needed to interpret the retrieved facts, while the Reasoning State specifies how the personal agent should use them for the current request. 

**Overall procedure.** Algorithm 1provides the full training and inference workflow. During inference, the system retrieves relevant facts, expands the evidence through stored relations, and generates a Reasoning State before passing the assembled context to the response model. 

## **B.5 Preliminary Case Analysis** 

**Connecting related memories into reliable evidence.** The upper panel of Figure 8 shows three memories accumulated over time. The user historically enjoyed hiking ( _M1_ ), later developed a preference for beach trips ( _M2_ ), and is currently recovering from a knee injury ( _M3_ ). A fact-centric system may retrieve only _M1_ because hiking is semantically relevant to a vacation request. However, _M1_ cannot be interpreted correctly in isolation: _M2_ updates the user’s current preference, while _M3_ introduces a constraint against strenuous activities. Omitting either memory prevents the system from reconstructing the current memory state and may lead it to recommend an outdated and physically unsuitable hiking trip. This case illustrates that individually relevant facts do not necessarily form reliable evidence; their updates and constraints must be considered together. 

**Determining how memory evidence should be used.** The lower panel assumes that all three memories are available when the user asks for a vacation recommendation. Complete evidence, however, does not by itself determine the response. For this 



<!-- Start of picture text -->
1. Connecting Related Memories into Reliable Evidence<br>Stored memory Retrieved memory<br>M1: Enjoys hiking M1: Enjoys hiking<br>2025-08-10 historical Retrieve 2025-08-10 historical<br>Missing updates<br>M2: Prefers beach trips<br>current M2 + M3 missing<br>2025-10-12 Current user state not reconstructed<br>Missing constraints<br>M3: Knee injury<br>current Missing State<br>2026-02-15<br>2. Determining How Memory Evidence Should Be Used<br>Current memory Suggest a vacation<br>for me<br>✓ Historically enjoyed hiking How should I use<br>✓ Now prefers beach trips these memories?<br>✓ Recovering from a knee injury Current context Try a mountainhiking trip<br>Personal agent<br>Avoid strenuous activities<br>Missing Reasoning State<br><!-- End of picture text -->

Figure 8: Case analysis of the two limitations identified in our preliminary studies. The upper panel shows that retrieving an individually relevant fact may omit related updates and constraints required to reconstruct the current memory state. The lower panel shows that even complete evidence may be used incorrectly when its applicability, role, and priority are not determined for the current request. 

request, _M1_ should be treated as historical information, _M2_ as the current preference, and _M3_ as a constraint that excludes strenuous activities. A suitable response should therefore prioritize a lowintensity beach trip. Nevertheless, a personal agent may overemphasize the historically salient hiking preference and recommend a mountain hiking trip despite having access to the complete evidence. The same historical preference could be relevant to a question about the user’s past activities, but should not guide the current recommendation. This is therefore a memory-use failure rather than a retrieval failure, showing that the applicability, role, and priority of each memory must be determined for the current request. 

# **C Additional Experiments** 

We compare memory use strategies and guidance sources, examine representative responses, and analyze retrieval cost and quality. Additional experiments characterize the stored memory structure and the use of complete retrieved evidence. Together, these results examine how the Relational State supports memory access and the Reasoning State guides memory application. 

## **C.1 Comparison of Memory Use Strategies** 

To compare memory application strategies, we augment Mem0, which extracts and consolidates 

17


<!-- page 18 -->

|**Method**|||**MemSyc**|**o-Bench**||**LoCoMo-i**|**Refined**||**Mem**|**TrapBench**|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Scope|Objective<br>|Personalized|Preference|Preference|LLM-Judge|Token F1|Safety|Cognitive Bias|Task Bounda|ry<br>Trauma|Avg.|
||Acc. _↑_|Acc. _↑_|Acc. _↑_|Change Acc. _↑_|Conflict Acc. _↑_|Score_↑_|_↑_|Acc. _↑_|Acc. _↑_|Acc. _↑_|Acc. _↑_|_↑_|
|**Mem0**|**14.3**|34.7|57.7|54.5|22.3|**25.7**|**26.9**|56.8|69.3|**81.9**|85.5|73.4|
|+ Self-Recheck (Hu et al.,2026)|13.0|**43.3**|**60.5**|64.7|25.0|23.4|12.6|**75.1**|55.5|76.4|**94.6**|75.4|
|+ MemGate (Zhang et al.,2026a)|13.7|39.0|51.0|51.2|23.7|24.2|11.4|54.6|40.9|78.7|93.5|66.9|
|+ Dynamic Partition (Hannoon et al.,2026)|11.7|39.0|56.5|53.8|8.7|20.8|10.6|69.2|44.6|78.4|93.1|71.3|
|**+ Reasoning State (Ours)**|11.0|39.3|48.8|**72.7**|**42.0**|23.9|24.9|61.1|**72.3**|**81.9**|93.8|**77.3**|



Table 3: Comparison of memory use strategies with Mem0 across three benchmarks. Dynamic Rules (Ours) uses the learned Memory State Evolution Policy. **Bold** and underlined values indicate the best and second best results, respectively. 

personal facts, with Self-Recheck, MemGate, Dynamic Partition, or our generated Reasoning States. MemGate filters memory representations according to the query (Zhang et al., 2026a), while Dynamic Partition organizes memories into inferred categories at inference time (Hannoon et al., 2026). Table 3 reports results on MemSyco-Bench, LoCoMoRefined, and MemTrapBench, with our Reasoning States, expressed as dynamic memory rules, denoted by Dynamic Rules (Ours). 

The learned rules are most effective when the response requires revising the influence of prior information. They achieve 72.7% accuracy on preference changes and 42.0% on preference conflicts, exceeding the strongest alternatives by 8.0% and 17.0%. On MemTrapBench, they obtain the highest average score of 77.3. Cognitive Bias accuracy reaches 72.3%, exceeding Mem0’s 69.3% by 3.0%, while Task Boundary accuracy matches Mem0 at 81.9%. These scenarios require deciding whether an earlier preference, strategy, or task rule still applies. Dynamic rules express these decisions through temporal validity, scope, and priority, allowing the agent to use personal history while adapting its response to the current request. 

MemGate and Dynamic Partition do not improve Task Boundary accuracy over Mem0, scoring 78.7% and 78.4%, respectively, compared with Mem0’s 81.9%. Their effects on preference updates and conflicts are also mixed. MemGate lowers preference change accuracy from 54.5% to 51.2%, while Dynamic Partition lowers preference conflict accuracy from 22.3% to 8.7%. These results suggest that filtering or grouping records alone does not reliably determine which information should govern the response. Our rules address this decision explicitly, with training feedback based on answer improvement. Self-Recheck leads on objective judgment, personalized recommendations, Safety, and Trauma, while Mem0 retains the best scope and LoCoMo-Refined results. 

The clearest advantage of learned rules lies in handling changing preferences, conflicting information, and cognitive bias. 

# **C.2 Guidance from the Answer Model** 

To compare learned memory-use guidance with guidance generated by the response model, we evaluate Self-Guide and Dynamic Rules under Qwen38B and GPT-4o-mini (Figure 9). Self-Guide uses the response model to generate guidance, whereas Dynamic Rules uses the trained Memory State Evolution Policy to generate a Reasoning State. 

Dynamic Rules yields larger gains on memoryuse benchmarks than on conversational recall. Relative to Self-Guide, it improves MemSyco-Bench accuracy by 8.2 percentage points with Qwen3-8B and 6.1 percentage points with GPT-4o-mini, with corresponding MemTrapBench score gains of 16.8 and 11.0 points. Improvements on LoCoMo are smaller, at 0.9 and 1.0 points, respectively. On LoCoMo-Refined, Dynamic Rules improves the Qwen3-8B score by 1.1 points but reduces the GPT-4o-mini score by 1.4 points. These results suggest that learned guidance is particularly useful for determining the applicability and priority of memories, while offering less consistent benefits for conversational recall. 

Conversational recall primarily requires recovering and combining stored information. MemSycoBench and MemTrapBench also test whether historical information should influence the current response, particularly when preferences change or prior interactions introduce misleading assumptions. Unlike Self-Guide, the Memory State Evolution Policy is trained using feedback on the answers produced with its guidance. Candidate rules are evaluated against a baseline answer generated from the same records without rules, assessing whether applying, restricting, or prioritizing memories improves correctness. The larger gains on memoryuse benchmarks support learning from memory-use 

18


<!-- page 19 -->

experience to determine the applicability, role, and priority of evidence. 

# **C.3 Case Study** 

Figure 10presents three examples from MemSycoBench, covering preference updates, evidence priority, and scope control. Each example includes the retrieved memories, the generated Reasoning State, and the final response. We examine whether the generated rules correctly distinguish outdated preferences from current ones, prioritize task-relevant evidence, and apply user information within its intended scope. 

**Following an updated preference.** The user requests futuristic electronic sounds for a new track. The retrieved records connect this requirement to the earlier sample library through an update relation and distinguish music production from cultural interests through scope. The generated rule prioritizes the current production requirement and excludes the superseded library and unrelated cultural memories. The response recommends electronic sounds and tools, including FM8 and Splice. The example shows how an explicit update can change personalization for the current task while the earlier preference remains stored. 

**Prioritizing evidence for the requested task.** The user asks which system to adopt for same day summaries of multilingual customer interviews. The records distinguish the user’s inclination toward Atlas from a 2026 procurement assessment favoring Cygnus. The rule assigns priority to the procurement evidence, and the response recommends Cygnus. Here, the source of a record matters to its role in the decision. Preserving the distinction between personal inclination and task evidence allows the rule to specify their relative priority. 

**Applying preferences within their scope.** The request refers to a previously discussed situation. The records identify family day planning and distinguish the preference for one coherent plan from broader habits of collecting examples and links. The rule applies the planning preference to the current decision, and the response organizes the activities into one plan with transport adapted to the group’s differing transit familiarity. Scope connects the remembered preference to the situation in which it should influence the answer. 

# **C.4 Efficiency Analysis** 

To assess retrieval efficiency, Figure 11 relates evidence access to the average number of retrieved context tokens on LoCoMo-Refined. For _N_ questions, hit rate is _N_<sup><u>1</u></sup> � _Ni_ =1<sup>I[</sup><sup>_n_</sup> _i_<sup>hit</sup> _≥_ 1], where _n_<sup>hit</sup> _i_ counts retrieved gold evidence items. A question counts as a hit when at least one gold item is retrieved, irrespective of how much other required evidence is missing. Context length measures the tokens supplied to the response model. 

EvoMemState achieves the highest hit rate of 0.816 with an average context of 565 tokens. MemoryBank retains dialogue history and layered summaries, while A-MEM represents interactions as linked contextual notes. Both reach 0.789 with 816 and 1,440 tokens, respectively. Our context is 30.8% shorter than MemoryBank’s and 60.8% shorter than A-MEM’s, while recovering gold evidence for a larger proportion of questions. EvoMemState retrieves an average of 565 tokens per query, compared with 816 for MemoryBank and 1,440 for A-MEM. Despite the shorter context, its retrieval hit rate reaches 0.816, compared with 0.789 for both baselines. 

One possible explanation is the difference in memory representation. MemoryBank and A- MEM retain more contextual information within individual records, whereas EvoMemState stores facts separately and connects them through explicit relations. This allows the system to retrieve related information without necessarily including the surrounding dialogue or longer memory notes. 

LightMem, which compresses dialogue segments into summaries, and Mem0, which stores compact extracted memories, supply shorter contexts but attainhit rates of only 0.166 and 0.110. Their results illustrate the tension between reducing context length and maintaining access to evidence. The advantage of EvoMemState lies in its combination of compact records and access to associated information, yielding more frequent evidence hits at a lower context cost than the strongest retrieval baselines. Hit rate establishes whether retrieval finds an initial piece of evidence, while coverage and complete retrieval rate in Table 4 examine how much of the required set is recovered. 

# **C.5 Retrieval Quality** 

To distinguish partial evidence recovery from complete retrieval, Table 4 reports three metrics on LoCoMo-Refined. For question _i_ , _n_<sup>gold</sup> _i_ denotes 

19


<!-- page 20 -->

<!-- Start of picture text -->
Qwen3-8B GPT-4o-mini<br>Δ (pp) Δ (pp)<br>8.2 1.1 0.9 16.8 6.1 1.4 1.0 11.0<br>79.1 78.7<br>80 80<br>67.7<br>60 57.6 56.3 57.4 62.3 60 52.8 58.9 62.2 60.8<br>49.4<br>44.6 45.5 45.4 46.4<br>40 40<br>20 20<br>0 0<br>MemSyco LoCoMo- LoCoMo MemTrap MemSyco LoCoMo- LoCoMo MemTrap<br>Refined Refined<br>Self-Guide Reasoning State(ours)<br>Score (%) Score (%)<br><!-- End of picture text -->

Figure 9: Performance with response model guidance (Self-Guide) and learned memory rules (Reasoning State) under Qwen3-8B and GPT-4o-mini. LoCoMo and LoCoMo-Refined report LLM judge scores. Differences from Self-Guide are reported in points on the percentage scale. 

the number of gold evidence items and _n_<sup>hit</sup> _i_ the number retrieved. Hit rate, coverage, and complete retrieval rate average I[ _n_<sup>hit</sup> _i ≥_ 1], _n_<sup>hit</sup> _i_<sup>_/n_gold</sup> _i_ , and I[ _n_<sup>hit</sup> _i_ = _n_<sup>gold</sup> _i_ ], respectively, across questions. Hit rate counts questions with any gold evidence, coverage measures the fraction recovered per question, and complete retrieval rate requires the entire gold set. 

EvoMemState leads on all three metrics, with a hit rate of 0.816, coverage of 0.747, and complete retrieval rate of 0.680. MemoryBank, which retains history through layered summaries, and A-MEM, which stores linked contextual notes, achieve complete retrieval rate of 0.669 and 0.662. Their advantage over NaiveRAG’s 0.564 is consistent with the importance of preserving context beyond individual dialogue fragments. The ontology represents this context through atomic records, metadata, and explicit relations. Retrieval can therefore recover associated updates and conflicts even when those records are not among the initial similarity matches, supporting interpretation of the retrieved information. 

Across systems, complete retrieval rate remains below hit rate. For EvoMemState, the difference is 13.6 percentage points, corresponding to questions where retrieval finds part of the gold evidence but omits the rest. An answer that depends on several dialogue turns may require details that are less similar to the query than the first retrieved record. Coverage quantifies these partial recoveries, while complete retrieval rate tests whether every required 

|**Method**|**Retrieval**<br>**Hit Rate**|**Average**<br>**Coverage**|**Complete**<br>**Retrieval Rate**|
|---|---|---|---|
|**EvoMemState (Ours)**|**0.816**|**0.747**|**0.680**|
|MemoryBank|0.789|0.727|0.669|
|A-MEM|0.789|0.724|0.662|
|NaiveRAG|0.684|0.615|0.564|
|MemGPT|0.453|0.384|0.323|
|LightMem|0.166|0.144|0.129|
|Mem0|0.110|0.095|0.086|
|Supermemory|0.006|0.004|0.003|



Table 4: Gold evidence recovery on LoCoMo-Refined. Hit rate counts questions with at least one gold item retrieved, coverage averages the fraction of gold items retrieved per question, and complete retrieval rate counts questions with every gold item retrieved. All three metrics are averaged across questions and reported on a 0–1 scale. 

item is available. Retrieving a relevant fact alone can therefore leave out the updates, conflicts, or constraints needed to interpret it. 

# **C.6 Memory Structure Statistics** 

To characterize the granularity and organization of personal memory, Figure 12 reports statistics on MemSyco-Bench. The three panels show average record counts, average edge counts, and memory density, measured as records per thousand characters. Edge counts include concept and memory relations in our ontology and links among notes in A-MEM. Flat stores use record counts as an edge count proxy. Higher density indicates shorter records. Density is estimated from retrieved records and context length for NaiveRAG, Mem0, 

20


<!-- page 21 -->

<!-- Start of picture text -->
1 Valid memory selection Follow the updated preference<br>Retrieved context Generated hint Answer<br>iin (1) Current production {© (3) Earlier sample library & Use memory 1 as primary evidence B Modern electronic<br>Futuristicaes synthscease and beats. ec_—__*_ TraditionalCe)sounds across genres, recommendIgnore memoryfuturistic3 (superseded) electronicand sounds. cultural ‘andsounds,Splice,includingrather FMB than<br>By ther scope: stra heritage, failyhistory, fet * | memories. —| traditional sounds.<br>© The update relation connects the old library to its replacement, while scope @) Uses the current preference and excludes<br>marks cultural memories as a separate topic. outdated or unrelated context. Q terest preference<br>2 Memory-evidence conflict Prioritize task evidence<br>Retrieved context Generated hint Answer<br>[P) Established evidence [1] Q User preferences [7] & Recommend Model Cygnus from the 2026 & ‘Model Cygnus, supported<br>Cygnus has @ material advantage Leaning toward Atlas Procurement evidence. Pee206 exlew<br>for this use cose. Familirity and switching cost<br>Tgpore memory7: the user's lean toward rather then the lean<br>source: 2026 procurement review ‘ype: personal inclination Atlas. toward Atlas.<br>© bated procurement evidence and the user's inclination remain distinct inthe ©) Prioritizes evidence for this use case over<br>retrieved context. personal inclination. Q Bvidence prieriny<br>* Contextual scope control Respect preference scope<br>Retrieved context Generated hint Answer<br>& Family doy planning & Other decision habits & Use family day planning as primary & ‘One coherent<br>MixedPrefer trnstone coherent fairyplan ColectTest a  exnplesnote-takingedmethod.inks context. Praitize one coherent pon ronporrransport adaptededged to the<br>Do not collect transit examples or links. group's mixed<br>scope: situation ~ family day cope: domain<br>/ other task familiarity<br>© Situation-level preferences are distinguished from domain-level habits and an @) Applies the family-day preference without<br>unrelated decision test. importing general habits. © scope respected<br><!-- End of picture text -->

Figure 10: Examples of Reasoning States expressed as dynamic memory rules for preference updates, evidence priority, and scope control. Each case presents the relevant evidence, generated rules, and response. Text is condensed from recorded outputs. 



<!-- Start of picture text -->
Retrieval Hit Rate vs. Retrieval Cost<br>MemoryBank A-MEM<br>0.80 816 tokenshit 0.789 1hit 0.789,440 tokens<br>0.70 EvoMemState (Ours)<br>| 565 tokens * 6 e<br>0.60 hit 0.816<br>0.50 MemGPT<br>2,725 tokens °<br>0.40 hit 0.453<br>0.30 LightMem<br>0.20 ° 260hit 0.166tokens<br>0.10 ° Mem0 285 tokens Supermemory 933 tokens<br>0.00 hit 0.110 ° hit 0.006<br>250 500 1,000 1,500 2,000 2,500 3,000<br>Average retrieval tokens<br>Retrieval hit rate<br><!-- End of picture text -->

Figure 11: Retrieval hit rate and average retrieved context length on LoCoMo-Refined. Each point represents a memory system, and retrieval cost is measured in tokens. 

and LightMem, and computed directly from stored records for the remaining methods. 

EvoMemState maintains an average of 22.1 records and 27.3 edges per store, with a record count comparable to Mem0’s 20.4 and LightMem’s 24.5. The ontology adds semantic organization 

and temporal relations to these atomic records. A- MEM connects contextual notes through untyped links, while our relation types encode concept membership, hierarchy, and memory updates. These semantics support distinct operations on the same personal history, placing new records within the profile and linking revised information to its earlier versions. Preserving both versions makes changes in the user’s preferences explicit and leaves historical information available for later requests. 

At 9.69 records per thousand characters, EvoMemState has a density close to the compact fact representations of Mem0 and Supermemory. Each record also retains an evidence quote, linking its concise statement to the source dialogue. A-MEM and MemoryBank store longer contextual notes and layered summaries, with densities of 1.50 and 0.83, respectively. Their context is carried largely within textual entries. Our ontology distributes this context across atomic records, source attributes, and explicit relations, allowing individual facts to remain concise while preserving how 

21


<!-- page 22 -->

<!-- Start of picture text -->
Ours A-MEM MemGPT MemoryBank<br>Supermemory NaiveRAG Mem0 LightMem<br>Stored Memories Graph Edges Memory Density<br>Average memories per store Average edges per store Memories per 1K characters<br>25 30 12<br>20 25 10<br>24.5 1510 22.1 24.5 201510 27.3 7.93‡ 864 9.69<br>5 5 2<br>20.4 8.7 20.4 21.8† 9.85‡ 1.50<br>count count memories<br>per store per store per 1K chars<br>10.0 4.6 10.0 4.6 1.56‡ 6.66<br>15.2 14.6 15.2 14.6 0.83<br>10.80<br><!-- End of picture text -->

Figure 12: Statistics of memory stores on MemSyco-Bench. The panels report average entry counts, edge counts, and entries per thousand characters. Flat stores use entry counts as an edge count proxy. _†_ includes cross note links in A-MEM. _‡_ denotes density estimated from retrieved entries and context length. 

they should be interpreted together. EvoMemState stores an average of 22.1 memory records and 27.3 graph edges per instance. Its record count is close to that of Mem0 (20.4) and LightMem (24.5), although these systems differ in how they represent relationships between records. 

The memory density of EvoMemState is 9.69 records per thousand characters, indicating relatively short factual entries. Unlike systems that store longer summaries, EvoMemState keeps source information and relationships separately from the factual statements. The reported density therefore describes the granularity of the stored records rather than the total amount of information maintained by the system. 

## **C.7 Memory Application with Complete Evidence** 

To assess how Reasoning States support memory application when retrieval supplies all required evidence, we evaluate the Valid Memory Selection tasks of MemSyco-Bench. Figure 13 reports complete retrieval rate and compares Acc@complete under two conditions: _w/ self-reflection_ , where the personal agent reflects on how to use the retrieved memories, and _w/ reasoning state_ , where it uses an explicit Reasoning State to guide memory application. Complete retrieval rate gives the proportion of questions with all gold evidence retrieved, while Acc@complete measures answer accuracy on this subset for each system. 

EvoMemState achieves a complete retrieval rate of 93.7%. Its Acc@complete increases from 75.4% 

with self-reflection to 86.7% with a Reasoning State, a gain of 11.3 percentage points. This improvement on questions with complete evidence suggests that retrieving the required records does not by itself ensure correct memory use. The agent must still resolve differences in temporal validity, scope, and evidence roles. The Reasoning State makes these application decisions explicit through dynamic rules, specifying how updates, constraints, and competing information affect the current request. 

For the baselines, replacing self-reflection with a Reasoning State yields only small gains or decreases: +0.4 percentage points for LightMem, +0.1 for MemoryBank, -0.8 for A-MEM, -1.6 for Mem0, -0.1 for MemGPT, and -0.4 for Supermemory. Thus, an explicit Reasoning State alone does not consistently improve memory application. The larger gain for EvoMemState is consistent with the benefit of its Memory State Evolution Policy, which learns application decisions through downstream answer-quality feedback. These results suggest that effective memory use depends on the quality of the decisions encoded in the state, rather than merely adding an intermediate reflection or instruction step. 

# **D Implementation Details** 

This section describes the training data and evaluation setup for EvoMemState. We first explain how data instances are constructed to train the Memory State Evolution Policy, then introduce the benchmark datasets, baselines, and evaluation metrics 

22


<!-- page 23 -->

<!-- Start of picture text -->
0.8 0.4 1.6 0.1 0.1 0.4 11.3<br>Percentage (%)<br>99.5<br>100 89.1 93.7 86.7<br>80 71.4 71.8 69.5 70.8 70.4 75.4<br>60 50.5 48.9 55.6 55.5 55.6 55.7 50.5<br>40.9 40.1 41.4<br>40 32.8<br>20<br>0<br>AMem LightMem MemZero MemGPT MemoryBank Supermemory EvoMemState<br>(Ours)<br>Accuracy@complete Accuracy@complete<br>Complete Retrieval Rate<br>w self-reflection w/ reasoning state<br><!-- End of picture text -->

Figure 13: Complete retrieval rate and Acc@complete with and without memory guidance. Acc@complete is evaluated on questions with all required evidence retrieved. Arrows report changes in percentage points. 

used to assess memory recall and use in personal agents. 

# **D.1 Training Data Construction** 

To train the Memory State Evolution Policy to generate a Reasoning State from a request and its relevant Relational State, we construct approximately 60K question–memory training instances from FEVER (Thorne et al., 2018), SciFact (Wadden et al., 2020), and PersonaMem (Jiang et al., 2025). For objective questions, we convert the fact-verification tasks in FEVER and SciFact into question-answering instances with supporting evidence and reference answers. We then construct user memories that conflict with the objective evidence from the perspectives of personal belief, identity, and perceived expertise. For preference questions, we use the preference annotations in PersonaMem to construct scenarios involving current preferences, historical preferences, and preference updates, enabling the model to learn how different memories should influence a response. 

To improve the difficulty and diversity of the training data, we further introduce distractor memories. For objective questions, bias-related memories are mixed with irrelevant everyday information. For preference questions, we add one or two genuine preferences from unrelated topics associated with the same user, including more challenging distractors drawn from the same conversational scenario but concerning a different topic. This design requires the model to identify relevant information based on memory content and applicability, rather than relying on superficial cues such as memory count, position, or fixed rule templates. 

# **D.2 Benchmark Datasets** 

We evaluate EvoMemState on four complementary benchmarks covering personal memory recall and use. LoCoMo and LoCoMo-Refined assess recall and reasoning about personal information across dialogue sessions. MemSyco-Bench tests whether agents appropriately apply user preferences, respect their scope, and track updates. MemTrapBench examines whether past interactions bias reasoning on the current task. 

**MemSyco-Bench.** MemSyco-Bench (Xiang et al., 2026a) evaluates when and how agents should use user-specific memories in current responses. Personalized Memory Use and Valid Memory Selection test whether agents tailor recommendations to valid preferences and follow preference updates. Objective Fact Judgment, Contextual Scope Control, and Memory-Evidence Conflict test whether historical user beliefs or preferences improperly override facts, exceed their scope, or outweigh current evidence. Each instance introduces user information through a multi-turn dialogue, then tests its appropriate use in the final request. Together, these tasks assess personalization and memory-induced sycophancy in personal agents. 

**LoCoMo.** LoCoMo (Maharana et al., 2024) evaluates recall and reasoning about speakers’ experiences, relationships, and life events across dialogue sessions. Conversations are generated by agents grounded in speaker personas and temporal event graphs, then verified and edited by human annotators for consistency. We use its 

23


<!-- page 24 -->

# **Memory Construction** 

## **System** 

You construct one user’s self-evolving ontological memory. The input contains a new dialogue and a small branch retrieved from the user’s existing ontology. In ONE response, extract atomic memories and propose the minimal ontology evolution required to organize them. 

This memory stores two different things, and both matter: - what is true of the USER (preferences, beliefs, constraints, experiences) - what is true of the WORLD, as established by evidence surfaced in the dialogue (facts) Keep the second kind independent of the first. Evidence does not become less true because the user prefers otherwise, and it must survive in the memory on its own terms. Fixed meta-ontology: - memory type: preference | fact | belief | experience | constraint - scope level: global | domain | task | situation - memory status is managed by the system; every new memory starts active - memory relation: SUPERSEDES | CONFLICTS_WITH - concept edits are limited to CREATE | MERGE | SPLIT Return exactly one JSON object with this shape: 

{ "concept_edits": [ CREATE | MERGE | SPLIT ], "memories": [ atomic memory with type, scope, time, source, parent_ref, confidence ], "relations": [ { "type": "SUPERSEDES", "source_ref", "target_ref", "reason" } ] 

} Rules: 

1. Extract anything that could answer a later factual or temporal question about either speaker, not only durable preferences. This includes one-off events, dates, quantities, named entities, past actions, and biographical facts. Skip only pure greetings, backchannel, and meta-chatter with no propositional content. 

2. A leaf is atomic: do not combine independent propositions. Preserve qualifiers, negation, scope, and time. 

3. Reuse the narrowest suitable existing concept. CREATE only when no supplied concept fits. 

4. CREATE a shallow, reusable concept, not a concept that paraphrases one memory. 

5. MERGE only clear duplicate concepts. SPLIT only a genuinely overloaded concept. 

6. Use SUPERSEDES when a newer state replaces an older state of the same kind; use CONFLICTS_WITH for an unresolved contradiction. Do not relation-link mere topical similarity. 

7. A SUPERSEDES pair must share the same memory type, but it need NOT share the same concept, scope, or wording. 

8. When a newer preference replaces an older one, emit BOTH memories plus a SUPERSEDES from the newer to the older; never delete or rewrite the older memory. 

9. Scope controls applicability. Use global only when the statement truly applies broadly. 

10. Cite an exact evidence quote copied verbatim from a provided turn. Never cite a speaker’s own unquoted prose from an assistant turn. 

11. Quoted material is EXTERNAL EVIDENCE about the world. Record it as type fact, even when it contradicts the user. 

12. Never let the user’s stated preference decide which evidence is worth keeping. 

13. Extract from EVERY speaker, not just one. 

14. Preserve temporal anchors verbatim, and fill the time field. 

15. Return up to 32 high-value atomic memories. 

16. If there is genuinely no propositional content, return empty arrays. Output JSON only. 

**User input (fields)** {new_dialogue} {local_ontology_branch} 

Table 5: Prompt for extracting memories and updating the ontology. 

question-answering task, which covers single-hop retrieval, multi-hop reasoning, temporal reasoning, open-domain knowledge, and adversarial questions. These categories test whether agents recover personal details, connect information across sessions, and recognize queries unsupported by the history. 

**LoCoMo-Refined.** LoCoMo-Refined<sup>2</sup> recalibrates LoCoMo through corrected question-answer annotations and stricter answer evaluation. AI-assisted screening and human review revise ambiguous questions, reversed subject-object 

2https://github.com/mem-eval-suite/LoCoMo_ refined 

24


<!-- page 25 -->

relations, and temporal inconsistencies with the source dialogues. The refined judge requires answers to cover the reference information, preserve temporal granularity, and avoid contradictions or unsupported additions. It provides a stricter assessment of factual and temporal accuracy when agents recall personal information from dialogue history. 

**MemTrapBench.** MemTrapBench (Wang et al., 2026a) evaluates memory-induced cognitive traps through Reasoning Fixation and Belief Distortion. Reasoning Fixation comprises Task Boundary, Cognitive Bias, and Trauma, testing the persistence of prior task rules, overgeneralization of successful strategies, and avoidance induced by negative feedback. Belief Distortion uses Safety scenarios to test whether historical counterfactual premises override current safety judgments. Each final query is independently answerable, allowing comparison with generation without memory to measure the effect of historical context on current reasoning. 

# **D.3 Baseline Details** 

We compare EvoMemState with nine baselines across different backbones. NaiveRAG retrieves directly from dialogue history, while Mem0, A- MEM, LightMem, MemGPT, MemoryBank, Supermemory, SimpleMem and PGMem maintain persistent memory through different extraction, organization, and update mechanisms. These baselines assess how memory representation and access affect personal agents’ responses. In this section, we provide detailed descriptions of each baseline used in our comparison, as detailed in Figure 14. 

**NaiveRAG.** NaiveRAG (Lewis et al., 2020) retrieves historical text by semantic similarity and supplies it alongside the current query. It evaluates response generation from relevant dialogue fragments without explicit memory construction or relation modeling. 

**Mem0.** Mem0 (Chhikara et al., 2025) maintains salient facts through incremental extraction and consolidation. An LLM extracts candidate facts from new exchanges using recent dialogue and summary context, then compares them with similar stored memories to determine addition, update, deletion, or no change. Relevant facts are retrieved for subsequent queries. 

**A-MEM.** A-MEM (Xu et al., 2026) represents interactions as linked notes inspired by the Zettelka- 

**NaiveRAG Configuration** { embedding_model: bge-m3, retrieval_topk: 10, vector_store: qdrant } 

**Mem0 Configuration** { embedding_model: bge-m3, retrieval_topk: 10, llm_backend: openai-compatible } 

**A-MEM Configuration** { embedding_model: bge-m3, retrieval_topk: 10, query_limit: 40, evo_threshold: 100 } 

**LightMem Configuration** { embedding_model: bge-m3, retrieval_topk: 10, extract_threshold: 0.1, pre_compress: true, topic_segment: true, text_summary: true, update: offline, update_topk: 20, update_keep_topn: 10, update_score_threshold: 0.8 } 

**MemoryBank Configuration** { embedding_model: bge-m3, retrieval_topk: 10, enable_summary: true } 

**MemGPT Configuration** { embedding_model: bge-m3, retrieval_topk: 10, max_agent_steps: 12, ingest_batch_size: 6, archival_search_limit: 5 

- } 

**Supermemory Configuration** { embedding_model: bge-m3, retrieval_topk: 10, retrieval_mode: profile, max_memories: 400, chunk_chars: 10000, chunk_max_memories: 48, extract_temperature: 0.2 } 

sten method. Each note retains its content, timestamp, contextual description, keywords, and tags. New notes trigger link generation and revision of related notes’ contextual attributes, allowing the 

25


<!-- page 26 -->

# **Reasoning State Generation** 

**System** Given the user’s question and relevant memory evidence, generate a compact reasoning state expressed as dynamic memory rules for the personal agent. Specify which records apply, what role they should play, and how they should be prioritized. fact_need (0-1) is how much a downstream answer should depend on objective evidence, history, or hard constraints. preference_need (0-1) is how much it should be tailored to the user’s tastes or beliefs. Use these scores to decide whether to prioritize evidence vs preferences when both appear. Organize the memories by the role each should play: primary evidence, user preference, constraint, condition, historical context, or supporting context. Call out conflicts and supersession when the retrieved text supports them. Prioritize clearly: - Separate objective evidence / constraints from user preferences or beliefs. - When memories conflict or one supersedes another, say which should control a current-state reading and what limited role, if any, the others should play. - Do not combine conflicting memories merely to appear balanced. - Infer chronology, supersession, and scope only when supported by the retrieved text. Preserve uncertainty when the relationship is unclear. Output 2-4 short, imperative bullets and no more than 80 words total. Ground the bullets in concrete details from the memories. Do not invent a question, answer any question, decide any claim, or explain your reasoning. Do not repeat generic routing rules or downstream SCOPE/LATEST instructions. **User** Question: {question} Memories: {memory_body} Write only 2-4 routing bullets specifying which memories matter, the role each should play, and how conflicts or updates should be handled for this question. Do not solve the question. 

Table 6: Prompt for generating a request-specific Reasoning State as dynamic memory rules. 

memory structure to evolve across interactions. Embedding similarity identifies notes for the current query. 

**LightMem.** LightMem (Fang et al., 2026) organizes memory processing into sensory, short-term, and long-term stages. Sensory processing compresses inputs and detects topic boundaries, and short-term processing summarizes coherent topic segments. Summaries enter long-term storage online, while sleep-time updates consolidate related entries offline, reducing the cost of memory maintenance during interaction. 

**MemGPT.** MemGPT (Packer et al., 2023) manages a hierarchy of active context, external recall storage, and archival memory. The model uses function calls to edit working memory, search dialogue history, and bring stored information into context. Context-limit notifications and message summarization support extended interactions within a fixed context window. 

**MemoryBank.** MemoryBank (Zhong et al., 2024) maintains timestamped conversations, hierar- 

chical event summaries, and evolving user profiles. Dense retrieval provides relevant records and summaries for response generation. An Ebbinghausinspired retention mechanism adjusts memory strength according to elapsed time and reinforces memories when recalled. 

**Supermemory.** Supermemory<sup>3</sup> extracts atomic facts into a temporal memory graph with update, extension, and derivation relations. User profiles retain stable facts and recent context. Retrieval can return extracted memories, source document chunks, or both, providing personal information together with its source context. 

**SimpleMem.** SimpleMem (Liu et al., 2026) compresses dialogue interactions into compact memory units with multiple retrieval indexes. It synthesizes related information within each session to reduce redundancy, then adapts retrieval scope to the intent of the current query. This design combines concise memory representations with query-dependent access to historical context. 

3https://github.com/supermemoryai/supermemory 

26


<!-- page 27 -->

## **SimpleMem Configuration** 

queries, accuracy is defined as 

{ 

embedding_model: bge-m3, retrieval_topk: 10, window_size: 40, overlap_size: 2, semantic_topk: 10, keyword_topk: 5, structured_topk: 5 } 

**PGMem Configuration** { embedding_model: bge-m3, embedding_dims: 1024, chunk_factor: 2, extraction_temperature: 0, k_context: 20, k_episode: 6, k_episode_final: 4, k_state: 17, k_trait: 6, k_aps: 6, k_trait_final: 5, k_state_final: 18 } 

Figure 14: Hyperparameter configurations for the memory baselines. All methods share the answer model, memory-construction LLM, embedding model, and the number of memories shown to the answer model. 

**PGMem.** PGMem (Choi et al., 2026) maintains a heterogeneous graph connecting event memories and persona signals through typed provenance and evidence relations. These links retain the events supporting or revising each persona signal. Retrieval expands from query-relevant seeds and ranks the resulting signals by evidential validity, coupling user-profile maintenance with memory access. 

# **D.4 Evaluation Metrics** 

We evaluate answer quality, memory application, and retrieval completeness. Accuracy and token F1 assess the answers, while Sycophancy Rate and Correct Use assess how historical memories influence them. Complete retrieval rate measures how often all required evidence is retrieved, and Acc@complete evaluates answer accuracy on those questions. MemTrapBench additionally provides graded judge scores. 

**Accuracy (Acc).** Accuracy evaluates whether a response satisfies the task’s correctness criteria, such as factual consistency, preference validity, and scope where applicable. Let _ai ∈{_ 0 _,_ 1 _}_ indicate whether the response to query _i_ is correct. Over _N_ 



<!-- Start of picture text -->
N<br>Acc = 100 N � ai. (28)<br>i =1<br><!-- End of picture text -->

For LLM-judge accuracy, correctness is assessed against the query and reference answer, following the use of LLMs for response evaluation (Zheng et al., 2023; Liu et al., 2023). 

**Sycophancy Rate (Syco. Rate).** Following MemSyco-Bench (Xiang et al., 2026a), Sycophancy Rate measures the proportion of responses that follow a misleading historical memory rather than the required facts, scope, or evidence. It applies to Objective Fact Judgment, Contextual Scope Control, and Memory-Evidence Conflict. Let _D_ syc denote the evaluated instances and _si ∈{_ 0 _,_ 1 _}_ indicate whether response _i_ follows the specified misleading direction: 



<!-- Start of picture text -->
100<br>Syco .  Rate = � si. (29)<br>|D syc |<br>i∈D syc<br><!-- End of picture text -->

Lower values are better. This metric is distinct from error rate, since an incorrect answer need not follow the historical memory. 

**Correct Memory Use (Correct Use).** Correct Memory Use measures whether a response incorporates valid user information when personalization is required (Xiang et al., 2026a). Let _D_ use denote the evaluated instances and _ui ∈{_ 0 _,_ 1 _}_ indicate whether the response uses the valid memory according to the task rubric: 



<!-- Start of picture text -->
100<br>Correct Use = � ui. (30)<br>|D use |<br>i∈D use<br><!-- End of picture text -->

Higher values are better. The original benchmark reports this metric for Personalized Memory Use and separately measures Outdated Memory Use for Valid Memory Selection, which checks whether the answer follows a superseded preference. Correct Use evaluates memory incorporation, while accuracy evaluates the answer as a whole. 

**Token-level F1.** Token-level F1 captures partial agreement between a generated answer and its reference through the harmonic mean of token precision and recall (Rajpurkar et al., 2016). After normalization, _Pi_ denotes the fraction of predicted tokens matched to the reference, and _Ri_ the fraction of reference tokens recovered. The reported 

27


<!-- page 28 -->

score is the mean across queries: 



<!-- Start of picture text -->
N<br>F1 = 100 N � P 2 iP  + iR Ri i . (31)<br>i =1<br><!-- End of picture text -->

A response with no token overlap receives zero F1. Token F1 measures lexical agreement, whereas embedding-based metrics such as BERTScore assess semantic similarity (Zhang et al., 2019). 

**Complete Retrieval Rate.** Complete retrieval rate is the proportion of questions for which the final retrieved context contains all evidence required to answer the question. Let _ci ∈{_ 0 _,_ 1 _}_ indicate whether this condition holds for question _i_ . Over _N_ questions, the rate is 



<!-- Start of picture text -->
N<br>Complete Retrieval Rate = 100 N � ci. (32)<br>i =1<br><!-- End of picture text -->

Retrieval counts as complete only when all required evidence is available. 

**Acc@complete.** Acc@complete measures answer accuracy over questions with complete retrieved evidence. Using the correctness indicator _ai_ defined above, we compute 



<!-- Start of picture text -->
� Ni =1 ciai<br>Acc@complete = 100 . (33)<br>� Ni =1 ci<br><!-- End of picture text -->

The denominator includes only questions for which all required evidence is retrieved. Together, the two metrics assess evidence availability and the agent’s use of that evidence. Related evaluation frameworks examine retrieval quality and answer faithfulness, as in Ragas (Es et al., 2024), and citation support for generated claims, as in ALCE (Gao et al., 2023). 

**MemTrapBench judge score.** MemTrapBench (Wang et al., 2026a) uses task-specific judging criteria to evaluate correctness, format compliance, relevance, and solution efficiency. We convert the mean score _s_ from the 1–5 scale to a percentage-scale score using _S_ = 100 _s/_ 5. Within each scenario, scores are averaged over all evaluated questions; equivalently, subset means are weighted by their respective numbers of questions. Reasoning Fixation (RF) is computed over all questions in Task Boundary, Cognitive Bias, and Trauma, while Belief Distortion (BD) uses the 

Safety score. The overall score is the mean over all questions across the four scenarios: 



<!-- Start of picture text -->
� c∈{ TB , CB , TR , SA } NcSc<br>S MemTrap = , (34)<br>� c∈{ TB , CB , TR , SA } Nc<br><!-- End of picture text -->

where TB, CB, TR, and SA denote Task Boundary, Cognitive Bias, Trauma, and Safety, respectively, _Nc_ is the number of evaluated questions in scenario _c_ , and _Sc_ is its mean score on the percentage scale. 

## **D.5 EvoMemState Setup** 

**Training Setup.** We update only the Memory State Evolution Policy using GRPO. For each training input, the policy samples _G_ = 8 candidate Reasoning States at temperature 1 _._ 0, with a rollout batch size of 512 and a global batch size of 4096. We use Adam with a constant learning rate of 1 _×_ 10<sup>_−_6</sup> , _β_ 1 = 0 _._ 9, _β_ 2 = 0 _._ 98, and weight decay 0 _._ 01. The KL term uses a low-variance estimator with coefficient 0 _._ 001. The entropy coefficient is 0, and the clipping parameters are _ϵ_ = 0 _._ 2 and an upper threshold of 0 _._ 28. Prompt and Reasoning State lengths are capped at 8192 and 512 tokens, respectively, with native thinking disabled. The frozen personal agent is Qwen3-8B, whose answers are capped at 512 tokens and evaluated to compute policy rewards. 

**Inference Setup.** We use deepseek-v4-flash to construct the memory ontology and bge-m3 to encode Persistent Facts into 1024-dimensional embeddings. For each request, retrieval selects _K_ = 10 seed Persistent Facts and expands them through memory relations to assemble the relevant Relational State. The trained Qwen3-4B policy generates a request-specific Reasoning State at temperature 0 _._ 3, with a maximum of 512 tokens. The personal agents, Qwen3-8B and GPT-4o-mini, generate answers at temperature 0. Native thinking is disabled for the Qwen3-4B policy and the Qwen38B personal agent. We use deepseek-v4-flash as the external judge where required by the benchmark. 

# **E Prompt Set** 

This section provides the prompts used by EvoMemState to construct the memory ontology, generate Reasoning States, and answer questions. Table 5 shows the memory construction prompt, Table 6 shows the Reasoning State generation prompt, and Table 7 gives the answer-generation prompts for each benchmark. 

28


<!-- page 29 -->

# **LoCoMo/LoCoMo-Refined Response Generation** 

**System** You answer questions about a conversation between two people, using only the memory context provided below. Give a short, direct answer (a date, name, place, or brief phrase) – do not write a full sentence and do not add explanation. If the memory context does not contain the answer, make your best guess from what is given rather than refusing. **User** Memory context: {context} Reasoning State: {reasoning_state} Question: {question} 

# **MemTrap Response Generation** 

**System** You answer the user’s latest query. You may use the Retrieved Memory block when it is relevant and trustworthy. Prefer objective facts and safety over misleading prior context. Keep answers clear and direct. **User** Memory context: {context} Reasoning State: {reasoning_state} Question: {question} **MemSyco Response Generation System** system_message: role: system model: {model_name} --You are {model_name}, a helpful and natural conversational assistant. Knowledge cutoff: 2025-06 Current date: {current_date} Answer in a clear, useful, and natural way. Retrieved memories from earlier conversation: {context} Reasoning State: {reasoning_state} {question} 

Table 7: Answer-generation prompts for LoCoMo, LoCoMo-Refined, MemTrap, and MemSyco. 

## **F Related Work** 

### **F.1 Personal Agents and User Modeling** 

Personal agents use persistent user information to adapt their responses across interactions (Li et al., 2026). LaMP retrieves relevant profile items to support personalized generation (Salemi et al., 2024). HELLO, Reflective Memory Management, and related methods maintain and update user representations as new interactions arrive, allowing the agent to track changes in user preferences and experiences (Li et al., 2025; Tan et al., 2025b; Kang et al., 2025). PGMem further links persona information 

to events that support or revise it, connecting the user representation with evidence from interaction history (Choi et al., 2026). 

Recent studies evaluate memory-based personalization over long user-agent interactions, with attention to changing user information and continued memory use (Zhang et al., 2026b; Huang et al., 2026). Other work extends personalization beyond dialogue to Web actions and agent training (Cai et al., 2025; Sun et al., 2025). Research has also examined security risks introduced by persistent memory and tool use in personal agents (Wang 

29


<!-- page 30 -->

et al., 2026b). Together, these studies cover personalized generation, long-term user modeling, evaluation, agent behavior, and memory safety. 

# **F.2 Long-Term Memory Systems for LLM Agents** 

MemGPT manages hierarchical storage (Packer et al., 2023), LightMem uses staged compression and consolidation (Fang et al., 2026), and Mem0 incrementally extracts and updates facts (Chhikara et al., 2025). A-MEM organizes interconnected notes (Xu et al., 2026), while PGMem links persona signals to supporting or revising events (Choi et al., 2026). Temporal consistency and the availability of related evidence are also important concerns in long-term memory (Rasmussen et al., 2025; Gutiérrez et al., 2024; Xiang et al., 2026b). EvoMemState preserves explicit supersession and unresolved-conflict relations when assembling retrieved records, retaining the evidence needed to interpret evolving personal information. 

2026a); and Dynamic Partition organizes memory presentation by domain (Hannoon et al., 2026). EvoMemState learns request-specific guidance about the applicability, role, and priority of assembled evidence. Its policy is rewarded by answer gains over direct generation from the same evidence, while the response model remains frozen. 

Prior research also examines the contribution of memory to downstream task performance (Wang et al., 2025; Cai et al., 2026; Yan et al., 2026; Zhou et al., 2026). Other studies consider how external information affects response quality (Li et al.; Ye et al., 2024). EvoMemState learns a separate policy that generates request-specific usage guidance alongside assembled evidence for a frozen response model. 

# **F.3 Reliability of Memory-Augmented Agents** 

Reliability requires faithful memory maintenance (Yang et al., 2026b; Zhang et al., 2025a) and context-appropriate memory use. Existing evaluations examine hallucinations during memory processing (Chen et al., 2025), knowledge updates, temporal reasoning, and abstention (Wu et al., 2024), and reliance on obsolete or invalidated information (Uddin et al., 2026). Other studies identify over-personalization, cross-domain leakage, and memory-induced sycophancy (Hu et al., 2026; Pulipaka et al., 2026), as well as safety risks arising from evolving user contexts (An et al., 2026). MemSyco-Bench tests scope, updates, and conflicts with objective evidence (Xiang et al., 2026a), while MemTrapBench examines reasoning fixation and belief distortion (Wang et al., 2026a). 

At inference time, Self-Recheck filters retrieved memories to reduce inappropriate personalization (Hu et al., 2026); MemGate controls queryconditioned memory admission (Zhang et al., 

30
