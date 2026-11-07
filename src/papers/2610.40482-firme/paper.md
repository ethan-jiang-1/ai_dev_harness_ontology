---
source: 2610.40482-firme.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# FIRME: Registry-Anchored Memory Graphs for Evolving, Heterogeneous Investor Knowledge · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

# **FIRME: Registry-Anchored Memory Graphs for Evolving, Heterogeneous Investor Knowledge** 

Yunbai Zhang<sup>∗</sup> Yunyi Gao<sup>∗</sup> Han-Tai Shiao<sup>†</sup> yunbai_zhang@vanguard.com yunyi_gao@vanguard.com han-tai_shiao@vanguard.com The Vanguard The Vanguard The Vanguard Malvern, Pennsylvania, USA Malvern, Pennsylvania, USA Malvern, Pennsylvania, USA 

## **Abstract** 

Financial AI workflows that reuse investor knowledge need persistent memory that integrates observations across sources and periods without losing identity or provenance. In a knowledge graph, recurring observations may use different surface forms, fragmenting relationship histories and preventing evidence from accumulating. We introduce Fusion and Identity Registry for Memory Evolution (FIRME), a registry-anchored memory graph that reconciles incoming observations to persistent canonical relationships and retains their source, time, and context. Within periods, rule-based fusion links investor-call discussions to portfolio cashflow signals, directly or through a fixed product–topic ontology. Across periods, canonical identities and persistent aliases direct recurring observations to the same relationship history; deterministic updates summarize reinforcement, inactivity, and reactivation. We evaluate FIRME on proprietary investor-call and cashflow records and on S&P 500 earnings-call transcripts. Compared with a historical registry that retains canonical identities and semantic fallback but omits alias memory, FIRME increases finalperiod Correct Match Rate by 7.8–12.1 percentage points across four dataset–backend settings under a fixed-judge and fallbackreview protocol. A blinded human audit of 200 incoming observations per setting finds Correct Match Rate gains of 9.0–16.5 points and reattachment-recall gains of 22.5–29.0 points, with higher observed merge precision in all four samples. A separate audit finds valid evidence paths for 293 of 300 outputs from full withinperiod fusion in the investor-call setting. Extraction-faithfulness and round-trip diagnostics assess source grounding and preservation of extractor-derived graph content. 

## **1 Introduction** 

Understanding an investor’s interests requires attention to current evidence and to how those interests and relationships change with market conditions. The prominence of a concern such as market volatility may rise during turbulence, recede as conditions stabilize, and return when uncertainty increases. Reconstructing these trajectories therefore requires combining heterogeneous sources of evidence. Unstructured text, including call records and meeting notes, provides discussion context, whereas structured records, such as financial-activity tables, capture measurable behavior. Because interests can persist and return, past evidence should neither remain permanently active nor disappear when observations 

> ∗Equal contribution. 

> †Corresponding author. 

> © 2026 The Vanguard Group, Inc. All rights reserved. 

> The paper is accepted at the 3rd Workshop on LLMs and Generative AI for Finance (AI4F) at ACM ICAIF 2026 (non-archival). 

are absent. Agentic and tool-augmented financial workflows that reuse investor knowledge depend on maintaining this knowledge across interactions. This requires recurring observations to update the correct existing relationships while retaining their supporting evidence. 

Maintaining evidence across sources and periods requires reconciliation. Structured records and unstructured text differ in format and vocabulary; the same entity or relationship can vary in name or phrasing over time. Before entering the knowledge store, new evidence must therefore be aligned across sources and matched to the correct persistent identity. Otherwise, observations describing the same relationship form separate entities or connections, each with a partial history, while cross-format supporting evidence remains disconnected. Fragmented relationship histories in agent memory can yield incomplete or redundant context for downstream reasoning about an investor’s recurring concerns. Stable identity is necessary to accumulate evidence under one persistent relationship and track its changes and lifecycle over time. 

Temporal graph memories provide an important starting point. Zep/Graphiti reconciles extracted entities with existing graph nodes, deduplicates facts, links facts to source episodes, and represents when facts are valid or invalidated; its evaluation emphasizes retrieval-supported question answering and latency [20]. In the financial settings we study, the central question is how evidence for the same relationship accumulates and changes across periods. Incoming observations may use different names or come from different sources, and some periods may contain no matched observation. The graph-update challenge is to determine which relationship history receives each new observation and how that relationship’s evidence strength evolves with recurrence, inactivity, and renewed evidence. 

We introduce Fusion and Identity Registry for Memory Evolution (FIRME), a knowledge graph (KG) memory framework, to address this challenge. A stable head identifier anchors whose relationship is being tracked, while an evolving registry reconciles target-name variants to canonical identities, anchoring what that relationship concerns. Together, these identities determine which persistent relationship history receives incoming evidence. The memory graph retains each observation’s relation label, source, time, and context. When conversational and structured evidence coexist, within-period fusion can recognize their corroboration while preserving both observations. Across periods, a recurring observation reinforces the corresponding history; periods without matched observations lower its evidence strength while leaving earlier evidence available. We test the incremental role of retained aliases against a control that still uses historical canonical reconciliation and semantic matching. 

1


<!-- page 2 -->

Zhang, Gao, and Shiao 

FIRME is intended to provide investors and financial professionals with a consolidated, longitudinal view of investor-related information. By accumulating observations under persistent relationship identities, it brings current evidence together with earlier observations across sources, preserving their provenance and historical context. 

# **1.1 Related Work** 

**Text-to-KG Construction and Canonicalization.** Text-to-KG construction progressed from pattern-based extraction and distant supervision [6, 17] to generative relation extraction [10] and LLM pipelines. LLM pipelines add schema control and canonicalization: EDC separates open extraction, schema definition, and canonicalization, while KGGen clusters related entities [18, 23]. GraphRAG structures extracted graphs for corpus-level summarization [4], whereas open-KG methods consolidate synonymous entity and relation expressions [3, 22]. These approaches reduce surface-form sparsity at construction time. They do not determine how recurring observations drawn from heterogeneous sources should accumulate under a single persistent relationship across successive time periods. 

**Temporal KGs and Dynamic Memory.** Temporal KGs model fact validity, while completion models predict missing or future facts from historical representations [9, 11, 13, 16]. ATOM separates observation time from validity time [12]; Zep adds bitemporal facts, provenance, resolution, and conflict-based invalidation for agent memory [20]; and FinDKG propagates latent representations across financial-news snapshots for prediction [15]. These systems foreground fact validity, retrieval, or predictive state. We complement them by asking how recurring or absent evidence changes the salience and lifecycle of an explicit, auditable relationship edge retaining source, time, context, and participants. Recurrence strengthens its evidence state; non-observation lowers current prominence without erasing provenance; later evidence may reactivate it. 

