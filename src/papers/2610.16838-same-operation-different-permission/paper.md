> PDF 文本抽取（pymupdf），保留 `<!-- page N -->`；表格/公式可能有版式噪声，引用前回 PDF 核。

<!-- page 1 -->
Same Operation, Different Permission: Evaluating Whether Guardrails
Honor Authorization
Huihao Jing *, Shaojin Chen *, Wenbin Hu , Yuxuan Liu , Haochen Shi ,
Zhongwei Xie , Haoran Li
† , Yangqiu Song
HKUST
hjingaa@connect.ust.hk
Abstract
As language-model agents write code, move
money and change records on behalf of users,
deciding whether an action is authorized has
become a central safety problem. Guardrails
are often placed in front of these actions, yet
few evaluations ask whether their decisions fol-
low authorization: blocking unauthorized ac-
tions while still allowing the same actions under
valid permission. We introduce Authorization-
Pairs, a benchmark that contrasts authorization
evidence for the same operation in its language
track. It combines expert-annotated natural-
language scenarios with executed and veri-
fied operations, plus externally sourced native-
policy requests.
AuthorizationPairs checks
each decision for correctness, usability and re-
sulting effect, and tracks each request across
guardrail changes. Our experiments show that
many blocked operations stem from failed re-
views, not correct denials. Repairing the output
format restores usable decisions but changes
which authorized requests are honored, and
adding a second reviewer removes some errors
while rejecting valid authorization. Guardrails
should therefore be evaluated on both the unau-
thorized actions they stop and the authorized
actions they let through.
1
Introduction
Language-model agents now act for users in real
systems. A coding agent may push commits to
a shared repository. A customer-service assistant
may issue a refund. Such agents often hold broad
credentials, and a single wrong action can move
money or leak private data before anyone notices.
The same action can be acceptable or forbidden
depending on authorization. A refund is allowed
under an active delegation but forbidden after its
revocation. Access-control systems encode such
*Equal contribution.
†Corresponding author.
rules as policies, evaluated separately from enforce-
ment (Hu et al., 2014; OASIS, 2013; Cutler et al.,
2024). A guardrail in front of an agent faces the
same decision. Both kinds of error are costly. Ap-
proving an unauthorized action can cause financial
loss or a data breach. Rejecting an authorized ac-
tion blocks legitimate work. Frustrated by repeated
false denials, users may disable the guardrail or
grant broader permissions, losing protection alto-
gether.
Existing evaluations cover parts of this prob-
lem.
AgentDojo and SafeArena measure secu-
rity and task outcomes (Debenedetti et al., 2024;
Tur et al., 2025), while Agent-SafetyBench pro-
vides interactive safety tests (Zhang et al., 2024).
ST-WebAgentBench credits only policy-compliant
task completions (Levy et al., 2026).
Context-
and permission-aware benchmarks score model
answers to individual queries (Sun et al., 2025;
Klisura et al., 2026; Sanyal et al., 2025). Our eval-
uation connects three requirements. First, permis-
sion contrasts keep the complete operation fixed.
Context-sensitive evaluations already study chang-
ing contexts, and we link permission evidence to
review decisions and executed effects. Second,
prevention totals alone cannot distinguish correct
denials from blocks caused by unusable reviews,
although these failures need different fixes. Third,
guardrail changes require request-level compar-
isons beyond aggregate totals (Xiang et al., 2025;
Wang et al., 2026; Greenblatt et al., 2024; Terekhov
et al., 2025). A change can raise the number of com-
pleted lawful requests while rejecting previously
successful ones.
We introduce AuthorizationPairs to close these
gaps. Its language track has fifty scenarios. Each
scenario places one operation in four contexts: two
lawful and two forbidden. Three security experts la-
beled all 200 contexts independently. Each allowed
operation runs in a local environment, and indepen-
dent checks confirm its effect. The native-policy
1
arXiv:2610.16838v1  [cs.AI]  12 Oct 2026

