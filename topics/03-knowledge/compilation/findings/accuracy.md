# 准确率与证据

## F1

- **判断**：在足够强的词法 harness 下，结构化工件（摘要树、wiki、实体图）在 FRAMES 上无可检出的准确率增益；PageIndex 大纲小规模中性、**FRAMES 规模实测为负**。
- **等级**：`已核`（CAI 一手正文）。
- **条件**：FRAMES；BM25/grep harness；MiniMax M3；glm-4-flash 抽取；单次运行、无 CI。结构变体（Table 3）各跑一次、原文未给 N；N=200 是主表 Table 4 的数，不能挪用到结构变体上。
- **反例/边界**：不能读成「零效应」；样本量不足以区分小效应；企业语料未测。PageIndex 的负面是 FRAMES 规模的观察，不是普遍规律；10^5 文档上「75% routing 成功」是解析模型，不是实测。
- **来源**：[CAI 卡](../../../../src/papers/2610.41172-context-as-infrastructure/card.md) · [digest](../../../../src/papers/2610.41172-context-as-infrastructure/digest.md) · [E-01](../../../conclusions.md)

## F6

- **判断**：结构不增加证据；只有「叶子带逐字证据」的 claim-leaf tree 测出正收益（token 端；准确率仍是 neutral）。设计规则是 **compile evidence, not prose**。
- **等级**：`已核`（CAI 一手正文）。
- **条件**：同一 carrier；RAPTOR 摘要树去 claim 后 neutral，PageIndex 大纲去 claim 后小规模 neutral、**FRAMES 规模实测为负**；wiki 与实体图 neutral；claim-leaf 平均 −38% token。
- **反例/边界**：树是 carrier，不是 retriever；PageIndex 的负面是 FRAMES 规模的观察，不是普遍规律；10^5 的 75% routing 是解析模型，不是实测。不能把 PageIndex 和 RAPTOR 一起写成「都 neutral」。
- **来源**：[CAI 卡](../../../../src/papers/2610.41172-context-as-infrastructure/card.md) · [digest](../../../../src/papers/2610.41172-context-as-infrastructure/digest.md) · [E-08](../../../conclusions.md)
