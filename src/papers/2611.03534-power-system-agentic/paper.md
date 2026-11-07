---
source: 2611.03534-power-system-agentic.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# An Agentic Framework for Automated Power System Studies and Grid Connection Assessment · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

# **An Agentic Framework for Automated Power System Studies and Grid Connection Assessment** 

Technical Report 

MaoXun Huang Kshitij Kapoor Eli Louise 

Grid Agents 

```
{mao, kaps, eli}@grid-agents.com
```

### **Abstract** 

Connecting new generation and demand to the grid depends on two scarce skills: checking applications against a large, changing body of regulation, and running the network studies that decide where and how a project connects. We present _Grid Agents_ , an AI system that brings both together, and the methodology we use to evaluate it. The _Grid Ontology_ is its knowledge system. It represents the regulation, standards and engineering knowledge that grid work depends on, makes it searchable, and evolves as the agents learn from use. Every answer drawn from it rests on evidence the agents cite. _Grid Studio_ is an agent system specialised for power-system engineering. It works in its own engineering environment with domain tools and a study framework, draws on the Grid Ontology, and relies on established solvers for every number it reports. In both, engineers make the decisions. We bring eight published power-system benchmark families, previously scattered across separate papers, into one suite of 519 tasks, and we verify not only each answer but the work behind it, by replaying the agent’s tool calls. The Grid Ontology cites the right regulatory evidence more often than a general coding agent or retrieval pipelines, leads on LegalBench-RAG and ranks first on the public leaderboards of the Enterprise RAG Challenge and ViDoRe V3. Grid Studio scores highest on the 519 power-system tasks and is the fastest of all the systems we compare, both by a statistically significant margin. With an optimiser in the loop, its reinforcement packages cost 33–67% less on average than those the agent designs alone. 



<!-- Start of picture text -->
Grid Studio Coding agent Base model<br>100 Grid Studio Codex CLI<br>Slower than Grid Studio and scoring lower<br>Claude Code<br>75 Power-Agent<br>50 GPT-6.1 sol<br>Sonnet 5.5 GPT-5.6 sol Fable 5.1<br>GPT-OSS-120B<br>25<br>Nova Pro GLM-4.7Kimi K2.5 DeepSeek V3.2 Qwen3-Coder-Next<br>Mistral Large 3<br>0<br>10 20 50 100 200<br>Median agent work time per task (s, log scale)<br>Better<br>(%)End-to-end E score<br><!-- End of picture text -->

**Figure 1: End-to-end score against agent work time per task.** Each point is one system on the same 519 tasks. Every other system is slower than Grid Studio and scores lower, and both differences are statistically significant (Table 4). 

## **1 Introduction** 

Grid connection, more than generation, now limits the energy transition. At least 3,000 GW of renewable projects 

were waiting in connection queues worldwide in 2023 [18]. In the United States alone, about 2,600 GW of generation and storage was seeking interconnection at the end of that year [45]. Both the United States and Great 

1


<!-- page 2 -->

Britain have reformed their connection processes in response [9, 38]. 

Each connection request needs two kinds of expert work. _Regulatory_ work checks the application against legislation, grid codes and standards that run to thousands of pages and change as reform proceeds. _Engineering_ work decides where the project can connect and what reinforcement it needs, by running power-flow, contingency (N-1) and short-circuit studies on a network model [25, 63]. Both are slow and both are short of people. 

Agents built on large language models (LLMs) plan, call tools and act on the results [48, 61, 67], which suits both tasks. They also fail in three ways that matter here. They write fluent text that no source supports [20]. They cannot be trusted with the arithmetic of large network equations. Finally, a correct answer does not show that the work behind it was correct. The same number can come from the right study, from memory or from a study of the wrong grid state, and most benchmarks grade only the number. Yet a connection decision commits costly network works and can be challenged by the applicant or the regulator, so the engineer must be able to show which study ran on which network. 

We present _Grid Agents_ , a system designed around these failure modes. It has two parts (Figure 2): 

- The **Grid Ontology** is the knowledge system of Grid Agents. It represents the regulation, standards and engineering knowledge that grid work depends on, makes it searchable by the agents, and evolves as they learn from use, with people approving what is shared.<sup>1</sup> Agents answer questions and review applications from it, and every answer rests on evidence they cite. 

