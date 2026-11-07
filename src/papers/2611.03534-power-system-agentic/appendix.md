---
source: 2611.03534-power-system-agentic.pdf
part: appendix
converted: 2026-11-07
converter: pymupdf4llm
---

# An Agentic Framework for Automated Power System Studies and Grid Connection Assessment · 附录

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

**Appendix** 

# **A Example Questions and Tasks** 

Table 6 gives one question per depth level. Examples 1 and 2 are regulatory questions, and Examples 3 to 5 are power-system tasks with their strict-pass checks. 

## **Example 1 A regulatory question from the GB Regulation Set** 

### **QUESTION** 

According to the TMO4+ Summary Decision Document, what target has the UK Government set for carbon-free electricity by 2030 as part of its Clean Power 2030 Action Plan? 

### **ANSWER KEY** 

95% carbon-free electricity by 2030. Evidence anchor: the TMO4+ Summary Decision Document (Ofgem, April 2025), page 4, “. . . to achieve 95% carbon-free electricity by 2030 . . . ” 

### **GRID ONTOLOGY** 

Correct, and its first citation is the anchored passage (recall 1.0, reciprocal rank 1). 

### **CLAUDE CODE WITH FILE TOOLS ONLY** 

Correct, but it cites nothing, so recall is 0. 

### **WHY IT MATTERS** 

Both answers are right, but only one can be checked against its source. Across the set, this is the recall gap in Table 3. 

## **Example 2 Clause-level evidence on LegalBench-RAG (CUAD)** 

**Example 3 Rebuilding a published operating point (PF** ∆ **, IEEE 14-bus, one unit out)** 

### **QUESTION (ABRIDGED)** 

Reproduce the operating point below on the base case, exactly as given, then run the study that answers the question and report the value it solves for. Every figure listed is an input to build. None of them is the answer. 

- Generating units out of service: gen_1 

- Demand by bus, [P MW, Q Mvar]: {"1": [27.126, 

- 3.916], "2": [40.063, 0.053], . . . eleven buses} 

- Scheduled active power by unit, MW: {"gen_0": 

- 59.0, "gen_2": 0.0, "gen_3": 0.0} 

- Voltage set-point by bus, pu: {"0": 1.06, "1": 

- 1.05067, "5": 1.06, "7": 1.06} 

- . . . What is the voltage magnitude (per unit) at bus 9? 

### **ANSWER KEY** 

0.904925 pu _±_ 0.001, from the authors’ Ipopt solution. 

### **STRICT-PASS CHECKS** 

(1) The answer is within 0.001 pu. (2) The replayed calls show gen_1 out of service and every stated demand, dispatch and set-point in force (values the base case already holds may be left as they are). (3) An AC power flow was solved after the last change. (4) Nothing else was changed. A correct number that fails (2), (3) or (4) is not a strict pass. 

### **RESULT** 

Grid Studio passes all 71 PF∆tasks strictly. Of the two frontier base models, GPT-6.1 sol answers 29.6% of them correctly, with its work verified on three 14-bus tasks, and Fable 5.1 answers 11.3%. 

### **QUESTION** 

Consider the Blockchain Administration and Development Agreement between ARCA U.S. Treasury Fund and ARCA Capital Management, LLC; What is the renewal term for this contract? 

### **GOLD CLAUSE (605 CHARACTERS, ABRIDGED)** 

“This Agreement shall continue in effect for two years from the date hereof, and thereafter shall continue automatically for successive annual periods, provided that such continuance is specifically approved at least annually [. . . ].” 

### **GRID ONTOLOGY** 

Cites the whole clause (precision, recall and F1 1.00). 

### **CLAUDE CODE WITH FILE TOOLS ONLY** 

Gives the same answer but cites only the first 149 characters (precision 1.00, recall 0.25, F1 0.40), leaving out the annual approval that makes the renewal conditional. 

**Example 4 A natural-language OPF modification (ProOPF-B, level 1)** 

### **REQUIREMENT (THE AUTHORS’ WORDS)** 

