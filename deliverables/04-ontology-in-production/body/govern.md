---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# C · 治：让 3 个查询变成「敢用」

> 接 [A](./build.md)/[B](./consume.md)：回答谁有权看、泄漏怎么发现、审计留什么。示例合成（200 表/5,000 列）；执行层按 `E-20` 代码核对写（只读未重跑），不是生产泄漏率。
> 本章的决定：**先分清标签/策略/执行三层，再谈「敢用」。**

## C.1 三层：标签 / 策略 / 执行

| 层 | 现在有什么 | 不能当什么 |
|---|---|---|
| 标签/分类 | **有来源**：Glyph 列级标签；单企业，不产策略、不执行（F1） | 策略；执行；漏标率 |
| 策略 | **有语义、有测试、缺领域映射**：GB/T 43697 只分三级，04 的 1–4 是工程映射；XACML/ODRL/Rego/ReBAC 语义不同；10 条测试 9 条有唯一期望（T9 优先级未定） | 执行；规则正确；标准原文 |
| 执行 | **单实现**：trustgraph 读路径 post-filter；fail-open、只删 subject；无合格第二实现 | 写授权；通用行为；生产效果 |

`E-22`：三层不能互推——有标签 ≠ 有策略 ≠ 执行正确；`E-23`：读路径的单实现 10 条用例里 4 类漏洞。策略层现在有「可判定的纸面语义」，不等于有「领域策略来源」；执行层有「一个实现」，不等于有「读路径授权」。

依据：T:[access-control F1–F3](../../../topics/01-constraint/access-control/findings.md)、[policy](../../../topics/01-constraint/policy/README.md)、[read-path](../../../topics/01-constraint/commit-gate/read-path.md) / S:[Glyph](../../../src/papers/2609.10430-glyph/digest.md)、[trustgraph](../../../src/open-source/trustgraph-ai-trustgraph/digest.md) / E-22

## C.2 策略表（可判定，不是标准）

| # | test | principal | action | kind | condition | effect | obligation |
|---|---|---|---|---|---|---|---|
| 1 | T1 | analyst | read | column | level ≤2 | allow | log |
| 2 | T2 | analyst | read | column | level ≥3 | deny | log |
| 3 | T3 | analyst | read | column | level = null | deny | log |
| 4 | T5 | steward | read | any | — | allow | log |
| 5 | T6 | service | write | any | — | deny | log |
| 6 | T7/T8 | any | read | table/dataset | — | **skip** | log |
| 7 | T9 | steward | read | table | — | **未定**（R4 vs R6） | log |
| 8 | T10 | any | any | any | 无命中 | **deny** | log |

策略文件：[policy.json](../example/policy.json)；测试：[policy_tests.json](../example/policy_tests.json)（10 条输入→期望）。

`E-24`：策略层可以纸面判定，但领域映射不是标准给的；10 条测试 9 条有唯一期望，T9 优先级未定。

**三条硬规则**：

1. **先 `kind` 后 `level`**：表/数据集不按列判（T7/T8）；但 T9 暴露「kind 先于 principal」没写——steward 读 table 时 R4 与 R6 谁先，**未定**。
2. **`skip` ≠ `allow`**：`skip` 是 XACML/ODRL 都没有的第 4 种效果；必须带 `reason`，审计单列。
3. **`clearance` 在 input 里但 7 条规则均未消费**：T2 的 clearance=3 仍 deny，T5 的 clearance=1 仍 allow；它现在只是审计字段，不是策略条件。

**标准与工程的分界**：GB/T 43697 只分核心/重要/一般三级（[卡](../../../src/web/gbt-43697/gbt-43697.card.md)）；GB/T 35273 只定义个人信息/敏感个人信息（[卡](../../../src/web/gbt-35273/gbt-35273.card.md)）；04 的 1–4 数值 + 2/3 阈值是**工程映射**，不是标准条款。GB/T 条款与 XACML/ODRL 语义在 [policy](../../../topics/01-constraint/policy/mechanism.md) 里标 `待核`。

依据：E-24 / T:[policy F1–F3](../../../topics/01-constraint/policy/findings.md) / S:[OPA](../../../src/open-source/open-policy-agent-opa/digest.md) / 工程产物 + 工程选择

## C.3 泄漏：object 方向与 10 条用例

`:col_ssn` 是 SSN（level 4），属 `:t_hr`；`:hasColumn` 是反向边。

```turtle
:col_ssn :hasTag :tag_ssn_1 .        # 删：subject 侧
:t_hr :hasColumn :col_ssn .          # 留：object 侧
```

表页探针 **T1**（不是第 4 个 CQ）：

```sparql
SELECT ?col WHERE { :t_hr :hasColumn ?col }
```

