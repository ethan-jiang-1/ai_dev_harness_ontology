---
updated: 2026-11-09
---

# deliverables：交付

流水线的第三个工位。把 `topics/` 里已经站得住的判断，重新组织成**对外可用的形态**：手册、Deck、图、讲稿。

## 抽取规则

1. **只引结论，不引原文。** 交付物引用 [topics/conclusions](../topics/conclusions.md) 的编号（E-xx），不直接引 `src/`。未经消化的材料不能以成品面貌流出。
2. **不新增判断。** 交付物里不允许出现 `topics/` 中不存在的结论。抽取时发现的缺口，回到 `src/` 或 `frontier`，不在交付物里补。
3. **每条可反查。** 交付物的每个要点都要能指回主题文档或结论编号。做不到，说明它还没被消化。
4. **标注可信度。** 已核与推测必须区分开——对外物最容易犯的错是把推测写成既成事实。

## 三个子目录 = 三种交付物

三层，不是三本平行的书：

```
01-capability-status/     判断层：今天能做成什么、不能承诺什么
        │
        ▼
02-engineering-playbook/  操作层：拿本体做某件事，具体怎么做
        │
        ▼
03-mechanism-reference/   依据层：为什么是这些位置/形态，边界在哪
```

| 子目录 | 回答什么 | 形态 | 状态 | 依据 |
|---|---|---|---|---|
| [01-capability-status](./01-capability-status/README.md) | 哪些能落地、哪些能试点、哪些只能设计；距离多远 | 判断 + 能力矩阵 | draft | E-01–E-20、C-01–C-04 |
| [02-engineering-playbook](./02-engineering-playbook/README.md) | 选位置/形态、R1–R9、开源与论文指示分级、验收与 stop | 步骤 + 接口 + 验收 | draft | E-xx + 各派 mechanism |
| [03-mechanism-reference](./03-mechanism-reference/README.md) | 为什么是六个位置、三条轴怎么分、15 条边界 | 参考 + 一页表 | draft | E-xx + [topics/README](../topics/README.md) |
| └ [附录：约束强度谱](./03-mechanism-reference/appendix-constraint-spectrum.md) | 03 的长版论证（约 0.97 万字） | Markdown 长文 | draft | E-01–E-05、E-12–E-17、E-20、C-03 |

**怎么读**：

- 只有 10 分钟 → [01 §0 一页结论](./01-capability-status/README.md#0-一页结论) + [02 §0 决策图](./02-engineering-playbook/README.md#0-一句话与五步法)。
- 手上有一个具体任务 → [02 §1 定错](./02-engineering-playbook/README.md#1-先定错五个问题) → §2 选位置 → §4 对应 R。
- 要说服别人/自查边界 → [03 §3 六位置表](./03-mechanism-reference/README.md#3-六个位置一页表) + §5 十五条边界。
- 想读完整论证 → [附录：约束强度谱](./03-mechanism-reference/appendix-constraint-spectrum.md)。

**反向加载**：从 [01 §9](./01-capability-status/README.md#9-期待与数据需求验收规格)/[plan](./01-capability-status/plan.md)、[02 §4](./02-engineering-playbook/README.md#4-九条工程做法r1r9)、[03 §3](./03-mechanism-reference/README.md#3-六个位置一页表) 出发，按 [meta/loading 的三条反向链](../meta/loading.md#从交付物倒查反向加载) 走；不要从 `src/papers/manifest.md` 开始扫。

## 期待 → 数据（验收规格）

三份 README 的末尾都有一节「期待与数据需求」：把交付物要回答的问题写成**可证伪的期待**，再倒推「支持它需要什么数据、现在有什么、缺什么」。

它的作用不是承诺结果，而是让缺口显形：**量不出「支持它需要的数据」，就说明这条期待还停在推测。** 这是交付物的验收规格（非 E），不是新结论；数据回 `topics/` 或 `frontier` 补，不在交付物里补。

01 的详细执行计划见 [plan.md](./01-capability-status/plan.md)：覆盖审计、现有 digest 回抽、新 `src/` 来源、WBS、排期、DoD 与停止规则。

## handbook 的去留（2026-11-09）

**没有独立的 handbook。** 原《本体在 harness 里如何被执行》7 章、4–6 万字的书稿计划已废弃：

- 书稿没有独立角色——01/02/03 已经把「判断/操作/依据」三层分开，再写一本会把它们混回去。
- 第四章缺一手失败复盘、第六章缺按机制分派的度量方案、第七章是案例不是对照；按仓库规则，写不动的地方是研究没做完，不应在交付物里绕过去。
- 主线「价值不在知道更多，而在让不该发生的事不发生」接近 P1a，但 E-01 的 ontology 是 `not measured`、E-04 的结构贡献未隔离；附录已把它收窄为「强端不是更好，是更窄」。

唯一保留的是**论证资产**：原第三章成为 [03 的长版附录](./03-mechanism-reference/appendix-constraint-spectrum.md)。原大纲与规划已删除，git 历史保留；不再有第四个 `handbook/` 目录。

## 待做

| 交付物 | 形态 | 状态 | 依据 |
|---|---|---|---|
| 一页图：约束强度谱 | 图 | 待画 | [03 §4](./03-mechanism-reference/README.md#4-强度覆盖率反向组织假设不是-e) + E-01/E-04（组织假设，标注不是 E 结论） |
| Deck：给工程团队的 30 分钟 | 幻灯片 | 待做 | 02 §0、§4、§7 |
| 案例页：一个端到端示例 | Markdown | 待做 | 02 §7；需一个真实场景，当前没有 |

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