**Heterogeneous Financial KG Fusion.** Multi-source KG integration commonly uses entity alignment and ontology matching [19, 21]. Financial KG research spans news extraction, temporal linkage, deduplication, conflict handling, table-aware construction, and evolving fundamentals or events [1, 5, 14, 24, 25]. These systems primarily organize corporate news, disclosures, fundamentals, or discrete events. Investor-centric data require a different combination: conversational and structured observations may corroborate the same relationship without being duplicates, and missing evidence need not terminate that relationship, whose memory state may decay and later reactivate. 



<!-- Start of picture text -->
𝐺𝑢 𝑡−1 ⊕𝐺𝑠 𝑡−1 𝐺𝑢 𝑡 ⊕𝐺𝑠 𝑡 𝐺𝑢 𝑡+1 ⊕𝐺𝑠 𝑡+1<br>𝑆 𝑡−1 𝑆 𝑡 𝑆 𝑡+1<br>𝑅 𝑡−1 𝑅 𝑡 𝑅 𝑡+1<br>𝑀 𝑡−1 𝑀 𝑡 𝑀 𝑡+1<br><!-- End of picture text -->

**Figure 1: Coupled short- and long-term fusion in FIRME across consecutive periods. Each short-term graph** 𝑆<sup>𝑡</sup> = 𝐺𝑢<sup>𝑡</sup> ⊕ 𝐺𝑠<sup>𝑡</sup> **fuses unstructured and structured graphs. Dashed arrows show registry update from** 𝑅<sup>𝑡−1</sup> **to** 𝑅<sup>𝑡</sup> **, conditioned on** 𝑆<sup>𝑡</sup> **; solid arrows to** 𝑀<sup>𝑡</sup> **show memory reconciliation of** 𝑆<sup>𝑡</sup> **,** 𝑅<sup>𝑡</sup> **, and** 𝑀<sup>𝑡−1</sup> **.** 

# **1.2 Contributions** 

FIRME’s central contribution is an identity-conditioned update of persistent relationship histories across periods (Figure 1). Withinperiod corroboration supports this update in paired investor-call data, while lifecycle states make the resulting histories interpretable. 

**Coupled registry–memory recurrence** . FIRME couples an evolving registry of canonical identities and retained aliases to a memory graph of relationship histories. A stable head identifier and a reconciled target identity determine which history receives each observation, even when names or evidence sources differ. The history retains each observation’s relation label, source, timestamp, and context; it receives at most one strength and lifecycle update per period. Against a no-alias control that retains historical canonical reconciliation and semantic fallback, full FIRME improves final-period Correct Match Rate (CMR) by 7.8–12.1 percentage points across four dataset–backend settings under the judge and fallback-review protocol (Table 3). In the shared blinded human audit (Table A2), reattachment recall improves by 22.5–29.0 points, and observed merge precision is higher in all four samples. 

**Audited within-period corroboration** . For paired investorcall and cash-flow records, same-investor, same-period rules identify direct product corroboration and ontology-mediated support from a discussed topic. The derived product relationship references its supporting observations without merging topic and product identities. In the final-period Opus 4.6 human audit, 293 of 300 Full fusion outputs had valid evidence paths, including 91 of 94 outputs triggered by Rule 4 but not Rule 3 (Table 7). 

**Interpretable lifecycle state assignment** . Given reconciled relationship histories, fixed rules update an evidence-strength score from matched or unmatched periods and assign one of five lifecycle states from match status, prior state, and consecutive unmatched periods. Each assigned state is traceable to retained observations and periods without a match, providing an interpretable summary of the relationship’s recorded evidence trajectory. 

2


<!-- page 3 -->

FIRME: Registry-Anchored Memory Graphs for Evolving, Heterogeneous Investor Knowledge 

The longitudinal investor-call corpus includes paired cash-flow records and tests identity continuity and short-term corroboration. The transcript-only S&P 500 corpus tests temporal reconciliation under a broader entity schema. Extraction-faithfulness and roundtrip recovery diagnostics, lifecycle trajectories, and analytical parameter behavior provide complementary checks. 

# **2 Problem Formulation** 

# **2.1 Preliminaries and Notation** 

A knowledge graph is 𝐺= (𝑉, ℛ, 𝐸), where 𝑉 is the entity set, ℛ the relation-type set, and 𝐸⊆𝑉× ℛ × 𝑉 contains directed, typed edges (𝑢, 𝑟, 𝑣) from head 𝑢 to tail 𝑣 through relation 𝑟. In the investor-call fusion setting, FIRME constructs a graph with the three entity types and three relation types defined in Section 3.1. We call the product or topic at tail 𝑣 the _target entity_ ; it is distinct from the head entity 𝑢. The S&P 500 transcript-only setting uses a broader set of extracted entity types. 

# **2.2 Data Modalities** 

In the investor-call setting, FIRME integrates two modalities. At period 𝑡, _unstructured data_ consists of text from call transcripts and meeting notes and yields 𝐺𝑢<sup>𝑡</sup> . Each tuple (𝑢, 𝑟, 𝑣) relates a person or organization 𝑢 through 𝑟 to a product or topic 𝑣 . The extractor is prompted to identify relationships involving substantive discussion. 

_Structured data_ consists of predefined records such as relational tables and yields 𝐺𝑠<sup>𝑡</sup> . A primary index identifies a person or organization; graph-construction rules specify which columns and value conditions instantiate edges. For example, an investor’s capital inflow into a product can instantiate an investor–product behavioral edge. 

# **2.3 Problem Statement** 

Constructing a temporally coherent graph from these inputs poses three interrelated problems. 

**Short-term fusion** . Given 𝐺𝑢<sup>𝑡</sup> and 𝐺𝑠<sup>𝑡</sup> within period 𝑡, shortterm fusion combines the two partial graphs into the coherent, consolidated graph 𝑆<sup>𝑡</sup> = 𝐺𝑢<sup>𝑡</sup> ⊕𝐺𝑠<sup>𝑡</sup> . Product- and topic-level evidence is aligned through a fixed product–topic ontology 𝑂 (Appendix G), while ⊕ combines discursive evidence with structured cash-flow signals. The strong-interest relation is assigned only when both modalities corroborate a relationship; it is a rule-based evidential label, not a calibrated preference or stance estimate. 