- **Grid Studio** is an agent system specialised for power-system engineering. It works in its own engineering environment, with domain tools and a framework that carries a study from the choice of connection point to the final report, and it is connected to the Grid Ontology for the knowledge its studies draw on. Established solvers compute every number it reports. 

## **Contributions.** 

1. **A design** for agents in regulated engineering work, built on three principles, with a memory that learns from use under human approval (Section 3). 

2. **A power-system benchmark suite** of 519 tasks from eight published benchmark families, on networks of 4 to 9,241 buses, graded the same way on one scale of depth (Section 4.1). 

3. **Results and findings** against coding agents, retrieval pipelines, leaderboard entries and frontier 

- 1We use _ontology_ for an organised body of domain knowledge, 

- not a formal specification of a conceptualisation [13]. 

models, with each agent’s work verified against the study it ran (Section 5). The Grid Ontology cites the right regulatory evidence more often than any other system. Grid Studio leads the best coding agent in both score and agent work time, by a statistically significant margin, and its lead is largest on the biggest networks. Optimisation in the loop makes reinforcement cheaper. 

# **2 Background and Related Work** 

**Retrieval and citation.** Retrieval-augmented generation conditions a model on passages fetched for the question [27]. In its common form a pipeline searches once and the model answers from what comes back. The search may be lexical or dense, often followed by a reranker [24, 37, 47]. It may also run over a graph built from the corpus [7] or follow a document’s own hierarchy [58]. Longer context windows do not remove the need to retrieve well [28]. Agentic approaches instead let the model decide what to retrieve and judge what it found [1], or explore the corpus from a programming environment [69]. Because a reviewer must be able to check every source, the citations matter as much as the answer. Work on attributed generation measures whether citations support the claims [10], and model judges score faithfulness and answer quality [8, 71]. LegalBench-RAG [42], built on CUAD [15] and related to LegalBench [14], scores retrieval on exact character spans, which separates finding the right document from finding the right clause. 

**Tool-using agents and their evaluation.** Engineering work needs an agent that acts as well as reads. ReAct interleaves reasoning and action [67], Toolformer learns when to call a tool [48], Reflexion adds self-critique [52], AutoGen composes several agents [65] and MANTA lets a multi-agent system adapt how its agents collaborate while it runs [17]. As agents began to act, their evaluation moved from judging text to checking outcomes. SWE-bench runs a repository’s tests [22], AgentBench spans many environments [29] and _τ_ -bench compares the final database state with a goal state [68]. Our strict pass brings this state-based grading to engineering studies by checking the grid state that each study ran on. 

**Agent memory.** An agent that works beside the same people for months should also keep what it learns. CoALA organises a language agent’s memory into working, semantic, episodic and procedural stores [53], after the distinction drawn in human memory [57]. MemGPT pages information between the context and external storage [39]. Generative Agents and Reflexion turn experience into reflections that guide later behaviour [41, 52], ExpeL distils insights from past trajectories [70] and Voyager grows a library of skills [60]. These systems learn on 

2


<!-- page 3 -->

<!-- Start of picture text -->
PEOPLE Developer Reviewer Planning engineer<br>submits an application grid operator • decides runs studies • decides<br>application findings • sign-off consults • decisions<br>Grid Ontology agent Grid Studio agent<br>AGENTS<br>answers and reviews with citations plans and runs studies<br>retrieve • cite recall • learn (approved) tool calls • results<br>Grid Ontology<br>Power-system solvers<br>KNOWLEDGE power flow • N-1 • OPF<br>& TOOLS Regulation corpus Memory short circuit • dynamics<br>legislation, codes and standards facts, skills, experiences time series<br><!-- End of picture text -->

**Figure 2: High-level system design of Grid Agents.** People sit above two agents. The Grid Ontology agent answers and reviews with citations, and Grid Studio runs engineering studies through established solvers. Both draw on the Grid Ontology’s knowledge (the regulation corpus and a memory that learns from use under approval). 

their own. In regulated work, one engineer’s session must not silently change a colleague’s agent, so the memory we describe in Section 3.2 adds human approval. 

