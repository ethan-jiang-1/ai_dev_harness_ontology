---
source: 2610.38326-mioe.pdf
part: appendix
converted: 2026-11-07
converter: pymupdf4llm
---

# Can LLMs Faithfully Solve Ontology Engineering Tasks? A Mechanistic Interpretability Study · 附录

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

# **Dataset Details** 

## **Dataset construction** 

Our dataset construction follows two design goals. First, the selected subjects should cover a broad range of ontology domains and popularity levels, following the head-totail motivation in factual-knowledge evaluation (Sun et al. 2024). Second, the selected subjects should not be so obscure that the underlying LLM fails on most target-relation or auxiliary-attribute queries, since the final benchmark retains only subject-template pairs for which the unintervened model predicts an accepted answer. We therefore sample a set of domains and select common but diverse ontology classes within each domain. For the instance of subset, we sample entities from each selected class by considering both their popularity level and the amount of structured information available on Wikidata, using the number of associated Wikidata statements as a practical proxy. For the subclass of subset, we similarly select parent classes whose subclasses cover a range of popularity levels, using the number of subclasses as a proxy. This sampling strategy aims to maximize ontology coverage while avoiding overly rare subjects that would be mostly removed by behavioral filtering. We retain at least ten candidate entities or subclasses for each selected class before filtering. To reduce ambiguity in factual evaluation, we avoid highly time-sensitive subjects and attributes whose values are expected to change frequently. Ground-truth attribute values are queried from Wikidata using SPARQL through the Wikidata Query Service. For attributes with corresponding values available in Wikipedia infoboxes, we cross-validate the Wikidata values against those infobox values. Conflicting values, missing values, and cases without aligned infobox evidence are manually checked against reliable web references. 

The class-specific attributes are defined at different levels for these two subsets. The first is at the instance level, where attribute values are specified for each instance. The second is at the class level, where attributes are more abstract, such as the general study object for an academic discipline. 

**Data appendix and release.** The anonymous code-anddata appendix contains the class CSV files, attribute-value dictionaries, prompt-template files, Wikipedia-derived context prompts, and construction scripts needed to reconstruct the benchmark instances. Upon publication, the code and data will be released under a research-permissive license. 

# **Implementation Details** 

The single-site SAE feature-selection pipeline and the DBM/MDBM and DAS/MDAS intervention implementations are adapted from the released RAVEL codebase (Huang et al. 2024).<sup>1</sup> We modify them for ontology-specific prompts, labels, and splits, and add the multi-layer DAS/MDAS extension described below. All intervention training and evaluation jobs used a single NVIDIA A100 GPU. The submitted code appendix specifies the software environment. Table 4 lists model-level settings, input lengths, batch sizes, seeds, and realized training-pair counts. 

1https://github.com/explanare/ravel 

## **Method-specific Implementation** 

**SAE.** For each site, we train a single-layer ReLU encoder with a linear decoder on unlabeled target-relation training activations ending at the subject position. We evaluate latent expansion ratios _d_ lat _/d ∈{_ 2 _,_ 4 _}_ , giving 5,120/10,240 latent dimensions for Qwen3-4B and 8,192/16,384 for Qwen3-8B. The autoencoder uses mean-squared reconstruction error plus mean absolute latent activation with coefficient _β_ = 0 _._ 5, optimized with AdamW at initial learning rate 10<sup>_−_4</sup> , weight decay 10<sup>_−_4</sup> , and cosine decay to 0 _._ 5 of the initial rate. We then fit an _ℓ_ 1-regularized linear SVM with _C ∈{_ 0 _._ 1 _,_ 1 _,_ 10 _,_ 1000 _}_ on latent codes to instantiate _Fτ_ as a selected latent feature set. During intervention, only these selected latent dimensions are replaced with source values before decoding. 

**DBM and MDBM.** DBM and MDBM learn one mask logit per residual-stream coordinate, giving ambient mask widths of 2,560 for Qwen3-4B and 4,096 for Qwen3-8B. The logits are initialized to zero, the temperature is linearly annealed from 10<sup>_−_2</sup> to 10<sup>_−_7</sup> , and optimization uses AdamW with constant learning rate 10<sup>_−_4</sup> and zero weight decay. DBM uses cause-only answer-token supervision with an _ℓ_ 1 coefficient _λ_ = 10<sup>_−_3</sup> on the relaxed mask, while MDBM mixes Cause examples with auxiliary examples and uses _λ_ = 0. Evaluation thresholds the relaxed mask at 0 _._ 5 and exchanges only the selected original-basis coordinates. Thus, the _Dimension_ column in the main paper denotes ambient mask width rather than effective feature size. The effective DBM/MDBM sizes are 1,631/1,684 and 2,211/2,580 for Qwen3-4B and Qwen38B on instance of, and 758/1,467 and 1,586/2,043 on subclass of. 

**DAS and MDAS.** DAS and MDAS learn a row-orthonormal map _W ∈_ R<sup>_k×d_</sup> , implemented as a bias-free linear map with PyTorch orthogonal parametrization to maintain _WW_<sup>_⊤_</sup> = _Ik_ . Single-layer experiments use _k ∈{_ 1024 _,_ 2048 _}_ , while multilayer ranks are specified below. The language model is frozen, and only the subspace parameters are optimized with AdamW at constant learning rate 10<sup>_−_4</sup> , zero weight decay, and no additional regularization. Training uses autoregressive crossentropy on answer tokens: DAS uses Cause examples whose target is the accepted answer corresponding to _cτ_ ( _s_ source), whereas MDAS mixes these Cause examples with auxiliary examples targeted to _vA_ ( _s_ base). 

## **Multi-layer Realization** 

Let _S_ = ( _ℓ_ 1 _, . . . , ℓm_ ) be an intervention window with _ℓ_ 1 _< · · · < ℓm_ , and let _zℓ_ ( _x_ ) denote the block-output residualstream activation at the subject position in layer _ℓ_ . We first run one clean source forward pass and cache 



<!-- Start of picture text -->
sj =  zℓj ( x source) , j = 1 , . . . , m.<br><!-- End of picture text -->

No intervention is applied during this pass, so every _sj_ is a clean source activation rather than the output of an earlier source-side intervention. We then run the base input once. Writing _b_ 1 = _zℓ_ 1( _x_ base) and letting Φ _ℓj−_ 1 _→ℓj_ denote the frozen Transformer computation between two intervention


