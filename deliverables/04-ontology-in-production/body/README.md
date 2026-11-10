---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# 04 主体：三章怎么串

> 三章不是三篇并列的文章，是一条链：**A 的产物是 B 的输入，B 的产物是 C 的输入，C 会把 A 打回。**

## 交接表

| 章 | 回答 | 你需要准备 | 做完得到 | 下一章用哪 |
|---|---|---|---|---|
| [A · 建](./build.md) | 消费者要什么、建到什么程度算可消费 | 3 个 consumer、6 项契约 | 契约、`ontology.ttl`、`shapes.ttl`、`build_report` | B 用契约里的 CQ；C 用 `policy_version`/`tag_version`（版本变化时回填 A.5） |
| [B · 用](./consume.md) | 按资产选哪条路线、3 条 CQ 怎么跑 | A 的 TBox/ABox；你的资产（RDF/关系库/endpoint） | 3 条 SPARQL、空结果分因表、纠错/OBDA 协议 | C 用 `query_id`（CQ1–CQ3）、结果集、snapshot；LEAK-T1 是 C.3 的单独探针，不在 B 的 3 条 CQ 里 |
| [C · 治](./govern.md) | 谁有权看、泄漏怎么发现、审计留什么 | B 的结果；标签/等级；principal/clearance | policy 表、10 条策略测试、12 条泄漏用例、audit schema | 版本变化时回填 A.5 的 `policy_version`/`tag_version` |

## 三章共同的写法

每章开头都回答四个问题：

1. **本章回答什么**：一句话。
2. **你需要准备什么**：输入清单。
3. **做完得到什么**：产物清单。
4. **怎么算做完**：本章验收。

章末有「证据与边界」：第一遍可跳过，需要时再看；`E-xx`、`T:`、`S:` 这些内码只在那里出现。

## 建议顺序

```
A.1 契约 → A.2 档位 → A.3 本体 → A.4 shapes → A.5 三关
  → B.0 资产 → B.2 CQ → B.3/B.4（可选）
  → C.1 三层 → C.2 策略 → C.3 泄漏 → C.4 审计
  → 回 A.5 补 policy_version/tag_version
```

跳过任何一步，都要在「验收清单」里对应地标「未做」，不要假装通过。
