---
source: 2610.37123-sfe-o.pdf
part: paper
converted: 2026-11-07
converter: pymupdf4llm
---

# SFE-O: An Ontology for Knowledge-Grounded AI in Supercritical CO2 Biomass Extraction and Fractionation · 正文

> 由 PDF 自动转换，保留原文顺序；公式/表格可能有版式噪声。页码标记为 `<!-- page N -->`。
> 正文见 [paper.md](./paper.md)；参考文献见 [references.md](./references.md)；附录见 [appendix.md](./appendix.md)。

<!-- page 1 -->

# SFE-O: An Ontology for Knowledge-Grounded AI in Supercritical CO2 Biomass Extraction and Fractionation 

|Thomas Pallet|Mario Lezoche|Gianpaolo Leone|
|---|---|---|
|_Universit´e de Lorraine, CNRS, CRAN_<br>Nancy, France|_Universit´e de Lorraine, CNRS, CRAN_<br>Nancy, France|_ENEA, Italian National Agency for New_<br>_Technologies, Energy and Sustainable_|
|_LIFIA, Facultad de Inform´atica_<br>_Universidad Nacional de La Plata_<br>La Plata, Argentina<br>_MG-IB_<br>´Epinal, France<br>ORCID: 0009-0000-3240-0269|ORCID: 0000-0002-3271-1742|_Casaccia Research Centre_<br>Rome, Italy<br>ORCID: 0000-0001-5165-4520|
|Daniele Pizzichini|Diego Torres|Herv´e Panetto|
|_ENEA, Italian National Agency for New_<br>_Technologies, Energy and Sustainable_<br>_Casaccia Research Centre_<br>Rome, Italy<br>ORCID: 0000-0003-0544-9993|_LIFIA, CICPBA-Facultad de Inform´atica_<br>_Universidad Nacional de La Plata_<br>La Plata, Argentina<br>_SIGMA, Depto CyT, UNQ, Argentina_<br>ORCID: 0000-0001-7533-0133|_Universit´e de Lorraine, CNRS, CRAN_<br>Nancy, France<br>ORCID: 0000-0002-5537-2261|
|M´elanie Glibusic<br>_MG-IB_<br>´Epinal, France|||



ORCID: 0009-0003-9802-0164 

- **_Abstract_ —Supercritical CO** 2 **extraction (CO** 2 **-SFE) offers a** 

- **sustainable route for recovering high-value compounds from biomass while limiting the use of conventional organic solvents, but its design and interpretation require heterogeneous knowledge spanning biomass properties, operating conditions, mass transfer, and product fractionation, typically fragmented across technical reports, engineering models, external databases, and expert practice. This paper introduces SFE-O, a modular Web Ontology Language (OWL 2) ontology for supercritical CO** 2 **biomass extraction, structured around interconnected Biomass, Process, and Product dimensions and extended with explicit representations of process topology, parameter provenance, external and internal mass-transfer phenomena, and the Constant Extraction Rate (CER) / Falling Extraction Rate (FER) mechanisms. Computational dependencies among process quantities are represented explicitly, without embedding numerical solving in the ontology, so that input, measured, computed, externally retrieved, and fitted parameters remain traceable. SFE-O reuses established semantic resources (ChEBI, QUDT, OWL-Time, PROV-O) and is evaluated through a worked example that instantiates a real pilot-scale extraction batch, a reasoner-based consistency check, and a competency-question SPARQL query. The resulting knowledge model provides a machine-actionable foundation for querying, consistency checking, and mechanistic explanation of SFE processes, and establishes a knowledge layer that could support future ontology-grounded AI reasoning, a direction this paper motivates but does not evaluate.** 

**_Index Terms_ —Supercritical CO** 2 **extraction, ontology engineering, knowledge representation, semantic interoperability, biomass valorisation, mass-transfer modelling, knowledge-grounded AI.** 

## I. INTRODUCTION 

The valorisation of biological resources requires extraction technologies capable of recovering high-value compounds while limiting environmental impact, solvent consumption, and degradation of thermosensitive molecules. In this context, supercritical carbon dioxide extraction (CO2-SFE) has emerged as a particularly relevant technology for processing plant and microbial biomass. Above its critical point, CO2 combines a liquid-like density with gas-like transport properties, while its solvent power can be tuned through pressure and temperature. These characteristics enable selective extraction under comparatively mild operating conditions and make CO2SFE attractive for applications in the food, nutraceutical, pharmaceutical, and cosmetic sectors [1], [2]. 

The design and interpretation of an SFE process nevertheless require substantially more knowledge than the specification of extraction pressure and temperature alone. Process behaviour depends simultaneously on the chemical composition and morphology of the biomass, pretreatment conditions,


