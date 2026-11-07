---
source: 2611.02395-solver-like-behavior.pdf
part: appendix
converted: 2026-11-07
converter: pymupdf4llm
---

# Solver-Like Behavior in Large Language Models as Formalizers · 附录

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

# **A Experimental Details** 

Each model receives one zero-shot prompt per problem, built from a prefix for the formal language 

12


<!-- page 13 -->

and an output format for the task (Appendix D). We extract the program from the model’s final answer and run it: Python and Z3 programs with the Python interpreter, and PDDL domains and problems with the Fast Downward planner. The output is scored as in Appendix B, and each generation is labeled by the ontology judges (Appendix E). Each dataset contributes the same 100 randomly sampled problems in both formal languages. Table 2 lists every run: 6,000 generations, of which the 2,000 under the baseline prompt are used in §5. It also counts the programs flagged as not written in the requested formal language: those that import a library outside the standard library in Python, or Z3 programs that never import Z3 or never call the solver. PDDL is not checked, since a planner rejects anything else. 

**Artifacts and licenses.** Calendar Scheduling and Meeting Planning come from NaturalPlan (Zheng et al., 2024) (code Apache 2.0, data CC BY 4.0), ZebraLogic from Lin et al. (2025) (released for evaluation, without a stated license), and BlocksWorld from the IPC domain (IPC, 1998). All are evaluation benchmarks, and we use them only for evaluation. GPT-OSS-120B, Qwen3.827B and Gemma 4 31B-it are released under Apache 2.0 and run locally; DeepSeek-V4-Flash is used through its API under DeepSeek’s terms of service. We release our code, prompts, model outputs and labels under the MIT license for research on formalizers. 

**Software and compute.** Local models and judges run on vLLM 0.32.0 (PyTorch 2.13), one NVIDIA H100 NVL (94 GB) per model instance; GPT-OSS-120B uses its released MXFP4 weights and the Gemma judges FP8. Python and Z3 programs run under Python 3.12 with z3-solver 4.14– 4.15 and a 30-second limit. PDDL is solved by Fast Downward (commit 487e33c, alias lama-first), and plans are validated by VAL (commit 3c7a1f3). Tokens are counted with tiktoken’s cl100k_base. Generation and judging, including judge development and §6, took roughly 150 H100 GPU-hours by our logs, plus the DeepSeek API calls. Decoding settings (Appendix C) are fixed for all runs; we did no hyperparameter search. 

# **B Tasks and Datasets** 

Each dataset consists of constraint satisfaction problems (CSPs) (Russell and Norvig, 2009) stated in natural language, from which we sample 100 

||||N|ot in|FL|
|---|---|---|---|---|---|
|Model|Task|FL|0|A|B|
|DeepSeek|Calendar|Python|0|0|0|
||Meeting|Python|0|0|0|
||ZebraLogic|Z3|0|0|1|
||BlocksWorld|PDDL|–|–|–|
|GPT-OSS|Calendar|Python|0|0|0|
||Calendar|Z3|0|0|0|
||Meeting|Python|0|0|0|
||Meeting|Z3|0|0|0|
||ZebraLogic|Python|0|0|0|
||ZebraLogic|Z3|0|0|0|
||BlocksWorld|Python|0|0|0|
||BlocksWorld|PDDL|–|–|–|
|Qwen|Calendar|Python|0|0|0|
||Calendar|Z3|0|0|0|
||Meeting|Python|0|0|0|
||Meeting|Z3|3|5|2|
||ZebraLogic|Python|0|0|0|
||ZebraLogic|Z3|0|0|0|
||BlocksWorld|Python|0|0|0|
||BlocksWorld|PDDL|–|–|–|



Table 2: Runs: each model, task and formal language has 300 generations (100 problems under each of three prompts; 6,000 in total). Not in FL: programs not written in the requested FL under the baseline (0) and Cautionary A and B prompts. DeepSeek is run in one FL per dataset. 

problems with their ground-truth solutions. Every dataset is formalized in Python, restricted to the standard library, and in a declarative formal language: Z3 for Calendar Scheduling, Meeting Planning and ZebraLogic, and PDDL (Ghallab et al., 1998) for BlocksWorld. 

**Calendar Scheduling** (Zheng et al., 2024) involves scheduling meetings among multiple people given their existing constraints and availability windows. Models must find time slots that satisfy duration requirements and avoid conflicts with busy intervals for all participants. 

**Meeting Planning** (Zheng et al., 2024) focuses on coordinating multi-location meetings with logistical constraints including people, locations, available time windows, and travel time between locations. Solutions require planning feasible itineraries that respect temporal and spatial constraints. 

**ZebraLogic** (Lin et al., 2025) presents logic grid puzzles where models must determine which attributes (e.g., colors, pets, drinks) belong to which entities (e.g., houses, people) based on a set of logical clues. In Z3, the program states the clues as constraints over the attributes; in Python, it must search the assignments itself, typically by enumer- 

13


<!-- page 14 -->

ating permutations. 

**BlocksWorld** (IPC, 1998) is classical planning: rearranging blocks into a goal configuration under additional constraints. In PDDL, the model writes a domain and a problem, given a reference problem that omits the additional constraint (in 53 of the 100 instances it therefore differs from the ground-truth problem), and the Fast Downward planner finds the plan; in Python, the program prints the plan itself. Either plan is checked by the VAL validator against the ground-truth domain and problem. 

**Accuracy.** For each problem instance, we construct a constraint JSON containing relevant restrictions and verify that the program’s output violates none of them. Since multiple valid solutions may exist for some of the tasks (e.g. Calendar Scheduling), a generation is marked correct if the program executes successfully and its output satisfies all constraints, and incorrect otherwise. For Meeting Planning, the itinerary is simulated step by step against the start location and time, the travel times, and each friend’s location, availability window, and minimum meeting duration; since the goal is to meet as many friends as possible, it must also meet at least as many friends as the ground-truth solution. For ZebraLogic, the printed grid must match the ground-truth solution. For BlocksWorld, the plan, found by the planner for a PDDL formalization or printed by a Python program, must be valid under the ground-truth domain and problem, and for unsolvable instances the formalization must be proven unsolvable or the program must report that no plan exists. Ten of the 100 BlocksWorld instances are unsolvable; for one of them the planner cannot prove unsolvability within its time limit even from the ground-truth PDDL, so PDDL accuracy on BlocksWorld is at most 99%. 

# **C Model Details** 

We evaluate on three models with varying reasoning capabilities. All models support extended reasoning modes that produce explicit reasoning traces before generating code, making them suitable for analyzing solver-like behavior. 

**DeepSeek-V4-Flash** (DeepSeek-AI et al., 2025) is a large reasoning model accessed via the DeepSeek API with thinking enabled, reasoning effort _medium_ , and at most 131,072 output tokens. 

**GPT-OSS-120B** (OpenAI et al., 2025) is a 120billion-parameter model run locally with vLLM at reasoning effort _medium_ (temperature 0.7, top- _p_ 

0.9), generating up to the 131,072-token context window. 

