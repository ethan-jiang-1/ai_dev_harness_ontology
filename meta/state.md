---
status: draft
updated: 2026-11-11
---

# 仓库状态戳

> 这是全仓**权威的当前计数**。README 只保留结构性摘要，checklist 不再抄数；数字冲突时以本页为准。
> 每次结构性提交前更新；自检命令见文末。历史日志见 [state-log](./state-log.md)。

## 当前状态（2026-11-11）

| 项 | 值 |
|---|---|
| 宪章 | [CHARTER](../CHARTER.md)：研究档案，不做实施；交付物是文档 |
| 阶段 | 内部研究档案；不做对外客户交付，因此不设客户资产/签核前置 |
| 论文 | 28 个目录（20 基础 + 4 扫描 + 4 补给），全部有 PDF + 三份 MD + card + digest |
| 开源 | 8 个项目（trustgraph / semantica / ontop / open-ontologies + OPA / Qlever + Great Expectations + OpenLineage），已 pin commit、已消化 |
| 材料卡 | 12 张（4 张 web + 8 张标准卡） |
| 主题 | 6 派 + 23 个子主题 + 00-harness 七部件 + 6 时刻 + 1 条形态轴 |
| 结论 | 27 条 E：21 已核原文 + 2 已核代码 + 4 推测；3 条 Q；4 条 C |
| 局部判断 | 79 条 L（01:19 / 02:10 / 03:16 / 04:7 / 05:10 / 06:17） |
| 硬对象 | 94（H3 36 / H2 58；E 级 H3 10/10） |
| 证据配比（28 篇 + 8 开源） | 9 execution-test（8 回路上 + 1 训练侧）/ 16 mechanism-only / 8 harness-evidence / 3 boundary-ruler |
| 执行形态（36 源：28 论文 + 8 开源） | engine 4 / compiled 7 / context 3 / label 2 / none 20 |
| 交付物 | 4 个子目录 + 共用入口 [START](../deliverables/START.md)：01-capability-status / 02-engineering-playbook / 03-mechanism-reference / 04-ontology-in-production；02 为 README 门厅 + 13 条 recipe（R0–R12）+ 账本/评测/成本/上线/领域 + 附录；03 为四层结构（入口 + 6 位置卡 + 谱外页 + 3 横切页 + 证据台账/边界/缺口）；04 为建/用/治生命周期（README + GUIDE + 3 body + sections + evidence，E-21/E-22 已升、未入库 signal 另列）；另有 `_plans/` 工作底稿（非交付）；原 7 章书稿计划已废弃，没有独立 handbook |
| 模型 | 不本地安装；Yovole 两个：`DeepSeek-V4-Flash` / `qwen3.8-27b`；直连超时；harness override 可调用，但 subagent 会调用工具，**不用于实验**，只做第二意见；见 [models](./models.md) |
| 最后自检 | 2026-11-11，`python3 meta/tools/check_repo.py`：0 坏链 / 0 坏锚 / 0 未定义 ID / 枚举通过（539 个 md；E=27，Q=3，C=4，L=79；28 论文 / 8 开源 / 12 材料卡） |

## 当前边界（不是阻塞）

1. **无外部资产请求**：D0/试点线已于 2026-11-09 删除；不再需要具名域、日志、题库、人或单价。
2. **独立复现仍是空缺**：不影响 desk research；若要升「已证」，需要独立复现，但不在本仓库做；不设实验目录，也不再用模型做实验被试。
3. **独立人类抽检**：只在对外交付时需要；内部研究不阻塞。
4. **开源执行线**：4 个项目已在 pin commit 上完成只读代码核对；矩阵进 [execution-forms](../topics/execution-forms.md#代码级核对2026-11-09)；`read-path` 已入库仍只有 1 个实现（外部扫描另见 sparql-guard 候选，未入库），需第二实现 + harness 调用点才能决定是否升第七时刻。

## 最近改动

- **2026-11-11 导航与质量管道修复** → [state-log](./state-log.md#2026-11-11-导航与质量管道修复)；本页只留当前计数。

## 怎么刷新

```bash
python3 meta/tools/check_repo.py
```

- 通过：更新本页的“最后自检”日期与计数；一次性的改动记录写 [state-log](./state-log.md)，不写回本页。
- 失败：先修，不提交。
- 本文的计数是**手工维护的唯一副本**；`check_repo` 会比对“最后自检”里的文件数，脚本能数的优先信脚本。