<!-- page 2 -->
track adds 1,594 OpenFGA and Cedar requests
from public sources, labeled by the policy engines
themselves. We record correctness and usability
for every decision, and verify application effects
in the language track. Stable request identifiers
across experiments reveal the exact requests helped
or hurt by each change.
We use AuthorizationPairs to answer three ques-
tions. RQ1: Do guardrail decisions follow autho-
rization? RQ2: Is a blocked operation a correct de-
nial or a failed review? RQ3: Do interface repairs
and extra reviewers keep honoring valid authoriza-
tion? We evaluate eight guardrail configurations.
We then compare four review interfaces on two
models with three seeds each. On the native-policy
track, we also combine three reviewers in fifteen
orders. Our contributions are:
1. Same action, different permission. Our lan-
guage track holds the complete operation fixed
and contrasts lawful and forbidden evidence,
so an always-allow or always-block reviewer
cannot score well. Executing and checking
language-track decisions ties each judgment
to a real effect.
2. Blocked does not mean denied. We record
decision usability separately from correctness.
Structured review leaves 117 to 124 of 160
inputs without a usable decision for Qwen3.5-
9B. For Qwen3.5-27B, the number is 48 to 50.
Each such failure stops the operation. Schema
decoding makes every decision usable in all
six runs, revealing the permission judgments
underneath.
3. Totals hide which requests a change breaks.
Following each lawful request shows what to-
tals hide. In five of six runs, moving from
direct review to schema decoding recovers
some lawful requests while losing others, with
net changes from −3 to +27. On the native-
policy track, adding Safeguard after Qwen3.5-
27B removes one incorrect approval but ve-
toes 171 lawful requests. From these records
we derive acceptance criteria for guardrail
changes.
2
Related Work
Access control and policy language.
Access-
control research established least privilege and
consistent, policy-based decisions (Saltzer and
Schroeder, 1975; Pang et al., 2019; Cutler et al.,
2024). Later work translates natural-language re-
quirements into formal rules (Lawal et al., 2024;
Vatsa et al., 2026; Wessner et al., 2026). Role-
Conditioned Refusals, OrgAccess and FraudBench
test whether language models respect permissions
in database, organizational and banking settings
(Klisura et al., 2026; Sanyal et al., 2025; Pai
and Xian, 2026). Our language track links fixed-
operation permission contrasts to usable review
decisions, verified effects and request-level inter-
vention records.
Guardrails and agent evaluation.
GuardAgent
and AgentSpec enforce safety rules on agent ac-
tions, and PolicyGuardBench checks trajectories
for policy compliance (Xiang et al., 2025; Wang
et al., 2026; Wen et al., 2025). AgentDojo and
SafeArena jointly evaluate security and task behav-
ior, while Agent-SafetyBench tests broader inter-
active safety risks (Debenedetti et al., 2024; Tur
et al., 2025; Zhang et al., 2024). ToolEmu emulates
tools to expose risky agent behavior (Ruan et al.,
2024). ST-WebAgentBench credits completions
that respect the applicable policies (Levy et al.,
2026). Our focus is narrower. We study how a
reviewer judges one operation under contrasting
permissions, and we track decision availability and
request identity across guardrail changes.
Contrastive testing and oversight.
Contrast
Sets perturb test instances to probe a model’s local
decision boundary (Gardner et al., 2020). Check-
List, metamorphic testing and access-control veri-
fication define expected relations between related
inputs (Ribeiro et al., 2020; Chen et al., 1998; Hu
et al., 2017). We apply the same idea to permission
evidence. AI control and Control Tax study audit-
ing, fallback and the cost of oversight (Greenblatt
et al., 2024; Terekhov et al., 2025). Our request-
level records make decision availability explicit
and separate output failures from usable denials.
3
The AuthorizationPairs Benchmark
3.1
Case format
Both tracks use a common case contract, with an
optional application effect:
(request, policy, evidence, effect, source).
The request names the subject, action, arguments,
resource, environment and purpose. The policy
and evidence keep their original text. The effect
describes a local operation for language cases, and
2

