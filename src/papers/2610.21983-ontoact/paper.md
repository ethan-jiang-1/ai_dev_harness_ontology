---
source: 2610.21983-ontoact.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# Preprint. Under review. · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

Preprint. Under review. 

# ONTOACT: HYPOTHESIS-BASED NEURO-SYMBOLIC AGENTS THROUGH ONTOLOGICAL ABSTRACTION 

**Donghyeok Lee**<sup>1</sup> **, Bong Gyun Kang**<sup>1</sup> **, Junyong Ahn**<sup>1</sup> **& Sungroh Yoon**<sup>1</sup><sup>_,_2</sup> 

1Interdisciplinary Program in Artificial Intelligence, Seoul National University, Seoul, South Korea 2Department of Electrical and Computer Engineering, Seoul National University, Seoul, South Korea Correspondence to: Sungroh Yoon <sryoon@snu.ac.kr> 



<!-- Start of picture text -->
(a) Constructing world knowledge (b) Reasoning and acting<br>World knowledge Hypotheses  Symbolic verifier<br>Typed relations + actions<br>Condition status<br>Storage Machine<br>Environment Proposals<br>feeds Condition status + verdicts Action verification<br>Agent<br>Ontological Use world<br>abstraction s ₁ m ₁ knowledge Hypothesis assessment H ?<br>feeds<br>Observations Actions Assess<br>Reference corpus Conditional axiomss ₂ type m ₂ Evidence + hypotheses + update<br>? Machine stoppedUpstream storage empty STOP New evidence ?<br>No incoming material<br>Tacit operational knowledge Storage is a repair candidate Environment<br>(c) Three situations during interaction<br>1 Resolve missing evidence 2 Reject an invalid action 3 Assess a hypothesis<br>Condition status Machine stoppedStorage empty Unresolvedcondition Action verification Required resourcemissing hypothesisCandidate Working hypotheses? SupportedUnresolvedRefuted<br>? Incoming flow Inspect incoming flow Proposed action Revise action Action rejected Check evidence<br>Update hypothesis status<br>Observed ...<br>Intervened ...<br>Outcome ...<br><!-- End of picture text -->

Figure 1: **The LLM proposes, the ontology verifies.** (a) OntoAct abstracts recorded experience into world knowledge over typed entities, relations, and conditions. (b) Symbolic checks assess proposed hypotheses and actions against current evidence. (c) Feedback guides observation, action revision, and hypothesis assessment. 

## ABSTRACT 

Learning from experience requires recovering reusable knowledge and determining when it applies to a new situation. We introduce OntoAct, a hypothesis-based neurosymbolic framework built on _ontological abstraction_ . OntoAct turns individual experiences into axioms over entity types, relations, and conditions, making their underlying patterns reusable across situations. A large language model (LLM) uses this world knowledge to propose hypotheses and actions, while a symbolic verifier assesses their supporting conditions against current observations. Verification identifies missing evidence, and new observations and intervention outcomes update hypothesis assessments and guide subsequent actions. We also introduce Tacit-FLE, a benchmark built on the Factorio Learning Environment (FLE) for diagnosing and repairing hidden faults in existing factories using inherited operational records. Its synthetic maintenance corpus distributes evidence across records, and an executed repair may leave the fault unresolved, requiring agents to reassess their diagnoses through interaction. Across Tacit-FLE, Mars, and ALFWorld, OntoAct achieves leading task performance with efficient interaction and inference. 

1


<!-- page 2 -->

Preprint. Under review. 

# 1 INTRODUCTION 

_“We can know more than we can tell.”_ 

— Michael Polanyi, _The Tacit Dimension_ (Polanyi, 1966) 

Agents often need to act in environments whose operating principles are only partially specified. Inherited logs, notes, and interaction trajectories record what happened and what was done. They may leave unstated the dependencies and conditions that made an action useful, or when that experience applies elsewhere. We call this _tacit operational knowledge_ : knowledge expressed through recorded observations, interventions, and outcomes but left implicit as reusable principles. 

Using this experience requires bridging two gaps. First, the agent must recover patterns that generalize beyond the entities named in individual records. A particular machine–storage connection, for example, instantiates a supplier–recipient relationship; reusable rules express conditions over the entity types and these relational roles. Second, it must determine whether those relationships and conditions hold in its current situation. Both gaps matter whether experience is retrieved as text or encoded as executable or symbolic rules (Lewis et al., 2020; Zhou et al., 2025b; Choi et al., 2025). The agent needs explicit hypotheses that it can test through observation and intervention, retain when supported, and revise when contradicted. 

We introduce OntoAct, a neuro-symbolic framework that connects these tasks through _ontological abstraction_ . It retains incident-specific entities and relations while expressing reusable axioms over types, relational roles, and operating conditions, so the same pattern can be instantiated for different entities. A large language model (LLM) proposes hypotheses and actions from this world knowledge; a symbolic verifier checks their support against current observations (Figure 1). Feedback identifies supported hypotheses and conditions requiring further observation. New observations and intervention outcomes guide hypothesis revision and subsequent actions. The guiding principle is simple: _the LLM proposes, the ontology verifies_ . 