<!-- page 2 -->

particle-size distribution, extraction-vessel geometry, fixed-bed characteristics, CO2 flow rate, possible co-solvent use, thermophysical fluid properties, molecular descriptors of the target compounds, hydrodynamic conditions, external and internal mass-transfer mechanisms, extraction time, and the configuration of the downstream separation stages. These quantities are mutually dependent and may originate from direct measurements, engineering calculations, external physicochemical databases, mathematical models, or parameter-fitting procedures. At pilot and industrial scales, the problem is further extended by closed-loop CO2 circulation and by sequential separators operated under different pressure and temperature conditions, allowing the extracted material to be fractionated according to the solubility behaviour of its constituents. 

The kinetics of SFE also involve mechanistic knowledge that cannot be reduced to a flat collection of process parameters. The Broken-and-Intact Cell (BIC) approach distinguishes an easily accessible solute fraction associated with structures disrupted during biomass pretreatment from a less accessible fraction retained within intact structures [3], [4]. This distinction underlies the interpretation of a fast extraction region dominated by external mass transfer and a subsequent region increasingly governed by internal diffusion. Consequently, quantities such as the broken-cell fraction, Reynolds, Schmidt, and Sherwood numbers, molecular and effective diffusivities, and external mass-transfer coefficients form a network of physical and computational dependencies that is necessary for explaining how process conditions influence extraction behaviour. 

While established, process engineering knowledge remains fragmented across literature, technical documents, code, and expert practice, hindering its computational use. To address this, general-purpose ontologies like OntoCAPE provide formal, reusable conceptualizations that support knowledge management and engineering applications [5], [6]. However, a general process ontology does not by itself provide the domain-specific representation required to connect biomass morphology and composition with SFE operating conditions, transport mechanisms, fractional separation, derived quantities, and the provenance of the knowledge used to calculate them. 

This paper addresses this problem through _SFE-O_ , a modular ontology for the formal representation of supercritical CO2 biomass extraction knowledge. SFE-O structures the domain around three interconnected dimensions, _Biomass_ , _Process_ , and _Product_ , while introducing dedicated representations for process topology, temporal phases, transport phenomena, computational dependencies, and parameter provenance. Rather than representing domain quantities as isolated datatype attributes, the ontology explicitly models their semantic context and derivation relationships, distinguishing values that are provided as inputs, directly measured, computationally derived, retrieved from external resources, or estimated through fitting. The ontology also formalises the relationship between biomass disruption and the Constant Extraction Rate (CER) and Falling Extraction Rate (FER) mechanisms, thereby connecting structural characteristics of the feedstock to external and internal 

mass-transfer phenomena. 

The contribution is therefore not intended to replace mechanistic or numerical SFE models. Instead, SFE-O provides a machine-actionable semantic layer in which such models, their required inputs, their outputs, and their provenance can be explicitly interconnected. This layer is designed to support semantic querying, consistency checking, traceable mechanistic explanations, and interoperability with established knowledge resources. In accordance with this objective, the present work focuses on knowledge formalization and ontology validation and does not expose or evaluate experimental datasets. 

# II. RELATED WORK 

The development of SFE-O lies at the intersection of three research areas: mechanistic modelling of supercritical-fluid extraction, semantic modelling for chemical and bioprocess engineering, and reusable ontologies for representing chemical entities, quantities, temporal information, and provenance. Existing work provides important components for each of these areas, but does not directly address their integration into a machine-actionable representation of supercritical CO2 biomass extraction. 

# _A. Process and Biomass Ontologies_ 

Ontologies have been investigated in chemical and process engineering as a means to make engineering knowledge explicit, reusable, and interoperable across heterogeneous software environments. A major contribution in this direction is OntoCAPE, a large-scale formal ontology for Computer-Aided Process Engineering (CAPE) [5], [6]. OntoCAPE provides a modular and layered representation of process-engineering concepts, including plant equipment, process systems, material streams, physical quantities, and mathematical models. Its architecture demonstrates how formal semantics can support knowledge management, process modelling, simulationrelated applications, and reuse across different engineering tasks. 

The biomass and biorefinery domain has also motivated more specialised semantic models. Trokanas _et al._ proposed BiOnto, an ontology representing biomass types, biomass composition, and biorefining processing technologies [7]. BiOnto was designed to support the identification and comparison of biomass-processing pathways and demonstrated the use of semantic reasoning for applications such as technology screening and industrial symbiosis. Subsequent work has further explored ontology-supported characterisation of biorefinery streams and the use of semantic knowledge to improve decision making in biorefinery value chains [8], [9]. 

