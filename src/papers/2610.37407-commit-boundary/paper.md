---
source: 2610.37407-commit-boundary.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# Constraining the Commit Boundary: A DIO/ODI-Informed Authorization Guardrail for Agentic Entity Resolution · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

# Constraining the Commit Boundary: A DIO/ODI-Informed Authorization Guardrail for Agentic Entity Resolution 

Daniel Beránek 

Independent Researcher, Brno, Czech Republic 

dan@danielberanek.cz 

November 4, 2026 

## **Abstract** 

Agentic Entity Resolution (ER) systems iteratively plan actions, retrieve evidence, revise hypotheses, and propose graph mutations. An erroneous identity hypothesis may condition later retrieval and produce apparent confirmation. This paper proposes a Digital Identity Optimization (DIO) and Ontology of Digital Identity (ODI)-informed authorization boundary between evidence available for reasoning and evidence eligible to authorize persistent identity-changing mutations. A domain-governed constraint-binding function maps selected reconstruction-failure distinctions to identity-preserving constraints. An abstract two-phase supervisor permits commitment only when claim-specific authorization-eligible evidence supports every required proposition, relevant conflicts are resolved, scope is valid, and bound state and policy versions remain current. Admission as `UNVERIFIED` does not confer authorization eligibility; separate claim-specific promotion is required, and insufficient support or unresolved material conflict defers the mutation. The guarantee is conditional on adequate domain policy, sound claim-specific evidence promotion, and faithful enforcement; the specification does not independently establish promotion correctness or semantic truth. The proposed contribution is a DIO/ODI-informed diagnostic-to-constraint organization integrated with an explicit authorization contract for claim-specific evidence promotion and mutation-specific proposition requirements. Scope binding, conflict handling, and commit-time version checks are treated as necessary contract elements, not as novel mechanisms in isolation. This is a conceptual architecture without implementation or empirical validation. It does not prevent erroneous hypotheses or hypothesis-conditioned retrieval; dependency-aware evidence flow remains future research. 

**Keywords:** Digital Identity Optimization (DIO); Ontology of Digital Identity (ODI); Agentic Entity Resolution; commit-boundary authorization; identity-preserving constraints; claim-specific evidence promotion. 

1


<!-- page 2 -->

# **Contents** 

|1. Introduction|3|
|---|---|
|2. Related Work and Positioning|5|
|3. Diagnostic Failure-Path Analysis of Agentic ER|7|
|3.1 Referential Reconstruction Failures (RRF) . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>7|
|3.2 Semantic Coherence Failures (SCF) . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>7|
|3.3 Temporal Reconstruction Failures (TRF) . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>8|
|3.4 Contextual Adequacy Failures (CAF) . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>8|
|3.5 Failure Stage, Control Boundary, and Limitation<br>. . . . . . . . . . . . . . . . . . .|. . . .<br>8|
|4. A Stylized Model of Apparent Verification|9|
|4.1 A Possible Hypothesis-Conditioned Feedback Path . . . . . . . . . . . . . . . . . .|. . . .<br>9|
|5. DIO/ODI-Informed Mutation Authorization|10|
|5.1 Semantic Target: Reconstruction Admissibility and Observation Context<br>. . . . .|. . . .<br>10|
|5.2 Constraint Binding and Its DIO/ODI Contribution . . . . . . . . . . . . . . . . . .|. . . .<br>11|
|5.3 Evidence States and Promotion Contract . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>12|
|5.4 Authorization Invariant and Assumptions . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>15|
|5.5 Boundary and Future Direction: Dependency-Aware Evidence Flow . . . . . . . .|. . . .<br>16|
|6. Abstract Interface Specification|17|
|6.1 State, Scope, and Version Contracts<br>. . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>17|
|<br>6.2 Phase 1 — Pre-Execution Authorization . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>18|
|6.3 Phase 2 — Post-Execution Validation and Commit<br>. . . . . . . . . . . . . . . . . .|. . . .<br>19|
|7. Illustrative Case: Corporate Entity Resolution in B2B Data Lakes|22|
|7.1 Scenario and Domain Constraints<br>. . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>22|
|7.2 Failure Case: Relatedness Is Mistaken for Identity<br>. . . . . . . . . . . . . . . . . .|. . . .<br>22|
|7.3 Temporal Scope Case: Reused Source-Local Identifier<br>. . . . . . . . . . . . . . . .|. . . .<br>23|
|7.4 Contrast Case: Documented Identity Continuity . . . . . . . . . . . . . . . . . . .|. . . .<br>23|
|8. Proposed Evaluation Protocol|23|
|8.1 Baselines and Corpus Construction . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>23|
|<br>8.2 Evaluation Metrics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>25|
|9. Limitations and Future Research|27|
|9.1 Dependency-Aware Evidence Flow . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>28|
|9.2 Domain-Policy Construction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>28|
|<br>9.3 Multi-Agent and Contextual Negotiation<br>. . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>28|
|10. Conclusion|28|
|References|29|
|Methodological Note on Model-Assisted Development of This Paper|32|



2


<!-- page 3 -->

# 1. Introduction 

Entity Resolution (ER) is the data-management task of determining whether distinct records, mentions, or representations refer to the same real-world referent. It supports master data management, knowledge-graph construction, and cross-silo integration in heterogeneous data environments [12, 19]. Traditional ER systems compare candidate pairs or clusters using rules, learned representations, or combinations of both [10, 12, 16, 25]. Entity linking and explainable entity matching address adjacent problems at mention or pair level [2, 3], while pretrained language models and LLM-assisted methods broaden the range of evidence and comparisons available to ER pipelines [15, 16, 20, 25]. This paper addresses a governance question that becomes especially important when resolution is iterative: which evidence may authorize a persistent identity change, and under what conditions may a proposed graph mutation be committed? 

Recent work has framed Agentic ER as a sequential decision-making process in which an autonomous agent plans actions, gathers evidence iteratively, invokes tools, revises its beliefs, and selectively defers cases [17]. This creates opportunities for adaptive evidence acquisition, but it also makes later actions dependent on prior intermediate states. A mistaken identity hypothesis can condition a retrieval query; the resulting material may be relevant to that query without independently establishing the identity claim. If the agent then treats the material as confirmation, an initial error may become harder to dislodge. We use _apparent verification_ for this possible mechanism. It is an analytical construct, not a claim that iterative retrieval inevitably produces self-confirmation; retrieval-augmented systems have been studied for related vulnerability patterns [23]. The problem is not that an agent must never reason with incomplete or uncertain evidence. Exploratory reasoning often requires provisional hypotheses. The architectural question is whether a hypothesis or observation that is useful for planning should automatically be eligible to authorize a persistent change to an entity’s identity. This paper proposes that these statuses should be separated. The agent may retain a provisional interpretation for reasoning, while a protected mutation boundary requires evidence that has passed a distinct, claim-specific authorization process. This guarantee is conditional on adequate domain policy, sound claim-specific evidence promotion, and faithful enforcement at the protected write boundary. The supervisor applies the stated contract to the evidence and validation records it receives; it does not independently establish the semantic correctness of the promotion decision or the underlying identity evidence. 

The paper connects this boundary to the Digital Identity Optimization (DIO) and Ontology of Digital Identity (ODI) Reference Model [5, 8, 9]. DIO/ODI supplies a reconstruction-oriented vocabulary and diagnostic distinctions across referential, semantic, temporal, and contextual failure modes [4, 6, 7]. The contribution here is not to claim that provenance tracking, invariant checks, transaction versioning, abstention, or human review are new in isolation. It is to propose an explicit bridge between DIO/ODI reconstruction diagnostics and mutation-specific authorization constraints, with a clear boundary around the property the architecture claims to provide. The proposed contribution has four parts: 

1. A lifecycle-to-boundary analysis that maps possible Agentic ER failure pathways to the guardrail’s controls and explicitly stated limitations. 

2. A domain-governed constraint-binding function that translates selected DIO/ODI distinctions into inspectable identity-preserving conditions for particular mutation classes. 

3. An abstract two-phase Minimum Viable Digital Identity Optimization (MVDIO) Supervisor Layer that separates Planner-visible evidence from claim-specific authorization-eligible evidence and gates persistent graph mutations on semantic evaluation, authorized scope, and valid state/policy versions. 

4. A prospective evaluation protocol that separates the effect of DIO/ODI-informed constraints from conventional identifier rules, generic authorization gates, and default-deny/abstention 

3


<!-- page 4 -->

# baselines. 

The formal invariant summarizes these obligations; it is not presented as an independent theorem of semantic correctness. The contribution is the proposed DIO/ODI-informed organization of domain constraints for mutation-specific authorization, integrated with established requirements for claim-specific evidence promotion, proposition coverage, conflict handling, scope binding, and commit-time version integrity. These contract requirements are not claimed as individually novel. This is a conceptual architecture and research proposal, not a completed implementation or an empirical claim of effectiveness. In particular, it does **not** prevent the agent from forming a wrong hypothesis, eliminate hypothesis-conditioned retrieval, or establish that all apparent confirmations are detected. A broader information-flow design that tracks dependencies between hypotheses, actions, observations, and subsequent claims remains a separate research direction. 



<!-- Start of picture text -->
1 · DIAGNOSTIC-TO-CONSTRAINT DESIGN<br>DIO/ODI diagnostics inform Constraint binding μΩ instantiates Identity-preserving constraints V_E<br>RRF · SCF · TRF · CAF domain-governed design step domain-configured constraint set<br>selected reconstruction-failure distinctions entity class · context · mutation class<br>2 · AGENTIC ER AND MUTATION CONTEXT<br>Agentic ER Planner proposes Proposed mutation m derives Supervisor derives required claims q_m<br>provisional hypotheses and reasoning operation · target · effect scope from m, domain constraints V_E, and versioned policy<br>3 · EVIDENCE ADMISSION AND CLAIM-SPECIFIC ELIGIBILITY<br>Observation P_quar P_active Claim-specific promotion P_auth(q_m, ω)<br>retrieved material QUARANTINE_EVIDENCE UNVERIFIED q_m · ω · policy claim-specific<br>admission conflict check Planner-visible recorded provenance authorization-eligible<br>not positive authorization support and validation basis evidence<br>4 · TWO-PHASE SUPERVISOR AND PROTECTED COMMIT<br>PHASE 1 · PRE-EXECUTION PHASE 2 · POST-EXECUTION Commit gate<br>Atomic<br>Authorize proposed mutation Validate isolated candidate G_cand PASS commit<br>q_m · V_E · P_auth · conflict state re-derived q_m · α_m · P_auth coverage AND ScopeValid<br>G_prod · v_G<br>issues α_m: claims · scope · versions G_cand · conflicts · V_E · scope/versions · σ_c AND VersionsValid<br>BREACH: reject / escalate<br>UNKNOWN_EVIDENCE: defer<br>CONDITIONAL GUARANTEE · ASSUMPTIONS 1–7<br>Domain-policy adequacy · sound claim-specific promotion · fail-closed behavior · enforced protected write path<br>derived claims · scope/version integrity · recorded-basis and eligibility integrity<br>OUTSIDE THE PRESENT ARCHITECTURE · FUTURE RESEARCH<br>Dependency-aware evidence lineage and control of the full hypothesis-conditioned feedback loop<br><!-- End of picture text -->

Figure 1: Overview of the proposed DIO/ODI-informed commit-boundary architecture. Selected diagnostic distinctions inform domain-configured identity-preserving constraints; the proposed mutation and versioned policy determine required propositions; and observations progress through admission and claim-specific promotion. `UNVERIFIED` evidence remains available for Planner reasoning but cannot provide positive authorization support, although it may indicate an unresolved conflict. The twophase supervisor validates the proposed operation and then the realized candidate. A protected commit requires `PASS` , valid scope, and valid versions at the same commit snapshot. The guarantee is conditional on Assumptions 1–7. Dependency-aware control of the upstream feedback loop is outside the present architecture. 

4


<!-- page 5 -->

# 2. Related Work and Positioning 