To evaluate knowledge recovery and use, we also introduce Tacit-FLE, a maintenance benchmark built on the Factorio Learning Environment (Hopkins et al., 2025). It asks agents to diagnose hidden faults in existing plants from a finite corpus of synthetic maintenance logs and operating documents, together with live observations (Figure A1). Evidence is distributed across records, and an executed repair may leave the fault unresolved. Success therefore requires selecting useful evidence and translating it into an effective repair. The benchmark evaluates how agents combine inherited knowledge with feedback from their own observations and interventions. Our contributions are: 

- **Tacit-FLE** (Section 2), a benchmark for diagnosis and repair from inherited operational records, designed to test the combination of distributed evidence with observations and intervention outcomes; 

- **OntoAct** (Section 3), a framework that turns individual experiences into reusable ontological world knowledge and uses it to form, test, and revise hypotheses that guide interaction; 

- **Performance and efficiency** (Section 4), demonstrating leading task performance and efficient interaction across Tacit-FLE, Mars, and ALFWorld. We further support these results with a range of analyses across experimental settings. 

We introduce Tacit-FLE in Section 2 and present the OntoAct framework in Section 3. Section 4 evaluates the framework on Tacit-FLE and existing benchmarks, followed by related work in Section 5 and conclusions in Section 6. 

# 2 TACIT-FLE: A BENCHMARK FOR TACIT KNOWLEDGE 

Tacit-FLE evaluates how agents recover dependencies and repair conditions from past incidents and apply them to new faults. Built on the factory simulation of FLE (Hopkins et al., 2025), it pairs existing plants with inherited maintenance records and supports diagnosis through observation and intervention (Appendix A, Figure A1). 

2


<!-- page 3 -->

Preprint. Under review. 

## 2.1 TASK SETTING 

**Existing plant.** An _episode_ starts with one hidden fault in an existing plant. The agent receives unit kinds, positions, and operating readings. Inspections reveal further details, while production evolves as actions advance simulation time (Appendix A.1). 

**Reference corpus.** Each plant comes with a fixed, finite corpus _D_ of synthetic _maintenance logs_ and _operating documents_ , provided before evaluation. The logs describe local observations, checks, repairs, and outcomes; operating documents state selected expectations, such as planned outputs. These sources support inference of component dependencies and repair conditions. 

**Diagnosis and repair.** Within a fixed turn budget, the agent inspects units, waits, or attempts replacements or refills. A replacement restores the unit’s original specification, including configuration. Success requires replacing an accepted repair target or completing a valid refill of an accepted storage target with the required material. Failed attempts consume turns and provide feedback; episodes end upon success or budget exhaustion. 

## 2.2 FAULTS AND DIAGNOSTIC EVIDENCE 

Faults include supply interruptions and off-plan configurations, motivated by component failures and departures from intended operation in process diagnosis (Venkatasubramanian et al., 2003). Drawing on model-based diagnosis (de Kleer & Williams, 1987; 1989), we construct three task types that differ in how inherited records support a new diagnosis. Appendix A.3 provides examples of the records and observations in each setting. 

� **Chain.** Local incidents provide evidence of dependencies between components. For example, one log pairs a stoppage at _B_ with a failure at _A_ ; another pairs a stoppage at _C_ with a failure at _B_ . Combining the incidents suggests a dependency path _A → B → C_ . When _C_ stalls in a new episode, this path guides upstream inspections, where current readings help locate a supply interruption. 

� **Conjunction.** A repair precedent, an operating plan, and a current observation play complementary roles. For example, a past log records that replacing machine _A_ resolved a mismatch between its configured and planned output. In a new episode, the plan specifies product _X_ for machine _B_ , while inspection shows _B_ configured for _Y_ . Recognizing the shared mismatch condition connects a repair demonstrated on _A_ to a candidate intervention on _B_ . 

� **Elimination.** Records describe destroyed units, supply interruptions, and power failures, but omit the off-plan configuration encountered in evaluation. The agent uses recorded symptoms and checks to rule out explanations inconsistent with current observations. Further observations or interventions help distinguish the remaining possibilities. 

**Construction and evaluation.** Plants, fault cases, and reference corpora are generated from a common specification (Appendix A.2), with the evaluation population and scale-specific settings detailed in Appendix A.4 and construction checks in Appendix A.5. Records exclude repairs of evaluation targets; consistent plant-specific identifiers reduce shortcuts from Factorio vocabulary. We report repair success, mean turns, and spurious interventions (executed repairs that do not meet the success criterion); Appendix A.4.1 gives their definitions and aggregation rules. 

# 3 ONTOACT: ONTOLOGICAL ABSTRACTION FOR ACTION 

