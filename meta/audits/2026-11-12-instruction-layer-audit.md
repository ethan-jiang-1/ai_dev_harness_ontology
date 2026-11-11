---
status: draft
updated: 2026-11-12
---

# 指令层结构审计（2026-11-12）

> 范围：只审指令层（AGENTS/CHARTER/README/meta 规则/各层 README/模板/计划索引），不审研究内容。
> 结论与决策：[ADR 0012](../../adr/0012-instruction-layer-single-home.md)。本审计是它的证据底稿。

## 0. 一句话

骨架（src→topics→deliverables、digest 交换单元、E/L 晋升、宪章）成立；病灶在骨架外累积的治理层：**规则以复制而非引用方式生长（太多），最高频的修复动作恰是规则空白（太少）**。

## 1. 体量快照

| 项 | 值 |
|---|---|
| 仓库年龄 / 提交数 | 5 天 / 114（大量 repair/lift/re-audit/cold-read/再评分） |
| md 总量 | 450 文件；src 15,165 行 / topics 10,447 / deliverables 17,544 / meta 3,881 |
| 纯指令面 | 约 3,000 行 / 27+ 文件（loading.md 自述接手需 2,000–3,000 行） |
| AGENTS.md | 43→69→82→111 行，21 次修改，只加不减 |
| `deliverables/_plans/` | 35 文件 6,767 行，占交付层 39%；索引中 16 处标“现行” |
| 质量评分轮次 | 2 天内 5 轮（quality-review §10→§12.3） |

## 2. 路由重复：同一问题八张表

“我要改 02 交付物，该读什么？”在以下位置各有一份答案，用词不同（落点/加载/读法/导读/口径），加载集不一致：

1. README §0 路由（22 行）
2. AGENTS “先定位落点”（18 行）
3. meta/loading：15 分钟路径 + 接手路径 + 按任务加载表 + 反向加载表
4. topics/README 九种读法 + 反向读法表
5. deliverables/README 导读（按任务/按时间/每份阅读顺序）
6. meta/README 现行规则表
7. core-plan §9 新会话第一天 + §10 关键文件地图（自称“唯一执行口径”）
8. START.md（给人，合理，但 agent 也会撞到）

## 3. 规则复制与已证实的漂移

复述计数（指令层 grep）：素材准入 G1–G5 在 7 处；“自包含”25 次；“只抽不增”6 处；“4+1+1”5 处；digest 契约在 AGENTS/src README/checklist/loading/conventions 反复出现。

漂移实例（审计时点）：

| 位置 | 写的 | 权威值 | 性质 |
|---|---|---|---|
| README.md §4 | 9 张材料卡（1 HN + 8 标准） | state.md：11 张（1 HN + 10 标准），check_repo 同 | 计数复制件过期 |
| src/README.md 目录注释 | manifest“28 篇” | purge 后 10 篇 | 历史快照冒充现行 |
| AGENTS.md G2 行 | “180 天内还有提交/版本/讨论/采用吗” | CHARTER G2 另有“≥2 名独立贡献者”“社区 90 天” | 丢限定转述（与本仓库论文转述失真同构） |

## 4. 修复回路缺失

- 反向**读**的路径有（loading 倒查）；判断变更后的**回改**纪律有（updates:）；但“交付物被指错→补证→回写”的完整流程只存在于一次性计划（reverse-gap-plan、04-deep-plan，均已执行/历史）。
- AGENTS 落点表没有“交付物被指错”这一行。
- README“单向不可反向”字面上禁止修复必需的上溯，与“倒查/倒逼”共用一个“反”字，语义冲突。
- 修复无完成判据：check_repo 只查结构；质量评分卡是 182 行重武器，不适合单点缺陷收口。

## 5. 分类学负载

一张源卡约 15 个字段：status / source_type / reading / provenance / evidence_role / execution_form / quality / admission / gate_checked / impact_evidence / liveness / provenance_type / standing / ontology_role / seam，另加 home/subtopic/also_supports。编号体系 E/L/Q/C/O/EXP/G/N/K/H/D/W/R/M/S/P/I 并行。每个字段都源于一次真实混淆，但总量超过模型可稳定持有的范围；conventions 需要专门段落防止 status 与 reading 混用，即词汇自身过载的信号。处置：冻结（ADR 0012 §6），不在本轮合并字段。

## 6. 否定式 steering 与沉积

- AGENTS 22/86 非空行含否定词；“不要做”16 条；CHARTER §10 反模式 10 条。多数是同一组恐惧（写代码/弱源/新增判断）的十种说法。
- 每次危机新写一份“先读我”（loading 11-09、core-plan 交接版 11-11、IA-plan 11-12），不改常设文档。
- 三份日志并存：state“最近改动”、state-log（304 行）、command-board（239 行）。

## 7. 保留项（审计确认成立）

CHARTER 短宪章 + 用户同意锁；digest 自包含交换单元；E/L 晋升与唯一 E 表；check_repo 机器门；证据四级 + 反例同权；素材准入概念本身；ADR 编号决策。问题不在这些机制，在它们的复制件与缺失的修复流程。

## 8. 整改映射

| 病灶 | 处置 | 落点 |
|---|---|---|
| 八张路由 | AGENTS 唯一路由表；其余降为指针/给人 | AGENTS / README / loading / 各层 README |
| 规则复制 | 每条规则一个家 + 指针 | ADR 0012 §2 |
| 修复缺失 | 常设修复回路 + 完成判据 | AGENTS |
| “单向不可反向” | 判断顺流、证据逆流 | README / AGENTS |
| 计划沉积 | 现行唯一、core-plan 降格、状态重标 | _plans/README / core-plan |
| 漂移三例 | 删复制件或对齐权威 | README / src/README / AGENTS |
| 字段过载 | 冻结，新增需 ADR | conventions / ADR 0012 §6 |
