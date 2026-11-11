---
status: draft
updated: 2026-11-11
type: evidence-note
target: X1/X2/X7/X9
---

# P1/P2 源扫描：第二个 read-path、跨运行一致性、跨域复现

> **工作底稿，不是交付正文。** 本轮只做摘要级扫描；没有落盘、没有升 E。外部来源只作候选。

## 1. X7：第二个 read-path 实现

- 检索 `SHACL policy filter access control knowledge graph implementation`、`ontology-based access control agent read path authorization`。
- 命中：trustgraph 自己的文档（同一实现）、IATA ONE Record（标准/行业文档，不是代码）、W3C WebAccessControl（标准）、Zenodo 的 access-control/SHACL 书章（不是 agent 回路实现）。
- **没有找到第二个独立实现**。`read-path` 仍是单实现；X7 的 object 方向仍 `unknown`，不升第七时刻。

## 2. X9：跨运行一致性

### 候选：Suite v0（Zenodo 20285101）

**摘要级事实**（只读 Zenodo 描述，未读正文）：

- 把 agent 评测的 consistency 形式化为五轴：exact / syntactic / lexical / behavioral / decisional；证明单调性与 tradeoff：提高 pass rate 不保证其他轴不退化。
- Suite v0：50 tasks、$0/night、MIT；四个 consistency 轴 + cross-family critic constraint。
- 在真实 agent（Zeus）上：**62% 任务 pass，但每次 rerun 产物结构不同**；两个 scorer 对同一 artifact 不一致；prompt augmentation 把 pass rate 从 88% 提到 96%，同时 held-out generalization 退化；**client-side determinism（temperature=0、RNG seeding）不够**——rerun 不稳略升，pass rate 也升。
- 可五条命令复现；preprint，未同行评审。

**为什么重要**：它把「同一输入重复运行产物不同」变成可测的五轴，而不是只看 pass rate；和 E-18（54% run-to-run 方差）同向。它没有本体锚点，也不是 ontology-specific；所以**不能直接支撑 X9 的「本体作为锚点」**，但能支撑「跨运行一致性必须单独量」。

**go/no-go**：**go（候选，P2）**。落盘 + L2 digest 可补 X9 的 harness 级证据；但如果要回答「本体能否当锚点」，还需要 ontology-projection 的实现/实验，不是这篇能给的。

## 3. X1/X2：跨域复现

- 本轮没有找到 N&D 的独立域复现，也没有多设备/多站点的投影对照。
- X1/X2 保持 `supported（限定）`（单工厂、9 任务、答案基本写在文本里）；跨域仍 `unknown`。
- 不硬凑：没有独立域数据，就不把「单工厂」写成「跨域规律」。

## 4. 对 D1 的即时结论

- **X7**：`supported（限定）`（存在）/ `unknown`（object 方向）；第二个实现仍未找到。
- **X9**：仍 `unknown`（本体锚点无实现）；但 harness 级一致性有候选 Suite v0，可在 D1 §9 的「现在的证据」里注明「有 harness 级度量候选，未落盘」。
- **X1/X2**：不变。
- **下一步**：Suite v0 落盘/建卡（P2）；第二个 read-path 继续扫（P1）；不要为了填表把候选升 E。

> 回到 [数据表索引](./README.md)。
