---
source: 2611.02395-solver-like-behavior.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# Solver-Like Behavior in Large Language Models as Formalizers · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

# **Solver-Like Behavior in Large Language Models as Formalizers** 

**Rikhil Amonkar Stuti Mohan Kevin Nguyen Ceyhun Efe Kayan Ronan Le Bras Li Zhang** Drexel University Allen Institute for AI {rikhil.amonkar|harry.zhang@drexel.edu} 





## **Abstract** 

In the LLM-as-formalizer paradigm, a large language model translates a problem into a formal program and leaves the search to a solver, gaining the solver’s guarantees. Formalizers are now often reasoning models that write a long reasoning trace before the program, yet they are judged only by the program’s output. We find that the trace routinely does the solver’s job, assigning, testing and ruling out values until it often reaches the full answer; we call this _solver-like behavior_ (SLB). We define an ontology of SLB over the trace, the program and its output, and use LLM judges, checked against human labels, to label 2,000 generations from three reasoning models on four constraint satisfaction datasets, each formalized in a declarative and an imperative formal language. SLB appears in 85% of traces and takes 24% of reasoning tokens, yet the program usually recomputes the answer, so the effort is redundant. The 9% of programs that inherit the trace’s answer also inherit its errors, and pass output-based evaluation whenever that answer is correct. The amount of SLB is not associated with accuracy, and SLB is more common in imperative Python than in declarative Z3 or PDDL. Cautionary prompts reduce it by only a quarter, but hiding the problem’s values behind placeholders, which the program receives only at run time, removes 97% of it without loss of accuracy. Formalizers should therefore be evaluated by how their programs are reached, not only by what they output.<sup>1</sup> 

## **1 Introduction** 

In the LLM-as-formalizer paradigm (Tantakoun et al., 2025), a large language model (LLM) does not solve a problem but translates it into a formal program, such as a planning domain or a set of constraints, which a solver executes (Huang and Zhang, 2025; Lin et al., 2025; Amonkar et al., 2026). The 

> 1Our code is available at https://github.com/ rikhil-amonkar/solver-like-behavior-in-llms. 

LLM handles language, and the solver performs the search with guarantees that the LLM’s own reasoning lacks (Wei et al., 2025). Formalizers today are often reasoning models that write a long reasoning trace before the program. Yet they are judged almost only by whether the program’s output is correct, which cannot tell a program that searches from one that restates an answer the model already worked out in its trace. The trace itself has gone unexamined: work on reasoning traces, which finds them often unfaithful or wasteful (Lanham et al., 2023; Arcuschin et al., 2025; Chen et al., 2025a; Sui et al., 2025), studies models that solve the problem themselves, and formalizer traces have been discussed only in passing (Amonkar et al., 2026). 

We find that formalizers routinely do the solver’s job themselves, a phenomenon we call _solver-like behavior_ (SLB): before writing the program, the reasoning trace assigns, tests and rules out values of the problem’s variables, often until it reaches the full answer (Figure 1). This defeats the purpose of formalization in two ways. It is costly: constraint satisfaction is NP-complete (Cook, 1971), and solving in tokens grows with the instance: on Meeting Planning, solver-like tokens nearly triple from the smallest to the largest problems, though the program usually searches anyway. And it can silently void the solver’s guarantee: a program that prints the answer from the trace, i.e. _inherits_ it, passes output-based evaluation while also inheriting the trace’s errors, so where outputs are not independently validated, a formalization that looks correct may be no more verifiable than chain-of-thought. 

We study SLB in three reasoning models on four constraint satisfaction datasets, each formalized in a declarative formal language (Z3 or PDDL) and an imperative one (Python). We define an ontology over the trace, the program and its output (Figure 2), label 2,000 generations with LLM judges that agree with blind human labels on 94% of paragraphs, and test four hypotheses (§5). **(H1) SLB is** 

1


<!-- page 2 -->

