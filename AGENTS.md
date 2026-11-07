# AGENTS.md

本仓库是**持续生长的研究档案**：材料进来 → 精读成卡 → 沉淀成主题 → 抽成交付物。交付物是文档，不是代码。

任何改动都该让某条判断更清楚、更有证据，或更可证伪。

## 入口

- 流水线全景与目录推导：[README](./README.md)
- 研究问题与假设：[THESIS](./THESIS.md)
- 术语（动笔前先对齐用词）：[GLOSSARY](./GLOSSARY.md)

## 先定位工位

| 你在做什么 | 落点 |
|---|---|
| 存原文 | `source/`，并在 [manifest](./source/papers/manifest.md) 登记 |
| 记一篇材料说了什么 | `notes/`，用 [材料卡模板](./notes/_template.md) 或 [论文卡模板](./notes/papers/_template.md) |
| 综合几个来源、形成判断 | `topics/`，用 [机制笔记模板](./meta/note-template.md) |
| 修订跨主题结论 | [topics/conclusions.md](./topics/conclusions.md) |
| 做成对外物 | `deliverables/`，只从 `topics/` 抽取 |
| 设计验证 | `experiments/`，用 [实验模板](./experiments/_template.md) |

`topics/` 内部再分层：机制 → `harness/`，语义 → `ontology/`，二者交点 → `seams/`（★ 主战场），领域 → `cases/`。跨层洞见写进 `seams/`，两侧只留指针。

## 三条硬规矩

1. **每个主张带证据等级。** 已证 / 已核 / 推测 / 存疑，四选一。没写就是推测。定义见 [conventions](./meta/conventions.md#证据等级)。
2. **区分一手与转述。** 读原文就引 `source/` 下的文件或 arXiv 编号；读综述就在卡片里写「转述自」并标 `待核`。**综述摘要不等于论文结论**——转述常丢限定条件，本仓库已因三处转述失真修正过结论。
3. **反例与正例同权重。** 与结论冲突的证据照样入库，并在 conclusions 里保留冲突条目。

## 写之后

- 问一句「这次动笔改变了哪条判断」：改了 → 更新 [conclusions](./topics/conclusions.md)；没改 → 只补来源。
- 更新被改文件的 `updated` 与 `status`，并在 [notes 台账](./notes/README.md) 记一笔。
- 新术语进 [GLOSSARY](./GLOSSARY.md)；改了术语含义，扫一遍引用它的文档。

## 不要做

- 不为「看起来完整」创建空文件或占位小节。
- 不把综述的一句话扩散到多篇文档——那会把一次误读放大成仓库共识。
- 不在 `deliverables/` 里新增 `topics/` 没有的判断。
- 不引入代码目录。验证性实现放仓库外，靠 `EXP-xxx` 编号回链。
