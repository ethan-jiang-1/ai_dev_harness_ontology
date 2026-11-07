---
source: 2610.40482-firme.pdf
part: appendix
converted: 2026-11-07
converter: pymupdf4llm
---

# FIRME: Registry-Anchored Memory Graphs for Evolving, Heterogeneous Investor Knowledge · 附录

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

# **Appendix** 

# **A Human Audit of Relationship Reattachment** 

_Sampling and historical reference._ For each dataset–backend setting, we sampled 200 final-period incoming relationship units uniformly without replacement from the complete incoming population, including units left unmatched by the strategies. Each incoming observation counted as one unit; observations were not deduplicated for evaluation. Multiple observations could originate from the same call. All five strategies shared the sampled units and reference within a setting. RAW and spaCy-Lemma predictions were scored against the existing frozen reference without repeating annotation. Extracted streams and sampled units could differ between Opus 4.6 and GPT-5.4-mini. 

Two annotators independently reviewed all 800 units, yielding 1,600 initial reviews. Each of the two primary annotators spent approximately 65 hours on annotation. They inspected incoming source evidence and searched historical relationship observations and supporting evidence available through 𝑇−1. The eligible history and identity criteria were shared across strategies. Historical search extended beyond strategy-proposed candidates. Annotators were blinded to strategy predictions, automated judgments, and each other’s initial labels. 

_Evidence-aware labels._ Each unit received a MATCH, NEW, or UNRESOLVED label. MATCH required an evidence-supported 

historical relationship with the same head and typed target identity. Supported aliases and synonymous expressions could identify the same target; relationship-label differences alone did not establish different identities. NEW required a search of eligible history that found no corresponding relationship. Insufficient evidence led to UNRESOLVED. Annotation records linked incoming units and historical counterparts to witness edges, call identifiers, turn identifiers or stable source locators, supporting excerpts, and a short rationale. 

_Independent agreement and adjudication._ Initial labels were preserved before discussion. Substantive agreement required both annotators to select NEW or MATCH to the same historical identity. Different valid evidence passages supporting that identity counted as agreement. Different decisions or identities, initial uncertainty, and insufficient supporting evidence entered resolution. The two annotators discussed these cases using their evidence records; a third annotator adjudicated remaining disagreements. Agreement was computed from independent initial annotations, and strategy performance used the final adjudicated reference. Initial substantive agreement was 704/800 (88.0%); 22 of the 96 cases requiring resolution received third-person review. All final labels were resolved (Table A1). 

**Table A1: Human-audit annotation agreement and reference composition. Each setting contains 200 units. Agreement precedes discussion; third-person reviews are a subset of cases requiring resolution.** 

