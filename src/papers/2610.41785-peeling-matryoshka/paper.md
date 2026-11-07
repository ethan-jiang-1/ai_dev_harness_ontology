---
source: 2610.41785-peeling-matryoshka.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# Peeling the Matryoshka: Extracting Ontological Structure from Retrieval Embeddings · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

# **Peeling the Matryoshka: Extracting Ontological Structure from Retrieval Embeddings** 

**Eunchan Kim** 

Hanyang University 

eunchan@hanyang.ac.kr 

**Inwhee Joe** 

Hanyang University 

iwjoe@hanyang.ac.kr 

## **Abstract** 

Taxonomy construction is essential for knowledge-intensive NLP yet remains costly: clustering-based methods (i) need careful per-corpus tuning and yield unstable hierarchies, while LLM-based pipelines (ii) depend on expensive task-specific training that does not transfer across domains. We report an empirical finding that bears on both: in Matryoshka Representation Learning (MRL) embeddings, where each leading prefix is itself a usable, coarser vector, prefix length aligns with the coarse-to-fine granularity of gold taxonomies; shuffled- and reversedimension controls isolate the alignment to the learned early prefix dimensions. The pattern holds across three architecturally distinct MRL models (full statistics in §3). To test whether this regularity is usable, we introduce PEEL ( **P** eeling **E** mbeddings to **E** xtract **L** atent ontologies): a minimal probe over these frozen embeddings, trained once with an order-embedding objective that represents hierarchy as vector containment; a minimum spanning arborescence then decodes taxonomic DAGs. Using only a concept vocabulary (no documents), PEEL recovers taxonomic DAGs with high structural fidelity on two OLLM benchmarks, transferring to a new domain with no target-edge supervision. The end-to-end OLLM pipeline—which jointly discovers concepts and induces structure from document corpora—is reported as a cross-task reference (§5.3). Pre-trained retrieval embeddings encode a decodable granularity gradient; a minimal probe renders it as explicit parent–child (is-a) structure. 

## **1 Introduction** 

Domain taxonomies, hierarchical structures of concepts linked by taxonomic ( _is-a_ ) relations, are a fundamental form of ontological structure and the backbone of structured knowledge systems, from biomedical terminologies such as MeSH (Lipscomb, 2000) to web-scale category hierarchies 

like Wikipedia (Ponzetto and Strube, 2007) and academic classification schemes. Throughout, _ontological structure_ refers to this taxonomic ( _is-a_ ) backbone, following OLLM’s usage (Lo et al., 2024). Yet constructing them remains one of NLP’s most labor-intensive tasks. 

Automated taxonomy construction has been approached from two directions. Embedding-based methods range from flat clustering of term vectors to recursive or geometry-based schemes (e.g., hyperbolic and box embeddings); the former lose hierarchy, the latter require dedicated, hierarchysupervised embedding spaces. LLM-based methods instead generate hierarchy explicitly, yet demand extensive fine-tuning or prompt engineering per domain. Meanwhile, structural probing has shown that pre-trained representations encode rich linguistic structure recoverable via simple learned projections (Hewitt and Manning, 2019), but has focused on syntax, not taxonomic hierarchy. An alternative remains unexplored: do embeddings trained purely for retrieval already encode hierarchical signal exploitable for taxonomy construction? 

We find that they do: specifically, embeddings trained with Matryoshka Representation Learning (MRL; Kusupati et al., 2022), whose nested prefix structure makes truncation a principled resolution control. Every prefix of the full vector is itself a useful representation, concentrating coarse semantic information in early dimensions. We observe that this coarse-to-fine organization aligns with gold taxonomic structure: across three opensource MRL models spanning distinct encoder families and scales (nomic, 137 M, BERT; jina-v3, 572 M, XLM-R; Qwen3-Embedding, 600 M, decoder), MRL prefix truncation consistently outperforms both a shuffled-dimension control (ordering destroyed, content preserved) and a last- _k_ reverse control (tail dimensions), the advantage concentrated in the learned early prefix dimensions. A supporting ANOVA finds the label separation ef-


<!-- page 2 -->

fect large at the deepest taxonomic level, consistent across all model-by-dataset sequences (Table 1; full statistics in §3), indicating the structure is not specific to a single encoder family. 

