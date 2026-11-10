---
status: draft
updated: 2026-11-10
rq: [RQ2, RQ4]
evidence: [E-20, E-23]
---

# 读路径：策略过滤的方向性与第二实现

> `read-path` 是轴外位置（[seams](../../seams.md)）：查询结果返回前，按 `user_context` 过滤。
> 本页只问三件事：**过滤在哪个方向生效、异常路径往哪边倒、有没有第二实现。**

## 0. 三句话

- **trustgraph 只删 subject 侧**：命中 `tg-pol:blocks=true` 的节点，只删它作为 subject 的三元组；以它为 object 的三元组不删（`_triple_blocked` 只查 `triple.s`）。
- **错误路径 fail-open**：`sh:SPARQLTarget` 异常 → 当不命中；`sh:SPARQLRule` 异常 → 无判定；缺 `sh:select`/`sh:construct` → 跳过；没有策略 → 原样返回。唯一 fail-closed 是「有策略 + 请求未带 `user_context`」。
- **没有合格第二实现**：sparql-guard 方向相反（查询重写、fail-closed），但单作者/1★/3 周龄/无 harness 调用点，不够入库；Jena `jena-permissions` 已退役；Fuseki 的 ACL 是端点级，不是三元组级。

依据：E-20 / E-23；[commit-gate F5–F7](./findings.md)；[trustgraph digest](../../../src/open-source/trustgraph-ai-trustgraph/digest.md) §3–§6。

## 1. 十条一致性用例

> `期望` 是「安全的读路径」应该做的；`trustgraph` 是 pin `184f622` 的代码行为；`sparql-guard` 未跑，全 `?`。

| # | 用例 | 期望 | trustgraph（`184f622`） | sparql-guard |
|---|---|---|---|---|
| 1 | subject 命中 | 删除该节点作为 subject 的三元组 | **拦**（`PF._triple_blocked` 查 `triple.s`，此处恰好覆盖） | ? |
| 2 | object 命中 | 删除指向该节点的三元组 | **漏**（object 不删，返回 1 行） | ?（文档称默认隐藏 object） |
| 3 | 两侧都命中 | 两侧都删 | **半**（subject 删、object 留） | ? |
| 4 | 都不命中 | 原样返回 | **拦/放行**（无命中不删，`svc._filtered_query` 原批回送） | ? |
| 5 | target 抛异常 | fail-closed | **漏**（当不命中，策略不适用） | ?（加载期编译失败则拒绝启动） |
| 6 | 缺 `user_context` | 拒绝 | **拒**（`svc._needs_policy` → `policy-enforcement-error`） | ? |
| 7 | alias | 按同一实体过滤 | **漏**（target 不命中即跳过；无 default deny） | ? |
| 8 | 聚合（COUNT） | 不返回可反推的计数 | **空/不适用**（入口是三元组流，聚合不在接口内） | ? |
| 9 | 无策略 | 默认 deny 或显式 open mode | **漏**（`_needs_policy` 计 0 → `_passthrough`） | ? |
| 10 | 策略版本不匹配 | 拒绝/回退 | **漏**（60s 缓存，key 不含 policy version；判定记录无 `policy_version`） | ? |

**读法**：1/4 正常、2/3 是方向性、5/9/10 是错误路径与版本、6 是唯一 fail-closed、7/8 是判定单位盲区。只看第 1 条会得出相反结论。

## 2. 代码锚与失败路径

| 行为 | 代码锚 | 含义 |
|---|---|---|
| 只删 subject | `policy/policy_filter.py` 的 `_triple_blocked`（只读 `triple.s`） | object 方向泄漏；「节点 blocked ≠ 三元组不可见」 |
| target 异常 fail-open | `_run_sparql_target` 捕获异常 → 不命中 | 策略求值失败时放行 |
| rule 异常 fail-open | `_run_sparql_rule` 捕获异常 → 无判定 | 同上 |
| 缺 select/construct | 跳过该策略 | 策略写错不报错 |
| 无策略 | `PolicyFilter.apply` / `svc._passthrough` | open mode |
| 缺 user_context | `svc._needs_policy` → `policy-enforcement-error` | 唯一 fail-closed |
| 版本/缓存 | `NodeDeterminationCache` 30/64 条/60s；key 含 user context 哈希，不含 policy version | 旧判定可续用 ≤60s |

**限定（六条）**：只覆盖 triples-policy flow（可选组件，默认部署是否启用未定位）；只对非空策略图；判定单位是节点 IRI，不是 triple；`sh:order` 首命中即停；缓存 30/64/60s 且不含策略版本；31 条单测无异常注入、无 object 方向、无聚合。

**结论**：trustgraph 选了「可用性优先」；引用它做安全论证时，必须写清错误路径与方向性，不能写「读路径可授权」。这些是「错误路径的选择」（`已核`），不是「发生率」（`已证` = 0）。

