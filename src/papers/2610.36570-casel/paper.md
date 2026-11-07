---
source: 2610.36570-casel.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# CASEL: Consequence-Aware Selective Execution for Reliable Long-Horizon Tool-Using Agents · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

# CASEL: Consequence-Aware Selective Execution for Reliable Long-Horizon Tool-Using Agents 

1<sup>st</sup> Yanyan Zhang _Carnegie Mellon University_ Pittsburgh, PA 15213, USA zhangyanyanusa@gmail.com 

2<sup>nd</sup> Fei Shen 

_Feinity LLC_ 

Sacramento, CA 95816, USA shenfei2031@hotmail.com 

3<sup>rd</sup> Ting Yan 

_Computer Science Department Dartmouth College_ Hanover, NH 03755, USA ting.yan.gr@dartmouth.edu 

4<sup>th</sup> Hao Zhang<sup>*</sup> 

_Independent Researcher_ 

Los Angeles, CA 90095, USA 

> *Corresponding author: alex1995101099@gmail.com 

**_Abstract_ —Tool-using language agents increasingly modify external systems, yet most runtime safeguards allocate scrutiny by generic uncertainty scores or coarse mutation heuristics. We introduce CASEL (Consequence-Aware Selective Execution Layer), a model-agnostic runtime allocation policy that combines calibrated failure probability, state-dependent consequence, reversibility, ambiguity, and evidence freshness to choose, for each proposed tool call, among direct execution, verification, sandboxing, clarification, approval, and abstention by minimizing a per-mode cost. We formalize direct execution as selective prediction and state and test the validity conditions of a finite-sample threshold and a trajectory risk ledger. In a controlled simulation over 20 seeds with 120,000 test actions each, in which every method has the same intervention menu and the same compute cost, CASEL reduces harmful-side-effect trajectories from 14.75 percent for an uncertainty-ranked gate to 7.02 percent and mean normalized harm from 0.184 to 0.123. A gate ranked by the product of failure probability and consequence reaches similar harm (5.82 percent, 0.120) but sends 45 percent more actions to human approval, and removing reversibility-aware routing raises the rate to 15.53 percent. A trajectory-level risk budget, in contrast, increases harm at equal cost (11.82 percent). Intervention effectiveness is assumed, not measured: the results rank allocation rules under the simulator’s assumptions and do not establish deployment effectiveness.** 

**_Index Terms_ —LLM agents, tool use, reliability, selective prediction, uncertainty calibration, runtime verification, riskaware execution.** 

## I. INTRODUCTION 

Language-model agents increasingly act on external systems over long trajectories, and as models grow more capable they become autonomous domain-specific agents, e.g., SP-Mind runs complete spatial-proteomics analyses with specialized tools.<sup>[1]</sup> They now also generate device configurations for multi-vendor optical transport networks,<sup>[2]</sup> where an erroneous change can affect live services. Benchmarks such as WebArena, _τ_ -Bench/ _τ_<sup>2</sup> -Bench, and AgentDojo expose failures from stale state, planning errors, unsafe tool use, and adversarial observations.<sup>[3]–[6]</sup> Reflection and self-critique improve reasoning,<sup>[7],[8]</sup> and recent work studies clarification, abstention, mutating-action verification, least privilege, and 

transactional containment.<sup>[9]–[13]</sup> These mechanisms address different failure sources but leave a common allocation question: _how much scrutiny should be spent before a particular action is allowed to change the world?_ 

Uncertainty alone does not answer it. Two actions may share a 20% probability of error, yet a read-only search is cheap to retry while an irreversible transfer is costly; an uncertainty-only gate treats them alike, and a mutation-only gate still conflates a reversible edit with an irreversible commitment. 

We propose CASEL, a runtime layer between an arbitrary base agent and its tool executor (Figure 1). At each step the controller estimates failure probability _p_ ˆ _t_ , consequence _c_ ˆ _t_ , reversibility _ρt_ , ambiguity _gt_ , and evidence staleness _dt_ , and selects a graded intervention. Scrutiny should scale with consequence-weighted risk rather than generic confidence, the intervention should match the action’s reversibility, and direct execution should be calibrated as selective prediction.<sup>[14]–[16]</sup> CASEL is therefore not another uncertainty gate but a runtime _allocation policy_ that decides where scrutiny is worth its cost and calls existing safety mechanisms as its intervention branches. 

Our contributions are: (i) a consequence-aware execution objective with six intervention modes, five of which are exercised (abstain and the staleness signal _dt_ are not); (ii) explicit validity conditions for a finite-sample direct-execution threshold, shown to bind and hold over a sweep of _ϵ_ , and an analysis of a trajectory risk ledger whose premise fails in practice; and (iii) a reproducible controlled evaluation in which all comparators share the intervention menu and cost, with ablations, paired significance tests, stress tests, and a negative result for trajectory budgeting, plus a deployment path. 

## II. RELATED WORK 

