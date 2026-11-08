---
status: draft
updated: 2026-11-08
---

# 03 知识派：怎么让它知道得对

## 核心主张

两条，都与直觉相反：

1. **投影优于查询。** 把本体成段地写成文本放进上下文，比把它做成查询工具让模型自己调，更有效。
2. **编译解决预算，不解决准确率。** 预先整理结构化工件能省大量 token，但在开放域检索基准上量不出准确率增益。

这一派是六派里约束最弱的（随时可被忽略），却是工程上最常被问的一派——因为「让模型知道业务规则」几乎所有项目都从这里起步。

## 子主题地图

| 子主题 | 回答什么 | 状态 | 已发现 / 未发现 | 先读 |
|---|---|---|---|---|
| [projection](./projection/README.md) | 把领域知识投影成文本/JSON/工具 | `draft`，已拆 F/G | 4 F / 4 G | dashboard |
| [compilation](./compilation/README.md) | 把证据预编译成 claim–leaf 工件 | `draft`，已拆 F/G | 6 F / 6 G | dashboard |

## 本派当前判断

- **投影文本 > JSON/查询工具/文档检索。** 同一塔：文本 0.777、JSON 0.717、查询 0.638、检索 0.597；四个模型都有效。详见 [projection/F1](./projection/findings.md)。
- **最大一层增益是命名+单位，不是物理深度。** K0→K1 +54.6 pp，K1→K2 +19.8 pp；H2 未支持。详见 [projection/F2](./projection/findings.md)。
- **编译只解决预算。** claim–leaf 平均 −38% token，但准确率无可检出增益；盈亏平衡条件性。详见 [compilation/F2](./compilation/findings.md)。
- **两条不矛盾，差别在答案的位置。** 知识即答案 → 投影；答案要从语料检索 → 编译/检索。

## 三种供给形态

| 形态 | 做法 | 何时 |
|---|---|---|
| [投影](./projection/README.md) | 把本体成段写成文本/记录 | 知识小而深、就是答案 |
| [编译](./compilation/README.md) | 预整理成导航树/实体图/wiki | 语料大、需要反复检索 |
| 集成 | 知识并入既有系统（法规库、工单） | 有存量系统、需要治理（暂无专文） |

## 何时用 · 何时别用

**用**：封闭域、操作手册型知识、模型必须遵守某套规则。

**别用**：开放域检索、多跳问答——此时该投资的是检索 harness 本身，而不是工件。

## 本目录怎么长

| 文件/目录 | 作用 |
|---|---|
| `README.md` | 本页：派地图 + top claims；不展开机制 |
| `claims.md` | 本派局部结论账本（`03-Lx`） |
| `sources.md` | 本派 digest/card 索引 |
| `frontier.md` | 本派候选队列 |
| `<子主题>/README.md` | dashboard：覆盖/计数/当前判断/文件地图 |
| `<子主题>/findings.md` | 该子主题的发现与证据 |
| `<子主题>/frontier.md` | 该子主题的 gap/next |
| `<子主题>/mechanism.md` | 机制怎么跑（按需） |

## 持续挖掘

派级前沿、检索式与候选见 [frontier.md](./frontier.md)；子主题的 gap/next 在各自 `frontier.md`。
