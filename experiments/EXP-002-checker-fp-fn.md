---
id: EXP-002
status: draft
experiment_status: 未开始
updated: 2026-11-08
rq: [RQ4]
targets: [E-02]
artifact: pending（实现产物在仓库外）
---

# EXP-002 · 判定器的漏检/误报曲线

## 要回答什么

本体判定器的价值，能否用一条**漏检/误报曲线**刻画，而不是一个准确率？

## 会推翻什么

| 若结果为 A | 则 |
|---|---|
| 某来源在 FP/FN 上同时占优 | P3“无单一向优来源”被推翻 |
| 误报修复破坏不显著 | “误报比漏检更贵”降级为推测 |
| 三源曲线交叉 | 支持 P3；判定器要按 FA 预算选源，不按单一 precision |

## 设计

- **变量**：三源本体（人工/生成/挖掘）各建一个判定器；同一批产出。
- **对照**：空结果重试、随机 flag、LLM judge。
- **被控住的混淆项**：同一 KG/查询集；同一阈值扫描；同一标注协议；同一 judge。
- **度量**：漏检、误报、误报导致的修改破坏（改了之后更错的比率）；per-flagged 成本；分母写清（真实答案/人工故障/混合集）。
- **非对称代价**：漏检（放过错）vs 误报（改坏对）；分开报，不合成 accuracy。

## 状态与阻塞

- `experiment_status: 未开始`
- 阻塞：需要标注集；混合集比例要预注册。

## 回链

- 结论：[E-02](../topics/conclusions.md)
- 主题：[02/checker](../topics/02-judgment/checker/README.md) · [02/calibration](../topics/02-judgment/calibration/README.md)
- 相关 digest：[Ontology Catch](../src/papers/2610.37809-what-does-an-ontology-catch/digest.md)
