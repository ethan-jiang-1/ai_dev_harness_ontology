# 按需加载：渐进披露

这个仓库不要求一次读完。**先读路由，再按任务加载。**

## 15 分钟路径（只够“读懂”，不够“改仓”）

1. [README](../README.md) §1-3：问题、三个工位、六派。
2. [THESIS](../THESIS.md) 的「研究问题」与 P1a/P1b/P1c、P2、P3a/P3b。
3. [AGENTS](../AGENTS.md) 的「先定位落点」表。
4. [topics/README](../topics/README.md)：四轴 + 4+1+1；[execution-forms](../topics/execution-forms.md)：第四根形态轴。
5. [meta/state](./state.md)：当前计数、边界与最后自检；先看这一页，避免把旧数字当真。
6. [conclusions](../topics/conclusions.md)：E-01…E-20 的等级与出处；至少读 E-01、E-04、E-20。
7. 任选一派 README，读它的「本目录怎么长」。

到这里你能复述“它在研究什么”。**要安全地改仓库，还不够**——走下面的接手路径。

## 30–45 分钟接手路径（要改仓库时）

1. [meta/state](./state.md)：当前计数、边界、最后自检；先看这一页。
2. [src/README](../src/README.md) §5：论文/开源入库的完整流程与模板。
3. [meta/conventions](./conventions.md)：字段、证据等级、命名、台账纪律。
4. [meta/checklist](./checklist.md)：交稿前检查；再跑 `python3 meta/tools/check_repo.py`。
5. 目标派的 `README.md` + `sources.md` + `claims.md` + `frontier.md`。
6. 至少一份完整 `digest.md`（要改哪条判断就读哪篇）。
7. 改完：更新 `meta/state` 计数，commit 前再跑 checker。

实际加载约 2,800–3,000 行，是 15 分钟路径的 6–9 倍——这是“接手”的真实成本，不是 15 分钟。

## 按任务加载

| 你要做什么 | 只加载 | 先不要加载 |
|---|---|---|
| 了解仓库 | README §1-3、THESIS 的 RQ | 全部 topics |
| 看当前状态/阻塞 | [meta/state](./state.md) | 全部 archive |
| 找一条结论 | [conclusions](../topics/conclusions.md) 的 `E-xx` | 全部卡片 |
| 找本派判断 | `topics/<派>/claims.md` 的 `L-xx` | 其他派 |
| 在一个派内干活 | 该派 README + `claims.md` + `sources.md` + `frontier.md` | 其他派 |
| 写一个子主题 | 子主题 README + `sources.md` 里对应的卡 | 其他子主题 |
| 跑一次研究 | 子主题 `prompt.md` + 相关卡 | 全仓 |
| 加原文/卡 | [src/README](../src/README.md) + `_templates/`（论文 / 材料 / 开源三套） | topics |
| 读一个开源项目 | [open-source/README](../src/open-source/README.md) + 该项目 `digest.md` | 其他项目、全部论文 |
| 做交付 | [conclusions](../topics/conclusions.md) + [deliverables/README](../deliverables/README.md) | src 原文 |
| 用模型做第二意见（不用于实验） | [meta/models](./models.md) | 本地模型/实验被试 |
| 查结构决策 | [adr/](../adr/README.md)（0001–0008） | 全部 meta |
| 查 meta 有什么 | [meta/README](./README.md)：现行 / 模板 / 历史 | `archive/` |

## 三条规则

1. **`E-xx` 才是对外结论。** `E-xx` 在 `topics/conclusions.md`，可被 `deliverables/` 引用；`L-xx` 只在本派 `claims.md` 里工作，进交付物前必须先升 `E-xx`。
2. **派内工作只读该派目录。** 需要跨派时，先读 `conclusions` 的对应 `E-xx`，再回派里看细节；不要从派根开始把所有派扫一遍。
3. **`status` 不是“完成度”。** `seed` = 结构在、内容已开始、未交叉核对；`draft` = 论证完整、可能变；`superseded` = 已归档的历史文档。先看内容，不要因为 `seed` 跳过。

## 计数只有一个权威

README、checklist、manifest 不再各写一套“当前有多少”。**计数与阻塞只看 [meta/state](./state.md)**；`python3 meta/tools/check_repo.py` 是机器可核的那一半。

## 为什么不做一个总索引

总索引会变成第二份需要维护的内容，而且会和各层 README 漂移。**路由只写“去哪”，不复制“是什么”。** 具体判断仍在各派 README / claims / conclusions 里。

## 渐进披露解决不了什么

它解决“先读什么”，不解决“两个账本打架”。如果 `L-xx` 和 `E-xx` 对同一件事给出不同判断，少加载只会把冲突藏起来。所以仍要保留：

- 卡片 → `sources.md` → `claims.md` → `conclusions` 的 promote 路径；
- 交付物只引 `E-xx`；
- 发现冲突时，回 `claims.md` 与 `conclusions.md` 各改一处，别在交付物里调和。

它也不解决“历史快照冒充现行规则”：那由 [meta/README](./README.md) 的分栏与 `archive/` 解决。