OntoAct turns inherited experience into reusable world knowledge for assessing proposals during interaction. Following _the LLM proposes, the ontology verifies_ , the LLM proposes axioms, hypotheses, and actions, while a symbolic verifier checks them against supporting evidence using the ontology’s types, relations, and conditions. This division governs both knowledge construction and action (Figure 2). 

## 3.1 ONTOLOGICAL ABSTRACTION 

Reusing an incident requires identifying the relations and conditions that make it relevant to another situation. _Ontological abstraction_ expresses these requirements over entity types and relational roles while retaining the particular facts from which they were drawn. 

3


<!-- page 4 -->

Preprint. Under review. 



<!-- Start of picture text -->
(a) Constructing world knowledge<br>Ontological abstraction Symbolic admission World knowledge<br>Candidate Source Well-typed Admittedcandidates<br>Valid sources<br>Applicable constraints<br>Reference corpus<br>Assertions + axioms with sources Corpus check Typed assertions Conditional axioms<br>Ontology schema<br>(b) Reasoning and acting<br>Current context World knowledgeRelations + axioms Current evidenceObserved + admitted facts ? Working hypothesesAssessed explanations<br>Provide current context Admit Update status<br>(claims → evidence) (hypotheses → hypotheses)<br>Proposal revision Symbolic assessment<br>Update context Proposal Structural claims 1 Admit claimsSchema + available evidence Admitted claims Approved Execution<br>Update evidence<br>Reassess hypotheses Hypotheses 2 Admit + assess hypotheses ?<br>Agent proposer Action Current knowledge + observations Supported Unresolved Refuted Command<br>Goal<br>3 Verify actionApplicable axioms + current context ? Verdict +condition report Environment<br>Blocked; retries left<br>Revise claims, hypotheses, or action<br>Environment interaction New observations + action outcomes<br><!-- End of picture text -->

Figure 2: **The OntoAct framework.** (a) The LLM proposes axioms from a reference corpus; symbolic admission checks their conformance to the schema and applicable evidence constraints. (b) The LLM proposes claims, hypotheses, and actions using the resulting world knowledge; ontologybased verification supplies feedback for revision, while observations and action outcomes update the reasoning context. 

**World knowledge.** An ontology schema _T_ defines entity types, relations, observable attributes, and admissible axiom forms. The corpus-derived ontology separates ground assertions _AW_ from conditional axioms _RW_ , which express action requirements and diagnostic patterns: 



<!-- Start of picture text -->
KW = ( T, AW , RW  ) . (1)<br><!-- End of picture text -->

**Episode evidence.** Applying these reusable conditions requires evidence from the current situation. At step _t_ , _f_ ground converts observations into episode assertions _At_ . These assertions augment the corpus-derived facts, yielding the knowledge used to assess hypotheses and actions: 



<!-- Start of picture text -->
Kt = ( T, AW ∪ At, RW  ) . (2)<br><!-- End of picture text -->

This combines reusable knowledge with current evidence; see Appendix B.3.1 for a detailed example. 

# 3.2 CONSTRUCTING WORLD KNOWLEDGE 

To build this world knowledge, OntoAct processes the reference corpus _D_ before interaction. The LLM proposes candidate axioms, and the ontology checks which ones enter _KW_ . 

**The LLM proposes axioms.** For a record batch _b ⊆ D_ , the LLM proposes ground assertions and conditional axioms in the forms allowed by _T_ : 



<!-- Start of picture text -->
X � b =  f abs( T, b ) =  { ( xi, πi ) } n i =1 b , (3)<br><!-- End of picture text -->

Each candidate conditional axiom _xi_ is paired with source records _πi_ ; _nb_ counts all candidates. 

# **Algorithm 1** Constructing world knowledge 

**Require:** ontology schema _T_ , corpus _D_ 1: _KW ←_ ( _T,_ ∅ _,_ ∅) 2:3: **for** _X_ � each batch _b ← f_ abs( _T, b b ⊆_ ) _D_ **do** _▷_ LLM; Eq. 3 4: **for** each candidate ( _xi, πi_ ) _∈ X_<sup>�</sup> _b_ **do** 5: _αi ←_ Admissible( _xi, πi_ ; _KW , D_ ) _▷_ Eq. 4b 6: **if** _αi_ = 1 **then** 7: _KW ← f_ store( _KW , xi, πi_ ) _▷_ Store pair 8: **end if** 9: **end for** 10: **end for** 11: _KW ← f_ corpus( _KW , D_ ) _▷_ Corpus checks 12: **return** _KW_ 

4


<!-- page 5 -->

Preprint. Under review. 

**The ontology constrains admission.** Admission requires schema and source validity ( _βi_ ) and a set _Cxi_ of tests for its axiom type: 



<!-- Start of picture text -->
βi = Typed( xi ;  T )  1 [∅ ̸  =  πi ⊆ D ] , (4a)<br><!-- End of picture text -->



<!-- Start of picture text -->
αi = Admissible( xi, πi ;  KW , D ) =  βi � 1 [ c ( xi, πi ;  KW , D )] . (4b)<br><!-- End of picture text -->

