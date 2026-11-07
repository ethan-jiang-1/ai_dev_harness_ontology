---
source: 2610.41785-peeling-matryoshka.pdf
part: appendix
converted: 2026-11-07
converter: pymupdf4llm
---

# Peeling the Matryoshka: Extracting Ontological Structure from Retrieval Embeddings · 附录

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

# **A Additional Ablation Studies** 

Table 3, referenced from §4 and §5, reports PEEL’s primary ablation—input prefix truncation _d_ . Figure 4 visualises this sweep, showing PEEL’s Graph F1 and Cont. F1 relative to the OLLM reference baselines across the tested dimensions. 

**Probe output dimension.** Table 4 varies _d_ out with input dimension fixed at _d_ =512. Even at _d_ out=32 (24K parameters), PEEL achieves Graph F1 _._ 870 and Cont. F1 _._ 517. Performance improves monotonically with _d_ out, confirming that additional projection capacity helps but is not strictly necessary. 

**Edge budget sensitivity.** Table 5 varies the DAG expansion budget _n_ expand with all other hyperparameters fixed. Graph F1 remains above _._ 868 across all tested budgets (10K–25K). Cont. F1 peaks at _n_ expand=15 _,_ 000, the configuration used in Table 2. The stability across budgets confirms that _n_ expand is not a sensitive hyperparameter; Table 6 reports the corresponding literal edge precision and recall. 

# **B Qualitative Analysis** 

**Dimensional sensitivity of tree topology.** CLE trees extracted at different dimensions exhibit structurally distinct topologies (e.g., 10 top-level categories at _d_ =64 vs. 17 at _d_ =512 on arXiv-ol), con-


<!-- page 11 -->

|_n_expand|**Cont. F1**_↑_|**Graph F1**_↑_|**Motif Dist.**_↓_|**Model**|**Wiki**|**arXiv**|**Comb.**|**one-sided**_p_|
|---|---|---|---|---|---|---|---|---|
|10,000|.503|.899|.000|Nomic|26/30|16/20|42/50|5_._8_×_10<sup>_−_7</sup>|
|12,000|.533|.893|.000|jina-v3|30/33|20/22|50/55|1_._1_×_10<sup>_−_10</sup>|
|15,000<sup>_⋆_</sup>|.551|.885|.000|Qwen3|29/33|20/22|49/55|9_._1_×_10<sup>_−_10</sup>|
|20,000|.500|.876|.001||||||
|25,000|.451|.868|.001|Table 7: Per|-conditio|n MRL|_>_shuffle|ld win counts|
|OLLM (ref)|.500|.644|.080|fix_×_depth)<br>|and com<br>|bined on<br>|e-sided s<br>|ign test, by m<br>|



Table 7: Per-condition MRL _>_ shuffled win counts (prefix _×_ depth) and combined one-sided sign test, by model and benchmark. All per-model _p <_ 10<sup>_−_6</sup> . 

Table 5: DAG expansion budget ( _n_ expand) sensitivity on wiki-ol.<sup>_⋆_</sup> denotes the Table 2 configuration. Graph F1 is stable across all tested budgets. 

**Euclidean order embeddings.** PEEL trains only a 98K-parameter projection on top of frozen MRL embeddings using an order-embedding loss, requiring no hierarchy-aware pre-training of the encoder. The coordinate-wise dominance constraint directly encodes the asymmetric is-a relation, and the violation score derived from this constraint provides the edge weight for CLE tree extraction (§4.3). 

|_n_expand|**Lit-P**_↑_|**Lit-R**_↑_|
|---|---|---|
|tree only|16.9|9.3|
|10,000|14.6|10.0|
|12,000|12.8|10.5|
|15,000<sup>_⋆_</sup>|11.0|11.2|
|20,000|9.2|12.6|
|25,000|8.0|13.7|



**Comparison summary.** Both approaches map pre-trained language models to hierarchical structure, but differ on two axes: (i) _trainable parameters_ —22M–109M (HiTs) versus 98K (PEEL), a three-order-of-magnitude reduction; (ii) _training objective_ —hierarchy-aware contrastive loss applied to the entire encoder (HiTs) versus orderembedding loss applied only to a lightweight probe over frozen embeddings (PEEL). A direct headto-head benchmark comparison between HiTs and PEEL on the OLLM taxonomies is left for future work. 

