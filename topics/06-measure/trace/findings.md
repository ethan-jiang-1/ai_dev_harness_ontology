# 过程有效性 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `trace/Fx`。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | SLB 普遍：85% 轨迹、24% token | 已核 |
| F2 | 输出评估结构上看不见 B1–B4 | 已核 |
| F3 | SLB 与准确率无关联 | 已核 |
| F4 | Placeholders 的 SLB 降幅最大；cautionary 弱、batching 伤；但无数值成本对照 | 已核 |
| F5 | 形式语言解释力最大 | 已核 |
| F6 | Codebook 排除：题面限制不算 SLB | 已核 |
| F7 | 闭源无 trace 是盲区；buy 臂按 seat/trace + 集成人周算 NPV | 已核（盲区）/ 推测（采购规则） |
| F8 | 低延迟/无需 solver 保证/值结构不可分 → 别用 | 已核（出处）/ 推测（归类） |

## F1 · 普遍性

- **数字**：85% traces；24% reasoning token；77% 轨迹的 SLB 段落单独给出完整答案。
- **条件**：3 reasoning models、4 CSP、2 FL、2,000 generations。
- **来源**：§5-H1, p.5；Fig. 2。

## F2 · 输出看不见

- **判断**：B1–B4 都可能通过 program accuracy；163/1,791 继承；reasoning 错时 hardcoded 0/19 正确，independent 32%。
- **含义**：只看最终产物会放过冗余与错误继承。
- **来源**：§5-H2, p.5。

## F3 · 与准确率无关

- **数字**：ratio +0.1 → +0.007 [−0.011,+0.022]；+1,000 tokens → +0.005 [−0.002,+0.013]。
- **含义**：SLB 不是「多想就更好」；它是浪费/保证失效。
- **来源**：§5-H3, p.6。

## F4 · 修复排序（按 SLB 降幅，不是按成本）

- **Placeholders**：SLB token −97%，准确率 +2.6（digest 记「不降」，未给区间）。
- **Cautionary**：ratio −0.053/−0.058，准确率不变；可能推成更隐蔽的 B2/B3。
- **Batching**：SLB token −62%，accuracy −5.9。
- **来源**：§6, p.7–8；Fig. 6。

## F5 · 形式语言

- **数字**：Python 比 Z3/PDDL 多 0.03–0.20 ratio；FL 解释 0.123 > 数据集 0.057 > 模型 0.008。
- **含义**：能交给声明式 solver 就交；Python 把搜索留给模型。
- **边界**：PDDL 臂有 prompt 混淆。
- **来源**：§5-H4, p.7。

## F6 · Codebook 的排除项

- **判据**：只有 trace 必须自己「求解」才算 SLB；从题面直接读出的限制不算。
- **为什么要先写**：不写这条，「读题」与「求解」在标注时不可分；人工标 30 条时按它校准 judge，≥90% 一致后再冻结 codebook。
- **来源**：digest §3.2；`已核`。

## F7 · 采购：buy 臂与闭源出局

- **盲区（`已核`）**：闭源 API 常只回摘要，没有完整 trace 就测不了 SLB；这是结构性盲区，不是采样误差。
- **采购处置（`推测`，digest E4）**：把「返回完整 trace」写成资格项而不是评分项，无完整 trace 的闭源 API 直接出局；能提供 trace 的评测/审计工具按 seat/trace 报价 + 集成人周算 NPV，低于 build 才买，否则只做 audit-only 或自建。
- **来源**：digest §5 限制 1、§6.3、§6.6 E4。

## F8 · 什么时候别用

- **digest 明确列出（`已核`）**：闭源无完整 trace；任务不能把值与结构分离；需要单次低延迟；不关心求解保证。
- **处置（`推测`）**：低延迟与「不需要保证」两类直接不做 trace 审计/placeholders；值与结构不可分 → 换 Z3/PDDL 或只做 validator 审计；闭源 → audit-only。
- **来源**：digest §6.3。
