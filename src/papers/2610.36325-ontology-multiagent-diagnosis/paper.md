---
source: 2610.36325-ontology-multiagent-diagnosis.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# Ontology-guided multi-agent reasoning for explainable differential diagnosis · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

# Ontology-guided multi-agent reasoning for explainable differential diagnosis 

Roxana Ramona Szomiu, George Ursu, Adrian Groza 

_Artificial Intelligence Research Institute AIRi@UTCN_ 

_Department of Computer Science, Technical University of Cluj-Napoca_ 

Cluj-Napoca, Romania 

Email: Roxana.Szomiu@cs.utcluj.ro, Ursu.Da.George@student.utcluj.ro, Adrian.Groza@cs.utcluj.ro 

**_Abstract_ —Effective differential diagnosis depends on wellstructured and unambiguous patient case descriptions, since incomplete or ambiguous clinical information readily leads to diagnostic errors and inconsistent reasoning. Large Language Models (LLMs) have recently shown promising capabilities in medical question answering and clinical reasoning; however, even when achieving competitive performance on medical benchmarks, they often rely on pattern recognition learned from training data rather than grounded clinical evidence, and can generate plausible yet unsupported diagnostic conclusions. Their reasoning remains largely opaque, making it difficult for clinicians to assess the evidence and rationale behind a given recommendation.** 

**To address this gap, we propose an ontology-guided, multiagent differential diagnosis framework that replicates the iterative reasoning process of physicians. The framework grounds diagnostic inference in a structured, expert-curated medical knowledge base, enabling interpretation of symptoms, clinical findings, or disease relationships, while decomposing diagnosis into explicit, auditable reasoning steps. This ontology-based grounding constrains inference to evidence-backed associations, reducing hallucination and improving diagnostic transparency, traceability, and consistency. The system then identifies the most discriminative missing symptoms and generates targeted followup questions to reduce uncertainty through a process that mirrors to clinical inquiry. Together, these components improve the reliability, explainability, and diagnostic accuracy of AI-assisted differential diagnosis. The source code is publicly available.** **_Index Terms_ —differential diagnosis, multi-agent systems, LLMs, ontology-based reasoning, explainable AI** 

## I. INTRODUCTION 

Differential diagnosis is an iterative process used to distinguish between two or more diseases with similar symptoms. Initial patient notes are often incomplete, making reliable diagnostic decision-making difficult without further investigation. Early evaluations of LLMs in healthcare formulated diagnostic reasoning as a _single-turn question-answering task_ , assuming that all the information required for diagnosis and treatment selection was available at the time of prediction [1]. 

Transitioning from static QA systems [2] to interactive, multi-turn diagnostic dialogues is crucial for clinical decisionmaking. Physicians iteratively collect information through 

> 1Roxana Ramona Szomiu was supported by an Adobe Romania grant. Adrian Groza was supported by the Romanian Hub for Artificial Intelligence (HRIA), funded through the Smart Growth, Digitization and Financial Instruments Program (MySMIS No. 334906). The authors gratefully acknowledge the administrative and technical support provided by the Technical University of Cluj-Napoca during the development of this research. 

targeted questions to reduce uncertainty, highlighting diagnosis as an interactive process rather than a single-step inference. 

Motivated by the potential of LLMs to support differential diagnosis and clinical decision-making [3], we propose an ontology-based multi-agent system (MAS) that replicates iterative clinical reasoning and assists clinicians in diagnosis. 

Our neuro-symbolic framework integrates LLM-based language understanding with ontology-driven symbolic reasoning. Organized into two modules, it employs a task-oriented multi-agent architecture to interpret clinical narratives, extract symptoms, and manage patient interactions. 

The symbolic reasoning module, grounded in medical ontologies (SYMP [4], DOID [5], and HPO [6]), performs transparent disease scoring and differential diagnosis. The module queries the medical knowledge graph (KG) to identify the most informative symptoms that distinguish among competing diagnoses. Based on this analysis, the dialogue-generator agent autonomously formulates targeted Yes/No follow-up questions that efficiently reduce diagnostic uncertainty, and maximize diagnostic information gain. Rather than relying on a single prediction from a fixed set of symptoms, the framework incrementally refines the differential diagnosis as new clinical evidence becomes available. 

By combining LLMs with ontology reasoning, the proposed MAS supports an adaptive and explainable diagnostic workflow. Explainability is achieved through traceable decisionmaking: mathematical scoring functions rank diagnoses based on extracted evidence and ontology relationships. The system links each refinement with the contributing symptoms and scores, allowing clinicians to transparently interpret the reasoning behind the diagnosis. This enables a transparent, clinically meaningful interpretation of the diagnosis and its reasoning by clinicians. 

In summary, our main contributions are as follows: 

- ontology-guided multi-agent framework: We propose a neuro-symbolic framework that separates language understanding from clinical reasoning and grounds diagnostic scoring in expert-curated ontologies, reducing LLM hallucinations. 