We present PEEL ( **P** eeling **E** mbeddings to **E** xtract **L** atent ontologies), a lightweight pipeline that exploits this signal. Pre-trained embeddings mix taxonomic structure with retrieval-specific features; PEEL trains a 98K-parameter probe with an order-embedding loss (Vendrov et al., 2016) to project frozen retrieval embeddings into a space where coordinate-wise dominance reflects parent– child relations. A Chu-Liu/Edmonds minimum spanning arborescence (Chu and Liu, 1965; Edmonds, 1967) then extracts a threshold-free taxonomy tree, expanded into a DAG by greedily adding lowest-violation edges up to a budget. 

On the OLLM benchmarks (Lo et al., 2024), PEEL—using only the concept vocabulary, no documents—performs taxonomy structure induction over a given concept set, recovering taxonomic DAGs with high structural fidelity (Graph F1 _._ 885 _/._ 931 on Wikipedia and arXiv; cross-task comparison with the document-fed OLLM pipeline in §5.3). 

Our contributions are: 

1. **Discovery.** An empirical finding that pre-trained MRL embeddings encode taxonomic structure in their learned early prefix dimensions, isolated by shuffled- and reverse-dimension controls and replicated across three architecturally distinct open-source MRL models (§3). 

2. **Demonstration.** PEEL, a minimal probe decoding taxonomy DAGs via minimum spanning arborescence without task-specific embedding training (§4). 

3. **Evaluation.** On two OLLM benchmarks, PEEL recovers taxonomic DAGs from a concept vocabulary alone with high structural fidelity on the primary structure-sensitive metrics (Graph F1 and Cont. F1); we report the document-fed OLLM pipeline—which jointly discovers concepts _and_ induces structure from documents—as a cross-task reference (§5). 

# **2 Related Work** 

## **2.1 Taxonomy Construction** 

Automated taxonomy construction has evolved through several paradigms. _Pattern-based_ methods, originating with Hearst patterns (Hearst, 1992) and revisited at scale by Roller et al. (2018), extract hy- 

pernymy from lexico-syntactic cues but suffer from low recall. _Statistical_ approaches integrate heterogeneous evidence to induce taxonomies with supervised classifiers (Snow et al., 2006) or structured prediction (Bansal et al., 2014). Embedding-based methods such as TaxoGen (Zhang et al., 2018) cluster term embeddings recursively. 

More recently, large language models have been applied directly. OLLM (Lo et al., 2024) fine-tunes an LLM to generate ontology subgraphs end-toend; Chain-of-Layer (Zeng et al., 2024) decomposes taxonomy induction into a layer-by-layer prompting procedure; TaxoLLaMA (Moskvoretskii et al., 2024) unifies taxonomy tasks via instruction tuning; and TaxoAdapt (Kargupta et al., 2025) adapts LLM-generated taxonomies to evolving corpora. 

These methods share a common pattern: they either _learn_ taxonomy structure through taskspecific training or _generate_ it via prompted LLMs. LLMs4OL (Babaei Giglou et al., 2024) organises ontology learning into three tasks—term typing, taxonomy discovery, and non-taxonomic relation extraction—and PEEL targets taxonomy discovery: recovering _is-a_ pairs over a given set of types. Whether pre-trained embeddings—trained solely for retrieval—already encode exploitable taxonomic structure has remained unexplored. 

## **2.2 Hierarchical Representation Learning** 

Order Embeddings (Vendrov et al., 2016) encode hierarchy directly in embedding geometry, modelling asymmetric _is-a_ relations via coordinatewise inequalities: a parent’s coordinates are no larger than its child’s in every dimension. Later work extends this ordering to density-based formulations (Athiwaratkun and Wilson, 2018). Poincaré Embeddings (Nickel and Kiela, 2017) use hyperbolic space to capture tree-like hierarchies. 

Most closely related to our approach, HiTs (He et al., 2024) retrains pre-trained sentence transformers in Poincaré space with a centripetal loss to produce a hierarchy encoder. While both HiTs and PEEL map pre-trained language models to hierarchical structure, they differ fundamentally: HiTs _injects_ hierarchy by retraining the entire encoder (22M–109M parameters) with a hierarchyaware objective, whereas PEEL _discovers_ hierarchy latent in frozen retrieval embeddings via a 98Kparameter probe.


<!-- page 3 -->

## **2.3 Structural Probing of Pre-trained Representations** 

