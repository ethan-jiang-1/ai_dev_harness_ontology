---
source: 2610.41901-rex-gg.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# ReX-GG: a LLM Ensemble Pipeline for Relation-extraction and Graph Generation · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

# **ReX-GG: a LLM Ensemble Pipeline for Relation-extraction and Graph Generation** 

## **Giacomo Magnifico, Eduard Barbu** 

Institute of Computer Science, University of Tartu 

Tartu, Estonia 

```
{giacomo.magnifico,eduard.barbu}@ut.ee
```

### **Abstract** 

Current LLM ensemble frameworks focus on multi-step setups with additional modules for answer ranking, often opting for token and span analysis rather than structured outputs, leading to heavyweight architectures with potential fail states along the pipeline. Faster, lighter solutions are more vulnerable to hallucination propagation and can lack output control in more complex pipelines. This paper proposes a customisable, lightweight ensemble workflow of coordinated Large Language Models that leverages JSON-structured outputs and anonymous peer-review ranking to mitigate hallucinatory outputs and single-model failure points. The pipeline is demonstrated on a relation extraction task applied to popular science articles in English, targeting four ontologically-grounded relation types (strong causation, weak causation, contrastive, and compositional), with semantic node canonicalisation and interactive, colour-coded HTML causal graphs as the final output. Performance is evaluated through an anonymous user study, achieving an average perceived accuracy of 0.778 against a human-annotated gold standard. The modular architecture supports flexible deployment across both API-based and in-house LLM setups, and the full framework is released under an open license to foster reproducibility and collaborative research. 

**Keywords:** graph, human survey, lightweight framework, LLM ensemble, relation extraction, structured output 

## **1. Introduction** 

Since the advent of OpenAI and the permeating use of Large Language Models (LLMs) in everyday life and academia, the ease of access to state-ofthe-art models and diffusion has led to new avenues of research; from testing the limits of these models to mitigating their shortcomings, exposing their faults and tuning their performance. As expected, the use of individual models has led to the development of LLM ensembles, tailored to achieve more robust performance and to leverage perceived differences among these models (Jiang et al., 2023). Other ways to enhance the reliability and robustness of their output have been found at the intersection of formal structure and natural language processing (NLP), in the form of informationbased graphs, with examples of knowledge-graphinformed architectures that leverage the power of ontologies and formal structure (Zhou et al., 2025; Zhu et al., 2025). Within this specific niche, it is possible to find widely different research avenues - from graph-based LLM ensemble performance evaluations (He et al., 2025) to analyses of LLM inner workings via graph representation of their chain of thought (Zhiqiang et al., 2025). The production of knowledge graph outputs seems to be less explored, with Pham Hoang Le et al. (2025) and Li et al. (2025) as examples, although only the former explores ensembles and structured outputs, while the latter focuses on LLM tuning. 

To foster further research in this niche and to provide an accessible tool to the research commu- 

nity, this paper presents a **lightweight example of an information-extraction ensemble workflow, tailored for relation extraction and interactive graphs** . The proposed workflow can be deployed with a customisable selection of coordinated models, delivering robust performance and a reduced risk of hallucinatory or malformed output thanks to the peer-reviewed ranking of schema-enforced JSONs. The practical application of the pipeline targets English popular science articles, with performance tested via an anonymous survey to provide public-informed evaluation of the relation-extraction framework; anecdotal evidence shows a preference for colour-coded graph edges representative of the evaluated bonds. The secondary advantages of this work can be identified as the following: 

- simple overarching structure with flexible end use; 

- built-in mitigation of hallucination propagation; 

- reduced risk of malformed outputs failurechains; 

- fast deployment as a modular piece in larger architectures. 

Details regarding the structure and behaviour of the ensemble are provided in Section 3.1, along with the ontology and details regarding the nature of the relations chosen for extraction; further information related to the canonicalization of the extracted pairwise relation triplets and development of the graph structure are given in Sections 3.2 and


