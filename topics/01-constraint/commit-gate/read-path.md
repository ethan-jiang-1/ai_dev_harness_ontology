---
status: draft
updated: 2026-11-11
rq: [RQ2, RQ4]
evidence: [E-20, E-23]
---

# 读路径：策略过滤的方向性与第二实现

> `read-path` 是轴外位置（[seams](../../seams.md)）：查询结果返回前，按 `user_context` 过滤。
> 本页只问三件事：**过滤在哪个方向生效、异常路径往哪边倒、有没有第二实现。**

## 0. 三句话

- **trustgraph 只删 subject 侧**：命中 `tg-pol:blocks=true` 的节点，只删它作为 subject 的三元组；以它为 object 的三元组不删（`_triple_blocked` 只查 `triple.s`）。
- **错误路径 fail-open**：`sh:SPARQLTarget` 异常 → 当不命中；`sh:SPARQLRule` 异常 → 无判定；缺 `sh:select`/`sh:construct` → 跳过；没有策略 → 原样返回。唯一 fail-closed 是「有策略 + 请求未带 `user_context`」。**SHACL-AF 对不支持的 custom target 只写「behavior undefined」+ SHOULD warn，不要求拒绝**；所以 fail-open 是实现选择，不是标准要求（[SHACL-AF 卡](../../../src/web/w3c-shacl-af/w3c-shacl-af.card.md)）。
- **第二实现：机制有、证据不够**：sparql-guard（查询重写、fail-closed、subject+object 两侧、76 tests）在 2026-11-11 复跑 **76/76 通过**，是第二个 node-level 执行点；但单作者/1★/3 周/无独立采纳，不能当「已验证第二实现」。holosdb 是第三个执行点（扫描期、predicate/graph 级、默认拒绝），不能表达 node-level。
- **没有泄漏率**：三个执行点都只有 case-level tests，没有同一套 10 用例的泄漏/误拦率；见 §7 EXP-001。

依据：E-20 / E-23；[commit-gate F5–F7](./findings.md)；[trustgraph digest](../../../src/open-source/trustgraph-ai-trustgraph/digest.md) §3–§6。

## 1. 十条一致性用例

> `期望` 是「安全的读路径」应该做的；`trustgraph` 是 pin `184f622` 的代码行为；`sparql-guard` 未跑，全 `?`。

| # | 用例 | 期望 | trustgraph（`184f622`） | sparql-guard |
|---|---|---|---|---|
| 1 | subject 命中 | 删除该节点作为 subject 的三元组 | **拦**（`PF._triple_blocked` 查 `triple.s`，此处恰好覆盖） | ? |
| 2 | object 命中 | 删除指向该节点的三元组 | **漏**（object 不删；`?col` 全表探针 3 行，单 object 探针 1 行） | ?（文档称默认隐藏 object） |
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

## 3. 第二实现评估：三个执行点，不是一个机制

| 执行点 | 代表 | 粒度 | 方向 | 异常 | 测试 | 成熟度 | 能不能当第二实现 |
|---|---|---|---|---|---|---|---|
| 查询结果后过滤（post-filter） | trustgraph `184f622` | node（subject 侧） | 只删 subject | fail-open | 31 条单测；无 object/异常注入 | 2,902★，30 贡献者 | **第一实现**；单实现限定仍成立 |
| 查询重写（rewrite） | sparql-guard `6b68d76` | node + graph（SHACL 行级） | subject+object（含 triple term） | fail-closed；不能安全重写就拒 | **76/76 通过**（EXP-001，2026-11-11） | 1★，2026-10-10 建，单组织 | **机制合格、成熟度不够** → 候选 |
| 扫描期过滤（scan） | holosdb `666238f` | predicate + graph | 方向无关（按谓词/图） | 默认 deny；编译错误传播 | **20/20 通过**（EXP-006） | 1★，2026-08 建，单作者 | **第三执行点**；不能表达 node-level → 不是替代 |

**判定**：

- **没有「已验证的第二实现」**：sparql-guard 机制合格、测试复跑通过，但单作者/1★/3 周/无独立采纳/无泄漏率；holosdb 是另一个执行点，粒度不同，不能替代 node-level post-filter。
- **E-23 的「单实现」限定只指 trustgraph 的 SHACL-AF post-filter**；不要读成「read-path 只有一个实现」。
- **共同缺口是评测，不是实现**：三者都只有 case-level tests，没有同一套 10 用例的泄漏/误拦率。

