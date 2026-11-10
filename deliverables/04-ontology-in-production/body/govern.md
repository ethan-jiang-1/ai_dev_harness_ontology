---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# C · 治：让 3 个查询变成「敢用」

> 接 [A](./build.md)/[B](./consume.md)：回答谁有权看、泄漏怎么发现、审计留什么。示例合成（200 表/5,000 列）；执行层按 `E-20` 代码核对写（只读未重跑），不是生产泄漏率。

## C.1 三层：标签 / 策略 / 执行

| 层 | 来源状态 | 不能当什么 |
|---|---|---|
| 标签/分类 | **有来源**：Glyph 列级标签；单企业，不产策略、不执行（F1） | 策略；执行；漏标率 |
| 策略 | **无来源**：无领域策略来源；OPA 是通用候选（F3） | 执行；规则正确 |
| 执行 | **单实现**：trustgraph 读路径 post-filter；fail-open、只删 subject（F2） | 写授权；第二实现；生产效果 |

`E-22`：三层不能互推——有标签 ≠ 有策略 ≠ 执行正确。

依据：T:[access-control F1–F3](../../../topics/01-constraint/access-control/findings.md) / S:[Glyph](../../../src/papers/2609.10430-glyph/digest.md)、[trustgraph](../../../src/open-source/trustgraph-ai-trustgraph/digest.md) / E-22

## C.2 策略表（模板）

| # | principal | action | kind | condition | effect |
|---|---|---|---|---|---|
| 1 | analyst | read | column | level ≤2 | allow |
| 2 | analyst | read | column | level ≥3 | deny |
| 3 | analyst | read | column | level = null | deny |
| 4 | steward | read | any | — | allow |
| 5 | service | write | any | — | deny |
| 6 | any | read | table/dataset | — | **skip** |
| 7 | any | any | any | 无命中 | **deny** |

策略文件：[policy.json](../example/policy.json)。**优先级：先 `kind` 后 `level`**（6 先于 1–3，表/数据集不按列判）；列内 deny-overrides；**`skip` ≠ `allow`**。`principal` 来自 A.1：UI/agent→steward，governance→analyst；`resource_level` = 列 max，`user_context.clearance` = clearance。**CQ3 是元数据报表，不进列策略**；CQ1/CQ2 的结果按列过滤。open mode 只对未注册资源+flag（F6）。

**模板**：策略层无领域来源（F3）；OPA 不解析本体、只返回 decision；配置/Rego=gap。OPA input（手工投影）：`{"principal":"analyst","action":"read","resource_iri":":col_ssn","resource_level":4,"context":{"clearance":2}}`。

依据：T:[commit-gate F5–F6](../../../topics/01-constraint/commit-gate/findings.md) / S:[OPA](../../../src/open-source/open-policy-agent-opa/digest.md) / 模板

## C.3 泄漏用例：object 方向漏出

`:col_ssn` 是 SSN（level 4），属 `:t_hr`；`:hasColumn` 是反向边。

```turtle
:col_ssn :hasTag :tag_ssn_1 .        # 删：subject 侧
:t_hr :hasColumn :col_ssn .   # 留：object 侧
```

表页探针 **T1**（不是第 4 个 CQ）：
```sparql
SELECT ?col WHERE { :t_hr :hasColumn ?col }
```

`_triple_blocked` 只查 `triple.s`（`O-C02`），异常 target fail-open 原样返回（`O-C03`）。分析师（clearance 2）仍能发现「t_hr 有一列 col_ssn」——不是策略写错，是执行层单侧行为；修法（两侧约束/策略层/粗粒度 deny）未测。

依据：T:[commit-gate F6–F7](../../../topics/01-constraint/commit-gate/findings.md) / S:[trustgraph](../../../src/open-source/trustgraph-ai-trustgraph/digest.md) / 模板 / gap：object 方向无已测修法

## C.4 审计（模板）

```json
[
 {"decision_id":"dec-0001","query_id":"CQ2","executor":"rdflib+pyshacl","snapshot":"example/ 2026-11-10","who":"analyst:alice","action":"read","judged_subject":":col_ssn","subject_kind":"column","judged_triple":[":col_ssn",":columnOfTable",":t_hr"],"resource_level":4,"user_context":{"role":"analyst","clearance":2},"policy_version":"0.3.0","tag_version":"0.1.0","decision":"deny","reason":"policy_deny","evidence":[":tag_ssn_1"],"outcome":"row withheld; CQ2 0/7 for analyst","leak_check":"passed"},
 {"decision_id":"dec-0002","query_id":"T1","executor":"rdflib+pyshacl","snapshot":"example/ 2026-11-10","who":"analyst:alice","action":"read","judged_subject":":t_hr","subject_kind":"table","judged_triple":[":t_hr",":hasColumn",":col_ssn"],"resource_level":null,"user_context":{"role":"analyst","clearance":2},"policy_version":"0.3.0","tag_version":"0.1.0","decision":"skip","reason":"table_subject_not_judged","evidence":[":tag_ssn_1"],"leaked_object":":col_ssn","leaked_object_level":4,"outcome":"returned t_hr/col_ssn","leak_check":"object_direction_failed"}
]
```

最小单元=请求+`user_context`+版本+evidence+outcome+leak_check。`skip` 与 `object_direction_failed` 并存正是 C.3；`decision ∈ {allow,deny,skip}`；`reason ∈ {policy_allow,policy_deny,table_subject_not_judged,default_deny}`；`leak_check ∈ {passed,object_direction_failed}`。

依据：T:[06/trace 审计最小单元](../../../topics/06-measure/trace/mechanism.md) / 模板 / gap：访问审计字段未验证

## C.5 gap：输出校验与失败传播

- **输出校验 = gap**：无 in-scope 来源，03/querying 推给下游 checker。
- **端到端失败传播 = 模板 + gap**：旁证只有部分：[04/identity](../../../topics/04-state/identity/findings.md) 的 alias 错配沿后续观察传播（无自动回滚，幅度未测，`推测`）；[06/coverage](../../../topics/06-measure/metrics/coverage.md) 的中间产物错误是唯一无主机制类别（分类判断，非测量）。
- Graph-Agentic 未入库，只作 signal。

依据：T:[identity F3](../../../topics/04-state/identity/findings.md)、[coverage G](../../../topics/06-measure/metrics/coverage.md) / 模板 / gap：输出校验、失败传播

## C.6 证据边界

`E-22` 是单企业+单实现综合，`E-20` 是代码级分类、不支撑效应量。本章只证明三层来源与 object 机制；不证明端到端访问控制/泄漏率/审计。读过滤≠写授权；模板≠效果。

**交接**：`policy_version/tag_version` 回写 A.5；`query_id` 取自 B。

**停**：object 方向泄漏未修 / 无策略 / 无审计 → 不上线。

依据：E-22 / E-20 / gap：端到端访问控制
