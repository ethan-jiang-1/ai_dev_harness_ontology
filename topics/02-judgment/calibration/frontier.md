# 校准 · 未发现与下一步

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | 真实部署错误分布下的 p 与 precision | 57.1% 是人工故障 + 25% 假设；真实 p 未知 | 真实 agent trace + 分层抽样标注 | 企业 trace / 标注 | 高 |
| G2 | 接地等级的每级 precision/recall | OA-RAG 只给 entailed/supported 切片；等级自评 | 独立标注 + 每级混淆矩阵 + CI | 自建审计；OA-RAG 后续 | 高 |
| G3 | 误报修复的净收益（fixed − corrupted） | digest 有比例，无工时/真实 trace；02-L3 仍是推测 | 配对实验 + 修复工时 | 团队 trace | 高 |
| G4 | 域移后的阈值 | UniProt 唯一 confirmatory；OA-RAG 仅生物医学 | 多域同口径复现 | 其他 KG / 非医学域 | 中 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变 | 成本 |
|---|---|---|---|---|
| N1 | 真实 trace 上的 p/catch/FA | `checker false positive deployment trace` | F1/F2 / G1 | 中 |
| N2 | 等级独立校准 | `grounding level calibration ontology RAG` | F3 / G2 | 中 |
| N3 | 误报修复净收益 | `false alarm repair damage agent` | F4 / G3 | 中 |

## 不适用/未吸收（G-X）

- **ECE/可靠性图/isotonic/temperature scaling**：两篇 digest 均未测；本页不采用，不据此设门（`推测`）。
- **同源「只做路由」**：digest 仅有探索性观察（catch 下降，机制未定），不写成部署规则。

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-08 | 校准页重写（G-X 复核） | 吸收空结果基线/增量门/grounding 切片/per-flag 成本；ECE 与同源路由标为不适用/未核 | 本页 F1–F4 成形 |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| Can We Trust LLM Judges（2609.12002） | judge 能力偏差 + 多 judge 校准 | 待扫描 | 判断能否用于 G2 |
| checker calibration 线 | 误报代价与校准 | 待扫描 | 用 N1/N3 检索式 |