依据：E-20 / E-23；[EXP-001 §7](#7-exp-001三个执行点的代码测试复核2026-11-11)；[commit-gate frontier](./frontier.md)。

## 4. 10 用例 × 3 执行点（按代码/测试读取，未跑同一协议）

| # | 用例 | trustgraph（post-filter） | sparql-guard（rewrite） | holosdb（scan） |
|---|---|---|---|---|
| 1 | subject 命中 | 拦 | 拦（EXP-002） | **不适用**（无 Subject scope） |
| 2 | object 命中 | **漏** | 拦（EXP-002） | **不适用** |
| 3 | 两侧都命中 | 半 | 拦（EXP-002） | **不适用** |
| 4 | 都不命中 | 放行 | 放行（EXP-002） | 放行 |
| 5 | target 异常 | **漏**（fail-open） | 拒（EXP-002：不支持的 shape 加载期抛错） | 编译错误传播；无 target 概念 |
| 6 | 缺 context | 拒 | 匿名视图（EXP-002：仅 public） | 拒（anonymous + default deny，除非策略允许） |
| 7 | alias | **漏** | **漏（policy gap；EXP-002）** | 不适用（无 alias 概念） |
| 8 | 聚合 | 空/不适用（三元组流） | 拦（EXP-002：COUNT=2 / salary=0） | 可（scan 后 COUNT；统计/推理是 caveat） |
| 9 | 无策略 | **漏**（passthrough） | 拒（EXP-002：空 policy 抛错） | 拒（default deny） |
| 10 | 版本 | **漏**（60s 缓存不带版本） | 部分（新 PolicySet 生效；热更新未测） | ?（按字典增长重编译，不按 policy version） |

**读法**：

- **trustgraph 的 10 格里 5 格漏（2/5/7/9/10）+ 1 格半（3）**，原因是 post-filter + fail-open + 无版本；这是已核代码，不是测评。
- **sparql-guard 的 10 用例实跑：7 pass + 1 fail-closed + 1 defined anonymous + 1 leak（alias）+ 1 partial（version）**；0 false-block。它的 76/76 是全量测试，10 用例是另一套协议。
- **holosdb 有 4 格「不适用」**（1/2/3/7）：它没有 Subject/Object scope，只能按 predicate/graph 隐藏；这不是 bug，是粒度不同。
- **没有一种执行点覆盖全部 10 格**；覆盖表不是泄漏率——没有分母、没有标签、没有跨实现同一协议。

> 填表纪律：一格一观察带锚；未跑写 `?`；每格同时记 `decision` 与 `unavailable`（blocked ≠ denied）；合法/禁止成对记（借 `AuthorizationPairs` 的 80/80）。**EXP-001（§7）只做了代码/测试读取；同一协议复跑是 EXP-002。**

## 5. 最小可移植策略

```json
{
  "policy_version": "0.4.0",
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
- **执行点 ≠ 一个机制**：post-filter / rewrite / scan 的粒度、方向和错误路径不同；引用「read-path」时必须写清是哪一种。


## 7. EXP-001：三个执行点的代码/测试复核（2026-11-11）

> 仓库外验证：只读代码 + 复跑测试；**工程产物，不入 E**。代码在 `/tmp/exp-001/`（不 vendor、不进仓库，机器重启即失；pin commit 在文中）。

### 7.1 做了什么

| 项 | 命令 / 路径 | 结果 |
|---|---|---|
| sparql-guard 测试 | clone `6b68d769ccbf76a2544be9d80006a279ae8f3fa7`；`npm ci`；`npx vitest run` | **76/76 passed**（6 files，1.36s） |
| holosdb 测试 | clone `666238f24adc8d65538f262e8731a8a45ed8bd3c`；aarch64 toolchain + arm64 clang wrapper；`cargo test -p holos-security --target aarch64-apple-darwin` | **20/20 通过**（EXP-006）。x86_64 主机经 Rosetta 调 arm64 linker 的坑已绕过：`arch -arm64 /usr/bin/clang` wrapper |
| trustgraph | 不重跑；沿用 2026-11-09 在 pin `184f622` 的只读代码核对（31 条单测） | 只读；无 object / 异常注入 |

### 7.2 读到了什么

- **sparql-guard**：76 条里有 12 条直接针对泄漏/绕过——`hides references to hidden resources`、`cannot be bypassed through FILTER EXISTS / MINUS or aggregates / sub-queries`、`does not leak through DESCRIBE / CONSTRUCT`、`refuses property paths over a hidden property`、`refuses SERVICE / updates`、`hides triple terms … as plain objects`。
- **holosdb**：`Scope` 只有 `Everything / Graph / Predicate / GraphPredicate`，**没有 Subject/Object**；`holos-engine/src/view.rs:247` 对每个 quad 调 `decide_quad`，所以方向无关，但只能按谓词/图 hide，不能按实体 hide。
- **两边都自称安全，且互相拆台**：holosdb 的 `policy.rs` 说「rewrite 是 leak generator，总有一个 operator 被忘掉」；sparql-guard 的 README 说「rewrite, not result filtering；MINUS/聚合/子查询都在受限视图上算」。**这是设计之争，不是已裁决的事实。**

### 7.3 没证明什么

- **没有泄漏率/误拦率**：76/76 是「作者写的用例通过」，不是独立评测；没有标签、没有负例集、没有跨实现同一协议。
- **没有 harness 集成**：sparql-guard 是 SPARQL 代理，holosdb 是 DB 引擎；都不是 agent harness 里的调用点。
- **没有生产/规模**：1★ / 单作者 / 3 周，不能外推。
- **一篇相关论文未纳入**：SEMANTiCS 2024 的 SHACL 数据泄漏/校验绕过论文（Dao & Debruyne）检索到，但 PDF 不可达；未读、未引，留给下一轮。

### 7.4 结论

**第二实现「有机制、没证据」。** 下一步不是再找一个引擎，而是把 §1 的 10 条用例做成共同协议，在三个执行点上各跑一遍，报泄漏率/误拦率。**EXP-002 的第一列（sparql-guard）已跑，见 §8；holosdb 的 20 条单测也已复跑通过（EXP-006），但 10 用例仍是复刻（无 node-level）；trustgraph 仍是复刻，不是产品测量。**

### 7.5 EXP-002 协议（下一步，不在本轮）

- **固定 fixture**：8–12 个 triple；1 个敏感谓词（如 `salary`）、1 个敏感节点（如 `alice`）、1 个别名、1 个聚合查询。
- **同一策略语义**：node-deny + predicate-deny + fail-closed；三个执行点各自实现，不改语义。
- **10 用例**：按 §1；每格记 `leak / false-block / undecidable / pass`，并给代码/查询锚。
- **指标**：leak（敏感 triple 出现在结果）、false-block（合法 triple 被删）、undecidable（实现无法表达）；**分母是 10，不是请求量**。
- **通过线**：5 个安全关键用例（1/2/3/5/8）0 leak；false-block 报数不设线；undecidable 单列。
- **标签**：独立人/规则给，不用被测实现自证；每格附查询与期望。


## 8. EXP-002：10 用例在 sparql-guard 上的实跑（2026-11-11）

> 仓库外：`test/exp002.test.ts`；`npx vitest run test/exp002.test.ts` → **10/10 tests pass**；结果 JSON `/tmp/exp-001/exp002-sparql-guard.json`。**工程产物，不入 E。**

| # | 用例 | 结果 | 观察 |
|---|---|---|---|
| 1 | subject | pass | bob 作为 subject 0 行 |
| 2 | object | pass | bob 作为 object 0 行；`ASK` false |
| 3 | both | pass | 两侧 0 行 |
| 4 | neither | pass | alice name = Alice（0 false-block） |
| 5 | exception | pass (fail-closed) | 不支持的 shape 在加载期抛错 |
| 6 | missing context | defined anonymous | 只见 ACME（public），无 HR |
| 7 | alias | **leak (policy gap)** | 未类型化的 alias `ex:a1 ex:name "Bob"`（Bob 被隐藏）仍返回 Bob |
| 8 | aggregate | pass | `COUNT` worksFor acme = 2；`COUNT` salary = 0 |
| 9 | no policy | pass (fail-closed) | 空 policy 抛错，不 passthrough |
| 10 | version | partial | 新 PolicySet 生效；热更新/版本号未测 |

### 8.1 三执行点汇总

| 执行点 | 跑了吗 | leak | false-block | undecidable / partial |
|---|---|---|---|---|
| sparql-guard | **实跑 10/10** | 1（alias） | 0 | 1 partial（version） |
| trustgraph | 复刻（未跑产品） | 5 + 1 conditional + 1 partial | 0（复刻） | 0 |
| holosdb | 复刻（未跑产品） | 1（alias） | 0（复刻） | 4 undecidable |

> **复刻脚本**：`/tmp/exp-001/exp002-replicas.mjs`；按 trustgraph `_triple_blocked`（只查 `triple.s`、fail-open）与 holosdb `Scope`（predicate/graph、默认 deny）的语义写。**不是产品测量**；数字是 10 用例计数，不是率。聚合那格标 conditional：trustgraph 的接口是三元组流，COUNT 是否经过过滤器未定。

> **不要把这张表读成「sparql-guard 最好」。** 三者粒度不同：holosdb 的 4 个「undecidable」是它根本不表达 node-level，不是它更安全；trustgraph 的 5 个 leak 是 post-filter 的已知边界，不是新发现。**唯一新的实测结果是 alias leak**（sparql-guard 的 shape 不覆盖未类型化 alias；两个复刻也会漏）。

**结论**：

- **7 pass + 1 fail-closed + 1 defined anonymous + 1 leak + 1 partial，0 false-block**。
- 唯一 leak 是 **alias**：shape 按 `ex:Employee` 过滤，未类型化的 alias（指向被隐藏的 Bob）不在 shape 覆盖内。这不是 rewrite 的 bug，是**策略建模**的边界；EXP-003 显示前置能修 node-level，不修 predicate-level。
- **没有 rate**：分母是 10 个用例，不是请求量；没有误拦率、没有时延、没有跨实现同一协议。
- **trustgraph / holosdb 没跑同一协议**：trustgraph 的 Python 依赖装不上（pip index 无 pydantic/rdflib）；holosdb 的 rustc 目标架构不匹配（x86_64 主机 + arm64 linker）。两列仍是**代码级映射**，不是实跑；这是 EXP-002 的明确边界。

## 9. EXP-003：alias 前置（复刻，2026-11-11）

> 仓库外 `exp003-alias.mjs`；fixture：bob 隐藏，`a1` 是 bob 的未类型化 alias；前置把 `a1 → bob`。**工程产物，不是产品测量。**

| 执行点 | 无前置 | 有前置 | 说明 |
|---|---|---|---|
| post-filter（trustgraph） | leak | pass | 按 canonical subject 删 |
| scan（holosdb） | leak | **leak** | 粒度是谓词，不能 hide node |
| rewrite（node-level） | leak | pass | 前置 + node 过滤 |
| false-block（alice） | pass | pass | 前置不误伤可见实体 |

**结论**：

- **alias 前置是必要条件，不是充分条件**：它修 node-level（post-filter / rewrite），不修 predicate-level（scan）。
- 规则要写三层：①**解析**以获得完整候选集；②**授权按 alias 逐个判**，身份合并不自动扩权；③执行点必须能表达 node-level deny。只做①，scan 仍漏；只做③不做①，node-level 也漏。
- **规范只支持一半**：已断言的 `sameAs` 在 OWL 2 RL/DL 下必须展开（W3C OWL 2 Profiles 的 `eq-rep-s/p/o`）；未断言时 RDF 1.1 §2 不允许推定同一。**「解析必须先于过滤」没有标准/论文直接规定**，只有 GraphDB/Virtuoso/RDF4J 的工程证据（关掉 sameAs 结果变小、opt-in 易漏、默认无 reasoner）。
- **反向风险**：解析本身是一次身份合并，可能把两个主体的数据并到一起，造成过度暴露；所以「先解析」不能无条件写成安全规则——解析保匹配完整性，授权仍按 alias 逐个判，合并动作单独授权。

**EXP-005（2026-11-11，真实 sparql-guard）**：在真实实现上跑 alias 前置 3 用例——无前置 `ex:a1 ex:name "Bob"` 返回 Bob（leak）；前置把 `a1→bob` 后，`?s ex:name` 不再返回 Bob（pass）；alice 仍可见（false-block 0）。3/3 tests pass。**这是「前置 + 代理」的产品级组合测试，不是代理自身的功能**；它证明前置在真实 rewrite 上有效，但不证明 trustgraph/holosdb。

## 10. 外部依据（alias）

- [W3C OWL 2 Profiles 卡](../../../src/web/w3c-owl2-profiles/w3c-owl2-profiles.card.md)：`eq-rep-s/p/o` / `SameIndividual` / RDF 1.1 §2；条件性（只在声明 RL/DL 蕴含时成立）。
- 对照：Kirrane 等 2017（Semantic Web 8(2)）把 sameAs 放进访问控制传播；关键句为转述，二手；GraphDB/Stardog/Virtuoso/RDF4J 文档只作工程证据，不是规范。
- 本页只用它说明「规则能写到什么程度」，不用它升 E。

- [Kirrane 2020 卡](../../../src/web/kirrane-2020-qbac/kirrane-2020-qbac.card.md)：把「查询重写」与「结果过滤」放在同一策略下用 secure/sound/maximum 对照；FILTER 式重写在否定/子查询/聚合下不正确；倾向「像未授权数据不存在」的 fail-closed 语义。**这是 §4 矩阵里「聚合/否定」两格的外部形式化依据**，但仍不是 RDF 上的泄漏率。
