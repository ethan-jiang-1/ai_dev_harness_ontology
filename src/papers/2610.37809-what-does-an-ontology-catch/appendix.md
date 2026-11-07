---
source: 2610.37809-what-does-an-ontology-catch.pdf
part: appendix
converted: 2026-11-07
converter: pymupdf4llm
---

# What Does an Ontology Catch? Curated, LLM-Generated and Data-Derived Ontologies as Checkers of LLM Agents over Knowledge Graphs · 附录

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

# **A The replication package** 

The replication package is available at https://anonymous.4open. science/r/www-2027-replication-package-36D6. It holds the code, under the MIT licence; the frozen inputs and configurations; each model’s final settings; the commands that run the study; and the analysis that reproduces every number reported here, with the data under CC BY 4.0. The private graph contributes rates only: its data, its alignment mapping, its generated ontologies and the checks’ messages on it are not released. 

# **B The method in detail** 

This part describes how the study was carried out, beyond Sections 3 and 4. It lists the checks, describes the LLM-generated ontologies, and gives the cost of checking. 

# **B.1 The checks in detail** 

Table 7 lists every check, what it reads, and when it cannot decide. The checks are compiled from the ontology into SPARQL queries over the bindings of a query, and into tests on the parsed query. The supported fragment includes basic graph patterns, OPTIONAL, negation, aggregates, and fixed-length paths; constructs outside it, including UNION and subqueries, give an unknown verdict rather than a pass or a flag. The numbers-traceable check needs no ontology and enters no comparison between ontologies. 

**Table 7: The checks: what each reads, and when it reports unknown.** 

|Check|Reads|Unknown when|
|---|---|---|
|Term exists|the query|—|
|Class membership|<br>query; bindings|a value has no type|
|Domain and range|query; bindings|a value has no type|
|Disjointness|query; bindings|a value has no type|
|Datatype range|bindings|—|
|<br>Numbers traceable|answer and results|—|



# **B.2 The LLM-generated ontologies** 

The three ontologies an LLM wrote from the masked UniProt summary keep 87–90% of the data-derived ontology’s domain and range pairs and add none of their own, so their property sets almost coincide with it (Jaccard similarity 0.93), and they add 73, 759 and 77 disjointness pairs, for which the data-derived ontology has no layer. Their domain and range overlap little with the curated ontology’s (Jaccard similarity 0.21–0.22). 

The model that writes the ontologies matters. Claude Opus 5.5, DeepSeek-V4-Flash and Qwen3.8-27B each wrote three ontologies by the same recipe; on UniProt’s artificial faults and averaged over each model’s three ontologies, Opus’s ontologies catch 60.4% of the faults that change the answer and flag 10.3% of the untouched correct queries, DeepSeek’s catch 84.1% and flag 59.5%, and Qwen’s catch 81.9% and flag 61.0%. Whether a model’s ontology misses its own agent’s errors was also registered, as an interaction _𝐼_ between two models predicted to be negative; the result is inconclusive: of the two pairs whose agents both give at least 20 wrong answers, 

**Table 8: What checking costs on UniProt, per kind of ontology, pooled over the seven models (median, with the 90th percentile in parentheses).** 

||Setup|Per answer checked|<br>Per answer fl|lagged|
|---|---|---|---|---|
|Check from|(US$)|triples read|tokens|time (s)|
|Curated|—|25 (277)|65,976 (435,066)|46.0 (420.0)|
|same flags, generic message|—|—|60,927 (308,426)|49.2 (309.7)|
|Data-derived|—|25 (269)|28,076 (202,405)|17.2 (112.3)|
|LLM-generated, draft 1|0.43|24 (267)|42,027 (181,818)|22.4 (170.5)|
|LLM-generated, draft 2|0.47|25 (269)|58,719 (455,836)|29.5 (456.1)|
|LLM-generated, draft 3|0.39|24 (267)|65,030 (369,424)|25.7 (342.7)|
|LLM-generated, masked (three)|0.48–0.98|25 (269)|—|—|
|Combined|—|50 (552)|63,819 (429,171)|28.7 (337.5)|



