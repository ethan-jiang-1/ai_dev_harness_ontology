---
id: EXP-007
status: seed
experiment_status: 设计中
updated: 2026-11-09
rq: [RQ1, RQ2, RQ5]
targets: [P1a, P2, E-04, E-16]
artifact: 仓库外（未开始）
---

# EXP-007 · 同一接缝、只换执行形态

## 要回答什么

同一份本体、同一个接缝位置、同一个模型与任务，只改**执行形态**（引擎求值 / 编译成约束 / 文本上下文 / 仅标签表），行为差异有多大？

## 会推翻什么

| 若结果为 A | 则 |
|---|---|
| 四种形态的行为差异 ≤ run-to-run 噪声 | 「形态是独立变量」被削弱；P2 只剩位置效应 |
| 文本上下文 ≈ 引擎求值 | 「执行」不是必要条件；P1a 要收窄为「约束内容」而非「执行形态」 |
| 引擎/编译显著优于文本，且 false-veto 可控 | 支撑「形态 × 位置」的交互；E-04 的边界可写进结论 |
| 引擎/编译的 false-veto 显著更高 | 执行形态的代价是误拦；P3a 扩展到形态选择 |

## 设计

- **变量**：同一本体内容，四种形态：
  1. `engine`：OWL/SHACL 求值（如 pySHACL 或自研求值器）；
  2. `compiled`：把本体编译成命令式校验（if/else 或 Datalog 规则）；
  3. `context`：把同内容投影成文本，放进 prompt；
  4. `label`：只给类型/关系名，不给约束。
- **接缝**：固定一个。优先 `action-gate`（工具调用前），因为它有可观测的阻断；次选 `checker`（输出后）。
- **对照**：同任务、同模型、同预算、同本体内容；只换形态。每形态 ≥150 次决策，重复 5 次（参考 E-18 的 54% 方差基线）。
- **被控住的混淆项**：本体内容、接缝位置、模型、任务集、上下文预算、工具集。
- **度量**：主指标 = 不可逆错误放行率（false approve）+ false-veto；过程指标 = 覆盖率、审批/千次、token、时延。不用单一准确率替代（C-03）。
- **分母**：按决策/轨迹；稀疏事件给最低样本与置信区间。

## 代理试点 v0（2026-11-09，已完成；不构成正式结果）

**目的**：在投入真 runner 前，先用当前可用的 DeepSeek 模型看四种形态有没有可观察差异。

- 模型：`deepseek-v4-pro`（DeepSeek API，`temperature=0`，单次）。**2026-11-09 起模型来源受 [meta/models](../meta/models.md) 约束：本地不装模型，只用 Yovole 的 `DeepSeek-V4-Flash` / `qwen3.8-27b`；后续正式实验按此重跑。**
- 设计：4 个退款审批 case × 4 种形态 = 16 次调用；case 含阈值（>500）与角色（support agent 批准不算 manager 批准）。
- 形态：`engine`（外部 SHACL 求值器返回 blocks=true/false）、`compiled`（if/else 规则）、`context`（政策散文）、`label`（只有类型标签，无阈值/规则）。
- 结果：

| 模型 | engine | compiled | context | label |
|---|---:|---:|---:|---:|
| DeepSeek V4 Pro | 4/4 | 4/4 | 4/4 | 0/4 |
| Qwen 3.8 27B（OpenRouter） | 4/4 | 4/4 | 4/4 | 1/4 |

label 的失败以 JSON 解析失败/空内容为主（Qwen 有 2 次 provider 返回空 content），不能当成“决策错误”解读。

**解释（`推测`）**：这是**天花板效应**，不是“形态无用”。两个模型在 engine/compiled/context 上都满分；label 视图故意缺阈值，属于不公平的对照，模型只能拒答或猜。16 次/模型、单次调用，不能支持或否定 P2。

**它改变了什么**：EXP-007 原设计需要改——case 要更难（冲突证据、歧义、需要多步核对），label 对照要公平（给标签 + 可查的阈值，或明确标为“信息不足”基线），engine 形态要走真实求值器而不是一句 verdict。更根本的是：**engine 一旦以 oracle verdict 出现，任务就退化成“照抄”，测不到形态差异**；正式实验要让 engine 也带不确定性/覆盖缺口，或者把任务设计成“验证器只覆盖一部分，剩余要 agent 判断”。**不要用纯文本 chat 代替执行形态实验。**

### Yovole 路径尝试（2026-11-09，作废）

用户提供的两个模型（`DeepSeek-V4-Flash` / `qwen3.8-27b`）可以通过 workflow 的 provider override 调用；但 **subagent 不是 raw chat**：它带工具和仓库上下文，prompt 里写了“不要用工具”也不保证遵守。本次 qwen 的输出直接出现「I've recorded the full analysis in the repo's `runs/` location」「Self-check result for `ai_dev_harness_ontology`: OK」等语句，并且真的写了 `topics/01-constraint/action-gate/runs/2026-11-09-refund-block-run.md`（已删除）；它读了仓库、跑了 checker。**这一轮结果作废，不能与前面的 raw API pilot 合并。**

**方法结论**：不要把 subagent / workflow 当实验被试；需要 raw chat endpoint，或一个明确禁用工具、禁用仓库访问的 runner。当前环境下 Yovole 直连 HTTP 超时，所以这条实验线在工具层也不成立。

## 状态与阻塞

- `experiment_status: 设计中`（代理试点完成；正式实验未跑）
- 需要：一个可控的工具调用沙箱 + 一份带约束的小本体 + 能注入四种形态的 runner + 一个可调用的模型 endpoint（或本地模型）。当前环境没有模型 endpoint，故停在协议；不请求用户提供资产。
- 不依赖外部客户资产；可用合成域先做 v0。

## 回链

- 结论：[E-04、E-16](../topics/conclusions.md)、[P1a/P2](../THESIS.md)
- 主题：[01/action-gate](../topics/01-constraint/action-gate/README.md)、[execution-forms](../topics/execution-forms.md)
- 相关 digest：[POLAR](../src/papers/2610.08082-polar/digest.md)、[OntoAct](../src/papers/2610.21983-ontoact/digest.md)、[Ontology Catch](../src/papers/2610.37809-what-does-an-ontology-catch/digest.md)
