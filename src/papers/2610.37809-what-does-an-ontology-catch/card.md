---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-08
arxiv: 2610.37809
title: What Does an Ontology Catch? Curated, LLM-Generated and Data-Derived Ontologies as Checkers of LLM Agents over Knowledge Graphs
authors: Michal Orzechowski, Rund Tawfiq, Tomasz Kosciolek
pdf: 2610.37809-what-does-an-ontology-catch.pdf
direction: 1
home: topics/02-judgment
subtopic: checker
updates:
  - topics/02-judgment/checker/README.md
  - topics/02-judgment/claims.md
  - topics/02-judgment/sources.md
  - topics/conclusions.md
---

# What Does an Ontology Catch? Curated, LLM-Generated and Data-Derived Ontologies as Checkers of LLM Agents over Knowledge Graphs · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

把「本体当判定器」本身作为研究对象：curated / LLM 生成 / 数据派生三种来源，分别作 prompt 上下文、作 checker、或两者兼用，在 7 个模型、5 个知识图上测「抓到了什么、误报了什么」；**curated 本体抓得多但误报最多，真实答案上的精确度只略高于随机**；数据派生本体误报少，但只抓到不到一成的真错；空结果重试是很强的基线。

## 问题与设定

- **问题**：LLM agent 用 SPARQL 答知识图谱问题；答案可以语法有效、执行无错、却答错。用图的本体做 checker 是常见做法，但 **checker 自己也会错**：漏检，或把正确答案标错、逼 agent「修」成错的。
- **图**：UniProt（4.0×10⁸ triples，confirmatory；curated 声明 domain/range/disjointness）、Rhea（5.5×10⁶，exploratory；只有类层级）、Rhea-masked（标识符替换为不透明 id）、Corporate（2.7×10⁴）、Private（~10⁹；只报率）。
- **本体来源**：curated（按发布原样）、data-derived（从数据总结；模式至少出现 5 次；无 disjointness）、LLM-generated（Claude Opus 5.5 从同一 summary + instance sample 写；另有 masked 变体）。
- **用法**：as context（渲染进 prompt）、as check（编译成 checker）、both。
- **模型**：7 个（Claude Sonnet 5.5 / Haiku 5.5；Qwen3.8-27B、Qwen3-Coder-30B-A3B、GLM-5.3-Flash、Gemma-4-31B、DeepSeek-V4-Flash）。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 机制/设定 | digest §1–3；原文见 `paper.md` |
| 关键数字 | Table 2 / Table 3 / Table 8 / §6 / §1 |
| 图表 | 见下表 / `figures/` |
| 判断/工程用法 | [digest.md](./digest.md) |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| `fig-1-setting.png` | — | 见 digest 图注 | ✓ |
| `fig-2-caught-missed.png` | — | 见 digest 图注 | ✓ |

## 作者自述局限

- 评估依赖知道每个问题的正确答案；真实使用没有这个条件。
- 人工故障可能不代表真实错误；真实 agent 错误很少，分布不均。
- 只有 UniProt 是 confirmatory；其他图是 exploratory，private 只报率。
- 三个注册的 source sensitivity 与 selective check 没跑。
- curated 本体的 setup 成本没有测；data-derived 的生成成本 <$1。
- 检查器不支持 UNION/subquery，返回 unknown；这会影响覆盖率。

## 原文

- PDF：同目录 `2610.37809-what-does-an-ontology-catch.pdf`
- arXiv:2610.37809