- interactive clinical reasoning: The system generates targeted follow-up questions for missing discriminative symptoms, reducing diagnostic uncertainty and compensating for up to 30% loss in initial symptom disclosure.


<!-- page 2 -->

- traceable explainability: Mathematical scoring functions rank diagnoses at each stage, enabling traceable diagnostic refinement. 

# II. RELATED WORK 

Singhal et al. [7] introduced Med-PaLM2, a medical LLM that achieved expert-level performance in several clinical question-answering benchmarks, including 86.5% accuracy on MedQA, representing a more than 19% improvement over Med-PaLM [8]. However, single-turn question-answering has a key limitation: even fully specified symptoms rarely finalize a diagnosis. In practice, doctors must actively gather missing information through targeted follow-up questions. 

Muntean et al. [9] demonstrate that Med-PaLM2 can provide accurate and clinically appropriate responses for patient education tasks, to ophthalmology-related questions. However, the interaction is limited to a single-turn exchange, which prevents the model from clarifying ambiguities or refining differential diagnoses through iterative dialogue. This limitation motivates a shift from static QA benchmarks to interactive diagnosis, where diagnoses are progressively refined through iterative doctor-patient questioning. 

The Q4Dx [10] benchmark evaluates the strategic inquiry capability of diagnostic systems. It assumes real encounters begin with incomplete, noisy descriptions, requiring doctors to recover missing information through adaptive, contextdependent questioning. Synthetic patient notes are generated from the SymbiPredict dataset [11] at various completeness levels (100%, 80%, 50%). GPT-4.1 and GPT-4o-mini agents simulate patient-physician interactions to assess diagnostic uncertainty reduction over multiple turns. The study reveals that while partial information significantly reduces single-shot diagnostic performance, interactive questioning can recover much of this loss, underscoring the importance of dialoguebased reasoning in clinical diagnosis. Baseline accuracy declines from 51% to 44% and 37% as symptom disclosure decreases from 100% to 80% and 50%, respectively. 

Recent work on interactive clinical reasoning introduces complementary benchmarks and frameworks that together advance multi-turn diagnostic modeling. MedKGI [12] improves diagnostic dialogue by grounding reasoning in medical knowledge graphs, selecting questions based on information gain, and maintaining structured state tracking, leading to more efficient and coherent interactions. MedPI [13] evaluates flagship models across 7,100 simulated conversations, showing that despite strong static benchmark performance, LLMs struggle with full patient-clinician dialogues. Similarly, MINT [14] highlights issues like premature diagnostic commitment, sensitivity to misleading evidence, and limited self-correction. They show that delayed questioning and structured evidence presentation significantly improve accuracy by up to 62,6% . Overall, these studies demonstrate that effective clinical diagnosis requires grounded, multi-turn, and temporally aware reasoning rather than single-step prediction. 

Gond et al. [15] introduce MedDialogRubrics, a benchmark of 5,200 synthetic patient cases and over 60,000 expert-refined 

rubrics for multi-turn clinical consultations, and show that even strong models (e.g., Gemini-2.5-Pro) miss nearly half of the must-ask questions. Their analysis shows that diagnostic performance peaks at approximately 10-11 turns and declines with longer interactions. These findings motivate limiting the interviewer agent to 11 follow-up questions, which maximizes accuracy while avoiding reduced diagnostic alignment and unnecessary consultation length. 

MedAgents [16] is one of the first multi-agent collaboration frameworks designed specifically for the medical domain. Evaluated on nine multiple-choice datasets, MedAgents reaches an average accuracy of 86.7% with GPT-4, slightly above a stronger few-shot CoT (Chain-of-Thought) baseline despite using no in-context examples. 

# III. METHODOLOGY 

MedMAS-DDX is a multi-agent system (MAS) that treats differential diagnosis as a multi-step process, not a single inference. It translates patient’s free-text complaint to a ranked, explained list of probable diseases through a sequence of transformations: unstructured language becomes structured symptoms, symptoms become candidate diseases, and candidate diseases are organized into an initial ranking representing the differential diagnosis. That ranking is then sharpened by a short exchange of questions, and the answers are fed back into the scoring to produce the final diagnosis. 

Two principles govern every step. First, responsibility is split by reliability: language models handle only natural language understanding and generation, while all rankingrelated computations are done by deterministic code, ensuring that diagnosis does not depend on model-based calculations. Second, all medical knowledge is stored in an external curated source and is explicitly queried during the process, rather than being learned from the model’s parameters. 

MedMAS-DDX realizes the preceding principles as a neurosymbolic pipeline in which a small set of LLM-based agents is embedded within, and coordinated by, a deterministic control layer (Figure 1). The multi-agent system is implemented using the CrewAI<sup>1</sup> framework, which manages agent definition and execution. Each agent is designed as a distinct role-goalbackstory persona operating based on the same LLM (via LiteLLM<sup>2</sup> ), with specialized, non-interchangeable functions. 

