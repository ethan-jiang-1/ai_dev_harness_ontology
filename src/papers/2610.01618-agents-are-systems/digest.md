---
status: draft
updated: 2026-11-07
quality: A
based_on: card.md
claims: [06-L5]
---

# Agents Are Systems, Not Models · 消化

> 事实、数字、页码回 [card.md](./card.md)。这里只写**我们怎么用**、值不值得、哪里会坏。

## 工程思路

**如果你要评/调一个 agent，按这个顺序：**

1. **把 agent 当 config，不是 model。** 固定任务，变五个轴：信息、推理、验证、预算、模型；至少做全因子或分组对照。
2. **先量 run-to-run 噪声。** 同一配置重复 5 次；如果 54% 方差是噪声，单次跑分的结论不可信。
3. **报 completion、variance、cost、calibration，不只报 score。** 不同配置的完成率不同；只看得分会被「完成偏差」骗。
4. **先加信息，再换模型/加预算。** Information 在每个任务上都是第一；它还同时降成本、改善校准。
5. **预算不是独立旋钮。** 时间只在信息足够/模型足够强时有用；否则只是让 agent 在错误路径上跑更久。
6. **验证要靠工具，不靠 prompt。** 从 none 到 binding，行为只从 19% 到 22%；给 oracle 直接翻三倍。
7. **不要假设 agent 会拒绝弱 specialist。** mmlu-astronomy 上 99.8% 仍用 AstroSage；即使给 oracle 也不显著改善。
8. **效率 ≠ 结果。** Claude Sonnet 5 工具调用少、错误少、校准好，但 pooled G 更低；别把「执行效率」当能力。
9. **按行为分类诊断。** 用轨迹 taxonomy 看 verification/planning/execution，而不是只看分数。

## 实用意义

它解决的操作问题：

- **「同一个 agent，跑两次分数差很多。」** → 54% 方差是 run-to-run；重复采样 + 报 CI。
- **「换更大模型没提升。」** → 先加信息；信息影响 > 模型大小。
- **「给 agent 更多时间反而更差。」** → 预算与信息/模型交互；时间不是独立收益。
- **「prompt 让 agent 自检，它还是不自检。」** → 给验证工具；行为靠系统提供。
- **「agent 明明有更强 backbone，却用了弱 specialist。」** → 99.8% 的 authority bias/探索不足；需要在系统层强制比较。
- **「agent 执行很快，但结果不好。」** → 效率 ≠ 结果；要同时报 G、cost、calibration。
- **「评测结论不可复现。」** → 报 completion/variance/cost/CI，不只报均值。

**何时用**：长程 agent；多配置/多模型；需要可靠性与成本；有 specialist/tool 可调用。

**何时别用**：单步任务；配置轴不适用；没有足够 runs 做方差；没有 specialist reference。

## 质量评估

- **证据类型**：实证·基准（`已核`，一手正文；全因子实验 + 18k 轨迹）。
- **样本与对照**：4 tasks × 432 cells × 5 runs = 8,640 runs；3 Qwen models + Step/Claude ablations；oracle 实验；行为 taxonomy。
- **优点**：全因子设计；方差/完成率/成本/校准都报；行为分类；跨模型 family 对照；开放轨迹。
- **主要威胁**：4 tasks/2 domains；排除了 memory/multi-agent；验证结论只一个维度；FP8 量化；specialist reference 依赖。
- **`quality: A` 理由**：设计严谨、规模大、指标全、结论可操作；外部效度受任务/轴范围限制。

## 洞察

1. **54% 的 score variance 是 run-to-run 噪声。** 单次跑分的差异很可能不是配置效应；**评测必须重复**。`已核`
2. **信息 > 模型 > 推理 > 预算 > 验证。** Information 在每个任务上第一；99% bootstrap 排名第一。`已核`
3. **信息没有 tradeoff。** 它同时提高 G、降成本、降 runtime、改善校准；这是少见的「免费」改进。`已核`
4. **预算与信息/模型交互。** 对小/中模型，加时间提高 completion 但降低 G；对大模型才两者都升。**时间不是独立旋钮。** `已核`
5. **验证行为靠系统，不靠 prompt。** prompt none→binding 只 19→22%；oracle 翻三倍。**「让 agent 自检」是 prompt 幻觉。** `已核`
6. **Agent 不拒绝弱 specialist。** 99.8% 仍用 AstroSage；authority bias 或探索不足；需要在系统层强制比较。`已核`
7. **执行效率 ≠ 结果。** Sonnet 工具调用少、错误少、校准好，但 pooled G 更低；不要用效率代理能力。`已核`
8. **评测单位是 config，不是 model。** 同一 model，换信息/预算/验证，结果与可靠性都变。`已核`

## 成本与使能条件

| 成本 | 一次性 / 每次 | 说明 |
|---|---|---|
| 全因子实验 | 一次性 | 432 cells × 5 runs × tasks；算力/时间大 |
| Specialist sandbox | 集成一次性 | GPU + 环境 + README；任务特定 |
| 轨迹分类 | 每批 | judge + embedding + clustering |
| 重复采样 | 每次 eval | 5 runs/cell 起步；CI 仍宽 |
| 验证工具 | 集成一次性 | oracle/validator；成本上升 |
| 维护 | 任务/模型变更 | 重新跑网格 |

**使能条件**：可配置 harness；可重复 sandbox；specialist reference；足够算力做重复。

**2022 年做会卡在哪**：长程 agent/工具调用不成熟；没有 18k 轨迹级实验基础设施；specialist sandbox 不标准。

**反向条件**：单步任务；配置轴不适用；算力不足；没有 reference。

## 与现有判断的关系

| 关联 | 关系 |
|---|---|
| **06-L5** | **一手依据**：agent 评测应把配置当变量；54% 方差来自重复配置。 |
| **E-06** | 支撑「失败多归工作流」：配置轴（信息/预算/验证）比模型更能解释结果。 |
| **P2** | 强支撑：同一 model，换 harness/config，结果不同。 |
| **C-03** | 又一例：只看 score 会漏掉 completion/variance/cost/calibration。 |
| [metrics](../../../topics/06-measure/metrics/README.md) | 核心文献；机制细节回 card。 |
| [06-measure/README](../../../topics/06-measure/README.md) | 评测方法论的核心一手证据。 |

## 不可迁移

- 4 tasks / 2 scientific domains；其他领域未测。
- 排除 memory/multi-agent 轴；不能外推到完整 agent 系统。
- 验证工具结论只在一个维度（verification）上验证。
- 模型 FP8 量化；预算 3 档；specialist reference 依赖。
- 54% 方差是这套任务/配置的估计，不是普遍常数。

## 开放问题

- memory / multi-agent 轴加入后，Information 是否仍第一？
- 其他领域（软件工程/客服/研究）是否同样？
- 54% 方差在其他 benchmark 上是否复现？
- oracle 的 4.4% hill-climbing 是否被低估？
- 验证工具的效果能否推广到 planning/exploration 行为？
- 如何在不做全因子的情况下做配置敏感性分析？
