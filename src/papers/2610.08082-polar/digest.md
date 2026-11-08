---
status: draft
updated: 2026-11-08
quality: B
based_on: card.md
claims: [E-04, E-13]
---

# POLAR：动作前问「有没有逆操作」，而不是「模型觉得危不危险」

> 这篇消化不假设你读过论文。先把「可逆性门」讲清楚，再解释数字、T1-only 的反例、能力反向、工程上怎么用。

## 0. 三句话

1. **它问什么**：工具调用 agent 要改真实系统（取消订单、退款、改配置）；能不能在动作执行前，用**结构化的可逆性判据**阻止不可恢复的动作？
2. **它怎么做**：两层本体——静态动作本体（T1–T5 可逆关系 + curator 权重）+ 动态状态投影；从候选动作往回找逆操作序列，整条序列取「最弱一步」分数；低于阈值就 veto。
3. **它发现什么**：在 τ²-bench 上，airline 的弱中模型有 +0.11–0.18 的收益，但 18 个模型-域格只有 8 个改善；retail 和更强的模型经常回退。更关键的是 **T1-only 接近 blanket veto，增益却不比 full 小**——测到的收益可能来自「保守拒绝」，不是「结构推理」。

## 1. 它解决什么问题

### 1.1 背景

工具调用 agent 一旦拿到写权限，最危险的失败不是答错，而是**不可恢复的动作**：取消唯一订单、给错误账户退款、删除唯一副本、对外发送不可撤回的消息。事后补偿往往来不及，或者根本不存在。

现有护栏有三类：
- **事后补偿**：先执行，再用注册的 compensator 撤销；问题是撤销可能失败。
- **LLM-as-a-judge**：让模型给 allow/block 标签；问题是标签没有结构依据，不可审计。
- **微调/CoT**：让模型在动作前多想；问题是仍然靠模型自觉。

POLAR 的立场：**安全是结构问题**。不要问「模型觉得这个动作危不危险」，要问「**是否存在一个可接受的逆操作序列**」。后者的答案来自本体 + 状态查询，而不是模型自评。

### 1.2 一个具体例子

用户说：「请取消我的预订 R1。」（先假设一个 T1/T2 有界可逆的工具；再看 airline 的真实情况。）

- **假设情形**：Layer A 给 `cancel_reservation` 一条 T2 有界可逆注释；Layer B 检查 bound（座位/支付状态）；找不到完整逆序列或最弱一步 φ<0.80，就 veto。
- **airline 实际**：`cancel_reservation` **没有 T1 注释**；取消后重订会分配新的 `reservation_id`，所以它是 T3 compensable，不是 `book_reservation(R1)` 这种精确逆。POLAR 会走 T3/NO_CANDIDATE，而不是 T1。
- 这个区别很重要：把 airline 的取消/重订当成 T1，会高估结构反向组合的能力。

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **POLAR** | 本文的可逆性门系统名；论文没有把它展开成首字母缩写。 |
| **mutating tool** | 会改变外部世界的工具（取消、退款、写配置），不是只读查询。 |
| **reversibility** | 这个动作能不能撤销；不是「危不危险」的同义词。 |
| **inverse sequence（π）** | 一串能把状态撤回的逆操作；POLAR 找的是候选序列。 |
| **Datalog** | 一种声明式规则语言；本文用它写逆关系/约束。 |
| **Layer A（动作本体）** | 手写的 Datalog：每个 mutating tool 的逆关系 T1–T5、curator 权重。 |
| **Layer B（状态投影）** | 从真实 DB + 已执行工具重建的 `slot(entity,id)=value`。 |
| **T1–T5** | 五类可逆关系：精确逆、有界可逆、可补偿、不可逆消费、外部副作用。 |
| **φ（phi）** | 每一步的可逆性分数，0–1；整条序列取 min。 |
| **curator weight（w）** | 人工标注者对这条逆关系的置信度；T3 还有 loss weight。 |
| **DecisionPolicy** | 拿到 φ 后决定 APPROVE / VETO / ESCALATE；判定与执行分离。 |
| **blanket veto** | 不看结构、一律拒绝 mutating 动作。 |
| **τ²-bench** | 多域工具调用基准（airline/retail/telecom）；本文 6 模型 × 3 域 × 4 臂。 |
| **reward** | 任务完成奖励；**不是**防伤害的直接度量。 |

## 3. 它怎么做

### 3.1 两层本体

