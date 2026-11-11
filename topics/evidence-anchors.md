---
status: draft
updated: 2026-11-11
scope: evidence-anchors
---

# 证据锚：E 行的承重数/条件与 digest 节

> **这是什么**：`conclusions.md` 的 E 行是摘要；交付物引 E 时，具体数字/条件常在 digest。本页给每条承重 E 一个「承重数/条件 + digest 节」锚，供交付物引用与读者核对。
>
> **不是什么**：不是新 E，不改 E 的判断；只是地址层。E 行仍是主句，本页只回答「这个数在哪一节、带什么条件」。
>
> 用法：交付物写「E-xx（[锚](./evidence-anchors.md)）」；不要复制本页的数，改数先改 E/ digest。
>
> **效果（EXP-004b）**：同一 20 条 claim，只引 E 行时 strict support 5/20（25%）；加本页锚后 11–13/20（55–65%），N 从 2 降到 0。剩下的 P 多是「处方/解释」，不是缺数——那些应标 `工程建议/推测`，不要挂 E。

## E-01

- **承重数/条件**：强检索 harness 下，被测量的摘要树/大纲/wiki/实体图在 FRAMES 上无准确率增益；PageIndex 大纲退化；ontology `not measured`；单基准、单类工件。
- **digest 节**：[CAI §4 结果](../src/papers/2610.41172-context-as-infrastructure/digest.md#4-结果数字与条件)
- **不能证明**：本体无增益；可外推到所有工件。
- **适用**：01 boundaries §4.2/§4.3；02 R1/R2 的边界。

## E-02

- **承重数/条件**：curated / data-derived / masked 三来源 catch/FA 各有偏向；空结果重试是关键基线；curated precision 仅略优于随机；judge 修坏多于修好。
- **digest 节**：[Ontology Catch §3.6 空结果基线](../meta/audits/2026-11-11-source-purge.md#src-2610-37809) · [§4 结果](../meta/audits/2026-11-11-source-purge.md#src-2610-37809)
- **不能证明**：部署 precision；false-veto；跨域；语义错。
- **适用**：02 R5；01 E4；03 checker。

## E-03

- **承重数/条件**：强制接地等级平均最优；Tests 1–2 +10–15pp；等级是模型自评；检索是主瓶颈；三个大本体、六个医学 QA、2 个 backbone。
- **digest 节**：[OA-RAG §4 结果](../meta/audits/2026-11-11-source-purge.md#src-2610-36335)
- **不能证明**：形式保证；等级校准；句级 span。
- **适用**：02 R4；01 E4；03 evidence。

## E-04

- **承重数/条件**：18 个模型-域组合仅 8 个改善；retail/强模型回退；T1-only ≈ blanket veto；false-veto 未测；τ=0.80 下 airline 只保留 36.6% 候选动作。
- **digest 节**：[POLAR §4 结果](../meta/audits/2026-11-11-source-purge.md#src-2610-08082)
- **不能证明**：结构判据有效；reward 低估；合法意图误拦。
- **适用**：01 E5；02 R6；03 action。

## E-05

- **承重数/条件**：alias CMR +7.8–12.1pp（4 settings）；reattachment recall +22.5–29.0pp；human-audit CMR +9.0–16.5pp；token −40.3%；专有数据、3 periods。
- **digest 节**：[FIRME §4 结果](../src/papers/2610.40482-firme/digest.md#4-结果数字与条件)
- **不能证明**：长期污染；跨运行；通用域；registry 净效应。
- **适用**：01 E6；02 R7；03 memory。

## E-08

- **承重数/条件**：证据充分时 −91% token；不充分时 +1.9%；平均 −38%；准确率 neutral；只测 navigation tree；FRAMES 规模。
- **digest 节**：[CAI §4 结果](../src/papers/2610.41172-context-as-infrastructure/digest.md#4-结果数字与条件)
- **不能证明**：准确率提升；无条件省 token；本体形态。
- **适用**：02 R3；01 E3；03 context 的编译。

## E-12

- **承重数/条件**：K1 +54.6pp；K2 +19.8pp；0.777/0.717/0.638/0.597；GLM JSON 0.900 > 文本 0.891；Qwen 工具 0.407 < 文档 0.538；单工厂、9 任务、45k 字符、答案写在文本里。
- **digest 节**：[N&D §4 结果](../src/papers/2610.11768-narrow-and-deep/digest.md#4-结果数字与条件)
- **不能证明**：跨域；多设备；顺序迁移；本体归属性。
- **适用**：01 E1/E2；02 R1/R2；03 context。

## E-13

- **承重数/条件**：斜率 −0.76/−0.67/−0.31；R² 0.92/0.98/0.65；六点描述性拟合，不是预测曲线。
- **digest 节**：[POLAR §4 结果](../meta/audits/2026-11-11-source-purge.md#src-2610-08082)
- **不能证明**：零交叉阈值；预测曲线；因果。
- **适用**：01 E5 的边界；03 action。

## E-18

- **承重数/条件**：54% 方差来自重复同一配置的 run-to-run；配置当系统变量；信息 > 模型/预算。
- **digest 节**：[Agents are Systems §4.1 方差](../src/papers/2610.01618-agents-are-systems/digest.md#41-方差)
- **不能证明**：本体增益；跨域常数；排除 memory/multi-agent。
- **适用**：03 measurement；M1 的噪声地板。

## E-20

- **承重数/条件**：engine 至少四种语义；trustgraph fail-open、只删 subject；semantica 派生 SHACL + pyshacl；ontop OWL 2 QL 重写；open-ontologies 0/2/3 且 exit code 折叠；31 条单测。
- **digest 节**：[execution-forms §代码级核对](../topics/execution-forms.md#代码级核对2026-11-09) · [trustgraph §3–§6](../src/open-source/trustgraph-ai-trustgraph/digest.md)
- **不能证明**：效应量；形态改变行为；所有实现。
- **适用**：01 E7/E8；02 R8/R10/R11；03 execution-forms。

## 维护

1. 新增一条承重 E：先有 digest 节，再加本页；没有节就写 `gap`。
2. 改数：先改 digest/E，再改本页；本页不产生数。
3. 交付物引 E 时，优先「E-xx + 本页锚」，不要只写 E-xx；EXP-004 显示只写 E 行时 strict support 只有 5/20。
