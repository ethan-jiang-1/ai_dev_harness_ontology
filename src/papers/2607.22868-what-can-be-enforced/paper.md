> PDF 文本抽取（pymupdf），保留 `<!-- page N -->`；表格/公式可能有版式噪声，引用前回 PDF 核。

<!-- page 1 -->
What Can Be Enforced? A Theory of Certified Runtime Safety for Tool-Using
Agents
Shawn Ray
Carnegie Mellon University
shawnray@cmu.edu
Code and cached scores:
https://github.com/shawnray-research/certified-agent-guardrails
Abstract
Runtime guardrails act before irreversible tool calls, but their
guarantees depend on what policy state is representable, what
a judge observes, and whether intervention changes future
behavior. We separate three questions. First, relative to fixed
oracle predicates, a deterministic gate enforces exactly the
nonempty safety policies whose good prefixes its register
model recognizes; policy nontriviality is undecidable with
two decrementable counters but in pspace for a separable
monotone fragment. Second, under a fixed exogenous law,
Neyman–Pearson gives the exact false-block/miss frontier and
conformal calibration gives a finite-sample marginal certifi-
cate, possibly via block-all. Third, once blocking changes fu-
ture proposals, static scores and ungated trajectories need not
identify the closed-loop frontier; a specified finite controlled
model instead yields an occupancy program. Bounded repre-
sentation attacks add a robustness margin, so benign calibra-
tion alone does not transfer. Experiments target these distinc-
tions through static diagnostics, controlled-model enumera-
tion, representation rewrites, and paired closed-loop reruns.
1
Introduction
Tool-using language-model agents increasingly act in the
world: they send email, move money, edit files, and call ex-
ternal APIs. A large and fast-growing body of work equips
such agents with runtime guardrails, monitors that inspect
a proposed action and block, rewrite, or escalate it before it
executes (Wang, Poskitt, and Sun 2026; Wang et al. 2025; Mi-
culicich et al. 2025; Doula, Mühlhäuser, and Sanchez Guinea
2025; Kamath et al. 2025; Wu et al. 2026). These are mech-
anisms; we ask the prior foundational question: which safety
policies can a runtime guardrail enforce at all, and at what
utility price?
For programs, execution monitors enforce safety proper-
ties (Schneider 2000), while edit automata gain power by sup-
pressing and reinserting actions (Ligatti, Bauer, and Walker
2005). Agent guardrails stress four assumptions behind this
picture: policy predicates may be judged fallibly; external ef-
fects may be irreversible; actions carry unbounded data; and
untrusted content can steer proposals (Greshake et al. 2023).
These departures require different mathematical regimes. We
do not claim that one theorem removes all four assumptions
simultaneously; each result below states its oracle, stochas-
tic, sequential, or adversarial scope. Throughout, “certified”
means either streamwise enforcement relative to fixed oracle
predicates or a marginal risk bound under explicit stochastic
assumptions, not universal semantic safety.
Example 1 (Running example: an email/payments as-
sistant). Throughout we follow an assistant acting for
a user through tools such as send_email(to, body) and
transfer(to, amount), under three policies: (P1) never email
a body containing PII to a recipient not on the approved
list; (P2) never let cumulative transfer to any recipient ex-
ceed cap c in a trusted clock-supplied day bucket; (P3) after
the user revokes access, send nothing further. P2 and P3 are
data-carrying properties an oracle can check; P1 rests on the
semantic predicate “contains PII,” which only a fallible judge
evaluates.
Attribution and paper-specific delta.
We import rather
than claim classical enforcement, Neyman–Pearson optimal-
ity, CPOMDP occupancy methods, conformal risk control,
and two-counter undecidability. Our contribution is their
regime-correct composition for irreversible semantic gates:
an exogenous ROC need not identify the endogenous fron-
tier, so ungated evidence need not suffice over the stated
model class; exact cap saturation plus a one-witness reduc-
tion also makes a useful keyed-counter fragment analyzable.
The supplement gives full proofs and executable audits.
Results and evidence.
• Oracle and symbolic boundaries. Relative to avail-
able oracle predicate bits, deterministic pre-execution
gates enforce exactly the nonempty register-representable
safety policies (T1), strictly below edit automata. Non-
triviality is undecidable with two decrementable counters
but in pspace for a separable monotone fragment covering
caps and revocation (T3).
• Statistical and sequential boundaries. For a fixed ex-
ogenous decision, Neyman–Pearson gives the exact false-
block/miss ROC frontier. For a specified finite model
where blocking changes future observations, a belief-state
occupancy program gives the closed-loop frontier. Static
scores and ungated trajectories need not identify it with-
out the controlled response (T2).
• Calibration and attack boundaries. Label-conditional
arXiv:2607.22868v1  [cs.AI]  24 Jul 2026