What linguistic structure pre-trained representations encode has been studied extensively through probing classifiers (Belinkov and Glass, 2019; Conneau et al., 2018; Tenney et al., 2019). Most directly relevant, Hewitt and Manning (2019) demonstrate that a linear transformation of BERT representations recovers parse tree distances, establishing the _structural probe_ paradigm: a simple learned projection can extract complex structure from frozen representations. Subsequent work has examined what probing accuracy actually reveals: Hewitt and Liang (2019) propose control tasks to measure probe selectivity, and Voita and Titov (2020) frame probing as compression, arguing that a probe’s minimum description length—not just accuracy— determines whether structure is genuinely encoded. 

Crucially, existing structural probes target _syntactic_ structure (dependency and constituency trees). PEEL extends this paradigm to _taxonomic_ structure: we show that a learned projection of retrieval embeddings, trained with an order embedding loss, recovers parent–child relations in concept hierarchies—a qualitatively different structural signal from syntax. 

## **2.4 Matryoshka Representation Learning** 

Matryoshka Representation Learning (MRL; Kusupati et al., 2022) trains embeddings so that every prefix of the full vector is itself a valid representation, producing a nested family of _O_ (log _d_ ) representations from a single forward pass. Originally designed for efficient retrieval at variable compute budgets, MRL models are now widely deployed in production systems. Its authors already noted that this nesting “naturally captures the underlying hierarchy of the class labels” in a two-level ImageNet superclass setting (their §5). 

Hanley and Durumeric (2025) instead engineer it: they train custom Matryoshka embeddings with a modified contrastive loss that explicitly encodes news similarity hierarchies into different dimension ranges, an approach we term _hierarchy injection_ . We establish the complementary result: standard MRL models—trained only for retrieval, with no hierarchical supervision—already exhibit prefix structure that tracks depth in a multi-level gold concept taxonomy, an alignment that §3 isolates with shuffled- and reverse-dimension controls and replicates across three architecturally distinct encoders. 

This _hierarchy discovery_ requires no custom training and applies to any MRL-capable encoder. 

**Summary.** PEEL sits at the intersection of four threads: it applies the structural probe paradigm (§2.3) with order embedding geometry (§2.2) to frozen MRL representations (§2.4) for taxonomy construction (§2.1), requiring neither task-specific embedding training nor LLM generation. 

# **3 MRL Prefixes Encode Taxonomic Structure** 

As noted in §1, MRL embeddings concentrate coarse semantic information in early dimensions by design (Kusupati et al., 2022). We hypothesize that this coarseness aligns with _taxonomic structure_ : shorter prefixes capture broad category distinctions while longer prefixes preserve finer-grained structure. 

**Experimental design.** We evaluate kNN label purity ( _k_ =10) across three MRL models spanning distinct encoder families and scales: Nomic-embedtext-v1.5 (Nussbaum et al., 2025) (137 M, BERT), jina-embeddings-v3 (Sturua et al., 2024) (572 M, XLM-R), and Qwen3-Embedding (Zhang et al., 2025) (600 M, decoder), on two taxonomic benchmarks. We compare MRL prefix truncation against two controls: (i) a _shuffled_ control that randomly permutes all dimensions before truncation, preserving total information content while destroying the learned dimension ordering (cf. control tasks; Hewitt and Liang, 2019), and (ii) a _reverse_ control that truncates the last _k_ dimensions, excluding the front-loaded learned structure. 

**Results.** MRL prefix truncation outperforms _both_ controls (the order-destroying shuffled control and the last- _k_ tail-dimension reverse control) across all three architecturally distinct encoder families, with the advantage concentrated in the early, truncated prefix dimensions (Figure 1). At full dimensionality the prefix coincides with the complete embedding, so all three coincide by construction; the separation therefore reflects the _learned earlyprefix ordering_ . That the advantage holds for every model against _both_ a randomly permuted and a tailtruncated control isolates the signal to this learned ordering. This directional consistency holds for every model (one-sided sign test; Appendix D). As supporting triangulation, we quantify how strongly taxonomic labels separate at each depth via oneway ANOVA over every embedding dimension,


<!-- page 4 -->

|**Model**|**Data**|**Depth 1 **|**Depth 2 **|**Depth 3**|
|---|---|---|---|---|
|Nomic (137M)|wiki|.058|.159|.364|
|jina-v3 (572M)|wiki|.067|.181|.400|
|Qwen3 (600M)|wiki|.043|.131|.337|
|Nomic (137M)|arXiv|.039|.122|—|
|jina-v3 (572M) <br>|arXiv<br>|.078|.205|—|
|Qwen3 (600M)|arXiv|.039|.131|—|



