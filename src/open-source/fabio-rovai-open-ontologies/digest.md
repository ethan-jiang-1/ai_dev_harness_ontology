---
status: draft
updated: 2026-11-09
quality: C
based_on: card.md
commit: 375fbc4789debfb57e9c7dfc6bf0e8db8fb21f9b
claims: []
---

# open-ontologies：把「本体执行」做成可审计的工具面——但这次我们没跑起来

> **自包含**：不假设读者读过 README、card 或论文。代码位置写到 `文件:类型/函数`，不贴大段代码。
> **证据等级**（四档）：
> - `已核`：读过代码，能指到文件/函数；或读过一手文档原文。
> - `已证`：不仅跑通，且能用 `EXP-xxx` 在本仓库外复现；**跑通示例不等于机制有效**。
> - `推测`：只读 README/文档/issue，没有代码定位。
> - `存疑`：README 与代码/issue 冲突，或核心闭源。
> `reading: 已读代码` 指读到哪；本页 **C2 未跑通**，已如实标阻塞原因。

## 0. 三句话

1. **它是什么**：Rust 写的本体引擎（MIT，2.8k★）：单二进制，带 CLI 与 MCP server；SHACL 校验、SHIQ tableaux 推理、SPARQL、变更影响/保守性检查。
2. **本体怎么被用**：**作为可执行对象**。SHACL 约束真的被求值（默认编译成 SPARQL 交给 Oxigraph；另有 `--verified` 的 SHACL Core 求值器）；变更影响有 `closure_diff` 报告（丢了多少蕴含、证书、exit code）。
3. **证据到哪**：代码与测试设计可读（`已核`）；**执行没跑起来**——cargo 拉 `oxigraph` 分支依赖时 submodule 取不到，预编译二进制下载被网络阻断（`存疑`/阻塞，见 §5）。

## 1. 项目与维护状态

- 仓库：`fabio-rovai/open-ontologies`，MIT，本次 pin `375fbc47`；release v2.1.0。
- 规模：2,848★；2026-03 建，2026-11-04 仍在推送；12 贡献者、1,080 commits。
- 风险信号：**680/1,080 提交来自 `claude` 账号**；仓库 392MB（含 `benchmark/`、`studio/`、`case-studies/` 与 Dafny/Isabelle/Lean/Rocq 目录）。AI 辅助密集，不代表造假，但 commit 数不是人力。
- 与本研究的关系：它把「本体能不能被执行」做成了**工具面**（CLI/MCP），而不是论文里的一个模块；还额外提供「未验证 vs 已验证」两条求值路径。

## 2. 本体在哪

| 形态 | 位置 | 格式 | 谁提供 | 用途 |
|---|---|---|---|---|
| 本体/数据 | 用户文件或 store | RDF/OWL（Turtle/N-Triples/RDF-XML/JSON-LD/OFN…） | 用户 | 加载、查询、推理 |
| SHACL shapes | 用户文件（`shacl --shapes`） | SHACL/Turtle | 用户 | 校验数据 |
| W3C 套件 | `tests/w3c-shacl/manifest.ttl` | SHACL 测试清单 | 仓库 | 一致性 ratchet |
| 规则包 | `src/enforce.rs` 内置 + 自定义（SQLite） | 规则/查询 | 用户/仓库 | 设计模式强制 |
| 变更证书 | `src/closure_diff.rs` 报告 | JSON | 引擎 | 变更影响面 |

**关键**：仓库不自带领域本体；它提供的是**执行器 + 证据结构**（报告里带证书、覆盖率、gaming direction、exit code）。

## 3. 调用链

```
# 默认 SHACL（约束 → SPARQL → Oxigraph）
open-ontologies --data-dir DIR load data.ttl
open-ontologies --data-dir DIR shacl --shapes shapes.ttl
 → setup(data_dir) → GraphStore
 → ScopeRequest::from_args(valid_at/as_of/all_versions)
 → ShaclValidator::validate_scoped → 约束编译为 SPARQL → Oxigraph
 → JSON（conforms / violations / skipped_constraints）；exit code 来自 verdict

# 已验证 SHACL（SHACL Core；undetermined 是一等答案）
... shacl --shapes shapes.ttl --verified
 → shacl_verified::validate_verified
     → 拒绝 sh:sparql / 用户自定义组件（W3C 120 条里 22 条）
     → 0 = verdict；2 = 文件读失败；3 = undetermined（没检查完）
     （这是 oo-shacl 子进程的码；外层 CLI 见 §3 的代码核对）
 → 「conforms: true」只由机器检查过的定理覆盖

# 变更影响
open-ontologies diff old.ttl new.ttl → OntologyService::diff → JSON
# 库侧：closure_diff::ClosureDiffReport（entailments_lost / lost_by_warrant /
#       monotonicity_violations / coverage_proxy / exit_code 0/1/2）
```

