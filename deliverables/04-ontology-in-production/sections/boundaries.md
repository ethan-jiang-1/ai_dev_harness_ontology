---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# 4. 边界与反例

> 能否落地看位置×成本（E-19，推测）；外部 signal 不作依据。段内限定见 [build](../body/build.md)、[consume](../body/consume.md)、[govern](../body/govern.md) 的「证据边界」。

## 4.1 十条边界

| 边界 | 影响段 | 什么会改变它 |
|---|---|---|
| 建无 in-scope 评估，只到候选+人审 | 建 | 独立复现的建模基准 |
| E-02 的 catch/FA 同源，precision 随错答案基率变 | 建 | 换基率仍成立 |
| E-12 薄层优先：单工厂、9 任务、答案在文本 | 建 | 跨域、深结构 |
| E-21 三路线各单设置、无头对头；Match 允 superset | 用 | 跨域对照 |
| execution accuracy ≠ 业务正确；空结果不分因 | 用 | 自域配对 |
| OBDA 是本体+映射→SQL，不是 NL→SPARQL | 用 | 同查询集对比 |
| E-22 三层不可互推：标签有、策略无、执行单实现 | 治 | 第二实现、领域策略 |
| 读路径过滤≠写授权；fail-open、只删 subject | 治 | object 受控且 fail-closed |
| 失败跨段传播（推测）：单点准确率看不见 | 治 | 端到端注入实验 |
| 成本/组织无实测，厂商 token 说法只是 signal | 全 | 你的单价数据 |

依据：1 T:05/produce · gap；2 E-02/O-F08；3 E-12/O-F14；4 E-21；5 T:03/querying F1–F3 · E-21 · S:Qlever digest；6 T:02 R11 · E-20；7 E-22/O-N28；8 E-20/O-C02/O-C03；9 E-06 · gap；10 gap

## 4.2 反模式

1. 先建整座本体再找消费者：无 CQ/负例，无法验收。
2. LLM 生成的类/公理直接当结论；读路径过滤当写授权。
3. 只做输入侧约束（闸门），不做输出校验：E-04 的输入 gate 只在单 benchmark 上部分改善。

依据：T:05/representation 建模 · E-02/E-04 · E-22 · gap

## 4.3 gap

输出校验（约束都在输入侧）、端到端访问控制（无领域策略来源、读路径单实现）、失败传播（无跨段注入实验；E-06 只到工作流派）三处仍是 gap。04 给接口与模板，不给效果。

依据：gap · E-06 · E-22 · T:02/checker · T:06/failure-attribution