| 层 | 内容 | 何时构建 | 谁维护 |
|---|---|---|---|
| Layer A | 静态动作本体：T1–T5 类型化逆关系，每条边带 curator 权重 w | 域级，手写 | 域 curator |
| Layer B | 动态状态投影：`slot(entity_type, entity_id)=value`，从 τ²-bench DB + 已执行工具记录重建 | 每轮 | 系统，不让 LLM 想象 |

### 3.2 五个可逆层级

| tier | 关系 | 每步 φ | 含义 |
|---|---|---|---|
| T1 | `inverse_of(Ta,Tb,Slot,w)` | `w` | 有精确逆操作 |
| T2 | `bounded_reversibility(T,Bound,w)` | `w · 1[Bound at s]` | 在边界内可逆 |
| T3 | `compensates(Ta,Tb,LossClass,w)` | `w · (1−w_loss)` | 可补偿，但有损 |
| T4 | `irreversibly_consumes(T,EntitySlot)` | 0 | 不可逆消费 |
| T5 | `external_side_effect(T,SinkClass)` | 0 | 外部副作用，fail-closed |

### 3.3 反向搜索

给定候选动作，从**最近的动作往回**枚举 Layer A 里的 undo 边，组合候选逆序列 π；T2 的 bound 与 overlap 对 Layer B 当前投影检查。成功 → 得到 π；失败 → 报告第一个不可接受步骤及原因。**不调用外部符号规划器**；判定由匹配到的注释 + Layer B 快照决定。

### 3.4 评分与策略

- 整条序列的分数是**最弱一步**：`φ_POLAR(π)=min φ(u)`；一步不可逆就把整条拉到 0，并报告 bottleneck。
- 阈值 τ=0.80；低于阈值或找不到完整 π → Veto。
- DecisionPolicy 分离「判定」与「执行」：APPROVE / VETO / ESCALATE。**只有 VetoPolicy 有可比的 reward 结果**；Escalate/Advisory 的归档均值与提交表冲突，作者撤回比较。
- 评分前先做 admissibility：provisional / revoked / disputed / 未接地的注释不进入序列。

### 3.5 被评估的 wrapper

- **不模拟完整 post-action state s′**；只对可用 Layer B 当前投影检查。
- ThreeWayClassifier 与 IntentParser 不作为决策时组件。
- VetoPolicy 用静态 refusal 替换 agent message。

## 4. 结果：数字与条件

### 4.1 总体

- 6 个模型 × 3 域 × 4 臂；每格 150 attempted runs；72 格；10,800 rollouts。
- **18 个 model–domain 格只有 8 个改善**；airline 的六个模型中四个 +0.11–0.18。
- retail 与更强模型经常回退。

| 模型 | airline | retail | telecom |
|---|---|---|---|
| llama-3.1-8b | +0.182 | +0.029 | +0.053 |
| qwen3-8B | +0.111 | −0.100 | +0.038 |
| nemotron-9b | +0.110 | −0.033 | −0.053 |
| gemini-flash-lite | +0.109 | −0.026 | 0.000 |
| gpt-oss-120B | −0.073 | −0.242 | +0.020 |
| qwen3.5-27B | −0.119 | −0.209 | −0.060 |

> 出处：Table 3, p.6。Δ 是「分别误差过滤后的 arm mean 差」，不是配对估计；每格 150 attempted runs，valid counts 不同。主 cell（qwen3-8B airline）配对估计 +0.119，95% CI [+0.057,+0.184]（Appendix D）。

### 4.2 能力反向

- **Δ 随 baseline reward 上升而下降**：airline −0.76、retail −0.67、telecom −0.31；R² 0.92/0.98/0.65。**这是描述性拟合：baseline 同时进入横纵轴，存在数学耦合；斜率不识别 causal headroom。**
- **这是六点描述性拟合，不是部署阈值**；作者明确说不能拿它做 zero-crossing 规则。

> 出处：Figure 4（Δ vs baseline reward）；斜率与 R² 在 §4.2。

### 4.3 阈值保留率

| τ | airline | retail | telecom |
|---|---|---|---|
| 0.50 | 100% | 100% | 100% |
| 0.80（anchor） | 36.6% | 100% | 98.7% |
| 0.90 | 17.6% | 48.9% | 98.7% |

同一个阈值在不同域含义不同；airline 的 verdict 分布对工作点很敏感。

