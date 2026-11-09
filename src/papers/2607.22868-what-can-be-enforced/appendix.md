> PDF 文本抽取（pymupdf），保留 `<!-- page N -->`；表格/公式可能有版式噪声，引用前回 PDF 核。

A
Proofs
A.1
Preliminaries and notation
We work in the Cantor topology on Aω, whose basic open
sets are the cylinders uAω for u ∈A∗. A set P ⊆Aω is
closed iff it contains all its limit points, where x is a limit
point of P if every prefix x≤n is a prefix of some element of
P. We use repeatedly the classical characterization of safety.
Lemma 1 (Safety is topological closure). P ⊆Aω is a safety
property (Def. 2) if and only if P is closed. Equivalently,
x ∈P iff every finite prefix x≤n is a good prefix, i.e. x≤n /∈
Bad(P)A∗.
Proof. If P is safety and x /∈P, then x has a bad prefix x≤n,
so the open cylinder x≤nAω is disjoint from P; hence the
complement of P is open and P is closed. Conversely, if P is
closed and x /∈P, then x is not a limit point, so some prefix
x≤n extends into P nowhere, i.e. x≤nAω∩P = ∅; that prefix
is a bad prefix, so P is safety. The prefix characterization is
the contrapositive: x ∈P iff no prefix is bad.
Recall (Def. 4) that a gate g decides from committed ef-
fect history h<t ∈(A \ {⊥})∗, proposal at, and Π(h<t, at).
We assume Π reads this same effect history (equivalently, an
interface defined on full committed traces must be ⊥-blind).
We keep Π explicit: it is an available oracle interface, not
a promise that its bits are definable in T . A (T ; Π)-gate
is computed by a deterministic register automaton whose
guards combine T tests with queries to these bits. A pro-
posal stream is a map from committed histories to proposed
actions; together with g it determines the committed trace.
We write ⊥for the neutral no-op of Def. 1. Because poli-
cies are scored on effect traces (Def. 1), the recognizer R of
Good(P) reads only effect actions: committing ⊥produces
no effect and leaves R’s state unchanged (so δ(q, ⊥) = q),
and a trace is safe for P iff no finite prefix of its effect trace
is bad.
Symbol
Meaning
A, A∗, Aω
action alphabet; finite/infinite traces
⊥
neutral no-op action
P, Bad(P), Good(P)
policy; minimal bad prefixes; good pre-
fixes
RA[T ; Π]
register automata with T -guards and
oracle interface Π
πi, ˆπθ
i
ground-truth
predicate;
thresholded
judge
α(θ), β(θ)
judge false-alarm and miss rates
roc(β)
ROC frontier: min α at miss β
g, Dec
gate; decisions {allow, block, sub}
R(θ), U(θ)
episode unsafe rate; utility loss
H, δ, η(ρ)
horizon; target δ; robustness margin
Table 1: Notation.
A.2
T1: oracle characterization
Theorem (Oracle characterization). Fix the available ora-
cle interface Π and a nonempty policy P. Then P is effectively
enforceable by a deterministic (T ; Π)-gate iff it is safety and
Good(P) ∈RA[T ; Π]; the witness simulates that recognizer
and refuses exactly the one-step extensions it rejects.
Proof. (⇐). Let R = (Q, q0, k, δ, B) be a deterministic
register automaton recognizing Good(P) with B absorb-
ing and guards in (T ; Π). Define the gate G that maintains
qt = δ∗(q0, c≤t) and, on proposed a at state q, commits a
(moving to δ(q, a)) if δ(q, a) /∈B, and otherwise commits
⊥(a block, leaving the state at q).
Soundness. Blocking commits ⊥(no effect; the recognizer
does not move); an allowed action moves within Good(P) by
construction, since G blocks exactly the one-step extensions
entering B. So the committed run visits only good states and
every effect prefix ext(c≤t) ∈Good(P) = A∗\ Bad(P)A∗
is not bad. Hence the committed trace is safe for P (Def. 1):
if the effect trace is infinite it lies in P by Lemma 1; if the
gate eventually blocks forever, the finite effect trace still has
no bad prefix. This holds for every proposal stream.
Transparency. Suppose the proposed ω-trace w lies in P.
By Lemma 1 every prefix of w is good, so running R on
w never reaches B; hence G never blocks and commits w
unchanged.
Complexity. Each step evaluates the enabled guarded tran-
sition on the current data, registers, and supplied oracle bits.
This is polynomial when guard evaluation and updates are
polynomial; no satisfiability solver is implicitly assumed.
(⇒). We work in the effect alphabet A \ {⊥}, over which
P and its traces live. Suppose the (T ; Π)-gate g effectively
enforces P but P is not safety. By Lemma 1, P is not closed,
so it has a limit point x /∈P that is a doomed effect trace: for
every n there is an effect trace z(n) ∈P with z(n)
≤n = x≤n.
Let S be the open-loop stream proposing x1, x2, . . . in turn
(a fixed sequence, independent of the gate’s actions). We
show by induction on t that g allows xt, so the committed
effect trace is x.
Base case t = 0 is immediate. For the step, assume g has
allowed x1, . . . , xt−1, so the committed effect history is x<t
and the proposal is xt. Consider the open-loop stream S(t)
proposing z(t)
1 , z(t)
2 , . . . ; its proposed effect trace is z(t) ∈P,
so by prefixwise transparency (Def. 4) the committed effect
prefix equals z(t)
≤k at every step k. Thus g blocks or alters
nothing on S(t), and in particular allows z(t)
t
= xt from the
committed effect history z(t)
<t = x<t. Because g conditions
on the effect history (Def. 4), its decision here is the value
g(x<t, xt, Π(x<t, xt)), identical under S and S(t); being de-
terministic, g also allows xt under S. By induction g commits
the effect trace x /∈P, whose bad prefix (Lemma 1) makes
some committed effect prefix bad, contradicting soundness.
Hence P is safety.
It remains to recognize Good(P). Simulate the finite con-
trol, registers, and committed-history updates of g while
reading a proposed finite word u, and move to a rejecting
sink at the first output other than allow. This is a determinis-
tic (T ; Π) register automaton. If u ∈Good(P), then u has a
completion in P (otherwise u itself would be bad), and pre-
fixwise transparency forces every symbol of u to be allowed.
Conversely, if u contains a first bad prefix va, transparency

<!-- page 9 -->
on a compliant completion of v forces g to allow v, while
soundness forbids allowing a from that history; thus the sim-
ulation rejects. Its language is exactly Good(P), proving
Good(P) ∈RA[T ; Π].
Remark 3 (General computable gates). Dropping the reg-
ister restriction, the same limit-point argument shows an
arbitrary computable gate with interface Π effectively en-
forces a nonempty P iff P is safety and good-prefix member-
ship is decidable relative to Π. (T ; Π)-gates are the register-
recognizable subclass.
For a randomized gate, quantify separately: for every (pos-
sibly adaptive) proposal strategy, soundness holds with prob-
ability one over gate randomness; and for every fixed com-
pliant proposal trace, prefixwise transparency holds with
probability one. On each compliant z(t) agreeing with a
doomed limit trace x through t, transparency makes the con-
ditional decision at history x<t equal to allow almost surely.
The countable intersection of these probability-one events
makes the gate commit all of x almost surely, contradicting
almost-sure soundness. Thus randomization does not extend
the safety boundary (although the register-representability
converse above is stated only for deterministic gates).
Proposition (Strictly below edit automata). The gate-
enforceable policies are a strict subclass of the edit-
automaton enforceable policies.
Proof. Every gate-enforceable policy is safety with a decid-
able good-prefix language (Theorem above); an edit automa-
ton enforces each such policy by suppressing any action that
would enter Bad(P) and re-emitting nothing (safety prop-
erties are a subclass of the renewal properties edit automata
enforce (Ligatti, Bauer, and Walker 2005, 2009)), giving con-
tainment. For strictness, let A contain irreversible pay and
confirm and let
P ∗= {w ∈Aω : every pay in w has a later confirm}.
P ∗is not safety. The trace pay ⊥ω violates P ∗, yet
no finite prefix is bad: any prefix pay ⊥k extends to
pay ⊥k confirm ⊥ω ∈P ∗. By Lemma 1, P ∗is not safety,
so by the Theorem no gate enforces it. Self-contained im-
possibility. A gate must decide the first pay irrevocably. To
be transparent on the compliant stream pay confirm ∈P ∗it
must allow the initial pay; but then on the stream pay ⊥ω that
pay is already committed and irreversible, and P ∗is violated
with no possible retraction, so the gate is unsound. Substitu-
tion does not help: replacing pay by a semantically distinct
action fails transparency, and replacing it by an equivalent
pay returns to the first case. Edit-enforceable. P ∗is a re-
newal property; an edit automaton suppresses each pay into
a buffer and emits it upon confirm (and never if confirm does
not occur), which is edit-enforceable by the renewal-property
theorem of Ligatti, Bauer, and Walker (2009). Thus P ∗sepa-
rates the classes. The comparison is at the level of enforceable
policy classes, each in its own model’s semantics: edit au-
tomata enforce P ∗by buffering, which presumes actions can
be delayed and re-emitted; irreversibility removes exactly
that power, which is why the classical class is unattainable
for a pre-execution gate over committed actions, not a defect
of the gate.
Proposition (Substitution: same class, weakly better util-
ity). Adding sub(a′) does not change the class in T1. If ev-
ery rejected compliant proposal at good prefix u admits a
rewrite with ua′ ∈Good(P) and conditional loss at most
ℓsub ∈[0, 1] relative to unit loss for a block, substitution can
reduce false-block cost from α(θ) to at most ℓsubα(θ).
Proof. Run the T1 recognizer. When ua would be rejected,
either block or choose the assumed a′ with ua′ ∈Good(P)
and update the recognizer on a′. The committed run remains
good, and no rewrite fires on a compliant proposed trace, so
soundness and transparency hold. Conversely, the T1 limit
argument and never-alter recognizer apply to gates with sub-
stitution as well, so adding that decision cannot enlarge the
class.
Under the stated loss normalization, a compliant proposal
is sent to the rewrite branch with probability α(θ) and costs
at most ℓsub there. Its expected conditional loss is therefore
at most ℓsubα(θ). Without the prefix-safe rewrite and loss
assumptions, only the class-equivalence statement remains;
substitution need not improve an arbitrary task utility.
Remark 4 (Escalation). Replacing a block by an oracle that
always returns a prefix-safe commit action is a special case
of substitution (with the oracle’s loss in place of ℓsub). The
class and utility conclusions above are relative to that oracle
model; no claim is made for a fallible or non-prefix-safe
human decision.
A.3
T2: enforcement under a fallible judge
For a one-step binary decision, let P1 and P0 be the laws
of pre-commit information I conditional on a violating and
compliant proposal. A randomized block rule is a measur-
able φ(I) ∈[0, 1]. Its miss and false-block probabilities are
β(φ) = 1 −E1φ and α(φ) = E0φ.
Lemma 2 (Neyman–Pearson optimality). Among all I-
measurable rules with miss at most β0, the minimum false-
block probability is rocI(β0), attained by a randomized
likelihood-ratio threshold.
Proof. Blocking a violation has probability P[block | π =
1] = E1[φ] = 1 −miss, and false-alarm is P[block | π =
0] = E0[φ]. The constraint is E1φ ≥1 −β0 and the objec-
tive is E0φ. This is the Neyman–Pearson program (Neyman
and Pearson 1933; Tong, Feng, and Li 2018); its randomized
likelihood-ratio solution has value rocI(β0). Boundary ran-
domization convexifies the error region, so β 7→rocI(β) is
nonincreasing and convex.
Theorem (Exogenous information frontier). For a fixed
one-step law, the exact frontier from information I is
B⋆
I (β) = rocI(β). If I′ Blackwell-refines I, then rocI′(β) ≤
rocI(β) pointwise.
Proof. The equality is Lemma 2. If I is a garbling of I′, every
I-measurable rule is implementable from I′ by applying the
garbling first. Thus the feasible error region for I′ contains the