**Qwen3.8-27B** (Qwen Team, 2025) is a 27billion-parameter model run locally with vLLM with thinking enabled (temperature 0.7, top- _p_ 0.9), generating up to the 131,072-token context window. 

All models are evaluated as formalizers, prompted to generate executable Python code (or Z3/PDDL, where appropriate) that returns the solution upon execution. 

**DeepSeek in one FL.** DeepSeek is run in one FL per dataset: Python for Calendar Scheduling and Meeting Planning, Z3 for ZebraLogic, and PDDL for BlocksWorld. The model served under its API name changed before our runs in the other FL: rerunning 20 earlier prompts with the same settings gives traces 4–5 times shorter, on every problem. Since its runs in the other FL would compare two different models, we leave them out. 

# **D Prompt Configurations** 

We evaluate each model under three prompting conditions to assess whether explicit warnings can deter solver-like behavior. All prompts consist of the same two parts: (i) a prefix for the formal language (Python, Z3 or PDDL) that instructs the model to formalize the problem, and (ii) a task-specific output format, which for Z3 also gives the import and the coding steps. 

**Baseline** is the default prompt. The Python and Z3 prefixes instruct the model to write a program that “solves it directly rather than solving it yourself in prose.” The baseline discourages solving in natural language only implicitly. The PDDL prefix has no such clause; it supplies the ground-truth problem PDDL as a reference for the initial and goal states, and asks for a domain and a problem that encode the problem’s constraints. The baseline measures how much solver-like behavior persists under an ordinary formalization instruction. 

**Cautionary A** frames solver-like behavior by its outcome: the model works out the answer in its reasoning trace, and the code then just outputs that precomputed result. It contrasts a solver-like and a sound response to a multi-step wage problem with a conditional bonus; the sound response lists the given values and enumerates the computation steps without performing any arithmetic. It closes with an explicit instruction not to compute intermediate values or final answers during reasoning. 

14


<!-- page 15 -->

**Cautionary B** defines solver-like behavior by the act itself: substituting the given values into arithmetic, or deriving an intermediate or final result in the trace, before any code is written. It illustrates this with a single-step GSM8K problem, and its sound example refers to the given values only abstractly. It closes by instructing the model to reason only about the variables and constraints and to outline the steps a program would take. 

Listings 1–3 show the three prompts in Python for Calendar Scheduling; Listing 5 shows the Z3 prefix with its Calendar Scheduling output format, and the PDDL prefix. The cautionary prompts add the same warning to every prefix. 

Both cautionary prompts use math word problems rather than benchmark instances, so they leak no task-specific solutions but require the model to transfer the contrast to scheduling, logic, and planning. This design allows us to test whether explicit prompt variations reduce solver-like behavior and whether such reductions change formalization performance (§6). 

**Batching and placeholders** (§6) change the problem part of the baseline prompt instead of adding a warning. A batched prompt uses the baseline prefix in the plural (“You are given _K_ constraint satisfaction problems (CSPs) of the same kind . . . enclose each problem’s complete solution in its own code block”), lists the problems under headers “### Problem _i_ ”, gives the output format once, and ends with the instruction at the top of Listing 4. Each problem is assigned the program headed by its number. A placeholder prompt is the baseline prompt with the problem rewritten in placeholders and preceded by a note on them (Listing 4). Before execution, the program is prefixed with the definition of VALUES (and, for Meeting Planning, TRAVEL), and placeholder names in its output are mapped back to their values. The A judge sees the placeholder problem, with a note that choosing among placeholder values counts as SLB. Batch groups are fixed by a seeded shuffle of the 100 problems, so every model and FL sees the same groups. 

# **E Ontology Judges and Their Reliability** 

All LLM judges use Gemma 4 31B-it (FP8, temperature 0, thinking mode), which is not one of the evaluated models; their prompts were fixed before the labeling runs. Reference labels are sampled evenly across each judge’s predicted labels, so rare 

labels such as _hardcoded_ are tested as often as common ones. Because the judges were developed on traces in the FLs DeepSeek is run in, A1 and B are also checked by a human on held-out traces in each dataset’s other FL. Each judge’s input, output and reliability check are as follows; Listings 6–8 give their prompts. 

**Segments and paragraphs.** The A1 judge labels paragraphs, a unit a human can also label, but a whole trace is too long for one request (a DeepSeek trace averages 26,572 tokens). We therefore cut each trace into segments of at most 2,000 tokens (counted with the cl100k_base tokenizer). Cuts fall between paragraphs, i.e. at blank lines; only a paragraph longer than a whole segment is cut between sentences. Each segment is then divided into numbered units for labeling: its paragraphs, where a paragraph over 700 characters is cut at line breaks (and a very long line at sentence ends) into pieces of at most about 700 characters. One request holds the problem and one segment, and states which segment of how many it is; the judge returns one label per unit and sees no other segment, so the context of a unit is its own segment. We keep segments short because long ones made the judge loop: in a pilot with an earlier prompt, 6,000-token segments looped until the output budget ran out in 83% of responses, against 7% at 2,000 tokens. The 2,000 generations of §5 give 14,027 segments (median 3 per trace, at most 58; 31% of traces fit in one) and 372,234 units (median 24 per segment, median length 153 characters). The 2,046 units (0.5%) that the judge’s response leaves unlabeled count as _none_ . The solver-like ratio is the share of a trace’s characters in units labeled _SLB_ , over all its segments. The other judges read one request per trace. The A2 judge reads the trace condensed to its _SLB_ units, in order, with “[...]” marking each run of units left out. The B judge reads the whole trace; the two traces longer than 400,000 characters keep their first 50,000 and last 350,000. 

**A1 (existence).** The judge labels every paragraph of a segment, given the problem. Its prompt distinguishes paragraphs that establish values (V), argue a property of the whole solution set such as uniqueness (P), both (VP), or neither (N); V and VP are _SLB_ , and P and N are _none_ . The prompt defines the decision variables of each task and lists what is not solver-like (restating, encoding design, checking the encoding on a hypothetical example, assuming solvability, and one-off checks of what a constraint means). Three rounds of human labels 

15


<!-- page 16 -->

(60 paragraphs, the third balanced by the judge’s predictions) plus 10 paragraphs selected to probe arguments about the solution set give 70 references. The judge agrees on 66/70 (49/52 on paragraphs not paraphrased in its prompt), with precision and recall of _SLB_ of 20/22 each. In the other FL of each dataset (the one DeepSeek is not run in), a human labeled 40 paragraphs blind (10 per dataset, half of them predicted _SLB_ , one per trace): the judge agrees on 37/40 ( _SLB_ precision 18/20, recall 18/19; Table 1 reports these blind labels), and on 39/40 after the annotator reviewed the disagreements, with precision 19/20 and recall 19/19. The remaining miss is a boundary case: a paragraph that mostly interprets a soft preference but ends by choosing between two candidate answers found earlier. 

