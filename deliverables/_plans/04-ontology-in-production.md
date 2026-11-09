---
status: draft
updated: 2026-11-09
target: 04-ontology-in-production
---

# 04 支撑计划：topics/src 补给与 04 升级

> **本计划不是 04 正文，也不是 E。** 它把“04 现在靠外部信号”变成“04 能引 topics/E”的施工顺序；结论仍回 `topics/`，04 只做抽取。
>
> 上游缺口矩阵见 [04-upstream-gaps](../../meta/archive/2026-11/04-upstream-gaps.md)。

## 0. 一句话

**04 先保持 field guide 定位**；只做 **5 个核心 intake + 1 个可选 intake**，补 **3 个 topics 页面**，把 04 的 A/B/C 三段从“外部信号”升级成“可引用判断”。不新开交付物，不铺 20 个来源。

## 1. 决策（先定，不再反复）

| # | 决策 | 理由 |
|---|---|---|
| D1 | 04 暂不标 `stable`，保持 `draft` | 大部分机制仍是 signal；等 5 个 intake 完成再评估 |
| D2 | 只补 **5 个核心来源 + 1 个可选** | 04 的缺口集中在 querying/evaluation/access control，不在“再多读几篇” |
| D3 | 新开 **3 个 topics 页面**：`03/querying`、`05/evaluation`、`01/access-control` | 都有 ≥2 来源或独立机制；04 的三段各缺一个“家” |
| D4 | 不新增 E，除非出现跨派结论 | 04 的多数判断是工程配方（`推测`），不需要 E |
| D5 | 现场数据不补 src | CQ 覆盖、execution accuracy、policy/audit 标签只能自己量 |

## 2. 现在的支撑水位

| 04 段 | topics 够不够 | src 够不够 | 结论 |
|---|---|---|---|
| A 建 | 方法够（05/representation、02 R0、checker F2）；缺“CQ/公理评估”页 | 缺 2512.05594、2507.14552；CASTON/SFE-O 已有 | **补 1 个 topics 页 + 2 个 src** |
| B 用 | 只有 03/compilation/projection；缺 querying | 缺 CK25、GGC；ontop 已有 | **补 1 个 topics 子主题 + 2 个 src** |
| C 治 | 有 01/commit-gate/read-path；缺 ABAC/输出校验/失败传播 | 缺 VAULT、2609.06391；trustgraph 已有 | **补 1 个 topics 子主题 + 1–2 个 src** |
| 验收 | 方法够（06/metrics/feasibility）；缺现场数据 | 不适用 | **只写协议，不补 src** |

## 3. 五个核心 intake（+1 可选）

> 落点规则：arXiv 进 `src/papers/{id}-{slug}/`；Zenodo/会议/DLR 进 `src/web/{source}/`（或按 `src/README §5` 的例外处理，先问 owner）。所有 intake 必须 card + digest，digest 自包含。

| # | 来源 | 落点 | 04 用在哪 | 最小产出 |
|---|---|---|---|---|
| 1 | **2512.05594** 公理识别 benchmark | `05-produce/evaluation/` | A.3 公理质量 | card + L1/L2 digest；拟新增 05-L 条目：“公理候选 F1 单域、需人审” |
| 2 | **2507.14552** LLM 本体评估 | `05-produce/evaluation/` | A.5 CQ 评估 | card + L1 digest；拟新增 05-L 条目：“LLM CQ 评估接近普通用户，不是专家” |
| 3 | **CK25**（Zenodo 16912605） | `src/web/ck25/` | B.3 Text2SPARQL benchmark | 材料卡 + 数据说明；`03/querying` 的 benchmark 基线 |
| 4 | **GGC** 2607.28082 | `src/papers/2607.28082-ggc/` | B.3 选择性纠错 | card + digest；`03/querying` 的 correction finding |
| 5 | **VAULT**（DLR 214536） | `src/web/vault/` | C.1 文档/节点级权限 | 材料卡 + digest；`01/access-control` 的机制 finding |
| 6（可选） | **2609.06391** graph-agentic RAG | `src/papers/2609.06391-graph-agentic-rag/` | C.4 失败传播 | card + digest；`06/failure-attribution` 的 finding |

**先不做**：2604.00555、AWS 指南、SAGA、SchemaForge、Build2SPARQL。它们继续留在 04 `evidence/` 的 signal 表；只有 04 需要“更多对照”时再开。

## 4. 三个 topics 页面

### 4.1 `topics/03-knowledge/querying/`（新建）

- **成立理由**：CK25 + GGC ≥2 来源；有独立机制（schema grounding / selective correction）与独立 frontier。
- **最小文件**：`README.md`（dashboard）、`findings.md`（F1: benchmark 基线；F2: selective correction）、`frontier.md`（G1: 跨域；G2: 空结果分因）、`mechanism.md`（query/correction 流程）。
- **04 改动**：`body/consume.md` 把“外部信号”改成“引 querying F1/F2 + E-20（OBDA 不等于 NL→query）”。