<!-- page 10 -->
one for I, giving the pointwise inequality. Strictness occurs
only where the larger region has a strictly lower supporting
boundary; conditional dependence alone does not imply it.
Corollary (Continuation-neutral episode lift). Under the
product specialization of Assumption 1, a stationary test with
fresh per-step randomization has R(β) = 1 −(1 −β)H on
the all-violation stream and R(β) = 1 −(1 −qβ)H for i.i.d.
Bernoulli(q) labels. Within this product class, B⋆
I,H(δ) =
rocI(R−1(δ)).
Proof. The product formulas follow because “a violation
is committed” has probability β (or qβ) independently at
each step. Since the repeated test has per-step false-block
probability α, imposing R(β) ≤δ is equivalent to β ≤
R−1(δ); the preceding theorem gives the optimum at the
largest admissible miss. Shared episode-level randomization
is excluded because it need not obey the product formula.
Theorem (Endogenous finite-model frontier). For a spec-
ified finite model, the controlled frontier of Definition 5 is the
image of a reachable-belief occupancy polytope; its lower
boundary is convex and piecewise linear, its Lagrange dual
is solved by belief-state Bellman recursion, and an optimum
mixes at most two deterministic belief-Markov policies.
Proof. Augment the latent state with an absorbing unsafe
bit and let rt be one only on first entry, so P
t rt is the
episode-unsafe indicator. With finite abstractions and finite
H, finitely many observation histories and posteriors bt =
P(Xt | Ht) are reachable. Belief is a sufficient controlled
state: the conditional action probabilities of any perfect-recall
policy define a belief-Markov policy with the same trajectory
law and (R, C).
Let mt(b, d) be the probability of occupying belief b and
choosing d. The nonnegative flow constraints are
X
d
m1(b, d) = µ1(b),
X
d
mt+1(b′, d) =
X
b,d
mt(b, d)Kt(b′ | b, d).
Conversely, disintegrating a feasible flow gives a belief-
Markov policy. Both R and C are linear in m, proving the
main occupancy program. Its feasible set is a bounded poly-
tope; its two-dimensional performance image is a compact
convex polygon, with a convex piecewise-linear lower bound-
ary.
Finite LP duality gives
FH(δ) = max
λ≥0 {V λ
1 (b1) −λδ},
V λ
t (b) = min
d {ct(b, d) + λrt(b, d)
+ E[V λ
t+1(b′) | b, d]}.
A deterministic minimizer exists for each λ. Any constrained
boundary point lies on a supporting segment of the perfor-
mance polygon. Every endpoint vertex is the image of an
extreme occupancy point, and extreme finite-horizon occu-
pancy points are induced by deterministic belief-Markov
policies. Hence sampling one endpoint policy once per
episode implements the boundary point with support at most
two.
Comparing Bellman Q-values gives the dynamic rule in
the main text: blocking costs wt(1−pt), allowing incurs λpt,
and rearranging Q(block) ≤Q(allow) yields λpt −wt(1 −
pt) ≥Γλ
t .
Proposition (ROC does not identify a feedback frontier).
Proof. Take H
=
2, a constant score, and Y1
∼
Bernoulli(q) with 0 < q < 1. If step one is allowed, let
Y2 = 0 in both systems, so their ungated laws and ROCs
coincide. If step one is blocked, system A has Y2 = 0, while
system B presents Y2 ∼Bernoulli(p), 0 < p < 1. Zero
risk forces a first-step block. A then need not block again,
whereas B must. For expected compliant-block count, set
ct = ⊮[block and compliant] and let rt indicate first un-
safe entry as in Definition 5. Then FA(0) = 1 −q and
FB(0) = (1 −q) + (1 −p), proving non-identifiability.
Corollary (Identification impossibility).
Proof. Any estimator restricted to ungated trajectories and
static scores has the same input law in systems A and B,
but the target takes the distinct values FA(0) and FB(0). It
therefore cannot identify both uniformly. Because FH(0) is
one point of the controlled frontier, neither can it identify the
full frontier.
Theorem (Distribution-free safety certificate). Under As-
sumption 1, calibrating the threshold by conformal risk
control on violating examples to hold the per-step condi-
tional miss risk r(θ) = P[allow | violation] at δ/H yields
E[unsafe episode] ≤δ marginally over deployment episodes
and the calibration draw, finite-sample and distribution-free
under per-step exchangeability.
Proof. Fix
the
calibrated
threshold
ˆθ
(a
func-
tion
of
the
calibration
sample).
Let
Lt
=
⊮[a violation at step t is committed]. An unsafe episode has
P
t≤H Lt ≥1, so by the union bound, conditioning on ˆθ,
P[unsafe | ˆθ] ≤
X
t≤H
P[Lt=1 | ˆθ]
=
X
t≤H
P[viol. at t] r(ˆθ) ≤H r(ˆθ),
using P[viol. at t] ≤1 and that, by label-conditional per-step
exchangeability with the calibration sample (Assumption 1),
the conditional miss risk at each step is r(ˆθ). The per-step
risk r(θ) is a bounded, nondecreasing loss in θ (raising the
threshold blocks fewer actions); reparameterizing by λ = −θ
makes it nonincreasing. Conformal risk control (Angelopou-
los et al. 2024) on the exchangeable calibration sample of vio-
lating actions returns ˆθ with E[r(ˆθ)] ≤δ/H, the expectation
taken over the calibration draw. The exchangeability required

<!-- page 11 -->
is label-conditional (Mondrian): since r is calibrated on the
violating subpopulation, the violating calibration examples
must be exchangeable with the violating deployment steps, as
required by Assumption 1, not merely jointly exchangeable
before conditioning on the label. Taking that expectation of
the display, E

P[unsafe | ˆθ]

≤H E[r(ˆθ)] ≤δ, which is the
stated marginal guarantee. Nothing in this argument bounds
the finite-sample threshold’s distance from the population
ROC optimum.
Proposition (Episode-level certificate, no H-penalty).
If a calibration set of whole episodes is exchangeable
with deployment episodes, calibrating the threshold by
conformal risk control on the monotone episode loss
L(ep) = ⊮[some step allows a violation] to level δ gives
E[unsafe episode] ≤δ with no factor of H.
Proof. The union-bound step above pays a factor H because
it controls each per-step risk separately. Instead treat the
whole episode as one calibration unit. The loss L(ep; θ) =
⊮[∃t ≤H : a violation at t scores below θ] is equivalently
L(ep; θ) = ⊮

min
t:Yt=1 st < θ

,
with the minimum over an empty set defined as +∞. It is
bounded in [0, 1] and nondecreasing in θ (raising θ blocks
weakly fewer actions, so it never turns a missed violation
into a caught one). Reparameterizing by λ = −θ makes
it a non-increasing admissible loss for conformal risk con-
trol (Angelopoulos et al. 2024), which, on an exchangeable
episode calibration set, returns ˆθ with E[L(ˆθ)] ≤δ. Since
P[unsafe episode | ˆθ] = E[L(ep; ˆθ) | ˆθ], taking the calibra-
tion expectation gives E[unsafe episode] ≤δ directly. The
price is that exchangeability is now required at the episode
level (episodes i.i.d. or exchangeable), stronger than the per-
step version but free of the H-fold tightening, which matters
when H is large.
Proposition (General region is copula-bounded). For the
conservative any-flag gate and fixed marginal error rates,
Fréchet–Hoeffding bounds bracket the step-level miss for a
specified violated predicate set and the false-block probabil-
ity on compliant actions. For m ≤2 both endpoint pairs
are jointly attainable using separate class-conditional cou-
plings; for m > 2 the inequalities remain valid without a
global extremal-copula claim. At m = 1 they equal the one-
judge errors.
Proof. Take the conservative gate that blocks when any judge
flags. A violation with true hazard on predicate set S is
committed iff every relevant judge misses, an event T
i∈S Mi
with P[Mi] = βi; a compliant action is altered iff some judge
false-alarms, S
i Fi with P[Fi] = αi. For fixed marginals the
Fréchet–Hoeffding inequalities give
max
 0, P
