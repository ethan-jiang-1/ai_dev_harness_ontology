# 交稿前检查

每次改完跑一遍。任何一条不通过，不要提交。

## 1. 链接

- 所有相对链接的目标存在。
- 标签指向正确概念，不只是「能点开」；重点查 `seams.md`、`frontier.md`、`conclusions.md` 的交叉链接。
- 旧结构名（`30-seams`、`findings/`、`topics/harness/` 等）不再出现。

## 2. frontmatter

- 文档：`status` ∈ {`seed`, `draft`, `stabilized`, `superseded`}。
- 笔记：`source_type` ∈ {`paper`, `preprint`, `blog`, `engineering`, `standard`, `talk`, `survey`}；`reading` ∈ {`未读`, `综述级`, `摘要级`, `精读`, `已消化`}；`provenance` ∈ {`原文正文`, `原文摘要`, `综述转述`, `未核`}；`home` 指向 `topics/<派>`，`subtopic` 指向子主题。
- 实验：`experiment_status` ∈ {`未开始`, `设计中`, `运行中`, `已完成`, `已放弃`}。
- 交付：`deliverable_status` ∈ {`draft`, `stable`, `frozen`}。
- `updated` 是最后一次实质修订，不是搬家日期。

## 3. 证据

- 正文引用的 `E-xx / Q-xx / C-xx` 都在 `conclusions.md` 有定义。
- 每个「推测 / 存疑」有未核理由或反例。
- 卡片修正了旧判断 → `updates:` 列全，主题页已回改。
- 派内新判断在 `claims.md`；没有跨派/交付物的理由时，不应改 `conclusions.md`。

## 4. 计数

- 20 篇基础 PDF + 2 篇扫描 PDF；20 张基础卡 + 2 张扫描卡 + 1 张材料卡。
- 6 派 / 6 个 `frontier.md` / 6 个 `claims.md` / 6 个 `sources.md` / 6 个时刻。
- README 的统计与 `conclusions.md` 的实际行数一致。
- 标题里的「N 种读法」与下面的条目数一致。

## 5. 术语

- `证据等级` 只指四档置信度；OA-RAG 的 entailed/... 用 `接地等级`。
- `接缝`（概念）/ `时刻`（六个位置）/ `派`（分类）不混用。
- 新术语进 `GLOSSARY.md`。

## 6. 结构

- `01-04` 问时刻，`05` 问来源，`06` 问尺子。
- 时刻表在 [topics/seams.md](../topics/seams.md)；派表在 [topics/README.md](../topics/README.md)；部件表在 [00-harness/README.md](../topics/00-harness/README.md)。
- 稳定判断在 `README.md`；活页在 `frontier.md`；局部结论在 `claims.md`；证据索引在 `sources.md`；详细论证在 `topics/<派>/<子主题>/README.md`。
- 改一个派只动该派目录；跨派结论才动 `topics/conclusions.md`。
- 博客/工程素材在 `src_raw/web/` 与 `src_notes/materials/`，不放进 `topics/`。
- 子主题有 `prompt.md` 才建 `runs/`；run 带 `prompt` / `model` / `sources` / `claims_changed`。
- run 不直接改 README；结论先过 `claims.md` / README。
