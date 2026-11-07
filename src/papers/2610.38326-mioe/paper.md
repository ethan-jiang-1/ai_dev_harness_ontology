---
source: 2610.38326-mioe.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# Can LLMs Faithfully Solve Ontology Engineering Tasks? A Mechanistic Interpretability Study · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

# **Can LLMs Faithfully Solve Ontology Engineering Tasks? A Mechanistic Interpretability Study** 

**Bohui Zhang**<sup>1</sup> **, Albert Meroño-Peñuela**<sup>1</sup> **, Elena Simperl**<sup>1,2∗</sup> 

1King’s College London, United Kingdom 

2Technical University of Munich, Germany 

bohui.zhang@kcl.ac.uk, albert.merono@kcl.ac.uk, elena.simperl@kcl.ac.uk 

### **Abstract** 

Ontological knowledge underpins large language model (LLM) performance on knowledge-intensive tasks. However, existing evaluations of LLMs’ ontological understanding largely rely on behavioral correctness, leaving the underlying mechanisms unexplained. Existing mechanistic interpretability work has largely focused on instance-level factual knowledge, leaving ontological knowledge under-explored. To bridge this gap, we introduce MIOE, a causal-abstraction benchmark that evaluates interchange interventions for two ontology engineering tasks: entity typing and subsumption prediction. MIOE tests whether learned internal intervention targets can change an ontologylevel target answer while preserving class-specific auxiliary information. Across Qwen3-8B and Qwen3-4B, we evaluate SAE-, DBM-, and DAS-based methods, including multi-task and multi-layer variants. Distributed subspace methods give the strongest results and generalize across prompt settings, but the induced changes remain only partially separated from auxiliary class-specific information. Multi-task objectives and contiguous layer-window interventions improve this balance, while class-level analyses reveal substantial variation across ontology classes. These results suggest that ontological predictions are mechanistically accessible in LLMs, although current methods do not yet isolate a cleanly disentangled causal mechanism for ontological knowledge. 

**Code** — 

https://github.com/King-s-Knowledge-Graph-Lab/MIOE 

## **Introduction** 

Formal ontologies provide schema-level knowledge for many knowledge-intensive tasks in the AI era. They define classes, relations, constraints, and hierarchies that support structured knowledge representation, semantic reasoning, and data integration (Pan et al. 2023). As LLMs become increasingly capable of generating, validating, and revising knowledge, they are also being explored as assistants for ontology engineering tasks, including ontology construction, completion, alignment, and evaluation (Babaei Giglou, D’Souza, and Auer 2023; Lo et al. 2024; Zhang et al. 2025a,b). 

Despite this promise, recent empirical evidence suggests that LLMs still face substantial limitations in ontology engineering. While they can perform well on basic ontologyrelated tasks (He et al. 2023; Babaei Giglou, D’Souza, and 

∗Corresponding author. 

Auer 2023), their performance remains suboptimal and often unpredictable on more advanced tasks, such as ontology evaluation (Tsaneva et al. 2025). This leaves open a critical question: whether correct ontology-oriented outputs are supported by internal computations that track the relevant ontological relation, and how these computations interact with broader subject information. This raises a concern about faithfulness, defined as the degree to which a model’s output reflects the internal process that produced it (Wiegreffe and Pinter 2019; Jacovi and Goldberg 2020). However, most existing evaluations of LLMs for ontology-related tasks remain behavioral, asking whether the model outputs the correct label, axiom, or judgment under a given prompt. Such evaluations are necessary, but they do not reveal the mechanism by which the answer is produced. 

Mechanistic interpretability offers a way to study this problem by connecting high-level variables to causal mechanisms inside the model. Interchange interventions provide a causal abstraction test: they replace internal representations across inputs and examine whether the model’s behavior changes according to the corresponding high-level variable (Geiger et al. 2021, 2022). Prior work has applied mechanistic interpretability to factual knowledge in LLMs, including the localization, editing, causal role of factual associations, and feature disentanglement (Geva et al. 2022; Dai et al. 2022; Meng et al. 2022; Huang et al. 2024). However, ontological knowledge plays a different role from ordinary factual or attribute-level knowledge. While factual attributes capture local properties of a subject, ontology-level relations determine its type, taxonomic position, and the constraints or properties that are applicable to it. This makes ontological knowledge a distinctive target for mechanistic interpretability. 

In this paper, we investigate mechanistic interpretability for ontological knowledge in LLMs. We move beyond outputlevel correctness and ask whether ontology-level variables can be connected to the model’s internal computation through testable causal interventions. We introduce Mechanistic Interpretability for Ontology Engineering (MIOE), an ontologycentric benchmark for evaluating interchange interventions over two fundamental ontology engineering tasks. MIOE pairs target ontological relations with class-specific auxiliary attributes, prompt templates, and contextual inputs, enabling us to measure both intervention effects on the target relation and preservation of non-target subject information.


<!-- page 2 -->

We ask the following research questions: 

