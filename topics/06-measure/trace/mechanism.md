# 过程有效性 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 问题

形式化器的设计初衷是：模型把问题写成程序，求解器负责搜索并给出保证。**判据通常是「程序输出对不对」——但这看不出程序是在搜索，还是在复述。**

SLB：在写程序之前，推理轨迹里已经在赋值、试算、排除变量取值，常常一路算到最终答案；程序只是把答案重述一遍。

## SLB 本体

| 部分 | 节点 | 判据 |
|---|---|---|
| A. Trace | A1 existence | trace 是否 assign/test/rule out 决策变量 |
| | A2 extent | 是否给每个变量赋值（complete/partial） |
| | ratio | SLB 段落占 trace 比例 |
| B. Program | B1 Hardcoded | 打印答案，不计算 |
| | B2 Partly fixed | 计算，但把 trace 决策写进源码 |
| | B3 Steered | 搜索，但 tiebreak/order 被选成返回 trace 答案 |
| | B4 Independent | 在所有约束下搜索；trace 的 SLB 是浪费 |
| C. Output | C1 / C2 | 输出是否匹配 reasoning answer / reasoning answer 是否正确 |

**只有 B4 真正把搜索交给 solver；B1–B3 都能通过输出评估。**

## 两种伤害

1. **成本随实例增长。** 约束满足是 NP 完全的；在 token 里求解，token 随实例规模增长（Meeting Planning 3,873→10,971 tokens；ZebraLogic 532→4,148）。
2. **保证失效。** solver 本该提供模型推理所缺的保证；若程序只复述轨迹答案，这层保证不存在。163/1,791 程序继承 reasoning answer；reasoning 错时 hardcoded 0/19 正确，independent 32% 正确。

## 数字

- **85%** traces 含 SLB；71% 占 ≥10% token；47% ≥1,000 token；**24%** 推理 token 是 SLB。
- **77–89%** 程序仍独立重算；**88%** 独立程序输出恰好等于 reasoning answer。
- **SLB 与准确率无关联**：ratio +0.1 → +0.007 [−0.011,+0.022]；+1,000 tokens → +0.005 [−0.002,+0.013]。
- **形式语言影响最大**：Python 比 Z3/PDDL 多 0.03–0.20 ratio；FL 解释 0.123 方差，数据集 0.057，模型 0.008。
- **Cautionary prompts**：ratio −0.053/−0.058（≈1/4），准确率不变；但会把 hardcode 推成更隐蔽的 partly fixed/steered。
- **Placeholders**：SLB token **−97%**（2,820→78），ratio 0.25→0.005，traces 94%→15%，准确率 **+2.6 [−0.5,+5.9]**（不降）。
- **Batching**：SLB token −62%，但 reasoning −61%，ratio 几乎不变；准确率 **−5.9**。

## 为什么输出评估看不见

只看程序输出对不对，结构上无法区分 B1/B4。这不是「测不准」，是「测不到」。任何只看最终产物的判据，都会放过冗余与错误继承；要看见它们，判据必须能读中间（轨迹、程序、检索路径）。

## 失效模式

- **Hardcode 被输出正确掩盖。**
- **Partly fixed/steered 更隐蔽**；cautionary prompt 可能把它们推得更深。
- **Batching 砍 reasoning 总量**，SLB 比例不变但准确率下降。
- **闭源模型无完整 trace**，无法测。
- **Placeholders 不适用于值与结构不可分的任务。**

## 与本体 / 回路的关系

本体/形式化在 formalizer 里是 **目标语言 + 约束**；约束强度中（能限制程序结构，不能保证 solver 真搜索）。被违反时通常没有信号，除非读 trace。

## 关联

- [SLB digest](../../../src/papers/2611.02395-solver-like-behavior/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
- [metrics](../metrics/README.md)
