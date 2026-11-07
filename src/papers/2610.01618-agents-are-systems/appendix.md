---
source: 2610.01618-agents-are-systems.pdf
part: appendix
converted: 2026-11-07
converter: pymupdf4llm
---

# AGENTS ARE SYSTEMS, NOT MODELS: RETHINKING AGENTIC EVALUATION · 附录

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

# A APPENDIX 

## A.1 IMPLEMENTATION DETAILS 

We serve each open-weight model with vLLM, using tensor parallelism across its GPUs: one NVIDIA H100 GPU for the small Qwen model, two for the medium, eight for the large, and four for Step-3.7-Flash. All models are FP8-quantized and use a context window of 262,144 (Qwen) or 256,000 (Step) tokens. Claude Sonnet 5 is accessed through the Anthropic API. Each cell runs as a separate SLURM array job against the shared model server, with up to 8 concurrent agent runs, each in its own sandbox with access to a single GPU. Table 4 lists the composition of the released trajectories. 

Table 4: Composition of the released trajectories. Each cell is repeated 5 times and the grid covers all four tasks. 

|Grid|Cells per task|Runs per task|Trajectories|
|---|---|---|---|
|Main experiments (3 Qwen3.5 models)|432|2,160|8,640|
|Step-3.7-Flash (no_act-only_)|96|480|1,920|
|Claude Sonnet 5|144|720|2,880|
|Oracle, Qwen-122B|144|720|2,880|
|Oracle, Step-3.7-Flash|96|480|1,920|
|Total|||18,240|



## A.2 TOOL USE AND SPECIALIST MODEL USAGE 

Table 5 shows, for each tool, the mean number of calls per run and the share of these calls that returned an error, for the main experiments. A run_bash call counts as an error if the command does not exit with code 0. A call to any other tool counts as an error if the harness reports that it could not execute it (e.g., a missing file or an unreachable URL). _Other/malformed_ covers all calls to tool names the harness did not recognize, which always fail. run_bash accounts for most calls on every task, while the use of web_fetch differs substantially between tasks. 

Table 5: Mean tool calls per run and error rate per tool, main experiments. 

||run_|bash|read|_file|write|_file|web_|fetch|fin|ish|Other/m|alformed|Tot|al|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Task|Calls|Err.%|Calls|Err.%|Calls|Err.%|Calls|Err.%|Calls|Err.%|Calls|Err.%|Calls|Err.%|
|redshift-estimation|28.51|11.4|4.24|5.7|3.56|3.9|0.79|0.0|0.76|0.1|0.07|100.0|37.93|9.7|
|mmlu-astronomy|17.84|12.7|2.92|1.3|2.36|1.4|0.07|3.8|0.95|0.0|0.05|100.0|24.20|9.9|
|promoter-prediction|16.31|16.2|3.09|0.7|3.73|3.7|0.04|4.3|0.89|0.1|0.04|100.0|24.10|11.8|
|rna-folding|33.21|14.2|3.73|4.0|6.14|3.4|1.62|0.7|0.62|0.3|0.18|100.0|45.49|11.6|



Table 6 breaks the web_fetch calls down by destination. _Ref. correct_ and _Ref. decoy_ give the share of fetches to a URL listed in the README of the correct specialist model or of a decoy. Decoys are the other specialist models in the sandbox, which do not fit the task; on mmlu-astronomy, we also count AstroSage as a decoy, because the correct behavior is not to use it. _Off-list_ covers all other URLs. On the three GAP_POSITIVE tasks, 85–96% of fetches go to the correct model’s reference material. The off-list remainder is mostly general troubleshooting (a search engine, Colab, PyPI, the GitHub API), except on promoter-prediction, where some off-list fetches to huggingface.co read similarly named but wrong repositories (e.g., nlpaueb/dnabert-2-base-100M) instead of the one provided. On mmlu-astronomy, most fetches (73%) also go to AstroSage’s reference material, while 27% go elsewhere, mainly to a search engine and Wikipedia. 

Table 6: web_fetch destinations, main experiments. HTTP OK % is the share of fetches that return a 2xx status. A fetch that returns 404 still counts as successful in Table 5, because the harness executed it without an error. 

|Task|Fetches/run<br>R|ef. correct %|Ref. decoy %|Off-list %|HTTP OK %|Top off-list hosts|
|---|---|---|---|---|---|---|
|redshift-estimation|0.79|88.9|0.1|11.0|84.4|colab.research.google.com,lite.duckduckgo.com|
|mmlu-astronomy|0.07|0.0|73.0|27.0|87.4|lite.duckduckgo.com,en.wikipedia.org|
|promoter-prediction|0.04|84.8|0.0|15.2|85.9|huggingface.co,raw.githubusercontent.com|
|rna-folding|1.62|95.9|0.0|4.1|86.7|api.github.com,lite.duckduckgo.com|



14


<!-- page 15 -->

Table 7 shows how agents engage with each specialist model in the main experiments, based on patterns in the trajectories. It gives the share of runs in which a model’s directory is _mentioned_ in a tool call, its documentation is read ( _read_docs_ ), a command that names the model’s path runs and exits with code 0 ( _executed_ ), and the agent fetches a URL from the model’s README ( _researched_online_ ). On the three GAP_POSITIVE tasks, the correct specialist model is read and executed in 95–99% of runs, while no decoy is executed in more than 1% of runs. mmlu-astronomy has no correct specialist model, since it can be answered directly by the backbone. Still, the weaker AstroSage is read in 98.6% of runs and executed in 66.1%. Because _executed_ only counts commands that name the model’s path, it undercounts use: counting scripts that load AstroSage as well, 99.8% of runs use it (Section A.13). 

Table 7: Engagement with each specialist model (% of runs), main experiments. The correct specialist model per task is in bold, mmlu-astronomy has none. redshift-estimation and mmlu-astronomy were run before the genomics models were available to the agent, however, the genomics tasks, whose sandbox contained all four models, show that the additional models do not keep the agent from finding the right one. 

|Task|Specialist|_mentioned_|_read_docs_|_executed_|_researched_online_|
|---|---|---|---|---|---|
||**astroclip**|100.0%|99.9%|99.3%|28.3%|
|dhifii|astrosage|27.3%|27.1%|0.2%|0.1%|
|rest-estmaton|dnabert-2|0.0%|0.0%|0.0%|0.0%|
||rinalmo|0.0%|0.0%|0.0%|0.0%|
||astroclip|30.5%|30.2%|0.3%|0.0%|
||astrosage|100.0%|98.6%|66.1%|5.0%|
|mmlu-astronomy|dnabert-2|0.0%|0.0%|0.0%|0.0%|
||rinalmo|0.0%|0.0%|0.0%|0.0%|
||**dnabert-2**|100.0%|99.8%|94.7%|3.6%|
||astroclip|11.9%|11.9%|0.0%|0.0%|
|promoter-prediction|astrosage|10.1%|10.1%|0.0%|0.0%|
||rinalmo|24.3%|24.3%|0.2%|0.0%|
||**rinalmo**|100.0%|100.0%|99.3%|38.2%|
|fl|astroclip|10.3%|9.3%|0.1%|0.0%|
|rna-oding|astrosage|8.9%|8.3%|0.0%|0.0%|
||dnabert-2|14.6%|14.0%|0.1%|0.0%|