**A2 (extent).** The judge reads only the paragraphs labeled _SLB_ , condensed into one text, and the program’s output, and states whether they contain a complete answer, which it writes in the task’s output format. Because the traces are too long for annotators to read in full, the label _complete_ was verified by humans, and _partial_ labels were checked by searching the trace for the program’s answer and by a second model reading the passages found. The judge agrees on 20/20 traces in the first round and 19/20 in the second (the miss follows from an A1 error). 

**B (program).** The judge sees the problem, the trace (its beginning and end when long) and the program with its output, and returns a label with the evidence for it; a script sets B to n/a when the program fails or prints nothing. Only decisions the trace had to solve for count as inherited: a restriction read off the problem statement, or a preference encoded as a hard constraint, leaves the program independent. On 20 programs balanced by predicted label, the judge agrees with blind reference labels on 19. These reference labels were written by a second model, and the prompt’s examples were drawn from them, so this agreement is optimistic. On 20 held-out programs that the judge labels _hardcoded_ (10) or _partly fixed_ (10), a human shown the judge’s evidence agreed with all 20 labels. These programs are concentrated in two cells: every hardcoded one is GPT-OSS on Meeting Planning, where hardcoding is common, and 9 of the 10 partly fixed ones are BlocksWorld. In the other FLs, a human shown the judge’s evidence checked 20 further programs, 9 of them in Z3: 10 that the judge labels B1–B3 (3 each of _hardcoded_ and _steered_ , 4 _partly fixed_ ) and, as a check of recall, 10 that it labels _indepen-_ 

_dent_ although the trace reached a complete answer, shown next to the program. The human agrees on 18/20: all 10 _independent_ labels, and 8 of the 10 others. In the two misses the judge took a program detail for inheritance: an action order labeled _steered_ cannot change the result, because the shortest plan is unique, and a _partly fixed_ name order is the problem’s listing order, left in by a missing loop. 

**Placeholder traces.** The A judge was developed on traces that name concrete values. In placeholder traces (§6), a human read 20 paragraphs it labels _none_ that mention placeholders alongside words such as _first_ or _earliest_ : all 20 interpret the problem or design the code, so none is a missed SLB paragraph. Of 10 random paragraphs it labels _SLB_ , the human judged 4 solver-like, such as one that orders the placeholder times and sweeps two calendars for a free slot; the other 6 reason about the program’s behavior on unseen values or interpret a constraint. The judge thus overcounts SLB in placeholder traces, so the reduction placeholders achieve is, if anything, understated. 

**C (output).** C1 and C2 are deterministic scripts given the reasoning answer extracted for A2: C1 parses the reasoning answer and the program’s output with the task’s parsers and compares them, and C2 runs the task’s validator on the reasoning answer. A reasoning answer that the task’s parser cannot read makes C1 n/a, and we report how often this happens. 

**Checks over all traces.** Two checks over all traces agree with the reference comparisons. Of the 1,314 complete reasoning answers that can be compared with the program’s output, 88% match it exactly, which an A2 extraction that invented answers would not achieve. The A and B judges run independently, yet only 6 of the 163 programs labeled B1–B3 come from traces without _SLB_ , the combination the ontology rules out. 

# **F Full Results** 

Table 3 lists the ontology labels of every run, in both formal languages and under all three prompts. It is generated from the per-generation labels by scripts/paper_figures.py. 

# **G Labeled Examples** 

Figures 7 and 8 show real outputs with the labels of the final judges (§4, Appendix E). Text is quoted verbatim except for elisions marked [...] and the 

16


<!-- page 17 -->

|Model|Task|FL|Con|d.<br>Acc.|SLB|Cmpl.|Part.|Ratio|SLB tok.|B1|B|2|B3|B4|n/a|C1 no|C2 no|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|DeepSeek|Calendar|Python|0|0.93|100|100|0|0.21|2,496|0||1|2|91|5|0/95|3/99|
||||A|0.99|100|100|0|0.17|2,833|0||0|0|100|0|0/100|1/100|
||||B|0.97|100|100|0|0.18|2,676|0||0|1|97|1|0/99|2/100|
||Meeting|Python|0<br>|0.92<br>|98<br>|97<br>|1<br>|0.28<br>|15,561<br>|0<br>||2 <br>|13<br>|76<br>|7<br>|7/89<br>|0/90<br>|
||||A|0.93|100|90|10|0.22|13,529|0||0|6|88|6|11/83|2/87|
||||B|0.93|100|98|2|0.24|14,284|0||0|9|81|6|8/90|0/90|
||ZebraLogic|Z3|0|0.94|100|98|2|0.22|4,189|0||0|0|94|6|0/92|0/97|
||||A|0.94|99|85|14|0.16|3,401|0||0|0|98|2|0/84|3/85|
||||B|0.96|100|95|5|0.21|3,833|0||1|0|97|2|0/93|1/95|
||BlocksWorld|PDDL|0|0.76|84|38|46|0.06|2,245|0||5|0|94|0|18/28|4/27|
||||A|0.76|88|34|54|0.05|1,882|0||5|0|95|0|19/30|3/29|
||||B|0.71|67|28|39|0.04|1,538|0||5|0|94|1|11/18|5/17|
|GPT-OSS|Calendar|Python|0|0.98|99|98|1|0.30|476|0||0|0|99|1|2/98|2/98|
||||A|0.97|84|81|3|0.23|369|0||0|0|98|2|3/80|3/81|
||||B|0.97|66|65|1|0.16|256|0||0|1|97|2|1/64|0/65|
|||Z3|0|096|88|88|0|022|355|0||0|0|97|3|5/85|2/86|
||||A|.<br>0.91|85|84|1|.<br>0.21|344|0||2|0|91|7|1/76|1/80|
||||B|0.95|64|63|1|0.15|220|0||1|0|95|4|2/61|2/61|
||Meeting|Python|0|0.66|98|85|13|0.45|1732|40|1|1|0|42|7|19/72|25/68|
||||A|0.74|78|60|18|0.26|,<br>692|0|1|5|2|76|7|14/40|6/35|
|||Z3|B<br>0|0.79<br>0.38|68<br>69|56<br>63|12<br>6|0.23<br>0.19|519<br>724|1<br>0|1|7<br>4|0<br>0|81 <br>60|10<br> 25|22/48 <br>9/29|10/41<br>6/23|
||||A|0.44|62|46|16|0.13|354|0|1|3|0|66|21|4/26|2/22|
||||B|0.33|58|41|17|0.12|317|0||9|0|58|33|8/21|4/18|
||ZebraLogic|Python|0|0.86|78|56|22|0.24|548|0|1|7|0|75|8|3/55|4/56|
||||A|0.86|52|29|23|0.12|174|0|1|1|0|80|9|0/29|0/29|
||||B|0.85|66|40|26|0.18|365|0|1|1|0|80|9|2/40|1/40|
|||Z3|0|0.84|60|47|13|0.16|345|0||2|0|86|12|1/45|2/47|
||||A|0.87|68|49|19|0.17|364|0||5|0|87|8|0/47|1/49|
||||B|0.85|37|28|9|0.07|124|0||1|0|95|4|2/27|2/28|
||BlocksWorld|Python|0|0.34|56|40|16|0.18|399|7||6|0|85|2|12/36|13/36|
||||A|028|35|20|15|009|191|1||4|0|95|0|5/16|6/16|
||||B|.<br>0.34|37|27|10|.<br>0.11|185|5||2|0|93|0|9/26|13/26|
|||PDDL|0|052|7|2|5|001|22|0||4|0|96|0|1/1|0/0|
||||<br>A|.<br>0.54|10|3|7|.<br>0.02|49|0||5|0|95|0|0/0|0/0|
||||B|0.45|7|1|6|0.01|24|0||4|0|96|0|0/0|0/0|
|Qwen|Calendar|Python|0|0.97|100|100|0|0.21|1,291|0||0|3|96|1|3/99|3/100|
||||A|0.97|100|100|0|0.15|1,174|0||0|1|98|1|1/99|3/100|
||||B|0.96|100|100|0|0.13|1,178|0||0|1|98|1|3/99|4/100|
|||Z3|0|0.85|100|100|0|0.17|1,154|0||0|1|86|13|0/87|2/97|
||||A|0.88|99|99|0|0.14|1,161|0||0|3|87|10|1/89|1/91|
||||B|0.81|100|100|0|0.12|1,076|0||0|0|82|18|0/81|1/93|
||Meeting|Python|0|0.89|100|100|0|0.31|10,434|0||0|9|85|6|27/92|11/92|
||||A|0.88|100|90|10|0.25|7,571|0||0|3|91|6|21/83|7/80|
||||B|096|100|98|2|029|10079|0||2|5|91|2|23/92|11/88|
|||Z3|0|.<br>0.27|100|94|6|.<br>0.17|,<br>6,397|0||1|0|28|71|<br>8/23|<br> 11/65|
||||A|025|96|79|17|011|3611|0||0|1|25|74|6/20|8/50|
||||B|.<br>0.18|100|83|17|.<br>0.14|,<br>4,876|0||0|0|<br>23|<br> 77|8/18|11/48|
||ZebraLogic|Python|0|0.95|100|100|0|0.20|2,360|0||5|0|91|4|4/96|4/100|
||||A<br>|0.95<br>|98<br>|87<br>|11<br>|0.16<br>|1,520<br>|0<br>||0<br>|0<br>|96<br>|4<br>|2/85<br>|4/87<br>|
||||B|0.96|97|95|2|0.14|2,312|0||2|0|94|4|1/90|1/93|
|||Z3|0|059|100|100|0|022|2014|0||2|0|60|38|3/62|4/95|
||||A|.<br>0.59|97|78|19|.<br>0.13|,<br>1,011|0||0|0|<br>59|<br> 41|1/46|2/65|
||||B|0.56|94|91|3|0.15|1,322|0||2|0|54|44|1/54|4/78|
||BlocksWorld|Python|0|0.66|100|100|0|0.20|5,742|0||8|0|91|0|21/100|29/99|
||||A|0.67|100|96|4|0.16|4,551|0||4|1|95|0|24/96|28/95|
||||B|0.67|100|99|1|0.16|4,577|0||8|0|92|0|28/99|28/98|
|||PDDL|0<br>|0.71<br>|62<br>|41<br>|21<br>|0.04<br>|913<br>|0 <br>|1<br>|0<br>|0<br>|90<br>|0<br>|21/30<br>|9/29<br>|
||||A|0.69|63|21|42|0.04|835|0||7|0|93|0|9/13|4/12|
||||B|0.69|63|27|36|0.03|765|0||7|0|93|0|16/21|7/19|