These approaches establish the relevance of ontology engineering for both process systems and biomass valorisation. However, their modelling scope is broader than the specific mechanisms governing supercritical-fluid extraction. In particular, the representation required for CO2-SFE must connect biomass morphology and chemical composition with extraction-system topology, supercritical-fluid properties, hydrodynamics, molecular transport, extraction kinetics, and


<!-- page 3 -->

fractional separation. It must also distinguish the origin of process quantities and explicitly represent dependencies among parameters used by engineering correlations and mechanistic models. 

# _B. Reusable Semantic Resources_ 

Rather than reproducing knowledge already formalised in established resources, domain ontologies can improve interoperability by reusing or aligning existing semantic models. Chemical entities are particularly relevant in SFE because extraction behaviour is molecule dependent. The Chemical Entities of Biological Interest ontology (ChEBI) provides a curated ontology and reference vocabulary for chemical entities and their structural and functional classifications [10]. Its hierarchy and stable identifiers enable molecules such as fatty acids and carotenoids to be connected to broader chemical classes without reconstructing an independent chemical taxonomy. Functional roles represented in ChEBI are also useful for linking extracted compounds to downstream interpretations such as antioxidant, pigment, or nutritional functions. 

For biomass-derived products intended for food-related applications, FoodOn provides an interoperable ontology for food materials, their biological origins, processing, and derived products [11]. Such external domain resources complement SFE-specific knowledge by allowing product fractions to be connected to broader application and valorisation contexts. 

Engineering knowledge additionally requires a consistent representation of physical quantities and units. The Quantities, Units, Dimensions and Types ontology (QUDT) provides ontologies for quantities, quantity kinds, units, dimensions, and numerical quantity values [12]. This distinction is important for SFE knowledge, where quantities such as pressure, temperature, mass flow, density, viscosity, diffusivity, and extraction yield are expressed using heterogeneous units and may also depend on a reference basis such as dry or wet biomass. 

Temporal semantics are required because an extraction process comprises ordered stages and time-dependent regions. OWL-Time provides concepts for temporal intervals, durations, instants, and their ordering relations [13]. These constructs can be specialised for representing extraction batches, extraction cycles, transient periods, operating-regime intervals, and kinetic extraction phases. 

Finally, the origin of a parameter is essential to its interpretation. A value may be experimentally measured, supplied as an operating set point, computed from other quantities, retrieved from an external physicochemical resource, or estimated through parameter fitting. The W3C PROV Ontology (PROV-O) provides a general provenance model based on entities, activities, agents, and derivation relations [14]. Its specialisation therefore enables the derivation chain of an SFE quantity to be represented explicitly rather than treating all numerical values as semantically equivalent. 

# _C. Research Gap and Positioning of SFE-O_ 

The reviewed approaches provide important building blocks but leave a modelling gap at their intersection. General process 

ontologies describe engineering systems at a broad level, whereas biomass and biorefinery ontologies primarily address feedstock classification, processing technologies, and transformation pathways. Conversely, chemical and metrological ontologies provide reusable semantics for individual information dimensions but do not describe how these dimensions interact within an SFE extraction mechanism, as summarised in Table I. 

TABLE I POSITIONING OF SFE-O RELATIVE TO RELATED ONTOLOGIES 

|**Ontology**|**Scope**|**Gap addressed by SFE-O**|
|---|---|---|
|OntoCAPE|General<br>CAPE<br>process|No SFE-specific mass-transfer,|
|[5], [6]|systems,<br>equipment,<br>streams|CER/FER, or fractionation se-<br>mantics|
|BiOnto [7]–<br>[9]|Biomass/biorefinery feed-<br>stock and conversion path-<br>ways|No extraction-process topology<br>or kinetic mechanisms|
|ChEBI,<br>QUDT,<br>OWL-Time,<br>PROV-O<br>[10],<br>[12]–<br>[14]|Chemical identity, units,<br>time, provenance (reused<br>by SFE-O)|Provide reusable semantics but<br>no SFE process model|
|**SFE-O**<br>**(this paper)**|SFE-specific:<br>biomass–<br>process–product,<br>BIC/CER-FER, parameter<br>provenance|—|



To our knowledge, no existing ontology specifically formalises the supercritical CO2 extraction domain, combining Broken-and-Intact Cell (BIC) extraction kinetics with explicit parameter provenance; this motivates the SFE-specific contribution below. 

SFE-O addresses this gap rather than competing with the aforementioned ontologies; instead, it specialises the extraction domain while reusing their semantics wherever appropriate, providing the formal structure required for traceable reasoning and subsequent knowledge-grounded AI applications. 

