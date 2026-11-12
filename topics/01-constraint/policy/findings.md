# 策略层 · 发现（F）

> 只放已经能站住的判断；标准/实现未入库前，条款与 API 标 `待核`。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 策略层是独立层：标签 ≠ 策略 ≠ 执行；不能从标签推出 allow/deny | `已核`（综合，E-22） |
| F2 | 策略语言能表达冲突/默认/义务，但 XACML/ODRL/Rego/ReBAC 语义不同，不能混用 | `已核`（标准卡；条款待核） |
| F3 | 领域标准给等级/处置，不给 principal/action 映射；映射是工程选择 | `已核`（GB/T 摘要）/ `推测`（映射） |
| F4 | 判定单位、`skip` 语义、冲突次序是策略设计的三个坑；不钉死，测试全绿也只证明自洽 | `已核`（构造可复算）/ `推测`（生产普遍性） |

## F1 · 策略层是独立层

- **判断**：访问控制至少三层——标签/分类、策略、执行。标签回答「这列是什么」，策略回答「谁在什么条件下 allow/deny」，执行回答「在哪拦、拦不住怎么办」。三层不能互推。
- **证据**：Glyph 做列级标签，不产策略、不执行；OPA 是通用策略引擎，不解析 OWL/SHACL、不消费 Glyph 标签；trustgraph 是读路径单实现，fail-open、只删 subject。
- **条件**：Glyph 单企业；trustgraph 单实现/只读代码；策略层无领域来源。
- **边界**：本页不证明「有标签就能做访问控制」；也不证明「OPA + 标签」能自动生成策略。
- **来源**：[access-control F1–F3](../../01-constraint/access-control/findings.md)；[E-22](../../conclusions.md)；[OPA digest](../../../src/open-source/open-policy-agent-opa/digest.md)。
- **等级**：`已核`（综合；三层对照）。

## F2 · 策略语言的语义不同

- **判断**：四种策略语义不能混：
  - **XACML 3.0**：policy set 的合并算法（deny-overrides / permit-overrides / first-applicable / deny-unless-permit / permit-unless-deny）+ obligation。
  - **ODRL 2.2**：permission / prohibition / duty；`odrl:conflict` 取 `perm` / `prohibit` / `invalid`；没有 XACML 式算法。
  - **Rego/OPA**：默认 deny（约定），规则序/冲突由作者写；没有内置 obligation。
  - **OpenFGA**：ReBAC，关系闭包；没有「冲突」概念，只有 check/expand。
- **含义**：策略表若写 `deny-overrides`，就要说明这是 XACML 语义，不是 ODRL；若写 `skip`，要说明它不是 allow（见 [F4](#f4--判定单位与三种未判定是策略设计的坑构造性发现)）。
- **边界**：标准条款/版本待入库核对；OpenFGA 不是策略语言，是关系授权。
- **来源**：[XACML 卡](../../../src/web/oasis-xacml-3.0/oasis-xacml-3.0.card.md) · [ODRL 卡](../../../src/web/w3c-odrl-2.2/w3c-odrl-2.2.card.md) · [OPA digest](../../../src/open-source/open-policy-agent-opa/digest.md)；Rego/OpenFGA 待入库。
- **等级**：`已核`（标准卡；条款/API 待核）。

## F3 · 领域标准不给映射

- **判断**：GB/T 43697 给数据分类分级框架与级别（核心/重要/一般；分级要素/流程），GB/T 35273 给个人信息类别与处理规则；两者都不回答「level 4 的列，analyst 能不能读」。
- **含义**：`标签 → level` 可以找标准；`level + principal + action → effect` 是工程选择，要写清是「我们的默认」，不是标准要求。
- **可证伪**：找到任一标准/监管文件，直接给出「级别 × 角色 × 动作」的 allow/deny 表，F3 后退。
- **边界**：条款号未核；标准可能要求「分级 + 审批 + 审计」，但不等于策略表。
- **来源**：[GB/T 43697 卡](../../../src/web/gbt-43697/gbt-43697.card.md) · [GB/T 35273 卡](../../../src/web/gbt-35273/gbt-35273.card.md) · 工程映射的构造例见 [F4](#f4--判定单位与三种未判定是策略设计的坑构造性发现)。
- **等级**：`已核`（GB/T 摘要）/ `推测`（映射）。

## F4 · 判定单位与三种「未判定」是策略设计的坑（构造性发现）

> 这是在一个 8 条规则 / 11 条测试的构造 fixture 上复算出来的，**不是生产泄漏率**；「生产普遍如此」是 `推测`。原走查文档已退役（[ADR 0015](../../../adr/0015-retire-04-and-renumber-05-to-10.md)），判断与字段留在这里。

- **判断**：一条策略链跑通之后，最容易在四条边上漏：
  1. **判定单位错位（LEAK-T1）**：判定按输出行的 subject 做——列查询判列、dataset 查询判 dataset；**表级/无 subject 的查询没有主语**，落到 `skip`，而执行层仍可能返回。构造例：`SELECT ?col WHERE { :t_hr :hasColumn ?col }` 的 subject 是表，规则给 `skip`，执行层返回了 `:col_ssn`（level 4）——`skip` 被当成了「不拦」。
  2. **`skip` 不是 allow**：它是 XACML 3.0 / ODRL 2.2 都没有的第 4 种效果（本仓库 `local` 扩展），必须带 `reason`、审计单列；执行层可以返回、也可以 withhold。所以「判定为 skip」与「没泄漏」是两件事。
  3. **`clearance` 在输入里但规则不消费**：角色/密级写进了上下文，规则却没有一条读它；「clearance=3 仍 deny、=1 仍 allow」是正常行为，不是 bug——要消费它得另写规则。
  4. **同优先级平局（T9）**：steward 读表同时命中 `allow` 与 `skip`，同优先级不同 effect → `undetermined`（`priority_gap`），不能偷偷改成 allow/deny；它暴露的是「kind 先于 principal」没写全。
- **含义**：设计策略表时先钉三件事——**判定单位**（列/表/dataset/聚合）、**未判定的执行语义**（skip 返回还是 withhold）、**冲突次序**（谁先于谁）。三件不钉，11 条测试全绿也只证明测试内部自洽。
- **可证伪**：找到一份公开策略规范/实现，把「无 subject 的查询」明确判为 allow 或 deny，并给出执行语义，第 1 条后退。
- **边界**：执行层是单实现（trustgraph 读路径 post-filter、fail-open、只删 subject），不能外推为「普遍行为」；本页也不说「有策略就能拦」。
- **来源**：E-21/E-22（[conclusions](../../conclusions.md)）；[access-control F1–F3](../../01-constraint/access-control/findings.md)；[XACML 卡](../../../src/web/oasis-xacml-3.0/oasis-xacml-3.0.card.md) · [ODRL 卡](../../../src/web/w3c-odrl-2.2/w3c-odrl-2.2.card.md)。
- **等级**：`已核`（构造可复算）/ `推测`（生产普遍性）。