The general mechanisms used by the proposed guardrail—authorization gates, provenance records, version checks, graph validation, scope binding, and conservative deferral—are established in adjacent work. The comparison below therefore focuses on each line’s relevant contribution and the narrower identity-resolution question addressed here; it does not imply that a mechanism omitted from a row is absent from the cited system. 

Table 1: Positioning relative to adjacent work. 

|**Prior work / line**|**Established contribution**<br>**relevant here**|**Scope and distinction of this paper**|
|---|---|---|
|Conventional ER,<br>LLM-assisted ER, and<br>Agentic ER [10, 12,<br>15–17, 20, 25]|Entity matching, data integration,<br>language-model assistance, and<br>sequential agent workflows.|Does not propose a new matching algorithm<br>or agent workflow. Focuses on authorization<br>conditions for persistent identity-changing<br>mutations.|
|Constraint-based<br>deduplication and ER<br>[37]|Declarative and domain-specific<br>constraints can restrict collective<br>deduplication;<br>must-link/cannot-link constraints<br>and richer relational constraints are<br>established approaches.|Does not claim to introduce constraint-based<br>ER. Uses selected DIO/ODI reconstruction<br>distinctions to organize mutation-specific<br>propositions and authorization at an agentic<br>persistence boundary.|
|Ontology-governed<br>enterprise agents [29]|Ontology-grounded entity<br>alignment, graph simulation,<br>isolated staging,<br>provenance-bearing traces, and<br>confidence-gated acceptance with<br>clarification or ontology-gap<br>handling.|Targets heterogeneous ER merges and<br>identity-continuity claims through<br>DIO/ODI-informed, mutation-specific policy<br>rather than a configured enterprise-ontology<br>scenario.|
|Runtime authorization<br>of agent-generated<br>subgoals [28]|Version-bound authorization<br>witnesses and rechecking protected<br>effects at an atomic commit<br>boundary.|Treats the general runtime authorization<br>boundary as prior work; focuses on the<br>identity or continuity propositions and<br>evidence required for a particular ER<br>mutation.|
|Commit-time<br>authorization [32]|Freshness, causal precedence, effect<br>binding, and revalidation of<br>authority for durable effects.|Shares the commit-time concern but asks<br>which identity or continuity proposition<br>must be established, not only whether earlier<br>authority remains valid.|
|Hard-KLAIM and<br>AGATE [33, 34]|Hard-KLAIM: typed effects,<br>operational semantics,<br>proposal–approval–commitment<br>binding, provenance constraints,<br>and mechanized trace-safety<br>proofs. AGATE: an implemented<br>runtime authorization/provenance<br>gate with parameter-bound grants,<br>source observations, effect tracking,<br>and empirical evaluation.|Does not claim comparable formal proof,<br>implementation, or empirical evaluation.<br>Proposes an ER-specific semantic<br>authorization contract.|
|EBL-Core and<br>CONTINUITY [35, 36]|Candidate-bound execution<br>authorization, evidence and policy<br>binding, current-condition checks,<br>and continuity of authorization<br>context across agent components.|Does not propose another general<br>execution-boundary contract; focuses on<br>identity propositions and domain constraints<br>for an ER mutation.|



5


<!-- page 6 -->

|**Prior work / line**|**Established contribution**<br>**relevant here**|**Scope and distinction of this paper**|
|---|---|---|
|ARGUS [22]|Influence-provenance tracing,<br>selective admission of context as<br>usable evidence, and<br>evidence-sensitive authorization of<br>consequential actions.|Addresses a different threat model. The<br>present design does not reconstruct<br>comprehensive causal lineage and does not<br>claim to solve the full feedback cascade.|
|SHACL and PROV-O<br>[30, 31]|Graph-constraint validation and<br>standardized representation of<br>provenance.|Provide relevant concepts or potential<br>implementation substrates, but do not by<br>themselves specify the DIO/ODI<br>diagnostic-to-constraint mapping proposed<br>here.|
|DIO/ODI reference<br>work [4–9]|Reconstruction-oriented concepts<br>and distinctions covering<br>referential, semantic, temporal, and<br>contextual failure modes.|Supplies the diagnostic vocabulary used in<br>the proposed domain-governed mapping;<br>does not automatically generate the<br>executable constraints or establish their<br>incremental value.|



Constraint-based ER is also prior art, not an omitted precursor. Must-link/cannot-link constraints and declarative relational constraints, including Dedupalog, already express conditions on deduplication outcomes [37]. At the diagnostic level, the present RRF distinctions overlap with familiar over-merging and under-merging error classes: Merge Failure corresponds to false co-reference or over-merging, while Split Failure corresponds to missed co-reference or under-merging. The DIO/ODI terms retain their broader reconstruction framing; this paper uses them to organize selected domain constraints, not to rename or replace conventional ER error analysis. 

The closest authorization-related neighbors establish that version-bound commit checks and evidence-aware execution gates are not, by themselves, novel. Zhu and Wang [28] authorize self-generated subgoals against a principal-approved task contract, while Santos-Grueiro [32] examines whether authority for a durable effect remains fresh, causally prior, and valid at commit time. Zhu et al. [29] additionally cover ontology-grounded entity alignment and scenario-driven graph simulation, with low-confidence cases held from simulation for clarification or ontology-gap resolution. The distinction proposed here is narrower: the required identity or continuity proposition is derived for a particular ER mutation and assessed under domain-configured constraints informed by selected DIO/ODI diagnostics. 

Hard-KLAIM [33], AGATE [34], EBL-Core [35], CONTINUITY [36], and ARGUS [22] further establish relevant approaches to typed effects, runtime authorization, provenance-aware execution, current-condition checks, or cross-component authorization continuity. The present manuscript does not claim comparable formal guarantees or an implemented runtime defense. Nor does it claim comprehensive causal-lineage reconstruction; the handling of dependencies that are absent from recorded provenance remains outside the stated guarantee. 

SHACL [30] specifies graph-shape validation, and W3C PROV-O [31] provides a vocabulary for representing and exchanging provenance. These can support implementation of parts of an authorization architecture, but neither supplies the policy decision about which identity-changing proposition must be established for a particular mutation. Similarly, the DIO/ODI contribution here is not automatic SKOS entailment or an established advantage over a generic policy built from the same domain facts. It is the proposed diagnostic-to-constraint mapping: selected reconstruction-failure distinctions organize which claim a mutation requires, which relations are insufficient to establish it, and when temporal or contextual conditions call for deferral. Its incremental value remains an open empirical question. 

6


<!-- page 7 -->

# 3. Diagnostic Failure-Path Analysis of Agentic ER 

The Agentic ER operational cycle alternates through four stages: _Plan_ (select actions from the current state), _Act_ (execute a tool or operation), _Observe_ (receive evidence or a mutation result), and _Update Beliefs_ (revise the internal state) [17]. The following mapping applies the DIO/ODI Reconstruction Failure Mode taxonomy diagnostically to that cycle [7, 8]. It is a proposed analytical application of the taxonomy, not a claim that the taxonomy was part of the original Agentic ER proposal. The DIO/ODI diagnostic vocabulary covers four dimensions: 

- **Referential Reconstruction Failures (RRF):** Entity Substitution (ES), Merge Failure (MF), Split Failure (SF), and Entity Omission. 

- **Semantic Coherence Failures (SCF):** Semantic Fragmentation (SFR). 

- **Temporal Reconstruction Failures (TRF):** Temporal Discontinuity (TD) and Temporal Misalignment (TM). 

- **Contextual Adequacy Failures (CAF):** Contextual Displacement (CD). 

The diagnostic dimensions inform analysis across the Agentic ER lifecycle, but the proposed commit-boundary guardrail operates only at the persistence boundary: it governs mutation authorization and commitment, not all hypothesis formation, query conditioning, or intermediate belief updates. 

## 3.1 Referential Reconstruction Failures (RRF) 

Referential failures concern incorrect identity assignment or cardinality violations between an intended referent 𝐴 and its reconstructed identitŷ 𝐴 [6, 7]. 

- **Merge Failure** ({𝐴, 𝐵} →̂ 𝑋, 𝐴≠𝐵): distinct referents are consolidated into one representation [7, 12]. 

- **Split Failure** (𝐴→{̂𝐴1,̂ 𝐴2, …}): one referent is represented as disconnected identity clusters because temporal or relational continuity was not reconstructed. 

- **Entity Substitution** (𝐴→̂ 𝐵, 𝐴≠𝐵): a less prominent target is displaced by a structurally or lexically prominent namesake. Entity-overshadowing research provides a relevant example of this ambiguity class [18]; entity-linking work provides adjacent context [2]. 

- **Entity Omission:** the system fails to generate a reconstruction despite sufficient representational grounds within the defined observation domain. 

In a sequential agent, an early referential failure may influence later query formulation, evidence selection, and mutation proposals. The resulting process might compound the error, correct it, or leave it unchanged. The authorization design proposed here does not determine which trajectory occurs; it governs whether a persistent identity-changing mutation is permitted at the final protected boundary. 

## 3.2 Semantic Coherence Failures (SCF) 

**Semantic Fragmentation** occurs when the system retains referential unity but fails to reconcile incompatible relational claims or representations into a coherent profile [6, 7]. Referential correctness alone does not guarantee that the resulting set of claims is coherent or usable. A mutation that consolidates records must not be treated as resolving contradictions merely because the records have been clustered together. 

7


<!-- page 8 -->

# 3.3 Temporal Reconstruction Failures (TRF) 

**Temporal Discontinuity** and **Temporal Misalignment** arise when representations are not adequately anchored in time [4, 24]. Temporal misalignment assigns an obsolete state to a referent whose identity remains correct; temporal discontinuity treats historical states of a continuous referent as separate entities. This distinction matters for acquisitions, legal renaming, changing officers, product transitions, and other cases where attributes and relations legitimately evolve. 

# 3.4 Contextual Adequacy Failures (CAF) 

**Contextual Displacement** occurs when a reconstruction may be factually valid but does not satisfy the requirements of the current observation domain Ω [6, 7]. A matching result adequate for product-catalog deduplication may not be adequate for legal-entity compliance. Domain and purpose therefore matter when translating a diagnostic concept into an authorization rule. 

# 3.5 Failure Stage, Control Boundary, and Limitation 

The failure mapping is diagnostic; the following table makes its operational scope explicit. 

Table 2: Failure pathways across the Agentic ER lifecycle and the scope of the proposed commit-boundary control. 

|**Lifecycle stage**|**Potential failure**<br>**pathway**|**What the**<br>**commit-boundary**<br>**guardrail does**|**What it does not claim**<br>**to do**|
|---|---|---|---|
|Plan|A mistaken identity<br>hypothesis conditions an<br>action or query (potential<br>RRF, TRF, or CAF<br>pathway).|Binds any proposed<br>mutation to an explicit<br>authorization record and<br>policy scope.|Does not prevent a<br>wrong hypothesis from<br>shaping the Planner.|
|Act|A query retrieves<br>material selected or<br>phrased under the<br>current hypothesis<br>(potential CAF pathway).|Checks the declared<br>action scope; retrieval<br>results enter a controlled<br>admission path.|Does not guarantee<br>independent retrieval or<br>infer causal<br>independence.|
|Observe|Retrieved content<br>appears consistent with<br>the hypothesis or<br>conflicts with other<br>claims (potential<br>SCF/TRF pathway).|Stages observations;<br>records detected material<br>conflicts for<br>deferral/adjudication.|Does not reliably detect<br>all apparent verification<br>or infer causal<br>dependence among<br>sources.|
|Update Beliefs|An observation affects<br>the Planner’s internal<br>state and may reinforce a<br>substitution or stale<br>interpretation (potential<br>RRF/TRF pathway).|Separates Planner<br>eligibility from<br>authorization eligibility.|Does not block all effects<br>of `UNVERIFIED`material<br>on internal reasoning.|
|Persistent graph<br>mutation|A hypothesis is<br>converted into a durable<br>merge or<br>identity-changing edge.|Requires a`PASS`under<br>the declared constraints<br>on claim-specific𝑃auth,<br>valid scope, and current<br>state/policy versions.|Does not prove that the<br>domain policy or<br>evidence validator is<br>infallible.|



