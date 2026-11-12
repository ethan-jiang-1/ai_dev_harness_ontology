---
status: draft
type: execution-plan
updated: 2026-11-12
scope: deliverables/05 + src/papers + topics
current: false
---

# 05 收口计划（2026-11-12，第三轮：把新发现的内缺口做完）

> 现行计划（[_plans 至多一份](./README.md)）。前两轮（[缺口补齐](./2026-11-12-05-gap-closure-plan.md)、[证据池修复](./2026-11-12-05-evidence-pool-plan.md)）已执行。
> 本计划只处理 2026-11-12 复评发现的**内部可修**六条；外部八条不在此列（见 05 的 8.2）。

## 0. 要修什么

| # | 缺口 | 判据 |
|---|---|---|
| G1 | 会场级检索没做 | 扫 VLDB vol19 目录、ICDM 2026 accepted、SIGMOD/KDD industry track；有就评，没有就写阴性 |
| G2 | 验证深度（两篇新论文标「已消化」但只精读部分） | 补读 CoeusBI/UniDataAgent 的方法与结果节；够了升「已消化」，不够保持「精读」并写清读了什么 |
| G3 | 联通双记录关系未知 | 查论文/采购是否互相引用；查不到就写「关系未知，勿合并」并留 frontier 线 |
| G4 | Glyph 双口径（card `admitted` vs 05 表 A（probation）） | 在 06.1 表下加一行脚注说明两个口径；90.1 已有 |
| G5 | C2 回归（主路径 33.6k 汉字） | 压到 ≤30k；并按 01.1 三条读者路径给出**每条路径的长度**，在质量评估里写清口径 |
| G6 | 定位张力（标题说本体，证据大半是语义层） | 在 README 第一屏更早说破：先给「本体少、语义层多」的配比结论 |

## 1. 做法

### G1 会场扫（先做，可能加证据）

- VLDB vol19 目录（`vldb.org/pvldb/vol19.html` 或卷内 index）：筛 title/abstract 含 ontology / knowledge graph / semantic layer / BI 的工业论文。
- ICDM 2026 accepted papers：筛 ontology/KG/enterprise 相关（Demo/Industry track）。
- SIGMOD 2026 industry track、KDD 2026 ADS track：只做关键词命中检查。
- 命中处理：能过门（G1–G5）→ 建卡；否则 frontier 一行。**不硬升**。

### G2 补读

- CoeusBI：读 §3–§6（视图生成、schema linking、路由、编译器）+ §8（实验）+ §9（局限）。
- UniDataAgent：读 §III（OAV/QRE）+ §IV（结果）+ 局限段。
- 只改 `reading` 与 digest 中与原文不符的句子；不改结论。

### G3 联通

- 检索「联通软研院 政企本体建模」「UniDataAgent 联通」；看论文是否引用采购、采购是否提系统。
- 查不到 → 04.4.9 的「勿合并」保留，frontier 加一行「两者关系待查」。

### G4 Glyph 脚注

- 06.1 表下加：「Apple Glyph 的卡是 `admitted`（§4.4 公司例外，只有 I3）；本表按 05 的分级记 A（probation），因为 05 的 A 要求独立信号。」

### G5 压缩（主体工作）

按「同一事实只留一处 canonical」压，不动证据表：

1. **06.2 六个短案例** → 压成一张「案例 / 一句结论 / 详见」表，保留每案最关键的 1 个数字；细节回 06.1 与 03/04。
2. **04.4.1–4.4.5（中泰）** → 合并为 2 小节：4.4.2 报了什么（保留数字）+ 4.4.3/4.4.4（没报什么、三个退役判例），删与 06.2 重复的叙述。
3. **03.3 Palantir** → 客户名单从 10 个压到 4 个 + 「等」；3.4 Snowflake/Sigma 的细节与 06.2 重复的删。
4. **05 经济** → 5.4 三个量级判断压成 3 行；5.2 表保留。
5. **04b** → 标「选读（底座选项）」，并把与 02/4b 重复的 OKF 定义压 5 行。
6. **00** → 与 README 重复的「30 秒结论」不删（入口功能），但删重复的解释句。

目标：33.6k → ≤30k（汉字）；同时算三条读者路径长度并写进质量评估。

> **不追 20k**：要到 20k 得删证据。C2 的判定改用「同一事实 canonical + 每路径 ≤ 2 万字」；全节并集长度如实披露。

### G6 定位

- README 的「30 秒结论」第 1 条前加一句配比：「8 条证据里，严格 OWL 只有 1 条，语义层/标签层 6 条——所以本份答的是『本体在生产里以什么薄形态存在』，不是『本体塔普及了吗』。」

## 2. 收口

- `check_repo` 0 error；state/state-log/_plans 更新；质量评估写「六期」delta 与主路径口径。
- 判断有变的先改 `topics/` 再改 05。

## 3. 不做

- 不重画图；不写代码；不把厂商材料填缺口；不为压字数删证据表；不把「没公开」写成「没做」。

## 4. 预算

- 轮次 60；每篇论文补读 ≤3 轮；压缩 ≤10 轮。

## 5. 进度

| 阶段 | 状态 | 结果 |
|---|---|---|
| 计划落盘 | done | 2026-11-12 |
| G1 会场扫 | done | VLDB vol19 457 篇：CoeusBI 已入、DBAIOps G1 超窗、Hamilton 学术 demo；ICDM/SIGMOD 站点未取到；**无新准入** |
| G2 补读 | done | reading 降「精读」；补读 OAV 四阶段与 CoeusBI §4–6；修正「专家评审是硬门槛」措辞 |
| G3 联通 | done | 同院同期、无互引 → 写「关系未知、勿合并」 |
| G4 Glyph 脚注 | done | 06.1 表下加双口径说明 |
| G5 压缩 | done | 主并集 33.6k → **28.1k**；路径长度写入 01.1 与质量评估 |
| G6 定位 | done | README 第一屏加「一句话配比」 |
| 收口 | done | check_repo 通过；state/state-log/_plans/质量评估已更新 |
