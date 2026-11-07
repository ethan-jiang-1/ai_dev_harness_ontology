---
source: 2610.01618-agents-are-systems.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# AGENTS ARE SYSTEMS, NOT MODELS: RETHINKING AGENTIC EVALUATION · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

AGENTS ARE SYSTEMS, NOT MODELS: RETHINKING AGENTIC EVALUATION 

**Luis Wiedmann**<sup>**1,2**</sup> **, Leander Girrbach**<sup>**1,2**</sup> **, Cordelia Schmid**<sup>**3**</sup> **, Zeynep Akata**<sup>**1,2**</sup> 1Technical University of Munich, MCML 2Helmholtz Munich 3Inria, École normale supérieure, CNRS, PSL Research University 

# ABSTRACT 

Agent evaluations increasingly go beyond a single success rate, reporting metrics such as cost, consistency, and robustness. Yet they typically treat the agent itself as fixed. In practice, an agent is a configurable system: users decide what to tell it, how long to let it run, and which model to use, and each of these choices can change how well and how consistently it performs. We study these choices on a new benchmark of four scientific tasks, where a coding agent must find and correctly operate a published specialist model. We investigate five parts of the agent’s configuration: task information, reasoning, self-verification, time budget, and backbone model. We find substantial run-to-run variability, with approximately 54% of the outcome variance coming from repeating the same configuration rather than changing it. Across configurations, the information provided to the agent has the largest effect, exceeding both time budget and model size, while also reducing cost and improving calibration. Configuration choices also interact: additional time helps only when the agent has sufficient information or a capable enough model to use it. Finally, a trajectory-based taxonomy of agent behavior reveals that prompting an agent to verify its answer has little effect on its verification behavior, whereas providing a dedicated verification tool changes that behavior substantially. These results suggest that agents should be evaluated as configurable systems themselves, and that some desired behaviors are more effectively implemented in the system than requested through prompting. We release the benchmark and more than 18,000 agent trajectories<sup>1</sup> . 

# 1 INTRODUCTION 

When agents are used to solve complex tasks, we care not only about whether they succeed, but also about how reliably they do so, and about which parts of their configuration determine capability and reliability. Recent work broadens what is measured about an agent: Kapoor et al. (2025) argue that evaluations should not focus only on performance, but also account for cost and comparability between methods. Rabanser et al. (2026) show that capability gains do not automatically translate into reliability gains, and argue for a decomposition of agent reliability into consistency, robustness, predictability, and safety. It remains less clear how an agent’s configuration itself shapes these measurements: which of its parts drive capability and reliability, and how these parts interact. 

Scientific workflows are a natural setting to study this. Many scientific tasks rely on specialist models (trained for a specific scientific domain or task) that a general-purpose LLM cannot directly replace, so an agent cannot solve them from its own knowledge. Instead, it has to find the right model, prepare the input data, and write the code to run it, and each of these steps can be affected by how the agent is configured. Published results of these specialist models further provide reference scores against which the agent’s outcome can be checked. One example is estimating redshift from galaxy images. Fine-tuning a multimodal LLM to process galaxy images would be costly, but specialist models for this task already exist, and an agent can use them instead. We are interested in _how reliably agents can use such specialist models_ in scientific workflows, and _what contributes to their effective use_ . 

> 1https://github.com/lusxvr/rethinking-agent-evaluation 

1


<!-- page 2 -->

In this paper, we use the following terms: the _model_ (or _backbone_ ) is the LLM itself, with no memory across calls and no ability to act on its own. An _agent_ wraps a model in a loop that lets it act repeatedly: read the current state, decide on an action, execute it, observe the result, and decide again. The agent’s _harness_ is the infrastructure that runs this loop: it dispatches tool calls and manages the model’s context at each step, including memory and compression. Fundamentally, an agent is a _system_ consisting of a model and a harness (de Macedo, 2026; Paniego & Roy Gosthipaty, 2026), which is reflected in recent implementations of production coding agents such as Codex or Claude Code (Lopopolo, 2026; Young, 2025; Shi et al., 2026). 

We systematically evaluate how an agent’s configuration affects how well it uses specialist models to solve scientific tasks. Concretely, we study five axes of the agent’s configuration: (1) what _information_ the agent is given; (2) whether the agent generates _reasoning_ and keeps it across steps; (3) how strongly the agent is asked to _verify_ its own answer; (4) how much runtime _budget_ the agent has to solve the task; and (5) how strong the agent’s backbone _model_ is. By varying these axes on a new benchmark of four scientific tasks from astrophysics and genomics, we measure how each one contributes to the agent’s outcome and reliability, and how they interact. In each task, the agent’s outcome is compared against the specialist model on an evaluation from its original paper. 

