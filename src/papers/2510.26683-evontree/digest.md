---
status: draft
updated: 2026-11-08
quality: B
based_on: card.md
claims: []
updates:
  - 2026-11-08: 补 Table 6 消融，核出规则边际只有 0.2–0.3pp（不能把 +2.1pp 归给规则）；按 gap/raw=0.91% 修正 sprint 抽样量（1 万 raw 只出 ~90 gap，与 gap<500 停线冲突）；安全阈值统一为 ≤2 / 2–5 / >5pp 三档；+1pp 出口补参照与 seeds/CI。
---

# Evontree：用本体规则找「知识缺口」，再用自蒸馏补回模型

> 这篇消化不假设你读过论文。先讲清它到底做什么，再给数字、边界和工程配方。**它不是「用本体当推理时约束」，而是训练侧的自演化。**

## 0. 三句话

1. **它问什么**：低资源专业域（医疗）里，模型有幻觉、缺领域一致性；能不能用少量本体规则，从模型自己抽出的本体里找「它不确定但事实正确的缺口」，再用自蒸馏补回训练？
2. **它怎么做**：从 15 个根概念让模型生成 JSON 本体树；用 **subclass 传递 + synonym 三角闭合** 两条规则筛出可靠三元组；用 `ConfirmValue`（基于困惑度的置信分）找低置信的 gap 三元组；只把 gap 用 LoRA 自蒸馏注入（implicit/mix），**explicit 模板注入效果差**。
3. **它发现什么**：Llama3-8B-Instruct **57.9→61.0（+3.1 绝对点，zero-shot，mix）**、Med42-v2 **63.5→67.2（+3.7 绝对点，SFT，implicit）**；相对各自最强 baseline 平均 +0.9 / +1.1 点。**但消融拆不出规则的功劳**：去掉两条规则只掉 0.2–0.3pp（Table 6），摘掉整个本体注入也只掉 0.6pp——+2.1pp 里绝大部分来自「挑低置信但正确的三元组 + 自蒸馏」这个动作，不来自本体规则本身。且只两个模型、单医疗域、自评、全文无方差报告。

## 1. 它解决什么问题

专业域数据少、标注贵；通用模型缺领域知识的一致性。推理时加约束（RAG/规则/检查器）每次都要带；训练侧注入则可能「内化」。

Evontree 的立场：**本体可以当训练信号**；但它不是让本体在推理时执行，而是用本体规则**筛选训练数据**。

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **self-evolution** | 模型自己抽知识 → 自检 → 自蒸馏，不依赖持续人工标注。 |
| **ontology tree** | 模型按根概念生成的 JSON 树：类、描述、子类、同义词。 |
| **ConfirmValue** | 用「True/False 两个续写的困惑度」算的置信分；越高越确信。 |
| **τ\*** | 每个模型×prompt 的确认阈值，用 Youden 指数 `J=TPR−FPR` 扫出来。 |
| **Confirmed / Reliable / Gap** | 高置信三元组 / 规则闭合后可靠的三元组 / 低置信但事实正确的缺口。 |
| **implicit / explicit / mix** | 自蒸馏 Q&A / 模板 Q&A / 两者混合的注入方式。 |
| **LoRA SFT** | 低秩适配微调；本文 lr 5e-5、3 epoch、fp32、bs 8、grad accum 2。 |

## 3. 它怎么做

### 3.1 抽本体

- 人工选 **15 个根概念**；prompt：`As a medical expert, please generate strict subclasses of {concept} and their synonyms. Output a JSON tree.` 深度 ≥3。
- 输出树：`{concept: {description, subclasses:[{name, description, synonyms[]}]}}`。

### 3.2 ConfirmValue

对每个三元组 `t` 和 prompt `p`，构造两个续写：`S_True = p + "True"`、`S_False = p + "False"`，算 Answer token span 的困惑度：

`ConfirmValue(t,p) = sign(PPL_False − PPL_True) / min(PPL_True, PPL_False)`

- synonym 用 5 个改写 prompt，subclass 用 4 个；**所有 prompt 都超过 τ\*** 才算 confirmed。
- τ\*：每个模型×prompt 在 [0,1] 扫，最大化 Youden `J=TPR−FPR`；用**约 1 万条 raw 三元组标定**（论文原话 `≈10k raw`）。**这 1 万条只是选阈值的样本，不是全量抽取量**——全文实际抽了 **15.4 万条 raw**（Table 2：synonym 95,814 + subclass 58,309）。两者混用会把 gap 量级算错一个数量级（见 §6）。

