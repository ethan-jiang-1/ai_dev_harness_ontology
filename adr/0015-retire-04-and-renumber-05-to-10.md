---
status: draft
updated: 2026-11-12
---

# ADR 0015：退役 04，实证份改为 10 系列

## 背景

04（*worked-example*，合成走查）的定位在 [ADR 0014](./0014-deliverable-scope-single-home.md) 已修过一次：改名（原 *ontology-in-production*）、写 SCOPE、钉死「示例·合成」。但**那次修的是名实，不是对象**。

04 的九件产物是 `TBox → shapes → CQ → policy → audit`——一条「已经决定要建」之后的链。而 01 的头号建议是「不要先做整座塔，先对齐点位语义（K1）」，原 05（现 10）的结论是生产里跑的是薄语义层而非本体塔。于是 04 成了一份**教人从第 5 步开始的、写得很好的教程**，而档案本身说别从第 5 步开始。这不是笔误，是**时序**：04 先写，写完上游判断变了（E-12/E-01 落地后「先别建塔」才立得住），交付物跟着过期。

用户判断：04 对其**几乎没有价值**，且实证份与 01–03 视角不同（01–03 谈「你的项目」，实证份谈「世界实际怎样」），不该排成一条序列。要求：删掉 04，把 05 改为 10。

## 决策

1. **退役 04**，不打补丁、不原地重写。理由：价值不在叙述而在产物与门槛，产物本身没坏，坏在「默认你要建」；再改一次 SCOPE 只会是第三次化妆。
2. **先打捞，再删除**（证据与判据不随文档一起消失）：
   - 判定单位 / `skip` / `clearance` / 冲突次序 + LEAK-T1 构造例 → [policy F4](../topics/01-constraint/policy/findings.md)。
   - audit record 字段清单 + 泄漏观测两栏 → [output-validation §2.5](../topics/02-judgment/checker/output-validation.md)。
   - 6 行消费者契约 + 9 件产物 + 5 组门槛 → [02 附录 D §10](../deliverables/02-engineering-playbook/05-appendices/04-artifact-pack.md)。
   - `03/95-claim-walkthrough`、`02/附录 D`、`topics/trunk.md`、`consumability.md` 的 04 指针改指上述三处。
   - **不搬**：全部 fixture 数字（5 表/13 列、200 表/5,000 列、成本与规模）——编造值留在仓库里才会被误引。
3. **05 → 10**：`deliverables/05-production-landscape/` 改名为 `deliverables/10-production-landscape/`，份号、frontmatter、正文份号、索引表同步。理由：01–03 是同一组（判断/做法/机制，谈你的项目），10 是另一组（实证，谈世界）；删掉 04 后 `01/02/03/05` 读起来是断号序列，`01/02/03/10` 读起来是另一个架子，且给后续实证份（案例台账、成本研究）留出 10 系列。
4. **历史档案保留旧号**：`meta/archive/`、`meta/audits/`、`meta/status/state-log.md`、`deliverables/_plans/` 里的「04/05」是当时的事实记录，**不改写**；只把指向被删目录的 markdown 链接去链（保留文字），避免坏链。

## 后果

- 交付物从五份变四份：01 判断 / 02 做法 / 03 机制 / 10 实证。索引、START、`meta/deliverables/scope.md`、`meta/rules/loading.md`、`state.md` 的计数同步。
- 旧链接（52 处引用、26 个文件）改指新家或去链；`check_repo` 必须 0 坏链 0 坏锚。
- 04 的 35 个文件与 fixture 删除；LEAK-T1 不再是「可跑的探针」，降级为**构造性发现**（`已核` 构造可复算 / `推测` 生产普遍性），引用时不得写成「实测」。
- 读 10 时看到的份号是 10；读 `meta/archive` 与 `_plans` 时看到的 05 指同一份。

## 被否决的替代方案

- **原地重写成「轻的走查」**（OKF/语义层 → K1 → 一个 CQ）：方向对，但要换对象、重写 30+ 文件，实质是新交付物；且 02 的 recipe、10 的阶梯已覆盖其内容。若将来要做，按新份立项，不占用 04 的编号。
- **只改 SCOPE 第三次**：改不动对象，只会让「定位正确、内容过期」的状态更隐蔽。
- **保留 04 降格为模板包**：仍要维护 35 个文件里的 30 个，且其存在本身仍在暗示「建塔是默认路径」。