The system consists of four agents: (i) a symptom extraction agent ( _symptom_ _<u>extractor</u>_ ), (ii) an interviewing agent ( _followup_ _<u>interviewer</u>_ ), (iii) an explanatory agent ( _diagnosis_ _<u>refiner</u>_ ), (iv) a patient agent ( _patient_ _<u>simulator</u>_ ) used only to drive automated evaluation and never contributes to a live diagnosis. The first three agents participate in the diagnosticmaking process, while the last agent simulates the patient. 

The MAS is characterized by high control over execution, predictable processing paths, making it well-suited for strict business logic. In this architecture, agents communicate indirectly through deterministic Python-based coordination. This 

> 1https://crewai.com/ 

> 2https://www.litellm.ai/


<!-- page 3 -->

<!-- Start of picture text -->
Deterministic Layer<br>Deterministic Score<br>Deterministic Differential<br>Patient Text SymptomMapping Initial Ranking Profile Retrieval Patient Answers RefinementTool Final Diagnosis<br>Semantic Layer<br>LLM AgentSymptomExtractor Lookup Profiles InterviewerLLM AgentFollow-up LLM AgentSimulatorPatient Diagnosis TaskLLM Agent<br>Knowledge Layer<br>Ontologies &<br>Graph Database<br><!-- End of picture text -->

Fig. 1: System components and their interactions. 

control layer validates and transforms intermediate representations, ensuring structured, code-mediated interactions rather than unconstrained agent-to-agent dialogue. The diagnosticmaking pipeline allocates specific tasks to three active agents during a live diagnosis, while a fourth persona is reserved exclusively for methodological validation. 

# _A. Symptom extractor agent_ 

The symptom extractor agent, an LLM-based component without external tool access, constitutes the first step of the pipeline by parsing the patient’s initial, natural-language clinical note - often incomplete and informal - and transforming it into a structured intermediate representation of symptoms. For each identified symptom, it generates a canonical medical term, alternative phrasings, and optional contextual details such as duration or location, while keeping descriptive information separate from standardized terminology to ensure consistency and support ontology matching in the next step. 

Our solution follows the methodology of extracting information from unstructured clinical notes and map them to corresponding ontology terms [17], [18]. According to this, in the second phase of the pipeline, the linking symptoms to diseases process occurs in two stages- _resolution and retrieval_ - and constitutes the first interaction with external knowledge. In the _resolution stage_ , each symptom is deterministically mapped to a standard medical concept through an ordered matching process that first attempts the canonical term, then alternative phrasings, and finally a secondary synonym vocabulary. Unresolved symptoms are retained for traceability, but excluded from further processing to avoid affecting the following inference steps. 

In the _retrieval stage_ , resolved concepts query a knowledge graph of expert-defined symptom-disease relationships via a consolidated lookup. Diseases enter the candidate set only if explicitly linked to at least one patient symptom, ensuring grounding in verifiable knowledge. 

All medical knowledge is stored in a GraphDB<sup>3</sup> triple store and queried exclusively via SPARQL, ensuring no diseasesymptom relations are drawn from LLM hallucinations. 

3https://graphdb.ontotext.com/ 

The knowledge base spans two repositories: one for the Symptom (SYMP) and Human Disease (DOID) Ontologies, and another for the Human Phenotype Ontology (HPO), acting as a synonym bridge during resolution. Since queries are executed in Python rather than by LLM-based agents, knowledge access remains uniform, inspectable, and model-independent. 

The retrieved candidate diseases and their associated symptoms advance to the third phase: ranking. Here, diseases are deterministically ranked based on symptom matches, assigning higher weights to rarer, more informative symptoms to produce the initial differential diagnosis. 



<!-- Start of picture text -->
1<br>specificity weight ( s ) = (1)<br>log2(1 +  Nd ( s ))<br><!-- End of picture text -->

Eq. 1 encodes a key idea that rare symptoms are more informative than common ones. Let _Nd_ ( _s_ ) denote the number of diseases associated with symptom _s_ in the KG, and the logarithm reduces the impact of very large disease counts. If a symptom _s_ appears in many diseases, then _Nd_ ( _s_ ) is large, the denominator is large so weight becomes small (low specificity). If a symptom _s_ appears in few diseases, then _Nd_ ( _s_ ) is small, the denominator is small so weight becomes large (high specificity). 

For each candidate disease _d_ , a raw diagnostic score is computed by summing the diagnostic weights of all matched symptoms: 



<!-- Start of picture text -->
raw score ( d ) = � specificity weight ( s ) (2)<br>s∈ matched( d )<br><!-- End of picture text -->

A _coverage factor_ measures the proportion of the patient’s mapped symptoms explained by each candidate disease _d_ : 



<!-- Start of picture text -->
match count ( d )<br>coverage ( d ) = (3)<br>total mapped symptoms .<br><!-- End of picture text -->