<!-- page 3 -->
the source records provenance. Native-policy cases
are decision-only and have no application effect.
A case is lawful if the policy permits the request
under the evidence and forbidden otherwise.
In the language track, each scenario keeps the
request, policy and effect fixed and changes only
the authorization evidence across four contexts. A
variant may change the scope, status or issuer of
a grant, or add irrelevant evidence. Because the
operation never changes, a reviewer that always
approves or always rejects fails half of the con-
texts. Scenarios cover delegation limits, handoffs,
withdrawals and representative authority.
The two lawful contexts of a scenario often grant
permission through different paths, for example an
active grant in one and an accepted handoff in the
other. A reviewer may accept one path and reject
the other. The backend can still run the operation,
yet one valid authorization no longer enables it.
Stable scenario and request identifiers let us detect
such cases after every change.
Models receive the public policy, request and ev-
idence through each configuration’s interface. Ref-
erence labels and scoring annotations stay hidden.
Every input is stored with its hash, so each record
shows exactly what the reviewer saw.
The fixed operation includes its arguments.
Changing a payment amount, recipient or deploy-
ment artifact changes the request itself. Our con-
trasts instead change the evidence that permits that
complete request. This controls for the operation’s
content: a reviewer cannot pass by learning that re-
funds, deployments or data transfers should always
be blocked. It must use the grant, scope and status
supplied in the context. A lawful and a forbidden
context therefore test opposite sides of one permis-
sion boundary while leaving the backend’s ability
to perform the operation unchanged.
The recorded policy and evidence identify which
permission route a false denial rejects. Matching
that request across interventions provides a targeted
regression test: a repair must preserve its valid au-
thorization while rejecting its forbidden counter-
part.
3.2
Reference labels
Three annotators with experience in security and
access control labeled every language context as
lawful or forbidden. They worked independently
from a shared guideline (Appendix B). Each anno-
tator saw the same policy, request and evidence as
the models, without other labels or model predic-
tions. All three agreed on 186 of the 200 contexts
(Fleiss’ κ = 0.91). We form initial majority labels,
then adjudicate disagreements through discussion.
Adjudication of the 14 non-unanimous contexts
changed 3 initial majority labels. The final labels
match the frozen scoring references case by case,
so all reported scores retain the same reference.
The annotators also wrote interpretation notes for
67 contexts.
To check internal consistency, we encoded the
labels as fifty policy expressions over typed facts
linked to source spans.
Two separately imple-
mented evaluators reproduce all 198 determinate
labels. The other two contexts retain lawful ex-
pert labels but remain unresolved under the stricter
encoded reading of an approval’s issuer. We also
report results excluding them (Appendix B). An
automated annotation pass serves as an extra check
and changes no label (Appendix B.2).
3.3
Native-policy track
The native-policy track reuses public OpenFGA
and Cedar examples without modification. It con-
tains 1,594 distinct requests from 47 source appli-
cations and sixty policy encodings. In 23 groups,
the same policy and query appear with both lawful
and forbidden states. We split connected groups
of source applications and shared policy encod-
ings. This gives 379 development and 1,215 test
requests. The native engines reproduce every refer-
ence label (OpenFGA Contributors, n.d.b,n; Cedar
Policy Contributors, n.d.b). Models see the pol-
icy, request and state, but not the expected answer.
Appendix B.3 gives source details and engine ver-
sions.
3.4
Execution and effect checks
In the language track, an enforcement point re-
ceives the reviewer’s decision and a description of
the effect. It never sees the reference label. An
ALLOW decision runs the operation in a local envi-
ronment. Any other output, including an unusable
one, leaves the operation unexecuted. The nine
effect types range from ledger transfers and code
deployment to document signing and file delivery.
Independent checks read back balances, database
rows, file bytes and signatures, and all 1,600 orig-
inal effects match the dispatched decisions. The
task is therefore permission review for a given op-
eration, not planning or tool choice. We record
three outcomes separately: the correctness of the
judgment, the availability of a usable decision and
3

