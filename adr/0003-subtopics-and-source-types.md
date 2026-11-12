# 子主题与素材类型：让 topics 能长第二层

## 背景

`topics/` 的六派目前是扁平的：每个派只有 `README.md`、`frontier.md` 和若干正文文档。材料一多，派根会变成一堆文件；而「论文 vs 博客」不是主题差异，不能拿来源类型当目录轴。

## 决策

1. **派 = 地图，不是桶。** 派 README 只放核心主张、边界、子主题表；详细论证下沉到 `topics/<派>/<子主题>/README.md`。
2. **子主题按子机制/子问题命名**，不按来源类型，也不按领域。
3. **子主题的成立条件**（满足其一）：
   - 有自己的判断与边界，塞回派 README 会失焦；
   - 已有 ≥2 张卡片共享同一子机制；
   - 需要自己的 frontier。
   不预建空子目录。
4. 子主题可以有 `frontier.md`（子扫描）与 `sources.md`（卡片清单）；派 `frontier.md` 仍是汇总，不重复子主题的正文。
5. **素材类型放在 `src/`，不进 `topics/`**：
   - `src/papers/{arxiv_id}-{slug}/`：一篇一目录，内含 `<stem>.pdf` / `card.md`（分解）/ `digest.md`（消化）/ `figures/`；
   - `src/web/`：网页/博客原文 + 同名 `.card.md`；
   - 卡片用 `source_type` 区分 `paper` / `preprint` / `blog` / `engineering` / `standard` / `talk` / `survey`。
6. **证据天花板**：paper/preprint 与 standard 可支撑 `已核`；blog/engineering 只对「作者报告了 X」算 `已核`，一般性结论默认 `推测`；survey 只作索引。细则见 [source-types](../meta/rules/source-types.md)。
7. **入口**：博客/工程素材先入 `src/web/`；只有改变判断时才进 `topics/`，否则留在 `frontier` 候选队列。

## 后果

- 现有正文文档下沉到子主题目录；派 README 变短。
- 卡片 `home` 指向子主题；`updates` 仍用于反向修订。
- 链接一次性迁移；之后新增子主题不再搬动派根。
- `00-harness/` 保持扁平：七个部件各一篇；某部件出现第二篇独立文档时，再建 `00-harness/<component>/`。

## 考虑过的选项

- **按来源类型建目录**（papers/blogs）：错。来源类型不是研究结构，且会让同一子机制被拆到两处。
- **全扁平**：派根会膨胀，且无法给子机制独立 frontier。
- **三层全展开**：过度；子主题下暂不再分层，除非出现独立的子子机制。

## 2026-11-09 补充：薄页

实践里出现了 1 篇论文也开子主题的情况（calibration、determinism、lifecycle、representation 等）。不强行合并，但加一条纪律：

- 独立来源 <2 的子主题必须在派 README 标「薄页」，且**不承担稳定判断**；只能放候选、边界或单来源发现。
- 连续两轮（约两个月）仍 <2 篇，考虑并入相邻子主题；合并时保留重定向指针。
- 新子主题仍优先满足「≥2 张卡片共享同一子机制」；「有自己的判断与边界」这条豁免只用于确实需要独立 frontier 的薄页。
