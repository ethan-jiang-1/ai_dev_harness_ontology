# 校准 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `calibration/Fx`。证据等级见 [conventions](../../../meta/rules/conventions.md#证据等级)。

## 索引
> **2026-11-12 对账（等级以 README 为准）**：本页索引里的「已核」是**撤源前**的记录；支撑它的来源已按 [CHARTER §4](../../../CHARTER.md#4-素材准入material-gate) 移出，这些条目现等级见 [README](./README.md)（多已降 `推测`/`withdrawn`）。**引用请用 README 的等级，不要用本页索引的历史等级。**


| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 先分 catch/FA；precision 必须带错误率假设 | 已核 |
| F2 | 空结果重试是基线；只有增量 catch 才值得付费 | 已核（基线）/ 推测（5pp 门） |
| F3 | 接地等级是自评切片，不是校准曲线 | 已核（数字）/ 推测（stop） |
| F4 | 成本按 per-flagged；FA 放大重试与修复成本 | 已核 |

## F1 · 口径：catch/FA 与 precision 的错误率条件

- **判断**：判定器的校准先对齐口径：catch 与 FA 分开报；precision 是部署错误率 p 的函数，不能脱离 p 引用。
- **真实答案（UniProt，3,383 可检查）**：curated catch 18.9% / FA 16.8%；data-derived 8.2% / 3.5%；masked LLM 5.0% / 1.8%；空结果重试 2.5% / 0.1%。
- **precision（人工故障 + 25% 错答案假设）**：curated 57.1、data-derived 72.3、masked LLM 93.7。p=25% 是分析设定，不是部署分布；不能与真实答案 catch/FA 拼表。
- **公式**：`precision(p) = p·catch / (p·catch + (1−p)·FA)`；p 为部署集错答案占比。真实答案 precision 论文未直接给；把 18.9/16.8 硬套 p=25% 会得约 27.3%，但这是反推，不是论文报告值（digest §4.1）。
- **随机基线**：curated 真实答案 precision 仅比同率随机 flag 高 +1.6 点（CI −2.3~+6.3，跨零）；data-derived 29.9%（+14.4 点），但 catch 只有 8.2%。
- **工程含义**：报告必须同时带 p、catch、FA、n；否则 precision 不可比。看到 57.1% 先问「p 是多少、人工故障还是真实答案」。
- **条件**：UniProt confirmatory；5 图 7 模型；人工故障 9,753 条 + 正确 control 3,630 条。
- **边界**：其他图 exploratory；private 图只报率；25% 错答案是分析假设，不是真实 agent 错误分布。
- **来源**：Table 2/3, p.7；§5 RQ1；digest §3.1、§4.1、§5 第 1 条。

## F2 · 空结果基线：先证明增量

- **判断**：空结果重试不需要本体，是强基线；ontology check 只有抓到「空结果重试抓不到」的错，才有增量价值。
- **数字**：人工 fault 上空结果重试 catch 79.2%、FA 0%；真实答案 catch 2.5%、FA 0.1%。同为人工 fault，curated 60.1% / FA 15.0%、data-derived 75.6% / 9.7%，都低于空结果基线。
- **增量口径**：同一批题上 `增量 catch = catch(checker) − catch(空结果重试)`；优先限定在「查询仍有结果但答错」的子集，因为空结果重试对这类错误几乎为 0（它的人工 fault catch 高，靠的是让查询返回空的那部分故障；rows returned 上 catch 0.0%）。
- **门**：增量 catch <5pp → 停（digest §6.5 工程配方，非论文测量；`推测`）。
- **含义**：先跑基线，再叠 checker；否则只是多一次重试、多一份 token。
- **条件**：UniProt；人工故障与真实答案分开报；79.2% 是人工 fault，不是真实 agent 错误。
- **来源**：Table 2, p.7；§5 RQ1；digest §4.2、§6.5。

## F3 · 接地等级：切片不是校准曲线

- **判断**：OA-RAG 的四级 grounding（entailed/supported/related/unrelated）是有正确率切片的序数信号，不是概率校准；不能把 entailed 当「一定对」。
- **数字**：Qwen Test 3：entailed 94.9% 正确、supported 82.1% 正确；entailed+supported 占 70.0%（Llama）/ 53.2%（Qwen）；unrelated 0.2% / 7.8%。
- **条件**：GO/FoodOn/SNOMED 三个生物医学本体、六个医学 QA 任务；等级由模型在 answering 阶段自报，作者明确不提供形式正确性保证。
- **边界**：只给切片正确率，没有每级 precision/recall、没有阈值扫描、没有跨域；不能推出「entailed ≥ x% 就自动放行」。
- **stop**：entailed+supported 占比 >90% → 抽样校准，不自动放行（OA-RAG digest §6.5 工程配方；`推测`）。
- **工程含义**：等级当路由/抽检触发器；要定阈值，先独立标注每级样本，算每级 precision + CI。
- **来源**：OA-RAG digest §3.3、§4.3、§6.5。

## F4 · 成本：per-flagged，不是 per-answer

- **判断**：checker 成本按「被 flag 的答案」计；FA 越高，重试/修复越多，per-1k 成本随之放大。
- **数字**：curated 65,976 tokens / 46.0 s（median，per flagged）；data-derived 28,076 / 17 s。LLM ontology 生成 <$1/个；data-derived setup 未记录；curated setup/维护未测。
- **公式**：`flag_rate(p) = p·catch + (1−p)·FA`；`per-1k cost = flag_rate × per-flagged cost × 1000`。先测 flag_rate；不能把 66k 当每答案成本，也不能只用 FA 代替 flag_rate。
- **修复破坏**：curated specific feedback 修复 28.3% flagged wrong、corrupt 1.0% flagged correct；generic 20.2% / 0.2%；C5 最终准确率差异未确立（0.2，CI −3.2~3.1）。judge 分支检错更多但修坏多于修好（checker/F6；digest §6.5），计数见其 findings。
- **含义**：FA 不只是「多标一个」；它触发重试与修复，可能把对的改错。报成本要同时报 per-flagged、flag_rate、修复破坏。
- **条件**：UniProt；成本是 median per flagged，不是所有图/模型；修复破坏的工时未测。
- **边界**：`<$1` 是 LLM ontology 的生成成本，不是 data-derived，也不是维护成本。
- **来源**：Table 2/3；Table 8 / Appendix B.3；digest §4.3、§4.4、§6.2；judge 分支见 checker/F6。
