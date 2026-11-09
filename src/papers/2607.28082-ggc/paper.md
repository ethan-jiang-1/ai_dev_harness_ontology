---
source: 2607.28082-ggc.pdf
part: paper
converted: 2026-11-09
converter: pdftotext-layout
---

# GGC: Selective Query Correction for Reliable Text-to-SPARQL Generation · 正文

> 由 `pdftotext -layout` 从 PDF 直接转换，保留原页顺序；两栏页面的左右栏在同一行并排出现，逐行读即可，引用前回 PDF 核。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

                                         GGC: Selective Query Correction for Reliable Text-to-SPARQL Generation

                                                           Yang Ziyi1 , Thanh-Son Nguyen2 , Nguyen Tuan Anh1 , Lihui Chen1 *
                                                      1
                                                          Nanyang Technological University, Centre for Info. Sciences and Systems
                                                                       2
                                                                         Institute of High Performance Computing,
                                                           Agency for Science, Technology and Research (A*STAR), Singapore



                                                                 Abstract                             In the context of RDF-based (Kellogg et al.,
                                              Large language models (LLMs) have demon-             2026) KGs, Text-to-SPARQL is an important
                                              strated strong capabilities in structured query      approach to KGQA. RDF-based KGs represent
                                              generation, making them a natural choice             knowledge as subject-predicate-object triples, and
                                              for Text-to-SPARQL, which translates natural         SPARQL (Harris and Seaborne, 2013) is the stan-
                                              language questions into executable SPARQL            dard query language for RDF data. Therefore,
                                              queries over knowledge graphs. However, their        Text-to-SPARQL aims to translate NLQs into ex-
                                              initial outputs remain unreliable: generated
                                                                                                   ecutable and semantically consistent SPARQL
arXiv:2607.28082v1 [cs.CL] 30 Jul 2026




                                              queries may be executable yet semantically mis-
                                              aligned with input questions, leading to incor-      queries. Compared with direct natural language
                                              rect retrieval. To address this issue, we propose    answer generation, this approach retrieves answers
                                              Generator–Gate–Corrector (GGC), a frame-             through explicit query execution over an external
                                              work for reliable LLM-based Text-to-SPARQL           KG, making the intermediate query and retrieved
                                              generation. GGC first uses a Generator to pro-       graph facts inspectable and facilitating more verifi-
                                              duce an initial query, then applies a Gate to pre-   able and interpretable results (Pan et al., 2024).
                                              dict whether correction is needed, and finally          In recent years, large language models (LLMs)
                                              invokes a Corrector only for selected high-risk
                                                                                                   have demonstrated strong capabilities in natural lan-
                                              queries. This selective correction mechanism
                                              avoids unnecessary modifications and reduces         guage understanding, generation, and code-related
                                              the risk of degrading originally correct queries.    tasks (Brown et al., 2020; Chen et al., 2021). These
                                              Experiments on MCQA show that GGC im-                capabilities make them a natural choice for Text-
                                              proves query-level accuracy from 90.23% to           to-SPARQL, where models must understand user
                                              98.33% while reducing inference overhead by          questions and generate semantically consistent and
                                              45% compared with correcting all generated           executable structured queries.
                                              queries. Ablation studies show that the Gate
                                                                                                      However, Text-to-SPARQL is not merely a text
                                              is robust across thresholds and that Corrector
                                              training data composition affects correction ef-     generation task. Generated queries must be exe-
                                              fectiveness and stability. Overall, the results      cutable while faithfully encoding the entities, rela-
                                              demonstrate that selective correction enhances       tions, constraints, variable bindings, and reasoning
                                              the accuracy, reliability, and efficiency of LLM-    paths expressed in the NLQ (Banerjee et al., 2022).
                                              based text-to-SPARQL generation.                     Since executability alone does not guarantee se-
                                         1    Introduction                                         mantic correctness, LLM-based Text-to-SPARQL
                                                                                                   requires mechanisms to verify consistency with the
                                         Knowledge graph question answering (KGQA)                 original question, especially as LLMs may produce
                                         aims to answer natural language questions (NLQs)          plausible but unfaithful outputs (Xu et al., 2023).
                                         by grounding them in the structured facts of knowl-          Our experiments further show that this prob-
                                         edge graphs (KGs). Existing KGQA methods are              lem is particularly prominent in Text-to-SPARQL.
                                         typically categorized into semantic parsing (SP)-         While the fine-tuned Generator achieves high
                                         based methods and information retrieval (IR)-based        query-level accuracy, many of its remaining errors
                                         methods (Lan et al., 2023). The former generates          are executable yet semantically flawed. We define
                                         logical forms or query structures, while the latter       Generator errors as initial SPARQL queries pro-
                                         obtains answers through entity, relation, or path         duced by the Generator that are judged incorrect
                                         retrieval over the graph.                                 against the ground-truth queries. On the Movie
                                             * Corresponding author: elhchen@ntu.edu.sg.           Complex Question Answering (MCQA) (Hoang

<!-- page 2 -->

et al., 2024) dataset, semantic errors account for       to obtain answers (Lan et al., 2023). These methods
77.70% of Generator errors, while syntactic errors       provide relatively explicit reasoning processes, but
account for only 21.07%. This indicates that rely-       their performance depends heavily on the quality of
ing solely on execution failures to trigger correc-      the generated intermediate structures. In contrast,
tions will miss many semantic errors.                    IR-based methods retrieve relevant entities, rela-
   The key insight of this paper is that in LLM-         tions, or subgraphs from topic entities and obtain
