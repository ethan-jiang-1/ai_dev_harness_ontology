---
status: draft
source_type: standard
standing: normative
admission: admitted
gate: standard-in-force
gate_checked: 2026-11-11
impact_evidence: I1 标准组织（OMG，1998 年起为 ISO/IEC JTC 1 PAS submitter）；I2 多主体（88solutions / Adaptive / Airbus / Dassault 等贡献）；I3 采用（FIBO、RIO、MVF、LCC、API4KP 将其列为上游可复用库，待核具体条款）
liveness: 1.3 formal，2026-06 发布；贡献者版权 2024–2025
reading: 摘要级
provenance: 原文摘要
updated: 2026-11-11
batch: 2026-11-11 基线批
source: https://www.omg.org/spec/Commons/1.3/
author: Object Management Group
published: 2026-06
updates: []
---

# OMG Commons Ontology Library 1.3

> 标准卡。读的是 OMG 规范目录页与 About 摘要；**未读规范正文**，模块清单与条款号 `待核`。
> 用途：给「可复用本体模块」「最小承诺」这两个说法一个 `normative` 锚，并说明它与顶层本体、领域本体的关系。

## 它定义什么

1. **一组小本体**（a set of small ontologies），提供可跨建模与数据环境复用的构造，且**承诺最小**（minimal commitments）——不强迫使用者接受一整套世界观。
2. **可扩展**：新本体、甚至对应的 UML 模型，可以按跨域需求加进来；需求来源包括 OMG 的其他规范（MVF、LCC、API4KP）与领域规范（RIO、FIBO）。
3. **模块化组织**：按主题拆成小模块（具体模块清单 `待核`），而不是一个大而全的企业本体。

## 它不定义什么

- **不是顶层本体**：不替代 BFO/DOLCE/TUpper；它假设上层已有 TLO，自己补中层/通用概念。
- **不定义领域语义**：行业词（金融、零售、工业）留给 FIBO、RIO 等领域本体。
- **不规定建模方法**：不管你怎么建、怎么治理、成熟度几级。
- **不保证跨库对齐**：用了 Commons 不等于两个本体自动一致；它只提供共同的最小承诺。

## 对我们的用法

- **「可复用模块」的锚**：我们说「本体塔要分层、要可挂载」时，可以引 Commons 的 minimal-commitment 设计，而不是自造「技能包」式的比喻。
- **判「divergent」**：如果我们的「本体」暗含「一个大而全的模型」，与 Commons 的模块化+最小承诺相反——这是 `divergent`，要改。
- **边界**：Commons 是「通用概念库」，不是「企业知识图谱」；不能拿它证明 EKG 的成熟度或效果。

## 证据强度

- **一手还是转述**：OMG 规范目录 + About 摘要；正文未读。
- **等级**：
  - 版本、状态、日期、贡献者——`已核`（OMG 页面）。
  - 「FIBO/RIO/MVF/LCC/API4KP 采用」——About 自述，`待核` 具体引用位置。
  - 模块清单——`待核`。

## 与已有判断的关系

| 结论编号 | 关系 | 说明 |
|---|---|---|
| —（05/03 暂无对应 L） | 新锚 | 给「可复用本体模块」「最小承诺」提供 `normative` 锚；不改变现有 E |

## 待核项

- [ ] 模块清单与各模块范围
- [ ] FIBO/RIO 引用 Commons 的具体条款
- [ ] 1.3 相对 1.2 的变更
- [ ] 是否有 ≥2 个独立实现（非 OMG 成员）

## 喂到哪个主题

- `GLOSSARY`：可复用本体模块 / 最小承诺
- `topics/05-produce`：本体分层的规范化依据
- `meta/term-baseline.md`：差异表 v0

## 原文摘录

> The Commons Ontology Library provides a set of small ontologies designed to provide a useful set of modeling constructs that are reusable in different modeling and data deployment environments with minimal commitments. It is intended to be extensible such that new ontologies and potentially other models (for example, UML models corresponding to the ontologies) can be added as cross-domain requirements present themselves.