<!-- page 4 -->
the resulting effect. A usable decision can still be
wrong, and an unusable one blocks execution with-
out judging anything. Native-policy cases have no
executable effect and are scored on the decision
alone.
4
Evaluation Protocol
4.1
Guardrail configurations
The language track covers fourteen authorization
families.
Ten scenarios form the development
split and forty form the test split, giving 40 and
160 inputs. We evaluate eight configurations on
these inputs. Three general models receive our
authorization policy in the prompt:
Qwen3.5-
9B without thinking, Qwen3.5-27B with think-
ing (Qwen Team, 2026) and Nemotron (NVIDIA,
2026). Four guardrails use their own policy inter-
faces: GPT-OSS Safeguard (Safeguard) (OpenAI,
2025), Granite Guardian (Granite) (IBM Research,
2025), PolicyGuard (Rakancorle1, 2025) and the
NeMo Guardrails self-check (NeMo) running on
Qwen3.5-9B (NVIDIA, n.d.). Qwen3Guard keeps
its fixed content-safety taxonomy and serves as a
control (Qwen Team, 2025).
All configurations share a 32K-token context,
a single attempt and a one-hour deadline. Their
prompt templates and reasoning settings differ, so
we compare complete configurations, not isolated
model factors. Development runs only checked that
the pipeline worked, and we did not tune prompts
for accuracy. A response that the interface cannot
parse blocks execution and counts as unavailable.
An explicit UNKNOWN counts as an abstention.
Every case stays in every denominator. Appendix A
lists all generation settings and label mappings.
4.2
Outcome measures
The language test set has 80 lawful and 80 for-
bidden inputs. A forbidden effect is an executed
forbidden request, and a lawful completion is an
executed lawful request. A usable denial of a law-
ful request is a false denial. A response without a
usable decision is an unavailable decision. Usable
correctness counts usable decisions that match the
reference. The native-policy track runs no effects,
so we report incorrect approvals, false denials and
unavailable decisions against the engine reference.
These measures only make sense together.
Consider the original temperature-zero run with
Qwen3.5-9B (Table 4).
Structured review and
schema review both produce zero forbidden effects.
Lawful completions separate them, ten against 71.
Availability explains the gap. Structured review
blocks 58 of the 80 forbidden requests through un-
available decisions and only 22 through correct
denials (Table 8).
To compare two configurations, we match lawful
requests by identity. A lost request completes only
before the change, and a gained request completes
only after it. The net change is gains minus losses.
Each scenario contributes four related contexts, so
all summaries keep scenario membership.
The unit of comparison remains the request
throughout these analyses. A configuration’s com-
pletion total summarizes its successful set, but an
intervention is evaluated by matching the members
of that set. A gain and a loss can occur together
even when the total increases. We retain both di-
rections rather than assigning a newly completed
request to replace a rejected one. The same iden-
tities also distinguish a usable false denial from a
lawful request blocked by output failure. These
transitions connect an aggregate change to the per-
mission evidence affected by it.
Scenario membership supplies the dependence
structure for repeated comparisons. The four con-
texts share an operation and policy, and repeated
seeds revisit those contexts. We therefore keep sce-
nario clusters intact in the paired analysis instead
of treating every response as a new independent
authorization task. The seed summaries describe
response variation on the same requests. The clus-
tered analysis separately describes how the mea-
sured difference depends on which scenarios are
included.
4.3
Matched interface study
This study compares review interfaces under shared
models, evidence and generation settings. Direct
review asks for a single decision. Structured re-
view also asks for the policy requirements, findings
and supporting evidence. NeMo self-check returns
the component’s native yes or no. Schema review
keeps the structured-review prompt and only adds
JSON-schema decoding. The schema fixes the out-
put format but carries no permission information.
Only structured versus schema review changes de-
coding alone. Other contrasts compare interface
configurations whose prompts and parsers vary
jointly.
The original study ran each interface once on
Qwen3.5-9B at temperature zero. We repeat it
on Qwen3.5-9B and Qwen3.5-27B, both without
4