based Text-to-SPARQL, the issue is not only how          answers through path search or neural reasoning.
to generate queries, but also when to correct them.      They are flexible for multi-hop reasoning but are
Correcting all generated results may fix incorrect       often less interpretable than explicit query-based
queries, but it also incurs higher inference over-       methods.
head and may degrade originally correct queries.            Query Graph Generation (QGG) (Lan and Jiang,
In contrast, selective correction concentrates com-      2020) and Neural State Machine-hybrid (NSMh )
putation on high-risk samples, improving accuracy        (He et al., 2021) are representative methods of these
while reducing unnecessary rewriting. Experimen-         two directions respectively. QGG constructs query
tal results show that the proposed Generator–Gate–       graphs with entities, relations, constraints, and an-
Corrector (GGC) framework improves query-level           swer variables, while NSMh improves multi-hop
accuracy from 90.23% to 98.33%, with only about          reasoning by learning intermediate supervision sig-
10% additional inference time over Generator-only        nals. Unlike these methods, we focus on the relia-
inference. Compared with correcting all samples,         bility of LLM-based Text-to-SPARQL generation,
selective correction achieves higher accuracy while      especially how to identify and correct high-risk
reducing inference time by about 45%.                    SPARQL queries after generation. Since QGG and
   In summary, our contributions are as follows:         NSMh are important reference baselines on the
                                                         MCQA dataset, they are included in the experi-
    • We analyze LLM-based Text-to-SPARQL                ments for comparison.
      from a reliability perspective and show that
      executable but semantically flawed queries are     2.2   Text-to-SPARQL and SPARQL Semantic
      a significant source of errors affecting system          Parsing
      performance.                                       With the development of pre-trained language mod-
                                                         els, Text-to-SPARQL has shifted from rule-based,
    • We propose the GGC framework, which per-
                                                         template-based, and task-specific semantic parsing
      forms selective query correction through a
                                                         methods toward generation-based approaches (Lan
      detect-then-correct strategy and achieves a bet-
                                                         et al., 2023). Prior work has compared BART, T5,
      ter balance between accuracy and inference
                                                         and pointer-generator models on LC-QuAD 1.0
      efficiency.
                                                         and LC-QuAD 2.0, showing that pre-trained mod-
    • We conduct systematic experiments and abla-        els provide strong baselines for SPARQL semantic
      tion analyses on MCQA to examine the im-           parsing (Banerjee et al., 2022).
      pact of the Generator, Gate, Corrector, KG ex-        Recent studies have further applied LLMs to
      ecution feedback, and Corrector training data      SPARQL generation (Xu et al., 2023; D’Abramo
      composition, providing empirical evidence for      et al., 2025) over Wikidata (Vrandečić and
      building more reliable Text-to-SPARQL sys-         Krötzsch, 2014). By translating NLQs into exe-
      tems. Additional results on SciQA (Auer et al.,    cutable SPARQL queries, these methods retrieve
      2023), reported in Appendix D.2, further sup-      answers from KGs through an explicit query execu-
      port these findings.                               tion process, improving verifiability compared with
                                                         direct answer generation. More recently, FIRES-
2     Related Work                                       PARQL introduced a modular LLM-based frame-
                                                         work for SPARQL generation over scholarly knowl-