> 出处：Table 4, p.7。36.6% 是「996 条有非空候选池的 logged decisions」在独立 instrumented 固定轨迹 run 上的保留率；原文明确它不估计其他阈值的 reward，也不确立最优阈值。

### 4.4 tier ablation

| 配置 | Δ | 95% CI |
|---|---|---|
| full（T1,T2,T3） | 0.080 | [0.013, 0.147] |
| no T3 | 0.073 | [0.020, 0.127] |
| T1+T3 | 0.087 | [0.027, 0.147] |
| T1 only | 0.087 | [0.020, 0.153] |
| no irreversible（T4/T5 以 φ=1 放行） | 0.060 | [−0.007, 0.127] |

**T1-only 在 airline 没有 T1 注释时接近 blanket veto，增益却不比 full 小。** 作者自述：不能把「结构反向组合」的贡献与「保守拒绝」分开。

> 出处：Table 5, p.7–8。这是 **qwen3-8B airline、150 runs/arm 的单格消融**，不是 18 格整体；五个配置各自 separate baseline rerun，ablation full 0.080 ≠ 主实验 +0.111。

### 4.5 被拦了什么

- 1,745 条 blocked decisions；最高 block 次数：GPT-OSS-120B retail return 150 次、exchange 103 次；Nemotron-9B airline update_flights 77 次。
- **没有独立的 harm/authorization 标签**；无法算 false-veto 率。

> 出处：§4.6 block log；1,745 条 blocked decisions。

### 4.6 为什么 T1-only 接近 blanket veto

airline 的工具在 Layer A 里**没有** T1 注释；T1-only 遇到 mutating tool 时找不到精确逆，于是对**所有** mutating 调用返回 veto。它不是「更保守的结构判断」，而是**结构退化成「凡 mutating 就拒」**；这正是 blanket veto 的形态。

实验结果却显示它的增益与 full 相近（0.087 vs 0.080），说明 airline 的收益可能主要来自「拒绝 mutating 动作」，而不是「结构反向组合」。要分开这两者，必须做同一 baseline、同一轨迹的配对实验；本文没有。

## 5. 这些数字不能说明什么

1. **reward 不是防伤害。** 被 veto 的风险动作不体现在 reward 里；airline 的 +0.11 只说明任务奖励，不能证明防伤害，也不能隔离 reverse search 与 conservative blocking。
2. **T1-only ≈ blanket veto。** 测到的收益可能来自保守拒绝；不能声称「结构推理有效」。
3. **retail 的失败不一定是机制失败。** 退货/换货是合法用户请求；可逆性不是唯一判据，需要意图/授权层。
4. **不是部署阈值。** 斜率是六点描述性拟合；作者说给不出 zero-crossing。
5. **不模拟完整 s′、不验证逆执行。** 「有逆序列」不等于「恢复会成功」。
6. **单基准、单 wrapper。** τ²-bench 是合成环境；对照臂是适配，不是复现。
7. **false-veto 未知。** 1,745 条 blocked decisions 没有 harm/authorization 标签。

## 6. 工程上怎么用

### 6.1 复刻顺序

1. **先列 mutating tools 和槽位。** 哪些工具会改世界？改哪些实体/字段？
2. **写 T1–T5 关系。** 每个工具：有没有精确逆、有没有 bound、补偿损失、不可逆消费、外部副作用；给 curator 权重。
3. **状态投影必须来自真实系统。** 从 DB + 已执行工具重建 Layer B；不让 LLM 想象。
4. **反向搜索只判「有没有路」。** 不要求执行逆操作，也不要求证明恢复成功；先把「有没有路」和「路好不好」分开。
5. **分数取最弱一步。** 一步不可逆就整条归零；bottleneck 就是审计理由。
6. **判定与执行分离。** 同一个 φ 可以驱动硬 veto、escalate、advisory；策略可配置。
7. **阈值先按保留率/覆盖率校准，再按 reward 校准。** airline 在 0.80 只保留 36.6%，retail 100%；这个 36.6% 是 996 条有非空候选池的 logged decisions 在固定轨迹上的保留率，不是 reward 曲线，也不估计最优阈值。
8. **上线前单独量 false-veto。** 必须有 harm/authorization 标签或人工审计。
9. **按能力分层部署。** 弱模型 + 高不可逆风险：硬 veto；强模型：advisory/动态门；强模型 + 合法用户意图：不要用可逆性单独裁决。

### 6.2 成本与使能

