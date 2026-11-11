---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# 附录 B · 追溯表：R → E → mechanism → 边界

> 每个 R 至少有一条 E、一个 mechanism 页、一个明确的「不能证明」。没有孤儿 recipe；没有只靠交付物新增的判断。
>
> **2026-11-11 证据重置**：R4/R5/R6/R12 的主 E 已撤回/移出，评级改 **gap**；本表保留旧行只作追溯，不再表示“可试点”。

## 1. 主表

| R | 主 E | mechanism / 主题页 | 关键限定 | 01 评级 | 不能证明 |
|---|---|---|---|---|---|
| R0 准入 | E-12/E-20；E-02/E-03 撤回 | 工程建议；原 SFE-O/checker F2 移出 | 检查项是工程配方（`推测`） | 前置 | 通过 R0 ≠ 有效 |
| R1 K1 | E-12 | [projection](../../../topics/03-knowledge/projection/mechanism.md) | 单工厂/9 任务/答案在文本 | A | 跨域增益 |
| R2 投影 | E-12 | 同上 | 单 plant；排序非普适；顺序敏感 | B | 开放域/多设备；手工 SOP 对照 |
| R3 编译 | E-08/E-14 | [compilation](../../../topics/03-knowledge/compilation/mechanism.md) | FRAMES；单 compiler；时延 3× 仅 7 题 | B | 准确率提升；企业语料 |
| R4 证据 | E-03 withdrawn | [evidence](../../../topics/02-judgment/evidence/mechanism.md) | 旧数字停用 | **gap** | 形式保证；跨域 |
| R5 checker | E-02 withdrawn；E-20 代码级 | [checker](../../../topics/02-judgment/checker/mechanism.md) | 旧数字停用 | **gap** | 语义正确；真实错误分布 |
| R6 动作闸 | E-04/E-13 withdrawn；E-15 参照 | [action-gate](../../../topics/01-constraint/action-gate/mechanism.md) | 旧数字停用 | **gap** | 结构有效；安全保证 |
| R7 记忆 | E-05/E-17 | [identity](../../../topics/04-state/identity/mechanism.md)、[memory](../../../topics/04-state/memory/mechanism.md) | 专有数据/文本 only/需训练信号 | B | 跨模态；false merge 传播 |
| R8 读路径 | E-20 | [commit-gate F5–F7](../../../topics/01-constraint/commit-gate/findings.md)、[trustgraph](../../../src/open-source/trustgraph-ai-trustgraph/digest.md) | fail-open；subject-only；单实现（候选第二实现未入库） | B（条件性） | 写授权；object 方向；可上线 |
| R9 落盘 | E-20 | [commit-gate](../../../topics/01-constraint/commit-gate/mechanism.md) | 概念；无实现；false-defer 未测 | C | 已落地；效果 |
| R10 离线 SHACL | E-20 | [semantica](../../../src/open-source/semantica-agi-semantica/digest.md)、[open-ontologies](../../../src/open-source/fabio-rovai-open-ontologies/digest.md) | CLI；未跑通；派生 shapes 未测 | A | in-loop 自动拒收；语义正确 |
| R11 OBDA | E-20 | [ontop](../../../src/open-source/ontop-ontop/digest.md) | OWL 2 QL；无 agent 集成；无消融 | A | 本体独立贡献；DL 推理 |
| R12 受监管 | Grid 已移出（非 E） | [compilation 机制三](../../../topics/03-knowledge/compilation/mechanism.md) | benchmark 已移出 | **gap** | 客户指标；形式安全 |

> R12 的唯一 benchmark 已移出；现在没有 admitted 来源，不能当 E 引用。R0 也没有单一 E；它是工程建议，旧 E-02/E-03 已撤回。

## 2. 与 01 的 crosswalk

| 01 能力 | 02 recipe | 一致性 |
|---|---|---|
| K1 | R1 | A ↔ A |
| 投影 | R2 | B ↔ B |
| 编译 | R3 | B ↔ B |
| evidence | R4 | **gap ↔ gap** |
| checker | R5 | **gap ↔ gap** |
| 动作闸 | R6 | **gap ↔ gap** |
| 记忆 | R7 | B ↔ B |
| 读路径 | R8 | B ↔ B（条件性；单实现） |
| 落盘授权 | R9 | C ↔ C |
| OBDA | R11 | A ↔ A |
| 离线 SHACL | R10 | A ↔ A |
| 推理期 | 不写成 R；见 §4 | C ↔ C |
| 审批/多模式 | R6 的可选节 | C ↔ C |
| 确定/多智能体 | 不写成 R；见 §4 | C/空白 |

## 3. 与 03 的 crosswalk

- 六位置：R1–R5 对应 context/evidence/checker；R6/R8/R9 对应 action/read-path/commit；R7 对应 memory；R10/R11 对应 checker/supply。
- 三轴：R 的「接缝/形态」必须与 [seams](../../../topics/seams.md)、[execution-forms](../../../topics/execution-forms.md) 一致；不一致时以 topics 为准，回改 02。
- 强度–覆盖率反向是组织假设（非 E）；02 不把它写成证明。

## 4. 不写成 recipe 的三件事

| 事项 | 为什么 | 去哪 |
|---|---|---|
| 推理期条件闸（E-16） | 模拟、固定 schema、无真实工厂；与 action-gate 边界未稳 | [reasoning-gate](../../../topics/01-constraint/reasoning-gate/mechanism.md)；01 C |
| 跨运行确定性 | 只有设计提案，无实现/度量 | [determinism](../../../topics/04-state/determinism/mechanism.md)；01 C |
| 多智能体共享本体 | 无可判定设计/证据；00-harness 唯一空白 | [orchestration](../../../topics/00-harness/orchestration.md)；01 C/空白 |

## 5. 孤儿检查

- 每个 R 都有 E + mechanism + 限定 + 不能证明。
- 02 不引 L-xx；需要局部判断时回 topics 的 claims，升 E 后才进交付物。
- 新增/修改 R 时，先改本表，再改正文；本表是「没有孤儿」的机器可查清单。

**出处**：[conclusions](../../../topics/conclusions.md) · [01](../../01-capability-status/README.md) · [03](../../03-mechanism-reference/README.md)