**Power-system studies.** In engineering work, the actions an agent takes are calls to power-system analyses whose methods are long established. A power flow solves the AC network equations for voltages and flows at one operating point [63]. Security standards require the system to survive any single credible outage [36], so a contingency (N-1) analysis repeats the power flow with each element out of service. Short-circuit, stability and dynamic studies cover fault levels and the seconds after a disturbance [25], and optimal power flow (OPF) finds the least-cost dispatch within network limits. Open-source solvers such as MATPOWER [72], pandapower [54] and PowerModels.jl [5] implement these analyses, and several benchmarks take their answer keys from them. For an engineer, and for an agent, the difficulty lies less in the computation than in choosing which studies to run on which network state, and in reading the results against the rules. 

load, dispatch and topology variation (PF∆[46], solved with Ipopt [59]) and natural-language OPF modifications (ProOPF [51]). Older datasets supply independent references, among them PGLib-OPF [2], OPFData [31], Grid2Op/L2RPN and RL2Grid [6, 33, 34] and the IEEE PES small-signal benchmark systems [4]. 

# **3 System Overview** 

## **3.1 Design principles** 

- **P1. Evidence before answers.** Every answer and finding is anchored to a passage in a source document or in the applicant’s submission. 

- **P2. Computation by established solvers.** The model chooses, sequences and interprets studies, and solvers produce every number. 

- **P3. Human decision authority.** Agents prepare the work and people decide. Agent verdicts sit beside human verdicts, decisions need sign-off by named people, and studies pause at decision points [40]. 

**Language models for power systems.** Language models have only recently been applied to this work. Surveys map the opportunities and risks [11, 16, 32]. Agent systems include multi-agent simulation frameworks [21], agents for analysis and operations [23, 62], an agent for connection impact assessment [49] and tool servers for power-system software [43]. Several are evaluated on task sets of their own [23, 62], which makes them hard to compare. Shared benchmarks have followed. They cover power-flow questions (PFBench [50]), agentic studies (PowerAgentBench [35], PSAB [56]), natural-language study tasks (PowerCodeBench [64]), power flow under 

## **3.2 The Grid Ontology** 

**Knowledge base.** The Grid Ontology holds the legislation, grid codes, standards and process documents that an application is checked against. The GB corpus in our experiments has 27 documents with 6,347 pages, including their figures and tables. 

**Grounded answers.** An agent answers questions and reviews applications from this knowledge base. It answers only from evidence it has found and must cite the passages its answer relies on. 

3


<!-- page 4 -->

**Memory.** Documents state the rules, and memory holds what the agents learn while applying them. Following the CoALA taxonomy [53], it holds three kinds (Table 1). 

**Table 1: Memory carries what the agents learn beyond the documents.** The three kinds held in the Grid Ontology. 

|Kind|Holds|
|---|---|
|Semantic|Facts about the domain, an operator and its<br>projects, and rules for responding|
|Procedural|Skills, which are written methods for a task<br>such as a connection study|
|Episodic|Experiences and the lessons drawn from them|



**Self-evolving memory.** All three kinds of memory change with use. Lessons drawn from recent work [41, 70] become experiences, and facts, rules and skills are added or revised as the work shows what the agents lack. A change that would affect other people takes effect only after a person approves it. The agents therefore improve with use while every shared change stays visible and attributable, which is principle P3 applied to learning. 

## **3.3 Grid Studio** 

**Studies through established solvers.** Grid Studio gives the agent power-system studies as tools. The agent chooses which studies to run and on which network state, and reads the results, while established solvers compute every number (P2). 

**Reinforcement planning.** When a project needs reinforcement, the agent calls an optimiser that proposes the least-cost package of works, in the spirit of transmission expansion planning [26]. Section 5.2 evaluates it. 

# **4 Experimental Setup** 

## **4.1 Benchmarks** 

Table 2 lists the benchmarks and what each tests. We also give every task a _depth_ , how much work the system must do to reach the answer, in the spirit of PowerCodeBench’s difficulty levels [64]. Figures 3 and 4 place each benchmark on this scale, and Table 6 in Appendix A gives an example of each step. 

**Regulatory knowledge.** The GB Regulation Set is our own set of 45 questions on GB grid regulation, asked of the 27 documents of the GB corpus (6,347 pages). An R1 question is answered by one passage, an R2 question by a figure or table, and an R3 question only by combining passages. We built it evidence first. Passages 



<!-- Start of picture text -->
R1 R2 R3 R4<br>GB Regulation Set 25 14 6<br>ERC 41 8<br>LegalBench-RAG 50<br>ViDoRe V3 904 1,312 203<br><!-- End of picture text -->