the one on the masked copy of Rhea has _𝐼_ = −9 _._ 2 (−20 _._ 1 to 1 _._ 0), and the one on UniProt, DeepSeek and Qwen3.8, has _𝐼_ = +8 _._ 5 (1 _._ 5 to 15 _._ 3). 

# **B.3 The cost of checking** 

Table 8 reports what checking costs on UniProt, per kind of ontology. Setup is incurred once per graph. The curated ontology is used as published, and the cost of authoring it is borne by its publisher; each ontology Claude Opus 5.5 wrote for UniProt cost under one US dollar at batch prices; the time to build the data-derived ontology and the time a check takes were not recorded. Aligning the private graph’s curated ontology with the data’s identifiers took an expert three hours (Appendix C.4). What differs is the retry after a flag: one after a curated flag uses more tokens and time than one after a data-derived flag, and the curated check’s specific message costs about as much as a generic request to re-check. 

# **C Beyond the pooled comparison** 

This part asks whether the comparison behind RQ1 holds beyond the pooled UniProt results of Table 2. It repeats the comparison per model and under the registered sensitivities, against the comparators, on human-written questions, and on the other graphs. 

# **C.1 Per model and under the registered sensitivities** 

Table 9 gives each model’s accuracy with each kind of ontology in the prompt, the change in accuracy the curated check makes through its retry, and the effect of the check’s specific message per flagged answer. Table 10 gives each model’s catch and false-alarm rates on its answers given with no ontology: for each of the six models with enough correct answers (all but Qwen3-Coder), the curated check flags more correct answers than the data-derived and masked LLM-generated ontologies and catches more wrong ones, so the pooled pattern of Table 2 is not one model’s. Sonnet and Haiku are wrong on fewer than 30 answers and Qwen3-Coder gives 44 answers, so their rates rest on few answers. The per-model rate of invented identifiers, registered for this appendix, was not computed. 

Re-running or excluding the attempts disturbed by time-outs (4.8% of all attempts) leaves every registered decision unchanged and moves no estimate by more than 0.3 points; the data-derived ontology gives identical rates on real answers at frequency thresholds of 2 and 20 instead of 5; and no attempt was missing or refused. Under the earlier version of the scorer’s rules (the frozen rules only add correct verdicts), C1a is −1 _._ 2 points (−2 _._ 7 to 0 _._ 2), and excluding


<!-- page 11 -->

What Does an Ontology Catch? 

**Table 9: Per model, on UniProt: accuracy with each ontology in the prompt, in %, and the curated check’s net change after its retry and the specific message’s effect per flagged answer (C5), in points.** 

||<br>|Accuracy,<br>|ontology in the prompt<br>|Curat<br>|ed check<br>f|
|---|---|---|---|---|---|
|Model|none|curated|data-derived LLM-generated|net change|message effect|
|Claude Sonnet 5.5<br>|95.6|95.2|96.0<br>97.5|0.3|0.9|
|Claude Haiku 5.5<br>|95.7|93.8|93.0<br>—|0.2|1.0|
|Qwen3.8-27B<br>|80.8|79.7|80.8<br>81.9|0.8|0.0|
|Qwen3-Coder-30B-A3B<br>|1.6<br>|5.9<br>|9.0<br>—<br>|−0.2<br>|−7.1<br>|
|GLM-5.3-Flash<br>|82.4|86.5|87.1<br>—|0.6|−1.8|
|Gemma-4-31B<br>|15.7|44.4|52.7<br>—|1.0|6.2|
|DeepSeek-V4-Flash|82.2|84.8|86.2<br>—|1.0|2.0|



**Table 10: Each model’s checks on UniProt, on its answers with no ontology in the prompt: catch / false alarm, in %. The three masked LLM-generated ontologies give identical rates.** 

