---
status: draft
updated: 2026-11-09
---

# 01 约束派：怎么不让它做错事

## 核心主张

**安全是结构问题，不是判断问题。**

POLAR 把问题从「LLM 能否判断这个动作是否安全」换成「**是否存在一个可接受的逆操作序列**」——后者的答案是结构性的、可审计的；前者只是一个标签，而标签无法被验证。

这一派的判据尽量不依赖模型**自评**，而依赖可检查的世界状态/本体事实。但各子机制做到的程度不同：action-gate 查运行时状态，reasoning-gate 的候选仍由 LLM 提出、只验证条件，commit-gate 的**写路径**仍是概念设计、无实现（读路径已有开源实现，见 [commit-gate F5](./commit-gate/findings.md)）。这不是说它是唯一不依赖模型输出的一派。

## 子主题地图

| 子主题 | 回答什么 | 状态 | 已发现 / 未发现 | 先读 |
|---|---|---|---|---|
| [action-gate](./action-gate/README.md) | 动作前：可逆性够不够、该分配多少审查 | `draft`，已拆 F/G | 6 F / 5 G | dashboard → findings |
| [commit-gate](./commit-gate/README.md) | 落盘前：证据够不够授权持久化 | `seed`，已拆 F/G | 7 F / 4 G | dashboard |
| [reasoning-gate](./reasoning-gate/README.md) | 推理期：条件成不成立、知识源怎么取 | `draft`，已拆 F/G | 4 F / 4 G | dashboard |

## 本派当前判断

- **动作前**：可逆性可以做成 T1–T5 + 反向搜索的结构判据；但收益随基线能力下降，T1-only ≈ blanket veto，结构贡献未隔离。CASEL 的多模式分配应放在 harm–approval–cost–task success 前沿上看：相对只按 `p̂` 排序，HSR 降但审批与 task success 变差；NoRev 不能当「可逆性路由」的单变量消融。详见 [action-gate](./action-gate/README.md)。
- **落盘前**：可推理 ≠ 可授权；`UNVERIFIED` 不能当 positive authorization support；需 claim-specific promotion、冲突解决、scope/version 检查，批准不跨 mutation 继承。**写路径**只有概念架构、无实现；**读路径**已有开源实现（trustgraph，见 commit-gate F5）。详见 [commit-gate](./commit-gate/README.md)。
- **推理期**：它只拦有适用条件公理的动作，缺证据转观察；约束形式决定护栏还是天花板（验证条件不一定封顶，限制知识源可能封顶），但两项任务不是头对头，也不是安全保证。详见 [reasoning-gate](./reasoning-gate/README.md)。

## 何时用 · 何时别用

**用**：动作不可逆且代价高（对外发送、资金、删除唯一数据）；模型能力弱于域要求；域规则可被查询成事实。

**别用**：强模型 + 高基线（POLAR 已观察到回退）；动作的复合可逆性无法计算；判定所需事实依赖运行时状态而系统拿不到；合法意图主导（retail 退货/换货）且没有意图/授权层。

## 双重身份

多 agent 诊断同时属于 [06 测量/failure-attribution](../06-measure/failure-attribution/README.md)：它是「聚合指标掩盖 case-level」的案例（Top-1 只 +2.5 pp，个案可从 0.340 到 1.0），也是「curated KG 覆盖换可审计性」的案例——未覆盖诊断恒 0。digest 未见「性能换安全」的表述。

## 本目录怎么长

| 文件/目录 | 作用 |
|---|---|
| `README.md` | 本页：派地图 + top claims；不展开机制 |
| `claims.md` | 本派局部结论账本（`01-Lx`） |
| `sources.md` | 本派卡片索引 |
| `frontier.md` | 本派候选队列 |
| `<子主题>/README.md` | dashboard：覆盖/计数/当前判断/文件地图 |
| `<子主题>/findings.md` + `findings/` | 该子主题的发现与证据 |
| `<子主题>/mechanism.md` | 机制怎么跑 + 「工程发现 1–4」（接口/参数/成本/stop/客户指标） |
| `<子主题>/frontier.md` | 该子主题的 gap / next |
| `<子主题>/prompt.md` + `runs/` | 可选：常驻 prompt 与按日期输出 |

模板见 [meta/subtopic-template](../../meta/subtopic-template/README.md)。新增内容只改本目录；跨派才升 [conclusions](../conclusions.md)。

## 持续挖掘

派级前沿、检索式与候选见 [frontier.md](./frontier.md)；子主题的 gap/next 在各自 `frontier.md`。