1. Can learned internal intervention targets reproduce the counterfactual behavior specified by ontology-level variables in entity typing and subsumption prediction? 

2. Can learned internal interventions change the ontologylevel target variable while leaving class-specific auxiliary variables invariant? 

3. How do intervention method, representation site, prompt type, and ontological class affect target-relation intervention effects and auxiliary preservation? 

Our contributions are summarized as follows: 

1. We formulate mechanistic interpretability for ontology engineering as a causal abstraction problem over ontologylevel variables, shifting the evaluation of ontological knowledge from behavioral correctness to testable internal interventions. 

2. We introduce MIOE, a mechanistic interpretability benchmark for ontology engineering covering entity typing and subsumption prediction. MIOE provides target ontology queries, class-specific auxiliary attributes, and prompt variants for evaluating interchange interventions over ontology-level variables. 

3. We provide a systematic empirical analysis of SAE, DBM/MDBM, and DAS/MDAS on Qwen3 models. Our results show that ontology-level predictions are causally accessible but only partially disentangled, and that multitask objectives and contiguous multi-layer interventions improve preservation and overall intervention quality. 

# **Related Work** 

## **Mechanistic Interpretability** 

Mechanistic interpretability aims to reverse-engineer the internal computation of black-box models by describing them in terms of transparent and human-interpretable algorithms (Geiger et al. 2025). A central difficulty is polysemanticity, where a single component or direction can encode multiple features. This difficulty is often linked to superposition: models can represent more features than their available dimensions would otherwise allow. Sparse Autoencoders (SAEs) have therefore become a prominent approach for decomposing activation vectors into sparse latent features that are more amenable to monosemantic interpretation (Bricken et al. 2023; Cunningham et al. 2023). Subsequent work has addressed limitations of vanilla SAEs from both architectural (Rajamanoharan et al. 2024; Gao et al. 2025; Bussmann, Leask, and Nanda 2024) and training-strategy perspectives (Ghilardi et al. 2025; Braun et al. 2024). A complementary line of mechanistic interpretability is grounded in causal abstraction, which asks whether a high-level causal model is faithfully implemented by the low-level computation of a neural network (Geiger et al. 2021, 2025). Interchange interventions provide an operational test for such alignments by replacing internal representations across inputs and measuring whether the resulting behavior changes according to the corresponding high-level variable. Methods in this family include Differential Binary Masking (DBM), which searches for axis-aligned 

causal feature masks (De Cao et al. 2020), and Distributed Alignment Search (DAS), which learns distributed subspaces aligned with interpretable causal variables (Geiger et al. 2024; Wu et al. 2023b). Alongside method development, evaluation has become an increasingly important problem, since interpretability has multiple desiderata and is difficult to define with a single metric (Mueller et al. 2025). Recent benchmarks therefore evaluate different aspects of interpretability, including feature disentanglement in RAVEL (Huang et al. 2024), known circuit recovery in InterpBench (Gupta et al. 2024), and SAE-specific performance across diverse evaluation dimensions in SAEBench (Karvonen et al. 2025). Recent work has also identified failure modes and phenomena that complicate feature-level interpretation, such as feature absorption (Chanin et al. 2025). However, existing evaluations largely focus on entity attributes, factual recall, or synthetic circuits, leaving high-level ontological knowledge under-explored. 

## **LLMs for Ontology Engineering** 

The rise of LLMs has made them increasingly relevant to ontology engineering tasks that have traditionally relied on ontology engineers, domain experts, and rule-based tools. More broadly, the relationship between LLMs and knowledge graphs has motivated growing interest in how parametric knowledge can be used for, combined with, or evaluated against explicit knowledge representations (Pan et al. 2023; Petroni et al. 2019). Recent work has investigated the use of LLMs across a wide range of ontology engineering tasks, including requirement elicitation (Zhang et al. 2025a), ontology subsumption inference (He et al. 2023), ontology learning (Babaei Giglou, D’Souza, and Auer 2023; Lo et al. 2024), ontology alignment (He et al. 2022), and ontology evaluation (Tsaneva et al. 2025). These studies show that LLMs and LLM-based systems can extract and generate ontological knowledge (Lo et al. 2024), improve on complex subsumption inference when a small number of annotated examples are available (He et al. 2023), and memorize certain ontological knowledge while using implicit knowledge for reasoning (Wu et al. 2023a). At the same time, this ability remains imperfect. Prior work reports limitations on specialized ontology tasks (He et al. 2023; Tsaneva et al. 2025; Wu et al. 2023a; Zhang et al. 2025b) and on long-tail factual knowledge (Huang et al. 2025). LLMs may perform well on some ontology-related tasks while failing on others, suggesting incomplete and unevenly accessible ontological knowledge (He et al. 2023; Wu et al. 2023a). 

# **The MIOE Benchmark** 

## **Task Formulation** 

