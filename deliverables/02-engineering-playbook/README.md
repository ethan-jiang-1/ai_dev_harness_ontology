---
status: draft
deliverable_status: draft
updated: 2026-11-09
target: 工程负责人 / 架构师
basis: E-01–E-20, C-03; recipes R0–R12
---

# 02 · 工程实施：把本体接进 harness 的做法

> **读者**：工程负责人 / 架构师 ｜ **回答**：拿本体做某件事，具体怎么做 ｜ **不回答**：值不值得做（去 01）、为什么是这些位置（去 03）。

> 完整阅读顺序见 [deliverables/README 导读](../README.md#导读先读哪份按什么顺序)。

<img src="../_figures/02-recipes-map.svg" alt="02 选一条 recipe" width="100%">

> 这份交付物回答：**本体拿进来之后，到底能帮什么；如果我要做某件事，工程上从哪一步开始、接口长什么样、开源/论文里有没有能照抄的东西。**
>
> 它不建本体，也不评价本体质量；它假设你已经有（或能拿到）一份领域本体，问题是怎么让它被机器执行。
>
> **证据等级**：接口/公式/代码锚点标 `已核` 或 `已核（代码）`；工程配方、阈值、人日估算标 `推测`。交付物只引 E-xx，细节回 `topics/`。
>
> **R0–R12 是从 `topics/` 各派 `mechanism.md` 与代码级核对抽取的工程配方，不是新的 E。** 它们回答「怎么做」，不回答「做了有没有用」；效应量仍以 E-xx 为准。



## 0. 一页结论

**这份交付物只回答「怎么做」，不回答「做了有没有用」。**

1. **先过 R0**：名字/单位、声明、覆盖、执行落点四项检查不过，后面的 recipe 都是沙上。
2. **只选一条主 recipe**：按错误类型选 R1–R12；先 shadow，不要同时上三个。
3. **每条 recipe 十字段**：目标/前提/接口/步骤/证据/成本/验收/失效/锚点；填不满的字段就是上游任务。
4. **证据只到 E-xx**：recipe 是工程配方，不是新结论；效应量仍看 E-xx 的限定。
5. **如果只做一件事**：R0 + 账本 + K1；不要先建整座塔。


## 目录

| 节 | 文件 | 内容 |
|---|---|---|
| 2 地图 | [sections/map.md](./sections/map.md) | 五步法、定错、选位置/形态 |
| 3 主体 | [sections/approach.md](./sections/approach.md) | R0–R12 索引、开源、指示分级、架构、路线 |
| 4 边界 | [sections/boundaries.md](./sections/boundaries.md) | 反模式、不能证明什么 |
| 5 验收 | [sections/acceptance.md](./sections/acceptance.md) | stop、缺口、期待 |
| 6 关系 | [sections/relations.md](./sections/relations.md) | 与 01/03 的关系、附录、维护 |
| 配方 | [recipes/README.md](./recipes/README.md) | 13 条完整 recipe |
| 运行 | [operations/README.md](./operations/README.md) | 账本、评测、成本、上线、领域 |
| 附录 | [appendices/README.md](./appendices/README.md) | 接口、追溯、案例 |

## 关注什么 / 需要什么材料

| 项 | 内容 |
|---|---|
| 关心 | 拿本体做某件事时，从哪一步开始、接口长什么样、怎么验收/停 |
| 需要材料 | E-xx、各派 `mechanism.md`、4 个开源 digest、`recipes/` 的十字段 |
| 不做什么 | 不建本体、不评价本体质量、不新增 E；只把已有证据写成可执行配方 |
