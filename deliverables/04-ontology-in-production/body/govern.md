---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# C · 治：让 3 个查询变成「敢用」

> 接 [A](./build.md)/[B](./consume.md)：示例合成（5 表/13 列）；执行层按代码核对写；不是生产泄漏率。
>
> **本章回答**：谁有权看、泄漏怎么发现、审计留什么。
> **你需要准备**：B 的结果；标签/等级；principal/clearance。
> **做完得到**：policy 表、10 条策略测试、12 条泄漏用例、audit schema。
> **怎么算做完**：C.6 证据与边界 + [acceptance](../sections/acceptance.md) 的 C1–C5。

## C.1 三层：标签 / 策略 / 执行

| 层 | 现在有什么 | 不能当什么 |
|---|---|---|
| 标签/分类 | **有来源**：Glyph 列级标签；单企业，不产策略、不执行（F1） | 策略；执行；漏标率 |
| 策略 | **有语义、有测试、缺领域映射**：GB/T 43697 只分三级，04 的 1–4 是工程映射；XACML/ODRL/Rego/ReBAC 语义不同；10 条测试 9 条有唯一期望（T9 优先级未定） | 执行；规则正确；标准原文 |
| 执行 | **单实现**：trustgraph 读路径 post-filter；fail-open、只删 subject；无合格第二实现 | 写授权；通用行为；生产效果 |

三层不能互推——有标签 ≠ 有策略 ≠ 执行正确；读路径的单实例 10 条用例里 4 类漏洞。

## C.2 策略表（可判定，不是标准）

| # | test | principal | action | kind | condition | clearance | effect |
|---|---|---|---|---|---|---|---|
| 1 | T1 | analyst | read | column | level ≤2 | 2 | allow |
| 2 | T2 | analyst | read | column | level ≥3 | 3 | deny |
| 3 | T3 | analyst | read | column | level = null | 2 | deny |
| 4 | T4 | analyst | read | column | level = 4 | 4 | deny |
| 5 | T5 | steward | read | column | — | 1 | allow |
| 6 | T6 | service | write | any | — | 5 | deny |
| 7 | T7/T8 | analyst | read | table/dataset | — | 2 | **skip** |
| 8 | T9 | steward | read | table | — | 3 | **undetermined**（R4 vs R6） |
| 9 | T10 | analyst | any | any | 无命中 | 2 | **deny** |

策略文件：[policy.json](../example/policy.json)（7 条规则）；测试：[policy_tests.json](../example/policy_tests.json)（10 个测试 ID → 期望）。上表 9 行是 10 个测试 ID 的归并（T7/T8 同 skip），不是按 decision 归并；`clearance` 只记录、不参与判定。`obligation` 是审计字段，不在 [policy.json](../example/policy.json) 的 7 条规则里；表比文件多一列是有意的。

策略层可以纸面判定，但领域映射不是标准给的；10 条测试 9 条有唯一期望，T9 优先级未定。

**三条硬规则**：

1. **先 `kind` 后 `level`**：表/数据集不按列判（T7/T8）；但 T9 暴露「kind 先于 principal」没写——steward 读 table 时 R4 与 R6 谁先，**未定**。
2. **`skip` ≠ `allow`**：`skip` 是 XACML/ODRL 都没有的第 4 种效果；必须带 `reason`，审计单列。
3. **`clearance` 在 input 里但 7 条规则均未消费**：T2 的 clearance=3 仍 deny，T5 的 clearance=1 仍 allow；它现在只是审计字段，不是策略条件。

**标准与工程的分界**：GB/T 43697 只分核心/重要/一般三级；GB/T 35273 只定义个人信息/敏感个人信息；04 的 1–4 数值 + 2/3 阈值是**工程映射**，不是标准条款。条款与 XACML/ODRL 语义见 evidence 附录。

## C.3 泄漏：object 方向与两套用例

`:col_ssn` 是 SSN（level 4），属 `:t_hr`；`:hasColumn` 是反向边。

```turtle
:col_ssn :hasTag :tag_ssn_1 .        # 删：subject 侧
:t_hr :hasColumn :col_ssn .          # 留：object 侧
```

表页探针 **LEAK-T1**（不是第 4 个 CQ，也不是策略测试 T1）：

