---
status: draft
updated: 2026-11-08
---

# 01 约束派：怎么不让它做错事

## 核心主张

**安全是结构问题，不是判断问题。**

POLAR 把问题从「LLM 能否判断这个动作是否安全」换成「**是否存在一个可接受的逆操作序列**」——后者的答案是结构性的、可审计的；前者只是一个标签，而标签无法被验证。

这是六派里唯一一派，其判据不依赖模型输出，只依赖对世界的查询。

## 子主题地图

| 子主题 | 回答什么 | 状态 | 已发现 / 未发现 | 先读 |
|---|---|---|---|---|
| [action-gate](./action-gate/README.md) | 动作前：可逆性够不够、该分配多少审查 | `draft`，已拆 F/G | 6 F / 4 G | dashboard → findings |
| [commit-gate](./commit-gate/README.md) | 落盘前：证据够不够授权持久化 | `seed`，已拆 F/G | 4 F / 4 G | dashboard |
| [reasoning-gate](./reasoning-gate/README.md) | 推理期：结论能不能取用 | `draft`，已拆 F/G | 4 F / 4 G | dashboard |

## 本派当前判断

- **动作前**：可逆性可以做成 T1–T5 + 反向搜索的结构判据；但收益随基线能力下降，T1-only ≈ blanket veto，结构贡献未隔离。详见 [action-gate/findings](./action-gate/findings.md)。
- **落盘前**：可推理 ≠ 可授权；`UNVERIFIED` 不能当 positive authorization support；需 claim-specific promotion、冲突解决、scope/version 检查。详见 [commit-gate](./commit-gate/README.md)。
- **推理期**：约束形式决定天花板还是护栏；验证条件（OntoAct）可提升，限制知识源（curated KG）可能封顶。详见 [reasoning-gate](./reasoning-gate/README.md)。

## 何时用 · 何时别用

**用**：动作不可逆且代价高（对外发送、资金、删除唯一数据）；模型能力弱于域要求；域规则可被查询成事实。

**别用**：强模型 + 高基线（POLAR 已观察到回退）；动作的复合可逆性无法计算；判定所需事实依赖运行时状态而系统拿不到。

## 双重身份

多 agent 诊断同时属于 [06 测量](../06-measure/README.md)：它给出了一个少见的、作者自认的「性能换安全」的显式取舍。

## 本目录怎么长

| 文件/目录 | 作用 |
|---|---|
| `README.md` | 本页：派地图 + top claims；不展开机制 |
| `claims.md` | 本派局部结论账本（`01-Lx`） |
| `sources.md` | 本派卡片索引 |
| `frontier.md` | 本派候选队列 |
| `<子主题>/README.md` | dashboard：覆盖/计数/当前判断/文件地图 |
| `<子主题>/findings.md` + `findings/` | 该子主题的发现与证据 |
| `<子主题>/frontier.md` | 该子主题的 gap / next |
| `<子主题>/prompt.md` + `runs/` | 可选：常驻 prompt 与按日期输出 |

模板见 [meta/subtopic-template](../../meta/subtopic-template/README.md)。新增内容只改本目录；跨派才升 [conclusions](../conclusions.md)。

## 持续挖掘

派级前沿、检索式与候选见 [frontier.md](./frontier.md)；子主题的 gap/next 在各自 `frontier.md`。
