# 过程有效性 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `trace/Fx`。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | SLB 普遍：85% 轨迹、24% token | 已核 |
| F2 | 输出评估结构上看不见 B1–B3 | 已核 |
| F3 | SLB 与准确率无关联 | 已核 |
| F4 | Placeholders 是最强修复；cautionary 弱、batching 伤 | 已核 |
| F5 | 形式语言解释力最大 | 已核 |

## F1 · 普遍性

- **数字**：85% traces；24% reasoning token；77% 轨迹的 SLB 段落单独给出完整答案。
- **条件**：3 reasoning models、4 CSP、2 FL、2,000 generations。
- **来源**：§5-H1, p.5；Fig. 2。

## F2 · 输出看不见

- **判断**：B1–B4 都能通过 program accuracy；163/1,791 继承；reasoning 错时 hardcoded 0/19 正确，independent 32%。
- **含义**：只看最终产物会放过冗余与错误继承。
- **来源**：§5-H2, p.5。

## F3 · 与准确率无关

- **数字**：ratio +0.1 → +0.007 [−0.011,+0.022]；+1,000 tokens → +0.005 [−0.002,+0.013]。
- **含义**：SLB 不是「多想就更好」；它是浪费/保证失效。
- **来源**：§5-H3, p.6。

## F4 · 修复排序

- **Placeholders**：SLB token −97%，准确率 +2.6 [−0.5,+5.9]。
- **Cautionary**：ratio −0.053/−0.058，准确率不变；可能推成更隐蔽的 B2/B3。
- **Batching**：token −62%，accuracy −5.9。
- **来源**：§6, p.7–8；Fig. 6。

## F5 · 形式语言

- **数字**：Python 比 Z3/PDDL 多 0.03–0.20 ratio；FL 解释 0.123 > 数据集 0.057 > 模型 0.008。
- **含义**：能交给声明式 solver 就交；Python 把搜索留给模型。
- **边界**：PDDL 臂有 prompt 混淆。
- **来源**：§5-H4, p.7。
