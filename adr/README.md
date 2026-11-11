---
status: draft
updated: 2026-11-12
---

# 结构决策（ADR）

> 这里是“为什么长成这样”，不是“现在是什么”。现行规则见 [meta/README](../meta/README.md)，当前状态见 [meta/state](../meta/state.md)。

| 编号 | 决策 | 一句话 |
|---|---|---|
| [0001](./0001-research-repo-over-code.md) | 以文档为主要交付物，而非代码仓 | 验证性实现放仓库外，靠 `EXP-xxx` 回链 |
| [0002](./0002-three-axes.md) | 以派为主轴，时刻与部件作横切索引 | 派是稳定综合单元；时刻不建目录 |
| [0003](./0003-subtopics-and-source-types.md) | 子主题第二层，素材类型留在 `src/` | 子主题按子机制，不按来源类型；薄页有纪律 |
| [0004](./0004-open-source-source-type.md) | 新增第三类源材料 open-source | 不 vendor，pin commit，代码是一手原文 |
| [0005](./0005-repo-self-check.md) | 允许 `meta/tools/` 的只读自检 | 文档纪律需要可执行的门，不是代码仓 |
| [0006](./0006-execution-form-axis.md) | 增加执行形态轴 | 位置与形态正交；形态不建目录，建横切页 |
| [0007](./0007-no-external-asset-gate.md) | 不设外部资产前置 | 删除 D0/试点线；agent 不得自行创造人类前置 |
| [0008](./0008-thin-subtopics-merge-audit.md) | 薄子主题合并审计 | 15 个薄页本轮不合并；给出门槛与下轮复核点 |
| [0009](./0009-object-layer.md) | 证据对象层（O-xx） | 交付物可引 O 作地址、主句仍落 E；**已接受（方案 A）** |
| [0010](./0010-three-layer-information-flow.md) | 三层信息流 | `src` 给 Agent 干货、`topics` 给 Agent+人判断、`deliverables` 给人成品；主路径自包含 |
| [0011](./0011-source-standing-and-term-baseline.md) | 源位阶与术语基线 | `normative` 定词、`informative` 佐证；术语定义不许引资料性源 |
| [0012](./0012-instruction-layer-single-home.md) | 指令层单一出处与常设修复回路 | AGENTS 唯一路由；规则一个家；判断顺流、证据逆流；_plans 现行唯一 |

**新增 ADR 的判据**：改变目录/层级/字段契约，或引入新的源类型/验证方式。只改内容判断，不写 ADR。
