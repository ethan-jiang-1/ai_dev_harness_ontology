---
status: draft
updated: 2026-11-08
quality: A
based_on: card.md
claims: [06-L5]
---

# Agents Are Systems：评的是配置，不是模型

> 这篇消化不假设你读过论文。先讲清「agent = 模型 + 配置」这件事，再看五轴实验、54% 方差、以及「验证靠工具不靠 prompt」。

## 0. 三句话

1. **它问什么**：agent 评测通常把 agent 当固定模型，只报一个 success rate；但用户实际可配「告诉它什么、让它跑多久、用哪个模型、怎么验证」，这些选择会改变能力与可靠性。
2. **它怎么做**：4 个 AI4S 任务 × 5 个配置轴（信息/推理/验证/预算/模型）× 432 cells × 5 runs；共 8,640 runs、18,240 trajectories；报 GAP_CLOSED、completion、variance、cost、calibration。
3. **它发现什么**：**54% 的 score variance 来自同一配置的重复运行**；信息轴影响最大（> 模型 > 推理 > 预算 > 验证）；预算只在信息/模型足够时有用；**提示 agent 自检几乎不改变行为，给验证工具才会**。

## 1. 它解决什么问题

### 1.1 背景

Agent 不是「一个模型」，是「模型 + harness + 配置」。同一模型，换任务信息、推理方式、验证要求、时间预算、backbone，结果会变。

但很多评测只报一个分数，把 agent 当固定对象；这导致：
- 无法判断「是模型不行，还是配置不行」；
- 单次跑分不可复现；
- 成本/可靠性/校准被忽略。

### 1.2 论文的立场

**评 agent 要评配置。** 至少变信息、推理、验证、预算、模型；报方差、完成率、成本、校准。

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **configuration axes** | 可配置的五轴：Information / Reasoning / Verification / Budget / Model。 |
| **GAP_CLOSED** | `G=(S−B)/(R−B)`：agent 得分相对 backbone/specialist 的差距关闭比例。 |
| **completion** | agent 在预算内提交答案的比例。 |
| **hurdle** | 是否超过任务的 trivial 分数 + margin；过滤「没真正尝试」的 run。 |
| **outcome consistency** | 同一 cell 多次运行的结果一致性。 |
| **calibration** | 模型自报置信度与实际正确率的匹配。 |
| **specialist model** | 领域专用模型；agent 要找到并正确操作它。 |
| **AI4S** | AI for Science；本文四个科学任务。 |

## 3. 它怎么做

### 3.1 任务

4 个科学任务，agent 要找到并正确操作一个已发表的 specialist model：

- Redshift-Estimation：AstroCLIP，pre-processing。
- MMLU-Astronomy：AstroSage-8B，declining（应拒绝弱 specialist）。
- Promoter-Prediction：DNABERT-2，fine-tuning。
- RNA-Folding：RiNALMo，post-processing。

### 3.2 五轴

| 轴 | 水平 |
|---|---|
| Information | none / identity / interface / protocol |
| Reasoning | act-only / think-act / ReAct |
| Verification | none / asked / reported / binding |
| Budget | 5 / 10 / 20 min |
| Model | Qwen3.5-35B-A3B / 122B-A10B / 397B-A17B |

4×3×4×3×3 = 432 cells；每 cell 5 runs；每 task 2,160 runs；4 tasks = 8,640 runs。

### 3.3 指标

- **GAP_CLOSED**：`G=(S−B)/(R−B)`；只对 `R>B` 的任务定义。
- **completion**：是否在预算内提交。
- **hurdle**：是否超过 trivial + margin；排除「没真正尝试」。
- **consistency/calibration/cost**：结果一致性、置信度校准、token/时间。

### 3.4 一个具体例子

Information 轴：

- `none`：agent 不知道有 specialist。
- `identity`：知道模型名/论文。
- `interface`：知道怎么调用。
- `protocol`：知道输入/输出/预处理/常见错误。

同一模型，从 `none` 到 `protocol`，GAP_CLOSED 大幅提升；还降成本、改善校准。

## 4. 结果：数字与条件

### 4.1 方差

- **54%** 的真实尝试 score variance 来自同一配置的 run-to-run 噪声。
- 不排除 hurdle 失败时，配置只解释 39.4%；排除后 46.1%。

### 4.2 轴的影响

| 轴 | 平均排名 |
|---|---|
| Information | **1.00** |
| Model | 2.67 |
| Reasoning | 3.00 |
| Budget | 3.33 |
| Verification | 5.00 |

- Information 在 99% bootstrap 样本中排名第一；effect size 1.925/1.452/1.496（promoter/redshift/rna）。
- Information 同时降成本/降 runtime/改善校准。

### 4.3 交互与行为

- 预算只在信息足够/模型足够强时有用；否则只是让 agent 在错误路径上跑更久。
- **99.8%** 的 mmlu-astronomy runs 仍使用较弱 specialist；给 oracle 也不显著改善。
- Verification prompt 从 none→binding，reference-based verification 只 19%→22%；给 oracle 翻三倍。
- ~3/4 的 runs 只做 format-only verification；oracle 的 hill-climbing 只 4.4%。

### 4.4 这些数字之间的逻辑