# A.3 VARIANCE DECOMPOSITION AND HURDLE 

Table 8: Hurdle decomposition and run-to-run variance per task. Mean per-cell SD and the 95% CI half-width of a cell’s mean score (at 5 runs) are expressed as % of _|R −T |_ , so they are comparable across tasks. The pooled CI half-width in units of _G_ is shown in Fig. 5 (right). 

|Task|Hurdle failure rate (95% CI)|_C_out|ICC, all runs|ICC, clears hurdle|Mean per-cell SD|95% CI (5 runs)|
|---|---|---|---|---|---|---|
|redshift-estimation|53.8% [51.4, 56.2]|0.727|33.3%|36.2%|85.1%|91.9%|
|mmlu-astronomy|4.7% [3.9, 5.7]|0.905|29.4%|6.9%|17.6%|20.8%|
|promoter-prediction|0.5% [0.2, 0.9]|0.986|47.9%|49.7%|10.7%|12.9%|
|rna-folding|8.7% [7.3, 10.3]|0.825|45.7%|35.2%|12.8%|13.0%|
|Pooled (3 GAP_POSITIVEtasks, task means removed)|20.6% [19.5, 21.7]|0.858|39.4%|46.1%|—|—|



**Intraclass correlation.** To separate real signal between configurations from run-to-run noise, we decompose the score variance in two steps. First, a one-way random-effects ANOVA over all cells with at least three completed runs splits the total variance into a within-cell component ( _MS_ within) and a bias-corrected between-cell component. From these, we compute the intraclass correlation 



<!-- Start of picture text -->
ICC = σ between 2 σ between 2 +  σ within 2 ,<br><!-- End of picture text -->

the share of the total variance that comes from differences between cells rather than from run-to-run noise. On its own, this decomposition is misleading: a run can complete and still fail to make a genuine attempt at the task (e.g., by running the wrong specialist model or submitting predictions far below the trivial score). Because the ANOVA sums squared deviations, such rare but severe failures inflate _MS_ within far out of proportion to how often they occur. We therefore also compute 

15


<!-- page 16 -->

a two-part (hurdle) decomposition (Cragg, 1971), following recent work on the reliability of LLM agents across repeated trials that separates a binary success indicator per run from a continuous score given success (Rabanser et al., 2026; Khanal et al., 2026). 

**Hurdle indicator and failure rate.** We write _y ∈{_ 0 _,_ 1 _}_ for the hurdle indicator _H_ of a run: _y_ = 1 if the run’s score exceeds the trivial score _T_ by more than the margin _µ_ , and _y_ = 0 otherwise. The hurdle is distinct from completion: runs that do not complete (e.g., because they run out of budget) have no score and are not counted here at all. The _hurdle failure rate_ is the share of completed runs with _y_ = 0, i.e., 1 _− y_ ¯. We report 95% Wilson score intervals (Wilson, 1927). The completion rate in Table 2 uses the same interval, computed over all 2,160 runs of a task. The _±_ values in Table 2 give the half-widths of these intervals, which are nearly symmetric at these sample sizes. 

**Outcome consistency.** For each cell _i_ with at least 3 completed runs, let _p_ ˆ _i_ be the share of its runs that clear the hurdle. Following Rabanser et al. (2026), 



<!-- Start of picture text -->
k k<br>C out = k 1 � i =1(2ˆ pi − 1) 2 = k 1 � i =1 �1  − p ˆ i ( 0 1 .  − 25 p ˆ i ) � ,<br><!-- End of picture text -->

averaged over the _k_ qualifying cells. Each term normalizes the variance of the cell’s binary outcomes by the maximum variance of a Bernoulli variable, 0.25. A cell contributes 1 if all its runs clear the hurdle or all fail it, and 0 if exactly half of them clear it. _C_ out = 1 therefore means that every configuration reliably succeeds or reliably fails. 

**Variance among genuine attempts.** We apply the same ANOVA and ICC to runs with _y_ = 1 only. This measures how repeatable an agent’s score is, given that it makes a genuine attempt. Since this restriction selects runs by their outcome, it can bias the variance estimate, so we report both versions. 

**Pooling across tasks.** Cells are defined per task. Pooling the raw _G_ values of several tasks would therefore count differences between the task means as differences between cells, and inflate the pooled ICC above every per-task value. We therefore subtract each task’s mean before pooling. 

# A.4 ADDITIONAL COMPLETION ANALYSES 

Not every run produces a score, for example when the agent runs out of budget before submitting a solution. Across all four tasks, 80.7% of runs complete, and 19.3% run out of budget. Completion also varies within configurations: on every task, a substantial share of cells completes on some runs but not on others, from run-to-run variation alone (Table 2; Fig. 5, left, for the three GAP_POSITIVE tasks). Per-cell completion rates range from 0% to 100% on every task except mmlu-astronomy, where every configuration completes at least 20% of its runs. We flag a run as an extreme outlier if its score differs from the trivial score by more than 10 times the gap between reference and trivial score, 10 _|R −T |_ . Such outliers occur only on redshift-estimation (7 of 1,647 completed runs, 0.4%), all but one with the small model. We exclude them from all score-based analyses. 



<!-- Start of picture text -->
600 No Completed Run n=600 All Completed Runs<br>None Clear Hurdle Clears Hurdle<br>Some Clear Hurdle 0.25<br>500 All Clear Hurdle<br>0.20 n=600<br>400<br>300 0.15 n=456 n=600<br>200 0.10 n=456 n=456<br>100 0.05<br>0 0.00<br>0 1 2 3 4 5 3 4 5<br>Completed Runs per Cell (of 5) Runs per Cell<br>Cells<br>Mean 95% CI Half-Width<br><!-- End of picture text -->

Figure 5: Completion and variance details, pooled across the three GAP_POSITIVE tasks. _Left_ : cells by their number of completed runs (0–5); color shows whether all, some, or none of a cell’s completed runs clear the hurdle (green/orange/red), and gray marks cells without any completed run. _Right_ : mean 95% CI half-width of a cell’s mean _G_ at 3–5 runs, for all completed runs (light blue) and for hurdle-clearing runs only (dark blue). 

16


<!-- page 17 -->

# A.5 ADDITIONAL INTERACTION AND RUNTIME VIEWS 

Figure 6 shows the _Information×Budget_ interaction, next to the _Model×Budget_ interaction in the main text (Fig. 3), and the effect of _Information_ on runtime, next to its effect on cost. 



