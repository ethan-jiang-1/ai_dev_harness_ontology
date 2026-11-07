---
source: 2610.08082-polar.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# POLAR: Ontology-Guided Risk Prevention for Tool-Calling LLM Agents · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

# **POLAR: Ontology-Guided Risk Prevention for Tool-Calling LLM Agents** 

**Yunju Kang**<sup>1*</sup> **Seonghyeon Cho**<sup>1*</sup> **Irene Li**<sup>2</sup> **Yeo-Chan Yoon**<sup>3†</sup> **Chanjun Park**<sup>1†</sup> 1Soongsil University 2Tokyo University 3Jeju National University {gardengnosis, chosh040}@soongsil.ac.kr irene.li@weblab.t.u-tokyo.ac.jp ycyoon@jejunu.ac.kr chanjun.park@ssu.ac.kr 

## **Abstract** 

LLM tool-use agents operate in dynamic environments where many actions carry operational risk. However, most safety mechanisms react only after errors manifest. Existing pre-emptive approaches either fine-tune the agent on chain-of-thought deliberation or compile natural-language guardrails into runtime checks, but they do so without exposing a structural, auditable verdict. We propose POLAR, a guardrail framework for small tool-calling agents that assesses reversibility through a structured two-layer ontology. POLAR assigns each action a graded reversibility score by deriving a candidate inverse sequence; calls failing a threshold are pruned before execution. Evaluated on _τ_<sup>2</sup> -bench across six agent models, POLAR improves mean task reward by 0.11 to 0.18 points on airline for four of six agents, but only eight of eighteen model–domain cells improve overall; retail and stronger agents often regress. POLAR provides an auditable structural check and characterizes its task-utility trade-offs. Reward is not a direct measure of prevented harm. 

## **1 Introduction** 

The capabilities of Large Language Models (Xi et al., 2025; Wang et al., 2024) have rapidly evolved from dialogue generation through tool-augmented language modeling (Schick et al., 2023) to autonomous agentic behaviors (Yao et al., 2022; Shinn et al., 2023) that orchestrate multi-tool workflows (Qin et al., 2024). As these agents gain direct write-access to live external systems (initiating payments, finalizing bookings, modifying customer records), a single mistaken tool call can produce irreversible consequences. The hazard is asymmetric: hours of correct execution can be undone by 

> *Equal contribution. 

> †Corresponding authors. 