Table 1: ANOVA effect sizes ( _η_<sup>2</sup> ) for kNN label purity by taxonomy depth, reported as a supporting crossmodel consistency check. arXiv has max depth 2. The depth ordering holds in every row. Because gold class counts differ sharply across depths (Wikipedia: 33/875/7124 at Depth 1/2/3), these values index consistency, _not_ an absolute cross-depth magnitude. Cohen’s benchmarks: _._ 01 small, _._ 06 medium, _._ 14 large (Cohen, 1988). 

reporting the mean _η_<sup>2</sup> (Table 1): on Wikipedia, effects are small-to-medium at Depth 1 (.04–.07), medium at Depth 2 (.13–.18), and Cohen’s-large at Depth 3 (.34–.40); the shallower arXiv taxonomy (two gold levels) shows the same direction (Depth 1 .04–.08, Depth 2 .12–.20). The depth ordering of effect sizes holds without exception across all six model _×_ dataset sequences. This _η_<sup>2</sup> comparison serves only as a supporting cross-model consistency check. 

The signal’s concentration in early dimensions, with higher dimensions adding little over the controls, suggests that full embeddings mix taxonomic structure with retrieval-specific features that dilute hierarchy. A learned projection trained to preserve parent–child ordering should therefore separate these components. A training-free pre-probe check is reported in Appendix E. §4 operationalizes this insight. 

# **4 Method** 

PEEL operationalizes the observation from §3— that MRL prefixes encode taxonomic structure— through three stages (Figure 2): (1) projecting frozen embeddings into an order-embedding space (Vendrov et al., 2016) via a probe trained once on source-domain gold edges, (2) extracting a threshold-free taxonomic tree via ChuLiu/Edmonds minimum spanning arborescence (Chu and Liu, 1965; Edmonds, 1967), and (3) expanding the tree into a DAG by adding lowviolation edges. Each component is deliberately simple: §3 establishes that the hierarchical signal is already present in pre-trained embeddings; PEEL demonstrates that it is operationally exploitable with simple machinery. 

## **4.1 Order-Embedding Probe** 

Pre-trained MRL embeddings mix taxonomic signal with retrieval-specific features in overlapping dimensions (§3). Following the structural probing paradigm (Hewitt and Manning, 2019), we train a learned projection to separate these components: 



<!-- Start of picture text -->
f = ReLU( W e  +  b ) , W ∈ R d out ×D (1)<br><!-- End of picture text -->

We take this paradigm as conceptual inspiration—a minimal probe can surface latent structure—and PEEL serves as a demonstration that the structure §3 establishes is operationally exploitable, not as a diagnostic claim about the embeddings. ReLU projects outputs into the non-negative orthant R<sup>_d_</sup> +<sup>out</sup> required by the order-embedding framework (Vendrov et al., 2016). We set _d_ out=128 based on ablation (Table 4). 

We train the projection using order-embedding loss (Vendrov et al., 2016): 



<!-- Start of picture text -->
L  =  L + +  L− (2)<br>L + = |P| 1 �( p,c ) ∈P ��max( 0 , f p− f c )��2 (3)<br><!-- End of picture text -->



<!-- Start of picture text -->
L− = |N| 1 �( p,n ) ∈N max �0 , m<br>−<br>��max( 0 , f p− f n )��2� (4)<br><!-- End of picture text -->

where _L_ + encourages **f** _p ≤_ **f** _c_ for positive parent– child pairs _P_ , and _L−_ pushes negatives apart by margin _m_ ( _N_ = negative pairs). Because §3 isolates this signal using controls that involve no probe training, the learned projection recovers a granularity ordering the embeddings already encode rather than imposing it through supervision. 

We choose order embeddings for two reasons: (1) they directly encode the asymmetric is-a relation, unlike symmetric contrastive losses; and (2) the coordinate-wise ordering constraint yields the violation score used for tree extraction (§4.3). 

## **4.2 Random Truncation Training** 

Datasets differ in domain and structural profile, so no single truncation captures the full taxonomic structure. We exploit MRL’s prefix-truncation property: at each training step, we randomly sample _d ∈{_ 64 _,_ 128 _,_ 256 _,_ 384 _,_ 512 _,_ 768 _}_ , truncate all embeddings to _d_ dimensions, and zero-pad back to _D_ =768 before projection. This produces a single model that handles all resolutions; at inference, we select the best dimensionality per dataset. Training at a single truncation length would tie the probe to


<!-- page 5 -->