Perform AC optimal power flow (ACOPF) on the IEEE 14-bus system (case14). Scale the active power demand at bus 3 by a factor of 1.8. Set the maximum active power output of all generators at bus 2 to 200 MW. Set the OPF violation tolerance (opf.violation) to 1e-6, and write the corresponding MATPOWER code. 

### **ANSWER KEY** 

Objective 11,178.32 from the authors’ MATPOWER run, at the benchmark’s relative tolerance of 10<sup>_−_4</sup> . 

13


<!-- page 14 -->

**Table 6: One question per depth level (abridged).** Questions in quotation marks are as the system receives them, and the others are paraphrased. Answer keys are the benchmarks’ own. 

|Dep|th level|Question|Answer key|
|---|---|---|---|
|R1.|Single passage|“In the RIIO-3 Final Determinations for Electricity Transmission, what are<br>‘user progression milestones’ as referenced in the CUSC?”|Conditional and<br>Construction<br>Progression Milestones|
|R2.|Figure or table|“According to the G99 connection process diagram for Types A-D PGMs,<br>how many sequential phases are shown in the flowchart, . . . ?”|Six phases|
|R3. <br>pass|Several<br>ages|“Under the Grid Code, . . . what is the post-fault voltage recovery level<br>(Urec2) at tclear according to Figure ECC.6.3.15.7, and at what operating<br>condition must the equipment be capable of satisfying the Fault Ride<br>Through requirements . . . ?”|0.85 pu at 0.14 s, at<br>rated MW and<br>maximum leading<br>power factor|
|R4.|Clause spans|“Consider the Blockchain Administration and Development Agreement<br>between ARCA U.S. Treasury Fund and ARCA Capital Management, LLC;<br>What is the renewal term for this contract?”|A 605-character clause|
|L1.|As given|“On the PEGASE 9241-bus, run DC power flow. What is the loading of<br>transformer 1652 in percent?”|976.22%|
|L2.|Stated changes|On case118, scale the load at bus 7 by P_×_0.9705 and Q_×_1.0312 and the<br>load at bus 56 by P_×_1.0881 and Q_×_0.9949, run an AC power flow and<br>report the voltage magnitude at bus 79.|1.009223 pu|
|L3. <br>mod|Resolve, then<br>ify|“On the PEGASE 9241-bus, identify the most heavily loaded line under the<br>current operating point and take that line out of service, run DC power<br>flow. What is the loading of transformer 1602 in percent?”|61.62%|
|L4. <br>poin|Operating<br>t|Rebuild the demand at eleven buses, the dispatch of three units, four<br>voltage set-points and one unit outage on the IEEE 14-bus system, then<br>report the voltage at bus 9 (Example 3).|0.904925 pu|
|L5.|Reformulate|“Perform AC optimal power flow (ACOPF) on the IEEE 14-bus system<br>(case14). Scale the active power demand at bus 3 by a factor of 1.8. Set the<br>maximum active power output of all generators at bus 2 to 200 MW. . . . ”<br>(Example 4)|Objective 11,178.32|



### **STRICT-PASS CHECKS** 

The objective is within tolerance, and the replay shows bus 3’s active demand at 1.8 times its base value (reactive demand unchanged) and the bus-2 unit’s maximum at 200 MW before the OPF is solved. The solver tolerance is a MATPOWER setting, not part of the network, and is not graded. 

## **Example 5 Comparing switching states (RL2Grid adaptation, IEEE 30-bus)** 

### **QUESTION (PARAPHRASED)** 

In case30 at base load, evaluate these simultaneous double-line outages independently: (L9, L28), (L28, L29) and (L28, L15). Which produces the highest maximum branch loading, and what is that loading? 

### **ANSWER KEY** 

The pair (L9, L28), at 154.5% _±_ 1 point, from the reference solver (an adapted family, Table 2). 

### **STRICT-PASS CHECKS** 

Each pair is built as one joint state and solved, the network is restored between pairs, and every named pair 

is evaluated. An answer read off a single-outage screen fails even when its number is close, because post-outage flows do not add up across outages. 

### **RESULT** 

Every tool-using system answers all seven RL2Grid tasks. Of the frontier base models, GPT-6.1 sol answers two and Fable 5.1 one, and the work of neither is verified on any. 