<!-- Start of picture text -->
(1) Problem (2) Reasoning trace (3) Program<br>none<br>Schedule a 30-minute We need a common free 30-minute slot. I will busy = {"Patrick": [(540, 570), (600, 630), (810, 840)],<br>meeting on Monday, represent times as minutes and let the code scan "Kayla": [(570, 750), (900, 1020)], ...}<br>9:00–17:00, for Patrick, the day for the first free start time. [. . . ] def free(s):<br>Kayla, Carl and Christian. return all(e <= s or s + 30 <= b<br>SLB for bs in busy.values() for b, e in bs)<br>Patrick is busy 9:00–9:30, Patrick is free 9:30–10:00, 10:30–13:30 fmt = lambda m: f"{m // 60}:{m % 60:02d}"<br>10:00–10:30 and and 14:00–17:00. Kayla is free 9:00–9:30 for s in range(540, 991, 5):<br>13:30–14:00; Kayla and 12:30–15:00, so together they are free if free(s):<br>9:30–12:30 and 12:30–13:30 and 14:00–15:00. [. . . hundreds print(f"Monday {fmt(s)}-{fmt(s + 30)}")<br>15:00–17:00; Carl to thousands of tokens checking each calendar break<br>12:30–13:30 and . . . ] Christian is free from 14:00, which leaves<br>14:30–15:00; Christian only 14:00–14:30. So the meeting is Monday run<br>9:00–14:00. 14:00–14:30 . Output: Monday 14:00–14:30<br>none<br>LLM as Now the code: convert the busy blocks to minutes<br>formalizer and print the first start time that fits all four<br>calendars. [. . . ] LLM judge scripts<br>LLM judge<br>(4) Ontology labels<br>A. Reasoning trace B. Program C. Output<br>A1 SLB (1 of 3 paragraphs) B4 Independent: searches every start time C1 Match: yes, the trace and the program<br>A2 complete: Monday 14:00–14:30 against all four calendars. both give 14:00–14:30.<br>Solver-like ratio 0.45 Had it been print("Monday 14:00-14:30"): B1 C2 Correct: yes, the reasoning answer<br>Hardcoded . passes the validator.<br><!-- End of picture text -->

Figure 1: Overview on a calendar scheduling problem (1). An LLM as formalizer writes a reasoning trace (2) and then a program (3), which is run and scored. The middle paragraph is **solver-like** : it solves the problem in the trace, finding first the common free intervals and then the meeting time, which is the solver’s job; in real traces such a passage runs to hundreds or thousands of tokens. Our ontology (§3) labels every generation (4): whether the reasoning trace is solver-like (A), how much of the reasoning answer the program inherits (B), and whether the program’s output matches the reasoning answer, which is checked for correctness (C). Here the program searches independently, so the solver-like behavior, 45% of the trace, was wasted. 

**common and redundant:** 85% of traces contain it, yet the program usually recomputes the answer. **(H2) Its forms differ in harm:** the 9% of programs that inherit the reasoning answer also inherit its errors, and pass output-based evaluation whenever that answer is correct; hardcoding is rare and mostly comes from one model on one dataset. **(H3) Its amount is not associated with accuracy** on the same problem. **(H4) The formal language matters most:** Python draws more SLB than Z3 or PDDL in every dataset. Cautionary prompts cut SLB by about a quarter, while hiding the problem’s values behind placeholders that the program receives at run time removes 97% of it without loss of accuracy (§6). SLB is thus pervasive and mostly redundant, and occasionally voids the solver’s guarantee. 

# **2 Related Work** 

**LLMs as formalizers.** An LLM paired with an external solver writes PDDL for classical planners (Liu et al., 2023; Guan et al., 2023; Xie et al., 2023; Zuo et al., 2025; Hu et al., 2025; Huang and Zhang, 2025; Gong et al., 2025; Huang et al., 2026), logic for theorem provers and SAT/SMT solvers (Pan et al., 2023; Olausson et al., 2023; Ye et al., 2023), optimization models (Li et al., 2026) and schedul- 

ing constraints (Amonkar et al., 2026); Tantakoun et al. (2025) survey the planning line, and programaided reasoning (Gao et al., 2023; Chen et al., 2023; Lyu et al., 2023) likewise delegates computation to an interpreter. These works evaluate the program, by whether it executes, matches a reference or yields a valid solution; we examine the reasoning that precedes it. 

**Reasoning traces.** Chains of thought often misrepresent the computation behind the answer: models omit cues that sway them (Turpin et al., 2023; Chen et al., 2025b), rationalize after the fact (Arcuschin et al., 2025), and keep their answer when the reasoning is truncated or corrupted (Lanham et al., 2023). Other work dissects traces into behaviors such as verification and backtracking (Marjanovi´c et al., 2025; Gandhi et al., 2025) or finds the sentences that steer the outcome (Bogdan et al., 2025). Reasoning models also spend far more tokens than a problem needs (Chen et al., 2025a; Sui et al., 2025; Cuadron et al., 2025), which motivates budgets on reasoning length (Muennighoff et al., 2025) and measures of effort beyond length (Chen et al., 2026), while accuracy can still collapse as problems grow complex (Shojaee et al., 2025). All of this work studies models that solve the problem themselves. For a formalizer, solver-like behavior 

2


<!-- page 3 -->

is a specific waste: its tokens duplicate the solver’s work and grow on the hard instances that formalization is meant to offload. 

**Delegation and hardcoding.** LLMs often reason in text when code would serve better (Chen et al., 2025d,c), or call tools they do not need (Qian et al., 2025; Wang et al., 2025); solver-like behavior is a failure to delegate that persists after the model has written a program. Its extreme form, a program that prints the trace’s answer, resembles reward hacking in code generation, where models hardcode test outputs (Baker et al., 2025; Zhong et al., 2025); training against a monitor of the trace can drive such behavior into less visible forms (Baker et al., 2025), much as our cautionary prompts turn literal itineraries into fixed orders (§6). 

