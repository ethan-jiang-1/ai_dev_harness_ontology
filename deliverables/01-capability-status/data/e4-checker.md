---
status: draft
updated: 2026-11-11
type: evidence-note
target: X4 checker
---

# X4 数据表：checker 的 catch/FA 有 prior，但没有你的故障分布

> **工作底稿，不是交付正文。** 数字用于更新 D1 的 X4 verdict；正式引用走 E-02 与 [02/checker](../../../topics/02-judgment/checker/README.md)。来源为 Ontology Catch digest 与论文 Table 2/3/4/6；不新增结论。

## 1. 已发表什么

### 真实答案（UniProt，4,410 条，3,383 可检查）

| 来源 | catch | FA | 备注 |
|---|---:|---:|---|
| curated | 18.9% | 16.8% | catch 最高，FA 也最高 |
| data-derived | 8.2% | 3.5% | FA 最低 |
| masked LLM（三个） | 5.0% | 1.8% | catch 最低 |
| 空结果重试 | 2.5% | 0.1% | 强基线；真实错误上很弱 |

### 人工故障（9,753 faults + 3,630 controls）

| 来源 | catch（all） | catch（rows returned） | FA |
|---|---:|---:|---:|
| curated | 60.1% | 54.3% | 15.0% |
| data-derived | 75.6% | 62.1% | 9.7% |
| 空结果重试 | 79.2% | 0.0% | 0% |

### 其他数字

- **precision（人工故障 + 25% 错答案假设）**：curated 57.1、data-derived 72.3、masked LLM 93.7、空结果 100。
- **真实答案 precision 与随机比**：curated +1.6（CI −2.3~6.3，跨零）；LLM judge +15.8（12.5~19.3）。
- **LLM judge**：catch 40.3%、FA 16.2%、precision 31.3%；**40 条修好 / 83 条修坏**。
- **结构检查对 changes of meaning**：curated/data-derived/masked LLM **0%**；LLM judge 抓到它判过的 41 条。
- **成本（per flagged answer）**：curated 65,976 tokens / 46 s；data-derived 28,076 / 17 s。
- **C2**：curated − data-derived：FA +8.6（6.0,11.2）；type-swap catch −22.3（−23.5,−21.0）。
- **C3**：curated − masked LLM：FA +15.7（13.7,17.9）。
- **C4 组合**：不优于 curated，且显著差于 data-derived；组合增加 FA。
- **C5 feedback**：specific 修复 28.3% / corrupt 1.0%；generic 20.2% / 0.2%；最终准确率差异未确立。
- **FA 归因（Table 6）**：盲审 32 个双标注一致项中，undeclared term 17、closed-world 11、data clash 0。

## 2. 用 D1 的 X4 阈值去套

X4 的验收线是「增量 catch ≥5pp、FA ≤15%」，反事实是空结果重试（真实答案 catch 2.5%/FA 0.1%）。

| 来源 | 增量 catch vs 空结果 | FA | 是否过 X4 线 |
|---|---:|---:|---|
| curated | 18.9 − 2.5 = **+16.4pp** | **16.8%** | **否**：FA 超 15% |
| data-derived | 8.2 − 2.5 = **+5.7pp** | **3.5%** | **是**（UniProt 真实答案上） |
| masked LLM | 5.0 − 2.5 = +2.5pp | 1.8% | 否：增量不足 5pp |
| LLM judge | 40.3 − 2.5 = +37.8pp | 16.2% | 否：FA 超 15%；且修坏 > 修好 |

> 这是把 D1 的工程阈值套到论文数字上的**分析**，不是论文结论。论文自己的结论是「没有单一向优来源」；data-derived 过线不等于它抓得住语义错（0% changes of meaning）。

## 3. 缺什么

- **自己的故障分布**：UniProt 的真实答案错误 ≠ 你的 agent 错误；真实错误稀疏且分布不均。
- **false alarm 的信任成本**：16.8% FA 会让人忽略告警；论文没有测量。
- **净修复**：catch 高不代表净收益；LLM judge 40 修好/83 修坏是反例。
- **语义错误**：结构检查 0%；需要独立 judge/人工，但 judge 也有修坏问题。
- **部署 precision**：没有 ground truth 时算不出；只能 100–400 条分层抽样 + Wilson CI。

## 4. X4 verdict 候选

| 子句 | verdict | 依据 | 边界 |
|---|---|---|---|
| checker 能抓结构/声明错误 | `supported（限定）` | E-02；UniProt confirmatory | 单图、单 compiler；人工故障可能不代表真实错误 |
| data-derived 过「+5pp / FA≤15%」 | `supported（限定）` | 真实答案 +5.7pp、FA 3.5% | 仅 UniProt；语义错 0% |
| curated 过线 | `contradicted` | FA 16.8% > 15% | 高 catch 但高 FA；需先审计/补声明 |
| 部署有效 | **`unknown`** | 缺自己的故障分布/标注 | 先建 200 题基线 |

**结论**：X4 不是「checker 有没有用」，而是「哪种来源、在什么错误分布上、过不过你的 FA 预算」。D1 应写 `supported（限定）` + `unknown（部署）`，并明确 curated 的 FA 超线。

## 5. 什么会改变它

- 自己的 200 题标注集：空结果重试 vs data-derived 的增量 catch/FA。
- 真实 agent trace 的错误分布：若语义错为主，结构 checker 不适用。
- FA 预算：若业务能接受 >15%，curated 的高 catch 可能值得；若不能，data-derived 更稳。
- LLM judge 的净修复/成本：若修坏降下来，可能改变来源选择。