**Figure 3: How deep each regulatory benchmark goes.** Rows are the Grid Ontology’s benchmarks and columns the steps of depth. An R1 question is answered by one passage, R2 by a figure or table, R3 by combining passages and R4 by the exact span of a clause. Each cell counts the questions at that step, and darker cells are deeper. ERC is the Enterprise RAG Challenge, and its 51 questions with no answer in the reports are not shown. 



<!-- Start of picture text -->
L1 L2 L3 L4 L5 Buses<br>PowerAgentBench-SS 15<br>PSAB 19<br>PGLib-OPF 18<br>PowerCodeBench 13 205 134<br>PFBench 18<br>RL2Grid 2 5<br>PF ∆ 71<br>ProOPF-B 19<br>10 100 1k 10k<br><!-- End of picture text -->

**Figure 4: How deep each power-system benchmark goes.** Rows are Grid Studio’s benchmarks and columns the steps of depth. An L1 task runs one study on the published network, L2 first applies the changes it states, L3 must first find what to change, L4 rebuilds a published operating point and L5 turns a written requirement into a changed optimisation problem. Cells count tasks as in Figure 3, and each bar on the right spans the network sizes a benchmark uses. 

and figures are sampled from the corpus, a model writes a question from each, questions the evidence does not support or that need no evidence are discarded, and the domain owner approves the rest (Appendix D). The Enterprise RAG Challenge asks similar questions of 100 company annual reports (14,454 pages), and about half have no answer in the reports, so the system must also recognise when there is none. LegalBench-RAG (R4) asks for the exact span of a clause in a long contract, and we use a fixed sample of 50 questions from its CUAD subset [15], whose 462 contracts are plain text without pages (about 3.9 million words). ViDoRe V3 [30] asks 2,419 questions of 19,252 pages of visually rich documents in English and French, and scores the ranking of the pages a system returns. Its own question labels give each question a depth (Appendix D). 

**Power-system engineering.** Eight benchmark families give 519 tasks on networks of 4 to 9,241 buses. An L1 task runs one study on the network as published, an L2 task first applies stated changes, and an L3 task 

4


<!-- page 5 -->

**Table 2: The benchmarks.** Who developed each one, what it tests and how deep it goes, in the steps of Figures 3 and 4. OPF is optimal power flow, the least-cost dispatch within network limits.<sup>_†_</sup> Adapted to a network-study interface, so its answer key comes from a reference solver (Appendix D). 

|Benchmark|Developed by|What it tests|Depth|Items|
|---|---|---|---|---|
|_Regulatory knowledge_<br>_(Grid Ontology)_|||||
|GB Regulation Set|Grid Agents (this work)|Questions on GB grid regulation|R1–R3|45|
|Enterprise RAG Challenge [55]|TimeToAct Austria|Questions on annual reports|R1–R3|100|
|LegalBench-RAG [42]|ZeroEntropy, UC Berkeley (CUAD)|Exact clause spans in contracts|R4|50|
|ViDoRe V3 [30]|Illuin Technology, NVIDIA|Pages of visually rich documents|R1–R3|2,419|
|_Power-system engineering_<br>_(Grid Studio)_<br>|||||
|PowerAgentBench-SS<sup>_†_ </sup>[35]<br>|NTUA, Harvard and others|Single-outage screening (N-1)|L1|15|
|PSAB<sup>_†_ </sup>[56]|Pskov State University|Overload, voltage, outage checks|L1|19|
|PGLib-OPF [2]|IEEE PES Task Force|Power flow and OPF|L1|18|
|PowerCodeBench [64]|University of Exeter|Study requests in plain English<br>l|L1–L3|352|
|PFBench [50]<br>|Kansas State University|Power flow after load changes|L2|18|
|RL2Grid<sup>_†_ </sup>[33]|MIT, RTE, National Grid ESO|Switching after double outages|L2–L3|7|
|PF∆[46]|MIT|Rebuilding a published grid state|L4|71|
|ProOPF-B [51]|Peking U., Zhejiang U.|OPF changes from a written brief|L5|19|



must first find what to change, such as the most heavily loaded line. An L4 task rebuilds a published operating point of 20 to 261 values, and an L5 task turns a written requirement into a changed optimisation problem. None poses a multi-stage study, so Section 5.2 measures one separately. 