|Model|Curated|Data-derived|LLM-generated, masked|
|---|---|---|---|
|Claude Sonnet 5.5|7.1 / 17.4|0.0 / 1.7|0.0 / 1.2|
|Claude Haiku 5.5|14.8 / 15.9|0.0 / 5.0|0.0 / 2.2|
|Qwen3.8-27B|13.2 / 16.7|0.8 / 3.5|0.0 / 2.0|
|Qwen3-Coder-30B-A3B|32.4 / 30.0|35.3 / 10.0|14.7 / 0.0|
|GLM-5.3-Flash|14.3 / 18.1|1.9 / 5.6|1.9 / 2.7|
|Gemma-4-31B|30.2 / 19.2|24.0 / 6.1|16.7 / 5.1|
|DeepSeek-V4-Flash|19.6 / 15.1|4.5 / 1.4|2.7 / 0.4|



the two questions whose curated prompt contains a correct answer value leaves it at −2 _._ 0 (−3 _._ 3 to −0 _._ 8). The unadjusted bootstrap _𝑝_ -values are 0.002 (C1a), 0.113 (C1b), _<_ 0.001 (C2), _<_ 0.001 (C3), 1.000 (C4) and 0.457 (C5)„ and a cluster-robust (CR2) Wald test agrees. Three registered source sensitivities and a registered selective check were not run. 

# **C.2 Comparators** 

Table 11 places the ontology-derived checks beside the comparators of Section 4.7. The LLM judge reads the question, the query, the results and the answer; it is played by the agent’s own model on real answers and by Claude Sonnet 5.5 and Haiku 5.5 on the 2,238 artificial faults whose question has a text. On real answers it catches more wrong answers than the curated or the data-derived ontology, at about the data-derived ontology’s precision; on artificial faults it catches nearly every fault, including every change of meaning, and flags 30–38% of the faulty queries whose answer is nonetheless correct. SPARQL-LLM’s validator does no better than a random flag at its rate. The Ontology-based Query Check’s eight rules together flag most answers, wrong and correct alike. Acted on, the judge’s flags corrupted more correct answers than they fixed wrong ones, and the other checks’ retries changed few answers. Combining the curated and data-derived checks adds 3 catches to the curated check’s at 28 more false alarms, and 59 to the data-derived check’s at 407 more. 

# **C.3 Human-written questions** 

SIB’s published human-written questions were also run with no ontology in the prompt, for Sonnet and Qwen3.8 on UniProt and Rhea (Table 12); they are analysed apart from the generated questions. Of SIB’s 173 primary UniProt questions, 170 are analysed, since three ask for a graph, not an answer; of its 124 Rhea examples, 101, after excluding 18 with a SERVICE clause, by a rule fixed before the gold run, and 5 with an empty gold answer. The agents are far less accurate than on the generated questions, and most of their 

**Table 11: Comparators on UniProt, in %, on real answers and on artificial faults with a question text. Vs rand.: points by which precision beats a random flag at the same rate; fix / corr.: answers fixed and corrupted after one retry; the judge on faults: Sonnet / Haiku.** 

|||R<br>|eal an<br>|swers<br>|i|Ari<br>|tificial faul<br>|i ts|
|---|---|---|---|---|---|---|---|---|
|Check|catch|false al.|prec.|vs rand.|fix / corr.|catch|false al.|prec.|
|Retry on empty<br>|2.5|0.1|81.3<br>|+65_._8<br>|2 / 0<br>|80.4<br>|0.0|100|
|Curated<br>|18.9|16.8|17.1|+1_._6<br>|28 / 5|59.7|13.2|60.1|
|Data-derived<br>|8.2|3.5|29.9|+14_._4<br>|3 / 1|75.5|9.3|73.0|
|Combined<br>|19.5|17.8|16.7|+1_._3<br>|30 / 5<br>|—<br>|—<br>|—<br>|
|LLM judge<br>|40.3|16.2|31.3|+15_._8<br>|40 / 83<br>|98.7 / 98.0|11.4 / 11.6|74.2 / 73.8|
|SPARQL-LLM<br>|5.5|6.5|13.5|−2_._0<br>|2 / 1|—|—|—|
|Query Check, 8 rules<br>|87.8|90.2|15.1|−0_._4|—|—|—|—|
|Query Check, 1–6<br>l|34.8|22.1|22.3|+6_._9|—|—|—|—|
|Always flag<br>l|100|100|15.5|—|—|100|100|25.0|
|Never flag|0.0|0.0|—|—|—|0.0|0.0|—|