<!-- page 11 -->

sites, the base execution follows 



<!-- Start of picture text -->
bj = Φ ℓj− 1 →ℓj ( ˜ bj− 1) ,<br>˜ bj = Γ ( ϑ ℓ j j )( bj, sj ) , j = 2 , . . . , m.<br><!-- End of picture text -->

with<sup>˜</sup> _b_ 1 = Γ<sup>(</sup> _ϑ_<sup>_ℓ_</sup> 1<sup>1)(</sup><sup>_b_1</sup><sup>_, s_1).Thus,thehooksareinvokedin</sup> ascending layer order: the base activation encountered at _ℓj_ already reflects all interventions at lower layers. The layerspecific parameters _{ϑj}_<sup>_m_</sup> _j_ =1<sup>are optimized jointly under the</sup> same autoregressive objective. 

We evaluate contiguous two- and four-layer windows. For DAS and MDAS, each layer has an independent rank- _k_ orthogonal map, so the total intervention dimension is _mk_ . The two-layer sweep uses _k_ = 512 (1,024 dimensions in total), while the four-layer sweep uses _k ∈{_ 256 _,_ 512 _}_ (1,024 or 2,048 dimensions in total). All reported multi-layer results use block-output interventions at the subject position. 

# **Additional Results** 

## **LLM Performance on Ontology Engineering Tasks** 

Table 5 summarizes the LLMs’ micro- and class-macro accuracy on target axiom prediction and auxiliary attribute prediction under each axiom type. 

## **Class-Level Intervention Analysis** 

Figures 4 and 5 break down the four MDAS class-evaluation runs by ontology class. We use the same role terminology as in the interchange-intervention formulation: the base class is the class of the subject whose computation receives the intervention, whereas the source class is the class of the subject that supplies the intervened representation. In the base-role panels, each point aggregates examples whose base subject belongs to that class. In the source-role panels, each point aggregates examples whose source subject belongs to that class. All scores use the Entity split and task-macro aggregation: each prompt-specific evaluation condition is scored first, and the resulting condition-level scores are then averaged with equal weight. 

**Class-level heterogeneity is systematic.** The scatter plots show substantial class-level heterogeneity behind the aggregate scores reported in the paper. Table 6 reports Cause, Iso, and Disentangle after first computing scores for each ontology class and then averaging over classes. For instance of, Iso is consistently higher than Cause under this class-level averaging. This means that the main bottleneck is not preserving auxiliary attributes after intervention, but changing the target ontology answer toward the source subject’s answer. For subclass of, the pattern is different: Cause is comparable to or higher than Iso, especially for classes in the base role. This supports the paper’s aggregate finding that subsumption prediction is more entangled with surrounding semantic and attribute information than entity typing. 

**The class ranking is stable across model scale.** For each axiom type and role, we rank ontology classes by their classlevel Disentangle scores. Table 7 reports Spearman rank correlations over these class rankings. The first two columns compare Qwen3-8B and Qwen3-4B within the same role, 

asking whether the same classes are easy or difficult across model sizes. The last two columns compare base-role and source-role rankings within the same model, asking whether classes that work well as intervention bases also work well as intervention sources. The high cross-model correlations show that class-level variation is not merely model-specific noise. The much lower base–source correlations show that class difficulty is role-dependent. 

Figure 7 visualizes these rank correlations. Points close to the diagonal correspond to classes whose relative intervention difficulty is similar in Qwen3-8B and Qwen3-4B, while offdiagonal points identify classes whose difficulty changes substantially with model scale. 

The last two columns of Table 7 show a second, more subtle pattern: base and source rankings are only weakly related. Thus, being easy to rewrite in the base role is not the same as being effective in the source role for rewriting other subjects. This role asymmetry is important mechanistically. It suggests that class-level ontology representations do not behave like a single undirected semantic distance metric. Instead, a class can perform well in the base role, the source role, both, or neither. For example, in instance of, stock exchange is strong in the base role but weak in the source role, whereas disease, data set, and algorithm are stronger in the source role. In subclass of, measuring instrument, theory, and scientific instrument are stronger in the base role, while algorithm, music, activity, and creative work are stronger in the source role. 

Figure 8 shows the largest base–source role gaps directly. Positive values mark classes that are more successful in the base role; negative values mark classes that are more successful in the source role. 

**High-performing classes tend to have compact semantic signatures.** Table 8 lists recurring high-scoring classes across Qwen3-8B and Qwen3-4B. For instance of, stable high-scoring classes include concrete, attribute-regular categories such as airport, city, country, currency, software, and university. These classes often have distinctive attribute profiles: airports have location and code attributes; currencies have issuers, jurisdictions, and symbols; cities and countries have administrative and demographic attributes. Such compact semantic signatures make the target class easier to change without disrupting unrelated attributes. For subclass of, stable high-scoring classes in the base role include flower, tree, measuring instrument, and medical device, while stable high-scoring classes in the source role include activity, creative work, emotion, and music. The lower-scoring subclass classes often correspond to broad or internally diverse superclasses such as food, biological process, body of water, geographical feature, and material. These categories are not simply harder labels; they also have more diffuse attribute neighborhoods, making it harder to intervene on the taxonomic relation while preserving auxiliary semantic facts. 

**Pair-level effects are directionally asymmetric beyond isolated extremes.** For an unordered class pair _{A, B}_ ,


<!-- page 12 -->

|**Setting**|**Qwen3-4B**|**Qwen3-8B**|
|---|---|---|
|Layers / hidden size|36 / 2,560|36 / 4,096|
|Prompt / answer length|48 / at most 3 tokens|48 / at most 3 tokens|
|Site / position|block output / last subject subtoken|block output / last subject subtoken|
|Supervised train / eval batch|128 / 128|128 / 128|
|Epochs|6|6|
|Random seed|42|42|
|instance ofCause / Iso pairs|54,184 / 68,936|55,888 / 70,872|
|subclass ofCause / Iso pairs|44,864 / 21,448|43,552 / 31,720|



Table 4: Experimental settings. Training pair counts are the examples passed to the supervised methods after dataset construction. 