**Agents and benchmarks.** ReAct interleaves reasoning with action and Reflexion stores verbal feedback across attempts;<sup>[7],[8]</sup> WebArena and the _τ_ -family emphasize stateful, long-horizon tool use.<sup>[3]–[5]</sup> Focus-Then-Contact learns robot skills with residual RL under timed human intervention,<sup>[17]</sup> and


<!-- page 2 -->

<!-- Start of picture text -->
(a) CASEL runtime: one routing decision per proposed tool call<br>User objective Risk signals of the proposed call  at CASEL selective controller direct verify<br>and context ht mt<br>p ˆ t failure prob. c ˆ t consequence J ( m )= γm  ˆ ptc ˆ t + λk ( m )+ µq ( m ) sandbox approve<br>m ∗ = arg min m∈Mt ( ρt )  J ( m )<br>ρt reversibility gt, dt ambiguity, age optional: Ht− 1+¯ rt>BH ⇒ escalate clarify abstain<br>Base agent at high gt ⇒ clarify; stale dt ⇒ re-read<br>(any LLM)<br>Ht− 1<br>observations, evidence age Optional risk ledger outcome Tool executor<br>Ht = � i≤t, i∈D r ¯ i ≤ BH & environment<br>(b) Same calibrated p ˆ t = 0 . 20 , different consequence  ⇒ three different modes<br>read-only search direct reversible edit sandbox irreversible transfer approve Parameters λ =0 . 02, µ =0 . 015<br>dir. ver. sbx. appr.<br>Jp ˆ(= m 0): . 20direct, c ˆ = 0verify . 05 ⇒ r ˆ = 0 . 010 Jp ˆ(= m 0): . 20direct, c ˆ = 0verify . 40 ⇒ sandbox r ˆ = 0 . 080 Jp ˆ(= m 0): . 20direct, c ˆ = 0verify . 90 ⇒ approve r ˆ = 0 . 180 kγm ( m ) 1.000 0.421 0.151.6 0.042.2<br>0.010 0.024 0.080 0.054 0.045 0.180 0.096 0.061 q ( m ) 0 0 0.04 0.65<br><!-- End of picture text -->

Figure 1. **CASEL routes every proposed tool call by consequence-weighted risk, not by uncertainty alone.** (a) Structured risk signals feed a controller that minimizes the per-mode cost _J_ ( _m_ ) over the modes feasible for the action’s reversibility class; dashed elements are not part of the main comparison; clarify is tested in Sec. VI-E, abstain is not exercised. (b) Worked example with the nominal parameters (inset): three calls with the same _p_ ˆ _t_ but different _c_ ˆ _t_ go to direct execution, sandboxing, and approval (lowest _J_ in bold); an uncertainty-only gate cannot tell them apart. 

DRAFT-RL scores multi-agent reasoning drafts during RL.<sup>[18]</sup> Domain-specific agents bring domain-specific benchmarks, such as SP-Bench with 102 spatial-proteomics tasks.<sup>[1]</sup> These works strengthen base policies but do not decide when an action needs extra evidence. 

**Clarification, abstention, and tool safety.** SAGE-Agent selects clarification questions by value of information;<sup>[9]</sup> AgentAbstain tests whether agents recognize when acting is unjustified.<sup>[10]</sup> AgentDojo targets untrusted tool outputs,<sup>[6]</sup> which multi-agent evidence checking can screen;<sup>[19]</sup> AgenTRIM enforces adaptive least privilege,<sup>[12]</sup> SABER safeguards mutating steps,<sup>[11]</sup> and Cordon stages multi-step effects as semantic transactions.<sup>[13]</sup> 

**Selective prediction and calibration.** Reject-option prediction formalizes an accuracy–coverage trade-off;<sup>[14],[15]</sup> temperature scaling calibrates scores,<sup>[20]</sup> and conformal risk control bounds monotone risks in expectation,<sup>[16]</sup> weaker than the high-probability bound used here. RAGScope routes retrievalaugmented answers to acceptance, review, or an expensive verifier with a cheap, cost-aware evidence gate,<sup>[21]</sup> a pass/escalate decision that CASEL generalizes to several interventions. 

Table 1 summarizes the comparison, including orthogonal layers: REFLEX calls a strong LLM when its fast decision layer is unsure,<sup>[22]</sup> and CA2I scores whole action sequences before execution.<sup>[23]</sup> CASEL’s product risk signal makes uncertainty-, consequence-, and mutation-only gates (evaluated in Sec. VI) special cases, and its heterogeneous interventions make the specialized mechanisms candidate branches rather than competitors. 

# III. PROBLEM FORMULATION 

At step _t_ , history _ht_ holds the user objective, observations, and prior actions, and a base policy proposes a tool call _at_ = ( _zt, θt_ ). Let _Ft ∈{_ 0 _,_ 1 _}_ indicate that _at_ is invalid relative to 

the task, policy, tool contract, or environment state. Its failure probability is 



