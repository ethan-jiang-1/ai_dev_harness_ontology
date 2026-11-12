> **历史快照（2026-11-08/09）**：已归档，不再维护。现行规则见 `meta/README.md`，当前状态见 `meta/status/state.md`。文中的计数与结论可能已被后续修复取代。

# digest → topic 吸收矩阵（G-X）

> 目的：回答“digest 的工程发现有没有真的进 topics 的判断/claims”，而不是两层各自合格。
> 状态：`absorbed` / `partial` / `orphan` / `explained-not-applicable`。Phase 2.5 逐行修到 22/22。

| D-ID | digest | 工程发现（E3/E4 新增） | 被哪些 topic 吸收 | 状态 | 动作 |
|---|---|---|---|---|---|
| D-01 | MIOE | 接口/训练参数/数据 pair/成本/stop/first sprint/V3 | [06/mechanism](../../../../topics/06-measure/mechanism/README.md) 的 F1–F5；成本/stop 未进 topic | G-X pass | G-X pass |
| D-02 | CAI | 工具 schema/topN/k/p_h 分离/c/φ 测法/stop/sprint/V3 | [03/compilation](../../../../topics/03-knowledge/compilation/README.md) 的成本/盈亏；00/context | G-X pass | 补接口/参数/φ 到 compilation 的 mechanism |
| D-03 | POLAR | Layer A/B、反向搜索、成本/stop/shadow/V3 | [01/action-gate](../../../../topics/01-constraint/action-gate/mechanism.md) 实施/客户价值 | G-X pass | 补 E4 成本/ESCALATE 人时到 findings |
| D-04 | N&D | 投影序列化/工具接口/rubric/stop/sprint/V3 | [03/projection](../../../../topics/03-knowledge/projection/README.md) 机制/发现 | G-X pass | G-X pass |
| D-05 | Ontology Catch | checker 接口/参数/成本/stop/部署度量/V3 | [02/checker](../../../../topics/02-judgment/checker/mechanism.md) 实施/客户价值 | G-X pass | G-X pass |
| D-06 | CASEL | 控制器/γ 标定/校准/c_base/stop/E4 公式/V3 | [01/action-gate](../../../../topics/01-constraint/action-gate/mechanism.md) 实施 | G-X pass | 把 γ_m 标定/审批成本写进 findings |
| D-07 | FIRME | registry/edge schema/match 契约/$100K/stop/冷启动/V3 | [04/memory](../../../../topics/04-state/memory/README.md)、[04/identity](../../../../topics/04-state/identity/README.md) | G-X pass | G-X pass |
| D-08 | OntoAct | condition/axiom/hypothesis/verify/stop/sprint/V3 | [01/reasoning-gate](../../../../topics/01-constraint/reasoning-gate/mechanism.md) 实施 | G-X pass | 补覆盖率/stop 到 findings |
| D-09 | SLB | placeholders 契约/codebook/样本量/stop/V3 | [06/trace](../../../../topics/06-measure/trace/README.md) 机制/发现 | G-X pass | 把 codebook/placeholders 写进 mechanism |
| D-10 | Grid | citation/study/strict-pass/memory/pause/stop/V3 | [03/compilation](../../../../topics/03-knowledge/compilation/mechanism.md) 受监管段 | G-X pass | 补接口/参数/stop 到 compilation |
| D-11 | Diagnose | case table/repair trace/intent gate/stop/sprint/V3 | [06/failure-attribution](../../../../topics/06-measure/failure-attribution/README.md) | G-X pass | 把 schema/stop 写进 mechanism |
| D-12 | OntoDoc | prompt/ASK 校验/schema/发布闸门/stop/V3 | [05/generation](../../../../topics/05-produce/generation/README.md) | G-X pass | 把 ASK/发布闸门写进 mechanism |
| D-13 | OA-RAG | concept card/工具/预算/stop/sprint/V3 | [02/evidence](../../../../topics/02-judgment/evidence/mechanism.md) 实施 | G-X pass | 补预算/stop 到 findings |
| D-14 | Commit Boundary | mutation/q_m/promotion/两阶段/失败表/stop | [01/commit-gate](../../../../topics/01-constraint/commit-gate/mechanism.md) 实施 | G-X pass | 补 false-defer 到 findings |
| D-15 | Multi-agent | 确定性评分/角色/追问/stop | [01/reasoning-gate](../../../../topics/01-constraint/reasoning-gate/README.md)、06/failure | G-X pass | 把评分/追问接口写进 reasoning mechanism |
| D-16 | EvoMemState | facts/relational/reasoning schema/GRPO/stop | [04/memory](../../../../topics/04-state/memory/README.md) | G-X pass | 把 schema/GRPO/stop 写进 mechanism |
| D-17 | Agents | 五轴/54% 方差/GAP_CLOSED/验证工具 | [06/metrics](../../../../topics/06-measure/metrics/README.md) | G-X pass | 把配置轴/方差写进 metrics mechanism |
| D-18 | CASTON | 两阶段/embedding/confidence/stop | [05/refinement](../../../../topics/05-produce/refinement/README.md) | G-X pass | 把阈值/召回边界写进 findings |
| D-19 | Peeling | 编码器/探针/DAG I/O/stop | [05/generation](../../../../topics/05-produce/generation/README.md) | G-X pass | 把参数/I/O 写进 mechanism |
| D-20 | Evontree | 3.1/3.7%、ConfirmValue/τ*/规则/LoRA/安全 | [05/generation](../../../../topics/05-produce/generation/README.md)、[05/lifecycle](../../../../topics/05-produce/lifecycle/README.md) | G-X pass | 重写 generation 的 Evontree 段与 lifecycle 证据 |
| D-21 | SFE-O | schema/SHACL/外部服务/stop | [05/representation](../../../../topics/05-produce/representation/README.md) | G-X pass | 把 schema/SHACL 写进 representation |
| D-22 | ReX-GG | JSON schema/匿名互评/去偏/stop | [05/generation](../../../../topics/05-produce/generation/README.md) | G-X pass | 把互评算法写进 generation mechanism |