This table is a diagnostic mapping of possible failure pathways to the proposed control boundary. It 

8


<!-- page 9 -->

does not claim that the lifecycle stages uniquely determine a failure category or that the proposed guardrail detects every listed pathway. The contribution concerns **authorization containment at the persistence boundary** , conditional on the assumptions specified below, not a full information-flow guarantee. 

# 4. A Stylized Model of Apparent Verification 

An abstract sequential agent may be represented by a state 𝑠𝑡 ∈𝒮 , an action 𝑎𝑡 ∈𝒜 , the observation 𝑜𝑡+1 ∈𝒪 returned after that action, and an update function 

𝑠𝑡+1 = Φ(𝑠𝑡 , 𝑎𝑡 , 𝑜𝑡+1). 

The indexing convention is action-first: executing 𝑎𝑡 from 𝑠𝑡 returns 𝑜𝑡+1, which is incorporated into 𝑠𝑡+1. 

## 4.1 A Possible Hypothesis-Conditioned Feedback Path 

Under hypothesis-conditioned retrieval and insufficiently independent validation, the following sequence is possible: 

1. **Latent distortion:** the state 𝑠𝑡 contains an erroneous identity hypothesis introduced by a noisy classifier, prior inference, or earlier evidence [7, 17]. 

2. **Biased action parameterization:** the next action is selected using the corrupted state, so a query or tool call encodes part of the earlier hypothesis [4, 11]. 

3. **Contextual ingestion:** retrieval returns material relevant to the query as formulated, but relevance does not independently establish the target referent’s identity [4, 23]. 

4. **Apparent convergence:** the apparent discrepancy between an observation and the existing hypothesis may decrease even when the hypothesis is wrong, because the observation process was conditioned on that hypothesis. 

A stylized residual is 



<!-- Start of picture text -->
‖Project(𝑜𝑡+1) − Expectation(𝑠𝑡 )‖ →0.<br><!-- End of picture text -->

Here, `Project` denotes an illustrative mapping of an observation into the representation used by the matcher, and `Expectation` denotes the representation predicted from the current state. The expression presupposes that both outputs are comparable in a common representational space; neither mapping nor the discrepancy measure is specified as a calibrated estimator. The arrow denotes a possible reduction in apparent discrepancy over a feedback sequence, not a convergence result established by this paper. The expression illustrates how a hypothesis-conditioned observation may appear to agree with the current state without independently establishing referential correctness. **Boundary of the proposed solution.** The proposed MVDIO Supervisor does not close the Plan–Act–Observe–Update feedback loop. It does not claim that a query is independent of the current hypothesis, that multiple returned sources provide independent corroboration, or that intermediate belief updates are free of contaminated evidence. It addresses the downstream authorization question: whether the evidence and constraints recorded for a proposed persistent mutation are sufficient to permit that mutation. This narrower boundary is deliberate and makes the proposed property inspectable without claiming a solution to the full cascade mechanism. 

9


<!-- page 10 -->

# 5. DIO/ODI-Informed Mutation Authorization 

The authorization design uses a reconstruction-oriented semantic model to inform constraints over identity-changing operations. A full agent planner may be modeled as a constrained sequential decision process, such as a Constrained Markov Decision Process [1], but this paper does not specify or claim to solve the Planner’s global optimization problem. Its formal focus is the authorization condition at a persistent mutation boundary. 

## 5.1 Semantic Target: Reconstruction Admissibility and Observation Context 

Let 𝜔= (𝑂, 𝐶, 𝑡) ∈Ω denote the observation domain relevant to a mutation: an observer or consuming system 𝑂, an operational context or purpose 𝐶, and the relevant temporal epoch or interval 𝑡. Let ℛ denote the space of analytically considered reconstructions. For a referent 𝐸, define the ideal admissible reconstruction set as 

Adm(𝐸, 𝜔) ⊆ℛ. 

Here, Adm(𝐸, 𝜔) denotes the reconstructions that preserve the intended referential assignment and satisfy the applicable semantic and temporal conditions for 𝐸 under 𝜔. It is an ideal semantic reference, not a set that the proposed supervisor can enumerate or verify directly from incomplete evidence. 

Let 𝒮 denote the relevant agent-state space, and let the partial projection from a state to a reconstruction be 

Γ ∶𝒮⇀ℛ. 

The partiality matters: some states do not yield a well-defined reconstruction in the observation domain. For states where a reconstruction is defined, the corresponding idealized inadmissibility set is 

𝒮ideal_fail(𝐸, 𝜔) ∶= {𝑠∈ dom(Γ) ∣Γ(𝑠) ∉ Adm(𝐸, 𝜔)}. 

This set is an analytical reference for a defined but inadmissible reconstruction; it is not an executable detector or a claim that the supervisor observes the agent’s full internal state. The expression does not classify an undefined reconstruction and must not be read as proof that an identity claim is false. Entity Omission—where no reconstruction is produced despite sufficient grounds within the observation domain—and upstream acquisition/coverage failures require separate analysis; the latter should not automatically be labeled reconstruction failures. 

The diagnostic distinctions in Section 3 organize different ways in which reconstruction can fail or become unsuitable. Defined-output cases of Entity Substitution, Merge Failure, and Split Failure can be characterized as candidate cases of idealized inadmissibility when assessed for the relevant referent and observation domain. The set does not itself classify the cause of inadmissibility or provide a one-to-one mapping to RRF, SCF, TRF, and CAF. In particular, Semantic Fragmentation is relational across multiple reconstructions, while Temporal Discontinuity may require a sequence of time-indexed states; neither is fully encoded by this single-state set definition. The taxonomy in Section 3 remains a diagnostic organization, not a partition theorem over 𝒮ideal_fail. Contextual Displacement is analytically distinct: a reconstruction may preserve referential identity while remaining inadequate for the current purpose, so contextual conditions must be represented by domain policy rather than inferred from referential inadmissibility alone. Contextual fitness remains distinct from admissibility. A reconstruction may preserve referential identity and temporal continuity yet still be inadequate for a particular task or consuming system. We do not assign a numeric contextual-adequacy score here, because no calibrated scoring function is specified. Instead, context-sensitive requirements must be expressed as explicit, versioned domain-policy conditions. The architecture does not assume an oracle for semantic truth: missing or inapplicable support blocks authorization but does not prove that two referents are different. 

10


<!-- page 11 -->

# 5.2 Constraint Binding and Its DIO/ODI Contribution 

The DIO/ODI Reference Model provides concepts, relationships, and diagnostic mappings. It does not automatically generate executable constraints. We propose a partial, domain-governed binding function 



<!-- Start of picture text -->
𝜇Ω ∶𝒞DIO/ODI ⇀𝒱𝐸,<br><!-- End of picture text -->

where 𝒞DIO/ODI denotes the selected failure-mode distinctions in the restricted domain, and 𝒱𝐸 denotes the space of admissible domain-level constraint specifications for referent or entity class 𝐸. Each element of 𝒱𝐸 is a specification that may contain one or more coordinated predicates; it is not assumed to be an atomic condition. The concrete collection configured for 𝐸 in a given observation domain is denoted by 𝑉𝐸 ⊆𝒱𝐸. The partial function 𝜇Ω maps a selected diagnostic distinction to one specification in 𝒱𝐸; the selected mappings inform the construction of 𝑉𝐸 but do not automatically determine every predicate or policy condition required in an implementation. The mapping is a policy-design step, not automatic SKOS entailment. In this notation, 𝐸 denotes the referent or entity class, 𝑉𝐸 the configured collection of constraint specifications, and 𝑣𝐸 the version counter for the evidence state—not a version of 𝐸 or 𝑉𝐸. 

For this paper, _reconstruction_ means forming a context- and time-bound representation of a referent’s identity from distributed representations and claims; it does not presuppose that one complete ground-truth profile is available. Digital Identity Optimization (DIO) is the broader framework for preserving and reconstructing coherent digital identity across such representations, while the Ontology of Digital Identity (ODI) organizes the concepts and relations used to describe that problem. In the present proposal, the domain of 𝜇Ω is restricted to the reconstruction-failure distinctions defined in Section 3 (RRF, SCF, TRF, and CAF) and the selected categories shown in the mapping below; it does not cover the whole DIO/ODI vocabulary. 

General RDF graph validation can provide an implementation substrate for some domain-level constraints. SHACL specifies how RDF data graphs may be checked against declared shapes and conditions [30]. A suitable SHACL/SPARQL validator could therefore evaluate selected graph conditions, but SHACL does not itself supply the DIO/ODI diagnostic mapping, decide which identity proposition is required for a particular mutation, or establish the adequacy of the evidence-promotion process. The proposed 𝜇Ω is a design-time binding step, not a graph-validation engine or an automatic constraint-generation mechanism. At minimum, a binding used for authorization should be: 

- **Domain-scoped:** applicable to a declared entity class, observation context, and mutation class. 

- **Semantically typed:** explicit about which relation or evidence type it accepts; relatedness must not silently become identity equivalence. 

- **Temporally scoped where relevant:** continuity and state claims must be evaluated for the interval to which the mutation applies. 

- **Inspectable and versioned:** the selected concept-to-constraint mapping and the policy version used at authorization can be recorded and audited. 

- **Fail-closed for irreversible mutations:** insufficient authorization-eligible evidence yields `UNKNOWN_EVIDENCE` , not implicit permission. 

An illustrative binding is shown below. It is a domain-policy example, not a validated general-purpose mapping or a property automatically produced by the reference vocabulary. The diagnostic categories in the left column come from the DIO/ODI framing; the specific predicates and rules are supplied by the domain policy. 

11


<!-- page 12 -->

Table 3: Illustrative DIO/ODI diagnostic-to-constraint mapping for identity-changing mutations. 

|**DIO/ODI diagnostic**<br>**distinction**|**Example domain-level**<br>**constraint**|**Authorization consequence for an**<br>**identity-changing mutation**|
|---|---|---|
|Entity Substitution /<br>Merge Failure (RRF)|Lexical similarity or a shared<br>commercial neighborhood does not<br>by itself establish that two records<br>denote the same referent.|Do not merge without claim-specific<br>evidence establishing co-reference.|
|Temporal Discontinuity<br>/ Misalignment (TRF)|A rename or continuity claim must<br>apply to the relevant referent and<br>validity interval.|Defer if temporal applicability or legal<br>continuity is unresolved.|
|Semantic<br>Fragmentation (SCF)|Materially incompatible claims<br>affecting identity are retained as a<br>conflict until reconciled; clustering<br>alone does not reconcile them.|Require reconciliation or defer the affected<br>mutation. This mapping covers the<br>identity-affecting subset; other attribute-level<br>incompatibilities remain governed by domain<br>policy.|
|Contextual<br>Displacement (CAF)|The same`brand_of`relation may<br>be adequate in a brand catalogue<br>but insufficient for the legal-entity<br>identity proposition required in a<br>compliance context.|Preserve the typed relation; require evidence<br>and constraints appropriate to the current<br>observation purpose.|
|Split Failure / valid<br>continuity (RRF/TRF)|Documented, temporally applicable<br>evidence may establish that distinct<br>records refer to one continuing<br>entity.|Permit resolution when the claim-specific<br>evidence and all applicable constraints pass.|



The proposed DIO/ODI-informed contribution is a **diagnostic-to-constraint mapping** : selected reconstruction-failure distinctions are used to specify which claim a mutation requires, which relations are insufficient for that claim, and when temporal or contextual conditions require deferral. This is a design proposal rather than an established advantage over generic authorization. Its incremental value depends on whether this mapping improves the safety/coverage trade-off relative to policies built from the same domain facts without the diagnostic structure. 

# 5.3 Evidence States and Promotion Contract 