# **3 An Ontology of Solver-Like Behavior** 

We view each task as a constraint satisfaction problem: a set of _decision variables_ , the unknowns that together make up an answer (e.g., when a meeting starts, where each object goes, or which action comes next in a plan), and constraints on their values. In the LLM-as-formalizer paradigm, encoding the variables and constraints is the model’s job, and finding values that satisfy them is the solver’s. Figure 2 illustrates every definition below on a toy problem: seat Ann, Bob and Cy in chairs 1–3, with Ann left of Bob and Cy not in chair 1. Its decision variables are each person’s chair. 

**Solver-like behavior** (SLB) is text in the reasoning trace that does the solver’s job on the instance: assigning, testing or ruling out values of its decision variables. Designing the encoding, restating the problem’s data or constraints, choosing the output format, parsing, and interpreting an ambiguous constraint are not solver-like, unless the reading is chosen by solving under each one. A formalizer’s _generation_ has two parts: a _reasoning trace_ ( _trace_ for short), the natural-language text the model writes first, and a _program_ , whose _output_ is what it prints when run. An answer stated in the trace is the _reasoning answer_ . We describe solverlike behavior along these three components: the trace (A), the program (B), and its output (C). 

**A. Reasoning trace** is read from the trace alone. **A1 (existence)** is _SLB_ if the trace assigns, tests or rules out values of decision variables, and _none_ otherwise. Arguments about the solution set that commit no values, such as uniqueness, are rare and not counted. **A2 (extent)** applies when A1 is _SLB_ . 

It is _complete_ if every decision variable receives a value and _partial_ otherwise, including a tentative answer the trace later abandons. The **solver-like ratio** is the share of the trace that is solver-like. 

**B. Program** records how much of the reasoning answer the program inherits rather than computes. A program _inherits_ a decision when it takes the value from the trace instead of computing it; B1– B3 are the forms this takes. **B1 Hardcoded:** it prints an answer it does not compute, so the formalization adds no guarantee. **B2 Partly fixed:** it computes the answer, but decisions made in the trace are written into its source. This shrinks the solver’s search, which can be harmless or even necessary, as when a numerical BlocksWorld constraint, which PDDL cannot express, must be turned into fluents in the trace. **B3 Steered:** it searches, but its tiebreak, objective or iteration order is chosen so that the search returns the reasoning answer. **B4 Independent:** it searches under every constraint, so any SLB in the trace was wasted. Only decisions the trace had to solve for count as inherited; a restriction read off the problem statement is part of the encoding. B1–B3 presuppose A1 = _SLB_ , and B does not apply when the program does not run. 

**C. Output** compares the program’s output with the reasoning answer, and applies when A2 is _complete_ and the program runs. **C1 (match)** asks whether the reasoning answer equals the program’s output. **C2 (correct)** asks whether the reasoning answer passes the validator used to score the program. Together they distinguish programs that merely reproduce the reasoning answer from programs that override an incorrect one or are led astray by it. 

# **4 Methods** 

**Tasks, Datasets and Formal Languages.** Given a natural-language constraint satisfaction problem (CSP) (Russell and Norvig, 2009), the model must write a program in a formal language (FL) that returns a valid solution when executed. We sample 100 instances from each of four benchmarks. Calendar Scheduling and Meeting Planning (Zheng et al., 2024) require meeting times and multi-location itineraries that satisfy availability, duration, and travel-time constraints. ZebraLogic (Lin et al., 2025) consists of logic grid puzzles. BlocksWorld (IPC, 1998) is classical planning. Full task descriptions are in Appendix B. 

We formalize every dataset in two FLs; following the formalizer literature, FL here includes 

3


<!-- page 4 -->

<!-- Start of picture text -->
Example A. Reasoning trace B. Program C. Output<br>problem<br>Seat Ann, Bob and A1 Existence B1 Hardcoded C1 Match: reasoning answer =<br>Cysitsinleftchairsof Bob.1–3.CyAnnis does the trace assign, test or rule out prints an answer it does not compute program output?<br>not in chair 1. values of decision variables? e.g.: print("Ann 1, Bob 2, Cy 3") yes: trace “Ann 1, Bob 2, Cy 3”;<br>Decision variables: SLB: “Neither Cy nor Bob can be in 1, program prints Ann 1, Bob 2, Cy 3<br>each person’s chair. so Ann is.” (rules out values) B2 Partly fixed no: trace “Ann 1, Bob 2, Cy 3”;<br>Input to the judges: none: “One variable per person, values computes, but some decisions are program prints Ann 1, Cy 2, Bob 3<br>problem, reasoning 1–3.” (encoding design; also restating, written into the source<br>trace, program. formatting, parsing) e.g.: ann = 1; or bob != 1 instead of ann C2 Correct: reasoning answer<br>< bob passes the validator?<br>A2 Extent (if SLB) yes: trace “Ann 1, Bob 2, Cy 3”<br>does the trace give every decision B3 Steered no: trace “Bob 1, Ann 2, Cy 3” puts<br>variable a value? searches, but a tie-break, objective or Ann right of Bob<br>complete: “Ann is in 1, as neither Cy order is chosen to return the reasoning<br>nor Bob can be. Bob takes 2, leaving 3 answer<br>for Cy. So Ann 1, Bob 2, Cy 3.” (every e.g.: min(seatings, key=...) picked so it<br>chair) yields Ann 1, Bob 2, Cy 3<br>partial: “Ann is in 1, as neither Cy nor<br>Bob can be. The program will place B4 Independent<br>Bob and Cy.” (Ann’s chair only) searches all seatings under every<br>constraint<br><!-- End of picture text -->

