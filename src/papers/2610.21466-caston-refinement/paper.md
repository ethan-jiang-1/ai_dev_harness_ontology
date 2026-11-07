---
source: 2610.21466-caston-refinement.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# Ontology Refinement with Embeddings and LLMs: A Case Study on CASTON · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

# **Ontology Refinement with Embeddings and LLMs: A Case Study on CASTON** 

Hui Yang<sup>_1_,</sup><sup>_*_</sup> , Ziyu Li<sup>_3,5_</sup> , Xuan Liu<sup>_4_</sup> , Anders Jarfors<sup>_3_</sup> , He Tan<sup>_2_</sup> and Jiaoyan Chen<sup>_1_,</sup><sup>_*_</sup> 

_1University of Manchester, Manchester, UK_ 

_2Department of Computing, Jönköping University, Sweden_ 

_3Department of Materials and Manufacturing, Jönköping University, Sweden_ 

_4Department of Mechanical Engineering, National University of Singapore, Singapore_ 

_5COMPtech i Skillingaryd AB, Sweden_ 

### **Abstract** 

Ontologies are widely used to represent and organize complex knowledge in domains such as biomedicine and healthcare. However, constructing reliable ontologies remains challenging, as class hierarchies, whether manually or automatically constructed, may contain subtle subsumption errors that require careful refinement. We study this problem in CASTON, a casting-domain ontology, and present a lightweight but scalable refinement workflow that combines a fine-tuned ontology embedding model with Large Language Models (LLMs). The embedding model is used to extract a limited number of candidate axioms for refinement together with possible replacement candidates, and an LLM then returns repair suggestions. In a small expert evaluation, the default configuration using a CASTON-fine-tuned OnT embedding model and Qwen3-8B produced reliable high-confidence repairs: all six high-confidence replacements were accepted by both domain experts. The implementation is available at https://github.com/HuiYang1997/OntRefine. 

### **Keywords** 

Ontology embeddings, Large language models, Ontology refinement 

## **1. Introduction** 

OWL ontologies provide a formal way to represent domain knowledge through concepts, relations, and logical constraints. They support knowledge sharing, automated reasoning, and explainable systems across various real-world domains, such as biomedicine [1] and healthcare [2]. However, building and maintaining ontologies still requires considerable expert effort. In particular, incorrect asserted superclass axioms can affect reasoning results and downstream applications, making class hierarchy refinement an important but time-consuming task. 

Recent studies have explored the use of Large Language Models (LLMs) for ontology completion, matching, and validation [3, 4, 5, 6]. However, asking an LLM to inspect a whole ontology in order to refine subsumption axioms is not well targeted and can be computationally expensive. Therefore, we propose a two-stage approach. In the first stage, an embedding model helps narrow down the search by ranking the existing axioms and retrieving possible alternative parent classes. In the second stage, an LLM checks only these selected axiom groups. It compares the current parent class with the candidate parent classes using their class labels, and then gives structured refinement suggestions. This design keeps the LLM focused on a small local context. It also enhances the traceability of each suggested repair, because every repair is linked to a clear and limited set of candidate classes. 

We use CASTON<sup>1</sup> , a developing real-world ontology for metal casting, materials science, and manufacturing processes, as a case study to evaluate whether embedding-guided LLM review can support the refinement of asserted superclass axioms. Using the CASTON 1.0.0 snapshot released on 22 February 2026, we evaluated different combinations of embedding models and LLMs. Across these combinations, 

_ISWC 2026 Companion Volume, October 25–29, 2026, Bari, Italy_ 

> _*_ Corresponding author. 

> � hui.yang-2@manchester.ac.uk (H. Yang); ziyu.li@ju.se (Z. Li); xuanliu@u.nus.edu (X. Liu); anders.jarfors@ju.se (A. Jarfors); tan.he@ju.se (H. Tan); jiaoyan.chen@manchester.ac.uk (J. Chen) 

> © 2026 Copyright for this paper by its authors. Use permitted under Creative Commons License Attribution 4.0 International (CC BY 4.0). 

> 1https://inmost-research.org/ontologies/caston/


<!-- page 2 -->

<!-- Start of picture text -->
Input ontology Candidate generation LLM validation Refinement Suggestions<br>Refinement target detection<br>(e.g., CASTON) Prompting Parent replacements<br>& Parent candidate generation<br><!-- End of picture text -->

