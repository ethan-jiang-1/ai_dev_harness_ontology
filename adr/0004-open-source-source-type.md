# ADR 0004：第三类源材料 open-source

- 日期：2026-11-09
- 状态：接受

## 背景

`src/` 原来只有两类源材料：论文（`papers/`）与网页/博客（`web/`）。论文侧已收口（22 篇 digest、20 个子主题、E-01…E-19），但论文只证明「机制在论文条件下有效」，回答不了「本体在真实 harness 里以什么形式被执行」。ADR 0003 第 5 条把素材类型限定在 `paper/preprint/blog/engineering/standard/talk/survey`，没有代码这一类。

## 决策

1. **新增 `src/open-source/`**，一个项目一目录 `{org}-{repo}/`，内含 `card.md` / `digest.md` / `code-map.md`。
2. **不 vendor 代码**：只 pin commit/tag + 链接 + `文件:符号`；stars 只作影响力快照（`scan_date` / `stars_at_scan`）。
3. **角色关系不变**：card 是来源卡，digest 是自包含正文、下游唯一入口；`code-map.md` 只做索引，不承载判断。
4. **模板集中**：`src/_templates/` 新增 `open-source-card.md` / `open-source-digest.md` / `open-source-code-map.md`；源材料子目录不再自带模板。
5. **证据天花板**：`source_type: open-source` 以代码为一手原文，定位到 `文件:符号` 可到 `已核`；`已证` 需 `EXP-xxx` 在仓库外复现。README/star/单测覆盖率不能升等级；跑通官方示例只证明能执行。
6. **候选与入库分离**：候选池、选择标准、状态表在 `src/open-source/README.md`；只有建了 `card.md` 才在磁盘上开目录。
7. **不设试点线**：D0/客户资产前置已于 2026-11-09 删除；本类源材料不需要外部资产。

## 后果

- `source_type` / `reading` / `provenance` 枚举都要扩（见 conventions、checklist）。
- `seam` 字段取 [topics/seams.md](../topics/seams.md) 的六时刻，不用派名，避免轴混用。**2026-11-09 起**另接受 `read-path` / `supply` / `reasoning` / `training` 四个轴外位置（见 ADR 0006 与 seams 的「轴外位置」节）。
- 概念上的缺口（04 记忆、06 度量没有「本体真执行」的项目）会保留为缺口，不硬凑。
- 后续若出现第二类「不可读原文」的源材料，按本 ADR 的模板集中与证据天花板原则处理，不新开模板家。

## 考虑过的选项

- **每个源类型自带 `_templates/`**：会让同一套 card/digest 契约分叉，且入口表指向多处；否决。
- **把 `_templates/` 挪进 `src/papers/`**：`material-card` 服务 `web/`，挪进去名实不符；否决。
- **把开源项目写进 `topics/`**：违反「素材类型不进 topics」；否决。