own solution. Appendix B defines each term, describes how the work of each kind of system is verified, and gives the reasons for the weights. 

# **4.2 Evaluation metrics** 

**Regulatory knowledge.** We score the evidence each system _cites_ . A cited item matches a gold anchor if it comes from the same document and overlaps the anchor’s span, lies within one page of it, or is the anchored figure. We report recall, precision, MRR, nDCG@10 [19] and hit rate, and a model judge marks each answer against the gold answer [71]. LegalBench-RAG and the Enterprise RAG Challenge keep their own metrics and scoring script, and ViDoRe V3 its board’s nDCG@10, averaged over its sets. 

**Power-system engineering.** A correct number can come from memory, a lucky guess or a study on the wrong grid state, so we grade the work behind each answer as well as the answer. A task is a _strict pass_ only if its answer is within the benchmark’s tolerance and the system’s recorded work shows that the required study ran on the required grid state. With numeric closeness _c_ ¯, answer accuracy _A_ and strict pass rate _P_ , each taken over all _n_ tasks, the end-to-end score is 



<!-- Start of picture text -->
E = 0 . 25 ¯ c + 0 . 25  A + 0 . 5  P. (1)<br><!-- End of picture text -->

A base model, which answers without tools, gets the network as text in its prompt and reports the solved states its answer rests on, which we check against our 

# **4.3 Evaluation method** 

**Systems compared.** On the regulatory benchmarks we compare the Grid Ontology with a general coding agent (Claude Code) that has the corpus as files and its own file and shell tools, with one-shot retrieval pipelines that search once and answer from their top eight results, and on the Enterprise RAG Challenge and ViDoRe V3 with their published entries. On the power-system benchmarks we compare Grid Studio with two coding agents as shipped, Claude Code and Codex CLI on GPT-6.1 sol, each with a shell, Python and the network as a file. We also compare it with Power-Agent [43, 44], which installs PowerMCP’s pandapower tools and PowerSkills’ playbooks into Claude Code, and with eleven base models, which answer without tools from the network given as text, among them the frontier models GPT-6.1 sol and Fable 5.1. Claude Code and Power-Agent run on the same model as our agents, and Power-Agent uses its tools and playbooks as their authors publish them. We also time each system’s agent work, the time it spends on model turns and tool runs. Appendix D gives the evaluation protocol. 

5


<!-- page 6 -->

**Table 3: Grid Ontology results on four retrieval benchmarks.** (a) Every system uses the same model and is scored on the evidence it cites. F1 is shown with its 95% confidence interval, and a dash marks a system not run. (b) The top published entries on each public leaderboard, by the leaderboard’s own score (out of 150 for the Enterprise RAG Challenge, and _×_ 100 for ViDoRe V3). Best in **bold** . 

|_(a) Same model_||G|B Regula|tion Set||Le|galBench-|RAG|
|---|---|---|---|---|---|---|---|---|
|System|Recall_↑_|nDCG_↑_|MRR_↑_|Hit rate_↑_|Answer acc._↑_|Precision_↑_|Recall_↑_|F1_↑_|
|Grid Ontology|**0.967**|**0.945**|**0.944**|**0.978**|**1.000**|**0.980**|0.980|**0.980**_±_0_._030|
|Claude Code (file tools)|0.856|0.863|0.878|0.889|**1.000**|0.900|0.900|0.900_±_0_._080|
|Vector + reranker [24, 37, 47]|0.922|0.917|0.933|0.956|0.889|0.820|**1.000**|0.869_±_0_._057|
|PageIndex [58]|0.400|0.389|0.378|0.400|0.444|0.762|0.920|0.799_±_0_._090|
|MS GraphRAG [7]|0.344|0.347|0.367|0.378|0.333|–|–|–|
|Recursive LM [69]|–|–|–|–|–|0.860|0.860|0.860_±_0_._100|
|_(b) Top published entries_|||||||||
|Enterprise RAG Challenge||Score_↑_||ViDoRe V3||||nDCG@10_↑_|
|Grid Ontology||**124.5**||Grid Ontol|ogy|||**70.23**|
|Ilia Ris (1st)||123.7||VisAgentR|et (1st)|||70.01|
|Emil Shagiev||121.6||NeMo Retr|iever, agentic|||69.22|
|Dmitry Buykin||117.5||EVIE-4.5B|+ JEV-27B-VL|||68.25|
|Sergey Nikonov||116.4||jina-embed|dings-v4 + zeran|k-2||65.62|



