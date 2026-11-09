# 查询 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，缺口回 [frontier](./frontier.md)。
> 三条路线不是同一根管子的三段；它们是三种不同的介入点。

## 总链

```
question
  → [ontology-in-context]  full OWL + system prompt + rider      (NLKGQ)
  → [ontology-free]        think-act-observe + search/explore   (KGVoyager)
  → [generate]             SPARQL
  → [execute]              endpoint / QLever
  → [post-check]           empty/error → gate → correct          (GGC)
  → [verify]               answer type / result set
```

## 三条路线各做什么

| 阶段 | GGC | NLKGQ | KGVoyager |
|---|---|---|---|
| 生成前给什么 | 无 ontology；Generator 权重里带关系名 | 完整 OWL ontology + system prompt + domain rider | 无 ontology；只有 endpoint + class index |
| 生成 | Llama-3.2-3B LoRA SFT | Qwen3.6-27B，单次调用，t=0 | think–act–observe，工具调用 |
| 生成后 | Gate（RoBERTa-base）判该不该改；Corrector 只改高风险 | 直接执行；wrapper 查询由确定性 rewriter 还原 | 执行反馈 refine；工具可重试 |
| 执行 | MCQA/iMKG | QLever，固定 snapshot | 各 benchmark endpoint |
| 停在哪 | 单 KG/单骨干；没有 2×2 净收益 | 单 snapshot/单系统；Match 允许 superset | 4 个小 benchmark；rdf:type 限制 |

## 1. GGC 的 Gate/Corrector

- Generator 出初始 query；Gate 输入 `[NLQ; 初始 query]`，输出“是否需纠错”；τ=0.5。
- Gate 的标签是 gold 离线造的“初始 query 对/错”；trigger 9.31%、FPR 0.31%、recall 92.11%。
- Corrector 只在这 9.31% 上跑；默认 W1.0+C0.2（14,418 条），98.33% 是默认配比，不是最好配比（C0.8 98.80%，但训练更贵）。
- **没有**用执行结果/空结果作为 Gate 特征；**没有** 2×2 配对。

## 2. NLKGQ 的五类 token + wrapper/rewriter

- 五类 token：类、属性、domain/range、subClassOf、注释/标签。
- 完整 OWL（Turtle）进 context；不是 schema slice。
- 原生词汇不透明 → wrapper ontology（dblpx/oax）给干净词；模型只写 wrapper 查询；runtime rewriter 确定性还原成原生谓词/模式；一个 wrapper 词可展开成多条 triple。
- 单次调用、t=0、无 fine-tune/few-shot/entity linking；QLever 固定 snapshot。

## 3. KGVoyager 的三类工具

- **search**：按关键词找实体/类/属性；
- **exploration**：探属性的 domain/range、实际连接、样例值；
- **execution**：跑草稿 query，拿结果/错误，改下一轮。
- class index 从 endpoint 拉一次，缓存；只含类，不含实例；28 个 endpoint 中 ~68% 可建（Jena）。
- 不依赖 ontology、不要 text–SPARQL 例子；只支持 `rdf:type` 标注类型的图。
- 成本/墙钟低于 GRASP（$2.43 vs $3.94；85.6s vs 112.4s），但 4 个 benchmark 都小。

## 4. 哪里会断

- **GGC**：Gate 依赖分布内监督；换生成器/换图，FPR/trigger 会变；空结果不进 Gate。
- **NLKGQ**：ontology 太大超 context；endpoint 换 snapshot 分数会动；wrapper 手工。
- **KGVoyager**：非 `rdf:type` 图要 adapter；探索成本随图规模上升；小 benchmark 的 +3.7pp 不稳。
- 三条路线都**没有**把“执行结果是否正确”做成可审计的 verdict；这是 04 C.3/02 checker 的接口，不在本页。

## 5. 工程接线（给 04 B.3 用）

1. 先选路线：有完整 OWL、域不大 → ontology-in-context；只有 endpoint、无 ontology → agentic navigation；已有生成器、错例可标注 → gate/correction。
2. 固定执行器与 snapshot（Qlever/Oxigraph），记录 `endpoint/snapshot/version`。
3. 空结果分因（coverage/query/data）；不要只报 execution accuracy。
4. 记录 gate 的 trigger/FPR/recall 与 correction 的配对样本；没有配对就不报净收益。