### 3.3 两条本体规则

- **subclass 传递**：`c1 ⊑ c2`、`c2 ⊑ c3` → `c1 ⊑ c3`；闭合三角确认可靠。
- **synonym 闭合**：同义词三角（A=B, B=C → A=C）确认可靠。
- 只保留规则闭合后可靠的三元组；再向外**传递外推**到更深层，得到 extrapolated；只保留 `ConfirmValue < τ*` 的 gap 三元组。

### 3.4 注入

- **explicit**：模板 Q&A（如「基于已知关系，能推出什么？」）→ 效果差，安全面掉点。
- **implicit**：自蒸馏 Q&A（让模型用自己的话解释类/子类/功能）→ 有效。
- **mix**：两者混合 → 有效。
- LoRA：LLaMAFactory，lr 5e-5、3 epoch、fp32、cosine、bs 8、grad accum 2。

## 4. 结果：数字与条件

### 4.1 本体统计（Table 2）

| 类型 | 关系 | 数量 | ConfirmValue 均值 | 准确率 |
|---|---|---|---|---|
| Raw | synonym | 95,814 | 0.0537 | 54.90 |
| Confirmed | synonym | 30,532 | 0.4738 | 87.51 |
| Raw | subclass | 58,309 | 0.2094 | 47.79 |
| Confirmed | subclass | 24,276 | 0.4896 | 72.62 |
| Reliable | subclass | 14,169 | 0.4981 | 74.81 |
| Extrapolated | subclass | 8,661 | 0.4449 | 80.29 |
| Gap | subclass | 1,396 | 0.1595 | 74.57 |

**读法**：gap 的准确率（74.57）接近 confirmed（72.62），但 ConfirmValue 低（0.1595 vs 0.4896）——「事实对、模型不确定」，正是要补的缺口。**gap 只有 1,396 条**，不是大规模数据。

**产率链**（排期前必须算的折扣）：

`raw subclass 58,309 → reliable 14,169（占 raw subclass 24.3%）→ extrapolated 8,661（占 14.9%）→ gap 1,396（占 2.39%）`

**gap 只占全部 raw 的 0.91%**（1,396 / 154,123），占 raw subclass 的 2.39%，占 extrapolated 的 16.1%。**也就是说 1 万条 raw 只够折出约 90 条 gap。** 任何「抽 N 万 raw」的计划都要先乘 0.91% 再判断够不够训。

### 4.2 医疗 QA（Table 3）

| 设置 | 模型 | MedQA | MedMCQA | PubMedQA | 平均 |
|---|---|---|---|---|---|
| zero-shot | Llama3-8B-Instruct raw | 51.7 | 51.7 | 70.3 | 57.9 |
| zero-shot | Llama3-Evontree(mix) | 51.0 | **57.4** | 74.7 | **61.0**（+3.1 绝对点） |
| SFT | Med42-v2 raw | 57.8 | 58.1 | 74.6 | 63.5 |
| SFT | Med42-Evontree(implicit) | **60.3** | **62.4** | 78.9 | **67.2**（+3.7 绝对点） |

- 相对各自最强 baseline：Llama3 +0.9 点、Med42 +1.1 点（平均）；**这是两个不同 setting 块，不能把 SFT 的 62.5 当 zero-shot raw**。
- explicit 变体：Llama3 平均 56.1（低于 zero-shot raw 57.9，−1.8），Med42 平均 62.3（低于 raw 63.5，−1.2）——**模板注入不要用**。
- **消融表里的 60.0 是 implicit，不是 61.0。** Table 6 的 full 行 = Evontree(implicit)=60.0；headline 的 +3.1 是 mix=61.0。两者差 1.0pp，且分项方向不一致（MedQA：implicit 52.7 > mix 51.0；MedMCQA：mix 57.4 > implicit 54.4）——**按 benchmark 选变体，不要按平均数抄**。

### 4.3 消融：规则的边际只有 0.2–0.3pp（Table 6）

LLaMA3-8B，zero-shot，单次运行（论文未报 seeds / std / CI）。**设置是推断的**：Table 6 的 full 行 60.0 / 52.7 / 54.4 / 72.9 与 Table 3 的「LLaMA3 8B-Evontree(implicit)」逐位相同，而后者标在 zero-shot 块；论文本身没在 Table 6 表头写 setting。

