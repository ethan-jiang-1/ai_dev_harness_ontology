---
status: draft
updated: 2026-11-11
type: evidence-note
target: X5 false-veto / X7 read-path / X8 commit gate
---

# P0 源扫描：false-veto 与 commit gate

> **工作底稿，不是交付正文。** 扫描阶段只做摘要级 go/no-go；2610.16838 与 2607.22868 已于 2026-11-09 入档（L2 digest）。外部来源只作候选，不把摘要当结论。

## 1. 检索与筛选

| 检索 | 命中 | 判断 |
|---|---|---|
| `What Can Be Enforced? 2607.22868` | arXiv 2607.22868，26 页，理论 + 实验 | **高相关**；给 false-block/miss 前沿与 conformal 校准，可能改写 X5 的「false-veto 不可测」表述 |
| `commit boundary implementation entity resolution` | Zenodo 23580733（Commit Boundary 原论文，已入档）；arXiv 2610.16838（授权 benchmark） | **无实现**；X8 仍是 `unknown/无实现` |
| `false veto guardrail annotation blocked decisions agent` | arXiv 2610.16838；POLAR（已入档） | **高相关**；直接测「同操作、不同权限」下的误拦 |
| `SHACL access control read path policy filter ontology` | GraphDB 文档；无第二个独立实现 | X7 的第二个实现本轮未找到；保持 `unknown` |

## 2. 候选 A：What Can Be Enforced?（2607.22868）

**摘要级事实**（只读 arXiv 摘要，未读正文）：

- 把运行时 guardrail 拆成三个问题：可表示的策略、judge 观察到什么、干预是否改变未来行为。
- 对固定 oracle 谓词，确定性 gate 能执行的策略 = 其 register model 识别的「好前缀」；策略非平凡性在 2 个可减计数器下不可判定，在 separable monotone fragment 下是 PSPACE。
- 在固定外生 law 下，Neyman–Pearson 给出精确的 **false-block/miss 前沿**；conformal 校准给出有限样本边际证书（可能通过 block-all）。
- 一旦阻断改变未来 proposal，静态分数与 ungated 轨迹不必识别闭环前沿；需要有限受控模型 + occupancy program。
- 有界表示攻击会加 robustness margin；benign calibration 不自动迁移。
- 实验：静态诊断、受控模型枚举、表示重写、配对闭环重跑。

**为什么重要**：它把「false-veto」从「没有标签所以不可测」推进到「有 false-block/miss 前沿与校准证书」。如果成立，D1 的 X5 不应只写 `unknown`，而应写「可校准，但需要策略表示与 oracle 谓词；POLAR 没有这些」。

**go/no-go**：**go（P0，已入档 2026-11-09）**。它不是实证误拦率，不能直接填 X5 的「false-veto ≤5%」；但它给出 false-block/miss 前沿与校准协议，已写成 L2 digest（`src/papers/2607.22868-what-can-be-enforced/digest.md`），作为 X5 的边界，不升 E。

**入档判据**：报告 false-block/miss 前沿或校准协议，且能映射到 POLAR 的 blocked log；否则只进 `frontier`。

## 3. 候选 B：Same Operation, Different Permission（2610.16838）

**摘要级事实**（只读 arXiv 摘要，未读正文）：

- 提出一个 benchmark，对比「同一操作」在不同授权证据下的 guardrail 决策；语言轨 + 执行验证 + 外部 native-policy 请求。
- 检查每个决策的正确性、可用性、实际效果；跟踪同一请求在 guardrail 变化下的表现。
- 发现：很多被 block 的操作来自 **failed reviews**，不是正确的拒绝；修输出格式能恢复可用决策，但会改变哪些授权请求被放行；加第二个 reviewer 会去掉一些错误，但也会拒绝合法授权。
- 结论：guardrail 应同时在「拦住的未授权动作」和「放过的已授权动作」上评估。

**为什么重要**：这正是 X5 的 false-veto 与 X8 的 authorization 的交集；它提供了「同操作、不同权限」的评估设计，能补 POLAR 的「block log 无授权标签」。如果它的数据/代码公开，可作为 X5/X8 的实证来源。