We find that agent outcomes are noisy: about 54% of the score variance among genuine attempts is run-to-run noise rather than an effect of the configuration. In our main experiments, the information given to the agent has the largest effect among the axes, outranking both the budget and the backbone model. The effect of one axis can also depend on another: additional budget mainly improves the score when the agent already has enough information to use it productively. Finally, an analysis of the agent’s behavior shows that some behaviors, such as self-verification, are hard for the user to influence directly through prompting and should instead be shaped by the system’s design. 

In summary, our contributions are as follows: **(1)** We systematically study how the axes of an agent’s configuration influence its outcome and reliability, finding that information outranks model and budget. **(2)** We create an AI-for-Science (AI4S) benchmark in which the agent has to use specialist models under controlled conditions. We release the benchmark and 18,240 agent trajectories with their produced artifacts, enabling reproducibility and further analysis of agent behavior. **(3)** We derive a taxonomy of agent behavior from these trajectories and use it to show that some behaviors are hard for the user to influence directly and should instead be shaped by the system’s design. 

# 2 RELATED WORK 

**AI for Science.** Recent capability gains in machine learning methods and foundation models enable a broad range of applications in scientific fields outside classical computer science (Jumper et al., 2021; Wang et al., 2023). Furthermore, the transition from isolated models to agents has intensified the interest in AI as a scientific companion or as a scientist itself (Wei et al., 2025; Gridach et al., 2025; Xin et al., 2025; Lu et al., 2026). We organize the field into two focus areas: _(re-)implementation_ (Starace et al., 2025) and _discovery_ (Majumder et al., 2025). Works on (re-)implementation reuse scientific publications or their codebase, and test how well agents can reproduce the findings, methods, or implementations (Wang et al., 2026; Chen et al., 2025; Kim et al., 2026; Bogin et al., 2024; Falck et al., 2026; Shen et al., 2026). In parallel, a growing set of works evaluates agents’ ability to produce genuinely novel discoveries (Kirgis et al., 2026; Artiles et al., 2026; Si et al., 2025; Zahavy, 2026; Si et al., 2026; Messeri & Crockett, 2024). Our work is closer to the first area, i.e., (re-)implementation of existing work. We propose a coding-focused benchmark that enables the agent to freely explore, test, and write code to operate given specialist models, while its outcome is judged against their published performance. This makes the environment controlled and repeatable, so that the agent’s configuration can be varied systematically and outcomes can be scored without manual verification. 

**Agents and Their Evaluation.** As agents (Wooldridge & Jennings, 1995; Yao et al., 2023) become more capable, evaluating their performance (Chang et al., 2024) becomes more challenging. Their ability to tackle complex, long-horizon tasks (Kwa et al., 2025), potentially through multiple instances (Cemri et al., 2026), makes failures and capabilities harder to accurately estimate and understand, which makes a systematic study necessary (Zhu et al., 2025; Miller, 2024). Multiple works agree that a single success metric is insufficient, and that capabilities have to be judged both in the context of their task and in terms of their cost and reliability, broadening what is measured about an 

2


<!-- page 3 -->

<!-- Start of picture text -->
CONFIGURATION AXES SCIENTIFIC MODELS & TASKS<br>AGENTIC SYSTEM Astrophysics<br>Information<br>None  →  Identity  →  Interface  →  Protocol GPU Sandbox Redshift-Estimation<br>Harness AstroCLIP pre-processing<br>Reasoning<br>Act-Only  →  Think-Act  →  ReAct Backbone MMLU-Astronomy<br>AstroSage-8B declining<br>Verification CONFIG Model TASK &<br>None  →  Asked  →  Reported  →  Binding WEIGHTS Genomics<br>Budget Reason Act Result Promoter-Prediction<br>Short  →  Medium  →  Long DNABERT-2 fine-tuning<br>read/write_file run_bash web_fetch<br>Model RNA-Folding<br>Small  →  Medium  →  Large RiNALMo post-processing<br>EVALUATION<br>Performance Reliability Behavior<br><!-- End of picture text -->

Figure 1: Architecture of our agentic AI4S benchmark. The agent (center) has access to different specialist models and is evaluated against their published performance (right). By varying the axes of the agent’s configuration within the same task (left), we can systematically study its performance, reliability, and behavior under controlled, repeatable conditions (bottom). 

agent (Liang et al., 2023; Kapoor et al., 2026; 2025; Rabanser et al., 2026). We complement these works by treating the agent as a configurable system rather than a fixed model, and study how its configuration shapes these measurements. 

# 3 AGENT EVALUATION AND BENCHMARK TASKS 

In our setting, a single agent has access to a collection of specialist models, including their weights and pre-built environments (i.e., the libraries and dependencies required to run them). Given a task, the agent has to determine which model to use (if any) and then correctly operate it by writing its own code. In the following, we describe how our agents and tasks are implemented (see Fig. 1 for an overview). 

## 3.1 MODULAR AGENT IMPLEMENTATION FOR SCIENTIFIC WORKFLOWS 

