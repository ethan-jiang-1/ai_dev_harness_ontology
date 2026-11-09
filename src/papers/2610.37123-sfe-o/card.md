---
status: draft
source_type: preprint
reading: 摘要级
provenance: 原文摘要
updated: 2026-11-09
arxiv: 2610.37123
title: SFE-O: An Ontology for Knowledge-Grounded AI in Supercritical CO2 Biomass Extraction and Fractionation
authors: Thomas Pallet, Mario Lezoche, Gianpaolo Leone, et al.
pdf: 2610.37123-sfe-o.pdf
direction: 2
home: topics/05-produce
subtopic: representation
also_supports: []
evidence_role: boundary-ruler
execution_form: none
updates: []
---

# SFE-O

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 做了什么

超临界 CO₂ 萃取领域的 OWL 2 本体，围绕 Biomass / Process / Product 三维建模，显式表达过程拓扑、**参数溯源**、传质机制。

一个工程域本体的完整样本：概念、关系、约束，加一个端到端用例。

## 结果

无量化结果。但给出了极其有用的**局限清单**：

- 数值依赖**不在 OWL 里求解**。
- 约束尚未成为可执行的 SHACL shapes。
- 热物性、扩散系数等外部服务仍是集成点。
- 有效扩散系数需要生物质特定假设。

还有一组**数据层矛盾**，作者选择显式标记而非静默消解：界面面积公式两处不一致（`a = 6/dp` vs `a = dp/6`）、床体积表达式疑似缺一个几何因子、一个 ChEBI 标识符被两种脂肪酸共用。

## 没测什么

**作者自述**：局限「在执行而非表示」。

**读者补充**：无下游 agent 任务评估——它证明了「可以这样建」，没证明「这样建有用」。

## 对本仓库的意义

| 关联 | 关系 |
|---|---|
| 05 生产派 | 领域建模范本 |
| 02 判定派 | 「显式标记冲突」与 Commit Boundary 的「冲突清才放行」是同一条原则的两端 |
| [representation](../../../topics/05-produce/representation/README.md) | 反证：形式化不是瓶颈，执行才是 |

## 待核

- [ ] 「参数溯源」的建模方式（值得抄）
- [ ] SHACL 化之后的约束覆盖

## 原文

- PDF：同目录 `2610.37123-sfe-o.pdf`
- arXiv:2610.37123