Table 6: Literal edge precision and recall by expansion budget on wiki-ol (%).<sup>_⋆_</sup> denotes the Table 2 configuration; the reported setting is balanced rather than recallmaximizing. See §5.1 for the primary structure-sensitive metrics. 

sistent with the dimensional sensitivity observed in Figure 1. Figures 5 and 6 extend the _Mathematics_ example from Figure 3 to two additional categories, confirming that prefix-dependent unfolding of fine-grained structure generalizes across diverse subtrees. 

**Edge overlap vs. structural similarity.** On arXiv-ol, PEEL reproduces 18 of 60 gold edges exactly (30%), while achieving Graph F1 _._ 931. This gap reflects the difference between exact edge matching and SGConv-based structural similarity: PEEL captures global topology even when individual parent–child assignments differ from the gold standard. 

# **D Directional-Consistency Counts** 

Table 7 reports, for each model and benchmark, the number of prefix _×_ depth conditions in which MRL prefix truncation exceeds the shuffled-dimension control, with the combined-benchmark one-sided sign test (null _p_ 0=0 _._ 5). Every per-model _p_ is below 10<sup>_−_6</sup> . The four non-wins in the Nomic–arXiv cell are the full-dimensionality conditions, where the prefix coincides with the complete embedding and MRL, shuffled, and reverse are identical by construction; the cell remains significant (16 _/_ 20, _p_ =5 _._ 9 _×_ 10<sup>_−_3</sup> ). 

# **C Hyperbolic Comparison: Order Embeddings vs. Poincaré Approaches** 

PEEL’s probe operates in Euclidean space with coordinate-wise dominance constraints (Vendrov et al., 2016), rather than in hyperbolic space (Nickel and Kiela, 2017). This appendix details the comparison referenced in §6. 

# **E Raw Geometry Before the Probe** 

Before any probe training, the frozen embeddings already recover which of two concepts is more general: a training-free measure over raw prefixes scores 69 _._ 1% on gold parent–child pairs and 91 _._ 3% on ancestor–descendant pairs at depth gap _≥_ 2, while equal-granularity siblings sit at chance (50 _._ 0%). Explicit, coordinate-aligned _is-a_ containment remains the probe’s contribution: order viola- 

**Hyperbolic encoders.** Poincaré-based approaches such as HiTs (He et al., 2024) retrain the entire encoder (22M–109M parameters) with hierarchy-aware losses, exploiting the exponential volume growth of hyperbolic space to capture tree-like hierarchies with low distortion.


<!-- page 12 -->

<!-- Start of picture text -->
0.90<br>0.80<br>0.70 Grph.F1 (PEEL)<br>Cont.F1 (PEEL)<br>OLL M<br>0.60<br>Table 2<br>0.50 config OLL M<br>64 128 256 384 512 768<br>Embedding dimension<br>F1 score<br><!-- End of picture text -->

Figure 4: PEEL performance by embedding dimension on wiki-ol ( _d_ out=128 fixed).<sup>_⋆_</sup> marks the Table 2 configuration (dim=512). Dashed lines show OLLM baselines. 

tion on the raw axes is at chance under a randomrotation null.


<!-- page 13 -->

<!-- Start of picture text -->
1 childdim - =depth64 1 2 childrendim= - 256depth 1<br>Geography Geography<br>a So<br>38 childrendim= - 768depth 10<br>Geography<br>North Ameri... (10) North Ameri... (7) Regional ge... (5) Regions (4) +34 more<br><!-- End of picture text -->

Figure 5: _Geography_ subtree at three prefix dimensions. At _d_ =64, only 1 child is recovered at depth 1; at _d_ =256, 2 children remain at depth 1; at _d_ =768, 38 children span depth 10. Compare with Mathematics (Figure 3). 



<!-- Start of picture text -->
3 childrendim=- depth64 1<br>dim<br>27 children= -256depth 8<br>51 childrendim= - 768depth 17<br><!-- End of picture text -->

Figure 6: _Science_ subtree at three prefix dimensions. At _d_ =64, 3 children appear at depth 1; at _d_ =256, 27 children span depth 8; at _d_ =768, 51 children span depth 17. Together with Geography (Figure 5) and Mathematics (Figure 3), these examples confirm that prefix truncation induces qualitatively distinct hierarchical decompositions across diverse categories, consistent with the low inter-dimension Jaccard similarity ( _< ._ 18) reported in §5.4.
