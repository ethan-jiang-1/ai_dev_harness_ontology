---
status: draft
updated: 2026-11-08
quality: A
based_on: card.md
claims: [E-07, E-09]
---

# Solver-Like Behavior：程序跑对，不代表它在搜索

> 这篇消化不假设你读过论文。先讲清「LLM 写程序 + solver 搜索」是什么，再看模型怎么在推理轨迹里把 solver 的活干完、为什么输出评估看不出来、以及怎么修。

## 0. 三句话

1. **它问什么**：LLM 当 formalizer，把问题写成程序交给 solver；如果模型在写程序之前的推理轨迹里已经把答案算出来了，程序只是复述，solver 的保证还在吗？
2. **它怎么做**：定义一个 SLB 本体（轨迹 / 程序 / 输出），在 3 个 reasoning model、4 个约束满足数据集、2 种形式语言上标注 2,000 条生成；比较 cautionary prompt、batching、placeholders 三种干预。
3. **它发现什么**：85% 轨迹有 SLB、24% 推理 token 是 SLB；77–89% 的程序仍独立重算；9% 继承轨迹答案，并继承错误。**把问题的值藏到运行时占位符后面，SLB 减少 97%，准确率不降。**

## 1. 它解决什么问题

### 1.1 背景

**LLM-as-formalizer** 的分工是：模型负责把自然语言问题翻译成形式程序（Z3/PDDL/Python），求解器负责搜索并给出保证。模型不应该自己求解。

但现在 formalizer 常是 reasoning model，会先写一段很长的推理轨迹，再写程序。评估通常只看程序输出对不对——这看不出：

- 程序是在**搜索**，还是在**复述**轨迹里已经算好的答案？
- 如果轨迹算错了，程序会不会把错误一起继承？

### 1.2 一个具体例子

问题：把 Ann、Bob、Cy 安排在 1–3 号座位；Ann 在 Bob 左边；Cy 不在 1 号。

- 正常 formalizer：写约束，`solve()` 搜索，输出一个满足约束的座位。
- SLB：在推理轨迹里先试「Cy 不能在 1；如果 Ann 在 1，Bob 在 2，Cy 在 3；检查……」一路算到答案，然后写 `print("Ann 1, Bob 2, Cy 3")` 或写一个被答案「引导」的搜索。
- 输出评估：两种都「对」。但后者没有 solver 保证；如果轨迹算错，`print` 就输出错答案。

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **formalizer** | 把自然语言问题翻译成形式程序的 LLM。 |
| **solver** | 真正做搜索的程序（Z3、PDDL planner、Python 约束求解）。 |
| **reasoning trace** | 模型在写程序之前的长推理文本。 |
| **SLB（solver-like behavior）** | 轨迹里赋值、试算、排除变量取值，做了 solver 的活。 |
| **A1 existence** | 轨迹是否出现 SLB。 |
| **A2 extent** | 轨迹是否给每个决策变量赋值（complete/partial）。 |
| **B1 hardcoded** | 程序直接打印答案，不计算。 |
| **B2 partly fixed** | 程序计算，但把轨迹里的一些决策写进源码。 |
| **B3 steered** | 程序搜索，但 tie-break/order 被选成返回轨迹答案。 |
| **B4 independent** | 程序在所有约束下搜索；轨迹的 SLB 是浪费。 |
| **C1 / C2** | 程序输出是否等于 reasoning answer / reasoning answer 是否正确。 |
| **CSP** | 约束满足问题；本文四个数据集。 |

## 3. 它怎么做

### 3.1 数据与模型

- **4 个 CSP 数据集**：Calendar Scheduling、Meeting Planning、ZebraLogic、BlocksWorld；每个 100 个问题。
- **2 种形式语言**：Python（imperative）；Z3 或 PDDL（declarative）。
- **3 个 reasoning model**：DeepSeek-V4-Flash、GPT-OSS-120B、Qwen3.8-27B。
- **2,000 条生成**：Qwen/GPT-OSS 在每个数据集的两种 FL；DeepSeek 一种 FL；每个 100 题。
- 标注：LLM judge（Gemma 4 31B-it），与盲人标签一致率 90–98%。

