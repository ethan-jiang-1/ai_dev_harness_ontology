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
> **做完得到**：policy 表、11 条策略测试、12 条泄漏用例、audit schema + 3 条样例。
> **怎么算做完**：C.6 证据与边界 + [acceptance](../sections/acceptance.md) 的 C1–C5。

## C.1 三层：标签 / 策略 / 执行

| 层 | 现在有什么 | 不能当什么 |
|---|---|---|
| 标签/分类 | **有来源**：Glyph 列级标签；单企业，不产策略、不执行（F1） | 策略；执行；漏标率 |
| 策略 | **有语义、有测试、缺领域映射**：GB/T 43697 只分三级，04 的 1–4 是工程映射；XACML/ODRL/Rego/ReBAC 语义不同；11 条测试 10 条有唯一期望（T9 优先级未定） | 执行；规则正确；标准原文 |
| 执行 | **单实现**：trustgraph 读路径 post-filter；fail-open、只删 subject；无合格第二实现 | 写授权；通用行为；生产效果 |

三层不能互推——有标签 ≠ 有策略 ≠ 执行正确；读路径的单实例 10 条用例里 4 类漏洞。

## C.2 策略表（可判定，不是标准）

**8 条规则**（[policy.json](../example/policy.json)）；每条都带 `obligation: log`，它是审计字段，不参与判定。

| # | id | principal | action | kind | condition | effect | 优先级 |
|---|---|---|---|---|---|---|---|
| 1 | R1 | analyst | read | column | level 1–2 | allow | 10 |
| 2 | R2 | analyst | read | column | level 3–4 | deny | 10 |
| 3 | R3 | analyst | read | column | level null | deny | 10 |
| 4 | R4 | steward | read | any | — | allow | 20 |
| 5 | R5 | any | read | table / dataset | — | **skip** | 20 |
| 6 | R6 | service | write | any | — | deny | 10 |
| 7 | R7 | any | any | any | 无命中 | deny（default） | 99 |
| 8 | R8 | governance | read | dataset | — | allow | 10 |

**判定顺序**（按文字复算，不需要引擎）：

1. 按 `principal/action/kind/condition` 收集**非 default** 规则；R7 是 fallback，不参与竞争。
2. 没有命中 → R7，`default_deny`。
3. 取优先级数字最小的一组。
4. 该组只有一个 effect → 用它；同优先级但 effect 不同 → `undetermined`，`priority_gap`。
5. `reason`：具体规则 → `policy_allow`/`policy_deny`；skip → `table_subject_not_judged`；fallback → `default_deny`；平局 → `priority_gap`。

为什么 T9 是 `undetermined`：steward 读 table 同时命中 R4（allow）和 R5（skip），两者都是优先级 20，effect 不同。**不把 T9 偷偷修成 allow/deny**；它暴露的是“kind 先于 principal”没写全。

**11 条测试**（[policy_tests.json](../example/policy_tests.json)）：

| # | principal | action | kind | level | 期望 | reason | 命中 |
|---|---|---|---|---|---|---|---|
| T1 | analyst | read | column | 2 | allow | policy_allow | R1 |
| T2 | analyst | read | column | 3 | deny | policy_deny | R2 |
| T3 | analyst | read | column | null | deny | policy_deny | R3 |
| T4 | analyst | read | column | 4 | deny | policy_deny | R2 |
| T5 | steward | read | column | 4 | allow | policy_allow | R4 |
| T6 | service | write | column | 1 | deny | policy_deny | R6 |
| T7 | analyst | read | table | null | skip | table_subject_not_judged | R5 |
| T8 | analyst | read | dataset | 3 | skip | table_subject_not_judged | R5 |
| T9 | steward | read | table | null | **undetermined** | priority_gap | R4/R5 |
| T10 | analyst | delete | column | 1 | deny | default_deny | R7 |
| T11 | governance | read | dataset | null | allow | policy_allow | R8 |

`clearance` 只在输入/审计里，**8 条规则均未消费**；T2 的 clearance=3 仍 deny，T5 的 clearance=1 仍 allow。

**三条硬规则**：

1. **先 `kind` 后 `level`**：表/数据集不按列判（T7/T8）；但 T9 暴露「R4 与 R5 谁先」没写，**未定**。
2. **`skip` ≠ `allow`**：`skip` 是 XACML/ODRL 都没有的第 4 种效果；必须带 `reason`，审计单列。
3. **不要用 `clearance` 做策略条件**：它在 input 里但规则未消费；消费它需要另写规则，不是现有语义。

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

**判定单位是输出行的 subject**：列查询判列，dataset 查询判 dataset；没有 subject 的聚合查询（如只返回 `COUNT`）不在列策略覆盖内，标 gap。

**`skip` 是“未判定”，不是安全声明**：执行层可以返回、也可以 withhold。当前 trustgraph 返回（泄漏）；安全期望是**敏感 object 不出现**，不是“结果必须 0 行”。如果过滤器只按 level 去掉 `col_ssn`、留下 `col_dept`，`col_dept` 的 level 是 null，按 R3 也应 deny，所以本 fixture 的 governed 结果是 0；关键是 `col_ssn` 不能出现，0 行是 policy 的结果，不是 leak 的定义。

**两套不是一套**：10 条是 read-path 一致性用例（测实现差异），12 条是 [leak_cases.json](../example/leak_cases.json) 的泄漏面（object/alias/聚合/版本）；LEAK-T1 是后者的探针，编号不要混。12 条是**测试设计，不是可执行套件**：L4/L8/L9/L10/L11 需要额外 fixture 或开关（alias 三元组 / TriG / 版本缓存 / 缺 context / 无策略），reference §5 标了 `needs`。