实现细节（可核对）：

- **两条求值路径不是 superset 关系**：默认路径支持 `sh:sparql` 但会 skip 一些约束；verified 路径覆盖 SHACL Core 但拒绝 `sh:sparql`。CLI 明确拒绝把 `--verified` 和 `--valid-at/--as-of/--all-versions` 合用（否则 scope 会被静默丢弃）。
- **undetermined 有独立 exit code 3**：代码注释说得很直白——「conforms」与「我没检查完」不能合并。**但这是 `oo-shacl` 子进程的码**；外层 `gate_exit_code` 把 `conforms:null` 映射为 exit 2，与解析失败同码。JSON 保留 `conforms:null` + `undetermined`，shell 退出码不保留第三态。
- **2026-11-09 代码核对（pin `375fbc4`）**：`src/shacl.rs` 确认默认路径把核心约束编译为 SPARQL 交 Oxigraph；`src/shacl_verified.rs` 确认 verified 包装 `oo-shacl` 的 0/2/3；`src/main.rs:1822` 的 `gate_exit_code` 确认外层把 null 折叠成 2。
- **`enforce` 是 CI 规则门，不是 commit 授权**：`Gate::Enforce` 在任一 `severity=error` 时 exit 1，但它检查的是规则包（orphan class/missing domain 等），不对单次写/落盘签发授权。
- **变更报告带「gaming direction」**：`headline_gaming_direction` 明说 headline 指标可以被「缩小投影词表」刷低；报告把方向写进 payload，而不是只写文档。
- **MCP**：`src/server.rs` 用 `rmcp` 暴露工具；工具面可按 profile 裁剪（`--tool-profile`）。

## 4. 接缝判定

| 条件 | 是否成立 | 证据 |
|---|---|---|
| 有外部判据（来自本体，不是模型自评） | **成立** | SHACL 约束由 shapes 决定；变更报告由蕴含闭包决定 |
| 有阻断能力（违反可改变走向） | **部分成立** | SHACL 报告有 verdict；`closure_diff` 有 exit code 2（stop-the-line），但**是否阻断由调用方决定** |
| 位置明确（能指到回路某一时刻） | **成立，但不在回路内** | 它是 CLI/MCP 工具，被 agent 显式调用；没有自动挂在输出后 |

**结论**：它是 **checker + 变更分析工具**，不是 in-loop 接缝。它最有价值的不是「在 agent 里跑」，而是**把 checker 的答案分成三态**（通过 / 违反 / 没检查完）并把「没检查完」变成不可吞掉的状态。

## 5. 证据与最小复现

**C2 状态：阻塞（不是通过）。**

1. `CARGO_HOME=/tmp/cargo-home CARGO_TARGET_DIR=/tmp/oo-target cargo test --test w3c_shacl_conformance_test`
   - 失败：拉 `oxigraph` 的 git 依赖（`fabio-rovai/oxigraph` rev `37db8e15`）时，submodule `bench/bsbm-tools` 的 rev `59d0a8a` 取不到；`SecureTransport error: connection closed via error`。
   - 重试 `CARGO_NET_GIT_FETCH_WITH_CLI=true` 仍卡在同一处。
2. 预编译 `open-ontologies-aarch64-apple-darwin`（release v2.1.0，67.9MB）下载失败：`curl: (28) Failed to connect to github.com port 443`。
3. 工具链：本机 `rustc` host 是 `x86_64-apple-darwin`，但系统只有 arm64 的 CommandLineTools；`cargo build` 在链接 `libc`/`zerocopy` 时 `xcrun` 报「missing compatible architecture (need x86_64)」。`rustup target add aarch64-apple-darwin` 也因缓存路径失败。
4. 未尝试 Linux 版 `oo-shacl`（当前 macOS arm64 不可用）。