# III. KNOWLEDGE ELICITATION AND ONTOLOGY REQUIREMENTS 

The construction of SFE-O followed an iterative knowledgeengineering process in which domain knowledge was progressively extracted, structured, reconciled, and formalised. The methodology is a lightweight adaptation of the Ontology Development 101 iterative cycle [15], combined with the competency-question method of Gr¨uninger and Fox [16], applied here through five steps. In the present work, the objective was not to reproduce experimental datasets semantically, but to identify the concepts, relations, constraints, and computational dependencies required to describe and reason about a supercritical CO2 extraction process. 

# _A. Knowledge Sources and Elicitation Process_ 

The domain conceptualization was derived from six heterogeneous knowledge artefacts produced during the analysis of CO2-SFE processes. They comprised two technical reports describing bench- and pilot-scale extraction, a structured parameter-reference document, a computational spreadsheet


<!-- page 4 -->

TABLE II 

relating process quantities, a set of conceptual hierarchy diagrams, and an expert-authored descriptive model of the extraction mechanisms. Their complementary nature was important because no individual source contained all the knowledge required by the ontology. 

The bench-scale material provided the terminology associated with biomass characterisation, pretreatment, extraction equipment, target chemical compounds, operating conditions, co-solvent use, extraction time, and analytical characterisation. The pilot-scale documentation extended this description towards process topology by introducing closed-loop CO2 circulation, extraction cycles, equipment configuration, sequential separation stages, and the possibility of operating separators under distinct pressure and temperature conditions. The structured parameter material established correspondences among biomass properties, chemical compounds, process variables, units of measurement, and chemical identifiers. The computational representation exposed dependencies among quantities, whereas the conceptual diagrams organised these quantities into domain hierarchies and distinguished different origins of parameter values. Finally, the descriptive knowledge source provided explicit definitions of the relevant entities, extraction phases, physical mechanisms, equations, and domain constraints. 

Knowledge elicitation was performed by iteratively moving from terminology to conceptual dependencies. First, recurrent domain terms were identified and grouped according to their function in the extraction process ( _terminology elicitation_ ). Second, relationships among these terms were extracted, including structural, temporal, chemical, process, and computational relationships ( _relation extraction_ ). Third, mathematical expressions and engineering correlations were analysed to identify which quantities act as inputs and outputs of calculations. Fourth, domain constraints and modelling assumptions were separated from taxonomic knowledge ( _constraint separation_ ). Finally, the resulting conceptualization was reviewed with domain experts ( _expert review_ ) and reorganised into reusable ontology patterns. 

A major outcome of this process was the identification of three primary and causally connected domain perspectives: 



<!-- Start of picture text -->
Biomass  −→ Process  −→ Product . (1)<br><!-- End of picture text -->

The _Biomass_ perspective describes the material entering the extraction process, including its type, chemical composition, morphology, physical characteristics, and pretreatment state. The _Process_ perspective represents the extraction system, its geometry, equipment, operating parameters, fluid properties, temporal phases, hydrodynamics, and mass-transfer mechanisms. The _Product_ perspective describes the extract and its fractions, their chemical composition, and quantities such as extracted amount, yield, recovery, efficiency, and concentration. Equation 1 does not represent a purely sequential taxonomy: information from the three perspectives is linked through causal and computational dependencies. 

MAIN MODELLING REQUIREMENTS OF SFE-O 

|**Req.**|**Description**|
|---|---|
|R1|Represent Biomass, Process, and Product as interconnected but<br>modular domain perspectives.|
|R2|Reuse external semantic resources for chemical entities, quan-<br>tities, units, time, and provenance whenever appropriate.|
|R3|Represent physical and chemical quantities independently from<br>their numerical values, units, and reference bases.|
|R4|Distinguish intrinsic entity types from contextual roles, e.g., a<br>chemical entity playing the role of solute or co-solvent in a<br>process.|
|R5|Distinguish input, measured, computed, externally retrieved, and<br>fitted parameter values and preserve their provenance.|
|R6|Represent dependencies among quantities and mechanistic mod-<br>els without using OWL as a numerical solver.|
|R7|Represent extraction batches, cycles, stages, and an arbitrary<br>ordered sequence of separation stages rather than a plant-<br>specific fixed topology.|
|R8|Represent domain constraints and preserve distinctions among<br>missing, below-detection-limit, and actual zero-valued informa-<br>tion.|



# _B. Ontology Requirements_ 

The elicitation process resulted in eight principal modelling requirements, summarized in Table II. 