<!-- page 2 -->

3.3. In Sections 5 and 6, we discuss the results of our user study presented in Section 4, expand on the key findings of this paper, and outline potential future work. We reserve Sections 7 and 8 to discuss the shortcomings and limitations of our scope and to address potential concerns about the ethical standards of this work. 

# **2. Related Works** 

Multiple works deploy different sets of LLMs as ensembles with variable cohesion for a multitude of purposes: from Xu et al. (2025), which evaluates a 7B selection of models and enhances decisionmaking through token span analysis, to the more complex database-oriented tasks focusing on tabular data QA seen in Bujnowski et al. (2025), to striving for the optimization of the ensemble with additional framework refinement as proposed by Tekin et al. (2024). 

Related to our work are the concepts and implementation of the "LLM forest" found in He et al. (2025), which consists of a graph- _informed_ ensemble of models to achieve higher performance in data inputation for subsequent downstream tasks; the performance of graph-informed processes is further investigated in Zhiqiang et al. (2025), alongside the Explainable Graph Language Model framework. Graph- _represented_ decisions, which are closer to the scope of this paper, are explored in Xiong et al. (2025) as a means to clarify the reasoning process of LLMs, converting large freeform text chain-ofthoughts (CoTs) into a readable and measurable graph to explain the causal bonds; the difference in scope lies within model-reasoning applications compared to extractive tools for information transmission. While the output of LLMs is converted into graph form, and the enforced structure within responses is a shared property, the work presented in Wu et al. (2025) makes use of external repositories and ultimately outputs natural language text based on knowledge graphs. 

The two papers that share most of the background with the ensemble of our proposed work are Parfenova and Pfeffer (2025) and Pham Hoang Le et al. (2025); while the former proposes a twostaged ensemble with the aid of a moderator to be deployed for inductive coding, with an emphasis on the use of LoRA finetuned architectures, the latter provides a two-stage pipeline with a smaller zero-shot ensemble. Despite the structural similarities, our work differs both in scope and use case: the focus on causal relations and the use of fewshot prompts distances it from Pham Hoang Le et al. (2025), and the preferred deployment as an intermediary between freeform text and HTML graphs falls further away from Parfenova and Pfeffer (2025)’s scope. 

Lastly, what could be considered a precursor for this work is presented in Li et al. (2025) as a singlemodel pipeline that specifically produces causal graphs from narrative text; although both papers share similar goals, the core difference lies in the use of finetuned BERT architectures and summarisers to overcome the performance of base LLMs, turning the pipeline into a robust but heavy-weight solution. 

The reviewed literature reveals that while LLM ensembles have grown increasingly capable, their complexity has scaled accordingly, often requiring additional ranking modules, finetuned architectures, or external knowledge repositories. Works that produce graph-structured outputs tend to focus on model reasoning transparency rather than information transmission, and those that do target relation extraction either rely on heavyweight finetuned pipelines or limit themselves to single-model setups. No existing work combines a lightweight heterogeneous ensemble with schema-enforced structured outputs, ontologically-grounded relation types, and interactive graph visualisation in a single deployable framework. This paper directly addresses that gap, proposing a _modular, robust yet lightweight solution for everyday information extraction that prioritises accessibility and ease of deployment without sacrificing output reliability_ . 

# **3. Pipeline Structure** 

## **3.1. Model Ensemble** 

**Relation Extraction** . After receiving input from the user with the name and extension of the file to be processed, the read information is stored and sent to each model in the ensemble for the preliminary relation extraction. Our chosen focus is on narratively-driven direct pairwise relations, examples of which can be found both in scientificliterature-based tasks (Pham Hoang Le et al., 2025) and narrative text (Li et al., 2025); the relation types we focus on are based on the works by Ross (2025) and Magnifico (2025), among others, and are defined below. 