Figure 2: Ontology of solver-like behavior, with an example of each node on a toy seating problem (left). **A** describes the reasoning trace: whether it contains solver-like behavior (A1), and how much of an answer it reaches (A2). **B** describes how much of the reasoning answer the program inherits rather than computes; B1–B3 require A1 = SLB. **C** compares the program’s output with a complete reasoning answer (C1), and checks the reasoning answer with the validator (C2). 

general-purpose programming languages. The two differ in who searches for a solution, which is what solver-like behavior is about. A _declarative_ program states what a solution is and a solver finds one; an _imperative_ program states how to find one, so the model designs the search. Our imperative FL is Python with only the standard library. Our declarative FL is PDDL (Ghallab et al., 1998) for BlocksWorld, solved by a classical planner, and Z3 for the other datasets: Python programs that state constraints through the API of the Z3 SMT solver (de Moura and Bjørner, 2008), which returns a satisfying assignment. Programs that use another library, or Z3 programs that never call the solver, are flagged as not written in the requested FL (at most 5% of any run; Table 2). 

**Prompt.** Each model receives one prompt per dataset and FL: a prefix that instructs it to formalize the problem in the FL and let the program solve it, rather than solving it in the reasoning trace, followed by the task’s output format (Appendix D). All Z3 prompts give the import and coding steps of the ZebraLogic Z3 prompt (Lin et al., 2025). The PDDL prompt supplies the ground-truth problem PDDL as a reference and asks for a domain and a problem; the Python BlocksWorld prompt gives only the natural-language problem, which states the same initial and goal states. 

**Models.** We evaluate three reasoning models that write a reasoning trace before the program. We need the complete trace: closed frontier models 

such as Claude, GPT-5 and Gemini return at most a summary of their reasoning through their APIs, from which solver-like behavior cannot be measured. DeepSeek-V4-Flash (DeepSeek-AI et al., 2025) runs via API, and GPT-OSS-120B (OpenAI et al., 2025) and Qwen3.8-27B (Qwen Team, 2025) locally with vLLM. DeepSeek is run in one FL per dataset (Python for Calendar Scheduling and Meeting Planning, Z3 for ZebraLogic, PDDL for BlocksWorld), because the model behind its API changed between our runs (Appendix C). 

**Metrics.** We report the ontology labels of §3, the solver-like ratio, and program accuracy for every generation. 

**LLM judges.** No script can tell whether a passage does the solver’s job, and the traces are too many and too long to label by hand. We therefore label A1, A2 and B with LLM judges, using Gemma 4 31B-it (Gemma Team, 2026) (FP8), which is not one of the evaluated models. Traces are too long to judge at once, so we cut each into segments of at most 2,000 tokens at paragraph boundaries and give the A1 judge one segment at a time, with the problem, to label every paragraph as _SLB_ or _none_ ; a trace is _SLB_ if any paragraph is, and the solver-like ratio is the share of the trace’s characters in such paragraphs. The A2 judge extracts the reasoning answer from the _SLB_ paragraphs, and the B judge compares the program with the trace. C1 and C2 are scripts. Against reference labels covering both FLs of every dataset, the judges agree on 90–98% of cases (Table 1). Judge designs and 

4


<!-- page 5 -->

|Node|Reference|Agree|95% CI|
|---|---|---|---|
|A1 paragraph|human, blind|103/110|.87–.97|
|_SLB_precision|human, blind|38/42|.78–.96|
|_SLB_recall|human, blind|38/41|.81–.97|
|A2 extent|human + script|39/40|.87–1.00|
|B program|model, blind|19/20|.76–.99|
|B program (held out)|human, not blind|38/40|.83–.99|
|C1, C2|deterministic scri|pts||



Table 1: Agreement of each ontology judge with reference labels, with Wilson 95% confidence intervals. A1: one annotator, labeling blind (70 development and 40 held-out paragraphs). A2: _complete_ labels verified by humans, _partial_ ones by searching the trace for the program’s answer and having a second model read the passages found. B: blind reference labels by a second model; held out: a human shown the judge’s evidence, on programs labeled B1–B4. A1 and held-out B references cover both FLs of every dataset. C1 and C2 are computed by scripts from the A2 extraction, so they need no agreement check. 

