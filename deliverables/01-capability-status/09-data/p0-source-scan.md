---
status: draft
updated: 2026-11-11
type: evidence-note
target: X5 false-veto / X7 read-path / X8 commit gate
---

# P0 源扫描：false-veto 与 commit gate

> **2026-11-11 素材重置注（历史扫描工作底稿）**：本页提到的 `2607.22868`（What Can Be Enforced?）、`2610.16838`（Same Operation, Different Permission）、`2610.08082`（POLAR）与 `2610.37407`（Commit Boundary）均因未过 [CHARTER §4](../../../CHARTER.md#4-素材准入material-gate) 准入门于 2026-11-11 移出（见 [黑名单](../../../meta/rules/excluded-sources.md) 与 [审计](../../../meta/audits/2026-11-11-source-purge.md)）。本页仅保留为检索方法与问题定义参考，不再作入档/定锚证据。
>
> **工作底稿，不是交付正文。** 外部来源只作候选，不把摘要当结论。

## 1. 检索与筛选

| 检索 | 命中 | 判断 |
|---|---|---|
| `What Can Be Enforced? 2607.22868` | `[已移出/黑名单]` 原 arXiv 2607.22868 | 2026-11-11 因单作者/无采用移出（作概念对照：false-block/miss 前沿不可当单点阈值） |
| `commit boundary implementation entity resolution` | `[已移出/黑名单]` 原 Commit Boundary（2610.37407）与 2610.16838 | **无实现**；X8 仍是 `unknown/无实现` |
| `false veto guardrail annotation blocked decisions agent` | `[已移出/黑名单]` 原 arXiv 2610.16838 与 POLAR（2610.08082） | 2026-11-11 均已移出；方向保留：找带授权标签的过门新源 |
| `SHACL access control read path policy filter ontology` | GraphDB 文档；无第二个独立实现 | X7 的第二个实现本轮未找到；保持 `unknown` |

## 2. 候选 A（历史检索快照，已于 2026-11-11 移出）：What Can Be Enforced?（2607.22868）

**摘要级事实**（只读 arXiv 摘要，未读正文）：

- 把运行时 guardrail 拆成三个问题：可表示的策略、judge 观察到什么、干预是否改变未来行为。
- 对固定 oracle 谓词，确定性 gate 能执行的策略 = 其 register model 识别的「好前缀」；策略非平凡性在 2 个可减计数器下不可判定，在 separable monotone fragment 下是 PSPACE。
- 在固定外生 law 下，Neyman–Pearson 给出精确的 **false-block/miss 前沿**；conformal 校准给出有限样本边际证书（可能通过 block-all）。
- 一旦阻断改变未来 proposal，静态分数与 ungated 轨迹不必识别闭环前沿；需要有限受控模型 + occupancy program。
- 有界表示攻击会加 robustness margin；benign calibration 不自动迁移。
- 实验：静态诊断、受控模型枚举、表示重写、配对闭环重跑。

**为什么重要**：它把「false-veto」从「没有标签所以不可测」推进到「有 false-block/miss 前沿与校准证书」。如果成立，D1 的 X5 不应只写 `unknown`，而应写「可校准，但需要策略表示与 oracle 谓词；POLAR 没有这些」。

**go/no-go**：**已于 2026-11-11 随准入门移出**（原 2026-11-09 曾入档 L2，现见 [tombstone](../../../meta/audits/2026-11-11-source-purge.md#src-2607-22868)）；仅保留其「miss–false-block 前沿」问题框架，不可引用为现行证据。

**入档判据**：报告 false-block/miss 前沿或校准协议，且能映射到 POLAR 的 blocked log；否则只进 `frontier`。

## 3. 候选 B（历史检索快照，已于 2026-11-11 移出）：Same Operation, Different Permission（2610.16838）

**摘要级事实**（只读 arXiv 摘要，未读正文）：

- 提出一个 benchmark，对比「同一操作」在不同授权证据下的 guardrail 决策；语言轨 + 执行验证 + 外部 native-policy 请求。
- 检查每个决策的正确性、可用性、实际效果；跟踪同一请求在 guardrail 变化下的表现。
- 发现：很多被 block 的操作来自 **failed reviews**，不是正确的拒绝；修输出格式能恢复可用决策，但会改变哪些授权请求被放行；加第二个 reviewer 会去掉一些错误，但也会拒绝合法授权。
- 结论：guardrail 应同时在「拦住的未授权动作」和「放过的已授权动作」上评估。

**为什么重要**：这正是 X5 的 false-veto 与 X8 的 authorization 的交集；它提供了「同操作、不同权限」的评估设计，能补 POLAR 的「block log 无授权标签」。如果它的数据/代码公开，可作为 X5/X8 的实证来源。

**go/no-go**：**已于 2026-11-11 随准入门移出**（原 2026-11-09 曾入档 L2，现见 [tombstone](../../../meta/audits/2026-11-11-source-purge.md#src-2610-16838)）；§3.1 摘要数字仅作撤源前历史备份，不可引用为现行证据。

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

- X5 的 false-veto 仍没有「本体闸」的一手数；原 `2610.16838` 已移出（见黑名单），但其「授权标签 + 请求级配对」的评测思路可供新源对照；X5 verdict 保持 `unknown`。
- X8 的授权问题被具体化：guardrail 的「拒绝」可能是 review 失败，不是正确拒绝；commit gate 也需要区分「拒绝未授权」与「review 不可用」。
- 它**不改变** X5/X8 的 verdict：X5 false-veto 仍 `unknown`（POLAR 无标签）；X8 仍无 commit gate 实现。它改变的是「下一步怎么测」。

## 4. 对 X7/X8 的即时结论

- **X7**：本轮没有找到第二个独立 read-path 实现；`read-path` 保持轴外，object 方向仍 `unknown`。
- **X8**：本轮没有找到 commit gate 实现；Commit Boundary 仍是概念架构；X8 保持 `C 只能设计`，false-defer `unknown`。
- **X5**：POLAR 仍无 false-veto 标签；但 A/B 两个候选说明「可校准/可评估」的路径存在。D1 应把 X5 从「完全不可测」改成「**有校准/评估路径，但没有一手误拦数**」。

## 5. 下一步

1. 原 `2610.16838` 已于 2026-11-11 移出（见 [tombstone](../../../meta/audits/2026-11-11-source-purge.md#src-2610-16838)）；按五门重找带权限标签的 guardrail 过门新源。
2. 原 `2607.22868` 已于 2026-11-11 移出（见 [tombstone](../../../meta/audits/2026-11-11-source-purge.md#src-2607-22868)）；保留「miss–false-block 前沿」问题定义，等待过门新源。
3. 继续扫第二个 read-path 实现（P1）；没有就保持 `unknown`。
4. 把本页结论回写 [plan](../../../meta/archive/2026-11/plans/01-capability-status.md) §4 的 P0 行与 D1 §9 的 verdict。

> 回 [01 目录](../README.md) ｜ 回 [01 §数据表](../README.md)