<!-- page 5 -->
80
40
0
40
80
Lawful requests lost                   Lawful requests gained
Direct → Structured
Direct → NeMo
Direct → Schema
Structured → NeMo
Structured → Schema
NeMo → Schema
Direct → Structured
Direct → NeMo
Direct → Schema
Structured → NeMo
Structured → Schema
NeMo → Schema
2.0
47.3
23.7
14.3
2.3
69.0
57.3
11.7
0.3
26.0
2.7
2.3
1.3
28.3
27.3
0.7
1.0
2.7
Qwen3.5-9B
Qwen3.5-27B
Figure 1: Lawful requests gained and lost across all six interface changes for each model. Bars and labels show
means over three seeds, with whiskers spanning the observed minimum and maximum. Every run uses the same
eighty lawful requests. Schema denotes schema review. Forbidden effects appear in Table 1.
thinking, with three seeds each. All repeated runs
use temperature 0.7, top-p 0.95, a 16K output limit
and one attempt. Every model, interface and seed
sees the same 40 development and 160 test inputs,
for 4,800 calls in total. We report every run, includ-
ing unavailable outputs. Appendix E gives the full
protocol and the paired statistics.
4.4
Native-policy evaluation
Qwen3.5-9B, Qwen3.5-27B and Safeguard each
judge all 1,215 native-policy test requests. We
then combine the three reviewers under an all-must-
allow rule. A later reviewer sees a request only if
the earlier ones allow it. We replay cached de-
cisions for all fifteen orders, so the compositions
need no new inference.
5
Results
5.1
RQ1: Do decisions follow authorization?
Language track.
Table 4 reports all eight con-
figurations. Qwen3.5-27B and Safeguard match
the reference on all 160 test inputs. The other six
configurations fail in different ways. Qwen3.5-
9B, Granite and NeMo always return usable de-
cisions but err in both directions, with six to sev-
enteen forbidden effects and eight to fifteen false
denials. Nemotron allows 58 forbidden effects
and leaves twelve inputs without a usable deci-
sion. Qwen3Guard completes every lawful request
but also allows 72 of the 80 forbidden ones, so
content-safety labels transfer poorly to authoriza-
tion. Since two configurations reach the ceiling
here, the harder comparisons come from the native-
policy track and the interface study. Figure 3 breaks
the results down by authorization family.
Native-policy track.
On the 1,215 native-policy
test requests, Qwen3.5-27B is correct on 99.1%,
with one incorrect approval and ten false denials.
Safeguard is correct on 84.2%, mainly because
it falsely denies 174 of the 767 lawful requests.
Qwen3.5-9B is correct on 69.4% and approves 261
of the 448 forbidden requests. The ranking holds
when we average over source applications (Ap-
pendix C.3).
The two kinds of error look different. Qwen3.5-
27B’s only incorrect approval lets Bob view a root
folder. Bob owns a document inside the folder,
but owning a child grants no access to its parent.
Safeguard denies Diana access to an expense she
submitted and misses a valid path from submitter to
editor to viewer. The first error crosses a resource
boundary. The second misses an indirect grant.
Engine replay confirms both references.
The native examples also give concrete tests for a
prospective repair. The folder case requires respect-
ing a resource boundary: ownership of the child is
insufficient for the parent query. The expense case
5