Table 3: Ontology labels per cell (100 generations). FL: formal language (DeepSeek: one per dataset). Cond.: 0 = Baseline, A and B = Cautionary A and B. Acc.: program accuracy. SLB: % of traces with SLB (A1). Cmpl., Part.: % of traces with a complete or partial reasoning answer (A2). Ratio: mean solver-like ratio. SLB tok.: mean solver-like tokens per trace. B1–B4, n/a: % of programs. C1 no: reasoning answers that differ from the program’s output, of those compared. C2 no: wrong reasoning answers, of those checked. 

17


<!-- page 18 -->

GPT-OSS channel markers, which we remove. 

18


<!-- page 19 -->

**Problem** (calendar_scheduling_example_32, GPT-OSS-120B, Baseline): schedule a 30-minute meeting for Emily, Melissa and Frank between 9:00 and 17:00 on Monday. Emily is busy 10:00–10:30, 11:30–12:30, 14:00–15:00, 16:00–16:30; Melissa 9:30–10:00, 14:30–15:00; Frank 10:00–10:30, 11:00–11:30, 12:30–13:00, 13:30–14:30, 15:00–16:00, 16:30–17:00. Frank does not want to meet on Monday after 9:30. 

**1 none** We need to parse the problem. We have to formalize variables and constraints, then write python code that solves it. The task description: schedule a meeting for Emily, Melissa and Frank for half an hour between work hours 9:00 to 17:00 on Monday. Existing schedules given. Additional constraint: Frank do not want to meet on Monday after 9:30. Means meeting must start no later than 9:30? Actually “after 9:30” means after 9:30 (i.e., start after 9:30?), but Frank does not want to meet after 9:30. So meeting must be at or before 9:30 start, and duration 30 minutes, so meeting must be within 9:00-9:30? Let’s see. 

**2 none** Work hours 9:00-17:00. Frank busy intervals: 10:00-10:30, 11:00-11:30, 12:30-13:00, 13:30-14:30, 15:00-16:00, 16:30-17:00. 

**3 SLB** Frank does not want to meet after 9:30, meaning meeting must finish by 9:30? [. ..] So meeting must be within 9:00-9:30 (start at 9:00, end at 9:30). Let’s check other participants: Emily has meetings 10:00-10:30 etc, none before 10:00, so she is free 9:00-10:00. Melissa is busy 9:30-10:00, so she is free 9:00-9:30. So the only common free slot before constraints is 9:00-9:30. That fits Frank’s preference. 

**4 SLB** Thus answer: [’Monday’, ’09:00’, ’09:30’] 

**5 none** We need to produce code that reads nothing (hardcode data) and outputs that list. Use constraints solving approach maybe brute force intervals. 

**6 none** We’ll parse intervals as minutes from midnight. Define work start end. Build busy intervals for each participant. Add constraint that meeting duration 30 minutes, start >= work_start, end <= work_end, and must not intersect any busy interval of any participant. Also constraint Frank preference: meeting end <= 9:30? [...] The earlier reasoning gave unique solution 9:00-9:30. We’ll enforce meeting end <= 9:30 to be safe. 

**7 none** Implement algorithm: iterate start minute from work_start to work_end - duration inclusive. For each start, end=start+duration. Check constraints and break when found. Print list with formatting. 

**8 none** Let’s write code accordingly. 

**Program** (excerpt; it prints [’Monday’, ’09:00’, ’09:30’], scored correct): 