|||**instan**|**ce of**|||**subcla**|**ss of**||
|---|---|---|---|---|---|---|---|---|
|**Model**|**Target**<br>**Micro**|**Target**<br>**Macro**|**Attr.**<br>**Micro**|**Attr.**<br>**Macro**|**Target**<br>**Micro**|**Target**<br>**Macro**|**Attr.**<br>**Micro**|**Attr.**<br>**Macro**|
|Qwen3-4B|92.4|92.1|59.7|58.7|89.2|87.4|69.2|68.8|
|Qwen3-8B|94.7|94.3|64.9|63.8|93.0|91.8|69.1|68.3|



Table 5: Base LLM performance on ontology-oriented knowledge engineering queries. **Target Micro/Macro** denotes micro- and class-macro accuracy on target axiom queries; **Attr. Micro/Macro** reports the corresponding accuracy on auxiliary attribute queries. 

|**Model**|**Role**|**Cause**|**Iso**|**Disent.**|**∆**|
|---|---|---|---|---|---|
||**in**|**stanc**|**e of**|||
|Qwen3-8B|Base|0.539|0.674|0.606|+0.135|
|Qwen3-8B|Source|0.507|0.674|0.590|+0.167|
|Qwen3-4B|Base|0.521|0.613|0.567|+0.091|
|Qwen3-4B|Source|0.493|0.612|0.552|+0.119|
||**su**|**bclas**|**s of**|||
|Qwen3-8B|Base|0.545|0.446|0.496|-0.100|
|Qwen3-8B|Source|0.532|0.477|0.504|-0.055|
|Qwen3-4B|Base|0.527|0.447|0.487|-0.080|
|Qwen3-4B|Source|0.498|0.468|0.483|-0.030|



Table 6: Mean scores over ontology classes in the base and source roles. ∆ reports Iso _−_ Cause, with positive values indicating that changing the target answer is harder than preserving auxiliary answers and negative values indicating the reverse. 

# define the reciprocal gap 

∆ _A,B_ = _|D_ ( _A ← B_ ) _− D_ ( _B ← A_ ) _| ,_ 

where _D_ ( _A ← B_ ) is the task-macro Disentangle score when a source subject whose target ontology class is _B_ is used to intervene on a base subject whose target ontology class is _A_ . We retain only pairs with at least five Cause and five Iso examples in both directions. 

Figure 10 and Table 9 summarize the resulting reciprocal gaps. The median gap ranges from 0.132 to 0.179, and 29.8– 41.8% of eligible pairs differ by at least 0.2. Thus, directional asymmetry is not limited to a few extreme examples, although very large gaps remain less common: only 5.0–12.1% exceed 0.4. The largest eligible examples illustrate the scale of this 

tail. In Qwen3-8B instance of, animal _←_ academic journal scores 0.742 versus 0.194 in the reverse direction; in Qwen3-4B subclass of, body of water _←_ food scores 0.711 versus 0.042. 

The ordering across model sizes is not monotonic: Qwen34B has the larger median for instance of, whereas Qwen3-8B has the larger median and heavier tail for subclass of. More fundamentally, the same unordered class pair can change substantially when its base and source roles are exchanged. This suggests that intervention success is not determined only by undirected class similarity, but also by the ordered base–source assignment. Because reciprocal pairs sharing a class are statistically dependent, these distributions are interpreted descriptively rather than as independent samples for pairwise significance testing. 

Overall, the class-level analysis refines the aggregate findings in the main paper. The main results show that ontologyoriented predictions are causally accessible through learned intervention targets, while their separation from class-specific auxiliary information remains partial. The class-level results show that this partial separation is unevenly distributed across the ontology: MDAS performs better for classes with more regular attribute profiles, and worse for broader or more heterogeneous classes whose target labels are more tightly coupled with auxiliary semantics. The role- and pair-level analyses further show that intervention difficulty depends on the ordered base–source assignment, not only on the class considered in isolation. Together, these results suggest that ontology-level variables are mechanistically accessible in LLMs, but their separability from class-specific information depends on both class structure and intervention direction.


<!-- page 13 -->

|**Ai**||**Base**|**Source**|**8B**|**4B**|
|---|---|---|---|---|---|
|**xom**||**cross-model**_ρ_|**cross-model**_ρ_|<br>**base–source**_ρ_|**base–source**_ρ_|
|instance|of|0.831|0.810|0.273|0.267|
|subclass|of|0.752|0.671|-0.082|0.059|



Table 7: Rank stability of class-level Disentangle scores. Each value is Spearman’s _ρ_ over ontology classes. Base and Source cross-model _ρ_ compare Qwen3-8B and Qwen3-4B class rankings within the same role. The 8B and 4B base–source _ρ_ columns compare base-role and source-role rankings within the same model. 

|**Axiom**||**Role**|**Recurring high-scoring classes**|
|---|---|---|---|
|instance|of|Base|airport; city; country; currency; science award; software; stock exchange|
|instance|of|Source|airport; city; country; currency; data set; disease; type of sport; university|
|subclass|of|Base|animal organ; flower; measuring instrument; medical device; organization; theory; tree|
|subclass|of|Source|activity; creative work; emotion; fish; flower; music|



Table 8: Representative recurring high-scoring classes from the class-level Disentangle rankings. Rankings are computed separately for each axiom type and base/source role on the Entity split, and listed classes are high-scoring cases for both Qwen3-8B and Qwen3-4B within the same role. 

# **Qwen3-4B Single-Layer Results** 

Table 10 reports the corresponding single-layer results for Qwen3-4B. The results preserve the complete method ordering observed for Qwen3-8B on both Entity and Context: MDAS _>_ DAS _>_ MDBM _>_ DBM _>_ SAE. 

# **Layer-Wise Intervention Profiles** 

Figure 11 shows the SAE layer-wise profiles. Figure 12 shows the single-layer DBM/MDBM profiles. Figures 13 and 14 show the single-layer DAS/MDAS profiles grouped by subspace rank. Figures 15 and 16 report Qwen3-8B multilayer DAS/MDAS fixed-window profiles. For single-layer profiles, we report 12 of the 36 layers. For multi-layer profiles, we report 12 evenly spaced contiguous windows spanning the first to last transformer layer. 

# **Highest-Cause Single-Layer Configurations** 

