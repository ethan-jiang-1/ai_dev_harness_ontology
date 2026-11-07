---
source: 2611.03743-evomemstate.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# EvoMemState: Evolving Memory State for Personal Agents · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

# **EvoMemState: Evolving Memory State for Personal Agents** 

**Zhishang Xiang**<sup>1*</sup> **, Yunbo Tang**<sup>1*</sup> **, Zhongqiao Liu**<sup>2</sup> **, Junkai Chen**<sup>1</sup> **, Zerui Chen**<sup>1</sup> **, Qingguo Hu**<sup>1</sup> , **Yuxuan Zhang**<sup>3</sup> , **William Grant**<sup>4</sup> , **Qinggang Zhang**<sup>5†</sup> , **Jinsong Su**<sup>1†</sup> 

1Xiamen University 

2Nanyang Technological University 

3University of British Columbia 4University of Waterloo 5Jilin University 

{xiangzhishang,tangyunbo}@stu.xmu.edu.cn qinggangzhang@jlu.edu.cn jssu@xmu.edu.cn 

## **Abstract** 

Long-term memory enables large language model (LLM) agents to provide continuous personalized assistance by retaining user information across interactions. Existing systems support this process through fact extraction, organization, updating, and retrieval, but largely maintain memories as independent facts. This factcentric paradigm may overlook how new facts update, constrain, or conflict with earlier ones, while leaving their applicability, role, and priority for the current request implicit. In this paper, we introduce **EvoMemState** , a state-centric framework that augments persistent facts with two complementary states: Relational States that capture how facts remain valid and relate to one another as memory evolves, and a Reasoning State that determines how these facts should be applied to the current request. Specifically, EVOMEMSTATE consists of three key components: (i) Ontology-Guided Memory State Induction extracts Persistent Facts and constructs Relational States that maintain their validity, scope, and evolving relations. (ii) RL-Based State Evolution internalizes memory-use experience into a policy through reinforcement learning to generate a request-specific Reasoning State. (iii) State-Aware Reasoning then combines the relevant facts with their Relational States and the generated Reasoning State to guide the personal agent. Extensive experiments on long-term dialogue and memory-use benchmarks demonstrate consistent improvements over existing memory systems in retrieval completeness and memory-grounded response accuracy. Our code and implementation details are available at https://github.com/ XMUDeepLIT/EvoMemState.git. 

## **1 Introduction** 

Large language model (LLM) agents are increasingly used as personal agents that assist users over 

> *Equal contribution. 

> †Corresponding authors. 

extended periods, requiring continuity across interactions and adaptation to evolving needs (Westhäußer et al., 2025; Zhang et al., 2025b; Hu et al., 2025; Feng et al., 2026). Long-term memory supports this continuity by preserving user preferences, experiences, circumstances, and constraints across sessions (Li et al., 2026; Du et al., 2025; Ning et al., 2026; Yang et al., 2026a). This accumulated context provides a foundation for consistent and personalized assistance over time (Wang et al., 2026b; Zhang et al., 2026b). 

Recent work has explored how to construct and maintain long-term personal memory from interaction histories. MemoryBank (Zhong et al., 2024) summarizes user experiences for subsequent retrieval, while MemGPT (Packer et al., 2023) manages memory across storage tiers. LightMem (Fang et al., 2026) improves efficiency through compression and selective retrieval. Other systems emphasize memory organization and maintenance: Mem0 (Chhikara et al., 2025) extracts and updates atomic facts, A-MEM (Xu et al., 2026) dynamically associates related memories, and Supermemory (Supermemory AI, 2026) and SimpleMem (Liu et al., 2026) support continual updates and memory lifecycle management. Together, these approaches enable personal agents to retain and access information across interactions through memory extraction, organization, updating, and retrieval. 

Despite this progress, existing memory systems largely follow a **fact-centric paradigm** , focusing on the storage, updating, and retrieval of factual records. However, the validity and scope of a stored fact may change as related memories accumulate, while its appropriate use depends on the current request. Associating records or revising their contents alone may not adequately capture these dependencies. When memories are maintained or retrieved separately, conflicts between them may be overlooked, leaving individually accurate records without the context needed for correct 

1


<!-- page 2 -->

<!-- Start of picture text -->
(a) Memory-centric<br>e Dialogue Factual c Retrieved — Personal 3-8<br>history Memories Memories agent Response<br>(b) State-centric<br>Memory = Fact + State<br>Fact State<br>+<br>Relational Reasoning<br>Dialogue Personal state state Personal<br>Response<br>history Ontology agent<br><!-- End of picture text -->

Figure 1: Memory-centric and state-centric paradigms. Our retrieval preserves updates and conflicts, while generated reasoning states specify memory applicability, role, and priority for the current request. 

interpretation. Even when all relevant memories are retrieved, the personal agent must still determine their applicability and priority for the current request and may rely on outdated information or mishandle conflicts. These limitations motivate a **state-centric paradigm** that augments stored facts with evolving memory states. A memory state describes the status of stored facts and their roles in an interaction, which cannot be determined from factual content alone and must be considered in relation to other memories and the current request. Such states make the validity, scope, and relations of facts explicit and guide how retrieved memories should be used for the current request. 

