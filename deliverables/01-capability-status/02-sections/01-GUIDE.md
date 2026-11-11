---
status: draft
updated: 2026-11-11
parent: README.md
---

# 01 导读：先判断值不值得做

> **读者**：决策者 / 工程负责人 ｜ **读完你能**：给一项能力判 A/B/C/D，说出它离落地还差什么。

<img src="../_figures/01-capability-map.svg" alt="01 能力地图" width="100%">

## 最短路径（10 分钟）

1. 读 [README §0 一页结论](../02-sections/00-overview.md#0-一页结论)：先知道 A 可先落地、B 可试点、C 只能设计、D 反向。
2. 读 [地图 §2](02-map.md)：看能力矩阵与 X1–X9 verdict；不要一开始就翻逐项。
3. 记住一句话：**最确定的是点位语义（tag 名/单位/质量码；论文的 K1），其余都要先量 1–3 个数。**
4. 被 K0/K1/K2 卡住：读 [K 页](92-k-ladder.md)；它讲清「谁定义的、是不是标准、K3/K4 为什么不在主路径」。

## 连续读法（5 页，约 30 分钟）

按顺序读，不要跳：

1. [README §0 一页结论](../02-sections/00-overview.md#0-一页结论)：A/B/C/D 四档。
2. [地图 §2.1 判定口径](02-map.md#21-判定口径)：有序规则怎么走。
3. [决策记录 · 记录 1](09-decision-record.md)：点位语义（K1）为什么是 A，换域怎么停。
4. [边界 §4.3 反向](04-boundaries.md#43-反向在已测条件下不要做)：哪些事在已测条件下不要做。
5. [验收 §5.2](05-acceptance.md#52-期待与数据需求验收规格)：每条期待要量什么、没过怎么办。

这五页回答：**值不值得做、为什么是 A/B/C/D、什么情况下不要做、还差什么数。** 其余页是查阅，不是必读。

## 推荐顺序

| 步 | 读什么 | 读完你能 |
|---|---|---|
| 0 | [README §0](../02-sections/00-overview.md#0-一页结论) | 知道这份东西给谁、最重要三句 |
| 1 | [02-map.md](02-map.md) | 看懂 A/B/C/D 与每项判定从哪来 |
| 2 | [capabilities/README.md](../03-capabilities/README.md) | 按 A→B→C→D 找到你关心的能力 |
| 3 | [04-boundaries.md](04-boundaries.md) | 说出哪些不能当工作前提、哪些是反向 |
| 4 | [05-acceptance.md](05-acceptance.md) | 知道立项前还要量什么 |
| 5 | [关系与维护](../../README.md#关系与维护) | 需要时跳 02/03 |
| 6 | [09-decision-record.md](09-decision-record.md) | 看一条能力怎么从证据走到 A/B |
| 7 | [90-glossary.md](90-glossary.md) + [K 页](92-k-ladder.md) + [canonical](91-canonical.md) | 查内码/阈值/K 来源，不再翻三页 |
| 8 | [93-templates.md](93-templates.md) | 要自己填时，用空表 |

## 按目的

| 你要做什么 | 先读 | 再读 |
|---|---|---|
| 判断「要不要做本体」 | README §0 + 地图 | 能力 A/B + 边界 |
| 选第一个可落地的能力 | 地图的 A 行 | [capabilities/README.md#knowledge](../03-capabilities/README.md#knowledge) |
| 判断某能力能不能试点 | 地图的 B 行 | 对应 capability 文件 + 验收 |
| 评审「这个承诺靠不靠谱」 | 边界 | 验收 + 03 的 evidence |
| 只想知道「还差多远」 | 验收 | 地图的 X1–X9 verdict |
| 被 K0/K1/K2 弄晕 | [K 页](92-k-ladder.md) | [glossary](90-glossary.md) |

## 三种读法

| 时间 | 读什么 | 得到什么 |
|---|---|---|
| 10 分钟 | README §0 + 地图 | 知道结论、A/B/C/D 与最大风险 |
| 1 小时 | 0 + 地图 + 能力（先 A/B） | 能指到具体能力与证据 |
| 深读 | 0–6 全部 | 能复述条件、边界、验收与缺口 |

## 如果只做一件事

**先做点位语义（K1），再建账本。** 点位语义（tag 名/单位/质量码；论文 K1）是已测最大增益、最便宜、最可回退；账本是所有 go/no-go 的前提。

## 不要先读

- 不要先读 `data/`：那是工作底稿，先看结论与地图。
- 不要先读 03 附录：那是长版论证，等你要审边界时再看。
- 不要从「本体越全越好」开始：先看 D 反向清单。