<!-- Start of picture text -->
@  *call @ validator—_— ad<br>(a) Unguarded Tool Use (b) Post-Hoc Risk Detection<br>@-:->*F¥ @ as<br>Agent Judge Too! Agent {LaverB Tool<br>with(c) ProactiveLLM-as-a-JudgeAgent @(d) POLAR \ (Ours| )<br><!-- End of picture text -->

Figure 1: Four safety patterns for tool-calling LLM agents. **(a) Unguarded:** the agent simply calls the tool. **(b) Post-Hoc Risk Detection:** the tool executes and a registered compensator may undo it after observation. **(c) Proactive Agent with LLM-as-a-Judge:** an LLM gates the call with an allow-or-block label and no structural basis. **(d) POLAR (Ours):** a structural reverse search over the typed action ontology (Layer A) and the actual state (Layer B) produces an inverse sequence _π_ and an auditable score, which a pluggable DecisionPolicy converts into the verdict. 

one irreversible mistake, while no amount of subsequent reasoning can repair such a mistake once it has reached the environment. The most hazardous failure mode for a tool-using agent is therefore not an incorrect answer but an unrecoverable action, a harm class catalogued by recent work (Ruan et al., 2024; Andriushchenko et al., 2025) alongside benchmarks for agent safety (Yuan et al., 2024; Xia et al., 2025a; Debenedetti et al., 2024; Men et al., 2025). 

Despite the centrality of irreversibility, existing safety mechanisms rarely verify it before execution, and the few that do reason textually rather than structurally. SAND (Xia et al., 2025b) finetunes the agent to deliberate in natural-language chain-of-thought, InferAct (Fang et al., 2025) runs pre-emptive Theory-of-Mind belief reasoning over intent, and GuardAgent (Xiang et al., 2024) acts


<!-- page 2 -->

on natural-language guard requests supplied by an end user. These approaches motivate a complementary question: can a reversibility-specific verdict expose the typed relations and candidate recovery path underlying an intervention? 

We propose POLAR, a pre-emptive reversibility gate over a two-layer ontology. Layer A is a static, hand-authored action ontology that encodes each mutating tool’s typed reversibility relations. Layer B is a dynamic state ontology, rebuilt from the available environment state _s_ . Given a candidate action, POLAR backward-derives over Layer A grounded in the current Layer B to assemble a candidate inverse sequence _π_ and a graded reversibility score _ϕ_ POLAR _∈_ [0 _,_ 1]. The hypothetical post-action state _s_<sup>_′_</sup> denotes the intended effect; the evaluated wrapper does not simulate a complete _s_<sup>_′_</sup> before execution. The sequence is an auditable structural hypothesis, not proof that recovery will succeed. We keep Layer A hand-authored to make reversibility assumptions inspectable, although curation does not guarantee their correctness. Figure 1 situates POLAR against unguarded execution, posthoc compensation, and pre-emptive LLM judging. Our contributions are three-fold: 

- **A guardrail for small agents in invertible domains.** POLAR performs relatively well on small-to-mid agents operating in simple, well-bounded domains such as airline, where a mistaken booking can be hard to reverse. In these settings, the gate vetoes calls lacking admissible inverse paths, with positive mean reward differences for four of the six evaluated airline agents. 

- **A training-free pipeline.** POLAR runs as a pre-emptive gate over the existing tool-call interface, leaving agent weights and prompts untouched. Integrating the evaluated agents requires a configuration change; new tool ecosystems also require ontology curation. 

- **An ontology-grounded explanation for every refusal.** POLAR grounds every block in a typed reversibility ontology, with a score or bottleneck exposing the structural reason for refusal. Consequently, each verdict provides an interpretable audit trail, enabling toollevel scrutiny rather than a system-wide assessment. 

# **2 Related Work** 

## **2.1 Foundations of Action Reversibility** 

Classical STRIPS planning calls action _a_ reversible if some sequence _π_ restores the initial state after _a_ (Faber et al., 2021; Russell, 2010). Subsequent work refined this binary notion along strong/weak and uniform/non-uniform axes (Chrpa et al., 2024). Reinforcement learning takes a parallel route, learning reversibility end-to-end as a reset value function (Eysenbach et al., 2017), a self-supervised precedence probability (Grinsztajn et al., 2021), or a risk-critic over recovery zones (Thananjeyan et al., 2021). Together, these two lines establish reversibility as a graded property, a substantial advance over the binary criterion. We build on this foundation by deriving a graded reversibility score from typed ontological relations, retaining the graded character of prior signals while making both the per-action cost and the side-effect surface inspectable at decision time. 

## **2.2 Transactional Mechanisms and Compensation in LLM Agents** 

Recent work treats LLM agent behavior as a database transaction and adapts the Saga pattern (Garcia-Molina and Salem, 1987) to bring ACID-like recovery to long-running workflows. SagaLLM (Chang and Geng, 2025) synthesizes compensating actions _Ci_ at workflow construction time and invokes them in reverse on failure, anchoring recovery in LLM-generated logic and per-workflow checkpointing. STRATUS (Chen et al., 2026) runs mitigation as bounded transactions, each checkpointed and reverted by a systemwide Undo Agent maintaining a stack of executed actions, with a per-transaction commit/abort driven by a scalar severity metric (Transactional NonRegression). An adjacent guard on a disjoint surface is ToolEmu (Ruan et al., 2024), which emulates tool calls in a sandbox at pre-deployment. However, none of these systems exposes the recovery path itself as a declarative pre-emptive artifact: the verdict is a binary commit/abort, and the inverse trace is the recorded forward stack rather than an ontology-derived sequence over typed relations, so the rollback can only be audited after execution. In contrast, POLAR derives a concrete recovery sequence autonomously from typed relations and returns that sequence itself as the pre-emptive safety artifact, making the recovery path inspectable before approval.


<!-- page 3 -->

<!-- Start of picture text -->
ryUserEERequest Oe ner eerLayer Aaca(ActioneriOntology)coneoaee rr) poturnto Agent Loop<br>ve tier relation raw<br>i [omy | inverse-ot(ae) [10<br>ea)<br>care =erereton [ reC5 irene]| eter eecte sin) [over0 | sootsiwios‘ | (teredExeowion<br>LayerfmseratanB see ) Grounding Witness aes cont frwardcalT we<br>(State Snapshot) rw-prlecte'toLayeproject tolaye r h<br>carenSS)ren. ForwarderanTransition psteceeReverse comenleSearciliea2ey se)<br>[sites] oxo] s<br>[sett[seratont|avestia_[sai  —aoee|antinori| sm |un00 | Apply T(6)Jto states al| neat,oiixasononieear”)=a ss) | nardaeeé | (QegmmDecisionVetonny Policywane<br>[eration]<br>B= (Sz eee[rewritee| gsate e stt@s || me cacnea||",a¥g|uneo | asserons} 1) (SemprePaterarns otctec 7es oe [ectedeaaocontent<br>Deterministic a ee —, | aaa<br>Materialzation Resiitinglstatersy(hypothetical Joghia onlyconn+ (9-081do ot block<br><!-- End of picture text -->

Figure 2: Structural overview of the POLAR framework. In the evaluated wrapper, the candidate tool sequence is checked against the available current-state projection; a complete post-action state is not simulated, and the classifier and intent parser shown as modular components are not invoked at decision time. 

## **2.3 Proactive Safety and Structural Reasoning** 

Other pre-emptive approaches rely on naturallanguage reasoning rather than typed structure. SAND (Xia et al., 2025b) and InferAct (Fang et al., 2025), introduced in Section 1, demonstrate that pre-emptive intervention can prevent harms before they materialize. However, in each the safety verdict is a string-level judgement without a graded reversibility score or an executable inverse plan. POLAR instead computes this score from a backward inference over typed reversibility relations, returning a structural verdict rather than a textual judgement. Because each verdict is grounded in typed reversibility relations, the reason an action is flagged can be traced back to specific ontology edges rather than to a free-form rationale. The graded score further turns the enforcement choice into a tunable threshold rather than another LLM judgement, and the derivation produces an executable inverse sequence to enable pre-emptive validation of preconditions against the runtime state. 

# **3 Methodology** 

## **3.1 Overall Framework** 

We describe POLAR across four components: a two-layer ontology (Section 3.2), a reverse-search procedure that consults the ontology to assemble an executable inverse sequence (Section 3.3), a 

graded reversibility score _ϕ_ POLAR that quantifies the safety of that sequence (Section 3.4), and a pluggable decision policy that separates the safety verdict from the enforcement decision (Section 3.5). Figure 2 shows the structure of the POLAR framework. 

## **3.2 Two-Layer Ontology** 

POLAR maintains two ontology layers, separated by what they encode and when they are populated. 

## **Layer A: action ontology (static, per domain).** 

Layer A is a Datalog encoding, hand-authored by a domain _curator_ , of how each mutating tool affects the typed entity slots the domain bookkeeps. The curator is the human ontology author who declares each tool’s reversibility relations and anchors its per-step weights. It is organized as a hierarchy of five typed reversibility relations, _T_ 1 through _T_ 5, each mapped to a per-step score _ϕ_ (Table 1). 

The gradient runs from exact recovery ( _T_ 1, _T_ 2) through partial compensation ( _T_ 3) to fail-closed irreversibility ( _T_ 4, _T_ 5). Each annotation carries a curator weight _w ∈_ (0 _,_ 1] encoding annotation confidence. _T_ 2’s precondition Bound is checked against the available Layer B projection, and _T_ 3’s loss weight _w_ loss _∈_ [0 _,_ 1) is a curator-anchored scalar of the LossClass (e.g. a cancellation fee or audit-trail entry) selected before evaluation.


<!-- page 4 -->

|tier|relation|per-step_ϕ_|band|
|---|---|---|---|
|_T_1|inverse_of(_Ta, Tb,_Slot_, w_)|_w_|reversible|
|_T_2|bounded_reversibility(_T,_Bound_, w_)|_w ·_**1**[Boundat_s_]|reversible|
|_T_3|compensates(_Ta, Tb,_LossClass_, w_)|_w ·_(1_−w_loss)|compensable|
|_T_4|irreversibly_consumes(_T,_EntitySlot)|0|irreversible|
|_T_5|external_side_effect(_T,_SinkClass)|0|irreversible|



Table 1: Reversibility tiers and per-step _ϕ_ score. Each Layer-A annotation carries a curator weight _w ∈_ (0 _,_ 1]; the per-step _ϕ_ inherits _w_ and, for _T_ 3, the LossClass weight _w_ loss. Tiers _T_ 1– _T_ 2 form the reversible band; _T_ 3 is the compensable band (0 _< ϕ <_ 1); _T_ 4– _T_ 5 are irreversible ( _ϕ_ = 0, fail-closed). The score measures annotated recoverability, not overall action safety or user authorization. 

# **3.4 Reversibility Score** 

The per-step score _ϕ_ ( _u_ ) is set by the tier of the matching annotation _α_ (Table 1): a _T_ 1 step keeps its full curator weight _wα_ ; a _T_ 2 step keeps _wα_ only when its bound holds in the available Layer B projection at _s_ , otherwise zero; a _T_ 3 step pays a fraction proportional to its loss class; _T_ 4 and _T_ 5 are zero by construction. The score of the whole sequence is the weakest step, 



<!-- Start of picture text -->
ϕ POLAR( π ) = min u∈π ϕ ( u ) ∈ [0 ,  1] , (1)<br><!-- End of picture text -->

so a single irreversible step pulls the verdict to zero and is reported as the bottleneck. 

# **Layer B: state projection (dynamic, per ses-** 

**sion).** Layer B is the current state, written out as typed slot assertions of the form slot(entity_type _,_ entity_id) = value. We rebuild it at every turn from the _τ_<sup>2</sup> -bench database and the agent’s executed tool calls, not from anything the LLM imagines, so the safety verdict is always grounded in the actual environment. 