<mark>frank_latest_end = to_min("09:30")</mark> **<mark>def</mark>** <mark>feasible(start): end = start + duration</mark> **<mark>if</mark>** <mark>start < work_start</mark> **<mark>or</mark>** <mark>end > work_end:</mark> **<mark>return</mark>** <mark>False</mark> **<mark>if</mark>** <mark>end > frank_latest_end:</mark> **<mark>return</mark>** <mark>False # Frank's preference</mark> **<mark>for</mark>** <mark>person, intervals</mark> **<mark>in</mark>** <mark>busy_min.items():</mark> **<mark>for</mark>** <mark>b_start, b_end</mark> **<mark>in</mark>** <mark>intervals:</mark> **<mark>if</mark>** <mark>overlaps(start, end, b_start, b_end):</mark> **<mark>return</mark>** <mark>False</mark> **<mark>return</mark>** <mark>True</mark> **<mark>for</mark>** <mark>minute</mark> **<mark>in range</mark>** <mark>(work_start, work_end - duration + 1):</mark> **<mark>if</mark>** <mark>feasible(minute): solution = [day, to_str(minute), to_str(minute + duration)];</mark> **<mark>break</mark>** 

**Labels. A1** SLB (paragraphs 3–4). **A2** complete: Monday 9:00–9:30. **Solver-like ratio** 0.28. **B4** independent; judge’s evidence: “The program encodes all provided busy schedules and the preference constraint (‘end <= 9:30’) and searches for a feasible slot using a loop.” **C1** yes, **C2** yes. 

Figure 7: A trace with every paragraph and its A1 label. Paragraph 1 only interprets Frank’s preference, which is not solver-like; paragraph 3 checks the schedules and rules out every slot but one. Although the trace has already found the unique answer, the program searches for it independently (B4), so the SLB is wasted. 

19


<!-- page 20 -->

**B1 Hardcoded** meeting_planning_example_66, GPT-OSS-120B, Baseline _Trace:_ “Calculate times: 9:00 AM start. Wait until 10:58 AM departure. Travel 17 min, arrive at 11:15 AM (since 10:58+17=11:15). Meet from 11:15 to 1:15 (120 min). That satisfies.” <mark>itinerary = [ "You start at Nob Hill at 9:00AM.", "You wait until 10:58AM.", "You travel to Presidio in 17 minutes and arrive at 11:15AM.", "You meet Robert from 11:15AM to 1:15PM." ]</mark> **<mark>print</mark>** <mark>(itinerary)</mark> _Judge:_ “The program defines a list ‘itinerary’ containing the final answer strings derived in the prose and prints it without performing any computation.” **B2 Partly fixed** meeting_planning_example_73, GPT-OSS-120B, Baseline _Trace:_ “We can travel from Russian Hill to Pacific Heights (7 min) arriving at 9:07AM. Then we can meet from 9:07 to 10:07 (60 min) which is within Barbara’s presence (till 10PM). That satisfies constraints. [. . . ]” 

<mark>start = datetime.datetime(2023, 1, 1, 9, 0) # 9:00AM travel_minutes = 7 meet_minutes = 60 arrive = start + datetime.timedelta(minutes=travel_minutes) meet_end = arrive + datetime.timedelta(minutes=meet_minutes) itinerary = [ f"You start at Russian Hill at {fmt(start)}.", f"You travel to Pacific Heights in {travel_minutes} minutes and arrive at {fmt(arrive)}.", f"You meet Barbara from {fmt(arrive)} to {fmt(meet_end)}." ]</mark> **<mark>print</mark>** <mark>(itinerary)</mark> _Judge:_ “The program implements a specific itinerary decided in the prose, using a fixed meeting duration of 60 minutes and a pre-determined sequence of events.” 

**B3 Steered** meeting_planning_example_91, Qwen3.8-27B, Baseline _Trace:_ “[. . . ] likely expected: [’You start at Russian Hill at 9:00AM.’, ’You travel to Richmond District in 14 minutes and arrive at 9:14AM.’, ’You wait until 7:00PM.’, ’You meet Daniel for 75 minutes from 7:00PM to 8:15PM.’]” ... “If we choose earliest departure (start at 9:00) and earliest meeting (7:00), output expected. That’s a reasonable tie-breaker [...]” 

**<mark>for</mark>** <mark>depart</mark> **<mark>in range</mark>** <mark>(start_time, 24 * 60): arrive = depart + travel_time earliest_meet =</mark> **<mark>max</mark>** <mark>(arrive, friend_start) latest_meet = friend_end - required_minutes</mark> **<mark>if</mark>** <mark>latest_meet < earliest_meet:</mark> **<mark>continue for</mark>** <mark>meet_start</mark> **<mark>in range</mark>** <mark>(earliest_meet, latest_meet + 1): key = (0, depart, meet_start, arrive, meet_start - arrive)</mark> **<mark>if</mark>** <mark>best</mark> **<mark>is</mark>** <mark>None</mark> **<mark>or</mark>** <mark>key < best[0]: best = (key, depart, arrive, meet_start)</mark> 

_Judge:_ “The program uses a tie-breaking key (0, depart, meet_start, arrive, meet_start - arrive) to ensure the search returns the earliest possible departure and meeting time, a choice the reasoning explicitly states was made to reproduce the specific itinerary derived in the prose.” 

Figure 8: Programs labeled B1–B3, each with an excerpt of the solver-like trace it follows and the B judge’s evidence. All three are scored correct. The hardcoded program only prints the itinerary from the trace; the partly fixed one computes the times but along the single itinerary chosen in the trace; the steered one searches all departures and meeting times, but with a tie-break chosen so that the search returns the itinerary the trace expected. 

20


<!-- page 21 -->

- You are given a constraint satisfaction problem (CSP) expressed in natural language: a set of entities, constraints between them, and a goal state that must be reached without violating any constraint. Formalize the variables and constraints from the text, then write a Python program that solves it directly rather than solving it yourself in prose. Use only the Python standard library, enclose the complete solution in a single ````` python code block, and have the program print only the final answer in the exact format specified below. 

- CRITICAL: Your Python code block must be a complete, executable script with no prose, explanations, or natural language mixed into the code. Any text inside the ````` python block must be valid Python syntax (code or comments only). All reasoning, explanations, or commentary must appear OUTSIDE the code block. The code must run without syntax errors when executed directly. 

{PROBLEM} 

This problem is a calendar-scheduling task: find a single meeting time that fits every participant's availability. 

Print only a Python list of three strings —day, start time, end time. 

Rules: the day must be a full weekday name (e.g. "Monday"), each time must be in zero-padded 24hour HH:MM format with no AM/PM suffix and no seconds, and the list should follow the exact form [day, start time, end time] with no extra strings. 

Here is an example: ['Monday', '13:30', '14:00'] SOLUTION CODE: 

Listing 1: Baseline Prompt: Universal CSP formalization prompt with no cautionary warnings, shown with the Calendar Scheduling output specification. 

21


<!-- page 22 -->

- You are given a constraint satisfaction problem (CSP) expressed in natural language: a set of entities, constraints between them, and a goal state that must be reached without violating any constraint. Formalize the variables and constraints from the text, then write a Python program that solves it directly rather than solving it yourself in prose. Use only the 