<!-- page 2 -->
exchangeability yields a finite-sample marginal confor-
mal certificate, possibly by the vacuous block-all rule. A
bounded attack on the judge-visible representation instead
incurs a robustness-margin price; this is distributional and
is not universal semantic soundness.
• Evidence with uncertainty. A 23-judge static diagnostic,
exact finite controlled example, common-budget rewrite,
and paired end-to-end reruns separately expose calibra-
tion cost, policy-class gaps, representation attack, and
gate-induced feedback (Figure 1).
2
Related Work
Classical runtime enforcement.
Execution monitors en-
force only safety properties (Schneider 2000; Hamlen, Mor-
risett, and Schneider 2006); edit automata enlarge the class
via suppression and reinsertion (Ligatti, Bauer, and Walker
2005); shallow-history monitors (Fong 2004) are close to
our finite-memory gate. Later work relaxes single classi-
cal assumptions: Basin et al. (2013) separate controllable
from merely observable actions, and predictive enforcement
acts before the trace completes (Pinisetty et al. 2017) with-
out buffering, both close analogs of our pre-execution, no-
truncation gate; first-order monitoring (Basin et al. 2015;
Bauer, Leucker, and Schallhart 2011) handles data-carrying
policies such as P2–P3. Enforcement is a discipline distinct
from verification (Falcone, Fernandez, and Mounier 2012);
register automata (Kaminski and Francez 1994) supply the
infinite-alphabet machinery T3 turns on. Class-memory au-
tomata and data languages locate stronger decidable for-
malisms beyond our deliberately separable fragment (Bo-
janczyk et al. 2006). Mandatory-results automata already
model actions and their returned results (Ligatti and Reddy
2010); parametric monitoring dispatches data traces to per-
binding monitors (Roşu and Chen 2012); and integer-register
monitors study unbounded monitor memory (Ferrère, Hen-
zinger, and Saraç 2018). Our keyed-counter class is a sepa-
rable specialization: the claim is its exact cap-saturation and
one-witness analysis, not that per-key monitoring or counters
are new.
Statistical decisions and sequential control.
Reject-
option classification begins with Chow’s Bayes rule (Chow
1970); modern selective classification studies risk–coverage
tradeoffs (El-Yaniv and Wiener 2010; Geifman and El-Yaniv
2017). Our exogenous result instead fixes a tolerated miss
rate and uses Neyman–Pearson optimality, while Blackwell’s
order formalizes when richer observations can improve a
specific operating point (Blackwell 1953). Once interven-
tions alter trajectories, the appropriate standard machinery
is constrained MDP and belief-state POMDP control (Alt-
man 1999; Kaelbling, Littman, and Cassandra 1998), not
a static ROC. CPOMDP work gives a deterministic-policy
piecewise-linear update (Isom, Meyn, and Braatz 2008), ran-
domized exact and point-based methods (Kim et al. 2011),
belief-state occupancy LPs (Poupart et al. 2015), and a finite-
horizon policy-column LP with support-two optima for one
constraint (Walraven and Spaan 2018). Theorem 3 special-
izes this standard machinery to guardrails; its delta is first-
entry safety versus compliant-block cost, the condition recov-
ering a static ROC, and feedback non-identifiability. Episode
safety is a joint chance constraint (Prékopa 1995); our ex-
pected first-entry cost represents it exactly in the absorbing-
unsafe model, while the per-step certificate uses a union
bound.
Guardrails for LLM agents.
Recent systems enforce rules
at runtime: AgentSpec’s DSL (Wang, Poskitt, and Sun 2026),
probabilistic model checking with PAC bounds (Wang et al.
2025), verified code generation (Miculicich et al. 2025),
conformal prediction for navigation (Doula, Mühlhäuser,
and Sanchez Guinea 2025), temporal-constraint enforcement
via SMT and constrained generation (Kamath et al. 2025),
probabilistic-logic policy reasoning (Chen, Kang, and Li
2025), LLM-generated guard code (Xiang et al. 2024), adap-
tive lifelong guardrails (Luo et al. 2025), DSL privilege con-
trol with an SMT backend (Shi et al. 2025), programmable-
rails and tool-call interceptors that emit an allow/block ver-
dict before execution (Rebedea et al. 2023; Yang 2026),
and fine-tuned diagnostic guardrail judges (Liu et al. 2026).
These are mechanisms: each fixes a policy language and a
checker and reports empirical violation rates, instantiating
the “guaranteed-safe AI” program (Dalrymple et al. 2024).
Each lands in a regime of our characterization: an interceptor
is a block/allow gate (Def. 4); for a fixed exogenous exper-
iment, a fine-tuned guardrail is a fallible judge bounded by
its ROC (Thm. 2); the temporal-constraint work is a sub gate
in the T1 regime, and Wang et al. (2025) is predictive rather
than pre-execution (Thm. 1’s class is unchanged). What they
do not set out to give, and what we add, is a set of ex-
plicit enforceability, information, feedback, and decidability
boundaries. Feedback-driven systems such as ToolSafe and
TRIAD feed guard outputs back into planning (Mou et al.
2026; Sun et al. 2026); in our taxonomy these are controlled
processes because intervention changes later proposals.
Shielding and agent security.
A shield is a pre-execution
gate over an actuated learned policy (Alshiekh et al. 2018;
Bloem et al. 2015), extended to stochastic dynamics by prob-
abilistic shields (Jansen et al. 2020); Def. 4 is a shield in this
lineage. Our results isolate several differences: shields as-
sume an oracle-checkable state predicate and a finite/MDP
abstraction, whereas our judge is a fallible semantic clas-
sifier (giving the ROC frontier and certificate of §5 in the
exogenous regime) and our actions carry unbounded data
(giving the decidability boundary of §6). On the security
side, CaMeL (Debenedetti et al. 2025) and Constitutional
Classifiers (Sharma et al. 2025) raise the robustness margin
η(ρ) of Thm. 5, architecturally and inside the judge respec-
tively; closest in spirit is AI Control (Greenblatt et al. 2024), a
trusted monitor with a threshold and budget over an untrusted
model (our judge-plus-gate under an adversarial source),
whose game form (Griffin et al. 2024) numerically com-
putes safety/usefulness frontiers from the monitor’s ROC,
as do concurrent operating-point analyses of agent guards
(Hua et al. 2025; Turan 2026) (the latter independently finds
only moderate risk-annotation agreement); those optimize a
point, whereas we separate the exact one-step frontier from a
specified finite-model endogenous frontier and add symbolic
boundaries. Unlike alignment-impossibility results about a

