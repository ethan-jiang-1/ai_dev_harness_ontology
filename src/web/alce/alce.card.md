---
status: draft
source_type: paper
reading: 摘要级
provenance: 原文摘要
updated: 2026-11-11
batch:
source: https://arxiv.org/abs/2305.14627
author: Tianyu Gao, Howard Yen, Jiatong Yu, Danqi Chen (Princeton NLP)
published: 2023-05-23
influence: EMNLP 2023；代码 github.com/princeton-nlp/ALCE；被后续引用评估工作普遍当作 baseline（引用数/采用清单 待核）
updates: []
---

# ALCE：带引用的生成与 citation quality 两轴

> **arXiv 论文卡，不是 digest，也不入 `papers/`**（未存 PDF/paper.md）；只作外部参照，引用时按「摘要级/待核」对待。读的是 arXiv 摘要与 HTML 正文的定义/协议段；**未逐字通读全文**，公式与实验表 `待核`。
> 只取 02 R4 用得到的三件事：citation correctness 怎么定义、怎么算、边界在哪。

## 它主张什么

1. **citation quality 拆成 recall 与 precision 两轴**：recall 判「这句陈述是否被它引用的段落整体支持」；precision 判「这条引用是否不相关」，不相关 = 单看它不能支持该陈述，且去掉它后其余引用仍能支持（反事实移除）。
2. **判定按句/按引用，不按文档**：句子切分后逐句判 recall；precision 逐条引用判，允许冗余引用，不要求最小引用集。
3. **可复现的自动代理**：用 NLI 模型（TRUE）判 `φ(concat(C_i), s_i)`；人工评估验证自动指标与人的相关性；代码公开。

## 场景与 scope

- **场景**：ASQA/QAMPARI/ELI5 等长答案 + 检索段落；英文。
- **管什么**：引用是否支持陈述；引用是否冗余/不相关。
- **不管什么**：不判「陈述本身是否为真」；不判「引用是否最小」；不覆盖「部分支持」——作者在附录自承二值 NLI 会忽略 partial support。
- **不外推**：NLI 判官在域外/多语言/长文档上的表现未测；它给的是**下限**，不是完备判定。

## 证据强度

- **一手还是转述**：arXiv 摘要与 HTML 正文（2026-11-11 抓取）；未读 PDF 全文/附录表。
- **有数据吗**：有自动指标与人工相关性实验；具体数字未抄，`待核`。
- **可复现吗**：代码公开；NLI 模型版本与数据预处理需按 repo 复现。
- **等级**：定义/协议 `已核（摘要）`；实验数字 `待核`；跨域外推 `推测`。

## 与已有判断的关系

| 结论/判断 | 关系 | 说明 |
|---|---|---|
| 02 R4「引用率 ≥85%」 | **边界** | R4 只测 citation presence；ALCE 测 citation correctness，两者不是同一个指标 |
| E-03（输出证据契约） | 支持（边界） | E-03 的 grounding 是答案 vs 上下文；ALCE 是陈述 vs 引用，粒度更细 |
| 02 R4 的「引用形式化」失效模式 | 支持 | ALCE 的 precision 正是为「引用了但不支持」设计的 |

## 待核项

- [ ] ALCE 的 NLI 判官具体版本与阈值
- [ ] 附录 E 关于 partial support 的原文
- [ ] 自动指标与人工相关性的具体系数
- [ ] 中文/长文档上的适用性

## 喂到哪个主题

- `deliverables/02-engineering-playbook/recipes/judgment.md` R4 的「citation 正确性」小节
- `topics/02-judgment/evidence/`（若后续需要）

## 原文摘录

> "citation recall, which determines if the output is entirely supported by cited passages"（摘要）

> "citation precision, which determines if each citation is relevant"（摘要；precision 的反事实定义见正文）

## 对照来源（未单独入档）

- AIS / Measuring Attribution in NLG：https://arxiv.org/abs/2112.12870（Computational Linguistics 2023；「According to P, s」的判定式）
- AttributionBench：https://arxiv.org/abs/2402.15089（Findings ACL 2024；自动判官约 80% macro-F1 的经验上限）
- Evaluating Verifiability in Generative Search Engines：https://arxiv.org/abs/2304.09848（Findings EMNLP 2023；人评范式与现实基线）

> 这三条只作对照，未逐条入档；引用时按「转述/待核」对待。
