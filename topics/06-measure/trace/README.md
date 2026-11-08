---
status: draft
updated: 2026-11-08
rq: [RQ4]
evidence: [E-07, E-09]
---

# 过程是不是真的有效：solver-like behavior

> 形式化器的设计初衷是「模型写程序、solver 搜索」；但输出正确看不出程序是在搜索，还是在复述轨迹里已经算好的答案。这里问「怎么读中间、怎么修」。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 8 条（[findings](./findings.md)） |
| 未发现 / 开放 | 5 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | formalizer 的 trace/program 过程；不含输出后的语义判定（[checker](../../02-judgment/checker/README.md)） |

## 当前判断

- **SLB 很普遍。** 85% 轨迹有 SLB、24% 推理 token 是 SLB；77% 轨迹的 SLB 段落单独就给出完整答案。`已核`
- **输出评估结构上看不见。** B1–B4 都可能通过 program accuracy；163/1,791 程序继承轨迹答案，reasoning 错时 hardcoded 0/19 正确。`已核`
- **SLB 与准确率无关联。** ratio +0.1 → +0.007 [−0.011,+0.022]；不是「多想就更好」。`已核`
- **Placeholders 是最强修复。** SLB token −97%，准确率 +2.6（digest 记「不降」，未给区间）；cautionary prompt 只减 1/4，batching 伤准确率。`已核`
- **形式语言影响最大。** Python 比 Z3/PDDL 多 0.03–0.20 ratio；FL 解释 0.123 方差 > 数据集 0.057 > 模型 0.008。`已核`（PDDL 臂有 prompt 混淆，幅度 `存疑`）
- **先判适用，再谈收益。** 闭源无完整 trace → 只 audit-only；值与结构不可分、要求单次低延迟、不需要 solver 保证 → 别用 placeholders/审计。buy 臂：无完整 trace 的闭源 API 直接出局，不进短名单；能供 trace 的工具按 seat/trace + 集成人周算 NPV。`已核`（适用边界，digest §6.3）/ `推测`（采购）

## 文件地图

| 想知道 | 去 |
|---|---|
| SLB 本体/两种伤害/数字/修复 | [mechanism](./mechanism.md) |
| 八条判断的证据/边界 | [findings](./findings.md) |
| 采购、适用边界与 stop | [mechanism](./mechanism.md) 的「实施与客户价值」「stop condition」· [findings](./findings.md) F6–F8 |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始论文 | [SLB digest](../../../src/papers/2611.02395-solver-like-behavior/digest.md) |

## 边界

- **不是所有模型。** 3 个 reasoning model；闭源 API 无完整 trace。
- **不是所有任务。** 4 个 CSP、2 种 FL；定理证明/优化未测。
- **不是「SLB 一定有害」。** 它与准确率无关联；要害是 solver 保证失效。token 成本随实例上升只在 Meeting Planning/ZebraLogic 两个数据集成立，Calendar/BlocksWorld 不增长（`已核` 数字 / `存疑` 普遍规律）。
- **单次生成。** 所有数字是单次生成，不含采样方差；A1 只查段落，不查整条 trace。`已核`（digest §5 限制 3/5）
- **H4 有 prompt 混淆。** PDDL 臂另给参考 problem file，语言差异不纯。`已核`（digest §5 限制 4）
- **Placeholders 只测两数据集/两模型。**

## 关联

- 派：[06 测量](../README.md) · 结论：[E-07 / E-09](../../conclusions.md)
- 相邻：[metrics](../metrics/README.md) · [failure-attribution](../failure-attribution/README.md)
- 生产：[05 generation](../../05-produce/generation/README.md)
