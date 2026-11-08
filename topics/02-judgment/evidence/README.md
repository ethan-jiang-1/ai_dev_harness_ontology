---
status: draft
updated: 2026-11-08
rq: [RQ2, RQ4]
evidence: [E-03]
---

# 输出时证据契约

> 模型生成结论时。判定尚未发生，但输出格式已被约束：每个结论必须附带依据，以及依据与本体的关系强度。这里不负责输出后的 checker（[checker](../checker/README.md)）。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 8 条（F1–F3 论文结论，F4–F7 复刻配方，F8 预算口径）（[findings](./findings.md)） |
| 未发现 / 开放 | 5 条（[frontier](./frontier.md)） |
| 下一步 | 2 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 输出时的证据/接地等级；不含输出后的 checker 与推理期约束 |

## 当前判断

- **显式接地等级平均最优，但有例外。** 强制报告本体观察 + entailed/supported/related/unrelated，在三个本体、六个医学 QA 任务上平均优于文本 RAG；Test 2 MCQ Llama 52.2 vs RAGont(text) 53.4、Test 2 OQ Qwen 23.2 vs ReActont 32.9。`已核`
- **等级是模型自评，不是保证。** OA-RAG 自己写明「不提供形式正确性保证」；等级与正确率同向，但未校准。`已核`
- **检索是主瓶颈。** gold evidence 完全检索 MCQ 61.7% vs OQ 23.6%；检索到后 MCQ 95.1–98.4% 被引用。`已核`
- **可复刻的是接口 + 预算 + 覆盖门，不是一张卡。** 三查询原语（DESCRIBE/ASK/SELECT）、concept card 固定字段、name linking/BM25 fallback 见于论文正文；论文给的预算上限是 10 tool actions + 5,000 generated tokens（Answer Step 2 另 512，附录 A）。未知 IRI >20% 停、1–2 人日/本体与 1–2 人周 reasoner 集成是 digest 的工程配方与估算，论文未测（`推测`；接口/预算 `已核`）。详见 [findings F4–F8](./findings.md)。
- **V1 受益者/痛点（`推测`）。** 受益者是医学/生物本体问答产品；痛点是答案无依据/不可审计、术语歧义、检索失败与推理失败分不开。详见 [mechanism · 客户价值](./mechanism.md)。

## 文件地图

| 想知道 | 去 |
|---|---|
| 四个等级/为什么有用/失效 | [mechanism](./mechanism.md) |
| 接口字段、调用预算、name linking 参数 | [mechanism · 接口与预算](./mechanism.md) · [findings F4/F5/F8](./findings.md) |
| 成本、stop condition、客户价值（V1–V3） | [mechanism · 实施与客户价值](./mechanism.md) · [findings F6/F7](./findings.md) |
| 何时别用（无 reasoner/SPARQL、超出覆盖、文本阅读/计算为主） | [mechanism · 何时别用](./mechanism.md) |
| 八条判断的证据/数字 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始论文 | `src/papers/2610.36335-oa-rag/` · [digest](../../../src/papers/2610.36335-oa-rag/digest.md) |

## 边界

- **不是形式保证。** 等级是模型自评；不能当自动放行依据。
- **不是输出后判定。** 它约束输出的格式与证据声明；是否放行仍由 checker/人决定。
- **不解决检索覆盖。** 过滤后 E=∅ 时走 `P_own`、不报 grounding，也不能补内容；`unrelated` 只表示「有观察但与问题/答案无关」，不是「没检索到」。
- **没有文本 span。** 观察是整卡/ASK 结论/查询绑定级别的引用；句级定位是缺口（[frontier G3](./frontier.md)）。
- **不同 context 预算不可直接比。** 8,192 是论文全方法统一口径；96.7k tokens/22 calls 是 i-MedRAGdoc 在 262k 下的加报，不是 8k 同预算对照；32k 论文未测（digest 的外推，`推测`）。见 [findings F8](./findings.md)。
- **前提不满足就别上。** 没有 OWL reasoner/SPARQL endpoint、问题超出本体覆盖、答案主要靠文本阅读/计算、需要形式正确性保证时，机制不成立（方法依赖 `已核`；选型判断 `推测`）。详见 [mechanism · 何时别用](./mechanism.md)。

## 关联

- 派：[02 判定](../README.md) · 结论：[E-03](../../conclusions.md)
- 相邻：[checker](../checker/README.md) · [03 知识 projection](../../03-knowledge/projection/README.md)
- 成本：[06-measure/feasibility](../../06-measure/feasibility/README.md)