- **Strong Causation** . Explains a phenomenon by specifying explicit causal mechanisms or multiple steps in a causal chain. The underlying process is made clear. _“Your lack of sleep is making you clumsy. That’s why you spilled the milk.”_ 

- **Weak Causation** . Explains through correlational or probabilistic relationships between variables without specifying the underlying mechanism. Often involves associations, tendencies, or indirect influences. _“Diseases with_


<!-- page 3 -->

<!-- Start of picture text -->
= Embedder<br>Title IN Model Ensemble htm IN<br>. *<br>Lorem ipsum ——T— (A, B, edge), (C, D, edge), ... ,<br>Saeed (A.B, edge), (B, D, edge)... —<br>|FF | extraction | ranking | i]fe— \ Graph Maker /<br>¢ collectedanswers<br><!-- End of picture text -->

Figure 1: Schematic representation of the pipeline presented in the paper: a text file is fed to the LLM ensemble, where relation extraction is performed, and the best output is decided through anonymous peer-ranking; the extracted relation triplets iterate through an embedding model to improve graph structure and assimilate nodes with semantic similarity. The final result is a causal graph in HTML format. 

_uncertain causes were about 50% more likely to attract religious or magical treatments.”_ 

- **Contrastive** . Explains a phenomenon by highlighting differences between alternative conditions or cases (A vs B). _“In the treatment group, 70% recovered; in the placebo group, only 30% recovered.”_ 

- **Compositional** . States what something is made of, contains, consists of, or is defined as (whole/entity →part/definition). _“Protons and neutrons are combinations of even tinier particles, called quarks.”_ 

To maximise the potential of the extraction pipeline, further rules for the two extremes of the pairwise relations are introduced. First, each leftmost extreme (the future _head_ node) is defined as a _[concept, cause, outcome A, entity]_ , while the rightmost extreme (the future _tail_ node) is defined as a _[concept, effect, outcome B, constituent]_ . Second, each extracted extreme must be a _minimal span of words_ , preferably a _nominal phrase_ - as it is the minimal identifier for a concept, be it a subject or an object in a sentence - and with each pronoun/anaphora resolved to its _explicit referent_ . Third, rewriting the original text is preferable to quoting long sentences directly. A possible example of the extracted relations for the paragraph 

# _“Of course your hands are all jittery, you had a big gulp of coffee earlier! Maybe that’s why you’re dropping stuff?”_ 

would be _[“big gulp of coffee”, “jittery hands”, strong causation]_ , and _[“jittery hands”, “dropped stuff”, weak causation]_ . After lengthy tuning, the final set of instructions follows the best practices for prompt engineering and can be summarised with this outline: 

- task definition; 

- output schema example; 

- rules for schema completion; 

   - rules for node extraction; 

   - rules for edge extraction; 

- set of input-output examples 

As a reliable method of enforcing the schema structure given with the prompt, the choice of `structured_output` settings is enabled; the resulting output is in JSON format as a single-entry Python dictionary, with the word "document" as the _key_ and a list of smaller dictionaries as the _value_ . The list formatting allows for the iterative use of dictionaries with the same shared keys ("bond", "span 1", "span 2") associated with different values, corresponding to the extracted pairwise relations and relation extremes. In this section of the pipeline, there is no interaction among the models, and each output is produced independently. All the JSON-structured outputs from this first pass through the ensemble, representative of the relation bonds extracted from the input document, are then passed along in the pipeline. 

**Model Peer Ranking** . As the outputs of the first ensemble pass have been stored separately for each individual model, they are anonymised to avoid both potential self-preference bias from any architecture and tuning-induced preferences present in the training data. To facilitate easy postprocessing de-anonymisation, each model is assigned a corresponding letter from the English alphabet, starting with A. The anonymised outputs are then given to each model in the ensemble, along with the original document and a reminder of the classification rules, with the explicit task of assigning a 10-point grade to each. 

Once more, these outputs are forced into a JSON structure and must provide the following dictionary entries: 

- _answer :_ string, label of the ranked answer (e.g. A, B, C);


