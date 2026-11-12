---
status: draft
updated: 2026-11-12
---

# ADR 0012：指令层单一出处与常设修复回路

## 背景

五天 114 次提交中，纪律以“每次出错加一条”的方式累积：AGENTS.md 从 43 行长到 111 行、改了 21 次；“同一件事去哪办”的路由表至少有 8 张（README §0、AGENTS 落点表、meta/loading 三张表、topics 九种读法、deliverables 导读、meta/README、core-plan §9/§10），用词与加载集互不一致。规则靠复制传播：素材准入在 7 处复述、“自包含”在指令层出现 25 次，并已发生漂移（README 材料卡 9≠state 11；src/README 注释仍写 28 篇；AGENTS 的 G2 是 CHARTER G2 的丢限定转述）。最高频的任务——“交付物被指错后回上游补证再回写”——没有常设流程，只存在于已执行完的一次性计划里；“单向不可反向”的字面表述还与倒查/倒逼冲突。诊断证据见 [指令层审计](../meta/audits/2026-11-12-instruction-layer-audit.md)。

## 决策

1. **AGENTS.md 是唯一的 agent 路由表**：任务→落点→加载，一张表。README 回归给人看；[meta/loading](../meta/rules/loading.md) 只做加载集与阅读路径参考；各层 README 只讲本层。路由只写“去哪”，不复制“是什么”。
2. **每条规则一个家**：准入门→CHARTER §4；字段与证据等级→conventions；计数→state；digest 契约→src/README 与模板；质量口径→deliverable-quality；frontier/run 纪律→topic-research-protocol。其它位置只留指针，不复述判据。
3. **常设“修复回路”**写进 AGENTS：缺陷→定位承重句/E→核 digest→不足则按五门补证→L→E→回写交付物→收口。完成判据：被指的那句话能指到 admitted 源的 digest 节且数字条件与原文一致；指不到就显式标 `推测`/gap 并在 frontier 记缺什么。
4. **主干表述改为“判断顺流而下，证据逆流而上”**：deliverables 不新增判断；修复必须先走上游。替代“单向不可反向”的空间隐喻，消除与反向加载的字面冲突。主干信息流本身（src→topics→deliverables，ADR 0010）不变。
5. **`_plans/` 治理而非搬迁**：保留 `deliverables/_plans/` 物理位置——迁出要改约 70 处链接，收益只是目录纯洁；下划线前缀与“非交付”声明已把它挡在读路径外。治理口径：现行计划至多一份，其余降为日志/参考；core-plan 不再自称“唯一执行口径”，常设规则以 AGENTS/CHARTER 为准。
6. **字段词汇冻结**：新增字段或枚举值必须先过 ADR；现有字段定义以 conventions 为唯一出处。

## 后果

- 改规则只改一处；复制件删除后，漂移只能发生在指针失效上，而指针由 check_repo 查。
- AGENTS 更短、触发词更密；加载细节下沉到 loading 与各层 README，按任务披露。
- 修复成为常设任务：不再为每次“交付物不对”新开一份计划；计划层只留日志。
- 被否决的替代方案：把 _plans 迁到 meta/plans（链接代价大于收益）；把全部加载集塞进 AGENTS（always-loaded 预算爆炸）。
