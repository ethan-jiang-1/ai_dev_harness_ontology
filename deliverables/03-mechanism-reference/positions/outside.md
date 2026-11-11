---
status: draft
deliverable_status: draft
updated: 2026-11-11
position: outside
evidence: [E-16, E-17, E-20]
---

# 谱外位置：determinism、read-path、supply、reasoning、training

> **2026-11-11 证据重置**：**E-16 已撤回**；本页的 reasoning 部分只作回查。E-17（记忆）与 E-20（read-path/supply）仍 admitted；determinism 仍只有设计。


> **一句话**：六个位置不是全集。至少还有五类位置对中心问题重要，但它们不满足「单次路径上的强度谱」或「六时刻硬闸」的条件；本页说明为什么放在谱外，以及什么会让它们升进来。

**为什么 read-path 不在六位置**：只有 1 个实现、fail-open、只删 subject，不满足扩轴规则；**为什么 determinism**：跨运行，不在单次路径。

## 1. 为什么有谱外

03 的六位置按「能否改变走向 + 覆盖」收：context、memory、evidence、checker、action、commit。以下五类不进来，不是因为不重要，而是因为：

- 不在单次执行路径上（determinism 跨运行）；
- 是轴外位置，只有 1 个实现或不满足硬闸（read-path、supply）；
- 与 action-gate 的边界未稳定（reasoning）；
- 不在推理回路内（training）。

> 把它们塞进强度谱，会让「强度」变成「所有东西」。谱外不是降级，是分类边界。

## 2. 一页表

| 位置 | 接缝 | 派 | 形态 | 机器做什么 | 主证据 | 为什么谱外 |
|---|---|---|---|---|---|---|
| determinism | 跨运行 | 04 状态 | 设计 | 把两次产物投影到本体结构，比对漂移；或作为生成时的约束 | 无 E；E-17 是跨轮，不是跨运行 | 不在单次路径上；无实现、无度量 |
| read-path | 轴外 | 01 约束 | `engine` | 检索结果进入上下文前，按 user_context + SHACL-AF 过滤；被 block 的 subject 侧三元组删除 | E-20（trustgraph） | 只有 1 个实现；fail-open；只删 subject 侧 |
| supply | 轴外 | 03 知识 | `engine` | 查询编译：TBox 饱和 + 重写 → SQL；改变「给什么」，不直接拦模型动作 | E-20（ontop） | 不是 gate；不校验输出 |
| reasoning | 轴外 | 01 约束 | `compiled` | 推理期条件验证：三值 ⊤/⊥/? + 假设 revision；缺证据转观察 | E-16（OntoAct；模拟） | 与 action-gate 的边界未稳定；模拟、固定 schema |
| training | 轴外 | 05 生产 | `none` | 训练侧用规则筛数据/注入结构；不在推理回路内 | 训练侧项目（报告值，`存疑`） | 不在回路内；增益仅报告值 |

## 3. 逐个说明

### 3.1 determinism（跨运行）

**问题**：同一输入两次运行得到不等价产物。它约束的不是某一步，而是「同一输入应得同一结论」这个性质。

**本体的两种用法（方向相反）**：生成时作约束（缩小解空间）；生成后作锚点（投影到本体结构，比对漂移）。常见讨论多讲前者；03 认为后者的价值被低估（`推测`）。

**为什么不在六位置**：它不在单次执行路径上，没有「动作前/输出后」这种时刻；也没有实现与度量。E-17 是跨轮状态，不是跨运行重放。

**什么会让它升进来**：同一输入重复运行的收敛/漂移度量；本体作为锚点的实现；≥2 个独立实现/论文。`已核`（E-17 的边界）/ `推测`（升格条件）

### 3.2 read-path（检索返回前）

**机制**：trustgraph 从 `urn:graph:policy` 加载 SHACL-AF NodeShape，对候选节点跑 `sh:SPARQLTarget` + `sh:SPARQLRule`；命中 `tg-pol:blocks` 的 subject 侧三元组从查询结果删除。`已核（代码）`（E-20）

