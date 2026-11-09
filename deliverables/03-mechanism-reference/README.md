---
status: draft
deliverable_status: draft
updated: 2026-11-09
target: 架构师 / 研究者
basis: E-01–E-20, C-03/C-04; topics/README 四轴
---

# 03 · 机制参考：六个位置、三根分类轴与证据边界

> **读者**：架构师 / 研究者 ｜ **回答**：为什么是这些位置/形态、证据边界在哪 ｜ **不回答**：具体怎么做（去 02）、今天能做成什么（去 01）。

> **这不是一本手册，也不是教程。** 它是交付物的「依据层」：解释为什么把本体接在六个位置、三根分类轴怎么分、每条判断的证据边界在哪。
>
> 2026-11-09 起，本目录从「一篇长附录」升级成四层：**入口（本页）→ 位置卡 → 横切页 → 证据台账/边界/缺口**。原第三章保留为长版论证 [appendix-constraint-spectrum.md](./appendix-constraint-spectrum.md)（约 0.97 万字）；附录是历史论证，位置细节以 `positions/` 为准。


## 0. 一页结论

- **强度不是好坏。** 强度问「违反时能不能改变走向」；覆盖率问「能碰到多少类失效」。强端管得硬，但管得少。
- **强端不是更好，是更窄。** 但它不是一条可排序的强度线：六位置是专门化的，查 [coverage 矩阵](./cross-cutting/coverage.md)，不查直线。
- **尺子跟机制走。** 不改变走向的供给/契约位置，准确率/token 仍可用；能改变走向的判定/动作/落盘位置，用单一 accuracy/reward 会错配（C-03）。
- **六个位置问的问题不同。** context 看到什么、memory 记得什么、evidence 带什么依据、checker 对不对、action 能不能做、commit 够不够授权；不是「六个都该做」。
- **承重墙是 M1/M2。** 没有同本体跨位置对照，也没有覆盖率测量；这份参考能给出分类与边界，不能给出效应量。


## 1. 怎么读

### 1.1 加载集（按需披露）

| 要做 | 只读 | 不读 |
|---|---|---|
| 查某个位置 | `positions/<position>.md` + 本页 §3 | 附录全文、其他位置卡、`src/` 原文 |
| 查某条判断的边界 | [boundaries.md](./boundaries.md) + [evidence-ledger.md](./evidence-ledger.md) + [conclusions](../../topics/conclusions.md) 的 E 行 | `src/` 原文、其他派 `mechanism.md`、全部 `paper.md` |
| 查为什么是六个位置 | 本页 §2/§3 + [coverage](./cross-cutting/coverage.md) + [execution-forms](./cross-cutting/execution-forms.md) | 全部论文正文 |
| 查下一步研究什么 | [gaps.md](./gaps.md) + 各派 `frontier.md` | 本页不复制候选 |