<!-- page 4 -->

- _points :_ integer, points assigned to the ranked answer (0 to 10); 

- _thinking :_ string, providing a reasoning behind the score of the ranked answer. 

embedding as a lightweight yet effective form of control. Each list of dictionary-encoded relation pairs is processed as detailed in Algorithm 1 before moving forward in the pipeline. 

**Algorithm 1** Semantic Triples Node Assimilation 

The points for each answer label are stored and summed as each model in the ensemble goes through this process, forming a "leaderboard" with the comprehensive rating of each anonymous output. Afterwards, the answers are de-anonymised, and the user is informed of _how high each model’s output scored, along with the one chosen as the most accurate_ . The best-voted output is then sent along the pipeline. 

Of relevant mention is the use, through the entire ensemble pipeline, of continuously updated `query_logs` and `error_logs` ; not only is the entirety of the content generated by the ensemble safely stored in a separate text file, but each potential break in the sequence due to unstructured outputs is recorded in a dedicated log file. From the input given to the ensemble to the final structured output, everything is stored for maximum clarity of use. 

The models used for the setup presented in this paper have been deployed through API calls via the OpenRouter platform<sup>1</sup> , with an approximate cost of £10 for the entirety of the multi-stage process. One model for each major corporation has been chosen based on popularity and performance ratings on aggregator websites as of February 2026. The final ensemble of LLMs is comprised of GPT 5.2 (2025), Claude Sonnet 4.5 (2025), Gemini 3 Flash (2025), Deepseek 3.2 (2024), Llama 3.3 (70B-instruct) (2024), Nova 2 Lite V1 (2024), Grok 4.1 Fast (2025); all of the outputs are set to `structured` , with a 4000 token limit and the same fixed seed for the entire process to keep consistency as high as possible. 

# **3.2. Embedding Model** 

After the LLM ensemble, the second block of our pipeline prepares the best-voted answers (as lists of dictionary-encoded lists of semantic triples) for later graph representation. As the semantic triples are stored with a high likelihood of non-identical text strings for similar concepts (e.g. “a coffee”, “coffee”, “nice cup of coffee”), a graph derived by the raw list would be scattered and represent only two-node relations; with no changes, the compositional properties of causal bonds would be lost, as well as any other defined relation type that spans multiple concepts. To achieve a cohesive structure and minimise fragmentation, we turn to semantic 

_inputs ←_ list of dictionaries _relations_ = [ ] **for** _i_ in _inputs_ **do if** _i_ [ _relation_ ] _̸_ = none **then** _pair ←_ ( _i_ [ _A_ ] _, i_ [ _B_ ] _, i_ [ _relation_ ]) _relations ← relations_ + _pair_ **end if end for for** _i_ = 1 to _i_ = # _relations_ **do** _x ← relations_ [ _i −_ 1][1] _y ← relations_ [ _i_ ][0] _X, Y_ = _embedder.encode_ ( _x, y_ ) **if** _embedder.similar_ ( _X, Y_ ) _≥ value_ **then** _y ← x_ **end if end for** 

The first half of the process shows how the inputs received from the LLM ensemble are converted from dictionary encoding into _tuple_ object types, all while keeping the RDF structure 



<!-- Start of picture text -->
A → relation → B<br><!-- End of picture text -->

with possible examples being 

_coffee → strong causation → jittery hands_ 

_jittery hands → weak causation → drop stuff._ 

An immediate change in the conversion is the substitution of the relation types mentioned in Section 3.1 with the colour associated with them. Since the final output of the pipeline has to be intuitively understandable and easy to read, we opt for the colour-coding _[red, orange, cyan, green]_ for _[strong causation, weak causation, contrastive, compositional]_ . Thus, the two examples above would be converted into 

_coffee → red → jittery hands_ 



<!-- Start of picture text -->
jittery hands → orange → drop stuff.<br><!-- End of picture text -->

