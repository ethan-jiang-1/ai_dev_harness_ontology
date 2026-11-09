---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# A · 建：从 CQ 到可消费本体

> 本章回答：怎么用 CQ/负例/评估把本体做到“下游能用”。 ｜ 读完你应该能：写出一份 `build_report`，而不是一版 OWL 文件。

## A.1 先定消费者和 CQ

**不要先建类层次。** 先写：

- 消费者是谁：agent、查询接口、checker、CI、人；
- 它要回答/拒绝什么；
- 3–10 个 CQ（competency questions），每个 CQ 对应一个可执行检查；
- 每个约束至少 1 个已知违反 + 1 个干净样本（负例）。

**没有 CQ/消费者/负例 → 停。** 这不是“本体工程”，是无法验收的文档工作。

## A.2 候选生成：LLM 只做候选

外部信号（未入库）：

- [Ontology Generation](https://arxiv.org/abs/2503.05388)：10 个本体、100 CQs、29 user stories；o1-preview + Ontogenia 能产出“专家可接受”的候选，但仍有常见错误与质量波动。
- [Axiom Benchmark](https://arxiv.org/abs/2512.05594)：9 个本体、17,118 triples、2,771 axioms；subclass F1 在 FOAF 0.642、music 0.218，整体不足以全自动。
- [LLM-assisted ontology evaluation](https://arxiv.org/abs/2507.14552)：1,393 CQs；LLM 自动 CQ 验证大致接近普通用户，不是专家。

**做法**：

1. 用 CQ + 领域样本生成候选类/属性/公理；
2. 每个候选必须有人审、来源、负例；
3. 只接受“能被执行/能被 CQ 验证”的候选，不接受“看起来合理”；
4. 记录候选生成器、prompt、模型、版本；否则无法复现。

## A.3 公理质量：先查“能触发”的错

按风险排序：

| 公理 | 先查什么 | 负例 |
|---|---|---|
| subclass | 子类是否过宽/过窄 | 一个应属于、一个不应属于 |
| disjoint | 是否把真实重叠类判互斥 | 一个合法重叠实例 |
| domain/range | 是否把合法数据判错 | 一个跨域但合法的实例 |
| cardinality | 是否把合法多值判错 | 一个多值实例 |

**度量**：不要只报“通过率”；报“已知违反检出 / 干净样本误报 / 人审接受率”。

## A.4 对齐与精化：候选 + 人审

- **对齐**（Agent-OM 等）：先 identifier/标签/结构，再语义；候选要能回指两侧本体。
- **精化**（CASTON 等）：embedding 取候选，LLM 给修复建议；high-confidence 6/6 接受，medium 0–25%，必须人审。
- **版本**：每次对齐/精化递增 `ontology_version`，保留 `supersedes`。

## A.5 评估：三种尺子分开

| 尺子 | 问什么 | 不能当什么 |
|---|---|---|
| CQ 验证 | CQ 能不能被执行/回答 | 语义正确性的形式证明 |
| reasoner/一致性 | 本体是否一致、可满足 | 业务正确性 |
| 人审 | 领域专家是否接受 | 可扩展的自动指标 |

**最低验收**：CQ 覆盖、负例通过、一致性、人审接受率、下游消费者加载；五项缺一项就不是“可消费”。

## A.6 数据契约：`build_report`

```text
{
  domain, ontology_version, source_version,
  consumers[], cqs[],
  classes, properties, axioms,
  negative_examples[],
  evaluation: {cq_coverage, violation_catch, clean_false_alarm,
               consistency, human_acceptance},
  provenance: {source, curator, date, supersedes},
  blockers[]
}
```

## A.7 停 / 反模式

- 没有 CQ/消费者/负例 → 停。
- LLM 候选未人审 → 停。
- 没有版本/来源 → 停。
- 下游消费者不加载 → 只算“文档”，不算“可消费本体”。
- 把 CQ 通过当语义正确 → 过度承诺。

## A.8 不能证明

- 生成本体跨域可消费；
- 公理 F1 能迁移到你的域；
- CQ 覆盖 = 业务正确；
- 人审接受率 = 下游效果。