**Admissibility check before scoring.** Scoring only runs on steps that have already passed admissibility. Annotations that are provisional (LLMdrafted, not yet promoted), revoked, disputed, or ungrounded against Layer B never enter the sequence in the first place. This keeps untrusted annotations from contaminating the safety verdict through future aggregator changes. 

# **3.5 Decision Policies** 

# **3.3 Reverse Search** 

Let _s_ be the state before the agent’s candidate tool call and _s_<sup>_′_</sup> its hypothetical post-action state. In the evaluated wrapper, POLAR checks the candidate tool sequence against the available current-state projection rather than a fully simulated _s_<sup>_′_</sup> : walking the candidate tools most-recent-first, it queries Layer A for an inverse. A matching annotation in Layer A yields an inverse step _u_ and its weight; bounded_reversibility contributes only when its Bound holds in the available Layer B projection. Concretely, for each candidate tool the search enumerates its admissible undo edges and combines them into candidate inverse sequences, with _T_ 2 bound conditions and overlap checks evaluated against the available Layer B projection. 

The search terminates either by composing a full inverse sequence _π_ = _⟨un, . . . , u_ 1 _⟩_ as a candidate recovery path, or by reporting the first step that fails admissibility, with a reason. This backward derivation parallels reachability-based safety analysis (Fisac et al., 2018) but operates over typed reversibility relations rather than continuous state; unlike LLM+P (Liu et al., 2023), no external symbolic planner is invoked. The verdict is fully determined by the matched annotation and the available Layer B snapshot. 

