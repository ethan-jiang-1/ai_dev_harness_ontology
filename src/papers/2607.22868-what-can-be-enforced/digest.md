---
status: draft
updated: 2026-11-09
quality: B
based_on: card.md
claims: []
---

# What Can Be Enforced?：guardrail 的 false-block/miss 是一个前沿

> 这篇消化不假设你读过原文。先讲清三个边界（表达力 / 统计 / 可判定），再看 AgentDojo 的 23 个 judge、block-all 与表示攻击，最后说它对「本体闸」的 false-veto 意味着什么。

## 0. 三句话

1. **它问什么**：动作前的 guardrail 到底能保证什么？取决于策略状态是否可表示、judge 能观察到什么、阻断是否改变未来行为。
2. **它怎么做**：把问题拆成 T1 表达力、T2 统计/安全、T3 可判定性；T2 用 Neyman–Pearson 给 false-block/miss 前沿，用 conformal 给有限样本证书；再用 AgentDojo、有限受控模型、表示攻击、闭环 rerun 做诊断。
3. **它发现什么**：在固定一步 law 下，false-block 的下界是 `roc_I(β)`；低 miss 的 conformal 证书可能只能靠 **block-all**；一旦阻断改变未来 proposal，静态分数/ungated 轨迹不必识别闭环前沿。

## 1. 它解决什么问题

Tool-using agent 的动作前 gate 常被当成「加一个分类器」：给它一个 allow/block 判断，报一个准确率/拦截率。但 gate 的保证不是单一数字：

- **策略状态**：计数器、撤销、cap 等状态，gate 能不能表示？
- **judge**：语义谓词（如「含 PII」）只能由 fallible judge 判断；它的 ROC 是什么？
- **反馈**：阻断会改变 agent 后续 proposal；静态评测还能不能代表部署？

论文把这三件事分开，并给出各自的边界；核心立场是：**不要把「拦截率」当保证，也不要把静态 ROC 当闭环前沿。**

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **gate** | 动作前 allow/block 的确定性/随机化规则。 |
| **register automaton** | 带有限寄存器（计数器等）的自动机；T1 用它刻画可执行的策略类。 |
| **T1 表达力边界** | 相对固定 oracle 谓词，确定性 gate 能执行的非空安全策略类。 |
| **T2 统计/安全边界** | fallible judge 下 false-block/miss 的极限；NP 前沿 + conformal 证书。 |
| **T3 可判定性边界** | 给定策略规范，判断「它是否会触发」是否可判定。 |
| **false-block** | 合规动作被 block 的概率。 |
| **miss** | 违规动作被 allow 的概率。 |
| **ROC / roc_I(β)** | 在信息 I 下，给定 miss 上限 β 的最小 false-block。 |
| **conformal certificate** | 有限样本、分布自由的边际风险证书；可能是 vacuous。 |
| **block-all** | 全拦；零 miss，但零可用性。 |
| **closed-loop frontier** | 阻断改变未来 proposal 后的前沿；需要受控模型/occupancy program。 |
| **representation attack** | 改 judge 可见的表示（不改变真实语义）来绕过 gate。 |

## 3. 它怎么做

### 3.1 T1：表达力

- 相对固定 oracle 谓词，确定性 gate 执行的正是**非空 register-representable safety policies**；严格弱于 edit automata。
- 策略 nontriviality：两个可减计数器下不可判定；在 separable monotone fragment（覆盖 cap/revocation）下是 PSPACE。
- 含义：不是所有「安全策略」都能被一个有限状态 gate 执行；counter/revocation 类状态要单独设计。

### 3.2 T2：统计与安全

