---
status: draft
deliverable_status: draft
updated: 2026-11-09
target: 架构师 / 研究者
basis: E-01–E-20, C-03/C-04; topics/README 四轴
---

# 03 · 机制参考：六个位置、三根分类轴与证据边界

> **读者**：架构师 / 研究者 ｜ **回答**：为什么是这些位置/形态、证据边界在哪 ｜ **不回答**：具体怎么做（去 02）、今天能做成什么（去 01）。

> **这不是一本手册，也不是教程。** 它是交付物的「依据层」：解释为什么把本体接在六个位置、三根分类轴怎么分、每条判断的证据边界在哪。
>
> 2026-11-09 起，本目录从「一篇长附录」升级成四层：**入口（本页）→ 位置卡 → 横切页 → 证据台账/边界/缺口**。原第三章保留为长版论证 [appendix-constraint-spectrum.md](./appendix-constraint-spectrum.md)（约 0.97 万字）；附录是历史论证，位置细节以 `positions/` 为准。



## 0. 一页结论

- **强度不是好坏。** 强度问「违反时能不能改变走向」；覆盖率问「能碰到多少类失效」。强端管得硬，但管得少。
- **强端不是更好，是更窄。** 但它不是一条可排序的强度线：六位置是专门化的，查 [coverage 矩阵](./across-positions/coverage.md)，不查直线。
- **尺子跟机制走。** 不改变走向的供给/契约位置，准确率/token 仍可用；能改变走向的判定/动作/落盘位置，用单一 accuracy/reward 会错配（C-03）。
- **六个位置问的问题不同。** context 看到什么、memory 记得什么、evidence 带什么依据、checker 对不对、action 能不能做、commit 够不够授权；不是「六个都该做」。
- **承重墙是 M1/M2。** 没有同本体跨位置对照，也没有覆盖率测量；这份参考能给出分类与边界，不能给出效应量。



## 1. 怎么读

### 1.1 加载集（按需披露）

| 要做 | 只读 | 不读 |
|---|---|---|
| 查某个位置 | [positions/README.md](./positions/README.md) | 附录全文、其他位置卡、`src/` 原文 |
| 查某条判断的边界 | [boundaries.md](./evidence/boundaries.md) + [evidence-ledger.md](./evidence/ledger.md) + [conclusions](../../topics/conclusions.md) 的 E 行 | `src/` 原文、其他派 `mechanism.md`、全部 `paper.md` |
| 查为什么是六个位置 | [§2 地图](./sections/map.md) + [§3 主体](./positions/README.md) + [coverage](./across-positions/coverage.md) + [execution-forms](./across-positions/execution-forms.md) | 全部论文正文 |
| 查下一步研究什么 | [gaps.md](./evidence/gaps.md) + 各派 `frontier.md` | 本页不复制候选 |

> 反向链见 [meta/loading §从交付物倒查](../../meta/loading.md#从交付物倒查反向加载)：边界 → E 行 → digest §5/§9 → 附录。


### 1.2 三条阅读路径

| 时间 | 读什么 | 得到什么 |
|---|---|---|
| 10 分钟 | §0 + [§2.3 六位置表](./sections/map.md#23-六个位置一页表) | 知道六个位置问什么、为什么不是一条强度线 |
| 1 小时 | §1 + [§2](./sections/map.md) + [§3](./positions/README.md) | 能指到某个位置卡、某条边界、某个缺口 |
| 深读 | `positions/` + `across-positions/` + `boundaries.md` + `evidence-ledger.md` | 能复述机制、证据、不能证明什么 |


### 1.3 读法

- 想知道「这个机制能不能用」→ [01 §2 的能力矩阵](../01-capability-status/sections/map.md)。
- 想知道「拿本体做 X 怎么做」→ [02 §3.1 的 R0–R12](../02-engineering-playbook/sections/approach.md#31-十二条工程做法r0r12)。
- 想知道「为什么是这六个位置」→ [§2 地图](./sections/map.md) + [§3 主体](./positions/README.md) + [coverage](./across-positions/coverage.md) + [execution-forms](./across-positions/execution-forms.md)。
- 想知道「这个位置该量什么」→ [measurement](./across-positions/measurement.md)。
- 想知道「这条判断的边界」→ [boundaries.md](./evidence/boundaries.md) + [evidence-ledger.md](./evidence/ledger.md)。
- 想知道「下一步研究什么」→ [gaps.md](./evidence/gaps.md) + 各派 `frontier.md`。



## 目录

| 节 | 文件 | 内容 |
|---|---|---|
| 2 地图 | [sections/map.md](./sections/map.md) | 主张类型、四轴、六位置、强度矩阵 |
| 3 主体 | [positions/README.md](./positions/README.md) | 六张位置卡 + 三张横切页索引 |
| 4 边界 | [sections/boundaries.md](./sections/boundaries.md) | 15 条边界摘要；全文在 [boundaries.md](./evidence/boundaries.md) |
| 5 验收 | [sections/acceptance.md](./sections/acceptance.md) | M1–M5、缺口 |
| 6 关系 | [sections/relations.md](./sections/relations.md) | 与 01/02 的关系、维护、目录 |
| 证据 | [evidence-ledger.md](./evidence/ledger.md) | E-xx 支持/不支持哪个位置 |

## 关注什么 / 需要什么材料

| 项 | 内容 |
|---|---|
| 关心 | 为什么是这些位置、形态怎么分、每条判断的证据边界在哪 |
| 需要材料 | E-xx、`topics/` 的 mechanism/seams/execution-forms、`boundaries.md` |
| 不做什么 | 不写操作手册（去 02）、不做能力判断（去 01）；只做依据与边界 |