Let 𝑃active be the evidence admitted for use by the Planner and 𝑃quar the evidence retained in quarantine outside that admitted set. 𝑃active may include records marked `UNVERIFIED` . Let 𝑞𝑚 denote the identity or continuity proposition—or set of propositions—that must hold for mutation 𝑚 to be authorized. Let 𝑃auth(𝑞𝑚, 𝜔) ⊆𝑃active be the evidence eligible to bear on the claim-specific assessment of those propositions in observation domain 𝜔, including its relevant temporal epoch or interval. This includes evidence that may support a proposition, establish a policy-relevant contradiction, or reveal an unresolved material conflict; the role taken by each item must be recorded in its claim-specific validation basis. Authorization eligibility is not itself a verdict and is not a global label asserting that a document is universally true. `UNVERIFIED` is an admission-level status: it means that the item has not yet been established as eligible for the proposition under assessment, not that it is universally unverified or false. Eligibility must be assessed relative to the particular proposition, observation domain, temporal applicability, and policy version. The same source may support one proposition while contradicting or being insufficient for another; use for a different proposition requires a separate policy assessment. 

A retrieved observation first enters `QUARANTINE_EVIDENCE` . Following basic admission checks, it may be added to 𝑃active with status `UNVERIFIED` , but that step does not promote it into 𝑃auth(𝑞𝑚, 𝜔). 

12


<!-- page 13 -->

Promotion requires a separate, auditable policy that assesses the identity or continuity claim needed for the proposed mutation. 



<!-- Start of picture text -->
Claim-<br>QUARANTINE specific role 𝑃auth Commit-time<br>observationRetrieved Admission EVIDENCE UNVERIFIED 𝑃active andassessmenteligibility claim-specific(𝑞𝑚, 𝜔) graphevaluationconstraints,<br>eligible<br>conflict check (𝑞𝑚, policy, evidence scope, versions<br>provenance)<br>conflict /<br>indeterminate<br>role<br>Planner may use assessed<br>CONFLICT or this material for PASS + valid<br>INDETERMINATE : reasoning; it is not Support may satisfy scope/versions<br>retain in quaran- positive autho- positive requirements; → commit<br>tine; adjudicate rization support eligible contradiction BREACH → re-<br>and re-check may establish BREACH ; ject/escalate<br>unresolved indications UNKNOWN_EVIDENCE<br>block PASS and yield → defer<br>UNKNOWN_EVIDENCE unless<br>BREACH takes precedence<br><!-- End of picture text -->

Figure 2: Evidence admission and claim-specific eligibility assessment. The path from quarantine to 𝑃active applies only when admission returns `NO_CONFLICT_DETECTED` ; the path into 𝑃auth applies only when a claim-specific assessment establishes eligibility in the recorded role. 𝑃auth may contain evidence in support, contradiction, or unresolved-indication roles, each recorded for the proposition being assessed. Only support can satisfy a required positive condition; eligible contradiction evidence can establish a relevant conflict, while an unresolved indication blocks `PASS` and yields `UNKNOWN_EVIDENCE` unless an established `BREACH` takes precedence under the status aggregation rule. Admission to 𝑃active grants only `UNVERIFIED` status; it does not authorize a mutation. Commit remains conditional on graph constraints, authorized scope, and current versions. 

The minimum promotion contract is: 

1. It evaluates the **specific proposition** required for the candidate mutation, rather than document relevance, query match, or plausibility alone. 

2. It records the source/provenance basis, the proposition assessed, the item’s role (support, contradiction, or unresolved indication), temporal applicability where relevant, the validation basis, and the policy/validator version. 

3. It does not treat Planner confidence, an LLM-generated `verified` label, or repetition across `UNVERIFIED` observations as sufficient authorization evidence. 

4. It does not promote a claim solely because the Planner’s hypothesis induced the query that retrieved supporting material. Corroboration used for promotion must have a claim-specific basis under the declared policy; simple agreement or document count is not enough by itself. Observations whose recorded provenance indicates a shared upstream query, hypothesis, source, or derivation path must not be counted as independent corroboration merely because they appear as separate items. 

5. It must not infer positive support merely from the absence of a detected conflict. 

6. The recorded provenance and validation basis for a promoted claim must not cite a shadow candidate or a claim whose own recorded basis cites shadow content. A promotion process must preserve enough recorded basis to apply this restriction transitively along that recorded chain. 

7. Evidence becomes authorization-eligible only for the proposition, evidentiary role, and applicability established under the declared policy. Evidence that does not qualify as positive support cannot satisfy a required positive condition. 

13


<!-- page 14 -->

These requirements constrain the promotion decision on the basis of recorded provenance; they do **not** claim that the system can reconstruct every causal dependency among retrieval actions and evidence origins. The shadow exclusion applies to the recorded validation/provenance chain used for promotion. Unrecorded or undisclosed derivations cannot be reliably screened by this contract and remain outside the guarantee; the broader dependency problem remains future research. The validator implementation and its trust base are outside this paper’s scope. This is a material assumption, not a solved subproblem. Eligibility metadata may be written or changed only by the designated promotion process or by a versioned policy/adjudication operation that triggers a new authorization decision; the Planner and raw tool outputs cannot directly assign or alter authorization eligibility. The architecture is conditional on the promotion process correctly applying the stated policy. It cannot protect against a validator that systematically misclassifies unsupported claims as authorized, a false authoritative source, or a policy that encodes the wrong identity conditions. In domains where the validity of a mention-to-identifier link is itself uncertain, the linkage must be treated as a claim requiring evidence; the existence of an identifier alone does not prove that the mention refers to its holder. 

For evidence admission, a mutation-independent check uses the observation itself and the current evidence stores: `CheckAdmissionConflict(o, P_active, P_quar)` returns `CONFLICT` , `NO_CONFLICT_DETECTED` , or `INDETERMINATE` . `CONFLICT` denotes a supported material conflict; `INDETERMINATE` denotes a plausible material conflict that cannot be resolved on the available basis. `NO_CONFLICT_DETECTED` means only that this admission check did not establish a conflict. It is not positive evidence of identity, and the check cannot certify that all conflicts have been detected. The admission check does not take `q_m` as an input because no mutation-specific proposition need be fixed at read time. A conflict or indeterminate result keeps the observation quarantined for adjudication; otherwise it may be admitted to `P_active` as `UNVERIFIED` , without authorization promotion. An admission-level `CONFLICT` is a reason to quarantine the observation, not by itself a mutation-level `BREACH` verdict. 

A quarantined item remains outside Planner-visible shared evidence until a policy-designated adjudication or versioned rule determines its disposition. Such a decision must be recorded, advance the evidence-state version, and trigger a fresh admission check before an item is released to `P_active` ; release confers only `UNVERIFIED` status, not claim-specific authorization eligibility. If no authorized reviewer or applicable rule is available, the item remains quarantined and may cause a mutation to be deferred. Escalation does not itself release evidence or authorize a commit. At mutation evaluation, the supervisor performs a separate claim-specific check: `CheckClaimConflict(q_m, P_auth, P_active, P_quar)` . It returns `CLEAR` only when no unresolved material conflict bearing on the propositions in `q_m` is detected. It returns `CONFLICT` only when claim-specific authorization-eligible evidence, assessed under the applicable policy, establishes a relevant contradiction or prohibitive condition. It returns `INDETERMINATE` when a possible material conflict is indicated only by `UNVERIFIED` evidence in `P_active` or by evidence in `P_quar` , or when conflicting authorization-eligible items cannot be reconciled under the policy’s authority and temporal rules. A detected `CONFLICT` or `INDETERMINATE` must prevent `PASS` . An `UNVERIFIED` item may therefore cause deferral by revealing an unresolved conflict, but it cannot itself establish a mutation-level `BREACH` or count as positive support for identity. For action and graph evaluation, the statuses are: 

- `PASS` : every required positive condition is supported by claim-specific authorization-eligible evidence, no applicable prohibition is established, and `CheckClaimConflict` returns `CLEAR` . 

- `BREACH` : authorization-eligible evidence establishes a relevant contradiction or violation of an explicit prohibitive constraint. 

- `UNKNOWN_EVIDENCE` : required positive support is insufficient, or a material conflict remains unresolved or indeterminate. 

14


<!-- page 15 -->

The status aggregation rule is **`BREACH` takes precedence over** **`UNKNOWN_EVIDENCE` , which takes precedence over** **`PASS`** : an established violation rejects the candidate even if other conditions are unknown; otherwise any missing required support or unresolved material conflict blocks a pass. Positive/sufficiency constraints state what must be supported to authorize a mutation. Prohibitive constraints state what must not be asserted or committed. A relation such as `brand_of` is not, by itself, proof that two referents are different; it is insufficient to establish legal-entity identity unless a separate policy rule and evidence support that conclusion. `UNKNOWN_EVIDENCE` blocks an irreversible mutation because authorization has not been established, not because the system has proven the identity claim false. 

# 5.4 Authorization Invariant and Assumptions 

Let 𝑚 be a proposed mutation, 𝑞𝑚 the proposition or set of propositions required to authorize it, 𝐺cand its candidate graph, 𝛼𝑚 the authorization record, and 𝜎𝑐 the consistent commit-time snapshot of the relevant graph, evidence stores, policy, shadow store if used, and their versions. The required proposition set is derived by the supervisor from the candidate operation, its target/effect scope, and the applicable versioned policy instance, which is configured for the relevant observation domain: 



<!-- Start of picture text -->
𝑞𝑚 ∶= DeriveRequiredClaims(𝑚, 𝑉𝐸, 𝑣pol).<br><!-- End of picture text -->

The resulting 𝑞𝑚 is bound in 𝛼𝑚; the Planner cannot weaken or replace that derived set. The domain-specific policy instance represents the applicable observation context and temporal conditions. Accordingly, 𝜔 in 𝑃auth(𝑞𝑚, 𝜔) is fixed by the policy instance bound through 𝑣pol(𝛼𝑚); it is not an unbound runtime input. The claim-specific evidence assessment evaluates applicability to 𝑞𝑚 within that bound context. This is the operational bridge from domain-configured constraints to the specific propositions that must be supported for a mutation. The ideal set Adm(𝐸, 𝜔) defined in Section 5.1 is not evaluated directly at commit time. Rather, the design-time mapping 𝜇Ω selects explicit constraints from the DIO/ODI diagnostic vocabulary, the versioned policy instantiates the required propositions and constraints, and the commit contract checks their satisfaction against claim-specific authorization-eligible evidence. Consequently, a `PASS` result establishes compliance with the configured contract; it does not prove membership in the ideal admissible set or the semantic truth of the underlying evidence. An operation is treated as a protected identity-changing mutation whenever its realized or potential shared effects can alter the graph’s identity interpretation. This applies to merges, splits, and corrective un-merges or other reversals when they alter shared identity interpretation; the versioned domain policy defines the required propositions separately for each mutation type. Reversing a prior merge does not, by itself, establish that the affected referents are distinct. If the effect class is ambiguous, it is treated as protected rather than classified as harmless or reversible by the Planner. 

The authorization record binds the domain-policy version 𝑣pol(𝛼𝑚). The functions ScopeValid and VersionsValid are defined in Section 6. **Under Assumptions 1–7 below, the proposed commit invariant is:** 



<!-- Start of picture text -->
(𝑣pol(𝛼𝑚))<br>Commit(𝑚) ⇒ EvaluateGraphConstraints(𝑉𝐸 , 𝑞𝑚, 𝑃auth (𝜎𝑐) (𝑞𝑚, 𝜔), 𝑃 active (𝜎𝑐) , 𝑃 quar (𝜎𝑐) , 𝐺 cand (𝜎𝑐) ) =  PASS<br>∧ ScopeValid(𝑚, 𝛼𝑚) ∧ VersionsValid(𝛼𝑚, 𝜎𝑐).<br><!-- End of picture text -->

`EvaluateGraphConstraints` evaluates both the candidate graph against applicable constraints and the evidence-to-claim support needed to authorize the proposed mutation; it is not merely a graph-shape validator. Each required proposition in 𝑞𝑚 must be covered separately by at least one item in 𝑃auth(𝑞𝑚, 𝜔) whose recorded claim-support and validation basis is applicable to that proposition, including temporal applicability where required. The authorization record 𝛼𝑚 must bind 𝑞𝑚 and, for each required proposition, identify the promotion/validation record or stable record identifier relied on for its claimed support. Mere membership in 𝑃auth without proposition-specific 

