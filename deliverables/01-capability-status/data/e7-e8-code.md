---
status: draft
updated: 2026-11-11
type: evidence-note
target: X7 read-path / X8 commit gate
---

# X7/X8 代码核对：执行 ≠ 健全 ≠ 授权

> **工作底稿，不是交付正文。** 用于更新 D1 的 X7/X8 verdict；正式引用走 E-20 与 [execution-forms](../../../topics/execution-forms.md#代码级核对2026-11-09)、[01/commit-gate](../../../topics/01-constraint/commit-gate/README.md)。数字/行为来自 4 个开源项目的 pin commit 只读代码核对；本轮**没有重新跑代码**。

## 1. X7 读路径

### trustgraph（`184f622`，`read-path`）

| 项 | 事实 | 含义 |
|---|---|---|
| 策略 | `policy/policy_filter.py` 从 `urn:graph:policy` 加载 SHACL-AF NodeShape | 有外部判据 |
| 求值 | `sh:SPARQLTarget`（SELECT）+ `sh:SPARQLRule`（CONSTRUCT）+ `sh:order` | 真执行，不是 prompt |
| 阻断 | 命中 `tg-pol:blocks=true` 的节点，剔除其作为 **subject** 的三元组 | **只删 subject 侧**；object 方向不删 |
| 异常 | target 抛异常 → 当作不命中；rule 抛异常 → 无判定；缺 `sh:select`/`sh:construct` → 跳过 | **fail-open** |
| 位置 | 查询结果返回前，介于图存储与 agent 上下文之间 | 是 `read-path`，不是六时刻 |
| 测试 | 31 条单测存在；跨项目核对时跑过 | 代码按预期跑；不等于机制有效 |
| 未验证 | object 方向、异常策略的实际泄漏、生产误拦/吞吐 | 需要第二个实现/异常用例 |

### 其他项目

- **semantica**（`39cf721`，`checker`）：`OntologyEngine.to_shacl` 派生 SHACL；`validate_graph` 调 pyshacl，`inference="none"`；CLI 校验。**不是 in-loop**；派生 shapes 的质量未测。
- **open-ontologies**（`375fbc4`，工具面/CI）：默认 `ShaclValidator` 把 SHACL 编译成 SPARQL 交 Oxigraph；`--verified` 走 `oo-shacl` 0/2/3（3=undetermined）；外层 `gate_exit_code` 把 `conforms:null` 映射为 exit 2。**JSON 保留第三态，shell 退出码不保留**。
- **ontop**（`964dbb7`，`supply`）：TBox 饱和 + 查询重写 → SQL；不是闸。

### X7 verdict

| 子句 | verdict | 依据 | 边界 |
|---|---|---|---|
| 读路径过滤有实现 | `supported（限定）` | trustgraph 代码级；31 条单测 | 单实现；best-effort |
| object 方向不泄漏 | **`unknown`** | 代码只删 subject；未构造对象用例 | 需要第二个实现/异常用例 |
| 可当写授权 | `contradicted` | trustgraph 是读路径；open-ontologies 只做 CI/报告 | 不是 commit gate |
| 可升第七时刻 | **`unknown`** | 只有 1 个独立实现 | 第二个实现才决定 |

## 2. X8 写路径

| 项目 | 能做写入授权吗 | 事实 |
|---|---|---|
| trustgraph | 否 | 读路径策略过滤；不是单次写/落盘授权 |
| semantica | 否 | CLI 校验；不在 agent loop 内 |
| open-ontologies | 否 | `enforce` 是 CI 规则门；`closure_diff` 报影响面，不签授权 |
| ontop | 否 | 查询重写；不是 gate |

**结论**：四个项目里**没有一个是单次写授权/commit gate**。Commit Boundary 是概念架构；false-defer 未测。

### X8 verdict

| 子句 | verdict | 依据 | 边界 |
|---|---|---|---|
| 写路径有实现 | **`unknown`/无** | E-20 否定证据 | 需要实现 + false-defer |
| 可做设计 | `supported（概念）` | Commit Boundary 契约 | 不是已落地机制 |
| 部署有效 | **`unknown`** | 无实现、无数据 | 不要声称 |

## 3. 还缺什么

- **X7**：第二个独立 read-path 实现；object 方向泄漏测试；异常策略的 fail-open 验证；生产误拦/吞吐。
- **X8**：单次写授权实现；一个 mutation class 的 false-defer 样本（20–50 条）；审计存储/事务/scope-version 检查。
- **共同**：执行 ≠ 健全 ≠ 授权；三态在接口层会被折叠；不要用「有引擎」代替「会拦/有授权」。

## 4. 什么会改变它

- 第二个 SHACL/策略过滤实现，且能测 object 方向 → X7 可升第七时刻/更强 verdict。
- 任何 commit gate 实现 + false-defer → X8 可从 `C 只能设计` 升级。
- 异常/对象用例跑出泄漏 → X7 的 `supported（限定）` 要收窄。
