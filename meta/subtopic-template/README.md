# 子主题模板

一个子主题是一个独立研究单元。起新子主题时，复制这个目录到 `topics/<派>/<子主题>/`，再改 README。

## 结构

```
<subtopic>/
├── README.md      # 稳定综合：问题、机制、证据、失效模式、开放问题
├── prompt.md      # 这个子主题的常驻研究 prompt
└── runs/          # prompt 的输出，按日期命名
    └── YYYY-MM-DD-<slug>.md
```

## 规则

- README 是稳定判断；run 是过程产物。**run 不直接改 README**；先审 run，再把结论写进 README / `claims.md`。
- 每个 run 必须带：prompt 路径、模型、输入卡片、改变了哪条 claim、遗留问题。
- 没有 prompt 的子主题，先不建 `runs/`；不预建空目录。
- 子主题成立条件见 [ADR 0003](../../adr/0003-subtopics-and-source-types.md)。