**边界**：不是动作前 gate；异常 fail-open；只删 subject 侧，object 方向可能泄漏；只有 1 个独立实现。它是 best-effort 可见性过滤，不是写授权。

**为什么不在六位置**：只有 1 个实现，不满足「≥2 个独立实现」的扩轴规则；且 fail-open/单侧过滤让它不够「硬闸」。

**什么会让它升进来**：第二个独立实现；object 方向受控；异常 fail-closed；阻断测试。`已核（代码）`（E-20）/ `推测`（升格条件）

### 3.3 supply（查询编译）

**机制**：ontop 的 `QuestQueryProcessor` 在构造时 `rewriter.setTBox(saturatedTBox)`；`reformulateIntoNativeQuery` 做 rewrite → unfold → SQL；`QuestStatement` 执行。`已核（代码）`（E-20）

**边界**：不是 gate；不校验输出；不是 LLM agent；只支持 OWL 2 QL。它改变「给什么」，不直接拦模型动作。

**为什么不在六位置**：供给内部执行，不是回路上的一个可阻断时刻；把它当闸会混淆「查询重写」与「动作授权」。

### 3.4 reasoning（推理期）

**机制**：OntoAct 用三值条件 ⊤/⊥/? + 假设 revision；限制知识源（curated KG）可能封顶，验证条件可能同时提高成功率与减少无效干预。`withdrawn`（原 E-16；模拟、固定 schema、无真实工厂）

**边界**：与 action-gate 的边界未稳定；它只拦有适用条件公理的动作，缺证据转观察；不是安全保证。

**为什么不在六位置**：同一时刻的另一种判据，和 action-gate 的分工还没稳定；先留在 01 派内，不单列。

### 3.5 training（训练侧）

**机制**：训练侧用规则引导本体自演化，把规则用于训练数据筛选/注入；增益仅报告值，`存疑`。

**为什么不在六位置**：不在推理回路内；没有「动作前/输出后」的时刻；也不是 harness 的执行形态。

## 4. 什么会改变谱外名单

- `read-path` 出现第二个独立实现 + object 方向受控 + 阻断测试 → 按 [seams](../../../topics/seams.md#轴外位置可记录但不是六时刻) 的扩轴规则讨论升第七时刻。
- `determinism` 出现可复算的漂移度量 + 实现 → 从设计升为「有限证据」。
- `reasoning` 与 `action` 的判据边界稳定，且有独立证据 → 合并或单列。
- `supply` 出现「查询重写 + 输出校验 + 授权」的完整链 → 拆开供给/判定/授权，不整体升格。
- `training` 进入推理回路（如在线自演化）→ 重新判归派。

## 5. 这张表不能证明什么

1. 不能证明谱外位置「不重要」；它们可能比六位置更重要，只是分类不同。
2. 不能证明 `read-path`/`supply` 的实现「有效」；E-20 只给代码级机制，不是效应量。
3. 不能证明 `determinism` 可度量；它是设计提案，无 E。
4. 不能把 `reasoning` 的数字当本体增益；E-16 是模拟、固定 schema。
5. 不能把 `training` 的报告值当已核；训练侧项目的增益是 `存疑`。

## 6. 上游

- [topics/seams.md](../../../topics/seams.md)（六时刻 + 轴外 + 扩轴规则）
- [topics/execution-forms.md](../../../topics/execution-forms.md)（形态/执行链）
- [topics/04-state/determinism/README.md](../../../topics/04-state/determinism/README.md)
- [topics/01-constraint/commit-gate/README.md](../../../topics/01-constraint/commit-gate/README.md)（read-path）
- 施工：[02 R8 读路径 / R11 OBDA](../../02-engineering-playbook/recipes/README.md)；determinism/reasoning/training 暂无 recipe
- [conclusions](../../../topics/conclusions.md) E-16/E-17/E-20