Table 11 reports the highest-Cause single-layer configuration for each model, axiom type, and method.


<!-- page 14 -->

|**Axiom**||**Model**|**_N_**|**Mean**|**Median [IQR]**|**Pr(∆****_≥_0****_._2)**|**Pr(∆****_≥_0****_._4)**|
|---|---|---|---|---|---|---|---|
|intn|f|Qwen3-8B|121|0.166|0.132 [0.076, 0.256]|29.8%|5.0%|
|sace|o|Qwen3-4B|141|0.184|0.158 [0.069, 0.253]|39.0%|7.1%|
|bl|f|Qwen3-8B|91|0.204|0.179 [0.090, 0.287]|41.8%|12.1%|
|sucass|o|Qwen3-4B|52|0.185|0.152 [0.075, 0.291]|36.5%|7.7%|



Table 9: Distribution of absolute reciprocal Disentangle gaps ∆ _A,B_ over eligible unordered class pairs for the best MDAS setting in each model–axiom combination. _N_ is the number of eligible pairs, IQR denotes the interquartile range, and probability columns report the fraction of eligible pairs exceeding each threshold. Eligibility requires at least five Cause and five Iso examples in each direction. 

|**Axiom**||**Method **|**Dimension **|**Layer**||**Ent**|**ity**||**Con**|**text**|
|---|---|---|---|---|---|---|---|---|---|---|
||||||**Cause**|**Iso**|**Disentangle **|**Cause**|**Iso**|**Disentangle**|
|||SAE|5120|14|0.408|0.375|0.391|0.350|0.369|0.359|
|||DBM|2560|10|0.458|0.354|0.406|0.400|0.350|0.375|
|instance|of|MDBM|2560|10|0.404|0.436|0.420|0.340|0.430|0.385|
|||DAS|1024|22|0.516|0.537|0.527|0.489|0.509|0.499|
|||MDAS|2048|16|0.520|0.592|**0.556**|0.471|0.639|**0.555**|
|||SAE|10240|13|0.562|0.257|0.409|0.633|0.252|0.442|
|||DBM|2560|12|0.525|0.333|0.429|0.549|0.351|0.450|
|subclass|of|MDBM|2560|12|0.526|0.360|0.443|0.536|0.370|0.453|
|||DAS|2048|16|0.632|0.289|0.460|0.683|0.302|0.492|
|||MDAS|2048|20|0.511|0.510|**0.511**|0.540|0.591|**0.566**|



Table 10: Qwen3-4B single-layer intervention results under the same reporting rule as the Qwen3-8B comparison. For each axiom type and method, we report the layer/configuration with the strongest Entity Disentangle score and evaluate the same configuration on Context. Dimension denotes subspace rank for DAS/MDAS, ambient mask dimension for DBM/MDBM, and latent width for SAE. 

|**Axiom**|**Model**|**Method**|**Dim.**|**Layer**|**Cause**|**Iso**|**Disentangle**|
|---|---|---|---|---|---|---|---|
|||SAE|5120|10|0.458|0.292|0.375|
|||DBM|2560|9|0.463|0.323|0.393|
||Qwen3-4B|MDBM|2560|10|0.404|0.436|0.420|
|||DAS|2048|14|**0.615**|0.346|0.481|
|instance of||MDAS|2048|13|0.524|0.559|0.541|
|||SAE|16384|13|0.472|0.350|0.411|
|||DBM|4096|10|0.441|0.409|0.425|
||Qwen3-8B|MDBM|4096|10|0.418|0.469|0.443|
|||DAS|2048|13|**0.633**|0.425|0.529|
|||MDAS|2048|13|0.536|0.624|0.580|
|||SAE|10240|12|0.567|0.244|0.406|
|||DBM|2560|8|0.553|0.257|0.405|
||Qwen3-4B|MDBM|2560|10|0.531|0.318|0.425|
|||DAS|2048|8|**0.668**|0.182|0.425|
|subclass of||MDAS|2048|8|0.597|0.313|0.455|
|||SAE|16384|12|0.584|0.210|0.397|
|||DBM|4096|8|0.530|0.282|0.406|
||Qwen3-8B|MDBM|4096|10|0.504|0.362|0.433|
|||DAS|2048|13|**0.636**|0.308|0.472|
|||MDAS|2048|13|0.520|0.500|0.510|



Table 11: Highest-Cause single-layer intervention results on the Entity split, selecting the configuration with the highest Cause score for each model, axiom type, and method.


<!-- page 15 -->

<!-- Start of picture text -->
1.0 1.0<br>airport<br>film award currency<br>film<br>0.8 stock exchange 0.8 professional sports league magazine disease<br>literary work sculpture<br>city<br>film award<br>0.6 television series mountain 0.6large language modelpainting tourist attraction lake country universityairport currency<br>academic journal island<br>painting<br>data set<br>research institute<br>0.4 type of musical instrument 0.4<br>protein<br>0.2 0.2<br>0.0 0.0<br>0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0<br>Cause Cause<br>(a) Qwen3-8B base (b) Qwen3-8B source<br>1.0 1.0<br>airport<br>film award national park<br>0.8 currency 0.8<br>country<br>academic conference software<br>science award type of musical instrument magazinemountain data set airport<br>literary work<br>city film award city<br>0.6 library 0.6<br>political partypainting television series magazine painting academic conference country currency<br>mountain<br>album<br>0.4 0.4<br>type of sport type of musical instrument<br>protein<br>0.2 0.2<br>0.0 0.0<br>0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0<br>Cause Cause<br>(c) Qwen3-4B base (d) Qwen3-4B source<br>Iso Iso<br>Iso Iso<br><!-- End of picture text -->

Figure 4: Class-level Cause–Iso scatter plots for the best MDAS instance-of settings. Each row shows base classes on the left and source classes on the right.


<!-- page 16 -->

