---
source: 2610.21983-ontoact.pdf
part: appendix
converted: 2026-11-07
converter: pymupdf4llm
---

# Preprint. Under review. · 附录

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

# A TACIT-FLE: SPECIFICATION, EXAMPLES, AND VALIDATION 

This appendix specifies the benchmark introduced in Section 2. **GitHub repository:** _will be released_ . 

## **Section Contents** 

- A.1 Agent inputs, observations, and actions 

- A.2 Plant generation and reference corpus construction 

- A.3 Illustrative examples of the three task types 

- A.4 Evaluation population and scoring 

- A.5 Benchmark construction checks 

## A.1 TASK AND INFORMATION AVAILABLE TO THE AGENT 

A world _w_ = ( _P, D_ ) pairs a plant _P_ with a fixed reference corpus _D_ . An episode _e_ = ( _w, c_<sup>_∗_</sup> _, B_ ) introduces one hidden fault _c_<sup>_∗_</sup> and allows _B_ interaction turns. The agent receives the corpus, a task brief, a unit roster, and observations of the faulty plant. The agent interacts with the plant through Tacit-FLE’s text commands for inspection and repair. Tacit-FLE runs on the Factorio server infrastructure of FLE and adds a plant generator, fault injection, a maintenance corpus, a text command interface, and repair evaluation. Whereas the troubleshooting suite of FLE evaluates spatial error identification in existing factories, Tacit-FLE evaluates diagnosis and executed repairs from finite maintenance records. 

## A.1.1 OBSERVATIONS AND ANONYMIZATION 

The task brief gives the turn budget and the plant’s normal production rate in final products per minute; the roster lists unit kinds and positions. A public status board reports machine run states, storage totals and changes, elapsed game time, and shipping counts. Power and material-transfer devices require inspection, while opening a unit returns itemized contents. Conjunction also exposes the configured output for comparison with its operating plan. Table A1 separates available information from evaluator metadata. Figure A2 illustrates the initial input and a subsequent command response. 

Table A1: **Information boundary.** Public records can disclose selected planned facts; the complete original specification remains evaluator metadata. 

|Source|Available information|
|---|---|
|Initial task|Turn budget, normal production rate (final products/minute), unit kinds,<br>and coordinates.|
|Inherited records<br>|Local incident observations, checks, repairs, and outcomes; buffer policy<br>for Chain; planned outputs for Conjunction.<br>|
|Current observations|Machine states, storage totals and changes, shipping; inspections and<br>itemized readings on request.|
|Repair feedback|Episode termination after an accepted repair; continued interaction<br>otherwise.|
|Evaluator only|Injected fault, accepted repair targets, full original plant specification, and<br>coverage annotations.|



Items, entities, recipes, and fluids are anonymized with consistent world-specific labels across records and observations. Unit kinds, positions, structural suffixes, and measured states remain visible. This reduces reliance on familiar Factorio names while retaining spatial and operational cues. 

## A.1.2 ACTIONS AND REPAIR FEEDBACK 

In Factorio, production evolves with simulation time: machines process inputs, materials move between components, and inventories and shipping counts change. Table A2 lists the available commands and the game time each advances. A replacement restores a unit to its original specification, 

13


<!-- page 14 -->

Preprint. Under review. 



<!-- Start of picture text -->
(a) Inherit a plant and its records<br>Cause unknown Unit Type Status Maintenance logs Operating plans<br>Given Stopped Storage Time Observation Repair Outcome Target products:<br>A partially observed ? ? ? Machine ······ ······ ······ ······<br>factory with current Machine ··· ··· ··· ··· ···<br>symptoms and records. ···        ···          ···<br>Existing plant Unit roster<br>Finite reference corpus<br>(b) Three task types<br>1 Chain 2 Conjunction 3 Elimination<br>Join local dependencies Combine complementary evidence Rule out known explanations<br>Log 2 Log 1 Repair precedent Operating plan Live reading Documented explanations Live evidence<br>A → B B → C Expected: Configured: A Contradicted<br>(supply dependency) (supply dependency) Past mismatch<br>repaired Contradicted<br>B<br>?<br>≠<br>A B St op ped Mismatch ?<br>C<br>Further investigation<br>Trace upstream from a symptom Relate the mismatch to a repair precedent<br><!-- End of picture text -->

Figure A1: **Tacit-FLE.** (a) An agent inherits an existing plant, a finite reference corpus of maintenance logs and operating documents, and observations of a new fault. (b) � Chain links dependencies across incidents; � Conjunction combines repair precedents, plans, and observations; � Elimination rules out known explanations contradicted by current evidence. 

**Task brief and unit roster** Contract throughput: about 2 final products per minute. st-04 @(150.5,192.5) st-05 @(164.5,164.5) **Initial observation** [STATUS] first reading machines: mat-078 running, mat-214 running, st-00 stopped, st-01 stopped, st-02 stopped, st-03 stopped, st-04 stopped, st-05 running Shipping buffer ship cumulative 8 (mat-136 x8). (elapsed 0s) **Agent command** open st-05 **Environment response** st-05 opened: input buffer empty. configured output: mat-232. [STATUS] change over the last 10s Shipping buffer ship cumulative 10 (mat-136 x10). (elapsed 60s) [SHIFT] not fixed yet; the shift goes on. 

Figure A2: **Example interaction in Tacit-FLE.** A medium-scale Conjunction episode: the task brief, roster, initial status, and a later open command with its response. Only the selected lines are shown; identifiers and wording are preserved. 

including its configuration; a refill specifies the storage, item, and amount. Valid actions advance the simulation by the durations in Table A2, and each response reflects the updated plant state. Malformed commands consume a turn without advancing the plant. An accepted repair ends the episode; otherwise interaction continues and supplies further evidence. 

# A.2 CONSTRUCTING PLANTS AND INHERITED RECORDS 

A common seeded specification ties the simulated plant to its synthetic records. Construction has four components: 

1. **Generate the plant.** Select target products according to the scale profile, then trace Factorio’s recipe graph backward to identify the required intermediate products and raw inputs. Compile 

14


<!-- page 15 -->

Preprint. Under review. 

Table A2: **Agent actions in the evaluated protocol.** Each action uses one turn. The plant advances by the indicated game time; LLM deliberation itself is not charged as game time. The status board is included in observations at no additional turn cost. 

|Command|Game seconds|Effect or returned information|
|---|---|---|
|inspect _<_unit_>_|5|External state; power and material-transfer device<br>readings require this probe.|
|open _<_unit_>_|10|Itemized storage or input contents; configured<br>output in Conjunction.|
|wait _<_seconds_>_|specified|Advance the plant and receive an updated status<br>board.|
|replace _<_unit_>_|15|Restore the addressed unit to its original<br>specification.|
|refill _<_storage_>_|10|Insert the selected item into storage; success also|
|_<_item_> <_count_>_||depends on the repair target and item.|



these dependencies into a spatial layout of machines, input and output storage, material-transfer devices, and power infrastructure. The world seed controls product selection and layout choices, including shared production stages and spatial spread. 

2. **Establish normal operation.** Build the plant in Factorio and measure positive healthy shipping. 

3. **Introduce a fault.** Inject a supply cut for Chain or an off-plan machine configuration for Conjunction and Elimination. Cap downstream inventory so it cannot mask the fault indefinitely, and require stalled shipping or a persistent telemetry deviation. Other product lines may continue operating. 

4. **Construct the reference corpus.** Render historical incidents and operating documents from the same specification, withhold evaluation incidents, and check the intended distribution of evidence. 

Appendix A.5 summarizes the checks applied to generated plants and corpora. 

**Example plant topologies.** Figures A3–A4, A5–A6, and A7–A8 show small, medium, and large plants, respectively. Four selected examples per scale illustrate variation in production depth, branching, and shared intermediate stages. Arrows indicate material flow; dots join branches, and curved crossings are unconnected. Small squares denote input and output buffers. Positions are rearranged for readability, and utilities are omitted. Anonymized unit identifiers are shown above original names in italics, which are included only as a reading aid. 

15


<!-- page 16 -->

Preprint. Under review. 



<!-- Start of picture text -->
st-00<br>Iron gear<br>wheel<br>mat-110_in_W Iron ore mat-110 Iron plate Offshore st-01 pump Shippingbuffer ship<br>st-02<br>Pipe<br>(a) World 47728<br>mat-223_in_W mat-223 mat-053 mat-061 Electronic mat-212<br>Copper ore Copper plate Copper cable circuit Rail signal<br>ship<br>Shippingbuffer<br>mat-170_in_W mat-170<br>Iron ore Iron plate<br>(b) World 22970<br><!-- End of picture text -->

Figure A3: **Small-scale plant examples (a)–(b).** Each plant has one target product. One input stream splits and reconverges in (a), while (b) combines iron and copper through a circuit stage. 



<!-- Start of picture text -->
mat-095_in_W mat-095 st-02 Electronic st-03<br>Copper ore Copper plate Copper cable circuit<br>mat-098-1_in_W mat-098-1 st-00 st-04 st-01 ship<br>Iron ore Iron plate Iron gearwheel Inserter Long handedinserter Shippingbuffer<br>mat-098-2_in_W mat-098-2<br>Iron ore Iron plate<br>(c) World 62689<br>mat-095_in_W mat-095 mat-054 Firearm<br>Copper ore Copper plate magazine<br>mat-044<br>mat-013_in_W mat-013 mat-242 Piercing<br>Iron ore Iron plate Steel plate rounds<br>magazine<br>ship<br>Shippingbuffer<br>mat-015_in_W Coal mat-015 Grenade science pack mat-152 Military<br>mat-082_in_W mat-082 mat-118<br>Stone Stone brick Stone wall<br>(d) World 50676<br><!-- End of picture text -->

Figure A4: **Small-scale plant examples (c)–(d).** Each plant has one target product. A deeper assembly sequence in (c) contrasts with several material branches converging on one science pack in (d). 

16


<!-- page 17 -->

Preprint. Under review. 



<!-- Start of picture text -->
mat-205_in_W mat-205 mat-193 mat-228 Electronic mat-220<br>Copper ore Copper plate Copper cable circuit Inserter<br>mat-150-1_in_W mat-150-1 mat-033 mat-155 mat-032<br>Iron ore Iron plate Iron gearwheel Transport belt science packLogistic<br>ship<br>Shippingbuffer<br>mat-150-2_in_W mat-150-2<br>Iron ore Iron plate<br>mat-180_in_W mat-180<br>Wood Wooden chest<br>(a) World 14275<br>mat-078_in_W mat-078 st-00 Electronic st-02 Decider st-04<br>Copper ore Copper plate Copper cable circuit combinator<br>st-05 ship<br>Iron gear Shipping<br>wheel buffer<br>mat-214_in_W mat-214 st-03 st-01<br>Iron ore Iron plate Pipe Steam turbine<br>(b) World 73144<br><!-- End of picture text -->

Figure A5: **Medium-scale plant examples (a)–(b).** Each plant has two target products. An independent short production line accompanies the deeper chain in (a); the two targets reuse upstream products in (b). 

17


<!-- page 18 -->

Preprint. Under review. 



<!-- Start of picture text -->
mat-090_in_W mat-090 st-04 Electronic st-03<br>Copper ore Copper plate Copper cable circuit<br>mat-019-1_in_W Iron ore mat-019-1 Iron plate st-06 Pipe Pipe toground st-01<br>ship<br>Shippingbuffer<br>mat-019-2_in_W mat-019-2 st-00 st-02<br>Iron ore Iron plate Steel plate Gate<br>mat-044_in_W mat-044 st-05<br>Stone Stone brick Stone wall<br>(c) World 22606<br>mat-103_in_W mat-103 mat-046 mat-035 Electronic<br>Copper ore Copper plate Copper cable circuit<br>mat-228-1_in_W Iron ore mat-228-1 Iron plate mat-092 Iron gearwheel Transport belt mat-211 Underground mat-013 belt underground mat-244 Fastbelt<br>ship<br>Shippingbuffer<br>mat-047<br>Steel plate<br>mat-228-2_in_W mat-228-2 mat-116 mat-240 mat-165<br>Iron ore Iron plate Pipe Engine unit Locomotive<br>(d) World 16060<br><!-- End of picture text -->

Figure A6: **Medium-scale plant examples (c)–(d).** Each plant has two target products. Parallel material branches in (c) contrast with the longer transport and engine chains in (d). 

18


<!-- page 19 -->

Preprint. Under review. 



<!-- Start of picture text -->
mat-115_in_W Copper ore Copper plate mat-115 magazineFirearm st-01<br>mat-030-1_in_W mat-030-1 st-04 st-03<br>Iron ore Iron plate Pipe Steam engine<br>ship<br>Shippingbuffer<br>mat-030-2_in_W Iron ore mat-030-2 Iron plate Iron gear st-02 wheel<br>mat-067_in_W mat-067 st-00<br>Stone Stone furnace Shotgun shell<br>(a) World 5246<br>mat-031_in_W mat-031 mat-204 mat-010 Arithmetic<br>Copper ore Copper plate Copper cable combinator<br>mat-072 mat-161<br>Electronic Decider<br>circuit combinator<br>ship<br>Shippingbuffer<br>mat-237 mat-191<br>Transport belt Fast transportbelt<br>mat-151_in_W Iron ore mat-151 Iron plate mat-119 Iron gearwheel mat-198 Lab<br>(b) World 44309<br><!-- End of picture text -->

