---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-08
arxiv: 2610.35267
title: Before Blaming the LLM, Diagnose the Workflow: A Role-Level Difficulty Profile for Translating Natural Language into Ontology-Grounded Statements
authors: Liang Zhang, Benoît Daireaux, Sergey Alyaev（NORCE）
pdf: 2610.35267-diagnose-workflow.pdf
direction: 3
home: topics/06-measure
subtopic: failure-attribution
updates:
  - topics/06-measure/failure-attribution/README.md
  - topics/06-measure/claims.md
  - topics/06-measure/sources.md
  - topics/conclusions.md
---

# Before Blaming the LLM, Diagnose the Workflow: A Role-Level Difficulty Profile for Translating Natural Language into Ontology-Grounded Statements · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

把 NL→本体接地 DSL 的失败从「模型弱」重新归因到**工作流**：五个角色（Input / Generator / Output / Validator / Repairer）+ 七个诊断变量，每项给问题、证据、重设计杆；用一个钻井 ABox 例子展示「语法对、语义不足」的失败。

## 问题与设定

- **问题**：ontology-grounded ABox DSL 生成中，**语法有效比语义充分容易**；失败常被归因于 generator 模型，但结构性的输入不足、上下文缺失、模板/词汇缺口、校验弱、非局部修复也会造成同样表现。
- **任务**：自然语言描述 → 本体词汇下的 ABox 断言（不是 TBox 构建）。
- **例子系统**：钻井信号 ABox DSL（DWIS/DDHub 风格）；原型本体快照约 **2,250 个类声明、200 个对象属性声明**。
- **性质**：**position paper / 经验框架**；没有量化评测，没有跨系统实验；七变量非穷尽、非正交。
- **能证明**：框架能把一个笼统的「语义不太对」拆成角色级、可改设计的具体问题。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 机制/设定 | digest §1–3；原文见 `paper.md` |
| 关键数字 | §4.2 / §5 |
| 图表 | 见下表 / `figures/` |
| 判断/工程用法 | [digest.md](./digest.md) |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| `fig-1-workflow-roles.png` | — | 见 digest 图注 | ✓ |

## 作者自述局限

- 定性诊断，不预测性能、不比较模型、不证明一条 pipeline 优于另一条。
- 七变量非穷尽、非正交；低 context 会放大 grounding complexity，弱 template fit 会与 vocabulary coverage 交互。
- 没有经过严格的量化验证；需要更多 case study 看不同实践者是否给出相似 profile。
- 角色级判断可能有评估者差异。
- 假设本体至少部分可用；完全从零构建本体不在范围内。

## 原文

- PDF：同目录 `2610.35267-diagnose-workflow.pdf`
- arXiv:2610.35267