# **B Power-System Metrics** 

Each power-system task is graded on the answer a system reports and on the work that produced it. This appendix defines the terms of Eq. 1, how the work is verified and why the terms are weighted as they are. 

**Why the work is graded.** Most answers are voltages, loadings or costs on standard IEEE and PGLib networks, so a value can be recalled from published results, guessed close to the truth or reached by a study on the wrong grid state. An engineer acts on a result only when the study behind it is known to be right, so only a correct answer with verified work earns full credit. 

14


<!-- page 15 -->

**Terms for one task.** For task _i_ , let _ai_ be the reported value and _gi_ the answer key, compared at the benchmark’s own tolerance. 

- _Correct answer_ : _ri_ = 1 if _ai_ is within tolerance of _gi_ and every named choice, such as the outage pair in Example 5, matches the key, and _ri_ = 0 otherwise. 

- _Verified work_ : _vi_ = 1 if the recorded work shows the required study on the required grid state, and _vi_ = 0 otherwise. 

- _Strict pass_ : _si_ = _ri vi_ . 

- _Numeric closeness_ : _ci_ = 1 within tolerance, and max�0 _,_ 1 _−|ai − gi|/_ max( _|gi|,_ 1)� otherwise. 

_A_ , _P_ and _c_ ¯ are the means of _ri_ , _si_ and _ci_ over all _n_ tasks, so _E_ is the mean of _ei_ = 0 _._ 25 _ci_ + 0 _._ 25 _ri_ + 0 _._ 5 _si_ . A task scores 1 when its answer is correct and its work verified, 0.5 when only its answer is correct, at most 0.25 when its answer is wrong and 0 when it has no answer. Tasks a system cannot execute, for example for lack of a tool, stay in the mean. Leaving them out would grade that system on an easier subset. 

**Verifying the work.** The required work comes from the task, never from the answer key: the grid state the question fixes (the published network with every stated change), the type of study, any stated study arguments and, for a comparison, every candidate state. Table 7 shows what is checked for each kind of system. A value the base case already holds may be restated or left as it is, but any other change, such as an extra open line, makes a different state and fails. 

**Table 7: How the work of each kind of system is verified.** 

|System|Record checked|Work is verified when|
|---|---|---|
|Grid Studio|Its tool calls,<br>replayed|A study of the required<br>type ran on exactly the<br>required state|
|Power-Agent|Every state its<br>solver returned,<br>logged in the<br>sandbox|A logged state matches<br>our own solution of each<br>required network|
|Claude Code,<br>Codex CLI|The solved states<br>they report with<br>their answer|Each required state<br>matches our own solution<br>of the required network|
|Base models|The solved states<br>they report with<br>their answer|As for Claude Code and<br>Codex CLI|



The coding agents and the base models solve the network in their own code or by themselves, so they report with their answer the solved states it rests on. We solve the required network ourselves and accept a power flow when the reported voltages match ours at every bus within 10<sup>_−_4</sup> pu and 0 _._ 01<sup>_◦_</sup> , up to a common angle shift, an N-1 or a comparison when each of its states does, and an OPF when its dispatch balances and respects 

every limit of the required network. In a control on 31 sampled tasks, this check accepted every correct state and rejected states solved with a required change left out, apart from two OPF tasks where that change does not bind. Base models receive the network as text in their prompt, or the question alone where the network is too large to fit. 

**Why these weights.** Strict pass carries half the weight because it is the result that matters in use, so a system whose work cannot be shown reaches at most half the score. Answer accuracy carries a quarter, so a correct answer without verified work still beats a wrong one. Closeness carries the last quarter. It equals 1 on every correct answer and only separates a near miss from a large error. A guess at a per-unit voltage near 1 earns much of it, so it never decides a pass. 

# **C Full Results on the PowerSystem Benchmarks** 

Table 8 gives the end-to-end score of every system on the 519 tasks, and Figure 5 shows how much each system’s results vary across families and tasks. 

# **D Evaluation Protocol Details** 

