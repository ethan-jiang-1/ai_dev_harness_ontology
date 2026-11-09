---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# 2. 地图：主张、轴、位置

### 2.1 主张类型：E / C / H / D / G

03 里每个规范句都要带一个标记；没有标记的按「推测」读。

| 标记 | 含义 | 例子 | 要求 |
|---|---|---|---|
| **E** | 证据条目，来自 [conclusions](../../../topics/conclusions.md)；等级看原表 | E-04、E-20；E-19 是 `推测` | 必须链 conclusions；写清等级与限定 |
| **C** | 冲突/方法论条目 | C-03、C-04 | 不是证据等级；不合成结论 |
| **H** | 组织假设 | 强度–覆盖率反向 | 必须写「什么会推翻它」 |
| **D** | 设计提案/概念架构 | commit gate 三段式；覆盖率矩阵 | 必须写「无实现/未测」 |
| **G** | 缺口 | M1–M5 | 必须写「缺什么数据」 |

> 纪律：`deliverables/` 只引 E-xx，不引 L-xx。03 里如果只有 topics 的 L 支撑，要么在 topics 升 E，要么在 03 标 H/D，不能假装是 E。


### 2.2 四根轴，三根用于分类

`topics/` 有四根轴；03 用其中三根做分类，第四根（部件）只做落点索引。

| 轴 | 问什么 | 载体 | 在 03 里的用法 | 典型误用 |
|---|---|---|---|---|
| 派轴 | 本体凭什么起作用 | `01-06` | 解释位置背后的机制类型 | 把「知识注入」当「约束」 |
| 部件轴 | 接在机器的哪个部件 | `00-harness` | **落点索引**，不单独分类 | 把部件当机制 |
| 时刻轴 | 在哪个时刻介入 | 六个 seams + 轴外 | 排「六个位置」的时间读法 | 把「读路径」当「动作前」 |
| 形态轴 | 机器拿本体做了什么 | engine/compiled/context/label/none | 区分同一位置的执行语义 | 把「有引擎」当「会拦/有授权」 |

> 三根分类轴正交：同一份本体可以在不同时刻、以不同形态被执行；「强度」是时刻轴的排序，「形态」不是强度的刻度。第四根轴是「接在哪里」，不是第四种分类。

#### 2.2.1 位置 × 时刻 × 派 × 部件 × 形态

| 03 位置 | 时刻/接缝 | 派 | 主要部件 | 常见形态 |
|---|---|---|---|---|
| context | 无（供给；轴外 `supply`） | 03 知识 | context | `context` / `compiled` |
| memory | 跨轮 | 04 状态 | memory | `compiled` |
| evidence | 输出时 | 02 判定 | observability / context | `compiled` / `context` |
| checker | 输出后 | 02 判定 | verification | `compiled` / `engine` |
| action | 动作前 | 01 约束 | tools | `compiled` |
| commit | 落盘前 | 01 约束 | governance | 设计（无实现） |
| （谱外）determinism | 跨运行 | 04 状态 | memory / observability | 设计 |
| （谱外）read-path | 轴外 | 01 约束 | retrieval / tools | `engine` |
| （谱外）supply | 轴外 | 03 知识 | context | `engine` |

> **六个位置不是六个时刻。** `determinism` 是第六个时刻，但不在强度谱上；`context` 不是时刻，是供给；`read-path`/`supply` 是轴外位置。别把四张表混成一张。谱外位置（determinism / read-path / supply / reasoning / training）见 [positions/outside.md](../positions/outside.md)。


<a id="3-六个位置一页表"></a>
### 2.3 六个位置一页表

| 位置 | 问什么 | 本体角色 | 能阻断 | 主证据 | 主要代价 | 不能证明 | 卡 |
|---|---|---|---|---|---|---|---|
| context | 模型看到什么 | 投影/编译 | 否 | E-01/E-12/E-14 | token/编译 | 规则被执行 | [→](../positions/context.md) |
| memory | 下一轮记得什么 | 状态/对齐 | 否 | E-05/E-17 | 维护/训练信号 | 跨运行确定性 | [→](../positions/memory.md) |
| evidence | 产出带什么依据 | 证据契约 | 否 | E-03 | token/集成 | 形式保证 | [→](../positions/evidence.md) |
| checker | 产出对不对 | 外部判据 | 是 | E-02/E-20 | 每条判定/维护 | 语义正确 | [→](../positions/checker.md) |
| action | 动作能不能做 | 可逆性/条件 | 是 | E-04/E-13/E-15/E-16 | 审批/误拦 | 结构有效/安全 | [→](../positions/action.md) |
| commit | 证据够不够授权 | 授权判据 | 是（设计） | E-20 + gap | 无实现 | 已落地 | [→](../positions/commit.md) |

> 这不是「六个都该做」；是「六个位置问的问题不同」。选择规则见 [02 §2](../../02-engineering-playbook/sections/map.md#23-选位置六个时刻--四个轴外位置)。


<a id="4-强度覆盖率直线是摘要矩阵是操作定义"></a>
### 2.4 强度–覆盖率：直线是摘要，矩阵是操作定义

#### 2.4.1 直线（H，摘要）

```
约束强度   弱 ──────────────────────────────▶ 强
覆盖率     广 ◀────────────────────────────── 窄
位置      context   memory   evidence  checker  action  commit
```

**这是组织假设（H），不是 E。** 它把六位置排成一个「越强越窄」的次序，但没有被任何一条 E 直接测量；E-01/E-04 只作边界证据，不作证明。

#### 2.4.2 矩阵（D，操作定义）

把「覆盖率」拆成七类失效 × 八个位置后，直线要修正：

| 读法 | 是否成立 | 说明 |
|---|---|---|
| 越强，能**阻断**的失效类别越少 | 近似成立 | action/checker/memory 各只对 1 类 `●`；context/evidence/read-path 0 类；commit/determinism 没有 `●`（只有 ◐/?D） |
| 越强，能**影响**的失效类别越少 | **不成立** | checker 有 4 个 `●/◐`，action 只有 3 个 |
| 强度可以排成一条线 | **不成立** | 位置是专门化的；commit/determinism 的 `?D` 不能当强弱 |

**操作结论**：要问「这个位置能不能碰到这类失效」，查 [coverage 矩阵](../across-positions/coverage.md)，不查直线。直线只说明「强端少而硬、弱端多而软」。

> 如果你只想要一个可操作的结论：**强端不是更好，是更窄；用错尺子会得出「无增益」。**（H；矩阵是 D，不是测量）

**什么会推翻它**：强端机制在广覆盖上稳定有效，或弱端机制在高覆盖下仍能改变走向，且不是单案例；或出现可复算的覆盖率测量。