<!-- Start of picture text -->
pt = P( Ft = 1  | ht, at, st ) , (1)<br><!-- End of picture text -->

where _st_ is the environment state when _at_ would be committed, observed only partially through _ht_ . With _ct ∈_ [0 _,_ 1] the normalized consequence if the action is wrong, the one-step expected harmful loss is _rt_ = _ptct_ . **Notation.** Unhatted _pt, ct, rt_ are true, unobserved quantities used in the analysis; hatted _p_ ˆ _t,_ ˆ _ct,_ ˆ _rt_ = _p_ ˆ _tc_ ˆ _t_ are run-time estimates, and Algorithm 1 and all routing rules use only these. _r_ ¯ _t_ is the score charged to the optional ledger. Throughout, including Figure 1 and Table 1, _λ_ and _µ_ weight compute and interaction cost, _ρt_ is the reversibility class, and _γm_ the residual multiplier of mode _m_ . 

Before commitment, a controller chooses _mt_ from _M_ = _{_ direct _,_ verify _,_ sandbox _,_ clarify _,_ approve _,_ abstain _}_ . Mode _m_ has residual failure probability _p_<sup>(</sup> _t_<sup>_m_)</sup> , compute cost _k_ ( _m_ ), and interaction cost _q_ ( _m_ ), and the ideal myopic decision is 



<!-- Start of picture text -->
m ∗ t = arg min p ( t m ) ct  +  λk ( m ) +  µq ( m ) , (2)<br>m∈Mt � �<br><!-- End of picture text -->

where _Mt_ removes infeasible modes. For committed actions, linearity of expectation gives, without independence, 



<!-- Start of picture text -->
E t =1 ctFt = � T t =1 ptct, (3)<br>�� T �<br><!-- End of picture text -->

so cumulative risk can be tracked by a ledger; Sec. VI tests whether budgeting it helps. 

# IV. CASEL RUNTIME 

# _A. Structured Risk Signals_ 

**Failure probability.** A raw score _ut_ is calibrated on a heldout split, _p_ ˆ _t_ = _f_ cal( _ut_ ), by isotonic regression or, given logits, temperature scaling;<sup>[20]</sup> thresholds and budgets are then read


<!-- page 3 -->

Table 1 

QUALITATIVE COMPARISON WITH ALTERNATIVE APPROACHES. _Step_ : ONE DECISION PER PROPOSED TOOL CALL. 

|Approach|Problem focus|Granularity|Risk signal|Intervention space|Relation to CASEL|
|---|---|---|---|---|---|
|SAGE-Agent<sup>[9]</sup><br>REFLEX<sup>[22]</sup>|Underspecified intent<br>Compute-efficient decisions|Question<br>Decision|Spec. vs. model unc.<br>Model confidence|Clarify<br>Call strong LLM|Implements clarify; triggered by _gt_<br>Orthogonal: chooses the decision maker|
|CA2I<sup>[23]</sup>|Pre-execution outcomes|Action sequence|Predicted return, risk|Select a plan|Orthogonal: admits whole plans|
|**CASEL**|Scrutiny before commit|Step|ˆ_pt_ˆ_ct, ρt, gt, dt_|Six modes,<br>cost-aware|—|



|**Algorithm 1** Consequence-aware selective execution|
|---|
|**Require:** offline: _f_cal, threshold ˆ_τ_ (Eq. (5)); at step _t_: _ht_, _at_, ledger _Ht−_1<br>1: ˆ_pt ←f_cal(_ut_); estimate ˆ_ct, ρt, gt, dt_; ˆ_rt ←_ˆ_pt_ˆ_ct_<br>2: **if** _gt > τg_ **return** (clarify, _Ht−_1)<br>3: **if** _dt > τd_ and refresh exists **return** (verify, _Ht−_1)<br>4: _Mt ←_FEASIBLEMODES(_ρt, at_); **if** ˆ_rt >_ ˆ_τ_: remove direct<br>5: _m_<sup>_∗_</sup>_←_arg min_m∈Mt γm_ˆ_rt_+_λk_(_m_) +_µq_(_m_)<br>6: _optional ledger:_ **if** _m_<sup>_∗_</sup>= direct and _Ht−_1 + ¯_rt > BH_: _m_<sup>_∗_</sup>_←_<br>ESCALATE(_ρt, Mt_)<br>7: **return**<br>�<br>_m_<sup>_∗_</sup>_, Ht−_1+ ¯_rt_**1**[_m_<sup>_∗_</sup>=direct]<br>�|





<!-- Start of picture text -->
as probabilities. ut can also draw on model internal states, as<br>MISO does for ranking models. [24]<br>Consequence. The controller computes<br>c ˆ t = clip� c base( zt )  M scope( θt, ht ) , 0 , 1� , (4)<br><!-- End of picture text -->

where _c_ base is a frozen per-tool severity from auditable metadata (write access, privilege, data sensitivity, value transfer) and _M_ scope _≥_ 0 a bounded magnitude factor (records, amount, rollback cost). 

