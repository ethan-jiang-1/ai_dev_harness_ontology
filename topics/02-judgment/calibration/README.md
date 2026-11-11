---
status: draft
updated: 2026-11-08
rq: [RQ4]
evidence: [E-02, E-03]
---

# 校准：判定器的曲线与代价

> 判定器给出分数/等级之后。这里问「部署错误率是多少、阈值放哪、catch/FA/代价怎么换」，不重复 [checker](../checker/README.md) 的来源选择与接口。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 4 条（[findings](./findings.md)） |
| 未发现 / 开放 | 4 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | catch/FA 口径、precision 的错误率条件、空结果基线、接地等级切片、per-flag 成本；不含 checker 实现与概率校准（ECE） |

## 问题

判定器的价值不是一个准确率，而是**在什么阈值下、漏掉多少、误报多少、误报后修复代价多大**。

校准问的是：判定器的分数/等级在部署错误率 p 下对应多少 precision；阈值该按什么预算定。两篇 digest（Ontology Catch、OA-RAG）都只给单点/切片，没有做概率校准；本页只采用它们支持的口径，不把 ECE/isotonic/temperature 当已核机制。

## 当前判断

- **先分 catch/FA，再谈 precision。** 真实答案（UniProt，3,383 可检查）上 curated catch 18.9%、FA 16.8%；data-derived 8.2%/3.5%；masked LLM 5.0%/1.8%；空结果重试 2.5%/0.1%。`已核`
- **precision 必须带错误率假设。** 57.1/72.3/93.7 是**人工故障 + 25% 错答案**下的口径，不能与真实答案 catch/FA 拼表；真实答案 precision 论文未直接给。curated 在真实答案上的 precision 只比同率随机 flag 高 +1.6 点（CI −2.3~+6.3，跨零）；data-derived 29.9%（+14.4 点），但 catch 只有 8.2%。`已核`
- **空结果重试是必须先超过的基线。** 人工 fault 上 catch 79.2%、FA 0%；真实答案 2.5%/0.1%。只有「查询仍有结果但答错」的增量才值得付费；增量 catch <5pp 停（digest 工程门，非论文测量）。`已核`（基线）/ `推测`（5pp 门）
- **接地等级是粗粒度切片，不是校准曲线。** OA-RAG Qwen Test 3：entailed 94.9%、supported 82.1% 正确率；等级是模型自评、未校准；entailed+supported 占比 >90% 时抽样校准、不自动放行（digest 配方）。`已核`（数字）/ `推测`（stop）
- **成本按 per-flagged 算，FA 放大成本。** curated 65,976 tokens/46.0 s、data-derived 28,076/17 s（每被 flag 的答案，不是每答案）；`per-1k = flag_rate × per-flagged × 1000`。`已核`

## 文件地图

| 想知道 | 去 |
|---|---|
| catch/FA、precision 条件、空结果基线、等级切片、成本 | [findings](./findings.md) |
| 判定回路、阈值/抽样/成本/stop/第一个 sprint/V3 | [mechanism](./mechanism.md) |
| 还缺什么、下一步看什么 | [frontier](./frontier.md) |
| prompt 与运行记录 | [prompt](./prompt.md) · [runs](./runs/README.md) |
| 相邻：来源选择/接口 | [checker](../checker/README.md) · [evidence](../evidence/README.md) |
| 尺子与成本 | [metrics](../../06-measure/metrics/README.md) · [feasibility](../../06-measure/feasibility/README.md) |
| 原始论文 | [Ontology Catch digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-37809) · [OA-RAG digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-36335) |

## 边界

- **不是新的 checker。** 来源、接口、FA 归因在 [checker](../checker/README.md)；这里只定口径、阈值与代价。
- **不做概率校准。** ECE/可靠性图/isotonic/temperature scaling 不在两篇 digest 的证据范围；若团队要用，属通用工程做法，需自测并另立来源（`推测`）。
- **digest 只给单点。** Ontology Catch 是 checker on/off 的 catch/FA，不是阈值扫描；OA-RAG 是四级序数，不是连续校准曲线。要选阈值，得自己扫分数（工程配方）。
- **真实部署没有 ground truth。** precision 不能直接算；只能分层抽样审计 + 报 CI。
- **域移未测。** UniProt 是唯一 confirmatory；其他图 exploratory；OA-RAG 是生物医学三本体。
- **同源不等于只能路由。** 同源 context+checker 的 catch 下降是探索性观察（机制未定），不能写成部署规则。

## 关联

- 派：[02 判定](../README.md) · 结论：[E-02](../../conclusions.md) / [E-03](../../conclusions.md)
- 相邻：[checker](../checker/README.md) · [evidence](../evidence/README.md)
- 成本：[06-measure/feasibility](../../06-measure/feasibility/README.md)