<!-- page 3 -->
model’s expressivity (Wolf et al. 2024), Thm. 5 is about the
gate, whose calibration collapses under a bounded adversary.
Conformal prediction.
Conformal prediction has been
paired with fallible learned monitors before (Doula,
Mühlhäuser, and Sanchez Guinea 2025; Cairoli, Paoletti,
and Bortolussi 2023), and Ren et al. (2023) calibrate an
LLM agent’s action uncertainty to decide when to ask for
help; we import calibration rather than reinvent it. Our cer-
tificate is a marginal per-violation statement under label-
conditional exchangeability and can be vacuous; Theorem 5
separately quantifies representation-space shift, empirically
documented for LLM judges under injection (Maloyan and
Namiot 2025).
Paired inference.
Because all judges score the same items,
independent-sample uncertainty is inappropriate. We use De-
Long influence functions for correlated AUCs (DeLong, De-
Long, and Clarke-Pearson 1988), simultaneous max-T inter-
vals, and Holm-adjusted tests (Holm 1979); equivalence is
reported only when the entire familywise interval lies inside
the predeclared margin.
3
The Enforcement Model
Definition 1 (Actions, data, traces). Fix finite action types
Σ with arities ar : Σ →N and a data domain D (pos-
sibly infinite; with equality, optionally a linear order). An
action is a = (σ, ¯d) with ¯d ∈Dar(σ). The alphabet
A = S
σ{σ} × Dar(σ) is infinite when D is. Traces are
words in A∗(finite) or Aω (infinite); ⪯is the prefix order.
A distinguished no-op ⊥∈A has no external effect, and the
external-effect projection ext : A∞→(A \ {⊥})∞deletes
every ⊥. Policies here are safety properties (Def. 2), so we
score a committed trace c by the bad prefixes of its effect
trace: c is safe for P iff no finite prefix of ext(c) is a bad
prefix of P. This coincides with ext(c) ∈P when ext(c)
is infinite (safety closure, Lemma in App. A) and stays well
typed when the gate eventually blocks forever and ext(c) is
finite. Committing ⊥(blocking) therefore never adds a bad
prefix: from any good effect prefix, it is a safe default for a
nonempty safety P, with no extra no-op-neutrality assump-
tion.
This no-op is an external-effect abstraction: T1 ignores
a block’s latency, visibility, memory updates, retries, and
counter side effects. When those consequences change later
proposals, they belong in the controlled transition kernel of
Definition 5, not the T1 projection.
Definition 2 (Safety, register representation). A policy is
a set P ⊆Aω. P is safety (Alpern and Schneider 1987)
iff every x /∈P has a finite bad prefix: ∃n ∀y : x≤ny /∈
P. Let Bad(P) ⊆A∗be the minimal bad prefixes and
Good(P) = A∗\ Bad(P)A∗the (prefix-closed) good pre-
fixes. Our policy-automaton model is a keyed-counter reg-
ister automaton (a custom class): it extends the register
automaton of Kaminski and Francez (1994) with a finite-
support map of per-key counters. Concretely it has finite
control, a bounded number of data registers over D, per-key
counters over N (unattached keys default to 0), and, when de-
clared, one fixed finite vector of global N-counters. Numeric
counters are distinct from data registers; transitions choose
their successor and updates by T -guards on the current ac-
tion’s data, the registers, and the counters, with absorbing
bad states. Counter values are unbounded in general; the
guard theory T sets expressivity (the separable, key-local,
constant-guard monotone fragment T0 is decidable; T ∗with
two decrementable zero-test counters is undecidable; §6). At
any finite time only finitely many keys are active, so the rec-
ognizer stays deterministic and finitely represented. RA[T ] is
the class of policies whose good-prefix language such an au-
tomaton recognizes; P is T -representable safety if it is safety
and in RA[T ]. When guards may query a fixed finite vector
of externally supplied predicate bits Π, we write RA[T ; Π]
and say representable relative to Π; this interface does not
grant access to any other semantic fact.
For instance, P2 of Example 1 is recognized with
one monotone counter per composite key (k, w), testing
spentk,w +v ≤c on a transfer(k, v, w) whose day bucket w
is attached by a trusted clock adapter; its nontriviality needs
to track only a single witness key (Theorem 7), so its mono-
tone counters saturate for analysis even when unboundedly
many recipients are active at runtime. The class is not tuned
to the theorem: registers alone cannot count and unrestricted
counters are undecidable (§6); monotone per-key counters
are the middle ground deployed caps, quotas, and rate limits
use.
Definition 3 (Predicates, judge, error rates). Guards are
boolean combinations of T -constraints on data and se-
mantic predicates πi : (A \ {⊥})∗× A →{0, 1} eval-
uated on the committed effect history (ground truth). A
judge ˆπθ
i (τ, a) = ⊮[si(τ, a) ≥θi] approximates πi via a
score si; under a distribution P on (τ, a) its false-alarm
and miss rates are αi(θi) = P[ˆπi = 1 | πi = 0] and
βi(θi) = P[ˆπi = 0 | πi = 1]. The oracle case is αi = βi = 0
for the fixed available vector Π = (π1, . . . , πm). The ROC
frontier roc(β) is the least false-alarm rate attainable at miss
rate β by any randomized decision measurable with respect
to si, a nonincreasing convex function. It is the lower en-
velope over all score-measurable tests, not only thresholds:
when si is monotone in the violation likelihood ratio this
envelope is traced by thresholds on si (the case we sweep
empirically), and in general by likelihood-ratio tests on si.
Definition 4 (Gate, soundness, transparency, utility). A gate
is a computable map g : (A \ {⊥})∗× A × [0, 1]m →
Dec (the m judge scores; the oracle case of T1 restricts the
last argument to {0, 1}m), Dec = {allow, block, sub(a′)},
deciding before the (irreversible) action commits from the
committed effect history (blocks leave no effect to condition
on), the proposed action, and the scores. Against a proposal
stream it induces a committed trace (allow keeps a; block
commits ⊥; sub commits a′). g is sound if for every stream
the committed trace is safe for P (Def. 1: no finite prefix of
its effect trace is a bad prefix of P); transparent if for every
stream whose proposed effect trace lies in P the committed
effect prefix equals the proposed effect prefix at every step
(prefixwise, so no action of a compliant trace is ever blocked
or altered); effective if both. For horizon H and distribution
P, an episode is unsafe if some committed effect prefix is a