<!-- Start of picture text -->
Wikipedia (Depth 3) arXiv (Depth 2)<br>1.4 Model Comparison<br>Nomic vs Shuffled<br>jina-v3 0.5 vs Reverse<br>1.2 Qwen3<br>1.0 0.4<br>0.8<br>0.3<br>0.6<br>0.2<br>0.4<br>0.1<br>0.2<br>0.0 0.0<br>2 8 32 128 512 2 8 32 128 512<br>Embedding dimension Embedding dimension<br>log (MRL / control purity)2 log (MRL / control purity)2<br><!-- End of picture text -->

Figure 1: Relative advantage of MRL prefix truncation over two controls, by embedding dimension, on Wikipedia and arXiv at the deepest gold taxonomic level. _y_ = log2(MRL _÷_ control kNN purity); _y_ =0 is parity with the control. Solid = vs. shuffled control (dimension ordering destroyed); dotted = vs. reverse control (last- _k_ tail dimensions). Colors denote three architecturally distinct MRL models (Nomic, jina-v3, Qwen3). All curves rise above parity and peak within the early dimensions; at full dimensionality the prefix equals the complete embedding, so the controls coincide by construction. 

that resolution’s feature distribution; random truncation instead forces it to learn order-embedding relationships that hold across all resolutions simultaneously (Table 3). 

## **4.3 Tree Extraction via Chu-Liu/Edmonds** 

Given projected embeddings **f** , we define the violation score between nodes _i_ and _j_ as: 



<!-- Start of picture text -->
d out<br>v ( i, j ) = ��max(0 , fk ( i )  − fk ( j ))�2 (5)<br>k =1<br><!-- End of picture text -->

A low _v_ ( _i, j_ ) indicates that **f** _i ≤_ **f** _j_ coordinate-wise, suggesting _i_ is a parent of _j_ . 

We construct a directed graph weighted by violation scores and extract the minimum spanning arborescence (MSA) via the Chu-Liu/Edmonds algorithm (Chu and Liu, 1965; Edmonds, 1967), producing an optimal rooted tree with exactly _N −_ 1 edges. CLE requires no threshold, unlike containment-ratio or edge-weight thresholding approaches. 

## **4.4 DAG Expansion** 

A tree contains exactly _N −_ 1 edges, which may undercount the true is-a relations in a polyhierarchical ontology. To recover additional edges, we rank all non-tree node pairs by violation score and greedily add the lowest-violation pairs while maintaining acyclicity, up to an edge budget _n_ expand (§5.1). 

# **5 Experiments** 

## **5.1 Setup** 

**Datasets.** We evaluate on two datasets from the OLLM benchmarks (Lo et al., 2024), which pair document corpora with gold taxonomies. The two datasets span distinct domains and structural profiles. Wiki-ol provides 8,033 concept terms with a gold taxonomy of 14,673 edges at depth 3. ArXivol contains 61 categories in a shallow hierarchy of depth 2. 

**Evaluation Metrics.** We report five metrics from the OLLM evaluation suite (Lo et al., 2024): Lit. F1 (literal edge overlap, OLLM’s sanity-check reference), Fuzzy F1 (thresholded edge matching; allMiniLM-L6-v2, _τ_ =0 _._ 436), Cont. F1 (thresholdfree Hungarian edge matching, scored by the weaker of the two endpoint similarities), Graph F1 (Hungarian node matching over SGConv neighbourhood embeddings), and Motif Dist. (triadiccensus total-variation divergence). We designate Graph F1 and Cont. F1 as the primary structuresensitive metrics: they capture global structural similarity and edge-endpoint correspondence, and are robust to surface-level label variation. 

**Baselines.** All baselines are from Lo et al. (2024) with reported numbers: Memorisation (training edges verbatim), Hearst Patterns, Zero-shot and Finetune (Mistral-7B), and the full OLLM pipeline. PEEL receives only the gold concept vocabu-


<!-- page 6 -->

<!-- Start of picture text -->
Training<br>(B, 768) (B, 128)<br>Gold edges MRL encoder e ∈ ℝ⁷⁶⁸ PEEL probe f ∈ ℝ¹²⁸ Order emb. loss<br>768 → 128, ReLU<br>(parent, child) Pre-trained MRL (frozen) L_pos + L_neg<br>98K params<br>random dim ∈ {64, 128, …, 768}<br>Inference<br>N concepts (N, 768) Trained probe (N, 128) Violation matrix<br>MRL emb. (N, 768) N × N pairwise<br>CLE (MSA) tree DAG expansion<br>Ontology DAG<br>N−1 edges add near-miss edges<br><!-- End of picture text -->

