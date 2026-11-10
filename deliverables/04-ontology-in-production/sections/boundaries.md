---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# 4. 边界与反例

> 能否落地看位置×成本（E-19，推测）；外部 signal 不作依据。段内限定见 [build](../body/build.md)、[consume](../body/consume.md)、[govern](../body/govern.md) 的「证据边界」。

## 4.1 十二条边界

| 边界 | 影响段 | 什么会改变它 |
|---|---|---|
| 建无 in-scope 评估，只到候选+人审 | 建 | 独立复现的建模基准 |
| E-02 的 catch/FA 同源，precision 随错答案基率变 | 建 | 换基率仍成立 |
| E-12 薄层优先：单工厂、9 任务、答案在文本 | 建 | 跨域、深结构 |
| E-21 三路线各单设置、无头对头；Match 允 superset | 用 | 跨域对照 |
| execution accuracy ≠ 业务正确；空结果不分因 | 用 | 自域配对 |
| OBDA 是本体+映射→SQL，不是 NL→SPARQL | 用 | 同查询集对比 |
| E-22 三层不可互推：标签有、策略语义有但领域映射无、执行单实现 | 治 | 领域策略来源、第二实现 |
| 读路径过滤≠写授权；fail-open、只删 subject；sparql-guard 不够第二实现，Jena 已退役 | 治 | object 受控且 fail-closed、合格第二实现 |
| 策略 10 条里 T9 无唯一期望；`clearance` 未消费；`skip` 是第 4 种效果 | 治 | 补优先级声明、消费 clearance |
| 可消费性 10 个坏样本只稳定抓住 2 个；`violations=2` ≠ 干净 | 建 | 契约 schema、target 必填、跨 validator |
| 失败跨段传播（推测）：单点准确率看不见 | 治 | 端到端注入实验 |
| 成本/组织无实测，厂商 token 说法只是 signal | 全 | 你的单价数据 |

依据：1 T:05/representation consumability · 未测；2 E-02/O-F08；3 E-12/O-F14；4 E-21；5 T:03/querying compare · E-21 · S:Qlever digest；6 T:02 R11 · E-20；7 E-22/O-N28；8 E-20/E-23/O-C02/O-C03 · T:01/read-path；9 T:01/policy；10 T:05/consumability；11 E-06 · 未测；12 gap

## 4.2 反模式

1. 先建整座本体再找消费者：无 CQ/负例，无法验收。
2. LLM 生成的类/公理直接当结论；读路径过滤当写授权。
3. 只做输入侧约束（闸门），不做输出校验：E-04 的输入 gate 只在单 benchmark 上部分改善。

依据：T:05/representation 建模 · E-02/E-04 · E-22 · 未测

## 4.3 未测与缺口

四处仍是未测：① 输出校验只有六类骨架，生产误报与 `targeted=0` 未测；② 端到端访问控制缺领域策略来源与合格第二实现；③ 失败传播无跨段注入实验（E-06 只到工作流派）；④ 可消费性只到 fixture 三关，没有真数据/跨域。04 给接口、测试与停，不给效果。

依据：未测 · E-06 · E-22 · T:02/checker · T:06/failure-attribution
