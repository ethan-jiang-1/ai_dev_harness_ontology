---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-08
arxiv: 2611.03743
title: EvoMemState: Evolving Memory State for Personal Agents
authors: Zhishang Xiang, Yunbo Tang, Zhongqiao Liu, et al.（厦门大学等）
pdf: 2611.03743-evomemstate.pdf
direction: 4
home: topics/04-state
subtopic: memory
updates:
  - topics/04-state/memory/README.md
  - topics/04-state/claims.md
  - topics/04-state/sources.md
  - topics/conclusions.md
---

# EvoMemState: Evolving Memory State for Personal Agents · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

把长期记忆从「独立事实集合」改成**状态**：Persistent Facts + Relational State（有效性/scope/更新/冲突）+ Reasoning State（当前请求该用哪些、什么角色、什么优先级）；Relational State 由本体引导构造，Reasoning State 由 GRPO 训练的策略生成；四个记忆基准上一致提升。

## 问题与设定

- **问题**：fact-centric 记忆把每条事实独立存；相关事实的更新/冲突/约束不在一起检索，即使全部检索到，模型也未必知道怎么用。
- **两个 preliminary findings**：① 相关记忆经常没有一起被检索（MemoryBank/LightMem/Supermemory 缺 58–62%）；② 全部检索到也不保证正确使用；固定 self-reflection 反而使平均准确率 50.5→48.9%。
- **基准**：MemSyco-Bench（记忆使用：when/how to use、preference updates、conflicts）、MemTrapBench（安全/任务边界）、LoCoMo、LoCoMo-Refined（长对话回忆/推理）。
- **baseline**：9 个（NaiveRAG、MemGPT、MemoryBank、Mem0、LightMem、A-MEM、Supermemory、SimpleMem、PGMem）。
- **模型**：Qwen3-8B、GPT-4o-mini；离线构建 DeepSeek-V4Flash；策略初始化 Qwen3-4B-Instruct，GRPO 训练。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 机制/设定 | digest §1–3；原文见 `paper.md` |
| 关键数字 | §4.2 / Table 1 / §4.3 / Table 2 / §4.5 / §2.2 |
| 图表 | 见下表 / `figures/` |
| 判断/工程用法 | [digest.md](./digest.md) |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| `fig-4-pipeline.png` | — | 见 digest 图注 | ✓ |
| `fig-5-results.png` | — | 见 digest 图注 | ✓ |

## 作者自述局限

- 只测文本交互；多模态（文档/图片/用户 artifact）未覆盖。
- 策略训练（GRPO）需要 reward/答案；真实个人助手没有这个条件。
- 四个基准都是记忆使用/对话回忆，不是开放域长期部署。
- Relational State 的本体是增量构建的；概念层级质量依赖抽取。
- Reasoning State 是自然语言/结构化规则，不是可形式验证的保证。

## 原文

- PDF：同目录 `2611.03743-evomemstate.pdf`
- arXiv:2611.03743