The agent runs in a sandbox with access to a single GPU and a pre-built coding environment. The sandbox contains the weights and environments of all specialist models, each with a short README that names the model and links to its paper and code. Importantly, the specialist models are not available through a dedicated tool call, but have to be operated by the agent the same way a human scientist would. The agent receives a simple system prompt that describes it as an “autonomous research agent” (Section A.16). It is then given the task description, the available data, and the required solution format. It can read and write files, fetch web pages, and run terminal commands, and can therefore write and execute its own code. 

In each step, the agent’s backbone model sees the conversation so far, including the task description, all outputs, and every tool result. Then, it either outputs plain text or calls one of the available tools (Section A.2). A tool’s output is appended to the conversation before the loop repeats, so the agent always sees the outcome of its last action before choosing its next one. The loop ends when the agent calls a finish tool with its answer, or when the budget runs out. In its full form, this loop follows Yao et al. (2023), interleaving reasoning about what to do with the actions taken. 

For our main analysis, we select and systematically vary five axes, each targeting a distinct factor known to shape behavior. What agents are told determines what they still need to explore or retrieve themselves (Jimenez et al., 2024). Keeping reasoning in context is central to the performance gains of Yao et al. (2023), and agents that check their own work tend to succeed more often (Shinn et al., 2023; Madaan et al., 2023). Giving agents more time lets them solve harder problems, though with diminishing returns (Wijk et al., 2025; Chan et al., 2025). Finally, the capability of the backbone model should be evaluated separately from the harness built around it (Kapoor et al., 2025). To- 

3


<!-- page 4 -->

gether, the five axes cover what the agent knows, how it deliberates, whether it checks itself, how much time it has, and how capable it is, all of which can influence both outcome and reliability. We describe the axes and their levels below. For _Information_ and _Verification_ , each level adds to the previous one (marked with +). 

**Information.** This axis controls how much information the agent receives in addition to the task description: (i) _none_ : no additional information; (ii) _identity_ : which specialist model is associated with the task; (iii) _interface_ : + how to load and call the model; (iv) _protocol_ : + a full recipe for this specific task. 

**Reasoning.** This axis controls whether the agent generates reasoning and whether this reasoning stays in context for later steps: (i) _act-only_ : no reasoning is generated; (ii) _think-act_ : reasoning is generated in each step but discarded before the next; (iii) _ReAct_ : reasoning is generated and kept in context across steps. 

**Verification.** This axis controls how strongly the prompt asks the agent to verify its own answer: (i) _none_ : no instruction to verify; (ii) _asked_ : the agent is asked to verify its answer; (iii) _reported_ : + the agent must state the score it expects and the evidence from its verification; (iv) _binding_ : + the agent is told not to submit unless its own verification is convincing. 

**Budget.** This axis controls how much wall-clock time the agent has to solve the task. We limit runtime rather than the number of steps, because the duration of a step varies widely (from a quick file read to fine-tuning a specialist model): (i) _short_ : 5 min; (ii) _medium_ : 10 min; (iii) _long_ : 20 min. 

**Model.** This axis controls the size, and therefore the capability, of the agent’s backbone model: (i) _small_ : Qwen3.5-35B-A3B; (ii) _medium_ : Qwen3.5-122B-A10B; (iii) _large_ : Qwen3.5-397B-A17B. All models are FP8-quantized due to resource limitations. 

# 3.2 BENCHMARK TASKS FROM ASTROPHYSICS AND GENOMICS 

To create the tasks, we identify published scientific works that propose a new specialist model. For each, we reproduce the evaluation from the original publication ourselves, reducing its size where necessary so that it can be completed within the shortest budget (e.g., by downsampling the evaluation dataset). The score of the specialist model in our reproduction is the task’s reference score. Each task tests, in a controlled setup, the agent’s ability to understand, reproduce, and use prior work to complete a scientific workflow. We include the following tasks (Table 1 and Section A.17): 

**redshift-estimation.** The agent has to estimate the cosmological redshift of galaxies directly from multi-band photometric images. Given 20 galaxy image cutouts and a labeled reference set, it has to use the pretrained AstroCLIP model (Parker et al., 2024) to predict continuous redshift values. Performance is measured by _R_<sup>2</sup> against spectroscopic ground-truth measurements. 

**mmlu-astronomy.** This task consists of 152 multiple-choice questions on topics from stellar evolution to cosmology. The specialist model, AstroSage-8B (de Haan et al., 2025), is weaker than the agent’s backbone model, so the task tests whether the agent recognizes this and answers the questions itself instead of relying on the specialist. Performance is measured by accuracy. 

**promoter-prediction.** The agent has to classify 613 human DNA sequences as promoter or nonpromoter regions. To do so, it has to locate, pre-process, fine-tune, and operate DNABERT-2 (Zhou et al., 2024). Performance is measured by the Matthews correlation coefficient (MCC). 