| 变体 | MedQA | MedMCQA | PubMedQA | 平均 | Δ vs full |
|---|---|---|---|---|---|
| w/o reliable triple sel. | 52.4 | **54.7** | 72.3 | 59.8 | −0.2 |
| w/o gap triple sel. | 52.6 | 54.1 | 72.5 | 59.7 | −0.3 |
| w/o ontology injecting | 51.1 | 53.9 | **73.1** | 59.4 | −0.6 |
| **full = Evontree(implicit)** | **52.7** | 54.4 | 72.9 | **60.0** | 0 |

去掉两条规则的边际按四舍五入就是 **0.2pp / 0.3pp**；单基准上最大到 0.6pp（w/o reliable 的 PubMedQA 72.3、w/o ontology 的 MedQA 51.1）。**整段区间 0.2–0.6pp，属于「不可区分」量级**，下面第 3 条解释为什么。

**三条读法，按重要性排**：

1. **不能把 +2.1pp 记在规则头上。** full 60.0 − raw 57.9 = +2.1pp，但摘掉两条规则只掉 0.2–0.3pp（59.8 / 59.7），连摘掉整个本体注入也只掉 0.6pp（59.4）。2.1pp 里最多约 0.6pp 能归到「本体结构 + 规则」这条链，「选低置信三元组 + 自蒸馏」这个动作没被单独对照。**对外说「两条本体规则带来 +2.1pp」是超额归因。**
2. **规则的真实作用在「筛得对」，不在「端任务涨点」。** Table 5 同一组对照：w/o reliable selection 时外推三元组准确率 55.7（gpt-4o-mini 58.4 / DeepSeek-V3 53.0），加规则后 74.6（75.3 / 73.8）——三元组层面 **+18.9pp**，端任务层面只有 **+0.2pp**。两层差两个数量级：1,396 条 gap 的注入量不足以把三元组质量优势转成 QA 分数。
3. **0.2–0.6pp 落在本文自己的噪声量级之内。** 论文没有任何方差报告；Table 5 两个 judge 在同一变体上差 5.4pp（58.4 vs 53.0）；Table 6 的 MedMCQA 与 PubMedQA 两列还出现方向反转（w/o reliable 54.7 > full 54.4；w/o ontology 73.1 > full 72.9）。所以论文原话「declined the most」只能读成**排序描述**，不是显著性结论。

**一个未定义项，复现前必须问清**：论文没写 `w/o ontology injecting` 用什么替代注入（纯 SFT？随机三元组？别的模板？）。因此 59.4 **不能**读成「无本体的 LoRA 基线」——它仍比 raw 57.9 高 1.5pp，说明「把某个东西 SFT 进去」本身就有效，这个变体的对照意义被这 1.5pp 污染了。这是本文最大的可复现缺口。

### 4.4 安全/通用能力

- explicit 的安全面掉点：Llama3 Jailbreak Safe 96.35→83.65（**−12.70pp**）；Med42 60.19→45.19（**−15.00pp**）。远超 5pp，是硬反例。
- implicit/mix **不是零代价**，正确定位是「降到噪声边缘」：最差 −2.31pp（Llama3 mix Raw Safe 97.50→95.19）、−2.12pp（implicit 97.50→95.38）；Med42 上反而升（Jailbreak Safe 60.19→60.77 / 65.77，Raw Safe 83.85→86.54 / 89.23）。**2.31pp 已经越过「≤2pp 可接受」这条线**——所以阈值不能拍脑袋定，见 §6 的三档表。
- 通用能力（MMLU/TriviaQA/ARC）平均只降 0.15%，部分还升。
- 这说明「注入方式」比「注入多少」更重要。

## 5. 这些数字不能说明什么

1. **不是推理时约束。** 它改模型参数，不改变 agent 运行时回路；不能证明「本体在动作前被执行」。
2. **不是通用方法。** 只两个 Llama3 系模型、单医疗域；跨域/跨模型族未测。
3. **不是无人工。** 15 个根概念是种子；规则只覆盖 subclass/synonym；其他关系没测。
4. **不是独立复现。** 自评、自建 benchmark；没有第三方复现。
5. **不是「数据越多越好」。** gap 只有 1,396 条；增益来自「选得准」，不是「加得多」。
6. **explicit 是硬反例。** 模板注入在医疗 QA 和安全面都掉；不能把「本体注入」笼统当成有效。
7. **不能把 +2.1pp 归给本体规则。** 消融只拆出 0.2–0.6pp（§4.3）；规则的主要产出是三元组准确率（+18.9pp），不是端任务分数。谁能撑起那 2.1pp，本文没做对照。
8. **没有方差。** 全文无 seeds / std / CI，单次运行。所有 <1pp 的差异都无法排除运行噪声；任何「显著」的说法都要自己重跑 3 seeds 才能下。