<!-- Start of picture text -->
1.0 1.0<br>flower<br>0.8 0.8<br>animal organ<br>measuring instrument<br>0.6 astronomical object award tree medical device 0.6 problem insect facility algorithm<br>theory<br>biological process activityinsect industry biological processgeographic location theory creative work<br>chemical process flower<br>0.4 disease algorithmproblem geographic locationtool 0.4 body of watermeasuring instrument tree scientific instrumentindustry fish tool music<br>bird<br>material<br>food<br>0.2 facility 0.2<br>emotion<br>0.0 0.0<br>0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0<br>Cause Cause<br>(a) Qwen3-8B base (b) Qwen3-8B source<br>1.0 1.0<br>0.8 0.8<br>scientific instrument flower<br>tree<br>medical device<br>0.6 award measuring instrument 0.6 tool<br>algorithm food flower activity<br>insect biological processtheory creative workmusic<br>industry<br>biological process<br>0.4 0.4 body of water geographical feature fish<br>material mammal<br>problem tool<br>disease<br>color<br>mammal<br>geographical feature<br>0.2 bird 0.2<br>food<br>0.0 0.0<br>0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0<br>Cause Cause<br>(c) Qwen3-4B base (d) Qwen3-4B source<br>Iso Iso<br>Iso Iso<br><!-- End of picture text -->

Figure 5: Class-level Cause–Iso scatter plots for the best MDAS subclass-of settings. Each row shows base classes on the left and source classes on the right.


<!-- page 17 -->

<!-- Start of picture text -->
1.0 1.0<br>airport<br>film award country city currency<br>software<br>0.8 national park 0.8 sculpture album research institute protein video game<br>science award disease<br>island city currency<br>country airport<br>research institute university<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0<br>Cause Cause<br>(a) instance of, base (b) instance of, source<br>1.0 1.0<br>0.8 flower 0.8<br>measuring instrument animal organ<br>music science medical device insect facility algorithm<br>biological process medical device color<br>0.6 scientific instrument 0.6 organization fish flowermusic<br>theory<br>geographical feature mammal tool<br>science<br>0.4 0.4<br>food<br>0.2 0.2<br>0.0 0.0<br>0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0<br>Cause Cause<br>(c) subclass of, base (d) subclass of, source<br>Iso Iso<br>Iso Iso<br><!-- End of picture text -->

Figure 6: Class-level Cause–Iso scatter plots for the best Qwen3-8B multi-layer MDAS settings. Each row corresponds to one axiom type, with base classes on the left and source classes on the right.


<!-- page 18 -->

<!-- Start of picture text -->
score r=0.779, rank r=0.831 score r=0.813, rank r=0.810<br>1.0 1.0<br>50 political party . oe a 50 e en.”<br>arena<br>eo . %.<br>library e musical group %  e@Ye 0.8 0.8<br>40 , film se 40 J magazine sports award literary work L<br>. “ tourist attraction<br>e mountainvideo game ° lake  &e 0.6 academic journal o°%-« lakeacademic conference 0.6<br>algorithm mountain<br>30 tourist attraction university - ee magazine a animal ° 30 ©. science award {eek library<br>e ° academic conference vy @ algorithm e ey ° album<br>20 °% Je e e stadium 0.4 20 video game eo ev mountain range ° research institute 0.4<br>company programming languagedisease e river ov’<br>arena protein<br>10 o~%?* city e science award o museum e 0.2 10 data set ve musical groupcompany ee chemical element professional sports league 0.2<br>softwarecurrency countryfirst-level administrative divisionnational parkprofessional sports league diseasecurrency AS universitycountry<br>airport<br>airport 0.0 city 0.0<br>10 20 30 40 50 10 20 30 40 50<br>Qwen3-8B rank (1=best) Qwen3-8B rank (1=best)<br>(a) instance of, base (b) instance of, source<br>score r=0.741, rank r=0.752 score r=0.746, rank r=0.671<br>1.0 1.0<br>problem<br>35 35 theory<br>machine<br>color bird 0.8 algorithm 0.8<br>30 30 protein<br>astronomical object<br>sport<br>activity<br>fish<br>25 insect 25 disease<br>0.6 machine 0.6<br>creative work er sport<br>protein facility<br>20 . 20 insect academic discipline tree<br>wa vehicle : } . science<br>algorithm animal organ<br>tool astronomical object a ° measuring instrument :<br>0.4 0.4<br>15 body of water 15 facility organization<br>award . po software . e tool material<br>industry music food<br>10 academic discipline 10 . mammal ve color e<br>medical device software<br>animal organ . organization 0.2 flower fish 0.2<br>emotion industry<br>5 theory 5 emotion<br>measuring instrumenttree . oe creative work ° bird<br>scientific instrument activity<br>flower music<br>0.0 0.0<br>5 10 15 20 25 30 35 5 10 15 20 25 30 35<br>Qwen3-8B rank (1=best) Qwen3-8B rank (1=best)<br>(c) subclass of, base (d) subclass of, source<br>Mean Disentangle Mean Disentangle<br>Qwen3-4B rank (1=best) Qwen3-4B rank (1=best)<br>Mean Disentangle Mean Disentangle<br>Qwen3-4B rank (1=best) Qwen3-4B rank (1=best)<br><!-- End of picture text -->

Figure 7: Cross-model class-rank correlation for task-macro Disentangle scores. Each point denotes one high-level class, with coordinates given by its Qwen3-8B and Qwen3-4B ranks for the same axiom and role. _Score r_ is the Pearson correlation between the two models’ class-level Disentangle scores; _rank r_ is the Pearson correlation between their ranks, equivalently Spearman’s _ρ_ . Color gives the arithmetic mean of the two Disentangle scores. Point area increases with class-level evaluation support, using the larger support count across the two runs.


<!-- page 19 -->

<!-- Start of picture text -->
stock exchange stock exchange<br>large language model programming language<br>tourist attraction arena<br>protein type of sport<br>data set stadium<br>disease national park<br>academic journal island<br>algorithm protein<br>island sculpture<br>type of sport data set<br>programming language musical group<br>first-level administrative division type of chemical entity<br>motorsport racing track type of musical instrument<br>sports organization album<br>museum university<br>painting political party<br>international organization large language model<br>software city<br>sculpture motorsport racing track<br>video game first-level administrative division<br>film award sports award<br>modern language film award<br>−0.3 −0.2 −0.1 0.0 0.1 0.2 0.3 −0.3 −0.2 −0.1 0.0 0.1 0.2 0.3<br>Base-role Disentangle − Source-role Disentangle Base-role Disentangle − Source-role Disentangle<br>(a) Qwen3-8B, instance of (b) Qwen3-4B, instance of<br>algorithm theory<br>measuring instrument scientific instrument<br>facility body of water<br>emotion activity<br>tree bird<br>body of water food<br>geographical feature creative work<br>mammal tree<br>fish music<br>animal organ color<br>medical device mammal<br>theory fish<br>material material<br>food chemical process<br>activity measuring instrument<br>music vehicle<br>disease geographical feature<br>geographic location geographic location<br>creative work flower<br>biological process medical device<br>tool animal organ<br>organization disease<br>−0.3 −0.2 −0.1 0.0 0.1 0.2 0.3 −0.3 −0.2 −0.1 0.0 0.1 0.2 0.3<br>Base-role Disentangle − Source-role Disentangle Base-role Disentangle − Source-role Disentangle<br>(c) Qwen3-8B, subclass of (d) Qwen3-4B, subclass of<br><!-- End of picture text -->