further checks are in Appendix E, labeled examples in Appendix G. 

**Accuracy.** A program is correct if it runs and its output satisfies every constraint of the problem (Appendix B). 

# **5 Results** 

We label 2,000 generations: Qwen and GPT-OSS in both FLs of each dataset and DeepSeek in one, each on 100 problems under the prompt above, and test the four hypotheses of §1. Confidence intervals are 95% bootstrap intervals over problems; Appendix F lists the labels of every run. 

## **H1: SLB is common and redundant** 

We call solver-like behavior practically significant in a trace when it takes at least 10% of the trace or at least 1,000 tokens. **By either measure, it is the norm.** 85% of traces contain SLB (91% outside BlocksWorld in PDDL), 71% spend at least 10% of their tokens on it, and 47% at least 1,000 tokens (Figure 3). Across all traces, 24% of reasoning tokens are solver-like. A DeepSeek trace spends on average 6,123 of its 26,572 reasoning tokens on solver-like behavior, a Qwen trace 3,788 of 15,310, and a GPT-OSS trace 575 of 1,892. The one setting where it is rare is BlocksWorld in PDDL (51% of traces, ratio 0.04). Stray paragraphs do not drive this: only 29 of the 1,699 traces with SLB spend under 2% of their text on it, and in 77% of all traces the SLB paragraphs alone state a complete answer. 

**It grows with the problem.** From the smallest 

to the largest third of problems, solver-like tokens per trace rise from 3,873 to 10,971 on Meeting Planning (by number of friends) and from 532 to 4,148 on ZebraLogic (by grid size), as accuracy falls from 0.70 to 0.51 and from 0.90 to 0.78; GPTOSS on ZebraLogic is the exception. On Calendar and BlocksWorld they do not grow. 

**The program rarely uses it.** Of the generations whose trace contains SLB, the program computes the answer anew (B4; Figure 3, top) in 89% for DeepSeek and 77% for Qwen and GPT-OSS. Yet the two usually agree: where the trace states a complete answer and the program prints one, an independent program prints exactly the reasoning answer in 88% of cases (1,027 of 1,174; C1). The solving duplicates the work the program then does. 

## **H2: SLB takes forms that differ in harm** 

**SLB usually reaches a complete answer.** When a trace contains SLB, it states a complete answer in 87% (DeepSeek), 86% (GPT-OSS) and 96% (Qwen) of cases (A2), i.e. the very answer the program is meant to compute. The reasoning answer is wrong in 2% (DeepSeek), 11% (Qwen) and 13% (GPT-OSS) of the complete answers that can be checked (C2). 

**Inheritance is rare and concentrated.** Of the 1,791 programs that ran, 163 inherit the reasoning answer (grey in Figure 3, top, which shows the 157 whose trace contains SLB): 47 are hardcoded (B1), 40 of them GPT-OSS on Meeting Planning in Python; 88 are partly fixed (B2), mostly on BlocksWorld, Meeting Planning and ZebraLogic; and 28 are steered (B3), mostly Meeting programs in Python that try friends in the order of the reasoning answer. As B1 implies, 44 of the 45 hardcoded programs whose output can be compared print exactly the reasoning answer (C1). 

**Inheritance passes on errors in the reasoning answer.** When the reasoning answer is wrong, none of the 19 hardcoded programs and 1 of the 13 partly fixed ones is correct, against 32% of the 84 independent programs, which recompute the answer and can recover. Recomputing is no guarantee, though: 37 of those 84 independent programs print the same wrong answer as the trace (C1), so a program can share the trace’s error without taking any value from it, unless the B judge misses subtler inheritance. Steering is harmless: both steered programs with a wrong reasoning answer are correct. When the reasoning answer is correct, all four kinds of program are correct at least 93% of 

5


<!-- page 6 -->

<!-- Start of picture text -->
DeepSeek (B4) GPT-OSS (B4) Qwen (B4) B1 hardcoded B2 partly fixed B3 steered No output<br>100<br>80<br>60<br>40<br>20<br>– – – –<br>0<br>0.4<br>0.2<br>0.0<br>Calendar Calendar Meeting Meeting ZebraLogic ZebraLogic BlocksWorld BlocksWorld<br>Python Z3 Python Z3 Python Z3 Python PDDL<br>Traces with SLB (%)<br>Solver-like ratio<br><!-- End of picture text -->

Figure 3: H1 and H2: solver-like behavior is common, and the program rarely inherits it. For each dataset and FL, the share of traces with SLB (A1) and the mean solver-like ratio, with 95% confidence intervals. Each SLB bar is split by the program’s label (B): programs that inherit the reasoning answer (B1–B3, grey) at the bottom, independent programs (B4) in the model’s colour, and programs with no output (missing, failed, or printed nothing) hatched; most of these are Qwen’s Z3 programs, which call Z3 methods that do not exist. DeepSeek is run in one FL per dataset (–). 