| 成本 | 一次性/每次 | 说明 |
|---|---|---|
| Layer A 本体 | 每域一次性 | 人工 curator；工具/槽位/逆关系；本文未测工时 |
| Layer B 状态投影 | 集成一次性 | 接 DB + 工具执行记录；必须真实 |
| 反向搜索 | 每次候选调用 | 图遍历 + T2 bound 检查；轻量 |
| 阈值/策略校准 | 每域一次 | 保留率、reward、false-veto |
| 审计/日志 | 每次 | bottleneck + 注释边；否则不可审计 |
| 维护 | 工具/本体变更 | 新工具、槽位变更、注释修订 |

**使能条件**：类型化工具 schema；可读真实状态；可枚举的撤销操作；有 curator 维护本体。

**2022 年做会卡在哪**：工具调用 agent 不普遍；没有 τ²-bench 这类多域工具基准；状态投影/工具 schema 不标准；LLM 多步工具任务不稳。

### 6.3 何时用 / 何时别用

**用**：动作不可逆且代价高；模型弱于域要求；域规则可查询成事实；有真实状态投影；能承担本体维护。

**别用（本文观察/读者推断）**：强模型 + 高基线常回退；用户意图主导、动作本身合法（retail）；拿不到状态；只用 reward 评估；本体没人维护。是否部署要自己的 false-veto/成本数据，不能照搬斜率。

### 6.4 最小落地清单

1. **列 mutating tools 和槽位。** 只对会改变外部世界的工具建本体。
2. **写 T1–T5 + curator 权重。** 先只写 T1/T4/T5，T2/T3 可以后补；但 T1-only 会退化，别拿它当 full。
3. **接真实状态投影。** 从 DB + 工具执行记录重建 Layer B；不要让 LLM 想象。
4. **反向搜索只判「有没有路」。** 先不验证逆执行；把「有路」与「路能走通」分开。
5. **阈值按保留率校准。** airline 在 0.80 只保留 36.6%，retail 100%；同一阈值跨域不通用。
6. **上线前单独量 false-veto。** 没有 harm/authorization 标签，就不知道拦对了多少。
7. **按能力分层部署。** 弱模型硬 veto；强模型 advisory/动态门；合法意图主导的动作不要只靠可逆性。

## 7. 质量与边界

- **证据类型**：实证·基准（一手正文）。
- **强项**：多模型、多域、多臂；有 tier ablation、阈值敏感性、block log；作者主动写清「reward 不是伤害度量」。
- **主要威胁**：单一合成基准；无 harm/authorization 标签；T1-only ≈ blanket veto，结构贡献未隔离；不模拟完整 s′、不验证逆执行；归档 provenance 不完整；对照臂是适配；retail 的失败可能是任务形态。
- **`quality: B`**：内部对照和多模型覆盖不错；外部效度、机制隔离、部署观测不足。

## 8. 与仓库判断的关系

- **E-04（已核）**：18 格仅 8 格改善；airline 弱中模型 +0.11–0.18，retail/强模型回退；T1-only ≈ blanket veto。
- **E-13（已核）**：约束收益随基线能力上升而下降；斜率 −0.76/−0.67/−0.31，R² 0.92/0.98/0.65；六点拟合，不是部署阈值。
- **P3（判定是权衡）**：漏检（漏掉不可逆关系 → false approval）与误报（拦合法动作 → false veto）此消彼长。
- **C-03（度量错配）**：用 reward 量护栏会得出「有用/没用」的错结论；目标指标是 prevented harm / false veto。
- **01-L1**：安全是结构问题；但「结构」目前只到「有逆序列」，没到「逆序列可执行」。

## 9. 还没解决 / 下一步

- **T1-only vs full 的配对实验**：同一 baseline、同一轨迹，分开「结构」与「保守拒绝」。
- **False-veto 率**：1,745 条 blocked decisions 能否人工标注「本可合法执行」？
- **复合动作的可逆性**：POLAR 会组合候选逆序列，但不模拟完整 post-action state s′、不验证逆执行；组合可逆性仍是未测。
- **意图/授权层**：可逆性门 + 用户确认 + 策略引擎，谁做最终裁决？
- **动态/不确定性感知门**：强模型上保留结构检查而不回退？
- **本体编写成本**：一个人天/域？工具变更后的维护成本？

## 10. 原文

- arXiv:2610.08082
- PDF：同目录 `2610.08082-polar.pdf`
- 代码/数据：论文未给独立仓库。