MIOE is formulated as a causal abstraction benchmark for ontological knowledge. We use two ontology engineering tasks, entity typing and subsumption prediction, to define the high-level causal variables: a subject induces a target taxonomic variable, such as its entity type or superclass, together with non-target background information reflected by class-specific auxiliary attributes. The benchmark asks whether a mechanistic interpretability method can identify a low-level intervention target whose interchange intervention


<!-- page 3 -->

matches this high-level counterfactual: replacing the base subject’s target taxonomic value with the source subject’s value while preserving the base subject’s auxiliary values. 

Formally, let _τ_ denote the target axiom type, with _τ_ = instance of for entity typing and _τ_ = subclass of for subsumption prediction. Let _Sτ_ be the set of subjects for axiom type _τ_ , and let _cτ_ ( _s_ ) _⊂Cτ_ be the ground-truth set of ontology classes for subject _s_ . For _τ_ = instance of, each subject _s ∈Sτ_ is an entity, and the model predicts a class label _yτ_ ( _s_ ). For _τ_ = subclass of, each subject _s_ is a class or concept, and the model predicts a parent class _yτ_ ( _s_ ). In addition to the target ontological relation, each subject _s_ is associated with a set of class-specific auxiliary attributes _A_ ( _s_ ). For each attribute _A ∈A_ ( _s_ ), the model predicts an attribute value _yA_ ( _s_ ), with ground-truth value _vA_ ( _s_ ). We write _x_ = _p_ ( _s_ ) for the instantiated model input obtained by applying prompt template _p_ to subject _s_ , with _p ∈{pτ , pA, pw}_ denoting target-relation, auxiliary-attribute, or Wikipedia-derived contextual prompts. 

The mechanistic interpretability task tests whether this high-level causal description can be supported by low-level interventions in the language model. For each target axiom type _τ_ , we ask whether there exists a low-level intervention target _Fτ_ such that interchange interventions on _Fτ_ produce the behavior predicted by the high-level model: the target ontological prediction transfers from the source subject, while class-specific auxiliary predictions remain those of the base subject. To test this, we use interchange interventions between a base subject _s_ base and a source subject _s_ source such that _cτ_ ( _s_ base) and _cτ_ ( _s_ source) differ. Let _M_ denote the model under analysis. For a generic low-level intervention target _F_ , base input _x_ base, and source input _x_ source, we define the interchange intervention as 



<!-- Start of picture text -->
II( M, F, x base ,x source) :=<br>MF ← GetFeature( M ( x source) ,F  )( x base) (1)<br><!-- End of picture text -->

where the value of _F_ in the computation for _x_ base is replaced with the value induced by _x_ source. A successful intervention target _Fτ_ should satisfy two requirements. First, it should support _target-answer replacement_ : when the base input queries the target relation, intervening with the source should change the prediction from the base subject’s target label to the source subject’s target label. Second, it should satisfy _auxiliary invariance_ : when the base input queries an auxiliary attribute, the same intervention should preserve the base subject’s attribute value. For example, in instance of, the base class assertion may be city(Amsterdam), while the source class assertion is country(Australia). After intervening with the source, a target query such as _Amsterdam is an instance of_ should output _country_ , whereas an auxiliary prompt such as _“Amsterdam” belongs to the country of_ should still output the base auxiliary value _Netherlands_ . 

# **Dataset** 

We construct the MIOE dataset for evaluating interchange interventions over the two target axiom types. Each axiomtype subset is organized around subjects, ontology target classes, class-specific auxiliary attributes and values, and 

prompt templates. Dataset statistics are reported in Table 1, with additional construction details provided in the supplementary materials. The dataset is sampled and refined from Wikidata (Vrandečić 2012), WordNet (Fellbaum 2005), and schema.org (Guha, Brickley, and Macbeth 2016). To support cross-class interventions, the subject sets are organized around diverse high-level classes: 54 classes for instance of and 39 classes for subclass of. For each subject, we provide a set of class-specific attributes and values for evaluating auxiliary invariance. Detailed attribute information is provided in the supplementary materials. 

The prompt template set consists of two parts, following a RAVEL-style sampling strategy (Huang et al. 2024). The first part consists of task-specific templates, including templates for entity typing, subsumption prediction, and attribute-based queries. The second part consists of Wikipedia-based prompt samples drawn from Wikipedia corpus sentences containing the corresponding subjects (Wikimedia Foundation 2022). The two prompt sets play complementary roles in the benchmark. The ontology-oriented templates provide controlled queries for both target axioms and auxiliary attributes, while the Wikipedia-based prompts place the same subjects in more natural contexts. This separation allows us to evaluate whether the identified intervention targets remain effective beyond prompt formats and under contextualized surface realizations. 

We use these prompt families to define two evaluation settings. The Entity setting evaluates held-out subjects while reusing training prompt templates, whereas the Context setting evaluates held-out prompt templates while reusing training subjects. In both settings, the source input is instantiated with a source subject and may use either an ontology-template prompt or a Wikipedia-derived contextual prompt. 

# **Evaluation** 

