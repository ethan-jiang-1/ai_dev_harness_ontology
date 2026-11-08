---
status: draft
updated: 2026-11-08
quality: B
based_on: card.md
claims: [01-L3]
---

# MedMAS-DDx：确定性评分 + 多 agent 追问的鉴别诊断

> 这篇消化不假设你读过论文。先讲清「鉴别诊断」这项工作，再看四角色、确定性评分、Q4DX 上的结果与边界。

## 0. 三句话

1. **它问什么**：单轮问答假设诊断所需信息已齐；真实鉴别诊断是迭代追问。LLM 直接推理不可审计、易幻觉。能不能把语言理解交给 LLM，把排序/评分交给代码和 curated 本体？
2. **它怎么做**：四角色（症状抽取 / 追问 / 患者模拟 / 诊断精化）；LLM 只做语言，排序/评分由确定性代码在 SYMP/DOID/HPO 上算；Yes/No 追问补缺失症状。
3. **它发现什么**：Q4DX 99 cases/29 diagnoses 上，Top-1 18.7→21.2%、Top-3 25.8→27.3%；聚合提升不大，但 case-level 可以把 0.340 拉到 1.0。curated KG 覆盖不到诊断（Jaundice/Vertigo 被归为症状）时准确率恒 0。

## 1. 它解决什么问题

### 1.1 背景

鉴别诊断（differential diagnosis）：从相似症状里区分几种病。真实过程是迭代的：先问病史，缺什么问什么，逐步收敛。

LLM 单轮问答的失败：
- 输入不全也硬答；
- 推理不可审计；
- 候选病可以凭空生成；
- 评分/排序不可复现。

### 1.2 论文的立场

**LLM 只做语言，排序交给代码。** 这样每条诊断都能回指症状 + 本体关系；代价是覆盖受本体限制。

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **differential diagnosis** | 鉴别诊断：在多个可能病里排序。 |
| **Q4DX** | 本文基准：99 cases、29 diagnoses；80%/50% 症状完整度。 |
| **SapBERT** | 语义相似度模型；本文用 cosine ≥0.6 判正确。 |
| **specificity weight** | 越少疾病共享的症状，权重越高。 |
| **coverage** | 匹配症状 / 总映射症状。 |
| **discriminative weight** | 一个症状能区分多少候选病。 |
| **追问** | 只问可观察、未报告、能区分候选的 Yes/No 症状。 |
| **patient simulator** | 评估用自动患者；可访问完整 profile，是乐观估计。 |

## 3. 它怎么做

### 3.1 四角色

| 角色 | 做什么 | 是否实时 |
|---|---|---|
| Symptom extractor | 自由文本 → 结构化症状 | 是 |
| Follow-up interviewer | 选有区分度的 Yes/No 问题 | 是 |
| Diagnosis refiner | 用回答更新评分，生成解释 | 是 |
| Patient simulator | 自动回答，驱动评估 | 否（仅评估） |

### 3.2 确定性评分

1. **Specificity weight**：`1 / log2(1 + N_d(s))`；越少疾病共享的症状越有信息量。
2. **Raw score**：匹配症状的 specificity 求和。
3. **Coverage**：`match_count / total_mapped`。
4. **Composite**：`raw × (0.5 + 0.5×coverage)`；coverage 是软调整。
5. **Discriminative weight**：`1 − diseases_with_symptom(s) / n_profiled`；用于追问后的 support/conflict。
6. **Final score**：`composite × (1 + α·support_norm − β·conflict_norm)`；α=0.6、β=0.2。
7. **Threshold**：保留领头分数的一小部分或至少匹配 2 个症状的候选。

### 3.3 追问

- 最多 11 个问题（引 MedDialogRubrics：准确率约 10–11 轮达峰，之后下降）。
- 只问 patient-observable、非既有、能区分候选的症状；回答限定 yes/no/unsure。
- 回答进确定性评分；不是让 LLM 自由对话。

### 3.4 一个具体例子

Case #96：患者有黄疸但初始描述漏了。

- 初始：anthrax 0.922 vs hepatitis 0.861；Top-1 错。
- 追问 11 个问题，确认 jaundice。
- Hepatitis A/B/C 分数上升（0.872），anthrax 下降（0.781）。
- Top-1 变成 Hepatitis A；similarity 0.340→1.0。

## 4. 结果：数字与条件

| 指标 | Phase 1 | Phase 2 |
|---|---|---|
| Top-1 accuracy | 18.7%（37/198） | **21.2%（42/198）** |
| Top-3 accuracy | 25.8%（51/198） | **27.3%（54/198）** |
| mean similarity top-1 | 0.449 | 0.466 |
| mean similarity top-3 | 0.523 | 0.537 |

- 80% completeness：0.4589→0.4792；50%：0.4394→0.4527。
- Top-3 at 80%：25.3→30.3；**Top-3 at 50%：26.3→24.2（下降）**。
- 症状映射：91.3% 成功（77.3% SYMP + 14.0% HPO fallback；8.7% unmapped）。

### 4.4 这些数字之间的逻辑

