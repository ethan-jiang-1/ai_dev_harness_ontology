# 输出后判定 · 发现（F）

> 只放已经能站住的判断。`F` 编号是子主题局部编号；跨页引用写 `checker/Fx`。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 三种本体来源在漏检/误报上无单一向优 | 已核 |
| F2 | curated 真实答案 precision 仅略优于随机；FA 主源是 declaration/domain-range，不是「与数据矛盾」 | 已核 |
| F3 | 空结果重试是强基线；ontology check 必须先超过它 | 已核 |
| F4 | curated + data-derived 组合无净收益 | 已核 |
| F5 | specific feedback 修复更多，但 corrupt 也更多 | 已核 |
| F6 | LLM judge 检错更多，但修坏多于修好；不能默认更好 | 已核（单图比较器） |

## F1 · 三源权衡

- **判断**：curated 抓得多、FA 高；data-derived FA 低、catch 低；LLM 生成不稳定。
- **数字（真实答案，UniProt，3,383 可检查；catch/FA）**：curated 18.9/16.8；data-derived 8.2/3.5；LLM masked 5.0/1.8；空结果重试 2.5/0.1。
- **precision 单列（人工故障 + 25% 错答案假设，不是真实答案口径）**：curated 57.1、data-derived 72.3、LLM masked 93.7、空结果 100。
- **条件**：5 图、7 模型、210 题 ×3 attempts；UniProt confirmatory。
- **边界**：其他图 exploratory；private 只报率。
- **工程含义**：data-derived summary 规模按 1–2 万实体估，超过就分域重建；重建频率与部署抽样是工程配方，不是论文测量（`推测`；见 [mechanism](./mechanism.md) 建库参数）。
- **来源**：Table 2, p.7；§5 RQ1。

## F2 · curated 不是权威

- **判断**：curated 在真实答案上的 precision 只略高于同率随机 flag（+1.6 点，CI −2.3~+6.3，跨零）；57.1% 是人工故障 + 25% 错答案假设下的 precision，不是真实答案口径。
- **FA 归因**：curated 的 FA 主源是 domain/range 与 declaration check（C3：curated 与 masked LLM 的人工故障 FA 差异，由这两类承担；盲审 32 个 FA 的双标注一致项中，undeclared term 17、closed-world 11，data clash 0；Table 6 / Appendix D.1）。「curated schema 与自身数据矛盾」是 Table 5 的独立观察，不是 FA 主因；审计仍必要，但不能拿它解释 FA。
- **对照**：data-derived 真实答案 precision 29.9%，比同率随机 flag 高 +14.4 点；但它 catch 只有 8.2%。
- **数字**：14.3% Linked Data triples 使用未声明属性（外部 crawl 统计，非本文测量）；每个缺失声明会经 declaration check 误报用到它的正确答案。
- **工程含义**：上线前先自动补声明（domain/range），补不了的进人工队列；审计 Table 5 的矛盾，但不要把它当 FA 主因。curated 审计工期未测——`1–2 人日` 是 data-derived setup 的估算，不能挪到 curated（`推测`；见 [mechanism](./mechanism.md)「curated 审计」）。
- **条件**：precision 数字：UniProt curated；真实答案 + 人工故障（precision 口径）。FA 归因：32 条盲审样本（四个公开图）+ C3 消融（curated vs masked LLM）。
- **边界**：不是所有 curated 本体都矛盾；需审计。盲审样本小，FA 归因不是全量分解。
- **来源**：Table 2/3/5/6, p.7–8；Appendix D.1/D.2；digest §5 第1条、§6.1 第2条。

## F3 · 空结果基线

- **判断**：查询返回空就重试，不需要本体；人工 fault 上 catch 79.2%、FA 0%；真实答案 catch 2.5%、FA 0.1%。
- **含义**：ontology check 只有抓到「空结果重试抓不到」的错，才有增量价值。
- **来源**：Table 2, p.7；§5 RQ1。

## F4 · 组合无净收益

- **判断**：curated + data-derived 组合 catch 19.5%、FA 17.8%；比 curated 单用只多 0.6 点 catch，却多 1.0 点 FA；C4 无净收益。
- **条件**：UniProt；同一 compiler；组合策略。
- **来源**：Table 2/3；§5 RQ3。

## F5 · feedback 的双刃

- **判断**：specific feedback 修复 28.3% flagged wrong，但 corrupt 1.0% flagged correct；generic 是 20.2% / 0.2%；C5 最终准确率差异未确立。
- **含义**：specific 的净修复更高（28.3% vs 20.2%），但 corrupt 也更多（1.0% vs 0.2%）；C5 最终准确率差异未确立（0.2，CI −3.2~3.1），不能默认 generic 更安全。未验证前先 generic 是风险默认，不是安全结论（`推测`）。
- **来源**：Table 2/3, p.7；§5 RQ3。

## F6 · LLM judge：检错更多，但修坏多于修好

- **判断**：UniProt 真实答案上 LLM judge catch 40.3%、FA 16.2%、precision 31.3%；catch 高于 curated（18.9）与 data-derived（8.2），FA 与 curated（16.8）接近、高于 data-derived（3.5）。人工故障上，curated/data-derived/masked LLM 对 changes of meaning 的 catch 是 0%（Table 4）；judge 能抓这类语义错（它判定的 41 个 changes of meaning 全抓到；Appendix C.2）。
- **代价**：把 flag 当行动信号后，40 条修好 / 83 条修坏（Table 11）。人工故障（有题面文本的 2,238 条）上 catch 98.7/98.0（Sonnet/Haiku），但会把 30–38% 答案仍正确的故障查询 flag。
- **含义**：检错多不等于净收益；judge 每条答案要一次模型调用，成本/稳定性未测。不能默认 judge 更好；也不能只凭 corrupt>fixed 判它无用——需在目标错误分布上测净修复（fixed − corrupted）；这是部署判断（`推测`）。
- **条件**：UniProt 主表；Appendix C.2 比较器；真实答案由 agent 自己的模型扮演，人工故障由 Claude Sonnet 5.5 / Haiku 5.5 扮演。
- **边界**：单图为主；成本/稳定性未做头对头。
- **来源**：Appendix C.2, Table 11；§6 Discussion；digest §6.5 部署度量。
