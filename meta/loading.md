# 按需加载：渐进披露

这个仓库不要求一次读完。**先读路由，再按任务加载。**

## 15 分钟路径

1. [README](../README.md) §1-3：问题、三个工位、六派。
2. [THESIS](../THESIS.md) 的「研究问题」：RQ1-RQ5。
3. [AGENTS](../AGENTS.md) 的「先定位工位」表。
4. [topics/README](../topics/README.md)：三轴 + 4+1+1。
5. 任选一派 README，读它的「本目录怎么长」。

到这里已经够接手；下面的内容按任务再开。

## 按任务加载

| 你要做什么 | 只加载 | 先不要加载 |
|---|---|---|
| 了解仓库 | README §1-3、THESIS 的 RQ | 全部 topics |
| 找一条结论 | [conclusions](../topics/conclusions.md) 的 `E-xx` | 全部卡片 |
| 找本派判断 | `topics/<派>/claims.md` 的 `L-xx` | 其他派 |
| 在一个派内干活 | 该派 README + `claims.md` + `sources.md` + `frontier.md` | 其他派 |
| 写一个子主题 | 子主题 README + `sources.md` 里对应的卡 | 其他子主题 |
| 跑一次研究 | 子主题 `prompt.md` + 相关卡 | 全仓 |
| 加原文/卡 | [src/README](../src/README.md) + `_templates/` | topics |
| 做交付 | [conclusions](../topics/conclusions.md) + [deliverables/README](../deliverables/README.md) | src 原文 |
| 设计验证 | [experiments/README](../experiments/README.md) + 对应 E-xx | 全部卡片 |

## 三条规则

1. **`E-xx` 才是对外结论。** `E-xx` 在 `topics/conclusions.md`，可被 `deliverables/` 引用；`L-xx` 只在本派 `claims.md` 里工作，进交付物前必须先升 `E-xx`。
2. **派内工作只读该派目录。** 需要跨派时，先读 `conclusions` 的对应 `E-xx`，再回派里看细节；不要从派根开始把所有派扫一遍。
3. **`status` 不是“完成度”。** `seed` = 结构在、内容已开始、未交叉核对；不是空。`draft` = 论证完整、可能变。先看内容，不要因为 `seed` 跳过。

## 为什么不做一个总索引

总索引会变成第二份需要维护的内容，而且会和各层 README 漂移。**路由只写“去哪”，不复制“是什么”。** 具体判断仍在各派 README / claims / conclusions 里。

## 渐进披露解决不了什么

它解决“先读什么”，不解决“两个账本打架”。如果 `L-xx` 和 `E-xx` 对同一件事给出不同判断，少加载只会把冲突藏起来。所以仍要保留：

- 卡片 → `sources.md` → `claims.md` → `conclusions` 的 promote 路径；
- 交付物只引 `E-xx`；
- 发现冲突时，回 `claims.md` 与 `conclusions.md` 各改一处，别在交付物里调和。