_c∈Cxi_ 

Here Typed checks schema conformance and **1** [ _P_ ] indicates whether _P_ holds. Every test _c ∈Cxi_ must pass; Appendix B.2 specifies the tests for each environment. Admitted axioms ( _αi_ = 1) enter _AW_ or _RW_ with their sources via _f_ store; _f_ corpus checks the assembled knowledge (Algorithm 1). 

# 3.3 REASONING AND ACTING WITH WORLD KNOWLEDGE 

**The LLM proposes claims and actions.** Let _A_ , _K_ , and _H_ denote current assertions, knowledge, and hypotheses; primes mark updates. Given goal _g_ and feedback _η_ (initially empty each turn), the LLM proposes claims ∆ _A_ , hypotheses ∆ _H_ , and action _a_ : 



<!-- Start of picture text -->
(∆ A,  ∆ H, a ) =  f propose( g, K, H, η ) . (5)<br><!-- End of picture text -->

Structural claims specify relations. Each hypothesis _h_ specifies required relations and nonempty expected conditions Φ( _h_ ), instantiating an induced pattern or proposing a new explanation. 

**Checking claims against current evidence.** For episode claims, _f_ admit checks types, structural evidence, and correspondence with cited patterns, including every required condition. Admitted structural claims update knowledge: 



<!-- Start of picture text -->
A ′ =  A ∪ f admit(∆ A ;  K ) , (6a)<br>K ′ = ( T, AW ∪ A ′ , RW  ) . (6b)<br><!-- End of picture text -->

# **Algorithm 2** Reasoning and acting 

**Require:** _KW_ , goal _g_ , initial observation _o_ 1 **Require:** _B_ turns; up to _J_ proposals per turn 1: _A, H, a_ prev _←_ ∅ 2: **for** _t_ = 1 _, . . . , B_ **do** 3: _A ← f_ ground( _A, ot_ ) _▷_ Observations 4: _K ←_ ( _T, AW ∪ A, RW_ ) 5: _H ← f_ eval( _H_ ; _K, a_ prev) _▷_ Reassess hypotheses 6: _η ←_ ∅ 7: **for** _j_ = 1 _, . . . , J_ **do** 8: (∆ _A,_ ∆ _H, a_ ) _← f_ propose( _g, K, H, η_ ) _▷_ Eq. 5 9: _A ← A ∪ f_ admit(∆ _A_ ; _K_ ) _▷_ Eq. 6a 10: _K ←_ ( _T, AW ∪ A, RW_ ) _▷_ Eq. 6b 11: _H ← f_ eval( _H ∪ f_ admit(∆ _H_ ; _K_ ); _K_ ) _▷_ Eq. 8 12: ( _v, η_ ) _← f_ verify( _a_ ; _K, H_ ) _▷_ Eq. 9 13: **if** _v̸_ = _⊥_ **then break** 14: **end if** 15: **end for** 16: ( _a_ prev _, ot_ +1) _← f_ execute( _a, v_ ) _▷_ Act; observe 17: **if** terminated **then break** 18: **end if** 19: **end for** 

When _h_ instantiates pattern _r_ with conditions Φ _r_ , Φ( _h_ ) retains every condition, substituting current entities. Each atom _φ_ = ( _u, p,_ op _, z_ ) tests entity _u_ ’s observable attribute _p_ against expected value _z_ with comparison op; current readings yield: 



<!-- Start of picture text -->
 ⊤, resolved evidence satisfies  p ( u ) op  z,<br>[[ φ ]] K′ = ⊥, resolved evidence contradicts  p ( u ) op  z, (7)<br><br>? , otherwise .<br><!-- End of picture text -->

Missing readings remain unknown (?), and the same evaluations test action conditions. An open, admitted hypothesis receives the status: 



<!-- Start of picture text -->
refuted , ∃φ ∈ Φ( h ) : [[ φ ]] K′ =  ⊥,<br>Status( h )  ← confirmed , ∀φ ∈ Φ( h ) : [[ φ ]] K′ =  ⊤, (8)<br><br>open , otherwise .<br><!-- End of picture text -->

Confirmation records observational support, subject to refutation by later readings or repair outcomes; updated hypotheses form _H_<sup>_′_</sup> . 

**The ontology verifies the action.** The verifier tests _RW_ : violated conditions and prohibitions block actions; missing readings alone do not. An action requiring explanatory support needs a confirmed hypothesis whose conditions still hold; observations need no confirmed hypothesis. It returns: 



<!-- Start of picture text -->
( v, η ) =  f verify( a ;  K ′ , H ′ ) , (9)<br><!-- End of picture text -->

A blocked verdict _v_ = _⊥_ requests revision while budget remains; _η_ reports failed and unresolved checks. Algorithm 2 summarizes this interaction loop. Appendix B.3 details hypothesis admission, condition evaluation, repair verification, and refutation by observations and outcomes. 