<!-- Start of picture text -->
Solver-like ratio (+0.1)<br>SLB tokens (+1,000)<br>Any SLB<br>Program inherits (B1–B3)<br>Calendar: ratio (+0.1)<br>Meeting: ratio (+0.1)<br>ZebraLogic: ratio (+0.1)<br>BlocksWorld: ratio (+0.1)<br>−0.05 0.00 0.05 0.10 0.15<br>Change in program accuracy (within run and problem)<br><!-- End of picture text -->

Figure 4: H3: the amount of solver-like behavior is not associated with accuracy. Change in the probability that the program is correct per unit of each measure, from a linear model with fixed effects for model, dataset and FL and for the problem, with 95% confidence intervals. Grey: the ratio’s effect within each dataset. 

the time, so output-based evaluation cannot tell a hardcoded program from an independent one: all 26 hardcoded programs with a correct reasoning answer pass it. 

# **H3: The amount of SLB is not associated with accuracy** 

Harder problems may draw both more SLB and more errors, so we compare generations of the 



<!-- Start of picture text -->
Python Z3 or PDDL<br>GPT-OSS Qwen<br>Calendar (Z3)<br>Meeting (Z3)<br>ZebraLogic (Z3)<br>BlocksWorld (PDDL)<br>0.0 0.2 0.4 0.0 0.2 0.4<br>Solver-like ratio Solver-like ratio<br><!-- End of picture text -->

Figure 5: H4: on the same 100 problems, Python draws more solver-like behavior than each dataset’s declarative FL (in parentheses). Mean solver-like ratio per model, with 95% confidence intervals. 

same problem: a linear probability model of program correctness with fixed effects for the problem and for each model, dataset and FL. **The amount of solving has no detectable effect** (Figure 4). Ten more points of solver-like ratio change accuracy by +0 _._ 007 [ _−_ 0 _._ 011 _,_ +0 _._ 022], and 1,000 more solver-like tokens by +0 _._ 005 [ _−_ 0 _._ 002 _,_ +0 _._ 013]; within datasets the ratio’s effect lies between _−_ 0 _._ 03 and +0 _._ 02, except on BlocksWorld (+0 _._ 047 [+0 _._ 004 _,_ +0 _._ 083]). Programs that inherit the reasoning answer are not less accurate on average 

6


<!-- page 7 -->

( _−_ 0 _._ 00 [ _−_ 0 _._ 09 _,_ +0 _._ 07]). Traces with no SLB are less often correct ( _−_ 0 _._ 09 [ _−_ 0 _._ 15 _, −_ 0 _._ 02] relative to traces with some), but the gap lies in programs that fail to run: 25% of them crash, against 12%, and among programs that run the gap is _−_ 0 _._ 04 [ _−_ 0 _._ 09 _,_ +0 _._ 03]. We cannot rule out that working through the problem helps a model write a program that runs. The interventions of §6 agree: removing solver-like behavior does not lower accuracy. 

## **H4: SLB differs by formal language** 

**On the same problems, Python draws more SLB than either Z3 or PDDL, in every dataset** (Figure 5; pooled over the two models, with Qwen on ZebraLogic the one exception). The ratio is higher in Python by 0 _._ 06 [0 _._ 04 _,_ 0 _._ 08] on Calendar, 0 _._ 20 [0 _._ 17 _,_ 0 _._ 23] on Meeting Planning and 0 _._ 03 [0 _._ 01 _,_ 0 _._ 06] on ZebraLogic than in Z3, and by 0 _._ 16 [0 _._ 14 _,_ 0 _._ 18] on BlocksWorld than in PDDL. In a linear model of the ratio with all three factors (Qwen and GPT-OSS; _R_<sup>2</sup> = 0 _._ 27), removing the FL loses 0 _._ 123 of explained variance, the dataset 0 _._ 057, and the model 0 _._ 008. Using only the FLs DeepSeek is run in, where all three models are run, the model explains 0 _._ 011. 

**The dataset matters through the search the FL leaves to the model.** The FL effect is largest where the declarative FL takes over a search that is hard to program: in PDDL the planner finds the plan, and in Z3 the solver chooses Meeting Planning’s friend order, which in Python the model must program as a search over orders. On Calendar (a trivial search) and ZebraLogic (permutations in Python) the FLs differ little. With the FL fixed, the datasets differ in Python (Meeting Planning 0.38, the others 0.19–0.25) but not in Z3 (0.18–0.19). The two prompts of a dataset also differ in more than the FL (§4): the PDDL prompt supplies the reference problem file, which may account for part of the BlocksWorld gap, so the Z3 comparisons are the cleaner test of the FL. 

# **6 Deterring Solver-Like Behavior** 

We test three ways to deter SLB: warning against it in the prompt, batching several problems into one prompt, and hiding the problem’s values behind placeholders. Each generation is compared with the baseline generation of the same problem (Figure 6). 

## **Cautionary prompts** 