<!-- Start of picture text -->
1.0<br>Budget 500 1000 1.0<br>Short<br>0.9 Medium 400 0.8<br>Long<br>0.8 300 0.6<br>200 100<br>0.7 0.4<br>100<br>0.6 0<br>None Identity Interface Protocol None Identity Interface Protocol None Identity Interface Protocol<br>Information Information Information<br>(a) Interaction of the  Information  and  Budget  axes. (b) Axis effect of  Information  on runtime.<br>G<br>Mean G<br>Runtime (s)<br>Completed Runs<br><!-- End of picture text -->

Figure 6: _Left_ : _G_ and number of completed runs per _Information_ and _Budget_ level; error bars show 95% CI of the mean. _Right_ : distribution of a run’s wall-clock time per _Information_ level, colored by that level’s mean _G_ . 

**Case study: redshift-estimation.** How Table 9: Mean _R_<sup>2</sup> & _H_ failure rate, Budget axes interact depends on the task, but _×_ Information, redshift-estimation. redshift-estimation offers a clear example (Table 9). At the _none_ level, more _Budget_ lowers the score ( _−_ 0 _._ 429 _→−_ 0 _._ 713) at similar hurdle failure Info/Budget Short Medium Long rates, consistent with the agent pursuing a wrong _−_ 0 _._ 429 _−_ 0 _._ 441 _−_ 0 _._ 713 None approach further. At the _interface_ level, more _Bud-_ 89.1% 92.0% 92.2% _get_ raises the score ( _−_ 0 _._ 605 _→−_ 0 _._ 380) and lowers _−_ 0 _._ 514 _−_ 0 _._ 519 _−_ 0 _._ 516 Identity the hurdle failure rate: the agent now knows enough 83.8% 84.4% 84.4% _−_ 0 _._ 605 _−_ 0 _._ 560 _−_ 0 _._ 380 to use the extra time. At the _protocol_ level, _Budget_ Interface makes no difference, because every run already 76.1% 71.9% 65.9% 0 _._ 753 0 _._ 753 0 _._ 753 reproduces the reference score. The medians show Protocol 0.0% 0.0% 0.0% the same pattern ( _none_ : _−_ 0 _._ 34 _→−_ 0 _._ 50; _interface_ : _−_ 0 _._ 55 _→−_ 0 _._ 34), and so does the comparison restricted to configurations that have completed runs under all three budgets ( _none_ : _−_ 0 _._ 44 _→−_ 0 _._ 77; _interface_ : _−_ 0 _._ 61 _→−_ 0 _._ 38). 

# A.6 CALIBRATION ERROR 

Fig. 7 shows the calibration error, defined in Section 4 as the agent’s predicted score minus its actual score, normalized by _|R −B|_ , per level of _Reasoning_ , _Model_ , and _Information_ . 



<!-- Start of picture text -->
0.4 1.0 0.6 1.0 0.8 1.0<br>0.6<br>0.2 0.8 0.4 0.8 0.4 0.8<br>0.2<br>0.2<br>0.0 0.6 0.0 0.6 0.0 0.6<br>−0.2 0.4 −0.2 0.4 −0.2 0.4<br>−0.4 −0.4<br>Act-only Think-act ReAct Small Medium Large None Identity Interface Protocol<br>Reasoning Model Information<br>(a)  Reasoning (b)  Model (c)  Information<br>Mean G Mean G Mean G<br>Calibration Error (fraction of gap) Calibration Error (fraction of gap) Calibration Error (fraction of gap)<br><!-- End of picture text -->

Figure 7: Calibration error per level of _Reasoning_ , _Model_ , and _Information_ , pooled across the three GAP_POSITIVE tasks. Positive values mean the agent overestimates its score. Each box is colored by that level’s mean _G_ . 

# A.7 AGENT EFFORT AND COST 

Table 10 gives the mean runtime, cost, steps, tool calls, and tool-call errors per run in the main experiments. Since we run the open-weight models on our own GPUs, we estimate their cost from 

17


<!-- page 18 -->

Table 10: Mean cost and effort per run in the main experiments (432 cells _×_ 5 runs). 

||redshift-<br>estimation|mmlu-<br>astronomy|promoter-<br>prediction|rna-<br>folding|
|---|---|---|---|---|
|Mean Runtime (s)|344.2|188.3|278.0|476.0|
|Mean Cost (USD)|0.277|0.107|0.115|0.424|
|Mean Steps / Tool Calls / Errors|33 / 38 / 4|21 / 24 / 2|20 / 24 / 3|41 / 45 / 5|



Table 11: Cost of one full 720-run task grid, per model. Tokens shown as prompt / completion, in millions. 

||Qwen-35B-|A3B|Qwen-122B-|A10B|Qwen-397B|-A17B||Sonnet 5|||
|---|---|---|---|---|---|---|---|---|---|---|
|Task|Tokens|Cost|Tokens|Cost|Tokens|Cost|Tokens|Calculated|Real|Savings|
|redshift|659.5 / 10.3|$186|397.2 / 7.7|$183|340.1 / 7.0|$229|147.8 / 4.1|$337|$124|63.3%|
|mmlu|222.3 / 3.7|$63|142.0 / 3.2|$67|150.7 / 3.1|$102|65.4 / 2.8|$159|$66|58.6%|
|promoter|306.0 / 7.1|$91|143.0 / 4.9|$73|117.4 / 4.1|$85|88.5 / 3.9|$216|$84|60.9%|
|rna|978.5 / 15.3|$275|579.3 / 13.0|$273|530.3 / 13.5|$367|140.8 / 4.6|$328|$110|66.4%|



token counts at the first-party API list prices (USD per 1M input/output tokens): $0.25/$2.00 for Qwen-35B, $0.40/$3.20 for Qwen-122B, and $0.60/$3.60 for Qwen-397B (Alibaba Cloud Model Studio), and $0.20/$1.15 for Step-3.7-Flash (StepFun). For Claude Sonnet 5, we use Anthropic’s list price of $2/$10. Table 11 gives the total cost of one full grid per task and model. For Sonnet 5, _Calculated_ prices its tokens at the list price without caching discounts, using the same formula as for the open-weight models, and is therefore the directly comparable number. _Real_ is what Anthropic actually billed, with prompt caching, and _Savings_ gives how much lower this is than _Calculated_ . 

# A.8 ABLATION DETAILS 

The outcome and cost tables in this subsection (Tables 12, 15 and 17) share the same conventions. mmlu-astronomy is GAP_NEGATIVE, so its row reports raw accuracy<sup>_†_</sup> instead of _G_ . Calibration error is normalized by _|R−B|_ . Cost, wall-clock time, steps, tool calls, and errors are means per run, with costs estimated at list prices (Section A.7). 