- **为什么排序交给代码？** LLM 排序不可复现、不可审计；确定性评分每项回指症状 + 本体关系。语言理解仍由 LLM 做。
- **为什么 curated KG 会封顶？** Jaundice/Vertigo 被本体归为症状，不是诊断；系统只能从本体关系里出候选，没有的诊断永远出不来。
- **为什么 Top-3 在 50% 时会降？** 追问会替换弱候选；新信息可能把正确诊断挤下去，或把错误候选拉上来。Top-1/Top-3 不是同向。
- **为什么聚合提升小？** 99 cases；平均值掩盖 case-level 的大幅变化（0.340→1.0）。要看「可解决歧义」子集。

## 5. 这些数字不能说明什么

1. **样本小。** 99 cases / 29 diagnoses；不能外推到临床。
2. **模拟患者是乐观估计。** 可访问完整 profile；真人对话未测。
3. **单本体。** SYMP/DOID/HPO；跨本体/开放域未测。
4. **聚合提升小。** Top-1 +2.5 pp；case-level 大，但平均值掩盖。
5. **Top-3 可能下降。** 追问替换弱候选，50% 时 Top-3 从 26.3→24.2。
6. **curated KG 封顶。** Jaundice/Vertigo 被本体归为症状，系统无法输出为诊断，准确率恒 0。
7. **不是确诊。** 系统只做 differential；最终诊断仍靠医生。

## 6. 工程上怎么用

### 6.1 复刻顺序

1. **把 LLM 限制在语言层。** 抽取症状、生成问题、写解释；排序/评分/更新全部用确定性代码。
2. **先做症状映射。** canonical → alternatives → synonym/HPO fallback；映射失败保留 trace，不进推理。
3. **候选集只从本体关系来。** 疾病必须显式链接到至少一个患者症状。
4. **评分要能解释。** specificity + coverage + support/conflict；每项回指症状与本体关系。
5. **追问只问有区分度、可观察、未报告的症状。** Yes/No/unsure；最多 10–11 问。
6. **阈值宁宽勿严。** 早期丢掉的候选后面回不来。
7. **聚合指标会掩盖 case-level 价值。** 同时报「可解决歧义」子集。
8. **同时报 Top-1 与 Top-3。** 追问可能伤 Top-3。
9. **换更强 LLM 不解决结构错。** 先修本体覆盖/粒度/术语。

### 6.2 成本与使能

| 成本 | 一次性/每次 | 说明 |
|---|---|---|
| 本体 + KG | 一次性/持续 | SYMP/DOID/HPO；GraphDB；术语对齐 |
| 症状映射 | 每次 | 91.3% 成功；8.7% 丢失 |
| LLM 抽取/提问/解释 | 每次 | 3 个 agent |
| 追问 | 每次 | ~10 问；患者/用户时间 |
| 评估 | 每 case | SapBERT/人工；模拟患者 |
| 维护 | 本体更新 | 新疾病/症状/术语 |

**使能条件**：curated 本体；可查的症状-疾病关系；能接受 Yes/No 追问；有审计需求。

### 6.3 何时用 / 何时别用

**用**：有 curated 医学本体；症状-疾病关系可查；需要可审计的鉴别诊断；能接受 Yes/No 追问。

**别用**：开放域/罕见病；本体覆盖不足；需要 severity/temporal 细节；真人对话成本高；需要确诊。

### 6.4 最小落地清单

1. **先做本体映射。** canonical → alternatives → synonym/HPO fallback；映射失败保留 trace，不进推理。
2. **候选只从本体关系来。** 疾病必须显式链接到至少一个患者症状；不要自由生成候选。
3. **评分可解释。** specificity + coverage + support/conflict；每项回指症状与本体关系。
4. **追问只问有区分度、可观察、未报告的症状。** Yes/No/unsure；最多 10–11 问。
5. **阈值宁宽勿严。** 早期丢掉的候选后面回不来。
6. **同时报 Top-1/Top-3 与 case-level。** 聚合会掩盖可解决歧义。
7. **不做确诊。** 系统只做 differential；最终诊断仍靠医生。
8. **先修本体覆盖/粒度。** 换更强 LLM 不解决「本体没有这个诊断」的结构错。

## 7. 质量与边界

- **证据类型**：实证·基准（小样本、模拟患者）。
- **强项**：确定性评分 + 本体 grounding；可解释；追问机制；case-level 分析；诚实写「封顶」与「聚合掩盖」。
- **主要威胁**：小样本；模拟患者乐观；SapBERT 0.6 阈值；本体覆盖/术语不匹配；问题预算高；无真人。
- **`quality: B`**：机制清晰、可审计；但样本小、模拟患者、单本体，外部效度有限。

## 8. 与仓库判断的关系

- **01-L3（已核）**：推理期约束限制知识源（curated KG）可能封顶；Jaundice/Vertigo 恒 0。
- **E-06**：失败多归工作流：错误主要来自 KG 稀疏/粒度/术语，不是 LLM 语言能力。
- **P2**：同一 LLM，换确定性评分/本体/追问，结果不同。
- **02 判定**：确定性评分 + 本体关系是「外部判据」。

## 9. 还没解决 / 下一步

- **真人患者下 refinement 的增益？**
- **本体扩展（Jaundice/Vertigo）后准确率变化？**
- **问题选择策略的消融**：specificity/discriminative/information gain。
- **11 问上限是否最优？**
- **severity/temporal 能否编码进回答格式，同时保持确定性评分？**
- **多本体/罕见病如何扩展？**

## 10. 原文

- arXiv:2610.36325
- PDF：`src/papers/2610.36325-ontology-multiagent-diagnosis/`
- 代码/数据：论文未给公开仓库。