**Long-term fusion** . Long-term fusion maintains a temporally coherent memory graph as investment interests emerge, strengthen, persist, weaken, and may resurface after dormancy. Each canonical relationship in 𝑀<sup>𝑡</sup> is a time-indexed edge whose attribute vector 𝒉𝑡 accumulates observations (𝑢, 𝑟, 𝑣) and supporting evidence, together with first- and last-seen periods, a memory-strength score, and a lifecycle state. As Figure 1 shows, 𝑆<sup>𝑡</sup> is normalized through the prior registry 𝑅<sup>𝑡−1</sup> ; these edges are reconciled with the prior memory graph 𝑀<sup>𝑡−1</sup> . These operations define 



<!-- Start of picture text -->
𝑅 𝑡 = Θ1(𝑅 𝑡−1 , 𝑆 𝑡 ) ,<br>(1)<br>𝑀 𝑡 = Θ2(𝑀 𝑡−1 , 𝑅 𝑡 , 𝑆 𝑡 ) ,<br><!-- End of picture text -->

**Table 1: Entity and relation schema for investor-call fusion.** 

|**Entity types**||
|---|---|
|person/org<br>product|Tracked investor or asset-management firm<br>Financial instrument (e.g.,VOO,BND)|
|topic|Investment theme (e.g., ESG Investing)|
|**Relation types**||
|discussed<br>_Unstructured_<br>cf-signal|Product/topic identified as substantively<br>discussed<br>i l|
|_Structured_|Investor shows significant inflow into a<br>product|
|strong-interest<br>_Fusion_|Corroborating evidence in both modalities|



where Θ1 and Θ2 denote the coupled registry and memory reconciliation dynamics. We initialize 𝑅<sup>0</sup> = 𝑀<sup>0</sup> = ∅. At 𝑡= 1, candidates in 𝑆<sup>1</sup> are deduplicated by lemmatized string equality and then by semantic matching for unresolved same-type candidates; all normalized edges enter 𝑀<sup>1</sup> in the _Emerging_ state with a baseline score of 0.5. For 𝑡> 1, unresolved same-type candidates are semantically compared only with 𝑅<sup>𝑡−1</sup> . 

**Entity normalization** . Entity normalization determines whether text-extracted entities 𝑣𝑖 and 𝑣𝑗 in 𝐺𝑢 denote the same entity. Without it, near-duplicates fragment one relationship’s history and burden both fusion stages; Section 3 presents the registry-based solution. 

# **3 Methodology** 

# **3.1 Entity and Relation Schema** 

The investor-call fusion schema in Table 1 has three entity types: person/org for the person or organization whose relationships are tracked, product for a specific financial instrument, and topic for an investment theme or strategy. Three relation types link these head entities to products and topics. The discussed relation denotes a product or topic identified by the extractor as substantively discussed in the call. Structured cf-signal marks significant capital allocation toward a product, and strong-interest is a rulederived evidential label requiring cross-modal corroboration, not a calibrated preference or stance estimate. 

The S&P 500 transcript-only evaluation uses a broader extraction schema, with entity types such as Company, Person, Product, GeographicRegion, and FinancialMetric. These entities enter temporal reconciliation without the investor-call cash-flow fusion rules. 

The graph head is the tracked business entity: an investor or asset-management firm in the investor setting, or a reporting company in the S&P 500 corpus. In the investor-call corpus, the call’s canonical subject_entity_id and the cash-flow record’s owner identify the same investor. The actual call speaker is recorded separately in raw_subject and speaker_role; a speaker change does not change the graph head. Cross-modal corroboration therefore requires the same investor ID and period, as well as the product or topic conditions in Section 3.3. 

3


<!-- page 4 -->

Zhang, Gao, and Shiao 

# **3.2 Knowledge Graph Construction** 

FIRME’s text-to-graph component, _LLM2Graph_ , builds the unstructured graph 𝐺𝑢 by processing each document 𝑑∈𝐷 and emitting (𝑢, 𝑟, 𝑣, 𝑑), where 𝑑 records the supporting textual evidence. In the investor-call setting, it preserves each source-provided head ID and maps raw product and topic mentions to period-local normalized candidates, assigning each a deterministic identifier derived from its entity type and lemmatized name. The extractor’s canonical layer performs period-local normalization without access to the historical entity registry or its learned aliases. The investor-call extraction system prompt is provided in Appendix F.1. 

After period-local graph construction and, when structured data are available, short-term fusion, the persistent registry maps candidates to cross-period canonical identities through deterministicidentifier, normalized-name, and alias matching. LLM-based semantic matching against canonical names and aliases is reserved for unresolved same-type candidates. Matched candidates adopt the anchor ID and add their surface forms to the anchor’s alias set in 𝑅<sup>𝑡</sup> . Only candidates unresolved after all matching tiers retain their identifiers and extend the registry. 

The structured graph 𝐺𝑠 captures cash-flow signals, namely capital inflows from investors into products, as (𝑢, cf-signal, 𝑣). Following the use-case definition of a material allocation, 𝐺𝑠<sup>𝑡</sup> includes an edge only when monthly inflow exceeds $100K; otherwise, the signal is ignored to avoid over-counting weak signals. Each record’s owner field is the stable investor identifier. 

# **3.3 Short-Term Fusion** 

Within each period, short-term fusion combines 𝐺𝑢<sup>𝑡</sup> and 𝐺𝑠<sup>𝑡</sup> into 𝑆<sup>𝑡</sup> . Conversational product expressions are mapped to official product identities (e.g., _Vanguard S&P 500 ETF_ to _VOO_ ). We derived the product–topic ontology 𝑂 from our proprietary internal resource, manually annotated by our financial analyst team, and froze it before evaluation. The association semantics, representative records, and their use in Rule 4 are illustrated in Appendix G. Original observations retain source indicator 1 for unstructured evidence or 2 for structured evidence. Corroborated product relationships receive the derived hybrid indicator 3; this does not change the source indicators of their observations. 

Table 2 defines four rules. Rules 1–2 retain uncorroborated relationships with their original labels. Rule 3 performs direct corroboration: a current discussion and cash-flow signal for the same investor–product pair assign strong-interest to the product relationship. Rule 4 combines a current topic discussion with a current cash-flow signal for an ontology-linked product from the same investor. The product relationship is labeled strong-interest, while the topic relationship remains discussed. A topic may corroborate several allocated products without being duplicated in its own history. 

Fusion retains the original targets and provenance of all observations. Under Rule 3, both observations belong to the same product history; under Rule 4, the product relationship references the supporting topic discussion, which also remains in its own topic history. All applicable direct and ontology-mediated support paths 

are retained as references, not additional observations. All original targets remain available for registry reconciliation. Appendix E provides pseudocode and cross-period examples. 

