---
status: draft
updated: 2026-11-09
---

# 仓库状态戳

> 这是全仓**权威的当前计数**。README 只保留结构性摘要，checklist 不再抄数；数字冲突时以本页为准。
> 每次结构性提交前更新；自检命令见文末。

## 当前状态（2026-11-09）

| 项 | 值 |
|---|---|
| 阶段 | 内部研究档案；全审结论「内部可签 / 对外 no-go」 |
| 论文 | 22 个目录（20 基础 + 2 扫描），全部有 PDF + 三份 MD + card + digest |
| 开源 | 4 个项目（trustgraph / semantica / ontop / open-ontologies），已 pin commit、已消化 |
| 主题 | 6 派 + 20 个子主题 + 00-harness 七部件 + 6 时刻 + 1 条形态轴 |
| 结论 | 19 条 E：17 已核 / 2 推测；3 条 Q；4 条冲突 |
| 局部判断 | 65 条 L（01:15 / 02:9 / 03:11 / 04:7 / 05:9 / 06:14） |
| 证据配比（22 篇） | 9 execution-test（8 回路上 + 1 训练侧）/ 4 mechanism-only / 6 harness-evidence / 3 boundary-ruler |
| 执行形态（26 源） | engine 4 / compiled 7 / context 2 / label 1 / none 12 |
| 实验 | 6 个协议 + 1 个形态消融（EXP-007 提案）；D0 资产门未签核，EXP-004/005/006 暂不可开跑 |
| 交付物 | 手册大纲 7 章；正文未写 |
| 最后自检 | 2026-11-09 09:40，`python3 meta/tools/check_repo.py`：0 坏链 / 0 未定义 ID / 枚举通过 |

## 当前阻塞

1. **D0 外部资产**：具名域、≥500 条带 `state_hash` 日志、200 题 + gold、K2 的 3 人、单价/人时。没有它，三个试点不能开跑。
2. **独立人类抽检**：5 digest + 5 topic 未做；AI 代办不等于 human sign-off。对外交付前必须补。
3. **形态消融**：EXP-007 不依赖客户资产，可先用合成域做 v0；这是当前唯一能自主推进的实证线。

## 扫描状态（全局视图）

候选队列分散在各派 `frontier.md`；本表只汇总“最后一次扫描”，不复制候选。每周扫描后更新一行。

| 派 | 最后扫描 | 下一步 | 入口 |
|---|---|---|---|
| 01 约束 | 2026-11-09（开源 trustgraph） | false-veto/剪枝率；Commit Boundary 实现 | [frontier](../topics/01-constraint/frontier.md) |
| 02 判定 | 2026-11-07（首轮外部） | LogT / CORE-LLM-Bench 待落盘 | [frontier](../topics/02-judgment/frontier.md) |
| 03 知识 | 2026-11-07（首轮外部） | Grep 候选；投影粒度 | [frontier](../topics/03-knowledge/frontier.md) |
| 04 状态 | 2026-11-07（首轮外部） | APEX-MEM 候选；determinism 设计 | [frontier](../topics/04-state/frontier.md) |
| 05 生产 | 2026-11-08（G-X 回写） | KROMA 候选；可消费性 | [frontier](../topics/05-produce/frontier.md) |
| 06 测量 | 2026-11-07（首轮外部） | AgentDebugX 候选；机制→尺子表 | [frontier](../topics/06-measure/frontier.md) |

## 本轮修复（2026-11-09）

- E 层：全部 E-xx 出处改链 digest（17 条）；E-04 去掉“支撑 P3”的范畴错误，改标 P3a，并新增“E-04 能/不能支撑什么”范围框；Q-03 收窄到单基准/单 gate；outline 第 6 章去掉“reward 低估”的方向断言；EXP-005 把“合法意图”降回 `推测`；pilot 去掉“结构判据”标签。E-04 共 37 处引用，4 类过度解读（结构有效 / P3b / reward 低估 / 合法意图）已修。
- 硬矛盾：E-05 错挂回改；02-L2 改为“模型自评”；开源接缝改为 `read-path` / `supply` / `none`；manifest 合并为 22 篇单账；experiments 计数与状态修正；GLOSSARY 工位改为 3 个；P3 拆 P3a/P3b。
- 结构：新增 `execution_form` 轴（[topics/execution-forms.md](../topics/execution-forms.md)，[ADR 0006](../adr/0006-execution-form-axis.md)）、`evidence_role`、`also_supports`；26 个来源全部落字段（9/4/6/3；engine 4 / compiled 7 / context 2 / label 1 / none 12）；E 行影响列改用 P1a/P1b/P1c/P2/P3a/P3b；16 个薄子主题标记；L1/L2/L3 定义与长度门重写；EXP-007 形态消融提案。
- 账本：meta 索引 + 归档（8 个一次性文档 + full-audit）；state.md（本页）；可执行自检（ADR 0005）；ADR 索引（含 0006）；manifest 合并为 22 篇单账（含批次列），删除 manifest-scan。

## 怎么刷新

```bash
python3 meta/tools/check_repo.py
```

- 通过：更新本页的“最后自检”日期与计数。
- 失败：先修，不提交。
- 本文的计数是**手工维护的唯一副本**；如果脚本能数，优先信脚本输出的数字。
