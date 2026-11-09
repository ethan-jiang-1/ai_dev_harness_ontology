---
status: draft
updated: 2026-11-09
rq: [RQ4]
evidence: [C-03]
---

# 用错了尺子：按机制分派指标

> 文献里「本体有用」与「本体无用」长期并存；多数不是相反结论，而是**用不同的尺子量不同的机制**（`推测`；[06-L4](../claims.md) 的解释框架）。这里问「什么机制该用什么指标」。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 4 条（[findings](./findings.md)） |
| 未发现 / 开放 | 4 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 指标选择/度量错配；不含具体 trace/mechanism 分析（见同派子页） |

## 当前判断

- **度量错配可能让结论反向，不只是失真。**（`推测`；06-L4）POLAR 用 reward 量护栏：18 个模型-域格只有 8 个 reward 改善；作者声明 reward 不是防伤害度量。`已核`（E-04）
- **catch/FA 与 precision 不能跨口径拼。** Ontology Catch 的**真实答案** catch 18.9% / FA 16.8%；precision 57.1% 是**人工故障 + 假设 25% 错答案**下的数，不是同一组。只看 accuracy 会把「多抓错、多杀对」混在一起。`已核`（E-02）
- **输出正确会掩盖过程无效。** SLB：85% 轨迹、24% token；B1–B4 都能通过 program accuracy，输出评估区分不出 hardcoded 与 independent。`已核`（E-07/E-09）
- **单次 score 不可靠；复合指标的定义域/档位决定可比性。** Agents are Systems：54% 方差来自**真实尝试**（过 hurdle）的同一配置重复运行；配置只解释 39.4–46.1%（取决于是否排除 hurdle 失败）；GAP_CLOSED 只在 `R>B` 定义；五轴要记档位；效率≠结果（工具调用少/错误少/校准好 ≠ pooled G 高）。`已核`（E-18）
- **覆盖率只能按失效类别分类，不能合成百分比。** 把「强度–覆盖率反向」拆成七类失效 × 八位置后，强端只在「能阻断的类别数」上更少，在「能影响的类别数」上并不更少；位置是专门化的，不是一条强度线。`推测`（设计；[coverage](./coverage.md)、[06-L15](../claims.md)）

## 文件地图

| 想知道 | 去 |
|---|---|
| 四种量错 / 方法要求 / 度量契约（工程发现 1–4：GAP_CLOSED、五轴档位、效率≠结果） | [mechanism](./mechanism.md) |
| 八行位置分派（context/memory/evidence/checker/action/commit/read-path/determinism） | [mechanism §按位置分派](./mechanism.md#按位置分派八行设计) |
| 覆盖率定义 / 七类失效 × 八位置矩阵 | [coverage](./coverage.md) |
| 四条判断的证据/口径 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 相关子页 | [trace](../trace/README.md) · [mechanism](../mechanism/README.md) · [failure-attribution](../failure-attribution/README.md) |

## 边界

- **不是「换一个指标就好」。** 要先声明机制的失效形态；指标跟着失效形态走。
- **不是「所有机制都要过程指标」。** 有些机制（动作闸门）的终点是不可逆错误，不是过程（`推测`：按 01 派的机制定义）。
- **没有统一评分卡。** 目前只有按机制分派的雏形，未做成实验。

## 关联

- 派：[06 测量](../README.md) · 冲突：[C-03](../../conclusions.md)
- 成本：[feasibility](../feasibility/README.md)
