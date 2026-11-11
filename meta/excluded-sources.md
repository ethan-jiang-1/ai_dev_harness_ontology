---
status: draft
updated: 2026-11-12
type: source-blacklist
---

# 来源黑名单（禁读 / 禁引）

> 这是全仓**权威的“禁读/禁引”清单**。采一个源、引一个源之前，先来这里查：**在名单上的，一律不读、不引、不入库**，避免把判断带偏。
> 本页是**现行权威**；历史清除明细见 [2026-11-11 来源清除审计](./audits/2026-11-11-source-purge.md)（快照，不是现行清单）。新增剔除：先记本页，再在 `meta/audits/` 留历史明细。
> 判定依据 [CHARTER §4](../CHARTER.md#4-素材准入material-gate)。**白名单不另设文件**：`src/` 里 `admission: admitted`（含 probation）的卡就是白名单，`check_repo` 强制校验，清单见 [manifest](../src/papers/manifest.md) / [src 台账](../src/README.md) / [规范主干](../topics/trunk.md)。

## 为什么有黑名单

准入门（CHARTER §4）在**入库时**挡坏源；但 agent 做网络调研时可能**重新撞见已被剔除的源**，若不查黑名单就会再次引用、把判断带偏。黑名单是“研究/引用前”的前置闸，和准入门互补：**门管入库，黑名单管复见**。

## 论文（18）

| 来源 | 判定 | 一句话理由 | 历史明细 |
|---|---|---|---|
| 2510.26683 Evontree | excluded | G1 过期（2025-10） | [tombstone](./audits/2026-11-11-source-purge.md#src-2510-26683) |
| 2607.22868 What Can Be Enforced | excluded | 单作者、无 I1–I3、无采用 | [tombstone](./audits/2026-11-11-source-purge.md#src-2607-22868) |
| 2609.01780 KGVoyager | excluded | 单机构；匿名仓库无外部使用者 | [tombstone](./audits/2026-11-11-source-purge.md#src-2609-01780) |
| 2609.14652 NLKGQ | excluded | 单作者；无采用/社区 | [tombstone](./audits/2026-11-11-source-purge.md#src-2609-14652) |
| 2610.08082 POLAR | excluded | 单机构；无代码/采用 | [tombstone](./audits/2026-11-11-source-purge.md#src-2610-08082) |
| 2610.16838 Same Operation | excluded | 单机构；无采用 | [tombstone](./audits/2026-11-11-source-purge.md#src-2610-16838) |
| 2610.21983 OntoAct | excluded | 单机构；模拟、无采用 | [tombstone](./audits/2026-11-11-source-purge.md#src-2610-21983) |
| 2610.35267 Diagnose Workflow | excluded | position paper；质量 C | [tombstone](./audits/2026-11-11-source-purge.md#src-2610-35267) |
| 2610.36325 Ontology multi-agent | excluded | 单机构；单域 | [tombstone](./audits/2026-11-11-source-purge.md#src-2610-36325) |
| 2610.36335 OA-RAG | excluded | 单机构；无代码/采用 | [tombstone](./audits/2026-11-11-source-purge.md#src-2610-36335) |
| 2610.37123 SFE-O | excluded | 质量 C；约束未落 SHACL | [tombstone](./audits/2026-11-11-source-purge.md#src-2610-37123) |
| 2610.37407 Commit Boundary | excluded | 单作者；质量 C | [tombstone](./audits/2026-11-11-source-purge.md#src-2610-37407) |
| 2610.37809 Ontology Catch | excluded | 单机构；无代码/采用 | [tombstone](./audits/2026-11-11-source-purge.md#src-2610-37809) |
| 2610.38326 MIOE | excluded | 单机构；有代码但无独立使用 | [tombstone](./audits/2026-11-11-source-purge.md#src-2610-38326) |
| 2610.41785 Peeling Matryoshka | excluded | 单作者；L1 摘要级 | [tombstone](./audits/2026-11-11-source-purge.md#src-2610-41785) |
| 2610.41901 ReX-GG | excluded | L1；无采用 | [tombstone](./audits/2026-11-11-source-purge.md#src-2610-41901) |
| 2611.01276 OntoDoc | excluded | 单机构；无采用 | [tombstone](./audits/2026-11-11-source-purge.md#src-2611-01276) |
| 2611.03534 Power System Agentic / Grid Agents | excluded | 公司技术报告；无独立采用 | [tombstone](./audits/2026-11-11-source-purge.md#src-2611-03534) |

## 网页 / 其它（3）

| 来源 | 判定 | 一句话理由 | 历史明细 |
|---|---|---|---|
| ALCE | excluded | G1 过期（2023） | [tombstone](./audits/2026-11-11-source-purge.md#src-web-alce) |
| Kirrane 2020 QBAC | excluded | G1 过期；预印本无同行评审 | [tombstone](./audits/2026-11-11-source-purge.md#src-web-kirrane-2020-qbac) |
| 老刘说NLP · 本体 4 方向 20 工作 | excluded | 二手综述；单账号；已造成 3 处转述失真 | [tombstone](./audits/2026-11-11-source-purge.md#src-web-weixin-laoliu) |

## 怎么用

- **研究/引用前**：候选源先对本表查一次（按 arXiv 号 / 名称 / URL）。命中 → 不读不引，回 `frontier.md` 记「已剔除」即可。
- **不是永久封杀**：若某源后来补到了过门证据（如独立采用），按 CHARTER §4 重新准入，并从本表移除、在 `meta/audits/` 记复审。黑名单挡的是“当前不合格”，不是“永远不合格”。
- **signal 不在本表**：`signal`（G1/G5 过、G2/G3 未证）只是不够格入库，仍可作 frontier 线索；本表只放 `excluded`（禁读禁引）。