Augmenting personal memory with explicit states presents two challenges: (i) **It is challenging to construct and maintain coherent memory states.** Personal information accumulates across conversations as scattered and inconsistent observations. Simply collecting these observations leaves their relations implicit, while merging them into a summary may lose historical information and hide conflicts between records. The challenge is to organize related facts and maintain their validity, scope, and relations as new information arrives, while preserving the original records. (ii) **It is challenging to learn memory-use strategies from experience.** The same memory can serve different purposes across requests, so its validity and relations alone do not determine how it should affect the agent’s behavior. This requires learning when memories should inform, constrain, or have no bearing on that behavior, using feedback from memory use to refine these judgments. 

To address these challenges, we introduce EVOMEMSTATE, a state-centric framework for maintaining and using long-term personal memory. First, **Ontology-Guided Memory State Induction** extracts Persistent Facts from personal in- 

teractions and incrementally organizes them into a personal memory ontology. It preserves the original facts while maintaining their validity, scope, and evolving relations as Relational States. Second, **RL-Based State Evolution** internalizes memoryuse experience into a policy through reinforcement learning. The learned policy generates a requestspecific Reasoning State that specifies the applicability, role, and priority of relevant facts. Third, **State-Aware Reasoning** combines the relevant Relational States with the generated Reasoning State to guide the personal agent’s response. Together, these components connect fragmented facts through Relational States and combine them with a request-specific Reasoning State, enabling personal agents to interpret and use memory appropriately. Our contributions are summarized as follows: 

- We identify the limitations of fact-centric personal memory: individually maintained facts may lack the relational context needed for interpretation, and complete retrieval does not ensure appropriate memory use. 

- We introduce EVOMEMSTATE, a state-centric long-term memory framework representing personal memory through Persistent Facts, Relational States, and Reasoning State. It realizes this formulation through OntologyGuided Memory State Induction, RL-Based State Evolution, and State-Aware Reasoning. 

- We evaluate EVOMEMSTATE on long-term dialogue and memory-use benchmarks, demonstrating consistent improvements over existing memory systems in retrieval completeness and memory-grounded response accuracy. 

# **2 Preliminary Studies** 

In this section, we conduct two preliminary studies on the Valid Memory Selection subset of MemSyco-Bench (Xiang et al., 2026a), where correct answers require jointly considering memories linked by updates, conflicts, or constraints. Our findings reveal two limitations: related memories are not consistently retrieved together, leaving individual facts without the context needed for correct interpretation; and even when all relevant memories are retrieved, personal agents may misjudge their applicability, roles, and priorities for the current request. A detailed case analysis is provided in Appendix B.5. 

2


<!-- page 3 -->

<!-- Start of picture text -->
Retrieval share (%) Conditional<br>MemGPT acc. (%)<br>57.1<br>13.0 87.0<br>55.6<br>MemoryBank 23.4<br>58.9 38.6<br>55.6<br>MemZero<br>44.6<br>43.3 53.8<br>50.5<br>LightMem<br>38.1<br>61.8 30.2<br>71.4<br>Supermemory 58.7<br>58.0 41.9<br>70.8<br>0 20 40 60 80 100 0 40 80<br>Retrieved incomplete Retrieved complete<br>Neither retrieved<br><!-- End of picture text -->

Figure 2: Retrieval completeness and conditional answer accuracy on the Valid Memory Selection subset of MemSyco-Bench across evaluated systems. 

## **2.1 Do Fact-Centric Systems Capture Relations among Memories?** 

To examine whether fact-centric memory systems capture relations among memories, we evaluate five systems. As shown in Figure 2, MemoryBank, LightMem, and Supermemory do not retrieve all relevant information in 58.9%, 61.8%, and 58.0% of cases, respectively. For four of the five systems, answer accuracy is 5.9–33.3% higher when all required memories are retrieved than when some are missing. These findings motivate explicit modeling of memory relations, so that individual facts can be interpreted alongside the information affecting their validity and scope. 

## **2.2 Can Personal Agents Use Fully Retrieved Memories Appropriately?** 

To examine whether personal agents use memories appropriately when all relevant memories are available, we compare direct reasoning with a fixed selfreflection that asks the agent to reconsider memories before responding. As shown in Figure 3, self-reflection reduces accuracy for most systems, with the largest drop of 1.6% on Mem0, and lowers average accuracy from 50.5% to 48.9%. These results show that access to all relevant memories does not ensure appropriate use, and the fixed reflection prompt offers no consistent improvement. This motivates learning memory-use strategies from experience to determine how memories should be 



<!-- Start of picture text -->
Accuracy (%)<br>0.8 0.4 1.6 0.1 0.1 0.4<br>80 71.4 71.8 70.8 70.4<br>60 50.5 55.6 55.5 55.6 55.7<br>48.9<br>40.9<br>40 40.1<br>20<br>0<br>AMem LightMem MemZero MemGPT MemoryBank Supermemory<br>w/o self-reflection w/ self-reflection<br><!-- End of picture text -->

