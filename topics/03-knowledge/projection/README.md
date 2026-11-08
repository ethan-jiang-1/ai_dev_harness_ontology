---
status: draft
updated: 2026-11-08
rq: [RQ1, RQ5]
evidence: [E-12]
---

# 投影：把本体写成它读得懂的东西

> 本体是给机器推理用的结构，模型吃的是文本。这里问「怎么把结构翻译成文本、值不值得」，不负责编译证据（[compilation](../compilation/README.md)）。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 4 条（[findings](./findings.md)） |
| 未发现 / 开放 | 4 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 领域知识 → 文本/JSON/工具/检索；不含证据编译与输出判定 |

## 当前判断

- **投影文本 > JSON/查询工具/文档检索。** 同一塔：文本 0.777、打乱 0.685、JSON 0.717、查询 0.638、检索 0.597。`已核`
- **最大的一层增益是命名+单位，不是物理深度。** K0→K1 避坑率 +54.6 pp；K1→K2 +19.8 pp；H2（随容量上升）未支持，p=0.85。`已核`
- **投影是「把归纳提前做掉」，不只是换格式。** 运行教训写进塔/提示会被用；留在日志里只 4/80 被检索。`已核`
- **投影仍是弱约束。** 能被忽略；安全层必须独立于 agent。`已核`

## 文件地图

| 想知道 | 去 |
|---|---|
| 四种形态/成本/失效 | [mechanism](./mechanism.md) |
| 四条判断的证据/数字 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始论文 | [N&D digest](../../../src/papers/2610.11768-narrow-and-deep/digest.md) |

## 边界

- **不是通用知识注入。** 增益集中在「答案基本写在文本里」的任务；物理推导未测。
- **不是强约束。** 投影在上下文里，能被忽略；要硬约束进 01/02。
- **不解决可追溯。** 文本陈述不能指回节点；查询工具能，但不是所有模型会用。

## 关联

- 派：[03 知识](../README.md) · 结论：[E-12](../../conclusions.md)
- 相邻：[compilation](../compilation/README.md) · [02 evidence](../../02-judgment/evidence/README.md)
- 成本：[06-measure/feasibility](../../06-measure/feasibility/README.md)
