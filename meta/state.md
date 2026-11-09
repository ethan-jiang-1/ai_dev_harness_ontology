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
| 阶段 | 内部研究档案；不做对外客户交付，因此不设客户资产/签核前置 |
| 论文 | 22 个目录（20 基础 + 2 扫描），全部有 PDF + 三份 MD + card + digest |
| 开源 | 4 个项目（trustgraph / semantica / ontop / open-ontologies），已 pin commit、已消化 |
| 主题 | 6 派 + 20 个子主题 + 00-harness 七部件 + 6 时刻 + 1 条形态轴 |
| 结论 | 20 条 E：17 已核原文 + 1 已核代码 + 2 推测；3 条 Q；4 条 C |
| 局部判断 | 65 条 L（01:15 / 02:9 / 03:11 / 04:7 / 05:9 / 06:14） |
| 证据配比（22 篇） | 9 execution-test（8 回路上 + 1 训练侧）/ 4 mechanism-only / 6 harness-evidence / 3 boundary-ruler |
| 执行形态（26 源） | engine 4 / compiled 7 / context 2 / label 1 / none 12 |
| 交付物 | 手册大纲 7 章；规划建议已写；正文未写（不执行） |
| 模型 | 不本地安装；Yovole 两个：`DeepSeek-V4-Flash` / `qwen3.8-27b`；直连超时；harness override 可调用，但 subagent 会调用工具，**不用于实验**，只做第二意见；见 [models](./models.md) |
| 最后自检 | 2026-11-09 12:25，`python3 meta/tools/check_repo.py`：0 坏链 / 0 未定义 ID / 枚举通过 |

## 当前边界（不是阻塞）

1. **无外部资产请求**：D0/试点线已于 2026-11-09 删除；不再需要具名域、日志、题库、人或单价。
2. **独立复现仍是空缺**：不影响 desk research；若要升「已证」，需要独立复现，但不在本仓库做；不设实验目录，也不再用模型做实验被试。
3. **独立人类抽检**：只在对外交付时需要；内部研究不阻塞。
4. **开源执行线**：4 个项目已在 pin commit 上完成只读代码核对；矩阵进 [execution-forms](../topics/execution-forms.md#代码级核对2026-11-09)；`read-path` 仍只有 1 个实现，需第二个才能决定是否升第七时刻。

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

## 2026-11-09 删除 D0/试点线

按用户决定，“D0 资产门 + 内部试点”整条线删除：

- 删除 `meta/implementation/`（7 个文件：plan/status/gates/cost-model/d0-gate/report/README）。
- 删除 `deliverables/pilot-playbook.md`。
- 删除 `experiments/EXP-004-narrow-deep-k1.md`、`EXP-005-action-gate-shadow.md`、`EXP-006-ontology-checker.md`、`_pilot-template.md`。
- 不再请求具名域、日志、题库、人或单价；外部客户试点不是本仓库的路径。
- git 历史保留；若以后真要做企业试点，可从历史恢复，但不在门厅出现。

## 执行形态代码核对（2026-11-09）

在 card 所 pin 的 commit 上读代码（未跑测试；不改结论等级为「已证」）：

| 项目 | commit | `seam` | `execution_form` | 核对要点 |
|---|---|---|---|---|
| trustgraph | `184f622` | `read-path` | `engine` | SHACL-AF 策略求值；fail-open；只删 subject 侧；31 条策略测试存在 |
| semantica | `39cf721` | `checker` | `compiled` | 本体→SHACL；pyshacl `inference="none"`；CLI 校验 |
| ontop | `964dbb7` | `supply` | `engine` | TBox 饱和 + 查询重写 → SQL；不是 gate |
| open-ontologies | `375fbc4` | `none` | `engine` | SHACL→SPARQL / verified Core；影响报告 + CI 规则门；不是单次写授权 |

写入位置：[topics/execution-forms.md](../topics/execution-forms.md#代码级核对2026-11-09)（矩阵 + 4 条代码级判断）、[seams](../topics/seams.md#轴外位置可记录但不是六时刻)、4 个 digest 的「2026-11-09 代码核对」段、checker F7 的接口边界。

关键发现：`engine` 不是一种语义（OWL 重写 / SHACL-AF / SHACL 校验）；执行 ≠ 健全（trustgraph fail-open）；执行 ≠ 授权（open-ontologies 只做 CI/报告）；三态在 JSON 保留、在 shell 退出码被折叠。已升 [E-20](../topics/conclusions.md)（`已核（代码）`，不是 `已证`）。

## 薄页合并审计（2026-11-09）

15 个独立来源 <2 的子主题逐页审计：全部有独立机制或独立判断，**本轮 0 个合并**；`determinism` / `lifecycle` 列为下轮复核。规则与审计表见 [ADR 0008](../adr/0008-thin-subtopics-merge-audit.md)。「薄」是来源计数，不是冗余信号。

## 本轮修复（2026-11-09）

- E 层：全部 E-xx 出处改链 digest（17 条）；E-04 去掉“支撑 P3”的范畴错误，改标 P3a，并新增“E-04 能/不能支撑什么”范围框；Q-03 收窄到单基准/单 gate；outline 第 6 章去掉“reward 低估”的方向断言；合法意图归因降回 `推测`。E-04 共 37 处引用，4 类过度解读（结构有效 / P3b / reward 低估 / 合法意图）已修。
- 硬矛盾：E-05 错挂回改；02-L2 改为“模型自评”；开源接缝改为 `read-path` / `supply` / `none`；manifest 合并为 22 篇单账；GLOSSARY 工位改为 3 个；P3 拆 P3a/P3b。
- 结构：新增 `execution_form` 轴（[topics/execution-forms.md](../topics/execution-forms.md)，[ADR 0006](../adr/0006-execution-form-axis.md)）、`evidence_role`、`also_supports`；26 个来源全部落字段（9/4/6/3；engine 4 / compiled 7 / context 2 / label 1 / none 12）；E 行影响列改用 P1a/P1b/P1c/P2/P3a/P3b；15 个薄子主题标记；L1/L2/L3 定义与长度门重写。
- 账本：meta 索引 + 归档（8 个一次性文档 + full-audit）；state.md（本页）；可执行自检（ADR 0005）；ADR 索引（含 0006）；manifest 合并为 22 篇单账（含批次列），删除 manifest-scan。

## 怎么刷新

```bash
python3 meta/tools/check_repo.py
```

- 通过：更新本页的“最后自检”日期与计数。
- 失败：先修，不提交。
- 本文的计数是**手工维护的唯一副本**；如果脚本能数，优先信脚本输出的数字。