We add one of two warnings to the prompt of §4 (Appendix D; Listings 1–3). **Cautionary A** frames 

solver-like behavior by its outcome, precomputing the answer in the trace and hardcoding it, and **Cautionary B** by the act, substituting the given values into arithmetic in the trace. Each illustrates the contrast with a math word problem, so no taskspecific solution leaks. We run both for every model, dataset and FL of §5. 

**Cautionary prompts reduce solver-like behavior by about a quarter, without removing it or changing accuracy** (Figure 6). From a baseline of 0.20, the ratio falls by 0 _._ 053 [0 _._ 045 _,_ 0 _._ 061] under Cautionary A and 0 _._ 058 [0 _._ 051 _,_ 0 _._ 065] under Cautionary B, and solver-like tokens by 689 and 443 per trace (23% and 15%). Yet most traces still contain SLB: the share with SLB falls by 4 and 9 points, almost all of it GPT-OSS ( _−_ 10 and _−_ 19 points), while DeepSeek (+1, _−_ 4) and Qwen ( _−_ 1, _−_ 1) barely change. Programs that inherit the reasoning answer fall by 4 points. Accuracy does not change (+0 _._ 01 [ _−_ 0 _._ 01 _,_ +0 _._ 02] and _−_ 0 _._ 00 [ _−_ 0 _._ 02 _,_ +0 _._ 01]), so reducing solver-like behavior neither helps nor hurts, as H3 found by observation. 

**The prompts remove hardcoded answers more than inherited decisions.** GPT-OSS’s 40 hardcoded Meeting programs in Python fall to 0 and 1, but its partly fixed ones go from 11 to 15 and 7: the program now encodes the problem, yet still follows a friend order chosen in the trace. 

## **Batching and placeholders** 

A trace can only assign, test or rule out values it is given. Two changes to the problem make this harder while leaving the formalization task intact. **Batching** gives _K_ problems of the same dataset in one prompt and asks for _K_ separate programs, each headed by its problem’s number: the encoding can be designed once, but solving in prose must be done _K_ times. **Placeholders** replace every value of a problem by a name (Person1, Day1, T1 for clock times, D1 for durations, L1 for locations, and a table TRAVEL for Meeting Planning’s travel times), and the program receives the values only when it runs, as a dictionary VALUES (Appendix D, Listing 4). The model must therefore write out the problem’s structure in placeholder names. Placeholder numbers are shuffled, so their order reveals nothing about the times. The model can still choose among placeholders (“meet Person2 first, from T3”), which the A judge counts as SLB. We apply placeholders only to Calendar and Meeting Planning, whose values separate cleanly from the structure. We run both methods for Qwen 

7


<!-- page 8 -->

<!-- Start of picture text -->
Pooled (95% CI) DeepSeek GPT-OSS Qwen<br>Solver-like tokens per problem (%) Solver-like ratio Program accuracy (points)<br>Cautionary A<br>Cautionary B<br>Batching ( K =5)<br>Placeholders<br>−100 −75 −50 −25 0 −0.2 −0.1 0.0 −10 −5 0 5<br><!-- End of picture text -->

Figure 6: Placeholders all but remove solver-like behavior without costing accuracy; cautionary prompts remove about a quarter of it, and batching shortens all reasoning at a cost in accuracy. Change from the baseline prompt on the same problems in solver-like tokens per problem (% of the baseline mean), solver-like ratio, and program accuracy (points): pooled estimate with 95% bootstrap confidence interval, and one dot per model. Each method is measured where it was run: cautionary prompts for every model, dataset and FL (2,000 pairs), batching ( _K_ = 5) for Qwen and GPT-OSS in every dataset and FL except PDDL (1,400), placeholders for Qwen and GPT-OSS on Calendar and Meeting Planning in Python and Z3 (800). The subsets differ, so the text compares each method with the cautionary prompts on its own problems. 

and GPT-OSS on the same 100 problems of every dataset and FL except PDDL, with _K_ = 5, and add _K ∈{_ 2 _,_ 10 _}_ for GPT-OSS on Calendar and Meeting Planning in Python. A batch’s trace serves _K_ problems, so each of them is credited with the trace’s ratio and 1 _/K_ of its tokens. The A judge overcounts SLB in placeholder traces, which can only understate the placeholders’ effect (Appendix E). 

**Placeholders all but remove solver-like behavior without costing accuracy** (Figure 6). Solverlike tokens per problem fall by 97% [96 _,_ 98], from 2,820 to 78; the ratio falls from 0.25 to 0.005, and the share of traces with SLB from 94% to 15%, for both models in both FLs. On the same problems, the cautionary prompts cut solver-like tokens by only 32% and 18%. Accuracy rises by 2.6 points [ _−_ 0 _._ 5 _,_ +5 _._ 9]. The largest gain, GPT-OSS on Meeting Planning in Python (0.66 to 0.82), comes partly from programs that inherited the reasoning answer: 13 of the 28 problems that placeholders fix had such a program under the baseline. Since the model never sees a value, it cannot hardcode an answer, and the program, not the trace, computes the result. The cost is length for Qwen, whose reasoning per problem grows by 54% (more than threefold on Calendar); in the longest of these traces we read, the added text concerns the program’s robustness to values it cannot see, such as intervals ending at 24:00, not the solution. GPT-OSS’s reasoning shrinks by 31%. 

