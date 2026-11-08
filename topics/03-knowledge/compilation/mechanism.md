# 编译 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 问题

agentic 检索会重复查询、重读文档、把窗口塞满未使用的段落；知识编译在检索前把源文档加工成不含于任何单一片段的结构（导航层级、实体图、时间线、wiki、本体、记忆）。

## 机制一：需求侧的三层（CAI）

![Figure 1: Context as infrastructure](../../../src/papers/2610.41172-context-as-infrastructure/figures/fig-1-context-as-infrastructure.png)

> 原图：CAI, p.4, Figure 1（arXiv:2610.41172）。版权归作者，研究评论用途。

**看什么**：供给（index time）、契约（tools）、控制（query time）是三种职责。编译在检索之前发生，但「什么进窗口、什么时候停」仍由 harness 决定。

| 步骤 | 做什么 | 工程要点 |
|---|---|---|
| Parse | 原文件 → 规范表示 | 保留标题、表格、页锚 |
| Chunk | 自然边界切块 | chunker 与基线固定 |
| Enrich | 小模型逐块抽 claim–evidence | 可以用便宜模型 |
| Validate | span 逐字比对，对不上就丢 | 不让模型修 |
| Assemble | claim 聚类成树/图 | 内部节点是标签，不是摘要 |
| Register | 源版本、offset、抽取器版本、ACL | 审计/fallback/增量 |

## 机制二：三种服务模式（CAI）

| 模式 | 做什么 | 代价 |
|---|---|---|
| E1 evidence-first | 直接在证据索引上词法检索 | 少一跳；优于文档→树 |
| E2 substitution（默认） | 定位 chunk 后用 claim–evidence 替换 | 省 token 但增加轮次 |
| E3 decision-gated | 小决策模型判断是否深读 | 控制读不读；无证据时省 30% |

**树是 carrier，不是 retriever。** 检索始终是词法的；语义步由 agent 改写查询完成。

## 机制三：harness 六条不变量（CAI）

1. Evidence before thought；2. Discard on insufficiency；3. Tool gating；4. Budgeted calls；5. Citations at delivery；6. Guaranteed close。

工具按失败组织：词汇不匹配、定位、跨源关系、时间歧义、综合负担、工具/语法错误。

## 机制四：受监管知识系统（Grid Agents）

Grid Ontology = 27 docs / 6,347 pages 的法规/标准 + 语义/程序/情景记忆；Grid Studio = 领域工具 + solver + optimizer。

- 答案必须引用 evidence；数字由 solver 算；人做决策。
- **strict pass**：重放工具调用，检查 study 跑在哪个 network state。
- **工具必须到达研究**：PowerMCP 只在 46/519 任务被调用。
- optimizer 在环：加固方案便宜 33–67%。

## 失效模式

- **平均掩盖条件。** −38% 是 −91% 与 +1.9% 的混合。
- **省 token 换时延。** 证据替换增加轮次；配对子集时延约 3×。
- **接受率当正确率。** `p_h` 只说放行多少，不说放对没有；φ 未测。
- **编译产物被当事实。** 产物有误差，进入后续对话后不再被质疑。
- **大纲式结构在规模上退化。** PageIndex 的失败是规模观察，不是普遍规律。
- **树被当检索器。** 树是 carrier；路由用树会多一跳且可能带偏。
- **部署价值被当已证。** Table 2 为空；引用时必须标「作者主张，未量化」。

## 与本体 / 回路的关系

本体在编译里以 **typed artifact / constraint / evidence** 出现；约束强度弱到中（能省预算、能做审计，但不阻止动作）。被违反时通常没有信号——这是它必须配 harness/判定器的原因。

## 关联

- [CAI 卡](../../../src/papers/2610.41172-context-as-infrastructure/card.md) · [digest](../../../src/papers/2610.41172-context-as-infrastructure/digest.md)
- [Grid 卡](../../../src/papers/2611.03534-power-system-agentic/card.md) · [digest](../../../src/papers/2611.03534-power-system-agentic/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