**rna-folding.** The agent has to predict the secondary structures of 300 RNA sequences. It has to use the pretrained RiNALMo model (Peni´c et al., 2025) to predict contacts between nucleotide pairs, and then apply a post-processing procedure to obtain valid secondary structures. Performance is measured by the structure-level pairing _F_ 1 score. 

We distinguish two regimes: a task is GAP_POSITIVE if the specialist’s reference score is higher than the score of the backbone model alone ( _R > B_ ), and GAP_NEGATIVE if it is lower. The four tasks each stress a different part of using a specialist model correctly. redshift-estimation and rna-folding reward finding a stronger specialist and using it without fine-tuning, but the difficult step differs (pre-processing input images before embedding them, and post-processing the predicted contacts into valid structures). promoter-prediction instead requires fine-tuning DNABERT-2, because its pretrained checkpoint is not trained for promoter classification. mmlu-astronomy is 

4


<!-- page 5 -->

Table 1: The four tasks of the benchmark, together with one example instance per task. Each task belongs to one of two domains and one of two regimes, and focuses on a different aspect of the specialist models’ operation. 

||redshift-<br>estimation|mmlu- astron|omy|prom|oter- predicti|on<br>rna-f|olding|
|---|---|---|---|---|---|---|---|
|Domain|Astrophysics|Astrophysics||Gen|omics|Genom|ics|
|Size<br>Metric|20 galaxy images<br>_R_<sup>2</sup>|152 question<br>Accuracy|s|613<br>MC|DNA sequences<br>C|300 R<br>_F_1|NA sequences|
|Specialist<br>Challenge|AstroCLIP<br>Pre-processing|AstroSage-8<br>Declining|B|DN<br>Fine|ABERT-2<br>-tuning|RiNA<br>Post-p|LMo<br>rocessing|
|Regime|GAP_POSITIVE|GAP_NEGAT|IVE|GAP|_POSITIVE|GAP_P|OSITIVE|
|**red**|**shift-estimation**|**mmlu-astronomy**||**promoter-p**|**rediction**|**rn**|**a-folding**|
|**Expe**|**cted Answer:**0.2656<br>For each galaxy image<br>below, estimate its cosmic<br>redshift. Respond with a<br>single decimal number per<br>galaxy.|What element is most<br>common among the Jovian<br>Planets?<br>A: Hydrogen<br>B: Helium<br>C: Carbon<br>D: Oxygen<br>**Expected Answer:**A|**DNA sequen**<br>GCAATAAAAG<br>ATAGTGCATG<br>ACTTCTAGGG<br>GCATGTACAC|**ce, 70bp:**<br>GCTTAGCCAC<br>CAGAGCTCTG<br>CAAAACATAA<br>**Expected A**|Determine whether it is<br>a functional core<br>promoter region or not.<br>Respond with 1 if it is,<br>0 if it is not.<br>**nswer:**0|**RNA sequence,**<br>**37nt:**<br>GUUUCAAUCC<br>UCUACGAGGC<br>UGACGGGGUU<br>UGCAACG<br>**Expected Answer:**|Predict the secondary<br>structure (which bases<br>pair with which) in<br>extended dot-bracket<br>notation.<br> .((.(((.(( ((............)))).) )).))..|



GAP_NEGATIVE: its specialist model has been surpassed by general-purpose LLMs and is weaker than the backbone, so the correct behavior is to decline the specialist rather than use it. With two domains, two regimes, and four different demands on the specialist model, no single fixed strategy (always use the model, or never use it) performs well across all four tasks. To succeed, the agent has to investigate and judge each specialist’s capabilities and work out its specific operating details. 

# 4 EXPERIMENTS AND RESULTS 

## 4.1 EXPERIMENTAL SETUP AND EVALUATION METRICS 

To evaluate the agent, we use three quantities. _B_ is the score of the backbone model alone, i.e., the LLM answering the task directly, without an agent or specialist model. _R_ is the reference score of the specialist model in our reproduction. _S_ is the agent’s score on the task. Our main metric is the share of the gap between backbone and specialist that the agent closes (GAP_CLOSED): 



<!-- Start of picture text -->
G = S −B (1)<br>R −B ,<br><!-- End of picture text -->

where _G_ = 0 means no improvement over the backbone alone and _G_ = 1 means the agent matches the specialist’s reference score. It is defined only for GAP_POSITIVE tasks ( _R > B_ ). A run _completes_ if the agent submits an answer with the finish tool before its budget runs out; runs that do not complete receive no score. For every completed run, we also record a binary _hurdle_ indicator _H_ , which states whether the run’s score exceeds the trivial score _T_ of the task by more than a margin _µ_ (Section A.14). _H_ thus captures whether a run makes a genuine attempt at the task, and _G_ captures how close it comes to the reference. For each task, we evaluate the full grid over our axes: 4 ( _Information_ ) _×_ 3 ( _Reasoning_ ) _×_ 4 ( _Verification_ ) _×_ 3 ( _Budget_ ) _×_ 3 ( _Model_ ) = 432 configurations, which we call _cells_ . To measure how much outcomes vary between runs, we repeat every cell 5 times, which gives 2,160 runs per task and 4 _×_ 2 _,_ 160 = 8 _,_ 640 runs in total for our main experiments. 