## 6. 工程配方（E3）

### 数据与接口

- 输入：15 个根概念 + 域文档/词典（可选）；输出：JSON 本体树 + 三元组表 `(head, relation, tail, ConfirmValue, reliable, gap)`。
- 接口：`extract(root_concepts, depth≥3)`；`confirm(triples, prompts)`；`close_rules(triples)`；`select_gap(τ*)`；`inject(gap, mode=implicit|mix)`。
- 训练：LoRA lr 5e-5、3 epoch、fp32、bs 8、grad accum 2；单卡/多卡按模型。
- **量级口径（先对齐再排期）**：15 根 × 深度 3 在论文里产出 **15.4 万条 raw**（synonym 95,814 + subclass 58,309），折出 reliable 14,169 / extrapolated 8,661 / **gap 1,396**。**gap/raw = 0.91%**。排计划时先算 `预期 gap ≈ raw × 0.91%`：**1 万 raw ≈ 90 gap，3 万 ≈ 270，6 万 ≈ 540**。gap 只从 subclass 链来（raw subclass 口径下产率 2.39%，更高），所以「raw」若指纯 subclass 三元组，数字要按 2.39% 重算。

### 成本

- 抽本体：15 根 × 深度 3，约 1–3 小时 GPU（`推测`）；sprint 抽 3–6 万 raw 按比例放大。
- **ConfirmValue 是主要推理开销**：全量 raw × 4–5 prompt（subclass 4、synonym 5）。论文口径 ≈ 15.4 万 × 4–5 ≈ **62–77 万次前向**；其中 **τ\* 标定只吃掉 ~1 万条 ≈ 4–5 万次**。sprint 抽 3–6 万 raw ≈ 13.5–27 万次前向。**别把「1 万条标定」当成 ConfirmValue 的总预算。**
- 训练：论文 1,396 gap 条 × 3 epoch；sprint 270–540 条更少。LoRA 成本低，约数小时–1 天（`推测`）。
- 人工：15 根概念 + 规则/τ\* 复核；约 2–3 人日（`推测`）。
- 维护：域/模型变更后重抽/重训。

### stop condition

**安全阈值：三处（sprint 出口 / V3 成功线 / 生产上线）共用这一张表，不再各写一套。**

| 安全面变动 vs raw（同 prompt 集、同 judge、同 seed 数） | 动作 |
|---|---|
| **≤ 2pp** | 通过：sprint 出口、V3 成功条件 |
| **2–5pp** | 灰区：仅当 3 seeds 的配对 95% CI **包含 0**（掉点与噪声不可区分）才继续；CI 整段落在 0 以下 → 按停处理 |
| **> 5pp** | 硬停：sprint、V3、上线同一数值，不给例外 |

参照（Table 4，Jailbreak Safe）：explicit −12.70pp（Llama3）/ −15.00pp（Med42）→ 远超 5pp，硬停；implicit/mix 最差 −2.31pp（Llama3 mix Raw Safe 97.50→95.19）→ 紧贴 2pp 线，比论文自己做到的还严。**若你的域安全评测自身有 ±2pp 抖动，2pp 出口线就没有判别力**——先用 3 seeds 标出噪声带，再决定 2pp 是线还是摆设（`推测`）。

**其余停线**

- 规则覆盖率 <50%（subclass/synonym 之外的关系多）→ 停，不要硬套。
- **gap 供给**：产率 0.91%，所以 **1 万 raw 只出约 90 条 gap**。**别用「1 万 raw + gap<500 停」这个组合**——它会在第一天就误触停线。改成：
  - 抽 **3–6 万 raw**（≈270–540 gap）再判断；
  - **raw < 6 万时 gap 少只触发「扩量」**（加根概念 / 加深一层 / 补 synonym 词典），不是停；
  - **raw ≥ 6 万 且 gap/raw < 0.5%**（论文产率的一半，即 gap <300）→ 停：这个域没有「低置信但正确」的空间，继续抽是浪费。
- ConfirmValue 区分度不显著（confirmed 与 gap 的准确率拉不开）→ 停。
- held-out 增益 <1pp，或增益主要来自数据清洗/模板 → 停。

### 第一个 sprint

2 周、Llama3-8B、单医疗子域、**3 seeds 起**：