- **为什么 54% 是噪声？** 同一配置重复跑，模型采样/工具状态/环境时序都在变；单次分数差异很容易被误读成配置效应。
- **为什么 Information > Model？** agent 的瓶颈常是「不知道有 specialist / 不知道怎么调」，不是「模型不够聪明」；补信息直接消除瓶颈，换模型不能。
- **为什么预算与信息/模型交互？** 时间只让 agent 在已有路径上多试；信息不足时，多试只是在错误路径上跑更久。
- **为什么验证工具 > prompt？** prompt 要求自检，但模型没有外部信号；工具提供可验证的反馈。行为从 19% 到 22%，oracle 翻三倍。
- **为什么 agent 不拒绝弱 specialist？** 可能是 authority bias（默认 specialist 更强）或探索不足（从不比较 backbone 自己的答案）。

## 5. 这些数字不能说明什么

1. **不是所有域。** 4 tasks / 2 scientific domains；其他领域未测。
2. **不是完整 agent。** 排除了 memory、multi-agent；不能外推到完整系统。
3. **验证结论只一个维度。** 「系统设计 > prompt」只在一个行为（verification）上验证。
4. **模型 FP8 量化；预算 3 档。**
5. **54% 是这套任务/配置的估计**，不是普遍常数。
6. **specialist reference 依赖**；任务选择可能影响轴效应。

## 6. 工程上怎么用

### 6.1 复刻顺序

1. **把 agent 当 config，不是 model。** 固定任务，变五轴；至少全因子或分组对照。
2. **先量 run-to-run 噪声。** 同配置重复 5 次；单次跑分不可信。
3. **报 completion/variance/cost/calibration**，不只报 score。
4. **先加信息，再换模型/加预算。** Information 在每个任务上第一；还降成本/改善校准。
5. **预算不是独立旋钮。** 时间只在信息/模型足够时有用。
6. **验证要靠工具，不靠 prompt。** 给 oracle，不要只写「请自检」。
7. **不要假设 agent 会拒绝弱 specialist。** 99.8% 仍用；需要在系统层强制比较。
8. **效率 ≠ 结果。** Sonnet 工具调用少、错误少、校准好，但 pooled G 更低。
9. **按行为分类诊断。** 用轨迹 taxonomy 看 verification/planning/execution。

### 6.2 成本与使能

| 成本 | 一次性/每次 | 说明 |
|---|---|---|
| 全因子实验 | 一次性 | 432 cells × 5 runs × tasks；算力/时间大 |
| Specialist sandbox | 集成一次性 | GPU + 环境 + README；任务特定 |
| 轨迹分类 | 每批 | judge + embedding + clustering |
| 重复采样 | 每次 eval | 5 runs/cell 起步；CI 仍宽 |
| 验证工具 | 集成一次性 | oracle/validator；成本上升 |
| 维护 | 任务/模型变更 | 重新跑网格 |

**使能条件**：可配置 harness；可重复 sandbox；specialist reference；足够算力做重复。

### 6.3 何时用 / 何时别用

**用**：长程 agent；多配置/多模型；需要可靠性与成本；有 specialist/tool 可调用。

**别用**：单步任务；配置轴不适用；没有足够 runs 做方差；没有 specialist reference。

### 6.4 最小评测清单

1. **把 agent 当 config。** 固定任务，变五轴；至少全因子或分组对照。
2. **先量 run-to-run 噪声。** 同配置重复 5 次；单次跑分不可信。
3. **报 completion/variance/cost/calibration。** 不只报 score。
4. **先加信息，再换模型/加预算。** Information 在每个任务上第一；还降成本/改善校准。
5. **预算不是独立旋钮。** 时间只在信息/模型足够时有用。
6. **验证要靠工具。** 给 oracle/validator，不要只写「请自检」。
7. **强制比较弱 specialist。** 不要假设 agent 会拒绝；在系统层让它比较。
8. **效率 ≠ 结果。** 同时报 tool calls/错误/校准与 pooled G。

## 7. 质量与边界

- **证据类型**：实证·基准（全因子实验 + 18k 轨迹）。
- **强项**：全因子设计；方差/完成率/成本/校准都报；行为分类；跨模型 family 对照；开放轨迹。
- **主要威胁**：4 tasks/2 domains；排除 memory/multi-agent；验证结论只一个维度；FP8 量化；specialist reference 依赖。
- **`quality: A`**：设计严谨、规模大、指标全、结论可操作；外部效度受任务/轴范围限制。

## 8. 与仓库判断的关系

- **06-L5（已核）**：agent 评测应把配置当变量；54% variance 来自重复配置。
- **E-18（已核）**：Information > Model > Reasoning > Budget > Verification；验证靠工具不靠 prompt；agent 99.8% 仍用弱 specialist。
- **E-06**：失败多归工作流；配置轴比模型更能解释结果。
- **P2**：同一 model，换 harness/config，结果不同。
- **C-03**：只看 score 会漏掉 completion/variance/cost/calibration。

## 9. 还没解决 / 下一步

- **memory/multi-agent 轴** 加入后，Information 是否仍第一？
- **其他领域**（软件工程/客服/研究）是否同样？
- **54% 方差**在其他 benchmark 上是否复现？
- **oracle 的 4.4% hill-climbing** 是否被低估？
- **验证工具效果**能否推广到 planning/exploration？
- **不做全因子时**如何做配置敏感性分析？

## 10. 原文

- arXiv:2610.01618
- PDF：`src/papers/2610.01618-agents-are-systems/`
- 代码/数据：论文释放 benchmark + 18,000+ trajectories。
