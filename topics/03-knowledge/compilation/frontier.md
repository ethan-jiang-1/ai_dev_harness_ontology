# 编译 · 未发现与下一步

> `G` = gap（还没站住的判断）；`N` = next（下一步看什么）。稳定判断回 [findings](./findings.md)。

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | 企业语料的 `p_h` / miss penalty | FRAMES 是英文 Wikipedia；企业表格/扫描/行话会改变盈亏平衡 | 在真实企业语料上量 `p_h`、miss、抽取质量 | 企业 RAG 复盘；CAI 作者后续 | 高 |
| G2 | false-accept rate φ | `p_h` 是接受率，不是正确率；不知道 φ 就不能自动放行 | 100–400 条标注审计 | CAI §8.6 的 estimator；企业标注 | 高 |
| G3 | 证据替换的时延代价能否压下来 | 省 token 用轮次换；时延硬约束时不能买 | 并行/预算控制实验；E1 vs E2 vs E3 | CAI serving ablations | 中 |
| G4 | 增量维护成本 | 文档频繁变更时，registry/重抽/聚类更新会吃掉 token 收益 | 变更率 × 重抽成本模型 | 文档流水线；CAI §3.2 | 中 |
| G5 | 部署层回报的量化 | 治理/上手/审计通过率仍只有定性断言 | 部署指标 + 对照 | CAI Table 2；N&D 工业案例 | 高 |
| G6 | 投影 vs 编译的边界 | C-04 的解释仍靠人工预判「答案在不在文本里」 | 可自动判定的任务形态指标 | N&D/CAI 对照；03 projection | 高 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变哪条 F/G | 成本 |
|---|---|---|---|---|
| N1 | 企业语料上的编译复现 | `knowledge compilation enterprise RAG claim evidence` | F2/F3 / G1 | 高 |
| N2 | φ 的实测 | CAI §8.6；`gate false accept audit agentic retrieval` | F2 / G2 | 中 |
| N3 | 增量维护成本 | `incremental knowledge compilation update cost` | F2 / G4 | 中 |
| N4 | 部署指标 | `deployment metrics knowledge compilation onboarding audit` | F4 / G5 | 中 |
| N5 | 边界判据 | N&D 9 tasks 设计；`answer in context vs retrieval task taxonomy` | F6 / G6 | 中 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-08 | CAI + Grid Agents 深读 | F1–F6 成形；G1–G6 明确 | 先做 G1/G2 的实测/标注 |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| 企业 RAG 复盘 | 企业 `p_h` 可能远低于 43% | 待扫描 | N1 |
| 增量编译成本线 | 维护是长期成本大头 | 待扫描 | N3 |
| 「答案在文本里」判据 | C-04 的关键 | 待扫描 | N5 |