5


<!-- page 6 -->

Preprint. Under review. 

# 4 EXPERIMENTS 

## 4.1 EXPERIMENTAL SETUP 

**Environments and records. Tacit-FLE** tests hidden-fault repair across three task types and plant scales (Section 2). **Mars** (Tang et al., 2024b) tests survival and crafting under altered world mechanics; we use the eight-world configuration of Zhou et al. (2025b). **ALFWorld** (Shridhar et al., 2021) tests household instruction following on 134 unseen tasks. Corpus-based methods share plant maintenance and operating records, Mars exploration records, or ALFWorld training-game trajectories; Appendix E.1 details these corpora and evaluation tasks. 

**Baselines.** We compare **OntoAct** with **ReAct** (Yao et al., 2023), retrieval-augmented **ReAct**<sup>*****</sup> (Lewis et al., 2020), corpus-adapted **Reflexion** (Shinn et al., 2023), and **IfR** (Tang et al., 2024b), which uses natural-language rules. **NeSyC** (Choi et al., 2025) and **WALL-E** (Zhou et al., 2025b) check actions against induced answer-set programs and executable rules, respectively. Implementations and prompts are detailed in Appendix C.2. 

**Models and protocol.** We use GPT-5.6 Luna (OpenAI, 2026a) with reasoning effort none. Medium Tacit-FLE and Mars also use Luna with medium effort (Luna<sup>_R_</sup> ) and GPT-5.6 Terra (Terra; none) (OpenAI, 2026b). Methods share tasks and interaction budgets; Appendix E details settings, budgets, and metrics. 

## 4.2 TACIT-FLE 

**How well does OntoAct repair hidden faults?** Failed repairs consume turns without ending an episode, so eventual success can mask repeated unsuccessful interventions. OntoAct achieves the highest overall success at every scale with 70–91% fewer spurious interventions than IfR, the strongest baseline by overall success (Table 1). It also uses the fewest turns among methods with successful repairs. Its largest advantage is on chain tasks requiring dependency inference across records; IfR matches or exceeds it on elimination. 

Table 1: **Repair performance on Tacit-FLE.** Success (%) by type and overall (All); SI: mean spurious interventions; Turns: mean turns. Failed episodes use the full budget (Appendix A.4.1). Bold: best; underlined: second-best overall success, interventions, and turns. Intervention and turn rankings require at least one repair. 

||||Repair succe|ss (%)_↑_||||
|---|---|---|---|---|---|---|---|
|Scale|Method|�Chain|�Conjunction|�Elimination|All|SI_↓_|Turns_↓_|
||ReAct|0.0|71.4|**75.0**|39.3|4.6|22.2|
||ReAct<sup>*</sup>|15.4|85.7|37.5|39.3|7.2|22.9|
||Reflexion|7.7|71.4|**75.0**|42.9|5.3|23.2|
|Small|l<br>IfR|38.5|**100.0**|**75.0**|64.3|6.4|17.4|
||NeSyC|0.0|0.0|0.0|0.0|0.0|30.0|
||WALL-E|7.7|14.3|12.5|10.7|7.1|29.0|
||OntoAct (ours)|**69.2**|**100.0**|**75.0**|**78.6**|**1.9**|**11.8**|
||ReAct|28.6|64.3|75.0|52.8|11.3|41.8|
||ReAct<sup>*</sup>|21.4|64.3|87.5|52.8|13.4|38.7|
||Reflexion|21.4|42.9|37.5|33.3|15.4|46.4|
|Medium|l<br>IfR|28.6|85.7|**100.0**|66.7|11.9|31.7|
||NeSyC|0.0|0.0|0.0|0.0|0.0|60.0|
||WALL-E|14.3|28.6|87.5|36.1|10.1|48.0|
||OntoAct (ours)|**57.1**|**100.0**|**100.0**|**83.3**|**2.4**|**19.4**|
||ReAct|5.9|72.7|75.0|45.0|16.1|49.9|
||ReAct<sup>*</sup>|23.5|36.4|66.7|40.0|19.6|56.4|
||Reflexion|11.8|9.1|50.0|22.5|23.2|63.1|
|Large|l<br>IfR|23.5|90.9|**100.0**|65.0|17.8|42.6|
||NeSyC|0.0|0.0|0.0|0.0|0.0|75.0|
||WALL-E|5.9|45.5|75.0|37.5|14.9|56.6|
||OntoAct (ours)|**82.4**|**100.0**|91.7|**90.0**|**1.6**|**17.2**|



6


<!-- page 7 -->

Preprint. Under review. 



<!-- Start of picture text -->
Small Medium Large<br>100<br>75<br>50<br>25<br>0<br>Init. +1 +2 +3 … Final<br>Target precision (%)<br><!-- End of picture text -->



<!-- Start of picture text -->
Luna Luna R Terra SI<br>100 16<br>75 12<br>50 8<br>25 4<br>0 0<br>ReAct ReAct*Reflexion IfROntoAct⋆<br>Repair success (%) Spurious interv. ( ↓)<br><!-- End of picture text -->

