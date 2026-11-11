---
status: draft
updated: 2026-11-12
rq: [RQ2, RQ3]
---

# 05 生产派 · 前沿与挖掘

> 活页。稳定判断见 [README](./README.md)；证据见 [src](../../src/)；时刻位置见 [seams](../seams.md#六个时刻)。

## 这一派现在的前沿问题

1. **精化能否产品化**：给定一个本体和一批下游错误，自动定位该修哪条子类/约束？CASTON 既没有「下游错误 → 公理」映射，也没报 recall@30/recall@10（[refinement/frontier](./refinement/frontier.md) 的 G1）。
2. **来源标记如何进入判定权重**，而不让判定变得不可解释？E-02 只测到来源差异，加权效果未测（[generation/frontier](./generation/frontier.md) 的 G3）。
3. **本体是否需要「测试」**：一组必须成立/必须不成立的事实对，能不能当回归测试（[refinement/frontier](./refinement/frontier.md) 的 G2）。
4. **生成物的可消费性怎么测**：四条生成路线只测说明、结构或用户感知，没有「判定器能否加载/解释/复现」的评测（[generation/frontier](./generation/frontier.md) 的 G1/G4）。
5. **表示选型假设是否成立**：第二档（结构表 + SHACL）能否覆盖多数判定场景、边界在哪；三档成本差没有对照（[representation/README](./representation/README.md#开放问题)）。这是本页假设，不是 SFE-O 的结论。

## 信号源

- **会议/期刊**：ISWC、ESWC、K-CAP、JIST；ACL/EMNLP 的 ontology generation 线。
- **标准/工具**：OWL 2、SHACL、SPARQL、ontology testing 工具。
- **领域本体**：工业设备（SFE-O）、生物医学/农业 KG（OntoDoc）、金融/电网（FIRME）。
- **实验室/团队**：CASTON、OntoDoc、Peeling、Evontree、ReX-GG、FIRME、OntoAct。
- **arXiv**：cs.AI / cs.CL / cs.DB / cs.LG。

## 检索式

- `ontology refinement LLM embedding`
- `ontology generation evaluation LLM`
- `ontology consumability checker evaluation`
- `SHACL constraints LLM agent`
- `ontology learning from embeddings`
- `ontology source provenance trust`

## 候选队列（2026-11-12 按 [清除审计](../../meta/audits/2026-11-11-source-purge.md) 对账）

> 「已移出」= 原源未过准入，不再撑任何判断；方向仍开放，按五门找新源。「G1 不过」= 首公开早于 2026-06-01。

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| CASTON（2610.21466） | 精化路线；high 6/6 被 2 位专家接受，但单一本体、单一公理类型、medium 0–25% | 已入档 | 补 recall@30/@10；找后续/可复现实现 |
| SFE-O（2610.37123） | 参数溯源建进本体；表达≠执行 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2610-37123)：质量 C） | 「表达≠执行」方向待过门新源 |
| OntoDoc（2611.01276） | 为任意 IRI 生成说明；151 术语 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2611-01276)：单机构） | 可消费性评测方向不变 |
| Peeling（2610.41785） | 从 MRL 嵌入抽 DAG；未测下游 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2610-41785)：单作者） | 嵌入→本体方向待新源 |
| Evontree（2510.26683） | 规则引导自演化 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2510-26683)：G1 过期） | 自演化方向待窗口内新源 |
| FIRME（2610.40482） | 跨期 registry + 观察级来源；`CMR=MMR×precision` | 已入档 | 把工程发现 1–3 落进 lifecycle 台账 |
| OntoAct（2610.21983） | 写入准入/覆盖率 stop；只借准入 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2610-21983)：单机构） | 准入闸门设计回 lifecycle 自身机制 |
| 本体测试线 | 必须成立/不成立的事实对 | 待扫描 | 用检索式 2/3 |
| KROMA（2507.14032，ISWC 2025） | RAG + LLM 本体匹配 | G1 不过（2025-07 首公开） | 不建卡；匹配方向待窗口内新源 |
| LightOL（IEEE 2026） | 轻量本体学习 | 待核 G1 | 读摘要，核发表日期 |
| Systematic Assessment of LLM-Based Ontology Learning（IEEE） | 本体学习评估框架 | 待核 G1 | 读摘要；对应 05 的评估缺口 |
| Automating OntoClean Verification | 本体验证 | 待扫描 | 与 02 共享 |

## 入档判据

- 报告 **精化精度、下游可用性、来源元数据** 中的至少一个。
- 给出可复现的本体/约束，而不只是生成文本。
- 会改变 05 的「来源影响可信度」或「表示 ≠ 执行」；后者目前只到 SFE-O 单域，跨域证据会改写限定。

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-07 | 本地 20 篇复筛 | CASTON 规模小；SFE-O 执行缺口；Peeling 未测下游 | 三条进候选队列头 |
| 2026-11-07 | 首轮外部扫描（web） | 4 个候选；KROMA 摘要已读 | 入队；top 1 待落盘/建卡 |
| 2026-11-08 | 四子主题 G-X 回写 | generation 6F/6G、refinement 6F/4G、representation 4F/5G、lifecycle 3+4F/3G；来源偏向标签降为 `推测`，medium 改为「不是全 mixed」 | 父页已回写；按本轮计划 1–2 补缺口 |

## 本轮计划

> 2026-11-08 父页已按子主题回写；当前优先补三个缺口，不再扩候选面。

1. **可消费性评测**：按 [generation/N1](./generation/frontier.md) 找评测口径，先能回答「判定器能否加载/解释/复现生成结构」；没有这个数，生成路线只能停在候选。
2. **精化召回**：先有专家标注的真错全集，再报 recall@30/@10（[refinement/F5](./refinement/findings.md)）；否则 6/6 不能当覆盖率。
3. **表示选型**：先写消费者契约，再比较第二档（结构表 + SHACL）与第三档；不拿 digest 的 2–4 人周估算当测量，也不默认第二档够用（[representation/mechanism](./representation/mechanism.md)）。

## 候选（signal，未准入）

- **本体/KG 的成本结构（叶小钗, 人人都是产品经理, 2026-08-31）**：数据清洗偶尔 >50%、小场景常从 10 万级起步、AI 把初稿成本降到约 1/10，但维护/治理未消失。按 material gate 判 `signal`（个人经验、浏览/评论不算信号），**不撑 L/交付物**；只作线索。URL: https://www.woshipm.com/ai/6457053.html