_match_ _<u>count(d)</u>_ denotes symptoms matched by disease _d_ , while _total_ _<u>mapped symptoms</u>_ denotes all successfully mapped symptoms. The _coverage_ factor rewards diseases explaining a larger fraction of reported symptoms, complementing the informativeness-based raw score.


<!-- page 4 -->

The raw score 2 and the coverage factor 3 are then combined into a final _composite score_ : 

_comp_ _<u>score</u>_ ( _d_ ) = _raw_ _<u>score</u>_ ( _d_ ) _×_ �0 _._ 5+0 _._ 5 _×coverage_ ( _d_ )� (4) The _composite score_ combines two complementary aspects of diagnostic quality: the strength of supporting evidence and the completeness of symptom coverage. Here, _raw_ _<u>score(d)</u>_ measures the total diagnostic evidence for disease _d_ , computed from the weighted contributions of matched symptoms. In contrast, _coverage(d)_ measures how much of the patient’s symptom set is explained by the disease _d_ . 

The term (0 _._ 5+0 _._ 5 _·_ coverage( _d_ )) is a bounded scaling factor in [0.5,1] that adjusts rather than dominates the raw score. It ensures that coverage acts as a soft adjustment to the diagnostic evidence: when (coverage(d)=0), the score is reduced but not eliminated (scale (=0.5)), while full coverage preserves the raw score (scale (=1)). This design prevents excessive penalization of low-coverage candidates while maintaining stable ranking behavior and balancing evidence strength with explanatory completeness. 

An inclusive threshold then keeps every candidate that is plausibly relevant: those that reach a small fraction of the leading score, or that match at least two symptoms. The threshold is set to a low value on purpose because a candidate discarded here cannot be recovered later. At this stage, a single remaining candidate is returned directly; otherwise, the process proceeds to questioning. 

# _B. Follow-up interviewer agent_ 

When multiple candidate diseases remain, the system enters a differentiation phase. The characteristic symptom profiles of the leading candidates are retrieved from the knowledge source and combined with the current ranking and reported symptoms to form an enriched state. The follow-up interviewer agent is responsible for resolving ambiguities and collecting missing clinical information. The interviewer agent filters non-discriminative and previously reported symptoms, selects patient-observable ones, and generates targeted Yes/No questions to refine the differential diagnosis. 

At this stage, we have a human-in-the-loop interaction point in the system. After the system generates follow-up questions, the process stops temporarily to allow the patient (or user) to respond. The responses are constrained to a simple, structured format-“yes”, “no”, or “unsure”-which makes the input easy to process deterministically and avoids ambiguity in following reasoning steps. The mechanism that collects the answers is kept separate from the diagnostic logic, so the same pipeline runs unchanged whether answers come from a command line, a web interface, or an automated non-interactive source. This step turns a one-shot classification into a consultation. The system has formed the initial hypotheses and identified the most informative missing facts, and it obtains exactly those before concluding, much as a clinician narrows the possibilities through targeted questioning. 

# _C. Patient simulator agent_ 

To ensure rigorous and automated pipeline evaluation, a fourth persona is employed exclusively as a testing mechanism. The patient agent receives a fully specified case description and generates responses to the questions posed by the _followup_ _<u>interviewer</u>_ , based only on the information contained in the current case. This agent operates entirely outside the production environment, with no external tool access and no involvement in live diagnostic sessions, serving exclusively for system validation purposes. 

# _D. Diagnosis refiner agent_ 

The diagnosis refiner agent serves as the final analytical component of the live diagnostic process, synthesizing all iteratively collected findings into a coherent medical conclusion. It uses confirmed symptoms and disease-symptom relations retrieved from GraphDB to produce a final diagnosis with a clear, evidence-based explanation. 

The patient agent’s answers are reintroduced into the pipeline and used to update the differential diagnosis through deterministic scoring. For each queried symptom _s_ , a _discriminative weight_ is computed as: 



<!-- Start of picture text -->
with symptom ( s )<br>discriminative weight ( s ) = 1  − diseases<br>nprofiled<br>(5)<br><!-- End of picture text -->

The _diseases_ _<u>with symptom(s)</u>_ denotes the number of profiled candidate diseases that present symptom _s_ , and _nprofiled_ is the total number of profiled candidate diseases. This weight quantifies the ability of a symptom to distinguish among the remaining candidates: symptoms shared by many diseases receive lower weights, whereas symptoms present in only a few candidates receive higher weights. Consequently, responses to highly discriminative symptoms have a greater influence on the final ranking, while common symptoms contribute less because they provide limited additional diagnostic information. This approach penalizes common features, similar to the established IDF (Inverse Document Frequency) principle in information retrieval. However, rather than adopting the standard logarithmic scaling of IDF (log( _nprofiled/diseases_ _<u>with symptom</u>_ ( _s_ )) ), Eq. 5 utilizes a linear complement. This design choice is tailored to the specific constraints of the diagnostic pipeline and bounds discriminative weights to [0, 1), ensuring mathematical stability in subsequent multiplicative score updates. Moreover, while logarithmic smoothing is necessary for massive document corpora, a linear formulation provides a more distinct and clinically intuitive separation of symptom specificity when evaluating the small and dynamic pools of candidate diseases typical in differential diagnosis. 