**Reversibility.** The class _ρt_ (read, reversible, compensable, or irreversible) changes the feasible set _Mt_ ( _ρt_ ) rather than scaling _c_ ˆ _t_ . Direct, verify, clarify, and abstain are always feasible; sandbox requires a reversible mutation or a dry-run interface such as the forkable environments of Counterfactual Rollout Replay,<sup>[25]</sup> never for irreversible commitments; approve applies to compensable and irreversible actions. 

**Ambiguity and freshness.** _gt_ captures missing intent that more sampling cannot recover and routes to clarification; _dt_ captures stale evidence and triggers a re-read. For GUI agents, perception errors (object detection,<sup>[26]</sup> graphic understanding<sup>[27]</sup> ) propagate into _ut_ and _dt_ . 

# _B. Adaptive Intervention_ 

For feasible mode _m_ , let _γm_ ( _ξt_ ) _∈_ [0 _,_ 1] be the empirically estimated residual-error ratio, so _p_ ˆ<sup>(</sup> _t_<sup>_m_)</sup> = _γm_ ( _ξt_ )ˆ _pt_ , where _ξt_ collects the step features that determine how effective _m_ is (tool _zt_ , reversibility _ρt_ , available checker); the simulator uses one constant _γm_ per mode. Substituting into Eq. (2) gives _J_ ( _m_ ) = _γmr_ ˆ _t_ + _λk_ ( _m_ )+ _µq_ ( _m_ ). The expected harm reduction of _m_ is _Vm_ = (1 _− γm_ )ˆ _rt_ , so, ignoring interaction cost, _m_ beats direct execution when _Vm > λk_ ( _m_ ). 

# V. SELECTIVE-RISK CONTROL 

# _A. Direct-Execution Set and Finite-Sample Threshold_ 

Let _X_ be an action record, _S_ ( _X_ ) a scalar score, and _L_ ( _X_ ) _∈_ [0 _,_ 1] a harmful-loss label such as _cF_ . For threshold _τ_ , the direct-execution set is _Aτ_ = _{X_ : _S_ ( _X_ ) _≤ τ }_ , with selective 

risk _R_ ( _τ_ ) = E[ _L | X ∈ Aτ_ ] and coverage _C_ ( _τ_ ) = P( _X ∈ Aτ_ ). The objective is to maximize coverage subject to _R_ ( _τ_ ) _≤ ϵ_ . With _nτ_ calibration examples in _Aτ_ and empirical risk _R_<sup>ˆ</sup> <u>(</u> _τ_ <u>),</u> Hoeffding’s inequality gives _R_ ( _τ_ ) _≤ R_<sup>ˆ</sup> ( _τ_ ) + ~~�~~ ln(1 _/δ_ ) _/_ (2 _nτ_ ) with probability at least 1 _− δ_ for a fixed threshold. For a fixed grid of _K_ thresholds, a union bound yields the selection rule _R_ ˆ( _τ_ ) + ~~�~~ ln( _K/δ_ ) _/_ (2 _nτ_ ) _≤ ϵ._ (5) 

**Proposition 1** (Selective-risk validity) **.** _Fix the scorer S and a K-element grid before the calibration records are drawn, and let the records_ ( _Xi, Li_ ) _, Li ∈_ [0 _,_ 1] _, be i.i.d. from the deployment distribution of proposed actions and disjoint from the data used to fit f_ cal _. Then, with probability at least_ 1 _− δ, every grid threshold with nτ >_ 0 _that satisfies Eq._ (5) _has R_ ( _τ_ ) _≤ ϵ, the risk of executing all of Aτ directly._ 

_Proof._ Given the membership indicators, the _nτ_ losses in _Aτ_ are i.i.d. with mean _R_ ( _τ_ ), so Hoeffding’s bound holds for each _τ_ at level _δ/K_ ; a union bound covers the grid. 

**Scope.** (i) Actions in a trajectory are dependent (exchangeability is not enough), so calibration uses one record per trajectory. (ii) The bound covers _Aτ_ as a whole, not a furtherselected subset, which can concentrate high-loss actions. To cover the deployed policy, Eq. (5) is applied to the set that the complete policy _πτ_ executes directly, whose indicator is a fixed function of the trajectory prefix. 

# _B. Trajectory Ledger_ 