Because target class labels and auxiliary attribute values can admit multiple valid surface forms, we evaluate predictions against accepted ground-truth answer sets. A target relation prediction is counted as correct when _yτ_ ( _s_ ) _∈ cτ_ ( _s_ ), and an auxiliary prediction is counted as correct when _yA_ ( _s_ ) _∈ vA_ ( _s_ ). Following the benchmark construction, we evaluate interventions only on retained prompt instances where the unintervened model already produces an accepted answer. Base-model accuracies before this filtering step are reported in the supplementary materials. 

The task formulation above defines the intervention operator and the two desired behaviors. We instantiate them as Cause and Iso metrics, following (Huang et al. 2024) and adapting them to ontological relations. Let _Eτ_<sup>cause</sup> denote the retained Cause examples for axiom type _τ_ . Each example _e ∈Eτ_<sup>cause</sup> contains a base subject _s_ base, a source subject _s_ source, a target-relation base input _x_ base = _pτ_ ( _s_ base), and a source input _x_ source instantiated with _s_ source. The examplelevel Cause indicator is 



<!-- Start of picture text -->
Cause( e ) := I(II( M, Fτ , x base , x source)  ∈ cτ ( s source))  .<br><!-- End of picture text -->



<!-- Start of picture text -->
(2)<br><!-- End of picture text -->

Similarly, let _Eτ_<sup>iso</sup> denote the retained auxiliary-invariance examples. Each example _e ∈Eτ_<sup>iso</sup> contains a base subject _s_ base, a source subject _s_ source, an auxiliary attribute _A ∈_


<!-- page 4 -->

|**Axiom Type**|**# Classes**|**# Subjects**|**# Attributes**<br>**(avg./class)**|**Avg. # Attribute Values**<br>**(per subj. / per attr.)**|**# Prompt Templates**<br>**(avg./class)**|
|---|---|---|---|---|---|
|instance of|54|1,099|376 (7.0)|12.0 / 2.0|4,288 (79.4)|
|subclass of|39|1,113|160 (4.1)|51.8 / 17.1|2,095 (53.7)|



Table 1: Dataset statistics by axiom type, including counts of domain classes, subjects, auxiliary attributes and values, and prompt templates. For auxiliary attributes, we report the average number of values per subject and per instantiated attribute. 

_A_ ( _s_ base), an auxiliary base input _x_ base = _pA_ ( _s_ base), and a source input _x_ source instantiated with _s_ source. The examplelevel Iso indicator is 



<!-- Start of picture text -->
Iso( e ) := I(II( M, Fτ , x base , x source)  ∈ vA ( s base))  . (3)<br><!-- End of picture text -->

We aggregate scores at the task level rather than directly over raw examples. Each group contains retained intervention examples sharing the same base prompt template, split, and evaluation type. We first average example-level success within each group and then macro-average across groups, preventing prompt groups with more retained examples from dominating the reported score. Let _Gτ_<sup>cause</sup> and _Gτ_<sup>iso</sup> denote the resulting sets of Cause and Iso evaluation groups, respectively. We define 



<!-- Start of picture text -->
1 1<br>Cause τ := � � Cause( e ) , (4)<br>|Gτ cause | g∈Gτ cause |g| e∈g<br><!-- End of picture text -->



<!-- Start of picture text -->
1 1<br>Iso τ := � � Iso( e ) , (5)<br>|Gτ iso | |g|<br>g∈Gτ iso e∈g<br><!-- End of picture text -->

and the final disentanglement score as 



<!-- Start of picture text -->
Disentangle τ := 1 (6)<br>2 (Cause τ + Iso τ )  .<br><!-- End of picture text -->

# **Experiments** 

## **Mechanistic Interpretability Methods** 

A range of mechanistic interpretability methods can be instantiated in MIOE. We evaluate SAE, DBM, and DAS, along with the multi-task variants MDBM and MDAS, following prior work (Huang et al. 2024), and extend DAS/MDAS to multi-layer settings. Most methods operate on a single residual-stream intervention site: a fixed layer _ℓ_ and the subject-token position determined by each prompt template. Multi-layer DAS and MDAS instead intervene on a small layer window, using separate subspaces at each layer. For a single-layer intervention site, each intervention example _e_ induces a base activation _z_ = _h_<sup>(</sup><sup>_ℓ_)</sup> ( _x_<sup>(</sup> base<sup>_e_)) and a source activa-</sup> tion _z_<sup>_′_</sup> = _h_<sup>(</sup><sup>_ℓ_)</sup> ( _x_<sup>(</sup> source<sup>_e_)). Each method defines an intervention</sup> target _Fτ_ , together with an intervention operator Γ _ϑ_ ( _z, z_<sup>_′_</sup> ) that produces an intervened representation _z_ ˜. Replacing _z_ with _z_ ˜ in the forward pass instantiates the interchange intervention operator II( _M, Fτ , x_ base _, x_ source) defined in the task formulation. 

