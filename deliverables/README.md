---
updated: 2026-11-07
---

# deliverables：交付

流水线的第四个工位。把 `topics/` 里已经站得住的判断，重新组织成**对外可用的形态**：手册、Deck、图、讲稿。

## 抽取规则

1. **只引结论，不引原文。** 交付物引用 [topics/conclusions](../topics/conclusions.md) 的编号（E-xx），不直接引 `src/`。未经消化的材料不能以成品面貌流出。
2. **不新增判断。** 交付物里不允许出现 `topics/` 中不存在的结论。抽取时发现的缺口，回到 `experiments/` 或 `src/`，不在交付物里补。
3. **每条可反查。** 交付物的每个要点都要能指回主题文档或结论编号。做不到，说明它还没被消化。
4. **标注可信度。** 已核与推测必须区分开——对外物最容易犯的错是把推测写成既成事实。

## 清单

| 交付物 | 形态 | 状态 | 依据 |
|---|---|---|---|
| [手册大纲](./handbook/outline.md) | 结构化大纲 | draft | 全仓库 |
| 手册正文 | Markdown → 可导出 | 待写 | 大纲七章 |
| 一页图：约束强度谱 | 图 | 待画 | E-01、E-04、[topics/README](../topics/README.md) |
| Deck：给工程团队的 30 分钟 | 幻灯片 | 待做 | 手册第 1、3、4 章 |

## 交付阶段（`deliverable_status`）

| 状态 | 含义 |
|---|---|
| `draft` | 结构在改 |
| `stable` | 结构冻结，可对外 |
| `frozen` | 内容冻结，仅随新证据被动修订 |

文档本身的 `status` 仍用 `seed / draft / stabilized / superseded`；`deliverable_status` 只表示交付阶段。见 [conventions](../meta/conventions.md#字段与词汇)。

## 一条判据

交付物做不出来的地方，就是研究没做完的地方。

如果某一章反复卡住，说明 `topics/` 里对应结论还是「推测」——回去补证据，而不是在交付物里绕过去。
