---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# 术语与内码速查（03）

> 第一次读 03 先看这一页。这里只解释「读 03 会用到的词与码」；完整术语见仓库根 [GLOSSARY](../../../GLOSSARY.md)。
>
> **术语基线**：ADR 0011 / 2026-11；K0–K4 标 `local`（论文条件，非 normative 源）。

<a id="term-sources"></a>
## 0. 名词从哪来（N / local）

> `N:` = 规范性锚，只定词与合格性、**不撑效果**；`local` = 本仓库工作词，首现解释。完整清单见 [规范主干](../../../topics/trunk.md)，逐词判定见 [术语基线](../../../meta/term-baseline.md)；撤回依据见 [evidence/ledger §2.5](../evidence/ledger.md#w-table)。

| 词 | 来源 | 一句话 |
|---|---|---|
| 本体 / 顶层本体 | `N: ISO/IEC 21838-1/-2`（本仓库义更宽，判 `broader`） | 概念/关系/约束的显式规范；标准只给 TLO 合格性 |
| 可复用模块 / 最小承诺 | `N: OMG Commons 1.3` | 模块化本体与最小承诺；不是 TLO |
| 约束 / 校验 / 三态 | `N: W3C SHACL` | 图约束与三态；不能折叠 unknown |
| 规则 / target | `N: W3C SHACL-AF` | 规则与 target；不是执行点 |
| 推理 / profile | `N: W3C OWL 2 Profiles` | profile 语义；不证明效果 |
| 策略表达 / 判定架构 | `N: W3C ODRL 2.2` / `N: OASIS XACML 3.0` | 写法与 PDP/PEP；不含执行点 |
| 六位置 / 接缝 / 强度 / 覆盖率 / 形态 | `local` | 本仓库分类轴；没有标准定义 |
| 接地 / checker / 动作闸 / 落盘 | `local` | 机制词；原锚撤回的按 W 表重测 |
| 论文条件 K0–K4 | `local`（论文条件，非术语） | 五个实验条件编号 |

## 1. 五个主张标记

| 标记 | 含义 | 要求 | 例子 |
|---|---|---|---|
| **E** | 证据条目，来自 [conclusions](../../../topics/conclusions.md) | 必须链 conclusions；写清等级与限定 | E-12、E-20 |
| **C** | 冲突/方法论条目 | 不是证据等级；不合成结论 | C-03、C-04 |
| **H** | 组织假设 | 必须写「什么会推翻它」 | 强度–覆盖率反向 |
| **D** | 设计提案/概念架构 | 必须写「无实现/未测」 | commit gate 三段式 |
| **G** | 缺口 | 必须写「缺什么数据」 | M1–M5 |

> **纪律**：`deliverables/` 只引 E-xx，不引 L-xx。03 里如果只有 topics 的 L 支撑，要么在 topics 升 E，要么在 03 标 H/D，不能假装是 E。

## 2. 位置与轴

| 词 | 含义 | 注意 |
|---|---|---|
| **六位置** | context → memory → evidence → checker → action → commit | 按回路功能排；context 是供给、determinism 是第六个时刻，不在强度谱上 |
| **谱外/轴外** | determinism、read-path、supply、reasoning、training | 不在六位置强度谱上，但可以作为能力/边界出现 |
| **seams（接缝）** | 本体在回路的哪个时刻介入 | 六个 seams + 轴外 |
| **supply** | 查询/映射编译（OBDA 等），本体在供给时被执行 | 不是 `context`；不校验输出 |
| **强度** | 违反时能否改变走向（剪动作/拒输出/阻落盘/要授权） | 不是「本体多完整」 |
| **覆盖率** | 某位置能碰到的失效类别集合 | **不是百分比**；不是召回率 |
| **执行形态** | 机器拿本体做了什么：`engine` / `compiled` / `context` / `label` / `none` | 「有引擎」≠「会拦」≠「有授权」 |

## 3. 覆盖率符号

| 符号 | 含义 | 判据 |
|---|---|---|
| `●` | 能阻断/改变走向 | 能在坏结果发生前或发生时阻止；有实现或强机制证据 |
| `◐` | 能影响/部分覆盖 | 能改变输出或流程，但不能单独阻断 |
| `○` | 碰不到 | 该位置对该类失效没有作用 |
| `?D` | 只有设计 | 没有实现，不能判 |

> **`●` 的计数不是「越强越多」。** 矩阵是分类，不是测量；强弱不能按格子总数排（[coverage §3](./../across-positions/coverage.md)）。

## 4. 边界与等级

| 词 | 含义 |
|---|---|
| **B1–B15** | 15 条边界：什么不能当工作前提 / 什么会改变判断 |
| **N01–N12** | 12 条反例：常见主张 + 已测反例 + 什么会推翻它 |
| **已核** | 一手原文/代码核对过 |
| **已核（代码）** | 读代码核对过，不是效应量 |
| **已核（概念架构）** | 概念架构核对过，没有实现（**不要用它当「已核」的证据**） |
| **推测** | 从一手材料推的，或工程估算 |
| **存疑/contested** | 主结论可站，某个读法被削弱 |
| **三态** | SHACL 的 0/2/3：通过/违反/未检查完（3 = undetermined） |

> 等级词汇以 [台账 §2](./../evidence/ledger.md) 的四档为准；`已核（概念架构）` 只在 commit 卡出现，不是第五档等级的证据。

## 4.1 指标与符号

| 符号 | 含义 | 坑 |
|---|---|---|
| `p_h` | 命中率：回答所需证据已在上下文中的比例 | 不是「检索到没有」 |
| `p_min` | 编译盈亏平衡命中率：`2% + c/(0.929Q)` | `c/Q` 要自己量 |
| `c` | 每次编译成本（相对单位） | 不是 token 单价 |
| `Q` | 每问 token 预算 | 与上下文窗口不是一回事 |
| `FA` | false alarm：checker 把对的判错的比例 | 与 catch 分开报 |
| `HSR` | harm success rate：有害轨迹比例 | 不是 task success |
| `CMR` | 跨期匹配率：同一实体跨会话能否对上 | 与 `Acc@complete` 不同 |
| `SLB` | solver-like behavior：轨迹里先算答案、程序只复述 | 不是「模型推理强」 |
| `δ` | miss 上限（校准证书的容忍度） | 不是 false-block 率 |

## 5. 内码

| 码 | 指向 | 在哪 |
|---|---|---|
| `O-xx` | 对象地址（公式/代码/表/反例） | [objects](../../../topics/objects.md) |
| `C-xx` | 冲突/方法论条目 | [conclusions](../../../topics/conclusions.md) |
| `M1–M5` | 03 的 5 条研究期待（承重假设） | [gaps](../evidence/gaps.md) |
| `B/R` | 边界 / 反例 | [boundaries](../evidence/boundaries.md) |
| `T1–T5` | 动作本体里的类型化逆关系 | [action](../positions/action.md) |
| `K0–K4` | N&D 实验条件代号（原始点位/点位语义/知识投影文本/流程摘要/运行记录检索；**非标准**） | [01 K 页](../../01-capability-status/02-sections/92-k-ladder.md) |
| `Q-01` / `RQ5` | 存疑条目 / 研究问题 | [conclusions](../../../topics/conclusions.md) |
| `P0/P1b/P1c/P2` | 按机制分派的度量优先级 | [measurement](../across-positions/measurement.md) |

## 6. 常见误读

| 误读 | 实际 |
|---|---|
| 「有引擎 = 会拦」 | 执行 ≠ 健全 ≠ 授权（E-20） |
| 「强端更好」 | 强端不是更好，是更窄；六位置是专门化的 |
| 「覆盖率是一条强度线」 | 覆盖率是类别集合；矩阵不是测量 |
| 「read-path 能防泄漏」 | 它是 best-effort 可见性过滤；fail-open、只删 subject、单实现 |
| 「commit gate 已落地」 | 只有概念架构；无实现 |
| 「M1–M5 是结论」 | 是研究期待；未开/部分，不是证据 |