## 4.2 RESULTS 

The four tasks differ widely in both score and reliability (Table 2). promoter-prediction is the most reliable: almost all of its completed runs clear the hurdle, and repeated runs of the same configuration agree closely. redshift-estimation is by far the least reliable, with more than half of its completed runs failing to clear the hurdle. Unless noted otherwise, the remaining analyses pool the three GAP_POSITIVE tasks, for which _G_ is defined. 

**Agent outcomes are noisy.** Even among genuine attempts, about 54% of the score variance is runto-run noise rather than an effect of the configuration (Fig. 2, right). Without excluding runs that fail the hurdle, the noise appears even larger: differences between configurations then explain only 

5


<!-- page 6 -->

Table 2: Results per task for the main experiments (432 cells _×_ 5 runs). Completion rate is computed over all runs; all other outcome rows are computed over completed runs. _C_ out is computed over cells with at least 3 completed runs. Full breakdown in Table 8.<sup>_†_</sup> Raw scale, not comparable across tasks. 

|||redshift-<br>estimation|mmlu-<br>astronomy|promoter-<br>prediction|rna-<br>folding|
|---|---|---|---|---|---|
|_Runs & Completion_<br># Runs||2,160|2,160|2,160|2,160|
|Completion Rate||76.3%_±_1.8%|95.3%_±_0.9%|89.3%_±_1.3%|61.7%_±_2.0%|
|% Cells that (always / mixed / never) com|plete|54.6 / 40.3 / 5.1|81.9 / 18.1 / 0.0|63.7 / 36.1 / 0.2|21.3 / 72.0 / 6.7|
|_Anchors_||||||
|REFERENCE_R_||0.753|0.671|0.746|0.735|
|BACKBONE_B_||_−_2.701|0.967|_−_0.030|0.000|
|TRIVIAL_T_||0.000|0.250|0.000|0.000|
|MARGIN_µ_||0.250|0.050|0.100|0.100|
|_Outcome_<br>||||||
|Mean Score_S_<sup>_†_</sup>||_−_0.109|0.685|0.625|0.628|
|Mean GAP_CLOSED_G_||0.750|—|0.844|0.854|
|Hurdle Failure Rate||53.8%_±_2.4%|4.7%_±_0.9%|0.5%_±_0.4%|8.7%_±_1.5%|
|Outcome Consistency_C_out||0.727|0.905|0.986|0.825|
|promoter||ICC=39.4%|ICC=46.1%|Figure 2: Out|come variance|
|0.8<br><br>~~redshift~~|1.0<br>|||across cells.|_Left_: mean _G_|
|on<br>rna|0.8<br>ance|||vs. SD per cell|(_≥_3 completed|
|0.6<br>viati|Vari|||runs), with Spe|arman correla-|
|De|0.6<br>tal|||tion. Color: al|l/some/no runs|
|0.4<br>dard|of To|||clear the hur|dle (green/or-|
|Stan|0.4<br>are|||ange/red)._Rig_|_ht_: variance be-|
|0.2<br>|0.2<br>Sh|Between|-Cell (Signal)|tween vs. with|in cells, for all|
|0.0<br>Spearmanρ= -0.79||<br>Within-C|<br>ell (Noise)|completed run<br>|s and hurdle-<br>|
|0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>MeanGper Cell|0.0|All Completed Runs|Clears Hurdle|clearing runs o|nly.|



39.4% of the variance, instead of 46.1%. This noise is not uniform: cells with higher scores have systematically lower variance (Fig. 2, left). Whether a run clears the hurdle at all is also inconsistent across repeated runs, and this differs strongly between tasks: the pooled outcome consistency is 0.86, but only 0.73 for redshift-estimation, whose repeated runs disagree far more often than those of the other tasks (Tables 2 and 8). Even with 5 runs per cell, the 95% confidence interval of a cell’s mean score remains wide (Section A.3). Given the level of run-to-run noise and the uneven completion rates across configurations and tasks, our results reinforce recent calls for more rigorous reporting of completion rates, variance, and confidence intervals alongside raw scores as standard practice in agent evaluations (Kapoor et al., 2025; Rabanser et al., 2026). 