15


<!-- page 16 -->

support is insufficient. `EvaluateGraphConstraints` returns `PASS` only if all required positive conditions are supported by claim-specific authorization-eligible evidence, no applicable prohibition is established, and `CheckClaimConflict` returns `CLEAR` for the evidence stores in the same snapshot 𝜎𝑐. It returns `BREACH` for an established policy violation and `UNKNOWN_EVIDENCE` for insufficient positive support or a conflict reported as unresolved or indeterminate. The check is not assumed to detect contradictions absent from, or unrecognized in, its inputs. A conforming implementation must reject or defer unless the result is `PASS` , the realized operation falls within its authorized scope, and all relevant versions remain current through the commit point. `VersionsValid` must verify both that the authorization record was based on the relevant snapshot and that the graph, evidence-state, policy, and (if used) shadow versions still match that snapshot atomically at commit; validation against a stale snapshot alone is insufficient. This is an **interface invariant** : it specifies the protected commit path, not a theorem that the evidence or policy is true. 

The conditional property relies on seven stated conditions with different logical roles. Assumptions 4–6 below are the enforcement and binding premises of the commit implication. Assumptions 1, 2, and 7 are adequacy conditions for interpreting a `PASS` as support for an identity claim; they do not independently establish semantic correctness. The fail-closed behavior in Assumption 3 restates the `PASS` / `UNKNOWN_EVIDENCE` outcome contract: insufficient support or unresolved material conflict cannot authorize an irreversible mutation. 

1. **Domain-policy adequacy:** 𝑉𝐸 expresses relevant identity-preserving constraints for the entity class, context, time, and mutation type. 

2. **Claim-specific promotion:** evidence enters 𝑃auth(𝑞𝑚, 𝜔) only under the promotion contract in Section 5.3, including its limits on Planner/query-conditioned promotion and corroboration by `UNVERIFIED` material. 

3. **Fail-closed authorization:** insufficient evidence or an unresolved material conflict does not authorize an irreversible identity change. 

4. **Enforced and conservative mutation classification:** every relevant production write passes through the supervisor, and any operation that may alter shared identity interpretation is treated as protected. Unmanaged write paths are outside the guarantee. 

5. **Derived authorization propositions:** 𝑞𝑚 is derived by the supervisor from the mutation, its target/effect scope, and the versioned domain policy; the Planner cannot supply a substitute claim set or weaken the derived authorization obligation. 

6. **Scope and version integrity:** the operation, target, domain-policy version, graph state, complete evidence state (including quarantine), authorization eligibility, and shadow state if used remain valid through the commit point. 

7. **Recorded-basis and eligibility integrity:** the promotion process controls eligibility metadata and applies the recorded-provenance restrictions in Section 5.3; the guarantee does not extend to derivations absent from that recorded basis. 

The property is conditional on the promotion process applying the stated contract. It cannot protect against an invalid authoritative source, a validator that misclassifies unsupported claims, or a policy that encodes the wrong identity conditions. It does not guarantee that upstream reasoning is uncontaminated or that every material conflict is detected. 

# 5.5 Boundary and Future Direction: Dependency-Aware Evidence Flow 

A broader design could also control how evidence and intermediate hypotheses influence subsequent actions. That is a different problem from authorization at the commit boundary. A plausible future research direction is a dependency-aware information-flow layer that investigates three requirements: 

16


<!-- page 17 -->

1. **Derivation lineage:** retain links among observations, the actions or queries that produced them, the hypotheses that conditioned those actions, and claims subsequently derived from them. 

2. **Dependency-aware corroboration:** avoid treating several observations as independent confirmation solely because they appear in separate documents or endpoints when their derivation paths are materially dependent. 

3. **Controlled feedback to the Planner:** preserve or expose dependency status when evidence is reused for planning, and test when dependent evidence should be withheld, quarantined, discounted, or sent through an alternative validation path. 

This is a research agenda, not a mechanism implemented or validated here. It would require a clear dependency model, an explicit information-flow contract, and evaluation using controlled hypothesis-conditioned perturbations or trajectory replay. Its effectiveness should not be implied by the commit-boundary authorization invariant. 

# 6. Abstract Interface Specification 

We propose the **MVDIO Supervisor Layer** as a governance gateway for Agentic ER [17]. The architecture has a pre-execution authorization phase and a post-execution validation phase. Its purpose is to govern evidence admission and persistent mutation authorization; it is not a controller for the agent’s complete reasoning trajectory. 

## 6.1 State, Scope, and Version Contracts 

The supervisor distinguishes four action classes: 

- `READ` : retrieval or exploration within a declared scope. 

- `STAGE_LOCAL` : local preparation with no shared-state effects. 

- `REVERSIBLE_WRITE` : a provisional operation authorized only for an isolated staging target, such as `G_shadow` , where effects are separated from production identity state, Planner-visible shared identity state, downstream consumers, and all `P_auth` inputs, and can be safely discarded. It does not authorize publication to the production graph. 

- `IRREVERSIBLE_WRITE` : the protected operational class for any operation whose realized or potential shared effects can persistently alter identity interpretation, such as merging legal-entity nodes or publishing an identity-changing edge. The label means that authorization is required at the shared persistence boundary; it does not assert that technical rollback is impossible. A candidate may be classified as `REVERSIBLE_WRITE` only when the isolation conditions are positively established under policy; if classification or isolation is uncertain, the operation is treated as `IRREVERSIBLE_WRITE` . 

A `READ` result must not directly overwrite Planner-visible shared memory. The raw result first enters `QUARANTINE_EVIDENCE` ; after admission checks, it may be admitted to 𝑃active as `UNVERIFIED` . The Planner may then use it for reasoning. This design does not claim to prevent the Planner from being influenced by it. Only the separate promotion contract determines whether it is eligible for 𝑃auth(𝑞𝑚, 𝜔). `UNVERIFIED` is an admission-level status, not a universal judgment about an item’s truth: for a proposition under assessment, it means that claim-specific eligibility has not been established. Admission as `UNVERIFIED` is never itself promotion; eligibility is specific to the proposition, observation domain, temporal applicability, and policy version, and remains subject to the policy/version checks. 

17


<!-- page 18 -->

The authorization record binds the permitted operation type, target and effect scope, and applicable domain-policy version 𝑣pol. For protected graph mutations it also binds the supervisor-derived required-claim set 𝑞𝑚, graph version 𝑣𝐺, evidence-state version 𝑣𝐸, and shadow version 𝑣𝑆 when a shadow layer is used. Version bindings are action-specific: a READ authorization does not bind a pre-retrieval 𝑣𝐸 or 𝑣𝐺 whose change would force the retrieval to be replayed; its returned observation is admitted through the current-state protocol in Algorithm 2. A STAGE_LOCAL authorization binds shared-state versions only when the declared local operation explicitly depends on them. A REVERSIBLE_WRITE binds 𝑣𝑆, the policy version 𝑣pol, and the versions of any separately versioned isolation state relevant to staging. Use one evidence-state version, 𝑣𝐸, for the complete relevant evidence state: it advances whenever 𝑃active or 𝑃quar changes, including quarantine intake, removal, or adjudication outcome, and whenever authorization eligibility is promoted, demoted, or revoked. Every such change invalidates protected-write authorization based on the prior 𝑣𝐸. `ScopeValid` checks the realized operation type, target, and allowed effects against the record. `VersionsValid` checks all versions bound and relevant to that operation at the required linearization or commit point. The policy is versioned and checked at authorization and at any later decision that relies on it. We define an abstract `AtomicSnapshot` operation that returns a consistent logical snapshot of the production graph, both evidence stores ( `P_active` and `P_quar` ), the authorization-eligibility state, the applicable policy, the staging-isolation state when a `REVERSIBLE_WRITE` is authorized, the optional shadow store, and the versions of these state components. A conforming implementation may use different underlying mechanisms but must satisfy the declared snapshot semantics. A production commit must atomically validate relevant versions and apply the candidate against the same commit point. Merely checking versions at separate earlier times is insufficient. A stable `operation_id` supports idempotency and reconciliation after uncertain network outcomes; it does not by itself provide atomicity. The transaction layer reports one of four outcomes: `COMMITTED` , `VERSION_CONFLICT` , `COMMIT_FAILED` , or `TIMEOUT_UNKNOWN` . These are transaction outcomes, not supervisor directives or semantic identity verdicts. `COMMITTED` maps to the supervisor directive `COMMITTED` ; a version or snapshot conflict triggers `RETRY_REEVALUATE` against a fresh snapshot, subject to one common retry budget across all retry triggers, and exhaustion yields `TRANSACTION_RETRY_EXHAUSTED` ; a confirmed `COMMIT_FAILED` with no committed effect maps to `SYSTEM_FAILURE_ESCALATE` ; and `TIMEOUT_UNKNOWN` maps to `COMMIT_UNKNOWN_RECONCILE` until the outcome can be reconciled. Any human adjudication that changes the case disposition must result in a new authorization decision against current versions; approval must not silently revive a stale candidate. A confirmed infrastructure failure yields `SYSTEM_FAILURE_ESCALATE` , not a semantic identity verdict. 

# 6.2 Phase 1 — Pre-Execution Authorization 

The abstract pre-execution interface evaluates the proposed action against its declared scope, the domain policy, and the evidence eligible for the relevant authorization proposition. For a persistent identity-changing operation, it returns an authorization record only after the applicable action constraints pass. 

```
Algorithm1:AbstractPre-ExecutionAuthorization
Input:actiona_t,domainpolicyV_Eandversionv_pol,
```

```
P_active,P_quar,currentgraph/evidence/policyversions,anyseparately
versionedstaging-isolationstatewhenrelevant,andv_Sifused
```

```
Output:directiveand,ifauthorized,aboundauthorizationrecord
```

`1. If the operation type is unsupported, return REJECT_UNSUPPORTED_OPERATION.` 

`2. If the action has unmanaged external effects, return OUT_OF_BAND_AUTHORIZATION_REQUIRED; do not execute that effect under this interface.` 

`3. Classify the operation from its schema, potential effects, and applicable policy. An operation that may alter shared identity interpretation is IRREVERSIBLE_WRITE. Classify as REVERSIBLE_WRITE only when isolated staging` 

```
andsafediscardarepositivelyestablishedunderthepolicy;ambiguityisprotected.
```

18


<!-- page 19 -->

`4. For READ or STAGE_LOCAL, authorize only the declared scope; do not treat this as validation of returned content. Return the applicable directive (READ_AUTHORIZED for READ; STAGE_LOCAL_AUTHORIZED for STAGE_LOCAL) together with the corresponding scope-bound authorization record, including the operation type, authorized scope, and versions required for that action class.` 

`5. For REVERSIBLE_WRITE, authorize staging only to G_shadow after verifying isolation from production identity state, Planner-visible shared identity state, downstream consumers, and P_auth inputs. Bind the permitted type, target/effect scope, policy, and relevant state versions in a stage-only authorization record; it cannot authorize production commit. Return that record. If isolation cannot be established,` ↪ `do not stage;` 

```
classifytheintendedsharedeffectasIRREVERSIBLE_WRITEandcontinueatStep6
throughtheprotectedauthorizationpathbeforeexecution.
```

`6. For a protected graph mutation, derive q_m from the mutation, target/effect scope, and versioned policy. Bind this derived set in the authorization record; do not substitute a Planner-supplied claim set.` 

`7. Perform an action-level preflight against the current graph/evidence/policy snapshot: assess claim-specific evidence bearing on q_m, applicable constraints that can be checked before execution, declared scope, and claim-specific conflicts. Do not evaluate a not-yet-realized candidate graph; Algorithm 2 performs the full graph evaluation after constructing the isolated candidate.` 

`8. If evaluation is BREACH, reject the candidate and return REJECT_CANDIDATE_AND_ESCALATE.` 