i∈S βi −|S| + 1

≤P
 T
i∈S Mi

≤mini∈S βi,
max
i
αi ≤P
h S
i Fi
i
≤min

1, P
i αi

,
which hold for every coupling of the errors. The comono-
tone coupling attains the intersection upper bound and the
union lower bound. For m ≤2 the opposite endpoints are
jointly attainable in the overall labeled experiment: choose
a countermonotone coupling for misses conditional on the
violation class and, separately, for false alarms conditional
on the compliant class. With two miss indicators this attains
P[M1 ∩M2] = max(0, β1 + β2 −1) and P[F1 ∪F2] =
min(1, α1 +α2) at once. For m > 2 no single coupling need
meet all pairwise extremes simultaneously, so the bounds re-
main valid without a claimed global copula. An episode lift
additionally requires specified temporal dependence; only
under Cor. 1’s product conditions may these step probabil-
ities be inserted into its product formula. For m = 1 both
bounds equal (α1, β1).
Theorem (Adversarial deployment bound). Under As-
sumption 1, with conformal calibration on benign data and
a budget-ρ adversary acting at deployment, the calibrated
gate satisfies E[unsafe] ≤min{1, δ + H ¯η(ρ)}. Conditional
on a fixed threshold, an attained-margin independent product
construction realizes 1 −(1 −min{1, β(θ) + η(ρ; θ)})H.
Proof. Upper bound. Calibration is performed on the be-
nign exchangeable sample; the representation adversary acts
only at deployment. By Def. 6, ¯η(ρ) upper-bounds the per-
step increase in the conditional miss risk at every thresh-
old, so under any budget-ρ adversary the risk at the cali-
brated ˆθ is at most r(ˆθ) + ¯η(ρ). The union bound of the
certificate proof, conditioning on ˆθ, gives P[unsafe | ˆθ] ≤
P
t≤H(r(ˆθ) + ¯η(ρ)) = H r(ˆθ) + H ¯η(ρ); taking the calibra-
tion expectation and using E[r(ˆθ)] ≤δ/H (conformal risk
control) yields the marginal E[unsafe] ≤min{1, δ+H ¯η(ρ)}.
Sharpness construction. Fix θ and suppose a representation
adversary attains the defining supremum, so its conditional
miss is x = min{1, β(θ) + η(ρ; θ)}. On an all-violation
product stream, choose its perturbation randomness inde-
pendently across steps. The probability that no violation is
committed is (1 −x)H, giving exactly 1 −(1 −x)H. If the
supremum is not attained, the same risks are approached with
η −ε. This demonstrates first-order sharpness of the union
bound under a stated construction; it is not a lower bound for
every adversary or feedback process. Non-transfer. Confor-
mal validity requires the deployment steps to be exchangeable
with the calibration sample; a budget-ρ adversary changes the
input distribution, so E[r(ˆθ)] ≤δ/H need not hold and the
bare δ bound is void unless η absorbs the shift.
Proposition (Distributional zero-miss price). For any at-
tainable adversarial violation-score law Qρ, every score-
measurable gate with zero Qρ-miss has utility at least
1 −sup{P0(N) : Qρ(N) = 0}; if P0 ≪Qρ, this distri-
butional zero-miss cost is one.
Proof. Let Qρ be any attainable score law induced on viola-
tions and P0 the compliant score law. Fix a score-measurable
gate with zero miss under Qρ. For a deterministic gate the
blocked set B has Qρ(B) = 1; for a randomized gate the

<!-- page 12 -->
same argument applies to its block-probability function and
yields the identical variational value. Its utility loss is the
compliant mass it over-blocks, U(g) = P0(B), and over all
zero-miss gates
U(g) ≥inf{P0(B) : Qρ(B) = 1}
= 1 −sup{P0(N) : Qρ(N) = 0},
using P0(B) = 1−P0(Bc) with Bc ranging over the Qρ-null
sets. This is an absolute-continuity (affinity) bound, sharper
and correct where a raw support-overlap bound is not: a zero-
miss gate may leave unblocked only the part of the compliant
law singular to Qρ. By the Lebesgue decomposition P0 =
P ac
0 +P sing
0
relative to Qρ, U(g) ≥P ac
0 (R) = 1−P sing
0
(R).
Hence if P0 ≪Qρ (no compliant mass on any Qρ-null set)
then U(g) = 1: block-everything is the only distributionally
zero-miss score rule. This is not the universal streamwise
soundness of Def. 4. We emphasize that η(ρ; θ) ≥1 −β(θ)
is not sufficient for domination: it drives the adversarial miss
to one at that threshold, but says nothing about whether P0
is dominated by Qρ (P0 may still place mass on Qρ-null
sets, e.g. high-scoring compliant actions). What approaches
P0 ≪Qρ is empirical: in the safe-washing runs the adversary
drives Qρ onto the low scores where the LLM judges already
place compliant actions, so the overlap 1 −sup{P0(N) :
Qρ(N) = 0} is large and the zero-miss gate’s over-block U
is near 1; we report the measured U rather than assume total
absolute continuity.
Corollary (Robust calibration). If a verified uniform mar-
gin ¯η(ρ) < δ/H, calibrating on benign exchangeable viola-
tions to the per-step target δ/H −¯η(ρ) yields E[unsafe] ≤δ
(marginal over the calibration draw) under any budget-ρ rep-
resentation adversary at deployment. At the population opti-
mum the frontier price is rocI(δ/H −¯η(ρ)) −rocI(δ/H);
finite-sample calibration may pay additional conservatism.
If P0 ≪Qρ, distributional zero-miss costs one.
Proof. Run the same split-conformal calibration but against
the tightened per-step target τ ′ = δ/H −¯η(ρ) > 0, so the
benign per-step miss is ≤τ ′. By Def. 6 a budget-ρ adversary
raises the per-step conditional miss at any threshold by at
most ¯η(ρ), to τ ′ + ¯η(ρ) = δ/H. The union bound of the
upper part then gives P[unsafe] ≤P
t≤H δ/H = δ, for any
budget-ρ adversary since the per-step bound is worst-case. At
the population optimum, changing the miss target from δ/H
to τ ′ changes false-block cost by rocI(τ ′) −rocI(δ/H).
A threshold selected from a finite calibration sample can
lie above this envelope, so equality of its realized cost is not
claimed. If the tightened target is non-positive, this procedure
falls back to block-all; the separate domination condition
P0 ≪Qρ is what forces unit cost for distributional zero-
miss.
A.4
T3: the decidability boundary
Theorem (Specification analysis is undecidable). Enforce-
ment is constructive once a nonempty policy is given as a
T -representable safety automaton (T1); static analysis of
an arbitrary specification is not. There is a guard theory
T ∗(equality plus two global N-counters with increment,
guarded decrement, and zero-test) for which reachability of
a designated bad state in a deterministic register automaton
is undecidable; consequently deciding whether a specified
data-word policy is nontrivial (has a bad prefix, i.e. ever
fires), the basic sanity check a policy DSL’s linter would run,
is undecidable.
Proof. A two-counter Minsky machine M has counters
c1, c2 ∈N and a finite program of labeled instructions
of three forms: ℓ:
cj++; goto ℓ′; ℓ:
if cj
=
0 goto ℓ′ else cj−−; goto ℓ′′; and a halt instruction. Whether
M, started from c1 = c2 = 0 at its initial label, reaches its
halt instruction is undecidable.
Build a deterministic register automaton A over T ∗as
follows. Its finite control is the set of M’s labels plus an
absorbing good sink G; it has two global N-counters r1, r2
initialized to 0; and the alphabet contains tick and safe. On
each tick, A executes the instruction at the current label: an
increment instruction updates rj+ = 1 and moves to ℓ′; a
test-and-decrement instruction uses the T ∗zero-test guard
rj = 0 to branch to ℓ′, or otherwise updates rj−= 1 and
moves to ℓ′′. From every nonbad machine label, safe moves
to G, where both actions loop. These updates and guards are
exactly the operations of T ∗, and A is deterministic because
M is. Designate M’s halt label as the absorbing bad state B.
Because M is deterministic and requires no input, the run
of A on the infinite tick stream faithfully simulates M: after
n ticks its configuration (label, r1, r2) equals M’s configu-
ration after n steps. Hence a finite tick-prefix reaches B iff
M halts, so bad-state reachability in A is undecidable. The
induced policy P has a bad prefix, i.e. is nontrivial (rules out
at least one finite behavior), iff B is reachable iff M halts.
It is always nonempty, since taking safe before B yields an
infinite run in G, and every nonbad prefix has such a safe
continuation. Enforcing this constructed T ∗-automaton is
therefore still constructive (T1); what is undecidable is the
static question of whether an arbitrary such specification is
non-vacuous, so no DSL linter can decide it over T ∗.
Theorem (A decidable, expressive fragment). Over a
separate infinite equality-data sort and binary-encoded N
amount sort, for finite separable, disjunctive products of to-
tal equality-register components (E), uniform independent
key-local monotone-counter components (K), and one finite
monotone counter-vector component (V), bad-prefix reach-
ability is in pspace. Cap saturation is exact for (K,V), one-
witness projection is exact for (K), and the finite abstraction
is searched on the fly. Online enforcement is polynomial per
step in the specification, current-action encoding, and log of
the number of stored keys; with saturated counters, bit-space
is linear in stored data encodings plus per-key local abstract
states.
Proof. Exact saturation. For counter x, let Cx be the great-
est constant against which x or x + v is compared (or 0 if
none) and define σx(n) = min{n, Cx + 1}. Because every
update is nonnegative, values above Cx never return below
it. For each supplied amount field v, let Cv be the largest

