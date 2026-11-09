---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-09
arxiv: 2610.11768
title: Narrow and Deep: An Ontology Tower as the Knowledge of an LLM Agent for an Industrial Equipment System
authors: Younghwan Joo, Sung-il Kim（韩国能源研究院）
pdf: 2610.11768-narrow-and-deep.pdf
direction: 4
home: topics/03-knowledge
subtopic: projection
also_supports: []
evidence_role: execution-test
execution_form: context
updates:
  - topics/03-knowledge/projection/README.md
  - topics/03-knowledge/claims.md
  - topics/03-knowledge/sources.md
  - topics/domains.md
  - topics/conclusions.md
---

# Narrow and Deep: An Ontology Tower as the Knowledge of an LLM Agent for an Industrial Equipment System · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

把**单个设备系统**的知识做成「窄而深」的本体塔（测点 + 绑定 + 假设 + 物理推导 + 运行教训），投影成约 45k 字符文本放进 prompt；在真实低湿空气处理试验台上，9 个预注册任务、4 个 9B–750B 模型：避坑率 0.605→0.802，**投影 > 查询工具 > 文档检索**；但增益集中在「答案基本写在文本里」的任务，物理推导未被测。

## 问题与设定

- **问题**：工业设备 agent 需要的是**少数实体、深知识**（值怎么推导、依赖哪些假设、运行中发生过什么），而 Brick/SAREF 等建筑本体是**多实体、浅描述**；知识以什么形式供给 agent 没有被测过。
- **对象**：真实低湿空气处理试验台（带 PLC，商用除湿转轮/空调箱/冷水机），多个研究组每天使用。
- **任务**：9 个从运行记录回放的任务——5 个读数解释 + 4 个真实事故诊断；每个任务定义 ground-truth 元素与「最可能的误判」（primary trap）。
- **条件**：K0 地址级、K1 标签级、K2 投影文本、K3 流程摘要、K4 日志检索；另 K4x（去掉本事故记录）、K2-sub（文档检索替代投影）、K3-sub、scrambled-order、K2-json、K2-tool。
- **规模**：1,304 trials；4 个 open-weight 模型（Qwen3.5-9B / gemma-4-31B-it / EXAONE-4.5-33B / GLM-5.2 ~750B）；60 steps / 1,500 s per trial；LLM judge gpt-5.6-sol，第二 judge claude-opus-5-5，κ=0.819；作者与 judge κ=0.696。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 机制/设定 | digest §1–3；原文见 `paper.md` |
| 关键数字 | §3.1 / Table 2 / §3.3 / §3.4 |
| 图表 | 见下表 / `figures/` |
| 判断/工程用法 | [digest.md](./digest.md) |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| `fig-1-ontology-tower.png` | — | 见 digest 图注 | ✓ |
| `fig-3-avoidance.png` | — | 见 digest 图注 | ✓ |
| `fig-5-five-trajectories.png` | — | 见 digest 图注 | ✓ |

## 作者自述局限

- 一个 plant、九个任务、四个模型；投影的增益是在「答案基本写在文本里」的任务上测的。
- 三个预注册假设之外，其余比较、教训形式实验、live runs 都是探索性的，每格 trial 很少。
- 塔的物理推导没有被测；任务不要求推导量。
- 文本投影不能追溯来源；查询工具能，但不是所有模型都会用。
- 预注册评分规则改过一次；作者与 judge 的一致性 κ=0.696，略低于 0.7 门槛。

## 原文

- PDF：同目录 `2610.11768-narrow-and-deep.pdf`
- arXiv:2610.11768