Figure 8: Largest base–source class role gaps for the best MDAS settings. Rows correspond to axiom types and columns to model sizes. The horizontal axis reports base-role Disentangle minus source-role Disentangle. Colors denote stronger base-role performance or stronger source-role performance .


<!-- page 20 -->

<!-- Start of picture text -->
protein medical device<br>national park biological process<br>video game body of water<br>tourist attraction measuring instrument<br>motorsport racing track geographical feature<br>disease algorithm<br>island geographic location<br>sculpture insect<br>international organization tool<br>software facility<br>algorithm fish<br>political party emotion<br>first-level administrative division animal organ<br>type of sport scientific instrument<br>large language model mammal<br>stock exchange music<br>type of chemical entity color<br>science award science<br>painting astronomical object<br>data set food<br>chemical element theory<br>museum award<br>−0.3 −0.2 −0.1 0.0 0.1 0.2 0.3 −0.3 −0.2 −0.1 0.0 0.1 0.2 0.3<br>Base-role Disentangle − Source-role Disentangle Base-role Disentangle − Source-role Disentangle<br>(a) Qwen3-8B, instance of (b) Qwen3-8B, subclass of<br><!-- End of picture text -->

Figure 9: Largest base–source class role gaps for the best Qwen3-8B multi-layer MDAS settings. The horizontal axis reports base-role Disentangle minus source-role Disentangle. Colors denote stronger base-role performance or stronger source-role performance <mark>.</mark> 



<!-- Start of picture text -->
instance of subclass of<br>100%<br>Qwen3-8B ( n  = 121) Qwen3-8B ( n  = 91)<br>Qwen3-4B ( n  = 141) Qwen3-4B ( n  = 52)<br>80%<br>60%<br>40%<br>20%<br>0%<br>0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7<br>Absolute reciprocal-gap threshold  x Absolute reciprocal-gap threshold  x<br>Empirical survival Pr(|Δ| ≥) x<br><!-- End of picture text -->

Figure 10: Empirical survival distributions of absolute reciprocal Disentangle gaps for the best MDAS settings. At horizontal position _x_ , each curve reports the fraction of eligible unordered class pairs satisfying ∆ _A,B ≥ x_ . Curves are pair-macro: each eligible reciprocal pair contributes once, without weighting by its evaluation support.


<!-- page 21 -->

<!-- Start of picture text -->
1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0 5 10 15 20 25 30 35 0 5 10 15 20 25 30 35<br>Layer Layer<br>(a) instance of, Qwen3-4B, 2 d ,  C = 1000 (b) instance of, Qwen3-4B, 4 d ,  C = 1000<br>1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0 5 10 15 20 25 30 35 0 5 10 15 20 25 30 35<br>Layer Layer<br>(c) instance of, Qwen3-8B, 2 d ,  C = 1000 (d) instance of, Qwen3-8B, 4 d ,  C = 1000<br>1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0 5 10 15 20 25 30 35 0 5 10 15 20 25 30 35<br>Layer Layer<br>(e) subclass of, Qwen3-4B, 2 d ,  C = 10 (f) subclass of, Qwen3-4B, 4 d ,  C = 1000<br>1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0 5 10 15 20 25 30 35 0 5 10 15 20 25 30 35<br>Layer Layer<br>(g) subclass of, Qwen3-8B, 2 d ,  C = 10 (h) subclass of, Qwen3-8B, 4 d ,  C = 1000<br>Score Score<br>Score Score<br>Score Score<br>Score Score<br><!-- End of picture text -->

Figure 11: SAE single-layer profiles across model sizes, axiom types, and latent widths.


<!-- page 22 -->

<!-- Start of picture text -->
1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0 5 10 15 20 25 30 35 0 5 10 15 20 25 30 35<br>Layer Layer<br>(a) instance of, Qwen3-4B, DBM (b) instance of, Qwen3-4B, MDBM<br>1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0 5 10 15 20 25 30 35 0 5 10 15 20 25 30 35<br>Layer Layer<br>(c) instance of, Qwen3-8B, DBM (d) instance of, Qwen3-8B, MDBM<br>1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0 5 10 15 20 25 30 35 0 5 10 15 20 25 30 35<br>Layer Layer<br>(e) subclass of, Qwen3-4B, DBM (f) subclass of, Qwen3-4B, MDBM<br>1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0 5 10 15 20 25 30 35 0 5 10 15 20 25 30 35<br>Layer Layer<br>(g) subclass of, Qwen3-8B, DBM (h) subclass of, Qwen3-8B, MDBM<br>Score Score<br>Score Score<br>Score Score<br>Score Score<br><!-- End of picture text -->

Figure 12: Fixed-layer DBM/MDBM intervention profiles across model sizes and axiom types.


<!-- page 23 -->

<!-- Start of picture text -->
1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0 5 10 15 20 25 30 35 0 5 10 15 20 25 30 35<br>Layer Layer<br>(a) instance of, Qwen3-4B, DAS (b) instance of, Qwen3-4B, MDAS<br>1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0 5 10 15 20 25 30 35 0 5 10 15 20 25 30 35<br>Layer Layer<br>(c) instance of, Qwen3-8B, DAS (d) instance of, Qwen3-8B, MDAS<br>1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0 5 10 15 20 25 30 35 0 5 10 15 20 25 30 35<br>Layer Layer<br>(e) subclass of, Qwen3-4B, DAS (f) subclass of, Qwen3-4B, MDAS<br>1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0 5 10 15 20 25 30 35 0 5 10 15 20 25 30 35<br>Layer Layer<br>(g) subclass of, Qwen3-8B, DAS (h) subclass of, Qwen3-8B, MDAS<br>Score Score<br>Score Score<br>Score Score<br>Score Score<br><!-- End of picture text -->