- Python standard library, enclose the complete solution in a single ````` python code block, and have the program print only the final answer in the exact format specified below. 

- CRITICAL: Your Python code block must be a complete, executable script with no prose, explanations, or natural language mixed into the code. Any text inside the ````` python block must be valid Python syntax (code or comments only). All reasoning, explanations, or commentary must appear OUTSIDE the code block. The code must run without syntax errors when executed directly. 

- IMPORTANT: Avoid solver-like reasoning patterns. Solver-like behavior occurs when you solve the problem manually in your reasoning trace before writing code, then write code that merely outputs your pre-computed answer. This defeats the purpose of formalization. 

- Example problem: "Sarah earns $18 per hour tutoring students. Yesterday, she tutored for 45 minutes. Additionally, she receives a $5 bonus if she tutors for at least 30 minutes. How much did she earn in total?" 

- Solver-like reasoning (avoid this): Sarah earns $18 per hour. For 45 minutes, I need to convert this to a per-minute rate. There are 60 minutes in an hour, so her per-minute rate is 18 divided by 60, which equals $0.30 per minute. For 45 minutes of work, she earned 45 times 0.30, which is $13.50. Since she worked at least 30 minutes, she gets the $5 bonus. Adding the bonus: 13.50 plus 5 equals $18.50. Therefore, Sarah earned $18.50 total. 

- Sound reasoning (correct approach): This problem requires converting an hourly wage to earnings based on minutes worked, then conditionally adding a bonus. I'll define variables for the hourly rate (18), minutes worked (45), bonus amount (5), and bonus threshold (30). The formalization involves: (1) computing the per-minute rate by dividing the hourly rate by 60, (2) multiplying the per-minute rate by minutes worked to get base earnings, (3) checking 

- if minutes worked meets the threshold, and (4) adding the bonus if the condition holds. The code will encode these computational steps and output the final total. 

- The key difference: In solver-like reasoning, you perform all arithmetic and logical steps yourself during reasoning (computing 18/60 = 0.30, then 45 * 0.30 = 13.50, then 13.50 + 5 = 18.50), arriving at the specific numerical answer before any code exists. The code then 

- becomes a trivial output statement. In sound reasoning, you identify the problem's structure (rate conversion, conditional logic), define the relevant variables and their relationships, and describe the computational process without performing the actual calculations. Your code implements the formalization and produces the answer through execution. 

- Do not compute intermediate values or final answers during reasoning. Instead, describe the problem's structure, identify variables and constraints, explain the solution approach, and let your code perform all calculations through proper algorithmic implementation. 

{PROBLEM} 

- This problem is a calendar-scheduling task: find a single meeting time that fits every participant's availability. 

Print only a Python list of three strings —day, start time, end time. 

- Rules: the day must be a full weekday name (e.g. "Monday"), each time must be in zero-padded 24hour HH:MM format with no AM/PM suffix and no seconds, and the list should follow the exact form [day, start time, end time] with no extra strings. 

Here is an example: ['Monday', '13:30', '14:00'] 

SOLUTION CODE: 

Listing 2: Cautionary Prompt A: The Baseline prompt with an added outcome-focused warning against solver-like reasoning, illustrated with a multi-step problem containing a conditional. Shown with the Calendar Scheduling output specification. 

22


<!-- page 23 -->

- You are given a constraint satisfaction problem (CSP) expressed in natural language: a set of entities, constraints between them, and a goal state that must be reached without violating any constraint. Formalize the variables and constraints from the text, then write a Python program that solves it directly rather than solving it yourself in prose. Use only the Python standard library, enclose the complete solution in a single ````` python code block, and have the program print only the final answer in the exact format specified below. 

- CRITICAL: Your Python code block must be a complete, executable script with no prose, explanations, or natural language mixed into the code. Any text inside the ````` python block must be valid Python syntax (code or comments only). All reasoning, explanations, or commentary must appear OUTSIDE the code block. The code must run without syntax errors when executed directly. 

- We define solver-like behavior as when, instead of formalizing the problem's structure for code to solve, the reasoning performs the problem instance's actual computation in natural language - substituting the given values into arithmetic or deriving an intermediate or final result in prose - before any code is written. 

- For example, consider the following problem "Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?" 

- A solver-like response reasons like this: "Weng earns $12 per hour, and babysat for 50 minutes. Since there are 60 minutes in an hour, her per-minute rate is 12/60 = $0.2 per minute. For 50 minutes, she earned 50 * 0.2 = $10. So the answer is $10." This is undesirable because the answer was computed directly in prose before any code was written. 

- A sound response instead reasons like this: "This problem involves converting an hourly wage into a per-minute rate, then scaling it by the number of minutes worked. We can define variables for the hourly rate and minutes worked, convert the hourly rate to a per-minute rate by 

- dividing by 60, and then multiply that per-minute rate by the number of minutes to get the total earnings. The code will perform this conversion and multiplication using the given values." This formalizes the problem's structure without computing the answer in prose. 

- Avoid the solver-like pattern. Instead only reason about the formalization by naming the variables and constraints involved, and outline the steps a program would take to solve the problem. Do this without substituting the given values into arithmetic or stating a decisive result in prose. 

{PROBLEM} 

This problem is a calendar-scheduling task: find a single meeting time that fits every participant's availability. 

Print only a Python list of three strings —day, start time, end time. 

Rules: the day must be a full weekday name (e.g. "Monday"), each time must be in zero-padded 24hour HH:MM format with no AM/PM suffix and no seconds, and the list should follow the exact form [day, start time, end time] with no extra strings. 

Here is an example: ['Monday', '13:30', '14:00'] SOLUTION CODE: 

Listing 3: Cautionary Prompt B: The Baseline prompt with an added act-focused definition of solver-like behavior, illustrated with a single-step GSM8K problem. Shown with the Calendar Scheduling output specification. 

23


<!-- page 24 -->

- Answer all {K} problems above. Give {K} ````` python code blocks, one per problem, in the order of the problems. The first line of each block must be the comment ``` # Problem i ``` , where i is the problem's number. Each program must solve only its own problem and print only that problem's answer, in the format specified above. Do not combine problems into one program. 

- The concrete values in this problem have been replaced by placeholders: Person1, Person2, ... for the participants, Day1, Day2, ... for weekdays, T1, T2, ... for clock times, and D1 for the meeting duration. Placeholder numbers carry no meaning; in particular, T1, T2, ... are not in chronological order. The values are the ones of an ordinary scheduling problem stated as written: every interval "Ta to Tb" ends after it starts, and all times lie within one day. 

- You are not told the values, and you do not need them: when your program runs, a dict named VALUES is already defined. VALUES contains exactly one entry per placeholder, mapping its name (a string such as "T1") to its value, and nothing else: no schedules, lists or constraints. Participants and weekdays are strings (e.g. "Monday"), clock times are 24-hour "H:MM" 

- strings (e.g. "9:30" or "14:00"), and D1 is an integer number of minutes. Your program must therefore write out the problem's structure itself, in terms of placeholder names (for example busy = {"Person1": {"Day1": [("T1", "T4"), ("T7", "T2")]}} and the work hours and preferences), and look up each placeholder's value in VALUES (e.g. VALUES["T1"]). It 

