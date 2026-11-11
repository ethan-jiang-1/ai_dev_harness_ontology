---
status: draft
deliverable_status: draft
updated: 2026-11-11
position: evidence
evidence: [E-03]  # withdrawn
---

# evidence：产出带什么依据

> **2026-11-11 证据重置**：主锚 **E-03 已撤回**；本卡的 grounding 等级与效应量只作回查，不再作为 admitted 结论。
>
> **词源**：「接地（grounding）/ 接地等级 / 输出契约」是 `local` 工作词，没有标准锚（[规范主干 §4](../../../topics/trunk.md) 已列为缺口）；「约束 / 校验」有 `N: W3C SHACL`，但它定的是图约束，不是「输出带依据」。


> **一句话**：这是**输出契约**，不是判定器。它让「无根据」变成可见字段，但不阻断、不保证语义正确；等级是模型自评，不是形式证明。

**为什么不是相邻位置**：不是 checker（checker 判对错，evidence 只带字段）；不是 context（输出时，不是供给）。

## 1. 机制

模型生成结论时，输出被要求带两类东西：

| 字段 | 内容 | 作用 |
|---|---|---|
| `observations[]` | 所用到的本体观察：concept card、`ASK` 结论、`SELECT` bindings | 让结论可追溯 |
| `grounding` | 观察与答案的关系：`entailed` / `supported` / `related` / `unrelated` | 给可靠性一个可排序字段 |

四个等级的边界：

| 等级 | 含义 | 不能读成 |
|---|---|---|
| `entailed` | 可由观察中的事实逻辑推出 | 形式证明 |
| `supported` | 观察 + 参数知识可合理推断 | 严格逻辑后承 |
| `related` | 观察相关，但不足以确定答案 | 支持 |
| `unrelated` | 有观察，但与问题/答案无关 | 「没检索到」 |

OA-RAG 的实际做法：`DESCRIBE` 取 concept card，`ASK` 问 reasoner 是否 entailed（Not Entailed ≠ false，开放世界），`SELECT` 检索；精确查询空结果走 BM25 fallback；E=∅ 时走 `P_own`，**不报 grounding**。`withdrawn`（原 E-03）

## 2. 触发、输入、输出

| 项 | 内容 |
|---|---|
| 触发 | 答案生成/Answering 阶段；判定尚未发生 |
| 输入 | 问题、本体观察、reasoner/SPARQL 结果 |
| 输出 | `{answer, observations[], grounding}`；E=∅ 时没有 grounding 字段 |
| 下一步 | 读者/下游按等级分流；是否放行由 checker/人决定 |

## 3. 能改变什么

- **旧观察里整体准确率更优。** 旧设计是「几个大本体 + 六个医学 QA 任务 + 2 个 backbone」，相对文本 RAG 有增益；具体数值随 E-03 撤回停用。`withdrawn`（原 E-03）
- **同预算下曾显示可比。** 旧观察在固定上下文预算下对比了 i-MedRAGdoc；具体分数随 E-03 撤回停用。`withdrawn`（原 E-03）
- **把三种情况分开。** 没有可用观察（E=∅）、检索到但不足以定答案（`related`）、检索到但无关（`unrelated`）；这是字段设计的价值，论文未把「可审计」单独量化。`已核`（机制）/ `推测`（可审计收益）
- **预算可记（设计）。** 旧协议给了 tool actions / generated tokens 上限，以及实测调用与 token 均值；具体数值随 E-03 撤回停用。`withdrawn`（原 E-03）

## 4. 拦不住什么 / 失效模式

| 失效 | 说明 | 证据/等级 |
|---|---|---|
| 等级自评 | 模型给自己打分；作者明确不提供形式正确性保证 | `withdrawn`（原 E-03） |
| 等级未校准 | entailed/supported 的 precision/recall 未知；旧切片数字随 E-03 撤回停用 | `withdrawn`（原 E-03） |
| 等级通胀 | 全标 supported，字段存在但无区分度 | `推测`（论文给了分布，未测校准） |
| 引用形式化 | 引用了观察，但结论与观察无关 | `推测`（论文未单列测量） |
| 检索可能是主瓶颈 | 旧观察里 gold evidence 完整检索后 MCQ/OQ 差距很大；具体数值停用 | `withdrawn`（原 E-03） |
| 无句级 span | 观察是整卡/ASK 结论/bindings 级引用 | `withdrawn`（原 E-03） |
| 格式开销 | 每条结论带证据会增加输出 token；论文未单列 | `推测` |

## 5. 使能条件

- 有 OWL reasoner / SPARQL endpoint；只有 concept card 会向普通文本 RAG 靠拢；
- 问题在本体覆盖内；未知 IRI 高时先补本体；
- 答案不是主要靠文本阅读/计算；
- 需要可审计依据，但**不需要形式正确性保证**；要形式保证直接用 reasoner。

## 6. 证据与边界

| 证据 | 等级 | 支持什么 | 不能证明什么 |
|---|---|---|---|
| E-03 | **withdrawn** | 输出契约的整体准确率；四等级；预算；检索瓶颈 | 形式保证；等级校准；句级 span；跨预算效率 |

> **历史**：旧 E-03 有两套预算口径（小/大上下文），不可直接对照；E-03 撤回后数值停用。`withdrawn`

## 7. 可证伪条件

- 给 grounding 等级做独立标注后，等级与正确率的排序不成立 → 收窄「等级可排序」；
- gold evidence 完整检索后，契约相对纯文本 RAG 的增益消失 → 说明增益主要来自检索，不是契约；
- 强制契约后，无依据输出的比例显著下降且不是模型自述 → 支持「契约能约束输出」；
- 句级 span 版本带来额外审计收益 → 扩大契约的粒度。

## 8. 上游指针

- 机制：[evidence/mechanism](../../../topics/02-judgment/evidence/mechanism.md)
- 判断：[02-judgment/README](../../../topics/02-judgment/README.md) · [conclusions](../../../topics/conclusions.md) E-03
- 施工：[02 R4（recipes）](../../02-engineering-playbook/recipes/README.md) · [01 能力 4](../../01-capability-status/sections/map.md#22-一张表)
- 长版论证：[附录 §3.4.3](../appendix-constraint-spectrum.md#343-evidence输出时的证据契约)
