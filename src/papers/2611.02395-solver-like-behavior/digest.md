---
status: draft
updated: 2026-11-07
quality: A
based_on: card.md
claims: [E-07, E-09]
---

# Solver-Like Behavior · 消化

> 事实、数字、页码回 [card.md](./card.md)。这里只写**我们怎么用**、值不值得、哪里会坏。

## 工程思路

**如果你用「LLM 写程序 + solver 搜索」，按这个顺序防 SLB：**

1. **先看 trace，不只看输出。** 程序跑对不代表它在搜索；B1–B3 都能通过输出评估。用 A/B/C 本体标注 trace。
2. **量 solver-like ratio。** SLB 段落占 trace 的比例；85% 轨迹有，24% token 是 SLB。
3. **看程序是否继承。** B1 hardcoded / B2 partly fixed / B3 steered / B4 independent；只有 B4 才真正把搜索交给 solver。
4. **优先用 placeholders，不要靠 prompt 警告。** 把问题的值藏到运行时 `VALUES`；模型只写结构。SLB −97%，准确率不降。
5. **Cautionary prompts 只能当辅助。** 只减约 1/4，而且可能把 hardcode 变成更隐蔽的 partly fixed/steered。
6. **不要 batching 求省 token。** SLB 比例几乎不变，reasoning 总量和准确率一起掉（−5.9 点）。
7. **评估 formalizer 要报 trace 指标。** 只看 program accuracy 会把「复述」当「搜索」；应报 SLB 比例、继承率、C1/C2。
8. **注意 FL 的选择。** Python 比 Z3/PDDL 更容易诱使模型自己写搜索；能交给声明式 solver 就交。
9. **闭源模型拿不到完整 trace 时，明确标「无法测 SLB」**，不要用输出准确率假装它没有。

## 实用意义

它解决的操作问题：

- **「程序跑对了，但不知道是 solver 算的还是模型抄的。」** → trace-level 评估 + B 分类。
- **「agent 写 PDDL/Z3，token 账单却很高。」** → SLB 可能占了 24%；placeholders 可砍 97%。
- **「想让模型别在推理里算，prompt 警告没用。」** → 让它看不到值；结构/值分离。
- **「换 Python 后模型表现更差。」** → Python 把搜索交给模型；用声明式 FL 或 placeholders。
- **「输出评估通过了，但错误被继承。」** → hardcoded/partly fixed 会继承 trace 错误；C2 检查 reasoning answer。
- **「formalizer 的保证到底是什么？」** → 只有 B4 才保留 solver 保证；B1–B3 只是看起来可验证。

**何时用**：LLM-as-formalizer；solver-backed agent；需要审计「程序怎么来的」；有完整 trace。

**何时别用**：闭源模型无完整 trace；任务不能把值与结构分离；需要单次低延迟；不关心求解保证。

## 质量评估

- **证据类型**：实证·基准（`已核`，一手正文；2,000 generations）。
- **样本与对照**：3 模型 × 4 数据集 × 2 FL；baseline + 3 干预；LLM judge 与人类标签 90–98%；H1–H4。
- **优点**：现象新且重要；本体清晰；多模型/多数据集/双 FL；干预有强结果（placeholders）；诚实写局限。
- **主要威胁**：闭源模型未测；单次生成；judge 参考样本小；H4 受 prompt 混淆；placeholders 只测两数据集；任务类型有限。
- **`quality: A` 理由**：多模型、多数据集、双 FL、干预、judge 校验；现象与评估含义都强。外部效度受任务/模型限制。

## 洞察

1. **「程序跑对」不等于「程序在搜索」。** 85% trace 有 SLB，24% token 是 SLB；输出评估区分不出 B1/B4。`已核`
2. **SLB 大多是浪费，不是帮助。** 77–89% 的程序仍独立重算；SLB 与准确率无关联（+0.007/0.1 ratio）。`已核`
3. **少数继承会继承错误。** 163/1,791 程序继承 reasoning answer；reasoning answer 错时，hardcoded 0/19 正确，independent 32% 正确。**输出评估全过。** `已核`
4. **形式语言是最强解释变量。** Python 比 Z3/PDDL 多 0.03–0.20 SLB ratio；FL 解释 0.123 方差，数据集 0.057，模型 0.008。**让 solver 真搜，模型就不自己搜。** `已核`
5. **Placeholders 是最有效的工程修复。** SLB token −97%，准确率 +2.6（不降）；比 cautionary prompt（−25%）强一个数量级。`已核`
6. **Cautionary prompts 会把行为推得更隐蔽。** GPT-OSS hardcoded 40→0/1，但 partly fixed 11→15/7；**警告不是约束**。`已核`
7. **Batching 省 token 但伤准确率。** SLB 比例几乎不变，reasoning 总量 −61%，准确率 −5.9。`已核`
8. **评估 formalizer 必须看「怎么到达程序」。** 这是本文对 06 派最直接的贡献：输出尺子不够，需要 trace 尺子。`已核`

## 成本与使能条件

| 成本 | 一次性 / 每次 | 说明 |
|---|---|---|
| 完整 trace | 每次 | 闭源 API 常只给摘要；无法测 SLB |
| Judge 标注 | 每批 | LLM judge + 人类校验；2,000 条 |
| Placeholders | 集成一次性 | 值/结构分离；运行时注入 VALUES |
| Cautionary prompt | 每次 | 便宜但效果弱 |
| Batching | 每次 | 省 token 但伤准确率 |
| 评估 | 每 benchmark | A/B/C 本体 + C1/C2 |

**使能条件**：能拿到完整 trace；任务的值与结构可分离；有 solver/validator；能接受 placeholders 的运行时注入。

**2022 年做会卡在哪**：reasoning model 的长 trace 还不普遍；formalizer 范式不成熟；没有这套 SLB 本体。

**反向条件**：闭源无 trace；值与结构不可分；任务需要模型自己设计搜索（如 Python）；单次低延迟。

## 与现有判断的关系

| 关联 | 关系 |
|---|---|
| **E-07** | **一手依据**：formalizer 的 trace 会替 solver 做搜索；成本随实例增长；形式化保证失效。 |
| **E-09** | **从推测升已核**：85% traces、24% token、9% inherit、placeholders −97%；这些数字已在正文确认。 |
| **P2** | 强支撑：同一模型，换 FL/占位符/评估，行为不同。 |
| **C-03** | 又一例：只用 program accuracy 会漏掉 SLB；需要 trace 指标。 |
| [trace](../../../topics/06-measure/trace/README.md) | 核心文献；机制细节回 card。 |
| [02 判定](../../../topics/02-judgment/README.md) | 「程序跑对」是输出判定；SLB 说明输出判定不够。 |

## 不可迁移

- 3 个 reasoning model、4 个 CSP 数据集、2 种 FL；其他任务/语言未测。
- DeepSeek 只跑一种 FL；H4 主要靠 Qwen/GPT-OSS。
- 单次生成；不含采样方差。
- 闭源模型无完整 trace；不能外推。
- Placeholders 只测 Calendar/Meeting；值与结构不可分的任务不适用。

## 开放问题

- 闭源模型（Claude/GPT-5/Gemini）的 SLB 有多普遍？没有 trace 怎么测？
- 定理证明/优化任务是否同样普遍？
- Placeholders 能否推广到不能分离值与结构的任务（如交互式规划）？
- Batching 的准确率损失能否通过批内隔离/独立上下文避免？
- 能否训练模型「不 SLB」而不只是外部约束？
- SLB 与 reward hacking 的关系：hardcode 是极端形式，steered 更隐蔽。
