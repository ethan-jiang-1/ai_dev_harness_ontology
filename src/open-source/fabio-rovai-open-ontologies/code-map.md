---
status: seed
updated: 2026-11-09
repo: fabio-rovai/open-ontologies
commit: 375fbc4789debfb57e9c7dfc6bf0e8db8fb21f9b
---

# fabio-rovai/open-ontologies · 代码地图

> 只做定位：文件 / 符号 / 谁调用谁。不贴代码、不写判断；判断在 `digest.md`。
> 路径相对仓库根；commit `375fbc4`。

## 入口

| 入口 | 形态 | 说明 |
|---|---|---|
| `open-ontologies`（`src/main.rs`） | CLI | `load` / `validate` / `query` / `diff` / `shacl` / `reason` / `version` / `rollback` / `defects` |
| `src/server.rs`（`rmcp`） | MCP server | `onto_validate` / `onto_load` / `onto_query` 等工具；`serve` 起服务 |
| 库 | Rust crate | `ShaclValidator`、`Enforcer`、`ClosureDiffReport` |

## 本体 / SHACL / 变更相关文件

| 文件 | 符号 | 作用 | 被谁调用 |
|---|---|---|---|
| `src/shacl.rs` | `ShaclValidator::validate/report_scoped` | SHACL 校验（默认路径：约束编译成 SPARQL 交给 Oxigraph） | CLI `shacl`、MCP、库 |
| `src/shacl_verified.rs` | `validate_verified` | 已验证求值器（SHACL Core；`oo-shacl`；undetermined=exit 3） | CLI `shacl --verified` |
| `src/server.rs` | `#[tool]` 方法 | MCP 工具面（validate/load/query…） | agent 通过 MCP 调用 |
| `src/enforce.rs` | `Enforcer::enforce` | 规则包执行（generic/boro/value_partition/hierarchy/ies4） | CLI/库 |
| `src/closure_diff.rs` | `ClosureDiffReport` | 蕴含闭包差分：丢了多少结论、证书、exit code | `coevolve`/batch/库 |
| `src/conservativity.rs` | `conservativity_check` | 扩展的演绎保守性 | 变更分析 |
| `src/main.rs` | `Commands::Shacl/Diff/Reason` | CLI 分发 | 用户 |
| `src/ontology/...` | `OntologyService::diff` | CLI `diff` 的两版本体对比 | CLI `diff` |

## 调用链

```
# 默认 SHACL 路径
open-ontologies --data-dir DIR load data.ttl
open-ontologies --data-dir DIR shacl --shapes shapes.ttl
 → setup(data_dir) → GraphStore
 → read shapes file
 → ScopeRequest::from_args(valid_at/as_of/all_versions)
 → ShaclValidator::validate_scoped/report_scoped
     → 约束编译为 SPARQL → Oxigraph 执行 → sh:ValidationReport
 → JSON（conforms / violations / skipped_constraints）
 → exit code 由 verdict 决定

# 已验证路径
... shacl --shapes shapes.ttl --verified
 → shacl_verified::validate_verified(graph, shapes)
     → SHACL Core；拒绝 sh:sparql / 自定义组件
     → 0 = 有 verdict；2 = 读文件失败；3 = undetermined（没检查完）
 → JSON 带 undetermined，不把「没检查」说成「通过」

# 变更影响
open-ontologies diff old.ttl new.ttl
 → OntologyService::diff(old, new) → JSON
# 库侧：closure_diff::ClosureDiffReport（entailments_lost / lost_by_warrant /
#       monotonicity_violations / exit_code 0/1/2）
```

## 测试与示例

| 路径 | 覆盖什么 | 怎么跑 |
|---|---|---|
| `tests/w3c_shacl_conformance_test.rs` | W3C SHACL 套件（manifest 驱动；gated 列 = conforms + focus/sourceShape/组件集合） | `cargo test --test w3c_shacl_conformance_test` |
| `tests/w3c-shacl/manifest.ttl` | 套件入口 | 由上一个测试读取 |
| `tests/shacl_audit_regressions_test.rs` | 审计发现的四类 SHACL 缺陷回归 | `cargo test --test shacl_audit_regressions_test` |
| `tests/shacl_core_verified_test.rs` | 已验证求值器 | 同上 |

## 运行记录（C2）

**状态：阻塞（不是通过）。**

1. `CARGO_HOME=/tmp/cargo-home CARGO_TARGET_DIR=/tmp/oo-target cargo test --test w3c_shacl_conformance_test`
   - 失败：拉 `oxigraph` git 依赖（`fabio-rovai/oxigraph` rev `37db8e15`）时，submodule `bench/bsbm-tools` 的 rev `59d0a8a` 取不到；`SecureTransport error: connection closed via error`。
2. 预编译二进制 `open-ontologies-aarch64-apple-darwin`（release v2.1.0）下载失败：`curl: (28) Failed to connect to github.com port 443`。
3. 未尝试：Linux 的 `oo-shacl`（当前 macOS arm64 不可用）。

→ 代码与测试设计可读（`已核`）；**执行未验证**。C2 阻塞原因已留档，不当作跑通。

## 未定位

- MCP 工具在真实 agent 里的调用记录（仓库无生产 trace）。
- `closure_diff` 与 CLI `diff` 的分工（前者是闭包/证书，后者是 `OntologyService::diff`）。
- Lean/Dafny/Isabelle/Rocq 形式化与 `Shacl.validate_spec` 的对应关系（只读目录名与文档句）。