Figure 2: The PEEL pipeline. **Training** (top): frozen MRL embeddings are projected through a probe (98K parameters) trained with order embedding loss under random dimensional truncation. **Inference** (bottom): the trained probe maps _N_ concept embeddings to a 128-d order-embedding space; a pairwise violation matrix is constructed and resolved by Chu-Liu/Edmonds’ algorithm into a threshold-free tree, then expanded into a directed acyclic graph via near-miss edges. 

lary; all LLM-based baselines (Zero-shot, Finetune, OLLM) additionally consume each article’s title and abstract per the OLLM protocol (Lo et al., 2024, Figs. 5–6), and Hearst extracts from the source corpus. For arXiv-ol, OLLM (transfer) finetunes on 2,048 additional arXiv samples; PEEL uses no arXiv training data (zero-shot). 

**Implementation.** PEEL uses Nomic-embedtext-v1.5 (Nussbaum et al., 2025) as the frozen encoder (768-dimensional). The probe is a single linear layer (768 _→_ 128) followed by ReLU, totaling 98K trainable parameters. We train with Order Embedding loss (margin _m_ =4 _._ 0) using Adam (learning rate 5 _×_ 10<sup>_−_4</sup> , batch size 512) on wiki-ol gold parent–child edges for 10 epochs on a single GPU ( _∼_ 4 seconds).<sup>1</sup> 

**Training and inference protocol.** The probe is trained on wiki-ol gold parent–child edges, with the training graph split 80%/10%/10% into train/validation/holdout (edge-level split); each epoch we track validation loss and edge-ranking AUROC, retaining the lowest-loss checkpoint over the 10-epoch schedule. Negative pairs use a 10:1 negative-to-positive ratio, mixing 50% random nodes, 30% sibling distractors (other children of the same parent), and 20% reversed pairs. For tree extraction, the virtual root connects to every node at edge weight equal to the 95th percentile of positive violation scores. Wiki-ol inference hyperparameters (prefix truncation _d_ =512, DAG expansion budget _n_ expand=15 _,_ 000, CLE candidate count _k_ =10) 

> 1Code and data: https://github.com/ Eunchan24/PEEL 

are chosen on wiki-ol validation performance; Table 3 reports per- _d_ sensitivity. For arxiv-ol, the wikiol-trained probe is applied unchanged, with inference settings ( _d_ =768, _k_ =20, tree-only) following from the dataset’s compact 61-concept structure rather than from arxiv-ol-specific tuning; no arxivol data is used for training, validation, or hyperparameter selection. 

# **5.2 Structural Fidelity from a Concept Vocabulary** 

PEEL (a 98K-parameter probe receiving _only_ the concept vocabulary) recovers taxonomic DAGs with Graph F1 _._ 885 on wiki-ol (supervised, edgelevel 80/10/10 split) and _._ 931 on arXiv-ol (zeroshot transfer from the wiki-ol-trained probe). OLLM, which consumes the document corpus and fine-tunes Mistral-7B to jointly discover concepts and induce structure, scores _._ 644 and _._ 633 on the same benchmarks as a cross-task reference (§5.3). Table 2 reports all five metrics. 

The probe trained on 80% of wiki-ol gold edges (§5.1) recovers _._ 885 Graph F1 across the full 8 _,_ 033concept structure, generalizing the taxonomic signal beyond the training-edge-replay floor (Memorisation: _._ 419). 

**Wiki-ol.** On wiki-ol’s 8,033 concepts, Cont. F1 rises from _._ 500 (OLLM) to PEEL’s _._ 551. On the two label-string metrics (Lit. F1, Fuzzy F1), LLM label-generation systems hold an expected advantage; Memorisation tops Lit. F1 ( _._ 134) by replaying training edges verbatim, and OLLM leads Fuzzy F1 ( _._ 915) via title-string overlap.


<!-- page 7 -->