The remaining requirements are briefly motivated before the two most structurally demanding ones, R3 and R5– R6, are discussed in detail. R1 and R2 shape the overall architecture: R1 reflects the three causally linked perspectives identified during elicitation (Eq. 1), realised through the separate but interconnected sfeo-biomass, sfeo-process, and sfeo-product modules (Section IV), while R2 avoids re-formalizing chemical identity, units, time, and provenance semantics already covered by ChEBI, QUDT, OWL-Time, and PROV-O (Section II). R4 and R7 keep the model generic rather than plant-specific: R4 treats roles such as solute or co-solvent as contextual and process-dependent rather than intrinsic to a chemical entity, since the same compound can play different roles across batches, while R7 generalizes separation topology to an ordered sequence of stages (Eq. 2) instead of fixed, plant-specific separator classes. Finally, R8 preserves the distinction between a missing value, a belowdetection-limit measurement, and an actual measured zero, a distinction that matters wherever all three occur in productcomposition data (Section VII). 

Requirement R3 was particularly relevant because the source material combines quantities expressed using different units and reference bases. A chemical concentration, for example, is not represented merely as a molecule-specific datatype property; it is modelled as a contextualized quantity concerning a chemical entity and a material, associated with a numerical value, unit, and, where necessary, a reference basis such as dry or wet biomass. This design prevents the ontology schema from growing whenever a new chemical compound is introduced. 

Requirement R5 emerged from the observation that process knowledge combines quantities having different epistemic origins. An extraction pressure may be introduced as an operating


<!-- page 5 -->

set point, biomass composition may result from measurement, Reynolds or Sherwood numbers may be calculated, CO2 thermophysical properties may be obtained from an external computational resource, while parameters such as the brokencell fraction or effective diffusivity may be estimated by fitting. Making these distinctions explicit is necessary for traceability and for subsequent explanation of how a result has been obtained. 

Requirement R6 concerns the mechanistic structure of the extraction process. The elicited knowledge identifies dependencies linking biomass morphology, process geometry, fluid properties, molecular descriptors, hydrodynamics, and mass transfer. For instance, Reynolds and Schmidt numbers contribute to the determination of the Sherwood number, which is subsequently involved in the determination of the external mass-transfer coefficient. These relations must therefore be represented as explicit computational dependencies while leaving their numerical evaluation to appropriate external software or mathematical services. 

The same requirement applies to the distinction between the Constant Extraction Rate (CER) and Falling Extraction Rate (FER) regions. The broken-cell fraction _g_ identifies the portion of the biomass whose solute is immediately accessible after pretreatment and is therefore associated with the faster, externally controlled extraction mechanism. Conversely, the remaining intact fraction (1 _− g_ ) introduces internal masstransfer resistance and contributes to the diffusion-controlled extraction mechanism. Preserving this mechanistic distinction was considered essential for supporting explanations that connect pretreatment and biomass morphology to extraction behaviour. 

# _C. Competency Questions_ 

The requirements were complemented by competency questions (CQs) expressing representative information needs that SFE-O should support. A subset used to guide the present ontology is reported below: 

- **CQ1:** Which biomass characteristics and chemical entities are relevant to a given supercritical CO2 extraction process? 

- **CQ2:** Which geometric and operating quantities characterize a given extraction batch and its process stages? 

- **CQ3:** Which quantities are required to derive _Re_ , _Sc_ , _Sh_ , and _kf_ , and what is the provenance of each required quantity? 

- **CQ4:** How is the broken-cell fraction related to the portions of a target compound associated with the CER and FER mechanisms? 

- **CQ5:** Which separation stage generates a given product fraction, and under which pressure and temperature conditions? 

- **CQ6:** Which chemical entities or chemical classes characterize a product fraction and which functional roles can be associated with them? 

- **CQ7:** Was a process quantity supplied, measured, calculated, retrieved from an external resource, or estimated through fitting? 

- **CQ8:** Are the represented quantities and relationships compatible with the domain constraints encoded for the extraction process? 

These competency questions define the boundary between domain information that merely occurs in the source material and knowledge that must be explicitly accessible through the ontology. They consequently guided the modular architecture, reuse decisions, properties, and constraint representations presented in the following section. 

# IV. SFE-O ARCHITECTURE AND SEMANTIC REUSE 

SFE-O is implemented as a modular OWL 2 ontology whose organisation reflects the separation of concerns identified during knowledge elicitation. The SFE-O v0.1.0 ontology described in this paper is openly available on Zenodo [17] and is organised into seven local modules ( _Core_ , _Biomass_ , _Process_ , _Transport_ , _Product_ , _Provenance_ , and _Application_ ) together with an aggregate ontology importing the complete model. Fig. 1 summarizes this architecture and its connections with external semantic resources. 