Figure 3: **Hypothesis precision over turns.** Target precision for all tracked hypotheses before selection (Init.) and those retained +1/+2/+3 turns after admission or at the final episode turn. 

Figure 4: **Repair success and SI.** Medium TacitFLE, 36 tasks. Bars: success (left); markers: mean SI (right, lower is better). _R_ : medium reasoning. Full metrics are in Table A15. 

**Does diagnosis narrow toward the true fault?** OntoAct proposes fewer replacement targets than WALL-E and IfR, yet covers the true fault more often, overall and within its first three candidates (Table 2). Across scales, 71.4–90.0% of targetaligned hypotheses remain and 95.6–99.6% of off-target hypotheses are refuted (Figure 3; Table A27). Appendix D.7 details this refinement from observations and unsuccessful repairs. 

Table 2: **Candidate count and fault coverage.** Medium Tacit-FLE (36 tasks); targets include unexecuted proposals. Coverage counts tasks with the true fault among all candidates or the <u>first three.</u> 

||OntoAct|WALL-E|IfR|
|---|---|---|---|
|Distinct candidates/episode|3.36|5.14|9.00|
|Fault in candidate set|32/36|17/36|24/36|
|Fault in first 3|25/36|10/36|4/36|



**Does OntoAct benefit from reasoning and stronger backbones?** OntoAct benefits from both: reasoning and Terra raise success from 83.3% to 97.2% and 100.0%, while SI falls from 2.39 to 0.75 and 0.44, respectively (69% and 81% reductions; Figure 4). ReAct and ReAct<sup>*</sup> achieve higher success with Terra than with added reasoning, whereas Reflexion and IfR benefit more from reasoning. Yet higher success can mask repeated failed repairs: with reasoning or Terra, these baselines still incur 7.9–13.7 spurious interventions per episode. OntoAct also reduces mean turns from 19.4 to 8.4 in both conditions (Table A15). 

OntoAct benefits from both: 

# 4.3 MARS 

**How well does OntoAct adapt to altered mechanics?** OntoAct supports action under changed prerequisites, extending the framework’s utility beyond hidden-fault diagnosis. It achieves the highest mean Reward and Score across the seven modified worlds (Table 3), although combined changes remain difficult. Inspecting NeSyC’s low-scoring runs reveals overly restrictive learned conditions that block planning and trigger repeated waiting; Appendix D.2 details these failures. 

Compared with ReAct<sup>*</sup> , the strongest baseline by mean Score, OntoAct achieves about 50% higher Score with 45% fewer evaluation tokens per environment step (0.84k versus 1.54k; Figure 5). Compact learned conditions shorten input contexts at similar LLM call rates. Appendix D.6 analyzes context usage and reports construction costs separately. 



<!-- Start of picture text -->
OntoAct<br>16<br>12 ReAct *<br>ReAct IfR<br>8<br>Reflexion WALL-E<br>4<br>NeSyC<br>0<br>0.5 1 2 5 10<br>Evaluation tokens / env. step (k)<br>Score (%, world mean)<br><!-- End of picture text -->

Figure 5: **Mars Score and evaluation tokens.** Luna, seven modified worlds. Equal world weights; input/output tokens exclude knowledge construction. 

7


<!-- page 8 -->

Preprint. Under review. 

Table 3: **Mars Reward and Score by world.** Luna; five evaluation episodes per world. Reward combines achievement rewards and health changes (mean _±_ sample SD); Score geometrically aggregates achievement success rates. Average excludes Default; its Reward SD is computed across matched-seed world averages. Bold/underlined: best/second-best. Metric definitions are in Appendix E.3. 

