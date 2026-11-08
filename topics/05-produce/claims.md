---
status: draft
updated: 2026-11-08
---

# 05 生产派 · 局部结论

> 本页是本派的局部判断账本。跨派/对外引用的结论升到 [conclusions](../conclusions.md) 的 E-xx；`05-Lx` 只在本派内使用。

| ID | 判断 | 等级 | 证据 | 备注 |
|---|---|---|---|---|
| 05-L1 | 来源影响可信度；来源标记要进判定 | 推测 | 分析；E-02；generation/F5 | E-02 已核三源漏检/误报不同；按来源加权是否降误判未测 |
| 05-L2 | 精化可自动化到小规模：CASTON high-confidence 6/6 接受；pretrained ensemble 4/7（57.1%）；GPT-4o mini 5/16（31.3%） | 已核 | CASTON Table 1 | 单一本体/单一公理类型/6 条；medium 见 05-L9；GPT-4o mini 行同时换 embedding 与 LLM |
| 05-L3 | 生成产出候选，不是完备本体 | 推测 | generation/F1、F3 | 「四篇均未测下游」已核（缺口）；「完备」无操作定义 |
| 05-L4 | SFE-O 单域：OWL 2 表达力够，但执行不在 OWL 内（数值不求解、约束未落 SHACL、外部服务在外） | 已核（限 SFE-O） | SFE-O；representation/F2 | 「表示不是瓶颈」只到该文；跨域、第二档是否够用、三档成本差未测 |
| 05-L5 | 「精化瓶颈在定位与验证」是本仓库的工作假设，不是 CASTON 的测量 | 推测 | refinement/F6 | 旧版循环引证：证据就是 refinement 页；CASTON 未拆定位/验证、未报 recall@30/@10 |
| 05-L6 | 生成说明时先写 assumptions 再写 description 提升完整性：win 54–61%（LLM judge）；completeness 3.43→3.84 | 已核 | OntoDoc Table 4–6 | 151 terms/3 KGs；无下游任务；DBpedia 上 naive accuracy/clarity 更高 |
| 05-L7 | 说明质量 ≠ 可消费性：OntoDoc 没有测下游任务；文档变好不代表判定器/用户能用 | 推测 | OntoDoc；generation/F3 | 作者也未声称；四篇都没有可消费性评测 |
| 05-L8 | 「专家覆盖窄/维护贵、LLM 语义漂移、数据挖掘把常见当应然」在生成路线的 digest 中没有测量，不能当来源排序依据 | 已核（缺口） | generation/F4；generation/frontier G5 | E-02 只测到三源漏检/误报不同；维护成本、漂移未测 |
| 05-L9 | medium 接受率 0–25%，但不是全 mixed：default 0/2、pretrained 1/4、GPT-4o mini 1/5；medium 一律人审 | 已核 | CASTON Table 1 | default 的 2 条全 mixed；另两组各有 1 条被接受；每组 2–5 条 |

> **跨页说明（本次不动 conclusions）**：generation 原 frontmatter `evidence: [E-05]` 是错挂——E-05 属 FIRME/04-state，已改为空。05 引用的 E-02/E-05 均按 conclusions 现有条目，没有新增或修改 `E-xx`。
