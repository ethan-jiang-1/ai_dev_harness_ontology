---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# 4. 边界与反例

### 4.1 在已测条件下，可以当工作前提

1. **薄语义层先起量。** 命名+单位 +54.6pp > 深度结构 +19.8pp（E-12；单工厂）。
2. **强检索 harness 会吃掉结构化上下文的准确率增益。** 被测量的摘要树/大纲/wiki/实体图在 FRAMES 上无可检出增益；PageIndex 大纲退化（E-01；ontology not measured）。
3. **约束类收益随基线能力下降。** airline/retail/telecom 斜率约 −0.76/−0.67/−0.31，但只是六点描述性拟合（E-13）；强模型/retail 回退（E-04）。
4. **空结果重试是 checker 的强基线。** 人工 fault 上 catch 79.2%、FA 0%（E-02）；新 checker 必须先超过它。
5. **执行 ≠ 健全 ≠ 授权。** 四个开源项目给出四种语义；trustgraph fail-open、只删 subject；open-ontologies 只做影响报告/CI 门（E-20）。

### 4.2 还不能当工作前提

1. **「上本体能稳定提准确率」。** E-01 的 ontology 是 `not measured`；E-12 是单工厂、答案写在文本里；没有跨域复现。
2. **「结构判据有效」。** T1-only ≈ full，结构贡献未隔离；false-veto 未测（E-04）。
3. **「护栏的收益大于误拦成本」。** 审批量有模拟数，false-veto 没有标注；`γ_m` 是假设（E-15）。
4. **「写路径能授权」。** 没有实现；E-20 只有否定性证据。
5. **「本体越完备越好」。** Q-01 与 E-01 冲突；完备性与可判定性在工程上反向。

### 4.3 反向：在已测条件下不要做

1. **在强检索 harness 下为「提准确率」买结构化工件。** 被测量的摘要树/大纲/wiki/实体图没有可检出增益；PageIndex 大纲退化（E-01）。要买的是治理/预算/审计，不是准确率。
2. **把 curated 本体当权威 checker，不做审计/补声明。** curated 的 precision 仅略优于随机；FA 主源是缺声明/闭世界，不是「与数据矛盾」（E-02）。
3. **用 reward 或单一 accuracy 证明护栏有效。** 任务账看不见「被拦住的伤害」和「被误拦的正确动作」（C-03/E-04）。
4. **把 T1-only 当「结构判据有效」。** T1-only 接近 blanket veto，增益却不比 full 小；结构贡献未隔离（E-04）。
5. **把 grounding level 当形式保证。** 等级是模型自评、未校准（E-03）。
6. **把 commit gate 的概念架构当已落地机制。** 没有实现、没有 false-defer 数据；四个开源项目里没有单次写授权（E-20）。


<a id="7-证据边界"></a>
### 4.4 证据边界

这份交付物的判断都来自 [conclusions](../../../topics/conclusions.md) 的 E-01…E-20 与 C-01…C-04。引用时注意：

- E-01/E-08/E-14/E-15/E-18 是 harness/度量证据，不是本体专属；不要把「结构化上下文」读成「本体」。
- **换词检查（`推测`，分类判断）**：在当时的 26 个来源里，15 个的结论把「本体」换成「任意结构化上下文」仍然成立；只有 3 个（MIOE、Ontology Catch、OA-RAG）的结论依赖 OWL/DL 语义。也就是说，仓库过去测的更多是「结构化上下文 + harness 位置」，不是「本体形态」。这不是说本体没用，而是说不要把前者的证据当成后者专属的证据。见 [execution-forms](../../../topics/execution-forms.md)。
- E-04/E-15 是 `contested`：主结论可站，某个读法被削弱；E-12 的分数级是已核、排序级是存疑。
- E-20 是代码级核对（4 个项目、pin commit、只读代码、未做对照实验），不是效应量。
- 本仓库没有独立复现；「已核」只表示原文/代码读对了，不表示命题被验证。

更细的边界见 [03 机制参考](../../03-mechanism-reference/README.md) 与 [附录 §3.7](../../03-mechanism-reference/appendix-constraint-spectrum.md#37-本章不能证明什么)。