Worth noting is that each pairwise relation is stored in a _A-B-relation_ order, as a popular format for graph information storage is the _(head, tail, directed edge)_ notation. 

Presented in the second half of Algorithm 1 is our solution for graph sparcity: an iteration over the list of stored semantic triples using an embedding model to achieve a rudimentary but efficient form of multi-node relation canonicalization. As subsequent triples are iterated through, the _tail_ of 

> 1 `https://openrouter.ai/`


<!-- page 5 -->

the previous one is compared with the _head_ of the following through vector embedding and similarity measure between the embeds; if the semantic similarity is higher than a chosen threshold, the two concepts are assumed to be syntactic variations of the same semantic term. If that is the case, the two nodes become one and the same, transforming a pair of arcs 



<!-- Start of picture text -->
A → relation → B<br>C → relation → D<br><!-- End of picture text -->



<!-- Start of picture text -->
into<br><!-- End of picture text -->



<!-- Start of picture text -->
A → relation → B<br>B → relation → D<br><!-- End of picture text -->

which represent the assimilated triplet composition 



<!-- Start of picture text -->
dont, ua Sratytcomsmaar> th sa cana<br>a oo<br>sree an<br>siee tatoo - can an si<br>(@-<——i8eaSeeave been around 410 mation years<br>cuteransas<br>noe trough shel crete<br>ta pga4 cette tne styHo ea<br>nt<br>® sie panto gen<br>lctedundemes seamen<br>y<br>e<br>iepted desgs epg oot teeps hom ht<br><!-- End of picture text -->

_A → relation →_ ( _B → relation → D_ ) _._ 

We deploy `Jasper-Token-Compression600M` (Zhang et al., 2025) as a semantic embedding model, given its superior performance relative to near-state-of-the-art language models. 

## **3.3. Interactive Graph Maker** 

Given the input from the embedding algorithm, we populate a `NerworkX`<sup>2</sup> directed graph with given dimensions of 1080p _×_ 1080p. The directed graph is then converted into a `PyVis`<sup>3</sup> object to allow for better interactivity, and it is exported as an HTML file - akin to the sample provided in Figure 2 as an image. We chose this specific format because it enables a more hands-on approach for the end user, allowing them to move nodes around, enable/disable graph physics, highlight nodes and vertices, and so on. 

# **4. Human Evaluation** 

To avoid authorship bias in the effectiveness and correctness of the graphs generated by the pipeline, an anonymous survey was distributed to paid volunteers recruited via the _Prolific_ web app<sup>4</sup> . Two graphs were annotated by the authors to serve as a human-annotated gold standard baseline, and then evaluated by two dedicated groups of 3 anonymous testers. The remaining 18 articles in the set were processed by the pipeline and each was evaluated by 6 testers. The scoring method was as follows: a four-point evaluation of the usefulness of the graph; a five-point evaluation of the accuracy of the information provided in the graph; and a final four-point score for the tester’s confidence in their scores. Although the perceived usefulness of the graphs was 

> 2 `https://networkx.org/en/` 

> 3 `https://pyvis.readthedocs.io/en/ latest/index.html` 

> 4 `https://www.prolific.com/` 

Figure 2: A full graph output from our pipeline, derived from the article "Snow fleas use their tails to jump around the ice", available at this link. 

not considered in the current evaluation, the testers’ confidence was used to compute a weighted average across annotator groups for each article. The scores for the accuracy of author-annotated graphs served as a baseline for comparing the accuracy of the remaining data, as they represented the "ideal accuracy" for manual annotators. 

||**Accuracy**|**Length**|_×σ_|
|---|---|---|---|
|A1|0.807|2342|0.2|
|A13|0.939|2374|1.1|
|A14|0.903|2444|0.9|
|A7|1.000|2603|1.6|
|A10|0.745|3062|0.2|
|A12|0.880|3245|0.7|
|A5|0.550|3270|1.6|
|A18|0.521|3709|1.8|
|A3|0.880|3895|0.7|
|A15|0.953|4253|1.2|
|A6|0.623|4426|1.1|
|A4|0.790|4764|0.1|
|A8|0.835|4967|0.4|
|A16|0.831|5215|0.4|
|A11|0.636|5950|1.0|
|A17|0.815|9078|0.3|
|A2|0.632|9542|1.0|
|A9|0.670|10321|0.8|
|_Avg._|_0.778_|_4748_|_1_|



Table 1: Scores for the perceived accuracy of each graph, normalised against the human-annotated gold standard, with the distance from the mean measured in standard deviations. 

Divided by original document and in increasing


<!-- page 6 -->

length order, the scores for each graph’s perceived accuracy and standard deviation steps from the average are shown in Table 4. A visual representation is available in Figure 3, along with the projected mean of the perceived accuracy and a _±σ_ representation. The furthest outliers in the data (A5, A7, A18) are still within 2 _σ_ from the mean, and the majority of values are within one _σ_ . 

To provide a visual representation of the robustness of our proposed solution, Figure 4 presents the average grading for each individual model (dotted lines) across the selection of articles, with the model ensemble pipeline as a comparison (full line). 

limited span of distribution for the ratings supports the assumption of an effective pipeline. 

**Robustness** . Due to the nature of the ensemble architecture, each of the models is forced to produce a JSON output, and each part of the contentgeneration and recording sequence carefully looks for formatting errors; as each output is stored independently and given anonymously for peer-review ranking to each model, the pipeline avoids the pitfalls of hallucination propagation and unusable outputs. The anonymous nature of the ensemble rankings allows for personalised use with a _single LLM ensemble setups_ for even lighter-weight scenarios, and it is adaptable to both in-house and API LLM usage. 

# **5. Performance Analysis** 

# **6. Conclusions** 

The processed results from the anonymous survey can be helpful in defining the key properties of the deployed pipeline, ranging from the relation between performance and document length and the perceived accuracy of the graphs to the robustness of the ensemble. 

**Ensemble vs Single-model Rank** . As shown in Figure 4, the variability in the performance of each single LLM presents a wide margin of potential error that can lead to inaccurate graphs and poorlyformed outputs. Even the best-performing model is shown to have instances of rankings lower than 30 points, and the less-performing models at times rise to higher scores. Overall, the ensemble ranking leads to more stable, robust performance. 

**Document Length vs Accuracy** . Based on the results shown in Table 4 and the distribution presented in Figure 3, we can conclude that there is no direct relation between document length (measured in characters) and perceived accuracy of the relative graph. Both the Table and the Figure show that the highest accuracy and the lowest are both within the initial range (2000 to 5000 characters); it could be speculated that the accuracy scores show a diminishing trend as the documents become longer, but a more balanced evaluation would be that the variance between results lowers with longer documents. 

**Human-rated Accuracy** . Taking into consideration the mixed nature of the Accuracy score, indicative both of completeness compared to the original text (e.g. number of core relations reported in graph) and accuracy of the information presented (e.g. two elements put in correlation rather than contrast), our pipeline produces high-quality outputs with near-human annotation peaks and an average of _0.778_ . All of the human ratings for the interactive graph outputs are within 2 standard deviations from the mean, with the majority (66%) being within 1 standard deviation. Even without the removal of the largest outliers in both directions, the 

In this paper, we have presented a lightweight pipeline for information extraction that leverages an ensemble workflow of seven independent models, coordinated to reliably mitigate hallucinatory outputs and malformed graph generation. Our framework achieves robust performance by leveraging JSON-structured outputs and independent modelpeer-review ranking strategies. When the deployed pipeline is tested on a selection of English popular science articles, the reported performance is close to the human-annotated gold standard, with an average accuracy of the provided information of 0.778 - measured by aggregated scoring from anonymous annotators. The outputs are presented to end users as interactive, colour-coded HTML files that facilitate immediate, intuitive understanding. 

Anecdotal evidence supports the ease of use and deployment of the proposed pipeline even by less-specialised users, and the modular nature of the ensemble allows for highly customisable settings; possible implementations that benefit from the anonymous peer-review model-ranking include free and open source solutions, such as in-house single-LLM ensembles with multiple-persona structures, or heterogeneous ensembles that can benefit from an array of different-scale models. 

Future work is necessary to reach higher performance and more interpretable results, as reports from anonymous users in the study suggest that a central topic node and a specific top-down or left-right directionality would be beneficial for graph understanding. Further testing is also necessary to verify the robustness of our pipeline across different settings and contexts, aiming for higher generalisation and a wider selection of relation types; a potential addendum could be investigating input multimodality to determine the best format for maximal accuracy. Finally, developing a simpler software solution that allows non-command-line execution of


<!-- page 7 -->

<!-- Start of picture text -->
1.000<br>+<br>i :<br>+<br>g0.750 +<br>g+<br>8 0500 ’ { |<br>*<br>0.250<br>0.000<br>0 2500 5000 7500 10000<br>arlicle length (characters)<br><!-- End of picture text -->

Figure 3: Performance of the graph produced by our pipeline according to the anonymous survey. The averaged accuracy scores for each article are represented as filled _⋄_ , along with the line marking the mean value. 



<!-- Start of picture text -->
®  opt52claude sonnet.45<br>1 gemini-3.tash<br>: ‘ : 2 B . 11 deepseek32tame.32-70bsne<br>® ; : :<br>4 ; 1 nove 241<br>8 pos P p 7m grok tas<br><!-- End of picture text -->

Figure 4: Ranking of our ensemble scores compared to the performance of the individual model, ranging from a minimum of 0 to a maximum of 70 points, over the articles evaluated. 

the pipeline would improve accessibility and ease of use for the general public. 

All the software presented in this paper is freely available at our GitHub repository<sup>5</sup> to foster cooperative research and an open-science mindset in the academic community. 

# **7. Limitations** 

Since our paper focuses on presenting a lightweight alternative to heavier informationextraction pipelines, some limitations regarding performance and size are bound to the nature of the work. The current workflow has been tested with shorter documents, which are easier to read and evaluate for the anonymous testers; conse- 

quently, proper testing with sizeable documents (e.g. entire scientific research papers) falls outside of the current scope despite it being, perhaps, the more interesting application for our pipeline. For the sake of simplicity and customisation, aside from the processed data and the log information, all the information flow is strictly online, as the models are called through API, and a true analysis of the reasoning process for LLMs is not available. Anecdotal evidence also suggests that the output graphs would benefit from a central node with the general topic of the input document as the origin, with radial orientation to improve comprehension. Lastly, the human evaluation is more qualitative than quantitative, as the number of evaluated documents is on the lower end of the spectrum. 

> 5 `https://github.com/gima9552/ReX-GG`


<!-- page 8 -->

# **8. Ethical Considerations** 

The reliance on LLMs to extract information from texts and present it to the public can inherit datainduced bias and carry the harm of potential misinformation. Our framework mitigates the propagation of hallucinatory outputs by leveraging the ensemble-based ranking, but it is not guaranteed to have a completely faithful output in every single case; therefore, the recommendation is to always introduce human supervision in the loop, and generally defer judgment to the user. The evaluation done with anonymous testers was conducted with no risk of harm and within safe work regimes, and the payment was above the platform’s minimum wage standards. To the best of our knowledge, the work presented in this paper does not pose any significant risk of harm in itself. 

# **9. Acknowledgements** 

This work was supported by the project “Terminology-Aware Machine Translation for Accessible Science” (TaMTAS, MOB3ERA10), funded by the Estonian Research Council under the Mobilitas 3.0 ERA-NET programme and co-funded by the European Union under the CHIST-ERA Call 2025 “Science in Your Own Language.”