**SAE** SAE provides a two-stage alternative to counterfactual training. Instead of directly optimizing an intervention subspace against cause or iso supervision, SAE first learns a sparse 

latent representation of activations at the intervention site, and only then identifies a subset of latent features associated with the target ontological relation. Let _a_ = _Eϕ_ ( _z_ ) _∈_ R<sup>_d_lat</sup> be the encoder output and _z_ ˆ = _Dψ_ ( _a_ ) the decoder reconstruction, where _d_ lat is the latent dimension and the encoder includes a nonlinearity that encourages non-negative sparse activations. The autoencoder is trained on unlabeled activations by minimizing 



<!-- Start of picture text -->
L SAE = E z ∥z − Dψ ( Eϕ ( z )) ∥ 2 2 + β∥Eϕ ( z ) ∥ 1 .<br>� �<br><!-- End of picture text -->

After learning the latent space, SAE instantiates the intervention target as a latent feature set _Fτ ⊆{_ 1 _, . . . , d_ lat _}_ , selected by fitting a sparse linear classifier on latent activations to predict the target ontological labels. The resulting intervention is performed in latent space: 



<!-- Start of picture text -->
i ∈ Fτ ,<br>a ˜ i = ΓSAE( z, z ′ ) =  Dψ (˜ a ) .<br>� EEϕϕ (( zz′ )) ii,, i ∈/ Fτ ,<br><!-- End of picture text -->

**DBM** DBM instantiates _Fτ_ as an axis-aligned subset of residual-stream coordinates in the original representation basis, learning a sparse selector over the _d_ coordinates of _z_ . Let _α ∈_ R<sup>_d_</sup> be mask logits, _π_ = _σ_ ( _α/T_ ) _∈_ [0 _,_ 1]<sup>_d_</sup> the relaxed mask at temperature _T_ . We write _Pπ_ = diag( _π_ ) and let _I ∈_ R<sup>_d×d_</sup> denote the identity matrix. The DBM intervention is 



<!-- Start of picture text -->
ΓDBM( z, z ′ ) = ( I − Pπ ) z  +  Pπz ′ =  z  +  Pπ ( z ′ − z ) .<br><!-- End of picture text -->

The relaxed mask gives a coordinate-wise interpolation between base and source activations; in the hard-mask limit, selected coordinates are copied from source to base while the remaining coordinates are preserved. The DBM objective combines supervision on retained Cause examples with sparsity regularization on _π_ : 



<!-- Start of picture text -->
L DBM =<br>E e∼Eτ cause �CE � Mz← ΓDBM( z,z′ )( x base ( e ) ) , cτ ( s source ( e ) ) ��<br>+  λ∥π∥ 1 .<br><!-- End of picture text -->

**DAS** DAS assumes that the target concept may be distributed across neurons and should therefore be modeled as a low-dimensional linear subspace. We directly parameterize this feature subspace instead of learning a full _d × d_ rotation. Let _W ∈_ R<sup>_k×d_</sup> be a row-orthonormal matrix whose row span instantiates the intervention target _Fτ_ . The corresponding orthogonal projector is _PW_ = _W_<sup>_⊤_</sup> _W_ , and the intervention is 

ΓDAS( _z, z_<sup>_′_</sup> ) = ( _I − PW_ ) _z_ + _PW z_<sup>_′_</sup> = _z_ + _W_<sup>_⊤_</sup> _W_ ( _z_<sup>_′_</sup> _− z_ ) _._


<!-- page 5 -->

This exchanges only the component of the representation that lies in the learned subspace, while leaving the orthogonal complement unchanged. DAS is trained on retained Cause examples: 



<!-- Start of picture text -->
L DAS =<br>E e∼Eτ cause �CE � Mz← ΓDAS( z,z′ )( x base ( e ) ) , cτ ( s source ( e ) ) ��<br><!-- End of picture text -->

**Multi-task DAS & DBM** The objectives above train the intervention to change the target answer but do not explicitly train it to preserve auxiliary answers. We therefore use multitask variants, MDBM and MDAS, that additionally include auxiliary-invariance examples (Huang et al. 2024). For each training example _e_ , define the desired output 



<!-- Start of picture text -->
y ⋆ ( e ) = cτ ( s ( source e ) ) , e ∈Eτ cause ,<br>� vA ( e )( s ( base e ) ) , e ∈Eτ iso ,<br><!-- End of picture text -->

where _A_<sup>(</sup><sup>_e_)</sup> is the auxiliary attribute queried in example _e_ . The generic multi-task objective is 



<!-- Start of picture text -->
L MT( ϑ ) =<br><!-- End of picture text -->



<!-- Start of picture text -->
E e∼Eτ cause ∪Eτ iso �CE � Mz← Γ ϑ ( z,z′ )( x base ( e ) ) , y⋆ ( e ) ��<br>+ Ω( ϑ ) .<br><!-- End of picture text -->

