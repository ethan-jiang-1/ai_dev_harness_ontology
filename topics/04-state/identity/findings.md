# 身份 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `identity/Fx`。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | registry 分层匹配 + 持久别名能把跨期观察锚到同一段历史 | 已核 |
| F2 | 在 registry + 语义兜底之上，alias 有已测增量；各层贡献未拆分 | 已核（增量）/ 推测（主增量） |
| F3 | false merge 的污染是机制推断，未测量；merge precision 要与 CMR 同看 | 推测（污染）/ 已核（precision） |
| F4 | 身份变更需要独立授权，不能由「可推理证据」直接放行 | 推测 |

## F1 · registry 锚定

- **判断**：固定 product–topic 本体 + 规范身份/持久别名；重复观察定向到同一段历史。
- **证据**：FIRME 4 settings；Full vs LLM-Norm（每期独立语义归一化、再跨期确定性匹配）CMR 2.3–3.7×；final-period Full CMR 30.4%（investor/Opus）、57.4%（S&P/Opus）。
- **边界**：没有「完全不做身份对齐」的对照组；LLM-Norm 也保留跨期确定性匹配，registry 本身的净效应未单独识别。专有金融数据；period 口径按数据集分开——investor calls 是 10 个月度 period，S&P 500 只有 3 个 reporting period（297 家公司、无结构化现金流），10 期衰减/季节性结论不能套到 S&P；单一本体。冷启动的前提是 alias 只从已出现过的 surface form 学、不从未来数据回填，否则 final-period 增益本身被泄漏污染（digest §6.5 契约；泄漏幅度未测）。
- **来源**：FIRME §5、Table 3；digest §4.1。

## F2 · alias 的增量（有条件）

- **判断**：在已有 canonical registry + 跨期语义兜底的对照上，持久 alias 带来可测增量；但 registry / alias / semantic fallback 的分别贡献未拆分。
- **数字**：final-period CMR +7.8–12.1 pp（4 个 dataset–backend 设置）；human-audit CMR +9.0–16.5 pp、reattachment recall +22.5–29.0 pp；semantic matching token −40.3%，总 token −7.2%。
- **条件**：no-alias 对照仍保留 canonical ID/name 匹配与语义 fallback（不是「无身份对齐」）；token 仅 investor calls × Opus × final period，不含 registry 构建。
- **含义**：alias 命中会跳过语义调用，是省钱机制；但「alias 是主增量」「钱不该花在更强匹配器」是推断，作者在 §7 自述未拆分这三层。`推测`
- **来源**：Table 3/4、§4.2、§7 Limitations；digest §4.1、§9。

## F3 · false merge 的污染是推断，未测量

- **判断**：alias 命中会把 surface form 挂到 anchor；一旦匹配错，后续同一 surface form 的出现**可能**被路由到错误历史。这是机制推断，论文没有测传播幅度，也没有自动回滚。
- **数字**：Full FIRME 的 human-audit merge precision 85.6–97.5%（4 settings）——这是**被接受匹配的正确率**，不是污染幅度；对应错误率约 2.5–14.4% 由该区间补算。
- **边界**：无长期污染测量；无回滚机制；precision 是抽样审计（200 units/setting），不是全量。digest 的 `merge precision <90% 停` 是**预登记停线**，不是已验证阈值：论文自己的 Full FIRME 就落在 85.6–97.5%，部分设置已低于 90%，所以这条线在目标域要重标，不能当「已核的安全边界」。
- **来源**：FIRME §5（「an incorrect registry match can therefore route later occurrences to the wrong anchor and history」）、Table A2；digest §4.1、§4.3、§6.5。

## F4 · 身份变更是 commit 问题

- **判断**：`UNVERIFIED` 可进推理，但不能授权 merge/split；需要 claim-specific promotion、冲突解决、scope/version 检查。
- **写侧最小字段**（原 Commit Boundary 2610.37407 §6.5，已移出；作字段设计参考）：证据带 `hypothesis_id` / `source_id`（判同源，防止 hypothesis 诱导的检索被当独立确认）与 `role: support|contradiction|unresolved`；promotion 带 `promoted_by` / `promoted_at`（审计谁批的）；verdict 带 `failed_claims[]` / `unresolved[]` / `scope_valid` / `versions_valid`（defer 理由可回放）。缺这些，事后既分不清 false merge 与同源自证，也答不出为什么 defer。`推测`（概念字段参考，原源已移出）。
- **失败模式与处置**（Commit Boundary 失败表，§6.5）：promotion 被绕过 → 拒 commit；scope/version 过期 → defer；部分提交（graph 与 evidence 不一致）→ 回滚；同源 lineage 误判 → 降级为 `UNVERIFIED`；policy 本身错 → 停，先修 policy。这是契约级处置，没有实现、没有触发率，不能当成本/效果数字。
- **等级**：`推测`（Commit Boundary 是概念架构，无实现）。
- **边界**：没有 false-defer 率；没有工程集成；promotion 正确性依赖外部标注。
- **来源**：Commit Boundary §3–5、§6.5；digest §3、§6.5。