Figure 13: Fixed-layer DAS/MDAS intervention profiles across model sizes and axiom types with 1024-dimensional subspaces.


<!-- page 24 -->

<!-- Start of picture text -->
1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0 5 10 15 20 25 30 35 0 5 10 15 20 25 30 35<br>Layer Layer<br>(a) instance of, Qwen3-4B, DAS (b) instance of, Qwen3-4B, MDAS<br>1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0 5 10 15 20 25 30 35 0 5 10 15 20 25 30 35<br>Layer Layer<br>(c) instance of, Qwen3-8B, DAS (d) instance of, Qwen3-8B, MDAS<br>1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0 5 10 15 20 25 30 35 0 5 10 15 20 25 30 35<br>Layer Layer<br>(e) subclass of, Qwen3-4B, DAS (f) subclass of, Qwen3-4B, MDAS<br>1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0 5 10 15 20 25 30 35 0 5 10 15 20 25 30 35<br>Layer Layer<br>(g) subclass of, Qwen3-8B, DAS (h) subclass of, Qwen3-8B, MDAS<br>Score Score<br>Score Score<br>Score Score<br>Score Score<br><!-- End of picture text -->

Figure 14: Fixed-layer DAS/MDAS intervention profiles across model sizes and axiom types with 2048-dimensional subspaces.


<!-- page 25 -->

<!-- Start of picture text -->
1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0-3 6-9 12-15 18-21 24-27 30-33 0-3 6-9 12-15 18-21 24-27 30-33<br>Layer Window Layer Window<br>(a) DAS, 256  ×  4 (b) MDAS, 256  ×  4<br>1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0-1 6-7 12-13 18-19 24-25 30-31 0-1 6-7 12-13 18-19 24-25 30-31<br>Layer Window Layer Window<br>(c) DAS, 512  ×  2 (d) MDAS, 512  ×  2<br>1.0 1.0<br>Iso<br>Disentangle<br>0.8 0.8<br>Cause<br>0.6 0.6<br>0.4 0.4<br>Iso<br>0.2 0.2<br>Disentangle<br>Cause<br>0.0 0.0<br>0-3 6-9 12-15 18-21 24-27 30-33 0-3 6-9 12-15 18-21 24-27 30-33<br>Layer Window Layer Window<br>(e) DAS, 512  ×  4 (f) MDAS, 512  ×  4<br>Score Score<br>Score Score<br>Score Score<br><!-- End of picture text -->

Figure 15: Fixed-window multi-layer intervention profiles for Qwen3-8B on instance of. Each panel reports Cause, Iso, and Disentangle on 12 contiguous windows. The _a × b_ notation denotes _a_ intervened dimensions per layer over a _b_ -layer window.


<!-- page 26 -->

<!-- Start of picture text -->
1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0-3 6-9 12-15 18-21 24-27 30-33 0-3 6-9 12-15 18-21 24-27 30-33<br>Layer Window Layer Window<br>(a) DAS, 256  ×  4 (b) MDAS, 256  ×  4<br>1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0-1 6-7 12-13 18-19 24-25 30-31 0-1 6-7 12-13 18-19 24-25 30-31<br>Layer Window Layer Window<br>(c) DAS, 512  ×  2 (d) MDAS, 512  ×  2<br>1.0 1.0<br>Iso Iso<br>Disentangle Disentangle<br>0.8 0.8<br>Cause Cause<br>0.6 0.6<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>0-3 6-9 12-15 18-21 24-27 30-33 0-3 6-9 12-15 18-21 24-27 30-33<br>Layer Window Layer Window<br>(e) DAS, 512  ×  4 (f) MDAS, 512  ×  4<br>Score Score<br>Score Score<br>Score Score<br><!-- End of picture text -->

Figure 16: Fixed-window multi-layer intervention profiles for Qwen3-8B on subclass of. Each panel reports Cause, Iso, and Disentangle on 12 contiguous windows. The _a × b_ notation denotes _a_ intervened dimensions per layer over a _b_ -layer window.


<!-- page 27 -->

|**Class**|**# Entity**|**Attributes**|
|---|---|---|
|academic conference|30|inception, main subject, event interval, organizer|
|academic journal|27|main subject, country of origin, publisher, ISSN, indexed in bibliographic review,<br>inception, editor|
|airport|15|country, located in the administrative territorial entity, date of official opening,<br>elevation above sea level, IATA airport code, ICAO airport code, airline hub|
|album|15|form of creative work, genre, performer, publication date, record label, producer,<br>number of parts of this work, tracklist|
|algorithm|20|<br>inception, named after, discoverer or inventor, computes solution to, best-case time<br>complexity, average time complexity, best-case space complexity, worst-case time<br>complexity, worst-case space complexity, average space complexity|
|animal|20|<br>parent taxon, taxon rank, color, endemic to, main food source, gestation period,<br>diel cycle|
|arena|20|sport, country, located in the administrative territorial entity, date of official<br>opening, occupant, maximum capacity|
|chemical element|30|<br>atomic number, time of discovery or invention, discoverer or inventor, element<br>symbol, phase of matter|
|city|59|country, located in or next to body of water, population, official language, head of<br>government, continent|
|company|30|<br>country, headquarters location, inception, industry, chief executive officer, stock<br>exchange|
|country|30|capital, currency, continent, shares border with, anthem, official language|
|currency|14|country, central bank/issuer, start time, unit symbol, applies to jurisdiction, ISO<br>4217 code|
|data set<br>disease|10<br>20|inception, creator, copyright license, main subject, has use<br>symptoms and signs, drug or therapy used for treatment, has cause, medical<br>examination, disease transmission process, possible treatment|
|film|25|<br>director, genre, country of origin, narrative location, production company, publica-<br>tion date|
|film award|10|inception, country, start time, conferred by, location|
|first-level<br>administrative<br>division|20|country, official language, population, shares border with, located in or next to<br>body of water, capital|
|international organization|20|<br>inception, chairperson, official language, headquarters location, operating area,<br>position held by head of the organization, field of work|
|island|15|continent, country, located in the administrative territorial entity, located in or next<br>to body of water, highest point|
|lake|13|<br>inflows, outflows, drainage basin, basin country, country, located in the administra-<br>tive territorial entity|
|large language model|20|<br>inception, publication date, operator, developer, copyright license, context window|
|library|15|country, location, located in the administrative territorial entity, inception, director<br>/ manager|
|literary work|23|<br>genre, language of work or name, author, publication date, publisher, country of<br>origin|
|magazine|20|country of origin, inception, language of work or name, publisher, main subject,<br>editor, publication interval|
|modern language|20|<br>country, indigenous to, writing system, has grammatical case, ISO 639-1 code|
|<br>motorsport racing track|20|<br>sport, country, located in the administrative territorial entity, significant event,<br>length, inception|
|mountain|10|<br>continent, country, elevation above sea level, mountain range, topographic promi-<br>nence, significant event|
|mountain range|10|i<br>continent, country, highest point, elevation above sea level, time period|
|<br>museum|20|<br>inception, director / manager, located in the administrative territorial entity, country,<br>named after|
|musical group|20|genre, location of formation, country of origin, notable work, start of work period,<br>has part(s)|
|musical work|20|<br>genre, performer, lyricist, language of work or name, publication date, composer|