**go/no-go**：**go（P0，已入档 2026-11-09）**。它比 A 更直接：有 benchmark、有授权标签、有误拦结果。已下载 PDF、转 MD、建卡、L2 digest（`src/papers/2610.16838-same-operation-different-permission/digest.md`）；数字见 §3.1。

### 3.1 具体数字（摘要 + HTML 正文，2026-11-09）

| 项 | 数字/事实 |
|---|---|
| benchmark | AuthorizationPairs：语言轨 50 scenarios × 4 contexts = 200；40 dev / 160 test；**80 lawful / 80 forbidden**；1,600 effects |
| native 轨 | 1,594 requests / 47 apps / 60 policies；379 dev / 1,215 test；OpenFGA + Cedar；引擎复现所有标签 |
| 标注 | 3 位安全专家；200 contexts；Fleiss κ=0.91；14 个分歧裁决；67 条解释注记 |
| guardrail | 8 configs：Qwen3.5-9B/27B、Safeguard、Granite、PolicyGuard、NeMo、Qwen3Guard、Nemotron |
| native 结果 | Qwen3.5-27B 99.1%（1 incorrect approval、10 false denials）；Safeguard 84.2%（174/767 false denials）；Qwen3.5-9B 69.4%（261/448 incorrect approvals） |
| structured review | Qwen3.5-9B 117–124/160 **unavailable decisions**；27B 48–50/160；不是 truncation，是格式失败 |
| schema decoding | 所有决策可用；但 9B 仍最多 6 个 forbidden effects；27B 每 seed 5–6 个 false denials |
| 加 reviewer | Safeguard after 27B：去掉 1 个 incorrect approval，但 **veto 171 个 lawful requests** |
| direct→schema | 5/6 runs 同时有 gains 和 losses；net −3 到 +27；36 个对比里只有 1 个过 Holm |
| 核心句 | **「Blocked does not mean denied」**：unavailable decision 也会阻断执行，在 prevention 总数里看起来像 denial |

**对 D1 的意义**：

- X5 的 false-veto 仍没有「本体闸」的一手数；但 2610.16838 证明**授权标签 + 请求级配对**可以测「误拦合法请求」，而且误拦很常见（Safeguard 174/767）。这为 X5 提供了**评估方法**，不是 POLAR 的替代数字。
- X8 的授权问题被具体化：guardrail 的「拒绝」可能是 review 失败，不是正确拒绝；commit gate 也需要区分「拒绝未授权」与「review 不可用」。
- 它**不改变** X5/X8 的 verdict：X5 false-veto 仍 `unknown`（POLAR 无标签）；X8 仍无 commit gate 实现。它改变的是「下一步怎么测」。

## 4. 对 X7/X8 的即时结论

- **X7**：本轮没有找到第二个独立 read-path 实现；`read-path` 保持轴外，object 方向仍 `unknown`。
- **X8**：本轮没有找到 commit gate 实现；Commit Boundary 仍是概念架构；X8 保持 `C 只能设计`，false-defer `unknown`。
- **X5**：POLAR 仍无 false-veto 标签；但 A/B 两个候选说明「可校准/可评估」的路径存在。D1 应把 X5 从「完全不可测」改成「**有校准/评估路径，但没有一手误拦数**」。

## 5. 下一步

1. ~~落盘 2610.16838（P0），建卡 + L2 digest~~ **已完成**（2026-11-09）；下一步：把「同操作/不同权限」设计映射到本体 checker。
2. ~~读 2607.22868 正文的 false-block/miss 前沿与校准部分~~ **已完成并入档**；下一步：把 T2 前沿搬到本体 checker，不急着升 E。
3. 继续扫第二个 read-path 实现（P1）；没有就保持 `unknown`。
4. 把本页结论回写 [plan](../../_plans/01-capability-status.md) §4 的 P0 行与 D1 §9 的 verdict。

> 回 [01 目录](../README.md) ｜ 回 [01 §数据表](../README.md#数据表工作底稿)
