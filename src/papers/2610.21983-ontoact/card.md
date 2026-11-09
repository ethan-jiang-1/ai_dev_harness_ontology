---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-09
arxiv: 2610.21983
title: "OntoAct: Hypothesis-Based Neuro-Symbolic Agents through Ontological Abstraction"
authors: Donghyeok Lee, Bong Gyun Kang, Junyong Ahn, Sungroh Yoon（首尔大学）
pdf: 2610.21983-ontoact.pdf
direction: 4
home: topics/01-constraint
subtopic: reasoning-gate
also_supports: []
evidence_role: execution-test
execution_form: compiled
updates:
  - topics/01-constraint/reasoning-gate/README.md
  - topics/01-constraint/claims.md
  - topics/01-constraint/sources.md
  - topics/conclusions.md
---

# OntoAct: Hypothesis-Based Neuro-Symbolic Agents through Ontological Abstraction · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

**「LLM 提议，本体验证」**：把继承来的运行记录抽象成类型化的世界知识（实体类型、关系、条件公理），LLM 用它提出假设与动作，符号验证器按当前证据检查条件；在 Tacit-FLE、Mars、ALFWorld 上取得最高任务表现，并大幅减少无效干预。

## 问题与设定

- **问题**：agent 要在「操作原理只部分写明」的环境里行动；继承的日志/笔记记录了「发生了什么」，但没写「为什么有用、什么时候适用」（tacit operational knowledge）。
- **两个 gap**：① 从个案恢复可迁移的模式（类型/关系角色）；② 判断这些关系/条件在当前情境是否成立。
- **Tacit-FLE**：基于 Factorio Learning Environment 的工业维护基准；现有工厂 + 隐藏故障 + 固定维护记录/运行文档；3 种任务类型（chain / conjunction / elimination）、3 个规模（small/medium/large）。
- **其他环境**：Mars（8 个改机制世界，用 7 个 modified world 平均）、ALFWorld（134 unseen tasks）。
- **能证明**：类型化抽象 + 符号验证 + 假设 revision，在三个环境上同时提高成功率、减少无效干预、减少 LLM 调用/token。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 机制/设定 | digest §1–3；原文见 `paper.md` |
| 关键数字 | Table 1 / Table 2 / Table 3 / Table 6 / Table 5 |
| 图表 | 见下表 / `figures/` |
| 判断/工程用法 | [digest.md](./digest.md) |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| `fig-1-llm-proposes.png` | — | 见 digest 图注 | ✓ |
| `fig-4-success-si.png` | — | 见 digest 图注 | ✓ |

## 作者自述局限

- 评估使用**预定义 ontology schema 与固定的世界机制**；schema 学习/演化是 future work。
- Tacit-FLE 是合成环境；维护记录是生成的；不是真实工厂。
- Verifier 是 **auditability 的一步，不是 safety guarantee**；作者明确不声称可部署。
- Mars/ALFWorld 的收益依赖环境与 corpus；ALFWorld 只测 134 个未见任务。
- 知识构造成本与 evaluation tokens 分开报；构造开销不低。
- 三个环境都是模拟；真实工业的传感器噪声/缺失未覆盖。

## 原文

- PDF：同目录 `2610.21983-ontoact.pdf`
- arXiv:2610.21983
