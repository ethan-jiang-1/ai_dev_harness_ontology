---
status: draft
source_type: open-source
reading: 已读代码
provenance: 一手代码
updated: 2026-11-09
repo: open-policy-agent/opa
url: https://github.com/open-policy-agent/opa
commit: 3dc83ae32b43eb1a649ce0c5e6745fc7a4f3d146
release:
license: Apache-2.0
scan_date: 2026-11-09
stars_at_scan: 12452
last_push: 2026-11-09
ontology_role: none
seam: none
execution_form: none
evidence_role: mechanism-only
home: topics/01-constraint
subtopic: access-control
also_supports: []
updates:
  - topics/01-constraint/access-control/README.md
  - topics/01-constraint/claims.md
  - topics/01-constraint/sources.md
---

# open-policy-agent/opa · 来源卡

> 来源卡：只记可定位的事实。调用链与「执行还是装饰」的定级在同目录 [digest.md](./digest.md)。

## 一句话

CNCF graduated 的通用策略引擎：用 Rego 写 allow/deny，服务在需要决策时查询 OPA；它**不做本体推理、不执行 KG 过滤**，但能把 04 C.1 缺的“策略层”做成可部署的决策点。

## 本体在哪

- **没有 OWL/SHACL/RDF**。策略是 Rego；输入/数据是 JSON；`ast/`、`compile/`、`rego/` 处理的是 Rego 模块与 query，不是本体公理。
- 可以接收 Glyph 输出的标签（作为 JSON data / input），但**没有 label→policy 的映射**；映射要自己写 Rego。
- `ontology_role: none`：它是策略层 adjunct，不是本体实现。

## 调用链（文件:符号）

| 步 | 位置 | 做什么 |
|---|---|---|
| 启动 | `cmd/run.go` → `runtime/` | 起 OPA 服务/加载配置 |
| 策略分发 | `plugins/bundle/`、`plugins/discovery/` | 拉取/更新 policy bundle |
| 解析/编译 | `ast/`、`compile/`、`rego/rego.go` | 解析 Rego 模块、准备 query |
| 求值 | `topdown/topdown.go` | 对 input + data 求值，产出 decision |
| 决策 API | `server/server.go` | REST `/v1/data/...`；调用方拿 allow/deny |
| 审计 | `plugins/logs/` | decision logs |
| 执行 | **不在 OPA** | 调用方/网关按 decision 拦截；OPA 只返回判定 |

## 接缝判定

| 问题 | 回答 | 证据 |
|---|---|---|
| 有外部判据（判据来自本体，不是模型自评） | 否（判据来自 Rego，不是本体） | `rego/`、`topdown/` |
| 有阻断能力（违反可剪动作/拒输出/阻落盘） | 否（OPA 只给 decision；执行在调用方） | `server/server.go` |
| 位置明确（能指到回路某一时刻） | 否（可接 read-path/commit-gate，但不是接缝本身） | 本文 §6 |
| 失败处理 | 策略/调用方定义；OPA 返回 error，调用方必须 fail-closed | `server/` |

## 维护与采用

- CNCF graduated；`ADOPTERS.md` 列生产采用；12,452★；最后 push 2026-11-09；Apache-2.0。
- 只读代码，未在本仓库跑 OPA；`reading: 已读代码`，`quality: B`（有测试/CI/生产，但未复跑）。

## 原文

- Repo：https://github.com/open-policy-agent/opa
- 文档：https://www.openpolicyagent.org/docs
- pin commit：`3dc83ae32b43eb1a649ce0c5e6745fc7a4f3d146`