The reverse search and _ϕ_ POLAR produce a safety verdict on a candidate action; they do not by themselves decide what the agent does with that verdict. We separate verdict generation from policy execution through a DecisionPolicy interface that returns one of three actions: APPROVE, VETO, or ESCALATE. Three concrete policies are implemented; only VETOPOLICY has verified comparative reward results. 

- **VETOPOLICY** : Refuses a mutating tool call when reverse search either cannot find a complete inverse sequence _π_ or returns _ϕ_ POLAR( _π_ ) _< τ_ (fixed at 0 _._ 80). It acts as a strict, binary pre-emptive safety gate by replacing the agent message with a static refusal. 

- **ESCALATEPOLICY** : On unreachable turns, it checks recent user messages for an affirmative consent token using a regex baseline. If found, the call is approved; otherwise, it requests confirmation via a “Do you confirm? (yes/no)” prompt and drops the call. 

- **ADVISORYPOLICY** : Never blocks; emits an audit log entry only. Used for offline measurement that must not perturb the agent’s trajectory.


<!-- page 5 -->

|model|domain|baseline|InferAct|saga_lite|POLAR (Ours)|
|---|---|---|---|---|---|
||airline|0.351_±_0.039|0.393_±_0.040|0.440_±_0.041|**0.462**_±_0.041|
|qwen3-8B|retail|**0.213**_±_0.033|0.147_±_0.029|0.111_±_0.026|0.113_±_0.026|
||telecom|0.030_±_0.015|0.076_±_0.023|**0.157**_±_0.033|0.068_±_0.022|
||airline|0.291_±_0.040|0.402_±_0.054|0.403_±_0.044|**0.473**_±_0.047|
|llama-3.1-8b|retail|0.047_±_0.021|0.063_±_0.023|0.067_±_0.024|**0.076**_±_0.026|
||telecom|0.009_±_0.009|**0.085**_±_0.033|0.026_±_0.018|0.062_±_0.025|
||airline|0.277_±_0.037|0.333_±_0.038|0.353_±_0.039|**0.387**_±_0.040|
|nemotron-9b|retail|0.168_±_0.031|**0.180**_±_0.031|0.161_±_0.033|0.135_±_0.028|
||telecom|**0.133**_±_0.028|0.093_±_0.024|0.120_±_0.026|0.081_±_0.022|
||airline|0.370_±_0.044|0.367_±_0.046|0.398_±_0.047|**0.478**_±_0.047|
|gemini-flash-lite|retail|0.101_±_0.036|**0.113**_±_0.035|0.064_±_0.031|0.076_±_0.033|
||telecom|**0.012**_±_0.012|0.000_±_0.000|0.009_±_0.009|0.011_±_0.011|
||airline|**0.527**_±_0.041|0.423_±_0.041|0.493_±_0.041|0.453_±_0.041|
|gpt-oss-120B|retail|**0.455**_±_0.041|0.401_±_0.040|0.211_±_0.034|0.213_±_0.033|
||telecom|0.093_±_0.024|**0.203**_±_0.033|0.047_±_0.017|0.113_±_0.026|
||airline|**0.660**_±_0.040|0.527_±_0.041|0.572_±_0.041|0.541_±_0.041|
|qwen3.5-27B|retail|**0.383**_±_0.040|0.349_±_0.039|0.193_±_0.032|0.173_±_0.031|
||telecom|**0.327**_±_0.038|0.273_±_0.036|0.187_±_0.032|0.267_±_0.036|