`9. If evaluation is UNKNOWN_EVIDENCE, do not issue authorization. Return HALT_HITL only when policy requires review and a reviewer is available; otherwise return DEFER_UNRESOLVED. No protected candidate is staged or retained in G_shadow through this branch.` 

`10. On PASS, bind target, operation/effect scope, q_m, policy version, and the relevant graph, evidence-state, and shadow versions in the authorization record. For every required proposition in q_m, also bind the stable identifier of the promotion/validation record whose claim-specific support was relied on.` 

`11. Return the authorization record for post-execution validation.` 

The pseudocode is an abstract contract, not a production implementation recipe. It intentionally omits implementation-specific source-ranking rules, thresholds, proprietary prompts, and validator internals. Human review may be part of the domain policy for difficult cases; the paper does not assume that a reviewer is always available or that human judgment is infallible [14, 17]. A human may supply or assess evidence, promote a claim under the declared policy, or authorize a versioned policy change; a reviewer does not silently override `UNKNOWN_EVIDENCE` or bypass the commit invariant. Any such action requires a new authorization decision against current versions. When review is unavailable, the case remains deferred rather than being silently approved. 

# 6.3 Phase 2 — Post-Execution Validation and Commit 

The post-execution interface validates the realized outcome against the authorization record. `MatchesAuthorizedScope` checks action type, target, and permitted effects; it is not a content-truth test. For candidate graph writes, the supervisor constructs an isolated candidate, re-evaluates the candidate graph under the same applicable policy and claim-specific authorization evidence, and verifies that the policy/evidence/graph versions have not changed in a way that invalidates the authorization. A policy-version change requires re-evaluation just as a graph- or evidence-version change does. 

```
Algorithm2:AbstractPost-ExecutionValidation
Input:realizedoperationop_t(includingreturnedobservationo_{t+1}whenop_tisREAD),
authorizationrecord(includingboundq_mforprotectedgraphmutations),
productiongraphG_prod,P_active,P_quar,
domainpolicyV_E,optionalshadowstoreG_shadow,retry_count,retry_budget,
operation_id
```

```
Output:post-executiondirective
```

```
Theprotectedgraph-writepathappliesonlyaftertheREAD,STAGE_LOCAL,and
```

19


<!-- page 20 -->

```
REVERSIBLE_WRITEbranchesreturn.AREVERSIBLE_WRITEmaystageonlytoan
isolatedG_shadowandneverauthorizespublicationtoG_prod.
```

`1. If op_t does not exactly match the authorized action/effect scope, stop processing the result or candidate and return REJECT_CANDIDATE_AND_ESCALATE.` 

`2. Obtain a consistent snapshot sigma_c of the relevant production graph, P_active, P_quar, authorization-eligibility state, policy, staging-isolation state when a REVERSIBLE_WRITE is evaluated, optional G_shadow, and their versions, including v_E for all active/quarantined evidence changes.` 

```
3.ForREVERSIBLE_WRITEoraprotectedgraphwrite,ifanyversionboundtothe
authorizationrecordisstaleorincompatiblewithsigma_c,incrementretry_count.
Ifretry_countreachesretry_budget,returnTRANSACTION_RETRY_EXHAUSTED;otherwise
returnRETRY_REEVALUATEandrestartAlgorithm1againstafreshsnapshotwithanew
authorizationrecord.Donotreplayastalecandidate.ForREAD,ifitspolicy/scope
authorizationisnolongervalid,rejecttheresultandreturnREJECT_CANDIDATE_AND_ESCALATE.
Otherwisedonotrejectitmerelybecauseunrelatedsharedevidenceorgraphversions
changedduringretrieval;Step4linearizesadmissionagainstthecurrentevidencestate
andmustnotre-executetheREAD.ForSTAGE_LOCAL,ifanexplicitlyboundlocal
dependencyversionisstale,discardthelocalartifact,incrementretry_count,and
returnTRANSACTION_RETRY_EXHAUSTEDwhenthebudgetisusedorRETRY_REEVALUATE
againstafreshsnapshototherwise.Ifnorelevantlocaldependencyisstale,proceed
toStep5;shared-stateversionsarenotrequiredunlesstheoperationdependsonthem.
```

`4. If the action was READ:` 

   - `a. atomically place the returned material in QUARANTINE_EVIDENCE and advance v_E;` 

   - `b. run CheckAdmissionConflict(o_{t+1}, P_active, P_quar) against a consistent snapshot; this check does not depend on a mutation-specific q_m;` 

   - `c. on CONFLICT or INDETERMINATE, retain the item in quarantine and return QUARANTINE_ONLY, provided the evidence-state version remains the one checked; if it changed, increment retry_count and repeat the admission check against a fresh snapshot, or return TRANSACTION_RETRY_EXHAUSTED when the budget is used;` 

   - `d. if no conflict is detected, use compare-and-swap on that checked evidence-state version to atomically remove the item from P_quar, admit it to P_active as UNVERIFIED, and advance v_E; if the compare-and-swap fails, increment retry_count and repeat the check against a fresh snapshot, or return TRANSACTION_RETRY_EXHAUSTED when the budget is used;` 

   - `e. do not promote it into P_auth as part of this admission step; return ADMIT_EVIDENCE_COMMITTED.` 

`5. If the action was STAGE_LOCAL, confirm that no shared-state effects occurred. If confirmed, return STAGE_LOCAL_CONFIRMED; otherwise return REJECT_CANDIDATE_AND_ESCALATE.` 

`6. If op_t is a REVERSIBLE_WRITE, verify that its authorization permits staging to G_shadow and that the realized effects remain isolated from production, Planner-visible shared identity state, downstream consumers, and P_auth inputs. Revalidate the authorized target/effect scope and isolation conditions. Perform the version comparison and shadow write as one atomic operation: apply only to G_shadow if v_S, v_pol, and every other staging-relevant version bound to the authorization record—including the version of any separately represented isolation state—still match sigma_c at the operation's linearization point. On success, advance v_S and return SHADOW_STAGED_PROVISIONAL. If any bound version no longer matches, do not stage; increment retry_count and, if the retry budget is not exhausted, return RETRY_REEVALUATE and restart Algorithm 1 against a fresh snapshot. If the retry budget is exhausted, return TRANSACTION_RETRY_EXHAUSTED. If the authorized scope or isolation conditions cannot be verified, discard the candidate and return REJECT_CANDIDATE_AND_ESCALATE; any shared-identity attempt must restart through Algorithm 1 as an IRREVERSIBLE_WRITE.` 

`7. For a protected graph write, apply op_t only to an isolated candidate graph G_cand.` 

`8. Re-derive the required claim set from op_t and the policy in sigma_c. If it differs from the q_m bound in the authorization record, discard the candidate and return REJECT_CANDIDATE_AND_ESCALATE.` 

`9. Evaluate G_cand against the policy and evidence state in the same sigma_c, using the bound q_m, P_auth(q_m, omega), P_active, P_quar, and the claim-specific conflict check. For each required proposition, verify that the promotion/validation record identifier bound in alpha_m is present in the same snapshot and that its claim-specific support, role, applicability, and policy` 

20


<!-- page 21 -->

```
versionstillholdinP_auth.Re-deriveneithersupportnorprovenancefroma
latersnapshot.MapCheckClaimConflict=CONFLICTtoBREACHand
CheckClaimConflict=INDETERMINATEtoUNKNOWN_EVIDENCE;eitherresultblocksPASS.
```

`10. If the result is BREACH, discard the candidate and return REJECT_CANDIDATE_AND_ESCALATE.` 

`11. If the result is UNKNOWN_EVIDENCE, do not commit or stage the protected candidate in G_shadow; defer the identity-changing decision. Return HALT_HITL only when policy requires adjudication and a reviewer is available; otherwise return DEFER_UNRESOLVED.` 

`12. If the result is PASS, atomically attempt commit only if the authorized scope remains valid and the current graph version v_G, evidence-state version v_E, policy version v_pol, and shadow version v_S (if used and bound in the authorization record) still match sigma_c at the commit point. On successful commit, advance v_G and return COMMITTED. If atomic version validation fails, handle it as VERSION_CONFLICT under Step 13. A confirmed COMMIT_FAILED with no committed effect is handled under Step 13; an uncertain outcome is handled as TIMEOUT_UNKNOWN.` 

`13. On VERSION_CONFLICT, increment retry_count; if the retry budget is exhausted, return TRANSACTION_RETRY_EXHAUSTED, otherwise return RETRY_REEVALUATE and restart Algorithm 1 against a fresh snapshot with a new authorization record. This same retry budget applies to retry triggers in Steps 3 and 6 and to version changes or admission compare-and-swap failures in Step 4; for Step 4, rerun the admission check against a fresh snapshot rather than re-executing the READ action. On TIMEOUT_UNKNOWN,` ↪ `return` 

```
COMMIT_UNKNOWN_RECONCILEandfreezeuntiltheoperation_idoutcomeisreconciled.
OnconfirmedCOMMIT_FAILED,returnSYSTEM_FAILURE_ESCALATE;donottreatitas
asemanticidentityverdict.
```

**Lifecycle semantics.** Pre-execution directives, post-execution outcomes, and case statuses are distinct; the transaction-outcome mapping is defined in Section 6.1. `READ_AUTHORIZED` and `STAGE_LOCAL_AUTHORIZED` are pre-execution scope decisions, not validation of content or completed operations. `STAGE_LOCAL_CONFIRMED` means the local operation completed without shared-state effects. `REJECT_UNSUPPORTED_OPERATION` denotes rejection of an unsupported action type; `OUT_OF_BAND_AUTHORIZATION_REQUIRED` means execution is withheld pending authorization outside this interface. `COMMITTED` means that the protected candidate passed commit-time validation and was committed within the authorized scope, with the graph version advanced; it is not a claim of semantic truth beyond the stated policy and evidence assumptions. `QUARANTINE_ONLY` keeps an observation outside Planner-visible shared evidence pending adjudication; it does not label the item false or malicious. `ADMIT_EVIDENCE_COMMITTED` means an item entered 𝑃active as `UNVERIFIED` , not that it became authorization-eligible. `SHADOW_STAGED_PROVISIONAL` means a candidate was staged only in isolated 𝐺shadow; it is neither a production commit nor permission to publish and any later production mutation requires a new protected authorization decision. `DEFER_UNRESOLVED` terminates the current automated attempt but leaves the case available for later review or explicitly authorized retry. `HALT_HITL` is emitted only when the policy requires human adjudication and a reviewer is available; if no reviewer is available, return `DEFER_UNRESOLVED` . A human decision may update evidence eligibility or the versioned policy but cannot bypass the invariant; it requires a new authorization decision. `RETRY_REEVALUATE` requires a fresh snapshot and a new authorization decision. `TRANSACTION_RETRY_EXHAUSTED` is returned when the common retry budget is exhausted, regardless of which version/snapshot check triggered it; `COMMIT_UNKNOWN_RECONCILE` freezes the case until a timeout outcome is reconciled; and `SYSTEM_FAILURE_ESCALATE` reports a confirmed infrastructure failure. These are not semantic verdicts. `REJECT_CANDIDATE_AND_ESCALATE` discards a not-yet-committed candidate; it does not imply rollback of a previously committed mutation. Its destination is a policy-defined adjudication or operations queue; escalation does not itself change evidence eligibility or authorize a retry. `SHADOW_STAGED_PROVISIONAL` applies only to an explicitly authorized `REVERSIBLE_WRITE` under the Section 6.1 isolation conditions, not to a protected candidate deferred as `UNKNOWN_EVIDENCE` . 

The claimed property is limited to the protected persistence boundary: `UNVERIFIED` evidence is not eligible to satisfy positive authorization conditions unless and until it is separately promoted for the 

21


<!-- page 22 -->

specific claim under the stated contract. Evidence may still influence the Planner, and the interface does not establish that every bad claim or material conflict will be recognized, that provenance assertions are truthful, or that the agent’s internal state remains uncontaminated. 

# 7. Illustrative Case: Corporate Entity Resolution in B2B Data Lakes 

This hypothetical scenario concerns Enterprise Knowledge Graph construction for risk and compliance [4, 12, 19]. It illustrates the distinction between an identity relation and other relations. It is not an observation from a deployed system. 