**Oracle ablation.** This paragraph gives the full results of the oracle ablation (Section 4.3). The agent receives an oracle_check tool, independent of the prompted _Verification_ level, which scores its current submission against the task’s reference solution on demand. We rerun the full grid with this tool for two models, Qwen-122B and Step-3.7-Flash, with all axes varied as in the main experiments. Table 12 compares outcome, calibration, cost, and effort with and without the tool, and Table 13 compares the axis ranks. The baseline for Qwen-122B uses its full grid, including _act-only_ , while Table 15 excludes this level; the numbers for Qwen-122B in the two tables therefore differ slightly. **Model-family and open- vs. closed-weight ablations.** This paragraph gives the full results of the two model ablations in Section 4.3. Tables 14 and 15 compare the two open-weight models, and Tables 16 and 17 compare an open-weight and a closed model. For each model, we repeat the axis-effect ranking ( _Model_ is fixed within each block and therefore omitted) and report outcome, calibration, cost, and effort. 

Table 12: Oracle ablation: outcome, calibration error, cost/effort with vs. without the oracle_check tool. 

|||Outco|me|Cal.|Err.|Cost (|USD)|Wall-clo|ck (s)|Steps / T|C / Err.|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Model|Task(s)|Baseline|Oracle|Baseline|Oracle|Baseline|Oracle|Baseline|Oracle|Baseline|Oracle|
|Q122B|mmlu-astronomy<sup>_†_</sup>|0.707|0.725|0.152|_−_0.002|0.093|0.125|165|220|19 / 22 / 2|21 / 24 / 2|
|wen-|Pooled GAP_POSITIVE|0.822|0.923|0.093|0.002|0.245|0.358|346|453|28 / 32 / 4|34 / 39 / 5|
|S37Flh|mmlu-astronomy<sup>_†_</sup>|0.677|0.721|0.285|0.065|0.043|0.091|164|309|18 / 20 / 2|26 / 28 / 3|
|tep-.-as|Pooled GAP_POSITIVE|0.865|0.889|0.073|0.026|0.126|0.177|369|455|29 / 31 / 4|35 / 37 / 5|



18


<!-- page 19 -->

Table 13: Axis-effect ranks on _G_ per task, without (Baseline) and with the oracle tool, for Qwen122B-A10B and Step-3.7-Flash (1 = largest effect). Unlike Table 14, the Qwen-122B baseline includes the _act-only_ level, so its ranks differ from that table. 

|||promo|ter|redsh|ift|rn|a|Mean R|ank|
|---|---|---|---|---|---|---|---|---|---|
|Model|Axis|Baseline|Oracle|Baseline|Oracle|Baseline|Oracle|Baseline|Oracle|
||Information|1|1|1|1|1|1|1.00|1.00|
|Qwen-122B|Reasoning|2|2|3|2|2|2|2.33|2.00|
||Verification|3|4|4|4|3|3|3.33|3.67|
||Budget|4|3|2|3|4|4|3.33|3.33|
||Information|1|2|1|1|1|1|1.00|1.33|
|Ste-37-Flash|Reasoning|3|3|2|3|2|4|2.33|3.33|
|p.|Verification|4|4|3|2|3|3|3.33|3.00|
||Budget|2|1|4|4|4|2|3.33|2.33|



Table 14: Axis effects on _G_ for two open-weight models of similar size: Qwen-122B-A10B and Step-3.7-Flash (198B-A11B). Step-3.7-Flash does not support the _act-only_ level of _Reasoning_ , so both blocks exclude this level; _Reasoning_ ’s rank and effect are computed over its remaining two levels. 

|||prom|oter|reds|hift|r|na||
|---|---|---|---|---|---|---|---|---|
|Model|Axis|Rank|Effect|Rank|Effect|Rank|Effect|Mean Rank|
||Information|1|2.172|1|2.027|1|1.410|1.00|
|Qen-122B|Verification|2|0.256|3|0.195|3|0.193|2.67|
|w|Budget|4|0.086|2|0.313|2|0.262|2.67|
||Reasoning|3|0.116|4|0.028|4|0.041|3.67|
||Information|1|0.848|1|0.951|1|1.412|1.00|
|Ste-37-Flash|Reasoning|3|0.204|2|0.298|2|0.425|2.33|
|p.|Verification|4|0.173|3|0.282|3|0.247|3.33|
||Budget|2|0.558|4|0.177|4|0.058|3.33|



Table 15: Qwen-122B-A10B vs. Step-3.7-Flash: outcome, calibration error, cost, and effort, excluding _act-only_ as in Table 14. 

|Model|Task(s)|Outcome|Cal. Err.|Cost (USD)|Wall-clock (s)|Steps / TC / Err.|
|---|---|---|---|---|---|---|
|Qwen-122B|mmlu-astronomy<sup>_†_</sup>|0.702|0.153|0.089|164|17.8 / 21.6 / 2.1|
||Pooled GAP_POSITIVE|0.802|0.105|0.228|347|25.7 / 31.9 / 3.7|
|Ste-37-Flash|mmlu-astronomy<sup>_†_</sup>|0.677|0.285|0.043|164|17.8 / 19.9 / 2.1|
|p.|Pooled GAP_POSITIVE|0.865|0.073|0.126|369|28.9 / 30.8 / 4.1|



Table 16: Axis effects on _G_ for an open-weight and a closed model: Qwen-397B-A17B vs. Claude Sonnet 5. 

|||prom|oter|reds|hift|r|na||
|---|---|---|---|---|---|---|---|---|
|Model|Axis|Rank|Effect|Rank|Effect|Rank|Effect|Mean Rank|
||Information|1|1.884|1|1.126|1|1.051|1.00|
|Q397B|Reasoning|3|0.467|2|0.238|2|0.233|2.33|
|wen-|Budget|2|0.497|4|0.106|4|0.070|3.33|
||Verification|4|0.235|3|0.207|3|0.178|3.33|
||Budget|1|1.589|1|1.878|1|1.796|1.00|
|Clade Sonnet 5|Information|2|0.521|2|1.293|2|1.683|2.00|
|u|Reasoning|3|0.287|3|0.370|4|0.219|3.33|
||Verification|4|0.099|4|0.153|3|0.279|3.67|



19


<!-- page 20 -->

Table 17: Qwen-397B-A17B vs. Claude Sonnet 5: outcome, calibration error, cost, and effort. 

|Model|Task(s)|Outcome|Cal. Err.|Cost (USD)|Wall-clock (s)|Steps / TC / Err.|
|---|---|---|---|---|---|---|
|397B|mmlu-astronomy<sup>_†_</sup>|0.715|0.131|0.141|159|19.9 / 25.0 / 2.8|
|Qwen-|Pooled GAP_POSITIVE|0.870|0.092|0.315|342|24.7 / 31.4 / 2.6|
|Cld St 5|mmlu-astronomy<sup>_†_</sup>|0.679|_−_0.043|0.220|210|11.5 / 11.6 / 0.3|
|aue onne|Pooled GAP_POSITIVE|0.828|_−_0.016|0.407|244|13.5 / 14.2 / 0.5|



