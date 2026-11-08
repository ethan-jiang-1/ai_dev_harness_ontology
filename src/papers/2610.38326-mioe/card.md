---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-08
arxiv: 2610.38326
title: Can LLMs Faithfully Solve Ontology Engineering Tasks? A Mechanistic Interpretability Study
authors: Bohui Zhang, Albert Meroño-Peñuela, Elena Simperl
pdf: 2610.38326-mioe.pdf
direction: 3
home: topics/06-measure
subtopic: mechanism
updates:
  - topics/06-measure/mechanism/README.md
  - topics/06-measure/claims.md
  - topics/06-measure/sources.md
  - topics/conclusions.md
---

# MIOE · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

本体预测在内部是因果可干预的，但不能与类别辅助信息干净分离；正确输出不等于内部有一个干净、模块化的本体机制。

## 问题与设定

- 问题：行为正确率不能证明模型内部在算本体关系；需要因果干预。
- 任务：entity typing（instance of）/ subsumption（subclass of）。
- 数据：54 classes/1,099 subjects/376 attrs/4,288 prompts；39/1,113/160/2,095。
- 模型：Qwen3-8B、Qwen3-4B；36 层。
- 方法：SAE、DBM、MDBM、DAS、MDAS；单层 36 层 + 2/4 层窗口。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 任务/因果抽象定义 | §3, p.2–4 |
| 方法 | §4, p.4–5 |
| 单层主结果（C/I/D） | Table 2, p.6 |
| 多层窗口 | Table 3, p.7 |
| 层剖面 | Fig. 1, p.6 |
| Cause–Iso 平面 | Fig. 2, p.6 |
| 类级分析 | Fig. 3, p.7 |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| Fig. 1 | p.6 | Cause/Iso/Disentangle 层剖面 | ✓ |
| Fig. 2 | p.6 | Cause–Iso 平面 | ✓ |
| Table 2 | p.6 | 单层最佳配置 | — |
| Table 3 | p.7 | 多层窗口 | — |

## 作者自述局限

- 只 Qwen3-4B/8B；只 entity typing/subsumption。
- 干预位置只有 subject-token residual stream。
- 聚合分数掩盖类级差异；“部分分离”可能是表示纠缠，也可能是方法不够强。
- 无下游/部署评估。

## 原文

- PDF：同目录 `2610.38326-mioe.pdf`
- arXiv:2610.38326
- 代码：https://github.com/King-s-Knowledge-Graph-Lab/MIOE