Figure A7: **Large-scale plant examples (a)–(b).** Each plant has four target products. Shorter parallel paths in (a) contrast with the reuse of a compact upstream circuit and belt network in (b). 

19


<!-- page 20 -->

Preprint. Under review. 



<!-- Start of picture text -->
mat-135-1_in_W Iron ore mat-135-1 Iron plate mat-203 Iron gearwheel Transport belt mat-230 mat-132 Splitter<br>mat-188_in_W mat-188 mat-019 mat-242 Electronic mat-123<br>Copper ore Copper plate Copper cable circuit Fast splitter<br>ship<br>Shippingbuffer<br>mat-135-2_in_W mat-135-2 mat-240 mat-007<br>Iron ore Iron plate Steel plate Gun turret<br>mat-164_in_W mat-164 mat-158 mat-093<br>Stone Stone brick Stone wall Gate<br>(c) World 64320<br>mat-109_in_W mat-109 st-05 Electronic st-07 Decider st-00<br>Copper ore Copper plate Copper cable circuit combinator<br>mat-002-1_in_W Iron ore mat-002-1 Iron plate Iron gear st-01 wheel Transport belt st-03 Underground st-02 belt underground st-06 Fastbelt<br>ship<br>Shippingbuffer<br>mat-002-2_in_W mat-002-2 st-10 st-08<br>Iron ore Iron plate Steel plate Steel chest<br>mat-112_in_W mat-112 st-09 st-04<br>Stone Stone furnace Pipe Boiler<br>(d) World 20024<br><!-- End of picture text -->

Figure A8: **Large-scale plant examples (c)–(d).** Each plant has four target products. Direct shipping accompanies further assembly in (c), while (d) contains fifteen processing units across several intermediate stages. 

20


<!-- page 21 -->

Preprint. Under review. 

# A.2.1 CORPUS CONTENTS AND PROVENANCE 

Each maintenance log contains five fields: OCCURRED, OBSERVED, CHECKED, ACTION, and RESULT. These describe local symptoms, checks, and repairs, leaving relations and conditions to be inferred across records. The corpus also includes explicit operating information: Chain supplies a buffer-policy note, and Conjunction supplies planned outputs. 

Three construction details matter for interpreting these records: 

- **Synthetic provenance.** Historical incidents are rendered from templates over the same plant specification. 

- **Document counts.** Required incidents and distractors are supplemented to the configured corpus size; a recurring incident may appear under separate log identifiers. Chain can add dependency records and its operating note afterward. Table A6 reports the resulting document counts, including these additions and repetitions. 

- **Held-out faults.** No registered test fault appears as a historical repair target in the shared corpus. The same unit may still appear as a downstream observation, roster entry, or planned-output entry. Records are shuffled, and the Conjunction plan lists applicable machines rather than singling out the faulty one. 

# A.3 THREE TASK TYPES: ILLUSTRATIVE EXAMPLES 

Tables A3–A5 pair excerpts from the maintenance logs and operating documents with environment responses to the agent’s commands. Each table pairs original document and response excerpts with an interpretation of their diagnostic relevance. 

- � **Chain: compose dependencies.** Local records connect successive units. A separate bufferpolicy note distinguishes normally empty internal buffers from yard-stocked intakes whose lack of incoming material indicates a supply cut. 

- � **Conjunction: combine complementary evidence.** A prior incident supplies a repair pattern, a plan supplies the expected output, and a current reading supplies the actual output. The mismatch is unit-specific: an item label alone does not indicate a fault. 

- � **Elimination: test alternative explanations.** Records describe destroyed units, supply cuts, and power failures, but omit the off-plan configuration encountered in evaluation. Rejecting documented explanations narrows the search; further observations or interventions may still be needed to distinguish remaining candidates. 

Table A3: � **Chain: an illustrative example.** Record excerpts and command responses from a medium-scale evaluation case. 

|Evidence source|Exact excerpt|
|---|---|
|Log log<br>~~6~~056|[OBSERVED] mat-193 stopped, input buffer empty.<br>[CHECKED] site visit — mat-205 found destroyed.|
|Log log<br>~~7~~299|[OBSERVED] mat-228 stopped, input buffer empty.<br>[CHECKED] site visit — mat-193 found destroyed.|
|Ops note buffer-policy|[NORM] Line-internal feed buffers are pulled<br>just-in-time and normally sit empty; an empty internal<br>buffer during a stall is expected, not evidence.<br>[NORM] Raw-material intake buffers are kept stocked by<br>the yard at all times.<br>An intake buffer found empty<br>with nothing arriving means its supply feed is severed<br>— replace that storage.|
|Command responses|mat-205<br>~~i~~n<br>~~W~~ opened:<br>empty.<br>flat at zero.|
|Interpretation|The two logs connect mat-205 to mat-193 and mat-193 to mat-228. The operating<br>note distinguishes an intake supply cut from normal internal-buffer emptiness.|



21


<!-- page 22 -->

Preprint. Under review. 

Table A4: � **Conjunction: an illustrative example.** Record excerpts and command responses from a medium-scale evaluation case. 

|Evidence source|Exact excerpt|
|---|---|
|Log log<br>~~5~~841|[CHECKED] opened st-04 — configured output does not<br>match the plan.<br>[ACTION] replaced st-04 with a fresh unit (as-built<br>configuration restored).|
|Plan norm<br>~~3~~982|- unit st-05:<br>planned output mat-231|
|Command responses|st-05 opened:<br>input buffer empty.<br>configured output:<br>mat-232.|
|Interpretation|A repair precedent on st-04 applies to a different unit: st-05 is planned to output<br>mat-231 but currently outputs mat-232.|



Table A5: � **Elimination: an illustrative example.** Record excerpts and command responses from a medium-scale evaluation case. 

|Evidence source|Exact excerpt|
|---|---|
|Log log<br>~~7~~360|[CHECKED] site visit — mat-027 found destroyed.|
|Log log<br>~~8~~680|[CHECKED] opened storage mat-070<br>~~i~~n<br>~~W~~ — found empty, no<br>inbound material.|
|Log log<br>~~3~~569|[OBSERVED] multiple machines in the zone stopped at<br>once.<br>[CHECKED] zone-wide simultaneous stoppage — power<br>distribution loss confirmed.|
|Command responses|mat-027 opened:<br>input buffer mat-089 x5, mat-074 x3.<br>mat-027:<br>old unit removed, replacement installed to<br>plan.<br>[SHIFT] not fixed yet; the shift goes on.<br>st-00 opened:<br>input buffer empty.<br>mat-070:<br>running.|
|Interpretation|Replacing mat-027 did not end the episode, which rejects the destroyed-unit<br>explanation of log<br>~~7~~360. A running machine (mat-070) is incompatible with the<br>zone-wide power loss of log<br>~~3~~569. The stopped st-00 matches none of the recorded<br>incidents and becomes the unit to investigate.|



22


<!-- page 23 -->

Preprint. Under review. 

# A.4 EVALUATION POPULATION AND SCORING 

Each combination of scale and task type has ten worlds: the first five are reserved for development, and the last five for evaluation. All registered fault positions in the evaluation worlds are tested, giving 45 world–type corpora and 104 episodes (Table A6). For each world, we rebuild the same plant and inject each registered fault in a separate episode, keeping its reference corpus fixed. Small, medium, and large use one, two, and four target products, respectively; corpus size, realized topology, task mix, and turn budgets also vary. 

Table A6: **Evaluated Tacit-FLE profiles.** Document counts include maintenance logs and operating documents in each corpus. Episodes correspond to the specified fault positions; _B_ is the turn budget. Scale conditions vary jointly in target products, corpus sizes, and interaction budgets. 

|Scale|Products|Type|Worlds|Documents/world|Episodes|_B_|
|---|---|---|---|---|---|---|
|Small|1|Chain|5|7–16|13|30|
|||Conjunction|5|5|7|30|
|||Elimination|5|4–5|8|30|
|Medium|2|Chain|5|32–40|14|60|
|||Conjunction|5|30|14|60|
|||Elimination|5|30|8|60|
|Large|4|Chain|5|63–72|17|75|
|||Conjunction|5|60|11|75|
|||Elimination|5|60|12|75|



A method may construct reusable knowledge from the corpus or retrieve records according to its evaluation procedure. No additional exploratory training episodes are supplied. Corpus-derived knowledge may be shared across a world’s episodes, but test observations, hypotheses, and outcomes are reset each time. The no-corpus control omits the records; method-specific access is detailed in Appendix C.2. 

# A.4.1 REPAIR CRITERION AND METRICS 

The evaluator retains an accepted repair-target set that is hidden from the agent. Replacing an accepted target completes the episode. A refill must address an accepted target, be accepted by the environment, and use the planned supply item when specified. Otherwise the attempt consumes a turn and the episode continues, until a repair succeeds or the budget is exhausted. 

- **Repair success:** the fraction of scheduled evaluation episodes with an accepted repair within the turn budget. 

- **Turns:** mean interaction turns, including the full budget for unsuccessful episodes. 

- **Spurious interventions:** mean executed replacements or refills per episode that fail the repair criterion, including an unsuccessful refill of an otherwise relevant unit. 

LLM calls and tokens are accounted for separately from environment turns (Appendix D.6). 

# A.5 BENCHMARK CONSTRUCTION CHECKS 

These checks assess whether generated cases realize the intended task type: an operating plant develops an observable fault, and its corpus provides the specified evidence. Table A7 summarizes the checks on plant behavior, corpus construction, and reproducibility. 

23


<!-- page 24 -->

Preprint. Under review. 

Table A7: **Benchmark construction checks.** The checks cover simulated plant behavior, corpus conditions, and reproducible evaluation inputs. 

|Check|Evidence|What it establishes|
|---|---|---|
|Plant behavior|Healthy production, followed by<br>stalled shipping or a persistent<br>change in operating readings after<br>fault injection.|The injected fault has an observable<br>effect on an operating plant.|
|Corpus construction|Required document fields and<br>vocabulary, declared evidence<br>coverage, and exclusion of test-fault<br>repair records.|Compliance with the corpus<br>construction conditions.|
|Reproducibility|Exact regeneration of all 45<br>evaluation corpora.|Consistent corpus inputs for the 104<br>evaluation episodes.|



# B METHOD DETAILS 

## B.1 REPRESENTATION AND INFORMATION ACCOUNTING 

The world knowledge is _KW_ = ( _T, AW , RW_ ), with an ontology schema _T_ = ( _C, R, P,_ Θ). Here _C_ is the set of entity types, _R_ the relations, _P_ the observable attributes, and Θ the admissible axiom templates with their evaluation procedures. The induced axioms comprise ground assertions in _AW_ , which preserve particular entities and their connections, and conditional axioms in _RW_ . Equation 2 combines these with the episode assertions _At_ ; Algorithm 2 uses the same tuple with the within-turn variables _A_ and _K_ . The templates differ by environment, as listed in Table A13. The predicate Typed in Equation 4a checks conformance to this vocabulary and its admissible axiom forms; empirical support is evaluated separately. 

An induced element retains a provenance set _π ⊆ D_ identifying its source records. Some sources are attached automatically by the induction procedure, while other templates require the LLM to cite record identifiers. Source association provides traceability; the additional support and compatibility checks are described below. Table A8 distinguishes fixed representation choices from induced knowledge and current observations. The experimental corpus and observation conditions, including the separately reported observation control, are specified in Appendix E.1. 

Table A8: **Information accounting for OntoAct.** The origins and roles of information used in construction and interaction. 

|Origin|Content|Role|
|---|---|---|
|Task inputs|Reference corpus, task description,<br>observations, action interface|Use and any observation controls<br>follow the experimental protocol.|
|Given representation|Schema_T_, observation map_ρ_,<br>template semantics|Method-specific representation and<br>interpretation choices; fixed before<br>learning.|
|Induced knowledge|_AW_,_RW_, source records_π ⊆D_|Constructed from the reference<br>corpus and fixed during evaluation.|
|Episode evidence|_At_|Grounded in public observations;<br>reset for each episode.|
|LLM proposals|Action_a_; structural and diagnostic<br>claims where supported|Checked against the current<br>knowledge and evidence.|



**Knowledge lifetime.** The corpus-derived world knowledge is reused without learning from test episodes. Each episode starts from that knowledge and obtains a fresh state _At_ from observations. Historical status readings are not copied into the live state; roster information can correct an entity’s 

24


<!-- page 25 -->

Preprint. Under review. 

type in the episode’s working representation. The distinction between world knowledge and episode state concerns lifetime and evidential scope. Both may contain assertions about individuals. 

# B.2 KNOWLEDGE CONSTRUCTION AND ADMISSION 

**Shared procedure.** This section expands Algorithm 1 and Equation 4b into the checks used to admit corpus-derived knowledge in each environment. _f_ abs in Equation 3 denotes the proposal procedure, including the association of each candidate with its source records. The admission indicator Admissible in Equation 4b requires schema and source validity ( _βi_ ), then applies the constraints _Cx_ supported by the knowledge type. The indicator **1** [ _P_ ] converts a satisfied condition to one and a failed condition to zero; the product in Equation 4b is one exactly when every applicable criterion holds. The membership and semantics of _Cx_ differ by knowledge type: source-link requirements, structural consistency, empirical support, and contradiction tolerances are specified below. _f_ corpus denotes validation against the assembled records: some checks run during admission, while others require a later pass over the assembled knowledge. Bounded correction requests within knowledge construction are included in the proposal procedure. The deterministic checks run without LLM calls. 

