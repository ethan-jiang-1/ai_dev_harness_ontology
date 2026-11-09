---
status: draft
updated: 2026-11-09
rq: [RQ2, RQ4, RQ5]
evidence: [E-02]
---

# 输出后判定：本体当 checker

> 产出已形成、尚未被使用。这里问「用什么本体、以什么方式检查、代价是什么」，不负责动作前拦截（[action-gate](../../01-constraint/action-gate/README.md)）或推理期约束（[reasoning-gate](../../01-constraint/reasoning-gate/README.md)）。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 8 条（[findings](./findings.md)） |
| 未发现 / 开放 | 5 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-09 |
| 覆盖 | 输出后的语义/结构检查；不含格式检查与行为测试（见 [00-harness/verification](../../00-harness/verification.md)） |

## 当前判断

- **判定器本身是研究对象。** 不是「有没有本体」，而是「哪种来源、什么代价、漏检/误报怎么换」。`已核`
- **三种来源无单一向优。** 真实答案上 curated catch 18.9%、FA 16.8%；data-derived 8.2%/3.5%；LLM 生成不稳定（同 recipe 不同 draw 差异大；masked 三个 draw 均值 5.0%/1.8%）。precision（人工故障 + 25% 错答案假设）curated 57.1、data-derived 72.3、LLM masked 93.7，不能与真实答案口径混用。`已核`
- **curated 的 FA 主源是 declaration/domain-range，不是「与数据矛盾」。** 盲审 32 个 FA 的双标注一致项中 undeclared term 17、closed-world 11，data clash 0；Table 5 的矛盾是另一类观察，不能拿来解释 FA。`已核`
- **先超过空结果重试基线。** 空结果重试在人工 fault 上 catch 79.2%、FA 0%；真实答案上 catch 2.5%、FA 0.1%。`已核`
- **LLM judge 检错更多，但修坏多于修好。** 真实答案 catch 40.3%、FA 16.2%；40 修好 / 83 修坏；curated/data-derived 的结构检查对 changes of meaning 是 0%，judge 能抓这类错；但每条答案一次模型调用，成本/稳定性未测，不能默认更好。`已核`（Appendix C.2 比较器；部署判断 `推测`）
- **同源检查的 catch 下降是探索性观察。** 同一 artifact 既做 context 又做 checker 时 catch 下降；机制（确认偏差 vs 信息冗余）未定，不能写成「必须不同源」的部署规则。`推测`
- **checker 要报三态。** 通过 / 违反 / 未检查完；把「没检查完」合并进 pass 会污染 catch/FA 的分母。开源侧已有实现把 undetermined 做成独立 exit code。`已核`（代码；未跑）
- **覆盖与保证不可兼得。** 同一 SHACL 引擎的两条路径：默认支持 `sh:sparql` 但会 skip；verified 覆盖 Core 但拒绝 `sh:sparql`（22/120）。选型时要说明用哪条、拒了什么。`已核`（代码；未跑）

## 文件地图

| 想知道 | 去 |
|---|---|
| 三种来源/curated FA 归因/空结果/同源（探索性）/失效 | [mechanism](./mechanism.md) |
| 接口/成本口径/公式、建库参数、curated 审计、LLM judge 分支、部署抽样/客户指标、catch ≥30% 门 | [mechanism](./mechanism.md) |
| 每条判断的证据/数字/条件 | [findings](./findings.md) |
| 还缺什么、下一步看什么 | [frontier](./frontier.md) |
| 原始论文 | `src/papers/2610.37809-what-does-an-ontology-catch/` · [digest](../../../src/papers/2610.37809-what-does-an-ontology-catch/digest.md) |

## 边界

- **只查语义/结构，不查格式/行为。** 格式检查管不到语义；测试管不到语义。
- **不保证发现语义错。** 类型都对、关系方向反了/边界划错，curated/data-derived 的结构检查抓不到（changes of meaning catch 0%）；需要 LLM judge/人工。judge 能抓这类错，但修坏多于修好（F6），不能默认更好。
- **不解决「该不该阻断」。** 判定只是信号；阻断/退回/仅标注是策略层。

## 关联

- 派：[02 判定](../README.md) · 结论：[E-02](../../conclusions.md)
- 相邻：[evidence](../evidence/README.md)（证据接地）· [00-harness/verification](../../00-harness/verification.md)
- 成本：[06-measure/feasibility](../../06-measure/feasibility/README.md)