# _A. Modular Architecture_ 

The sfeo-core module provides the common semantic backbone, including material and process entities, equipment, material streams, contextual roles, parameter values, and activities responsible for producing or deriving knowledge. The sfeo-biomass module specialises this backbone with biomass types and batches, pretreatment operations, morphology, physical characteristics, chemical composition, and the distinction between broken and intact structural units required by the Broken-and-Intact Cell representation. 

The sfeo-process module represents extraction systems, batches, cycles, equipment, operating conditions, geometry, fluid properties, and temporal process stages. An ExtractionBatch denotes the complete extraction operation performed on a defined biomass load, whereas an ExtractionCycle represents one circulation of CO2 through the relevant functional stages. This distinction supports both single-pass laboratory systems and closed-loop pilot or industrial configurations. 

Separation topology is intentionally generalized. Rather than defining plant-specific classes such as SE1, SE2, and SE3, an extraction cycle may contain an ordered sequence of SeparationStage individuals, 



<!-- Start of picture text -->
S 1 ≺ S 2 ≺· · · ≺ Sn, (2)<br><!-- End of picture text -->

each associated with its equipment, pressure, temperature, and generated ProductFraction, so a three-separator pilot plant is one instantiation, not a structural limit. 

The sfeo-transport module represents hydrodynamic and mass-transfer knowledge, including molecular and effective diffusivity, Reynolds, Schmidt, and Sherwood numbers,


<!-- page 6 -->

**SFE-O Architecture** 



<!-- Start of picture text -->
External semantic sfeo.owl<br>resources<br>QUDT sfeo-core<br>quantities, units common, process & equipment entities, material streams,<br>OWL-Time contextual roles, parameter values, computational activities<br>temporal entities<br>semantic backbone<br>PROV-O<br>provenance<br>sfeo-biomass sfeo-process sfeo-transport sfeo-product<br>NCBI Taxonomy types & batches, SFE system, hydrodynamics, extracts, fractions,<br>organism taxa pretreatment, stages & cycles, mass transfer, yield, recovery,<br>morphology, equipment, CER / FER regimes efficiency,<br>ChEBI cell state, conditions, fluid concentration,<br>chemical entities composition Re, Sc → Sh → kf functional roles<br>Biomass Process Product<br>sfeo-application sfeo-provenance<br>FoodOn application-level SFE knowledge, input, measured, computed,<br>no experimental observations retrieved & fitted values<br>food products<br>LIPID MAPS<br>lipid classes<br>Legend owl:imports owl:equivalentClass rdfs:seeAlso causal flow<br><!-- End of picture text -->

Fig. 1. Modular architecture of SFE-O and its relationships with reused or aligned external semantic resources. 

the external mass-transfer coefficient _kf_ , and the CER/FER mechanisms. The sfeo-product module describes total extracts and separated fractions together with quantities such as extracted amount, yield, recovery, efficiency, concentration, and functional roles. Finally, sfeo-provenance distinguishes input, measured, computed, externally retrieved, and fitted parameter values, while sfeo-application contains application-level SFE knowledge without representing experimental observations. 

# _B. Semantic Modelling Patterns_ 

Three modelling patterns are central to SFE-O. 

First, chemical composition is represented through a reified relation between a material, a chemical entity, and a quantity value rather than through molecule-specific datatype properties. Conceptually, a composition statement is represented as 



<!-- Start of picture text -->
⟨M, C, Q, R⟩, (3)<br><!-- End of picture text -->

where _M_ is a biomass or product material, _C_ the chemical entity, _Q_ the associated quantity, and _R_ an optional reference basis such as dry or wet mass (Eq. 3). New compounds can therefore be introduced without modifying the ontology schema. 

Second, SFE-O distinguishes intrinsic entity types from contextual process roles: a chemical entity is not intrinsically a _solute_ , but may play a SoluteRole in a given extraction context, and the same pattern applies to solvent and cosolvent participation, since these roles depend on the process configuration and operating conditions. 

Third, computational dependencies are explicitly represented without requiring OWL to execute numerical models. 

A calculation is connected to its required quantities and generated output, 



<!-- Start of picture text -->
Calculation<br>{Q 1 , . . . , Qn} −−−−−−−→ Q out . (4)<br><!-- End of picture text -->

For example, this pattern (Eq. 4) represents that the Sherwood number depends on Reynolds and Schmidt numbers and that the external mass-transfer coefficient subsequently depends on Sherwood number, solute diffusivity, and particle size. Numerical evaluation remains delegated to appropriate engineering software, while the ontology preserves the semantic dependency and provenance chain. 

