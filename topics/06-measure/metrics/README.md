---
status: draft
updated: 2026-11-08
rq: [RQ4]
evidence: [C-03]
---

# 用错了尺子：按机制分派指标

> 文献里「本体有用」与「本体无用」长期并存；多数不是相反结论，而是**用不同的尺子量不同的机制**。这里问「什么机制该用什么指标」。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 4 条（[findings](./findings.md)） |
| 未发现 / 开放 | 4 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 指标选择/度量错配；不含具体 trace/mechanism 分析（见同派子页） |

## 当前判断

- **度量错配会让结论反向，不只是失真。** POLAR 用 reward 量护栏：18 组仅 8 组改善；但 reward 不是防伤害度量。`已核`
- **非对称代价必须分开报。** checker 的 catch 18.9% / FA 16.8% / precision 57.1%；只报 accuracy 会把「多抓错、多杀对」混在一起。`已核`
- **输出正确会掩盖过程无效。** SLB：85% 轨迹、24% token，输出评估区分不出 hardcoded 与 independent。`已核`
- **单次 score 不可靠。** Agents are Systems：54% 方差来自重复同一配置；必须重复采样 + 报 completion/cost/calibration。`已核`

## 文件地图

| 想知道 | 去 |
|---|---|
| 四种量错/方法要求 | [mechanism](./mechanism.md) |
| 四条判断的证据/数字 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 相关子页 | [trace](../trace/README.md) · [mechanism](../mechanism/README.md) · [failure-attribution](../failure-attribution/README.md) |

## 边界

- **不是「换一个指标就好」。** 要先声明机制的失效形态；指标跟着失效形态走。
- **不是「所有机制都要过程指标」。** 有些机制（动作闸门）的终点是不可逆错误，不是过程。
- **没有统一评分卡。** 目前只有按机制分派的雏形，未做成实验。

## 关联

- 派：[06 测量](../README.md) · 冲突：[C-03](../../conclusions.md)
- 实验：[EXP-003](../../../experiments/README.md)
- 成本：[feasibility](../feasibility/README.md)