**GB Regulation Set.** Pages and figures are sampled from the corpus with a seeded generator, never through the system under test. A model sees only the sampled passage or figure and writes a question, its answer and verbatim quotations. Separate checks discard questions the evidence does not support and questions answerable without it [12], and the domain owner approves the rest. Each question keeps its evidence anchors (document, page, character span or figure). The 45 questions (25 text, 14 figure, 6 multi-hop) come from 23 of the 27 documents. 

**ViDoRe V3 depth.** From the benchmark’s own labels, the 203 multi-hop questions are R3, the 1,312 others answered from a table, chart, infographic or image are R2, and the remaining 904 are R1. 

**Power-system questions.** Every task is posed as a question about a stated network with one value to report, so that every system receives the same wording and is graded the same way. PFBench, PowerCodeBench and ProOPF-B publish such questions, and we ask them in their authors’ words. Where one omits a quantity or choice its answer depends on (156 of 352 PowerCodeBench and 6 of 19 ProOPF-B items), we restore it from the item’s own record, never adding the answer. PF∆and PGLib-OPF publish networks and solved results but no questions, so we pose each task from a fixed 

15


<!-- page 16 -->

**Table 8: End-to-end score of every system on each benchmark family.** _E_ (%, Eq. 1) on the 519 tasks, with PowerCodeBench (PCB) at 352. _±_ is the half-width of Grid Studio’s 95% confidence interval. Base models get the network as text. 

|||||End-to-|end score|_E_ (%)_↑_||||
|---|---|---|---|---|---|---|---|---|---|
|System|PFBench|PF∆|PAB-SS|PSAB|PCB|PGLib|ProOPF|RL2Grid|Mean|
|Grid Studio|100.0_±_0.0|100.0_±_0.0|100.0_±_0.0|100.0_±_0.0|99.2_±_0.9|100.0_±_0.0|100.0_±_0.0|100.0_±_0.0|**99.9**_±_0.1|
|_Coding agents and _|_Power-Agent_|||||||||
|Codex CLI|100.0|100.0|100.0|100.0|94.9|100.0|100.0|100.0|99.4|
|Claude Code|94.5|92.5|91.0|84.4|78.5|88.3|63.8|89.9|85.4|
|Power-Agent|100.0|97.9|100.0|100.0|97.5|100.0|100.0|100.0|99.4|
|_Proprietary base mo_|_dels_|||||||||
|GPT-6.1 sol|45.5|32.8|41.8|58.2|42.9|42.5|31.6|31.4|40.8|
|GPT-5.6 sol|36.5|24.6|36.6|44.8|35.0|32.9|30.2|22.0|32.8|
|Fable 5.1|24.4|16.8|36.1|54.7|14.8|19.3|35.5|24.7|28.3|
|Sonnet 5.5|29.3|15.0|35.9|44.3|24.2|28.5|24.6|24.4|28.3|
|Nova Pro|14.1|11.3|6.1|16.7|14.3|22.4|6.4|18.0|13.7|
|_Open-weight base m_|_odels_|||||||||
|GPT-OSS-120B|17.5|14.2|24.4|32.4|20.0|22.6|21.3|19.1|21.4|
|Kimi K2.5|21.2|15.5|24.1|28.9|18.7|21.0|19.1|18.5|20.9|
|DeepSeek V3.2|17.7|15.0|27.8|29.7|20.3|17.8|7.9|25.1|20.2|
|Qwen3-Coder-Next|18.7|14.9|27.7|22.3|18.0|18.4|7.6|19.7|18.4|
|GLM-4.7|16.1|15.6|17.9|27.8|18.6|18.6|7.8|16.5|17.4|
|Mistral Large 3|16.8|14.8|6.3|22.0|17.4|20.3|19.6|20.9|17.3|



template that names the network, any stated changes and the quantity to report. PowerAgentBench-SS releases task specifications without a question set, PSAB’s tasks are built for agents that work on files, and RL2Grid scores reinforcement-learning episodes rather than answers. For these three we keep the kind of study each one tests and write the questions ourselves, with answers from a reference solver. In all, 389 of the 519 questions are in their authors’ words and 130 are ours. Ours come from fixed templates, not from a language model. 

