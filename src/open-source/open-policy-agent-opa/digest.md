---
status: draft
updated: 2026-11-09
quality: B
based_on: card.md
commit: 3dc83ae32b43eb1a649ce0c5e6745fc7a4f3d146
claims: []
---

# open-policy-agent/opa：把“策略层”做成可部署的决策点

> **自包含**：不假设读者读过 README、card。代码位置写到 `文件:符号`，不贴大段代码。
> `已核` = 读过代码、能指到文件/函数；`推测` = 只读 README/文档。

## 0. 三句话

1. **它是什么**：CNCF graduated 的通用策略引擎；Rego 写 allow/deny；服务通过 REST/Go SDK 查询 decision；有 bundle 分发、decision logs、discovery。
2. **本体怎么被用**：**没有**。OPA 不解析 OWL/SHACL/RDF，不做 entailment/查询重写；策略的输入是 JSON（可以把 Glyph 的标签作为 data/input 喂进去），但 label→policy 的映射要自己写。
3. **证据到哪**：读到调用链（`cmd/run.go` → `server/server.go` → `rego/rego.go` → `topdown/topdown.go`）；未跑 OPA、未做延迟/冲突测试。`quality: B`。

## 1. 项目与维护状态

- **定位**：general-purpose policy engine；不是 KG/本体项目，是**策略层 adjunct**。
- **维护**：CNCF graduated；`ADOPTERS.md` 列生产采用；12,452★；最后 push 2026-11-09；commit `3dc83ae`；Apache-2.0。
- **能力面**：Rego 语言、AST/编译器、topdown 求值、REST decision API、Go SDK、bundle/discovery、decision logs、WASM 目标。
- **不把它当**：本体引擎、SHACL 校验器、KG 查询过滤器。它只回答“这个 input 下 allow/deny 是什么”。

## 2. 本体在哪

- **没有**。`ast/` 是 Rego AST；`compile/` 是 Rego 编译；`rego/` 是查询入口；`topdown/` 是求值。没有 OWL/SHACL/RDF 的解析或推理。
- 如果要把 Glyph 的标签接进来：标签是 JSON data；策略要自己写“哪个 label/tier + 哪个 subject/resource/action → allow/deny”。OPA 不提供标签体系、不提供冲突消解默认值。
- 因此它填的是 **C.1 的“策略层”**，不是标签层，也不是执行层。

## 3. 调用链

| 步 | 文件:符号 | 做什么 |
|---|---|---|
| 启动 | `cmd/run.go` → `runtime/` | 加载配置、插件、服务 |
| 策略分发 | `plugins/bundle/`、`plugins/discovery/` | 拉取/激活 policy bundle |
| 解析/编译 | `ast/`、`compile/`、`rego/rego.go` | 解析 Rego、准备 query |
| 求值 | `topdown/topdown.go` | 对 input + data 求值，产出 decision |
| 决策 API | `server/server.go` | REST `/v1/data/...`；返回 allow/deny/结果 |
| 审计 | `plugins/logs/` | decision logs（谁、什么 input、什么 decision） |
| 执行 | **调用方** | 网关/服务/agent 按 decision 拦截；OPA 不直接阻断 |

**失败处理**：OPA 返回 error 时，调用方必须 fail-closed；OPA 本身不替你决定默认 allow/deny。策略里可以写 `default allow := false`，但这是策略作者的责任。

## 4. 接缝判定

| 问题 | 回答 | 证据 |
|---|---|---|
| 有外部判据（判据来自本体） | **否**：判据来自 Rego，不是本体 | `rego/`、`topdown/` |
| 有阻断能力 | **否**：OPA 只返回 decision；执行在调用方 | `server/server.go` |
| 位置明确 | **否**：可接 read-path/commit-gate，但不是接缝本身 | 本文 §6 |
| 与本体执行的关系 | 无：不解析/不求值本体 | `ast/`、`compile/` |

## 5. 真执行还是装饰

- **真执行**：Rego 被解析/编译/求值；decision 由 `topdown` 算出；有单测/CI/生产采用。不是“把策略塞进 prompt”。
- **但不是本体执行**：没有 OWL entailment、没有 SHACL 校验、没有查询重写；它执行的是**策略**，不是本体。
- **不能证明**：接了 OPA 就有访问控制；OPA 只给 decision，执行/覆盖/标签正确性仍要看调用方与数据。

## 6. 对 04 C.1 的用法

三层里它只填**策略层**：

```
标签/分类 (Glyph) → 策略 (OPA：Rego + input/data) → 执行 (trustgraph 读路径 / 调用方)
```

- **能补的**：谁写策略（Rego）、默认 allow/deny、冲突/优先级（Rego 规则顺序/complete vs partial rules）、策略版本（bundle）、审计（decision logs）。
- **不能补的**：标签质量/漏标率（Glyph）、读路径过滤（trustgraph）、写授权（commit gate）；OPA 与 trustgraph 没有现成集成。
- **接线要点**：把 `subject/resource/action/labels/tier` 作为 input；policy 里显式写默认 deny；decision log 带 `policy_version`；执行点必须 fail-closed。

## 7. 成本 / 运维

- **形态**：Go 二进制；sidecar/daemon/库；bundle 分发；decision logs 落盘/远端。
- **成本**：未在本仓库测延迟/吞吐；OPA 的求值是内存内，通常低延迟，但 decision log/bundle 拉取与策略复杂度会加开销。
- **风险**：策略作者写错默认值；label→policy 映射错；bundle 版本漂移；decision log 没接审计。

## 8. 与 E-22 / trustgraph 的关系

- **E-22** 说“标签层有 Glyph、策略层没有来源、执行层只有 trustgraph”；OPA 是**策略层的候选来源**，不是 E-22 已包含的证据。
- **trustgraph** 的 SHACL-AF post-filter 是执行层；OPA 是决策层。两者可以串（OPA decision → trustgraph/调用方执行），但**没有现成集成**，不能把 OPA 的存在读成“访问控制可执行”。
- 如果要把 OPA 写进 E-22，需要另做一次代码级/实测核对；本页只是候选。

## 9. 还没解决 / 下一步

- label→policy 的映射：Glyph 的 275-leaf 标签怎么变成 Rego 的 input/data？未做。
- 冲突/优先级：多策略命中同一资源时谁赢？Rego 的规则语义够不够？未测。
- decision log 的 schema 与 04 C.6 的 `audit` 字段怎么对齐？未做。
- 延迟/吞吐：sidecar 形态下的 p99？未测。
- 与 trustgraph 的集成：OPA 决策能不能驱动 SHACL-AF 的 policy graph？未做。

## 10. 代码位置

- 入口：`cmd/run.go`、`main.go`
- 服务/API：`server/server.go`
- Rego：`rego/rego.go`、`ast/`、`compile/`
- 求值：`topdown/topdown.go`
- 分发/审计：`plugins/bundle/`、`plugins/discovery/`、`plugins/logs/`
- 代码地图：[code-map.md](./code-map.md)（文件/符号索引）
- 文档：https://www.openpolicyagent.org/docs
- pin：`3dc83ae32b43eb1a649ce0c5e6745fc7a4f3d146`