### 3.2 SLB 本体

| 部分 | 节点 | 判据 |
|---|---|---|
| A. Trace | A1 existence | trace 是否 assign/test/rule out 决策变量 |
| | A2 extent | 是否给每个变量赋值（complete/partial） |
| | ratio | SLB 段落占 trace 比例 |
| B. Program | B1 hardcoded | 打印答案，不计算 |
| | B2 partly fixed | 计算，但把 trace 决策写进源码 |
| | B3 steered | 搜索，但 tiebreak/order 被选成返回 trace 答案 |
| | B4 independent | 在所有约束下搜索 |
| C. Output | C1 match | 输出 == reasoning answer？ |
| | C2 correct | reasoning answer 通过 validator？ |

**只有 trace 必须「求解」才算 SLB**；从题面读出的限制不算。

### 3.3 三种干预

- **Cautionary prompts**：在 prompt 里警告不要 precompute/substitute。
- **Batching**：一个 prompt 放 K 个问题。
- **Placeholders**：把问题里的值替换成 `Person1`/`Day1`/`T1` 等，程序运行时才拿到 `VALUES`；模型只能写结构，不能提前算值。

## 4. 结果：数字与条件

### 4.1 SLB 有多普遍

- **85%** traces 含 SLB（BlocksWorld PDDL 例外 51%）。
- 71% traces 的 SLB 占 ≥10% token；47% ≥1,000 token；**24%** 推理 token 是 SLB。
- 77% traces 的 SLB 段落单独就给出完整答案。
- 例：DeepSeek 平均 6,123/26,572 推理 token 是 SLB；Qwen 3,788/15,310；GPT-OSS 575/1,892。

### 4.2 程序有没有继承

- **77–89%** 的程序仍独立重算（B4）；但独立程序输出恰好等于 reasoning answer 的占 **88%**（1,027/1,174）。
- **163/1,791** 程序继承 reasoning answer：47 hardcoded、88 partly fixed、28 steered。
- reasoning answer 错时：hardcoded **0/19** 正确；partly fixed 1/13；independent **32%** 正确。
- 44/45 可比较的 hardcoded 程序输出 == reasoning answer。

### 4.3 与准确率的关系

- ratio +0.1 → 程序正确率 +0.007 [−0.011,+0.022]；+1,000 SLB token → +0.005 [−0.002,+0.013]。
- **SLB 的量与准确率无关联**；它不是「多想就更好」。

### 4.4 形式语言

- Python 比 Z3/PDDL 的 SLB ratio 多：Calendar +0.06、Meeting +0.20、Zebra +0.03、BlocksWorld +0.16。
- 解释方差：形式语言 0.123 > 数据集 0.057 > 模型 0.008。
- **让 solver 真搜，模型就不自己搜。**

### 4.5 干预

| 干预 | SLB token | ratio | traces | 准确率 |
|---|---|---|---|---|
| Cautionary A/B | −23% / −15% | −0.053/−0.058 | — | 不变 |
| Batching K=5 | −62% | 几乎不变 | — | **−5.9 点** |
| **Placeholders** | **−97%** | 0.25→0.005 | 94%→15% | **+2.6（不降）** |

- Placeholders 让模型看不到值，只能写结构；这是最强、最便宜的修复。
- Cautionary prompt 只减约 1/4，而且会把 hardcode 推成更隐蔽的 partly fixed/steered。

> 出处：§5-H1/H2/H3/H4, p.5–7；Fig. 2（SLB 本体）；Fig. 6（干预）。

## 5. 这些数字不能说明什么

1. **不是所有模型。** 3 个 reasoning model；闭源 API 不返回完整 trace，无法测。
2. **不是所有任务。** 4 个 CSP、2 种 FL；定理证明/优化未测。
3. **单次生成。** 区间不含采样方差。
4. **H4 受 prompt 混淆。** PDDL 臂还给了参考 problem file；语言差异不纯。
5. **judge 参考样本小。** A1 110 段、A2 40 traces、B 60 programs；A1 只检查段落，不检查整条 trace。
6. **B/C 覆盖非随机子集。** 只程序能跑、只 complete reasoning answer。
7. **Placeholders 只测两个数据集/两个模型。** 值与结构不可分的任务不适用。

