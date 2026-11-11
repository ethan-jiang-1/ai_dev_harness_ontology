---
status: draft
deliverable_status: draft
updated: 2026-11-11
target: 架构师 / 研究者
basis: E-01–E-20, C-03/C-04; topics/README 四轴
---

# 03 · 机制参考：六个位置、三根分类轴与证据边界

> **读者**：架构师 / 研究者 ｜ **回答**：为什么是这些位置/形态、证据边界在哪 ｜ **不回答**：具体怎么做（去 02）、今天能做成什么（去 01）。

> **怎么用**：先读 [GUIDE.md](./GUIDE.md)；下面按四层展开。


> **这不是一本手册，也不是教程。** 它是交付物的「依据层」：解释为什么把本体接在六个位置、三根分类轴怎么分、每条判断的证据边界在哪。
>
> 2026-11-09 起，03 从「一篇长附录」升级成四层：**入口（本页）→ 位置卡 → 横切页 → 证据台账/边界/缺口**。原第三章保留为长版论证 [appendix-constraint-spectrum.md](./appendix-constraint-spectrum.md)（约 0.97 万字）；附录是历史论证，位置细节以 `positions/` 为准。



## 0. 一页结论

- **强度不是好坏。** 强度问「违反时能不能改变走向」；覆盖率问「能碰到多少类失效」。强端管得硬，但管得少。
- **强端不是更好，是更窄。** 但它不是一条可排序的强度线：六位置是专门化的，查 [coverage 矩阵](./across-positions/coverage.md)，不查直线。
- **尺子跟机制走。** 不改变走向的供给/契约位置，准确率/token 仍可用；能改变走向的判定/动作/落盘位置，用单一 accuracy/reward 会错配（C-03）。
- **六个位置问的问题不同。** context 看到什么、memory 记得什么、evidence 带什么依据、checker 对不对、action 能不能做、commit 够不够授权；不是「六个都该做」。
- **承重墙是 M1/M2。** 没有同本体跨位置对照，也没有覆盖率测量；这份参考能给出分类与边界，不能给出效应量。



## 导航

| 节 | 文件 | 内容 |
|---|---|---|
| 导读 | [GUIDE.md](./GUIDE.md) | 先读哪一页、按什么顺序 |
| 2 地图 | [sections/map.md](./sections/map.md) | 主张类型、四轴、六位置、强度矩阵 |
| 3 主体 | [positions/README.md](./positions/README.md) | 六张位置卡 + 三张横切页索引 |
| 4 边界 | [sections/boundaries.md](./sections/boundaries.md) | 15 条边界 + 12 条反例；全文在 [boundaries.md](./evidence/boundaries.md) |
| 5 验收 | [sections/acceptance.md](./sections/acceptance.md) | M1–M5、缺口 |
| 6 关系 | [sections/relations.md](./sections/relations.md) | 与 01/02 的关系、维护、目录 |
| 术语 | [sections/glossary.md](./sections/glossary.md) | E/C/H/D/G、O/B/R、seams、覆盖率符号 |
| 读者检查 | [sections/reader-checks.md](./sections/reader-checks.md) | 5 组：定位/证据/边界/形态/判不了 |
| Claim 走查 | [sections/claim-walkthrough.md](./sections/claim-walkthrough.md) | 读路径能不能防泄漏 |
| Placement | [sections/placement.md](./sections/placement.md) | 五步把 claim 放到正确位置 |
| 模板 | [sections/templates.md](./sections/templates.md) | claim 走查空表 |
| 证据 | [evidence-ledger.md](./evidence/ledger.md) | E-xx 支持/不支持哪个位置 |

## 关注什么 / 需要什么材料

| 项 | 内容 |
|---|---|
| 关心 | 为什么是这些位置、形态怎么分、每条判断的证据边界在哪 |
| 需要材料 | E-xx、`topics/` 的 mechanism/seams/execution-forms、`boundaries.md` |
| 不做什么 | 不写操作手册（去 02）、不做能力判断（去 01）；只做依据与边界 |