### 4.2 `topics/05-produce/evaluation/`（新建）

- **成立理由**：2512.05594 + 2507.14552 ≥2 来源；CQ/公理评估是 05 现有页面没有的独立问题。
- **最小文件**：`README.md`、`findings.md`（F1: 公理 F1 范围；F2: CQ 评估接近普通用户）、`frontier.md`（G1: 跨域；G2: 人审成本）、`mechanism.md`（评估三把尺）。
- **04 改动**：`body/build.md` A.2/A.3/A.5 从“外部信号”改成“引 05 evaluation F1/F2”。

### 4.3 `topics/01-constraint/access-control/`（新建）

- **成立理由**：VAULT + trustgraph ≥2 来源；读/写/节点级权限和 action-gate/commit-gate 是不同机制。
- **最小文件**：`README.md`、`findings.md`（F1: 文档级/节点级；F2: fail-closed vs fail-open；F3: 读路径不等于写授权）、`frontier.md`（G1: 第二实现；G2: 审计）、`mechanism.md`（policy/请求/verdict）。
- **04 改动**：`body/govern.md` C.1 从“VAULT 信号”改成“引 access-control F1–F3 + 01/commit-gate F5–F7”。

### 4.4 可选：`06-measure/failure-attribution` 加 finding

- 2609.06391 的“evidence→retrieval→reasoning→capability→outcome”五契约，作为一条 `F9` 或 `F10`；不新开子主题。
- 04 改动：`body/govern.md` C.4 从“外部信号”改成“引 06/Fx”。

## 5. 现场数据，不进 src

| 04 要的数字 | 怎么量 | 写在哪 |
|---|---|---|
| CQ 覆盖 | 目标消费者 3–10 个 CQ，逐条执行/人审 | `sections/acceptance.md` |
| execution accuracy | 100–200 问题 + SPARQL + 答案；同一 schema/模型 | `sections/acceptance.md` |
| 权限覆盖/泄漏 | 20–50 条 policy 用例 + object 方向 | `sections/acceptance.md` |
| 审计/false-defer | 20–50 条 mutation 样本 | `sections/acceptance.md` |

**这些不进 topics，也不进 src；04 只写协议与 stop。**

## 6. 阶段与 DoD

| 阶段 | 时间 | 做什么 | DoD |
|---|---:|---|---|
| P0 冻结 | 0.5 天 | 锁 5+1 来源；把 04 A/B/C 每条改成“待引”清单 | 一页 claim→source 映射；无新 E |
| P1 querying | 2–3 天 | CK25 + GGC 落盘；`03/querying` 四件套；03 claims/sources/frontier | `03/querying` 可读；04 consume 引 F1/F2 |
| P2 access-control | 1–2 天 | VAULT 落盘；`01/access-control` 四件套；01 claims | 04 govern 引 F1–F3；不把 R8 当 R9 |
| P3 evaluation | 1–2 天 | 2512 + 2507 落盘；`05/evaluation` 四件套；05 claims | 04 build 引 F1/F2；公理/CQ 数字带条件 |
| P4 failure（可选） | 1 天 | 2609 落盘；06 finding | 04 govern C.4 从 signal 改引 F |
| P5 回写 | 1–2 天 | 04 evidence 状态改“已入库”；04 body 去 signal；deliverables/README、state、loading | check_repo 通过；04 仍标 draft（除非再评估） |

**最小路径**：P0 + P1 + P2 + P5 ≈ **4–6 天**；querying 与 access-control 是最缺的两块。
**完整路径**：加 P3 + P4 ≈ **7–9 天**。

## 7. 风险

| 风险 | 表现 | 处置 |
|---|---|---|
| 来源拿不到 | PDF/网页 403 | 换官方 PDF/arXiv HTML；拿不到就留在 signal，不硬编 |
| 单来源太薄 | querying 只有 CK25 | GGC 必进；否则 `03/querying` 标薄页，不承担稳定判断 |
| 04 过度升级 | 把 signal 改成 E | 只引 topics 的 F/L/E；没有就保留“外部信号” |
| 页面膨胀 | querying 变成第二篇综述 | 只写机制/发现/frontier；不复制 04 正文 |
| 现场数据被当 src | 用 benchmark 代 CQ 覆盖 | 04 验收表分开：src 数字 vs 自域数据 |

## 8. 不做

- 不补 20 个来源；只做 5+1。
- 不新开 05/06/07 交付物。
- 不为“看起来完整”建空子主题；先有 2 个来源再开。
- 不把 2604.00555/AWS 指南升 E；它们是 signal。
- 不在 04 里调和 topics 冲突；冲突回 `claims.md`。

## 9. 下一步（P0 产物）

1. 一页 `claim → 来源 → 落点 → 04 段` 映射；
2. 确认 CK25/VAULT 的落点（`src/web` vs 例外）；
3. 先开 P1（querying）与 P2（access-control），P3/P4 排队。

**做完 P0 再决定 04 是否值得升 `stable`；现在不改。**