**Tacit-FLE: structure and diagnostic patterns.** The LLM processes each reference document using the supplied vocabulary and proposes entities, structural relations, diagnostic patterns, and nonevidence axioms. Entity types and relation names are closed; relation domain and range constraints and incompatible component types are checked when proposals enter the store. The current document identifier is attached to its extracted facts and patterns. A diagnostic pattern specifies the symptom type and status, the cause’s relation to that symptom, optional cause type and readings, and a repair action when the documented intervention has a corresponding command. For example, an incomingflow condition is retained only when the source record supplies it. Relations preserve particular component identities, whereas the diagnostic pattern refers to types and roles. 

When repair observations can be extracted from the cited records, a support check tests whether at least one cited incident instantiates the pattern’s symptom–cause relationship. An unsupported pattern is returned to the LLM once with the discrepancy; a revised proposal that still fails is discarded. Operating documents without a repair incident are not evaluated by this repair-specific test. After assembling the corpus, a further check removes self-cause patterns that would confirm themselves from the symptom alone when a recorded incident shows that symptom but documents a repair of another component. 

**Tacit-FLE: operating information.** Operating practices and service-count samples are elicited from the joined corpus because their evidence can span documents. Practice templates express a forbidden action under a stated condition, a check before an intervention, or a preference between actions. They require a valid typed form and nonempty citations drawn from the presented corpus, but do not undergo the repair-pattern support test. Non-evidence axioms encode explicit operating notes that make a status non-diagnostic for a component class, with any stated exceptions. Service samples are checked against their cited records and aggregated by production duty into an empirical prior over usage counts. 

**Mars.** The LLM reads the reference transitions and proposes typed action conditions and effects for collection, crafting, placement, movement, drinking, creatures, and material neighborhoods, together with blocked-action conditions. Admission checks the schema and requires at least one cited transition concerning the subject of the proposed axiom. Applicable recorded transitions are then checked for outcomes or effects that contradict it. The experiment configuration allows at most one contradictory transition; blocked-action rules additionally require recorded unsuccessful attempts without a recorded success under the claimed condition. This compatibility check is performed during admission. 

**ALFWorld.** Records are grouped by action and processed in batches of at most 24 transitions. The LLM proposes necessary action conditions over five supplied predicates: being at the target, holding the object, having empty hands, the object’s presence at the target, and the target’s openness. Every cited index must identify a record of the corresponding action. At least one cited successful transition must observe and satisfy all proposed conditions, and no successful transition in the corpus may contradict them. These checks establish positive support and compatibility with recorded successes. 

25


<!-- page 26 -->

Preprint. Under review. 

# B.3 DIAGNOSTIC HYPOTHESES AND VERIFICATION 

= **Hypothesis representation.** In the diagnostic variant, a hypothesis is written as _h_ ( _c, e, r,_ Φ _, σ, π, α_ ). Its fields are a candidate cause _c_ , the anomaly _e_ it explains, a referenced pattern _r_ , expected observational atoms Φ, required structural relations _σ_ , cited evidence _π_ , and a prescribed repair _α_ . The pattern can refer to an induced diagnostic pattern or aggregate prior, or describe an explanation proposed by the LLM beyond those patterns. An atom names an entity, an observable attribute, a comparison, and an expected value. 

**Admission of episode claims.** _f_ admit checks the structured claims proposed during interaction. Named entities and anomalies must exist in the current representation, the expected attributes must be readable, and required relations must already be established. A newly proposed relation must first be supported by a permitted basis, such as documented structure, layout connectivity, or observed contents. For a pattern-backed diagnosis, admission also checks the correspondence between the proposed cause, the symptom, and the conditions of that pattern. A hypothesis cannot cite a pattern requiring no incoming material while omitting the corresponding expected reading. An operating note that makes a status non-evidence can invalidate a claim relying on that status. 

**Three-valued evaluation.** The observation map _ρ_ grounds readings in the current state, and an atom evaluates as 

# [[ _φ_ ]] _Kt ∈{⊤, ⊥,_ ? _}._ 

The values denote support, contradiction, and an unresolved reading, respectively. Missing readings remain unknown. For a current status that disagrees with the claim, the implementation also considers recent readings and can leave an isolated fluctuation unresolved. An open, admitted hypothesis is refuted when an atom evaluates to _⊥_ , confirmed when all its atoms evaluate to _⊤_ , and remains open otherwise. For open hypotheses, unresolved atoms are mapped to available probes and included in the context supplied to the LLM. Confirmation records agreement with the specified observations. 

**Hypotheses beyond recorded patterns.** The LLM may propose an explanation for a cause not covered by an induced pattern, provided that its claim meets the structural and observational admission requirements. The reasoning context also lists recorded explanations that still owe a reading, open rival hypotheses, and the stopped units that no recorded pattern explains; an explanation outside the recorded patterns is marked as supported when its cause is one of these unexplained units. 

**Checking repairs and incorporating outcomes.** A repair is backed when an admitted LLMproposed hypothesis is confirmed, its nonempty set of atoms still holds, it prescribes the repair verb, and the target is named by the hypothesis’s cause or one of its atoms. Observation actions do not require a confirmed repair hypothesis; operating practices and repetition checks can nevertheless provide feedback on proposed commands. If an executed repair targets a hypothesis’s candidate cause and the episode continues, that outcome refutes the hypothesis on the next observation. A command refused by the environment is not counted as an executed repair. Confirmed hypotheses can also be refuted by subsequent contradictory readings or by the disappearance of the anomaly they explained. The LLM remains responsible for selecting a cause and an action from this evidence. When the proposal limit is reached, the final proposal and its verification verdict are passed to the executor. 

# B.3.1 EXAMPLE: FROM CORPUS RECORDS TO ACTION 

This example starts with a small reference corpus, shows the knowledge constructed from it, and follows its use in a new episode. The records and observation branches are condensed, fictional examples. 

**Step 1: read the records and construct world knowledge.** Suppose the agent receives the following two documents, _D_ = _{d_ 1 _, d_ 2 _}_ , before evaluation. 

# **Reference corpus.** 

_d_ 1 **: Line A handover note.** “Storage _s_ 1 supplies iron plates to machine _m_ 1. Mover _q_ 1 delivers plates into _s_ 1 and is its only incoming connection.” 

_d_ 2 **: Line A maintenance record.** “Machine _m_ 1 had stopped. Its supplying storage _s_ 1 contained no iron plates. Inspection of its sole incoming mover _q_ 1 found no material arriving. We added iron plates to _s_ 1; _m_ 1 then resumed production.” 

26


<!-- page 27 -->

Preprint. Under review. 

The ontology schema _T_ provides the types Storage, Machine, and Mover, the relation feeds, and the observable attributes. The LLM proposes a particular supply relation and a reusable diagnostic pattern. The relation has compatible endpoint types; the pattern’s cited incident matches its stoppedmachine symptom, supplying-storage cause, and refill intervention. After the applicable admission checks, _KW_ = ( _T, AW , RW_ ) retains 



<!-- Start of picture text -->
AW ⊇{ feeds( s 1 , m 1) } supported by  d 1 , d 2 ,<br>RW ∋ r with source  πr =  {d 2 }.<br><!-- End of picture text -->

The content of _r_ makes the reusable roles explicit: 

symptom: _m_ : Machine is stopped _,_ candidate cause: _s_ : Storage is depleted _,_ required relation: _σr_ ( _s, m_ ) = _{_ feeds( _s, m_ ) _},_ expected readings: Φ _r_ ( _s_ ) = _{_ stock( _s_ ) = 0 _,_ inflow( _s_ ) = 0 _},_ prescribed repair: refill( _s_ ) _._ 

The concrete identities remain in _AW_ , while _r_ replaces them with roles that can match another storage–machine pair. The empty-stock and no-inflow conditions come from _d_ 2; they specify what to check when proposing the same explanation for a new pair. Here and below, inflow = 0 means that no incoming material is observed. 

**Step 2: apply the pattern to a new situation.** Now consider a different pair, _s_ 2 and _m_ 2. The current layout and observations provide the following information. 

**Current episode. Layout.** Storage _s_ 2 supplies machine _m_ 2; mover _q_ 2 is the sole incoming mover connected to _s_ 2. **Observed.** Machine _m_ 2 is stopped, and inspection of _s_ 2 finds zero iron plates. **Not yet observed.** Mover _q_ 2 has not been inspected, so whether material is arriving remains unresolved. 

The layout establishes feeds( _s_ 2 _, m_ 2) in the episode evidence _At_ . The historical observation of _q_ 1 says nothing about the current inflow through _q_ 2. Using _r_ , the LLM proposes _h_ : “Depletion of _s_ 2 may explain the stopped _m_ 2; the corresponding repair is to refill _s_ 2.” Substituting _s �→ s_ 2 and _m �→ m_ 2 gives 



<!-- Start of picture text -->
σ ( h ) =  σr ( s 2 , m 2) =  { feeds( s 2 , m 2) },<br>Φ( h ) = Φ r ( s 2) = �stock( s 2) = 0 , inflow( s 2) = 0� .<br>� �� � � �� �<br>φ stock φ inflow<br><!-- End of picture text -->

Each _φ_ is a condition to test; for example, _φ_ stock has the tuple form ( _s_ 2 _,_ stock _,_ = _,_ 0) in Equation 7. The proposal retains both conditions from _d_ 2, including the inflow condition that has not yet been observed in this episode. Both attributes are observable, so the complete hypothesis can be admitted before every reading is available. 

Table A9 contrasts a complete proposal with three incomplete proposals, holding the other admission requirements fixed and satisfied. For the missing-relation case, assume the layout and records do not establish the supply connection. A missing reading is compatible with admission; an unsupported relation or omitted required condition is not. 

27


<!-- page 28 -->

Preprint. Under review. 

Table A9: **Admission before observation-based assessment.** 

|Case|Proposal|Admission and reason|
|---|---|---|
|Complete|Established supply relation; both<br>required conditions retained; inflow<br>still unread.|Admitted: Missing readings can be investigated after<br>admission.|
|Missing<br>relation|The proposal names a supplier relation<br>that has no supporting evidence.|Not admitted: Establish the relation before applying<br>this pattern.|
|Missing<br>condition|The proposal cites the pattern but<br>checks only whether storage is empty.|Not admitted: Retain the required no-inflow condition.|
|No conditions|The explanation supplies no observable<br>conditions.|Not admitted: An explanation needs a nonempty set of<br>testable conditions.|



An inadmissible proposal has not entered the hypothesis set. This differs from a _refuted_ hypothesis, which was admitted and then contradicted by evidence. 

**Step 3: inspect the missing condition and assess the hypothesis.** Equation 7 compares each expected condition with its current reading: _⊤_ means supported, _⊥_ means contradicted, and ? means unresolved. Equation 8 then combines those two results into the status of _h_ . In the current episode above, zero stock supports _φ_ stock, while _φ_ inflow is unresolved. Thus _h_ is open (case A): the past incident suggests an explanation, but the new evidence does not yet confirm it. The LLM can request inspect( _q_ 2) to learn whether material is arriving. With stock still zero and _m_ 2 still stopped, the response determines which branch follows. In each pair below, the first entry evaluates stock and the second inflow: 



<!-- Start of picture text -->
no material arriving<br>A: ( ⊤,  ?) , open −−−−−−−−−−→ B: ( ⊤, ⊤ ) , confirmed ,<br><!-- End of picture text -->



<!-- Start of picture text -->
material arriving<br>A: ( ⊤,  ?) , open −−−−−−−−→ C: ( ⊤, ⊥ ) , refuted .<br><!-- End of picture text -->

If inspection still leaves inflow unresolved, the case remains A and _h_ remains open. The no-inflow branch agrees with _d_ 2’s expected conditions; the inflow branch contradicts one of them, even though the storage is empty in both cases. Table A10 gathers these branches and two further alternatives, with the structure and stopped-machine anomaly held fixed. 

Table A10: **Different evidence for the same proposed explanation.** Independent alternatives; each case evaluates both expected conditions. 

|Case|Stock|Inflow|Values<br>(stock, inflow)<br>Eq. 7|Status<br>Eq. 8|Reason and next step|
|---|---|---|---|---|---|
|A|0|Unread|(_⊤,_?)|Open|Empty stock supports one condition; inspect<br>incoming supply to resolve the other.|
|B|0|None|(_⊤, ⊤_)|Confirmed|Both expected conditions are supported. Check<br>the proposed repair next.|
|C|0|Arriving|(_⊤, ⊥_)|Refuted|Observed inflow contradicts the no-inflow<br>condition. Revise the explanation.|
|D|5|Unread|(_⊥,_?)|Refuted|Nonzero stock already contradicts the claim;<br>the unread inflow cannot rescue it.|
|E|Unread|Unread|(?_,_?)|Open|Neither condition has been resolved. Obtain an<br>informative observation.|



In case D, the observed stock of five already contradicts the empty-storage condition; the unread inflow does not prevent refutation. Case E instead has no resolved condition, so there is no contradiction and no confirmation. 

**Step 4: check the proposed repair against the confirmed explanation.** Continue along branch B, with both conditions supported and _h_ confirmed. The LLM proposes refill( _s_ 2), transferring the repair in _d_ 2 to the storage occupying the same role in the new episode. The action matches _r_ ’s prescribed verb and _h_ ’s candidate cause; both required readings currently hold, so it is backed by _h_ . 