Table 2: Mean task reward _±_ SE on _τ_<sup>2</sup> -bench across six agent models (150 attempted runs per cell; error-terminated runs excluded). Bold = best arm in row. 



<!-- Start of picture text -->
o7 aitine eta tsecom<br>oe<br>Bos<br>i<br>goo<br>Fo2<br>oa<br>ve<br>oF Ph as ght sat i a a<br>OOP oP OOP OB OOPoO GO<br><!-- End of picture text -->

Figure 3: Mean task reward by domain, model, and safety arm (150 attempted runs each). Within each model group, the four bars are BASELINE, INFERACT, SAGA_LITE, POLAR (left to right). 

## **3.6 Putting It Together** 

# **4 Experiments** 

Given a candidate forward action, POLAR derives a verdict in four steps. (1) Layer B is reconstructed from the executed tool record to give the current state. (2) The reverse search consults Layer A to compose an admissible inverse sequence against Layer B. (3) The sequence is scored by its weakest step. (4) A pluggable DecisionPolicy converts the score into one of APPROVE, VETO, or ESCALATE. The broader architecture includes a ThreeWayClassifier for request routing and an IntentParser for intent mapping; neither is invoked in the evaluated wrapper. The evaluated gate repeats at candidate mutating tool calls, vetoing calls without an admissible inverse path. We turn to its quantitative evaluation in Section 4. 

We evaluate POLAR on three _τ_<sup>2</sup> -bench domains (Barres et al., 2025) across six agent models that span a wide range in baseline reward, comparing four safety arms with 150 task runs per cell. The remainder of this section moves from whether POLAR helps to which parts of the verdict drive that help, how the verdict can be enforced, and what it actually blocks: (i) the main reward result across all cells, together with a per-domain descriptive trend in POLAR’s observed reward differences; (ii) local sensitivity along two axes, with an anchor sweep over the ontology’s loss-class weights and a downward sensitivity analysis over the policy’s reward threshold; (iii) a tier ablation that probes reversibility relations; (iv) the available evidence


<!-- page 6 -->

for three decision policies on the reverse-search verdict; and (v) a qualitative breakdown of what POLAR actually blocks. 

# **4.1 Experimental Setup** 

For each of the 72 (model, domain, arm) cells we run three trials of 50 tasks each ( _n_ =150 per cell). The full model lineup is in Appendix A. Further supporting evidence, including per-cell error counts, is provided in Appendix B and Appendix B.4. The _τ_<sup>2</sup> -bench user simulator is held fixed at qwen/qwen3-8b, and both _τ_<sup>2</sup> -bench’s conversation reviewer and the retail natural-language judge use openai/gpt-4o-mini, isolating the agent as the only varying axis. The study protocol specifies fixed ontology weights, but contemporaneous registration and per-run ontology/configuration hashes are not independently archived. The four safety arms are: BASELINE (no safety gate), INFERACT (a two-stage critic adaptation of Fang et al. (2025)), SAGA_LITE (adapting the compensationregistry pattern of Chang and Geng (2025)), and POLAR (the veto policy of Section 3.5, the only POLAR variant reported in the main result). 

# **4.2 Main Result** 

Tables 2–3 report mean task reward and the difference of separately error-filtered arm means against the baseline; Figure 3 plots both. The eighteen (model, domain) cells fall into two regimes: POLAR’s gains are largest on weak-to-mid agents in airline, and its regressions concentrate on highbaseline agents and on the user-intent-dominated retail domain. An observed per-domain trend, characterized next, describes this split. On airline, POLAR outperforms INFERACT on all six cells and SAGA_LITE on four weak-to-mid cells. Overall, POLAR improves mean reward in eight of eighteen cells. These comparisons use evaluated adaptations rather than validated reproductions of the cited systems. Task reward does not directly measure prevented harm or isolate reverse search from conservative blocking. 

**An observed trend in baseline reward.** Plotting baseline reward against the difference of arm means across the eighteen cells (Figure 4) yields per-domain linear fits: the delta declines with the agent’s baseline at a rate near 0 _._ 7 on airline and retail and a shallower 0 _._ 31 on telecom ( _R_<sup>2</sup> = 0 _._ 92 _,_ 0 _._ 98 _,_ 0 _._ 65). These are descriptive fits to only six agent points per domain, not predictive laws or zero-crossing deployment rules. Headroom 

|model|airline|retail|telecom|
|---|---|---|---|
|qwen3-8B|+**0**_._**111**|_−_0_._100|+**0**_._**038**|
|llama-3.1-8b|+**0**_._**182**|+**0**_._**029**|+**0**_._**053**|
|nemotron-9b|+**0**_._**110**|_−_0_._033|_−_0_._053|
|gemini-flash-lite|+**0**_._**109**|_−_0_._026|0_._000|
|gpt-oss-120B|_−_0_._073|_−_0_._242|+**0**_._**020**|
|qwen3.5-27B|_−_0_._119|_−_0_._209|_−_0_._060|



