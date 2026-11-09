---
status: draft
updated: 2026-11-09
type: upstream-gap-analysis
---

# 04 逆向施压：topics 够不够，src 要补什么

> 结论：**04 作为“问题清单/最小验证”field guide，现有 topics + E 基本够；04 要作为“有机制、有数字”的 playbook，topics 不够，src 要补 5 个来源；还有 3 类只能靠现场数据，src 补不了。**

## 1. 先分三种“支持”

| 支持类型 | 04 里的内容 | 现有材料 | 需要做什么 |
|---|---|---|---|
| **方法/形状** | CQ、负例、stop、接口字段、验收表 | 02 R0/R5/R8/R9；05/03/01/06 的 mechanism/claims | topics 加 2–3 条 claim，避免 04 自创判断 |
| **机制/数字** | LLM 生成/公理/对齐、Text2SPARQL、VAULT、失败传播 | 外部 20 个来源，全部未入库；src 只有 CASTON/trustgraph/ontop/SFE-O 等 | 选 5 个入库、写 digest、回 topics |
| **现场数据** | CQ 覆盖、execution accuracy、policy/audit 标签 | 无；不是文献问题 | 04 只写测量协议，不写结论 |

## 2. 逐段矩阵

| 04 段 | 04 现在依赖 | topics 现有 | src 现有 | 缺口类型 | 上游动作 | 优先级 |
|---|---|---|---|---|---|---|
| A.1 CQ/消费者/负例 | 工程配方 | 05/representation 消费者契约；02 R0；checker F2 | SFE-O；checker digest | 方法有，**没有 CQ 页** | 05 加 `evaluation` 页/claim；04 引 02 R0 | P0 |
| A.2 LLM 候选生成 | 2503.05388 | 05 generation 四路线；05-L3/L7 | OntoDoc/CASTON/Peeling/ReX/Evontree | **src 缺** | 入库 2503.05388；05 generation claim | P0 |
| A.3 公理质量 | 2512.05594 | 05 refinement（CASTON）；05-L2/L9 | CASTON | **src 缺** | 入库 2512.05594；05 refinement claim | P0 |
| A.4 对齐 | Agent-OM | 05 frontier 候选 | 无 | **src 缺** | 入库 Agent-OM；与 CASTON 合一条 claim | P1 |
| A.5 评估三把尺 | 2507.14552 | 06 metrics；02 checker | 无 | **src 缺 + 无页** | 入库 2507.14552；06/05 评估 claim | P0 |
| B.2 KG 构建 | 2609.31663/2607.24551/2411.01612 | 05 representation；SFE-O | 无 | **src 缺** | 选 2 篇入库；05 representation claim | P1 |
| B.3 Text2SPARQL | CK25/GGC/SAGA/SchemaForge/Build2SPARQL | 03 compilation/projection；**无 querying** | 无 | **src 缺 + 无子主题** | 新 `03/querying`；入库 CK25 + GGC（+1） | P0 |
| B.4 语义层/OBDA/MCP | AWS 指南；ontop | execution-forms；03 compilation | ontop | **web/指南缺** | 建 `src/web` 材料卡；00-harness/context 注 | P1 |
| C.1 访问控制 | VAULT | 01 commit-gate F5–F7 | trustgraph | **src 缺（读路径有，ABAC 无）** | 新 `01/access-control`；入库 VAULT | P0 |
| C.3 输出校验 | 2604.00555 | 02 checker；01 commit | 无 | **src 缺** | 入库 2604.00555；02/01 各一条 claim | P1 |
| C.4 失败传播 | 2609.06391 | 06 failure-attribution（Diagnose） | Diagnose | **src 缺** | 入库 2609.06391；06 finding | P1 |
| C.5 审计/人审 | 工程配方 | 01 commit；02 rollout | 无 | 方法够，缺现场数据 | 04 写协议，不补 src | P2 |
| 5.1–5.3 验收 | 工程建议 | 06 metrics/feasibility | 无 | **现场数据** | 04 只写“要量什么” | P0（现场） |
| 成本/组织 | 行业信号 | 06 feasibility | 无 | **现场数据** | 不补 src；不拍单价 | P2 |

## 3. 推荐只补 5 个来源

1. **2512.05594**（公理识别 benchmark）→ `05-produce/refinement` 或新 `evaluation`；
2. **2507.14552**（LLM 本体评估）→ `05-produce/evaluation` / `06-measure`；
3. **CK25 + GGC**（企业 Text2SPARQL + 选择性纠错）→ 新 `03-knowledge/querying`；
4. **VAULT**（访问控制）→ 新 `01-constraint/access-control`；
5. **2609.06391**（graph-agentic 失败传播）→ `06-measure/failure-attribution`。

**2604.00555 与 AWS 指南先留作 signal**：前者是预印本+厂商系统声明，后者是厂商指南；不急着升 E。

## 4. 需要新建/扩展的 topics

| 落点 | 类型 | 成立理由 | 最小产出 |
|---|---|---|---|
| `03-knowledge/querying/` | 新子主题 | CK25+GGC（≥2 来源），有独立 frontier | README + findings + frontier + mechanism |
| `05-produce/evaluation/` 或 refinement 内页 | 新页/新节 | 2512.05594+2507.14552（≥2） | CQ/公理评估的 findings/claim |
| `01-constraint/access-control/` | 新子主题 | VAULT+trustgraph（≥2） | 读/写/节点级权限的 findings/frontier |
| `06-measure/failure-attribution` | 加 finding | 2609.06391 一条 | graph-agentic 失败链 finding |
| `00-harness/context` / `03-knowledge/compilation` | 加注 | AWS 指南 | MCP/A2A/语义层边界注 |

## 5. 什么 src 补不了

- 你的 CQ 覆盖、空结果率、execution accuracy；
- 你的 policy 是否正确、审计标签、false-defer；
- 你的单价/工时/维护成本。

这些只能现场量。04 已经把它们写成验收表，这是对的；不要为了“有来源”去伪造数字。

## 6. 下一步

1. 决定 04 的野心：**field guide（现状）** 还是 **playbook（要 5 个 intake）**。
2. 若 playbook：按 §3 做 5 个 intake，先 `03/querying` 与 `01/access-control`，因为它们最缺页。
3. 每落一个 source：src card/digest → topics claims → 04 正文从“signal”改成“引 E/L”；不能跳过 topics。