Continued on next page


<!-- page 28 -->

|**Class**|**# Entity**|**Attributes**|
|---|---|---|
|national park|14|country, inception, located in the administrative territorial entity, highest point,<br>elevation above sea level, heritage designation|
|painting|20|creator, inception, collection, genre, depicts|
|political party|10|chairperson, country, inception, political ideology, political alignment, founded by|
|professional sports league|10|sport, country, inception, number of participants, event interval|
|programming language|20|inception, designed by, developer, programming paradigm|
|protein|20|physically interacts with, active ingredient in, molecular function|
|recurring sporting event|25|event interval, inception, sport, organizer, number of participants, trophy awarded|
|research institute|10|located in the administrative territorial entity, country, inception, member of, field<br>of work, named after, chairperson|
|river|12|origin of the watercourse, mouth of the watercourse, tributary, drainage basin,<br>continent, country of origin|
|science award|15|country, conferred by, inception, named after, event interval, field of work|
|sculpture|10|inception, country, creator, made from material, location, depicts, time period,<br>owned by|
|software|27|inception, developer, operating system, publication date, copyright license, plat-<br>form, programmed in|
|sports award|20|conferred by, event interval, inception, sport|
|sports organization|50|country, inception, sport, head coach, home venue, league or competition|
|<br>stadium|20|<br>country, located in the administrative territorial entity, date of official opening,<br>maximum capacity, occupant, sport, surface played on|
|stock exchange|10|country, headquarters location, stock market index, inception, chief executive<br>officer|
|television series|20|fi<br>genre, creator, original broadcaster, country of origin, original language of film<br>or TV show, production company, distributed by, number of episodes, number of<br>seasons|
|tourist attraction|20|inception, country, located in the administrative territorial entity, made from<br>material, architectural style|
|type of chemical entity|30|<br>chemical formula, has use, melting point, boiling point, has part(s)|
|<br>type of musical instrument|20|<br>made from material, has part(s), used by, discoverer or inventor, time of discovery<br>or invention|
|type of sport|20|inception, authority, regulated by, country of origin, maximum number of players,<br>minimum number of players|
|university|30|country, inception, located in the administrative territorial entity, chairperson,<br>motto text, member of, founded by|
|video game|25|<br>genre, platform, developer, publisher, publication date, game mode, distributed by|



Table 12: Classes in the instance of dataset, their number of entities, and associated attributes.


<!-- page 29 -->

|**Class**|**# Concept**|**Attributes**|
|---|---|---|
|academic discipline|17|field of work, has subclasses, is the study of, part of|
|activity|65|has subclasses, location, participant|
|algorithm|34|has subclasses, has use|
|animal organ|17|body system, function, has part(s)|
|astronomical object|26|has part(s), has subclasses, parent astronomical body|
|award|17|conferred by, field of work, has subclasses|
|biological process|20|has effect, has part(s), has subclasses|
|bird|17|main food source, habitat, has subclasses, parent taxon|
|body of water|15|has part(s), has subclasses, largest example|
|chemical process|20|has part(s), has subclasses, product or material produced|
|color|21|has part(s), has subclasses, sRGB color hex triplet|
|creative work|80|creator role, form of creative work, has subclasses|
|disease|29|anatomical location, has subclasses, symptoms and signs|
|emotion|36|has subclasses, opposite of, positive valence|
|facility|77|has part(s), has subclasses, has use|
|fish|18|main food source, habitat, has subclasses, parent taxon|
|flower|14|blooming season, flower color, is pollinated by|
|food|79|has subclasses, physical state, vegetable or not|
|geographic location|23|has part(s), has subclasses|
|geographical feature|24|has part(s), has subclasses, largest example|
|industry|13|has subclasses, main offerings, occupation|
|insect|14|main food source, habitat, has subclasses, parent taxon|
|machine|17|has part(s), has subclasses, has use|
|mammal|20|main food source, habitat, has subclasses, parent taxon|
|material|41|has part(s), has subclasses, has use|
|measuring instrument|13|has use, measurement unit, measures|
|medical device|14|anatomical location, has part(s), has use|
|music|19|has subclasses, instrumentation|
|organization|84|field of work, has subclasses, occupation|
|problem|11|field of study, has cause, has effect, has subclasses|
|protein|29|has part(s), has subclasses, molecular function|
|science|27|has part(s), has subclasses, is the study of|
|scientific instrument|11|field of usage, has part(s), has use, observed object|
|i<br>software|41|i<br>has subclasses, has use, notable instance|
|sport|35|equipment, has subclasses, regulated by|
|theory|10|field of work, has subclasses, main subject|
|tool|26|i<br>has part(s), has use, made from material|
|tree|14|habitat, life expectancy, parent taxon|
|vehicle|25|has subclasses, operating medium, powered by|



Table 13: Classes in the subclass of dataset, their number of subclasses, and associated attributes.