An optional ledger tracks _Ht_ =<sup>�</sup> _i≤t_<sup>_Dir_¯</sup><sup>_i_,where</sup><sup>_Di∈_</sup> _{_ 0 _,_ 1 _}_ indicates direct execution, and blocks direct execution that would exceed a budget _BH_ . **Proposition 2** (Budgeted expected harm) **.** _Let Gt be the information available when step t is routed, with Dt and r_ ¯ _t Gt-measurable. If_ E[ _ctFt | Gt_ ] _≤ r_ ¯ _t whenever Dt_ = 1 _and_ � _t_<sup>_Dtr_¯</sup><sup>_t≤BHalmostsurely,then_E[�</sup> _t_<sup>_DtctFt_]</sup><sup>_≤BH._</sup> _Proof._ By the tower property, E[<sup>�</sup> _t_<sup>_DtctFt_]</sup> = E[<sup>�</sup> _t_<sup>_Dt_E[</sup><sup>_ctFt| Gt_]]</sup><sup>_≤_E[�</sup> _t_<sup>_Dtr_¯</sup><sup>_t_]</sup><sup>_≤BH_.</sup> 

This is conditional accounting, not a reliability guarantee: _r_ ¯ _t_ must upper-bound the true conditional harm at every step, which a calibrated point estimate does not, and the residual harm of intervened actions is outside the ledger. 

**Runtime use.** Offline, the operator selects the largest grid _τ_ ˆ whose complete-policy direct set satisfies Eq. (5) ( _S_ = _r_ ˆ, _L_ = _cF_ ); online, a call runs directly only if _r_ ˆ _t ≤ τ_ ˆ and


<!-- page 4 -->

direct minimizes _J_ ( _m_ ). The main comparison uses _τ_ ˆ = _∞_ ; Sec. VI-E tests the threshold rule and the ledger. 

VI. CONTROLLED EVALUATION 

# _A. Protocol_ 

Each seed has an independent 40,000-action calibration split and 6,000 test trajectories of 20 actions (120,000 test actions). Actions are read-only (58%), reversible (28%), or irreversible (14%). True failure probabilities come from class-dependent Beta distributions with a trajectory-level difficulty perturbation, creating within-task dependence; consequences lie mainly in [0 _._ 02 _,_ 0 _._ 20], [0 _._ 15 _,_ 0 _._ 70], and [0 _._ 55 _,_ 1] for the three classes. The controller sees a noisy raw failure score, isotonic-calibrated on the calibration split, and a noisy consequence estimate. 

The simulator instantiates direct, verify, sandbox, and approve with residual multipliers _γm_ of 1 _._ 00, 0 _._ 42, 0 _._ 15, and 0 _._ 04, compute costs _k_ ( _m_ ) of 0, 1 _._ 0, 1 _._ 6, and 2 _._ 2, and interaction costs _q_ ( _m_ ) of 0, 0, 0 _._ 04, and 0 _._ 65. These are assumed constants. Direct and verify are always feasible, sandbox only for reversible mutations, and approve only for irreversible ones with _c_ ˆ _t ≥_ 0 _._ 55. Clarify is exercised only in the ambiguity stress family (Sec. VI-E); abstain and the staleness branch ( _dt_ , _τd_ ) are not exercised. The cost weights keep _λ_ : _µ_ = 0 _._ 02 : 0 _._ 015; a common factor sets the operating point. 

**Comparators.** _Verify-only gates_ (the usual scalar gates) verify the actions ranked highest by _p_ ˆ or _c_ ˆ. _Menu gates_ rank by _p_ ˆ, _c_ ˆ, or _p_ ˆ _c_ ˆ and give the top-ranked actions their strongest feasible intervention (sandbox if reversible, approve if irreversible, otherwise verify), so they have CASEL’s menu. CASEL minimizes _J_ ( _m_ ). Ablations: CASEL-NoRev (verify only), CASEL+Budget ( _λ_ = 0 _._ 02 with the ledger, _BH_ = 0 _._ 08, _r_ ¯ _t_ = _p_ ˆ _tc_ ˆ _t_ ), and CASEL-Uncal (raw score). All of these are matched to one compute cost, 0 _._ 486 (for CASEL, cost-weight factor 0 _._ 58 _±_ 0 _._ 02), using scores but no outcome labels; Base, Always-Verify, and Mutation-Gated are fixed policies. 

**Metrics.** An action routed to _m_ fails with probability _γmpt_ , using one uniform draw per action shared by all methods (paired outcomes). _Task success_ is the fraction of trajectories with no failed action; the _harmful side-effect rate_ (HSR) is the fraction with at least one failed action of true consequence _ct ≥_ 0 _._ 45; _mean normalized harm_ (MNH) is the mean over trajectories of<sup>�20</sup> _t_ =1<sup>_ctFt_.Directcoverageistheshareof</sup> directly executed actions, cost the mean _k_ ( _m_ ) per action, and approvals the share of actions sent to human approval. Results average 20 seeds. 

# _B. Main Results_ 

Isotonic calibration lowers mean ECE by 94 _._ 5% and Brier score by 9 _._ 3% (Figure 2). 

**Main result.** With the same menu and the same cost, CASEL lowers HSR from 14 _._ 75% for UncertaintyMenu to 7 _._ 02% (paired difference _−_ 7 _._ 73 points, 95% CI [ _−_ 7 _._ 87 _, −_ 7 _._ 60]) and MNH from 0 _._ 184 to 0 _._ 123; task success is 1 _._ 79 points lower, because generic success weights every error equally (Table 2). 