**Table 12: Human-written questions (SIB) on UniProt and Rhea, no ontology in the prompt: accuracy and each check’s catch / false alarm, in %. Vs rand.: points by which precision beats a random flag; LLM-generated: range over three.** 

||Sonnet, UniProt|Sonnet, Rhea|Qwen3.8, Rhea|Qwen3.8, UniProt|
|---|---|---|---|---|
|Questions|170|101|101|170|
|Accuracy|11.8|11.9|9.2|9.0|
|Curated|34.3 / 11.7|41.8 / 41.7|35.3 / 46.4|35.3 / 4.3|
|vs rand.|+8_._7|0.0|−3_._2|+10_._7|
|Data-derived|0.8 / 0.0|2.8 / 0.0|1.0 / 0.0|5.6 / 0.0|
|LLM-generated|2.4–18.4 / 5.0–28.3|3.3–6.6 / 8.3|4.8–8.7 / 7.1|0.9–18.0 / 6.5–19.6|
|LLM judge|53.2 / 8.3|29.6 / 0.0|—|—|
|vs rand.|+11_._5|+14_._5|—|—|



submitted answers are wrong. On the UniProt questions the LLM judge, the curated check and the data-derived ontology keep their order by catch rate, and Sonnet’s curated check beats a random flag at its rate (by 8.7 points, 1.9 to 15.5); on the Rhea questions it does no better than one. The false-alarm rates rest on few correct answers, so they are not compared with those on the generated questions. 

# **C.4 The other graphs** 

Table 14 repeats the central comparison on the four exploratory graphs, for the two confirmatory models, on real answers. Rhea’s curated ontology declares no domain, range or disjointness axioms, so only class and declaration checks apply to it, and as context every ontology on Rhea is truncated to the prompt budget. Some of Rhea’s provisional artificial faults were exposed, so no artificial-fault result is reported for Rhea. 

On Rhea the pattern of Table 2 repeats, at a higher cost for the curated check: over the six models with enough correct answers (all but Qwen3-Coder), it flags 23.2–63.0% of them, against 15.1– 19.2% on UniProt and more than any other ontology, while the data-derived ontology and the first two LLM-generated ones flag few. The context difference seen on UniProt does not carry over: of the seven models, the data-derived ontology in the prompt gives the higher accuracy only for Gemma (83.0% against 40.6%) and Qwen3-Coder (16.7% against 9.4%), the two weakest; for GLM the two are nearly equal (87.9% and 87.8%). 

On the masked copy of Rhea, the three LLM-generated ontologies, written from masked names, stay within a few points of one another and of the data-derived ontology, flagging few correct answers and catching few wrong ones for every model, while the curated check’s rates vary widely across models. On the corporate


<!-- page 12 -->

Orzechowski et al. 

**Table 13: The checks layer by layer on UniProt, caught / false alarms in %: type swaps and untouched correct queries (artificial faults, per question), and real answers. C: class; DR: domain and range; +DJ: plus disjointness (J: the data-derived co-occurrence patterns); LLM-generated: mean of three.** 

|||Artificial faults (ca|i  ught / false alarms)|||Real answers (cau|ght / false alarms)||
|---|---|---|---|---|---|---|---|---|
|Ontology|C|C+DR|+DJ (J)|full|C|C+DR|+DJ (J)|full|
|Curated|26.5 / 0.0|41.3 / 7.1|41.3 / 7.1|56.3 / 15.7|3.1 / 0.6|8.0 / 8.8|8.0 / 8.8|18.9 / 16.8|
|Data-derived|46.8 / 0.0|73.7 / 0.0|78.5 / 7.1|78.5 / 7.1|1.0 / 0.2|1.0 / 0.3|4.8 / 2.1|8.2 / 3.5|
|LLM-generated, masked|31.9 / 0.0|50.4 / 0.0|50.4 / 0.0|50.4 / 0.0|1.0 / 0.2|1.0 / 0.3|1.0 / 0.3|5.0 / 1.8|
|LLM-generated, ordinary|30.4 / 0.0|46.8 / 0.0|46.8 / 0.1|55.3 / 10.3|—|—|—|—|