**Figure 1:** Overview of the ontology-refinement workflow. 

the system produced 40 replacement suggestions with high or medium confidence. Human evaluation by two domain experts shows that the default setting, which combines a CASTON-fine-tuned embedding model with Qwen3-8B, provides reliable high-confidence repairs: all six evaluated high-confidence replacements were unanimously accepted. These findings indicate that embedding-guided LLM review can provide practical support for ontology construction by prioritising likely problematic superclass axioms and suggesting localised repairs, thereby reducing manual inspection effort and improving scalability in large ontology development settings. 

# **2. Method** 

We focus on asserted in-ontology subsumption axioms between named CASTON classes. That is, each axiom has the form _𝐴 ⊑ 𝐵_ , where _𝐴_ and _𝐵_ are named CASTON classes and the axiom states that every instance of _𝐴_ is also an instance of _𝐵_ . As shown in Figure 1, the workflow has two stages: embedding-based candidate generation and LLM validation. 

**Stage 1: Candidate generation.** For each asserted axiom _𝐴 ⊑ 𝐵_ , we rank all named classes _𝐵_<sup>_′_</sup> _∈𝒪_ , excluding _𝐴_ , as possible parents of _𝐴_ . Let _𝑟𝑚_ ( _𝐴, 𝐵_ ) denote the rank assigned by embedding model _𝑚_ to the asserted parent _𝐵_ of class _𝐴_ , with rank 1 indicating the most plausible parent. Formally, 

_𝑟𝑚_ ( _𝐴, 𝐵_ ) = rank _𝑠𝑚_ ( _𝐴,𝐵_ ) _{𝑠𝑚_ ( _𝐴, 𝐵_<sup>_′_</sup> ) _| all classes 𝐵_<sup>_′̸_</sup> = _𝐴},_ 

where _𝑠𝑚_ ( _𝐴, 𝐵_<sup>_′_</sup> ) is the score function of the embedding model _𝑚_ for measuring the plausibility of the axiom _𝐴 ⊑ 𝐵_<sup>_′_</sup> . Thus, a larger value of _𝑟𝑚_ ( _𝐴, 𝐵_ ) indicates that the asserted parent is less compatible with the embedding model. We then select the top _𝑘𝑟_ axioms with the largest _𝑟𝑚_ ( _𝐴, 𝐵_ ) values, using _𝑘𝑟_ = 30 by default, as suspicious axioms for LLM-based validation. 

For each selected axiom _𝐴 ⊑ 𝐵_ , we use the same embedding model to construct a pool of alternative candidate parents. Specifically, for the child class _𝐴_ , we retain the _𝑘𝑎_ (with _𝑘𝑎_ = 10 by default) highestranked candidate parents that are neither _𝐴_ itself nor already asserted parents of _𝐴_ . We denote this set by _𝑃_ cand( _𝐴_ ). 

As the default embedding model, we use OnT [5] after fine-tuning it on CASTON. OnT is a hyperbolic ontology embedding method designed to adapt to a given _ℰℒ_ ontology. It models a score function _𝑠_ ( _𝐴, 𝐵_ ) based on the hyperbolic distance between the embeddings of _𝐴_ and _𝐵_ . Since CASTON falls within this ontology class, OnT is suitable for modelling its hierarchical structure. 

**Stage 2: LLM validation.** For each axiom _𝐴 ⊑ 𝐵_ selected in the previous stage, we construct a single LLM prompt that combines three sources of information: the child class _𝐴_ , its currently asserted superclass axioms, and the candidate parent set _𝑃_ cand( _𝐴_ ), as illustrated in Figure 2. For each class mentioned in the prompt, we include the available metadata, such as the class ID, label, definition or comment, and domain or scope note. The prompt also includes all other additional axioms involving _𝐴_ , such as existential restrictions of the form _𝐴 ⊑∃𝑟.𝐵_ 1, as background information where available. 

The LLM is asked to determine whether each current parent is a correct direct superclass, whether any parent should be removed or replaced by one of the suggested alternatives, whether any candidate parent should be added, and to provide a justification for each decision. The model returns a structured JSON object containing the parent-level verdict, a suggested replacement where applicable, a textual justification, and a confidence label: High, Medium, or Low. We retain suggestions with High or Medium confidence as candidate refinements for subsequent evaluation.