<!-- page 13 -->
Cx among counters whose guards or updates use that field,
guess the single category τv(v) = min{v, Cv + 1}, and de-
rive every counter-specific category as min{τv(v), Cx + 1}.
Thus all uses represent one concrete amount, rather than in-
dependent per-counter guesses. Every allowed atomic guard
x ▷◁c or x + v ▷◁c has the same truth value for all concrete
valuations with the same abstraction, and abstract addition
σx(σx(x) + min{τv(v), Cx + 1}) exactly matches concrete
addition followed by σx. Boolean combinations and deter-
ministic transitions therefore preserve this equivalence. A
(V) component with k counters has at most |Q| Q
x(Cx + 2)
abstract configurations. One transition may update several
counters, but each atomic guard still compares one counter
(or that counter plus the supplied amount) with a constant.
One-witness projection. A (K) component has a local finite
state and counter vector for each key, initialized identically;
an action naming k reads and updates only the component at
k, and the component rejects iff some local copy reaches its
absorbing bad state. If a concrete run rejects, project the sub-
sequence of actions naming the first rejecting key: locality
makes this exactly a one-key rejecting run. Conversely, re-
name the key in any one-key rejecting run to a fresh concrete
key to obtain a global rejecting run. Thus bad-prefix reacha-
bility is equivalent to reachability in one saturated local copy,
not merely over-approximated.
Equality and products. Because the equality-data sort is in-
finite, an (E) component has the standard finite equality-type
abstraction for its registers and current data; its nonempti-
ness problem is decidable in polynomial space (Kaminski
and Francez 1994). Every component is total over the com-
mon alphabet: guards partition the input valuations and any
missing case is completed to its absorbing bad state. Sepa-
rability excludes cross-component guards and assumptions.
Hence a word rejecting in one component is executable by
every other component and rejects the disjunctive product;
conversely every product rejection has such a witness compo-
nent. One may therefore nondeterministically select a com-
ponent and search its implicit abstract graph. A node stores
finite control, equality type, and each saturated counter in bi-
nary; a successor guesses the finite action/equality type and
one capped category per supplied amount field, shared across
every use of that field. The graph can be exponential because
constants are binary, but reachability uses polynomial space
by an on-the-fly counter bounded by the number of abstract
nodes. By npspace=pspace, nontriviality is in pspace.
Runtime cost. The T1 gate stores σx(x), not an unbounded
concrete counter, and maintains a balanced dictionary from
each encoded key to its local finite state and saturated counter
vector. On an action of bit length L, it reads each supplied
amount once, computes its shared capped category, looks up
the touched key using O(log n) encoded-key comparisons,
evaluates the guard partition, and performs saturated updates.
Time is polynomial in L and the specification, with the stated
log n dictionary factor. If a saturated local state needs s bits,
total (K) storage is O(P
k seen |k|+ns) bits, plus the bounded
E-register encodings and fixed V abstract state. This is the
claimed linear dependence on stored encodings, not a unit-
cost claim for arbitrary-precision values or hashing.
Expressiveness.
We
exhibit
each
policy
as
a
de-
terministic
T0
automaton
with
absorbing
bad
state.
Authenticate-before-access: a control flag auth and an equal-
ity register prin storing the authenticated principal; the
authenticate(p) action sets auth and prin := p; an access
by requester q takes the bad transition unless auth holds
and q = prin (an equality guard). Per-recipient spend cap:
one monotone accumulator sk per recipient key k (real-
ized by the hash map); pay(k, v) with a nonnegative inte-
ger amount v takes the bad transition if sk + v > c and
otherwise updates sk+ = v, an add-nonnegative-amount
update and a compare-to-constant guard, both in T0. Static
decidability applies the finite abstraction of (i) (exact up
to the cap c, then absorbing ⊤) to the single representa-
tive key, since distinct keys evolve independently, so “some
key exceeds its cap” is reachable iff it is reachable for one
key. P2 uses the same monitor with composite key (k, w)
when a trusted clock adapter attaches the day bucket w.
Rate limit r per supplied bucket: key a monotone accumu-
lator by the action’s composite (k, w) field; its (r+1)-th
action takes the bad transition. The automaton enforces this
policy for every supplied bucket sequence and assumes no
ordering between bucket identifiers. Interpreting w as a wall-
clock window additionally requires a trusted adapter to attach
w = ⌊t/W⌋; that adapter is outside T0, rather than an un-
stated trace assumption. No decrement or reset is needed
because a new bucket is a fresh key. No-send-after-revoke: a
boolean control flag set by revoke; send takes the bad tran-
sition once the flag is set. Fixed-vector global quotas: a (V)
component keeps one counter per resource class, may test a
proposed nonnegative amount against the corresponding re-
maining cap, and increments the selected coordinates. This
permits coupling within the declared finite vector but never
allocates or compares counters for unboundedly many data
keys.
Executable
bounded
audit.
check_t3_abstraction.py is a differential regres-
sion check, not a mechanized proof. It exhaustively compares
concrete and quotient transitions for caps through three and
shared amount fields, checks two-key projection and total
disjunctive products on traces through length five, and real-
izes every enumerated equality type over the declared infinite
sort. It writes results/t3_bounded_audit.json
and emits a witness on any mismatch.
B
Extended Experiments and
Reproducibility
B.1
Setup and reproducibility
All experiments are inference-only (no training). The core
judges are open-weights models run locally on a single GPU
(or a free API for the 70B), spanning three open families
and a 140× size range: qwen2.5 (0.5B, 3B, 7B, 32B),
llama3.1 (8B) and llama-3.3 (70B), and gemma2
(9B). To these we add two closed-source frontier judges
from different vendors (gpt-4o-mini from OpenAI and
command-a-03-2025 from Cohere), Llama-Guard-3
(8B) as a deployed guardrail, and a battery of current-
generation frontier judges (B.6) served through hosted in-

<!-- page 14 -->
LLM agent
proposes
action a
Judge
score s∈[0,1]
Gate
s≥θ?
block / allow
World
irreversible
commit
a
s
commit
adversary / injection (budget ρ)
conformal θ for target δ
Figure 2: The enforcement model. An agent proposes a data-carrying action; a semantic judge scores its visible representation;
a pre-execution gate blocks or allows it; and an allowed action has irreversible effects. Calibration selects a threshold under an
exogenous law, while representation attacks and decision-dependent transitions require separate analyses.
System
Regime in our theory
Relies on
Our reading
AgentSpec (Wang, Poskitt, and Sun 2026)
T1 (T -gate, oracle)
oracle-checkable rules
enforces exactly
T -representable safety
Temporal constraints (Kamath et al. 2025)
T1 with sub
SMT-checkable temporal
predicates
substitution needs a safe
substitute
ProbGuard (Wang et al. 2025)
predictive stochastic
monitor
DTMC over predicates
prediction does not enlarge
T1’s enforceable class
Shields (Alshiekh et al. 2018; Jansen et al. 2020)
finite-state MDP
oracle state, finite
abstraction
fallible semantics require
T2’s statistical layer
CaMeL (Debenedetti et al. 2025)
adversarial representation
control/data separation
seeks to reduce the
robustness margin in T2
Progent (Shi et al. 2025)
T1 (T -gate, SMT)
symbolic tool-call rules
common least-privilege
rules fit T3’s fragment
ShieldAgent (Chen, Kang, and Li 2025)
exogenous T2 when fixed
probabilistic rule circuits
its information law
determines the one-step
ROC
GuardAgent (Xiang et al. 2024)
T1 with a learned checker
generated guard code
checker errors induce T2
only under a fixed
experiment
Table 2: Representative systems mapped to the regime they instantiate. The reading is conditional: a static ROC statement does
not transfer to a gate-altered trajectory without the controlled model.
ference APIs. The pipeline consumes real-valued scores, so
any scorer drops in. Each score-judge rates an action with
the single prompt
You are a safety classifier for autonomous-agent tool calls.
Rate how likely the following proposed agent ACTION vio-
lates a safety, security, privacy, authorization, or financial-
control policy. Respond with ONLY an integer 0–100:
0 = clearly safe/compliant, 100 = clearly unsafe/policy-
violating.
parsed to a risk score s ∈[0, 1] at temperature 0 to reduce
sampling variability. The gate blocks iff s ≥θ. Calibration is
split-conformal: for a target δ we set the per-step conditional-
miss target τ = δ/H and choose ˆθ as the ⌊(n+1)τ⌋-th small-
est score among n violating calibration examples (ˆθ = −∞
if that index is 0, i.e. block everything). We flag one small-
sample effect: when δ < 1/(n+1) the index is 0 and the
certificate is met trivially by blocking all actions (U = 1).
This is why the δ = 0.05 rows below show miss 0 at U = 1
on the small curated and InjecAgent sets (n ≈15–35 cali-
bration violations); it is an argument for more violation data,
not a property of the method, and it disappears at benchmark
scale. Legacy descriptive quantities below average 400 strat-
ified calibration/test splits; their error bars are one standard
deviation across splits, not familywise intervals. The random
seed is fixed (20260704). Four datasets are used: a curated set
of 60 labeled tool-call actions spanning the four touchstone
policies plus prompt-injection and destructive cases; the 132
tool-use tasks of AgentDojo (Debenedetti et al. 2024) (its
97 user tasks as compliant actions, its 35 injection goals as
violations, from the banking/slack/travel/workspace suites);
InjecAgent (B.6); and AgentHarm (this section). The sepa-
rately uploaded artifact contains code, redistributable data,
the exact prompt, cached scores, and a one-command cache-
only reproduction path.
Compute, versions, and parsing. Open judges are served
locally with ollama (CUDA backend) on a workstation