28


<!-- page 29 -->

Preprint. Under review. 

For Table A11, take _H_<sup>_′_</sup> = _{h}_ and let _s_ 3 be another storage that is neither the cause nor an entity tested by _h_ . We write only each command’s verb and target, assuming valid material and amount arguments for a refill. The table evaluates the repair-backing requirement in Appendix B.3; other action checks still apply. 

Table A11: **Hypothesis confirmation and action backing.** Independent alternatives evaluated with _H_<sup>_′_</sup> = _{h}_ ; the backing check uses this candidate only. 

|Case|Proposal|Recorded<br>status|Conditions<br>(stock, inflow)<br>Eq. 7|Backed|Reason|
|---|---|---|---|---|---|
|R1|refill(_s_2)|Confirmed|(_⊤, ⊤_)|Yes|Prescribed verb, matching target,<br>and both conditions supported.|
|R2|replace(_s_2)|Confirmed|(_⊤, ⊤_)|No|The pattern prescribes a refill, not<br>replacement.|
|R3|refill(_s_3)|Confirmed|(_⊤, ⊤_)|No|The target is neither the cause nor<br>an entity tested by this hypothesis.|
|R4|refill(_s_2)|Confirmed|(_⊤,_?)|No|Stored confirmation is insufficient<br>when a current condition is<br>unresolved.|
|O1|inspect(_q_2)|Open|(_⊤,_?)|Not required|An observation does not require a<br>confirmed repair hypothesis.|



Rows R1–R3 show that the same confirmed explanation can back one repair and fail to back another. R4 considers a later state in which the recorded confirmation remains but a current reading is unresolved: this is why the repair check rechecks all expected conditions. O1 returns to case A and shows that the agent can seek evidence while the hypothesis is still open; an observation does not require repair backing. 

**Step 5: use the intervention outcome as new evidence.** Suppose the refill in R1 is executed. Table A12 separates possible responses from the environment. The refutation rule for an executed repair that leaves the episode running is the diagnostic outcome rule of Tacit-FLE described in Appendix B.3. 

Table A12: **Intervention outcomes after a backed refill.** 

|Event|Result|Meaning|
|---|---|---|
|The refill executes and the episode|Task completed|The episode ends; no additional hypothesis|
|terminates successfully.||status is needed.|
|The refill executes, but another episode|Hypothesis refuted|Under the diagnostic outcome rule, the|
|turn follows.||intervention contradicts this candidate-cause<br>claim.|
|The environment refuses the refill<br>command.|No intervention<br>evidence|Refusal alone does not refute the hypothesis;<br>inspect the feedback and current evidence.|



For the continuing-episode branch, the transition is 



<!-- Start of picture text -->
refill executed; episode continues<br>confirmed� �� � −−−−−−−−−−−−−−−−−→ �refuted�� � .<br>expected readings supported intervention contradicts the explanation<br><!-- End of picture text -->

This update uses intervention evidence, whereas Equation 8 assessed the initially open hypothesis from its expected readings. A refused command supplies no such intervention evidence; new observations may still change the assessment. 

29


<!-- page 30 -->

Preprint. Under review. 

## B.4 LEARNING SCOPE AND PROMPT CONTRACTS 

The separation between reusable knowledge and episode state follows Appendix B.1. The ontology schemas fix the vocabulary and rule forms. _f_ abs and _f_ propose are implemented through LLM calls; their inputs and output contracts are given below. Verification consists of the typed constraints, relation checks, and observational predicates of Equations 4 and 7–9. 

**Inputs and outputs.** Knowledge-construction prompts provide the schema and the corresponding record batch, requesting structured facts or axioms. The diagnostic action prompt provides world knowledge with its sources, layout facts, current readings, previous commands, hypothesis status, and available actions. It requests optional structural claims and hypotheses followed by one executable command. In Mars and ALFWorld, the actor instead receives the learned action conditions, task context, observations, and feedback from failed condition checks. The following blocks summarize the two Tacit-FLE prompt contracts; wording is condensed and bracketed fields stand for the corresponding inputs. 

### **Knowledge construction: record-level extraction** 

Input: [typed schema] and [reference document]. Extract the entities and structural relations stated or implied by the record. Generalize the incident using component types, the symptom, the cause’s relation to it, any stated observational conditions, and the documented repair. Do not copy historical status readings into persistent structural facts. Return structured entities, relations, diagnostic patterns, and explicit non-evidence policies. The current record identifier is attached as provenance. 

### **Diagnostic interaction: explanation and action** 

Input: [world knowledge and sources], [layout], [observations], [command history], [hypotheses and their standing], [verification feedback]. Propose which component could explain an observed anomaly and what readings would support that explanation. Name the pattern used, its required relations, expected readings, evidence, and a repair. Claim new structure with a permitted basis. Use unresolved conditions and contradictory evidence to decide what to observe or revise. Return optional structured claims followed by one command: inspect, open, wait, replace, or refill. 

# C ENVIRONMENT BINDINGS AND BASELINES 

## C.1 INSTANTIATION PER ENVIRONMENT 

Table A13 instantiates the construction and interaction procedures in Section 3. The common principle is to induce structured knowledge from the reference corpus and use it to check proposals against current evidence. The representations and verification procedures specialize this principle to each environment. Tacit-FLE combines component relations, diagnostic patterns, and an episode-specific hypothesis ledger; Mars uses typed action and effect templates; ALFWorld uses conditions over observed scene predicates. Appendix B.2 specifies their admission checks. 

**Observation grounding.** The function _f_ ground in Algorithm 2 updates episode assertions from observations using an environment-specific map _ρ_ , left implicit in the algorithm. In Tacit-FLE, component types and positions come from the public roster, while layout and readouts supply connection and state evidence. The mapping from a stock trend to an inflow reading is a fixed interpretation of public observations, rather than an induced axiom. A stock level that remains at zero does not alone settle whether material is arriving; other readings can be needed. These observation mappings are supplied by the environment binding. The Mars binding exposes position, inventory, 

30


<!-- page 31 -->

Preprint. Under review. 

Table A13: **Environment-specific instantiations of OntoAct.** The common construction and interaction procedures use the following representations and checks. 

|Element|Tacit-FLE|Mars|ALFWorld|
|---|---|---|---|
|Corpus_D_|One plant’s maintenance<br>logs and operating<br>documents|Recorded transitions<br>from one world|Recorded transitions<br>from training games|
|Vocabulary_T_|Component types,<br>material-flow relations,<br>statuses, and public<br>readings|Materials, items,<br>creatures, action and<br>effect templates|Action verbs and five<br>observation predicates|
|Induced<br>knowledge|Structural facts,<br>diagnostic patterns,<br>non-evidence axioms,<br>practices, aggregate<br>priors|Collect, make, place,<br>walk, drink, creature,<br>neighborhood, and<br>blocked-action<br>conditions|Necessary action<br>conditions|
|Evidence batch|One document; practices<br>and service samples over<br>the joined corpus|The supplied transition<br>buffer|By action, at most 24<br>transitions per batch|
|Corpus checks|Type-specific source,<br>structure, support, and<br>counterexample checks|Subject-linked citations;<br>at most one<br>contradictory transition|Action-linked citations;<br>positive support; no<br>successful<br>counterexample|
|Observation map<br>_ρ_|Roster, layout, public<br>readings; stock changes<br>inform inflow|Position, inventory,<br>vitals, visible cells|Parsed scene, inventory,<br>and receptacle state|
|Action checks|Repair backing;<br>operating practices;<br>repetition feedback|Learned applicability<br>conditions and<br>lethal-ground checks on<br>an exploration path|Learned conditions over<br>observed predicates|
|Proposals_J_|2|5|5|



31


<!-- page 32 -->

Preprint. Under review. 

vitals, and visible cells; the ALFWorld binding maps parsed scene information onto the five predicates used by its learned conditions. 

# C.2 BASELINE IMPLEMENTATIONS AND PROMPTS 

We implement each baseline’s knowledge representation and decision procedure using the published method and available reference code. Environment bindings supply the task description, observation format, action syntax, and reference records. The descriptions below specify how each method uses the corpus in our experiments. Where a released implementation omits a component or departs from the published procedure, we follow the paper; such adjustments are noted with each method. 

**ReAct and ReAct**<sup>*****</sup> **.** ReAct alternates a textual thought with an executable action based on the task description and observations. ReAct<sup>*</sup> supplements the same actor with up to five corpus records retrieved once at the start of an episode. The retrieval query uses the initial observation and, in Tacit-FLE, the plant roster. The retrieved records remain available in the episode context. Both variants share the actor prompt, action parser, and history handling within an environment. 

**Reflexion.** We use a corpus-based adaptation of reflective memory. Before evaluation, the model reads each reference document and writes a memory note describing useful evidence and conditional plans. At the start of an episode, the initial-observation query retrieves up to three relevant notes for the actor. The reflection prompt asks the model to distinguish observed outcomes from inferred advice and to preserve the conditions under which an action is useful. This adaptation constructs the reflective memory from the supplied records. 

**IfR.** The induction prompt converts recorded interactions into a natural-language rule library. On Tacit-FLE, repair records additionally populate a skill library describing successful procedures. The planner uses the task, observations, and retrieved knowledge to propose actions; an explanation prompt interprets unsuccessful execution and supports replanning. We route all LLM calls and actions through the shared interfaces while retaining the separate induction, planning, explanation, and replanning stages; the reference corpus initializes the rule library and, on Tacit-FLE, the skill library; episode history is retained across replanning rounds, and library entries above the similarity threshold are replaced by the newly induced rule. 

**WALL-E.** The learning stage compares predicted action outcomes with recorded outcomes. Prediction discrepancies drive natural-language rule proposals, which are compiled into executable checks and validated against recorded transitions. During evaluation, a proposer and world model use the learned knowledge, and the executable rules check candidate actions before execution. Our bindings present corpus records in the input format used by this learning procedure. The public release does not include the Mars learning and evaluation pipeline; we assemble it from the published procedure, the released prompts, and the released ALFWorld learning and verification components, align observation and action representations across corpus ingestion, rule validation, and execution, and fix interface errors in the released code. Candidate rejection and reproposal follow the released execution loop. On Tacit-FLE (Table 1), disagreement between an action-matched executable check and the LLM prediction triggers one further query about the same action, which includes the code verdict and feedback, following the alignment step in Zhou et al. (2025b, Eq. 9); the revised prediction determines rejection, and when no matching check can be evaluated, the initial prediction is retained. A passing Boolean check records the absence of an encoded failure condition. The action-proposal loop permits five attempts per environment turn and passes the final proposal to the executor if the limit is reached. The Mars binding supplies spatial context through the current observation and bounded interaction history. 

**NeSyC.** We reconstruct the induction and rule-application procedures in Algorithms 1–2 of Choi et al. (2025), using the released implementation as a reference. The learner proposes answer-set rules from the corpus and refines them using contrasting transition examples. At evaluation, observations are translated into facts and combined with the learned program for symbolic planning. We connect the hypothesis score to iterative rule revision, completing the refinement loop described in the paper: solver checks provide feedback on labeled examples, with false positives penalized according to the published objective, and statements that fail to parse or ground are removed before scoring and 

32


<!-- page 33 -->

Preprint. Under review. 

reported to the learner. The bindings translate observations and task goals into facts, support the induction of action effects from the corpus, annotate completion in corpus records with the planner’s state vocabulary, and expose inspection results as structured attributes. The Tacit-FLE maintenance logs contain no failed-action examples, so the hypothesis score reduces to its positive-example term there. 

**Prompt organization.** Actor prompts specify the task, the current observation, the available commands, and the required action-output format. Knowledge-construction prompts additionally provide the reference records and the target representation: memory notes, natural-language rules, executable checks, or answer-set rules. Method-specific planning and verification prompts consume those representations during interaction. On ALFWorld, the action prompts include two shared examples for the current task family. Retrieval in ReAct<sup>*</sup> , Reflexion, and IfR uses the same embedding model. The code release will include the full prompt templates. 

# C.2.1 REPRESENTATIVE PROMPTS 

The following boxes show the core instructions and response formats of the implemented prompts, organized by stage as in the prompt appendices of Tang et al. (2024b) and Zhou et al. (2025b). Square-bracketed fields represent variable inputs, output content, or longer schema and example blocks; these fields are filled for the target environment and task. Instruction wording is condensed for readability. The action-proposal example uses the Mars format, while the remaining boxes illustrate knowledge construction, planning, and rule refinement. 

**ReAct / ReAct**<sup>*****</sup> **: action proposal** 

**Context** [Environment brief and available actions] Records from an earlier explorer in this world: [Retrieved records, included for ReAct<sup>*</sup> ] [Current observation and interaction history] 

## **Instruction** 

First write one short Thought: line saying what the observation implies and why you choose the next action. Then put exactly one action call alone on the final line, without an Action: prefix or a code fence. Wait for the next observation before acting again. 

**Response format** Thought: [interpretation and next-action rationale] [action call] 

