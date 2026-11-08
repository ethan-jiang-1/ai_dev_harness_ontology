# 全审（Full Audit）

> **目的不是让 digest 更漂亮，而是确保它能被 topics 吸收成会影响实施的判断，并最终对客户价值负责。**

## 当前状态

- 状态：**Phase 1 进行中**（Phase 0 完成；MIOE E3、CAI E4、CASEL E3、N&D E3、Ontology Catch E4、FIRME E4；Phase 1 **22/22 E3+，12/12 L3 E4**；Phase 2 **A4 20/20**；G-X **20/20 pass**；跨页回写完成；Phase 3 V3 8 个；Phase 4 抽样 digest 2/5、topic 5/5；[report](./report.md) 为**条件 go（内部试点）/ 对外 no-go**；[human-review](./human-review.md) 已由用户授权 AI 代办（非独立人类）；6 派 status 在 [subdomains](./subdomains/README.md)）。
- 范围：22 篇 digest、20 个子主题、6 派 README、conclusions/THESIS/feasibility、sources。
- 方法：E0–E4（digest 工程度）、A0–A4（topic 吸收度）、V0–V3（价值链）；**全量 22/22 + 20/20**，不抽样；AI critic 全审 + 人类抽检。
- 入口：[plan.md](./plan.md)。

## 为什么单独建目录

- 它不是某个研究主题，不能塞进 `topics/`；也不是一次性报告，不能只放 `meta/` 根下。
- 它会产生自己的 ledger、critic log、value trace 和 report；放在 `meta/full-audit/` 便于持续迭代，不污染 `meta/` 的通用约定。
- 与 [quality-plan](../quality-plan.md) 的关系：quality-plan 管“结构/自包含/一致性”；full-audit 管“工程可实施性 + topics 吸收 + 客户价值”，是更严的一层。

## 文件

| 文件 | 作用 | 何时建 |
|---|---|---|
| [plan.md](./plan.md) | 完整计划、量表、流程、验收 | 现在 |
| `digest-ledger.md` | 22 篇 digest 的 E0–E4 审计 | Phase 1 |
| `topics-ledger.md` | 20 个子主题的 A0–A4 审计 | Phase 2 |
| `value-trace.md` | V0–V3 价值链与实施假设 | Phase 3 |
| `critic-log.md` | 独立 critic 的问题与修正 | Phase 4 |
| `report.md` | 最终报告与 go/no-go | Phase 5 |

不预建空文件；每个文件在对应 Phase 开始时创建。

## 开始条件

用户确认计划后，再 setup goal；本轮只交付计划。