<!-- page 3 -->

## **User Prompt Template** 

**Concept under review.** The prompt provides the ID, label, definition, domain, and other axioms for the child class _𝐴_ . **Current superclass axioms.** Lists the axioms _𝐴 ⊑ 𝐵_ 1 _, . . . , 𝐴 ⊑ 𝐵𝑛_ , together with the label/definition of _𝐵𝑖_ . **Top candidate parent classes.** The top _𝑘_ = 10 candidate parents _𝐵_<sup>_′_</sup> that are not in current parents. **Decision rule.** A direct parent must satisfy the following condition: every instance of _𝐴_ is necessarily an instance of _𝐵_ . Multiple inheritance is allowed. **Required JSON schema.** { "concept": "<class_id>", "verdict_per_parent": [ {"parent": "<parent_id>", "verdict": "correct|incorrect|partial", "confidence": "high|medium|low", "reason": "<brief explanation>"} ], "suggested_replacements": [ {"remove": "<parent_id>", "add": "<new_parent_id>", "reason": "<explanation>"} ], } 

**Figure 2:** Prompt used for the LLM validation stage. 

# **3. Experimental Setup and Preliminary Results** 

**Experiment setting. (1) Dataset:** We evaluate our method on the developing ontology CASTON, using the first release, version 1.0.0, which was released on 22 February 2026. This version contains 270 named classes, i.e., concepts, and 306 axioms. Of these, 292 are subsumption axioms involving atomic concepts, for which rank scores were assigned using the embedding models, as illustrated in the workflow. **(2) Configuration.** As shown in the first column of Table 1. We consider three different settings: _The default setting_ is CASTON-fine-tuned OnT + Qwen3-8B, where OnT is fine-tuned from the SBERT variant all-mpnet-base-v2. To analyze the influence of embedding models and LLMs, we compare the default workflow with _two non-fine-tuned comparison settings using Qwen3-8B or GPT-4o mini_ , where both method use a non-CASTON-fine-tuned ensemble embedding for candidate generation. The ensemble method composed of three sentence embedding models: OnT fine-tuned on the GALEN ontology, HiT fine-tuned on WordNetNoun, and standard SBERT. All three models are based on allmpnet-base-v2. In this ensemble setting, we use the mean rank across the embedding models to select candidate refinement axioms and generate candidate parent sets. **(3) Evaluation metric.** Two domain experts independently score each replacement suggestion using a five-point ordinal scale: _−_ 2 for completely wrong, _−_ 1 for seems wrong, 0 for vague or unclear, +1 for seems correct, and +2 for completely correct. We classify a suggestion as accepted when both experts assign positive scores, rejected when both assign negative scores, and mixed otherwise. 

**Results** Table 1 shows that the default configuration is highly reliable for the small set of highconfidence replacement suggestions evaluated in this study. With Qwen3-8B and fine-tuned OnT embeddings, all six high-confidence replacements are accepted by both experts (with score +2 for all cases), yielding a 100% acceptance rate with no mixed or rejected cases. In contrast, both mediumconfidence cases are mixed. This indicates that the LLM confidence score is useful for prioritization: high-confidence predictions under the default setting are trustworthy, whereas medium-confidence ones still require manual review. Replacing the fine-tuned embeddings with the pretrained ensemble markedly reduces reliability. With the same Qwen3-8B generator, the high-confidence acceptance rate drops from 100% to 57.1%: 4 of 7 cases are accepted, while 3 are rejected. Medium-confidence results are also weak, with only 1 of 4 cases accepted and 3 rejected. Thus, although the pretrained ensemble can recover some valid candidates, it lacks the precision of the fine-tuned OnT model, highlighting the importance of task-specific embedding finetuning. 

Using GPT-4o mini with the same pretrained ensemble further reduces the reliability of high-


<!-- page 4 -->

**Table 1** 

Expert outcomes by setting and LLM confidence. Accepted rows have positive expert agreement; parentheses give the +2/+1 breakdown. Mixed rows are expert disagreements or unclear cases. 