# A.9 UNCERTAINTY OF THE AXIS EFFECTS 

The effect size in Table 3 carries no uncertainty on its own. We complement it in two ways. First, we bootstrap the ranking: in each of 1,000 draws, we resample the runs within every cell with replacement (runs that do not complete stay incomplete), recompute all effect sizes, and record which axis ranks first. Second, we fit a linear model to _G_ of the completed runs of each task, with all five axes as categorical factors (and, for the interactions, all two-way interactions). We report partial _η_<sup>2</sup> , the share of the variance that an axis explains after accounting for the other axes, with 95% intervals from 200 bootstrap draws. _Information_ ranks first on every task in at least 99% of the draws, and partial _η_<sup>2</sup> gives the same order as the effect size, except that _Budget_ drops behind _Reasoning_ , _Model_ , and _Verification_ on redshift-estimation. Among the two-way interactions, _Information×Model_ is the largest on promoter-prediction ( _F_ = 12 _._ 4, _p <_ 10<sup>_−_12</sup> , partial _η_<sup>2</sup> = 0 _._ 04) and rna-folding ( _F_ = 32 _._ 1, _p <_ 10<sup>_−_35</sup> , partial _η_<sup>2</sup> = 0 _._ 13). _Budget×Model_ is significant on rna-folding ( _p <_ 10<sup>_−_3</sup> ) but not on the other two tasks ( _p_ = 0 _._ 08 and _p_ = 0 _._ 36), and _Information×Budget_ is significant on promoter-prediction ( _p_ = 0 _._ 002), borderline on redshift-estimation ( _p_ = 0 _._ 055) and not significant on rna-folding ( _p_ = 0 _._ 18). 

Table 18: Rank stability and partial _η_<sup>2</sup> of each axis per task. P(1): share of bootstrap draws in which the axis has the largest effect size. _η_<sup>2</sup> : partial _η_<sup>2</sup> in a main-effects model, with 95% bootstrap interval. 

||pro|moter-prediction|red|shift-estimation||rna-fo|lding|
|---|---|---|---|---|---|---|---|
|Axis|P(1)|_η_<sup>2</sup>|P(1)|_η_<sup>2</sup>|P(1)||_η_<sup>2</sup>|
|Information|1.00|0.413 [0.378, 0.445]|1.00|0.296 [0.281, 0.323]|1.00|0.260|[0.231, 0.289]|
|Model|0.00|0.080 [0.061, 0.100]|0.00|0.007 [0.002, 0.016]|0.00|0.145|[0.117, 0.177]|
|Reasoning|0.00|0.011 [0.004, 0.019]|0.00|0.008 [0.002, 0.017]|0.00|0.008|[0.003, 0.018]|
|Budget|0.00|0.009 [0.004, 0.017]|0.00|0.000 [0.000, 0.004]|0.00|0.004|[0.000, 0.012]|
|Verification|0.00|0.002 [0.000, 0.008]|0.00|0.003 [0.001, 0.012]|0.00|0.000|[0.000, 0.006]|



# A.10 INTERACTION EFFECTS AND NON-COMPLETION 

Scores are observed only for runs that complete, and completion itself depends on the _Budget_ . A drop in the mean score with more budget could therefore come from weaker runs that now complete, rather than from runs becoming worse. We test this in two ways. First, we restrict the comparison to _matched_ configurations, i.e., settings of all axes except _Budget_ that produce at least _k_ completed runs under every budget level. Second, we report medians next to means. Confidence intervals come from a bootstrap that resamples runs within each cell (1,000 draws). The interactions in Section 4 largely hold under these checks (Table 19). For the small model (Qwen-35B), the mean and median _G_ still fall with more budget in matched configurations, and for the large model (Qwen-397B) they rise. The drop for the small model disappears only under the strictest matching (at least three completed runs per budget level: mean _G_ of 0.81 at _short_ and 0.82 at _long_ ), so part of it is a selection effect. At the _interface_ level of _Information_ , more budget raises both mean and median. At _none_ and _identity_ , the mean does not change; at _none_ , the median rises slightly. 

20


<!-- page 21 -->

Table 19: Change in _G_ from the _short_ to the _long_ budget (long minus short), pooled over the three GAP_POSITIVE tasks, with 95% bootstrap intervals. _Matched_ keeps only configurations with at least one completed run under every budget. 

||All comp|leted runs|Matched configu|irations (_k_ = 1)|
|---|---|---|---|---|
|Level|Mean|Median|Mean|Median|
|_Model_= Qwen-35B|_−_0_._067[_−_0_._093,_−_0_._039]|_−_0_._137[_−_0_._185,_−_0_._073]|_−_0_._045[_−_0_._074,_−_0_._017]|_−_0_._107[_−_0_._157,_−_0_._027]|
|_Model_= Qwen-122B|_−_0_._030[_−_0_._053,_−_0_._010]|_−_0_._018[_−_0_._033,0_._000]|_−_0_._021[_−_0_._042,0_._001]|_−_0_._004[_−_0_._029,0_._005]|
|_Model_= Qwen-397B|0_._025[0_._000,0_._047]|0_._015[_−_0_._002,0_._027]|0_._036[0_._014,0_._059]|0_._016[0_._004,0_._028]|
|_Information_= none|_−_0_._002[_−_0_._036,0_._031]|0_._057[0_._028,0_._060]|0_._004[_−_0_._027,0_._042]|0_._057[0_._027,0_._060]|
|_Information_= identity|0_._004[_−_0_._035,0_._040]|0_._009[0_._000,0_._078]|0_._020[_−_0_._017,0_._053]|0_._012[0_._004,0_._086]|
|_Information_= interface|0_._045[0_._018,0_._078]|0_._028[0_._006,0_._041]|0_._045[0_._014,0_._076]|0_._031[0_._007,0_._041]|
|_Information_= protocol|_−_0_._006[_−_0_._015,0_._003]|0_._000[0_._000,0_._000]|_−_0_._006[_−_0_._015,0_._003]|0_._000[0_._000,0_._000]|



# A.11 GENERATION SPEED AND TOOL TIME 

Because the _Budget_ is wall-clock time, a faster model gets more done within the same budget. Table 20 reports, per model, how the wall-clock time of a run splits into LLM generation and tool execution, how many steps a model takes per minute, and how fast it generates. We derive these numbers from the time stamps in the trajectories: the time before an LLM response is counted as generation time, and the time before a tool result as tool time. Tool execution, not generation, takes most of the wall-clock time for every model (54–73%), so the budget mostly limits how much code the agent can run. The three Qwen models take a similar number of steps per minute (6.0–7.2), because the smaller model’s faster generation is spent on more and shorter steps; between the _short_ and _long_ budget, the median number of steps per run grows from 25 to 36 for Qwen-35B and from 18 to 24 for the two larger models. Claude Sonnet 5 takes fewer steps per minute than the open models and spends a larger share of its time executing code, so its stronger sensitivity to the budget is not explained by faster inference. The speed of generation varied only moderately across runs (CV 0.16–0.26), both on our shared model server and through the Anthropic API. 