|**Setting**|**Initial substantive**<br>**agreement**|**Cases requiring**<br>**resolution**|**Third-person**<br>**reviews**|**Final recurring /**<br>**new / unresolved**|
|---|---|---|---|---|
|Investor×Opus 4.6|176/200 (88.0%)|24|6|80 / 120 / 0|
|Investor×GPT-5.4-mini|172/200 (86.0%)|28|7|80 / 120 / 0|
|S&P 500×Opus 4.6|182/200 (91.0%)|18|4|130 / 70 / 0|
|S&P 500×GPT-5.4-mini|174/200 (87.0%)|26|5|100 / 100 / 0|
|**Total**|**704/800 (88.0%)**|**96**|**22**|**390 / 410 / 0**|



12


<!-- page 13 -->

FIRME: Registry-Anchored Memory Graphs for Evolving, Heterogeneous Investor Knowledge 

_Performance measures and uncertainty._ A reattachment was correct when its historical relationship identity matched the adjudicated reference. Human-audit CMR divides correct reattachments by all 200 sampled incoming units. Human-audit merge precision divides by accepted reattachments; human-audit reattachment recall divides by gold recurring units. A recurring unit attached to the wrong historical identity counts as both an incorrect accepted reattachment and a failure to recover the correct relationship. A new unit correctly left unmatched does not count as a correct reattachment. Human-audit F1 is the harmonic mean of precision and recall, 2𝑃𝑅/(𝑃+ 𝑅), using unrounded values from the same adjudicated reference. 

Table A2 reports CMR, precision, and recall with two-sided Wilson 95% confidence intervals using each metric’s denominator; F1 is reported as a point estimate. These pointwise intervals use a binomial approximation to random incoming-unit sampling without finite-population correction, conditional on the adjudicated 

reference. No units were excluded for unresolved final labels. Reattachment recall is conditional on the extracted streams and eligible history; extraction recall over the original transcripts is outside this audit’s scope. 

_Connection to Table 3._ RAW and spaCy-Lemma human-audit precision also supplies their Table 3 precision entries. Their CMR there multiplies the reported population MMR by this precision; Table A2 computes human-audit CMR directly as correct reattachments divided by 200. The former uses population acceptance rates and the latter uses sample acceptance rates, so their CMR estimates can differ. Baseline precision estimates use 12–51 accepted cases per setting, with uncertainty reported below. 

_F1 comparison._ Full FIRME achieved the highest observed human-audit F1 in every setting (76.4–92.7%), exceeding FIRME w/o Alias Memory by 17.2–20.5 percentage points. 

**Table A2: Human-audit performance on 200 shared incoming units per setting. Gold recurring counts are shared across strategies; accepted and correct reattachments are strategy-specific. All metrics are percentages; brackets give Wilson 95% confidence intervals for CMR, precision, and recall. F1 is a point estimate. Bold marks the highest CMR, recall, and F1 within each setting.** 

|**Dataset**×<br>**backend**|**Strategy**|**Gold**<br>**recurring**<br>**Ac**<br>**rea**|**cepted**<br>**ttach.**<br>**Co**<br>**rea**|**rrect**<br>**ttach.**|**Human-audit**<br>**CMR**|**Human-audit**<br>**merge precision**|**Human-audit**<br>**reattachment recall**|**F1**|
|---|---|---|---|---|---|---|---|---|
||RAW|80|12|12|6.0 [3.5, 10.2]|100.0 [75.8, 100.0]|15.0 [8.8, 24.4]|26.1|
||spaCy-Lemma|80|17|16|8.0 [5.0, 12.6]|94.1 [73.0, 99.0]|20.0 [12.7, 30.0]|33.0|
|Investor×<br>Opus 4.6|LLM-Norm<br>FIRME w/o|80|17|16|8.0 [5.0, 12.6]|94.1 [73.0, 99.0]|20.0 [12.7, 30.0]|33.0|
||Alias Memory|80|48|42|21.0 [15.9, 27.2]|87.5 [75.3, 94.1]|52.5 [41.7, 63.1]|65.6|
||**Full FIRME**|80|64|62|**31.0 [25.0, 37.7]**|96.9 [89.3, 99.1]|**77.5 [67.2, 85.3]**|**86.1**|
||RAW|80|12|12|6.0 [3.5, 10.2]|100.0 [75.8, 100.0]|15.0 [8.8, 24.4]|26.1|
||spaCy-Lemma|80|13|13|6.5 [3.8, 10.8]|100.0 [77.2, 100.0]|16.3 [9.7, 25.8]|28.0|
|Investor×<br>GPT-5.4-mini|LLM-Norm<br>FIRME w/o|80|18|16|8.0 [5.0, 12.6]|88.9 [67.2, 96.9]|20.0 [12.7, 30.0]|32.7|
||<br>Alias Memory|80|45|37|18.5 [13.7, 24.5]|82.2 [68.7, 90.7]|46.3 [35.7, 57.1]|59.2|
||**Full FIRME**|80|64|55|**27.5 [21.8, 34.1]**|85.9 [75.4, 92.4]|**68.8 [57.9, 77.8]**|**76.4**|
||RAW|130|28|28|14.0 [9.9, 19.5]|100.0 [87.9, 100.0]|21.5 [15.3, 29.4]|35.4|
||spaCy-Lemma|130|51|50|25.0 [19.5, 31.4]|98.0 [89.7, 99.7]|38.5 [30.5, 47.0]|55.2|
|S&P 500×<br>Opus 4.6|LLM-Norm<br>FIRME w/o|130|48|47|23.5 [18.2, 29.8]|97.9 [89.1, 99.6]|36.2 [28.4, 44.7]|52.8|
||Alias Memory|130|88|82|41.0 [34.4, 47.9]|93.2 [85.9, 96.8]|63.1 [54.5, 70.9]|75.2|
||**Full FIRME**|130|118|115|**57.5 [50.6, 64.1]**|97.5 [92.8, 99.1]|**88.5 [81.8, 92.9]**|**92.7**|
||RAW|100|21|21|10.5 [7.0, 15.5]|100.0 [84.5, 100.0]|21.0 [14.2, 30.0]|34.7|
||spaCy-Lemma|100|33|32|16.0 [11.6, 21.7]|97.0 [84.7, 99.5]|32.0 [23.7, 41.7]|48.1|
|S&P 500×<br>GPT-5.4-mini|LLM-Norm<br>FIRME w/o|100|32|30|15.0 [10.7, 20.6]|93.8 [79.9, 98.3]|30.0 [21.9, 39.6]|45.5|
||<br>Alias Memory|100|57|48|24.0 [18.6, 30.4]|84.2 [72.6, 91.5]|48.0 [38.5, 57.7]|61.1|
||**Full FIRME**|100|90|77|**38.5 [32.0, 45.4]**|85.6 [76.8, 91.4]|**77.0 [67.8, 84.2]**|**81.1**|



13


<!-- page 14 -->

Zhang, Gao, and Shiao 

# **B Reconciliation Strategies and Alias-Memory Control** 

Table B1 summarizes the three strategies used to interpret the contribution of persistent alias memory. FIRME w/o Alias Memory retains historical canonical identities and cross-period semantic fallback, so its comparison with full FIRME evaluates the incremental contribution of alias memory beyond canonical-only historical reconciliation. 

**Table B1: Reconciliation capabilities and comparison roles. Historical registry use refers to resolving incoming names against existing canonical identities; LLM-Norm can still reattach equal normalized names or identifiers through deterministic matching.** 

|**Strategy**|**Brief description**|**Historical registry used**<br>**during reconciliation**|**Learned alias**<br>**memory**|**Cross-period**<br>**semantic**<br>**fallback**|**Role in the comparison**|
|---|---|---|---|---|---|
|LLM-Norm|Independent within-period<br>semantic normalization|No|No|No|Reference for independent<br>normalization|
|FIRME w/o Alias<br>Memory|Canonical registry with<br>deterministic and semantic<br>matching, without alias<br>memory|Yes; canonical IDs and<br>names|No|Yes|Controls for historical<br>reconciliation and semantic<br>fallback while removing alias<br>memory|
|Full FIRME|Registry reconciliation with<br>persistent alias reuse|Yes; canonical IDs, names,<br>and aliases|Yes|Yes|Evaluates the incremental<br>contribution of alias memory<br>relative to the no-alias control|



The no-alias control disables learned-alias accumulation, deterministic alias lookup, and alias information in semantic candidate descriptions. Both FIRME variants retain cross-period semantic fallback and maintain their own evolving registries over the same period sequence, with the same incoming observations, backend, matching threshold, and fusion rules. The no-alias registry retains accepted canonical assignments but does not accumulate their alternative names. LLM-Norm can still reattach equal normalized names or identifiers through deterministic matching; it does not use historical canonical identities to resolve incoming names. 

14


<!-- page 15 -->

FIRME: Registry-Anchored Memory Graphs for Evolving, Heterogeneous Investor Knowledge 

# **C Cross-Period Entity Reconciliation Pseudocode** 

The procedure below updates the entity registry for 𝑡≥1, after within-period fusion. The first period establishes the registry; subsequent periods reconcile incoming entities against the prior registry. Candidates include all original target entities retained in 𝑆<sup>𝑡</sup> , including topic antecedents used by Rule 4. **Initialization:** Set 𝑅<sup>0</sup> = ∅ before processing the first period. **Input:** Incoming graph 𝑆<sup>𝑡</sup> , prior registry 𝑅<sup>𝑡−1</sup> . **Output:** Updated entity registry 𝑅<sup>𝑡</sup> . 

- 1 **if** 𝑡= 1: 

- 2 Initialize 𝑅<sup>1</sup> from deduplicated target entities in 𝑆<sup>1</sup> , retaining their aliases 

- 3 **return** 𝑅<sup>1</sup> 

- 4 𝑅<sup>𝑡</sup> ← copy(𝑅<sup>𝑡−1</sup> ) 

- 5 **for each** distinct target entity 𝑣 in 𝑆<sup>𝑡</sup> : 

- 6 _anchor_ ← deterministic_match(𝑣, 𝑅<sup>𝑡−1</sup> ) 

- 7 **if** no anchor is found: 

- 8 _anchor_ ← semantic_match(𝑣, 𝑅<sup>𝑡−1</sup> ) 

- 9 **if** an anchor is found: 

- 10 Add 𝑣 ’s surface forms to the anchor’s alias set in 𝑅<sup>𝑡</sup> 

- 11 **else** : 

- 12 Register 𝑣 with its original identifier in 𝑅<sup>𝑡</sup> 

- 13 **return** 𝑅<sup>𝑡</sup> 

At 𝑡= 1, deduplication uses lemmatized-name equality, followed by semantic matching for unresolved same-type candidates, as described in Section 2.3. For 𝑡> 1, deterministic matching checks identifiers, normalized names, and learned aliases in sequence, stopping at the first match. Semantic matching considers canonical names and aliases of same-type entities in the prior registry. All matching queries for these subsequent periods read 𝑅<sup>𝑡−1</sup> ; new identities and accepted aliases are written to 𝑅<sup>𝑡</sup> . Matched incoming targets adopt the selected canonical IDs for edge reconciliation; head IDs remain unchanged. 

# **D Exploratory Semantic Threshold Selection** 

_Evaluation setup._ We evaluated all 5,610 distinct entities that remained unresolved after deterministic identifier, normalizedname, and alias matching in the penultimate period (𝑇−1) of the investor-call corpus. The same entity set was evaluated at thresholds of 0.7, 0.8, and 0.9 using Opus 4.6. The LLM scored same-type registry candidates using their canonical names and aliases, following a similarity rubric with worked examples. At each threshold, the rule-based matcher selected the highest-scoring candidate whose score met or exceeded the threshold. 

_Entity match rate._ At each threshold, we calculate the fraction of evaluated unresolved entities accepted by semantic matching: 

## # matched entities 

Entity match rate = 

# evaluated unresolved entities<sup>.</sup> 

_Human-audited precision._ Two annotators independently reviewed accepted semantic matches, each assessing 100 matches per threshold. A match was judged correct when the incoming entity and the selected registry identity denoted the same entity. Each annotator’s precision was the number of correct matches divided by 100. We report the arithmetic mean of the two annotators’ precision estimates. 

**Table D1: Exploratory threshold analysis for semantic entity matching on investor-call data using Opus 4.6. Bold indicates the selected threshold.** 

|**Threshold**|**Entity match rate**|**Mean human-audited**|
|---|---|---|
|||**precision**|
|0.7|41.7%|85.0%|
|**0.8**|**35.5%**|**94.5%**|
|0.9|17.0%|95.5%|



_Threshold selection._ We selected 0.8 to improve precision over 0.7 while retaining more matches than 0.9 (Table D1). 

15


<!-- page 16 -->

Zhang, Gao, and Shiao 

# **E Rule-Based Fusion and Memory Continuity** 

# **E.1 Rule-Based Short-Term Fusion** 

The procedure summarizes all four rules in Table 2 for one period. Product identities are aligned as in Section 3.3, and 𝐺𝑠<sup>𝑡</sup> contains only eligible cash-flow signals. Using the paper’s (𝑢, 𝑟, 𝑣) notation, 𝑢 denotes the investor (head), and 𝑣 denotes the product target in the cash-flow edges below. 

**Input:** 𝐺𝑢<sup>𝑡</sup> , 𝐺𝑠<sup>𝑡</sup> , and ontology 𝑂. **Output:** Fused graph 𝑆<sup>𝑡</sup> . 

- 1 𝑆<sup>𝑡</sup> ← retain_and_group(𝐺𝑢<sup>𝑡</sup> ∪𝐺𝑠<sup>𝑡</sup> ) 

- 2 **for each** distinct edge (𝑢, cf-signal, 𝑣) ∈𝐺𝑠<sup>𝑡</sup> : 

- 3 **if** Rule 3 or 4 applies to this edge: 

- 4 Label the relationship from 𝑢 to 𝑣 in 𝑆<sup>𝑡</sup> as strong-interest, source 3 

- 5 Reference all matching observations and applicable ontology links 

- 6 **return** 𝑆<sup>𝑡</sup> 

Initialization groups relationships by investor and typed target, retaining each original observation once with its target, relation, source, and provenance. All matches of Rules 3–4 are evaluated against the unchanged current-period inputs; upgrades affect only the derived product label and source indicator. Supporting observations are referenced without being consumed or copied. Topic relationships and uncorroborated product relationships retain their original labels. 

# **E.2 Topic and Product Histories Across Periods** 

Emma discusses Tax Efficiency in three successive periods. In the second period, she also has an eligible cash-flow signal for VTEB, which the ontology links to Tax Efficiency. Rule 4 assigns strong-interest to the VTEB relationship while retaining discussed for the topic. Table E1 illustrates the deterministic memory updates; it is not a measured investor trajectory. 

**Table E1: Illustrative continuity of Emma’s topic and product histories. Memory columns report score and lifecycle state. Each relationship receives one update per period; a new relationship is initialized without an additional reinforcement.** 

|**Period**|**Current observations**|**Topic memory**|**VTEB memory**|
|---|---|---|---|
|1|Topic Obs. 1: Tax Efficiency discussion<br>fi|0.50, Emerging|Not yet present|
|2|Topic Obs. 2: Tax Efficiency discussion;<br>l    l|0.70, Reinforced|0.50, Emerging|
||Cash-flow Obs. 1: VTEB inflow|||
|3|Topic Obs. 3: Tax Efficiency discussion|0.90, Reinforced|0.40, Stable|



The topic history retains all three discussion observations. The VTEB history retains the cash-flow observation and a reference to the supporting discussion in Period 2. In Period 3, the topic is reinforced, while VTEB decays because it has no new observation. Historical support remains retrievable but does not trigger another update. 

If one discussion corroborates several allocated products, each product references the same discussion. The topic history and each observed product history are updated once per period, regardless of the number of support paths. This also applies when Rules 3 and 4 both support the same product. An ontology link alone creates no topic observation: without a current topic discussion, a cash-flow signal does not trigger Rule 4 or reinforce that topic. 

**Table E2: Illustrative memory-strength updates with initialization** 0.50 **, reinforcement** 0.20 **, retention** 0.80 **, and inactivity threshold** 𝑁= 3 **. Step 0 denotes this relationship’s initialization, not global period 0. Reinforcement is capped at** 1.00 **.** 

|**Step**|**Event**|**Calculation**|**Score**|**Memory state**|
|---|---|---|---|---|
|0|New|Initialization|0.50|Emerging|
|1|Matched|0.50 + 0.20|0.70|Reinforced|
|2|Matched|0.70 + 0.20|0.90|Reinforced|
|3|Matched|min(1.00, 0.90 + 0.20)|1.00|Reinforced|
|4|Unmatched|1.00 × 0.80|0.80|Stable|
|5|Unmatched|0.80 × 0.80|0.64|Stable|
|6|Matched|0.64 + 0.20|0.84|Reinforced|



16


<!-- page 17 -->

FIRME: Registry-Anchored Memory Graphs for Evolving, Heterogeneous Investor Knowledge 

# **F System Prompts** 

# **F.1 Relationship Extraction** 

Both investor-call prompt listings replace legacy advisor wording and role labels with investor, referring to the same business entity and identifier. The extraction prompt below describes the investor-call schema; the S&P 500 extraction uses a broader entity-type schema. 

You are a financial domain relationship extractor. Extract relationships between an investor and products/topics substantively discussed in a call. 

For each extracted relationship, return two linked layers: - Raw: source evidence and mention metadata. - Canonical: normalized fields for graph construction. 

Raw layer: - raw_subject: the speaker who mentioned the entity. - raw_relation: the exact relation phrase from the transcript. - raw_object: the exact entity mention, copied unchanged from the transcript. - speaker_role: e.g. "investor" or "crew". - mention_origin: e.g. "investor_proactive", "investor_responsive", or "crew_introduced". - evidence_text: a contiguous, verbatim transcript excerpt containing raw_object. - turn_ids: the source turn IDs. - confidence: extraction confidence between 0.0 and 1.0. 

Canonical layer: - subject_entity_id: the investor's stable entity ID, regardless of speaker. - relation_type: "DISCUSSED". - object_entity_name: the normalized/canonical entity name. - object_entity_type: "product" or "topic". - entity_match_status: "known" or "unknown". Rules: - Extract only from the transcript. Do not infer relationships from general knowledge. - Preserve raw_relation, raw_object, and evidence_text verbatim. Do not correct grammar, expand abbreviations, or reword them. - Unknown entities should still be extracted. - Return valid JSON only. Output format: { "relationships": [ { "raw": { "raw_subject": "...", "raw_relation": "...", "raw_object": "...", "speaker_role": "investor", "mention_origin": "investor_proactive", "evidence_text": "...", "turn_ids": [1], "confidence": 0.0 }, "canonical": { "subject_entity_id": "...", "relation_type": "DISCUSSED", "object_entity_name": "...", "object_entity_type": "topic", "entity_match_status": "known" } } ] } 

17


<!-- page 18 -->

Zhang, Gao, and Shiao 

# **F.2 Semantic Entity Matching** 

The following system prompt was used for semantic entity matching by full FIRME in the investor-call experiments. A similar prompt with minor adaptations was used for the S&P 500 experiments. It is applied only to incoming entities that remain unresolved after deterministic matching. The LLM scores all supplied same-type registry candidates using their canonical names and aliases. For FIRME w/o Alias Memory, candidate descriptions omit alias information, as specified in Appendix B. Thresholding, highest-score selection, and canonical-ID assignment are performed programmatically as described in Section 3.4. 

You are a knowledge graph entity matcher for investor interest tracking. 

## Input: 

You are given a batch of short-term edges and their associated same-type registry candidates. Each registry candidate includes a canonical ID, a canonical name, and aliases. 

For each incoming target entity from the short-term edges, score its semantic similarity to every supplied same-type registry candidate using the candidate's canonical name and aliases. 

## Scoring: 

- 1.0: Same entity or concept. 

- 0.8 <= score < 1.0: Likely the same entity or concept. 

- 0.5 <= score < 0.8: Related but distinct. 

- 0.0 <= score < 0.5: Different meanings. 

## Examples: 

- "Municipal Bonds" and "Muni Bond": equivalent entities (0.9+). 

- "Tax-Free product" and "Tax-Exempt product": closely related concepts (0.8+). 

- "Fixed Income" and "Growth Equities": distinct concepts (0.2). 

## Output format: 

Return only JSON keyed by incoming entity name. Each value must list all supplied candidates, with one numeric score per candidate. Always return the candidate's canonical name and canonical ID exactly as provided, including when similarity is established through an alias. 

Example output: 

{ "Municipal Bonds": [ { "memory_entity": "Muni Bond", "memory_entity_id": "XXXX", "similarity_score": 1.0 } ] } 

18


<!-- page 19 -->

FIRME: Registry-Anchored Memory Graphs for Evolving, Heterogeneous Investor Knowledge 

# **G Product–Topic Ontology: Representation and Use** 

The ontology is derived from a proprietary internal resource manually annotated by our financial analyst team and covering approximately 17,000 unique financial products. This resource is not publicly available. For the investor-call use case, we extracted the relevant product– topic associations from this broader resource; selected records are shown below. 

We use a fixed product–topic ontology 𝑂 as background domain knowledge for short-term fusion. In this work, 𝑂 denotes a lightweight set of associations between financial products and investment topics. A link (𝑝, 𝑡) ∈𝑂 indicates that product 𝑝 is associated with topic 𝑡. A product may be associated with multiple topics, and a topic may be associated with multiple products. These associations express topical relevance rather than entity equivalence. 

[ { "product_id": "VFIAX", "product_name": "Vanguard 500 Index Fund Admiral Shares", "product_category": "Large Blend", "topic_name": [ "Passive / Index Investing", "Large Cap" ], "relation": "RELATED_TO" }, { "product_id": "VTIP", "product_name": "Vanguard Short-Term Inflation-Protected Securities ETF", "product_category": "Short-Term Inflation-Protected Bond", "topic_name": [ "Fixed Income", "Inflation-Protected Bond / TIPS", "Short Duration / Short End of Curve" ], "relation": "RELATED_TO" }, { "product_id": "VGT", "product_name": "Vanguard Information Technology ETF", "product_category": "Technology", "topic_name": [ "Tech Stocks", "Sector Funds", "Passive / Index Investing" ], "relation": "RELATED_TO" } ] 

Under Rule 4, these associations connect topic-level discussion with product-level cash-flow evidence. For example, suppose an investor discusses Large Cap and has an eligible cash-flow signal for VFIAX in the same period. Because (VFIAX, Large Cap) ∈𝑂, the discussion corroborates the product allocation. FIRME labels the investor–VFIAX relationship as strong-interest while retaining the investor–Large Cap relationship as discussed. An ontology link alone does not constitute an investor observation or trigger this upgrade. 

19


<!-- page 20 -->

Zhang, Gao, and Shiao 

# **H Additional Evaluation Details** 

_Population judge and human fallback._ For each accepted reattachment, the judge received the incoming relationship and its source evidence, together with the selected historical relationship and supporting evidence available through 𝑇−1. Correctness required the same head and typed target identity. Two annotators reviewed cases initially judged incorrect; disagreements were resolved through evidence-based discussion, and the resulting human label replaced the initial judgment. 

_GraphRAG adapter._ The GraphRAG adapter retained relationship-level raw mentions, normalized targets, and candidate evidence excerpts from the extraction outputs. Text-unit identifiers located the original source passages, against which the candidate evidence and mentions were checked. Normalization was assessed on the corresponding raw-to-normalized target pairs. 

_Round-trip matching and scoring._ Nodes were matched one-toone using entity type and normalized-name equality under a fixed normalization rule. An edge matched only when its aligned endpoints, relation type, and direction matched the reference edge. For each sampled instance, let 𝑛ref and 𝑛rec count reference and recovered items, respectively, and let 𝑛match count matched items. Let 𝑛extra count otherwise unmatched recovered items judged by Gemini 3.1 Pro to be explicitly supported by the generated document. At each of the node and edge levels, 



<!-- Start of picture text -->
𝑃adj = 𝑛match + 𝑛extra ,<br>𝑛rec<br>𝑅= 𝑛match ,<br>𝑛ref<br>2𝑃adj𝑅<br>𝐹1 =<br>𝑃adj + 𝑅 .<br><!-- End of picture text -->

Grounded extra items contribute to adjusted precision but do not count as recovered reference items. We calculate each metric per sampled instance and then macro-average it separately across instances. 

# **H.1 Short-Term Fusion Annotation** 

_Annotation instructions._ The review unit was an investor– product–period relationship, together with its retained transcript evidence, structured cash-flow records, and any cited product– topic ontology entry. Reviewers checked three aspects: investor, product, and period alignment; source support for the discussion and eligible cash-flow signal; and justification under the applicable fusion rule. Rule 3 required discussion of the same product as the cash-flow signal. Rule 4 required discussion of a topic appropriately associated with that product in the frozen ontology. Direct outputs required a valid Rule 3 path; Full outputs required at least one valid Rule 3 or Rule 4 path. Correctness therefore concerned the evidence supporting the corroborated relationship. 

Two annotators independently assessed every relationship in both samples. The reported counts reflect their final judgments after disagreement resolution. 

_Disagreement resolution: a VTEB case._ One disagreement concerned an investor–VTEB relationship. Annotator A judged the corroboration correct because the topic discussion, ontology link to VTEB, and eligible cash-flow signal aligned. Annotator B judged it incorrect because the transcript did not directly mention VTEB. The annotators revisited the evidence and Rule 4 criteria. Because Rule 4 permits corroboration through a topic–product association, a direct product mention was not required. The relationship was therefore resolved as correct. This case illustrates how the rule criteria guided resolution of a disputed judgment. 

20