**Table 14: The central comparison on the exploratory graphs, real answers of Sonnet and Qwen3.8: accuracy, and each check’s catch / false alarm, in %. LLM-generated: one range on the masked copy; identical on the corporate and private graphs.**<sup>†</sup> **Very few wrong answers.** 

|||||LLM-ge|nerated|
|---|---|---|---|---|---|
|Graph|accuracy|Curated|Data-derived|drafts 1–2|draft 3|
|Rhea, Sonnet|96.0|8.0 / 63.0|0.0 / 2.1|0.0 / 3.0–3.3|36.0 / 9.8|
|Rhea, Qwen3.8|92.1|20.4 / 39.1|0.0 / 3.3|0.0 / 4.5–4.7|16.3 / 11.4|
|Masked Rhea, Sonnet|68.3|58.8 / 57.0|0.0 / 0.0|0.5–4.0 /|0.0–3.7|
|Masked Rhea, Qwen3.8|30.0|25.9 / 20.6|1.9 / 2.6|0.9–2.8 /|2.6–3.7|
|Corporate, Sonnet|99.4|50.0<sup>† </sup>/ 24.8|0.0<sup>† </sup>/ 0.5|0.0<sup>† </sup>|/ 0.0|
|Corporate, Qwen3.8|94.3|22.2 / 25.9|2.8 / 1.3|2.8 /|1.3|
|Private, Sonnet|100.0|— / 71.1|— / 1.6|— /|1.6|
|Private, Qwen3.8|98.1|50.0<sup>† </sup>/ 70.1|0.0<sup>† </sup>/ 0.5|0.0<sup>† </sup>|/ 0.5|



graph, whose curated ontology declares domain and range axioms but no disjointness, no model is less accurate with either ontology in the prompt, and the curated check flags 20.5–25.9% of the correct answers of the six models with enough of them (all but Qwen3Coder), while the data-derived and LLM-generated ontologies flag almost none. The setting a developer is likely to deploy, a dataderived context with a curated check, gains a little on UniProt but less, nothing or a loss on the other graphs: pooled over the seven models on UniProt, one retry raises accuracy by 1.0 point; one retry changes Sonnet’s accuracy by at most 0.5 point on each of the four graphs where it was run, and Qwen3.8’s by +1 _._ 6 points (0.3 to 3.0) on UniProt and by −3 _._ 8 (−5 _._ 9 to −1 _._ 9) on the corporate graph. 

On the private graph, with no ontology in the prompt, Sonnet, Haiku, Qwen3.8, GLM and DeepSeek answer at least 92.9% of the questions correctly, Gemma 59.2%, and Qwen3-Coder rarely submits an answer. The curated check flags 56.3–72.8% of the correct answers of the six models, while the data-derived ontology and the three LLM-generated ones, which give identical results, flag almost none. Only GLM and Gemma give enough wrong answers to compare catch rates: the curated check catches 73.0% and 74.0% of them, and the other ontologies none of GLM’s and 13.0% of Gemma’s. An expert also aligned the curated ontology’s terms with the data’s identifiers, in three hours for 115 terms. On the answers given with no ontology in the prompt, alignment raised the share of correct answers the checks flag for each of the six models, from 56.3–72.8% to 69.7–85.1%; the results with an ontology in the prompt are in the replication package. Leaving out the 20 questions that the triple store’s known query faults can affect keeps every model’s accuracy within its interval. 

# **D Where false alarms come from** 

This part collects the evidence behind RQ2 and behind the masked ontologies of C3. It switches the checks on layer by layer, describes the audit of false alarms and misses, and measures how far agents 