|**Setting**|**Confidence**|**Rows**|**Accepted**<br>**(+2/+1)**|**Mixed**|**Rejected**<br>**(-2/-1)**|**Acceptance rate**|
|---|---|---|---|---|---|---|
|Default: Qwen3-8B + CASTON OnT-FT|High|6|**6**(6/0)|0|0|**100%**|
|Default: Qwen3-8B + CASTON OnT-FT|Medium|2|0 (0/0)|**2**|0|0%|
|Ablation: Qwen3-8B + pretrained ensemble|High|7|**4**(4/0)|0|**3**|57.1%|
|Ablation: Qwen3-8B + pretrained ensemble|Medium|4|1 (0/1)|0|**3**|25.0%|
|Auxiliary: GPT-4o mini + pretrained ensemble|High|16|**5**(5/0)|1|**10**|31.3%|
|Auxiliary: GPT-4o mini + pretrained ensemble|Medium|5|1 (0/1)|0|**4**|20.0%|



confidence predictions. Among the 16 high-confidence replacements, only 5 are consistently accepted, 1 receives mixed judgments, and 10 are rejected, yielding an acceptance rate of 31.3%. This is 68.7 percentage points lower than the default setting. Notably, many replacements assigned high confidence by GPT-4o mini are rejected by both experts. These results indicate that, compared with Qwen3-8B, GPT-4o mini exhibits poorer confidence calibration for this task and a stronger tendency to produce unreliable decisions. 

**Case Studies** To better understand the strengths and limitations of the proposed workflow, we present detailed case studies generated using the default configuration (i.e., Qwen3-8B+OnT-FT). 

_Success case:_ A representative successful refinement is the concept chromite_sand. In the original ontology, chromite_sand was modelled as a subclass of green_sand_molding. The fine-tuned workflow instead suggested replacing its superclass with foundry_sand, a recommendation accepted by both domain experts (+2/+2). Semantically, green_sand_molding denotes a molding process, whereas chromite_sand is a mold material used in foundry applications. The suggested axiom therefore yields a more accurate material taxonomy while preserving the intended domain semantics. Similar refinements were observed for olivine_sand, silica_sand, and zircon_sand, indicating that the fine-tuned OnT embeddings can identify semantically appropriate superclass refinements rather than merely retrieving lexically related concepts. 

_Failure case:_ A representative failure case is semisolid_metal_(ssm)_processing. The original ontology classified this concept under high_pressure_die_casting, whereas the fine-tuned workflow suggested replacing its superclass with semisolid_casting. Although this suggestion is semantically related, the experts did not agree on its validity (0/-2). One expert noted that the hierarchy among these concepts is inconsistent in the current ontology and requires revision, while the other argued that semisolid_metal_processing should instead be modelled as a subclass of die_casting. This case shows that even fine-tuned embeddings may produce incorrect superclass assignments when the existing ontology hierarchy is incomplete or structurally inconsistent. 

# **4. Conclusion** 

This poster provides preliminary evidence that embedding-guided LLM review can support practical ontology hierarchy refinement when the embedding model is adapted to the target ontology. The CASTON-fine-tuned OnT + Qwen3-8B workflow identified a small but reliable set of high-confidence repairs, all of which were judged to be completely correct by two domain experts. The evaluation is currently limited to one ontology, replacement suggestions, and a small number of expert-assessed repairs. In future work, we plan to extend this pipeline to more complex axiom types, such as relational restrictions, and evaluate its effectiveness at larger scale across ontologies from diverse domains. We will also apply the pipeline to future versions of CASTON to support systematic hierarchy refinement, ontology enrichment, and continuous ontology evolution through expert-guided, LLM-assisted refinement.


<!-- page 5 -->

# **Acknowledgments** 

Hui Yang and Jiaoyan Chen are supported by the EPSRC project OntoEm (EP/Y017706/1). Xuan Liu acknowledges the support of the NUS Research Scholarship. Ziyu Li’s PhD project was funded by the Stiftelsen för kunskaps- och kompetensutveckling (KK-Stiftelsen) through the Smart Industry Sweden initiative (project number 2020-0044). 

# **Declaration on Generative AI** 

During the preparation of this work, the authors used ChatGPT for _Grammar and spelling check_ , _Paraphrase and reword_ , and _Improve writing style_ to check grammar and spelling and improve the clarity and readability of author-written text. Claude was used to assist in developing code implementations for the proposed methods. After using these tools and services, the authors reviewed and edited the generated content as needed and take full responsibility for the publication’s content.
