---
status: seed
source_type: open-source
reading: 已读代码
provenance: 一手代码
updated: 2026-11-09
repo: fabio-rovai/open-ontologies
url: https://github.com/fabio-rovai/open-ontologies
commit: 375fbc4789debfb57e9c7dfc6bf0e8db8fb21f9b
release:
license: MIT
scan_date: 2026-11-09
stars_at_scan: 2848
last_push: 2026-11-04
ontology_role: core
seam: none
execution_form: engine
evidence_role: mechanism-only
home: topics/05-produce
subtopic: lifecycle
also_supports: []
updates: []
admission: admitted
gate_checked: 2026-11-11
impact_evidence: "I2+I5: 12 contributors, W3C SHACL suite, 16 releases"
liveness: last_push 2026-11-04
provenance_type: community
---

# fabio-rovai/open-ontologies · 来源卡

> 来源卡：只记可定位的事实。调用链与定级在同目录 `digest.md`。

## 一句话

Rust 实现的本体工程工具链：SHACL 校验、变更影响/闭包差分、保守性检查，目标是让本体变更可验证、可回滚。

## 本体在哪

| 项 | 内容 |
|---|---|
| 文件 / 目录 | 仓库自带 314 个 `.ttl`（含 `tests/w3c-shacl/manifest.ttl`、`benchmark/reference/*.shacl.ttl`、`demo/corpus/.../recovered-shapes.ttl`）；SHACL 引擎在 `src/shacl.rs`、`shacl_verified.rs`、`shacl_report.rs` |
| 格式 | OWL/Turtle + SHACL；配套 Dafny/Isabelle/Lean/Rocq 形式化目录（`dafny/`、`isabelle/`、`lean/`、`rocq/`） |
| 谁生成、谁加载 | CLI / library 读入本体与 shapes；`plan_validate.rs` 做校验计划 |
| 是否版本化 / 可回滚 | 16 releases；CHANGELOG；变更影响面（`closure_diff.rs`、`conservativity.rs`、`coevolve.rs`）是核心模块 |

## 调用点

- SHACL 校验：`src/shacl.rs` + `shacl_verified.rs`；CLI 入口在 `src/`（`batch.rs` 等）
- 变更/影响面：`src/closure_diff.rs`（闭包差分）、`conservativity.rs`（保守性）、`coevolve.rs`（协同演化）
- 一致性/分类：`src/classify_el.rs`（EL 分类）、`align*.rs`
- 输入 / 输出：本体 + shapes → 校验报告 / 差分 / 影响面
- 失败时降级：未定位

## 证据入口

- tests：`tests/w3c_shacl_conformance_test.rs`、`tests/shacl_*.rs`、`tests/abox_realization_test.rs`、`tests/align_*_test.rs`；W3C SHACL 套件在 `tests/w3c-shacl/`
- benchmark：`benchmark/`（pizza shapes、reference shapes）
- issue / 生产案例：16 releases；真实用户未核
- 最小复现：`cargo test`（Rust 工具链）；先跑 `w3c_shacl_conformance_test`

## 与哪篇 digest 对照

| 论文 digest | 机制 | 这里对应 / 缺失 |
|---|---|---|
| [Commit Boundary](../../../meta/audits/2026-11-11-source-purge.md#src-2610-37407) | 落盘前的授权/证据判据 | 变更前的 SHACL 校验与差分；是否阻断 commit 未核 |
| [OntoDoc](../../../meta/audits/2026-11-11-source-purge.md#src-2611-01276) | 本体文档化/生成 | 未定位（待核） |

## 局限

- 12 贡献者、1,080 commits，其中 680 来自 `claude` 账号——AI 辅助密集；commit 数不代表人力。
- 仓库 392MB，含形式化与多语言绑定；**先读 `src/shacl*.rs` 与 `closure_diff.rs`，别通读**。
- 「blast radius / rollback」在 README 的声称要逐条回代码；目前只核到模块存在。
- 只到模块/测试层，未通读调用链。

## 待办

- [x] pin commit（375fbc4…）
- [x] 定位 SHACL 与变更模块
- [ ] 跑 `cargo test w3c_shacl_conformance`（或单测）
- [x] 已完成（2026-11-12 核对：文件已存在）
- [x] 已完成（2026-11-12 核对：文件已存在），回链 `topics/05-produce/lifecycle` 与 `01-constraint/commit-gate`