**Batching shortens all reasoning, not just the** 

**solving, and costs accuracy.** Solver-like tokens per problem fall by 62% [55 _,_ 68], but reasoning tokens fall almost as much (61%), so the ratio barely moves ( _−_ 0 _._ 02 [ _−_ 0 _._ 045 _,_ +0 _._ 001]; Qwen +0 _._ 04): the encoding is designed once for the batch, while each problem is still worked out in prose. Accuracy falls by 5.9 points [ _−_ 11 _._ 0 _, −_ 0 _._ 5], most on ZebraLogic, by 15 to 26 points for each model in each FL. Larger batches cut more: for GPT-OSS on Calendar and Meeting Planning in Python, solver-like tokens per problem fall by 56%, 78% and 91% at _K_ = 2, 5 and 10, with accuracy 2, 6 and 3 points above the baseline. 

# **7 Conclusion** 

Formalizers are meant to leave the search to a solver, yet their reasoning traces routinely do it themselves. Across three models and four datasets, this solver-like behavior is common and redundant, is not associated with accuracy, and depends most on the formal language. The few programs that inherit the reasoning answer also inherit its errors, and output-based evaluation cannot tell them from programs that search, so formalizers should be judged by how their programs are reached, not only by what they output. For practitioners, the most reliable remedy is to keep the instance’s values out of the prompt: placeholders bound at run time remove nearly all solver-like behavior without loss of accuracy and rule out hardcoded answers. Otherwise, cautionary prompts remove only a quarter of it, and batching costs accuracy. 

8


<!-- page 9 -->

# **Limitations** 

Our study covers three reasoning models and four constraint satisfaction datasets, each in two formal languages. Other task types, such as theorem proving or optimization, and other languages may show different amounts of solver-like behavior. DeepSeek is run in only one formal language per dataset because the model behind its API changed between our runs, so H4 rests on Qwen and GPTOSS, and its runs cannot be reproduced exactly. The two prompts of a dataset differ in more than the formal language (§4), notably the reference problem file in the PDDL prompt, which may contribute to the differences H4 attributes to it. Each problem is generated once per setting, so our intervals do not capture sampling variation across generations. 

Our ontology labels come from LLM judges and scripts. The judges agree well with reference labels (Table 1), but the reference samples are small (110 paragraphs for A1, 40 traces for A2, 60 programs for B) and come from one annotator, one B check compares against labels written by a second model and the other showed the human the judge’s evidence, A1 was checked on paragraphs and not on whole traces, and A2 was checked with the help of a script and a second model because full traces are too long to annotate by hand. B and C cover nonrandom subsets: B only programs that run (1,791 of 2,000, which drops most of Qwen’s crashing Z3 programs), and C only the 1,547 complete reasoning answers, of which C1 can compare 1,314 with the program’s output. C also covers only reasoning answers that the task’s parser reads, and for Meeting Planning an extracted reasoning answer sometimes combines two tentative itineraries, so its error rate is an upper bound. The solver-like ratio counts whole paragraphs, so a paragraph that mixes encoding and solving counts entirely toward it. 

Finally, H3 is observational: fixed effects for the problem remove differences in difficulty, but not every confounder. The cautionary prompts in §6 reduce solver-like behavior without changing accuracy, which supports H3, but they remove only part of it. Placeholders remove almost all of it, but apply only where a problem’s values separate from its structure; we test them, and batching, on two models and not in PDDL, and placeholders on two datasets. 

# **Ethical Considerations** 

**Risks.** We study how formalizers reach their programs and see no direct path to misuse. The risk our results point to is in deployment: a program that hardcodes or inherits the reasoning answer looks as verifiable as one that searches, so systems that trust formalizer output without validating it may act on answers no solver checked (§5). Solver-like reasoning is also redundant computation, which placeholders remove (§6). 

**Data.** The datasets are synthetic English constraint satisfaction problems. Calendar Scheduling and Meeting Planning refer to fictional people by first name only; the problems contain no information about real people, and we found no offensive content in them or in the traces we read. Datasets, models and licenses are listed in Appendix A. 

**Human annotation.** All human reference labels (Table 1, Appendix E) were written by one of the authors, an NLP researcher, using the definitions in the judge prompts. No crowdworkers or other participants were involved, and no personal data was collected. 

**Use of AI assistants.** We used Claude Code as a coding and writing assistant: to write and debug the experiment and analysis code, to run experiments, and to draft and edit text. The authors designed the study, directed and checked this work, and take responsibility for the paper; all reported numbers come from scripts in our repository.