<!-- page 4 -->
bad prefix of P, and the utility loss is U(g) = P[g alters at |
the proposed at is compliant].
4
T1: The Expressiveness Boundary (Oracle
Enforceability)
Call g a (T ; Π)-gate if its decisions are computed by a deter-
ministic register automaton with T -guards and queries to the
fixed predicate bits Π over the committed effect history (the
natural policy-specification class; general computable gates
are in Rem. 1). The substantive restriction below is seman-
tic: irreversibility plus prefixwise transparency forces safety
and decidable good prefixes. The automaton correspondence
then identifies the fragment left by the chosen implementa-
tion class.
Theorem 1 (Oracle characterization). Fix the available ora-
cle interface Π and a nonempty policy P. Then P is effectively
enforceable by a deterministic (T ; Π)-gate if and only if it is
safety and Good(P) ∈RA[T ; Π]. Enforcement is witnessed
by simulating that recognizer and refusing exactly the one-
step extensions it rejects; each step evaluates one enabled
transition in the given guard theory.
Sketch. (⇐) simulate the automaton and block any action
whose transition would enter a bad state; soundness holds
because a safety property is left only through a bad prefix,
and transparency because a compliant stream never targets a
bad state. (⇒) a T -gate decides from finite history and oracle
predicate values, so if P were not safety, transparency on
compliant prefixes approaching a doomed limit trace would
force the gate to allow that trace, breaking soundness. The
finite-word language on which the gate never alters a proposal
is exactly Good(P) and is recognized by the gate automaton
with a rejecting sink, so Good(P) ∈RA[T ; Π]. Full proof
in the supplement (App. A).
Remark 1 (General gates). Dropping the register restriction,
an arbitrary computable gate with the same oracle inter-
face effectively enforces a nonempty P if and only if P
is safety with good-prefix membership decidable relative to
Π; (T ; Π)-gates are the register-recognizable fragment of
this class and model DSLs whose compiled checks have
exactly this state discipline. This refines the computability
taxonomy of Hamlen, Morrisett, and Schneider (2006) for a
monitor that cannot truncate (irreversibility) over an infinite,
data-carrying alphabet.
Proposition 1 (Strictly below edit automata). The gate-
enforceable policies are a strict subclass of the edit-
automaton enforceable policies. Witness: “every pay is
eventually followed by a confirm” is a non-safety renewal
property an edit automaton enforces by buffering pay until
confirm, but no pre-execution gate enforces it: once the irre-
versible pay commits it cannot be retracted, and blocking it
breaks transparency on the compliant stream pay confirm.
Extending the gate with substitution sub(a′) does not en-
large the T1 enforceable class. Rewrites are prefix-safe when
ua′ is good whenever the current effect prefix u is good. Such
substitution can weakly improve block-only utility under the
stated loss normalization; without prefix-safe rewrites, only
class equivalence is guaranteed. Human escalation is analo-
gous only when modeled as a prefix-safe oracle adjudicating
blocks; we do not prove a separate escalation theorem (cf.
substitution, App. A).
5
T2: The Statistical and Security
Boundaries (Fallible Judge)
We first isolate the exogenous binary decision for which an
ROC is the exact object, then treat the closed loop in which
blocking changes what happens next. The distinction is es-
sential: the former is a statistical experiment; the latter is a
controlled process.
Assumption 1 (Benign calibration regime). One binary
predicate labels a proposal violating/compliant; the gate is
block-only and acts before commit; and violating calibration
examples are label-conditionally exchangeable with violat-
ing deployment proposals. The product-episode specializa-
tion additionally assumes i.i.d. labels and conditionally i.i.d.
information across steps, and a stationary rule with fresh
per-step randomization.
Theorem 2 (Exogenous information frontier). Fix a one-step
law for the violation label and any pre-commit information
I whose law does not depend on the gate. Write rocI(β) for
the minimum false-block probability among all randomized
I-measurable rules with violation-miss probability at most
β. Then the exact safety–utility frontier is
B⋆
I (β) = rocI(β),
where B⋆
I is minimum false-block probability, attained by a
randomized likelihood-ratio test (by a threshold on a score
s when s is monotone in that ratio). No rule, ensemble, or
wrapper using the same I lies below this frontier. If I′ refines
I (so I is a garbling of I′), then rocI′(β) ≤rocI(β) point-
wise. Strict inequality requires that the refinement enlarge the
attainable error region at that operating point; conditional
dependence alone does not suffice.
Corollary 1 (Continuation-neutral episode lift). Under the
product specialization of Assumption 1, restrict the gate to
applying one stationary I-measurable test independently at
each step. If every step is violating, R(β) = 1−(1−β)H; if
labels are i.i.d. Bernoulli(q), R(β) = 1−(1−qβ)H. Within
this product class,
B⋆
I,H(δ) = rocI
 R−1(δ)