<!-- Start of picture text -->
(a) ECE  ↓ (b) Brier score  ↓<br>− 94.5% − 9.3%<br>0.0390 0.075 0.0641<br>0.04 0.0581<br>0.050<br>0.02<br>0.025<br>0.0021<br>0.00 0.000<br>Raw score Isotonic Raw score Isotonic<br><!-- End of picture text -->

Figure 2. **Isotonic calibration turns the raw failure score into a usable probability.** (a) ECE and (b) Brier score of the raw score and of the calibrated _p_ ˆ on test actions. Bars: means over 20 seeds with 95% CIs; lines: paired per-seed values. 

**Simple consequence-aware gates are strong.** Risk-Menu has slightly lower HSR (5 _._ 82%) and MNH (0 _._ 120) than CASEL, and Consequence-Menu the lowest HSR (4 _._ 38%) with higher MNH (0 _._ 136) and the lowest task success. Both send more actions to human approval: 12 _._ 6% and 13 _._ 8% versus 8 _._ 7%. Matched on total cost _λk_ + _µq_ instead, Risk-Menu has HSR 6 _._ 22%, MNH 0 _._ 126, and task success 45 _._ 60% (CASEL: 7 _._ 02%, 0 _._ 123, 47 _._ 01%). The per-mode cost _J_ ( _m_ ) therefore does not reduce harm beyond a product-score gate; it reaches similar harm with about 30% fewer approvals and slightly higher task success, across the cost range (Figure 4(a,b)). 

# _C. Risk–Coverage Quality_ 

Figure 3 isolates score quality from the intervention model by ranking candidate direct actions by _p_ ˆ, _c_ ˆ, or _p_ ˆ _c_ ˆ. Averaged over coverage 0 _._ 1–1 _._ 0, selective-risk AUC is 0 _._ 01050, 0 _._ 00593, and 0 _._ 00533, respectively: the product reduces AUC by 49 _._ 2% relative to uncertainty and by 10 _._ 1% relative to consequence. 

# _D. Ablations_ 

**Reversibility.** Restricting CASEL to verification raises HSR from 7 _._ 02% to 15 _._ 53% and MNH to 0 _._ 194 at the same cost: matching the intervention to commitment semantics accounts for most of the gain. **Trajectory budget.** CASEL+Budget has HSR 11 _._ 82% and MNH 0 _._ 167 at the same compute cost and is dominated along its whole _BH_ sweep (Figure 4(a)): a full ledger escalates low-risk actions late in a trajectory, where expected harm is small. In the harm–approval plane it lies on CASEL’s curve (Figure 4(b)): it trades compute for approvals rather than reducing harm, so the default configuration omits the ledger. **Calibration.** Using the raw score raises HSR by 1 _._ 20 points and MNH by 0 _._ 005 and raises task success by 0 _._ 82 points. All ten differences in Figure 4(c) are significant (Holm-corrected _p <_ 10<sup>_−_4</sup> ). 

# _E. Checks of the Guarantees and Stress Tests_ 

**Threshold rule.** Per seed we keep one random step from each of 40,000 fresh calibration trajectories (i.i.d. records) and apply Eq. (5) to the deployed policy (20-point grid, _δ_ = 0 _._ 1). Sweeping _ϵ_ over 0 _._ 006–0 _._ 016: for _ϵ ≥_ 0 _._ 015 the rule certifies the unrestricted policy (coverage 69 _._ 1%, true selective risk 0 _._ 0048); at _ϵ_ = 0 _._ 014 it binds in all 20 seeds ( _τ_ ˆ = 0 _._ 014, coverage 62 _._ 3%, risk 0 _._ 0035, cost 0 _._ 553); below, the Hoeffding slack ( _≈_ 0 _._ 010) blocks certification. With 160 _,_ 000 records the


<!-- page 5 -->

Table 2 

CONTROLLED EVALUATION OVER 20 SEEDS (TASK SUCCESS AND HSR: MEAN _±_ ONE STANDARD DEVIATION). ALL METHODS BELOW MUTATION-GATED HAVE COMPUTE COST 0 _._ 486. MENU: INTERVENTIONS A METHOD MAY USE (FULL = VERIFY, SANDBOX, APPROVE). 