For each disease, only the relevant questions are considered, that is, those whose symptom lies in its profile. The _discriminative_ _<u>weights</u>_ of the confirmed symptoms and of the denied symptoms are summed and normalised by the number of relevant questions into a _support term_ and a _conflict term_ .


<!-- page 5 -->

These adjust thfe prior _composite score_ 4 through a bounded multiplicative update: 



<!-- Start of picture text -->
final score ( d ) =  composite score ( d )  ×<br>�1 +  α support norm ( d )  − β conflict norm ( d )� (6)<br><!-- End of picture text -->

where confirmations increase the score and denials decrease it according to their discriminative weights. 

Both the _support_ _<u>term</u>_ and the _conflict_ _<u>term</u>_ are normalized to the [0 _,_ 1] interval. The hyperparameters _α_ and _β_ control the relative contribution of supporting and conflicting evidence, respectively. Given that supporting evidence has substantially greater diagnostic significance than conflicting evidence in our framework, we established _α_ = 0.6 and _β_ = 0.2. These values were derived by empirical hyperparameter tuning on a validation subset. We systematically evaluated multiple parameter configurations and the combination of _α_ = 0 _._ 6 and _β_ = 0 _._ 2 yielded optimal diagnostic accuracy and rank stability. This configuration reflects a fundamental diagnostic principle: the presence of a highly specific symptom is typically stronger positive evidence for a disease than its absence is negative evidence, as symptoms may be unobserved by the patient, or simply delayed in their onset. 

In contrast, higher conflict-penalty weights ( _β_ = 0 _._ 4 and _β_ = 0 _._ 6) overly penalized plausible diagnostic candidates with temporarily unobserved symptoms, leading to their premature elimination from the differential. 

By limiting _β_ relative to _α_ , the model keeps the adjustment factor bounded, allowing follow-up responses to refine the initial diagnostic ranking without replacing it or artificially amplifying previously established evidence. The candidates are re-ranked and the most influential answer is identified. 

When the final diagnosis is determined, the language model returns to explain. It receives the computed scores and states, for each disease, why it rose or fell in the ranking. Each disease’s confidence is determined by the score margins instead of being asserted: high for a clear leader, cautious when the margin is narrow. The output is therefore a reranked differential in which every disease carries a calibrated confidence and an transparent, evidence-based explanation. 

# IV. EXPERIMENTS AND RESULTS 

This section evaluates MedMAS-DDx based on its diagnostic trajectory -its ability to acquire missing information through follow-up questions and iteratively refine the differential diagnosis - rather than as a static classifier. 

The active agents access LLMs via LiteLLM (remote API or self-hosted vLLM). All deterministic scoring and ranking processes run locally, independent of the LLM host. Section IV-C traces one evaluation case end to end to illustrate the mechanism concretely. 

# _A. Evaluation of framework and experimental setup_ 

The framework is evaluated on the Q4DX benchmark [10] using _PatientCases.csv_ (99 cases, 29 diagnoses) at two 

symptom-completeness levels: 80% and 50%. The 100% setting is excluded because no symptoms remain for follow-up. This yields _N_ = 198: 99 samples at 80%, 99 samples at 50%. 

Follow-up questions are answered by a deterministic simulated patient agent with access to the full symptom profile (case 100%), providing an optimistic estimate of interactive information recovery rather than real-patient performance. Diagnostic correctness is measured using SapBERT cosine similarity with the reference label (target diagnosis), using a 0.6 threshold to tolerate differences in medical terminology. 

# _B. Diagnostic accuracy and interactive refinement_ 

Symptom mapping was verified before assessing accuracy: 91.3% of 1,243 symptoms were mapped to ontology concepts. As Figure 2 illustrates, direct matching to the primary SYMP ontology covered 77.3% of symptoms. To minimize information loss, a sequential fallback strategy queried unresolved symptoms against the HPO ontology, recovering an additional 14.0% (e.g., “passage of gases” _→_ flatulence) and capturing expressions absent from SYMP. 

The remaining 8.7% unmapped symptoms primarily result from the LLM extracting overly complex descriptions lacking direct ontology equivalents. Furthermore, the fallback mechanism’s lexical tolerance occasionally introduces semantic errors (e.g., mapping “unsteady” to “hemodynamic instability”). 



<!-- Start of picture text -->
Primary (SYMP) Fallback (HPO) Unmapped<br>77.3% 14.0% 8.7%<br>0 20 40 60 80 100<br>Proportion of Extracted Symptoms (%)<br><!-- End of picture text -->

Fig. 2: Distribution of symptom mapping resolution 