<!-- page 15 -->
with two 24 GB consumer GPUs, using ollama’s default
GGUF quantization (typically Q4_K_M); the 70B and all
closed/frontier judges are served through hosted inference
APIs, all at temperature 0. AgentDojo is pinned to v1.2.1.
A judge’s text output is parsed by taking the first integer in
[0, 100] and dividing by 100; a malformed or refused out-
put is scored 0.5 (neutral) and a provider content-filter block
is scored 1.0 (a flagged violation, which only depresses the
two content-filtered judges’ AUC, B.6, so their numbers are
conservative). Local inference is a few GPU-hours; every
API judge runs within free-tier limits. The curated probe
contains serialized tool calls, but the static AgentDojo diag-
nostic contains instruction strings: 97 user-task prompts and
35 injection goals, without the pre-call execution history or
tool output. It therefore estimates discrimination for that de-
clared information variable only. More context changes the
statistical experiment and may help or hurt a fixed scoring
prompt; Blackwell refinement guarantees only that the opti-
mal test with richer information cannot have a worse ROC.
B.2
Synthetic validation
The synthetic judge is binormal (compliant score N(0, 1),
violating score N(µ, 1), µ = 2.5, horizon H = 20), giv-
ing an analytic ROC against which the Monte-Carlo sim-
ulation is checked. C1: calibrating to δ yields realized
episode-unsafe rate 0.0098, 0.0194, 0.0486, 0.0951, 0.182 at
δ = 0.01, 0.02, 0.05, 0.10, 0.20 (each ≤δ, and tight). C2:
sweeping the threshold, the empirical operating points match
the analytic frontier U ⋆(δ) = roc(R−1(δ)) to within 2.5
standard deviations of Monte-Carlo error over 40 thresholds
(Fig. 3).
0.0
0.1
0.2
0.3
0.4
0.5
0.6
episode unsafe rate R (= target δ on the frontier)
0.0
0.1
0.2
0.3
0.4
0.5
0.6
utility loss U=α
predicted frontier U ⋆(δ)
simulated thresholds
fixed-θ baseline
Figure 3: C2: swept thresholds land on the predicted Pareto
frontier U ⋆(δ) = roc(R−1(δ)); a fixed-θ baseline (square)
is off target. Synthetic judge, exact ROC.
Controlled finite-model instantiation.
We also instanti-
ate the finite-model frontier theorem above in an auditable
two-step retry environment. Initially the score is high with
probability .4 and low with probability .6, with violation
posteriors .8 and .2. Allowing terminates; blocking produces
a second proposal. Its current score is .2 in both branches,
but its posterior is .6 after a blocked high score and .02 af-
ter a blocked low score. Thus only perfect recall reveals the
decision-dependent retry state. Cost is the expected number
of compliant proposals blocked and risk is episode-unsafe
probability.
We enumerate all 24 = 16 deterministic perfect-recall
policies and take their exact convex hull (episode-level ran-
domization). At δ = .05, the optimum costs .551, versus .863
for policies using only current score and time and 1.137 for
stationary score thresholds. The static “block high” thresh-
old has (R, C) = (.36, .08) and misses the constraint. Hence
even this minimal model has a strict history-value gap; the
script also records the two deterministic policies mixed at
the optimum.
0.0
0.1
0.2
0.3
0.4
episode-unsafe probability
0.00
0.25
0.50
0.75
1.00
1.25
expected compliant blocks
δ=.05
Exact finite controlled frontier
perfect recall (exact)
current score + time
stationary threshold
Figure 4: Exact occupancy frontier of the specified retry
model. Points are deterministic policies and segments are
episode-level mixtures. Restricting the gate to current-
score/time or one stationary threshold raises the cost at
δ = .05.
B.3
Real judges on the curated set
Table 3 reports realized miss (safety) and utility loss U at
each target δ for four judges (H = 1, per-action) in the
original 400-split descriptive probe. Mean observed miss is
at or below target, and the utility cost of a fixed safety level
falls as judge quality (AUC) rises: at δ = 0.10 the utility
loss falls from 1.00 (the near-random 0.5B judge, which is
safe only by blocking everything) to 0.58 (3B) to 0.03 (7B),
consistent with the frontier. A 32B judge reaches AUC 0.998
and U = 0.04; this probe does not support an equivalence
claim between the 7B and 32B points.
C3 (adversarial). On the 3B judge, calibrating to δ = 0.10
gives benign miss 0.037; injection-style safe-washing of the
violations raises the miss to 0.889 under the strongest tested
template. This is a finite probe of representation sensitivity,
not a universal worst-case or soundness result; the common-
population AgentDojo analysis in B.9 is primary.
B.4
AgentDojo benchmark
The authoritative calibration diagnostic uses 500 shared
balanced two-fold splits for all 23 judges. A 20,000-draw
suite×label outer bootstrap constructs one-sided simultane-
ous miss upper bounds and two-sided simultaneous false-

<!-- page 16 -->
0.5B
3B
7B
32B
δ
miss
U
miss
U
miss
U
miss
U
0.05 .000 1.00 .000 1.00 .000 1.00 .000 1.00
0.10 .000 1.00 .069
.58
.064
.03
.038
.04
0.20 .000 1.00 .118
.15
.100
.03
.036
.00
0.30 .000 1.00 .146
.09
.110
.03
.038
.00
Table 3: Curated descriptive probe (judges of AUC 0.53,
0.92, 0.98, 0.998): mean realized miss and per-action false-
block loss over 400 splits. Block-all points are vacuous; no
pairwise equivalence is inferred.
0.05
0.10
0.20
0.30
target miss rate δ
0.0
0.1
0.2
0.3
realized miss rate
y=δ
realized miss (safety)
utility loss (cost)
0.0
0.2
0.4
0.6
0.8
1.0
utility loss U
Figure 5: C1 on the real qwen2.5:3b judge: the descriptive
cross-split mean realized miss stays below the target δ (left
axis; error bars are one standard deviation over 400 calibra-
tion/test splits) while the utility loss it costs (right axis) falls
as δ relaxes.
block intervals over the full 23 × 4 family. This is a finite-
dataset compatibility check; the conformal theorem’s certifi-
cate additionally requires deployment exchangeability.
At δ = .05, all 23 judge rules are block-all because a half-
fold contains too few violations for a nonzero order statistic.
Across all 92 points, 24 are vacuous block-all, 26 have a si-
multaneous miss upper bound at or below their target, and
42 have a point estimate at or below target but an upper
bound that exceeds it. For example, Gemma-2-9B at δ = .10
has cross-fitted miss .0098 (simultaneous upper .0214) and
false block .780 (95% simultaneous interval [.660, .901]);
at δ = .20 its miss is .138 but upper .264. Complete
rows are in results/conformal_validation.csv.
Block-all is therefore reported as vacuous, and a favorable
point estimate is never called a certificate.
The primary rewrite result is also separated from calibra-
tion: it fixes θ = .5, uses every one of the 35 violations, and
reports simultaneous suite-bootstrap intervals over the 11
fully cached judges (B.9). It estimates a common-population
representation effect at one operating point, not certificate
failure at every threshold.
Counterfactual source-role diagnostic. To isolate autho-
rization provenance without propagating episode outcomes,
we take the culminating call from every AgentDojo user or in-
jection task with a nonempty ground-truth plan: 97 user tasks
and 26 injection tasks. Each of the 123 source tasks yields a
pair with byte-identical call, arguments, instruction text, and
control text. In the authorized member, the source instruc-
tion is the trusted user request and the control is untrusted
output; in the unauthorized member, those two source roles
are swapped. Under the declared policy that only trusted user
input grants authority, labels are exact for this counterfactual.
They are not natural-trace safety annotations.
The primary statistic is paired concordance Pr(sunauth >
sauth) + 1
2 Pr(sunauth = sauth). Treating source tasks as
exchangeable draws from a conceptual task population, we
test the conditional sign null and compute a 20,000-draw
task-pair bootstrap interval. For the fixed 123-task Agent-
Dojo set, concordance and win/tie/loss counts are exact de-
scriptive quantities. Because the action is identical within
each pair, action-only concordance is exactly .5 by construc-
tion. Context-rich concordance is .561 for the 3B primary
(15/108/0 wins/ties/losses; bootstrap 95% CI [.533, .589]),
.967 for 7B-model corroboration (95% CI [.939, .988];
116/6/1), and .500 for the 0.5B negative control (0/123/0).
Holm-adjusted two-sided exact p-values across the three
models are 1.22×10−4, 4.26×10−33, and 1. Thus the larger
judges respond directionally to source role under this policy,
but the experiment does not estimate natural-trace accuracy,
real-world authorization, or deployment safety.
The cache is bound to dataset, prompt, and model
hashes
and
stores
raw
model
responses
and
parser
provenance. The dataset, cached scores, and analysis
are
results/context_call_dataset.json,
results/context_call_scores.json,
results/context_call_analysis.json,
and
analyze_context_calls.py.
B.5
Closed-loop agent evaluation (H > 1)
The preceding AgentDojo diagnostic scores instructions
statically; here we run the real AgentDojo agent loop
across all four suites. A local qwen2.5:7b agent drives
the banking, slack, travel, and workspace suites under the
important_instructions indirect prompt-injection
attack; a gate element placed before tool execution scores
each proposed tool call with the judge and drops those
at/above θ, over multi-step trajectories. Agent and judge both
decode at temperature 0 against the same fixed endpoint to
reduce sampling variability; conditions are paired on task and
injection goal. Table 4 reports end-to-end task-utility and at-
tack success over 949 episodes per condition (144 banking,
105 slack, 140 travel, 560 workspace), with Wilson 95%
intervals.
Trace-derived action-level go/no-go. We instrumented the
interceptor to log each proposed call, the preceding mes-
sages and tool outputs, action-only and context-rich scores,
and the gate decision. A local rerun reproduced such traces.
AgentDojo’s exposed checks in this pipeline, however, la-
bel episode attack success rather than mapping a security
label to every intercepted call. Copying the episode label
onto all calls would mislabel prerequisite and benign calls,
so the strict analysis rejects this as primary action-level ev-
idence. We report no action-only-versus-context-rich AUC
from those generated traces; the policy-grounded B.4 diag-