# **3.4 Long-Term Memory Fusion** 

Long-term memory fusion combines registry-based entity reconciliation with rule-based edge reconciliation. Entity reconciliation establishes persistent identities, while edge reconciliation accumulates observations and updates relationship histories, memory strength, and lifecycle states across periods. 

**Cross-Period Entity Reconciliation** . FIRME resolves incoming entities against the prior registry through identifier, normalized-name, and learned-alias matching, applied as sequential deterministic checks. That is, it first checks for an exact identifier match, then compares the incoming entity’s normalized name with registered canonical names, and finally checks for a matching alias previously associated with a canonical identity. The sequence stops once a match is found. For each unresolved entity, the candidate set comprises all entities of the same type in the prior registry 𝑅<sup>𝑡−1</sup> . The LLM assigns semantic similarity scores to these candidates using their canonical names and aliases. The system prompt for semantic matching is provided in Appendix F.2. A deterministic rule filters candidates with scores ≥ 0.8 and selects the highest-scoring candidate. The incoming entity adopts the selected canonical ID, and its surface forms are added to that identity’s alias set. If no candidate meets the threshold, the entity is registered as new. An exploratory threshold-selection analysis is provided in Appendix D. Appendix C provides pseudocode. 

**Cross-Period Edge Reconciliation** . After entity reconciliation, each original observation updates the history identified by its head ID and typed canonical target ID. Topic and product identities remain distinct; relation labels and source indicators are preserved per observation and excluded from the key. Each key undergoes one update per period: initialization if new, reinforcement if observed again, or decay if no current observation targets it. Multiple observations or corroboration paths do not produce additional score updates. Historical corroboration remains retrievable but does not count as current evidence. Relation upgrades follow Table 2 independently of memory-strength updates. 

Within this procedure, the _Memory Reinforcement–Decay Model_ updates the memory-strength score 𝜎𝑡 (𝑒) ∈[0, 1] through a deterministic match gate. It draws on the gating intuition of long shortterm memory (LSTM) networks [7], rather than adopting their learned recurrent architecture. A new edge starts at 𝜎init = 0.5. An existing matched edge is reinforced additively at rate 𝛼= 0.2, 



<!-- Start of picture text -->
𝜎𝑡 (𝑒) = min(1.0, 𝜎𝑡−1(𝑒) + 𝛼) , (2)<br><!-- End of picture text -->

driving repeated matches toward saturation. An unmatched edge decays multiplicatively at retention rate 𝛾= 0.8, 



<!-- Start of picture text -->
𝜎𝑡 (𝑒) = 𝛾𝜎𝑡−1(𝑒), (3)<br><!-- End of picture text -->

giving exponential decay. Scores below 0.01 become zero, but the edge remains stored. 

**Lifecycle States** . Lifecycle states provide an interpretable summary of each relationship’s temporal trajectory, determined by match status, prior state, and an inactivity counter for consecutive 

4


<!-- page 5 -->

FIRME: Registry-Anchored Memory Graphs for Evolving, Heterogeneous Investor Knowledge 

**Table 2: Short-term fusion rules in FIRME. Rules 1–2 retain uncorroborated relationships; Rules 3–4 assign strong-interest to products using current-period evidence from the same investor. Rule 4 retains the discussed-topic relationship. Original observations and provenance are preserved under all rules; TaxEff denotes Tax Efficiency.** 

|**Rule **|**Type **|**Antecedent**|**Consequent**|
|---|---|---|---|
|1|Pass|discussed(Alice, VFIAX, 1)|⇒discussed(Alice, VFIAX, 1)|
|2|Pass|cf-signal(Bob, VOO, 2)|⇒cf-signal(Bob, VOO, 2)|
|3|Fuse|discussed(Chris, BND, 1)⊕|⇒strong-interest(Chris, BND, 3)|
|||cf-signal(Chris, BND, 2)||
|4|Fuse|discussed(Emma, TaxEff, 1)⊕|⇒discussed(Emma, TaxEff, 1)|
|||cf-signal(Emma, VTEB, 2),<br>with(VTEB,TaxEff) ∈𝑂|andstrong-interest(Emma, VTEB, 3)|





<!-- Start of picture text -->
≤3 misses<br>> 3 misses<br>Stable Fading<br>New Emerg.<br>Reinf. React.<br><!-- End of picture text -->

**Figure 2: Memory-edge lifecycle with inactivity threshold** 𝑁= 3 **. The entry arrow initializes a relationship as Emerging. Solid transitions between states, including self-loops, denote matches; dashed transitions denote misses. Guards count consecutive misses including the current period; a match resets the count.** 

unmatched periods. An edge is _Emerging_ when newly created; _Reactivated_ when matched after _Fading_ or with prior inactivity above 𝑁 ; _Reinforced_ for other matches; _Stable_ when unmatched with inactivity at most 𝑁 ; and _Fading_ when unmatched with inactivity above 𝑁 . 

Initialization and matches reset the inactivity counter to zero; misses increment it. With 𝑁= 3, an edge remains _Stable_ through three consecutive unmatched periods and becomes _Fading_ on the fourth (Figure 2). Scores decay from the first unmatched period, including periods in the _Stable_ state. Appendix E provides worked examples. The resulting state estimates interest evolution from observed evidence rather than measuring latent preference directly. 

Entity reconciliation and edge reconciliation implement Θ1 and Θ2, respectively, in Equation 1. Edges are never removed; even zero-score edges remain available for reactivation. 

**Relationship as an Attribute Vector** . Whereas the base relation 𝑟 in a static triple (𝑢, 𝑟, 𝑣) is a single categorical label, its 



<!-- Start of picture text -->
counterpart in 𝑀 𝑡 is a time-dependent attribute vector,<br>𝑒𝑡 = (𝑢, 𝒉𝑡 , 𝑣) , (4)<br><!-- End of picture text -->

where 𝒉𝑡 stores each observation’s identifier, original typed target, relation type 𝑟, source indicator, timestamp, supporting context, and head identifier, plus speaker identity and role when available, together with edge-level first- and last-seen periods, memory state, and score 𝜎𝑡 (𝑒). Corroboration records reference supporting observations and applicable ontology links without changing the observations’ original targets. Observations reconciled to the same canonical edge accumulate in 𝒉𝑡 without overwriting earlier evidence, so score and state summarize the relationship’s evolving strength and lifecycle. 

# **4 Empirical Evaluation** 

# **4.1 Evaluation Criteria and Setup** 