Interactive refinement (Phase 2) consistently improves the zero-shot differential (Phase 1). Of the 42 correct top-1 predictions in Phase 2, only 6 were exact string matches, validating our use of semantic evaluation (SapBERT) over strict string matching. 

At the aggregate level, interactive refinement (Phase 2 follow-up) improves on the zero-shot differential (Phase 1) across every metric, including the mean semantic similarity of the top-ranked prediction computed with SapBERT semantic evaluation at the 0 _._ 6 threshold.(Table I). 

TABLE I: Global diagnostic accuracy: Phase 1 and Phase 2 

|**Metric**|**Phase 1**|**Phase 2**|
|---|---|---|
|Top-1 accuracy|18_._7% (37_/_198)|21_._2% (42_/_198)|
|Top-3 accuracy|25_._8% (51_/_198)|27_._3% (54_/_198)|
|Mean similarity (top-1)|0_._449|0_._466|
|Mean similarity (top-3)|0_._523|0_._537|



Table II presents an analysis of the mean semantic similarity per disclosure variant computed with SapBERT, identifying an important compensatory mechanism to our multi-agent architecture. By engaging in targeted follow-up questions, the system successfully recovers diagnostic confidence, matching the zero-shot baseline of cases with significantly richer initial


<!-- page 6 -->

narratives. This finding demonstrates that the interactive dialogue actively bridges the clinical information gap, effectively compensating for a 30% loss in initial symptom disclosure. 

TABLE II: Mean semantic similarity: Phase 1 (initial differential) and Phase 2 (after follow-up) 



<!-- Start of picture text -->
Completeness Variant Phase 1 Phase 2<br>80% Completeness 0 . 4589 0 . 4792<br>50% Completeness 0 . 4394 0 . 4527<br>Phase 1 (ZDA) Phase 2 (Refined)<br>30 . 3<br>30 26 . 324 . 2 24 . 2 25 . 3<br>21 . 2<br>20 16 . 2 18 . 2<br>10<br>0<br>T1 (50%) T3 (50%) T1 (80%) T3 (80%)<br>(%)Accuracy<br><!-- End of picture text -->

Fig. 3: Top-1 and Top-3 accuracy comparison between the initial Phase 1 and the interactively refined Phase 2. 

Figure 3 summarizes the results and shows, that refinement is not uniformly advantageous: performance improves from phase 1 to phase 2 in all cases, except for a slight decrease in Top-3 accuracy at 50% completeness. We use the Zero-shot Diagnostic Accuracy (ZDA) metric from the benchmark [10] for phase 1. This asymmetry, together with Case #96 below, is presented in the Discussions section. 

_C. Qualitative case study: Recovering the diagnosis of Hepatitis A (Case #96)_ 

To illustrate how a single follow-up answer can reorder a competitive differential, we trace Case #96 ( _Hepatitis A_ , 80% completeness) end to end. Its canonical profile includes ten symptoms; the 80% narrative omits _yellowish skin_ and _yellowing of eyes_ - i.e., jaundice, the most discriminative sign for hepatitis. The clinical narrative given to the pipeline at this completeness level reads as follows: 

_A 32-year-old male presented to the clinic with troubling symptoms, including persistent_ **_joint pain_** _that has worsened over the past two weeks. He reported episodes of_ **_vomiting_** _,_ **_nausea_** _, and a noticeable_ **_loss of appetite_** _. Moreover, he has been suffering from_ **_abdominal pain_** _, accompanied by_ **_diarrhea_** _. He also noted a_ **_mild fever_** _and_ **_muscle pain_** _that has hindered his daily activities, which has led to increased concern regarding his health status._ 

_a) Phase 1a:_ The _symptom_ _<u>extractor</u>_ maps all eight symptoms present in the narrative to SYMP concepts (8 _/_ 8); _jaundice_ is simply absent from the text, not lost in mapping. 

_b) Phase 1b:_ Without the _”jaundice”_ symptom, _”gastrointestinal anthrax”_ and _”oropharyngeal anthrax”_ lead with a _composite score_ of 0 _._ 922 (Eq. (4)), driven by the high 

_specificity weight_ of _”severe diarrhea”_ (Eq. (1)). Four _”hepatitis”_ subtypes (A, B, C, E) tie just below at 0 _._ 861. The top prediction’s SapBERT similarity to _”Hepatitis A”_ is only 0 _._ 340 - an incorrect Top-1. Although the correct label is tied for third place, the prediction is still considered correct under the Top-3 metric. 

_c) Phase 1c:_ The _followup_ _<u>interviewer</u>_ asks eleven targeted Yes/No questions (about ascites, acholic stool, dark urine, jaundice, liver inflammation, hematemesis, hematochezia, dyspnea, backache, headache, cough); the simulated patient confirms only _”jaundice”_ and denies the others. 