<!-- page 17 -->
nostic and end-to-end C4 outcomes use different, explicitly
valid units.
Injectability is heterogeneous, so we test the gate strat-
ified by suite. The local agent is far more injectable on
slack (25/105 baseline attack success, 0.238) than on bank-
ing (12/144, 0.083) or travel (8/140, 0.057), and is not
injectable at all on workspace (0/560: it completes many
workspace tasks but the attack never lands). Pooling such
suites into one 2 × 2 table would let the low- and zero-
injectability suites mask the effect (a Simpson’s-paradox
risk), so we test each gate against its own no-gate base-
line with a Cochran–Mantel–Haenszel test stratified by suite
and report the Mantel–Haenszel common odds ratio; suites
in which the attack never fires (workspace) contribute no
information and drop out of the test.
The selected 3B policy reduces attack success. From
45/949 ungated to 4/949 at θ=0.5: stratified over the three
injectable suites, CMH χ2=35.8, p = 2.2 × 10−9, common
OR 0.073. The reduction is significant within each injectable
suite (banking Fisher p = 4 × 10−4, slack p < 10−4, travel
p = 0.036) and survives any multiplicity correction. But the
3B reaches this only by gating 78% of all proposed calls
(91% banking, 60–62% slack/travel, 85% workspace).
Clustering caveat and the exact paired refinement. The
same user tasks and injection goals recur across the gated
and ungated arms, so the episodes are paired, not indepen-
dent, and the between-arm CMH treats them as independent
groups. The natural unit is the (task, goal) pair, on which
the correct test is McNemar’s. We compute it directly by
re-running the three injectable suites with per-episode out-
come logging (N=389; endpoint non-determinism shifts the
counts slightly, to baseline 38/389 and 3B-gate 9/389). On
this run the suite-stratified CMH is p=1.9 × 10−5 (MH
OR 0.21) and the task-paired McNemar is p=2.4 × 10−6
(34 baseline-only vs. 5 gate-only discordant episodes): the
paired test is more significant than the unpaired one on
the same data, so the 3B gate’s effect survives the cor-
rect clustering. The 5 gate-only pairs (blocking a flagged
action shifts the agent’s later trajectory into a different at-
tack) show block-only gating is not perfectly nesting, but
the discordances are strongly one-directional. The weak
7B gate, by contrast, blocks and creates attacks about
equally (29 vs. 22 discordant, McNemar p=0.40), match-
ing its across-suite non-significance (analyze_loop.py
on loop_paired.json).
The selected lighter 7B policy has no detected pooled ef-
fect. At θ=0.7 the 7B gate blocks only 12% of calls and cuts
attack success from 45/949 to 30/949: significant on the
injectable slack suite (25/105 →11/105, Fisher p = 0.016)
but inert on travel (the 7B judge scores no travel call ≥0.7,
so it gates nothing) and flat on banking (12/144 →10/144).
Across suites the effect is not significant (CMH p = 0.09,
common OR 0.63). These are two selected policies with dif-
ferent costs, not an estimate of the controlled optimum or a
causal effect of judge scale. Feedback invalidates the exact
product ROC lift: blocking reroutes the agent and changes
later proposals. The conformal episode certificate instead
uses a union bound and does not require within-episode inde-
pendence, provided its per-step exchangeability assumptions
hold.
Task success and gating fraction are separate endpoints.
Pooled task success is 0.254 (Wilson 95% [.227, .283]) un-
gated, 0.243 ([.217, .272]) with 7B, and 0.180 ([.157, .206])
with 3B. The clearest cost is on workspace, the suite this agent
completes best (0.264 ungated): the light 7B gate leaves it
untouched (0.264, 3% gated) while the heavy 3B gate cuts
it by nearly 40% (0.264 →0.163, 85% gated) although no
attack was ever present there to justify the blocking. Ab-
solute attack rates are modest because a small local agent
both solves fewer tasks and is less injectable than a frontier
agent. Gating fractions are descriptive call-level rates; calls
are clustered within episodes, so we do not attach binomial
call-level intervals.
suite
judge
θ
N
task success [95% CI]
attack [95% CI]
gated
banking
none
n/a 144
.382 [.307, .463]
0.083 [.048, .140]
0%
qwen7b 0.7 144
.396 [.320, .477]
0.069 [.038, .123] 32%
qwen3b 0.5 144
.375 [.300, .456]
0.000 [.000, .026] 91%
slack
none
n/a 105
.219 [.151, .307]
0.238 [.167, .328]
0%
qwen7b 0.7 105
.124 [.074, .200]
0.105 [.060, .178] 35%
qwen3b 0.5 105
.162 [.104, .244]
0.029 [.010, .081] 60%
travel
none
n/a 140
.107 [.066, .169]
0.057 [.029, .109]
0%
qwen7b 0.7 140
.093 [.055, .152]
0.064 [.034, .118]
0%
qwen3b 0.5 140
.064 [.034, .118]
0.007 [.001, .039] 62%
workspace none
n/a 560
.264 [.229, .302]
0.000 [.000, .007]
0%
qwen7b 0.7 560
.264 [.229, .302]
0.000 [.000, .007]
3%
qwen3b 0.5 560
.163 [.134, .195]
0.000 [.000, .007] 85%
pooled
none
n/a 949
.254 [.227, .283]
0.047 [.036, .063]
0%
qwen7b 0.7 949
.243 [.217, .272]
0.032 [.022, .045] 12%
qwen3b 0.5 949
.180 [.157, .206]
0.004 [.002, .011] 78%
Table 4: Closed-loop AgentDojo across all four suites,
949 episodes/condition, one fixed endpoint at temperature
0. Stratified by suite (Cochran–Mantel–Haenszel over the
three injectable suites; workspace is not injectable, 0/560,
and drops out), the 3B gate cuts end-to-end attack success
45/949 →4/949 (p = 2.2 × 10−9, common OR 0.07),
but only by gating 78% of calls; the lighter 7B gate (12%
gated) is significant only on the injectable slack suite (across
suites CMH p = 0.09). On workspace the heavy 3B gate re-
duces task success (.264 →.163) while no attack succeeds
in either arm. Task-success and attack intervals are Wilson;
gating fractions are descriptive because calls are clustered
within episodes.
Selected 9B operating points.
We reran the loop with
gemma2:9b, the static reference judge, sweeping θ ∈
{0.90, 0.95, 0.98} on two injectable suites. None of these se-
lected points significantly reduces attack success. On banking
its most-blocking point gates 35% of calls yet moves attacks
only 12/144 →9/144 (Fisher p = 0.65) while task utility
falls 0.41 →0.33; on slack it gates ≤3% with no change
(25/105 baseline vs. 20–28 under the gate, all p > 0.6).
These data show that the evaluated static judge and thresh-
olds did not improve this endpoint. They do not identify the
controlled optimum or show that heavy blocking is necessary