**Information has the largest axis effect.** We rank the five axes by effect size: the range of an axis’s mean _G_ across its levels, divided by the within-cell standard deviation. _Information_ has the largest effect on every task and clearly outranks _Model_ (Table 3). On average, _Reasoning_ matters more than _Budget_ , and _Verification_ ranks last. Because the levels of an axis complete at different rates, a ranking computed over completed runs can be affected by which runs complete. The ranking is nevertheless robust: _Information_ ranks first in at least 99% of bootstrap samples, and a linear model gives the same order (Section A.9). This suggests that a user configuring an agent may benefit more from prioritizing task information than from choosing a stronger backbone model or a larger budget. The effect of one axis can, however, depend on the others, which we examine next. 

**The effect of one axis depends on the others.** Increasing the _Budget_ for the small and medium _Model_ raises the completion rate but lowers _G_ , while for the large _Model_ it raises both (Fig. 3a). _Information_ shows a similar pattern: at lower levels, more _Budget_ raises the completion rate without raising _G_ , while at the _interface_ level it raises both (Fig. 6a). These patterns largely hold when we compare only configurations that complete under every budget, and the largest interaction overall is between _Information_ and _Model_ (Sections A.9 and A.10). One explanation is that additional budget 

6


<!-- page 7 -->

Table 3: Effect of each axis on _G_ per task (range of mean _G_ across the axis’s levels, divided by the within-cell standard deviation). Axes are ranked within each task (1 = largest effect). 

||promoter-|prediction|redshift|-estimation|rna-f|olding||
|---|---|---|---|---|---|---|---|
|Axis|Rank|Effect|Rank|Effect|Rank|Effect|Mean Rank|
|Information|1|1.925|1|1.452|1|1.496|1.00|
|Model|2|0.704|4|0.170|2|1.253|2.67|
|Reasoning|3|0.274|3|0.172|3|0.302|3.00|
|Budget|4|0.142|2|0.201|4|0.255|3.33|
|Verification|5|0.131|5|0.130|5|0.077|5.00|





<!-- Start of picture text -->
0.9 Budget Short 700 $1 1.0<br>Medium 600<br>Long 500 0.8<br>0.8<br>400<br>300 $0.1 0.6<br>0.7 200<br>0.4<br>100<br>0.6 0<br>Small Medium Large Small Medium Large None Identity Interface Protocol<br>Model Model Information<br>G<br>Cost ($) Mean G<br>Completed Runs<br><!-- End of picture text -->

(a) Interaction of the _Model_ and _Budget_ axes. 

(b) Axis effect of _Information_ on task cost. 

Figure 3: _Left_ : _G_ and number of completed runs per _Model_ and _Budget_ ; error bars show 95% CI of the mean. _Right_ : distribution of a run’s cost per _Information_ level, colored by that level’s mean _G_ . Additional plots are in Fig. 6. 

only improves the score once the agent can use it productively, either because it knows what to do (higher _Information_ ) or because it is capable enough (a larger _Model_ ). Without either, more time may mainly let the agent continue an unproductive approach until it submits, which would raise the completion rate without raising the score. The redshift-estimation case study matches this explanation: at the _none_ level, more budget lowers the score (Table 9). One axis can therefore change not only how strongly another axis matters, but also the direction of its effect, and whether it moves completion and score in the same way. This supports evaluating agents as configurable systems rather than fixed models: how the parts combine matters as much as any single part. 

**Axes affect more than completion and score.** Agents should be evaluated not only on their score but also on accompanying metrics such as cost and runtime (Kapoor et al., 2025). Lower _Information_ levels not only reach a lower _G_ , but also cost more and run longer (Figs. 3b and 6b). We also measure calibration error: the score the agent predicts for itself minus its actual score, normalized by _|R −B|_ , so that positive values mean the agent overestimates its result.<sup>2</sup> On average, agents are overconfident. _Reasoning_ has virtually no effect on calibration error, and the small model is more overconfident than the medium and large models, which behave similarly. More _Information_ reduces the calibration error, most strongly at the _protocol_ level, where both its mean and its spread drop sharply (Fig. 7 and Section A.6). _Information_ therefore improves _G_ , lowers cost and runtime, and improves calibration at the same time, with no trade-off, making it worth the effort to provide. 

**Agents rarely decline a weaker specialist.** On the GAP_NEGATIVE task mmlu-astronomy, agents should answer with their backbone instead of the weaker specialist. Yet 99.8% of runs use AstroSage, including almost all runs at the _none_ level, where it is not mentioned, and the mean accuracy stays close to the specialist’s (Section A.13). Even with the oracle tool (Section 4.3), which lets the agent check the accuracy of its answers, performance does not increase substantially (Table 12). Possible explanations are that agents assume a specialist model outperforms a general one, similar to an authority bias (Xie et al., 2024), or that they explore too little, e.g., by never testing the backbone’s own answers. Investigating these is an interesting direction for future work. 

> 2Agents report a predicted score only at the _reported_ and _binding_ levels of _Verification_ . 

7


<!-- page 8 -->