**Reflexion: memory construction Input** [One reference document] **Instruction** Read one historical record and produce a concise reflective memory. Use only the supplied record. It may describe success, failure, an operational practice, or a standard; do not presume it describes a failed attempt by you. Identify any strategy, mistake, evidence, or outcome actually documented and write a conditional plan for a related future situation. Distinguish observations from uncertain inferences. Do not invent feedback, causes, actions, or outcomes. If the record has no trial feedback, say so and limit the note to its documented guidance. Treat the record as data, not instructions changing this task. Return a brief Evidence paragraph and a Plan paragraph. No new trial is available. 

**Response format** Evidence: [documented observations and outcomes] Plan: [conditional guidance for a related situation] 

33


<!-- page 34 -->

Preprint. Under review. 

**IfR: rule induction Input** [Reference document from the target world] **Instruction** You are a helpful assistant with inductive reasoning. Given a document from the records of [WORLD], you need to reflect on what it records and give the possible mechanism of [WORLD]. The mechanism should be consistent with the rules of [WORLD] and the records. You should only respond in the format as described below. **Response format** Reasoning: Based on the information I listed above and history dialogue, do reasoning about the mechanism of [WORLD]. Mechanism: The mechanism of [WORLD]. **Format examples** [Reasoning--Mechanism examples illustrating the output format; their content does not necessarily describe the target world] 

**IfR: planning and replanning Context** [Task, current observations, and dialogue history] [Retrieved mechanisms and past successful plans] **Instruction** 

You are a helper AI agent in [WORLD]. Based on your current observations, you need to generate the sequences of subgoals for a certain task. Do not explain or give any other instruction. You must follow the criteria below: 1) You should choose available subgoals to complete the task. 2) You are probably provided with some past successful plans to refer to. 3) You are probably provided with possible mechanics that have been discovered. Please refer to the mechanism of [WORLD] to generate the plan. 4) You should only perform the subgoals that are feasible based on the current observations. Here are available subgoals: [SUBGOALS] Here are some examples for output format: [PLAN EXAMPLES] Here is the brief of [WORLD]: [BRIEF] **Replanning message after execution feedback** Please fix the above errors and replan the task [TASK]. 

34


<!-- page 35 -->

Preprint. Under review. 

**WALL-E: rule mining Input** Transitions: [ _{_ "state ~~0~~ ": [state], "action": _{_ "name": [action name], "args": [arguments] _}_ , "action ~~r~~ esult": _{_ "feedback": [feedback], "success": [execution outcome] _}}_ , ...] Existing rules: [rule list] The environment’s action space: [ACTIONS] The environment’s state format: [STATE FORMAT] **Instruction** You are responsible for mining new rules from the given transitions, ensuring that these rules differ from the ones already provided. Focus on generating general and universal rules that are not tied to any specific item or tool. Extract and utilize only the features that influence the outcome of the action. Generate only the rules under what conditions the action will fail. While generating a rule, you also need to state how to check if a transition satisfies this rule. Please be specific as to which and how features need to be checked. Ensure the response can be parsed by Python json.loads. **Response format** _{_ "new ~~r~~ ules": [ "Rule [number]: For action [action], [failure condition]; Checking Method: [features and checks]" ] _}_ 

**WALL-E: rule compilation Input** [Learned rule and state/action format] Current Knowledge Graph: [KNOWLEDGE GRAPH] Current Scene Graph: [SCENE GRAPH] **Instruction** You are responsible for generating code rules by implementing the learned rules in Python. Write a function that takes the current state and an action as inputs, optionally incorporating the graph to provide additional contextual information. The function should return feedback, success, and suggestion. feedback: a string giving the action feedback. success: a bool indicating whether the action is executed successfully. If the action type is not the action type in the rule, count as success. suggestion: a string giving a suggestion based on the rule, state, and action if the action fails. The state and action arguments are dicts; action has the form _{_ "name": "...", "args": _{_ ... _}}_ . The graph argument has the form _{_ "knowledge": [knowledge graph], "scene": [scene graph] _}_ . Respond only with the function, without example usage or other text. **Response format** def expected ~~r~~ ule ~~c~~ ode(state, action, graph): [condition checks] return feedback, success, suggestion 

35


<!-- page 36 -->

Preprint. Under review. 

## **NeSyC: rule induction Input** 

[ASP grammar, environment vocabulary, and target command] [Batch of reference records] Background Knowledge: [background program] [Rule kind] so far: [current rules, or none yet] **Instruction** Use inductive logic programming in Answer Set Programming. Learn from interpretations: a positive example should be a model of the background and hypothesis; negative examples should not. Apply theta-subsumption when generalizing. Use the supplied vocabulary and records. Unknown labels are not negative examples. Return the complete set of [rule kind] for the target command after reading this batch: keep earlier rules these records still support, generalize where they allow, and add what they require. One complete rule per line. Effects must come from observed changes or the supplied API description; do not treat an unsuccessful task as an unexecutable action. Return only the requested ASP, without explanations or markdown. 

**Response format** [Complete ASP rule] [Additional complete ASP rules, one per line] 

## **NeSyC: contrastive refinement Input** 

[Background program and current rules] [Hypothesis score and contrastive feedback on labeled examples] **Instruction** Revise the learned ASP rules using the contrastive feedback. Apply theta-subsumption: prefer the more general clause that still covers every positive example and excludes every negative one. A positive example must be a model of background and rules; a negative example must not be. Constraint rules are the hypothesis to revise. Effect rules (update/4 heads) are kept as learned unless the feedback reports two rules deriving different values; in that case return the resolved effect rules as well. Unknown labels are not negative examples. Never define goal, action, available, step or changed in a rule head. Return the complete revised rule set, one complete rule per line, without explanations or markdown. **Response format** [Complete revised ASP rule] [Additional complete ASP rules, one per line] 

# D FULL RESULTS AND COST ACCOUNTING 

D.1 REPAIR SUCCESS BY SCALE AND TYPE 

Table A14 gives the successes and denominators behind Table 1. 

**NeSyC evaluation trajectories.** For NeSyC, repair success is 0/28 and 0/36 on the small and medium suites. Across the 3,000 evaluation turns, every executed action was waiting. Of the 64 initial planner outputs, 47 return no plan and 17 return a single waiting action. These observations explain its absence from the repair-candidate diagnostics in Appendix D.7. 

**Model conditions.** Table A15 retains the full success, spurious-intervention, and turn comparison behind Figure 4 on the same 36 medium tasks. The model condition applies to both knowledge construction and interaction. WALL-E and NeSyC are compared under Luna only (Table 1). 

36


<!-- page 37 -->

Preprint. Under review. 

Table A14: **Repair success counts in the Luna condition.** Successes over scheduled episodes behind Table 1. The small, medium, and large suites contain 28, 36, and 40 episodes, respectively. Unsuccessful episodes remain in the denominators. Bold: best per column, ties included. 

|||Small|||Medium|||Large||
|---|---|---|---|---|---|---|---|---|---|
|Method|Chain|Conj.|Elim.|Chain|Conj.|Elim.|Chain|Conj.|Elim.|
|ReAct|0/13|5/7|**6/8**|4/14|9/14|6/8|1/17|8/11|9/12|
|ReAct<sup>*</sup>|2/13|6/7|3/8|3/14|9/14|7/8|4/17|4/11|8/12|
|Reflexion|1/13|5/7|**6/8**|3/14|6/14|3/8|2/17|1/11|6/12|
|IfR|5/13|**7/7**|**6/8**|4/14|12/14|**8/8**|4/17|10/11|**12/12**|
|NeSyC|0/13|0/7|0/8|0/14|0/14|0/8|0/17|0/11|0/12|
|WALL-E|1/13|1/7|1/8|2/14|4/14|7/8|1/17|5/11|9/12|
|OntoAct (ours)|**9/13**|**7/7**|**6/8**|**8/14**|**14/14**|**8/8**|**14/17**|**11/11**|11/12|



Table A15: **Model conditions on medium Tacit-FLE (36 tasks).** SR: repair success (%); SI: mean spurious interventions; T: mean turns. Bold/underline: best/second-best within each condition. 

||ReAct|ReAct<sup>* </sup>|Reflexion|IfR|OntoAct|
|---|---|---|---|---|---|
|_Luna_||||||
|SR_↑_|52.8|52.8|33.3|66.7|**83.3**|
|SI_↓_|11.3|13.4|15.4|11.9|**2.4**|
|T_↓_|41.8|38.7|46.4|31.7|**19.4**|
|_Luna_<sup>_R_</sup>||||||
|SR_↑_|44.4|38.9|52.8|86.1|**97.2**|
|<br>SI_↓_|9.0|11.4|9.7|9.8|**0.8**|
|<br>T_↓_|42.8|45.3|42.1|26.7|**8.4**|
|_Terra_||||||
|SR_↑_|52.8|55.6|38.9|66.7|**100.0**|
|<br>SI_↓_|13.7|12.6|10.5|7.9|**0.4**|
|T_↓_|32.7|35.3|42.2|28.2|**8.4**|



37


<!-- page 38 -->

Preprint. Under review. 

# D.2 MARS ACROSS MODEL CONDITIONS 

Tables A16 and A17 give the full world-level results behind the additional conditions in Table 4. The Luna world-level results remain in Table 3. Each reported world-level result aggregates five evaluation episodes. NeSyC’s results appear in Tables 3, A16, and A17. 

**NeSyC planning behavior.** In our Luna reconstruction, 5,325 of 6,326 turns across the seven modified worlds execute a no-op. Erroneous or overly restrictive learned rules can prevent executable plans; for example, a Terrain rule imposes a tool-inventory requirement without restricting it to the relevant action, contradicting the initial state. The runtime falls back to waiting when planning fails, while rule refinement requires a refused executed command. These observations concern our reconstruction (Appendix C.2). 

Table A16: **Mars performance with Luna**<sup>_R_</sup> **.** Luna<sup>_R_</sup> ; five evaluation episodes per world. Reward is mean _±_ sample SD; Score pools achievement success rates across episodes. Average excludes Default; its Reward SD is computed across matched-seed world averages. Bold/underlined: best/second-best. Metric definitions are in Appendix E.3. 

|World|ReAct|ReAct<sup>*</sup>|Reflexion|IfR|NeSyC|WALL-E|OntoAct|
|---|---|---|---|---|---|---|---|
|_Reward ↑_||||||||
|Default|12_._30_±_4_._82|**15****_._46****_±_5****_._35**|11_._30_±_2_._28|10_._70_±_3_._21|5_._77_±_0_._58|9_._90_±_2_._77|10_._90_±_3_._56|
|Terrain|13_._10_±_2_._55|10_._10_±_5_._87|14_._50_±_1_._14|**15****_._98****_±_2****_._06**|_−_0_._57_±_0_._58|10_._30_±_3_._11|14_._06_±_5_._67|
|Survival|9_._70_±_5_._18|13_._70_±_5_._73|9_._10_±_6_._78|12_._50_±_3_._51|4_._07_±_3_._55|10_._50_±_6_._54|**13****_._88****_±_5****_._60**|
|Task dep.|5_._70_±_2_._30|2_._10_±_0_._71|2_._90_±_1_._30|**7****_._70****_±_3****_._13**|1_._77_±_1_._53|3_._70_±_2_._51|5_._70_±_1_._14|
|Terr. surv.|7_._50_±_2_._61|5_._30_±_3_._27|6_._90_±_2_._59|8_._30_±_3_._11|5_._10_±_1_._00|7_._10_±_2_._65|**8****_._50****_±_3****_._44**|
|Terr. task|5_._30_±_2_._28|6_._30_±_2_._68|5_._70_±_2_._51|6_._90_±_2_._28|0_._10_±_1_._00|4_._70_±_2_._07|**8****_._10****_±_1****_._87**|
|Surv. task|5_._50_±_5_._08|6_._10_±_4_._30|5_._90_±_5_._07|5_._90_±_5_._63|_−_0_._23_±_0_._58|2_._30_±_1_._48|**7****_._30****_±_6****_._57**|
|All three|0_._70_±_2_._19|**1****_._70****_±_1****_._67**|1_._10_±_1_._87|0_._90_±_1_._10|0_._10_±_1_._00|_−_0_._30_±_0_._89|0_._90_±_1_._79|
|Average|6_._79_±_1_._10|6_._47_±_1_._21|6_._59_±_1_._35|8_._31_±_0_._68|1_._48_±_0_._94|5_._47_±_0_._97|**8****_._35****_±_1****_._26**|
|_Score (%) ↑_||||||||
|Default|46_._65|**68****_._27**|26_._44|29_._64|3_._86|15_._82|30_._26|
|Terrain|32_._57|22_._80|35_._52|**56****_._87**|0_._17|19_._66|52_._42|
|Survival|21_._70|56_._98|23_._66|43_._88|3_._24|31_._41|**58****_._48**|
|Task dep.|7_._43|1_._51|2_._33|**9****_._09**|1_._42|3_._17|3_._92|
|Terr. surv.|**12****_._86**|6_._73|7_._99|10_._67|3_._62|8_._43|12_._43|
|Terr. task|5_._20|6_._77|6_._29|**8****_._10**|0_._62|4_._80|7_._87|
|Surv. task|10_._45|10_._03|12_._72|14_._60|0_._21|1_._50|**24****_._30**|
|All three|1_._19|1_._77|**1****_._89**|0_._97|0_._42|0_._51|1_._48|
|Average|13_._06|15_._23|12_._91|20_._60|1_._39|9_._93|**22****_._99**|



# D.3 MARS PER TRIAL 

