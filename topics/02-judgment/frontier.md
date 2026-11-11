---
status: draft
updated: 2026-11-12
rq: [RQ4, RQ5]
---

# 02 判定派 · 前沿与挖掘

> 活页。稳定判断见 [README](./README.md)；证据见 [src](../../src/)；时刻位置见 [seams](../seams.md#六个时刻)。

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

## 候选队列（2026-11-12 按 [清除审计](../../meta/audits/2026-11-11-source-purge.md) 对账）

> 「已移出」= 原源未过准入，不再撑任何判断；方向仍开放，按五门找新源。「G1 不过」= 首公开早于 2026-06-01。

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| What Does an Ontology Catch（2610.37809） | 把 checker 当研究对象；三源权衡 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2610-37809)：单机构） | E-02 已撤回；三源偏向方向待过门新源 |
| OA-RAG（2610.36335） | 接地等级显式化；六个医学任务 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2610-36335)：单机构） | 接地等级方向待新源 |
| MIOE（2610.38326） | “答对≠内部有本体”，影响判定器的必要性论证 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2610-38326)：单机构） | 与 06 共享方向 |
| checker calibration 线 | 误报代价与校准 | 待扫描 | 用检索式 1/5 |
| ToolRosetta（2610.24055） | 量化 guard 误报代价：shell 形式下专用 guard FP 升 21–47 点、拦 1/3–9/10 良性动作；带 placebo 对照；JSON 基准准确率不预测 code-acting 下的操作点 | signal（NeurIPS 2026 workshop 弱 I1、无代码/独立采用） | 正中 P2 false-veto 缺口；不建卡，待独立影响信号再过门 |
| 串联判定 / cascade 线 | 早期误报放大 | 待扫描 | 用检索式 3 |
| LOGicalThought（2510.01530） | 逻辑本体接地；四基准 +11.84% | G1 不过（2025-10 首公开） | 不建卡；方向并入 checker 校准线 |
| CORE-LLM-Bench（Zenodo 2026） | 受控神经符号基准；9,048 QA 实例 | 待核 G1/G3 | 先核发表日期与独立信号 |
| Can We Trust LLM Judges（2609.12002） | judge 能力相关偏差 + 多 judge 校准 | 待扫描 | 读摘要；先过五门 |
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

> 2026-11-12 对账后：Ontology Catch/OA-RAG/MIOE 已移出，E-02/E-03 撤回；方向保留，证据按五门重找。

1. 三源偏向（curated/LLM/数据挖掘）与 checker 校准：按五门找过门新源，含工程侧数据质量复盘。
2. 用检索式 1/5 找 checker 校准/误报代价的工作。
3. 为误报/漏检曲线设计一个最小标注集方案（谁能标、标多少、怎么算曲线）；本仓库不设实验目录。
