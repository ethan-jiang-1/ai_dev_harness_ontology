---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-08
arxiv: 2610.37407
title: "Constraining the Commit Boundary: A DIO/ODI-Informed Authorization Guardrail for Agentic Entity Resolution"
authors: Daniel Beránek
pdf: 2610.37407-commit-boundary.pdf
direction: 1
home: topics/01-constraint
subtopic: commit-gate
updates:
  - topics/01-constraint/commit-gate/README.md
  - topics/01-constraint/claims.md
  - topics/01-constraint/sources.md
  - topics/conclusions.md
---

# Constraining the Commit Boundary: A DIO/ODI-Informed Authorization Guardrail for Agentic Entity Resolution · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

把**「推理时可用的证据」**与**「有权授权持久化身份变更的证据」**分开：`UNVERIFIED` 只表示可进 Planner 推理，不等于授权资格；需要 claim-specific promotion；两阶段 supervisor 只在所有必需命题都有授权证据、冲突已解决、scope/version 有效时允许 commit。

## 问题与设定

- **问题**：agentic entity resolution 中，错误身份假设会条件化后续检索，检索结果又像「确认」；如果这些证据直接授权图变更，初始错误会自我强化。
- **核心区分**：`P_active`（Planner 可用）≠ `P_auth(q_m, ω)`（claim-specific 授权资格）。
- **性质**：**概念架构，无实现、无实证**。作者明确写 "conceptual architecture without implementation or empirical validation"。
- **能提供**：一套可审计的接口契约与状态语义（PASS/BREACH/UNKNOWN_EVIDENCE），以及条件性保证。
- **不能提供**：不阻止错误假设、不消除 hypothesis-conditioned retrieval、不证明 promotion 正确或语义真值。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 机制/设定 | digest §1–3；原文见 `paper.md` |
| 关键数字 | 见 digest §4 |
| 图表 | 见下表 / `figures/` |
| 判断/工程用法 | [digest.md](./digest.md) |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| `fig-1-architecture.png` | — | 见 digest 图注 | ✓ |
| `fig-2-evidence-flow.png` | — | 见 digest 图注 | ✓ |

## 作者自述局限

- **无实现、无实证**；所有保证是条件性的。
- 不阻止错误假设，也不消除 hypothesis-conditioned retrieval。
- Dependency-aware evidence flow（假设→查询→观察→claim 的完整依赖）**不在架构内**，是 future research。
- Promotion correctness、domain policy adequacy、validator 正确性都依赖外部；架构不能保证语义真值。
- 不保护 unmanaged write path；不保护系统性 misclassification / false authoritative source。
- 没有量化评估；第 8 节只是 proposed evaluation protocol。

## 原文

- PDF：同目录 `2610.37407-commit-boundary.pdf`
- arXiv:2610.37407
