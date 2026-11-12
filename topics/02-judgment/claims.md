---
status: draft
updated: 2026-11-07
---

# 02 判定派 · 局部结论

> 本页是本派的局部判断账本。跨派/对外引用的结论升到 [conclusions](../conclusions.md) 的 E-xx；`02-Lx` 只在本派内使用。

| ID | 判断 | 等级 | 证据 | 备注 |
|---|---|---|---|---|
| 02-L1 | curated 不等于可靠；标记精确度仅略优于随机 | withdrawn | E-02（已撤回） | 2026-11-12 源撤回，等级随证据降；待新 checker 源重写 |
| 02-L2 | 接地等级显式化在医学 QA 上整体最优 | withdrawn | E-03（已撤回）；2026-11-12 等级随证据降 | 等级是**模型在 answering 阶段自评**、未校准；不能当形式保证（见 02-L8） |
| 02-L3 | 误报与漏检谁更贵由代价比 r 决定；**没有 r 就不能下结论**（安全关键域 r 常让漏检更贵，与本句旧写法相反） | 推测 | 仓库推断 | 旧写法「误报比漏检更贵」无条件、可反转，已作废；给出 r 才成判断 | 待仓库外验证 |
| 02-L4 | （口径提醒，非判断）选阈值至少需要 catch/FA 与代价比，单报准确率不够 | 推测 | 分析 | 原句「判定器需要校准」是无人反对的套话；保留仅作口径提醒，不作结论引用 | 曲线 + 代价 |
| 02-L5 | ontology check 必须先超过「空结果重试」基线：后者在人工 fault 上 catch 79.2%、FA 0% | withdrawn | E-02 / Ontology Catch | 2026-11-11 源移出；待重写。否则只是多一次重试 |
| 02-L6 | 没有单一向优的本体来源：data-derived precision 72.3% / catch 8.2%；curated 57.1% / 18.9%；LLM 不稳定 | withdrawn | E-02（已撤回）；2026-11-12 等级随证据降 | catch/FA 必须分开报 |
| 02-L7 | 同一个本体既做 context 又做 checker 会降低 catch（同源确认偏差） | withdrawn | Ontology Catch（探索性） | 2026-11-11 源移出；待重写。需要独立 checker |
| 02-L8 | grounding level 是模型自评的弱信号，不是形式保证；entailed 94.9%/supported 82.1% 是切片，未校准 | withdrawn | E-03 / OA-RAG | 2026-11-11 源移出；待重写。作者自述无形式保证 |
| 02-L9 | 检索是主瓶颈：gold evidence 完全检索率 MCQ 61.7% vs OQ 23.6% | withdrawn | E-03 / OA-RAG | 2026-11-11 源移出；待重写。先修检索，再修推理 |
| 02-L10 | 输出校验要六类（schema/基数/来源/新鲜度/跨字段/合理性）+ 三态；把 undetermined 当 pass 会污染分母；只有前两类成本低 | 推测（综合） | checker F7/F8；[output-validation](./checker/output-validation.md) | cross-field/合理性误报未测；Great Expectations 映射待核 |