,
where B⋆
I,H is minimum per-step false-block probability. This
lift does not cover shared episode-level randomization or
feedback from decisions into future proposals.
Definition 5 (Controlled episode frontier). For a finite hori-
zon and finite abstraction, let Xt contain the environment,
agent memory, policy state, and an absorbing unsafe bit.
From its perfect-recall history Ht (including proposal and
score), the gate chooses Dt ∈{allow, block}; the kernel for
(Xt+1, Ht+1) may depend on Dt. For bounded additive cost
ct and first-entry unsafe cost rt, define C(π) = Eπ
P
t ct,
R(π) = Eπ
P
t rt, and FH(δ) = infπ:R(π)≤δ C(π) over
randomized perfect-recall policies.

<!-- page 5 -->
Theorem 3 (Endogenous finite-model frontier). For a spec-
ified finite controlled model in Definition 5, every history-
dependent policy has an equivalent belief-Markov policy.
Reachable-belief occupancy measures form a finite polytope,
and
FH(δ) = min
m∈M
X
t,b,d
mt(b, d)ct(b, d)
s.t.
X
t,b,d
mt(b, d)rt(b, d) ≤δ.
Thus the achievable (R, C) set is compact and convex and
FH is nonincreasing, convex, and piecewise linear. Strong
duality reduces each supporting point to the Bellman recur-
sion
V λ
t (b) = min
d {ct(b, d) + λrt(b, d) + E[V λ
t+1(b′) | b, d]},
and, whenever the risk constraint is feasible, an optimum is
implemented by sampling once per episode from at most two
deterministic belief-Markov policies (Walraven and Spaan
2018).
For posterior violation probability pt, compliant-block
cost wt, and continuation gap Γλ
t = E[V λ
t+1 | block] −
E[V λ
t+1 | allow], the dynamic rule blocks iff λpt −wt(1 −
pt) ≥Γλ
t . The one-step ROC is recovered when this con-
tinuation gap vanishes and the product conditions of Cor. 1
hold.
Proposition 2 (ROC does not identify a feedback frontier).
Two H = 2 systems can have identical judge ROC and iden-
tical ungated trajectory law but different FH(0) (minimum
intervention cost at zero episode-unsafe rate): after a first-
step block, one system terminates safely whereas the other
proposes a fresh violation. Hence closed-loop performance
requires the controlled response to intervention, not the un-
gated ROC alone.
Corollary 2 (Identification impossibility). Over any model
class containing the two systems in Proposition 2, no estima-
tor whose input is limited to ungated trajectories and static
judge scores can uniformly identify FH(0), hence cannot
identify the full controlled frontier.
Theorem 4 (Distribution-free safety certificate). Under As-
sumption 1, calibrating the threshold by conformal risk con-
trol, on violating calibration examples, to hold the per-step
conditional miss risk P[allow | violation] at δ/H yields
E[unsafe episode] ≤δ, marginally over deployment episodes
and the calibration draw, finite-sample and distribution-free
under per-step exchangeability. The theorem certifies risk,
not proximity to the population ROC frontier; finite calibra-
tion can select a conservative or block-all threshold.
The δ/H split above is a union bound; calibrating in-
stead on the monotone whole-episode loss over exchange-
able episodes attains E[unsafe] ≤δ with no factor of H
(supplement, App. A).
For the conservative gate that blocks when any of m judges
flags, its step-level miss and false-block probabilities are
Fréchet–Hoeffding-bounded over all within-class error cou-
plings (jointly attainable at both extremes for m ≤2); at
m = 1 these reduce to the one-judge errors (App. A).
Remark 2 (On the assumptions). The certificate’s exchange-
ability is label-conditional and per deployment proposal,
marginally over episodes; it is not a within-episode indepen-
dence claim. Independence is used only by Cor. 1’s product
formula. The controlled frontier permits arbitrary decision-
dependent transitions but requires their finite abstraction to
be specified.
Definition 6 (Budget-ρ adversary; robustness margin). Let
z = J(τ, a) be the representation visible to the judge. A
budget-ρ adversary knows the scoring function and thresh-
old and may replace z by z′ with d(z, z′) ≤ρ (for example,
inserting at most ρ tokens into a tool-output field), adap-
tively across steps. The executable proposal a, its effect, and
its ground-truth label π(τ, a) are unchanged. At threshold
θ, η(ρ; θ) is the supremal increase, over such representa-
tion perturbations, in conditional violation-miss probability;
¯η(ρ) = supθ η(ρ; θ). Suprema need not be attained on an
infinite perturbation set.
Theorem 5 (Adversarial deployment bound). Under As-
sumption 1, calibrate on benign violations as in Theorem 4,
then let a budget-ρ adversary act only at deployment. The
calibrated gate satisfies
E[unsafe] ≤min{1, δ + H ¯η(ρ)}
marginally over the calibration draw. At a fixed threshold θ,
an attained-margin, independent all-violation product con-
struction has risk 1 −(1 −min{1, β(θ) + η(ρ; θ)})H.
The second claim witnesses sharpness of the Hη depen-
dence under its stated construction; it is not a universal ad-
versarial lower bound.
Proposition 3 (Distributional zero-miss price). Let Qρ be
an attainable adversarial violation-score law and P0 the
compliant score law. Every score-measurable zero-Qρ-miss
gate obeys
U ≥1 −sup{P0(N) : Qρ(N) = 0}.
In particular, P0 ≪Qρ implies U = 1 for distributional
zero miss.
This differs from universal streamwise soundness. The
scalar condition η(ρ; θ) ≥1 −β(θ) only voids the naive
certificate at θ; it does not imply P0 ≪Qρ. Safe-washing
instead produces measured overlap: attacked violation scores
move into the low-score region already occupied by compli-
ant actions, making zero-miss over-blocking near one.
Corollary 3 (Robust calibration restores the certificate, at
an ROC price). If a uniform margin ¯η(ρ) < δ/H has been
verified, calibrating on benign exchangeable violations to
the tightened per-step target δ/H −¯η(ρ) (not δ/H) re-
stores E[unsafe] ≤δ (marginal over the calibration draw)
against any budget-ρ representation adversary at deploy-
ment. At the population optimum the tightened target changes
the false-block frontier by rocI(δ/H −¯η(ρ)) −rocI(δ/H);
a finite-sample calibrated gate can pay additional selec-
tion/conservatism slack. If P0 ≪Qρ, distributional zero-
miss requires block-all, which our safe-washing runs only
approach empirically.