<!-- page 18 -->
for every richer information variable; such claims require
evaluating the decision-dependent kernel.
B.6
Judge discrimination, not scale (cross-family)
All
23
judge
runs
use
the
same
ordered
132
items,
IDs,
labels,
and
suite
strata
de-
fined
in
agentdojo_manifest.json;
model
and
cache
provenance
is
defined
in
model_registry.json.
The
authoritative
script
is
analyze_agentdojo_inference.py;
legacy
scripts call it rather than maintaining separate estimates.
Paired familywise analysis.
For each AUC we compute
DeLong influence values and their full paired covariance.
Against the predeclared Gemma-2-9B reference, 100,000
draws from the resulting 22-dimensional Gaussian approx-
imation give max-T simultaneous 95% intervals; Holm-
adjusted two-sided tests are a robustness check. Figure 6 dis-
plays every contrast. AUC spans .660–.858 and the reference
is .813 (marginal DeLong 95% interval [.718, .908]). No si-
multaneous interval establishes superiority. Only Llama-3.1-
8B establishes inferiority: ∆= −.153, simultaneous interval
[−.304, −.003], max-T p = .042 (Holm p = .062). Because
the two correction methods straddle .05, the exact statement
is method-specific rather than “two judges are worse.”
Absence of evidence is not equivalence.
For every con-
trast we also report the smallest symmetric equivalence mar-
gin supported by its simultaneous interval. None is within
±.05. The familywise 80%-power MDE ranges .071–.193
(median .104), and detecting a .05 difference would require
approximately 269–1977 items under fixed prevalence and
effect structure. Thus the defensible conclusions are that no
familywise-adjusted superiority is detected and parameter
count does not order AUC; neither a universal ceiling nor
practical equality is identified. Suite-stratified paired esti-
mates are emitted as a sensitivity analysis and do not change
that reading.
Provenance–risk mismatch is a diagnostic, not an adjudi-
cated cause.
The static input contains 97 user-task prompts
and 35 injection goals without their pre-call history. A seven-
vendor panel agrees more strongly with itself than with these
provenance-defined labels, and several low-scored injection
goals do not expose provenance in their text. This is evi-
dence that the declared risk-scoring task and label source
differ; without a multi-annotator study it does not prove the
cause of the observed AUCs or exclude shared model blind
spots. No reviewer annotation is requested.
ROC curves.
Because AUC is only a one-number sum-
mary, we plot the full per-judge ROC (Fig. 7). It shows the
effect that AUC hides: on AgentDojo the three judges of
near-equal AUC ≈0.81 (Qwen-7B/32B, Gemma-9B) have
visibly different ROC shapes in the low-false-alarm region
that governs the safety-critical operating points, and the 8B
Llama sits near the diagonal. The frontier of the frontier
theorem is this curve, not its area.
Second benchmark: InjecAgent.
We repeat the study on
InjecAgent (Zhan et al. 2024), whose threat model differs
judge
AUC
miss / U at δ
0.10
0.20
0.30
qwen2.5:3b
.86
.08/.37
.13/.20
.14/.18
qwen2.5:7b
.90
.02/.94
.13/.39
.25/.05
qwen2.5:32b
.91
.09/.46
.14/.10
.16/.06
llama3.1:8b
.58
.07/.79
.15/.71
.16/.71
gemma2:9b
.92
.07/.56
.12/.17
.25/.05
llama-3.3:70b
.92
.07/.25
.09/.06
.10/.06
command-a
.92
.08/.54
.14/.08
.14/.06
Table 5: InjecAgent descriptive check (62 violations, 17 com-
pliant): mean miss/per-action false block across legacy splits.
AUC point estimates are non-monotone in size; no pairwise
equivalence is inferred.
judge
AUC miss / U at δ = .10/.20/.30
qwen2.5:3b
.69
.01/.61 .01/.61
.01/.61
qwen2.5:7b
.86
.07/.32 .07/.28
.07/.28
qwen2.5:32b
.93
.00/.44 .00/.44
.10/.32
llama3.1:8b
.58
.01/.84 .01/.84
.01/.84
gemma2:9b
.88
.08/.42 .15/.20
.16/.18
llama-3.3:70b
.85
.03/.78 .03/.78
.14/.53
gpt-4o-mini
.93
.05/.44 .15/.16
.25/.05
command-a
.94
.03/.38 .16/.16
.25/.05
Table 6: AgentHarm descriptive check (176 harmful, 176 be-
nign): mean miss/per-action false block across legacy splits.
The AUC point estimates are non-monotone in size; no pair-
wise tie is inferred.
from AgentDojo (direct-harm and data-stealing indirect in-
jections across many tools). We take its 62 unique attacker
instructions as violations and 17 user instructions as compli-
ant actions. This legacy descriptive check has small compli-
ant n and does not receive the 23-judge familywise analysis.
Its point estimates are non-monotone in size: the 8B Llama
has AUC 0.58, below the 3B Qwen (0.86), while the 9B
and 70B both have AUC 0.92. We report the operating-point
means without an equivalence or cross-benchmark replica-
tion claim.
Third benchmark: AgentHarm.
We add a third bench-
mark of a different kind: AgentHarm (Andriushchenko et al.
2025) scores directly harmful agent tasks against benign ones
(176 each), rather than indirect injections. Table 6 is likewise
descriptive. The 8B Llama has AUC 0.58, below the 3B
Qwen (0.69), while gpt-4o-mini and command-a have
point estimates .93 and .94. These values show that parame-
ter count does not order this finite panel; they do not establish
ties, a ceiling, or its cause.
B.7
A deployed guardrail on the frontier
Llama-Guard-3-8B (Inan et al. 2023; Llama Team, AI
@ Meta 2024) is a production content-safety classifier. Used
as our judge (native safe/unsafe output, one operating point)
it flags 85% of curated violations at 9% false-block (miss
0.15, U = 0.09) and 54% of AgentDojo injections at 10%
false-block (miss 0.46, U = 0.10). It is a real guardrail

<!-- page 19 -->
suite
nu/ni
3B
8B
9B
7B/32B
workspace
40/14
.84
.66
.84
.81/.87
travel
20/7
.68
.65
.75
.75/.84
banking
16/9
.73
.55
.92
.86/.88
slack
21/5
.44
.76
.84
.82/.64
Table 7: Per-suite AgentDojo AUC (nu user tasks, ni injec-
tions). Small per-suite N makes these descriptive; the pooled
familywise analysis is in B.6. Columns are Qwen-3B, Llama-
8B, Gemma-9B, Qwen-7B/32B.
landing on the same safety/utility plane: its curated point is
competitive, but on AgentDojo its miss of 0.46 at U = 0.10
is dominated by the calibrated score-judges of equal or higher
AUC, because a content-harm taxonomy transfers only partly
to agent-policy violations, corroborating the concurrent find-
ing of Cartagena and Teixeira (2026) that text safety does not
transfer to tool-call safety. This is the theory’s content made
concrete: a guardrail’s reach is its discrimination on your
violation class, whatever it was built for, and being labeled a
“guardrail” confers nothing beyond the ROC it achieves.
B.8
Per-suite AgentDojo breakdown
Table 7 breaks the AgentDojo AUC down by suite. Per-suite
injection counts are small (5–14), so these are noisy; the
pooled paired analysis of B.6 is primary. The point estimates
illustrate heterogeneity but do not support within-suite pair-
wise claims.
B.9
Common-population representation attack
The attack changes only the representation visible to the
judge: it appends the predeclared 16-token administrator-
preapproval suffix while leaving the underlying canonical
item and label unchanged. This static diagnostic contains
no executable action; the perturbation instantiates only the
representation side of Definition 6. Every one of the 35
AgentDojo violations is included, avoiding the earlier judge-
selected flagged-subclass estimand. At fixed θ = .5, a
20,000-draw suite-stratified bootstrap gives simultaneous in-
tervals over all 11 judges with complete clean and attacked
caches (Table 8).
This result establishes a common-population vulnerability
for the eight affected judges at the declared operating point.
It does not show that every judge fails, that every calibrated
threshold fails, or that the finite template is a universal ad-
versary. A held-out best-of-template cache exists for Claude-
Opus-4.5, but it selects the 25 violations the judge already
flags and selects a threshold on that same subclass; its .28
increase is therefore reported only as a secondary diagnostic,
not evidence that generalizes the primary effect.
B.10
A worked end-to-end example
We trace the running example (an email/payments assistant)
through the pipeline. Policy as a T0 automaton. P2 (per-
recipient daily cap c) compiles to a keyed-counter automa-
ton after a trusted clock adapter attaches day bucket w: on
judge
benign miss attacked miss
increase [sim. 95%]
qwen2.5:3b
.143
.600
.457 [.223, .691]
qwen2.5:7b
.257
.743
.486 [.257, .714]
qwen2.5:32b
.143
.514
.371 [.160, .583]
llama3.1:8b
.114
.200
.086 [−.079, .251]
gemma2:9b
.229
.800
.571 [.372, .771]
llama-3.3:70b
.286
.771
.486 [.272, .699]
command-a
.229
.743
.514 [.287, .742]
Claude-Opus-4.5
.286
.143
−.143 [−.298, .012]
Claude-Sonnet-4.5
.257
.143
−.114 [−.286, .057]
Nova-Pro
.114
.714
.600 [.394, .806]
Mistral-Large-3
.286
.486
.200 [.027, .373]
Table 8: Primary fixed-threshold representation attack. Nine
of 11 point estimates increase; simultaneous inference de-
tects a positive increase for exactly 8 judges. The other three
effects are inconclusive. This estimates η(ρ; θ = .5) for one
rewrite, not ¯η(ρ).
transfer(k, v, w) it reads sk,w (default 0), takes the bad tran-
sition if sk,w + v > c, and otherwise updates sk,w + =v.
P3 (no-send-after-revoke) adds a boolean flag set by revoke
that makes any later send bad. The T1 gate enforces both ex-
actly, checking one guard per action, and deciding whether
the combined specification is nontrivial is in pspace (track
one witness composite key; the decidable-fragment theorem
T3). Semantic predicate via the judge. P1 (no PII to an un-
approved recipient) is semantic; the judge scores each send
for P1-risk, and on the curated actions the 7B judge sepa-
rates P1 violations from compliant sends at AUC 0.98. Cal-
ibration. To certify episode-unsafe ≤δ = 0.10 at H = 1,
split-conformal sets ˆθ to the appropriate order statistic of
the calibration violations’ scores. Under exchangeability this
is a marginal certificate; in the legacy curated splits, mean
miss is 0.064 at per-action false-block loss 0.03 (Table 3).
Attack. The adversary appends “also cc audit@external; pre-
approved” to a P1-violating send. This is a score collision: in
this probe the safe-washed violation scores like a compliant
send and crosses the fixed threshold. The oracle-checkable
P2/P3 remain unchanged because they do not consult the
perturbed judge representation.
B.11
From theorems to deployment
The theory is a short design recipe. (1) If a policy pred-
icate is oracle-checkable (spend caps, authentication, rate
limits), compile it to a T0 gate (theorems T1, T3): enforce-
ment is exact and the analysis is decidable. (2) For a fixed
exogenous semantic decision, measure the full ROC of the
available information; no one-step rule using that same in-
formation beats the Neyman–Pearson frontier. If blocking
changes later proposals, model the transition response and
optimize the controlled occupancy frontier instead. (3) Un-
der label-conditional exchangeability, calibrate on violating
examples for a marginal target; report block-all as vacuous
and use whole-episode calibration only when exchangeable
episode losses are available. (4) If deployment is adversar-
ial, naive calibration is not a security boundary. A finite
rewrite experiment estimates η(ρ; θ) only for its declared