Here _ϑ_ denotes the method-specific parameters that instantiate the single-site intervention target _Fτ_ , e.g., mask logits for DBM/MDBM or a subspace matrix for DAS/MDAS. MDBM instantiates Γ _ϑ_ with ΓDBM and Ω( _ϑ_ ) = _λ∥π∥_ 1, while MDAS instantiates Γ _ϑ_ with ΓDAS and Ω( _ϑ_ ) = 0. This trains the intervention to satisfy both target-answer replacement and auxiliary invariance. 

**Multi-Layer DAS & MDAS** We extend DAS and MDAS to an ordered layer set _S_ = ( _ℓ_ 1 _, . . . , ℓm_ ), allowing the intervention target to span adjacent residual-stream layers. For each _ℓj ∈ S_ , let _sj_ denote the source representation at the prompt-specific subject-token position, and let _bj_ denote the base representation encountered at the same layer during the intervened forward pass. The layer-specific intervention is 



<!-- Start of picture text -->
Γ ( ϑ ℓ j j )( bj, sj ) =  bj +  P  ( ϑ ℓ j j )( sj − bj ) ,<br>Pϑ ( ℓ j j ) = ( W ( ℓj ) ) ⊤ W ( ℓj ) .<br><!-- End of picture text -->

The multi-layer intervention Γ<sup>_S_</sup> Θ _S_<sup>, with layer-specific parame-</sup> ters Θ _S_ = _{ϑj}_<sup>_m_</sup> _j_ =1<sup>and</sup><sup>_ϑj_=</sup><sup>_W_(</sup><sup>_ℓj_) for DAS/MDAS, applies</sup> these layer-specific interventions across the ordered layer set. This yields a joint multi-site intervention: all layer-specific subspaces are optimized together, and lower-layer interventions can affect the later base states encountered during the same forward pass. For multi-layer DAS, the training objective is 



<!-- Start of picture text -->
L ML-DAS(Θ S ) =<br>E e∼Eτ cause �CE � MS← Γ S Θ S ( x base ( e ) ) , cτ ( s source ( e ) ) �� .<br>For multi-layer MDAS, the corresponding objective is<br>L ML-MDAS(Θ S ) =<br>E e∼Eτ cause ∪Eτ iso �CE � MS← Γ S Θ S ( x base ( e ) ) , y⋆ ( e ) �� .<br><!-- End of picture text -->

## **Setup** 

We evaluate Qwen3-4B and Qwen3-8B, two 36-layer decoderonly Transformers with hidden sizes 2,560 and 4,096, respectively (Yang et al. 2025). The single-layer experiments cover both axiom types and include SAE, DBM, MDBM, DAS, and MDAS. All methods intervene on block-output residual-stream activations at the prompt-specific subjecttoken position. For single-layer experiments, we evaluate each of the 36 layers as the intervention layer. The multi-layer experiments evaluate DAS and MDAS on Qwen3-8B for both axiom types, using contiguous two- and four-layer windows. For multi-layer DAS/MDAS, we use _k × w_ to denote rank- _k_ subspaces applied at each layer of a contiguous _w_ -layer window. We evaluate 256 _×_ 4, 512 _×_ 2, and 512 _×_ 4, giving total intervention dimensions of 1024, 1024, and 2048, respectively, comparable to the single-layer DAS/MDAS ranks. Full configurations are provided in the supplementary materials. 

# **Results** 

We first evaluate whether learned intervention targets support the expected intervention behavior for the target ontology variable in entity typing and subsumption prediction, including evaluation on both Entity and Context prompt settings. We then analyze whether this behavior remains confined to the target axiom by checking preservation of class-specific auxiliary variables. Finally, we examine how method choice, intervention dimension, representation layer, multi-layer windows, and ontology-class structure affect the balance between target-answer change and auxiliary preservation. 

Table 2 summarizes the strongest Qwen3-8B single-layer results. Distributed subspace methods give the best overall performance, with MDAS achieving the highest Disentangle scores across both axiom types. Its Disentangle scores on Entity and Context are 0.592/0.587 for instance of and 0.513/0.542 for subclass of. This suggests that the identified intervention targets are not tied only to the entity-prompt split used in the main comparison. The Qwen3-4B results provided in the supplementary materials preserve the same method ordering, indicating that the result is not specific to the larger checkpoint. 

The Iso scores reveal that methods without explicit auxiliary-preservation supervision, such as SAE and DBM, can produce non-trivial effects on target ontology predictions while often perturbing auxiliary attribute values. Multi-task variants directly address this issue by adding preservation supervision, and the effect is visible in Table 2: across the Entity and Context columns, the best reported multi-task configurations improve Iso over the corresponding single-task method family by 0.081 on average, while reducing Cause by 0.052 on average. Disentangle nevertheless improves because the gain in preserving non-target information outweighs the reduction in Cause. The same Cause–Iso tension is visible along the intervention-size axis: within the reported DAS/MDAS and SAE settings, increasing the intervention dimension can improve Cause while reducing Iso in some configurations, rather than uniformly improving both. 