|**Dataset**|**Method**|**Input**|**Lit.F1**_↑_|**Fuz.F1**_↑_|**Cont.F1**_↑_|**Grph.F1**_↑_|**Motif.D**_↓_|
|---|---|---|---|---|---|---|---|
|_Concept-_|_only methods (no docu_|_ment access)_||||||
|wiki-ol|Memorisation<br>|training edges<br>|.134<br>|.837<br>|.314<br>|.419<br>|.063<br>|
||PEEL (ours)|concepts only|.111|.877|.551|.885|.000|
|_Documen_|_t-using methods (corp_|_us + concepts)_||||||
|wiki-ol|Hearst Patterns<br>|corpus + concepts<br>|.003<br>|.538<br>|.350<br>|.544<br>|.163<br>|
||Zero-shot (M-7B)<br>|title + abstract<br>|.007<br>|.871<br>|.455<br>|.639<br>|.341<br>|
||Finetune (M-7B)<br>|title + abstract<br>|.124<br>|.884<br>|.470<br>|.588<br>|.050<br>|
||OLLM|title + abstract|.093|.915|.500|.644|.080|
|arXiv-ol|OLLM (transfer)|title + abstract|.040|.570|.357|.633|.097|
||PEEL (zero-shot)|concepts only|.298|.748|.604|.931|.011|



Table 2: Main results on OLLM benchmarks, grouped by input modality. LLM-based baselines additionally consume each article’s title and abstract per the OLLM protocol (Lo et al., 2024, Figs. 5–6); OLLM (transfer) fine-tunes Mistral-7B on 2,048 additional arXiv samples. PEEL rows use a gold concept vocabulary and a probe trained on wiki-ol gold edges (§5.1), the arXiv-ol row zero-shot; OLLM instead discovers concepts and structure from documents, so the OLLM scores are a cross-task reference, not a ranking. Motif Dist. values below 10<sup>_−_4</sup> are reported as _._ 000. 

**ArXiv-ol (zero-shot transfer).** The wiki-oltrained probe transfers zero-shot to arXiv-ol’s 61 categories: PEEL attains Graph F1 _._ 931 and Cont. F1 _._ 604; OLLM, which additionally finetunes Mistral-7B on 2,048 arXiv samples, scores _._ 633 and _._ 357. 

## **5.3 Cross-Task Reference** 

PEEL performs structure induction from a concept vocabulary alone. OLLM addresses a broader task—joint concept discovery _and_ structure induction—and, like the Mistral-7B baselines, consumes article text. The comparison is therefore asymmetric in both task scope and input: PEEL is given strictly less. We report it for reference, not as a same-conditions claim. 

## **5.4 Ablation Studies** 

**Embedding dimension.** Table 3 varies the input prefix truncation _d_ with probe output fixed at _d_ out=128. Cont. F1 peaks at _d_ =512 ( _._ 551) and drops at full dimensionality ( _._ 479 at _d_ =768), matching §3’s coarse-to-fine prefix gradient. We select _d_ =512 on validation Cont. F1; Graph F1 stays in _._ 879– _._ 906 across dimensions, peaking at _d_ =768. Even with _d_ out=32 (24K parameters; Appendix A, Table 4), PEEL yields Graph F1 _._ 870 and Cont. F1 _._ 517. 

**Multi-resolution decomposition.** We extract Chu-Liu/Edmonds trees at each truncation point. Edge-set Jaccard between all dimension pairs stays below _._ 18, with adjacent dimensions ( _d_ =512 vs. _d_ =768: _._ 178) sharing more edges than distant ones ( _d_ =64 vs. _d_ =768: _._ 018). Across all five dimensions, 99% of nodes change parents: prefix trunca- 

tion yields _non-nested decompositions_ , each prefix length inducing a qualitatively distinct hierarchy across resolutions. At the category level, the effect is vivid: the _Mathematics_ subtree grows from 1 child at _d_ =64 to 19 at _d_ =256 and 68 at _d_ =768, illustrating how increasing prefix dimension progressively unfolds fine-grained taxonomic structure (Figure 3). 

# **6 Discussion** 

**What the probe reveals about embedding structure.** A 98K-parameter probe recovers taxonomic DAGs (Graph F1 _._ 885 on Wikipedia, _._ 931 on arXiv) from _frozen_ retrieval embeddings, showing that the prefix-ordering regularity §3 isolates is decodable into explicit parent–child structure without retraining the encoder. The coarse-to-fine gradient isolated by shuffled- and reverse-dimension controls (§3) implies that MRL’s nested-prefix training implicitly organises semantic granularity along the dimension axis, a structural regularity that, to our knowledge, has not been previously documented in standard MRL encoders trained purely for retrieval. 

**Euclidean order embeddings vs. hyperbolic alternatives.** PEEL’s Euclidean order-embedding probe avoids the encoder-retraining required by hyperbolic alternatives such as HiTs (He et al., 2024), achieving structural fidelity with no hierarchyaware encoder training (geometry comparison in Appendix C). 