# **5 Results** 

## **5.1 Grid Ontology** 

**Takeaway:** The Grid Ontology cites the right regulatory evidence more often than any other system (0.967 recall). It also leads on LegalBench-RAG (0.980 F1) and ranks first among published entries on the Enterprise RAG Challenge and ViDoRe V3. 

Table 3 gives the results on all four benchmarks. On the GB Regulation Set and LegalBench-RAG, every system answers with the same model, so the differences come from the evidence each finds and cites. On the Enterprise RAG Challenge and ViDoRe V3, the Grid Ontology is first on the public board. 

**GB Regulation Set.** Both agents answer every question correctly, so the evidence they cite is what separates them. The Grid Ontology cites the right evidence for more questions than Claude Code (recall 0.967 against 0.856), and the gap is widest on single-passage questions that ask for a number (1.000 against 0.625). This matters in review, where a correct answer that cites the wrong passage still has to be checked by hand. The retrieval pipelines answer fewer questions correctly. Vector retrieval with a reranker comes closest, while PageIndex and GraphRAG find the evidence for fewer than half of the questions. Example 1 in Appendix A shows one question. 

**LegalBench-RAG.** The Grid Ontology reaches an F1 of 0.980, ahead of every baseline. It cites one contract per question, while the retrieval pipelines cite up to five, so the right contract is usually among theirs but 

so are wrong ones. Its one miss is a contract filed twice, where it cited the signed copy and the answer key names the unsigned draft. At the benchmark’s stricter clause level, its lead over the pipelines is an order of magnitude (Appendix E). 

**Enterprise RAG Challenge.** The challenge’s own script scores both the exact answers and the pages they cite, out of 150 [55]. The Grid Ontology scores 124.5 against 123.7 for the best published entry, and it correctly declines 45 of the 51 questions that the reports cannot answer. 

**ViDoRe V3.** The board scores the first ten pages returned for each English question by nDCG@10, averaged over eight public sets. The Grid Ontology scores 70.23 against 70.01 for the best published pipeline and leads on four of the eight sets (Appendix F). 

## **5.2 Grid Studio** 

**Takeaway:** Grid Studio scores highest, 99.9% with verified work on 516 of the 519 tasks, and it is the fastest system, at a median of 13.9 s of agent work per task. Both leads are statistically significant. With optimisation in the loop, its reinforcement packages are up to 67% cheaper. 

Table 4 gives the mean end-to-end score over the eight benchmark families, and Table 8 gives each family. Grid Studio scores 99.9%, with 100% on seven of the eight families and 99.2% on PowerCodeBench, statistically significantly above every other system. Codex CLI scores 99.4%, but 19 of its 23 misses are on networks above 2,000 buses, and it takes up to 55% longer per task. 

6


<!-- page 7 -->

**Table 4: End-to-end score and agent work time on the eight power-system benchmark families (519 tasks).** Mean _E_ (Eq. 1) and median time per task, _±_ the half-width of the 95% confidence interval. _†_ Statistically significantly better than every other system ( _p <_ 0 _._ 001, paired tests on the same tasks, Holm-corrected). 

|System|Mean _E_ (%)_↑_|Median time (s)_↓_|
|---|---|---|
|Grid Studio|**99**_._**9**_±_0.1<sup>_†_</sup>|**13**_._**9**_±_0.4<sup>_†_</sup>|
|Codex CLI|99_._4_±_0.3|21_._6_±_0.7|
|Claude Code|85_._4_±_3.2|22_._0_±_0.9|
|Power-Agent|99_._4_±_0.3|16_._8_±_0.5|
|GPT-6.1 sol, base model|40_._8_±_2.9|58_._2_±_10.6|
|Fable 5.1, base model|28_._3_±_3.0|162_._5_±_39.6|



Power-Agent also scores 99.4%, and Grid Studio scores higher on 13 tasks and lower on one, with Grid Studio’s time 0.75 of Power-Agent’s on the same task. Claude Code scores 85.4%. 