Figure 3: Effect of fixed self-reflection on answer accuracy when complete memory evidence is available. 

applied and prioritized for each request. 

# **3 Method** 

As illustrated in Figure 4, EvoMemState organizes personal memory around Persistent Facts and two complementary states. **Ontology-Guided Memory State Induction** extracts Persistent Facts from accumulated personal information and constructs Relational States that track their validity, scope, and evolving relations. **RL-Based State Evolution** learns a Memory State Evolution Policy that generates a request-specific Reasoning State from relevant memory evidence. **State-Aware Reasoning** then combines the Relational States and Reasoning State to guide the personal agent. 

## **3.1 System Concepts** 

Let _Ft_ = _{fi}_<sup>_N_</sup> _i_ =1<sup>_t_denote the Persistent Facts accu-</sup> mulated through turn _t_ , and let _qt_ denote the current request. We characterize personal memory using two complementary states; the complete formulation is provided in Appendix B.1. 

**Definition 1 (Relational States).** Each fact _fi_ is associated with a Relational State: 



<!-- Start of picture text -->
ri t = ( f i , a i t, ρt i ) , Rt =  {ri t | f i ∈F t }, (1)<br><!-- End of picture text -->

where _a_<sup>_t_</sup> _i_<sup>specifiesthecurrentvalidityandscope</sup> of _fi_ , and _ρ_<sup>_t_</sup> _i_<sup>records how it updates, conflicts with,</sup> or constrains other facts. Relational States persist across requests and evolve as new conversations update the memory. 

**Definition 2 (Reasoning State).** For request _qt_ , the Reasoning State is inferred from the request, Persistent Facts, and their Relational States: 



<!-- Start of picture text -->
Zqt = Ψ( qt, Ft, Rt ) , (2)<br><!-- End of picture text -->

where _Zqt_ specifies the applicability, role, and priority of memory evidence. The resulting Memory State is _St_ ( _qt_ ) = ( _Rt, Zqt_ ): Relational States represent whether facts remain valid and how they are 

3


<!-- page 4 -->

<!-- Start of picture text -->
Overall Pipeline Retrieval Seed Memories Memory State Evolution Policy<br>Dialogue H Ontology Graph Initial State Reward GRPO Update<br>Travel Reasoning State Computation<br>l M1: historical context<br>l M2: current preference<br>M1 M2 l ……<br>Compute 𝑅! Compute 𝐴!<br>(a) Ontology Guided Memory  (b) RL-Based State Evolution (c) State-Aware Reasoning<br>State Induction “Where should I vacation, and what is my budget?”<br>“I usually prefer hiking when I …” 2025-11-19 “Where should I vacation, and what is my budget?”<br>“I’d like to beach trips because …” 2026-06-23 Memory Evidence  𝑬𝒒<br>M1: hiking M3: $500<br>a QC<br>Extract  M1: hiking  M2: beach  Memory State Evolution Policy Reasoning State<br>atomic memories preference preference Question ll M1: historical contextM2: current preference<br>Organize & Link l M3/M4: unresolved budget but $900 is  Preferences Budget<br>current preference  CONTAINS CONTAINS<br>Ontology memory graph Travel 𝑬𝒒 Trainable Guidance: preference priority<br>CONTAINSPARENT_OF Preferences CONTAINSPARENT_OF Budget ae, Plan around $500 for a “Choose a beach trip. Frozen Personal Agent - Q 𝑈𝒒 M1:hiking (seed) historical ss SUPERSEDEDS M2:beachcurrent M3:$500 (seed) historical CONFLICTWITH M4:$900current<br>short gateway.” 𝑬𝒒<br>Relational State<br>M1:hikinghistorical SUPERSEDEDSConcept Node M2:beachcurrent M3:$500historical Memory NodeCONFLICTWITH M4:$900current —i¢- Internalizing memory application experienceQ Evolution PolicyMemory State  𝑈𝟏 e =)|O With Rule 𝒚𝒘𝒊 Performance Gain  OE Relational State Preferences M1:hikinghistorical SUPERSEDEDS M2:beachcurrent Memory + Directed New Memory + Old New Memory + Old  FI Update<br>Memory metadataType Source TimeStamp 𝑬𝒒 𝑈…𝑮 Without Rule 𝒚𝒘𝒐𝒊 Budget M3:$500historical ReaoningCONFLICT WITHState  M4:$900current Unresolved RelationMemory +  response<br>Scope Validity Relation 𝑅" = 𝑆𝑐𝑜𝑟𝑒 𝑦"#, 𝑦∗ −𝑆𝑐𝑜𝑟𝑒(𝑦"#%, 𝑦∗) GRPO +<br>& ° 6 Yo Becei On-6-& | | 3h eS|<br>a =<br><!-- End of picture text -->

Figure 4: Overview of EvoMemState for personal agents. Ontology-guided induction transforms accumulated personal information into Persistent Facts and Relational States. RL-based state evolution learns a Memory State Evolution Policy from memory-use experience and generates a request-specific Reasoning State. State-Aware Reasoning combines the Relational States and Reasoning State to guide the personal agent’s response. 