依据：[trustgraph digest](../../../src/open-source/trustgraph-ai-trustgraph/digest.md) §3/§6；[commit-gate F6](./findings.md)、[F7](./findings.md)。

## 3. 第二实现评估

| 候选 | 是什么 | 够不够入库 | 缺什么 |
|---|---|---|---|
| `Matdata-eu/sparql-guard` | TS 查询重写；fail-closed；object 默认隐藏；Vitest 用例 | **不够** | 单作者 / 1★ / 3 周龄 / 无 harness 调用点 / 无泄漏率；76 用例是外部复核，未复跑 |
| Apache Jena `jena-permissions` | SecurityEvaluator + 动态代理；Graph/Model CRUD，可选 triple 粒度 | **已退役** | Jena 5.6.0 最后版本；commit `3d4d5332`「Retire jena-permissions」；只能作历史对照 |
| Apache Fuseki | Shiro `shiro.ini` 的 `[urls]` ACL | **不是读路径** | 粒度是端点/URL/角色，不是三元组级 |
| `pwin/triplestore`（holosdb） | Rust；`crates/holos-security/` | **候选** | 未读代码；1★；需 pin commit + 调用点 |
| OPA | 通用策略引擎 | **adjunct** | 不解析 RDF/SHACL；只返回 decision |

**判定**：没有合格第二实现 → `C3` 只能写单实现 + 风险；不要把 sparql-guard 写成「已有第二实现」。它的价值是证伪「read-path 只有一种执行点」（post-filter vs query rewrite），不是补上实现。

依据：E-20；[commit-gate frontier](./frontier.md)；[02 R8](../../../deliverables/02-engineering-playbook/recipes/readiness.md)。

## 4. 10×2 结果矩阵（骨架）

| 用例 | trustgraph | 第二实现 | 差异 | 结论 |
|---|---|---|---|---|
| 1 subject | 拦 | ? | 空 | 空 |
| 2 object | 漏 | ? | 空 | 空 |
| 3 both | 半 | ? | 空 | 空 |
| 4 neither | 放行 | ? | 空 | 空 |
| 5 target 异常 | 漏 | ? | 空 | 空 |
| 6 缺 context | 拒 | ? | 空 | 空 |
| 7 alias | 漏 | ? | 空 | 空 |
| 8 聚合 | 空/不适用 | ? | 空 | 空 |
| 9 无策略 | open mode | ? | 空 | 空 |
| 10 版本 | 漏（60s） | ? | 空 | 空 |

> 填表纪律：一格一观察带锚；未跑写 `?`；每格同时记 `decision` 与 `unavailable`（blocked ≠ denied）；合法/禁止成对记（借 `AuthorizationPairs` 的 80/80）。

## 5. 最小可移植策略

```json
{
  "policy_version": "0.3.0",
  "rule_id": "R_read_column_level",
  "principal": {"kind": "role", "id": "analyst", "aliases": []},
  "action": "read",
  "resource": {"kind": "node", "iri": ":col_ssn", "level": 4},
  "condition": {"clearance_gte_level": true, "owner_eq_principal": false, "graph_in_granted": true},
  "effect": "deny",
  "obligation": "log_decision"
}
```

**方向无关**：`resource.kind = node|triple|graph`，subject/object 同判；`skip` 必须带 `reason`，无命中 = deny。

**三条测试**：

1. **方向不变式**：同一资源在 subject/object 两侧都 0 行；含 `FILTER EXISTS` / `COUNT` 的查询也要 0。
2. **fail-closed**：target 异常 / 缺 `user_context` / `level` 空 → deny 或显式 `unavailable`，永不 allow；审计留 `reason`。
3. **版本与 alias**：v1→v2 立即生效；未解析 alias 不得命中 owner 规则。

三测跑双实现差分；参考标签由独立引擎给，不用被测实现自证（`推测`）。

## 6. 边界

- **有实现 ≠ 安全**：31 条单测只证「按预期跑」；sparql-guard 自述限制含时序侧信道、store 错误回传、依赖 store 忠实实现 `FROM`。
- **读过滤 ≠ 写授权**：本页只覆盖读路径；写路径 commit gate 仍无实现（[commit-gate F4/F5](./findings.md)）。
- **单实现 ≠ 通用**：Jena 退役反证「标准栈也不一定长期维护读路径」；不能把 trustgraph 外推。
- **机制 ≠ 策略正确**：策略层无领域来源（[access-control F3](../access-control/findings.md)）。
- **用例 ≠ 评测**：没有 false-denial 率、effect、请求级配对；T1 只是单例。
- **接缝 ≠ 落地**：没有 harness 调用点；默认部署是否启用 triples-policy 未定位。