**Base models.** The best base model, GPT-6.1 sol, answers 250 of the 519 tasks (48%) correctly. Given the network as text, the strongest base models solve small power flows by hand, but none has its work verified on a network of more than 39 buses. None answers more than 30% of the PF∆tasks, where a published operating point must be solved, or more than two of the seven RL2Grid tasks, where switching actions must be compared, and none scores above 41% end to end. 

**Score against time.** Figure 1 sets each score against the agent work time. Grid Studio needs a median of 13.9 s per task, against at most 21.6 s for Codex CLI and 22.0 s for Claude Code, so it scores highest in the least time. Reading the network and writing out the solved states takes the base models a median of 20 s to almost 3 minutes per task, so every other system is both slower than Grid Studio and lower scoring. More time does not close the gap: GPT-6.1 sol and Fable 5.1 spend about 1 and 3 minutes per task and still stay below 41%. 

**Domain tools must reach the study.** Power-Agent installs PowerMCP’s pandapower tools and PowerSkills’ playbooks into Claude Code, on the same model as Grid Studio, and comes close to Grid Studio’s score. Its PowerMCP tools were called on only 46 of the 519 tasks and settled 16 on their own. The other 503 needed the agent’s own pandapower code, and 473 never called PowerMCP at all, while a PowerSkills playbook was followed in 409. Its results therefore come mostly from code the agent writes for each task rather than from the domain tools. Grid Studio’s tools reach every study the benchmarks ask for, which is what makes its work both verifiable and fast. 

**Table 5: Cost of the reinforcement packages.** Cost in US$ million, the mean of two runs, of the package the agent designed alone and with the optimiser. 

|Network|Project|Agent<br>alone_↓_|With<br>optimiser_↓_|
|---|---|---|---|
|30-bus|400 MW|151.0|**81.6**|
|118-bus|500 MW|173.3|**71.1**|
|118-bus|700 MW|395.3|**166.4**|
|118-bus, three cases|700 MW|481.0|**160.4**|
|2,000-bus|1,100 MW|512.7|**344.5**|



**Real studies are larger.** The benchmark networks have at most 9,241 buses. An operator’s planning model can run to tens of thousands of buses, and a connection study chains many studies, from screening the options to designing reinforcement. The baselines already fall short at the top of the benchmarks. Of the 109 tasks on networks above 2,000 buses, Power-Agent passes 106, Codex CLI 90 and Claude Code 74, against 108 for Grid Studio, and the base models pass none. Grid Studio takes its numbers from established solvers rather than from code written for each task, and its work can be checked at every step, which makes it the better design for real planning studies. 

**Optimisation makes reinforcement cheaper.** The benchmarks pose single studies, so we tested the reinforcement stage of a connection study separately. In five studies on networks of 30, 118 and 2,000 buses, the last the synthetic Texas grid ACTIVSg2000 [3], the agent designed the package twice on its own and twice with the optimiser, using the same model and catalogue of priced reinforcement works (Table 5). Both approaches cleared every overload the projects caused, as an independent AC N-1 check of each final network confirms. The optimiser’s packages were 33–67% cheaper on average. 

# **6 Conclusion** 

Grid Agents is built on three principles. Answers rest on cited evidence, numbers come from established solvers, and engineers make the decisions. The Grid Ontology cites the right regulatory evidence more often than a general coding agent or retrieval pipelines, leads on LegalBench-RAG, and ranks first on the public leaderboards of the Enterprise RAG Challenge and ViDoRe V3. On 519 tasks from eight published power-system benchmark families, Grid Studio scores highest and needs the least agent work time, both by a statistically significant margin. With an optimiser in the loop, its reinforcement packages cost 33–67% less on average than those the agent designs alone. 

7


<!-- page 8 -->

# **Acknowledgements** 

We thank the authors of every benchmark used here for releasing their questions, answer keys and reference solutions, and TimeToAct Austria, Illuin Technology and NVIDIA for running the public leaderboards of the Enterprise RAG Challenge and ViDoRe V3. The GB network models come from the University of Edinburgh Power Systems Test Case Archive, and Manolis Belivanis of the University of Strathclyde provided the reduced GB model. The synthetic Texas grid comes from the Texas A&M Electric Grid Test Case Repository, and the PGLib-OPF cases from the IEEE PES Task Force on Benchmarks for Validation of Emerging Power System Algorithms.