related, while the Reasoning State determines how they should be used for the current request. 

# **3.2 Ontology-Guided State Induction** 

Persistent Facts alone are insufficient to construct a memory state because their current meaning depends on their validity, scope, and relations to other facts. Therefore, we construct a personal memory ontology incrementally and induce Relational States from its evolving structure. Persistent Facts retain the original information, while their Relational States are updated as new facts are added. The resulting ontology and Relational States form the persistent personal memory. 

**Iterative ontology construction.** Given the conversations accumulated through turn _t_ , denoted by _Ht_ , we extract a time-ordered set of Persistent Facts: 



<!-- Start of picture text -->
Ft =  {f 1 , . . . , fNt } . (3)<br><!-- End of picture text -->

Each _fi_ contains a single proposition about a user preference, experience, belief, circumstance, or constraint, together with its source and time. Starting from an empty ontology _G_<sup>(0)</sup> , we incorporate each fact in temporal order: 



<!-- Start of picture text -->
G ( i ) = Induce � () G ( i− 1) , fi � , (4)<br><!-- End of picture text -->

# where 



<!-- Start of picture text -->
G ( i ) = VC ( i ) ∪V F ( i ) , E H ( i ) ∪E R ( i ) . (5)<br>� ( � )<br><!-- End of picture text -->

Here, _VC_<sup>(</sup><sup>_i_)</sup> and _VF_<sup>(</sup><sup>_i_)</sup> denote the concept and fact nodes after incorporating _fi_ . The structural edges _E_<sup>(</sup><sup>_i_)</sup> _H_<sup>use PARENT_OF to organize concept nodes hi-</sup> erarchically and CONTAINS to attach each fact to its most specific concept. The CREATE, MERGE, and SPLIT operations revise the concept hierarchy as new facts are added. The relation edges _ER_<sup>(</sup><sup>_i_)</sup> use SUPERSEDES to represent updates and CONFLICTS_WITH to preserve unresolved conflicts. 

**Ontology-induced Relational States.** The Relation State of each fact is derived from its current attributes and ontology relations. After incorporating the first _i_ facts, we define 