## 反向检查（Phase 2.5 填）

| T-ID | topic | 核心判断 | digest 来源 | 无来源 claim | 状态 |
|---|---|---|---|---|---|
| T-01 | 01/action-gate | 结构判据/能力反向/多模式前沿 | D-03/D-06 | — | 待核 |
| T-02 | 01/commit-gate | 推理≠授权/同源不确认 | D-14 | — | 待核 |
| T-03 | 01/reasoning-gate | 验证条件 vs 限制知识源 | D-08/D-15 | — | 待核 |
| T-04 | 02/checker | 三源权衡/空结果基线 | D-05 | — | 待核 |
| T-05 | 02/evidence | grounding 自评/检索瓶颈 | D-13 | — | 待核 |
| T-06 | 02/calibration | 漏检/误报/ECE | D-05/D-13 | — | 待核 |
| T-07 | 03/compilation | 编译只省预算/成本条件 | D-02/D-10 | — | 待核 |
| T-08 | 03/projection | 投影>查询/答案在文本里 | D-04 | — | 待核 |
| T-09 | 04/memory | 状态非事实集/会用>检索 | D-07/D-16 | — | 待核 |
| T-10 | 04/identity | 身份先于内容/false merge | D-07/D-14 | — | 待核 |
| T-11 | 04/determinism | 漂移=输入不完备 | D-16 | — | 待核 |
| T-12 | 05/generation | 生成是候选/可消费性缺 | D-12/D-19/D-20/D-22 | — | 待核 |
| T-13 | 05/refinement | 定位/验证瓶颈 | D-18 | — | 待核 |
| T-14 | 05/representation | 表示按消费位置 | D-21 | — | 待核 |
| T-15 | 05/lifecycle | 来源/演化/回滚 | D-20 | — | 待核 |
| T-16 | 06/mechanism | 可干预但部分分离 | D-01 | — | 待核 |
| T-17 | 06/failure-attribution | 失败归工作流 | D-11/D-15 | — | 待核 |
| T-18 | 06/trace | 输出正确掩盖过程 | D-09 | — | 待核 |
| T-19 | 06/metrics | 度量错配 | D-17 | — | 待核 |
| T-20 | 06/feasibility | 位置×成本×使能 | D-02/D-03/D-06 | — | 待核 |