**Answer keys.** Answer keys never come from the system under test. The regulatory keys are the published ones, apart from the GB Regulation Set’s, which the domain owner approved. PFBench, PowerCodeBench and ProOPF-B use their authors’ published answers, PF∆its authors’ Ipopt solutions, and PGLib-OPF its published OPF baseline, with a reference solver for its power-flow tasks. The three adapted families (Table 2) are graded against a reference solver, so we treat them as weaker evidence. Run with no model, the reference solver reproduces every published answer of PFBench, PF∆, PowerCodeBench and ProOPF-B (460 tasks), so a solver discrepancy is never counted as an agent failure. 

**Isolation.** Each coding-agent task runs in its own container (2 vCPU, 8 GB) with no answer key and no network access, and a task that fetched anything would count as unanswered. None did. An audit of every GB Regulation Set run with file access found no read of an answer key. Grid Studio runs with memory off, and its 

timed runs use the same container size, one task per container. 

**Agent work time.** Agent work is the time spent on model turns and tool runs, read from each agent’s own clock. It excludes start-up, which covers launching and tearing down the container and starting the agent and, for Grid Studio, its solvers. Codex CLI reports no such split, so its time is the whole run of its process, an upper bound. A base model spends all its time on one completion. Figure 1 reports the median over the 519 tasks. A coding agent loads its libraries inside its own scripts, while starting Grid Studio’s solvers, 6.7 s on average when we measured it, is not counted. 

**Systems compared.** Table 9 gives each system’s version and setting. The two base models in the table and the nine further ones in Figure 1 and Table 8 ran on the same 519 tasks between 29 and 31 October 2026, each with the network in its prompt, and were graded with the same grader. Grid Studio, Power-Agent and the base models ran once per task, and Codex CLI and Claude Code once on PowerCodeBench and five times on the other families. Power-Agent ran on 2 November 2026 in the same sandbox as the coding agents, with no network access beyond the model. GPT-5.6 sol lost 26 PowerCodeBench tasks and GPT-6.1 sol 3 to provider quota limits, counted as unanswered, and Fable 5.1 answered 146 PowerCodeBench questions in their earlier wording. Fable 5.1 and Sonnet 5.5 reached the reply limit without an answer on 170 and 128 tasks, and Fable 

16


<!-- page 17 -->

<!-- Start of picture text -->
Score on each benchmark family<br>100<br>75<br>50<br>25<br>0<br>GridStudioCodexClaudeCLIPower-AgentCodeGPT-6.1GPT-5.6sol FablesolSonnetGPT-OSS-120B5.1 5.5KimiDeepSeekQwen3-Coder-NextK2.5V3.2 MistralGLM-4.7LargeNova3 Pro<br>(%)End-to-end E score<br><!-- End of picture text -->



<!-- Start of picture text -->
Time on each task<br>1000<br>500<br>200<br>100<br>50<br>20<br>10<br>5<br>2<br>GridStudioCodexClaudeCLIPower-AgentCodeGPT-6.1GPT-5.6sol FablesolSonnetGPT-OSS-120B5.1 5.5KimiDeepSeekQwen3-Coder-NextK2.5V3.2 MistralGLM-4.7LargeNova3 Pro<br>(s,scale)Agentworktasklogtimeper<br><!-- End of picture text -->

**Figure 5: Spread of each system’s power-system results.** Left: _E_ on each of the eight benchmark families (box: middle half, whiskers: all eight, diamond: mean). Right: agent work time on each of the 519 tasks (box: middle half, line: median, whiskers: 5th to 95th percentile). 

5.1 refused 115. Where a provider’s quota ran out during a run, the remaining tasks ran on the same model through another provider (GPT-6.1 sol and Sonnet 5.5). Grid Studio’s tools were extended where a benchmark, PowerCodeBench among them, asked for a study they did not yet cover, and the affected benchmarks were run again. 

**Table 9: Systems compared on the power-system benchmarks.** 