Tables A18 and A19 report the recorded reward for each evaluation seed behind Table 3. The Luna comparison comprises seven methods, eight worlds, and seeds 0–4, for 280 episodes. Score is computed from achievement success rates pooled over the five episodes, as defined in Appendix E.3. 

D.4 MARS: APPLYING SHARED LEARNED CONDITIONS 

**Shared knowledge and evaluation scope.** We analyze the existing Luna trajectories from all seven modified worlds, with five evaluation seeds per world and method (35 episodes each). Both methods construct their knowledge before evaluation from the same 200 recorded transitions per world and keep their rule libraries fixed during these trajectories. The analysis distinguishes whether a method possesses a resource condition from whether its current action respects that condition. 

For each of the 14 paired knowledge-construction instances, we manually match explicit resource requirements for crafting and placement that both methods store correctly. We require an explicit material name; a requirement without a quantity supports only a minimum of one unit. This produces 22 pair-specific matches, including repeated conditions across instances; 13 of the 14 pairs have at 

38


<!-- page 39 -->

Preprint. Under review. 

Table A17: **Mars performance with Terra.** Terra; five evaluation episodes per world. Reward is mean _±_ sample SD; Score pools achievement success rates across episodes. Average excludes Default; its Reward SD is computed across matched-seed world averages. Bold/underlined: best/second-best. Metric definitions are in Appendix E.3. 

|World|ReAct|ReAct<sup>*</sup>|Reflexion|IfR|NeSyC|WALL-E|OntoAct|
|---|---|---|---|---|---|---|---|
|_Reward ↑_||||||||
|Default|10_._10_±_2_._74|10_._70_±_2_._97|10_._30_±_1_._10|**13****_._70****_±_2****_._88**|3_._50_±_1_._95|11_._30_±_2_._28|12_._50_±_2_._19|
|Terrain|11_._30_±_4_._21|10_._48_±_5_._82|11_._10_±_4_._85|**15****_._38****_±_4****_._55**|2_._28_±_2_._16|10_._12_±_4_._09|14_._04_±_3_._43|
|Survival|8_._10_±_5_._39|10_._28_±_6_._87|7_._10_±_3_._39|12_._78_±_8_._06|0_._70_±_0_._55|7_._10_±_4_._06|**15****_._50****_±_1****_._52**|
|Task dep.|6_._70_±_3_._51|6_._50_±_4_._34|6_._10_±_3_._94|7_._10_±_2_._24|0_._10_±_0_._00|4_._70_±_1_._82|**8****_._10****_±_3****_._94**|
|Terr. surv.|7_._50_±_2_._70|8_._10_±_4_._85|**9****_._90****_±_1****_._64**|5_._30_±_1_._30|1_._90_±_1_._10|4_._10_±_2_._35|6_._50_±_3_._13|
|Terr. task|**7****_._86****_±_1****_._87**|7_._68_±_3_._75|6_._90_±_1_._30|5_._10_±_1_._87|1_._10_±_0_._71|5_._50_±_2_._41|6_._10_±_2_._00|
|Surv. task|7_._50_±_5_._68|3_._30_±_5_._07|6_._30_±_3_._70|3_._10_±_2_._00|2_._70_±_0_._55|5_._10_±_3_._39|**7****_._90****_±_6****_._69**|
|All three|0_._30_±_1_._10|0_._70_±_2_._07|1_._30_±_1_._48|**3****_._10****_±_2****_._24**|_−_0_._70_±_0_._45|0_._70_±_2_._30|1_._50_±_2_._30|
|Average|7_._04_±_0_._86|6_._72_±_1_._59|6_._96_±_0_._86|7_._41_±_1_._82|1_._15_±_0_._51|5_._33_±_1_._15|**8****_._52****_±_1****_._54**|
|_Score (%) ↑_||||||||
|Default|21_._42|20_._03|18_._81|**42****_._95**|2_._98|23_._71|37_._87|
|Terrain|31_._84|33_._57|30_._44|**57****_._79**|1_._52|19_._18|38_._16|
|Survival|20_._77|37_._49|12_._58|50_._36|0_._49|12_._92|**57****_._22**|
|Task dep.|9_._43|12_._13|9_._74|8_._20|0_._23|4_._92|**14****_._43**|
|Terr. surv.|10_._06|**14****_._47**|14_._23|5_._08|1_._13|4_._57|8_._66|
|Terr. task|7_._49|**9****_._97**|6_._77|5_._08|0_._77|5_._25|6_._38|
|Surv. task|17_._17|6_._30|9_._32|2_._43|1_._55|6_._52|**23****_._35**|
|All three|0_._64|1_._44|1_._56|**3****_._10**|0_._15|1_._19|2_._81|
|Average|13_._91|16_._48|12_._09|18_._86|0_._84|7_._79|**21****_._57**|



least one match. The metric checks only these shared resource requirements against the inventory at action selection. Terrain, workstations, tools, and other feasibility conditions are outside this metric. 

**Candidates, commands, and denominators.** For OntoAct, the initial candidate is the first singleaction proposal in the current turn, before verification feedback. For IfR, it is the next executable step selected from the plan after processing the previous action’s outcome. We do not test future plan steps against the current inventory or count plan steps discarded while processing a preceding failure. Every candidate and command included in Table 5 has an observed inventory. 

The methods follow different trajectories, so their denominators count their own eligible candidates or issued commands rather than matched states. For OntoAct, the 245 initial candidates comprise 70 resource violations and 175 candidates satisfying the shared resource conditions. All 70 violations are redirected to gathering or exploration before execution. Another 39 candidates are redirected after terrain or workstation feedback, leaving 136 original crafting or placement commands to execute. For IfR, all 107 selected candidates are issued unchanged, including all 20 resource violations. The redirection row conditions on violating candidates only: 70 for OntoAct and 20 for IfR. 

**Timing and outcome of revision.** The 70 pre-execution redirections by OntoAct occur in 19 episodes across six worlds. The alternatives produce 54 controller successes and 16 failures, where controller success refers to the issued command. Of the 20 violations issued by IfR, 19 continue an existing plan without a new LLM call and one follows a fresh plan. All 20 attempts fail and together consume 20 environment steps. Each is followed immediately by an explanation and replanning turn that selects a different command outside the shared crafting and placement scope; these alternatives yield 16 controller successes and four failures. Thus, both methods revise their behavior, but the observed revisions occur before a known-invalid attempt for OntoAct and after the attempt for IfR. 

**Coverage beyond shared conditions.** The zero violations in Table 5 apply to the shared learned conditions. When the check is expanded to every actual resource requirement of OntoAct’s 781 issued crafting or placement commands, all 363 violations occur among the 622 commands whose action lacks an explicit typed resource-cost rule; the 159 commands whose actions have such rules contain none. 

39


<!-- page 40 -->

Preprint. Under review. 

Table A18: **Mars reward per evaluation seed (1/2).** Luna; all seven methods and seeds 0–4 from Table 3. Each seed column is one recorded episode reward; the final column reports the mean and sample SD across the five seeds. 

|World|Method|Seed 0|Seed 1|Seed 2|Seed 3|Seed 4|Mean_±_SD|
|---|---|---|---|---|---|---|---|
|Default|ReAct|7.10|17.10|7.10|13.10|6.10|10_._10_±_4_._80|
||ReAct<sup>*</sup>|10.10|11.10|7.10|8.10|10.10|9_._30_±_1_._64|
||Reflexion|8.10|3.10|8.10|11.10|9.10|7_._90_±_2_._95|
||IfR|6.10|7.10|11.10|6.10|10.10|8_._10_±_2_._35|
||NeSyC|1.10|0.10|1.10|1.10|0.10|0_._70_±_0_._55|
||WALL-E|5.10|16.10|7.10|0.10|3.10|6_._30_±_6_._06|
||OntoAct (ours)|13.10|12.10|13.10|10.10|12.10|12_._10_±_1_._22|
|Terrain|ReAct|9.10|6.10|7.10|12.10|9.10|8_._70_±_2_._30|
||ReAct<sup>*</sup>|13.10|12.10|12.10|17.40|6.10|12_._16_±_4_._03|
||Reflexion|11.10|3.10|2.10|13.10|14.00|8_._68_±_5_._66|
||IfR|10.10|3.10|9.10|14.10|10.10|9_._30_±_3_._96|
||NeSyC|-0.90|-0.90|-0.90|-0.90|-0.90|_−_0_._90_±_0_._00|
||WALL-E|5.10|4.10|5.10|12.10|11.10|7_._50_±_3_._78|
||OntoAct (ours)|11.10|13.10|10.10|12.10|15.10|12_._30_±_1_._92|
|Survival|ReAct|2.10|4.10|8.10|9.10|12.10|7_._10_±_4_._00|
||ReAct<sup>*</sup>|4.10|11.10|8.10|12.10|12.10|9_._50_±_3_._44|
||Reflexion|1.10|3.10|8.10|14.10|5.10|6_._30_±_5_._07|
||IfR|1.10|9.10|5.10|7.10|14.10|7_._30_±_4_._82|
||NeSyC|1.10|0.10|1.10|2.50|0.10|0_._98_±_0_._99|
||WALL-E|1.10|1.10|9.10|12.10|8.10|6_._30_±_4_._97|
||OntoAct (ours)|2.10|16.00|5.10|14.10|15.00|10_._46_±_6_._39|
|Task dep.|ReAct|3.10|4.10|5.10|3.10|5.10|4_._10_±_1_._00|
||ReAct<sup>*</sup>|1.10|4.10|4.10|3.10|2.10|2_._90_±_1_._30|
||Reflexion|9.10|3.10|2.10|4.10|2.10|4_._10_±_2_._92|
||IfR|7.10|6.10|9.10|7.10|7.10|7_._30_±_1_._10|
||NeSyC|1.10|1.10|1.10|0.10|1.10|0_._90_±_0_._45|
||WALL-E|3.10|5.10|4.10|3.10|4.10|3_._90_±_0_._84|
||OntoAct (ours)|12.10|10.10|12.10|10.10|12.10|11_._30_±_1_._10|



40


<!-- page 41 -->

Preprint. Under review. 

Table A19: **Mars reward per evaluation seed (2/2).** Luna; all seven methods and seeds 0–4 from Table 3. Each seed column is one recorded episode reward; the final column reports the mean and sample SD across the five seeds. 

|World|Method|Seed 0|Seed 1|Seed 2|Seed 3|Seed 4|Mean_±_SD|
|---|---|---|---|---|---|---|---|
|Terr. surv.|ReAct|4.10|8.10|3.10|7.10|8.10|6_._10_±_2_._35|
||ReAct<sup>*</sup>|7.10|6.10|12.10|7.10|8.10|8_._10_±_2_._35|
||Reflexion|3.10|7.10|6.10|1.10|8.10|5_._10_±_2_._92|
||IfR|3.10|2.10|6.10|6.10|13.10|6_._10_±_4_._30|
||NeSyC|3.10|5.10|0.10|2.10|3.10|2_._70_±_1_._82|
||WALL-E|7.10|0.10|3.10|2.10|7.10|3_._90_±_3_._11|
||OntoAct (ours)|10.10|2.10|6.10|5.10|8.10|6_._30_±_3_._03|
|Terr. task|ReAct|5.10|1.10|5.10|3.10|3.10|3_._50_±_1_._67|
||ReAct<sup>*</sup>|8.10|7.10|3.10|8.10|8.10|6_._90_±_2_._17|
||Reflexion|5.10|5.10|6.10|5.10|11.00|6_._48_±_2_._56|
||IfR|4.10|2.10|4.10|2.10|7.10|3_._90_±_2_._05|
||NeSyC|0.10|2.10|2.10|1.10|0.10|1_._10_±_1_._00|
||WALL-E|4.10|3.10|0.10|3.10|4.10|2_._90_±_1_._64|
||OntoAct (ours)|10.10|4.10|5.10|10.10|9.10|7_._70_±_2_._88|
|Surv. task|ReAct|2.10|3.10|12.10|14.10|1.10|6_._50_±_6_._11|
||ReAct<sup>*</sup>|-0.90|0.10|2.10|6.10|3.10|2_._10_±_2_._74|
||Reflexion|2.10|1.10|3.10|7.10|5.10|3_._70_±_2_._41|
||l<br>IfR|2.10|2.10|10.10|9.10|9.10|6_._50_±_4_._04|
||NeSyC|1.10|3.10|1.10|4.10|2.10|2_._30_±_1_._30|
||WALL-E|2.10|0.10|4.10|10.10|12.10|5_._70_±_5_._18|
||OntoAct (ours)|-0.90|0.10|5.10|11.10|12.10|5_._50_±_6_._02|
|All three|ReAct|2.10|5.10|-0.90|-0.90|-0.90|0_._90_±_2_._68|
||ReAct<sup>*</sup>|3.10|1.10|-0.90|5.10|-0.90|1_._50_±_2_._61|
||Reflexion|1.10|2.10|-0.90|0.10|0.10|0_._50_±_1_._14|
||IfR|-0.90|-0.90|2.10|0.10|-0.90|_−_0_._10_±_1_._30|
||NeSyC|-0.90|-0.90|-0.90|-0.90|-0.90|_−_0_._90_±_0_._00|
||WALL-E|3.10|1.10|-0.90|0.10|0.10|0_._70_±_1_._52|
||OntoAct (ours)|2.10|4.10|-0.90|-0.90|1.10|1_._10_±_2_._12|



41


<!-- page 42 -->

