---
status: draft
updated: 2026-11-09
---

# 模型可用性（用户约束）

> 2026-11-09 用户明确：**本地不安装模型**；可提供的是 **Yovole 里的两个模型**。任何依赖模型的工作都按这一条来，不要向用户要本地安装、GPU、API key 或别的 endpoint。

## 可用的两个模型

| 提供方 | 模型 ID | 说明 |
|---|---|---|
| Yovole | `DeepSeek-V4-Flash` | 快速档；适合低成本批量调用 |
| Yovole | `qwen3.8-27b` | Qwen 3.8 27B；适合第二意见/对照 |

配置位置（本机 DSH profile）：`~/.dsh/profiles/web/cordis.patch.yml` 的 `yovole` provider，`apiKeyEnv: AIDER_OPENAI_API_KEY`，`baseURL: https://ds-api.yovole.com/v1`。

## 访问方式

- **首选**：在 harness 里用 provider/model override（workflow 的 `agent(..., {provider:'yovole', model:'qwen3.8-27b'})`，或 UI 模型选择）调用；不要自己拼 HTTP。**但 subagent 不是 raw chat**：它会带工具、仓库上下文和系统提示；2026-11-09 的 Yovole mini-run 里，qwen 直接去读仓库、跑 checker，输出被污染。**不要把 subagent 当实验被试。**
- 2026-11-09 从 bash 沙箱直接请求 `https://ds-api.yovole.com/v1` 超时；这不代表模型不可用，只代表沙箱到该域名的直连不通。
- **不要**打印、提交或复制 key；不要为调用模型新建配置文件。
- **不要**安装本地模型、下载权重、起推理服务。

## 对实验的含义

- 任何模型依赖的实验只能用这两个模型；结论里要写清模型 ID 与提供方。
- 这两条模型不是“干净被试”：通过 harness 调用时，它们有系统提示、工具与上下文；2026-11-09 已观察到工具泄漏：qwen 直接读仓库、跑 checker，并写了 `topics/01-constraint/action-gate/runs/2026-11-09-refund-block-run.md`（已删除）。用于 pilot 时要标 `推测`，且必须说明污染；不能说 `已证`。真正要跑行为实验，需要 raw chat endpoint 或一个禁用工具/仓库访问的受限 runner。
- 如果两个模型都出现天花板/地板效应，说明**任务设计**不具判别力，不是“形态无用”；先改任务，不要换模型刷结果。
- 2026-11-09 的 EXP-007 代理试点曾用 DeepSeek V4 Pro（DeepSeek API）与 Qwen 3.8 27B（OpenRouter）；那是本约束之前的临时路径，结果已记录，但**不再作为标准路径**。

## 一条纪律

模型是**被试**，不是“学习工具”。如果目标只是消化概念，不需要模型；需要模型时，只用上面两个，并先说明实验要回答什么、会推翻什么。