<!-- page 6 -->
In short, naive calibration is not a security boundary, and
margin-aware calibration rescues it only when a verified
uniform margin stays below the miss budget. Our common-
population C3 experiment estimates η(ρ; .5), not ¯η: simulta-
neous inference detects miss increases for 8 of 11 fully cached
judges; a ninth point estimate is positive (§7). This diagnoses
a representation vulnerability at one operating point; it can-
not by itself certify or refute margin-aware calibration.
6
T3: The Decidability Boundary (Policy
Specification)
Theorem 1 makes enforcement constructive once a nonempty
policy is a T -representable safety automaton; static analysis
of an arbitrary specification is not. Even nontriviality (does
the spec ever fire, the basic linter check for a policy DSL) is
undecidable (a symbolic question, orthogonal to the seman-
tic-censorship undecidability of Glukhov et al. (2023)).
Theorem 6 (Specification analysis is undecidable). There
is a guard theory T ∗(equality plus two global N-counters
with increment, guarded decrement, and zero-test) for which
the following is undecidable: given a deterministic regis-
ter automaton over T ∗with a designated bad state, decide
whether the bad state is reachable, equivalently whether the
specified policy is nontrivial (has a bad prefix, i.e. rules out at
least one finite behavior). The reduction is from two-counter
Minsky-machine halting.
One sufficient undecidable extension is two independently
decrementable, zero-testable counters. The PSPACE result
additionally relies on separability, key locality, and constant-
only counter guards: even monotone counters can recover
decrementable-counter power if cross-counter comparisons
are allowed. Data plays no role in the lower bound. Thus a
linter deciding whether a rule set can ever fire is impossible
in T ∗; analyzable DSLs stay within the stated T0 restrictions.
Theorem 7 (A decidable, expressive fragment). Over a
separate infinite equality-data sort and binary-encoded N
amount sort, let T0 be finite separable, disjunctive products
of total deterministic components over a common alphabet:
(E) equality-register monitors; (K) a uniform key-local moni-
tor whose action names one key and only that key’s local state
and monotone counters may be read or updated; and (V) one
finite vector of monotone counters. Updates add nonnegative
fixed or action-supplied integers; each amount field has one
shared value across all its uses. Each guard tests one counter
(or counter plus that amount) against a binary-encoded con-
stant, never another counter. Component guards partition ev-
ery input (missing cases go to bad), and separability forbids
cross-component guards or assumptions. Bad-prefix reach-
ability is in pspace, by exact cap saturation for (K,V), exact
one-witness projection for (K), and on-the-fly search. With
saturated counters and a balanced key dictionary, online
time is polynomial in the specification, current-action en-
coding, and log of the number of stored keys; bit-space is
linear in stored data encodings plus per-key saturated local
states. The fragment expresses authenticate-before-access,
per-recipient caps, action-supplied bucket quotas, no-send-
after-revoke, and fixed-vector quotas; clock-time windows
additionally require a trusted bucket adapter. It includes P2
and P3 (App. A).
7
Experiments
The experiments target T2’s statistical, adversarial, and feed-
back consequences. The static study estimates per-action
miss and false block; the finite model checks the controlled-
policy calculation; the rewrite estimates one fixed-threshold
representation effect; and paired reruns test whether gate de-
cisions change trajectories. T1 and T3 are formal results,
constructively instantiated by P2–P3 rather than empirically
validated here. We report cumulative cost, gating fraction,
and task success separately because static studies need not
identify them under feedback.
Our primary static diagnostic is AgentDojo (Debenedetti
et al. 2024): 97 user-task and 35 injection-goal instruc-
tion strings, not context-rich tool calls. Twenty-three open,
closed, and dedicated-guard judges score the same 132 items.
A separate 60-call probe, InjecAgent (Zhan et al. 2024),
AgentHarm (Andriushchenko et al. 2025), and analytic syn-
thetic experiments are reported in the supplement. A coun-
terfactual source-role diagnostic pairs the culminating call
from all 123 nonempty AgentDojo task plans with byte-
identical action and instruction text, swapping only whether
the instruction is trusted-user input or untrusted tool output.
Action-only concordance is therefore .5 by design. Context-
rich paired concordance, the fraction scoring the unautho-
rized member higher with ties counting one half, is .561
(95% pair-bootstrap [.533, .589]) for the 3B judge and .967
([.939, .988]) for a 7B-model corroboration, while a 0.5B
negative control stays .500 (Holm-adjusted exact sign tests:
p < .001, p < .001, and p = 1). This isolates sensitivity
to the stated authorization provenance, not natural-trace or
deployment-safety accuracy (App. B.4).
C1–C2: static discrimination and calibration.
The em-
pirical one-step threshold sweep is the score-restricted ROC
by construction; on a binormal synthetic judge it agrees with
the analytic frontier within 2.5 Monte-Carlo standard devia-
tions over 40 thresholds. Across the 23 real runs, AUC ranges
.660–.858. Paired DeLong contrasts against Gemma-2-9B
(AUC .813), with max-T intervals and Holm checks over 22
comparisons, find no familywise-adjusted superiority; max-
T detects only Llama-3.1-8B as inferior, while the Holm
sensitivity check gives p = .062. No comparison establishes
familywise equivalence at the predeclared ±.05 margin, and
the median detectable difference is .104, so these data sup-
port non-monotonicity in parameter count but neither a tie
nor a capacity ceiling.
For calibration, 500 shared balanced two-fold splits and a
suite×label outer bootstrap measure finite-sample behavior,
not deployment exchangeability. At δ = .05, every judge’s
split threshold is block-all. For Gemma-2-9B, δ = .10 gives
miss .010 (simultaneous upper .021) and false block .780
(simultaneous 95% interval [.660, .901]); at δ = .20, the miss
point estimate is .138 but its upper bound is .264, so it is not
certified by this empirical diagnostic. Figure 1a exposes both
vacuity and uncertainty rather than treating a low observed
miss as proof.