|Method (ranking)<br>Menu|Task Success _↑_|HSR _↓_|MNH _↓_|Direct Cov.|Cost||Approvals|_↓_||
|---|---|---|---|---|---|---|---|---|---|
|Base<br>—<br><br>|29_._48_±_0_._49<br>|32_._76_±_0_._70<br>|0.428<br>|100.0%<br>|0.000<br>||0.0%<br>|||
|Always-Verify<br>verify<br>Mutation-Gated<br>verify<br><br>|58_._81_±_0_._71<br>43_._78_±_0_._62<br>|15_._47_±_0_._53<br>15_._47_±_0_._53<br>|0.180<br>0.196<br>|0.0%<br>58.0%<br>|1.000<br>0.420<br>||0.0%<br>0.0%<br>|||
|Uncertainty gate (ˆ_p_)<br>verify<br>Consequence gate (ˆ_c_)<br>verify|47_._78_±_0_._56<br>45_._10_±_0_._63|19_._25_±_0_._57<br>15_._47_±_0_._53|0.233<br>0.195|51.4%<br>51.4%|0.486<br>0.486||0.0%<br>0.0%|||
|Uncertainty-Menu (ˆ_p_)<br>full<br>|48_._79_±_0_._63<br>|14_._75_±_0_._41<br>|0.184<br>|66.9%|0.486<br>||6.9%|||
|Consequence-Menu (ˆ_c_)<br>full<br><br>|43_._54_±_0_._50<br>|4_._38_±_0_._29<br>|0.136<br>|74.7%<br>|0.486<br>||13.8%<br>|||
|Risk-Menu (ˆ_p_ˆ_c_)<br>full<br><br>|46_._26_±_0_._50<br>|5_._82_±_0_._35<br>|0.120|74.2%<br>|0.486<br>||12.6%|||
|**CASEL** (_J_(_m_))<br>full|47_._01_±_0_._56|7_._02_±_0_._30|0.123|69.1%|0.486||8.7%|||
|CASEL-NoRev<br>verify|46_._56_±_0_._54|15_._53_±_0_._52|0.194|51.4%|0.486||0.0%|||
|CASEL+Budget<br>full|45_._82_±_0_._64|11_._82_±_0_._54|0.167|63.9%|0.486||4.3%|||
|CASEL-Uncal<br>full|47_._83_±_0_._50|8_._22_±_0_._36|0.129|69.3%|0.486||8.4%|||
|−𝟥)<br>**(a) Risk**−**coverage curves**|𝟣𝟢−𝟥)<br>**(**|**b) Paired impro**|**vement**|**over**̂_𝘱_|𝟣𝟢−𝟥)||**(c) Area**|**under cu**|**rve**|
|0<br>10<br>20<br>elective risk (×𝟣𝟢<br>~~Uncertainty~~̂_~~𝘱~~_<br>Consequencê_𝘤_<br>CASEL risk̂_𝘱_̂_𝘤_<br>**−67%**<br>**at 0.65**|−10<br>−5<br>0<br>k vs.̂_𝘱_ranking (×|pea|kgain −7.<br>Conseque<br>CASEL ri|9 at 0.65<br>ncê_𝘤_<br>sk̂_𝘱_̂_𝘤_|n selective risk (×|0<br>5<br>10|0.01050|0.00593<br>−**43.5%**|0.00533<br>−**49.2%**|
|0.2<br>0.4<br>0.6<br>0.8<br><br>Direct-execution coverage<br><br>S|1.0<br><br>ris|0.2<br>0.4<br>Direct-exe|0.6<br>cution co|0.8<br>1.0<br>verage|Mea||̂_𝘱_|_𝘤_|_𝘱_̂_𝘤_|



Figure 3. **Ranking actions by** _p_ ˆ _c_ ˆ **halves the selective-risk AUC of uncertainty-only ranking.** (a) Selective risk (mean consequence-weighted loss of directly executed actions) versus coverage when actions are admitted in increasing order of _p_ ˆ, _c_ ˆ, or _p_ ˆ _c_ ˆ; the arrow marks the largest gap. (b) Per-seed paired difference from the _p_ ˆ ranking. (c) Area under each curve (average selective risk over coverage 0 _._ 1–1 _._ 0); dots are seeds. Bands and whiskers are 95% CIs over 20 seeds. 



<!-- Start of picture text -->
Uncertainty, verify only Uncertainty-Menu Consequence-Menu Risk-Menu CASEL+Budget ( 𝘉𝘏  sweep) CASEL (ours)<br>(a) Harm vs. compute cost (b) Harm vs. human approvals (c) Paired effects at cost 0.486<br>common cost vs. Uncert.-Menu −7.7*** −1.8***<br>0.486<br>20 20 vs. Risk-Menu +1.2*** +0.8***<br>+2.6***<br>vs. Conseq.-Menu +3.5***<br>10 10 same cost 0.486: −4.8***<br>vs. +Budget +1.2***<br>12.6%  →  8.7%<br>approvals vs. NoRev −8.5*** +0.4***<br>0 0<br>0.2 0.4 0.6 0 5 10 −10 0 10<br>Normalized compute cost Actions sent to human approval (%) CASEL − comparator (pp, 95% CI)<br>HSR (%)<br>Harmful side-effect rate, HSR (%)<br><!-- End of picture text -->

Figure 4. **With equal menus, consequence-aware allocation has far lower harm than uncertainty ranking at every cost; CASEL matches a risk-ranked gate with fewer approvals, and the trajectory budget does not help.** (a) HSR versus compute cost; the band marks the common cost 0 _._ 486. (b) HSR versus the share of actions sent to human approval. (c) Paired differences at cost 0 _._ 486, CASEL minus comparator, in HSR (red diamonds) and task success (blue dots), in points;<sup>_∗∗∗_</sup> : _p <_ 0 _._ 001, two-sided paired _t_ -test over the 20 seeds, Holm-corrected over the ten tests. Bands and bars are 95% CIs. 

rule binds at _ϵ_ = 0 _._ 009 (coverage 63 _._ 1%) and certifies 8 of 20 seeds at 0 _._ 008 (coverage 52 _._ 6%). True selective risk never exceeded _ϵ_ . 

**Ledger.** Proposition 2 is therefore an analysis of when budgeting is sound, not a guarantee of the evaluated system: for CASEL+Budget its premise fails on 54% of directly executed steps ( _ptct > r_ ¯ _t_ ). Realized direct-execution harm exceeds the budget by 10% at _BH_ = 0 _._ 04 and 2% at 0 _._ 08, and residual harm from intervened actions (0 _._ 086, about half of MNH) is not covered. 

**Ambiguity.** In 10% of test actions intent is missing: with 

probability _at ∼ U_ (0 _._ 2 _,_ 0 _._ 6) a correctly executed call is still wrong. Verify and sandbox leave this error, approval halves it, and clarify ( _k_ = 0 _._ 2, _q_ = 0 _._ 3) removes 95% before _J_ ( _m_ ) routes the call. With _gt_ = _at_ + _N_ (0 _,_ 0 _._ 08<sup>2</sup> ) and _τg_ = 0 _._ 2, CASEL clarifies 9 _._ 8% of actions (precision 94%, recall 92%) and lowers HSR from 19 _._ 1% to 8 _._ 4%; at equal compute cost, CASEL without _gt_ has 18 _._ 5% and Risk-Menu 16 _._ 4% (7 _._ 8– 12 _._ 4% for _τg ∈_ [0 _._ 1 _,_ 0 _._ 4]). 

**Misspecification.** Halving _p_ ˆ, _c_ ˆ, or every intervention’s effectiveness raises CASEL’s HSR to 16 _._ 6%, 18 _._ 8%, and 21 _._ 0%, still below Uncertainty-Menu at the same cost (23 _._ 4%,


<!-- page 6 -->

25 _._ 9%, 24 _._ 3%) and within 0 _._ 6 points of Risk-Menu: the ordering is stable, but absolute harm depends on _γm_ and unbiased estimates. 

# VII. DEPLOYMENT CONSIDERATIONS 

**Adaptation and drift.** Only the signals in _c_ base, _M_ scope and the preferred high-risk modes are domain-specific; in optical networks, for instance, alarm correlation and root-alarm detection<sup>[28]</sup> show how far a fault propagates and can inform the scope factor. _λ, µ_ are read off the deployment’s own cost– harm frontier (Figure 4), and _γm_ is estimated conservatively on trajectory-disjoint traces. Such gates must be recalibrated per domain: RAGScope’s gate transfers poorly across sources but recovers with 100–200 target labels.<sup>[21]</sup> When logged calibration or residual-risk drift leaves its tolerance region, the controller re-selects _τ_ ˆ, re-estimates _γm_ , or lowers _λ_ and _µ_ . **Integration with existing AI tooling.** CASEL needs only an interception point for tool calls (an MCP proxy, a pre-execution hook, or a policy engine) and no retraining. In network operations, robotic test-automation platforms for optical transport and commercial O-RUs<sup>[29],[30]</sup> automate validation runs that can back the verify and sandbox branches. Existing tools implement the branches: an LLM judge or an execution-grounded reward model such as BoostAPR’s repair assessors<sup>[31]</sup> for verify, Cordon for sandbox, an approval service for approve, and SAGE-Agent for clarify.<sup>[9],[13]</sup> 

# VIII. DISCUSSION AND LIMITATIONS 

CASEL is an allocation policy, not a safety guarantee; the simulation ranks allocation rules under assumed intervention effectiveness and costs, not their effect in deployment. **Roadmap.** Planned (not yet run) evaluations estimate _γm_ from real verifier and rollback outcomes on _τ_<sup>2</sup> -Bench, WebArena, AgentDojo, AgentAbstain, and ToolEmu<sup>[3],[5],[6],[10],[32]</sup> , and on domain benchmarks such as SP-Bench,<sup>[1]</sup> where consequence rubrics must be domainspecific. CASEL was not compared experimentally with REFLEX<sup>[22]</sup> or CA2I,<sup>[23]</sup> which act at other levels. 

# IX. CONCLUSION 

In a controlled simulation with equal menus and costs, allocating scrutiny by consequence-weighted risk and reversibility roughly halves severe side effects relative to uncertainty ranking; a per-mode cost matches a risk-ranked gate with fewer approvals, and a trajectory budget did not help.
