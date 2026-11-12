# 持久化前 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `commit-gate/Fx`。

## 索引
> **2026-11-12 对账（等级以 README 为准）**：本页索引里的「已核」是**撤源前**的记录；支撑它的来源已按 [CHARTER §4](../../../CHARTER.md#4-素材准入material-gate) 移出，这些条目现等级见 [README](./README.md)（多已降 `推测`/`withdrawn`）。**引用请用 README 的等级，不要用本页索引的历史等级。**


| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 推理证据 ≠ 授权证据；`UNVERIFIED` 不能当 positive support | 已核（概念） |
| F2 | 提交条件应显式化：证据齐/冲突清/版本有效；批准不跨 mutation 继承 | 已核（设计规范） |
| F3 | 同源检索不是独立确认；「没冲突」不是 positive support | 已核（概念） |
| F4 | 只有设计，没有实现；保证是条件性的 | 已核（概念） |
| F5 | 授权有读路径实现（策略过滤），写路径 commit gate 仍无 | 已核（代码） |
| F6 | 读路径策略执行是 fail-open：SPARQL 异常/缺字段即放行 | 已核（代码） |
| F7 | 读路径过滤只删 subject 侧三元组，object 方向可能泄漏 | 已核（代码） |

> `F` 只放判断；接口/字段/成本/stop/替代方案的工程口径放在 [mechanism](./mechanism.md) 的「工程发现 1–4」，不新增 `F` 编号。

## 怎么读

- 想看机制：去 [mechanism.md](./mechanism.md)。
- 想看接口/字段/成本/stop/替代方案的工程口径：去 [mechanism](./mechanism.md) 的「工程发现 1–4」。
- 想看缺什么/下一步：去 [frontier.md](./frontier.md)。

## F1 · 推理 ≠ 授权

- **判断**：能支持假设，不等于有权推动持久化变更；`UNVERIFIED` 可进 Planner，但不能当授权证据。
- **条件**：Commit Boundary 概念架构；无实现。
- **边界**：不是实证效果；只是状态语义。
- **来源**：Commit Boundary §3–5；digest §3。

## F2 · 三条件

- **判断**：证据齐、冲突清、版本有效，三条全过才 commit（实现上前两条聚合成 `PASS`，再验 scope/version）；不满足时 defer，不丢弃证据。
- **含义**：把「冲突已解决」「版本仍有效」写进提交条件，不留给模型自觉；`P_auth` 只对声明的命题/角色/观察域/policy version 有效，不跨 mutation 继承。
- **边界**：冲突清 vs 冲突已标注的降级条件未定。
- **来源**：§4–5；digest §3.1/§3.3/§6.5。

## F3 · 同源不确认

- **判断**：hypothesis 诱导的多个结果不能互相印证；同源 query/hypothesis/source 不算 corroboration；「没检测到冲突」也不是 positive support。
- **含义**：这是 agentic ER 的一类失败模式；dependency-aware lineage 仍是上游漏洞。
- **来源**：§5.3；digest §5。

## F4 · 只有设计

- **判断**：Commit Boundary 自述无实现、无实证；保证是条件性的——依赖域策略充分、promotion 可靠、强制执行等 7 条假设。
- **含义**：只能作设计提案引用，不能作效果证据；false-defer 率未知。
- **来源**：摘要/§8；digest §5。

## F5 · 读路径有实现，写路径没有

- **判断**：开源系统里已有「用户上下文 + SHACL-AF 策略」的**读路径**授权过滤（trustgraph `policy/policy_filter.py`）；但它拦的是检索结果，不是落盘变更。Commit Boundary 的**写路径** commit gate 仍无实现。
- **等级**：已核（代码；31 条单测已跑）。
- **条件**：策略存在才强制（无策略 → open mode）；错误路径 fail-open，未测；只删 subject 侧三元组。
- **含义**：F4 的「只有设计」对 commit gate 仍成立，但不能外推成「授权不可执行」——授权执行在开源里先落在读侧。引用时写清「读路径 vs 写路径」。
- **来源**：trustgraph digest §3–§4；`policy/triples/service.py`、`policy/policy_filter.py`。

## F6 · 读路径策略执行是 fail-open

- **判断**：trustgraph 的策略求值器在错误路径上放行：`sh:SPARQLTarget` 抛异常 → 当作不命中；`sh:SPARQLRule` 抛异常 → 无判定；策略缺 `sh:select`/`sh:construct` → 跳过该策略；没有任何策略 → 原样返回。只有「有策略 + 请求未带 user_context」是 fail-closed。
- **等级**：已核（代码；`policy_filter.py: _run_sparql_target/_run_sparql_rule`、`PolicyFilter.apply`）。
- **含义**：授权执行器的错误路径决定它是「安全默认」还是「可用性优先」。读路径实现选了可用性；引用它做安全论证时必须写清，且需要异常注入测试（当前没有）。
- **来源**：[trustgraph digest](../../../src/open-source/trustgraph-ai-trustgraph/digest.md) §3/§6；2026-11-09 在 pin `184f622` 上核对 `policy_filter.py`。

## F7 · 读路径过滤只删 subject 侧

- **判断**：命中 `tg-pol:blocks=true` 的节点，只会删掉它作为 **subject** 的三元组；以它为 **object** 的三元组不删（`_triple_blocked` 只检查 `triple.s`）。
- **等级**：已核（代码）。
- **含义**：敏感信息可能以「别人 → 指向 → 敏感节点」的方向返回。授权过滤的方向性与主体/客体语义绑定，不能假设「节点被 block = 完全不可见」。
- **来源**：[trustgraph digest](../../../src/open-source/trustgraph-ai-trustgraph/digest.md) §3/§6。


## F8 · 读路径有三个执行点，不是一个机制

- **判断**：read-path 至少有三种执行点：post-filter（trustgraph，node/subject，fail-open）、rewrite（sparql-guard，node+graph，fail-closed）、scan（holosdb，predicate+graph，默认 deny）。三者的粒度、方向和错误路径不同，不能互替。
- **等级**：已核（代码）；sparql-guard **76/76 tests 复跑通过**（EXP-001，2026-11-11）；holosdb **20/20 tests 复跑通过**（EXP-006，2026-11-11；用 aarch64 toolchain + arm64 clang wrapper）。
- **条件**：sparql-guard 1★/3 周/单组织；holosdb 1★/单作者；两者都无 harness 调用点、无泄漏率。
- **含义**：E-23 的「单实现」限定只指 SHACL-AF post-filter；不要把它读成「read-path 只有一个实现」。共同缺口是评测协议，不是再找引擎。
- **来源**：[read-path §3/§7](./read-path.md)；EXP-001。
- **EXP-002（2026-11-11）**：sparql-guard 10 用例实跑 **7 pass + 1 fail-closed + 1 defined anonymous + 1 alias leak + 1 partial，0 false-block**；trustgraph / holosdb 未跑产品，用代码忠实复刻（`exp002-replicas.mjs`）：trustgraph 5 leak + 1 conditional + 1 partial；holosdb 1 alias leak + 4 undecidable。alias leak 是策略建模边界，不是 rewrite bug。
