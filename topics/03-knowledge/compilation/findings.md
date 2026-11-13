# 编译 · 发现（F）

> 只放**已经能站住**的判断。每条带等级、条件、反例/边界、来源。
> `F` 编号是子主题局部编号；跨页引用写 `compilation/Fx`。

## 索引
> **2026-11-13 对账**：F5 / F8–F11 来源于 Grid Agents（2611.03534，已移出），已与 README 同步降为 `推测（源已撤回）`；F1–F4 / F6–F7 来源于 CAI（E-14 admitted），保持 `已核`。


| ID | 判断（一行） | 等级 | 详细 |
|---|---|---|---|
| F1 | 强 harness 下结构化工件不增加准确率；PageIndex 在 FRAMES 规模为负 | 已核 | [F1](./findings/accuracy.md#f1) |
| F2 | claim-leaf 的 token 收益是条件性的：−91%/+1.9%/−38% | 已核 | [F2](./findings/economics.md#f2) |
| F3 | 有限视野 `p_min=2%+c/(0.929Q)`；省 token 用轮次/时延换；E3 gate arm −52%/−30%、140→30 s | 已核 | [F3](./findings/economics.md#f3) |
| F4 | 本体在 CAI 里未被测量；部署价值是作者主张，ledger 无一行达标 | 已核 | [F4](./findings/deployment.md) |
| F5 | 受监管知识系统：证据引用 + solver + 人；对最强 agent baseline 仅 +0.5pp | 推测（源已撤回） | [F5](./findings/regulatory.md#f5) |
| F6 | 「compile evidence, not prose」：结构不增加证据，叶子带证据才有用 | 已核 | [F6](./findings/accuracy.md#f6) |
| F7 | 盈亏平衡的不确定性由 miss penalty 主导：先量 miss | 已核 | [F7](./findings/economics.md#f7) |
| F8 | 受监管支线：记忆与决策点暂停的契约 | 推测（源已撤回） | [F8](./findings/regulatory.md#f8) |
| F9 | strict-pass = state_hash + study_type + solver_version | 推测（源已撤回） | [F9](./findings/regulatory.md#f9) |
| F10 | 受监管客户指标：V3 假设；只有加固成本 −33–67% 有数 | 推测（源已撤回） | [F10](./findings/regulatory.md#f10) |
| F11 | 法规答案的引用/拒答契约：每条结论带 citation，不能引用就拒答；45/51 是结果不是阈值 | 推测（源已撤回） | [F11](./findings/regulatory.md#f11) |

## 怎么读

- 想看**机制**：去 [mechanism.md](./mechanism.md)。
- 想看**缺什么/下一步**：去 [frontier.md](./frontier.md)。
- 想看**原始论文**：CAI 见 `src/papers/2610.41172-context-as-infrastructure/`；Grid Agents（2611.03534）已于 2026-11-11 移出，见 [清除审计](../../../meta/audits/2026-11-11-source-purge.md#src-2611-03534)。