|World|ReAct|ReAct<sup>*</sup>|Reflexion|IfR|NeSyC|WALL-E|OntoAct|
|---|---|---|---|---|---|---|---|
||||_Re_|_ward ↑_||||
|Default|10_._10_±_4_._80|9_._30_±_1_._64|7_._90_±_2_._95|8_._10_±_2_._35|0_._70_±_0_._55|6_._30_±_6_._06|**12****_._10****_±_1****_._22**|
|Terrain|8_._70_±_2_._30|12_._16_±_4_._03|8_._68_±_5_._66|9_._30_±_3_._96|_−_0_._90_±_0_._00|7_._50_±_3_._78|**12****_._30****_±_1****_._92**|
|Survival|7_._10_±_4_._00|9_._50_±_3_._44|6_._30_±_5_._07|7_._30_±_4_._82|0_._98_±_0_._99|6_._30_±_4_._97|**10****_._46****_±_6****_._39**|
|Task dep.|4_._10_±_1_._00|2_._90_±_1_._30|4_._10_±_2_._92|7_._30_±_1_._10|0_._90_±_0_._45|3_._90_±_0_._84|**11****_._30****_±_1****_._10**|
|Terr. surv.|6_._10_±_2_._35|**8****_._10****_±_2****_._35**|5_._10_±_2_._92|6_._10_±_4_._30|2_._70_±_1_._82|3_._90_±_3_._11|6_._30_±_3_._03|
|Terr. task|3_._50_±_1_._67|6_._90_±_2_._17|6_._48_±_2_._56|3_._90_±_2_._05|1_._10_±_1_._00|2_._90_±_1_._64|**7****_._70****_±_2****_._88**|
|Surv. task|**6****_._50****_±_6****_._11**|2_._10_±_2_._74|3_._70_±_2_._41|**6****_._50****_±_4****_._04**|2_._30_±_1_._30|5_._70_±_5_._18|5_._50_±_6_._02|
|All three|0_._90_±_2_._68|**1****_._50****_±_2****_._61**|0_._50_±_1_._14|_−_0_._10_±_1_._30|_−_0_._90_±_0_._00|0_._70_±_1_._52|1_._10_±_2_._12|
|Average|5_._27_±_1_._10|6_._17_±_1_._31|4_._98_±_1_._40|5_._76_±_2_._14|0_._88_±_0_._37|4_._41_±_1_._91|**7****_._81****_±_1****_._75**|
||||_Sco_|_re (%) ↑_||||
|Default|**31****_._85**|13_._54|13_._67|11_._74|0_._69|15_._26|29_._70|
|Terrain|12_._71|32_._88|19_._29|22_._61|0_._00|13_._32|**34****_._34**|
|Survival|11_._10|18_._29|11_._58|14_._79|1_._15|11_._94|**25****_._83**|
|Task dep.|3_._26|2_._01|4_._46|8_._44|0_._51|2_._69|**20****_._73**|
|Terr. surv.|6_._49|**10****_._52**|5_._79|10_._12|2_._30|5_._10|7_._63|
|Terr. task|2_._65|6_._93|6_._31|3_._21|0_._76|2_._36|**10****_._17**|
|Surv. task|**17****_._65**|2_._18|3_._19|7_._09|1_._49|8_._73|11_._50|
|All three|**1****_._80**|1_._69|0_._67|0_._74|0_._00|1_._19|1_._27|
|Average|7_._95|10_._64|7_._33|9_._57|0_._89|6_._47|**15****_._92**|



**Does OntoAct benefit from more capable models?** OntoAct’s gains from reasoning and stronger backbones persist across environments, even though baseline responses change (Table 4). Unlike in Tacit-FLE, all displayed Mars baselines benefit from both changes; IfR narrows the gap under reasoning. OntoAct still retains the highest mean Score, supporting the framework’s ability to build on model improvements in both diagnosis and action under altered mechanics. Full results appear in Appendix D.2. 

Table 4: **Mars Score across model conditions.** Mean Score (%) over seven modified worlds. Bold/underlined: best/second-best per condition. 

|Method|Luna|Luna<sup>_R_</sup>|Terra|
|---|---|---|---|
|ReAct|7.95|13.06|13.91|
|ReAct<sup>*</sup>|10.64|15.23|16.48|
|Reflexion|7.33|12.91|12.09|
|IfR|9.57|20.60|18.86|
|WALL-E|6.47|9.93|7.79|
|OntoAct (ours)|**15.92**|**22.99**|**21.57**|



**Do learned conditions guide actions before execution?** OntoAct checks candidate actions Table 5: **Violations of shared learned conditions.** against learned rules before execution. For Resource conditions correctly stored by both methresource conditions learned correctly by both ods. Luna, seven modified worlds, 35 episodes methods, OntoAct redirects all 70 violating iniper method. Fractions use each method’s eligible tial candidates before execution, whereas IfR candidates or commands at the specified stage; Apexecutes 20 violating commands and replans af- <u>pendix D.4 details matching and denominators.endix D.4 details matching and denominators.g and denominators. and denominators.</u> ter their failures (Table 5). The distinction is OntoAct IfR when knowledge changes behavior: OntoAct 70/245 20/107 checks represented requirements against the curInitial candidate violations (28.6%) (18.7%) rent state before spending an environment in70/70 0/20 teraction. None of its 136 issued commands Redirected before execution (100%) (0%) violates these shared conditions. These traces 0/136 20/107 cover matched knowledge on different trajecIssued command violations (0%) (18.7%) tories; broader resource-rule coverage remains incomplete. Appendix D.4 details the shared-condition matching, trajectory analysis, and coverage limits. 

Table 5: **Violations of shared learned conditions.** Resource conditions correctly stored by both methods. Luna, seven modified worlds, 35 episodes per method. Fractions use each method’s eligible candidates or commands at the specified stage; Ap- <u>pendix D.4 details matching and denominators.endix D.4 details matching and denominators.g and denominators. and denominators.</u> 

8


<!-- page 9 -->

Preprint. Under review. 

## 4.4 ALFWORLD 

