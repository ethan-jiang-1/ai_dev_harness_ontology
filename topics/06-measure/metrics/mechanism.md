# 度量错配 · 机制

> 只写「它怎么错、怎么选」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 问题

文献里「本体有用」与「本体无用」两类证据长期并存。多数不是相反结论，而是用了不同的尺子去量不同的机制。

## 四种量错

| 机制 | 常用尺子 | 为什么错 | 更好的尺子 |
|---|---|---|---|
| 闸门/授权（01） | 任务奖励、准确率 | 被拦住的伤害不体现在奖励；护栏还会误剪合法动作 | 不可逆错误拦截率、误剪率、审批量 |
| 判定器（02） | 判定准确率 | 掩盖漏检与误报的非对称代价 | 漏检/误报曲线 + 「被误标后修坏」计数 |
| 知识供给（03） | 基准准确率 | 基准看不见治理、集成、上手 | 部署指标 + token/轮次/时延 |
| agent 配置（06） | 单次 run 的 score | 54% 方差是 run-to-run 噪声；轴交互 | 重复采样 + completion + cost + calibration + variance |

## 四个案例

1. **POLAR**：reward 衡量护栏，18 组仅 8 组改善，看着像失败；但 reward 不是防止伤害的度量。**护栏的目标是「不发生」，reward 只能度量「发生了且做对了」。**
2. **Ontology Catch**：curated checker catch 18.9%、FA 16.8%、precision 57.1%；只看 accuracy 会把「多抓错、多杀对」混在一起。
3. **SLB**：程序跑对不代表在搜索；85% 轨迹有 SLB、24% token 是 SLB，输出评估区分不出 hardcoded 与 independent。
4. **Agents are Systems**：54% 方差来自重复同一配置；单次跑分不可靠；Information > 模型/预算；验证靠工具不靠 prompt。

## 方法要求

1. **先声明机制的失效形态，再选指标。** 是「做错」还是「没做」？是「慢」还是「不准」？是「内部没有」还是「输出对了」？
2. **主指标 + 过程指标并报。** 只看一个数，任何机制都能被证成无用。
3. **报告非对称代价。** 漏检与误报不能合并成一个「准确率」；审批量与 false-veto 单独报。
4. **重复采样 + 方差。** 至少 5 runs/config；报 CI、completion、cost、calibration。
5. **能读中间。** formalizer 看 trace；agent 看轨迹；checker 看 catch/FA；记忆看 retrieval completeness 与 conditional accuracy。
6. **按配置轴做敏感性分析。** 至少变信息、预算、模型；看交互。

## 失效模式

- **平均掩盖两端。** CAI 的 −38% 是 −91% 与 +1.9% 的混合。
- **准确率掩盖非对称代价。** checker 的 FA 会让 agent 修坏正确答案。
- **最终产物掩盖过程。** B1–B4 都能通过输出评估。
- **单次跑分掩盖方差。** 54% 是噪声。
- **配置轴不独立。** 预算只在信息/模型足够时有用；一次只动一个会误判。

## 与本体 / 回路的关系

度量本身不在回路里；它决定回路的哪一段被看见。指标选错，机制会被证成无用或有用，而实际相反。

## 关联

- [findings](./findings.md) · [frontier](./frontier.md)
- [trace](../trace/README.md) · [mechanism](../mechanism/README.md) · [failure-attribution](../failure-attribution/README.md)
- [EXP-003](../../../experiments/README.md)
