# 准确率与证据

## F1

- **判断**：在足够强的词法 harness 下，结构化工件（摘要树、PageIndex、wiki、实体图）在 FRAMES 上无可检出的准确率增益；PageIndex 在规模上反而退化。
- **等级**：`已核`（CAI 一手正文）。
- **条件**：FRAMES N=200；BM25/grep harness；MiniMax M3；glm-4-flash 抽取；单次运行、无 CI。
- **反例/边界**：不能读成「零效应」；样本量不足以区分小效应；企业语料未测。
- **来源**：[CAI 卡](../../../../src/papers/2610.41172-context-as-infrastructure/card.md) · [E-01](../../../conclusions.md)

## F6

- **判断**：结构不增加证据；只有「叶子带逐字证据」的 claim-leaf tree 测出正收益。设计规则是 **compile evidence, not prose**。
- **等级**：`已核`（CAI 一手正文）。
- **条件**：同一 carrier；RAPTOR summary/PageIndex 去掉 claim leaves 后 acc. neutral；claim-leaf 平均 −38% token。
- **反例/边界**：树是 carrier，不是 retriever；PageIndex 的负面是规模观察，不是普遍规律。
- **来源**：[CAI 卡](../../../../src/papers/2610.41172-context-as-infrastructure/card.md) · [E-08](../../../conclusions.md)