**Summary.** Agent outcomes on long, specialized tasks are noisy: about 54% of the score variance among genuine attempts is run-to-run noise rather than an effect of the configuration, and completion and outcome consistency vary sharply between tasks. A single run’s score is therefore not a reliable signal on its own. Judging an axis only by its effect on _G_ is also incomplete. _Information_ has the largest effect on _G_ , and at the same time lowers cost and runtime and improves calibration. _Budget_ , in contrast, mainly raises _G_ when the agent has enough information or a large enough model to use the extra time productively. Agents also rarely question a weaker specialist. Building and evaluating agents for such tasks should therefore track completion, score, cost, runtime, and calibration jointly across the axes that shape them, rather than optimizing a single axis for a single metric. 

## 4.3 ABLATIONS 

**Different model families behave similarly, but are not interchangeable.** We rerun the experimental grid with an open-weight model from a different family, Step-3.7-Flash (comparable to the medium Qwen model, Qwen-122B), and with a closed model, Claude Sonnet 5 (roughly comparable to the large Qwen model, Qwen-397B). Both open-weight models rank _Information_ first, while the order of the other axes shifts slightly (Table 14). Step-3.7-Flash also reaches a higher _G_ than Qwen-122B at about half the cost per run (Table 15). The comparison between open-weight and closed model shows a sharper difference. The order of the other axes stays the same, but _Budget_ rises from third to first rank for Sonnet 5 (Table 16). _Information_ still matters, but less than time: the closed model is markedly more sensitive to how long it runs than to how much it is told. Sonnet 5 also executes far more efficiently: pooled across tasks, it needs less than half the tool calls of Qwen397B, produces about a fifth of the tool-call errors, and is better calibrated. Yet at list prices, it costs more, and its pooled _G_ is lower (Table 17). Efficient, low-error execution thus does not by itself lead to a better outcome, analogous to the decoupling of capability and reliability described by Rabanser et al. (2026). A system tuned to one model’s characteristics therefore does not automatically transfer to another, necessitating a systematic analysis like ours to inform the system’s priorities. 

**Verification works better at the system level.** The _Verification_ axis only prompts the agent to check its own work, as a user would, and its effect ranks last among all five axes (Table 3). To test whether verification works better when it is provided by the system instead, we equip the agent with an _oracle_ tool that it can call at any point to score its current submission against the task’s reference solution. The oracle represents the strongest form of system-level verification; in practice, a system would offer weaker checks, such as a validation set. We rerun the full grid with the oracle for two models, Qwen-122B and Step-3.7-Flash, with all axes varied as in the main experiments (Table 12). The oracle raises the score for both models on every task. It also sharply reduces the calibration error, which the prompted _Verification_ axis does not. These gains are not free: runtime and cost rise in every case, because the agent makes more tool calls. Since the agent could also use the oracle to search for the correct answer, we checked all oracle runs for such hill-climbing. It occurs in only 4.4% of runs, and excluding them barely changes the results (Section A.12). This indicates that some agent behaviors, and the outcomes that depend on them, are easier to influence through the system than through the user’s prompt. 

# 5 ANALYSIS: TAXONOMY OF AGENT BEHAVIOR 

Scores show whether an agent succeeds, but not how it behaves or why it fails. To study this, we automatically extract and classify the agents’ outcomes and the behaviors that lead to them from the trajectories, using the following pipeline: 

**Stage 1: Structured Per-Trajectory Extraction.** For every trajectory, we prompt a judge model, DeepSeek-V4-Flash-0731, to describe the trajectory along six dimensions: (i) an overall _result_ characterization, (ii) the single root _error category_ when applicable, (iii) specialist _model usage_ , (iv) _verification behavior_ , (v) _planning and exploration_ , and (vi) _execution quality_ . For every dimension, the judge receives the same context: the task description, the complete trajectory log, automatically derived facts about model usage and scoring, the task’s intended solution approach, and the agent’s final workspace. Following the extract-then-cluster method of Chirkova et al. (2026), each dimension is extracted as domain-agnostic free text rather than assigned from a predefined set of labels. The prompts are in Section A.18. 

8


<!-- page 9 -->

<!-- Start of picture text -->
No Verification Format-Only Verification Interim Verification Reference-Based Verification<br>1.0<br>19% 17% 23% 22%<br>0.8<br>56% 55% 63% 62%<br>0.6<br>0.4 76% 7% 77% 7% 71% 72%<br>7% 8%<br>0.2 35% 34% 26% 26%<br>0.0 5% 5%<br>Baseline Oracle Baseline Oracle Baseline Oracle Baseline Oracle<br>None Asked Reported Binding<br>Verification Levels<br>Share of Occurrences<br><!-- End of picture text -->

Figure 4: Distribution of verification behavior categories per level of the _Verification_ axis, without (Baseline) and with the _oracle_ tool, pooled across Qwen-122B, Step-3.7-Flash, and all tasks. 

