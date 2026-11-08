---
status: draft
source_type: preprint
reading: 精读
provenance: 原文正文
updated: 2026-11-08
arxiv: 2610.40482
title: "FIRME: Registry-Anchored Memory Graphs for Evolving, Heterogeneous Investor Knowledge"
authors: Yunbai Zhang, Yunyi Gao, Han-Tai Shiao（Vanguard）
pdf: 2610.40482-firme.pdf
direction: 4
home: topics/04-state
subtopic: memory
updates:
  - topics/04-state/memory/README.md
  - topics/04-state/identity/README.md
  - topics/04-state/claims.md
  - topics/04-state/sources.md
  - topics/conclusions.md
---

# FIRME: Registry-Anchored Memory Graphs for Evolving, Heterogeneous Investor Knowledge · 来源卡

> **这是来源卡，不是消化正文。** 机制、数字、判断、工程用法都在同目录 [digest.md](./digest.md)；下游默认只读 digest。

## 一句话（作者主张）

把投资人的跨源、跨期观察锚定到**持久关系身份**：registry 保存 canonical 身份 + learned aliases，短期做产品/主题本体介导的证据融合，长期用确定性强化/衰减与五态生命周期维护关系历史；alias memory 让 final-period CMR 提升 7.8–12.1 pp。

## 问题与设定

- **问题**：同一投资人/产品/主题在不同来源、不同时期以不同名字出现；不锚定身份，关系历史会碎成多个 partial history，证据无法累积，provenance 丢失。
- **数据**：① 专有投资人通话 + 月度组合现金流：10 个月度 period，每期约 1,200 calls；final period 约 1,300 calls / 10.3K incoming edges。② S&P 500 earnings transcripts：297 家公司、3 个 reporting period；final period 约 6.3K edges；**无结构化现金流**。
- **模型**：Claude Opus 4.6、GPT-5.4-mini；judge Gemini 3.1 Pro；human audit 200 incoming units per setting。
- **对照**：RAW、spaCy-Lemma、LLM-Norm、FIRME w/o Alias Memory、Full FIRME。
- **能证明**：alias memory 在 4 个 dataset–backend 设置上提升 CMR 7.8–12.1 pp；human audit CMR +9.0–16.5、reattachment recall +22.5–29.0；alias 复用降低 semantic matching token 40.3%。

## 机制 / 数字索引

| 想看 | 位置 |
|---|---|
| 机制/设定 | digest §1–3；原文见 `paper.md` |
| 关键数字 | Table 3 / §4.2 / Table 4 / Table 5 / §4.4 |
| 图表 | 见下表 / `figures/` |
| 判断/工程用法 | [digest.md](./digest.md) |

## 图表索引

| 图/表 | 页码 | 说明 | 已提取 |
|---|---|---|---|
| `fig-1-coupled-fusion.png` | — | 见 digest 图注 | ✓ |
| `fig-2-lifecycle.png` | — | 见 digest 图注 | ✓ |

## 作者自述局限

- 专有投资人数据与内部产品本体不可公开，限制复现。
- S&P 500 只有 transcript、无结构化现金流；只测抽取+时间对齐，不测完整异构融合。
- 两个 corpus 都不覆盖年度周期；seasonality/long-term 结论受限。
- human audit 是抽样（200 units/setting），不是全量；依赖 historical search/reference labeling。
- 产品-主题本体、$100K 阈值、生命周期参数都是 use-case specific；统一强化忽略关系类型/证据强度。
- **未匹配 ≠ 兴趣下降**：可能是输入缺失/没有观察机会；模型无法区分。

## 原文

- PDF：同目录 `2610.40482-firme.pdf`
- arXiv:2610.40482