## 7.1 Scenario and Domain Constraints 

An Agentic ER system is resolving the legal entity **Acme Global** , which has acquired **BetaTech** . A separate startup, **Acme AI, Inc.** , operates in a related technical sector. **Acme Cloud** is a brand of Acme Global ( `Acme Cloud brand_of Acme Global` ). Distributed evidence includes legal records, CRM entries, and noisy media reports that conflate Acme Cloud with Acme AI, Inc. because of lexical overlap. 

For a financial-compliance observation domain, the policy configures explicit identity-preserving constraints 𝑉𝐸 [6, 26, 27]. The following are illustrative policy-local predicates for this case, not claims that these exact relation labels are canonical predicates in the DIO/ODI vocabulary. Relevant relation types include: 

- `same_legal_entity` : an identity-equivalence relation subject to claim-specific authorization; 

- `renamed_to` : continuity of the same legal entity over time, subject to temporal validity; 

- `brand_of` : a brand-to-legal-entity relation that does not authorize identity merge; 

- `absorbed_by` : an acquisition relation that does not by itself establish `same_legal_entity` or legal continuity. It is a non-sufficient relation, not by itself a prohibitive finding that the identity claim is false; absent sufficient continuity evidence the result is `UNKNOWN_EVIDENCE` , while `BREACH` requires separate authorized evidence or an explicit policy condition establishing a contradiction. 

**Legal Lineage Constraint.** Distinct representations may be merged through an `IRREVERSIBLE_WRITE` only when authorization-eligible evidence establishes the required `same_legal_entity` condition or applicable legal continuity through `renamed_to` . A temporally valid Legal Entity Identifier (LEI) can provide relevant legal-entity evidence [26, 27], but the existence of an LEI does not by itself prove that a particular mention belongs to its holder. A brand relation or acquisition edge alone does not establish that two entities are identical. 

## 7.2 Failure Case: Relatedness Is Mistaken for Identity 

An unconstrained agent identifies lexical or semantic similarity between Acme Cloud and Acme AI, Inc. A retrieval step returns a speculative blog post discussing a commercial partnership. A naive matcher treats evidence of a partnership involving the Acme Cloud brand as evidence of referential identity and concludes that Acme AI, Inc. is identical to Acme Cloud. It then propagates the mistaken equivalence to Acme Global. This is an illustrative Merge Failure and Contextual Displacement under the DIO/ODI distinctions [7, 18]. 

For this example, assume that 𝑃auth contains no claim-specific evidence establishing `same_legal_entity` or an applicable `renamed_to` continuity claim between the two candidate referents. The speculative partnership post is available only as `UNVERIFIED` context, and no authorization-eligible evidence independently establishes the required identity proposition. The 

22


<!-- page 23 -->

brand and partnership relations therefore cannot satisfy the positive condition; the graph evaluation returns `UNKNOWN_EVIDENCE` , and the irreversible merge is deferred. If claim-specific authorized evidence instead established that the two legal entities were distinct, the result would be `BREACH` . This is an illustration of the commit-boundary property, not evidence that all variants of apparent verification will be intercepted. 

**Hypothesis-conditioned accumulation.** Suppose the same mistaken hypothesis also prompts searches of a trade directory and a news index. Three returned items appear to reinforce the proposed merge, but their recorded provenance links lead back to the same promotional announcement and none independently establishes `same_legal_entity` or valid legal continuity. The items may be admitted as `UNVERIFIED` observations, but their number and apparent agreement do not make them three independent grounds for promotion. Under promotion-contract items 3–4, they remain ineligible as positive identity support unless the declared policy accepts a separately recorded, claim-specific basis. The case therefore remains `UNKNOWN_EVIDENCE` and is deferred. This example tests the recorded-provenance restriction in the promotion contract; if the relevant derivation links are absent from the record, the architecture does not guarantee that the dependency will be detected. 

## 7.3 Temporal Scope Case: Reused Source-Local Identifier 

Consider a second hypothetical case involving a source-local supplier key, `SUP-041` . A source’s change log shows that the key was assigned to Supplier A during one validity interval, retired, and later reassigned to unrelated Supplier B. A flat rule that treats equality of this source-local identifier as sufficient identity evidence would merge the records despite their non-overlapping assignments. A TRF-informed constraint treats the identifier as temporally scoped: equality outside the same valid assignment interval cannot satisfy the identity proposition. If the reassignment record is authorization-eligible and establishes different assignments, evaluation returns `BREACH` ; if the interval or assignment remains unresolved, it returns `UNKNOWN_EVIDENCE` . Neither outcome authorizes the merge. 

This example distinguishes a temporally typed constraint from a **flat identifier-equality rule** , not from a competent baseline that already encodes the same validity intervals. It illustrates how a DIO/ODI diagnostic can make an identity-preserving condition explicit; it does not demonstrate empirical superiority over well-designed temporal entity resolution. 

## 7.4 Contrast Case: Documented Identity Continuity 

Consider a paired hypothetical case in which two records have different names because the same legal entity was formally renamed. If appropriate legal records establish the continuity claim for the relevant time interval, and claim-specific evidence satisfies the configured constraints, the guardrail may return `PASS` and permit the authorized resolution. If the available record merely establishes a commercial acquisition or brand relationship, that is insufficient. The contrast illustrates that the policy is not a blanket rule rejecting every uncertain match; it is a typed mapping between the relationship asserted, the evidence available, and the mutation requested. 

# 8. Proposed Evaluation Protocol 

This section proposes an evaluation plan for future empirical validation. No experimental results are claimed. The central question is whether DIO/ODI-informed mutation constraints improve the safety/coverage trade-off beyond generic authorization controls and conventional identifier rules, under comparable resources. 

## 8.1 Baselines and Corpus Construction 

The evaluation should compare at least four conditions: 

23


<!-- page 24 -->

- **Baseline A — Unconstrained Agentic ER:** a documented agent using retrieval tools and an ER matcher without the proposed mutation-authorization boundary. 

- **Baseline B — Conventional identifier/default-deny rules:** the same task with standard identifier constraints and abstention when required evidence is missing. 

- **Baseline C — Generic authorization boundary:** the same two-phase mutation gate and claim-specific evidence separation, but with conventional policy rules authored without the DIO/ODI diagnostic mapping. 

- **Challenger — DIO/ODI-informed guardrail:** the same gate, evidence-promotion process, validator class and configuration, domain facts, and resource budget as C, with those same prespecified domain facts organized through the proposed mapping from referential, semantic, temporal, and contextual reconstruction-failure distinctions to mutation-specific constraints. 

Baseline C and the Challenger must use the same case inventory, underlying domain-fact annotations, evidence-promotion process, validator class and configuration, action resources, and decision budget. Any non-policy component or configuration that cannot be shared must be declared in advance and recorded as a prespecified difference. Both conditions use the same validator class and configuration; the mutation-specific proposition sets 𝑞𝑚 may differ because policy organization is the intended treatment pathway, and the resulting differences in required propositions, their derivation, and coverage must be reported rather than hidden under the phrase “held constant.” The comparison holds the validator process constant, not the policy outputs that it evaluates. 

The case inventory and its diagnostic and taxonomy-neutral strata must be constructed or independently reviewed by a party not involved in authoring either compared policy. Construction and review must take place without access to frozen condition policies. At least one taxonomy-neutral stratum, defined from observable case properties without DIO/ODI labels, should be reported alongside the prespecified diagnostic strata. The diagnostic strata may include temporally reused source-local identifiers, context-dependent relation sufficiency, and hypothesis-conditioned observations with recorded shared upstream origins. The party constructing or adjudicating the corpus must not tailor cases to either policy’s specific rule wording. 

The Baseline C authoring team must not be given the DIO/ODI diagnostic mapping, its category labels, or the Challenger policy; otherwise, the generic condition may inherit the structure it is intended to test. Challenger authors may use the specified DIO/ODI mapping, but must not receive facts withheld from C. The same underlying domain facts must be available to both conditions. Authoring effort, available time, relevant ER/policy expertise, and non-policy execution resources should be matched as far as practicable; authors should not see the counterpart policy or its results before their versions are frozen, and adjudication rules should be prespecified. Prior DIO/ODI exposure must be recorded for all policy authors. 

With one author or team per condition, observed differences are exploratory and cannot isolate diagnostic organization from team-specific expertise. For multi-team replication intended to support stronger comparative claims, independently constituted author teams should be allocated to conditions using a prespecified random or expertise-blocked procedure. The allocation procedure, expertise strata, prior DIO/ODI exposure, and any contamination or cross-condition exposure must be recorded. Repeated runs of one authored policy do not count as independent authoring replications. Stronger comparative claims require multiple independently constituted author teams per condition and an uncertainty analysis that reflects between-team variation. If such replication is infeasible, the result should be reported as a comparison of the particular authoring teams, not as an isolated effect of the DIO/ODI mapping. 

The promotion process may itself govern whether recorded shared upstream origins count as independent corroboration. Strata whose principal challenge is that shared promotion rule should therefore be identified as common-control tests; they isolate an incremental mapping effect only if a distinct, prespecified diagnostic-to-constraint difference is also being tested. If Baseline C 

24


<!-- page 25 -->

independently encodes the same constraints from the same facts, identical outcomes are expected and do not count as evidence of a DIO/ODI advantage. The intended difference is diagnostic organization and its explicit mapping to constraints, not additional information, validator capability, or execution resources. 

The corpus should combine entity-resolution benchmarks with temporally evolving and ambiguous entities where licensing and annotation provenance permit reproducible use. Entity-overshadowing methods provide one source of inspiration [18], while TempEL provides a temporal-evolution setting [24]. Retrieval-augmented generation vulnerability research may inform future perturbation design [23]. The selected datasets, versions, licences, entity identifiers, ground-truth policies, case-construction procedure, and stratum weights must be documented in the experiment report. The commit-boundary test set should contain: (i) cases where names, brands, acquisitions, or partnerships are insufficient to establish identity; (ii) positive identity-continuity cases supported by temporally applicable evidence; (iii) conflicting or stale evidence, including source-local identifier reassignment; and (iv) cases in which mention-to-identifier linkage is uncertain. A taxonomy-neutral stratum should additionally be defined from factual properties without using the DIO/ODI categories. Annotation must separately label (a) whether a mutation is permitted by the common predeclared evaluation reference and (b) whether it is referentially correct according to independent ground truth. Threshold selection and model configuration must be separated from the final test split. Entity-disjoint and perturbation-template-disjoint splits should be used where feasible. Outcome adjudication for Safe Resolution Coverage (SRC), Unwarranted Abstention Rate (UAR), and False Positive Intervention Rate (FPIR) must use a common, independently specified evaluation reference, not either condition’s authored operational policy. Correctness, safety, admissibility, resolvability, and benignness are adjudicated against that common reference by adjudicators independent of policy authors and masked to condition where practicable. PEVR is different: it measures compliance with each condition’s applicable operational contract and is assessed against that contract. A policy-permitted mutation and a referentially correct mutation are separate labels; neither substitutes for the other. 

Concurrency tests should use shared versioned evidence and graph state under controlled workloads. They should measure stale-authorization commits, version-conflict retries, uncertain-commit reconciliation, and whether any candidate is applied after its assumed graph, evidence content, authorization eligibility, or policy context has changed. The promotion process and its version must be held constant between Baseline C and the Challenger; outcome analysis should also distinguish policy specification, evidence promotion, conflict handling, and enforcement/version-control failures. Shared upstream-origin cases governed only by the common promotion contract should not be presented as evidence of a distinct DIO/ODI mapping effect. 

# 8.2 Evaluation Metrics 

