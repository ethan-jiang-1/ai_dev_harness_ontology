---
status: draft
updated: 2026-11-07
---

# 06 测量派：它到底有没有用

## 核心主张

三句，每句都在打前面五派的脸：

1. **答对不等于内部有本体。** 模型输出正确的本体预测，机制上却无法证明它内部真有一张本体。
2. **失败多归工作流，不归模型。** 反复出现的错误来自输入不足、接地弱、模板缺口、校验弱、非局部修复。
3. **尺子选错就看不见问题。** 用准确率量闸门、用 reward 量护栏，都会得出错误结论。

这一派不造东西，只负责让其它五派的说法能被打折或被推翻。**本仓库把这一派放在与生产派同等重要的位置**——一个没有测量派的研究仓，会退化成文献复述。

## 四把尺子 + 一个经济性横切

| 文档 | 量什么 | 结论 |
|---|---|---|
| [mechanism](./mechanism/README.md) | 本体知识是否真在模型里 | 机制可干预，但未与类别信息分离 |
| [failure-attribution](./failure-attribution/README.md) | 失败出在哪一环 | 归因到工作流，按角色做难度画像 |
| [trace](./trace/README.md) | 过程是否有效 | 输出正确掩盖了冗余与错误继承 |
| [metrics](./metrics/README.md) | 尺子本身对不对 | 度量错配是文献冲突的主因 |
| [feasibility](./feasibility/README.md) | 值不值得 | 位置×成本×使能条件；三个可算的盈亏平衡 |

四把尺子 + 一个经济性横切，各有独立子主题目录：`mechanism/`、`failure-attribution/`、`trace/`、`metrics/`、`feasibility/`。本页只做地图；详细度量在各子主题。

## 双重身份

有两篇工作既是方案又是尺子，按主效应归派，在此登记：

- **Context as Infrastructure**（主效应 [03 知识](../03-knowledge/README.md)）：它提出编译，同时用同一批实验否证了编译在准确率上的价值。
- **The Ontology Catch**（主效应 [02 判定](../02-judgment/README.md)）：它提判定器，同时证明 curated 判定器的精确度仅略优于随机。

这两篇的共同点值得记下：**提出方案的人自己给出了反证。** 这种工作比单纯的成功案例有信息量得多。

## 何时用 · 何时别用

**用**：任何要写进 `deliverables/` 的结论，都该先过一遍本派。

**别用**：把本派当拖延借口——「还没测所以不做」。测量派的价值是给已有判断标价，不是阻止判断。

## 开放问题

- 能否设计一套**按机制类型分派**的度量方案？这是本仓库最大的空缺（见 [metrics](./metrics/README.md)）。
- 「部署层面的回报」如何量化？目前它只以定性断言存在。
- 落地经济学的三个盈亏平衡（编译/分配/能力）能否在同一个实验里同时测？
- 基准的慷慨程度能否被度量？例如统计「答案有多大比例直接出现在给定材料里」。

## 本目录怎么长

| 文件/目录 | 作用 |
|---|---|
| `README.md` | 地图 + 硬证据；只做索引 |
| `claims.md` | 本派局部结论账本（`06-Lx`） |
| `sources.md` | 本派卡片索引 |
| `frontier.md` | 本派候选队列 |
| `<子主题>/README.md` | 详细机制 |
| `<子主题>/prompt.md` + `runs/` | 常驻 prompt 与按日期输出（模板见 [meta/subtopic-template](../../meta/subtopic-template/README.md)） |

新增内容只改本目录；只有跨派结论或进 `deliverables/` 时，才升到 [conclusions](../conclusions.md) 的 E-xx。卡片 `home` 指向本派，`subtopic` 指向子主题。

子主题按 [模板](../../meta/subtopic-template/README.md) 起；没有 `prompt.md` 就先不建 `runs/`。

## 持续挖掘

前沿问题、信号源、检索式与候选队列见 [frontier.md](./frontier.md)。稳定判断只在本页被改变时改写。