<!-- page 6 -->
0
25
50
75
100
Queries (%)
656/767
Permit
187/448
Deny
757/767
Permit
447/448
Deny
588/767 (5)
Permit
435/448 (1)
Deny
648/767
Permit
447/448
Deny
503/767 (4)
Permit
436/448 (1)
Deny
586/767 (5)
Permit
448/448
Deny
502/767 (5)
Permit
448/448
Deny
Qwen3.5-9B
Qwen3.5-27B
Safeguard
Qwen3.5-9B +
Qwen3.5-27B
Qwen3.5-9B +
Safeguard
Qwen3.5-27B +
Safeguard
Qwen3.5-9B +
Qwen3.5-27B
+ Safeguard
Correct / N
Reference
Correct
False denial
Incorrect approval
Unavailable
Figure 2: Native-policy outcomes of single reviewers and all-must-allow compositions on the same 1,215 test
requests, replayed from cached decisions. Rows show correct counts by reference label. Parentheses give unavailable
decisions. An added reviewer can remove incorrect approvals but can also veto lawful requests. Table 2 gives the
evaluated orders.
requires preserving an indirect permission path:
submitter status already establishes the requested
access. These conditions concern different poli-
cies and requests. A reviewer that corrects the first
while rejecting the second changes protection and
authorization in opposite directions. The native
references stay fixed. Repair evaluation can there-
fore follow the particular permission relation that
caused an error rather than checking only whether
the overall approval count decreased.
5.2
RQ2: Correct denial or interface failure?
Structured review fails to produce a usable deci-
sion in every repeated run (Table 1). Qwen3.5-9B
leaves 117 to 124 of the 160 inputs without a us-
able decision, and Qwen3.5-27B leaves 48 to 50.
All responses end normally below the output limit,
so these are format failures, not truncation. Each
failure blocks the operation and looks like a denial
in prevention counts.
Schema decoding removes this failure. Both
models return a usable decision for every input in
all three seeds. Structured and schema review also
use similar output budgets, about fifty thousand to-
kens per run, so the repair does not rely on a larger
output limit or greater output-token consumption.
A usable decision is not necessarily a correct one.
With schema review, Qwen3.5-9B still allows up to
six forbidden effects, and Qwen3.5-27B falsely de-
nies five or six lawful requests in every seed. Direct
review and NeMo self-check also vary across seeds,
and NeMo on Qwen3.5-9B allows most forbidden
requests. Schema decoding fixes the decision chan-
nel. The decisions themselves still need permission
evaluation.
The repeated conditions reveal two distinct pat-
terns. Structured review’s output problem appears
in both backbones at every seed, whereas the
permission outcomes of usable interfaces change
across seeds. A format intervention can therefore
be stable at one level and variable at another. For
Qwen3.5-9B, schema review narrows the varia-
tion in lawful completion compared with direct re-
view, but its forbidden-effect count still varies. For
Qwen3.5-27B, schema review prevents the tested
forbidden effects at every seed while retaining sev-
eral false denials. Neither pattern is described ade-
quately by output availability alone.
The comparison with NeMo also separates per-
missiveness from permission discrimination. Com-
pleting every lawful request is desirable only when
the reviewer still rejects its forbidden counter-
parts. The supplied evidence makes that require-
ment testable without changing the operation. Con-
versely, a reviewer that blocks both counterparts
prevents the forbidden effect but fails to honor the
6

