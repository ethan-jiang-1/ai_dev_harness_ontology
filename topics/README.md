---
status: draft
updated: 2026-11-07
---

# topics：沉淀

流水线的第三个工位。材料在 `notes/` 里被读懂，在这里被**综合成可引用的判断**。

## 主题图

```
seams/  ★ 接缝 —— 本体在控制回路的五个落点
  ↑                    ↑
harness/  ★ 控制层     ontology/  语义层
              ↘        ↙
               cases/  领域约束
```

三层论点（harness / ontology / seams）加一个领域侧（cases）。层级关系与理由见 [根 README](../README.md#3-为什么-topics-只有三层)。

| 目录 | 回答 | 阅读顺序 |
|---|---|---|
| [harness/](./harness/README.md) ★ | 控制回路七环节各自如何工作、失效在哪 | 先 |
| [ontology/](./ontology/README.md) | 语义如何被表示、生产、存续 | 次 |
| [seams/](./seams/README.md) ★ | 语义在哪一步被执行、强度如何 | 核心 |
| [cases/](./cases/README.md) | 同一机制在不同领域受什么约束 | 按需 |

## 怎么增长

一个主题的正文只在被新证据**改变**时重写。触发条件有三种：

1. 新卡片（`notes/`）与已有判断冲突 → 修改正文并登记到 [conclusions](./conclusions.md) 的冲突栏。
2. 新卡片支持已有判断 → 只补来源，不改正文。
3. 新主题出现但无对应目录 → 先在 [conclusions](./conclusions.md) 里以「悬空结论」记录，累积到三条以上再开目录。

第 3 条是防止目录爆炸的闸门：**不为一篇论文开一个目录。**

## 正文的写法

- 每个文档开头是 `status` 与 `updated`，代表可信度而非篇幅。
- 结论必须带等级：**已证 / 推测 / 存疑**，与 [conventions](../meta/conventions.md) 一致。
- 与结论冲突的证据照样写入，并在 [conclusions](./conclusions.md) 保留冲突标记。
