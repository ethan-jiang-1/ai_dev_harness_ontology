# 子主题模板

一个子主题是一个独立研究单元。起新子主题时，复制这个目录到 `topics/<派>/<子主题>/`，再改 README。

## 结构

```
<subtopic>/
├── README.md       # index：dashboard + 当前判断 + 文件地图（一屏以内）
├── findings.md     # 发现索引：F1… 一行一条，带等级与链接
├── findings/       # 可选：每条/每组发现的详细证据（超过 ~5 行就拆）
├── frontier.md     # 未发现（G）+ 下一步（N）+ 候选/检索式
├── mechanism.md    # 可选：机制怎么跑
├── prompt.md       # 可选：常驻研究 prompt
└── runs/           # 可选：按日期输出
    └── YYYY-MM-DD-<slug>.md
```

## README 只做四件事

1. **覆盖**：这个子主题管什么、不管什么。
2. **计数**：已发现多少、未发现多少、下一步几个、最后扫描。
3. **当前判断**：3–5 条，带等级与链接；不展开机制。
4. **文件地图**：想知道细节时去哪个文件。

## 规则

- README 是 index；**findings / frontier / mechanism 才是正文**。README 超过一屏，就把内容下沉。
- `findings.md` 只放已经能站住的判断；`frontier.md` 只放还没站住的判断与下一步。
- run 不直接改 README；先审 run，再把结论写进 `findings.md` / `claims.md`。
- 每个 run 必须带：prompt 路径、模型、输入卡片、改变了哪条 claim、遗留问题。
- 没有 prompt 的子主题，先不建 `runs/`；没有内容，先不建 `findings/`、`mechanism.md`。不预建空目录。
- 子主题成立条件见 [ADR 0003](../../../adr/0003-subtopics-and-source-types.md)。
- 编号 `F1` / `G1` / `N1` 是子主题局部编号；跨页引用带路径。