# _C. Reuse of External Semantic Resources_ 

SFE-O adopts the selective reuse strategy already motivated in Section II (QUDT [12], OWL-Time [13], PROV-O [14]), illustrated on the left side of Fig. 1: quantities and units, temporal concepts, and the provenance of measurement, calculation, external-lookup, and fitting activities are each delegated to the corresponding external ontology rather than re-modelled locally. Chemical entities are likewise selectively aligned with ChEBI [10] rather than reconstructed through a local taxonomy, so that compounds such as carotenoids and fatty acids retain stable, externally maintained identifiers while remaining associated with SFE-specific process roles. Other resources serve only as interoperability or extension points, not full imports: NCBI Taxonomy [18] for biological-source identifiers, and FoodOn/LIPID MAPS as possible alignments for food-product and lipid-specific semantics. 

This architecture keeps SFE-O focused on knowledge specific to supercritical CO2 extraction while delegating chemical identity, units, time, and provenance to established resources.


<!-- page 7 -->

# V. MECHANISTIC KNOWLEDGE AND CONSTRAINT FORMALIZATION 

A distinctive feature of SFE-O is the explicit representation of mechanistic relationships connecting biomass structure, operating conditions, mass transfer, and product formation. 

# _A. CER/FER Representation_ 

Following the BIC interpretation [3], [4], let _ms_ be loaded biomass mass, _X_ 0( _i_ ) the initial concentration of compound _i_ , and _g_ the broken-cell fraction. SFE-O represents the initial, broken-cell, and intact-cell amounts as 

_C_ 0( _i_ ) = _msX_ 0( _i_ ) _, C_ 0 _,BC_ ( _i_ ) = _g msX_ 0( _i_ ) _, C_ 0 _,IC_ ( _i_ ) = (1 _− g_ ) _msX_ 0( _i_ ) _._<sup>(5)</sup> The broken fraction (Eq. (5)) is associated with the Constant Extraction Rate (CER) region, predominantly governed by external mass transfer, whereas the intact fraction contributes to the Falling Extraction Rate (FER) region, increasingly controlled by internal diffusion. The corresponding massbalance constraints are 



<!-- Start of picture text -->
M CER ≤ gmsX 0( i ) , M FER ≤ (1  − g ) msX 0( i ) ,<br>(6)<br>M TOT =  M CER +  M FER ≤ msX 0( i ) .<br><!-- End of picture text -->

Product indicators can then be linked to the same mechanistic model (Eq. (6)), e.g., _EFF_ = _M_ TOT _/C_ 0( _i_ ) and _CONC_ = _M_ TOT _/EA_ , where _EA_ is total extracted material. 

# _B. Hydrodynamic and Mass-Transfer Dependencies_ 

Extraction pressure and temperature determine supercriticalCO2 properties such as density _ρ_ and viscosity _µ_ ; biomass morphology contributes particle size _dp_ ; and molecular identity contributes diffusivity _D_ ( _i_ ). With flow and bed characteristics, these quantities determine _Re_ and _Sc_ , followed by 

_Sh_ = 2 + 1 _._ 1 _Re_<sup>0</sup><sup>_._6</sup> _Sc_<sup>0</sup><sup>_._33</sup> _, {Sh, D_ ( _i_ ) _, dp} → kf_ ( _i_ ) _._ (7) Each derivation is a CalculationActivity, with calibration and external lookups typed as ParameterFittingActivity and ExternalLookupActivity. Effective diffusivity _D_ EFF( _i_ ), governing internal transport, depends on porosity, tortuosity, and microstructure in a biomass-specific way for which the elicited sources give no single universal equation; SFE-O therefore records the dependency without imposing one. 

# _C. Constraints_ 

OWL axioms express logical conditions such as disjointness of broken/intact structures and CER/FER phases, while arithmetic bounds, parameter ranges, and derived-quantity relations are kept as machine-readable constraint expressions, not evaluated by the OWL reasoner itself. _Not analysed_ , _below detection limit_ , and a measured zero remain three distinct states, preserving semantic correctness while leaving numerical constraint execution to future validation or engineering services. 

# VI. KNOWLEDGE-GROUNDED AI PERSPECTIVE 