We evaluate FIRME primarily through **memory usability** , focusing on cross-period identity continuity and graph consolidation. **Extraction faithfulness** and **round-trip recovery** provide supporting diagnostics of source support and extractor-derived content preservation after graph-to-text-to-graph conversion. A final human audit evaluates the evidence supporting direct and ontology-mediated product corroboration. 

We evaluate on two corpora. The first is a proprietary corpus of real investor-call transcripts paired with monthly portfolio cash-flow records; it spans 10 monthly periods with roughly 1,200 calls each. The transcripts and cash-flow records were obtained from routine business records and linked by investor identifier and month. Any personally identifiable information (PII) was masked. These data are not publicly available due to confidentiality restrictions. 

The second corpus is the S&P 500 Earnings Transcripts Dataset [2]. We sampled 297 reporting companies with earnings calls dated February 2025 in the final period 𝑇 and used their available transcripts across three reporting periods. Extracted entity types include companies, people, products and services, geographic regions, and financial topics. Each reporting company ID serves as a graph head. Because this corpus contains only transcripts, it evaluates extraction and temporal reconciliation, not cash-flow fusion. 

Memory usability, extraction faithfulness, and round-trip recovery use evaluation inputs from the final period 𝑇 . The final period contains approximately 1,300 investor calls with 10.3K incoming 

5


<!-- page 6 -->

Zhang, Gao, and Shiao 

edges, and 297 S&P 500 earnings calls with approximately 6.3K incoming edges. The approximate edge totals refer to the Opus 4.6 reconciliation inputs. Round-trip recovery samples reference graphs from these final-period extracted outputs. 

Unless stated otherwise, primary language-model components use Claude Opus 4.6 (Opus 4.6), and both corpora are additionally evaluated with GPT-5.4-mini; both backends use temperature 0.0. The extraction-faithfulness benchmark includes GraphRAG [4] as an additional comparison framework. Gemini 3.1 Pro serves as the fixed LLM judge across both datasets and all evaluated backends and strategies. It assesses grounding, normalization accuracy, and adjusted-precision grounding in round-trip recovery. Reattachment correctness is assessed through two complementary protocols. For LLM-Norm, FIRME w/o Alias Memory, and FIRME, Gemini 3.1 Pro evaluates all accepted reattachments, with two annotators reviewing cases initially judged incorrect (Appendix H). A separate blinded human audit establishes an adjudicated reference for 200 incoming units per dataset–backend setting, shared by all five strategies (Appendix A). Memory updates use reinforcement 𝛼= 0.2, per-period retention 𝛾= 0.8, initialization 𝜎init = 0.5, inactivity threshold 𝑁= 3, and zeroing threshold 0.01. Deterministic identifier and name matches are accepted directly; unresolved candidates enter a semantic tier at threshold 0.8. This threshold was selected using the penultimate period (𝑇−1) of the investor-call corpus (Appendix D) and used for final-period evaluation. 

# **4.2 Memory Usability** 

We first evaluate whether registry-anchored reconciliation enables recurring observations to accumulate under persistent relationship identities. We define _identity continuity_ as linking semantically equivalent observations across periods to the same canonical relationship. We compare **RAW** exact surface forms, **spaCy-Lemma** deterministic lemmatization [8], **LLM-Norm** independent withinperiod semantic normalization, **FIRME w/o Alias Memory** , and full **FIRME** . LLM-Norm normalizes each period independently, after which equal names or identifiers can be matched deterministically across periods. To evaluate the incremental contribution of persistent alias memory, we introduce FIRME w/o Alias Memory as a canonical-only historical registry control. It retains canonicalID and canonical-name matching and cross-period semantic fallback, but removes the storage and reuse of alternative names. Appendix B details the control and the role of each comparison. 

The **Edge Compression Rate** and **Entity Compression Rate** measure reductions in distinct edges and entities in cumulative memory relative to RAW; higher values indicate greater consolidation. The **Memory Match Rate (MMR)** is the fraction of incoming observations represented in 𝑆<sup>𝑡</sup> that are reattached to cumulative memory 𝑀<sup>𝑡−1</sup> , and **Merge Precision** measures the proportion of accepted reattachments judged to target the correct existing relationship. **Correct Match Rate (CMR)** is the proportion of incoming observations judged to be correctly reattached to cumulative prior memory: 



<!-- Start of picture text -->
CMR = MMR × Merge Precision. (5)<br><!-- End of picture text -->

Within each dataset–backend setting, strategies share the same incoming observations. We evaluate whether each incoming observation is correctly reattached. Multiple observations can refer to the 



<!-- Start of picture text -->
muni bond<br>tlh<br>extending bond<br>duration municipal<br>bond<br>tax-loss<br>harvesting active<br>investor<br>management<br>lengthen<br>duration<br>extend munis<br>duration<br>investment-grade<br>treasury<br>harvesting<br>tax losses<br>(a) LLM-Norm<br>municipal<br>bond<br>tax-loss<br>harvesting active<br>investor<br>duration management<br>extension<br>investment-grade<br>treasury<br>(b) FIRME<br><!-- End of picture text -->

**Figure 3: Topic consolidation under LLM-Norm (a) and FIRME (b); colors link surface variants assigned to one canonical topic, while uncolored topics remain distinct.** 

same historical relationship, so they remain separate evaluation units while contributing to one relationship history. CMR uses all incoming observations as its denominator. Human-audit reattachment recall instead measures the fraction of gold-recurring incoming units correctly reattached to their historical identities. 

Compression rates describe cumulative memory at the final period; MMR covers all final-period incoming observations. In Table 3, precision and CMR for LLM-Norm, FIRME w/o Alias Memory, and FIRME use the judge and fallback-review protocol. RAW and spaCy-Lemma use backend-specific human-audit precision; their CMR estimates multiply the reported population MMR by that precision. The final column reports human-audit reattachment recall. Appendix A provides the complete human-audit results. 

Under the judge and fallback-review protocol, full FIRME increases CMR over FIRME w/o Alias Memory by 7.8–12.1 percentage points across the four settings (Table 3). These gains support the incremental contribution of persistent alias memory beyond canonical-only historical reconciliation. Full FIRME also achieves 2.3–3.7 times the CMR of LLM-Norm. The canonical-only control exceeds LLM-Norm in every setting, supporting the combined value of historical canonical reconciliation and semantic fallback. 

6


<!-- page 7 -->

FIRME: Registry-Anchored Memory Graphs for Evolving, Heterogeneous Investor Knowledge 