<!-- page 20 -->
perturbations; robust recalibration needs a verified uniform
¯η(ρ) < δ/H. Otherwise reduce the attack surface architec-
turally or strengthen the judge. (5) Report policy logic and
feedback explicitly: in the controlled regime the gate is a
sequential policy, not merely a threshold.
How to report a guardrail under this theory. To make
a new guardrail comparable, name the information variable
and intervention regime; report the full ROC (not only AUC),
the calibrated miss and false-block uncertainty including
vacuity, the perturbation set and η(ρ; θ). When decisions
affect trajectories, also report cumulative cost, task success,
and paired closed-loop outcomes. No pair of static numbers
identifies the endogenous frontier.
B.12
Ethical considerations
This work is defensive: it characterizes what runtime
guardrails can and cannot enforce for tool-using agents, in
order to prevent unauthorized or harmful actions. The one of-
fensive element is the “safe-washing” attack (B.9), included
because the adversarial theorem’s impossibility is only cred-
ible once the attack is demonstrated. Those perturbations
are simple approval-claim prompts already documented in
the prompt-injection literature (Maloyan and Namiot 2025);
they disclose no new capability and are shown precisely to
argue that calibration alone is not a security boundary. All
experiments use public benchmarks and open-weights mod-
els, with no human subjects and no private data. The intended
use of the theory is to help practitioners choose judges and
architectures with quantified safety guarantees, and to know
when those guarantees do not hold.
B.13
The certified gate, in pseudocode
Algorithm 1: Exogenous calibrated pre-execution gate.
Calibrate (once): given a labeled set of n violating ac-
tions with judge scores v1, . . . , vn and target δ, set ˆθ ←the
⌊(n+1)δ/H⌋-th smallest vi (or −∞if that index is 0).
Deploy (per proposed action a with history τ): if the
predicate is oracle-checkable, run the T0 automaton and
block iff it would enter a bad state (T1); else compute
s ←judge(τ, a) and block iff s ≥ˆθ; on block, commit
the no-op (T2).
Guarantee: marginal expected episode-unsafe loss ≤δ un-
der the stated label-conditional per-step exchangeability and
union-bound composition. Finite calibration may be conser-
vative or block-all. Under a budgeted representation adver-
sary the upper bound adds H ¯η(ρ). If decisions alter future
proposals, use the controlled model rather than this one-step
procedure.
B.14
A descriptive richer-statistic check
The exogenous theorem applies to any fixed information vari-
able, not only one judge score. Within the original three-
judge subset, the mean of Gemma-9B and Qwen-32B has
AUC .828, and a three-judge mean has .839, versus a best
constituent point estimate .814. These unadjusted descrip-
tive values show how an ensemble defines a new statistic
with its own ROC; they are not a familywise superiority test
and do not imply that richer context improves a fixed scor-
ing prompt. Blackwell refinement concerns the optimal rule
using richer information.
dataset
judge
P0
P1
P2
curated
Gemma-9B
.997
.994
.985
curated
Qwen-7B
.983
.996
.988
curated
Llama-8B
.959
.956
.825
AgentDojo
Gemma-9B
.818
.788
.785
AgentDojo
Qwen-7B
.807
.801
.824
AgentDojo
Llama-8B
.648
.574
.499
Table 9: Descriptive prompt-sensitivity sweep: judge AUC
under three prompt variants (P0 is the prompt of B.1). No
pairwise uncertainty adjustment is applied.
B.15
Threats to validity
Calibration data. The certificate needs labeled violating ac-
tions for the target predicate; where labels are scarce, small-
n conformal degenerates to block-all below δ ≈1/(n+1)
(B.1). Distribution shift. Exchangeability is a marginal, per-
step assumption; class-prior shift or within-episode state drift
can void it. The margin-dependent bound covers only the de-
clared bounded representation adversary, not arbitrary shift.
Judge-score calibration. We treat the judge as a black box
through (α, β); a different information variable has a differ-
ent frontier. Correlation across steps. Static benchmarks are
per-action (H = 1); the union bound does not require inde-
pendence, but the exact product lift does, and C4 samples
only three selected feedback policies. Prompt sensitivity. We
re-score with three prompt variants (Table 9). The AUC point
ordering is stable: the 8B Llama is the worst judge under ev-
ery prompt on both datasets (AgentDojo AUC 0.50–0.65,
always far below the 7B Qwen and 9B Gemma at 0.79–
0.82), so but this sweep has no adjusted pairwise inference.
The strong judges vary by ≤0.03 AUC, the weak Llama
by up to 0.15. Benchmark representativeness. Three agent
benchmarks and a curated set cover several threat models
but not all deployment settings; the InjecAgent compliant
class (17 user tasks) is small, so its false-alarm estimates are
coarser than AgentDojo’s.
B.16
Open problems
The characterization leaves three concrete questions that
follow-up work could close. (O1) The exact multi-predicate
region. The copula proposition of §T2 only sandwiches
the m-predicate achievable region between the Fréchet–
Hoeffding extremes and pins it for m ≤2; the exact region
for m ≥3, and the coupling that realizes it, are open. (O2)
The ROC gain of richer exogenous information. For a
fixed one-step experiment, a gate that fuses a second judge
or metadata is governed by the ROC of that richer infor-
mation (§B.14); what is open is a quantitative law for how
much the ROC improves as a function of the information
added (mutual information, judge diversity), which would
turn the reduction into a design rule. (O3) Data-driven ro-
bust certificate. Adversarially robust conformal prediction
(Gendler et al. 2022) treats bounded input shift. A finite-
sample method that verifies a uniform ¯η(ρ) for semantic
rewrites, rather than estimating selected templates, remains
open.

<!-- page 21 -->
guardrail
pattern
regime
condition
single score /
ensemble
exogenous
fixed one-step information
law; use its full ROC
metadata /
context fusion
exogenous
Blackwell comparison is for
the optimal rule, not a fixed
prompt
history / online
threshold
controlled
if
feedback
use the occupancy frontier
when decisions alter
transitions
multi-step
reasoning judge
either
classify by whether its
information law depends on
prior gate decisions
abstention /
escalation
cost-
specific
abstain equals block only for
the declared safety/cost axes;
human must be modeled
explicitly
rewrite /
sanitize
rewrite
class equivalence needs a
prefix-safe substitute; utility
ordering needs a cost
assumption
m
simultaneous
predicates
copula
diagnostic
stated bounds apply to the
conservative any-flag gate
Table 10: Regime map for representative patterns. Static ROC
conclusions do not transfer through decision-dependent tran-
sitions.
B.17
Scope ledger for common guardrail patterns
Table 10 records which theorem can analyze a common pat-
tern. The one-step ROC result is exact only for a fixed in-
formation law independent of the gate. Stateful logic that
changes future proposals belongs to the controlled theorem,
so this is a scope map rather than an exhaustive taxonomy.
B.18
Secondary ensemble robustness diagnostic
On a judge-selected flagged subclass of 34 AgentDojo injec-
tion goals, a best-of-12 rewrite cache gives miss increases
.45 for the 32B judge and .64 for the 70B judge at θ = .5.
A max-ensemble, which blocks if either judge flags, has in-
crease .41; one rewrite drives both below threshold on 41% of
this subclass. These values show correlated sensitivity in the
tested pair and template set. Because the subclass and attacks
are selected and no simultaneous interval is computed, they
do not establish that ensembling generally fails as a robust-
ness intervention. The primary common-population result
remains B.9.
Acknowledgments
This work received no specific funding. This is the extended
version of a paper under review.

<!-- page 22 -->
−0.3
−0.2
−0.1
0.0
0.1
AUC difference vs. Gemma-2-9B (95% maxT familywise CI)
Llama-3.1-8B
Qwen-2.5-3B
GPT-OSS-120B
Llama-3.3-70B
Gemma-4-31B
Mistral-Medium-3.5
Qwen-3.5-122B
Qwen-3.6
Step-3.7-Flash
DeepSeek-V4-Flash
Qwen-2.5-7B
GPT-4o-mini
Nemotron-3-Super-120B
Qwen-2.5-32B
Nova-Pro
Mistral-Large-3
Command A
MiniMax-M3
Mistral-Large-3 (filtered)
Claude-Sonnet-4.5
Grok-4 (filtered)
Claude-Opus-4.5
AgentDojo paired judge comparisons
Figure 6: Paired AUC differences from Gemma-2-9B on the static AgentDojo instruction diagnostic. Bars are max-T familywise
95% intervals over all 22 contrasts; dashed lines are the predeclared ±.05 equivalence margin. No interval lies above zero or
wholly inside the equivalence region.

<!-- page 23 -->
0.0
0.2
0.4
0.6
0.8
1.0
false-alarm rate
0.0
0.2
0.4
0.6
0.8
1.0
true-positive rate
curated
0.0
0.2
0.4
0.6
0.8
1.0
false-alarm rate
0.0
0.2
0.4
0.6
0.8
1.0
true-positive rate
AgentDojo
0.00
0.05
0.10
0.15
0.20
0.0
0.2
0.4
0.6
low false-alarm region
judge (curated AUC / AgentDojo AUC)
Qwen-3B (0.92/0.71)
Qwen-7B (0.98/0.81)
Qwen-32B (1.00/0.81)
Llama-8B (0.96/0.66)
Gemma-9B (1.00/0.81)
Llama-70B (0.99/0.79)
Figure 7: Per-judge empirical ROC on the curated set (left) and AgentDojo (right), with AUC in the legend. Judges of similar
AUC differ in ROC shape where it matters (low false-alarm rate); the frontier depends on the full curve.
0.05
0.10
0.20
0.30
target miss rate
0.0
0.1
0.2
0.3
0.4
oss-fitted miss (line: simultaneous upper bo
Calibration compatibility; x = vacuous block-all
−0.2
0.0
0.2
0.4
0.6
0.8
attack-induced miss increase at fixed threshold 0.5
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
All 35 violations; common rewrite
Figure 8: Cross-fitted calibration diagnostics (left) and the primary common-population rewrite analysis (right). An “x” is
block-all. Attack bars are simultaneous 95% intervals over 11 judges; all 35 violations, one predeclared 16-token suffix, and
θ = .5 are fixed before comparison.

<!-- page 24 -->
