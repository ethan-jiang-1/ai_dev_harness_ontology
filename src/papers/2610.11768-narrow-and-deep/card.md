---
status: draft
source_type: preprint
reading: 摘要级
provenance: 原文摘要
updated: 2026-11-07
arxiv: 2610.11768
title: Narrow and Deep: An Ontology Tower as the Knowledge of an LLM Agent for an Industrial Equipment System
authors: Younghwan Joo, Sung-il Kim（韩国能源研究院）
pdf: 2610.11768-narrow-and-deep.pdf
direction: 4
home: topics/03-knowledge
subtopic: projection
updates: []
---

# Narrow and Deep

## 做了什么

为**单个**工业设备系统建「本体塔」：窄而深，只覆盖一台设备，但知识沿两个方向加深——由物理关系从测点**推导**出的量，以及从运行日志里**提炼**出的教训节点。

然后在真实低湿空气处理试验台上，比较「塔投影成文本」与「塔做成查询工具」「文档放检索后面」三种交付形态。

## 结果（预注册）

- 投影文本把避坑率从 **0.605 提到 0.802**；odds ratio 5.45；Holm 校正 p = 6.0×10⁻⁷。
- 跨 9B–750B 四个开源模型均成立（element score 同向提升）。
- **交付形态决定效果**：塔做成查询工具只服务主动调用它的模型；文档放检索后面，「没有一个模型用得比投影文本好」。
- 操作经验写进塔里或作为记录放进提示时会被用；留在日志里则很少被用。去掉已并入的教训，element score 掉约 0.20。

## 没测什么

**作者自述**：单厂、9 任务、4 模型；物理推导部分未测；「增益是在**答案基本就写在文本里**的任务上测得的」。

**读者补充**：这条自述是最关键的限制——它把结论限定在「知识即答案」的任务形态。

## 对本仓库的意义

| 关联 | 关系 |
|---|---|
| E-12 | 一手依据：投影 > 查询 > 检索 |
| P1（价值在约束） | **限定**：在弱端（知识供给）也能测出真实增益，前提是任务形态匹配 |
| [projection](../../../topics/03-knowledge/projection/README.md) | 核心文献 |

## 待核

- [ ] 「记录只恢复了 23%」一说的完整数字
- [ ] element score 的具体定义
- [ ] 塔的规模（概念数、关系数）与投影长度
