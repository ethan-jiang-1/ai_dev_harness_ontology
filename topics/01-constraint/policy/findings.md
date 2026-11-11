# 策略层 · 发现（F）

> 只放已经能站住的判断；标准/实现未入库前，条款与 API 标 `待核`。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 策略层是独立层：标签 ≠ 策略 ≠ 执行；不能从标签推出 allow/deny | `已核`（综合，E-22） |
| F2 | 策略语言能表达冲突/默认/义务，但 XACML/ODRL/Rego/ReBAC 语义不同，不能混用 | `已核`（标准卡；条款待核） |
| F3 | 领域标准给等级/处置，不给 principal/action 映射；映射是工程选择 | `已核`（GB/T 摘要）/ `推测`（映射） |

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
- **含义**：04 的 policy 表若写 `deny-overrides`，就要说明这是 XACML 语义，不是 ODRL；若写 `skip`，要说明它不是 allow。
- **边界**：标准条款/版本待入库核对；OpenFGA 不是策略语言，是关系授权。
- **来源**：[XACML 卡](../../../src/web/oasis-xacml-3.0/oasis-xacml-3.0.card.md) · [ODRL 卡](../../../src/web/w3c-odrl-2.2/w3c-odrl-2.2.card.md) · [OPA digest](../../../src/open-source/open-policy-agent-opa/digest.md)；Rego/OpenFGA 待入库。
- **等级**：`已核`（标准卡；条款/API 待核）。

## F3 · 领域标准不给映射

- **判断**：GB/T 43697 给数据分类分级框架与级别（核心/重要/一般；分级要素/流程），GB/T 35273 给个人信息类别与处理规则；两者都不回答「level 4 的列，analyst 能不能读」。
- **含义**：`标签 → level` 可以找标准；`level + principal + action → effect` 是工程选择，要写清是「我们的默认」，不是标准要求。
- **可证伪**：找到任一标准/监管文件，直接给出「级别 × 角色 × 动作」的 allow/deny 表，F3 后退。
- **边界**：条款号未核；标准可能要求「分级 + 审批 + 审计」，但不等于策略表。
- **来源**：[GB/T 43697 卡](../../../src/web/gbt-43697/gbt-43697.card.md) · [GB/T 35273 卡](../../../src/web/gbt-35273/gbt-35273.card.md) · [04 C.2](../../../deliverables/04-ontology-in-production/03-body/03-govern.md)。
- **等级**：`已核`（GB/T 摘要）/ `推测`（映射）。