<!-- Start of picture text -->
R ( i ) = � f rf ( i ) = � ( f, a ( f i ) , ρ ( f i ) ���� yo f ∈VF ( i )� 4 , (6)<br><!-- End of picture text -->

where _a_<sup>(</sup><sup>_i_)</sup> _f_<sup>describes the current validity and scope</sup> of _f_ , and _ρ_<sup>(</sup> _f_<sup>_i_)contains its concept attachment and</sup> relations to other facts. Later facts may update these attributes and relations without overwriting _f_ . After all facts have been incorporated, we obtain 



<!-- Start of picture text -->
Rt =  R ( Nt ) . (7)<br><!-- End of picture text -->

4


<!-- page 5 -->

The Persistent Facts _Ft_ and Relational States _Rt_ are retained as personal memory and provide the persistent inputs for inferring a Reasoning State for each new user request. 

## **3.3 RL-Based State Evolution** 

Relational States capture how facts currently hold and relate, but do not specify how a personal agent should use them for a particular request. We therefore treat state evolution as the internalization of reusable memory-use experience and instantiate the state inference function Ψ with a Memory State Evolution Policy _πθ_ . Given request _q_ , relevant Persistent Facts _Fq_ , and their Relational States _Rq_ , the policy generates a Reasoning State: 



<!-- Start of picture text -->
Zq ∼ πθ  ( · | q, Fq, Rq )  . (8)<br><!-- End of picture text -->

We train _πθ_ by repeatedly generating and evaluating candidate Reasoning States, allowing the policy to learn reusable patterns of memory use. 

**Evaluating candidate Reasoning States.** A Reasoning State is useful only if it helps the personal agent use the given memory evidence correctly. Let 



<!-- Start of picture text -->
Mq = ( Fq, Rq ) (9)<br><!-- End of picture text -->

denote the relevant memory evidence for request _q_ . Given a candidate Reasoning State _Zq_<sup>(</sup><sup>_i_),we</sup> evaluate its effect on a frozen personal agent _A_ relative to a baseline that receives the same memory evidence without a Reasoning State: 



<!-- Start of picture text -->
Ri = Score A q, Mq, Zq ( i )<br>� � � , y ∗ � (10)<br>− Score ( A  ( q, Mq )  , y ∗ )  ,<br><!-- End of picture text -->

where _y_<sup>_∗_</sup> is the reference answer and Score is the task-specific evaluator. A positive reward indicates that the candidate improves how the personal agent uses the fixed memory evidence, whereas a negative reward penalizes candidates that distort or weaken that evidence. 

**Learning the state evolution policy.** We optimize _πθ_ using GRPO (Shao et al., 2024). For each training instance ( _q, Mq, y_<sup>_∗_</sup> ), we sample _G_ candidate Reasoning States from the previous policy: 



<!-- Start of picture text -->
Zq ( i ) ∼ πθ old ( · | q, Fq, Rq )  , i  = 1 , . . . , G. (11)<br><!-- End of picture text -->

Their relative rewards are normalized within the group to obtain advantages _A_<sup>�</sup> _i_ , which guide the 

policy update: 



<!-- Start of picture text -->
G Ti<br>1<br>L GRPO( θ ) = − G 1 � Ti � min� ρi,jA � i,<br>i =1 j =1<br>(12)<br>clip ( ρi,j,  1  − ϵ,  1 +  ϵ ) A � i �<br>+  β KL D KL ( πθ ∥ π ref )  .<br><!-- End of picture text -->

Here, _Ti_ is the length of candidate _Zq_<sup>(</sup><sup>_i_),</sup><sup>_ρ_</sup> _i,j_<sup>is</sup> the token-level probability ratio between _πθ_ and _πθ_ old, _ϵ_ is the clipping threshold, and _β_ KL controls regularization toward the reference policy _π_ ref . Through repeated optimization, _πθ_ internalizes memory-use patterns that generalize to new facts and requests. Training details are provided in Appendix B.3. 

## **3.4 State-Aware Reasoning** 

At inference, State-Aware Reasoning retrieves the Persistent Facts and Relational States required by the current request, generates a Reasoning State, and grounds the personal agent in both states. 

Given a request _q_ , we retrieve _K_ semantically similar Persistent Facts as seeds. Because a seed may be updated, constrained, or contradicted by other facts, we expand it by traversing the stored memory relations in both directions: 



<!-- Start of picture text -->
Fq = � Traverse ( f, Rt )  . (13)<br>f ∈ Retrievesim( q,Ft,K )<br><!-- End of picture text -->

Here, Traverse( _f, Rt_ ) includes _f_ and all facts connected to it through memory relations. Facts reached from multiple seeds are included only once. We denote the Relational States corresponding to _Fq_ as _R_<sup>�</sup> _q_ . 

The learned policy generates a Reasoning State from the request, retrieved facts, and their Relational States. The personal agent then produces its response using both states: 



<!-- Start of picture text -->
Zq =  πθ q, Fq, R � q ,<br>� �<br>(14)<br>y =  A q, Fq, R � q, Zq .<br>� �<br><!-- End of picture text -->

Together, relation traversal preserves the context needed to interpret the retrieved facts, while the Reasoning State specifies how the personal agent should use them for the current request. 

# **4 Experiment** 

In this section, we evaluate how EvoMemState constructs and applies memory states through the following four research questions. **Q1 (Main Results):** How does EvoMemState compare with 

5


<!-- page 6 -->

|**Memory**<br>**System**||**Mem**|**Syco-B**|**ench**|||**Mem**|**TrapB**|**ench**||**LoC**<br>**Refi**|**oMo-**<br>**ined**|**LoC**|**oMo**|**Overall**<br>**Avg.** _↑_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||WTU<br>Acc. _↑_|WTU<br>Syco. _↓_|HTU<br>Acc. _↑_|HTU<br>Use_↑_|Avg. _↑_|Safety<br>Score_↑_|CogBias<br>Acc. _↑_|Bound.<br>Acc. _↑_|Trauma<br>Acc. _↑_|Avg. _↑_|Judge<br>Score_↑_|Token<br>F1_↑_|Judge<br>Score_↑_|Token<br>F1_↑_||
||||||**Qwen**|**3-8B**||||||||||
|NaiveRAG (Lewis et al.,2020)|36.3|55.3|51.6|64.0|42.4|60.2|63.9|77.0|93.4|73.6|39.0|38.4|34.4|35.8|47.4|
|MemGPT (Packer et al.,2023)|29.0|66.7|54.0|67.0|39.0|62.2|66.0|64.5|52.4|61.3|45.7|40.0|36.8|37.0|45.7|
|MemoryBank (Zhong et al.,2024)|37.5|57.6|54.4|67.1|44.2|64.9|63.7|72.1|82.3|70.7|44.9|44.0|39.9|41.0|49.9|
|Mem0 (Chhikara et al.,2025)|25.9|47.8|52.0|63.8|36.3|56.8|69.3|81.9|85.5|73.4|25.7|26.9|21.4|23.8|39.2|
|A-MEM (Xu et al.,2026)|42.8|49.1|49.2|61.2|45.4|64.2|65.0|77.6|91.8|74.6|41.8|39.1|36.4|37.1|49.6|
|LightMem (Fang et al.,2026)|21.0|49.6|46.1|58.7|31.0|68.6|**69.9**|88.6|91.6|79.7|25.3|27.2|22.1|24.0|39.5|
|Supermemory (Supermemory AI,2026)|23.3|70.5|63.7|74.2|39.5|67.5|65.4|79.6|61.7|68.6|16.6|17.5|15.7|15.8|35.1|
|SimpleMem (Liu et al.,2026)|33.4|58.6|44.1|52.6|37.7|70.9|68.3|84.6|**95.8**|**79.9**|51.3|46.6|45.3|**46.4**|53.6|
|PGMem (Choi et al.,2026)|33.2|62.8|54.5|69.1|41.8|71.0|66.4|85.1|75.6|74.5|28.5|26.9|25.4|25.2|42.6|
|**EvoMemState (Ours)**|**47.7**|**38.0**|**72.4**|**81.3**|**57.6**|**73.8**|62.3|**88.8**|91.4|79.1|**57.4**|**47.3**|**45.5**|41.6|**59.9**|
||||||**GPT-4**|**o-mini**||||||||||
|NaiveRAG (Lewis et al.,2020)|48.3|42.8|49.2|61.1|48.7|61.7|58.6|65.0|**97.4**|70.7|43.2|39.1|34.4|36.9|49.3|
|MemGPT (Packer et al.,2023)|40.8|48.0|56.2|66.0|46.9|66.4|60.7|69.9|62.3|64.8|49.1|39.5|40.2|39.1|50.3|
|MemoryBank (Zhong et al.,2024)|48.9|42.2|48.3|62.3|48.7|66.4|59.8|73.4|90.5|72.5|52.8|46.6|42.7|45.3|54.2|
|Mem0 (Chhikara et al.,2025)|32.7|38.4|50.3|63.3|39.7|56.4|61.7|74.1|93.5|71.4|28.9|27.2|21.6|25.2|40.4|
|A-MEM (Xu et al.,2026)|**54.5**|35.7|50.9|63.1|53.0|63.1|59.6|69.3|95.8|71.9|49.1|42.7|39.4|41.9|53.4|
|LightMem (Fang et al.,2026)|25.0|42.9|46.9|60.4|33.8|70.2|63.8|80.8|95.2|77.5|24.2|26.9|21.8|25.1|39.3|
|Supermemory (Supermemory AI,2026)|35.0|56.3|52.9|65.9|42.2|67.4|58.8|74.2|76.4|69.2|15.8|16.0|14.9|14.8|35.5|
|SimpleMem (Liu et al.,2026)|25.0|63.2|47.6|60.7|34.0|69.7|64.6|72.7|97.3|76.1|53.8|48.0|**47.2**|**48.4**|52.8|
|PGMem (Choi et al.,2026)|39.6|54.4|53.7|66.3|45.2|73.9|60.9|81.1|83.1|74.7|19.8|18.9|16.7|17.6|39.1|
|**EvoMemState (Ours)**|53.1|**31.9**|**67.6**|**80.1**|**58.9**|**73.9**|**73.9**|**88.8**|90.4|**78.7**|**60.8**|**48.5**|46.4|45.2|**61.2**|



Table 1: Main results on four benchmarks with Qwen3-8B and GPT-4o-mini. _↑_ and _↓_ denote metrics to maximize and minimize, respectively. **Bold** and underlined values denote the best and second best results for each backbone. WTU/HTU: When/How to Use memory; Syco.: sycophancy rate; Use: correct use. 

existing memory systems? **Q2 (Memory State Effectiveness):** How effectively do the relational state and reasoning state support reliable memory use? **Q3 (Reasoning State Generalization):** How well does reasoning state generation transfer across tasks and memory systems? **Q4 (Ablation Study):** How does each component affect overall performance? Appendix C provides a case study and efficiency analysis. 

# **4.1 Experimental Setup** 

**Datasets.** We evaluate on four benchmarks covering memory use in personal agents and long term conversational memory. MemSyco-Bench (Xiang et al., 2026a) and MemTrapBench (Wang et al., 2026a) assess personal agents’ use of historical memories, including preference updates, evidence priority, and effects on reasoning. LoCoMo (Maharana et al., 2024) and LoCoMo-Refined<sup>1</sup> evaluate recall and reasoning across dialogue sessions. Dataset details appear in Appendix D.2. 

**Baselines.** We compare EvoMemState with nine baselines covering retrieval, persistent memory, and structured memory organization: 

1https://github.com/mem-eval-suite/LoCoMo_ refined 

NaiveRAG (Lewis et al., 2020), MemGPT (Packer et al., 2023), MemoryBank (Zhong et al., 2024), Mem0 (Chhikara et al., 2025), LightMem (Fang et al., 2026), A-MEM (Xu et al., 2026), Supermemory (Supermemory AI, 2026), SimpleMem (Liu et al., 2026), and PGMem (Choi et al., 2026). Details are provided in Appendix D.3. 

**Evaluation Metrics.** We evaluate answer quality, memory use, and retrieval completeness. Answer quality is measured by accuracy, F1, and MemTrapBench judge scores. Following MemSycoBench (Xiang et al., 2026a), we use Syco. Rate to measure inappropriate reliance on historical memories and Correct Use to measure valid personalization. Retrieval is evaluated by Complete Retrieval Rate and answer accuracy on complete-retrieval cases (Acc@complete). Full definitions are provided in Appendix D.4. 

**Implementation Details.** We use DeepSeek-V4Flash for offline memory construction and Qwen38B (Yang et al., 2025) and GPT-4o-mini as online response models. By default, the Memory State Evolution Policy is initialized from Qwen34B-Instruct-2507 (Yang et al., 2025) and trained with GRPO (Shao et al., 2024). Dataset construction, training details, and prompts are provided in 

6


<!-- page 7 -->

Percentage (%) 



<!-- Start of picture text -->
100<br>86.4 85.6<br>79.6<br>80 75.4 70.8<br>66.9 68.5<br>60 57.6 51.5 52.5 51.6 51.7 59.3 54.8 51.75<br>44.3<br>40 34.8 33.7 37.3 40.6 32.3 36.8 33.3 30.9 38.5 31.8<br>22.6<br>20<br>0<br>NaiveRAG Mem0 A-MEM LightMem MemGPT MemoryBank Supermemory PGMEM EvoMemState<br>(Ours)<br>Acc@complete Acc@complete<br>Complete Retrieval Rate LoCoMo-Refined MemSyco<br><!-- End of picture text -->

Figure 5: Complete retrieval rate and accuracy on questions with complete evidence using Qwen3-8B. Average complete retrieval rate reports the percentage of questions with all required evidence retrieved. Acc@complete reports accuracy on LoCoMo-Refined and MemSyco-Bench for questions with all required evidence retrieved. 

Appendices D.2, B.3, and E. 

# **4.2 Main Results (Q1)** 

We compare EvoMemState with memory systems using Qwen3-8B and GPT-4o-mini. Table 1 reports results on MemSyco-Bench and MemTrapBench for memory use, and on LoCoMo and LoCoMoRefined for long-term memory reasoning. 

**Obs.1. EvoMemState improves when and how** 

**memory is used.** On MemSyco-Bench, EvoMemState achieves accuracies of 57.6% and 58.9% with Qwen3-8B and GPT-4o-mini, outperforming the strongest baselines by 12.2% and 5.9%, respectively. It achieves the best When to Use and How to Use accuracy, the lowest Syco. Rate, and the highest Correct Use with Qwen3-8B. These results show more reliable decisions about whether and how history should affect the current response. 

**Obs.2. EvoMemState supports long-term recall and task-appropriate reasoning.** On LoCoMoRefined, EvoMemState achieves the highest LLMjudge and token F1 scores with both models, outperforming the strongest baseline in judge score by 6.1% and 7.0%. It also achieves the best Safety and Task Boundary scores on MemTrapBench, showing that factual records support recall while reasoning states prevent irrelevant history and prior task rules from overriding the current request. 

# **4.3 Memory-State Effectiveness (Q2)** 

To assess the two memory states, we examine whether the Relational State assembles complete evidence and whether the Reasoning State uses it correctly. Figure 5 reports Complete Retrieval Rate and Acc@complete on LoCoMo-Refined and MemSyco-Bench with Qwen3-8B; the metrics are 

considered jointly because complete-evidence subsets differ across systems. 

# **Obs.3. The Relational State connects related** 

**memories into reliable evidence.** EvoMemState achieves a complete retrieval rate of 85.6%, comparable to the best baseline. Guided by the personal memory ontology, its Relational State preserves each fact’s current attributes together with related updates, conflicts, and constraints. This organization allows related memories to provide complete evidence rather than remain independent records. **Obs.4. The Reasoning State supports reliable use of complete evidence.** Acccomplete reaches 70.8% on LoCoMo-Refined and 68.5% on MemSyco-Bench, exceeding the strongest baselines by 11.5% and 31.2%, respectively. These gains show that evidence completeness alone does not ensure correct use. By internalizing memoryuse experience, the learned policy generates a Reasoning State that makes the applicability, role, and priority of each memory explicit, helping the response model apply the assembled evidence appropriately and consistently. 

# **4.4 Reasoning-State Generalization (Q3)** 

To evaluate whether reasoning-state generation generalizes across tasks and memory systems, we pair the Memory State Evolution Policy with different memory systems on the benchmarks. Figure 6 reports cross-system performance changes, while Appendix C.1 compares alternative reasoning-state strategies across memory-use categories. 

**Obs.5. Reasoning states transfer across memory systems.** All six baselines improve when augmented with generated reasoning states, with overall gains ranging from 0.2% to 4.9%. NaiveRAG 

7


<!-- page 8 -->

||**MemSyco**|**LoCoMo-R**|**LoCoMo**|**MemTrap**||
|---|---|---|---|---|---|
|**Method**|Avg.|LLM-J.|LLM-J.|Avg.|**Overall**|
|**EvoMemState (Ours)**|**57.6**|**57.4**|**45.5**|**79.1**|**59.9**|
|w/o Relational State|48.7|54.9|45.2|72.7|55.4|
|w/o Reasoning State|49.6|55.8|42.5|64.1|53.0|
|w/o RL-Based State Evolution|49.7|55.4|45.0|62.7|53.2|



Table 2: Ablation results for EvoMemState with Qwen38B. The variants remove Relational State, Reasoning State or RL-Based State Evolution. 

and MemoryBank benefit most, improving by 4.9% and 4.8%, followed by A-MEM at 3.4%. These results show that the policy can produce useful reasoning states from evidence supplied by different memory systems. 

## **4.5 Ablation Study (Q4)** 

To examine the contribution of state composition and learned memory use (Q4), Table 2 compares three variants with Qwen3-8B. **w/o Relational State** uses retrieved seed records without incorporating related updates and conflicts into the state evidence. **w/o Reasoning State** provides the personal agent with state evidence but omits the policygenerated reasoning state. **w/o RL-Based State Evolution** retains reasoning-state generation but uses the policy before RL training. 

**Obs.6. Composing related records strengthens state evidence.** Removing relational state reduces MemSyco-Bench and the MemTrapBench score by 8.9% and 6.4%, respectively. The losses on LoCoMo-Refined and LoCoMo are smaller, at 2.5% and 0.3%. These larger losses on memoryuse tasks suggest that related updates and conflicts are particularly valuable for interpreting retrieved records before applying them to the response. 

**Obs.7. RL-based state evolution improves reasoning states.** Removing dynamic rules reduces MemSyco-Bench accuracy and the MemTrapBench score by 8.0% and 15.0%, respectively. Retaining rule generation without RL yields similar losses of 7.9% and 16.4%. Thus, generating rules alone provides little benefit on these benchmarks. These results support learning from memory application experience: answer-quality feedback helps the policy determine memory applicability, role, and priority, expressed as dynamic rules for each new user request. 



<!-- Start of picture text -->
Δ (pp)<br>NaiveRAG 51.7 4.9<br>56.5<br>Mem0 45.1 2.2<br>47.4<br>A-MEM 53.9 3.4<br>57.3<br>MemoryBank 53.358.0 4.8<br>MemGPT 48.6 0.7<br>49.3<br>LightMem 45.345.5 0.2<br>0 20 40 60 80<br>Score (%)<br>Base + Reasoning State<br><!-- End of picture text -->

Figure 6: Cross-system transfer of the Memory State Evolution Policy, averaged over MemSyco-Bench, MemTrapBench, and LoCoMo-Refined. Base and +Reasoning State denote results without and with generated reasoning states; ∆ is the gain. 

LaMP (Salemi et al., 2024) retrieves relevant profile items for personalized generation, while HELLO and related methods maintain and update user representations over time (Li et al., 2025; Tan et al., 2025a; Kang et al., 2025). PGMem (Choi et al., 2026) links persona information to events that support or revise it. Recent work further extends personalization to Web actions and agent training (Cai et al., 2025; Sun et al., 2025). Together, these studies cover persistent personalization across generation, user representation, and agent behavior. 

## **5.2 Long-Term Memory Systems** 

Long-term memory systems preserve information beyond the active context for later use (Ning et al., 2026; Xiao et al., 2026). MemGPT (Packer et al., 2023) manages information across storage tiers, MemoryBank (Zhong et al., 2024) maintains personal records, LightMem (Fang et al., 2026) uses compression and selective retrieval, and Mem0 (Chhikara et al., 2025) extracts and updates facts. A-MEM (Xu et al., 2026), Supermemory (Supermemory AI, 2026), and SimpleMem (Liu et al., 2026) further organize memories through links, temporal structure (Rasmussen et al., 2025), and update mechanisms. 

# **6 Conclusion** 

# **5 Related Work** 

## **5.1 Personal Agents and User Modeling** 

Personal agents use persistent user information to adapt across interactions (Li et al., 2026). 

In this paper, we presented EvoMemState, a statecentric long-term memory framework for personal agents that constructs coherent Relation States from multi-source memories and learns from con- 

8


<!-- page 9 -->

tinual memory use to generate Reasoning States. Experiments across memory-use and dialoguerecall benchmarks show consistent improvements, particularly under preference updates and conflicting evidence, demonstrating that reliable personal memory requires both coherent state construction and use-driven state evolution. 

# **Limitation** 

Our study focuses on text-based interaction histories. Real-world personal memory systems must also handle multimodal information, including documents, images, and other user artifacts. Extending our memory structure to represent, connect, and apply information across modalities remains an important direction for future work. 

- Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, and Deshraj Yadav. 2025. Mem0: Building production-ready ai agents with scalable long-term memory. _arXiv preprint arXiv:2504.19413_ . 

- Wonjun Choi, Yerim Kim, Yukyung Lee, and Susik Yoon. 2026. Pgmem: Tightly coupled personamemory graph for lifelong personalized agents. _arXiv preprint arXiv:2608.01708_ . 

- Yiming Du, Wenyu Huang, Danna Zheng, Zhaowei Wang, Sebastien Montella, Mirella Lapata, Kam-Fai Wong, and Jeff Z Pan. 2025. Rethinking memory in llm based agents: Representations, operations, and emerging topics. _arXiv preprint arXiv:2505.00675_ . 

- Shahul Es, Jithin James, Luis Espinosa Anke, and Steven Schockaert. 2024. Ragas: Automated evaluation of retrieval augmented generation. In _Proceedings of the 18th conference of the european chapter of the association for computational linguistics: system demonstrations_ , pages 150–158. 

# **Use of Large Language Models** 

During manuscript preparation, we used large language models to refine the English text, correct grammatical errors, and improve clarity and readability. We also used them to assist with table formatting. The authors reviewed and revised all suggestions to ensure that they preserved the intended scientific content and retain full responsibility for the accuracy and integrity of the final manuscript.