**12 条泄漏用例**在 [leak_cases.json](../example/leak_cases.json)；**10 条一致性用例里已核的 4 条**（完整表见 [read-path](../../../topics/01-constraint/commit-gate/read-path.md)）：

| 用例 | trustgraph（`184f622`） | 安全期望 |
|---|---|---|
| subject 命中 | 删 | 删 |
| object 命中 | **不删**（只查 `triple.s`） | 删 |
| target 异常 | **fail-open**（当不命中） | fail-closed |
| 缺 `user_context` | 拒（唯一 fail-closed） | 拒 |

分析师（clearance 2）仍能发现「t_hr 有一列 col_ssn」——不是策略写错，是执行层单侧行为；修法（两侧约束/策略层/粗粒度 deny）**未测**。`skip` 与 `object_direction_failed` 并存正是本节的审计样例。

依据：E-23 / T:[read-path](../../../topics/01-constraint/commit-gate/read-path.md) / S:[trustgraph](../../../src/open-source/trustgraph-ai-trustgraph/digest.md) / 未测：object 方向无已测修法

## C.4 审计（schema + replay）

```json
{"decision_id":"dec-0002","query_id":"T1","who":"analyst:alice","action":"read","judged_subject":":t_hr","subject_kind":"table","resource_level":null,"policy_version":"0.3.0","tag_version":"0.1.0","decision":"skip","reason":"table_subject_not_judged","outcome":"returned t_hr/col_ssn","leak_check":"object_direction_failed"}
```

> 只留一条（dec-0002）；完整字段见 [audit.schema.json](../example/audit.schema.json)，dec-0001 是同 schema 的 deny 记录。

最小单元 = 请求 + `user_context` + 版本 + evidence + outcome + leak_check。`decision ∈ {allow,deny,skip}`；`reason ∈ {policy_allow,policy_deny,table_subject_not_judged,default_deny}`；`leak_check ∈ {passed,object_direction_failed}`。

**schema 与 replay**：[audit.schema.json](../example/audit.schema.json) 定义必填字段；replay 要求同一 `decision_id` 能用 `policy_version + tag_version + snapshot` 复现 decision。**没有 replay，审计只是日志**。

依据：T:[06/trace 审计最小单元](../../../topics/06-measure/trace/mechanism.md)、[policy mechanism](../../../topics/01-constraint/policy/mechanism.md) / 工程产物 / 未测：访问审计字段

## C.5 输出校验与失败传播

`E-27`：输出校验六类 + 三态；跨段故障会换形态。

- **输出校验现在有六类**：schema / cardinality / provenance / freshness / cross-field / semantic plausibility；三态 pass/violation/undetermined，`pass` 只在 `targeted>0` 且 `skipped=0` 时给。见 [output-validation](../../../topics/02-judgment/checker/output-validation.md)。
- **仍是 gap**：六类里只有前两类成本低；cross-field/合理性的误报未测；`0 violation` 可能只是 `targeted=0` 的空转。
- **端到端失败传播 = 矩阵 + gap**：[propagation](../../../topics/06-measure/metrics/propagation.md) 给 10 类 × 3 段与四条链；[fault_matrix.json](../example/fault_matrix.json) 是注入骨架；仍无注入实验。旁证只有部分：[04/identity](../../../topics/04-state/identity/findings.md) 的 alias 错配沿后续观察传播（无自动回滚，幅度未测，`推测`）；[06/coverage](../../../topics/06-measure/metrics/coverage.md) 的中间产物错误是唯一无主机制类别（分类判断，非测量）。
- Graph-Agentic 未入库，只作 signal。

依据：T:[output-validation](../../../topics/02-judgment/checker/output-validation.md)、[identity F3](../../../topics/04-state/identity/findings.md)、[coverage G](../../../topics/06-measure/metrics/coverage.md) / 工程产物 / 未测：生产误报、失败传播

## C.6 证据边界

`E-22` 是单企业 + 单实现综合；`E-20` 是代码级分类、不支撑效应量；`E-23` 是读路径 10 用例的代码级核对，不支撑泄漏率/生产。本章只证明三层来源、策略纸面语义、object 机制与审计字段；不证明端到端访问控制/泄漏率/审计 replay 已跑。

- 策略：标准/实现待入库；T9 无唯一期望；`clearance` 未消费。
- 执行：单实现、fail-open、只删 subject；sparql-guard/Jena 都不够第二实现；读过滤 ≠ 写授权。

**交接**：`policy_version/tag_version` 回写 A.5；`query_id` 取自 B；`decision_id` 进 C.4 audit。

**停**：object 方向泄漏未修 / 无策略测试 / 无审计 schema → 不上线。

依据：E-22 / E-20 / 未测：端到端访问控制