```sparql
SELECT ?col WHERE { :t_hr :hasColumn ?col }
```

**两套不是一套**：10 条是 read-path 一致性用例（测实现差异），12 条是 [leak_cases.json](../example/leak_cases.json) 的泄漏面（object/alias/聚合/版本）；LEAK-T1 是后者的探针，编号不要混。

**10 条一致性用例里已核的 4 条**（完整表见 [参考表 §5](../sections/reference.md)）：

| 用例 | trustgraph（`184f622`） | 安全期望 |
|---|---|---|
| subject 命中 | 删 | 删 |
| object 命中 | **不删**（只查 `triple.s`） | 删 |
| target 异常 | **fail-open**（当不命中） | fail-closed |
| 缺 `user_context` | 拒（唯一 fail-closed） | 拒 |

分析师（clearance 2）仍能发现「t_hr 有一列 col_ssn」——不是策略写错，是执行层单侧行为；修法（两侧约束/策略层/粗粒度 deny）**未测**。`skip` 与 `object_direction_failed` 并存正是本节的审计样例。

## C.4 审计（schema + replay）

```json
{"decision_id":"dec-0002","query_id":"LEAK-T1","executor":"rdflib+pyshacl","snapshot":"example/ 2026-11-10","who":"analyst:alice","action":"read","judged_subject":":t_hr","subject_kind":"table","judged_triple":[":t_hr",":hasColumn",":col_ssn"],"resource_level":null,"user_context":{"role":"analyst","clearance":2},"policy_version":"0.3.0","tag_version":"0.1.0","decision":"skip","reason":"table_subject_not_judged","obligation":"log","evidence":[":tag_ssn_1"],"leaked_object":":col_ssn","leaked_object_level":4,"outcome":"returned t_hr/col_ssn","leak_check":"object_direction_failed"}
```

> 完整 2 条在 [audit_records.json](../example/audit_records.json)；正文只留 dec-0002，dec-0001 是同 schema 的 deny 记录。

最小单元 = 请求 + `user_context` + 版本 + evidence + outcome + leak_check。`decision ∈ {allow,deny,skip,undetermined}`；`reason ∈ {policy_allow,policy_deny,table_subject_not_judged,default_deny,priority_gap}`；`leak_check ∈ {passed,object_direction_failed,not_run}`。

**schema 与 replay**：[audit.schema.json](../example/audit.schema.json) 定义必填字段；[audit_records.json](../example/audit_records.json) 给 2 条记录。**没有 replay，审计只是日志**。

**replay 四步**：

1. 取 `decision_id` 与记录；
2. 同版本/快照重跑同一 query；
3. 对 `decision / reason / outcome`；
4. 不一致记 `replay_failed`。

## C.5 输出校验与失败传播

输出校验六类 + 三态；跨段故障会换形态。

- **输出校验现在有六类**：schema / cardinality / provenance / freshness / cross-field / semantic plausibility；三态 pass/violation/undetermined，`pass` 只在 `targeted>0` 且 `skipped=0` 时给。见 [参考表 §6](../sections/reference.md)。
- **仍是 gap**：六类里只有前两类成本低；cross-field/合理性的误报未测；`0 violation` 可能只是 `targeted=0` 的空转。
- **端到端失败传播 = 矩阵 + gap**：[参考表 §7](../sections/reference.md) 给 10 类 × 3 段与四条链；[fault_matrix.json](../example/fault_matrix.json) 是注入骨架；仍无注入实验。旁证只有部分：alias 错配沿后续观察传播（无自动回滚，幅度未测，`推测`）；中间产物错误是唯一无主机制类别（分类判断，非测量）。
- Graph-Agentic 只作 signal。

## C.6 证据与边界

> 证据见 [evidence](../evidence/README.md)。

本章不证明端到端访问控制/泄漏率/replay；限定的证据见 evidence。

- 策略：T9 未定；`clearance` 未消费。
- 执行：单实现、fail-open、只删 subject；sparql-guard/Jena 都不够第二实现；读过滤 ≠ 写授权。

**交接**：`policy_version/tag_version` 回写 A.5；`query_id` 取自 B；`decision_id` 进 C.4 audit。

**停**：object 方向泄漏未修 / 无策略测试 / 无审计 schema → 不上线。