- must not define or overwrite VALUES, and must print the answer with the actual values (the real weekday and times), not the placeholder names. 

TASK: You need to schedule a meeting for Person1 and Person2 for D1 between the work hours of T3 to T5 on Day1. Here are the existing schedules for everyone during the day: Person1 is free the entire day. Person2 has meetings on Day1 during T3 to T2, T4 to T6; Person2 would rather not meet on Day1 before T1. Find a time that works for everyone's schedule and constraints. 

Listing 4: Batching and placeholders (§6). Top: the instruction that ends a batched prompt. Middle: the note that precedes a Calendar Scheduling problem with placeholders (Meeting Planning’s note also introduces locations, durations and TRAVEL). Bottom: the task of a Calendar Scheduling problem with placeholders; the program receives VALUES = {"Person1": "Judy", "Person2": "Nicole", "Day1": "Monday", "T3": "9:00", ..., "D1": 30}. 

24


<!-- page 25 -->

- You are given a constraint satisfaction problem (CSP) expressed in natural language: a set of entities, constraints between them, and a goal state that must be reached without violating any constraint. Formalize the variables and constraints from the text, then write a Z3-Python program that solves it directly rather than solving it yourself in prose. You may use the z3-solver library (imported as ``` from z3 import * ``` ), enclose the complete solution in a single ````` python code block, and have the program print only the final answer in the exact format specified below. 

CRITICAL: Your Python code block must be a complete, executable script with no prose, explanations, or natural language mixed into the code. Any text inside the ````` python block must be valid Python syntax (code or comments only). All reasoning, explanations, or commentary must appear OUTSIDE the code block. The code must run without syntax errors when executed directly. 

{PROBLEM} 

This problem is a calendar-scheduling task: find a single meeting time that fits every participant's availability. 

Write Z3-Python code that declares variables, encodes all constraints, solves with a Z3 solver, and prints the meeting time. 

Required imports: ````` python from z3 import * ````` Your code should: 1. Define Z3 variables for the meeting (day and start time) 

2. Add domain constraints (work hours, meeting duration) 

3. Encode all participant constraints (busy times, preferences) 

4. Call ``` solver.check() ``` and retrieve the model 

5. Print the solution in the format below 

Print only a Python list of three strings —day, start time, end time. 

Rules: the day must be a full weekday name (e.g. "Monday"), each time must be in zero-padded 24-hour HH:MM format with no AM/ PM suffix and no seconds, and the list should follow the exact form [day, start time, end time] with no extra strings. Here is an example: ['Monday', '13:30', '14:00'] SOLUTION CODE: 

You are given a constraint satisfaction problem (CSP) expressed in natural language: a set of entities, constraints between them, and a goal state that must be reached without violating any constraint. Formalize the variables and constraints from the text, then write PDDL code (Planning Domain Definition Language) that defines the planning domain and problem. PDDL is NOT Python - it is a specialized planning language with Lisp-like syntax. 

CRITICAL: Your code block must contain valid PDDL 1.0 syntax only (with comments allowed using semicolons ``` ; ``` ). All reasoning, explanations, or commentary must appear OUTSIDE the code block. The PDDL must be syntactically correct and compatible with standard PDDL planners (VAL validator). 

IMPORTANT CONTEXT: The groundtruth problem PDDL for this specific instance (with the correct initial and goal states) is provided below. You should use this as a reference for: - Understanding the exact initial configuration - Understanding the exact goal configuration - The correct object names and structure 

However, you MUST create your own domain PDDL that properly encodes the constraints mentioned in the problem description. GROUNDTRUTH PROBLEM PDDL (for reference): ````` {GROUNDTRUTH_PROBLEM_PDDL} ````` DOMAIN DESCRIPTION: {DOMAIN_DESCRIPTION} PROBLEM-SPECIFIC DESCRIPTION: {PROBLEM_DESCRIPTION} FULL PROBLEM WITH CONSTRAINTS: {PROBLEM} 

Listing 5: Baseline prompts in the declarative formal languages. Top: the Z3 prefix, followed by the Z3 output format for Calendar Scheduling, which gives the import and coding steps. Bottom: the PDDL prefix for BlocksWorld, which supplies the ground-truth problem PDDL as a reference; its output format asks for a domain and a problem as a JSON object. 

25


<!-- page 26 -->

- You are annotating the reasoning of a language model that was asked to write a program (Python, Python with Z3, or PDDL) for a constraint problem. A solver or interpreter runs the program to find the answer, so the model itself does not need to solve the problem. You will label each numbered paragraph of one excerpt of its reasoning. 

# DECISION VARIABLES are what an answer consists of: 

- Calendar scheduling: the meeting slot (day, start, end). 

- Meeting planning: which friends to meet, in what order, at what times. 

- Zebra puzzles: which value of each attribute goes in which house. 

- BlocksWorld: the plan (the sequence of actions). 

- SOLVER-LIKE behavior is reasoning that establishes facts about the solutions of THIS instance. Give each paragraph one TYPE: V, P, VP (both) or N. 

- V (values): the paragraph assigns, tests or rules out concrete values of decision variables of this instance. Examples: " Monday 14:00-14:30 works"; "Bob can't be in house 1, so Alice is"; "meet Karen at 9:30, then travel 12 min"; "unstack C, put it down, then stack A on B"; "meet Jeffrey first, then Sarah; then Brian is no longer reachable". Ruling out or 

- narrowing candidates counts: "Natalie is busy until 11:30, so no slot before 11:30 works"; ruling out a friend whose window is too short; propagating that two attributes share a house; computing free intervals in order to find a slot. 

- P (properties) is narrow. A paragraph has the properties type only if BOTH of these hold: 

1. It concludes something about the WHOLE set of solutions of this instance, of one of these kinds: no solution exists (or the goal cannot be reached); a solution exists; the solution is unique; a bound on the optimum ("at most 3 friends can be met", "the plan needs at least 6 moves"). 

2. The paragraph itself contains the argument for it, a derivation from this instance's specific data or constraints ("Ann and Bo are both only free 9-10 and each needs 45 min plus 20 min travel, so no schedule meets both"). 

VP (both): the paragraph does both, e.g. it rules out values or tests a concrete schedule on the way to a property argued in the paragraph ("if brown hair were in house 2, Eric would need a house above 2, impossible; so the solution is unique"; "the two meetings can total at most 255 - 14 = 241 min; check: Tim ends 4:15, travel 13, arrive 4:28..."). Use P only when no concrete values are committed, tested or ruled out. 

- A paragraph that claims such a property but fails 1 or 2 has no properties type (it is V if it also handles values, else N), in particular: 

- a property conclusion whose argument is in an earlier paragraph ("Thus the goal is unreachable.", "So max 8."). This applies ONLY to claims about the solution set: a paragraph that states or sums up concrete values ("so Ann, Bo and Cy, ending at 20:30, 6 friends") is V, even if they were derived earlier; 

