---
status: draft
updated: 2026-11-07
rq: [RQ4]
evidence: [E-07, E-09]
---

# 尺子三：过程是不是真的有效

## 问题

形式化器的设计初衷是：模型负责把问题写成程序，求解器负责搜索并给出保证。**判据通常是「程序输出对不对」——但这看不出程序是在搜索，还是在复述。**

SLB 研究揭示第二种情况很普遍：在写程序之前，推理轨迹里已经在赋值、试算、排除变量取值，常常一路算到最终答案；程序只是把答案重述一遍。

## 一个本体（Fig. 2）

| 部分 | 节点 | 判据 |
|---|---|---|
| A. Trace | A1 existence | trace 是否 assign/test/rule out 决策变量 |
| | A2 extent | 是否给每个变量赋值（complete/partial） |
| | solver-like ratio | SLB 段落占 trace 比例 |
| B. Program | B1 Hardcoded | 打印答案，不计算 |
| | B2 Partly fixed | 计算，但把 trace 决策写进源码 |
| | B3 Steered | 搜索，但 tiebreak/order 被选成返回 trace 答案 |
| | B4 Independent | 在所有约束下搜索；trace 的 SLB 是浪费 |
| C. Output | C1 / C2 | 输出是否匹配 reasoning answer / reasoning answer 是否正确 |

**关键**：只有 B4 真正把搜索交给 solver；B1–B3 都能通过输出评估。

## 两种伤害

1. **成本随实例增长。** 约束满足是 NP 完全的；在 token 里求解，token 消耗随实例规模增长（Meeting Planning 上 3,873→10,971 tokens，ZebraLogic 532→4,148）。
2. **保证失效。** 求解器本该提供模型推理所缺的保证；若程序只复述轨迹答案，这层保证就不存在了。**163/1,791 程序继承 reasoning answer；reasoning answer 错时，hardcoded 0/19 正确，independent 32% 正确。**

## 数字（一手正文，`已核`）

- **85%** traces 含 SLB；71% 占 ≥10% token；47% ≥1,000 token；**24%** 推理 token 是 SLB。
- **77–89%** 的程序仍独立重算；**88%** 的独立程序输出恰好等于 reasoning answer。
- **SLB 与准确率无关联**：ratio +0.1 → +0.007 [−0.011,+0.022]；+1,000 tokens → +0.005 [−0.002,+0.013]。
- **形式语言影响最大**：Python 比 Z3/PDDL 多 0.03–0.20 ratio；FL 解释 0.123 方差，数据集 0.057，模型 0.008。
- **Cautionary prompts**：ratio −0.053/−0.058（≈1/4），准确率不变；但会把 hardcode 推成更隐蔽的 partly fixed/steered。
- **Placeholders**：SLB token **−97%**（2,820→78），ratio 0.25→0.005，traces 94%→15%，准确率 **+2.6 [−0.5,+5.9]**（不降）。
- **Batching**：SLB token −62%，但 reasoning −61%，ratio 几乎不变；准确率 **−5.9**。

## 尺子的问题在哪

只看输出正确与否的判据，**结构上无法区分** B1/B4。这就是「尺子选错」的典型：不是测不准，是测不到。

本仓库的推论：**任何只看最终产物的判据，都会放过冗余与错误继承。** 要看见它们，判据必须能读中间（轨迹、程序、检索路径）。

## 工程含义

- **优先 placeholders，不要靠警告。** 把值藏到运行时，模型只能写结构；这是最强、最便宜的修复。
- **Cautionary prompt 只能辅助。** 它减少显式 hardcode，但可能把行为推到 partly fixed/steered。
- **不要 batching 求省 token。** 它砍 reasoning 总量，也砍准确率。
- **能交给声明式 solver 就交。** Python 把搜索留给模型，SLB 更多。
- **评估 formalizer 要报 trace 指标**：SLB ratio、继承率、C1/C2；只报 program accuracy 不够。

## 与其它派的关系

- 为 [02 判定](../../02-judgment/README.md) 提供设计约束：判定器要能接受轨迹作为输入，而不只是最终输出。
- 为 [04 状态](../../04-state/README.md) 的「错误继承」提供机制解释：一旦上游答案被当作既定事实，下游程序会把它一起继承。
- 为 [05 生产](../../05-produce/README.md) 提供一条设计规则：结构与值分离，别让模型看见具体数值。

## 开放问题

- 闭源模型无完整 trace，怎么测 SLB？
- 定理证明/优化任务是否同样普遍？
- Placeholders 能否推广到值与结构不可分的任务？
- Batching 的准确率损失能否通过批内隔离避免？
- 能否训练模型「不 SLB」而不只是外部约束？
