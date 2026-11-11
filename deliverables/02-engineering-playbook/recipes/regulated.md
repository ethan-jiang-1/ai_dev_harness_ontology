---
status: draft
updated: 2026-11-11
parent: ../README.md
basis: compilation 机制三（Grid 已移出；旧数字停用）
---

# R12 · 受监管知识供给：证据 + solver + 人签核

> **W-05**：原锚 Grid 已移出；R12 转 gap。机制保留，效应量按 [W-05](../sections/canonical.md#w-table) 重测。

> 这不是「让模型更准」的 recipe，而是**受监管工作**的架构：答案必须引用证据，数字必须由成熟 solver 算，人做最终决策。三者写进架构，不写进 prompt。
>
> 它只适用于有成熟 solver、法规可检索、人能签核的域。没有这三项，别用。

## 目标

让 agent 准备「可审计的法规证据 + 可复算的研究结果」，由人签核；把责任留在人，把检索/计算/整理交给系统。


> **为什么是 gap**：原唯一锚 Grid 已移出；没有 admitted 来源，不能再判 B。0.95 的 citation precision 是**工程建议**，按 W-05 在你的域预注册，不是 Grid 结论。
## 适用 / 不适用

| 适用 | 不适用 |
|---|---|
| 受监管工程（并网、规划、合规审查） | 没有 solver/领域工具 |
| 法规/标准可检索、可引用 | 法规不可检索/不可引用 |
| 需要审计、可重放、人签核 | 需要完全自动无人决策 |
| 网络/系统规模在工具能力内 | 规模远超工具能力 |
| 能接受人签核吞吐限制 | 需要形式安全保证 |

## 前提

- 成熟 solver（潮流/N-1/短路/OPF 等）+ 领域工具 wrapper。
- 可检索、可引用的法规/标准语料（规模以你的域为准）。
- 人能签核，且流程允许「决策点暂停」。
- 能记录 study 状态（state_hash）、solver 版本、工具调用。
- 有 20–50 个 held-out 任务做验收。

## 接缝 / 形态

供给 + 输出时 + 人决策点；`context`/`compiled` + 外部 solver。它不是单一接缝，而是**一条受监管工作流**：检索 → 证据 → solver → strict pass → 人签核 → 落盘/交付。

## 最小数据契约

```text
citation: {doc_id, version, page, span, clause_id, retrieved_at}

study_tool:
  input:  {study_type, network_model, state_hash, solver_config}
  output: {result, solver_version, provenance, warnings}

strict_pass_log:
  {task_id, tool_calls[], network_state_hash, study_type,
   pass|fail, reason}

memory:
  {kind: semantic|procedural|episodic, content, source,
   approved_by, version}

decision_point:
  {decision_id, findings, citations, signer, timestamp}
```

**规则**：

- 每条法规结论必须带 citation；不能引用就拒答。
- 所有数字由 solver 产生；模型只选择/排序/解释。
- strict pass 重放工具调用：`state_hash` 一致 + `study_type` 匹配 + `solver_version` 已记，才算 pass。
- 未签核不继续；记忆共享变更需人批准。

## 做法（2 周最小闭环）

1. **先立三条原则**：证据先行、solver 算数字、人决策；写进架构。
2. **建可检索、可引用的法规库**；citation 对象 + 拒答规则（阈值配置化）。
3. **把研究做成工具**：study 输入/输出契约；每次记录 `state_hash`/`solver_version`/provenance。
4. **strict-pass 重放**：日志 + 判定脚本；state 不匹配即 fail。
5. **决策点暂停 + 具名签核**：`{decision_id, findings, citations, signer, timestamp}`。
6. **20 个 held-out 任务**：引用精度、state 漏报、人审分钟、任务完成；不追论文分数。
7. **第二 sprint** 再谈成本/替代方案/规模。

## 证据

**W-05；Grid 已移出，R12 没有 admitted 效应量。** 重启按 W-05 协议；下面只保留机制读法（`推测`）：

- **证据 + solver + 人签核**是架构约束，不是「让模型更准」的配方；没有这三件就别用 R12。
- **工具在环境里 ≠ 工具在回路里**：多数任务仍靠 agent 自己写代码，MCP 工具只被少数任务调用；这是机制判断，具体调用数按 W-05 在你的域测。
- **相对最强 agent baseline 的增益很小**，大差距只出现在 vs base model；这是旧对照的读法，具体差值按 W-05 重测。
- 条件（旧 benchmark 的边界）：单研究任务、不是真实运营商规模、不是完整 connection study、技术报告；换域必须重测。

> 要重启 R12，先找能复算「citation precision / 拒答 / strict-pass」的新源；在那之前只作架构参考。

## 成本

| 项 | 量级 | 等级 |
|---|---|---|
| 法规语料治理/索引 | 4–8 人周 | 推测 |
| 领域工具/solver wrapper | 4–8 人周 | 推测 |
| solver 授权费 | 按厂商 RFQ | 未知 |
| 人签核 | 5–15 分钟/决策 | 推测 |
| 运行 | 按你的 solver/端点实测 | 未测 |
| 维护 | 法规更新/工具版本/记忆审批 | 未知 |

## 验收 / 停

| 指标 | 通过线（工程建议） | 停 |
|---|---|---|
| citation precision | 按你的域预注册（旧 0.95 是工程建议，不是 Grid 结论） | 低于预注册 → 先修检索 |
| strict-pass 漏报 | 0 | >0 → 停，先修重放 |
| 拒答率 | 可解释、阈值配置化 | 异常 → 先修检索/规则 |
| 人签核吞吐 | 满足业务 | 不足 → 不扩规模，先改流程 |
| solver | 有成熟 solver/工具 | 没有 → 停，不要 LLM 手算 |
| 法规 | 可检索/可引用 | 不可 → 不做 |
| 形式保证 | 不承诺 | 需要 → 另做验证，不用本 recipe |

**拒答结果是结果，不是阈值**；阈值要按证据不足/引用缺失的规则配置并记录。

## 失效模式

- **把 benchmark 高分当「agent 比人强」。** 旧对照里相对最强 agent baseline 的增益很小，大差距只在 vs base model；具体分数停用。
- **把工具在环境里当工具在回路里。** 旧观察里 MCP 工具只被极少数任务调用；写代码也能到相近分数。
- **把 strict pass 当形式证明。** 它是工作验证，不是安全保证。
- **把 benchmark 当部署。** 旧 benchmark 是单研究任务、规模有限；不是真实运营商流程。
- **把旧拒答结果当阈值。** 旧数字是结果，不是预注册线。
- **人签核瓶颈。** 吞吐不足时，系统再准也扩不动。
- **法规版本频繁。** 语料/索引/引用版本要持续维护。

## 可抄锚点

- [Grid digest](../../../meta/audits/2026-11-11-source-purge.md#src-2611-03534) 的**结构**（§6.1 复刻顺序、§6.5 契约/成本/stop）可当历史模板；**§4 的数字停用**。
- [compilation 机制三](../../../topics/03-knowledge/compilation/mechanism.md) 的受监管支线、citation/拒答、strict pass。
- 不要抄「工具必须到达研究 = 分数保证」；作者立场是设计原则，不是效应量。

**出处**：[Grid digest](../../../meta/audits/2026-11-11-source-purge.md#src-2611-03534) · [compilation 机制](../../../topics/03-knowledge/compilation/mechanism.md)

> 回 [recipes 索引](./README.md) ｜ 回 [02 目录](../README.md)
