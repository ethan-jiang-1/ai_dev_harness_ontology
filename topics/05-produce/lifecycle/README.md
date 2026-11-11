---
status: seed
updated: 2026-11-09
rq: [RQ3]
evidence: [E-02, E-05]
---

# 生命周期：来源、精化、演化

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 4 条判断（本页）+ 4 条工程发现（[mechanism](./mechanism.md)「工程发现」） |
| 未发现 / 开放 | 3 条（见下） |
| 下一步 | 见「开放问题」（3 条） |
| 最后扫描 | 2026-11-09 |
| 覆盖 | 来源/精化/对齐/演化；薄页，未拆 findings/frontier |


## 问题

本仓库与多数本体文献的一个差别：不假设本体已经存在。本体从哪来，会影响它能否被信任——这又是接缝问题（判定器的可信度继承自本体来源；「继承」本身未测）。

## 三种来源及其偏向

| 来源 | 优势 | 系统性偏向 |
|---|---|---|
| 专家手工（curated） | 语义准确、边界清晰 | 覆盖窄，维护成本高，易过时 |
| LLM 生成 | 覆盖广、启动快 | 语义漂移、看似合理的关系方向错误 |
| 数据挖掘 | 贴合实际数据分布 | 把「常出现的」当「应当成立的」，缺约束 |

**这张表的「优势/系统性偏向」两列是综合判断（`推测`）**，不是 E-02 的测量项——E-02 测的是 catch/FA/precision，没有测维护成本、覆盖窄或语义漂移。

关键结论（E-02，`已核`）：三种来源在**漏检与误报**上的权衡不同，没有单一向优者（具体数字见 [02/checker](../../02-judgment/checker/README.md)）。原文把「checker 本身」当作研究对象，而不是比较「有没有本体」。

**另一条已核（E-05，FIRME）**：本体在记忆系统里只承担跨期对齐与印证条件，不承担自由推理；alias memory 让 final-period CMR +7.8–12.1 pp（4 settings），但 false merge 长期污染未测（详见 [mechanism](./mechanism.md)「证据锚点」与 [04/identity](../../04-state/identity/README.md)）。

详见 [ontology-as-checker](../../02-judgment/checker/README.md)。

## 四个阶段

1. **获取** —— 从需求、既有系统、数据反推。此阶段的产出是**候选**，不是本体。
2. **精化** —— 已有本体的修正，而非从零构建。多数真实项目处于这一阶段（`推测`，无统计），但文献偏好研究阶段 1。
3. **对齐** —— 跨系统身份统一。需要稳定的 registry 与时间维度，否则同一实体在不同时期被当成两个。
4. **演化** —— 规则引导的自演化，或用例驱动的增量修订。

这四段是框架性归纳（`推测`），不是三篇 digest 直接测出来的：CASTON 落在第 2 段，Evontree 落在第 1/4 段，FIRME 落在第 3 段。阶段 2 到 4 的共同难点：**没有人对「这个本体今天仍然成立」负责。** 与代码不同，本体没有测试，失效是静默的。

**工具侧的部分反例（`已核`，代码；未跑）**：open-ontologies 把本体变更做成可执行检查——SHACL 校验（默认路径会列 `skipped_constraints`；verified 路径的 `oo-shacl` 用 exit 3 = undetermined，外层 CLI 再把 `conforms:null` 映射为 exit 2）、闭包差分（丢了哪些蕴含、带证书与 exit code）。所以更准确的说法是：**本体没有回归测试，但可以有一致性/约束检查**；工具让失效可见，不替人负责语义正确。引用时不要把「有检查」写成「有测试」。详见 [open-ontologies digest](../../../src/open-source/fabio-rovai-open-ontologies/digest.md)。

## 失效模式

（`推测`；证据与反例见 [mechanism](./mechanism.md)）

- **把「涌现」当「演化」。** 自动更新缺少约束时，本体缓慢漂向高频但错误的形态。
- **身份漂移。** 跨期实体未对齐，历史证据挂不上新版本。
- **演化无回滚。** 一次错误的精化污染所有下游判定，且无法定位是哪一版引入的。
- **来源不可追溯。** 一个概念是专家加的、模型编的、还是从数据里挖的，下游判定器无法区分——这直接废掉了对来源的信任分级。

## 开放问题

- 本体是否也需要「测试」——一组必须成立/必须不成立的事实对？
- 来源标记能否进入判定逻辑，使不同来源的约束具有不同权重？
- 演化速度如何与下游判定器的重训/重载节奏对齐？

## 文件地图

| 想知道 | 去 |
|---|---|
| 生命周期回路、三篇各闭合哪段、证据与边界 | [mechanism](./mechanism.md)「机制」「证据锚点」 |
| 接口/参数/成本/stop/客户指标（吸收的 4 条工程发现：观察级契约、幂等键、`CMR=MMR×precision`、准入/覆盖率 stop/schema 成本） | [mechanism](./mechanism.md)「工程发现」 |
| 实施决策 D1–D5、人日、第一个 sprint、客户指标与反例 | [mechanism](./mechanism.md)「实施与客户价值」 |
| 三篇原始 digest | [CASTON](../../../src/papers/2610.21466-caston-refinement/digest.md) · [Evontree](../../../meta/audits/2026-11-11-source-purge.md#src-2510-26683) · [FIRME](../../../src/papers/2610.40482-firme/digest.md) |
| 准入闸门的出处（只借这一处） | [OntoAct digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-21983) |
| 相关主题 | [generation](../generation/README.md) · [refinement](../refinement/README.md) · [checker](../../02-judgment/checker/README.md) |

本页即 dashboard（薄页，未拆 findings/frontier）：判断在本页，机制/实施/工程发现在 [mechanism](./mechanism.md)。