2.1    Knowledge Graph Question Answering                edge graphs (Pan et al., 2025), combining fine-
Existing KGQA methods can generally be divided           tuning, optional retrieval-augmented context, and
into SP-based methods and IR-based methods. SP-          query correction. These studies demonstrate the
based methods convert natural language questions         potential of LLMs for SPARQL generation, but
into logical forms, query graphs, or structured          they pay less attention to the reliability of gen-
queries that can be executed on a knowledge graph        erated queries, especially executable but semanti-

<!-- page 3 -->

cally flawed queries. In contrast, our work focuses      whether the initial SPARQL query is likely to con-
on when post-generation correction should be trig-       tain errors, and then triggers corrections only for
gered. The proposed Generator–Gate–Corrector             high-risk queries. The overall goal is to improve
framework uses a learned Gate to selectively route       query accuracy while reducing unnecessary correc-
only high-risk queries to the Corrector, reducing        tion and additional inference overhead.
unnecessary rewriting and inference overhead.
                                                         3.1   Task Formulation
2.3    Constrained Generation and Error                  Given an NLQ, q, the objective of Text-to-SPARQL
       Correction in Structured Query                    is to generate an executable SPARQL query, s. The
       Generation                                        answer set can be retrieved from the KG by execut-
Text-to-SPARQL and Text-to-SQL are both natural-         ing the query. Compared with general text genera-
language-to-structured-query generation tasks that       tion tasks, Text-to-SPARQL requires the generated
require syntactically valid and semantically correct     queries to satisfy the following requirements: First,
outputs. Therefore, constrained decoding and error       queries must conform to the syntax of SPARQL,
correction methods in Text-to-SQL provide useful         and second, queries must be semantically consis-
references for Text-to-SPARQL.                           tent with original questions.
   For constrained decoding, PICARD (Scholak                The initial query is generated by the Generator,
et al., 2021) constrains autoregressive decoding         denoted as s(0) . If the query is determined to have
through incremental parsing and rejects tokens that      potential errors, a corrected query, s(c) , is generated
violate SQL syntax. For error correction, Text-to-       by the Corrector. The final output query is denoted
SQL works (Chen et al., 2023; Shi et al., 2025)          as ŝ. Therefore, we focus on how to generate s(0)
have shown that post-generation correction can im-       and on how to determine whether it needs to be
prove semantic parsing accuracy, and that struc-         corrected.
tured clause-level editing is often more suitable
                                                         3.2   Generator-Gate-Corrector Framework
than token-level editing for query repair.
   These studies show that improving structured          We separate the Text-to-SPARQL process into three
query generation does not only rely on stronger ini-     stages: initial generation, error detection, and selec-
tial generators, but can also benefit from constraint,   tive correction. The overall process is as follows:
validation, and correction modules.
                                                                             s(0) = G(q)