**可读到的证据（不等于跑通）**：

- `tests/w3c_shacl_conformance_test.rs` 是 manifest 驱动的 W3C 套件 ratchet，明确定义「gated 列」只比 `sh:conforms` + `(focus, sourceShape, sourceConstraintComponent)` 集合；文件头记录了 2026-09-13 审计发现的四个 SHACL 缺陷与修复。
- `src/shacl_verified.rs` 记录：verified 路径覆盖 SHACL Core、拒绝 `sh:sparql` 与自定义组件（120 条里 22 条）；exit 3 = undetermined。
- `closure_diff` 的报告结构包含 `entailments_lost`、`lost_by_warrant`、`monotonicity_violations`、`monotonicity_gate_skipped`、`skipped`、`exit_code`。

**quality: C 的理由**：代码与测试设计可读，但**没有一次成功执行**；按「C = 只读代码/无测试运行」定级，不冒充 B。

## 6. 不能证明什么

1. **不能证明它跑得起来**（本次环境）：网络阻塞；也没有别的执行记录。
2. **不能证明 W3C 一致性达标**：测试文件存在 ≠ 通过；ratchet 的当前通过数未知。
3. **不能证明 MCP 被 agent 用过**：仓库没有生产 trace；工具可被调用 ≠ 被调用。
4. **不能证明 verified 路径的定理覆盖 SHACL 全量**：只覆盖 SHACL Core，`sh:sparql` 被拒（22/120）。
5. **不能证明变更报告能替代 commit gate**：它报告影响，不做授权；exit code 2 仍需调用方执行。
6. **不能证明 AI 辅助提交不影响质量**：680/1,080 来自 `claude`；没有独立审计。
7. **不能证明 star 与 16 releases 等于采用**：release 数来自复核转述，未逐条核。

## 7. 与论文 digest 对照

| digest | 论文机制 | 代码里对应 | 缺什么 / 差异 |
|---|---|---|---|
| [What Does an Ontology Catch](../../../meta/audits/2026-11-11-source-purge.md#src-2610-37809) | 本体当 checker；catch/FA 是核心 | SHACL 求值器 + W3C ratchet；**第三态 undetermined** | 没有 catch/FA 测量；没有真实错误分布 |
| [Commit Boundary](../../../meta/audits/2026-11-11-source-purge.md#src-2610-37407) | 落盘前授权；证据≠授权 | `closure_diff` 报告影响面 + exit code | 报告不是授权；没有 promotion/scope 语义 |
| [SFE-O](../../../meta/audits/2026-11-11-source-purge.md#src-2610-37123) | 约束「未落 SHACL 只是文档」 | 这里 SHACL 真的被求值（两条路径） | 但本次没跑起来，不能当「已证」 |

**一句话**：它最值得带走的是**证据工程**：把「没检查完」做成独立状态、把指标的 gaming direction 写进 payload、把「verified」限定在定理覆盖的范围内。这些是 checker 类工作可以借鉴的，与它跑不跑起来无关。

## 8. 工程含义

- **接口**：CLI（`load`/`shacl`/`diff`/`reason`/`validate`）+ MCP 工具；单二进制、无 JVM。
- **数据**：用户自备 RDF/OWL + SHACL shapes；仓库不带领域本体。
- **成本**：单二进制 68–83MB；构建重（git 依赖 + submodule）；运行成本未测。
- **失败模式**：默认路径会 skip 约束（`skipped_constraints`），verified 路径会 undetermined（exit 3）；两者都要求调用方正确解释，不能只看 `conforms`。
- **什么时候别用**：需要完整 SHACL（含 `sh:sparql`）又要 verified 保证时，两条路径都不满足；需要 JVM 生态时也不合适。

## 9. 代码地图

见同目录 [`code-map.md`](./code-map.md)：入口、SHACL/变更符号、调用链、阻塞记录、未定位项。

## 10. 下一步

- 换网络/换环境重跑：`cargo test --test w3c_shacl_conformance_test` 或下载 macOS 二进制；把「通过数/失败数」写回 §5。
- 构造一个含 `sh:sparql` 的 shapes，对比默认与 `--verified` 的输出（一个 skip、一个 exit 3）。
- 回 topics：02/checker 加 F7（第三态）；05/lifecycle 加变更报告的边界（报告≠gate）。