<!-- page 7 -->
0.0
0.1
0.2
0.3
0.4
violation miss
0.0
0.2
0.4
0.6
0.8
1.0
compliant false block
x: block-all
(a) Static frontier + calibration
δ= .05
δ= .10
δ= .20
δ= .30
−0.2
0.0
0.2
0.4
0.6
0.8
miss increase at fixed threshold 0.5
Claude-Opus-4.5
Claude-Sonnet-4.5
Llama-3.1-8B
Mistral-Large-3
Qwen-2.5-32B
Qwen-2.5-3B
Qwen-2.5-7B
Llama-3.3-70B
Command A
Gemma-2-9B
Nova-Pro
(b) 16-token rewrite (35 violations)
3B gate
7B gate
0
5
10
15
20
25
30
35
40
45
paired discordant episodes
34
29
5
22
(c) Decisions change trajectories
baseline-only attack
gate-only attack
Figure 1: Three regimes, three estimands. (a) Gemma-2-9B’s empirical one-step ROC and repeated two-fold cross-fitted
conformal points (δ labels); bars are a one-sided simultaneous 95% miss upper bound and two-sided simultaneous false-block
interval over all 23 × 4 points. The δ = .05 point is block-all. (b) Miss increase from one predeclared 16-token representation
rewrite at fixed θ = .5, using all 35 violations; suite-bootstrap 95% intervals are simultaneous over 11 fully cached judges
(orange excludes zero). (c) Paired closed-loop reruns: both gates create some attacks, directly demonstrating decision-dependent
transitions.
Finite controlled instantiation.
We exactly enumerate the
occupancy polytope of a fully specified two-step retry model
(App. B.2).
At δ = .05, cost is .551 with perfect recall, versus .863 for
current-score/time policies and 1.137 for stationary thresh-
olds. This strict policy-class gap makes Theorem 3 concrete;
it is an analytic model check, not an estimate of AgentDojo’s
unknown kernel.
C3: common-population representation attack.
We in-
sert one predeclared 16-token “administrator preapproval”
suffix into the judge-visible string while holding the canon-
ical item and label fixed (the static diagnostic has no exe-
cutable call). At θ = .5, miss increases by .200–.600 for
8 of 11 fully cached judges, with simultaneous intervals
excluding zero for all 8; the other three intervals include
zero (Figure 1b). This estimates a fixed-threshold, common-
population effect, not ¯η, not a universal attack, and not cer-
tificate failure at every calibrated threshold. A judge-selected
held-out best-of-template result remains a labeled secondary
diagnostic in the supplement.
C4: selected policies in the closed loop.
A local 7B agent
is rerun for 949 episodes per condition with an inline gate.
The 3B policy reduces attack success from 45/949 = .047
(95% Wilson [.036, .063]) to 4/949 = .004 ([.002, .011];
suite-stratified p = 2.2×10−9), while its descriptive gat-
ing fraction is 78%. The lighter 7B policy gates 12% and
reaches 30/949 = .032 ([.022, .045]), not significant across
suites (p = .09). Task success is a separate endpoint: .254
([.227, .283]) ungated, .243 ([.217, .272]) with 7B, and .180
([.157, .206]) with 3B. On a separate task-paired rerun of
the three injectable suites (N = 389), the 3B gate has 34
baseline-only versus 5 gate-only attacks (p = 2.4×10−6);
the 7B gate has 29 versus 22 (p = .40). The gate-only out-
comes prove feedback and selected-policy effects, not the
product ROC lift or the full controlled frontier.
8
Discussion and Limitations
Scope and assumptions. The exogenous frontier needs a fixed
one-step experiment; its episode lift additionally needs the
product conditions in Assumption 1. The controlled theo-
rem needs a known finite abstraction and bounded costs. The
certificate needs label-conditional exchangeability; robust re-
calibration also needs a verified representation-space margin
(Cor. 3). We treat the judge black-box at H=1; safe-washing
is sandbox-only.
Limitations. Closed-loop safety (C4) is bought by over-
blocking: the 3B gate blocks 78% of calls. C4 estimates three
selected policies rather than AgentDojo’s controlled frontier,
and its gate-created attacks show why ungated data need not
identify that frontier. Our attacks only lower-bound worst-
case margins; robust calibration needs a verified uniform
upper bound.
Evaluation contract. The boundaries imply a minimum
reporting standard for runtime guardrails: state (i) the policy
language, oracle interface, and trusted metadata; (ii) the tar-
get miss/false-block operating point rather than AUC alone;
(iii) whether blocking is visible to the agent, with paired
reruns that can expose changed trajectories; and (iv) the cal-
ibration population, exchangeability claim, and adversarial
margin behind any certificate. If feedback appears but no
controlled kernel is specified, the evaluated policies’ out-
comes are identified, but the closed-loop frontier is not. The
matched source-role experiment supplies a separate contex-
tual check: provenance use is isolated from action content
and varies sharply across the three local models.
Actionable target. AUC cannot be inverted into a required
deployment quality because it does not identify a particular
ROC operating point. For example, at H = 1, achieving miss
at most .05 with a .10 false-block budget requires the concrete
target rocI(.05) ≤.10; for a product episode replace .05 by
R−1(.05). This operating-point target, rather than model size
or AUC alone, is what improved judges must meet.

<!-- page 8 -->