Metrics should jointly report unsafe persistence, resolution coverage, abstention, and operational cost. A single safety metric is insufficient because a system that defers every case could appear safe while offering little useful resolution. All outcome labels below, except contract-compliance labels used by PEVR, are assigned against the common independent evaluation reference defined in Section 8.1. **Counting codebook.** Before outcomes are examined, the protocol must define a case-level and operation-level counting codebook. A protected mutation attempt is identified by a unique `operation_id` ; retries, re-evaluations, and reconciliation attempts for the same intended operation do not create additional mutation attempts, while a genuinely new operation has a new identifier. The terminal outcome is assessed at a fixed observation/reconciliation cutoff. A case is resolved only when it reaches a correct terminal identity disposition within that window, including a correct non-match decision where non-identity is the ground-truth outcome. A temporary deferral later resolved within the window is not a final abstention; a case still unresolved at the cutoff remains unresolved. The codebook must define the ground-truth-positive, ground-truth-negative, benign, resolvable, admissible, and correctly resolved labels and their mapping to the case-level confusion 

25


<!-- page 26 -->

matrix. Unknown transaction outcomes still unreconciled at the cutoff remain `unknown` ; they must not be silently recoded as successful or failed commits. 

**Policy-Enforcement Violation Rate (PEVR).** Report protected mutations committed despite a failed authorization condition, unresolved required conflict, invalid scope, or stale bound version, divided by all unique attempted protected mutations. Retries and re-evaluations under the same `operation_id` count once in the denominator. This measures enforcement fidelity to the applicable operational contract; the raw numerator and denominator must also be reported. If there are no unique attempts, the rate is `undefined` . 

**Referentially False Commit Rate (RFCR).** Report referentially false identity-changing commits, as determined by independent ground-truth annotation, divided by all committed identity-changing mutations. Also report the count of false commits per unique attempted protected mutation. This measures the combined effect of policy adequacy, promotion quality, and enforcement; it must not be interpreted as an enforcement-only metric. If no identity-changing mutation is committed, RFCR is `undefined` . 

# **Safe Resolution Coverage (SRC).** 



<!-- Start of picture text -->
SRC = |Correctly and safel |All cases in the prespecified evaluation scope y resolved cases under the common evaluation reference | | .<br><!-- End of picture text -->

The evaluation scope is fixed by the independent corpus and annotation criteria before system outputs are examined; it must not be defined by either supervisor’s eligibility decisions. A resolved case must have a correct terminal match or non-match disposition and satisfy the common reference’s safety criteria. Deferred and still-unknown cases remain in the denominator and do not count in the numerator. If the denominator is zero, SRC is `undefined` . 

**Unwarranted Abstention Rate (UAR).** 



<!-- Start of picture text -->
UAR = |Final unresolved outcomes on common-reference-resolvable cases |All common-reference-resolvable cases| | .<br><!-- End of picture text -->

A common-reference-resolvable case is one for which independent annotation confirms that sufficient admissible evidence exists within the specified observation window. Admissibility is judged against the common evaluation reference, not the condition’s operational policy. An outcome is a final abstention only if it remains unresolved at the prespecified cutoff; temporary deferral followed by a correct resolution within the window is not counted as an abstention. If the denominator is zero, UAR is `undefined` . 

# **False Positive Intervention Rate (FPIR).** 



<!-- Start of picture text -->
FPIR = |Unnecessary interventions on common-reference-beni |All common-reference-benign and resolvable cases gn and resolvable cases | | .<br><!-- End of picture text -->

A benign case is not automatically an intervention error merely because it contains uncertainty: the common reference must also establish that a safe terminal disposition was available within the observation window and that the halt/deferral was unnecessary under the prespecified criteria. Benignness, resolvability, and the intervention window are labeled independently before system comparison. If there are no cases meeting the denominator criteria, FPIR is `undefined` . **Effectiveness.** Report Precision, Recall, and F1 under a prespecified case-level ground-truth policy and publish the confusion-matrix mapping. A predicted positive link between distinct referents is a false positive; a true positive link left unresolved at the cutoff despite being common-reference-resolvable counts as a false negative. Correct non-match decisions are negatives, not abstentions. Report unresolved and deferred outcomes separately. Precision, Recall, and F1 are each `undefined` when their respective denominator is zero; no zero value is substituted for an undefined metric. 

**Commit integrity.** Report counts of stale-authorization commits, duplicate commits after retries, unreconciled `TIMEOUT_UNKNOWN` outcomes, and commits that violate the bound target/effect scope. 

26


<!-- page 27 -->

The expected value for protected stale-authorization commits is zero under the tested transaction contract; this is a testable requirement, not a claim already demonstrated. Report unreconciled unknown outcomes separately at the fixed cutoff, without classifying them as successes or failures. **Efficiency.** The proposed Cost per Correct Resolution (CCR) is 



<!-- Start of picture text -->
Total system cost<br>CCR =<br>Number of confirmed correctly resolved entities .<br><!-- End of picture text -->

Total cost should specify API/token pricing, human validation time and rates, and the compute-pricing basis over a common costing horizon. Policy-authoring and evaluation-corpus construction costs should be reported separately; the report must state whether either is included in the CCR numerator. The denominator must use a declared entity-deduplication rule and count only entities represented by correctly resolved cases. If no entities are correctly resolved, CCR is `undefined` ; report it alongside SRC and abstention metrics. 

Before outcomes are examined, the evaluation must prespecify task- and policy-family-specific decision margins: 𝛿SRC for the largest acceptable reduction in SRC when claiming non-inferior coverage, and 𝛿RFCR for the largest acceptable increase in RFCR when claiming non-inferior false-commit performance. Both margins must be nonnegative and justified from domain risk and coverage requirements rather than selected after observing results. The uncertainty procedure, interval level, analysis unit, case/stratum weights, and aggregation rule must also be prespecified. Because the success rule has two alternative routes, the inferential procedure must account for this two-route decision structure when calibrating uncertainty and the overall claim criterion (for example, through simultaneous bounds or another prespecified multiplicity-control approach). For multi-team inference, the primary comparison should reflect author-team variation; repeated runs of a single policy are nested observations, not independent authoring replications. Case, mutation, run, dataset split, and author team must not be treated as interchangeable units. No particular estimator is mandated in this conceptual paper, but the chosen procedure must respect the declared clustered/repeated structure. 

Let 𝐿𝑆, 𝑈𝑆 denote the prespecified uncertainty bounds for Δ𝑆= 𝑆𝑅𝐶𝐶ℎ𝑎𝑙𝑙𝑒𝑛𝑔𝑒𝑟 −𝑆𝑅𝐶𝐶 , and 𝐿𝑅, 𝑈𝑅 the corresponding bounds for Δ𝑅= 𝑅𝐹𝐶𝑅𝐶ℎ𝑎𝑙𝑙𝑒𝑛𝑔𝑒𝑟 −𝑅𝐹𝐶𝑅𝐶 . The following are the **binding success criteria** , not examples. The incremental-value hypothesis is supported only if at least one of these two prespecified routes is established: 

1. **Lower RFCR at non-inferior coverage:** 𝐿𝑆 > −𝛿SRC and 𝑈𝑅 < 0. 

2. **Improved coverage without a material RFCR increase:** 𝐿𝑆 > 0 and 𝑈𝑅 ≤𝛿RFCR. 

The second route supports improved coverage within the prespecified RFCR tolerance; it does not establish improved safety or strict Pareto improvement. If RFCR is undefined in either condition, neither RFCR-based comparative route is established; the affected route is non-evaluable, not evidence of safety superiority or inferiority. If neither route is established, the incremental-value hypothesis is not supported by the evaluation; this does not by itself establish equivalence, inferiority, or harm. A result in which Baseline C matches or Pareto-dominates the Challenger counts against incremental mapping value for the task and policy family tested, not against DIO/ODI as a broader framework. Component ablations should compare conventional rules, the generic authorization gate, and DIO/ODI-informed binding without bundling all controls into one intervention. Any evaluation of dependency-aware cascade mitigation belongs to future research and must be reported separately from this commit-boundary evaluation. 

# 9. Limitations and Future Research 

The single evidence-state version 𝑣𝐸 is a deliberately conservative invalidation mechanism: a change to evidence unrelated to a particular 𝑞𝑚 can invalidate a pending authorization and increase retries 

27


<!-- page 28 -->

under contention. The design does not claim starvation-freedom or optimal concurrency. Because unresolved conflicts indicated by quarantined or `UNVERIFIED` items can defer an otherwise legitimate mutation, noisy or adversarial inputs may impede progress; abuse-resistant prioritization and adjudication are outside the present contract. Revoking evidence promotion invalidates pending authorizations, but does not retroactively undo completed commits; auditing dependent commits and deciding whether compensating mutations are warranted are outside this paper’s scope. The proposed C-versus-Challenger comparison is also sensitive to policy-authoring skill, as discussed in Section 8.1; a single author or team per condition supports only an exploratory team-level comparison, while stronger claims about incremental mapping value require replication across independently constituted author teams. 

## 9.1 Dependency-Aware Evidence Flow 

The principal limitation is deliberate: the proposed boundary does not prevent an agent from retaining a mistaken hypothesis or from selecting later retrieval actions under its influence. A future dependency-aware architecture could track high-level derivation lineage among hypotheses, actions/queries, observations, and subsequent claims; distinguish multiple documents from genuinely independent corroboration; and expose material dependency information to later planning. Its key test would be whether it reduces unsafe mutation proposals or improves calibrated deferral under controlled hypothesis-conditioned perturbations, without causing disproportionate unwarranted abstention. The present paper does not specify an estimator or claim that such a layer is straightforward to implement. 

## 9.2 Domain-Policy Construction 

The proposal assumes that domain-configured identity-preserving constraints 𝑉𝐸 can be supplied for an entity class and observation domain [6]. In closed enterprise environments, some constraints may be instantiated from schema or identity-management rules [12, 13]. In open-world settings, deciding which properties preserve identity across contexts and time remains difficult. Deriving defensible, domain-scoped constraints from unstructured and context-sensitive material remains an open problem; the present paper assumes that domain policy supplies these constraints and does not propose an automated extraction method. 

## 9.3 Multi-Agent and Contextual Negotiation 

Multi-agent environments may contain agents operating in different observation domains Ω𝐴 ≠Ω𝐵, producing legitimate context-specific reconstructions that differ without either necessarily being erroneous [6, 11, 17, 21]. A shared representation does not imply that every agent should produce an identical contextual reconstruction. Future work should develop protocols for sharing versioned evidence while preserving legitimate context-specific outputs and identifying genuine semantic fragmentation. The commit-boundary design addresses a class of persistence and write-contention risks; it does not resolve semantic disagreement among agents by itself. 

# 10. Conclusion 

Agentic ER enables iterative evidence acquisition and state updates, but an early identity hypothesis may influence later retrieval and create apparent confirmation. This paper deliberately does not claim to eliminate that feedback mechanism. It proposes a narrower architectural contribution: a DIO/ODI-informed boundary between evidence available to an agent for reasoning and evidence eligible to authorize a persistent identity-changing mutation. 

The proposed binding function translates selected distinctions in referential, semantic, temporal, and contextual reconstruction failures into domain-configured constraints for particular mutation classes. 

28


<!-- page 29 -->

Under the stated contract, a protected candidate may be committed only when the relevant candidate graph passes those constraints on claim-specific authorization-eligible evidence, the operation matches its authorized scope, and relevant state and policy versions remain valid. `UNVERIFIED` evidence is not positive authorization support unless separately promoted for the specific claim under the stated contract; insufficient support or unresolved material conflict leads to deferral rather than implicit permission. 

This property is conditional on the adequacy of the domain policy, the claim-specific evidence-promotion process, and enforcement of the commit boundary. The invariant summarizes the specified obligations; it is not offered as a stand-alone theorem of semantic correctness. The contribution is the proposed DIO/ODI-informed organization of domain constraints for mutation-specific identity propositions, integrated with established requirements for claim-specific promotion, proposition coverage, conflict handling, authorized scope, and commit-time version integrity. The paper does not claim novelty for those contract mechanisms individually. It is an abstract design claim, not an empirical result or a guarantee that the underlying evidence is true. The evaluation protocol is proposed future work. A dependency-aware information-flow layer that addresses the upstream hypothesis-conditioned feedback loop remains an explicit research direction beyond the present commit-boundary contribution.