At the clause level, agentic systems reach an F1 an order of magnitude above retrieval pipelines (0.47 to 0.62 against 0.03 to 0.09), so pipelines find the right contract but not the clause. In a sweep over chunking, hybrid search and embeddings [66], no pipeline configuration exceeded a clause F1 of 0.13. PageIndex reaches clause recall 0.72 but precision 0.05, because it returns whole sections. The Grid Ontology leads on both clause and document F1, and Example 2 shows what clause-level scoring rewards. 

|System|Configuration|
|---|---|
|Grid Studio|With its domain tools, memory off|
|Claude Code|CLI v2.1.289 on the same model as Grid<br>Studio, with shell and Python (NumPy,<br>SciPy)|
|Codex CLI|CLI v0.160.0 on GPT-6.1 sol, with shell<br>and Python (NumPy, SciPy)|
|Power-Agent|Claude Code CLI v2.1.289 on the same<br>model as Grid Studio, with|
||PowerMCP 0.4.1, the PowerSkills<br>playbooks as published, shell, Python and<br>pandapower|
|GPT-6.1 sol|One completion, no tools, network as text<br>in the prompt|
|Fable 5.1|Claude Fable 5.1, one completion, no tools,<br>network as text in the prompt|



**Table 10: LegalBench-RAG at the clause level.** _Span_ metrics are the benchmark’s own, scored on characters of the gold clause, and _Doc F1_ is the F1 of Table 3. All systems answer the same 50 questions. 

|||Span||Doc|
|---|---|---|---|---|
|System|P_↑_|R_↑_|F1_↑_|F1_↑_|
|Grid Ontology|0.587|0.748|**0.616 **|**0.980**|
|Claude Code (file tools)|0.570|0.679|0.561|0.900|
|Recursive LM|–|–|0.467|0.860|
|Vector + reranker|0.029|0.343|0.050|0.869|
|PageIndex, official|0.050|0.723|0.087|0.799|
|Dense hybrid, semantic|–|–|0.047|0.704|
|Dense hybrid, parent-child|–|–|0.034|0.796|



# **E LegalBench-RAG Details** 

# **F ViDoRe V3 Details** 

Table 3 scores LegalBench-RAG by document. Precision is the share of cited contracts that hold the answer, and recall the share of answer-holding contracts that were cited. The benchmark’s own metrics are stricter and score the character overlap between the cited text and the gold clause. Table 10 gives both. 

Table 11 gives the ViDoRe V3 scores of Table 3 per set. The Grid Ontology leads on four of the eight sets, VisAgentRet on three and EVIE-4.5B with JEV-27B-VL on physics. We chose the agent’s settings on the first 40 questions of each set, then ran all 2,419 questions. One question ended in an error and is left out of its set’s 

17


<!-- page 18 -->

**Table 11: ViDoRe V3 nDCG@10 (** _×_ 100 **) per set.** Ours is the Grid Ontology. VAR is VisAgentRet (EVIE-4.5B with a GLM-5.3-Flash agent), NeMo is NeMo Retriever’s agentic pipeline (ColEmbed-VL-8B with a Claude Opus 4.5 agent), JEV is EVIE-4.5B reranked by JEV-27B-VL, and Jina is jina-embeddings-v4 reranked by zerank-2. Best in **bold** . 

|||nDCG<br>|@10 (_×_<br>|100)_↑_<br>||
|---|---|---|---|---|---|
|Set|Ours|VAR|NeMo|JEV|Jina|
|Finance (EN)|**77.62**|76.67|75.88|74.49|74.24|
|Finance (FR)|**60.94**|60.30|58.60|56.96|51.43|
|Computer science|**85.60**|84.81|84.49|84.01|83.46|
|Human resources|73.48|**74.51**|74.50|71.68|69.10|
|Energy|75.36|**75.68**|75.52|73.42|71.17|
|Industrial|**65.49**|63.95|63.40|63.57|58.89|
|Pharmaceuticals|74.67|**75.14**|74.79|72.42|68.58|
|Physics|48.66|49.01|46.59|**49.42**|48.06|
|Mean|**70.23**|70.01|69.22|68.25|65.62|



mean (counted as zero, the mean is 70.20). 

18
