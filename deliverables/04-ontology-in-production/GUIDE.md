---
status: draft
updated: 2026-11-10
parent: README.md
---

# 04 导读：按你的时间选一条路

> 本页只给阅读路径，不重复正文。第一次来，先读 [README](./README.md) §0，再按本页选路径；术语卡在 [glossary](./sections/glossary.md)。

## 10 分钟：先判断要不要读

适合：只想判断这套东西值不值得投入；只读，不建。

1. [README §0](./README.md#0-你带着什么问题来)：先判断要不要读。
2. [A.1 契约](./body/build.md)：看 3 行契约长什么样，governance 用哪个 principal。
3. [A.5 三关](./body/build.md)：看 `build_report` 该有什么，版本从哪来。
4. [B.2 CQ1](./body/consume.md)：看一条 raw 查询和它的 principal。
5. [C.2 策略表](./body/govern.md)：看 T1/T2/T7/T9/T11 怎么复算。

**做完你能回答**：这张 fixture 能不能从契约走到一条受控查询；哪些数字是 raw，哪些是 governed。要更完整，走 [30 分钟 8 步](#p-30min)；要拿这个判断去拍板，读 [decision](./sections/decision.md) §0/§5。

<a id="p-30min"></a>
## 30 分钟：读懂一条最小链（8 步）

> 目标不是建完，是**读懂一条最小链**：契约 → TBox → shapes → 3 条 CQ → policy → audit → 回填。下面的“核对”都是读文件/看表，不运行代码。

| 步 | 读什么 | 核对什么 | 去哪 |
|---|---|---|---|
| 1 | 消费者契约 3 行 | consumer/principal/moment/answers/refuses/load 是否齐；governance 是 `governance` 不是 analyst | [A.1](./body/build.md) |
| 2 | 最小 TBox + ABox | 11 类/5 属性；`WorkEmail` 是 `Email` 子类；5 表/13 列 | [A.2](./body/build.md)–[A.3](./body/build.md) |
| 3 | 2 条 shape + 负例表 | 每条约束有已知违反 + 干净样本；范围 1–4 | [A.4](./body/build.md) |
| 4 | `build_report` 三关 | load/validate/answer 各记什么；`targeted=0` 不是 pass；版本来源表 | [A.5](./body/build.md) |
| 5 | 3 条 CQ | raw 2 列 2 表 / 7 列 4 表 / 4 数据集；每条 principal；0 行分因 | [B.0](./body/consume.md)–[B.2](./body/consume.md) |
| 6 | 8 条 policy + 判定顺序 | 复算 T1/T2/T7/T9/T11；T9 为什么 undetermined | [C.2](./body/govern.md) |
| 7 | 3 条 audit + query log | per-subject vs query 级；skip/returned vs skip/withheld | [C.4](./body/govern.md) |
| 8 | journey | 能说出 CQ1 steward vs analyst 的差别 | [journey](./sections/journey.md) |

这 8 步只读；不要求安装 `rdflib`/`pyshacl`，不要求跑 SPARQL。要看“一条查询从头到尾”，读 [journey](./sections/journey.md)；要自己试跑，见 [example/run.md](./example/run.md)。

**做完你能回答**：一条受控查询从契约到 audit 要哪些字段与门槛；哪些数字是 raw，哪些是 governed。

## 2 小时：建 + 用 + 治各读一遍

适合：要评估落地工作量；读，不跑。

1. [README §2 产物地图](./README.md#2-九件产物地图)：先看 9 件产物。
2. [A · 建](./body/build.md)：契约 → 表示 → 本体 → shapes → 三关。
3. [B · 用](./body/consume.md)：资产表 → 3 条 CQ → 空结果分因 → 纠错/OBDA。
4. [C · 治](./body/govern.md)：三层 → 策略/判定顺序 → skip/leak → 审计/query log。
5. [journey](./sections/journey.md) + [example](./example/README.md)：把一条查询从头到尾走一遍。

**做完你能回答**：这条链要哪些产物、哪些字段、哪些门槛。**具体工期看下面的工作量口径，不是 2 小时能估出来的。**

读完后要动手：读 [transfer](./sections/transfer.md) 选一条推导，再用 [templates](./sections/templates.md) 填。标签/等级从哪来：读 [label-source](./sections/label-source.md)；换一个域怎么走：读 [worked-example](./sections/worked-example.md)。要拍板：读 [decision](./sections/decision.md)。

## 工作量口径（`推测`，不是报价）

| 项 | 量级 | 说明 |
|---|---|---|
| 建模（结构表） | 2–4 人周 | 5 表/13 列的小域；来自 `topics/consumability` 的单域估算 |
| shapes | 3–5 人日 | 2 条 shape + 负例；不含跨 validator |
| 集成（外部服务） | 1–2 人周 | 外部服务集成估算；查询胶水未估 |
| 打标/执行层/审计 | 未估 | 标签来源、第二实现、审计运营；见 [decision §2](./sections/decision.md#2-成本先算分母) |

> 这是 `推测`，不是承诺；你的域/规模/现有栈会改变它。04 不给报价。

## 1 天：按角色走

| 角色 | 先读 | 再读 |
|---|---|---|
| 数据/本体 | [A.1](./body/build.md)–[A.5](./body/build.md) | [transfer §2–§4](./sections/transfer.md)、[label-source](./sections/label-source.md)、[worked-example](./sections/worked-example.md)、[T0/T2–T4](./sections/templates.md)、[acceptance](./sections/acceptance.md) |
| 应用/agent | [B.0](./body/consume.md)–[B.4](./body/consume.md) | [transfer §3–§5](./sections/transfer.md)、[T1/T5](./sections/templates.md)、[参考表 §3](./sections/reference.md)、[journey](./sections/journey.md) |
| 治理/安全 | [C.1](./body/govern.md)–[C.4](./body/govern.md) | [transfer §5–§6](./sections/transfer.md)、[label-source](./sections/label-source.md)、[T5–T6](./sections/templates.md)、[参考表 §5–§7](./sections/reference.md)、[boundaries](./sections/boundaries.md) |
| 评审/负责人 | [README §4](./README.md#4-验收5-组门槛) + [acceptance](./sections/acceptance.md) | [decision](./sections/decision.md) + [boundaries](./sections/boundaries.md) + 工作量口径 |

> **门槛 5 组见 acceptance**：A1–A4 / A5+B1–B3 / C1–C3 / C4–C5 / 无未修漏洞。别把 GUIDE 的阅读路径当门槛数。

## 卡住了

先查 [症状地图](./sections/map.md)：按「你看到什么」定位到章/节，不要从第一页重读。

## 读完之后

- 要判断「值不值得」：回 [01](../01-capability-status/README.md)。
- 要选接缝/recipe：回 [02](../02-engineering-playbook/README.md)。
- 要查机制/边界：回 [03](../03-mechanism-reference/README.md)。
- 要从自己的表动手：读 [transfer](./sections/transfer.md) + [templates](./sections/templates.md)；标签来源看 [label-source](./sections/label-source.md)；换域看 [worked-example](./sections/worked-example.md)。
- 要拍板/写 memo：读 [decision](./sections/decision.md)。
- 要查证据：看 [evidence/ledger.md](./evidence/ledger.md)（附录）。