SFE-O is also intended as a grounding layer for future AIassisted SFE interpretation using a Large Language Model (LLM); no LLM system is built or evaluated in this paper. Work on LLM–knowledge-graph integration highlights the value of combining generative language capabilities with explicit machine-interpretable knowledge [19]. An LLM could translate a natural-language question into a semantic query over SFE-O and use retrieved facts, mechanistic dependencies, and provenance as grounded context. For example, a question about _kf_ can expose the path from operating/biomass properties through _Re_ , _Sc_ , and _Sh_ (Eq. (7)) together with the provenance of the required quantities. 

This separates semantic validity from language generation: SFE-O would define admissible concepts, relations, and dependency chains; numerical services would execute calculations; and the LLM would provide interaction and orchestration. The present contribution does not evaluate such an LLM implementation, but establishes the formal layer required for subsequent ontology-grounded question answering and explainable process interpretation. 

# VII. EVALUATION AND DISCUSSION 

Evaluation concerns SFE-O as a knowledge representation rather than a predictive system. First, the modular OWL 2 files were checked for RDF/XML parsing and import-structure correctness. Second, the ontology was assessed against the requirements and CQs of Section III. It represents biomass and chemical characteristics, process geometry and operating quantities, the _Re_ – _Sc_ – _Sh_ – _kf_ dependency chain, CER/FER relations, ordered separation stages and product fractions, and the provenance of input, measured, computed, external, and fitted quantities. 

Third, CQ1–CQ8 are demonstrated through a worked example. The ontology is a schema with no individuals; one real pilot-scale extraction batch was instantiated using operating data for _Dunaliella salina_ (350 bar, 65°C, 0.31 kg/min CO2, 120 min) and its three-separator cascade (SE1/SE2/SE3, with SE2 at 56 bar/25°C and SE3 at 54 bar/25°C), asserting individuals such as DS04_SE2 (a SeparationStage) and DS04_Fraction_SE2 (the ProductFraction it generates), with a measured _β_ -carotene concentration (7.08 mg/g, 20.8% recovery). 

The instantiated ontology was classified with the HermiT Description Logic (DL) reasoner and confirmed consistent, satisfying all OWL axioms including the qualified-cardinality restriction on generatedBySeparationStage. The competency question CQ5 (“which separation stage generates a given product fraction, under which pressure and temperature”) was then answered with an executed SPARQL query against the resulting graph: 

SELECT ?fraction ?stage ?p ?t WHERE { 

?fraction sfeo-product: 

generatedBySeparationStage ?stage . 

?stage sfeo-process:hasOperatingQuantity ?pq, ?tq . 

- ?pq a sfeo-process:SeparatorPressure ;


<!-- page 8 -->

qudt:numericValue ?p . 

?tq a sfeo-process:SeparatorTemperature ; qudt:numericValue ?t . } 

matching the source value exactly. This single worked example shows CQ1–CQ8 to be expressible and queryable on real data; it does not constitute a performance benchmark. 

Fourth, the conceptual model was iteratively reviewed against the elicited engineering knowledge. General separator stages rather than fixed SE1--SE3, reified composition statements, and contextual _solute_ roles avoid over-specialisation to one plant or compound set. The main limitations concern execution rather than representation: numerical dependencies are not solved within OWL; constraints are not yet executable Shapes Constraint Language (SHACL) shapes; external thermophysical, descriptor, diffusivity, and fitting services remain integration points; and effective diffusivity requires biomassspecific assumptions. A few data-level inconsistencies also remain open for expert validation: a conflicting interfacial-area formula ( _a_ = 6 _/dp_ vs. _a_ = _dp/_ 6) across source documents, a bed-volume expression possibly missing a geometric factor, and one ChEBI identifier shared by two distinct fatty acids; these are flagged explicitly within the ontology rather than silently resolved. 

The paper also deliberately excludes broader experimental observations beyond the single worked example above. This establishes a transparent semantic layer before coupling SFE-O with data, numerical models, and generative AI. Future evaluation should therefore instantiate additional batches and competency questions beyond CQ5, test executable constraints, and determine whether ontology-grounded interaction improves traceability, consistency, explanation, and processspace exploration compared with unstructured AI interaction. 

# VIII. CONCLUSION 

SFE-O provides a modular semantic representation of supercritical CO2 biomass extraction, connecting biomass characteristics, process topology, transport phenomena, separation, products, and provenance. Its central contribution is the explicit formalization of BIC/CER–FER mechanisms and computational dependencies while reusing ChEBI, QUDT, OWLTime, and PROV-O, demonstrated on an instantiated extraction batch with a HermiT-checked full OWL 2 DL consistency result and an executed competency-question SPARQL query. Future work will add executable constraint validation, numerical/physicochemical services, experimental instantiation, and evaluation of ontology-grounded AI for process interpretation and optimisation. 

# ACKNOWLEDGMENT