Figure 1 illustrates that the target-answer intervention effect is highly layer-dependent. Full layer-wise profiles for SAE,


<!-- page 6 -->

||||**ins**|**tance**|**of**||||**sub**|**class**|**of**|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|**Dimension **|**Layer**||**Entity**||**Context**<br>|**Dimension **|**Layer**||**Entity**||**Contex**|**t**|
||||**C**|**I**|**D**|**C**<br>**I**<br>**D**|||**C**|**I**|**D**|**C**<br>**I**|**D**|
|SAE|8192|13|0.472|0.352|0.412|0.399 0.344 0.371|16384|12|0.584|0.210|0.397|0.624 0.233|0.429|
|DBM|4096|10|0.441|0.409|0.425|0.385 0.407 0.396|4096|10|0.528|0.334|0.431|0.526 0.359|0.443|
|MDBM|4096|10|0.418|0.469|0.443|0.344 0.472 0.408|4096|13|0.491|0.389|0.440|0.490 0.409|0.450|
|DAS|1024|17|0.589|0.579|0.584|0.582 0.512 0.547|1024|22|0.509|0.483|0.496|0.625 0.445|0.535|
|MDAS|2048|17|0.527|0.658|**0.592**|0.481 0.692 **0.587**|2048|18|0.496|0.530|**0.513**|0.525 0.560|**0.542**|



Table 2: Best single-layer intervention results for Qwen3-8B. C/I/D denote Cause/Iso/Disentangle. For each axiom type and method, we report the layer/configuration with the strongest Entity Disentangle score. Dimension denotes subspace rank for DAS/MDAS, ambient mask dimension for DBM/MDBM, and latent width for SAE. Qwen3-4B results are reported in the supplementary materials. 



<!-- Start of picture text -->
1.0<br>Iso 1.0<br>0.8 DisentanCause gle GOAL<br>256×4 (25%) 512×4 (50%)<br>0.6 0.8 512×2 (25%) 512×4 (50%)<br>0.4 25%<br>50%<br>0.2 0.6 25%<br>0.0 29% 35% 63% 50%<br>0 5 10 15 20 25 30 35<br>Layer 0.4 54%<br>1.0 SAE 48%<br>Iso DBM<br>0.8 DisentanCause gle 0.2 MDBM DAS<br>MDAS<br>0.6 ML-DAS<br>ML-MDAS<br>0.4 0.0<br>0.0 0.2 0.4 0.6 0.8 1.0<br>0.2 Cause Score<br>0.0<br>0-3 6-9 12-15 18-21 24-27 30-33 Figure 2: Cause–Iso scores for selected<br>Layer Window instance of configurations with different<br>Score<br>Iso Score<br>Score<br><!-- End of picture text -->

Figure 2: Cause–Iso scores for selected Qwen3-8B instance of configurations with different intervention dimensions. Percent labels indicate the dimensionality of _Fτ_ under each method’s parameterization; for multi-layer interventions, total rank is reported relative to a single-layer residual-stream width. 

Figure 1: Representative layer profiles for Qwen3-8B on instance of. The top panel shows single-layer MDAS with rank 2048, and the bottom panel shows four-layer MDAS with 256 _×_ 4 contiguous windows. Both panels report Cause, Iso, and Disentangle. 

single-layer interventions, and multi-layer interventions are provided in the supplementary materials. Across methods, Cause is weak in the earliest layers, rises through the middle of the model, and often reaches its strongest values in middle or middle-to-late layers. Later layers often obtain strong Iso, but Cause can simultaneously fall to very low values, suggesting that the intervention may no longer be effectively changing the model’s generated output. 

Contiguous layer-window interventions further improve over comparable single-layer settings, as shown in Table 3. The table reports both axiom types and gives ∆ against the single-layer result with the same method and total dimension. Figure 2 provides the same view geometrically: the multi-layer configurations move upward in Cause–Iso space relative to the corresponding single-layer DAS/MDAS points, mainly by improving Iso while retaining substantial Cause. On 

Qwen3-8B instance of, the strongest rows are four-layer windows: DAS 512 _×_ 4 reaches 0.667 Disentangle, while MDAS 256 _×_ 4 and 512 _×_ 4 reach 0.666 and 0.663. The gain is not explained by total dimensionality alone: at total dimension 1024, 256 _×_ 4 outperforms 512 _×_ 2 for both DAS and MDAS. These results suggest that the relevant intervention target is better captured across a short middle-to-late layer interval than at a single residual-stream site. 

Furthermore, Figure 3 and additional class-level analyses in the supplementary materials show that intervention success varies substantially across ontology classes. Figure 3(a,b) shows that base-role and source-role classes have different Cause–Iso profiles. Classes with concrete and regular attribute profiles, such as airport, country, currency, and university, often achieve higher class-level Disentangle, whereas broader or more heterogeneous classes, such as body of water, geographical feature,


<!-- page 7 -->