**Stage 2: Clustering and Category Induction.** We then consolidate the free-text descriptions of each dimension into a small set of general behavioral categories in three steps. First, we embed the descriptions with a Sentence-BERT model and cluster them with HDBSCAN; points that HDBSCAN leaves unassigned are added to their most similar cluster. Second, the judge model labels each cluster with a short, general description of the behavior, based on a representative sample of its members. Task-specific details go into a separate criterion rather than into the label. Third, the judge model reviews all cluster labels of one dimension at once and merges them into at most _K_ = 8 general categories, combining near-duplicates and overly specific labels. In practice, no dimension reached this limit. As a result, every trajectory receives one category per dimension, which we cross-tabulate against the experimental conditions (details in Section A.15). 

**Results.** Across all dimensions, _Information_ has the strongest association with the distribution of categories (Table 24), consistent with its dominant effect on scores. We highlight one case study that connects to the previous section: _verification behavior_ . The prompted _Verification_ axis had the smallest effect on the score (Table 3), while the oracle tool raised the score for both models on every task (Section 4.3). The taxonomy shows how the agents’ behavior differs between the two. Without the oracle, prompting barely changes how agents verify: from _none_ to _binding_ , the share of reference-based verification rises only from 19% to 22%, and about three quarters of runs check only the format of their answer (Fig. 4). With the oracle, the share of reference-based verification roughly triples at every prompt level. Part of this shift reflects the oracle calls themselves, but it shows that agents use a verification option when the system offers one, largely regardless of what the prompt asks for. This illustrates a broader point: some agent behaviors are hard to shift through the user’s prompt but respond strongly to what the system provides, and the system should be designed with this distinction in mind. 

# 6 CONCLUSION 

We systematically study how five axes of an agent’s configuration influence its outcomes on scientific tasks that require operating specialist models. Four findings stand out. First, agent outcomes are noisy: about 54% of the score variance among genuine attempts is run-to-run noise rather than an effect of the configuration. Second, in our main experiments, the information given to the agent has the largest effect on the score, outranking both the backbone model and the budget, and it also lowers cost and runtime and improves calibration. Third, axes interact: additional budget mainly raises the score when the agent has enough information or a large enough model to use it productively, and can lower the score otherwise, so axes cannot be tuned in isolation. Fourth, some agent behaviors, such as self-verification, barely respond to prompting by the user but shift strongly when the system provides a dedicated tool. Together, these results argue for evaluating and building agents as configurable systems rather than fixed models: tracking completion, variance, cost, and calibration alongside raw scores, and designing the system around behaviors that prompting alone cannot reliably control. 

9


<!-- page 10 -->

**Limitations.** Our analysis covers over 18,000 agent trajectories, but is limited to four tasks across two scientific domains. More tasks and domains would strengthen the generality of the conclusions. We exclude several further system components (memory, multi-agent coordination) that future work should vary as additional axes. Finally, our finding that some agent behaviors respond more to system-level design than to user prompting is demonstrated on one dimension (verification) and needs to be tested across other behavioral dimensions before it can be treated as a general principle. 

## AI USE STATEMENT 

In this work, we used generative AI tools to propose or refine hypotheses, design or provide feedback on research methodology or experiments, implement methods, support qualitative and thematic data analysis, and interpret results. We have not used generative AI tools (or it is not applicable to this work) to generate synthetic data sets, help develop theoretical models or conceptual frameworks, formulate mathematical claims, provide critical ingredients for proving mathematical claims or assist in the writing of proofs. Additionally, we used generative AI tools to create or modify scientific figures or images, suggest experimental parameters, create or edit software code, draft parts of a research paper, summarize or analyse existing literature, discover research topics or identify gaps, brainstorming, sourcing/searching for information, identify relevant literature, and propose a title or keywords for a research paper. We have reviewed all AI-assisted work. All AI use was exclusively used as a first step, and went through manual checks for accuracy, correctness, potential plagiarism, and understandability. We take responsibility for the final content of this work, including text, claims or artifacts produced with the aid of generative AI. 

## REPRODUCIBILITY STATEMENT 

To make the paper fully reproducible, we will release all code and instructions on how to use it. We will additionally release all produced artifacts (agent traces) and derived analyses (raw taxonomy data) to encourage further usage in the community. 

## ACKNOWLEDGMENTS 

This work was partially funded by the ERC (853489 - DEXIM) and the Alfried Krupp von Bohlen und Halbach Foundation, which we thank for their generous support. Cordelia Schmid would like to acknowledge the support by the Körber European Science Prize and the TUM-IAS Hans Fischer Senior Fellowship. The authors gratefully acknowledge the Gauss Centre for Supercomputing e.V. (www.gausscentre.eu) for funding this project by providing computing time on the Supercomputer JUPITER at Jülich Supercomputing Centre (JSC). We also acknowledge the use of the HPC cluster at Helmholtz Munich for the computational resources used in this study.