**Table 3: Memory usability. CR (compression rates) and MMR summarize population outputs. Precision uses human-audit estimates for RAW/spaCy-Lemma (** † **); otherwise, Gemini 3.1 Pro judges all accepted reattachments, with human review of initially incorrect cases. CMR is population MMR** × **precision. All reattachment recall values come from the shared human audit (200 incoming units per setting; CIs in Appendix A). Bold marks the highest CR, MMR, CMR, and recall within each setting.** 

|**Dataset **|**Backend **|**Strategy**|**Edge**<br>**CR**|**Entity**<br>**CR**|**MMR**|**Merge**<br>**precision**|**CMR**|**Reattachment**<br>**Recall**|
|---|---|---|---|---|---|---|---|---|
|||RAW|0.0%|0.0%|7.6%|100.0%<sup>†</sup>|7.6%<sup>†</sup>|15.0%|
|It||spaCy-Lemma|3.0%|7.6%|8.4%|94.1%<sup>†</sup>|7.9%<sup>†</sup>|20.0%|
|nvesor<br>calls|Opus 4.6|LLM-Norm<br>FIRME w/o|6.1%|22.6%|8.3%|98.5%|8.2%|20.0%|
|||Alias Memory|15.4%|43.7%|24.1%|92.3%|22.2%|52.5%|
|||**Full FIRME**|**20.2%**|**51.1%**|**31.8%**|95.5%|**30.4%**|**77.5%**|
|||RAW|0.0%|0.0%|5.9%|100.0%<sup>†</sup>|5.9%<sup>†</sup>|15.0%|
|It|GPT|spaCy-Lemma|1.9%|4.2%|6.6%|100.0%<sup>†</sup>|6.6%<sup>†</sup>|16.3%|
|nvesor<br>calls|-5.4-<br>mini|LLM-Norm<br>FIRME w/o|10.0%|26.5%|9.0%|83.5%|7.5%|20.0%|
|||Alias Memory|16.2%|35.2%|22.4%|83.3%|18.7%|46.3%|
|||**Full FIRME**|**20.7%**|**41.4%**|**31.9%**|83.0%|**26.5%**|**68.8%**|
|||RAW|0.0%|0.0%|19.0%|100.0%<sup>†</sup>|19.0%<sup>†</sup>|21.5%|
|||spaCy-Lemma|4.7%|6.9%|25.3%|98.0%<sup>†</sup>|24.8%<sup>†</sup>|38.5%|
|S&P 500|Opus 4.6|LLM-Norm<br>FIRME w/o|3.9%|6.0%|24.1%|99.3%|23.9%|36.2%|
|||Alias Memory|8.8%|14.7%|49.2%|93.8%|46.1%|63.1%|
|||**Full FIRME**|**10.5%**|**17.9%**|**59.1%**|97.2%|**57.4%**|**88.5%**|
|||RAW|0.0%|0.0%|14.1%|100.0%<sup>†</sup>|14.1%<sup>†</sup>|21.0%|
|||spaCy-Lemma|2.3%|5.2%|16.3%|97.0%<sup>†</sup>|15.8%<sup>†</sup>|32.0%|
|S&P 500|<sup>GPT-5.4-</sup><br>mini|LLM-Norm<br>FIRME w/o|2.8%|7.1%|16.2%|99.5%|16.1%|30.0%|
|||Alias Memory|5.4%|14.7%|28.6%|86.0%|24.6%|48.0%|
|||**Full FIRME**|**7.6%**|**18.2%**|**44.8%**|82.0%|**36.7%**|**77.0%**|



In this evaluation, merge precision improves with alias memory in both Opus 4.6 settings and changes little on investor calls with GPT-5.4-mini. On S&P 500 with GPT-5.4-mini, CMR increases from 24.6% to 36.7%, while precision decreases from 86.0% to 82.0%. These judge-based results indicate a coverage–precision trade-off in that setting. 

FIRME also yields the highest Edge Compression Rate and Entity Compression Rate in every setting, providing complementary evidence of reduced memory fragmentation. Figure 3 illustrates the reduction from 11 surface-form topics under LLM-Norm to five canonical topics under FIRME, while preserving distinct topics. 

**Human-audit methods.** Because population coverage statistics do not establish correctness or missed matches, we complemented them with a blinded human audit. We randomly sampled 200 final-period incoming relationship units per dataset–backend setting without replacement, including unmatched units, and evaluated all five strategies against the same reference. Two annotators independently searched historical evidence through 𝑇−1 and assigned recurring, new, or unresolved labels, blinded to strategy predictions, automated judgments, and each other’s labels. A third annotator adjudicated disagreements remaining after evidence-based 

discussion. Because fallback review covers only reattachments initially judged incorrect, the blinded audit also provides an independent check on errors among those judged correct. Appendix A details the evidence requirements, annotation agreement, metric denominators, and Wilson 95% confidence intervals. 

**Human-audit results.** Compared with FIRME w/o Alias Memory, full FIRME increased observed human-audit CMR by 9.0– 16.5 percentage points and reattachment recall by 22.5–29.0 points across the four settings (Table A2). Human-audit merge precision was also higher in all four samples, ranging from 85.6% to 97.5%. Full FIRME achieved the highest observed human-audit CMR and recall among all five strategies in every setting. Its recalls on investor calls were 77.5% and 68.8% with Opus 4.6 and GPT-5.4-mini, respectively; corresponding S&P 500 recalls were 88.5% and 77.0% (Table 3). RAW and spaCy-Lemma had high observed precision on smaller accepted subsets, with recall ranging from 15.0% to 38.5%. 

Across LLM-Norm, FIRME without Alias Memory, and Full FIRME, human-audit merge precision differed from populationprotocol estimates by 0.3–5.8 percentage points, while the CMR ordering was unchanged in all four settings (Tables 3 and A2). The broadly similar precision estimates and consistent CMR ordering 

7


<!-- page 8 -->

Zhang, Gao, and Shiao 

**Table 4: Token consumption for approximately 1,300 investor calls in the final period** 𝑇 **, using Opus 4.6. Totals cover entity canonicalization and cross-period semantic matching; earlier registry-construction periods are excluded. M denotes million tokens.** 

|**Strategy**|**Entity**<br>**canon.**|**Semantic**<br>**matching**|**Total**|
|---|---|---|---|
|LLM-Norm|5.42M|—|5.42M|
|FIRME w/o Alias Memory|5.29M|1.39M|6.68M|
|Full FIRME|5.37M|0.83M|6.20M|



provide independent human evidence supporting the populationlevel finding that alias memory improves correct relationship recovery in the evaluated settings. 

