---
id: EXP-007
status: seed
experiment_status: 未开始
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

## 状态与阻塞

- `experiment_status: 未开始`
- 需要：一个可控的工具调用沙箱 + 一份带约束的小本体 + 能注入四种形态的 runner。
- 不依赖 D0 的客户资产；可用合成域先做 v0。这是它与 EXP-004/005/006 的区别。

## 回链

- 结论：[E-04、E-16](../topics/conclusions.md)、[P1a/P2](../THESIS.md)
- 主题：[01/action-gate](../topics/01-constraint/action-gate/README.md)、[execution-forms](../topics/execution-forms.md)
- 相关 digest：[POLAR](../src/papers/2610.08082-polar/digest.md)、[OntoAct](../src/papers/2610.21983-ontoact/digest.md)、[Ontology Catch](../src/papers/2610.37809-what-does-an-ontology-catch/digest.md)