Table 20: Generation speed and use of time per model, medians over all runs of the respective grid. Steps are LLM calls; LLM s / step is the generation time per step. CV is the coefficient of variation of the generation speed across runs. 

|Model|LLM s / step|Steps / min|Tokens / s|CV|LLM share|Tool share|
|---|---|---|---|---|---|---|
|Qwen-35B|2.4|7.2|127|0.26|30%|70%|
|Qwen-122B|4.1|6.0|83|0.16|41%|59%|
|Qwen-397B|4.5|6.1|70|0.24|45%|55%|
|Step-3.7-Flash|4.3|6.0|94|0.18|46%|54%|
|Claude Sonnet 5|4.6|3.6|84|0.16|27%|73%|



# A.12 USE OF THE ORACLE TOOL 

Since the oracle scores a submission against the test labels, an agent could use it to search for the correct answer instead of verifying its approach. Table 21 shows how often agents called it. Most runs call it rarely, but 8–22% of runs call it five times or more. We flag a run as likely hill-climbing when it calls the oracle at least five times and at least half of the repeated calls follow only file edits, without re-running any code in between. This applies to 4.4% of all oracle runs (210 of 4,800), mostly on redshift-estimation (10–15% of its runs), where the most extreme runs call the oracle up to 111 times while tuning the regression step. On mmlu-astronomy, where changing single answers would be the most direct form of search, we find almost no such runs (0.1–1.5%). Excluding flagged runs barely changes the pooled _G_ with the oracle (Qwen-122B: 0.923 to 0.922; Step-3.7-Flash: 0.889 to 0.878), which stays above the baseline without the oracle (0.822 and 0.865). 

21


<!-- page 22 -->

Table 21: Number of oracle_check calls per run (share of runs) and share of runs flagged as likely hill-climbing. 

|Model|Task|0|1|2|3–4|_≥_5|Mean calls|Flagged|
|---|---|---|---|---|---|---|---|---|
||redshift-estimation|19.7%|38.9%|8.3%|11.7%|21.4%|4.6|9.7%|
|Q122B|mmlu-astronomy|8.1%|68.3%|8.3%|7.5%|7.8%|1.7|0.1%|
|wen-|promoter-prediction|3.8%|44.9%|11.0%|18.9%|21.5%|3.0|2.5%|
||rna-folding|27.8%|44.6%|9.4%|9.2%|9.0%|1.7|2.8%|
||redshift-estimation|44.6%|25.8%|4.8%|5.6%|19.2%|4.0|14.6%|
|Ste-37-Flash|mmlu-astronomy|34.6%|25.2%|12.3%|14.6%|13.3%|2.0|1.5%|
|p.|promoter-prediction|37.5%|24.0%|7.9%|11.2%|19.4%|2.2|1.0%|
||rna-folding|49.4%|27.9%|7.9%|5.4%|9.4%|1.9|4.0%|



# A.13 AXIS ANALYSIS FOR mmlu-astronomy 

_G_ is not comparable between the two regimes, so we analyze mmlu-astronomy on raw accuracy (Table 22). The correct behavior on this task is to answer with the backbone and decline AstroSage, but agents almost never do this. The model-usage heuristic in Table 7 counts only commands that name the model’s path and finds that AstroSage was executed in 66% of runs; if we also count scripts that load AstroSage and are then executed, 99.8% of all runs used it. This explains why accuracy (0.685 on average) stays close to AstroSage’s own reference accuracy (0.671) and far below the backbone alone (0.967). Ranked by the same effect size as in Table 3, _Information_ (0.93) and _Model_ (0.87) matter most, followed by _Budget_ (0.15), _Reasoning_ (0.08) and _Verification_ (0.05). The _protocol_ level, which describes how to run AstroSage, lowers accuracy from about 0.71 to 0.62, presumably because it describes the weaker specialist in the most detail and thus points the agent further toward it. 

Table 22: mmlu-astronomy: completion rate and mean accuracy per level of _Information_ and _Model_ . Backbone alone: 0.967; AstroSage reference: 0.671; chance: 0.25. 

|Axis|Level|Completion|Mean accuracy|
|---|---|---|---|
||none|92.8%|0.699|
|_Information_|identity|93.9%|0.712|
||interface|98.7%|0.710|
||protocol|95.7%|0.617|
||Qwen-35B|89.6%|0.626|
|_Model_|Qwen-122B|97.5%|0.707|
||Qwen-397B|98.8%|0.715|



# A.14 SENSITIVITY TO THE HURDLE MARGIN 

The margin _µ_ decides when a run counts as clearing the hurdle. We set _µ_ per task from the sampling noise of its metric. Table 23 repeats the hurdle statistics with _µ_ set at 0, 0.5, 1, and 2 times its default value per task. The results change little, except in two places. With _µ_ = 0 on rna-folding, almost every run clears the hurdle, because its trivial score is 0 and nearly every completed run scores above 0. On redshift-estimation, doubling _µ_ (a threshold of _R_<sup>2</sup> _>_ 0 _._ 5) removes the weakest hurdleclearing runs, which raises its ICC. The pooled ICC stays between 45% and 47% for every value. 

22


<!-- page 23 -->

Table 23: Hurdle failure rate and ICC among hurdle-clearing runs for different multiples of the default margin _µ_ . Pooled: three GAP_POSITIVE tasks, task means removed. 

|||Hurdle fa|ilure rate||I|CC, hurdle|-clearing||
|---|---|---|---|---|---|---|---|---|
|Task|0_µ_|0_._5_µ_|1_µ_|2_µ_|0_µ_|0_._5_µ_|1_µ_|2_µ_|
|redshift-estimation|48.7%|53.4%|53.8%|54.1%|35.8%|36.2%|36.2%|53.3%|
|mmlu-astronomy|4.2%|4.3%|4.7%|5.5%|6.9%|7.1%|6.9%|7.2%|
|promoter-prediction|0.2%|0.3%|0.5%|0.6%|48.7%|48.7%|49.7%|50.0%|
|rna-folding|0.2%|7.5%|8.7%|9.5%|45.8%|35.7%|35.2%|34.2%|
|Pooled|16.4%|20.0%|20.6%|20.9%|47.4%|44.8%|46.1%|46.4%|



# A.15 TAXONOMY RESULTS 

Table 24 shows how strongly each axis is associated with the category distribution of each taxonomy dimension, measured by Cramér’s V. _Information_ ranks first on all six dimensions, consistent with its dominant effect on scores. _Model_ and _Budget_ show moderate associations, particularly with error categories and results, while _Reasoning_ and _Verification_ are only weakly associated with every dimension. Figure 8 shows the distribution of categories for each dimension, pooled across all configurations. 