**Token consumption.** FIRME stores accepted semantic matches as alias-to-canonical mappings for later reuse. Recurring aliases can then be resolved deterministically, whereas the no-alias control requires semantic fallback whenever canonical-ID and canonical-name matching fail. On approximately 1,300 investor calls in the final period 𝑇 using Opus 4.6, the three strategies have similar entity-canonicalization token consumption (Table 4). Compared with FIRME w/o Alias Memory, full FIRME reduces semantic-matching consumption by 40.3% and total consumption across the two stages by 7.2%. These reductions are consistent with alias reuse. Measurements exclude earlier registry-construction costs. 

# **4.3 Extraction Faithfulness** 

Reliable memory accumulation requires not only cross-period identity continuity but also source-grounded observations within each period. We therefore assess extraction faithfulness through quotation verification, entity traceability, and entity normalization. Extraction faithfulness was evaluated on all final-period textextracted relationships produced by each extractor–backend configuration, before fusion and cross-period reconciliation. We trace four stages: document, quoted evidence, raw entity mention, and normalized entity. **Quotation Verification Rate** is the share of extracted evidence texts appearing in the source, flagging fabricated quotations. The **Entity Traceability Rate** measures the share of raw entity mentions located in their associated evidence text using 0.7 token-overlap fuzzy matching and a language-model fallback for paraphrases. **Entity Normalization Accuracy** is the share of raw-to-normalized mappings judged semantically correct. The **Hallucination Rate** is the proportion of evaluated relationships whose evidence fails quotation verification or whose raw target fails traceability. The **Normalization Error Rate** equals one minus normalization accuracy. These diagnostics do not separately assess relation entailment, direction, stance, or graph completeness. Because verification and normalization are independent, verified edges may be mismapped, while correctly mapped edges may contain hallucinated evidence. 

GraphRAG used GPT-5.4-mini as its backend. Its text-unit identifiers linked schema-aligned relationships to source chunks, allowing us to apply the same criteria reported in Table 5. Appendix H 

**Table 5: Extraction-faithfulness Hallucination (Hall.) and Normalization Error (N.Err.) rates by extractor and backend.** 

|**Dataset **|**Extractor**|**LLM**<br>**Backend**|**Hall.**|**N.Err.**|
|---|---|---|---|---|
|Investor<br>|LLM2Graph|Opus 4.6|3.3%|3.2%|
|calls|LLM2Graph|GPT-5.4-mini|6.6%|7.74%|
||LLM2Graph|Opus 4.6|7.4%|2.8%|
|S&P 500|LLM2Graph|GPT-5.4-mini|5.87%|22.16%|
||GraphRAG|GPT-5.4-mini|11.5%|17.0%|



describes the adapter. On investor calls, Opus 4.6 halved Hallucination Rate (3.3% versus 6.6%) and more than halved Normalization Error Rate (3.2% versus 7.74%) relative to GPT-5.4-mini; all Hallucination Rates were below 7%. On S&P 500, no backend dominated: GPT-5.4-mini lowered hallucination (5.87% versus 7.4%) but raised normalization error (22.16% versus 2.8%). Opus 4.6 normalization error was similar across corpora (3.2% and 2.8%). Against backend-matched GraphRAG, FIRME’s LLM2Graph extractor with GPT-5.4-mini roughly halved hallucination (5.87% versus 11.5%) but increased normalization error (22.16% versus 17.0%), so normalization varied more than hallucination across LLM2Graph backends under the fixed judge. 

# **4.4 Round-Trip Recovery** 

An extractor may produce source-grounded outputs while still omitting information from the input during extraction. Beyond extraction faithfulness, we therefore evaluate preservation across representations. Round-trip recovery measures how much extractor-derived graph content survives graph-to-text generation and subsequent re-extraction. Each reference graph contains the complete Opus 4.6 LLM2Graph output for one final-period call. For each corpus, we sampled 1,000 reference graphs uniformly with replacement and generated one document for each sampled instance using a fixed Opus 4.6 generator. These documents were shared across all evaluated re-extraction backends; only the re-extraction backend varied. Because generation may add document-grounded topics absent from the reference graph, adjusted precision accepts an extra recovered item only when the fixed Gemini 3.1 Pro judge determines that the document explicitly supports it. We independently macro-average adjusted precision, recall, and F1 across instances at node and edge levels. Appendix H specifies node/edge matching and the metric formulas. 

Table 6 shows similar investor-call node- and edge-level F1 across backends (0.923–0.931). For S&P 500, F1 is 0.862–0.865 with Opus 4.6 and 0.786–0.805 with GPT-5.4-mini, a larger gap. Adjusted precision remains 0.952–0.982, while recall carries most loss and reaches 0.697 on S&P inputs. High adjusted precision means recovered items match reference-graph content or have explicit support; lower recall means greater loss of reference-graph content. With shared Opus-generated documents, S&P-derived documents show lower preservation and greater backend sensitivity than investorcall-derived documents. 

8


<!-- page 9 -->

FIRME: Registry-Anchored Memory Graphs for Evolving, Heterogeneous Investor Knowledge 

**Table 6: Round-trip recovery: adjusted precision (Adj. P), recall (R), and F1, independently macro-averaged across instances at node and edge levels.** 

|**Dataset**|**LLM**<br>**Backend**|**Level **|**Adj. P**|**R**|**F1**|
|---|---|---|---|---|---|
||Ous 46|Node|0.952|0.918|0.931|
|Investor<br>|p .|Edge|0.954|0.917|0.929|
|calls|GPT-54-mini|<sup>Node</sup>|0.963|0.902|0.926|
||.|<br>Edge|0.968|0.898|0.923|
||Ous 46|Node|0.982|0.786|0.865|
|S&P 500|p .|Edge|0.982|0.783|0.862|
||GPT-54-mini|<sup>Node</sup>|0.975|0.697|0.786|
||.|<br>Edge|0.973|0.728|0.805|



**Table 7: Human audit of short-term fusion on final-period investor-call data using Opus 4.6. Precision uses final judgments after disagreement resolution. The final row is a subset of the 300 Full outputs and is included in the Full result.** 

|**Condition / output subset**|**Audited**<br>**cases**|**Human-audit**<br>**fusion precision**|
|---|---|---|
|Direct fusion (Rule 3)|200|99.0% (198/200)|
|Full fusion (Rules 3+4)|300|97.7% (293/300)|
|Added by Rule 4 beyond Rule 3|94|96.8% (91/94)|



# **4.5 Human Audit of Short-Term Fusion** 

The preceding evaluations assess identity continuity, source faithfulness, and content preservation. We now examine whether evidence from investor calls and cash-flow records supports the product corroborations produced by short-term fusion. 