<!-- page 7 -->
Interface
Forbidden
effects /80
Lawful
completions /80
Unavailable
decisions /160
Mean output
tokens
Qwen3.5-9B nonthinking
Direct review
3 / 0 / 14
57 / 41 / 71
0 / 0 / 0
963
Structured review
1 / 1 / 2
13 / 10 / 10
117 / 121 / 124
54,127
NeMo self-check
74 / 60 / 80
80 / 80 / 80
1 / 0 / 0
320
Schema review
6 / 0 / 3
69 / 68 / 68
0 / 0 / 0
50,940
Qwen3.5-27B nonthinking
Direct review
1 / 0 / 2
74 / 73 / 74
0 / 0 / 0
1,122
Structured review
1 / 1 / 0
48 / 45 / 51
48 / 50 / 48
57,119
NeMo self-check
6 / 3 / 11
76 / 75 / 78
0 / 0 / 0
320
Schema review
0 / 0 / 0
75 / 75 / 74
0 / 0 / 0
52,352
Table 1: Replicated matched-interface results. Each count lists seeds 0 / 1 / 2 on the same 160 test inputs. Both
models run without thinking, with identical sampling and a 16K output limit. Mean output tokens cover one
160-input run. All responses terminate normally, with no infrastructure errors. The eight original configurations and
temperature-zero study remain in Table 4.
Composition
Incorrect
approvals /448
Lawful
approvals /767
Cached
consultations
Qwen3.5-9B
261
656
1,215
Qwen3.5-27B
1
757
1,215
Safeguard
12
588
1,215
Qwen3.5-9B →Qwen3.5-27B
1
648
2,132
Qwen3.5-27B →Qwen3.5-9B
1
648
1,973
Qwen3.5-9B →Safeguard
11
503
2,132
Qwen3.5-27B →Safeguard
0
586
1,973
Safeguard →Qwen3.5-27B
0
586
1,815
Qwen3.5-27B →Safeguard
→Qwen3.5-9B
0
502
2,559
Table 2: Cached permission decisions and consultation counts for single reviewers and all-must-allow compositions
on the 1,215 native-policy test requests. The first reviewer always sees every request. Table 9 lists all fifteen orders
with unavailable decisions and selected token counts. Consultations select cached responses and do not represent
new inference.
valid grant. Joint reporting identifies these oper-
ating points, while the preserved response and re-
quest records show whether the distinction comes
from a usable judgment or a failed review.
5.3
RQ3: Do repairs and additional review
preserve valid authorization?
Interface changes.
Figure 1 shows the lawful
requests that each interface change gains and loses.
The move from direct to schema review matters
most, since schema review is the repaired interface.
In five of its six runs, this move both gains and
loses lawful requests. Net changes range from three
fewer to 27 more completions, and the totals hide
the losses. Protection also moves in both directions.
For Qwen3.5-9B, schema review raises forbidden
effects from three to six in seed zero but lowers
them from fourteen to three in seed two.
Across all 36 interface contrasts, twelve con-
tain both gains and losses. Among the six direct-
to-schema comparisons, only the 27-request gain
of Qwen3.5-9B in seed one remains significant
after scenario-cluster tests and Holm correction
across all 36 contrasts (Appendix E). The repeated
runs agree that schema decoding restores usable
decisions. They disagree on the set of lawful re-
quests it honors. The original temperature-zero run
shows the same pattern. It gains thirteen lawful
requests and loses two, a delegated refund and a
clinical handoff (Appendix G). Removing the two
unresolved contexts leaves these conclusions un-
changed.
Reference permissions and complete inputs stay
fixed across the repeated runs. Differences between
7