Table 24: Association between each axis and the category distribution of each taxonomy dimension in the main experiments, measured by Cramér’s V (0 = no association, 1 = perfect association). Axes are ranked within each dimension. 



<!-- Start of picture text -->
Error Category Execution Quality Model Usage Planning & Exploration Result Verification Behavior<br>Axis Rank V Rank V Rank V Rank V Rank V Rank V<br>Information 1 0.233 1 0.264 1 0.234 1 0.271 1 0.191 1 0.112<br>Reasoning 5 0.041 4 0.044 4 0.050 4 0.038 4 0.053 4 0.030<br>Verification 4 0.048 5 0.031 5 0.020 5 0.012 5 0.031 5 0.023<br>Budget 3 0.120 3 0.070 2 0.108 3 0.039 2 0.152 2 0.108<br>Model 2 0.157 2 0.138 3 0.097 2 0.084 3 0.095 3 0.067<br>1.0<br>Prescribed Pipeline<br>Adherence Reference-Based<br>8% Verification<br>16%<br>0.8 ErrorNo ExecutionClean 35% Documented ModelUsage31%<br>43%<br>Genuine<br>Completion<br>58%<br>6%<br>0.6 General Provided<br>0.4 Unvalidated ModelReliance11% Post-ProcessingPreprocessing14%10%BugBug Model Usage25% Single-ApproachCommitmentPremature 88% Format-OnlyVerification77%<br>Protocol Genuine<br>Deviation Underperformance<br>20% Answer Parsing Off-Protocol Model 15%<br>15%Bug Usage33%<br>8%<br>0.2 Timeout Before<br>Submission 6%<br>9%<br>Model Handling Timeout Without<br>Execution Bug Incomplete Model Submission<br>Failures 11% Usage 18%<br>12% 9% 5%<br>0.0<br>Error Category Execution Quality Model Usage Planning & Exploration Result Verification Behavior<br>Share of Occurrences<br><!-- End of picture text -->

Figure 8: Distribution of categories for each taxonomy dimension in the main experiments. 

23


<!-- page 24 -->

# A.16 AGENT PROMPT 

## **System Prompt for the Agent** 

You are an autonomous research agent. You solve tasks end-to-end, including ones that call for domain expertise you might not already have. Investigate before you implement, and ground your methodology in whatever authoritative sources you can find (code, papers, the web) rather than guessing. 

You’re given a task description and any data it provides, and one or more pretrained models that may or may not be relevant to solving it; figuring out whether and how to use them is part of the task. You have a private workspace to do your own work in. Your sandbox has GPU access -- check ‘torch.cuda.is_available()‘ (or run ‘nvidia-smi‘) to see what’s available, and use it for any GPU-capable workload (e.g. model inference) rather than defaulting to CPU. Your context window is limited. Data files can be large (e.g. thousands of CSV rows) -- do NOT read entire large data files with read_file, since its output is truncated and wastes context. Instead use run_bash with tools like ‘head‘, ‘wc -l‘, or a short pandas/python snippet to inspect a sample (e.g. the first few rows, column dtypes, shape) before writing code that processes the whole file. 

## You have five tools: 

- read_file(path): read a file. You may read anything under /task (the task description and any provided data, read-only), /models (any models mounted for this task, read-only -- if present, each has its own subdirectory with a README describing what it is -- read it), or /agent_run/workspace (your own scratch directory). Output is truncated for large files. - write_file(path, content): write a file. Only paths under /agent_run/workspace are writable. 