**10 条一致性用例里已核的 4 条**（完整表见 [参考表 §5](../sections/reference.md)）：

| 用例 | trustgraph（`184f622`） | 安全期望 |
|---|---|---|
| subject 命中 | 删 | 删 |
| object 命中 | **不删**（只查 `triple.s`） | 删 |
| target 异常 | **fail-open**（当不命中） | fail-closed |
| 缺 `user_context` | 拒（唯一 fail-closed） | 拒 |

分析师（clearance 2）仍能发现「t_hr 有一列 col_ssn」——不是策略写错，是执行层单侧行为；修法（两侧约束/策略层/粗粒度 deny）**未测**。`skip` 与 `object_direction_failed` 并存正是本节的审计样例。

## C.4 审计（schema + 3 条样例 + replay）

```json
{"decision_id":"dec-0002","query_id":"LEAK-T1","executor":"rdflib+pyshacl","snapshot":"example/ 2026-11-10","who":"analyst:alice","action":"read","judged_subject":":t_hr","subject_kind":"table","judged_triple":[":t_hr",":hasColumn",":col_ssn"],"resource_level":null,"user_context":{"role":"analyst","clearance":2},"policy_version":"0.4.0","tag_version":"0.1.0","decision":"skip","reason":"table_subject_not_judged","execution_effect":"returned","obligation":"log","evidence":[":tag_ssn_1"],"leaked_object":":col_ssn","leaked_object_level":4,"outcome":"returned t_hr/col_ssn","leak_check":"object_direction_failed"}
```

> 完整 3 条在 [audit_records.json](../example/audit_records.json)（dec-0001 deny、dec-0002 skip/leak、dec-0003 allow）；正文只留 dec-0002。

**粒度**：审计记录是 **per-subject**（`judged_subject` 一个），query 级 summary 用下表，不塞进一条记录。dec-0001 的 outcome 是“col_ssn withheld”，不是“CQ2 0/7”；0/7 是 query log 的事。

| query | principal | raw | decision | audit | governed / outcome |
|---|---|---|---|---|---|
| CQ1 | steward | 2/2 | allow | dec-0003 | 2/2 |
| CQ1 | analyst | 2/2 | deny（逐列） | 样例未列 | 0 |
| CQ2 | steward | 7/4 | allow（逐列） | 样例未列 | 7/4 |
| CQ2 | analyst | 7/4 | deny（逐列） | dec-0001（col_ssn） | 0/7 |
| CQ3 | governance | 4 | allow（R8） | 样例未列 | 4 |
| LEAK-T1 | analyst | 3 | skip | dec-0002 | returned t_hr/col_ssn（leak） |

最小单元 = 请求 + `user_context` + 版本 + evidence + outcome + `execution_effect` + leak_check。`decision ∈ {allow,deny,skip,undetermined}`；`reason ∈ {policy_allow,policy_deny,table_subject_not_judged,default_deny,priority_gap}`；`execution_effect ∈ {returned,withheld,error}`；`leak_check ∈ {passed,object_direction_failed,aggregation_failed,alias_failed,version_mismatch,not_run}`。后三类是给 12 条用例留的位置；fixture 只填了 object 方向。

**schema 与 replay**：[audit.schema.json](../example/audit.schema.json) 定义必填字段；[audit_records.json](../example/audit_records.json) 给 3 条记录。**没有 replay，审计只是日志**。

**replay 四步**：

1. 取 `decision_id` 与记录；
2. 同版本/快照重跑同一 query；
3. 对 `decision / reason / execution_effect / outcome`；
4. 不一致记 `replay_failed`。

**但 fixture 的 snapshot 是日期标签，不是内容 hash；`tag_version`/`contract_version` 是 fixture 约定，parser 版本未记**。所以当前只能做“同 fixture 对照”，不能做严格 replay；要严格 replay，先补 hash + parser 版本（见 [A.5](./build.md) 的版本来源表）。

## C.5 输出校验与失败传播

输出校验六类 + 三态；跨段故障会换形态。

- **输出校验现在有六类**：schema / cardinality / provenance / freshness / cross-field / semantic plausibility；三态 pass/violation/undetermined，`pass` 只在 `targeted>0` 且 `skipped=0` 时给。见 [参考表 §6](../sections/reference.md)。
- **成本与 gap**：前四类低（schema/cardinality/provenance/freshness），第五类中，第六类高；目前只测了前两类。cross-field/合理性的误报未测；`0 violation` 可能只是 `targeted=0` 的空转。
- **端到端失败传播 = 矩阵 + gap**：[参考表 §7](../sections/reference.md) 给 10 类 × 3 段与四条链；[fault_matrix.json](../example/fault_matrix.json) 是注入骨架；仍无注入实验。旁证只有部分：alias 错配沿后续观察传播（无自动回滚，幅度未测，`推测`）；中间产物错误是唯一无主机制类别（分类判断，非测量）。
- Graph-Agentic 只作 signal。

## C.6 证据与边界

> 证据见 [evidence](../evidence/README.md)。

本章不证明端到端访问控制/泄漏率/replay；限定的证据见 evidence。

- 策略：T9 未定；`clearance` 未消费；R7 是 fallback。
- 执行：单实现、fail-open、只删 subject；sparql-guard/Jena 都不够第二实现；读过滤 ≠ 写授权。
- 聚合：没有 subject 的 `COUNT` 不在列策略覆盖内；CQ3 是 dataset 级查询，所以用 R8，不是“列策略自动覆盖”。
- 版本：snapshot 不是 hash；严格 replay 缺 parser 版本。

**交接**：`policy_version/tag_version` 回写 A.5；`query_id` 取自 B；`decision_id` 进 C.4 audit。

**停**：object 方向泄漏未修 / 无策略测试 / 无审计 schema → 不上线。
