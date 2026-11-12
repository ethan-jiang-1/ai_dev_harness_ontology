---
status: draft
updated: 2026-11-08
---

# 03 知识派 · 局部结论

> 本页是本派的局部判断账本。跨派/对外引用的结论升到 [conclusions](../conclusions.md) 的 E-xx；`03-Lx` 只在本派内使用。

| ID | 判断 | 等级 | 证据 | 备注 |
|---|---|---|---|---|
| 03-L1 | 投影文本在已测条件里 pooled element score 最高（0.777 > JSON 0.717 > 查询 0.638 > 检索 0.597），但 JSON/工具是事后比较，排序有模型级反转 | 已核（分数）/ 存疑（普适排序） | E-12 | N&D 单 plant、9 任务、4 模型；GLM-5.2 的 JSON 0.900 > 文本 0.891；Qwen 的工具 0.407 < 检索 0.538 |
| 03-L2 | 编译只在 claim–leaf 上解决预算，不解决准确率 | 已核 | E-01 / E-08 | FRAMES 限定；claim-leaf 省 token 条件性（−91%/+1.9%/−38%）；省 token 用轮次/时延换 |
| 03-L3 | E-01 与 E-12 不矛盾；差别不只在答案位置，还在投影什么（证据 vs 领域知识） | 推测 | C-04 | 分析框架；判据仍靠人工预判「答案在不在文本里」 |
| 03-L4 | （缺口登记，非判断）投影粒度未定：整段/记录/主张-证据三种粒度无对照 | — | 无对照 | 这是 gap 不是知识；关闭它需 N&D 式的粒度消融，记入 frontier | 整段/记录/主张-证据；N&D 只测一种文本投影 |
| 03-L5 | 结构不增加证据；测出 token 收益的工件是带逐字 span 的 claim-leaf tree（准确率仍 neutral） | 已核 | E-08 | CAI；RAPTOR/wiki/实体图 acc. neutral；PageIndex 在 FRAMES 规模实测为负，不能写成 neutral |
| 03-L6 | 编译的盈亏平衡是条件性的：`p_h > 2% + c/(0.929Q)`；平均 −38% 不能当上线依据 | 已核 | E-14 / RQ5 | 有限视野公式；需先量 p_h、c、Q、时延；时延 3× 仅 7 题 |
| 03-L7 | 9B 带投影 0.737 > 750B 不带 0.672，但区间约 0.3 宽；H2（增益随容量上升）未支持；不能据此排「供给形态 vs 模型容量」 | 已核（数字）/ 推测（一般化） | E-12 / N&D | 单 plant、9 任务；不能当普遍规律 |
| 03-L8 | 运行教训在抽取时并入塔才常被用；日志里的本事故记录不提升诊断（K4 0.644 vs K4x 0.645；日志检索 4/80） | 已核（现象）/ 推测（因果解释） | E-12 / N&D | 「谁决定检索」：抽取时 vs 查询时；H3 未支持；「把归纳提前做掉」未做因果检验 |
| 03-L9 | 受监管知识供给的三原则（证据引用、solver 算数字、人决策）在 Grid 里有实现与指标；但「工具必须到达研究」只是设计原则——Grid 对最强 agent baseline 仅 +0.5pp，Power-Agent 46/519 调用 PowerMCP 仍到 99.4% | withdrawn | Grid Agents | 2026-11-11 源移出；待重写。519 tasks/8 families；99.9%/13.9 s；Codex/Power-Agent 99.4% |
| 03-L10 | 盈亏平衡的不确定性由 miss 主导：miss ±1.5pp → `p_h*` 0.4–3.6%，hit ±1.5pp → 2.0–2.1%；先量 miss | 已核（解析推导） | E-14 | CAI §6.5；解析值不是实测；企业语料 miss 更高 |
| 03-L11 | 受监管支线的可审计性靠契约：citation + 拒答、strict pass（state_hash/study_type/solver_version）、记忆与决策点签核；客户指标尚无基线 | withdrawn | Grid Agents | 2026-11-11 源移出；待重写。Grid §4.1/§6.5；45/51 是结果不是阈值；optimizer −33–67% 是唯一有数的客户项 |
| 03-L12 | 查询生成有三条独立路线：生成后选择性纠错（GGC）、ontology-in-context（NLKGQ）、ontology-free agentic navigation（KGVoyager）；各自单 benchmark，没有头对头 | withdrawn | querying F1–F3 | 2026-11-11 源移出；待重写。三条路线不能放一张表比较；GGC 单 KG/单骨干；NLKGQ 单 snapshot；KGVoyager 4 小 benchmark |
| 03-L13 | GGC 的 90.23→98.33 是答案集匹配率，不是 execution accuracy；90.23 是 Generator 单跑、92.34 是全量纠错；45% 是相对全量纠错的墙钟 | 已核（数字）/ 推测（跨域） | GGC digest | 单 KG/单 3B 骨干/单 seed；无 2×2 净收益；空结果未测 |
| 03-L14 | NLKGQ 在 DBLP-QuAD 3.1 上 89.9% Match / 81.3% Exact；2.0 确定性协议 57.6/20.1；wrapper +15.0/+25.3；单 snapshot/单系统，Match 允许 superset | withdrawn | NLKGQ digest | 2026-11-11 源移出；待重写。完整 OWL 进上下文；无 entity linking/闭源模型；3.1 是作者修订 |
| 03-L15 | KGVoyager 在 4 个小型 benchmark 上平均 F1 64.6 vs 60.9（+3.7pp，不是 4×）；成本 −38.3%、墙钟 −23.8%；只支持 rdf:type 图，class index ~68% endpoint | withdrawn | KGVoyager digest | 2026-11-11 源移出；待重写。4 benchmark 88–108 题、同源；GRASP best-case；preprint/无独立复现 |
| 03-L16 | 四条查询路线（GGC/NLKGQ/KGVoyager/OBDA）按资产条件选，不按总分排；失败分生成前/后、探索、重写、度量五段 | withdrawn | [querying/compare](./querying/compare.md)；E-21 | 2026-11-11 源移出；待重写。无头对头；OBDA 的问题量/指标/成本未报；P1/P2 空格见订单 |
