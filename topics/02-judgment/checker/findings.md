# 输出后判定 · 发现（F）

> 只放已经能站住的判断。`F` 编号是子主题局部编号；跨页引用写 `checker/Fx`。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 三种本体来源在漏检/误报上无单一向优 | 已核 |
| F2 | curated 真实答案 precision 仅略优于随机；schema 可与数据矛盾 | 已核 |
| F3 | 空结果重试是强基线；ontology check 必须先超过它 | 已核 |
| F4 | curated + data-derived 组合无净收益 | 已核 |
| F5 | specific feedback 修复更多，但 corrupt 也更多 | 已核 |

## F1 · 三源权衡

- **判断**：curated 抓得多、FA 高；data-derived FA 低、catch 低；LLM 生成不稳定。
- **数字（真实答案，UniProt，3,383 可检查）**：curated 18.9/16.8/57.1；data 8.2/3.5/72.3；LLM masked 5.0/1.8/93.7；空结果 2.5/0.1/100（catch/FA/precision）。
- **条件**：5 图、7 模型、210 题 ×3 attempts；UniProt confirmatory。
- **边界**：其他图 exploratory；private 只报率。
- **来源**：Table 2, p.7；§5.3。

## F2 · curated 不是权威

- **判断**：curated precision 57.1%，相对随机 flag 只 +1.6 点（CI −2.3~+6.3）；一个按发布状态使用的 curated schema 可能与自身数据矛盾。
- **数字**：14.3% Linked Data triples 使用未声明属性；每个缺失声明会误报用到它的正确答案。
- **条件**：UniProt curated；真实答案。
- **边界**：不是所有 curated 本体都矛盾；需审计。
- **来源**：Table 3, p.7；§5.3。

## F3 · 空结果基线

- **判断**：查询返回空就重试，不需要本体；人工 fault 上 catch 79.2%、FA 0%；真实答案 catch 2.5%、FA 0.1%。
- **含义**：ontology check 只有抓到「空结果重试抓不到」的错，才有增量价值。
- **来源**：Table 2, p.7；§5.4。

## F4 · 组合无净收益

- **判断**：curated + data-derived 组合 catch 19.5%、FA 17.8%；比 curated 单用只多 0.6 点 catch，却多 1.0 点 FA；C4 无净收益。
- **条件**：UniProt；同一 compiler；组合策略。
- **来源**：§5.5；Table 3。

## F5 · feedback 的双刃

- **判断**：specific feedback 修复 28.3% flagged wrong，但 corrupt 1.0% flagged correct；generic 是 20.2% / 0.2%；C5 无显著差异。
- **含义**：specific 不是免费更好；没有验证前，generic 更安全。
- **来源**：Table 2/3, p.7；§5.6。