<!-- page 8 -->
seeds therefore describe variation in the sampled re-
view decisions on those requests. Figure 1 summa-
rizes the transition counts with means and observed
ranges, while Table 1 keeps every seed’s outcomes.
The two views serve different purposes: the fig-
ure shows the direction and scale of an interface
change, and the table retains runs in which pro-
tection or lawful completion deteriorates. Request
identities show which authorizations survive.
Additional review.
An all-must-allow composi-
tion never accepts more requests than any of its
members.
The real question is which errors it
removes and which lawful requests it gives up
(Table 2, Figure 2).
Adding Qwen3.5-27B af-
ter Qwen3.5-9B removes 260 of 261 incorrect
approvals at the cost of eight lawful approvals.
Adding Qwen3.5-9B after Qwen3.5-27B removes
no error and loses 109 lawful approvals. Adding
Safeguard after Qwen3.5-27B removes its single
incorrect approval but rejects 171 lawful requests.
Each reviewer corrects different errors and brings
its own vetoes.
6
Discussion
Match the repair to the failure.
Our three
records point to different fixes. An unavailable
decision is a problem of the output channel, so the
first step is to repair the interface and re-check the
recovered decisions. An incorrect approval calls
for checking the grant or adding a reviewer that
rejects the request. A false denial gives a concrete
regression test, namely the evidence path that estab-
lishes permission. In each case, request identities
show the errors a change fixes and the valid autho-
rizations it breaks.
Treat preserved authorization as an acceptance
test.
A guardrail change should pass three checks.
It must block the designated forbidden effects, re-
turn usable decisions and keep honoring a declared
set of lawful requests. This set, such as routine
refunds or accepted clinical handoffs, is fixed be-
fore selection, and gains elsewhere cannot replace
a request in it. Our repeated results show why
the checks must stay separate. Schema review on
Qwen3.5-9B is always usable. Yet in one seed it al-
lows more forbidden effects than direct review, and
in another it loses six earlier successes. Schema
review on Qwen3.5-27B blocks every forbidden
effect but still rejects lawful requests in each seed.
Apply the test to a specific permission boundary.
A required lawful-request set makes preservation
testable before choosing a configuration. It may
include a routine refund covered by an active dele-
gation or a record update permitted by an accepted
handoff. The requirement attaches to those requests
and their authorization paths, not to a target number
of completed tasks. If a repair rejects one of them,
completing another request does not restore that
permission. The same request can also be checked
under forbidden evidence, so preserving its lawful
execution does not mean accepting it regardless of
authorization.
The evaluation should follow both sides of this
boundary after an intervention. First check that
the formerly forbidden effect is prevented by a us-
able denial. Then check that the designated lawful
counterpart still executes. Request identities con-
nect these checks to the evidence that establishes
or invalidates permission. This distinguishes a cor-
rected authorization error from a blanket veto, and
distinguishes recovered output from recovered law-
ful capability. A repair succeeds for the required
boundary only when its protection and preserva-
tion conditions both hold. These checks define
acceptance for the required requests.
Choose oversight by the required boundary.
Additional reviewers trade lawful approvals for
fewer incorrect approvals. Under a zero-incorrect-
approval requirement, Qwen3.5-27B followed by
Safeguard keeps 586 lawful approvals. Adding
Qwen3.5-9B as a third reviewer leaves 502. Either
choice fails if it drops a required request. Order
keeps the accepted set fixed but changes calls, to-
kens and reached failures. The best choice also
depends on how often forbidden requests occur
and on the relative cost of each error. Appendix F.1
reports all fifteen orders under a range of cost as-
sumptions.
7
Conclusion
AuthorizationPairs tests whether guardrails honor
authorization by keeping each operation fixed and
changing only its permission. The contrasts sepa-
rate correct denials from blocks caused by failed
reviews, and request identities show whether valid
authorization still works after a change. In our ex-
periments, output repair restores usable decisions
but changes the set of honored lawful requests. An
extra reviewer removes some permission errors and
vetoes valid authorization. Usable output and pre-
8

<!-- page 9 -->
served authorization are separate requirements, and
guardrail evaluation should check both.
Limitations
We drafted the fifty language scenarios with AI
assistance. All three annotators work in security,
so readers from clinical, legal or financial practice
may interpret some policies differently. Two issuer
readings remain unresolved. Native-policy refer-
ences hold only for the supplied formal policies.
Public examples may overlap with model training
data, and source and scenario identifiers record
these dependencies. The native-policy test split is
public, and 89 of its inputs appeared in an earlier
pilot. Models differ in reasoning settings, wrap-
pers and output limits, so our comparisons concern
complete configurations. Finally, each case is a
single review decision. Multi-step agent workflows
remain future work.
Ethical Considerations
Experiments use fictional identities, synthetic doc-
uments, local websites and simulated balances. No
real payment, external delivery, patient-record ac-
cess or production deployment takes place. AI tools
assisted with scenario drafting, code, analysis and
writing. All reference labels come from three hu-
man annotators with security expertise. They were
paid HKD 60 per hour and agreed to the release of
their labels. Automated annotation serves only as
a cross-check. The authors are responsible for the
reference semantics, the claims and the submission
disclosures.
