# 精化 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `refinement/Fx`。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 精化可自动化到小规模：high-confidence 6/6 接受 | 已核 |
| F2 | fine-tune embedding 是主要增益：100% vs 57.1% | 已核 |
| F3 | medium-confidence 全 mixed，必须人审 | 已核 |
| F4 | 「下游错误 → 该修哪条公理」未闭环 | 已核（缺口） |

## F1 · 小规模可自动化

- **数字**：CASTON 270 classes/292 subsumption；default high 6/6（100%）；pretrained 4/7（57.1%）。
- **条件**：单一本体、单一公理类型；2 专家 5 分制。
- **边界**：6 条高置信；preliminary。
- **来源**：Table 1, p.4；§3。

## F2 · embedding 是主要增益

- **判断**：fine-tuned OnT 100% vs pretrained ensemble 57.1%；GPT-4o mini high 31.3%。
- **含义**：不是「换更大 LLM」能补；任务特定 embedding 是关键。
- **边界**：跨本体 fine-tune 成本未测。
- **来源**：Table 1, p.4；§3。

## F3 · medium 不可靠

- **判断**：default medium 0/2（全 mixed）；pretrained medium 1/4；GPT-4o mini 1/5。
- **含义**：confidence 只能粗分；medium 必须人审。
- **边界**：校准是模型特定的。
- **来源**：Table 1, p.4。

## F4 · 下游未闭环

- **判断**：修复是否让判定器/应用变好，没测；「下游错误 → 该修的公理」没有通用答案。
- **含义**：精化质量 ≠ 下游收益；这是 05 的核心空缺。
- **来源**：CASTON §4；本仓库综合。