Table 3: Difference of separately error-filtered arm means ∆POLAR = _r_ POLAR _− r_ baseline across the 18 (model, domain) cells (150 attempted runs per arm; valid counts differ). Bold sign marks ∆ _>_ 0. A displayed 0 _._ 000 is a rounded difference, not evidence that both arm means are zero. Matched differences and effective pair counts are in Appendix D. 



<!-- Start of picture text -->
oy Celing effect POLAR gain shrinks as baseline rons<br>aad o ee<br>’ a 7<br>3z a“ moa . Ms,<br>3 ar ~<br>i2<br>z4 e .<br>E014 e i.<br>j . se<br>024 ae<br>.<br>feline reward 00 POLAR)<br><!-- End of picture text -->

Figure 4: Descriptive per-domain fits to differences of arm means across eighteen model–domain cells. Dashed lines are OLS fits, with airline ∆= _−_ 0 _._ 76 _b_ + 0 _._ 37 ( _R_<sup>2</sup> = 0 _._ 92), retail ∆= _−_ 0 _._ 67 _b_ + 0 _._ 06 ( _R_<sup>2</sup> = 0 _._ 98), and telecom ∆= _−_ 0 _._ 31 _b_ + 0 _._ 03 ( _R_<sup>2</sup> = 0 _._ 65). These six-point fits are not predictive laws or deployment thresholds; matched estimates with uncertainty are in Appendix D. 

(how often the unguarded agent is wrong on safetycritical calls) and fit between reversibility and the domain’s requirements are possible interpretations, not established mechanisms. The baseline appears on both axes, creating mathematical coupling; the slopes do not identify causal headroom. Matched estimates, uncertainty, and a corresponding plot appear in Appendix D. 

**Significance on the primary cell.** On the primary cell of qwen3-8B on airline with 150 attempted runs per arm, the originally reported +0 _._ 111 subtracts separately filtered arm means. It is not a paired estimator. Matching non-error observations by task and trial yields 143 pairs and a +0 _._ 119 mean difference with task-cluster bootstrap 95% CI [+0 _._ 057 _,_ +0 _._ 184] (Appendix D). We do not transfer the original tests to this new estimand; informative failures may still bias complete-case


<!-- page 7 -->

matching. 

togram of already admitted paths (Appendix B.1) comes from a different run. 

# **4.3 Robustness** 

We probe the headline along two axes: whether the verdict depends on the exact loss-class weights baked into Layer A, and whether the reward threshold of _τ_ = 0 _._ 80 is itself the post-hoc choice that drives POLAR’s gain. 

**Anchor sweep over loss-class weights.** Figure 5 reports a sensitivity sweep around the selected anchor for the primary agent (qwen3-8B). Airline and retail use a 5-by-5 grid over the two dominant loss classes per domain; telecom uses a 1-by-9 row over its single weighted loss class. Across all 58 sweep cells the maximum cell-to-anchor delta is 0 _._ 053, well within the anchor cell’s standard-error band. This local sweep does not validate annotation correctness or establish global robustness. 