1. 15 根概念 → JSON 树（深度≥3）；**全量抽 3–6 万 raw**。注意论文 15 根就出了 15.4 万条，所以这一步通常是**加深 / 加根 / 补词典**，不是重抽。
2. 从 raw 里取 **~1 万条标定 τ\***（论文口径），其余按同一 prompt 集补算；Youden 定 τ*。
3. 跑两条规则 → reliable / extrapolated / gap。**先报 gap 数和产率**：期望 270–540。若 gap <270 且 raw <6 万 → 回第 1 步扩量，**不要降阈值凑数**。
4. 只用 gap 做 implicit 自蒸馏 LoRA（lr 5e-5、3 epoch）。
5. held-out：MedQA / PubMedQA / MedMCQA；**四档对照** raw / w/o gap / w/o reliable /（可选）w/o ontology injecting；每档 **3 seeds**，报 mean±std 与配对 bootstrap 95% CI。
6. 记录规则覆盖率、GPU 时、安全面（Raw Safe + Jailbreak Safe，同 AdvBench prompt 集）。
7. **出口**：held-out 平均 **≥ +1pp vs 自建 raw 基线**，且 **3 seeds 同向、配对 bootstrap 95% CI 下界 > 0**；安全面走上表（≤2pp 通过）。
   - **参照**：论文 implicit +2.1pp（60.0 vs 57.9）、mix +3.1pp；但相对**最强已发表 baseline**只剩 **+0.9**（61.0 vs OntoTune_sft 60.1）和 **+1.1**（67.2 vs OntoTune_dpo 66.1）pp。所以 +1pp 不是松门槛，它约等于论文「超 SOTA」的全部幅度。
   - **seeds/CI 为什么必须**：论文没给方差，1pp 没有噪声基准。先跑 3 seeds 的 raw 与 implicit；若观测到 std ≥1pp，则 +1pp 不可判定，需要加 seeds 或换更大的 held-out。

### 替代方案

- 直接 SFT 领域数据；RAG/推理时约束；prompt 模板注入（explicit，本文证伪）；买领域模型。
- 论文没有与这些同口径成本-效果。

## 7. 客户价值假设（V2/V3，`推测`）

- **受益者**：医疗/法律等低资源专业域的产品团队；痛点：领域数据少、幻觉、标注贵。
- **指标**：held-out 准确率、幻觉率、安全面、标注/训练成本、专家复核工时。
- **反事实**：不做自演化 → 直接 SFT/RAG；先测 raw 基线与数据成本。
- **V3 试点**：单域、Llama3-8B；gap 规模按 §6 产率折算（照抄论文 = 1,396；自建 3–6 万 raw = 270–540）。
  - **成功** = held-out **≥ +1pp vs 自建 raw 基线**（3 seeds 同向 + 配对 bootstrap 95% CI 下界 >0）；安全面 **≤2pp**；成本 < 人工标注同量数据。
  - **失败 / 硬停** = 增益 <1pp；或安全面 **>5pp**（与 sprint、停线**同一数值**，不再另设口径）；2–5pp 走 §6 的灰区规则。
  - **停止线** = 年省标注 < 训练/维护成本。
  - **参照**：论文 +2.1 / +3.1pp vs raw，但只有 +0.9 / +1.1pp vs 最强已发表 baseline；且无 seeds/CI。所以 V3 的成功判据必须自带方差——否则 +1pp 和 ±1pp 的噪声分不开。
- **反例**：规则只覆盖 subclass/synonym；跨域失效；explicit 安全掉点；自评偏差。

## 8. 与仓库判断的关系

- **05 生产**：训练侧自演化路线；不是 01–04 的运行时约束。
- **P2**：训练侧与推理侧是两种 harness；本文只覆盖前者。
- **只作边界证据**：不能支撑「本体提升 agent 表现」；能支撑「本体规则可筛训练数据，但仅限 subclass/synonym、单域」。
- **归因要更保守**：本文能支撑「**被规则筛出的 gap 三元组**可当训练信号」；支撑不了「**本体规则**带来 +2.1pp」——规则在端任务的边际只有 0.2–0.3pp，摘掉整个本体注入也只有 0.6pp（§4.3）。

## 9. 还没解决 / 下一步

- 规则能否扩到其他关系（domain/range/disjointness）？
- 跨模型族/跨域是否成立？
- explicit 为什么安全掉点？能否修？
- 与 RAG/推理时约束叠加？
- 独立复现与第三方 benchmark。

## 10. 原文

- arXiv:2510.26683
- PDF：同目录 `2510.26683-evontree.pdf`
- 代码/数据：论文未给公开仓库。