We audited final-period investor-call data using Opus 4.6. Log records were deduplicated by investor, product, and period, retaining their evidence references. We randomly sampled 200 relationships triggering Rule 3 and separately sampled 300 relationships triggering Rule 3 or Rule 4, without replacement within each respective population. Within the Full sample, log tags identified the subset triggering Rule 4 but not Rule 3. Two annotators independently reviewed all sampled relationships. 

A correct corroboration required evidence from the same investor and period, correct product alignment, and an eligible cashflow signal. Transcript evidence had to support discussion of that product for Rule 3, or an appropriately linked ontology topic for Rule 4. Fusion precision was the proportion of reviewed relationships with a valid evidence path under the evaluated rule set, using final judgments after disagreement resolution. Appendix H.1 provides annotation instructions and a VTEB disagreement illustrating resolution through the rule criteria. 

Table 7 reports human-audit precision of 99.0% for Direct fusion and 97.7% for Full fusion. Within the Full sample, 94 of 300 relationships (31.3%) triggered Rule 4 without triggering Rule 3. Of these, 91 were judged correct, yielding a precision of 96.8%. Together, these findings support high precision for both direct and ontology-mediated corroboration in the audited setting. 

# **5 Discussion** 

Correct registry reattachments extend one cumulative evidence history rather than create duplicate _Emerging_ edges. FIRME’s higher CMR indicates that a larger fraction of incoming edges is judged to be correctly reattached to prior memory. MMR describes reattachment frequency, while Merge Precision measures accepted-link correctness. Accepted registry matches add their surface forms to the selected anchor’s persistent alias set; an incorrect registry match can therefore route later occurrences to the wrong anchor and history. Merge Precision therefore remains important alongside CMR when assessing incorrect reattachments. 

# **5.1 Lifecycle Behavior Over Time** 

Figure 4 shows observed Market Volatility activity rising and then subsiding. Under Eqs. (2)–(3) and the lifecycle definitions in Section 3.4, consecutive unmatched periods shift accumulated memory from _Emerging_ toward _Stable_ and _Fading_ ; no _Reactivated_ share appears in the observed window. These states reflect observed evidence rather than latent investor preference. 

# **5.2 Analytical Parameter Behavior** 

Table 8 reports analytical, not empirical, sensitivity. Parameter 𝛼 sets saturation speed; 𝛾 sets the decay rate. Decay begins with the first miss, whereas 𝑁 sets a separate threshold for _Fading_ . Under the defaults, an edge starting at 0.5 saturates after three consecutive matches and retains 51% of its pre-decay score after three consecutive misses. Periods are monthly for investor calls but reporting-period-based for S&P 500, so identical parameters span different calendar durations. 

**Table 8: Analytical effects of** 𝛼 **and** 𝛾 **across low, default, and high settings; bold marks defaults.** 

|**Parameter / behavior**|**Low**|**Default**|**High**|
|---|---|---|---|
|Reinforcement𝛼|0.1|**0.2**|0.3|
|Matched periods to reach1.0|5|**3**|2|
|Retention𝛾<br>t|0.7|**0.8**|0.9|
|% retained after 3 periods|34|**51**|73|



# **6 Conclusion and Future Work** 

We introduced FIRME, a registry-anchored memory-graph framework for heterogeneous, time-varying investor evidence. Withinperiod ontology-mediated fusion combines document-derived and structured evidence with provenance. Cross-period registry reconciliation maps surface variants to canonical relationships, allowing evidence to accumulate in one history through deterministic lifecycle updates. Under the judge and fallback-review protocol, FIRME increased CMR over the no-alias control by 7.8–12.1 percentage points and achieved 2.3–3.7 times LLM-Norm’s CMR. The shared human audit found CMR gains of 9.0–16.5 points and reattachment-recall gains of 22.5–29.0 points over the no-alias control, with higher observed merge precision in all four samples. Results support persistent identity for auditable evidence trajectories, not latent investor preference. 

9


<!-- page 10 -->

Zhang, Gao, and Shiao 



<!-- Start of picture text -->
Market Volatility Emerging Reinforced Reactivated Stable Fading<br>100%<br>400<br>50%<br>200<br>0 0%<br>Nov Dec Jan Feb Mar Apr May Jun Jul Aug Nov Dec Jan Feb Mar Apr May Jun Jul Aug<br>Observed investors<br><!-- End of picture text -->

**Figure 4: Market Volatility topic group in the investor-call corpus, November 2024–August 2025: monthly observed investors (left) and lifecycle-state shares over accumulated memory edges (right).** 

Future work should learn entity- and relation-specific decay, incorporate negative signals (outflows and dissatisfaction), support firm-level aggregation, and test longer windows, more backends, and independent judges and generators. 

# **7 Limitations** 

FIRME’s lifecycle model is implemented as a deterministic state machine. Given reconciliation decisions, its memory-strength score and lifecycle state follow fixed, evidence-grounded updates; extraction and semantic matching remain model-dependent. The alias-memory ablation evaluates persistent aliases as a combined mechanism, but does not separately quantify the effects of canonical registry state and semantic fallback. 

The proprietary investor-call corpus and the internal productannotation resource underlying the ontology are not publicly available, limiting independent reproduction of the corresponding experiments. The S&P 500 corpus contains transcripts for 297 sampled companies across three reporting periods but no paired structured cash-flow records. It therefore tests extraction and temporal reconciliation, not the full heterogeneous-fusion path. Neither window spans an annual cycle, limiting longer-term seasonality and lifecycle conclusions. 

The human audit estimates reattachment recall for sampled incoming units against an adjudicated historical reference; a complete population reference remains unavailable. It is conditional on each backend’s extracted observation stream and does not measure extraction recall or relationships omitted during extraction from the original calls. Estimates remain subject to sampling uncertainty and errors in historical search or reference labeling. The confidence intervals quantify sampling uncertainty conditional on the final reference. 

The product–topic ontology, $100K threshold, and lifecycle parameters are use-case specific; uniform reinforcement ignores relation type and evidence intensity. At memory update, an edge is unmatched when no current observation is successfully extracted, registry-normalized, and linked to it. This may reflect reduced engagement, missing inputs, or no observation opportunity, which the model cannot distinguish. 

Two backends limit model-level generalization. Using Gemini 3.1 Pro as the fixed judge keeps the evaluator constant while the extractor varies. The manual fallback review and human audit may retain annotator subjectivity. The Gemini 3.1 Pro judge is separate from the Opus 4.6 extractor, although reliance on a single LLM judge may introduce evaluator-specific bias. Opus 4.6 also generated all round-trip documents; sharing them controls input variation, although generator–extractor affinity may remain.