**Table 15: Closed-book probes, exact match in %: an answer (a) and a query (b) written from memory; and the agents’ accuracy with no ontology, masked Rhea minus Rhea, in points with 95% intervals.** 

||a: UniProt||b: quer|y from memory||agent accuracy|
|---|---|---|---|---|---|---|
|Model||UniProt|Rhea|masked Rhea|corporate|masked−Rhea|
|Sonnet|4.9|53.7|46.0|1.1|46.3|−27_._8(−32_._6,−22_._9)|
|Haiku|1.4|39.0|24.8|1.3|0.0|−35_._2(−40_._6,−29_._8)|
|Qwen3.8|0.8|0.0|4.9|0.0|26.7|−62_._1(−68_._2,−55_._8)|
|Qwen3-Coder|0.0|1.0|0.0|1.1|0.0|−2_._1(−3_._4,−0_._9)|
|GLM|1.7|26.7|21.7|0.0|37.5|−52_._9(−58_._0,−47_._6)|
|Gemma|0.0|0.6|0.0|1.0|0.0|−26_._5(−32_._3,−21_._0)|
|DeepSeek|0.2|1.9|1.4|0.6|0.0|−50_._5(−56_._2,−44_._8)|



and LLMs rely on recognising a graph’s vocabulary. 

# **D.1 The checks layer by layer** 

Table 13 switches each ontology’s checks on one layer at a time: class checks with the heuristic of Section 3.3, then domain and range, then disjointness (for the data-derived ontology, its checks on co-occurrence patterns instead), then the declaration check, which completes the full set. On real answers, the precision of the curated ontology’s domain and range flags differs from that of a random flag at the same rate by −1 _._ 2 points (95% CI −5 _._ 5 to 5 _._ 1), and that of its class membership and term-declaration flags by +8 _._ 0 points (1.8 to 15.3). In the data-derived ontology, the class, domain and range axioms catch more type swaps than the same axioms in the masked ontologies; without the heuristic they catch 37.2% of type swaps, against 73.4% with it, pooled over items, and most of the data-derived ontology’s false alarms arise from its checks on co-occurrence patterns. 

# **D.2 The audit** 

Two annotators coded a seeded, stratified sample of 145 answers from the test questions, one answer per question within each stratum: 64 wrong answers that no check flagged and 32 correct answers that the curated check flagged, spread evenly over the four public graphs (the missed answers also over Claude and the open-weight models), 16 wrong answers given with the curated ontology in the prompt that the curated check passed, ten of each of the first two kinds on the private graph, and 13 items allocated by a fixed rule. Annotators saw the question, the correct and the agent’s query and answer, and the check’s message or the ontology where relevant, but not the model or the condition. They coded each missed answer’s kind of error, each false alarm’s cause, and whether a wrong answer of the third kind follows from a wrong or misleading statement in the ontology. Cohen’s _𝜅_ over the 112 main items is 0.54 (kind of error), 0.79 (structural detectability), 0.77 (cause of a false alarm) and 0.33 (whether a wrong answer follows from


<!-- page 13 -->

What Does an Ontology Catch? 

the ontology); Table 6 counts the codes both annotators gave. Few wrong answers of the third kind followed from a statement in the ontology. On the private graph, every audited false alarm came from an undeclared term, and no missed answer could be flagged by a structural check. 

# **D.3 Recognising a graph’s vocabulary** 

Each model was also asked, with no tools, to answer each test question from memory (probe a) or to write its query from memory, run on the graph (probe b, public graphs only; GLM on 40 questions per graph); the registered expectations were near zero for answers 

everywhere, and for queries clearly above zero on UniProt and Rhea and near zero on masked graphs (Table 15). Answers from memory are exact for at most 9.8% of the questions on any public graph and 1.1% on the private graph. Queries from memory are exact for many questions on UniProt and Rhea for Sonnet, Haiku and GLM, and for almost none on the masked copy of Rhea, for every model. The other four models score low, but many of their replies contained no usable query, so their low scores do not by themselves show an absence of recall. The agents’ own accuracy also falls on the masked copy, for every model and prompt. Probes on the human-written questions were registered but not run.