2.4    Motivation for Selective Correction in
                                                                          g = Gate(q, s(0) )
       LLM-based Text-to-SPARQL                                           (
Existing work has advanced KGQA through                                    s(0) ,      if g = 0
                                                                     ŝ =         (0)
graph reasoning, semantic parsing, and structured                          C(q, s ), if g = 1
query generation. However, LLM-based Text-
                                                         where G(·) denotes the Generator, C(·) denotes
to-SPARQL methods still face reliability issues,
                                                         the Corrector, and g ∈ {0, 1} is the binary output
where executable queries may be semantically in-
                                                         of the Gate. The framework is shown in Figure 1.
consistent with the original question. Inspired by
                                                            Since not all initial SPARQL queries need to be
recent post-correction studies in Text-to-SQL, we
                                                         corrected, triggering the Corrector on all queries
explore post-correction for LLM-based Text-to-
                                                         would significantly increase inference overhead
SPARQL. Unlike prior work focusing mainly on
                                                         and could also corrupt queries that were initially
query generation, our approach emphasizes post-
                                                         correct. Therefore, the Gate in the framework acts
generation error detection and selective correction
                                                         as a query risk assessor, ensuring that the Corrector
to determine when and how corrections should be
                                                         is triggered only on high-risk queries.
applied for improved semantic consistency.
                                                         3.3   Generator
3     Methodology
                                                         The objective of the Generator is to translate an
We propose a Generator–Gate–Corrector frame-             NLQ, q, into an initial SPARQL query, s(0) . We
work to improve the reliability of LLM-based Text-       use a supervised fine-tuned LLM as the Generator.
to-SPARQL generation. Instead of correcting all          During training, the input is the NLQ, and the target
generated queries, this framework first determines       output is the corresponding ground-truth SPARQL

<!-- page 4 -->

         Figure 1: The proposed Generator-Gate-Corrector framework for Text-to-SPARQL generation.


query. During inference, the Generator generates        3.5   Corrector
an initial query s(0) based on the input question.
                                                        The Corrector aims to revise SPARQL queries iden-
   The Generator aims to produce an initial candi-
                                                        tified as high-risk by the Gate. Unlike the Genera-
date query that is as accurate as possible. However,
                                                        tor, the input to the Corrector contains an NLQ and
due to SPARQL’s strict requirements for entities,
                                                        a corresponding initial SPARQL query.
relations, constraints, and variable bindings, the
                                                            The objective of the Corrector is to fix potential
Generator’s output may still contain syntactic or
                                                        errors in entities, relations, constraints, variable
semantic errors. Therefore, the initial query is not
                                                        bindings, or query structure while preserving the
directly considered the final result but is further
                                                        correct parts of the initial query. During training,
passed to the Gate for reliability assessment.
                                                        the Corrector takes an NLQ and an initial query
3.4   Gate                                              produced by the Generator as input, and the corre-
                                                        sponding ground-truth SPARQL query as the target
The Gate is a binary classification module used to
                                                        output.
determine whether the initial SPARQL query needs
                                                            We further consider different training data com-
correction. Its input consists of an NLQ and the
                                                        positions for the Corrector. Using only incorrect
initial query produced by the Generator:
                                                        samples can provide a more direct correction sig-
                  xgate = [q; s(0) ]                    nal, while adding a certain proportion of originally
                                                        correct samples can help the Corrector learn to
   The Gate outputs the probability that correction     maintain stable output when the query is already
is required, and the final decision is obtained based   correct. The impact of different training data com-
on the threshold τ :                                    positions on correction effectiveness and stability
                                                        will be examined in section 4.3.
          g = I [P (g = 1 | xgate ) ≥ τ ]
                                                        3.6   Training and Inference
where, g = 1 indicates that the Corrector is trig-
gered, and g = 0 indicates that the initial SPARQL      Both the Generator and the Corrector are trained
query is kept. The default threshold is τ = 0.5.        using standard supervised fine-tuning, and train-
   Compared with methods that rely solely on ex-        ing samples are constructed using an instruction-
ecution feedback, the objective of the Gate is to       response format. For the Generator, the instruction
identify queries that may contain syntactic or se-      includes a task description and an NLQ, while the
mantic errors, including executable queries that are    response is a ground-truth SPARQL query. For the
semantically inconsistent with the NLQ. This is im-     Corrector, the instruction includes a task descrip-
portant because many incorrect SPARQL queries           tion, an NLQ, and an initial SPARQL query, while
are executable but return answers that do not match     the response is a ground-truth SPARQL query. Dur-
the question. Therefore, the Gate needs to identify     ing training, the language modeling loss is applied
not only syntactic or execution-related errors, but     only to the response portion.
also potential semantic errors.                            The Gate is trained as a separate binary classi-

<!-- page 5 -->

fier. Its training samples consist of an NLQ, an        Setting               Description
initial SPARQL query, and a binary label. If the        Generator-only        No correction; output s(0) .
initial query is incorrect, the label is "Correction    Gen. + Corr.          Correct all initial queries.
Required". If the initial query is correct, the label   Gen. + Gate + Corr.   Selectively correct initial queries.
is "No Correction Required".                            NSMh                  IR baseline reported in MCQA.
                                                        QGG                   SP baseline reported in MCQA.
   The inference procedure is summarized in Algo-
rithm 1:
                                                        Table 1: Evaluated settings and baselines. Gen. denotes
                                                        the Generator, Corr. denotes the Corrector.
Algorithm 1 Generator-Gate-Corrector Inference
Require: Natural language question q
Ensure: Final SPARQL query ŝ                           is used to generate initial queries on the remaining
 1: s(0) ← G(q)                                         training data, and training samples for the Gate and
 2: g ← Gate(q, s(0) )                                  Corrector are constructed accordingly. If the initial
 3: if g = 1 then                                       query generated by the Generator is incorrect, the
 4:      s(c) ← C(q, s(0) )                             corresponding sample is labeled "Correction Re-
 5:      ŝ ← s(c)                                      quired". Otherwise, it is labeled "No Correction
 6: else                                                Required".
 7:      ŝ ← s(0)                                      Compared Settings Table 1 summarizes the com-
 8: end if                                              pared settings in the experiments. Generator-only
 9: return ŝ                                           evaluates the initial generation capability, while
                                                        Gen. + Corr. tests the effect of correcting all ini-
   Through this pipeline, the system selectively cor-   tial queries. Gen. + Gate + Corr. represents the
rects high-risk queries, achieving a better balance     proposed selective correction framework. We also
between accuracy, reliability, and inference effi-      include NSMh and QGG as traditional KGQA ref-
ciency.                                                 erence baselines to assess end-task answer retrieval
                                                        performance. Since these methods do not directly
4     Experiments and Results                           generate SPARQL queries or report query-level
                                                        accuracy, their results are not strictly comparable
This section first introduces the experimental setup    to ours at the query level. Existing LLM-based
and compared systems, then presents the end-to-         Text-to-SPARQL methods are not included as main
end framework results and ablation studies on key       baselines because standardized implementations
components, including the Generator, Gate and its       and evaluation settings remain limited.
threshold sensitivity, KG execution feedback, and       Implementation Details Both the Generator and
Corrector training data composition.                    Corrector are supervised fine-tuned based on
                                                        Llama-3.2-3B-Instruct (Grattafiori et al., 2024),
4.1    Experimental Setup                               employing LoRA (Hu et al., 2022) and 4-bit quan-
Dataset The experiments were conducted on the           tized loading (Dettmers et al., 2023) to reduce train-
MCQA dataset (Hoang et al., 2024). MCQA is a            ing costs. Both used an instruction-response format
complex KGQA dataset for the movie domain con-          to construct training samples and applied the lan-
structed over iMKG, a KG based on Wikidata and          guage modeling loss only in the response portion.
MovieKG. Each sample contains an NLQ, ques-                The Gate is modeled as a binary classifier.
tion type, topic entity, answer, and corresponding      We compare the RoBERTa-based (Liu et al.,
ground-truth SPARQL query. This dataset is built        2019) Gate and the SBERT-based (Reimers and
on a movie-domain KG and is suitable for evaluat-       Gurevych, 2019; Wang et al., 2020) Gate, and use
ing Text-to-SPARQL and KGQA methods.                    the RoBERTa-based Gate, which performed better,
   The dataset includes training, validation, and       as the default setting.
test sets. The training set contains 119,409 sam-       Evaluation Metrics For the Generator, Corrector,
ples, the validation set contains 15,785 samples,       and framework, we report both query-level and
and the test set contains 31,570 samples. We use a      item-level metrics. Query-level accuracy measures
portion of the training data to fine-tune the Gener-    the matching between the answer sets retrieved
ator, enabling it to learn the mapping from NLQs        with generated SPARQL and with the ground-truth
to SPARQL queries. Then, the trained Generator          SPARQL, and is the primary evaluation metric.

<!-- page 6 -->

System                            Query Acc. (%) Item Prec. (%) Item Rec. (%) Item F1 (%) Infer. Time (Total / Q.)
NSMh                                    –             59.20           70.06           59.44               –
QGG                                     –             11.65           25.13           12.32               –
Generator-only                        90.23           37.96           85.76           52.63          ∼30h / ∼3.4s
Gen. + Corr. (correct-all)            92.34           91.62           93.43           92.51          ∼60h / ∼6.8s
Gen. + Gate + Corr. (selective)       98.33           99.62           98.70           99.16          ∼33h / ∼3.7s

Table 2: Main results on MCQA. The proposed selective correction framework achieves the best query-level
accuracy while requiring much less inference time than the correct-all baseline. Gen. denotes the Generator and
Corr. denotes the Corrector. Infer.Time (Total/Q.) refers to both the total inference time on the full test set, and the
average time per test question, respectively.


Item-level precision, recall, and F1 score measure            SPARQL queries, improving accuracy, reliability,
the matching between the answer set obtained by               and inference efficiency.
the generated SPARQL and the ground-truth an-
swer set, and are used for comparison with tradi-             4.3   Ablation Study on the Impact of each
tional KGQA baselines.                                              Component
   For the Gate, we report accuracy, precision, re-           To understand how each component contributes
call, F1 score, false positive rate (FPR), and trigger        to the framework, we conduct ablation studies on
rate. "Correction Required" is considered the pos-            them. We analyze the Generator-only performance,
itive class, and the trigger rate represents the pro-         evaluate the Gate’s ability to identify high-risk
portion of samples that the Gate determines need              queries, and study key design choices including
to proceed to the Corrector.                                  Gate threshold, KG execution feedback, and Cor-
   The detailed experimental setup and prompt tem-            rector training data composition.
plates are summarized in Appendices A and B.                  Generator-only Performance Generator-only
                                                              achieves a query-level accuracy of 90.23%, which
4.2   End-to-End Framework Results
                                                              indicates that the fine-tuned LLM already has a con-
We evaluate the end-to-end GGC framework and                  siderable Text-to-SPARQL generation capability.
compare it with traditional KGQA baselines on                 However, the item-level precision is only 37.96%,
MCQA. The results are shown in Table 2.                       significantly lower than the recall of 85.76%. These
   The proposed framework achieves strong overall             results in Table 2 indicate that although some gener-
performance, reaching 98.33% query-level accu-                ated queries may retrieve the correct answers, they
racy and 99.16% item-level F1. Compared with tra-             also return a large number of irrelevant answers.
ditional KGQA baselines, GGC obtains better item-             In other words, Generator errors are not primarily
level performance, showing that explicit SPARQL               non-executable queries, but are more likely to be
generation combined with selective correction can             semantic errors such as overly broad query scope,
improve final answer retrieval quality.                       incorrect relation selection, missing constraints, or
   However, this comparison should be interpreted             inaccurate variable binding.
carefully because the baselines and our method                   To further analyze the error source of the Gen-
optimize different objectives. Traditional KGQA               erator, we categorized the incorrect samples into
baselines such as NSMh and QGG are designed for               syntax error, semantic error, and ground-truth
answer retrieval, while our framework explicitly              SPARQL error. The results are shown in Table 3.
generates executable SPARQL queries. Since these              As can be seen, semantic errors account for 77.70%
baselines do not report query-level accuracy, they            of the Generator’s errors, significantly higher than
cannot be directly compared in terms of SPARQL                the 21.07% for syntax errors. This indicates that the
generation quality. Therefore, we use them as refer-          main challenge of LLM-based Text-to-SPARQL is
ence baselines for MCQA answer retrieval, rather              not merely generating executable queries, but rather
than as direct Text-to-SPARQL generation base-                generating queries that are semantically consistent
lines.                                                        with the NLQs. Therefore, relying solely on execu-
   Overall, the results show that the proposed GGC            tion failure to trigger correction is insufficient, as
framework achieves competitive answer retrieval               this approach misses a large number of executable
performance by additionally producing explicit                but semantically incorrect queries.

<!-- page 7 -->

  This result supports the necessity of introduc-       that the Gate is essential not only for reducing com-
ing the Gate. The goal of the Gate is to determine      putational cost, but also for avoiding unnecessary
whether a query can be executed, as well as to          correction of originally correct queries.
determine whether the initial query may have se-        Gate Threshold Sensitivity We analyze whether
mantic inconsistencies, thereby deciding whether        the Gate depends on careful threshold tuning. As
the Corrector should be triggered.                      shown in Table 5a, varying the threshold mainly
                                                        introduces a small precision–recall trade-off: lower
   Error Type             Count     Percentage (%)      thresholds trigger more corrections and slightly
   Syntax Error            650           21.07          improve recall, while higher thresholds reduce false
   Semantic Error         2,397          77.70          triggers and slightly improve precision. However,
   Gold SPARQL Error       38            1.23           the overall performance remains stable.
   Total                  3,085            –               When the threshold changes from 0.25 to 0.75,
                                                        the trigger rate only changes from 9.45% to 9.26%,
     Table 3: Error distribution of the Generator.      and the F1 score remains around 94%. This sug-
                                                        gests that the Gate learns stable question-query
Gate Performance To evaluate whether the Gate           mismatch signals rather than relying on a carefully
can identify which queries require correction, we       tuned threshold. We therefore use τ = 0.5 as the
compare the Gate with two backbones, and the            default setting.
results are shown in Table 4.                           Effect of KG Execution Feedback Intuitively,
   Both backbones achieved high classification per-     feedback from KG execution can provide useful
formance, indicating that strong error signals were     information, such as whether the query can be ex-
already present between the NLQ and the initial         ecuted successfully or whether the returned result
SPARQL query. The RoBERTa-based gate is bet-            is abnormal. Therefore, we compare the with-
ter than the SBERT-based gate in recall and F1          feedback and without-feedback settings for both
score. RoBERTa’s recall reached 92.11%, mean-           the Gate and the pipeline.
ing it could cover most queries that truly needed          The results in Table 5b demonstrate that KG
correction. Meanwhile, its FPR was only 0.31%,          feedback improves both Gate performance and end-
indicating it rarely misclassified originally correct   to-end pipeline performance. For example, pipeline
queries.                                                query-level accuracy increases from 98.27% to
   This is particularly important for the entire        98.70%. However, the improvement is relatively
pipeline. If the Gate’s recall is too low, the Cor-     limited, especially on the main query-level metric.
rector will not be triggered for many incorrect         In contrast, the without-feedback setting avoids an
queries. If the FPR is too high, the Corrector          additional execution step before correction, making
may be frequently triggered, corrupting originally      the pipeline simpler and more efficient.
correct queries. Therefore, the Gate’s role is not         Therefore, KG feedback is useful but not essen-
only to reduce inference overhead but also to per-      tial. The strong without-feedback results suggest
form risk screening between correct and incorrect       that the NLQ-SPARQL pairs already contain suffi-
queries. Due to the superior overall performance of     cient signals for detecting semantic errors. Consid-
the RoBERTa-based gate, we use RoBERTa as the           ering both performance and efficiency, the without-
default Gate backbone in subsequent experiments.        feedback setting is more practical as the default
Effect of Selective Correction We further com-          configuration.
pare selective correction with Generator-only and       Effect of Corrector Training Data Composition
Generator + Corrector, where the Corrector is ap-       Finally, we analyze how adding correct samples
plied to all generated queries. As shown in Table 2,    affects Corrector training. We use W to denote
Generator-only achieves 90.23% query-level ac-          initially wrong queries produced by the Generator
curacy with approximately 30 hours of inference         and C to denote initially correct queries. W 1.0
time. Correcting all samples increases the inference    denotes training only on the full set of wrong sam-
time to approximately 60 hours, but only improves       ples, while W 1.0 + C0.2, W 1.0 + C0.5, and
query-level accuracy to 92.34%.                         W 1.0 + C0.8 additionally add correct samples
   In contrast, the complete GGC framework              whose sizes correspond to 20%, 50%, and 80% of
achieves 98.33% query-level accuracy with approx-       all training samples, respectively. Thus, the train-
imately 33 hours of inference time. This indicates      ing set size increases as more correct samples are

<!-- page 8 -->

      Gate Model        Acc. (%)          Prec. (%)        Rec. (%)          F1 (%)          FPR (%)           Trigger Rate (%)
      RoBERTa             98.95             97.00              92.11          94.49               0.31                9.31
      SBERT               98.32             96.45              86.03          90.94               0.34                8.74

                                           Table 4: Comparison of Gate models.

            Threshold      Acc. (%)        Prec. (%)       Rec. (%)        F1 (%)     FPR (%)            Trigger Rate (%)
                 0.25        98.89           95.98           92.57         94.24           0.42                9.45
                 0.50        98.95           97.00           92.11         94.49           0.31                9.31
                 0.75        98.93           97.13           91.79         94.38           0.29                9.26

                                                    (a) Effect of Gate threshold.

       Setting              Gate Acc. (%)         Gate F1 (%)          Pipeline Query Acc. (%)            Pipeline Item F1 (%)
       With feedback              99.36                96.66                       98.70                          99.09
       Without feedback           98.95                94.49                       98.27                          97.72

                                                    (b) Effect of KG feedback.

                 Composition       Query Acc. (%)          Item Prec. (%)          Item Rec. (%)          Item F1 (%)
                 W1.0                     98.27                  97.09                 98.37                 97.72
                 W1.0 + C0.2              98.33                  99.62                 98.70                 99.16
                 W1.0 + C0.5              98.63                  87.66                 98.85                 92.92
                 W1.0 + C0.8              98.80                  99.66                 99.00                 99.33

                                     (c) Effect of Corrector training data composition.

                                      Table 5: Ablation results of the framework.


added.                                                                 5    Conclusion
   As shown in Table 5c, adding correct samples                        In this paper, we presented a GGC framework for
does not weaken the Corrector. Query-level ac-                         reliable LLM-based Text-to-SPARQL generation.
curacy increases from 98.27% under W 1.0 to                            The framework first generates an initial SPARQL
98.80% under W 1.0 + C0.8, suggesting that cor-                        query, uses a Gate to decide whether correction is
rect samples help the model preserve original                          needed, and triggers the Corrector only on high-risk
correct queries and reduce unnecessary rewriting.                      queries, improving accuracy and reliability while
Since larger C ratios also increase training over-                     reducing inference overhead.
head, we use W 1.0 + C0.2 as the default setting in                       Experiments on the MCQA dataset show that
the main experiments to balance performance and                        the main errors of the Generator are executable
training efficiency.                                                   but semantically inconsistent queries. This sug-
   Item-level metrics show some fluctuation. For                       gests that execution failure alone is insufficient for
example, W 1.0+C0.5 achieves higher query-level                        triggering correction. The Gate identifies queries
accuracy than W 1.0 + C0.2, but its item-level pre-                    requiring correction with a low FPR, and the full
cision and F1 are lower, possibly due to outlier                       framework substantially improves query-level ac-
queries with large answer sets. Therefore, we treat                    curacy over both Generator-only and correct-all
query-level accuracy as the primary metric and                         settings. Compared with correcting all generated
item-level metrics as supplementary evidence.                          queries, selective correction achieves higher accu-
   Overall, this ablation suggests that Corrector                      racy while reducing inference time by about 45%.
training benefits from both repair and preservation                       Overall, reliable Text-to-SPARQL requires both
signals: wrong samples teach correction, while cor-                    strong generation capability and effective detection
rect samples discourage unnecessary rewriting.                         of when to correct. The proposed GGC framework
   Additional case studies, subset-level Gate-                         demonstrates the potential of addressing this issue
Corrector coordination analysis and additional                         through a post-hoc and selective correction strategy,
dataset preliminary results are provided in Appen-                     and we hope it will encourage further research in
dices C, D.1, and D.2.                                                 this direction.

<!-- page 9 -->

Limitations                                           Ethical Considerations
While this paper proposes a Genera-                   Our proposed framework focuses on improving the
tor–Gate–Corrector framework for reliable             reliability of LLM-based Text-to-SPARQL genera-
LLM-based Text-to-SPARQL generation and               tion over knowledge graphs. The experiments are
demonstrates its effectiveness on MCQA, we            conducted on an existing KGQA dataset and do not
acknowledge several limitations that warrant          involve collecting private user data or annotating
further exploration in future work:                   sensitive personal information. However, if such
                                                      systems are deployed in real-world applications, in-
  • The main experiments are conducted on             correctly generated SPARQL queries may still lead
    MCQA, a movie-domain dataset with label-          to misleading or incomplete answers, especially
    based SPARQL queries. Although the re-            when the underlying knowledge graph contains
    sults demonstrate the effectiveness of selec-     outdated, biased, or incomplete facts. Therefore,
    tive correction in this setting, evaluation be-   practical deployment should include appropriate
    yond MCQA remains limited in scope. We            validation, uncertainty indication, and human over-
    provide an additional preliminary evaluation      sight in high-stakes scenarios. In addition, extend-
    on another Text-to-SPARQL dataset in Ap-          ing the framework to open-domain or ID-based
    pendix D.2, but more comprehensive exper-         knowledge graphs may introduce risks from entity
    iments across diverse domains, knowledge          linking errors and biases encoded in the knowl-
    graphs, SPARQL formats, and model back-           edge graph, which should be carefully examined in
    bones are needed to further assess the gen-       future work.
    eralizability of the GGC framework. In par-
    ticular, extending the framework to ID-based      Acknowledgment
    SPARQL settings may require additional en-
    tity linking, schema alignment, and relation      This project was supported by Nanyang Technolog-
    grounding mechanisms.                             ical University under the URECA Undergraduate
                                                      Research Programme.
  • Dependence on the Generator’s error distribu-
    tion. The Gate and Corrector are trained using
    the outputs of a specific Generator. Therefore,
    their performance may depend on the error
    patterns of that Generator. When a different
    or stronger base model is used, the Gate and
    Corrector may need to be retrained or adapted.

  • Additional offline computation. Although the
    proposed framework reduces unnecessary cor-
    rection during inference, constructing train-
    ing data for the Gate and Corrector still re-
    quires generating initial SPARQL queries on
    a large number of training samples. This in-
    troduces additional offline computational cost,
    especially when scaling to larger datasets or
    stronger base models.
