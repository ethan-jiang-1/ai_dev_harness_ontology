---
status: draft
updated: 2026-11-07
rq: [RQ4, RQ5]
---

# 02 判定派 · 前沿与挖掘

> 活页。稳定判断见 [README](./README.md)；证据见 [notes](../../src_notes/)；时刻位置见 [seams](../seams.md#六个时刻)。

## 这一派现在的前沿问题

1. **误报的破坏力**能否量化：被误标后 agent 去“修复”，改坏了多少？这是本派最贵的代价。
2. **判定器曲线**：漏检/误报 + 人工成本，能否离线测？标注集从哪来、谁标注？
3. **curated 精确度仅略优于随机**（E-02）是否跨域成立？哪些域是例外？
4. **接地等级由谁判定**：模型自评、独立判定器、还是本体推导？如何避免等级通胀？
5. **串联判定**：格式→语义→行为，早期误报如何放大成下游大量无效工作？

## 信号源

- **Benchmark / 数据**：UniProt、Web KG、私有大图；医学 QA（OA-RAG 的六个任务）。
- **会议/期刊**：ACL、EMNLP、NeurIPS、ISWC、K-CAP。
- **实验室/团队**：What Does an Ontology Catch（Wrocław）、OA-RAG（杭州/英国）、本体校验与数据质量团队。
- **工程侧**：数据质量、schema 校验、LLM-as-judge 校准的实践。
- **arXiv**：cs.AI / cs.CL / cs.DB。

## 检索式

- `ontology checker LLM agent false positive`
- `grounding level ontology question answering`
- `semantic validation agent knowledge graph`
- `curated ontology precision recall`
- `LLM judge calibration false positive cost`

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| What Does an Ontology Catch（2610.37809） | 把 checker 当研究对象；三源权衡 | 已入档 | 回正文补每源 FP/FN 与域 |
| OA-RAG（2610.36335） | 接地等级显式化；六个医学任务 | 已入档 | 确认等级判定由谁执行 |
| MIOE（2610.38326） | “答对≠内部有本体”，影响判定器的必要性论证 | 已入档（主归 06） | 与 06 共享 |
| checker calibration 线 | 误报代价与校准 | 待扫描 | 用检索式 1/5 |
| 串联判定 / cascade 线 | 早期误报放大 | 待扫描 | 用检索式 3 |
| LOGicalThought（2510.01530） | 逻辑本体接地；四基准 +11.84%，negation +10.2、implication +13.2、defeasible +5.5 | 摘要已读 | 落盘 + 建卡；看“本体”具体形态 |
| CORE-LLM-Bench（Zenodo 2026） | 受控神经符号基准；9,048 QA 实例、81,432 观测 | 摘要已读 | 先入候选；评估能否用于 EXP-002 |
| Can We Trust LLM Judges（2609.12002） | judge 能力相关偏差 + 多 judge 校准 | 待扫描 | 读摘要；对应 checker 校准 |
| Automating OntoClean Verification | 本体验证自动化 | 待扫描 | 与 05 共享 |

## 入档判据

- 同时报告 **漏检与误报**，或给出可复现的曲线。
- 测量 **误报后的修复破坏**，而不只是判定准确率。
- 跨域对照，能改变 E-02 的适用范围。

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-07 | 本地 20 篇复筛 | E-02 的跨域性未测；OA-RAG 的等级判定主体未写清 | 两条进候选队列 |
| 2026-11-07 | 首轮外部扫描（web） | 4 个候选；LogT、CORE-LLM-Bench 摘要已读 | 入队；top 2 待落盘/建卡 |

## 本轮计划

> 2026-11-07 首轮外部扫描已完成；下一步从候选队列里选 top 1-2 落盘 + 建卡。

1. 读 What Does an Ontology Catch 正文，补三源 FP/FN 与域，重写 E-02 的限定。
2. 用检索式 1/5 找 checker 校准/误报代价的工作。
3. 为 EXP-002 设计一个最小标注集方案（谁能标、标多少、怎么算曲线）。