## 6. 工程上怎么用

### 6.1 复刻顺序

1. **先看 trace，不只看输出。** 程序跑对不代表在搜索；B1–B3 都能通过输出评估。
2. **量 SLB ratio。** SLB 段落占 trace 比例；85% 轨迹有，24% token 是 SLB。
3. **看程序是否继承。** B1 hardcoded / B2 partly fixed / B3 steered / B4 independent；只有 B4 真把搜索交给 solver。
4. **优先 placeholders，不要靠 prompt 警告。** 把值藏到运行时；模型只写结构。
5. **Cautionary prompts 只能当辅助。** 它可能把 hardcode 推成更隐蔽的 partly fixed/steered。
6. **不要 batching 求省 token。** SLB 比例几乎不变，reasoning 总量和准确率一起掉。
7. **评估 formalizer 要报 trace 指标。** SLB 比例、继承率、C1/C2；只报 program accuracy 不够。
8. **能交给声明式 solver 就交。** Python 把搜索留给模型，SLB 更多。

### 6.2 成本与使能

| 成本 | 一次性/每次 | 说明 |
|---|---|---|
| 完整 trace | 每次 | 闭源 API 常只给摘要；无法测 SLB |
| Judge 标注 | 每批 | LLM judge + 人类校验；2,000 条 |
| Placeholders | 集成一次性 | 值/结构分离；运行时注入 VALUES |
| Cautionary prompt | 每次 | 便宜但效果弱 |
| Batching | 每次 | 省 token 但伤准确率 |
| 评估 | 每 benchmark | A/B/C 本体 + C1/C2 |

**使能条件**：能拿到完整 trace；任务的值与结构可分离；有 solver/validator；能接受 placeholders 的运行时注入。

### 6.3 何时用 / 何时别用

**用**：LLM-as-formalizer；solver-backed agent；需要审计「程序怎么来的」；有完整 trace。

**别用**：闭源模型无完整 trace；任务不能把值与结构分离；需要单次低延迟；不关心求解保证。

## 7. 质量与边界

- **证据类型**：实证·基准（2,000 generations）。
- **强项**：现象新且重要；本体清晰；多模型/多数据集/双 FL；干预有强结果（placeholders）；诚实写局限。
- **主要威胁**：闭源模型未测；单次生成；judge 参考样本小；H4 受 prompt 混淆；placeholders 只测两数据集；任务类型有限。
- **`quality: A`**：多模型、多数据集、双 FL、干预、judge 校验；现象与评估含义都强。外部效度受任务/模型限制。

## 8. 与仓库判断的关系

- **E-07（已核）**：formalizer 的 trace 会替 solver 做搜索；成本随实例增长；形式化保证失效。
- **E-09（已核）**：85% traces、24% token、9% inherit；placeholders −97%；cautionary 只减 1/4；batching 准确率 −5.9。
- **P2**：同一模型，换 FL/占位符/评估，行为不同。
- **C-03**：只用 program accuracy 会漏掉 SLB；需要 trace 指标。
- **06 trace**：这是「过程是不是真的有效」的核心一手证据。

## 9. 还没解决 / 下一步

- **闭源模型**：Claude/GPT-5/Gemini 的 SLB 有多普遍？没有 trace 怎么测？
- **定理证明/优化** 是否同样普遍？
- **Placeholders 推广**：不能分离值与结构的任务（交互式规划）怎么办？
- **Batching 损失**：能否通过批内隔离/独立上下文避免？
- **训练模型不 SLB**：不只外部约束，能否内化？
- **SLB 与 reward hacking 的关系**：hardcode 是极端，steered 更隐蔽。

## 10. 原文

- arXiv:2611.02395
- PDF：`src/papers/2611.02395-solver-like-behavior/`
- 代码：https://github.com/rikhil-amonkar/solver-like-behavior-in-llms
