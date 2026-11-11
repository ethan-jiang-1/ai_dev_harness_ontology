---
status: draft
updated: 2026-11-12
rq: [RQ1, RQ5]
---

# 03 知识派 · 前沿与挖掘

> 活页。稳定判断见 [README](./README.md)；证据见 [src](../../src/)；时刻位置见 [seams](../seams.md#六个时刻)。

## 这一派现在的前沿问题

1. **投影的最优粒度**：整段规则、结构化记录、还是「主张 + 证据」对？
2. **「答案是否写在知识里」能否自动化判定**？这是 C-04 的关键判据，目前靠人工预判。
3. **投影与 RAG 混用**：收益叠加还是互相干扰？
4. **编译的部署层回报**如何量化：上手时间、跨源引用率、审计通过率？
5. **为什么「主张-证据叶子」是唯一测出正收益的形态**？它是不是检索时真正需要的最小单位？
6. **查询生成三条路线**（选择性纠错 / ontology-in-context / ontology-free）没有头对头；见 [querying/frontier](./querying/frontier.md) 的 G1/G4。

## 信号源

- **Benchmark**：BrowseComp-Plus、FRAMES、多跳 QA；工业设备手册/工单。
- **会议/期刊**：ACL、EMNLP、NeurIPS、ISWC、SIGIR。
- **实验室/团队**：Narrow & Deep（韩国能源研究院）、CAI（infiniflow / RAGFlow）、Grid Agents。
- **工程侧**：context engineering、knowledge compilation、企业 RAG 的复盘。
- **arXiv**：cs.CL / cs.IR / cs.AI。

## 检索式

- `ontology projection LLM context`
- `knowledge compilation agent harness`
- `structured artifacts retrieval accuracy`
- `claim evidence tree retrieval`
- `context budget ontology agent`

## 候选队列（2026-11-12 按 [清除审计](../../meta/audits/2026-11-11-source-purge.md) 对账）

> 「已移出」= 原源未过准入，不再撑任何判断；方向仍开放，按五门找新源。

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| Narrow & Deep（2610.11768） | 投影 > 查询 > 检索；n=1 工厂、9 任务 | 已入档（probation） | 抽任务设计，做投影粒度对照 |
| CAI（2610.41172） | 强 harness 下工件无增益；唯一正收益是导航树 | 已入档 | 补 FRAMES 效应量/置信区间 |
| Grid Agents（2611.03534） | 法规/标准作为硬约束的知识供给 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2611-03534)：公司自证） | 法规硬约束方向待有独立采用的新源 |
| 投影粒度线 | 整段 vs 记录 vs 主张-证据 | 待扫描 | 用检索式 1/4 |
| 投影+RAG 混用线 | 叠加/干扰 | 待扫描 | 用检索式 3/5 |
| Grep is All You Need（Zenodo 2026） | grep + LLM 编译概念/FAQ 两层；76 agents、500 文本 | 待核 G1/G3 | 先核发表日期与独立信号，再决定建卡 |
| Knowledge-compile（Zenodo） | 知识编译 | 待扫描 | 读摘要 |
| Ontop（开源 OBDA） | 本体 + R2RML 在查询时编译成 SQL；供给型执行器，不是接缝 | 已核（代码+最小运行） | 包成 LLM 工具；做「有/无本体公理」消融 |
| Structured Contextual Distillation（SCD v3.1） | 确定性、可验证的持久 agent 状态 | 待扫描 | 与 04 共享 |
| Context Engineering（T3 blog） | 工程侧信号 | 只作 T3 | 不建卡 |

## 入档判据

- 同时报告 **准确率 + token/轮次**，能区分“省预算”与“提准确率”。
- 明确任务形态：答案是否写在知识里；否则无法与 C-04 对齐。
- 给出投影粒度/长度的对照，而不只是“用了本体”。

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-07 | 本地 20 篇复筛 | C-04 是最大张力；投影粒度无对照 | 两条进候选队列 |
| 2026-11-07 | 首轮外部扫描（web） | 4 个候选；Grep 摘要已读 | 入队；top 1 待落盘/建卡 |

## 本轮计划

> 2026-11-07 首轮外部扫描已完成；下一步从候选队列里选 top 1-2 落盘 + 建卡。

1. 从 Narrow & Deep 抽出 9 个任务的设计，判断哪些是“答案在文本里”。
2. 用检索式 1/4 找投影粒度的对照实验。
3. 若要验证，写一个仓库外最小对照：同一知识，投影 vs 查询 vs 检索。

## 候选（signal，未准入）

- **共享本体语义层（Emil Eifrem, Neo4j, AI Engineer 2026-07-22）**：业务本体 + 技术本体 + 映射 + 执行轨迹，把发现/可信/接线/学习从各 agent 收进一个有治理的层。按 material gate 判 `signal`（会议主 track 不算信号、公司自述、无独立采用），**不撑 L/交付物**；只作线索。URL: https://ai.engineer/talks/VGN22pPpb-8-thinner-agents-on-smarter-substrate-ontology-based