_d) Phase 2.:_ Confirming _”jaundice”_ (Eq. (5)) raises _Hepatitis A, B, and C_ to 0 _._ 872 despite three denials; _”Hepatitis E”_ gains less, since an added denial on _dark urine_ drops it to 0 _._ 838. Both _”anthrax”_ candidates receive no support and four denials, falling to 0 _._ 781, below all four _”hepatitis”_ subtypes. 

_e) Outcome: ”Hepatitis A”_ becomes the top prediction, with similarity rising from 0 _._ 340 to a perfect 1 _._ 0 - the largest jump in the entire batch. A single confirmed symptom, combined with tie-aware scoring at the group level, was enough to resolve the ambiguity among six equally scored Phase 1 candidates, which remained unresolved from the initial narrative alone. 

To demonstrate the explainability of the final output, Listing IV-C0e shows a subset of the structured reasoning trace generated by the system for the top candidate, _Hepatitis A_ . 

Listing 1: Agent-generated reasoning trace for the refined diagnosis of Hepatitis A 

|1<br>"rank": 1,|
|---|
|2<br>"disease": "hepatitis A",|
|3<br>"baseline_score": 0.861,|
|4<br>"followup_support": 0.095,|
|5<br>"followup_conflict": 0.083,|
|6<br>"final_score": 0.872,|
|7<br>"updated_confidence": "HIGH",|
|8<br>"reasoning": "Hepatitis A initially had a|
|score of 0.861. Follow-up questions|
|provided support by confirming the|
|presence of jaundice (weight +0.733),|
|but conflicted by denying ascites (|
|weight -0.467), acholic stool (weight|
|-0.733), and liver inflammation (|
|weight -0.733). The net effect was an|
|increase in the final score to 0.872,|
|with updated confidence rated as HIGH"|



# _D. Comparative analysis against the MedQDx baseline_ 

Figure 4 compares MedMAS-DDx against the MedQDx baseline (GPT-4.1) across both accuracy metrics and completeness levels. MedQDx achieves higher zero-shot Top-1 accuracy (44% at 80%; 37% at 50%), reflecting a different task formulation rather than better reasoning: as an openvocabulary classifier, it is never penalized for missing labels at the benchmark’s exact granularity, whereas MedMAS-DDx grounds each candidate in an explicit knowledge graph and refuses to generate a diagnosis with no ontology correspondent. This constraint enables greater explainability and traceability,


<!-- page 7 -->

<!-- Start of picture text -->
MedQDx (Top-1) MedMAS-DDx (Top-1)<br>MedMAS-DDx (Top-3)<br>44<br>40 37<br>30 . 3<br>24 . 2 24 . 2<br>20 18 . 2<br>0<br>50% Variant 80% Variant<br>(%)Accuracy<br><!-- End of picture text -->

Fig. 4: Performance comparison: MedQDx vs MedMAS-DDx 

as each prediction can be linked to structured evidence and a transparent reasoning process. 

Figure 4 shows the same comparison at Top-3, the appropriate granularity for a differential diagnosis: the gap narrows to 30 _._ 3% vs. 44% at 80% completeness, but less so at 50% (24 _._ 2% vs. 37%), where Top-3 also falls below its own Phase 1 value - the same pattern discussed above. 

The two systems also differ sharply in question budget: 2 _._ 4 for MedQDx versus roughly ten for MedMAS-DDx, a direct consequence of confirming specific ontology-mapped symptoms rather than a single free-form hypothesis. Whether this cost is acceptable depends on the deployment context, discussed further in the Discussion. 

# V. DISCUSSIONS AND LIMITATIONS 

In this section, we discuss the behavioral characteristics and the possible limitations of the proposed system. 

Our approach uniquely coordinates specialized agents via deterministic control logic rather than unconstrained communication. This architecture provides predictable execution, allowing validation of every intermediate decision. Consequently, the system suits safety-critical applications where reproducibility and auditability are essential. 

The system leverages multi-turn questioning to progressively enrich the clinical picture. When initial input is sparse, the interaction naturally shifts toward targeted questions that collect discriminative evidence. Each turn refines the differential diagnosis by incorporating new responses into the ranking, enabling gradual convergence toward accurate conclusions. This highlights the strength of structured dialogue in improving diagnostic precision while maintaining transparent, traceable reasoning. 

Overall, the contribution of interactive refinement is real but modest, and at 50% completeness it is not even uniformly positive: Top-1 accuracy improves at both completeness levels (Fig. 3), but Top-3 accuracy improves only at 80% completeness (25 _._ 3% _→_ 30 _._ 3%) and decreases slightly at 50% (26 _._ 3% _→_ 24 _._ 2%), a pattern that also makes the narrowing of the gap with the MedQDx baseline uneven across variants. 

However, the case study (Section IV-C) reveals a different dynamic. Case #96 shifts one instance’s Top-1 similarity from 0 _._ 340 to 1 _._ 0 by resolving ambiguity among six equally scored candidates via a single targeted confirmation. When initial 

