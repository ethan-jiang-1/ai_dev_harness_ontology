---
status: draft
updated: 2026-11-12
rq: [RQ4]
---

# 06 测量派 · 前沿与挖掘

> 活页。稳定判断见 [README](./README.md)；证据见 [src](../../src/)；时刻位置见 [seams](../seams.md#六个时刻)。

## 这一派现在的前沿问题

1. **按机制类型分派的度量方案**：闸门、判定器、知识供给、记忆各用哪把尺？这是全仓最大空缺。
2. **“部署层面回报”如何量化**：上手时间、跨源引用率、审计通过率、连续性？
3. **基准的慷慨程度**能否被度量：答案有多大比例直接出现在给定材料里？
4. **误报修复的破坏力**：被误标后 agent 改坏了多少？这是 02 派最贵的代价。
5. **过程指标与任务指标的联合分析**：token、轮次、重复查询率，如何与准确率一起报？

## 信号源

- **Benchmark**：τ²-bench、BrowseComp-Plus、FRAMES、AgentBench；机制可解释性基准（MIOE）。
- **会议/期刊**：NeurIPS、ICML、ICLR、ACL、EMNLP；FAccT / AIES 的评测线。
- **实验室/团队**：AI2 / Drexel（SLB）、MIOE（King's College London 等）、CAI（RAGFlow）。
- **工程侧**：eval 平台、agent observability、部署指标复盘。
- **arXiv**：cs.AI / cs.CL / cs.LG。

## 检索式

- `metric mismatch agent evaluation`
- `process metrics agent harness`
- `mechanistic interpretability ontology`
- `workflow failure attribution LLM`
- `solver-like behavior formalizer`

## 候选队列（2026-11-12 按 [清除审计](../../meta/audits/2026-11-11-source-purge.md) 对账）

> 「已移出」= 原源未过准入，不再撑任何判断；方向仍开放，按五门找新源。「G1 不过」= 首公开早于 2026-06-01。

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| MIOE（2610.38326） | 答对≠内部有本体；机制可干预 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2610-38326)：单机构） | 内部本体度量方向待新源 |
| Diagnose（2610.35267） | 失败归因到工作流；角色级画像 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2610-35267)：position paper） | 工作流归因方向待实证新源 |
| SLB（2611.02395） | 只看输出的尺子会漏掉冗余/错误继承 | 已入档 | 补 85/24/9/97 的原文数字 |
| CAI（2610.41172） | 提出方案又给反证；过程指标 | 已入档（主归 03） | 抽 token/轮次的度量设计 |
| Ontology Catch（2610.37809） | 判定器的 FP/FN 曲线 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2610-37809)：单机构） | 与 02 共享方向 |
| 部署指标线 | 上手/集成/审计 | 待扫描 | 用检索式 1/2 |
| Agents Are Systems（2610.01618） | 54% 结果方差来自重复同一配置；信息 > 时间/模型；验证工具 > 提示；18k 轨迹 | 已入档（probation） | 正文补方差分解与 config 定义 |
| AgentDebugX（EMNLP 2026 demo） | 失败观测/归因/修复闭环 | 待核 G1/G3 | 核发表日期与独立信号，再决定建卡 |
| Intention-behavior consistency failure attribution | 多 agent 失败归因 | 待扫描 | 读摘要 |
| Towards Outcome-Oriented, Task-Agnostic Evaluation（2511.08242） | 任务无关的结果导向评估 | G1 不过（2025-11 首公开） | 不建卡 |

## 入档判据

- 提出一个 **可操作的度量**，或报告一次“尺子错了导致结论反向”。
- 同时报告 **任务指标 + 过程指标**。
- 会改变 C-03，或给 RQ4 一个可执行的实验设计。

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-07 | 本地 20 篇复筛 | C-03 仍是最强判断；缺“机制→尺子”对照表 | 先做表，再扫外部 |
| 2026-11-07 | 首轮外部扫描（web） | 4 个候选；Agents Are Systems、AgentDebugX 摘要已读 | Agents 已落盘/建卡；AgentDebugX 待落盘 |

## 本轮计划

> 2026-11-12 对账后：MIOE/Diagnose/Ontology Catch 已移出；C-03 仍是本派最强判断，证据基座改为现存 10 篇 + 8 开源。

1. 做一张“机制类型 → 失效形态 → 主指标 → 过程指标”的表。
2. 用检索式 1/2 找评测方法论与部署指标。
3. 把现存语料里所有“用错尺子”的例子抽出来，补 C-03。

## 候选（signal，未准入）

- **多 agent 交接失败（ZS Associates, AI Engineer 2026-07-23）**：四 agent + orchestrator 找到正确原因却建议错动作；重建为确定性检测 + 单 agent 判断 + KG 控制面。按 material gate 判 `signal`（会议主 track 不算信号、公司案例、无独立复现），**不撑 L/交付物**；只作线索。URL: https://ai.engineer/talks/u6jJcIFDLE4-why-we-killed-our-multi-agent-pipeline