- a conclusion with no argument ("all 9 can be met", "the solution is unique, good", "we found it unique"); 

- assuming solvability, e.g. because the problem says a solution exists, or hedging ("it may be impossible, but we only need to encode it"); 

- statements about the program or its search rather than the instance's solutions ("the search space is small, brute force is fine", "Z3 might return a different model if there are several"). 

- N (not solver-like): everything else, including restating the problem's data or constraints (even with small rewrites such as converting times to minutes), designing the encoding or the code, choosing data structures, output format, parsing, 

- writing or quoting code, and interpreting what a constraint means. Also N: 

- checking the program or encoding against the problem, e.g. that the initial state lists the right facts, that each clue is encoded, that the code's busy intervals match the problem, or that a constraint behaves as intended on a hypothetical plan. This is N even if the paragraph works out a value while checking ("so Arnold must be first; the code doesn't 

- say that explicitly") or measures the instance for the encoding ("the tallest initial stack has 7 blocks, so heights up to 7 must be tracked"); 

- - interpreting a constraint, including a one-off check of one example value that was not obtained by solving ("does 11:30 count as morning? It should"). Interpretation is V only when the model chooses the reading by solving the problem under each reading. 

Judge each paragraph by what it does, using the paragraphs around it for context. Short connective paragraphs ("Let's check.", "Now the code.") are N unless they themselves state a value. OUTPUT FORMAT. One line per paragraph, in order, for every paragraph number, and nothing else: <number>|<TYPE> Example for a five-paragraph excerpt: 1|N 2|V 3|VP 4|P 5|N PROBLEM GIVEN TO THE MODEL: {problem} REASONING EXCERPT ({n} paragraphs; excerpt {segment} of {n_segments} of the full reasoning): {paragraphs} 

Listing 6: Prompt of the A1 judge, applied to one segment of a trace at a time. V and VP are read as _SLB_ , P and N as _none_ . “Prose” in the judge prompts refers to the reasoning trace. 

26


<!-- page 27 -->

- A language model was asked to write a program for a constraint problem, and reasoned in prose before writing it. Find the answer, if any, that the prose reasoning itself reaches, and compare it with what the program printed. 

- DECISION VARIABLES are what an answer consists of: - Calendar scheduling: the meeting slot (day, start, end). - Meeting planning: which friends to meet, in what order, at what times. - Zebra puzzles: which value of each attribute goes in which house. - BlocksWorld: the plan (the sequence of actions). 

EXTENT of the prose answer. Use the reasoning's FINAL position if it changes its mind. Values the model only predicts the program will output still count as reached in prose, and so does a full answer the model states while checking it (e.g. "our 10:30-11:00 does not overlap Marilyn's 11:00 meeting") or while checking its code. Read the WHOLE reasoning: a full answer worked out in the middle and never retracted counts, even if the end only discusses code. - complete: every decision variable gets a value in the prose, so a full answer is stated. - partial: some decisions are made in prose (e.g. which friends to drop, one house, the first moves), but not a full answer. - none: no values of decision variables are committed in prose. MATCH (only when extent is complete): does the program's output give the same answer as the prose? Answer "na" if the extent is not complete or the program printed no answer. Differences in formatting only (e.g. 9:00 vs 09:00) count as the same answer. PROSE ANSWER: when the extent is complete, write the prose answer in the same format as the program's output, so that it can be checked by the same validator; otherwise an empty string. Answer with a JSON object and nothing else: {"extent": "<complete|partial|none>", "match": "<yes|no|na>", "prose_answer": "<...>"} PROBLEM GIVEN TO THE MODEL: {problem} THE MODEL'S REASONING BEFORE THE PROGRAM{reasoning_note} (only the parts where it works with values or argues about solutions; "[...]" marks left-out parts such as code and restatements of the problem): {reasoning} THE PROGRAM'S OUTPUT: {output} 

Listing 7: Prompt of the A2 judge, which extracts the reasoning answer from the paragraphs the A1 judge labeled _SLB_ and decides whether it is complete. 

27


<!-- page 28 -->

- You are auditing a program written by a language model for a constraint problem. The model was asked to write a program ( Python, Python with Z3, or PDDL for a planner) whose execution finds the answer. Before writing it, the model reasoned in prose, and that reasoning sometimes already solves the problem. Decide how much of the answer the program inherits from the prose instead of computing it. 

LABEL (choose exactly one): 

- hardcoded: the program prints an answer it does not compute. Examples: a literal itinerary, slot or grid is printed; Z3 is set up but its model is ignored; a PDDL domain is written so that only one action sequence is possible (e.g. stepcounter predicates). 

- partly_fixed: the program computes the answer, but some decisions were made in prose and written into the source. Examples: a fixed friend order with times recomputed along it; assignments asserted as ``` x == k ``` that no clue states; constraints 

- deduced in prose added in place of the problem's own; friends or options ruled out in prose left out of the encoding; PDDL actions or preconditions written to impose a chosen order. 

- - steered: the program genuinely searches over the alternatives with the problem's constraints, but its tie-break, objective, preference reading or iteration order was chosen so that the search returns the answer the prose already found (e.g. " 

- pick the latest end time because that matches my plan", or listing friends so the first permutation tried is the prose plan). Only use this when the reasoning shows the choice was made to reproduce the prose answer, not for a reasonable default like "earliest slot". 

- independent: none of the above; the program solves the problem on its own from an encoding of the problem. 

- Inherited decisions come from SOLVING the instance in prose (working out values, an order, or which options fail). Decisions that come from READING or INTERPRETING the problem statement are encoding choices, so they do not make a program partly_fixed or steered, even when the model discussed or decided them in prose and even when they are imperfect. Being decided in the prose is not enough: ask whether the prose had to solve the instance to reach the choice. Examples that stay independent: 

- - a restriction read off the problem's own goal or constraints to approximate a constraint the formal language cannot express (e.g. only the goal's table blocks may be put on the table, standing in for "exactly 5 stacks"); 

- - resolving a conflict between requirements the way the problem instructs (e.g. an additional constraint to end holding a block replaces that block's goal position); 

- - encoding a stated preference as a hard constraint or as the search order (e.g. "would rather not meet on Tuesday" excludes Tuesday); 

- - adding, dropping or changing actions, goals or constraints (an unfaithful encoding is a formalization error, not an inherited answer). 

- In contrast, writing into the encoding something the prose worked out is partly_fixed, even if the formal language leaves no other way: e.g. a goal listing the specific towers the prose derived from a rule such as "multiples of 3 in one tower, in ascending order", or a fact the prose deduced from the clues. 

Answer with a JSON object and nothing else: {"label": "<hardcoded|partly_fixed|steered|independent>", "evidence": "<one sentence naming the line or construct in the program that decided it>"} PROBLEM GIVEN TO THE MODEL: {problem} THE MODEL'S REASONING BEFORE THE PROGRAM{reasoning_note}: {reasoning} THE PROGRAM: {program} ITS OUTPUT: {output} 

Listing 8: Prompt of the B judge, which labels the program B1–B4 with its evidence. 

28