<!-- Start of picture text -->
aitine — cancelation<br>fee x rebookingpce it<br>02 os<br>035<br>Ba<br>H oa<br>* 0.05.<br>on<br>00801Tebookingalspices0203 5;<br>035<br>rata — Rem swap, oven x paymentswaps overhead 3<br>$ :<br>3,- IBS we es 028i<br>5<br>Jen oo (Bes<br>oor payment00s swap.overneadans on 02<br>sr 000s 001 002t e lecom005Toss— lossco?elonee weghtal sweepais a2. 03<br><!-- End of picture text -->

Figure 5: Local anchor sensitivity for qwen3-8B: reported reward difference across the 58 sweep cells, with the main anchor marked. Maximum cell-to-anchor delta is 0 _._ 053, within the anchor’s standard-error band. 

**Downward threshold sensitivity.** Sweeping the reward threshold downward from 0 _._ 80 to 0 _._ 50 changes candidate retention in an instrumented fixed-trajectory run. The corresponding _ϕ_ his- 

|scope|0_._50|0_._70|0_._80|0_._85|0_._90|0_._95|
|---|---|---|---|---|---|---|
|all|100%|71.1%|70.7%|62.0%|50.6%|50.6%|
|airline|100%|36.6%|36.6%|17.6%|17.6%|17.6%|
|retail|100%|100%|100%|100%|48.9%|48.9%|
|telecom|100%|100%|98.7%|98.7%|98.7%|98.7%|



Table 4: Fraction of 996 logged decisions with nonempty candidate pools for which at least one candidate meets each reversibility threshold in the instrumented xmodel_phi_logged run. The 979 alreadyapproved paths in Table 8 come from different runs. 

The domain-specific cliff lies in the 0 _._ 70–0 _._ 95 range (Table 4). At the anchor cutoff, airline retains 36 _._ 6% of verdicts, retail retains 100%, and telecom retains 98 _._ 7%. Airline’s verdict distribution is therefore sensitive to the selected operating point, whereas retail and telecom retain more candidates in this fixed-trajectory diagnostic. This does not estimate task reward at other thresholds or establish an optimal cutoff. The four-bucket _ϕ_ distribution from a separate run is in Appendix B.1. 

# **4.4 Tier Ablation** 

To examine tier restrictions, we ablate Layer A on the primary cell (qwen3-8B airline, 150 attempted runs per arm). Table 5 reports five configurations from separate archived runs, each compared with its own baseline; the main-run +0 _._ 111 is not the ablation full-row value. 

**Which tiers carry the gain.** The airline ontology carries no _T_ 1 annotation, so the T1-only setting admits no active inverse edge for mutating calls and behaves close to a blanket veto. Its observed +0 _._ 087 gain is not smaller than the full setting’s +0 _._ 080 gain. The intervals overlap and each configuration used a separate baseline rerun. These results do not establish a reward contribution from structural reverse-path composition beyond conservative refusal. 

**Admissibility diagnostic.** The no-irreversible row probes the admissibility design of Section 3.4: when T4 and T5 are admitted with _ϕ_ = 1 rather than fail-closed at _ϕ_ = 0, the observed gain is 0 _._ 060 with an interval crossing zero. This suggests a possible contribution from fail-closed behavior, but separate runs do not isolate its causal effect or demonstrate harm prevention.


<!-- page 8 -->

|variant|∆|bootstrap 95% CI|perm._p_|
|---|---|---|---|
|full (T1, T2, T3)|0_._080|[0_._013_,_0_._147]|0_._036|
|no T3 (T1, T2)|0_._073|[0_._020_,_0_._127]|0_._013|
|T1 + T3 only|0_._087|[0_._027_,_0_._147]|0_._010|
|T1 only|0_._087|[0_._020_,_0_._153]|0_._017|
|<br>no irreversible|0_._060|[_−_0_._007_,_0_._127]|0_._121|



Table 5: Tier ablation on qwen3-8B airline (150 attempted runs per arm). Each row uses its own baseline rerun; FULL in this ablation differs from the main experiment. NO IRREVERSIBLE admits T4, T5 with _ϕ_ = 1 (no fail-closed). Archived stdout preserves rewards and summaries but not complete trial JSONL or exact configurations. 

## **4.5 Decision Policy Comparison** 

The reverse-search verdict is decoupled from the enforcement decision (Section 3.5): the same _ϕ_ POLAR and inverse sequence can drive a hard veto, a consent-aware escalation, or pure audit logging. We document the three on the primary qwen3-8B airline cell. Veto refuses unreachable calls; Escalate requests consent; Advisory logs without blocking. The verified main-run baseline and Veto means are 0 _._ 351 and 0 _._ 462, respectively. Archived Escalate and Advisory means conflict with the submitted table, while exact comparison baselines and trial JSONL are unavailable. We therefore withhold their comparative effects and policy ranking. The consent regex remains unvalidated, particularly for multilingual negation (Appendix B.2). 

## **4.6 What POLAR Blocks** 

To make the safety verdict concrete, we tabulate the tools POLAR most often blocks across the sixagent run. Table 6 lists the top (model, domain, tool) triples with their trigger reason. Two patterns emerge. 

|model|domain|tool|count|
|---|---|---|---|
|GPT-OSS-120B|retail|return_delivered_order_items|150|
|GPT-OSS-120B|retail|exchange_delivered_order_items|103|
|Nemotron-9B|airline|update_reservation_flights|77|
|Nemotron-9B|retail|exchange_delivered_order_items|69|
|Nemotron-9B|retail|return_delivered_order_items|69|
|GPT-OSS-120B|airline|update_reservation_flights|62|
|Qwen3-8B|airline|update_reservation_flights|61|
|Qwen3.5-27B|airline|update_reservation_flights|60|



Table 6: Top blocked (model, domain, tool) triples across the six-agent run, ranked by block count. The corresponding bottleneck reasons (NO_CANDIDATE for airline, EXTERNAL_SIDE_EFFECT for retail) are discussed in the text and decomposed fully in Appendix B.3. 

**Airline blocking pattern.** The dominant blocked tools on airline are update_reservation_ flights and cancel_reservation, both triggered by NO_CANDIDATE: the reverse search cannot compose a complete admissible inverse, so the gate fires. These are structurally unsupported calls under the ontology, but the log does not independently label each blocked call as harmful. 

**Retail blocking pattern.** The dominant blocked tools on retail are return_delivered_order_ items, exchange_delivered_order_items, and cancel_pending_order, all triggered by EXTERNAL_SIDE_EFFECT. These tools can be legitimate user requests; refusing them for low reversibility is a plausible explanation for the retail reward losses, especially on gpt-oss-120B. Because the evaluation reports task reward rather than independent harm or authorization labels, the block log cannot establish false-veto rates or prevented harm. Full decompositions over all 1 _,_ 745 blocked decisions are in Appendix B.3; pipeline prompts are in Appendix C. 

# **5 Conclusion** 

We presented POLAR, a pre-emptive framework that assesses tool-call reversibility by composing a candidate inverse sequence over a two-layer ontology and scoring it with a graded _ϕ_ POLAR. Beyond the headline reward gain, our multi-model experiments characterize when structural gating improves task reward and when it backfires: an observed per-domain trend on _τ_<sup>2</sup> -bench shows larger gains for weaker airline agents, while retail and stronger-agent cells often regress. Headroom and fit between reversibility and domain requirements are possible explanations, not established mechanisms. This analysis suggests a methodological shift: from asking “can the LLM judge whether this action is safe?” to asking “does an admissible inverse exist?”. The latter has an auditable structural answer rather than an unstructured label. Direct safety benefits and superiority to a trivial conservative blocker remain to be tested. 

# **Limitations** 

POLAR is a hard pre-emptive gate, and its reward gain shrinks as the unguarded agent’s baseline grows in this sample. The fitted trend does not define a zero-crossing deployment threshold. POLAR beats the unguarded baseline on eight of eighteen cells, not uniformly dominating other


<!-- page 9 -->

evaluated arms. A confidence-aware dynamic gate that invokes the reverse search only when an uncertainty signal (token log-probability, selfconsistency divergence, or a verifier head) exceeds a routing threshold might improve highbaseline performance without discarding the structural check on ambiguous calls, but is untested. For new domains, the observed trend suggests an authoring discipline that classifies each mutating tool as state-change-dominated or user-intentdominated, maps each category to the matching Layer A relations, and pairs the resulting ontology with a candidate enforcement policy accordingly (Appendix C.5). Both directions, together with a worked example on a fourth domain, are left to future work. 

Reward is not a direct safety label. The blocked decisions lack independent harm and authorization annotations, and the T1-only configuration does not isolate a benefit beyond blanket veto. The evaluated wrapper does not simulate a complete post-action state or validate inverse execution. Ontology authoring effort, semantic errors, and adversarial robustness remain unmeasured for the original study; a missing irreversible relation can permit false approval if a positive relation remains. Archived runs have incomplete configuration and ontology provenance, and the comparison arms are adaptations with different decision inputs and call budgets. 

# **Ethical Considerations** 

All evaluation is performed on _τ_<sup>2</sup> -bench, a publicly released benchmark whose tasks and underlying databases are synthetic and contain no real user data; agent and user turns are produced by language-model simulators, and no crowd work, annotation, or user study was conducted. The ontology, analysis pipeline, per-trial summaries, and the _τ_<sup>2</sup> -bench evaluation harness configuration are archived privately; their public release scope, licenses, and URL remain to be confirmed. The full multi-trial run spans 72 (model, domain, arm) cells at 50 tasks _×_ 3 trials per cell (10 _,_ 800 simulation rollouts), and the weight-sensitivity sweep adds _∼_ 2 _,_ 850 rollouts; all inference is served via thirdparty APIs (OpenRouter for agents, OpenAI for the external reviewer and the retail NL judge), so we do not amortize model-training emissions. We used large language models for editorial and analysiscode assistance; the authors remain responsible for the analyses, claims, and final text. 

**Potential Risks** A reversibility-based safety framework could in principle be inverted to author actions that are intentionally hard to undo. We consider this risk low: POLAR’s Layer A is declarative and auditable, and any adversarial use would require domain authoring access already sufficient to cause harm without POLAR. Conversely, publishing which actions are structurally irreversible primarily benefits deployers rather than attackers. 

# **Acknowledgements** 

This work was supported by the Korea Internet & Security Agency (KISA) grant funded by the Korea government (PIPC) (No. RS-2026-25526342, Development of Technologies for Preventing Sensitive Information Inference and Risk Assessment in Foundation Model Operations). This research was also supported by the Culture, Sports and Tourism R&D Program through the Korea Creative Content Agency grant funded by the Ministry of Culture, Sports and Tourism in 2026 (Project Name: Develop AI agent technology to connect knowledge through public cultural facility-based discussion and communication, Project Number: RS-202625520645). Further support was provided by the National Research Foundation of Korea (NRF) grant funded by the Korea government (MSIT) (RS-2026-25483747). This work was additionally supported by the Institute of Information & communications Technology Planning & Evaluation (IITP, AI Computing Support Project for R&D) grant funded by the Korea government (MSIT) (High-Performance Research AI Computing Infrastructure Support at the 2 PFLOPS Scale, RS-202625505492).