- 固定一步决策、固定外生 law：Neyman–Pearson 给出 exact frontier `B*_I(β)=roc_I(β)`；任何使用同一信息 I 的规则/集成/wrapper 都不能低于它。
- 信息 refinement（Blackwell）：I' 更细时 `roc_I'(β) ≤ roc_I(β)`；但条件依赖本身不够，必须扩大可达 error region。
- Conformal：label-conditional exchangeability 给有限样本边际证书；**可能是 vacuous 的 block-all**。证书证明风险，不证明接近 population frontier。
- 闭环：阻断改变未来 proposal 后，静态分数与 ungated 轨迹不必识别 closed-loop frontier；需要有限受控模型 + occupancy program。
- 表示攻击：对 judge 可见表示的 bounded attack 会加 robustness margin；benign calibration 不自动迁移。

### 3.3 T3：可判定性

- 即使策略是 register-representable，判断「它是否非平凡/会触发」也可能不可判定；这决定了静态分析能做什么、不能做什么。

### 3.4 实验

- **AgentDojo**：132 条（97 user-task + 35 injection-goal），23 个 open/closed/dedicated guard judges 打同一批。
- **有限受控两步 retry 模型**：exact occupancy polytope。
- **表示攻击**：一个预声明的 16-token 表示重写；11 个 fully cached judges。
- **闭环 rerun**：paired end-to-end。

## 4. 结果：数字与条件

### 4.1 校准可能是 vacuous

- **δ=.05 时，每个 judge 的 split threshold 都是 block-all。** 也就是说，要在 5% miss 下给证书，校准可能只能全拦。
- Gemma-2-9B：
  - δ=.10 → miss **.010**（同时上界 .021），false block **.780**（同时 95% 区间 **[.660,.901]**）。
  - δ=.20 → miss .138，但上界 .264，**未被这个诊断认证**。
- 含义：低 observed miss 不等于被认证；证书可能是 vacuous；「零 miss」可能只是 block-all。

> 出处：§7 / Figure 1。

### 4.2 闭环与策略类

- 有限两步 retry 模型：
  - perfect recall cost **.551**；
  - current-score/time policies **.863**；
  - stationary thresholds **1.137**。
- 这是 analytic model check，不是 AgentDojo 的未知 kernel；它说明策略类差距是真实的，不是估计噪声。
- paired closed-loop rerun：两个 gate 都制造了一些 attack，直接展示 decision-dependent transitions。

> 出处：§7 / Appendix B.2。

### 4.3 表示攻击

- 一个预声明的 16-token 表示重写，在 fixed θ=.5、35 个 violation 上测。
- simultaneous inference 在 **8/11** fully cached judges 上检测到 miss 增加；第 9 个点估计为正。
- 含义：benign calibration 不自动迁移；需要 margin-aware calibration，且 margin 必须低于 miss 预算。

> 出处：§5 / §7。

## 5. 这些数字不能说明什么

1. **不是本体评测。** 没有 ontology；gate 是通用 guardrail，不是 SHACL/OWL 判据。
2. **不是部署。** AgentDojo 是 prompt-injection 安全评测；不是工具授权/commit gate；没有真实客户流量。
3. **不是「低 miss 就等于安全」。** Block-all 是 vacuous certificate；false block .78 的 operating point 不可用。
4. **不是「静态 ROC 足够」。** 闭环反馈会改变前沿；静态分数/ungated 轨迹不必识别。
5. **不是 universal semantic soundness。** 表示攻击的 margin 是分布性的；不是所有语义错误都能被证书覆盖。
6. **不是「校准一定有用」。** Naive calibration 不是安全边界；margin-aware calibration 只在 verified uniform margin 低于 miss 预算时救得回来。
7. **不是「所有策略都可执行」。** T1 有表达力边界；counter/revocation 类要单独设计。

## 6. 工程上怎么用

### 6.1 对本体的 gate

- 如果本体 gate 是**确定性谓词**（SHACL/OWL 查询），它落在 T1：先问「策略状态是否 register-representable」；caps/revocation/计数类状态不能假装有。
- 如果本体 gate 依赖**fallible judge**（LLM/语义匹配），它落在 T2：不要只报一个 accuracy；报 **miss–false-block 前沿**，并给 miss 预算。
- 如果 block 会改变 agent 后续行为（重试、改写、绕过），它落在闭环：静态评测不够；需要 paired rerun/受控模型。
- **不要用 block-all 换零 miss**：那是 vacuous certificate，不是安全。

### 6.2 对 E5 的验收线

- 不要写「false-veto ≤5%」当单点；写「在给定 miss 预算下，报 false-block 前沿/若干 operating points」。
- 低 miss 的证书可能只能 block-all；要同时报可用性（lawful completion/retention）。
- POLAR 的 36.6% retention 不是 false-veto；没有授权标签就算不出来。
- 2610.16838 提供「同操作/不同权限」的请求级评测；2607.22868 提供「miss–false-block 前沿/校准」的理论；两者合起来，才是 E5 的完整评测设计。

### 6.3 对 E8 的启示

- commit gate 也是 gate：T1 的表达力边界（策略状态）、T2 的 fallibility（证据/judge）、闭环（defer 后重入）都适用。
- 「全 defer」是 block-all 的授权版本：零错误落盘，但零可用性；不是授权正确。

## 7. 质量与边界

- **证据类型**：理论 + 诊断实验（一手正文）。
- **强项**：三个边界清楚；NP 前沿/conformal/闭环各有形式化；AgentDojo 23 judges 的诊断；有限模型 exact enumeration；表示攻击。
- **主要威胁**：AgentDojo 是 prompt-injection，不是授权；23 judges 是静态诊断，不是部署；conformal 是 marginal/label-conditional；block-all 使证书 vacuous；代码未跑；没有本体。
- **`quality: B`**：理论强、诊断有限；外部效度（agent 授权、本体、部署）不足。

## 8. 与仓库判断的关系

- **E-04（动作闸）**：这篇不测本体闸，但把 false-veto 从「未测」推进到「可校准的前沿」；POLAR 的 blocked log 仍无标签，E5 的 false-veto 仍 `unknown`。
- **E-13（能力梯度）**：不直接相关；但「强模型回退」可以用闭环前沿解释（block 改变后续 proposal），不是单纯能力曲线。
- **E-20（执行 ≠ 授权）**：同向：gate 的「拒绝」不等于正确授权；block-all 是 vacuous certificate。
- **C-03（度量错配）**：只看 accuracy/拦截率会漏掉 false-block/miss 前沿；要同时报 miss、false-block、可用性。
- **checker/F7（三态）**：unavailable/undetermined 必须单列；block-all 也是一种「全 unavailable」的极端。
- **不新增 E/L**：这是 harness/理论证据，不是本体执行证据；留作 E5 的边界与 E8 的设计参考。

## 9. 还没解决 / 下一步

- 把 T2 的 miss–false-block 前沿搬到本体 checker：同一本体、合法/非法实例成对，测 false-block。
- 在 POLAR 的 blocked log 上标授权标签，给一个真实的 false-block 点。
- 闭环：本体 gate 的 block 是否改变 agent 后续 proposal？需要 paired rerun。
- 表示攻击：本体 gate 的输入表示（IRI/标签/证据）被改写时，会不会绕过？
- 与 2610.16838 的组合：同操作/不同权限 + miss 预算 + 请求级配对。

## 10. 原文

- arXiv:2607.22868
- PDF：同目录 `2607.22868-what-can-be-enforced.pdf`
- 代码/缓存分数：`https://github.com/shawnray-research/certified-agent-guardrails`（未跑）。