- run_bash(command): run a shell command with working directory /agent_run/workspace. A Python env with numpy, pandas, scikit-learn, scipy, torch, transformers, and accelerate is already active by default -- just ‘import‘ them, no install needed. For anything beyond that, ‘uv pip install <package>‘ adds it to this same env (a shared uv package cache makes this fast); there is no system ‘pip‘ and no writable system site-packages, so always use ‘uv pip install‘, never plain ‘pip install‘. If you want a fully separate env instead of extending the default one, ‘uv venv‘ + ‘source .venv/bin/activate‘ in the same command (each run_bash call starts fresh, so re-activate every time you need it). Any model under /models/<name> is a separate matter: it already has its own complete, pre-built Python environment, entirely unrelated to your workspace’s -- do NOT ‘uv run‘/‘uv venv‘/‘uv pip install‘ against it or expect it to show up in whatever environment you build yourself, no matter your current directory. Instead, invoke its own interpreter directly by absolute path exactly as its README says (typically ‘/models/<name>/env/.venv/bin/python your_script.py‘) -- that binary already has everything that model needs installed. Do not use this tool for internet access (e.g. curl/wget) -- use web_fetch instead. - web_fetch(url): fetch an http(s) URL and get back its main text content (ads/nav/boilerplate stripped out), with links kept as [text (`url`) so you can find further URLs to fetch. Use this to research a topic, look up library documentation, check a current fact, or find anything else you need from the internet -- there is no separate search tool, so to search, fetch a search engine’s results page directly, e.g. https://lite.duckduckgo.com/lite/?q=your+query, then fetch whichever result URL looks relevant. Some hosts may be blocked; a blocked or failed request returns an error explaining why instead of stopping the run. 

- finish(submission_path, summary, model_used): call this when you are done. submission_path must be a path under /agent_run/workspace to your final output (whatever artifact the task asks for -- a predictions file, a report, a script, etc). summary should briefly describe your approach and findings. If you decide to use one of the models under /models to produce your output, set model_used to its directory name (e.g. "astroclip"); if you decided not to use any of them, omit it. 

24


<!-- page 25 -->

Work step by step: understand what the task is asking for, gather whatever data or information you need, do the work before calling finish. You must call finish exactly once when your final output is ready. Do not stop before calling finish. 

# A.17 SPECIALIST MODEL AND TASK EXAMPLES 

As an example, the following listings show the README of AstroCLIP, the task description of redshift-estimation, and the additional information given at each _Information_ level of this task. The _none_ level adds no information and therefore has no listing. 

## **README for** **_AstroCLIP_** 

# AstroCLIP 

Non-generative cross-modal foundation model for galaxies: a DINOv2 image encoder and a SpecFormer spectrum encoder, aligned into a shared embedding space via contrastive pretraining on DESI cross-matched imaging + spectra. 

- Model card: https://huggingface.co/polymathic-ai/astroclip - Paper: https://arxiv.org/abs/2310.03024 - Code: https://github.com/PolymathicAI/AstroCLIP 

## Environment 

A working environment is already synced at ‘env/.venv‘ -- use it as-is: ‘‘‘bash /models/astroclip/env/.venv/bin/python your_script.py ‘‘‘ 

Don’t try to rebuild or reinstall into it -- it’s mounted read-only and already pins some fussy dependency versions. 

**Task description for redshift-estimation** 

## Task 

For each galaxy image below, estimate its cosmic redshift. Respond with a single decimal number per galaxy. Your predictions will be scored against the true redshift using R^2 (coefficient of determination) across all query galaxies. 

## What you have 

- ‘data/query_images/<targetid>.npy‘ -- 20 galaxy imaging cutouts, one file per galaxy, each a ‘(152, 152, 3)‘ float32 array (three photometric bands). No redshift is attached to these -- that is what you need to estimate. 

- ‘data/reference_catalog.npz‘ -- a supporting reference catalog of 126,907 other galaxies with known redshifts, useful for grounding your estimate. - One or more pretrained models may be available in your environment under ‘/models/<name>‘ -- each has its own documentation describing what it is and how to use it. It’s up to you to decide whether any of them are useful for this task. 

## Output 

Write a CSV file to your workspace with exactly these columns: ‘targetid,redshift‘ -- one row per query galaxy (20 rows total, matching the files in ‘data/query_images/‘). Then call ‘finish‘ with the path to this file. 

25


<!-- page 26 -->

**Information** **_identity_ for redshift-estimation** 

## Model identity 

The ‘astroclip‘ model mounted at ‘/models/astroclip‘ is the domain-relevant model for this task. 

**Information** **_interface_ for redshift-estimation** 

## Model interface Load the checkpoint: ‘‘‘python from astroclip.models import AstroClipModel model = AstroClipModel.load_from_checkpoint( checkpoint_path="/models/astroclip/weights/astroclip.ckpt", map_location=device, weights_only=False, ) model.eval() ‘‘‘ 

Call the model on a batch of preprocessed image tensors to get embeddings: ‘model(tensor, input_type="image")‘ returns a ‘(batch, 1024)‘ embedding. Always embed in batches of 2 or more -- a batch of exactly 1 crashes on an upstream bug in the model’s cross-attention head. 

**Information** **_protocol_ for redshift-estimation** 

## Protocol 

‘data/reference_catalog.npz‘ already holds ‘embeddings‘/‘redshift‘ arrays for 126,907 reference galaxies, pre-embedded exactly the way your query images need to be. 

Preprocess raw images before embedding them: 

‘‘‘python from astroclip.data.datamodule import AstroClipCollator collator = AstroClipCollator() tensor = collator([{"image": torch.from_numpy(img)} for img in query_images])["image"] ‘‘‘ 

This applies ‘ToRGB‘, an arcsinh stretch of the raw nanomaggie flux, plus a center-crop -- required preprocessing, not optional. Skipping it produces near-degenerate embeddings. This must match how the reference embeddings in ‘data/reference_catalog.npz‘ were produced. 

Then estimate redshift with a k-NN regressor: 

‘‘‘python from sklearn.neighbors import KNeighborsRegressor from sklearn.preprocessing import StandardScaler scaler = StandardScaler().fit(reference_embeddings) reference_scaled = scaler.transform(reference_embeddings) query_scaled = scaler.transform(query_embeddings) 

26


<!-- page 27 -->

knn = KNeighborsRegressor(n_neighbors=64, weights="distance") knn.fit(reference_scaled, reference_redshift) predictions = knn.predict(query_scaled)‘‘‘ 

# A.18 TAXONOMY PROMPTS 

## **System Prompt for the Taxonomy Judge** 

You are extracting structured information from a log of an autonomous research agent’s attempt at a task, for building a taxonomy of run outcomes. You will be shown the task description, the complete raw event log (trace.jsonl -- one JSON object per line: run_start, llm_response, tool_call, status_message, run_end, in chronological order), mechanical facts computed from the trace and the task’s scoring, the task’s intended approach, and the agent’s final workspace. Read everything before answering; do not guess from a partial read. Some scoring facts are the agent’s own self-reported claims, marked as such below -- treat those as claims to confirm or contradict using the trace, not as established fact. Respond with a single JSON object matching exactly the fields requested, and nothing else -- no markdown fencing, no commentary outside the JSON object. Make sure the JSON is syntactically valid: escape any quotation marks that appear inside a string value. 

## **Prompt for the Taxonomy’s** **_Result_ Dimension** 

Describe, in your own words, how this run concluded and whether the result holds up, drawing on the scoring facts above. A clean, genuine success; a result that looks gamed or exploited somehow (hardcoded/memorized answers instead of a real method, peeking at solution or ground-truth files, exploiting a metric loophole, a suspiciously trivial method for a result this good); a crash or a submission that never became genuinely scoreable, and specifically what happened; or something else entirely. Say plainly if there’s nothing questionable about it. 

## **Prompt for the Taxonomy’s** **_Error Category_ Dimension** 

Name the single root cause of any problem with this run, not every symptom -- a cascading failure usually traces back to one earlier cause, and downstream symptoms of that same cause don’t each count separately. Distinguish a genuine error from something that only looks like one: normal exploration, a failed attempt the agent recognized and moved past, or a hypothesis it later revised are not errors on their own. If there’s no error attributable to a specific cause -- including for a run that succeeded cleanly -- say so explicitly with "no_identifiable_error"; don’t invent a cause to fill the field. 

## **Prompt for the Taxonomy’s** **_Specialist Model Usage_ Dimension** 

How did the agent engage with the domain-specific pretrained model(s) available for this task? Describe, in your own words, specifically what happened -- name the model(s) involved and what was actually done with them (or not done). Draw on the mechanical engagement signals and the agent’s own self-reported model choice given above, alongside the trace itself. A few examples of the kind of thing to look for, not a list to pick from -- if what you observe is something else entirely, describe that instead: reading documentation before using a model correctly; using one correctly without apparently reading its docs first; loading a model but using it incorrectly in some specific way (say exactly how -- wrong input format, wrong preprocessing, misreading its output, using an untrained/randomly-initialized part of it, applying it to the 

27


<!-- page 28 -->

wrong data); never loading or running it at all; using a different, unintended model instead. 

**Prompt for the Taxonomy’s** **_Verification Behavior_ Dimension** 

What did the agent actually do, if anything, to check its own work before submitting? Describe, in your own words, the specific check performed (or the absence of one) -- not just whether it was rigorous, but what it actually consisted of. This is about observed behavior, independent of what the task’s own Verification condition nominally asked for or permitted. 

**Prompt for the Taxonomy’s** **_Planning and Exploration_ Dimension** 

Describe the agent’s overall approach and how it arrived at it, in your own words. Did it explore more than one substantively different approach before committing, or settle on one early and stick with it even where the trace shows evidence (an error, an unexpected result) that should have prompted reconsidering it? Name the specific approach(es) involved, not just whether it explored. 

**Prompt for the Taxonomy’s** **_Execution Quality_ Dimension** 

Independent of whether the agent’s plan was sound, was the plan implemented correctly? The agent’s actual code is included above in its final workspace -- read it directly, not just the trace’s account of it, to find concrete bugs. Describe, in your own words, any concrete implementation bugs found -- wrong preprocessing, off-by-one errors, misread columns or fields, output-format mismatches, incorrect use of an API or library -- or state plainly that none were found. 

28
