---
status: draft
updated: 2026-11-11
parent: README.md
---

# 证据台账：E / 按章 / O

> **2026-11-11 证据重置**：E-02/E-04/E-06/E-26 已撤回；下表对应行只作回查，不再作为 04 的结论锚。


> 本页是台账，不是正文。E 是结论，O 是地址；引用时不要把 O 当结论。正文只在章末说「见这里」，不重复内码。

## 1. 已入库 E

| E | 用在哪 | 等级 |
|---|---|---|
| E-02 | 建：负例/验收 | **withdrawn** |
| E-04 | 边界：输入 gate≠输出校验 | **withdrawn** |
| E-06 | 边界：失败在 workflow | **withdrawn** |
| E-12 | 建：薄层优先 | 已核 |
| E-19 | 全篇：位置×成本 | 推测（综合） |
| E-20 | 用/治：执行形态 | 已核（代码） |
| E-21 | 用：三路线 | 已核（原文） |
| E-22 | 治：三层访问 | 已核（原文+代码） |
| E-23 | 治：读路径 10 用例 / 第二实现 | 已核（代码） |
| E-24 | 治：策略层语义 / 11 测试 / 优先级空洞 | 已核（标准摘要+文件） |
| E-25 | 建：三关 / 10 坏样本 / 2 抓 2 | 已核（标准卡+文件） |
| E-26 | 用：四路线按资产选 | **withdrawn** |
| E-27 | 治：输出六类 + 跨段传播 | 推测（综合） |

依据：[conclusions](../../../topics/conclusions.md)；不新增 E。

## 2. topics 支撑页（不是 E，只作证据组织）

| 页 | 用在哪 | 组织什么 |
|---|---|---|
| [consumability](../../../topics/05-produce/representation/consumability.md) | 建：三关 + 10 坏样本 | SHACL/ODCS/LinkML + SFE-O/CASTON/OntoDoc |
| [querying/compare](../../../topics/03-knowledge/querying/compare.md) | 用：4×8 矩阵 + 17 类失败 | GGC/NLKGQ/KGVoyager/Ontop + E-21 |
| [policy](../../../topics/01-constraint/policy/README.md) | 治：策略 schema + 11 测试 | GB/T/XACML/ODRL/Atlas/Ranger/OpenFGA（待入库） |
| [read-path](../../../topics/01-constraint/commit-gate/read-path.md) | 治：10 条用例 + 第二实现 | trustgraph + sparql-guard/Jena（候选/退役） |
| [output-validation](../../../topics/02-judgment/checker/output-validation.md) | 治：六类 + 三态 | pyshacl/open-ontologies/PROV/GE |
| [propagation](../../../topics/06-measure/metrics/propagation.md) | 治：10 类 × 3 段 | **E-06 withdrawn**；E-05 + 三段 artifacts |

> 这些页不是 E；04 的主句仍落 `E-xx`。页只回答「证据怎么排成表」，不新增判断。三关协议、11 条策略测试、12 条泄漏用例、10×3 故障矩阵是**工程产物**，标「工程产物 / 待核」，不升 E；引用时写 `工程产物`，不写成「已验证」。

## 3. 按章证据（从正文移入）

| 章 | 节 | 证据 | 等级 |
|---|---|---|---|
| A | A.1 契约 | [consumability §3](../../../topics/05-produce/representation/consumability.md)；工程产物 | 未测（无 CQ） |
| A | A.2 档位 | E-12 / O-F14 | 推测 |
| A | A.3 本体 | E-22 / O-N28；T:01/access-control F1 | 工程产物 |
| A | A.4 shapes | **原 SFE-O/E-02 已移出/撤回**；只作历史模板 | 未测 |
| A | A.5 三关 | E-25；[consumability §1/§6](../../../topics/05-produce/representation/consumability.md)；版本来源表 | 工程产物 |
| A | 全章 | T:05/representation、T:05/generation、S:SFE-O/Catch/N&D/Glyph | 边界 |
| B | B.0/B.1 路线 | E-21 单路线；**E-26 withdrawn** | 已核（单设置）/ 推测（综合） |
| B | B.2 查询 | 工程产物（3 条 SPARQL）；E-21；T:querying §5；[Qlever digest](../../../src/open-source/ad-freiburg-qlever/digest.md) | 工程产物 |
| B | B.3 纠错 | E-21；[querying/F1](../../../topics/03-knowledge/querying/findings.md) | 未测：2×2、空结果 |
| B | B.4 OBDA | E-20；[Ontop digest](../../../src/open-source/ontop-ontop/digest.md) | 已核（代码） |
| B | B.6 验收 | 工程产物（验收表）；E-21 | 示例 |
| C | C.1 三层 | T:access-control F1–F3；[policy](../../../topics/01-constraint/policy/README.md)；[read-path](../../../topics/01-constraint/commit-gate/read-path.md)；S:Glyph/trustgraph；E-22 | 已核（综合） |
| C | C.2 策略 | E-24；T:policy F1–F3；[OPA digest](../../../src/open-source/open-policy-agent-opa/digest.md)；8 规则/11 测试 | 已核（标准摘要）/ 推测（映射） |
| C | C.3 泄漏 | E-23；[read-path](../../../topics/01-constraint/commit-gate/read-path.md)；S:trustgraph | 已核（代码） |
| C | C.4 审计 | T:06/trace；[policy mechanism](../../../topics/01-constraint/policy/mechanism.md)；3 条样例 + query log | 未测 |
| C | C.5 输出/传播 | [output-validation](../../../topics/02-judgment/checker/output-validation.md)、[identity F3](../../../topics/04-state/identity/findings.md)、[coverage G](../../../topics/06-measure/metrics/coverage.md)；工程产物 | 未测 |
| 附录 | transfer / templates / decision | A/B/C + [02 cost](../../02-engineering-playbook/operations/cost.md) / [evaluation](../../02-engineering-playbook/operations/evaluation.md) / [rollout](../../02-engineering-playbook/operations/rollout.md)；工程方法 | 工程产物 / `推测`（成本） |

> transfer / templates / decision 是**工程方法与成本口径**，不新增 E；成本只有量级（`推测`），没有单价与 ROI。

## 4. 对象地址（O-xx，不是 E）

| O | 是什么 | 值/公式 | 出处 |
|---|---|---|---|
| O-F08 | PPV 复算（A.4 的“PPV 见 evidence”） | `PPV = π·Se / (π·Se + (1−π)·FA)`；π=0.25；curated Se=60.1%、FA=15.0% → 57.2%（原文 57.1） | [objects](../../../topics/objects.md) |
| O-F14 | E-12 边际分解（A.2 的 54.6pp） | 54.6 + 19.8 = 74.4pp；薄层占 73.4% | [objects](../../../topics/objects.md) |

> O 是地址，不是结论；正文主句仍落 E。`PPV` 是复算值，不是论文直接给的 precision。