Preprint. Under review. 

# D.5 ALFWORLD FULL RESULTS 

Table A20 reports the three evaluated methods—NeSyC, WALL-E, and OntoAct—under standard and disclosed initial observations, with the input and output tokens behind the Luna condition in Table 6. 

**Initial-state disclosure.** Initial object locations specify which receptacle contains each object at episode reset, including contents that the agent has not yet observed through exploration. Inventory specifies the objects held by the agent, or explicitly states that its hands are empty. For this control, the initial object locations and inventory are appended as ordinary observation sentences to the first textual observation. The same disclosure procedure is applied to all three methods. Subsequent observations use the standard interface; no additional target annotations or action-effect rules are supplied. The model, learned knowledge, 134 unseen tasks, seed, and 49-step budget remain the same across the two observation conditions. 

Table A20 reports both conditions for every method. With disclosure, OntoAct completes 134/134 tasks rather than 132/134, and WALL-E completes 133/134 rather than 129/134; both also use fewer steps and evaluation tokens. Our NeSyC reconstruction completes 0/134 tasks under standard observations: initially unobserved target objects prevent planning, and all 6,566 executed steps are idle actions. With disclosure it completes 35/134 tasks. The _†_ rows in Tables 6 and A21 use this disclosed-state run for NeSyC, while the OntoAct and WALL-E rows use standard observations. 

**Evaluation call roles.** Across the 134 standard-observation tasks, all 1,833 evaluation calls by OntoAct propose actions; learned conditions are checked symbolically. The 3,862 calls by WALLE comprise 2,036 action proposals and 1,826 outcome predictions. These counts reconcile with Table A20: the methods execute 1,805 and 1,985 environment steps, giving 1.02 and 1.95 LLM calls per step, respectively. The prediction calls account for 90.0% of the 2,029-call difference and consume 1,919,113 tokens, or 92.2% of the observed evaluation-token difference. Knowledge-construction costs are reported separately (Table A25). 

Table A20: **ALFWorld with and without initial-state disclosure (Luna).** Each method uses the same learned knowledge and 134 unseen tasks in both conditions, with one attempt and a 49-step budget per task. Success gives completed tasks; Steps, Calls, and input (In) and output (Out) tokens in thousands are means over all 134 episodes, including failures. The disclosure condition supplies initial object locations and inventory to every method. 

|||Standar|d obser|vations|||Initial-|state dis|closure||
|---|---|---|---|---|---|---|---|---|---|---|
|Method|Success|Steps|Calls|In (k)|Out (k)|Success|Steps|Calls|In (k)|Out (k)|
|NeSyC|0/134|49.0|1.0|5.82|0.06|35/134|38.6|9.3|269.33|11.99|
|WALL-E|129/134|14.8|28.8|47.08|0.61|133/134|7.8|15.6|27.83|0.38|
|OntoAct (ours)|132/134|13.5|13.7|32.00|0.15|134/134|6.7|8.3|23.28|0.15|



Table A21 reports success by task family; following Shridhar et al. (2021), the families are Pick & Place, Clean & Place, Heat & Place, Cool & Place, Examine in Light, and Pick Two & Place. 

Table A21: **ALFWorld success (%) by task family under the Luna condition.** The six families follow Shridhar et al. (2021); parentheses give the number of unseen tasks. All is success over all 134 tasks, weighted by family size. Best values are bold; second-best All values are underlined. Ties share the same formatting.<sup>_†_</sup> Initial object locations and inventory are additionally provided to NeSyC. 

||Pick|Clean|Heat|Cool|Examine|Pick two||
|---|---|---|---|---|---|---|---|
|Method|(24)|(31)|(23)|(21)|(18)|(17)|All|
|NeSyC<sup>_†_</sup>|75.0|0.0|34.8|0.0|0.0|52.9|26.1|
|WALL-E|**100.0**|**96.8**|95.7|**100.0**|88.9|94.1|96.3|
|OntoAct (ours)|**100.0**|**96.8 **|**100.0 **|**100.0**|**94.4**|**100.0 **|**98.5**|



42


<!-- page 43 -->

Preprint. Under review. 

# D.6 LLM USAGE 

We separate knowledge-construction usage from evaluation usage. Construction costs are measured per construction run: for a plant in Tacit-FLE, a world in Mars, or a training corpus in ALFWorld. Evaluation costs are summed over the associated evaluation tasks and also reported per episode. 

For WALL-E in Table 1, construction usage includes the original construction costs of every knowledge base used in the evaluation protocol of Appendix E.1, including reused knowledge. Evaluation costs cover only the reported episodes. 

Table A22 reports the Tacit-FLE usage under Luna. Construction is a one-time cost per plant. OntoAct processes each document with the typed schema and elicits operating practices over the joined corpus, so its construction cost per plant exceeds that of WALL-E, IfR, and Reflexion. Evaluation dominates the total: on medium, construction for the 15 plants sums to 0.88M tokens against 9.6M evaluation tokens for OntoAct, which uses the fewest evaluation tokens per episode at every scale (excluding NeSyC). 

Table A22: **Tacit-FLE LLM usage (Luna).** Construction calls and tokens are per plant (15 plants per scale); evaluation calls and tokens are per episode (28, 36, and 40 episodes). Tokens sum input and output in thousands (k). ReAct and ReAct<sup>*</sup> construct no knowledge; NeSyC, which executes no repair action (Appendix D.1), is omitted. 

||Constru<br>|ction (per plant) <br>|Evaluatio<br>|n (per episode)<br>|
|---|---|---|---|---|
|Method|Calls|Tokens (k)|Calls|Tokens (k)|
|_Small_|||||
|ReAct<br>|0|0|22.2|154.6|
|ReAct<sup>*</sup>|0|0|22.9|166.6|
|Reflexion|6.8|2.3|23.2|170.4|
|IfR|6.8|3.7|13.8|135.3|
|WALL-E|13.4|11.7|88.0|436.6|
|OntoAct (ours)|13.1|14.8|16.2|128.0|
|_Medium_|||||
|ReAct|0|0|41.8|619.0|
|ReAct<sup>*</sup>|0|0|38.7|564.1|
|Reflexion|32.0|10.6|46.4|734.3|
|IfR|32.0|17.1|21.5|422.0|
|WALL-E|39.1|34.9|152.9|1574.0|
|OntoAct (ours)|48.8|58.7|27.1|265.5|
|_Large_|||||
|ReAct<br>|0|0|48.8|1204.3|
|ReAct<sup>*</sup>|0|0|56.4|1403.6|
|Reflexion|63.1|20.7|63.1|1606.2|
|IfR|63.1|33.8|32.2|1038.9|
|WALL-E|71.5|62.8|170.6|2541.4|
|OntoAct (ours)|95.8|119.7|24.6|309.4|



For Mars, Table A23 reports evaluation costs for all model conditions and Table A24 reports construction costs. Each method–model aggregate in these tables covers 40 evaluation episodes across eight worlds. Figure 5 uses the 35 Luna episodes from the seven modified worlds, matching the main performance average. For each world, we divide the total evaluation input and output tokens by the total executed environment steps across its five episodes. We then average these seven rates with equal world weights; the figure’s Score is the corresponding mean of the seven pooled world Scores. Environment steps count primitive controller interactions, not LLM calls or high-level command proposals. This rate normalizes for interaction length, and the figure pairs it with achievement Score. Knowledge-construction costs are excluded from this rate and reported separately. 

For the same seven-world Luna population, pooled input tokens per call are 2.36k for OntoAct and 4.26k for ReAct<sup>*</sup> . Their equally weighted world-average call rates are similar: 0.3655 and 0.3639 

43


<!-- page 44 -->

Preprint. Under review. 

per environment step. Prompt inspection shows that OntoAct supplies compact learned conditions, whereas ReAct<sup>*</sup> retains five retrieved transition documents; both retain ten turns of history. Across all 35 paired initial observations, which are identical between methods, first-call input averages 1,053 versus 2,982 tokens. The usage difference therefore lies primarily in input context. 

The ALFWorld evaluation costs appear alongside success in Table 6, with the full breakdown in Appendix D.5. Table A25 reports the separate knowledge-construction costs. 

An LLM call is one completed model response, including internal planning and verification responses; token counts are those reported by the provider. Input/call is the total input tokens divided by the number of recorded calls; it measures the mean context supplied to the model. Total tokens is the sum of input and output tokens before rounding, averaged per evaluation episode or per construction run as specified in each table. Knowledge-construction, planning, explanation, and verification calls are assigned to their corresponding phase. 

Table A23: **Mars evaluation resource use.** Means over 40 episodes per method and model (eight worlds, five episodes each). Steps are environment steps; Calls, In, Out, and Total tokens are per episode. Input/call is mean input tokens per call; Total tokens sums input and output before rounding. Token quantities are in thousands (k). Knowledge-construction costs are reported separately in Appendix D.6. 

|Method|Steps|Calls|In (k)|Out (k)|Input/call<br>(k)|Total tokens<br>(k)|
|---|---|---|---|---|---|---|
|_Luna_|||||||
|ReAct<br>|198.6|60.8|109.13|1.42|1.79|110.55|
|ReAct<sup>*</sup>|252.5|83.0|354.22|2.12|4.27|356.35|
|Reflexion|249.5|75.8|174.74|2.05|2.31|176.79|
|IfR|218.2|55.2|298.10|12.45|5.40|310.55|
|NeSyC|177.9|183.1|2237.98|13.65|12.22|2251.63|
|WALL-E|220.0|204.1|544.71|5.26|2.67|549.97|
|OntoAct (ours)|304.8|103.8|244.95|1.01|2.36|245.95|
|_Luna_<sup>_R_</sup>|||||||
|ReAct<br>|220.4|69.0|127.57|7.70|1.85|135.27|
|ReAct<sup>*</sup>|267.2|91.2|395.61|11.01|4.34|406.62|
|Reflexion|258.0|83.0|198.72|9.60|2.39|208.33|
|IfR|291.7|60.5|320.37|32.28|5.30|352.65|
|NeSyC|208.6|192.3|2182.93|114.77|11.35|2297.70|
|WALL-E|228.6|148.9|379.76|15.21|2.55|394.97|
|OntoAct (ours)|306.6|84.5|204.36|11.29|2.42|215.64|
|_Terra_|||||||
|ReAct|252.1|69.9|126.91|2.13|1.82|129.04|
|ReAct<sup>*</sup>|262.6|70.1|300.29|2.15|4.28|302.45|
|Reflexion|211.6|62.8|148.76|1.98|2.37|150.73|
|IfR|256.0|42.8|207.06|7.34|4.84|214.39|
|NeSyC|188.1|183.6|2067.74|13.62|11.27|2081.36|
|WALL-E|210.3|146.2|319.72|2.81|2.19|322.53|
|OntoAct (ours)|334.1|91.9|219.66|0.91|2.39|220.57|



44


<!-- page 45 -->

Preprint. Under review. 

Table A24: **Mars knowledge-construction resource use.** Calls, In, Out, and Total tokens are per construction run. NeSyC constructs its rules once per world (eight runs); its rule refinements during play are counted as evaluation (Table A23). ReAct and ReAct<sup>*</sup> require no LLM-based knowledge construction; their input length is undefined. Input/call is mean input tokens per call; Total tokens sums input and output before rounding. Token quantities are in thousands (k). 

|Method|Calls|In (k)|Out (k)<br>I|nput/call<br>(k)|Total tokens<br>(k)|
|---|---|---|---|---|---|
|_Luna_||||||
|ReAct<br>|0|0|0|—|0|
|ReAct<sup>*</sup>|0|0|0|—|0|
|Reflexion|20.0|12.76|2.61|0.64|15.38|
|IfR|20.0|18.28|3.88|0.91|22.16|
|NeSyC|63.5|3768.39|33.08|59.34|3801.47|
|WALL-E|255.3|1069.25|24.59|4.19|1093.84|
|OntoAct (ours)|1.0|10.91|1.34|10.91|12.25|
|_Luna_<sup>_R_</sup>||||||
|ReAct|0|0|0|—|0|
|ReAct<sup>*</sup>|0|0|0|—|0|
|Reflexion|20.0|12.76|5.01|0.64|17.77|
|IfR|20.0|18.28|7.04|0.91|25.32|
|NeSyC|63.5|3739.88|79.09|58.90|3818.98|
|WALL-E|228.1|1001.05|51.70|4.39|1052.75|
|OntoAct (ours)|1.0|11.00|3.19|11.00|14.19|
|_Terra_||||||
|ReAct|0|0|0|—|0|
|ReAct<sup>*</sup>|0|0|0|—|0|
|Reflexion|20.0|12.76|3.25|0.64|16.02|
|l<br>IfR|20.0|18.28|3.14|0.91|21.42|
|NeSyC|63.5|3729.85|12.96|58.74|3742.80|
|WALL-E|225.6|996.33|11.87|4.42|1008.20|
|OntoAct (ours)|1.0|11.20|1.12|11.20|12.32|



Table A25: **ALFWorld knowledge-construction LLM usage (Luna).** Totals for one construction run per method on the shared 238-transition corpus. Each resulting knowledge base is reused across 134 evaluation tasks. Token quantities use thousands of tokens (k); Total tokens sums input and output before rounding. Costs exclude corpus collection and evaluation. 