ambiguity exists, refinement resolves it decisively. Conversely, if one diagnosis dominates or no candidate is sufficiently close to the reference label, refinement has no actionable uncertainty, yielding a zero measured contribution by construction. 

The Top-3 drop at 50% completeness arises because incomplete symptom information admits weak candidates into the Top-3. Follow-up evidence legitimately replaces these incidental candidates via the score update (Eq. (4)) with better-supported ones, occasionally reducing Top-3 accuracy. Aggregating cases with and without resolvable ambiguity inherently understates refinement’s per-case impact; case-level trajectories provide a more faithful assessment of the followup loop. 

Despite the advantages, several limitations should be acknowledged. First, the quality of the differential diagnosis depends on the completeness and accuracy of the underlying biomedical ontology and its symptom-disease associations. Missing, incomplete, or outdated knowledge cannot be incorporated into the reasoning process. 

Other key limitation in medical diagnosis tasks is the mismatch between ontology terminology and dataset terminology, which arises from the gap between formal, structured medical knowledge (ground truth) and the context-dependent, heterogeneous language used in clinical data as it is recorded in realworld practice. This gap limits the alignment of patient data with ontology concepts, affecting tasks such as symptomsdisease mapping or information extraction. This limitation is partially mitigated by the extensive validation and widespread adoption of biomedical ontologies in research [19], [20], [21] that explicitly leverage DOID or HPO, which provide a robust semantic foundation for clinical reasoning and as well as their successful application in ontology-based systems across various domains [22], [23]. 

The knowledge base’s limitations are exposed by two reference labels, _Jaundice_ and _Vertigo_ : while the Q4Dx benchmark treats them as diagnoses, SYMP classifies them as symptoms. Because MedMAS-DDx candidates must correspond to explicit disease concepts in the knowledge graph, the system cannot output either label as a diagnosis, regardless of reasoning quality. This stems directly from ontology coverage, not the reasoning pipeline. For _Jaundice_ , this limitation is absolute: it is never proposed as a candidate disease. Instead, the system retrieves ontology-supported diseases featuring _jaundice_ (e.g., _Hepatitis E, D_ ) and queries it as follow-up evidence. Accuracy here remains zero until the ontology is explicitly extended. 

Analyzing unresolved cases post-Phase 2 reveals that errors stem primarily from structured reasoning constraints rather than language understanding. Typical errors involve: (1) conceptual mismatches, where the benchmark treats symptoms as diagnoses; (2) knowledge graph sparsity, where exact symptom-disease associations are absent despite highly accurate symptom extraction (88.4% mapping); (3) diagnostic granularity, where the system robustly identifies the broader disease family but struggles to isolate exact subtypes without specific laboratory results. 

Consequently, employing a more advanced LLM would not


<!-- page 8 -->

resolve these errors, as its role is deliberately restricted to semantic translation. These unresolved cases highlight an intentional limitation of our neuro-symbolic design: constraining inference to a curated knowledge graph structurally prevents hallucinating statistically plausible but unsupported diagnoses. This trade-off caps benchmark performance to guarantee transparent, clinically safe decision-making. 

Finally, the restricted interaction model limits follow-up responses to ”yes/no/unsure.” While supporting deterministic scoring and reproducibility, this fails to capture nuanced clinical information like symptom severity or temporal progression. 

# VI. CONCLUSION AND FUTURE WORK 

Overall, the methodology forms a directed pipeline with a single feedback loop: free text is transformed into structured symptoms, generating candidate diseases consolidated into an initial ranking that either terminates or triggers targeted questioning. The follow-up answers are then reintegrated into the scoring stage. Throughout the pipeline, each component has a distinct role: language models perform interpretation and generation, the external knowledge source provides symptomdisease associations, and deterministic code handles ranking, evaluation, and control flow. A sparse initial description simply produces a weaker initial ranking and shifts more work onto the questioning stage, allowing the inquiry depth to adapt to initial uncertainty. This consistency keeps the process transparent at all stages. 

The evaluation of the proposed method showed that interactive refinement improved global Top-1 accuracy from 18.7% to 21.2% and Top-3 accuracy from 25.8% to 27.3%. Notably, targeted follow-up questions recovered diagnostic confidence to levels comparable to the zero-shot semanticsimilarity baseline using substantially richer initial narratives. 

Despite these promising results, several development opportunities remain. The system requires validation on largescale, real-world datasets (e.g., MIMIC-IV [24], [25] or DDXPlus [26]), whose clinical notes, laboratory results, and diverse patient cases better reflect real-world complexity, addressing the current benchmark’s limited size. Future efforts will extend ontology coverage, enable richer patient interactions while preserving determinism, and conduct prospective clinical evaluations. Finally, integrating adaptive weighting and probabilistic evidence could further enhance accuracy of the ranking without compromising diagnostic transparency. 

# VII. ACKNOWLEDGEMENT 

The authors acknowledge Georgiana Copil (Adobe Romania) for her valuable guidance and coordination.