**Can OntoAct maintain high success with** Table 6: **ALFWorld success and evaluation cost. fewer LLM calls?** OntoAct completes Luna. SR: success (%); mean environment Steps, 132/134 tasks versus 129/134 for WALL-E, LLM Calls, and Tokens (k) per episode.<sup>_†_</sup> Initial using 52.5% fewer LLM calls and 32.6% fewer object locations and inventoryject locations and inventoryect locations and inventoryy <u>provided.rovided.</u> evaluation tokens (Table 6). Most savings arise Method SR (%) Steps Calls Tokens (k) from OntoAct’s symbolic condition checks versus WALL-E’s extra LLM outcome-prediction NeSyC<sup>_†_</sup> 26.1 38.6 9.3 281.32 calls (1.02 versus 1.95 calls per environment WALL-E 96.3 14.8 28.8 47.70 OntoAct (ours) 98.5 13.5 13.7 32.16 step); shorter trajectories also contribute. NeSyC’s 26.1% uses disclosed initial object locations and inventory ( _†_ ); Appendix D.5 compares observation conditions and LLM call roles. Task-family results and separate knowledge-construction costs appear in Appendices D.5 and D.6. 

Table 6: **ALFWorld success and evaluation cost.** Luna. SR: success (%); mean environment Steps, LLM Calls, and Tokens (k) per episode.<sup>_†_</sup> Initial object locations and inventoryject locations and inventoryect locations and inventoryy <u>provided.rovided.</u> 

# 5 RELATED WORK 

**Neuro-symbolic LLM agents.** Neuro-symbolic agents keep what an LLM learns about an environment in a checkable form, as code world models and planning domains (Tang et al., 2024a; Khan et al., 2026; Zhu et al., 2025), dependency graphs (Nottingham et al., 2023), or rule bases (Chen et al., 2024), each refined against the agent’s own interaction. WALL-E learns code rules and a state graph from mismatches between the predictions of an LLM world model and observed transitions, and lets the rules veto actions (Zhou et al., 2025b); NeSyC learns and continually repairs symbolic knowledge in answer-set form with a hypothesis-testing loop (Choi et al., 2025); IfR induces natural-language rules from experience in Mars (Tang et al., 2024b). A complementary line separates proposing from checking: solvers decide what an LLM formalizes (Pan et al., 2023; Olausson et al., 2023; Ye et al., 2023), and external critics or runtime guards check the plans and actions it proposes (Kambhampati et al., 2024; Chen et al., 2025; Xiang et al., 2025). 

**Acting with ontologies and knowledge graphs.** Agents also use structured knowledge: ontologies mediate planning (John & Koopmann, 2024), scene and procedural graphs constrain LLM planners (Rana et al., 2023; Zhou et al., 2025a), knowledge graphs serve as memory (Anokhin et al., 2025) and as the reference against which LLM plans are verified (Petruzzellis et al., 2025), and such graphs are built from text, including maintenance records (van Cauter & Yakovets, 2024; Zhang & Soh, 2024). OntoAct joins these threads by inducing ontological world knowledge from inherited records, and Tacit-FLE evaluates the repairs that follow. 

# 6 CONCLUSION 

We introduced OntoAct, a hypothesis-based neuro-symbolic framework that connects learning from experience to action through ontological abstraction. It recovers reusable axioms over entity types, relations, and conditions from operational records. An LLM uses this knowledge to propose hypotheses and actions, while symbolic verification checks their support against current evidence. Observations and intervention outcomes continually refine hypothesis assessments and guide subsequent decisions. We also introduced Tacit-FLE to evaluate how agents combine inherited operational knowledge with observation and intervention to diagnose and repair hidden faults. 

OntoAct achieves the highest overall repair success at every Tacit-FLE scale while substantially reducing spurious interventions. Reasoning and stronger backbones further increase success and reduce unsuccessful repairs. Results on Mars and ALFWorld extend these benefits to altered world mechanics and household tasks, demonstrating strong task performance alongside efficient interaction and inference. Our evaluation uses predefined ontology schemas and world mechanics that remain fixed during interaction. Future work will explore learning and extending these schemas from experience, and revising world knowledge as environments evolve. Together, these results show how reusable abstractions, explicit hypotheses, and ongoing verification connect accumulated experience to more successful and efficient action. 

9


<!-- page 10 -->

Preprint. Under review. 

## ETHICS STATEMENT 

All experiments run in simulators on synthetic data. The maintenance corpus of Tacit-FLE is generated and contains no record of any real plant, person, or organization. The work targets industrial maintenance, where an agent’s interventions can carry physical risk; the verifier of OntoAct is a step toward auditability, not a safety guarantee, and we make no claim of readiness for deployment. 

## REPRODUCIBILITY STATEMENT 

The benchmark generator, the agent, and every baseline port, with the seeds and prompts used in the experiments, will be released with the camera-ready version. Appendix A specifies the generator, Appendix C the bindings and baselines, and Appendix E the settings, budgets, and metric definitions behind each number.
