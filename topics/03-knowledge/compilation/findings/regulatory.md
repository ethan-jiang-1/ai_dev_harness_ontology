# 另一种编译：受监管知识系统

## F5

- **判断**：受监管知识供给的三条设计原则是证据引用、数字由 solver 算、人做决策；作者并主张「工具必须到达研究」。前两条有接口与结果指标（证据 recall、LegalBench-RAG F1、strict pass、E score）；「工具必须到达研究」是设计原则，Power-Agent 仅 46/519 调用 PowerMCP 仍到 99.4%（Codex CLI 也到 99.4%），说明「领域工具」不是分数必要条件（`推测`）。
- **等级**：`已核`（三原则与数字；Grid Agents 一手技术报告；工业系统）；工具/分数归因 `推测`。
- **条件/数字**：519 tasks / 8 families；Grid Studio E score 99.9%、中位 13.9 s；Codex CLI 99.4%、21.6 s；Power-Agent 99.4%、16.8 s（对最强 agent baseline 仅 +0.5pp，中位时间快 2.9–7.7 s）；Claude Code 85.4%、22.0 s；base model（GPT-6.1 sol）40.8%、Fable 5.1 28.3%；法规证据 recall 0.967 vs 0.856；LegalBench-RAG F1 0.980；>2,000 bus 108/109；optimizer −33–67%；PowerMCP 仅 46/519 被调用。
- **反例/边界**：benchmark 单研究；最大 9,241 buses；GB corpus 特定；无形式安全；长期维护未量化；99.9% 是任务级 E score，不是并网周期或审计发现数。Power-Agent 仅 46/519 调用 PowerMCP 仍到 99.4%，说明「领域工具在回路里」不是分数必要条件；Grid 的 0.5pp 优势与 2.9–7.7 s 提速来自哪一层未被单独消融（`推测`）。digest 的 99.9 vs 40.8 归因（工具/求解器）不变；这里降级的是「领域工具必须被调用」这一条。
- **来源**：[Grid 卡](../../../../meta/audits/2026-11-11-source-purge.md#src-2611-03534) · [digest](../../../../meta/audits/2026-11-11-source-purge.md#src-2611-03534) · [03-L9](../../claims.md)

**和 CAI 的区别**：CAI 编译「主张-证据叶子」省 token，没有 solver；Grid 编译「法规知识系统」做合规审查与 solver 调度。两者只共有「证据可追溯」；「数字不靠模型」只属于 Grid——CAI 无 solver，答案里没有 solver 计算的数字。

## F8

- **判断**：受监管支线的两个运行契约是 **记忆** 与 **决策点暂停**：记忆必须带 `kind/content/source/approved_by/version`，共享变更需人批准；决策点必须带 `decision_id/findings/citations/signer/timestamp`，未签核不继续。
- **等级**：`已核`（Grid digest §6.5 的接口契约；技术报告）。
- **条件**：记忆三类 semantic / procedural / episodic；暂停发生在人决策点，不是答案生成后。
- **反例/边界**：字段是工程配方，digest 未给实现细节与吞吐；人签核吞吐、审批延迟未量化。
- **来源**：[Grid digest](../../../../meta/audits/2026-11-11-source-purge.md#src-2611-03534) §3.1 · §6.5

## F9

- **判断**：strict pass 不是「答案对」，而是 **state_hash 一致 + study_type 匹配 + solver_version 已记录** 三者可核；study 工具输入带 `solver_config`、输出带 `solver_version/provenance`，solver 的容差/超时/版本按研究类型各自配置（digest 未给数值）。
- **等级**：`已核`（Grid digest §6.5；具体容差/超时数值 digest 未给）。
- **条件/数字**：N-1 / 潮流 / 短路 / OPF 各自配置；日志 `{task_id, tool_calls[], network_state_hash, study_type, solver_version, pass|fail, reason}`；516/519 工作被验证通过是结果，不是阈值。
- **反例/边界**：digest 不公布 solver 版本/容差；strict pass 是工作验证，不是形式安全证明；日志缺 `study_type` 或 `solver_version` 时只能判「不可核」，不能判 pass。
- **来源**：[Grid digest](../../../../meta/audits/2026-11-11-source-purge.md#src-2611-03534) §4.2 · §6.5

## F10

- **判断**：受监管支线的客户指标清单是 V3 假设：**申请周期、评审工时/单、返工率、审计发现数、每单加固成本、strict-pass 违规率**。当前唯一可用的量化项是 `每单加固成本` 的相对降幅——optimizer 让加固方案平均便宜 33–67%；周期、工时、返工率、审计发现数都没有基线。
- **等级**：`推测`（digest §6.6 明确标为 V2/V3 客户价值假设）；其中 optimizer −33–67% 是 `已核`（Table 5）。
- **条件/数字**：optimizer −33–67%（Table 5）；V3 建议单运营商 20–50 单、评审工时降 ≥20%、周期降 ≥10%、strict-pass 违规 0、citation precision ≥0.95（`推测`）。
- **反例/边界**：benchmark 单研究，没有 buy/do-nothing 对照；真实网络可达数万 buses；「每单加固成本」的代理只有 optimizer 的相对降幅，不是绝对金额。
- **来源**：[Grid digest](../../../../meta/audits/2026-11-11-source-purge.md#src-2611-03534) §4.2 · §6.6

## F11

- **判断**：法规答案的契约是 **每条法规结论带 citation，不能引用就拒答**；拒答阈值（证据不足/引用缺失的判定规则）必须配置并记录。45/51 是「正确拒答不可回答问题」的结果，不是阈值。
- **等级**：`已核`（Grid digest §4.1 表、§6.5 citation 与拒答阈值）；citation precision ≥0.95 是 V3/stop 配方（`推测`，见 F10）。
- **条件/数字**：citation `{doc_id, version, page, span, clause_id, retrieved_at}`；45/51 正确拒答；拒答阈值与 citation precision 0.95 是 digest 的工程配方，不是论文报告的实测值（`推测`）。
- **反例/边界**：digest 未给拒答阈值数值；45/51 是结果不是阈值；拒答率异常是 stop 信号，不是质量指标；只报 45/51 会把「拒答对」误读成「拒答阈值已校准」。
- **来源**：[Grid digest](../../../../meta/audits/2026-11-11-source-purge.md#src-2611-03534) §4.1 · §6.5
