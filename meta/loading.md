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

实际加载约 2,000–3,000 行（2026-11-09 冷启动复测约 2,100 行 / 27 个文件），是 15 分钟路径全文（约 720 行）的 3–4 倍；按指定章节读则约 4–5 倍——这是“接手”的真实成本，不是 15 分钟。

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
| 做 01 现状 | [01 §9](../deliverables/01-capability-status/README.md#9-期待与数据需求验收规格) + [plan](../deliverables/01-capability-status/plan.md) + [conclusions](../topics/conclusions.md) E 表 + 对应派 `sources.md`/子主题 + 指定 digest §4/§5 | 其他派、`card.md`/`references.md`/`appendix.md` |
| 做 02 工程 | [02 §0–§4](../deliverables/02-engineering-playbook/README.md) + 对应 recipe + 子主题 `mechanism.md` + [execution-forms](../topics/execution-forms.md) + 4 个开源 digest | 24 篇 `paper.md`、`card.md`、其他派 |
| 做 03 机制 | [03 §3/§4](../deliverables/03-mechanism-reference/README.md) + `positions/<位置>.md` + [boundaries](../deliverables/03-mechanism-reference/boundaries.md) + [conclusions](../topics/conclusions.md)；长版论证再看[附录](../deliverables/03-mechanism-reference/appendix-constraint-spectrum.md) §3.1–3.3/§3.7 | `src/` 原文、其他派 `mechanism.md`、全部 `paper.md` |
| 用模型做第二意见（不用于实验） | [meta/models](./models.md) | 本地模型/实验被试 |
| 查结构决策 | [adr/](../adr/README.md)（0001–0008） | 全部 meta |
| 查 meta 有什么 | [meta/README](./README.md)：现行 / 模板 / 历史 | `archive/` |

## 从交付物倒查（反向加载）

> 三个交付物是三种「下游规格」。不要从 `src/papers/manifest.md` 开始扫；从交付物的期待出发，沿链走到「够回答」就停。

```
D1 期待 → plan.md H1–H6 → topics 子主题 → digest §4/§5 → paper.md 指定节
D2 recipe → topics/<子主题>/mechanism.md → digest §6.5 → open-source digest/代码
D3 边界 → conclusions E 表 → digest §5/§9 → 附录 §3.7/§3.8
```

| 交付物 | 起点 | 走到哪停 | 默认不读 |
|---|---|---|---|
| 01 现状 | `01/README §9` + `plan.md` | 能填出 E1–E9 的 verdict + boundary | 全部 `paper.md`（只读指定节）、`card.md`（只作 provenance）、`references.md`/`appendix.md`、其他派 |
| 02 工程 | `02/README §0 决策图 + §4 R0–R12 + recipes/` | 能写出接口/字段/验收/停线 | 24 篇论文正文、其他派 mechanism、`conclusions` 全表 |
| 03 机制 | `03/README §3/§5` | 能指到 E-xx 与「不能证明什么」 | `src/` 原文、其他派 mechanism、全部 `paper.md` |

**三条反向规则**：

1. **从 E 倒查，不从 manifest 顺读。** E 行已经链到 digest；digest 不够再回 `paper.md` 的指定表/节。
2. **`digest.md` 是默认入口，`card.md` 只补 provenance。** 不要先读 card 再读 digest；没有 digest 的来源不算入库。
3. **每份交付物只带自己的「不读」清单。** 01 不读其他派，02 不读论文正文，03 不读 `src/` 原文；跨交付物需要时，回到 `deliverables/README` 的「怎么读」。

**支持层契约（`topics/` / `src/` 必须先满足）**：

| 层 | 要提供 | 现在怎么落地 | 不满足时 |
|---|---|---|---|
| topics | 每个 E 行链 digest；每个未关缺口在派/子主题 `frontier.md` 有 G/N，写「关闭它需要什么」 | `conclusions` E 表 + 派 `frontier`；E 行反向读 digest §4/§5 | 不升 E；留在 `frontier` |
| topics | E 只在 `conclusions`；`sources.md` 只做 L/digest 索引，不复制 E 表 | `conclusions` 是唯一 E 表；`sources.md` 保持 L | 出现两份 E 就回退 |
| src | digest §4/§5/§6/§8 编号稳定；§4 数字、§5 边界、§6 工程、§8 回链 | [src/README](../src/README.md) 的 digest 契约；模板固定骨架 | 反向读不到就回 `paper.md` 指定节 |
| src | `card.md` 不承载判断；`references.md`/`appendix.md` 默认不读 | [src/README](../src/README.md) §0/§3 | 不要把 card 当 digest |
| deliverables | 每份 README 有「加载集」；新增交付物先写期待与加载集 | 三份 README 的「加载集」表 | 没有加载集不算交付物 |

> **落地顺序**：先保证 topics/src 的契约（E→digest、frontier G/N、digest 四节、card 边界），再开始 D1 的 E1–E9 倒逼。契约不满足时，倒逼会退化成「从 manifest 顺读」，又变成乱忙。

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