**Each prefix length captures a different hierarchy.** §5.4 reports that CLE trees at different prefix lengths yield non-nested, complementary decompo-


<!-- page 8 -->

<!-- Start of picture text -->
dim = 64 dim = 256<br>1 child - depth 1 19 children - depth 2<br>Mathematics Mathematics<br>Elementary ... Elementary ... (4) Mathematics... (3) Mathematica... (1) +16 more<br>dim = 768<br>68 children - depth 12<br>Arithmetic (19) Works about... (7) Mathematica... (7) Mathematica... (5) +64 more<br><!-- End of picture text -->

Figure 3: Mathematics subtree extracted at three prefix dimensions from the trained probe: at _d_ =64, only one child is recovered; at _d_ =256, 19 children emerge across depth 2; at _d_ =768, 68 children span 12 levels of depth. Increasing prefix dimension progressively unfolds fine-grained hierarchical structure. 

sitions. This multi-resolution property—extracting multiple taxonomic granularities from a single forward pass over a frozen retrieval embedding, with no retraining or per-resolution recomputation— directly leverages MRL’s nested-prefix design. The kNN purity gradient (§3) and the prefix-level tree disjointness are complementary: the former is a local neighbourhood measure, the latter a global parent–child topology, so prefixes can share neighbourhoods yet decode distinct global hierarchies. 

## **Structure induction as a modular component.** 

PEEL performs structure induction _from a concept vocabulary alone_ , isolating it as a separable subproblem: a 98K-parameter probe over frozen embeddings recovers taxonomic DAGs at Graph F1 _._ 885 and _._ 931 with no document access. Any concept-discovery front-end—an LLM extractor, a corpus miner, or a curated vocabulary—can supply that vocabulary. OLLM, which couples concept discovery and structure induction in a single document-fed pipeline, addresses a broader task and serves as a cross-task reference (§5.3). Pairing PEEL with any such front-end yields an end-to-end taxonomy pipeline without retraining the structureinduction stage. 

# **7 Conclusion** 

Pre-trained Matryoshka Representation Learning (MRL) embeddings organise semantic granularity along the dimension axis; shuffled- and reversedimension controls isolate this gradient to the learned early prefix dimensions across three archi- 

tecturally distinct MRL models (§3). Exploiting this signal, PEEL (a 98K-parameter probe over _frozen_ embeddings, applied to a concept vocabulary alone) recovers taxonomic DAGs with high structural fidelity (Graph F1 _._ 885 on Wikipedia, _._ 931 on arXiv); the document-fed OLLM pipeline is reported as a cross-task reference (§5.3). 

A retrieval-efficiency objective thus yields a multi-resolution taxonomic geometry that PEEL can decode. 

Integrating PEEL with corpus-based concept discovery for end-to-end taxonomy construction is a natural direction for future work. 

# **Limitations** 

Our work has the following limitations. (1) Our evaluation covers two domains from the OLLM benchmarks (Lo et al., 2024) spanning distinct structural profiles (deep polyhierarchy and shallow tree). PEEL transfers zero-shot from wiki-ol to arXiv-ol (§5.2). Our validated transfer covers target ontologies no deeper than the source domain; how far this reach extends is genuinely open. Extension to specialised domains such as biomedicine and law is a natural direction for future work. (2) We adopt the five structural metrics established by the OLLM benchmark (Lo et al., 2024) (Lit F1, Fuzzy F1, Cont F1, Graph F1, Motif Distance), which evaluate taxonomy structure directly. Label realisation quality and downstream utility (e.g., retrieval, question answering) are outside this paper’s scope. (3) The resolution-control analysis in §3 relies on MRL’s nested prefix-truncation prop-


<!-- page 9 -->

erty. The probe itself (§4) operates on any fixeddimensional embedding. (4) PEEL assumes a gold concept vocabulary and source-domain training edges; transfer requires no target-domain edges. 

# **Ethics Statement** 

This work extracts taxonomic structure from publicly available pre-trained embedding models and evaluates on published benchmarks (Lo et al., 2024). No human subjects, private data, or crowdsourced annotations are involved. The taxonomies we construct reflect biases present in the pretraining corpora of the underlying MRL models; users deploying PEEL in sensitive domains should audit the resulting hierarchies for undesirable biases or omissions. Our method’s low computational cost (seconds on a single GPU) reduces the environmental footprint relative to approaches that require fine-tuning large language models.