<!-- Start of picture text -->
1. 0 1. 0<br>film award country airportcity currency national park protein<br>0. 8 science awardsoftwarenational park 0. 8 sculpture album research institute protein video gamedisease motorsport racing tracktourist attraction video game<br>island city currency disease<br>research institute universitycountry airport sculptureisland<br>0. 6 0. 6 international organization<br>software<br>algorithm<br>political party<br>first-level administrative division<br>0. 4 0. 4 type of sport<br>large language model<br>stock exchange<br>type of chemical entity<br>science award<br>0. 2 0. 2 painting<br>data set<br>chemical element<br>museum<br>0. 0 0. 0<br>0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0 −0.3 −0.2 −0.1 0.0 0.1 0.2 0.3<br>Cause Cause Base-role Disentangle − Source-role Disentangle<br>Iso Iso<br><!-- End of picture text -->

Figure 3: Class-level analysis of Qwen3-8B multi-layer MDAS for instance of. Left and middle: Cause–Iso scatter plots for base-role and source-role classes. Right: largest base–source role gaps, measured as base-role minus source-role Disentangle. Colors denote stronger base-role performance or stronger source-role performance . 

|_k × w_|**Method **|**Window **|**Cause**|**Iso**|**Disentangle (**∆**)**|
|---|---|---|---|---|---|
|||**inst**|**ance **|**of**||
|512_×_2|<sup>DAS</sup>|23–24|0.560|0.726|0.643 (+0.059)|
||<br>MDAS|22–23|0.529|0.730|0.629 (+0.038)|
|256_×_4|<sup>DAS</sup>|24–27|0.548|0.772|0.660 (+0.077)|
||<br>MDAS|22–25|0.590|0.741|0.666 (+0.074)|
|512_×_4|<sup>DAS</sup>|24–27|0.577|0.756|**0.667**(**+0.102**)|
||<br>MDAS|23–26|0.589|0.736|0.663 (+0.070)|
|||**subc**|**lass **|**of**||
|512_×_2|<sup>DAS</sup>|23–24|0.468|0.559|0.514 (+0.018)|
||<br>MDAS|22–23|0.440|0.617|0.529 (+0.036)|
|256 4|<sup>DAS</sup>|22–25|0.555|0.473|0.514 (+0.018)|
|_×_|<br>MDAS|21–24|0.486|0.616|0.551 (+0.058)|
|512 4|<sup>DAS</sup>|23–26|0.537|0.513|0.525 (+0.033)|
|_×_|<br>MDAS|22–25|0.537|0.593|**0.565**(+0.052)|



Table 3: Multi-layer DAS/MDAS results for Qwen3-8B. The _k × w_ column denotes a rank- _k_ subspace at each layer in a contiguous _w_ -layer window, and Window gives the contiguous layer span of the reported best configuration. ∆ reports the Disentangle improvement over the single-layer result with the same method and total dimension. 

food, biological process, and material, show lower scores and appear harder to change at the target level without also affecting auxiliary information. Figure 3(c) further shows role asymmetry: protein and video game are stronger as sources, whereas national park and tourist attraction are stronger as bases. This indicates that intervention difficulty depends not only on the class itself, but also on whether it supplies or receives the intervened representation. The supplementary analyses further show that similar class rankings recur across Qwen3-4B and Qwen3-8B, suggesting that this variation is not merely an artifact of one checkpoint. This gives MIOE a diagnostic role beyond aggregate method comparison: it identifies where ontology-level 

interventions are more effective and where they remain more tightly coupled to class-specific auxiliary information. Taken together, the results suggest that ontology-oriented predictions are causally accessible through learned intervention targets, while their separation from auxiliary class-specific information remains partial and class-dependent. 

# **Conclusion** 

We introduced MIOE, a causal abstraction benchmark for analyzing ontological knowledge in language models through interchange interventions. MIOE pairs target ontology variables from entity typing and subsumption prediction with class-specific auxiliary attributes, allowing us to test whether an internal intervention changes the target answer while preserving non-target information. 

Our experiments show that ontology-level predictions are mechanistically accessible but only partially disentangled. Multi-task objectives improve preservation of auxiliary answers, and contiguous layer-window interventions further improve over comparable single-layer settings, suggesting that the relevant computation is better captured across short middle-to-late layer spans than at a single residual-stream site. The class-level analysis also shows that intervention success varies substantially across ontology classes, indicating that aggregate scores hide meaningful differences in how different parts of the ontology are represented. 

Overall, these findings support a qualified interpretation of LLMs for ontology engineering. Correct ontological predictions do not by themselves imply a clean or modular internal mechanism for the corresponding axiom. Instead, MIOE suggests that ontological variables are causally accessible, but not cleanly separated from broader class-specific information, either because the representations are distributed and entangled with class-specific semantics or because current intervention-search methods remain insufficiently precise. Future work should extend this analysis to richer ontology constraints, broader model families, and settings that test whether ontology-level intervention behavior remains stable across domains, prompts, and complex reasoning contexts.


<!-- page 8 -->
