---
status: draft
deliverable_status: draft
updated: 2026-11-11
target: 工程负责人 / 架构师
basis: E-01–E-20, C-03; recipes R0–R12
---

# 02 · 工程实施：把本体接进 harness 的做法

> **读者**：工程负责人 / 架构师 ｜ **回答**：拿本体做某件事，具体怎么做 ｜ **不回答**：值不值得做（去 01）、为什么是这些位置（去 03）。
>
> **第一次来**：先读 [START](../START.md)（10 分钟），再回本份。
>
> **2026-11-11 证据重置**：R4/R5/R6/R12 的原锚（E-02/E-03/E-04/E-13、Grid）已撤回/移出；这 4 条转 **gap / 待新源**，不再算 B。**当前配方计数：A=3（R1/R10/R11）/ B=4（R2/R3/R7/R8）/ C=1（R9）/ gap=4（R4/R5/R6/R12）。** 撤回清单见 [审计](../../meta/audits/2026-11-11-source-purge.md)。

## 先看一个失败

一个 agent 要改一个生产参数：它读到 `P-101 = 0.42`，但没看到单位是 **bar**，按 **MPa** 写回；下游按 MPa 执行。错误不可逆、会扩散——这不是「模型不够强」，而是名字/单位没对齐、写路径没有授权。（示意，不是真实事故；单位/别名失败见 E-12 的 K1 实验）

所以 02 先问三件事：**错可逆吗？会扩散吗？判定所需事实拿得到吗？** 今天能走的是 R1（点位语义）、R2（投影）、R3（编译）、R7（记忆）、R8（读路径）、R10/R11（离线/OBDA）和 R9（落盘授权，只有设计）。**R5（checker）、R6（动作闸）的原锚已撤回，先标 gap，不要拿旧配方上线。**

**02 的主线只有一条**：先定错 → 过 R0 → 选一个位置 → 选形态 → 定尺子 → 做完一份产物包。R1–R12 是这条线上的分支，不是并列目录。

**三条判断（读完能复述）：**

1. **点位语义是最大单层增益。** K0→K1 +54.6pp；知识投影文本只再加 +19.8pp（E-12；单工厂、9 任务、答案基本写在文本里）。先做点位语义（K1），不要先建塔。
2. **R0 是准入，不是效果证明。** 四项检查（名字/单位、声明、覆盖、执行落点）不过，后面都是沙上；过了也只证明「值得进下一轮」。
3. **约束/判定配方今天不能承诺。** R4/R5/R6 的原锚 E-03/E-02/E-04/E-13 已撤回；18 格 8 改善、catch/FA、T1-only 等旧数字都不能再用。R9（落盘授权）仍只有设计、没有实现（E-20）。

> **只读 5 页（约 40 分钟）**：本页 §0 → [地图 §2.2 分诊](./sections/map.md#22-先定错五个问题) → [R0 体检](./recipes/readiness.md) → 按错误选一条：[R1](./recipes/knowledge.md#r1--点位语义k1先把-tag-名和单位对齐) / [R2](./recipes/knowledge.md#r2--知识投影文本把领域知识写成文本固定分节是工程建议) / [R8](./recipes/constraint.md#r8--读路径过滤只做可见性不要当授权) / [R9](./recipes/constraint.md#r9--落盘前授权现在只能设计不要声称已落地) → [附录 D 产物包](./appendices/artifact-pack.md)。
>
> **内码**：R0–R12 = 准入体检 + 十二条配方；K0–K2 = N&D 实验条件（非标准；见 [01 K 页](../01-capability-status/sections/k-ladder.md)）；p_h / p_min = 编译命中率 / 盈亏平衡；O-xx = 对象地址；φ = 可逆性分数（R6），`err_rate` = accepted query 答错率；F/G = 派内 finding/gap。详见 [术语](./sections/glossary.md)。
>
> **证据等级**：接口/公式/代码锚点标 `已核` 或 `已核（代码）`；工程配方、阈值、人日估算标 `推测`。R0–R12 是工程配方，不是新 E；效应量仍看 E-xx 的限定。

## 0. 一页结论

**这份交付物只回答「怎么做」，不回答「做了有没有用」。**

1. **先做准入体检（R0）**：名字/单位、声明、覆盖、执行落点四项检查不过，后面的配方都是沙上。
2. **只选一条主配方**：按错误类型选 R1–R12；先 shadow，不要同时上三个。
3. **每条配方十字段**：目标与适用 / 前提 / 接缝与形态 / 数据契约 / 步骤 / 证据 / 成本 / 验收与 stop / 失效模式 / 可抄锚点；填不满的字段就是上游任务（R0 是准入体检，不按这十项写）。
4. **证据只到 E-xx**：recipe 是工程配方，不是新结论；效应量仍看 E-xx 的限定。
5. **做完长什么样**：一份填好的 R2/R3 或 R8 产物包；[附录 D](./appendices/artifact-pack.md) 的 R4 包只作字段模板（E-03 已撤回，不是验收依据）。
6. **如果只做一件事**：准入体检（R0）+ 账本 + 名字/单位（K1）；不要先建整座塔。


## 目录

| 节 | 文件 | 内容 |
|---|---|---|
| 导读 | [GUIDE.md](./GUIDE.md) | 先读哪一页、按什么顺序 |
| 2 地图 | [sections/map.md](./sections/map.md) | 五步法、定错、选位置/形态 |
| 3 主体 | [sections/approach.md](./sections/approach.md) | R0–R12 索引、开源、指示分级、架构、路线 |
| 4 边界 | [sections/boundaries.md](./sections/boundaries.md) | 反模式、不能证明什么 |
| 5 验收 | [sections/acceptance.md](./sections/acceptance.md) | stop、缺口、期待 |
| 6 关系 | [关系与维护](../README.md#关系与维护) | 与 01/03 的关系、维护 |
| 术语 | [sections/glossary.md](./sections/glossary.md) | R0–R12、K0–K2、p_h/FA、O 码、证据等级 |
| 阈值 | [sections/canonical.md](./sections/canonical.md) | 一个数只写一次；false-veto / R1 / 162 三处对账 |
| 配方 | [recipes/README.md](./recipes/README.md) | 13 条完整 recipe |
| 运行 | [账本](./operations/ledger.md) · [评测](./operations/evaluation.md) · [成本](./operations/cost.md) · [上线](./operations/rollout.md) · [领域](./operations/domains.md) | 开工前定口径，再设计验收/预算/上线 |
| 附录 | [接口](./appendices/interfaces.md) · [追溯](./appendices/traceability.md) · [案例](./appendices/case.md) · [产物包](./appendices/artifact-pack.md) | 定接口、核证据、看走查、对产物 |

## 关注什么 / 需要什么材料

| 项 | 内容 |
|---|---|
| 关心 | 拿本体做某件事时，从哪一步开始、接口长什么样、怎么验收/停 |
| 需要材料 | E-xx、各派 `mechanism.md`、4 个开源 digest、`recipes/` 的十字段 |
| 不做什么 | 不建本体、不评价本体质量、不新增 E；只把已有证据写成可执行配方 |