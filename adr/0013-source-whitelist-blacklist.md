---
status: draft
updated: 2026-11-12
---

# ADR 0013：来源白名单 / 黑名单

## 背景

用户要求在 `src/` 维护白名单（核过的权威内容）与黑名单（通通不许看，防带偏）。盘点发现：**白名单已经存在**——`src/` 只住 `admission: admitted`（含 probation）的卡，`check_repo` 强制校验 admission/impact_evidence，manifest/台账/trunk 即清单；再建一份平行白名单就是第二份会漂移的副本（ADR 0012 刚治掉的病）。**黑名单是真缺口**：被剔除的源只躺在日期化的 purge 审计 tombstone 里，研究/引用流程没有“先查禁读清单”一步，agent 网研时复见 POLAR/OA-RAG 等已拒源可能再次引用。

## 决策

1. **白名单不另设文件**：= `src/` 的 admitted 卡集合，由准入门 + `check_repo` 强制；视图走 manifest / src 台账 / trunk。
2. **黑名单设常设权威**：[meta/excluded-sources.md](../meta/excluded-sources.md) 是“禁读/禁引”的唯一现行清单；purge 审计降为历史明细（仿 state.md/state-log 的权威/快照分工）。新增剔除先记黑名单，再留审计明细。
3. **查黑名单接进流程**：AGENTS 素材准入节与修复回路第 3 步、topic 协议入档判据、checklist §0.1 各加“采/引前先查黑名单，命中不读不引不入库”。门管入库，黑名单管复见。
4. **黑名单不是永久封杀**：源后来补到过门证据可按 CHARTER §4 复审移出；`signal` 不进黑名单（它只是不够格入库，仍可作 frontier 线索）。

## 后果

- 防止已剔除源在后续调研中被重新引用/重新入库；判断漂移多一道前置闸。
- 不产生平行白名单副本；黑名单与审计的分工明确，计数/判定只有一个权威。
- 被否决的替代方案：在 src/ 手工维护白名单文件（与卡集合重复，必漂）；只靠准入门不设黑名单（挡不住研究时复见）。