> 反向链见 [meta/loading §从交付物倒查](../../meta/loading.md#从交付物倒查反向加载)：边界 → E 行 → digest §5/§9 → 附录。


### 1.2 三条阅读路径

| 时间 | 读什么 | 得到什么 |
|---|---|---|
| 10 分钟 | §0 + §2.3 六位置表 | 知道六个位置问什么、为什么不是一条强度线 |
| 1 小时 | §1 + §2 + §3 索引 | 能指到某个位置卡、某条边界、某个缺口 |
| 深读 | `positions/` + `cross-cutting/` + `boundaries.md` + `evidence-ledger.md` | 能复述机制、证据、不能证明什么 |


### 1.3 读法

- 想知道「这个机制能不能用」→ [01 §2 的能力矩阵](../01-capability-status/README.md#2-地图能力矩阵)。
- 想知道「拿本体做 X 怎么做」→ [02 §3.1 的 R0–R12](../02-engineering-playbook/README.md#31-十二条工程做法r0r12)。
- 想知道「为什么是这六个位置」→ 本页 §2/§3 + [coverage](./cross-cutting/coverage.md) + [execution-forms](./cross-cutting/execution-forms.md)。
- 想知道「这个位置该量什么」→ [measurement](./cross-cutting/measurement.md)。
- 想知道「这条判断的边界」→ [boundaries.md](./boundaries.md) + [evidence-ledger.md](./evidence-ledger.md)。
- 想知道「下一步研究什么」→ [gaps.md](./gaps.md) + 各派 `frontier.md`。


## 2. 地图：主张、轴、位置

### 2.1 主张类型：E / C / H / D / G

03 里每个规范句都要带一个标记；没有标记的按「推测」读。

| 标记 | 含义 | 例子 | 要求 |
|---|---|---|---|
| **E** | 证据条目，来自 [conclusions](../../topics/conclusions.md)；等级看原表 | E-04、E-20；E-19 是 `推测` | 必须链 conclusions；写清等级与限定 |
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

> **六个位置不是六个时刻。** `determinism` 是第六个时刻，但不在强度谱上；`context` 不是时刻，是供给；`read-path`/`supply` 是轴外位置。别把四张表混成一张。谱外位置（determinism / read-path / supply / reasoning / training）见 [positions/outside.md](./positions/outside.md)。


<a id="3-六个位置一页表"></a>
### 2.3 六个位置一页表

| 位置 | 问什么 | 本体角色 | 能阻断 | 主证据 | 主要代价 | 不能证明 | 卡 |
|---|---|---|---|---|---|---|---|
| context | 模型看到什么 | 投影/编译 | 否 | E-01/E-12/E-14 | token/编译 | 规则被执行 | [→](./positions/context.md) |
| memory | 下一轮记得什么 | 状态/对齐 | 否 | E-05/E-17 | 维护/训练信号 | 跨运行确定性 | [→](./positions/memory.md) |
| evidence | 产出带什么依据 | 证据契约 | 否 | E-03 | token/集成 | 形式保证 | [→](./positions/evidence.md) |
| checker | 产出对不对 | 外部判据 | 是 | E-02/E-20 | 每条判定/维护 | 语义正确 | [→](./positions/checker.md) |
| action | 动作能不能做 | 可逆性/条件 | 是 | E-04/E-13/E-15/E-16 | 审批/误拦 | 结构有效/安全 | [→](./positions/action.md) |
| commit | 证据够不够授权 | 授权判据 | 是（设计） | E-20 + gap | 无实现 | 已落地 | [→](./positions/commit.md) |

> 这不是「六个都该做」；是「六个位置问的问题不同」。选择规则见 [02 §2](../02-engineering-playbook/README.md#2-选位置六个时刻--四个轴外位置)。


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

**操作结论**：要问「这个位置能不能碰到这类失效」，查 [coverage 矩阵](./cross-cutting/coverage.md)，不查直线。直线只说明「强端少而硬、弱端多而软」。

> 如果你只想要一个可操作的结论：**强端不是更好，是更窄；用错尺子会得出「无增益」。**（H；矩阵是 D，不是测量）

**什么会推翻它**：强端机制在广覆盖上稳定有效，或弱端机制在高覆盖下仍能改变走向，且不是单案例；或出现可复算的覆盖率测量。


## 3. 主体：六张位置卡 + 三张横切页

> 本页只做索引；每张卡回答「这个位置怎么跑、能改变什么、拦不住什么、证据到哪」。

| 卡 | 回答 | 入口 |
|---|---|---|
| context | 模型看到什么；供给/投影/编译 | [positions/context.md](./positions/context.md) |
| memory | 下一轮记得什么；registry/状态 | [positions/memory.md](./positions/memory.md) |
| evidence | 产出带什么依据；grounding | [positions/evidence.md](./positions/evidence.md) |
| checker | 产出对不对；三态/漏检/误报 | [positions/checker.md](./positions/checker.md) |
| action | 动作能不能做；可逆性/审批 | [positions/action.md](./positions/action.md) |
| commit | 证据够不够授权；设计/无实现 | [positions/commit.md](./positions/commit.md) |
| outside | 轴外位置：read-path / supply / reasoning / training | [positions/outside.md](./positions/outside.md) |

**横切页**：

- [measurement](./cross-cutting/measurement.md)：每个位置该量什么、不能量什么。
- [coverage](./cross-cutting/coverage.md)：七类失效 × 八位置的矩阵；组织假设，不是测量。
- [execution-forms](./cross-cutting/execution-forms.md)：执行链与四种 `engine` 语义。
- [boundaries](./boundaries.md)：15 条边界；[evidence-ledger](./evidence-ledger.md)：E-xx 台账；[gaps](./gaps.md)：下一步。

## 4. 边界与反例

### 4.1 证据边界：15 条，最常被越过的 5 条

完整表在 [boundaries.md](./boundaries.md)（每条带「挂在哪 / 什么会改变它」）。这里只留最容易被越过的五条：

1. **B1**：强度–覆盖率反向没有被直接测量；直线是 H，矩阵是 D。
2. **B2**：E-01 的 ontology 是 `not measured`；不能写「本体无增益」。
3. **B3**：E-04 的结构贡献未隔离、false-veto 未测；不能写「结构判据有效」。
4. **B13**：commit 写路径无实现；E-20 只给否定性证据。
5. **B14**：单来源为主、无独立复现；最高等级是已核。

> 每条 E 的限定见 [evidence-ledger.md](./evidence-ledger.md)；更细的逐条解释见 [附录 §3.7](./appendix-constraint-spectrum.md#37-本章不能证明什么)。


<a id="8-期待与数据需求验收规格"></a>
## 5. 验收与缺口

### 5.1 期待与数据需求（验收规格）

> 这一节不是结论，是**这份参考要成立需要什么证据**。它把「什么会改变判断」写成可检验的句子；缺的数据回 `frontier` 找，不在交付物里补。这是验收规格（非 E）。详细拆解与研究会话在 [gaps.md](./gaps.md)。

| # | 期待（可证伪） | 支持它需要的数据 | 现在的证据 | 缺口 |
|---|---|---|---|---|
| M1 | 同一份本体换位置/形态，效应量不同且大于 run-to-run 噪声 | 同一本体 ≥2 位置/形态；同一度量；重复运行 | 只有跨来源弱对照；E-18 噪声基线；E-12 形态比较 | 同本体跨位置对照 |
| M2 | 强度越高、覆盖率越窄（反向关系） | 每个位置的覆盖率测量 + 效应量 | H；矩阵是 D；E-01/E-04 边界 | 覆盖率测量 |
| M3 | 「有引擎」不等于「会拦/有授权」 | 代码级调用链 + 阻断测试 + 授权测试 | E-20 4 个项目；执行链五层 | 更多实现；写授权 |
| M4 | C-03 的度量错配是文献冲突主因 | 同一机制用任务账/风险账两把尺子测 | E-01/E-04/E-15 的间接证据；八行分派 | 配对度量实验 |
| M5 | 每条 E 的限定在跨域/独立复现后仍成立 | 跨域/独立复现；同一 E 的重复测量 | 单来源为主；无已证 | 独立复现（仓库外） |

**怎么用**：M1/M2 是这份参考的「承重墙」；它们不成立，六位置表仍可作分类，但「强度–覆盖率反向」只能当 H。M3/M4/M5 是边界检查，不是新结论。

### 5.2 缺口入口

- 不是「怎么改词」，是「下一步做什么」：见 [gaps.md](./gaps.md)。
- 每个位置卡的「上游指针」指向 `topics/` 的 mechanism/claims；本页不复制候选。


<a id="7-维护规则"></a>
## 6. 关系与维护

### 6.1 与另外两份交付物的关系

| 交付物 | 回答 | 读者 | 形态 |
|---|---|---|---|
| [01 现状](../01-capability-status/README.md) | 今天能做成什么、不能承诺什么 | 决策者/工程负责人 | 判断 + 矩阵 |
| [02 工程实施](../02-engineering-playbook/README.md) | 拿本体做某件事，具体怎么做 | 工程负责人/架构师 | 步骤 + 接口 + 验收 |
| **03（本份）** | 为什么是这些位置/形态，证据边界在哪 | 架构师/研究者 | 参考 + 边界 |

**一句话**：01 告诉你「值不值得做」，02 告诉你「怎么做」，03 告诉你「凭什么这么说、说到哪为止」。

### 6.2 维护规则

- **canonical 在 `positions/` 与 `cross-cutting/`**；附录是长版论证，不改结论。两者冲突时，以位置卡/横切页为准，并回改附录指针。
- 本页只从 [conclusions](../../topics/conclusions.md) 与 [topics/README](../../topics/README.md) 抽取；**不新增判断**。
- E-xx 变化时，先改 `topics/`，再回改本页、位置卡、台账与边界；不要在本页调和冲突。
- H/D 必须始终带标记；不要因为引用次数多就把它写成 E。
- 原 7 章书稿计划不再维护；没有独立 handbook。


### 6.3 本目录怎么长

| 文件 | 回答 | 什么时候读 |
|---|---|---|
| 本页 | 三根分类轴、六位置总表、M1–M5 | 第一次进 03 |
| [positions/context.md](./positions/context.md) | 供给位置为什么不能阻断 | 查知识供给 |
| [positions/memory.md](./positions/memory.md) | 为什么记忆是状态 | 查跨轮/身份 |
| [positions/evidence.md](./positions/evidence.md) | 输出契约为什么不是闸门 | 查接地等级 |
| [positions/checker.md](./positions/checker.md) | 判定器质量曲线与三态 | 查输出后判定 |
| [positions/action.md](./positions/action.md) | 三种动作前子机制 | 查可逆性/条件/分配 |
| [positions/commit.md](./positions/commit.md) | 为什么「能推理」不等于「能授权」 | 查落盘前 |
| [positions/outside.md](./positions/outside.md) | determinism/read-path/supply/reasoning/training 为什么在谱外 | 查第六时刻/轴外 |
| [cross-cutting/measurement.md](./cross-cutting/measurement.md) | 这个位置该量什么 | 设计验收 |
| [cross-cutting/coverage.md](./cross-cutting/coverage.md) | 强度–覆盖率到底是什么 | 查 §4/争论 |
| [cross-cutting/execution-forms.md](./cross-cutting/execution-forms.md) | 形态与执行链 | 查「有引擎」 |
| [evidence-ledger.md](./evidence-ledger.md) | 每条 E 支持/不支持哪个位置 | 核证据 |
| [boundaries.md](./boundaries.md) | 15 条边界 + 可证伪条件 | 审稿/自查 |
| [gaps.md](./gaps.md) | M1–M5、负结果、下一步 | 规划研究 |
| [appendix-constraint-spectrum.md](./appendix-constraint-spectrum.md) | 长版论证（历史） | 要完整论证时 |

> 本页只做入口；稳定判断在位置卡/横切页，证据在台账，缺口在 gaps。位置卡统一 8 字段：机制 / 触发输入输出 / 能改变什么 / 拦不住什么 / 使能条件 / 证据与边界 / 可证伪条件 / 上游指针。