|Method|Calls|In (k)|Out (k)|Total tokens (k)|
|---|---|---|---|---|
|NeSyC|79|1989.08|8.62|1997.70|
|WALL-E|254|349.37|14.84|364.21|
|OntoAct (ours)|15|116.43|0.94|117.36|



45


<!-- page 46 -->

Preprint. Under review. 

# D.7 TACIT-FLE CANDIDATE AND VERIFICATION DIAGNOSTICS 

These post hoc analyses use the 104 Luna episodes in Table 1: 28 small, 36 medium, and 40 large episodes from 15 plant worlds per scale. Anonymized identifiers are decoded only in this analysis, to compare a proposed target with the benchmark’s hidden fault target. Target alignment measures whether a candidate names the fault. NeSyC is excluded from these diagnostics because its inspected trajectories contain no repair executions. 

**Replacement candidates and coverage.** For OntoAct and WALL-E, we extract replacement proposals before their native action-verification procedures, including rejected proposals. For IfR, we parse replacement steps in each newly generated plan, including steps that are not subsequently executed. Quoted dialogue history, inspection targets, and explanation-only text are excluded. Within each episode, we retain distinct replacement targets in order of first proposal. If _Ce_<sup>(</sup><sup>_k_)</sup> is the first _k_ distinct targets and _c_<sup>_∗_</sup> _e_<sup>the true fault, coverage is</sup> 



<!-- Start of picture text -->
N<br>Coverage @ k = N 1 � ⊮ {c ∗ e ∈ C e ( k ) }. (A1)<br>e =1<br><!-- End of picture text -->

Episodes with fewer than _k_ candidates retain their complete observed candidate set and remain in the denominator. Table 2 reports _k_ = 3 and full-sequence counts on medium plants; Table A26 additionally reports _k_ = 1 and _k_ = 5 across all scales. Candidate precision divides the number of target-aligned episode–target pairs by the number of distinct proposed episode–target pairs. We use 20,000 paired world-cluster bootstrap draws within each scale and report percentile 95% intervals. The coverage-at-three difference between OntoAct and IfR has intervals of [26.7, 66.7], [33.3, 81.0], and [62.2, 90.2] percentage points across the three scales. 

Table A26: **Replacement-candidate diagnostics.** Targets is the mean number of distinct proposed replacement targets per episode. C@ _k_ and C@all are true-fault coverage (%) within the first _k_ targets and the complete sequence. Precision is correct-target/total episode–target pairs. Small, medium, and large contain 28, 36, and 40 episodes. 

|Scale|Method|Targets|C@1|C@3|C@5|C@all|Precision|
|---|---|---|---|---|---|---|---|
|Small|OntoAct (ours)|2.68|50.0|75.0|82.1|82.1|23/75|
||WALL-E|4.79|3.6|35.7|50.0|50.0|14/134|
||IfR|5.79|10.7|28.6|50.0|64.3|18/162|
|Medium|OntoAct (ours)|3.36|33.3|69.4|75.0|88.9|32/121|
||WALL-E|5.14|0.0|27.8|36.1|47.2|17/185|
||IfR|9.00|0.0|11.1|38.9|66.7|24/324|
|Large|OntoAct (ours)|2.78|57.5|87.5|92.5|97.5|39/111|
||WALL-E|5.70|5.0|22.5|37.5|52.5|21/228|
||IfR|14.38|0.0|10.0|20.0|65.0|26/575|



Table A27: **Selection within the hypothesis ledger.** Target-aligned/all tracked at baseline, then target-aligned/retained at later checkpoints (retained: open or confirmed). The last two rows give final target-aligned retention and off-target refutation; terminal-only hypotheses (9/15/14 by scale) are excluded. 

|Checkpoint / measure|Small|Medium|Large|
|---|---|---|---|
|All tracked|20/140|28/272|34/192|
|Checkpoint +1|19/68|23/112|31/98|
|Checkpoint +2|19/48|21/61|28/68|
|Checkpoint +3|19/32|20/36|28/42|
|Final|18/21|20/21|25/32|
|True-target retention|18/20|20/28|25/34|
|Off-target removal|117/120|243/244|151/158|



46


<!-- page 47 -->

Preprint. Under review. 

**Native hypothesis selection.** A registered OntoAct hypothesis is identified by its cause, pattern reference, and ordered atoms. The registered totals are 149, 287, and 206 across small, medium, and large, corresponding to 5.32, 7.97, and 5.15 per episode. Different conditions can name the same cause: the medium cohort contains 155 distinct episode–cause pairs, or 4.31 per episode. For the selection analysis, we follow the 140, 272, and 192 hypotheses that are visible at the start of a later turn. The remaining 9, 15, and 14 hypotheses are admitted only on the terminal turn and are excluded from both the initial and retained sets. Retained hypotheses are open or confirmed at the start of the final environment turn. Table A27 gives target precision, target-aligned retention, and off-target removal on this matched population. Figure 3 follows this same population at three intermediate checkpoints aligned by each hypothesis’s admission. For a hypothesis admitted at turn _a_ in an episode of _T_ turns, checkpoint + _k_ reads its status at the start of turn min( _a_ + _k, T_ ), for _k ∈{_ 1 _,_ 2 _,_ 3 _}_ ; Final reads turn _T_ . An episode that has already ended retains its last recorded status. The Init. baseline includes every hypothesis in the matched population before selection. At each later checkpoint, target precision is the fraction naming the true fault among open or confirmed hypotheses. Selection includes updates after unsuccessful interventions. 

Table A28: **Precision of executed replacement commands.** Each cell gives the percentage and correct-target/total commands. Repeated targets are counted each time. These final executions are distinct from proposed candidates and native gate passes. 

|Method|Small|Medium|Large|
|---|---|---|---|
|OntoAct (ours)|29.3% (22/75)|25.4% (29/114)|36.4% (36/99)|
|WALL-E|2.3% (3/133)|5.2% (12/232)|3.8% (14/364)|
|IfR|9.9% (18/182)|5.6% (24/426)|3.7% (26/694)|
|ReAct<br>|8.9% (11/124)|4.7% (15/321)|3.5% (17/482)|
|ReAct<sup>*</sup>|5.6% (11/197)|4.3% (17/392)|2.2% (15/688)|
|Reflexion|8.6% (12/140)|3.1% (12/387)|1.3% (8/600)|



**Explicit refutation and execution.** We separately link repair proposals, verifier feedback, and the action executed in the same turn. For explicit refutation, we count one choice per episode, environment turn, repair verb, and target, over both replacement and refill proposals. In the medium OntoAct cohort, 139 choices receive explicit refutation feedback; 137 target a noncausal unit, and all 137 are withheld or revised in that turn. Deduplicating across turns leaves 31 off-target choices among 33 distinct episode–verb–target choices. Explicit refutation is a subset of all negative gate decisions. Across all scales, 233 of 241 explicitly refuted choices are off-target and withheld in the corresponding turn. Refutations can follow an unsuccessful earlier repair, contradicted observations, or an explained anomaly disappearing. 

For broader gate diagnostics, we use the first decision on each distinct replacement target within a turn. For OntoAct, negative decisions include explicit repair, practice, or repetition feedback. For WALL-E, the decision is the final world-model Boolean after any code-conflict feedback, before execution at the proposal limit. IfR provides post-action explanations and replanning, without a corresponding pre-action verifier veto; a verifier rejection rate is therefore undefined for this method. Table A28 counts the replacement commands actually executed, including repeated targets and actions executed at the proposal limit. 

Repeated off-target repairs provide a separate outcome diagnostic. We count an executed repair command to a noncausal target as repeated if an earlier repair command in the same episode targeted that unit, including a change of repair verb. Across the 104 matched episodes, OntoAct, WALL-E, and IfR issue 13, 633, and 280 such repeats, respectively. 

**Illustrative traces.** The following cases illustrate distinct mechanisms. In a medium chain task, OntoAct proposes replacing the faulty input storage under an induced diagnostic pattern but omits its required inflow atom. The claim is not admitted, and the first executed action opens the storage. The next proposal adds the missing atom and replaces the target, completing the episode in two turns with no spurious intervention. On the same task, WALL-E initially predicts failure for an off-target locomotive replacement at turn 18. Executable-rule feedback changes the prediction to success, and the replacement executes; the episode finishes unresolved after 60 turns with 11 spurious interventions. The contrast illustrates how action-feasibility feedback can differ from evidence that a target explains the fault. 

47


<!-- page 48 -->

Preprint. Under review. 

In a medium elimination task, OntoAct’s five tracked hypotheses narrow to one naming the true target, st-04. Three hypotheses on st-00 or st-01 are refuted after earlier replacements fail to end the episode, and the anomaly explained by the st-02 hypothesis clears. The st-04 hypothesis remains confirmed, and the episode succeeds in eight turns with two spurious interventions. 

# E EXPERIMENTAL SETUP AND REPRODUCIBILITY 

This appendix specifies the reference corpora, evaluation schedules, model configurations, and aggregation rules used in Section 4.1. Knowledge construction and prompts are described in Appendices B.2, B.4, and C.2. 

## E.1 REFERENCE CORPORA AND EVALUATION TASKS 

Each evaluation episode starts with fresh interaction history and transient state. 

**Tacit-FLE.** We use the fixed reference corpora and evaluation population in Appendix A.4, with the scale-specific episode counts and turn budgets in Table A6. Corpus access follows the OntoAct construction procedure in Appendix B.2 and the baseline procedures in Appendix C.2. 

For WALL-E in Table 1, each scale uses one corpus-learned knowledge base for each of its 15 worlds. All knowledge bases remain fixed during evaluation. Each episode contributes one outcome under the procedure in Appendix C.2. 

**Mars.** Following the evaluation configuration of Zhou et al. (2025b), we use Default and seven worlds formed by changing terrain, survival mechanics, task dependencies, or their combinations. Methods share the same reference corpus of 200 recorded transitions per world. Each record contains the observed state, action, outcome, feedback, and subsequent state. For document-based processing, consecutive groups of ten records form 20 documents per world. 

The agent receives a textual local observation, including a 9 _×_ 9 view, nearby objects, inventory, and health, food, drink, and energy levels. The high-level commands are mine, attack, explore, make, place, and sleep. Each episode is capped at 1,000 environment steps and 1,000 agent turns, with ten turns of interaction history. A high-level command can consume multiple environment steps. Each method is evaluated on five seeds per world, giving 40 episodes across eight worlds for each model condition. 

**ALFWorld.** We use the text interface and all 134 unseen evaluation tasks, with the six task families and their sizes listed in Table A21. The reference corpus contains 238 transitions from six training games, one per task family. In each training game, 20 exploratory probes precede an expert-policy trajectory; the resulting corpus contains both successful and unsuccessful interactions. The same fixed corpus is used to construct each method’s knowledge. Each unseen task is evaluated once with a budget of 49 environment steps. OntoAct and WALL-E use standard textual observations; the reported NeSyC result additionally provides initial object locations and inventory (Appendix D.5). Environment steps include submitted think and idle commands; internal LLM calls are counted separately. We report the Luna condition for this benchmark. 

## E.2 MODEL AND INFERENCE SETTINGS 

The Luna condition uses the gpt-5.6-luna model with reasoning effort set to none. The Luna<sup>_R_</sup> condition uses the same model with reasoning effort medium; the Terra condition uses gpt-5.6-terra with effort none. Each condition uses its designated model for both knowledge construction and evaluation. We retain the provider’s default temperature settings and use the same model configuration across methods within a comparison. The Mars and ALFWorld runs cap each completion at 8,192 tokens. Retrieval uses the OpenAI text-embedding-3-small embedding model. The environment-specific proposal budgets of OntoAct are listed in Table A13. 

48


<!-- page 49 -->

Preprint. Under review. 

# E.3 TASK METRICS AND AGGREGATION 

**Tacit-FLE.** We aggregate the metrics defined in Appendix A.4.1 over all scheduled episodes at each plant scale and, where specified, by task type. 

**Mars.** Episode reward sums the environment rewards: one unit for the first completion of each achievement, together with a health-change contribution of 0 _._ 1 per health unit. We report the mean and sample standard deviation of episode reward over five evaluation episodes in each world, using denominator _n −_ 1 for the sample variance. For achievement _i_ in evaluation episode _r_ , let _zir_ = 1 if the achievement is attained at least once and 0 otherwise. Following the achievement-success-rate metric of Tang et al. (2024b), let _pi_ = (100 _/n_ )<sup>�</sup><sup>_n_</sup> _r_ =1<sup>_zir_be the percentage of episodes attaining</sup> achievement _i_ , with _n_ = 5. The achievement score is 



<!-- Start of picture text -->
22<br>1<br>Score = exp 22 � log(1 +  pi ) − 1 . (A2)<br>� i =1 �<br><!-- End of picture text -->

Success rates are computed across the five episodes within each world, model, and method before applying the geometric aggregation. This yields one Score per cell. Following the average-row convention of Zhou et al. (2025b), the cross-world summary excludes the Default world. The Score Average is the arithmetic mean of the seven modified-world Scores. For Reward, we first average the seven modified worlds within each matched environment seed; the Average row reports the mean and sample standard deviation across the five resulting seed averages. 

**ALFWorld.** Task success is the fraction of the 134 unseen tasks for which the environment reports completion within the step budget. Mean environment steps are the total executed steps divided by the number of evaluation tasks, including unsuccessful episodes. Environment steps count executed commands; internal planning and verification calls contribute to LLM usage instead. 

49
