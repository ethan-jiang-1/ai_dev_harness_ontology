---
status: draft
updated: 2026-11-12
---

# 状态日志（历史）

> 本页是 [meta/state](./state.md) 的历史日志：逐次改动与**当时的**计数。
> **这里的数字是快照，不是现行计数**；现行状态只看 [state](./state.md)。

## 2026-11-12 05 收口：会场扫、压缩与一致性

- **会场扫**：VLDB vol19 目录（457 篇标题）——CoeusBI 已在库；DBAIOps（KG 运维）arXiv 2025-08 首曝，**G1 超窗**，只作背景；Hamilton（交互式本体学习）是学术 demo。ICDM/SIGMOD 站点未取到（ICDM 以 UniDataAgent 脚注核到 Demo）。**无新准入**。
- **补读校核**：两篇新论文 reading 由「已消化」降「精读」；补读 OAV 四阶段与 CoeusBI §4–§6，修正「专家评审是硬门槛」——原文是 recommended。
- **一致性**：06.1 加 Glyph 双口径脚注；04.4.9 加联通采购与 UniDataAgent 的「关系未知、勿合并」。
- **压缩**：主并集（README + 00–08，不含 04b 选读与 90 出处）33.6k → **28.1k 汉字**；6.2 六个短案例压成一张表，中泰 4.4 五小节并为三节，4.6 三层缺口压三条，美章 Palantir/引文精简。路径长度：决策者 5.9k/13.1k/15.5k，架构师 4.0k/16.0k/19.9k。
- **定位**：README 第一屏加配比（8 条证据里 OWL 1 条、语义层/标签层 6 条）。
- **评分**：六期 C2 仍 3（28.1k > 2 万字），总分 **88.8**；要 90+ 只剩「把 8k 证据移出主路径」这一结构决策。
- **自检**：`check_repo` 通过（551 md；12 论文 / 8 开源 / 17 材料卡）。

## 2026-11-12 05 证据池修复：接通 papers + CoeusBI / UniDataAgent 准入

- **诊断**：05 的 8 条证据全来自 `src/web/`，与 `src/papers/` 断开；已过门的 Apple Glyph 与 Narrow and Deep 从未进入 05，窗口内还有一批未评的工业论文。
- **接通（不改准入）**：Glyph 进 06.1（#6）、00 证据表、03.5、02.1、90.1；判 **A（probation）**——card 是 `admitted`（§4.4 公司例外），但 05 的 A 要求独立信号，Glyph 只有 I3；到期 2027-03-09。上游改 E-28/E-29 与 L18/L19：新增「**权限会前置地限制语义生产**」（最敏感表不许先读值再分类）。
- **新准入**：`src/papers/2606.15384-coeusbi/`（百度，VLDB 2026 accepted，I1 VLDB + I2 百度/北邮）判 `admitted`，05 判 **A**；`src/papers/2609.27257-unidataagent/`（联通软研院+南开，I1 ICDM 2026 Demo + I2）判 `admitted`，05 判 **A**。复核时补核了两条会议信息：CoeusBI 已见 PVLDB Vol.19 p.4076 + DOI + artifact；UniDataAgent 的 arXiv HTML 脚注写明「accepted by ICDM 2026 Demo track」，据此把 probation 升为 admitted。两篇都补齐 card/digest/paper/references/appendix/README，manifest 10→12。
- **评估不入库**：AstraZeneca（19 作者全属公司、15,000 用户/首年）→ `signal`，进 06.1b/frontier；Same Context（USC/Oracle/UPenn，7 模型/1,514 任务）→ 学术对照，进 90.3 G6 行与 frontier；Auditable by Construction（单作者、公开基准）→ 不建卡，只进 frontier。
- **结构补口**：05.5c 收益侧（6 个收益点，逐条说明为什么不能当 ROI）；8.2 缺口 8（非中美无生产案例）；02.1 叠加例子（中泰 OKF+治理资产、Sigma dbt→Snowflake）并注明「两个语义层并行」仍无案例。
- **微观核实**：QCon PPT 服务 API（`/serv/ppt/list`，conid=173）——中泰有幻灯片但下载需登录，小红书 DIPB 无幻灯片（摘要级是上限）；Medact 的 FDP briefing 被 Cloudflare 挡，FOI 原始数据未取得；江西 KG 项目未见采购公告，`<50 万` 口径仍未说明。
- **自检**：`check_repo` 通过（550 md；E=32，Q=3，C=4，L=86；12 论文 / 8 开源 / 17 材料卡）。

## 2026-11-12 05 缺口二轮补搜：三条 signal + 两条价格锚点 + 阴性清单

- **问题**：05 的七条 gap 停在“已判定不存在/缺”，但部分检索面没扫过：TED 结构化 API、HN Algolia 日期检索、QCon 2026 日程（找中国具名案例）、云厂商产品名 + 客户、审计机关（NAO/GAO/ANAO）、FOI 调查报道。计划见 [gap closure plan](../../deliverables/_plans/2026-11-12-05-gap-closure-plan.md)。
- **命中（全部 signal/B 级，不过门）**：
  - 江西农商联合银行（金科创新社 2026-09-29）：**投入 <50 万元（上限）**；2026-05 需求→08 上线→10 月推广 86 家；6 试点/68 用户/3,000+ 隐性关系；三层解耦含「业务语义层」。
  - 江南农商银行（2026-09-22）：**12 个月、3 人核心组 ≈36 人月**；2,000+ 知识页/500 DAU；文档整理 2.7→0.27 工时/份，年省 ~1,200 工时。
  - 小红书 DIBP（QCon 上海 2026-10-22/24）：2026-02 起建，覆盖 **80%+ 员工**、主动会话周活 **8,800+**；Context Layer。判 **B**（具名采用，摘要级）。
  - NHS FDP × Palantir（Guardian 2026-11-02 / Register 2026-11-03）：£330M 合同；**29 家 FOI 否认使用**（Register 以 137 家「realising benefits」为分母≈21%；Guardian 记为「live」）；OSR 介入。判 **signal（调查报道）**，是「宣称 vs 使用」不是工程复盘。
  - 价格锚点：东北大学本体仿真服务 **¥80 万/1 年**（比选预算，2026-11-09）；Leibniz-IWT **€270k** 本体开发服务（TED 469346-2026，2026-07-08）。
- **上游回写**：mechanism F9 限定（不再说“没有一条给人月/金额”）、F10 证据（小红书 + NHS）、新增「2026-11-12 补搜」小节；findings F9；06-L21 改写 + 新增 **06-L24**；E-31 限定与出处；frontier 新增四行候选。
- **下游回写**：05 的 00（判断三/四）、03（NHS）、04（4.4.6 表加成本列 + 新增 4.4.7 小红书 + 4.5/4.7）、05（新增 D 组客户自述 + 5.5b 人月行 + 读法五句）、06（6.1b 三行 + 6.4）、08（缺口 3/5/6 + 反例）、90（90.2 三行、90.2d 四行、90.3 五格、90.3b 两行口径、90.4 检索面）、README（30 秒结论 3、证据基座）。
- **仍阴性（本轮新扫）**：五平台产品名 + 客户 0；审计机关无本体/KG 专项；HN 2026-06 后无 KG 关停复盘；无生产级同数据集对照（只有 Greptime 厂商 504 次对照，C）；仍无同一买方建设+维护配对、无人月单价、无回收期。
- **自检**：`check_repo` 通过（537 md；E=32，Q=3，C=4，L=86）。

## 2026-11-12 04b OKF 严格化：拆层 + 补证 + 降级

- **问题**：用户指 4b 是“硬挤进去”的，未走严格流程；尤其“靠向本体”一段混了三种东西——规范边界（不是本体）、映射机制（可以投影）、采用/迁移证据（有人在试），并夹带了没有上游的源（SCIMIN、Linked.Archi 无卡；Kunstenpunt/京东海博是 `signal` 却当交付物证据）与伪精度阈值（≥2 跳 >20%、>10^4 concept 等，无任何来源）。
- **诊断**：[04b provenance 审计](../audits/2026-11-12-04b-okf-provenance.md)（7 处 P0 / 9 处 P1 / 5 处 P2）。根因：先写正文再回头找材料；找不到的用记忆补，找到的越级用。
- **补证与判定（先建卡、后降级）**：读 [SCIMIN-CRM · Semantic MediaWiki](https://ceur-ws.org/Vol-4293/paper50.pdf)（SEMANTiCS 2026 / CEUR Vol-4293 paper50，2026-10-13）——**本体先行**：OWL 本体 + SMW 标注 + LLM 候选 + 自动校验 + 专家 HITL + 受控发布。**初判 `admitted` 是手松了**：这是承建方（AKKODIS Research）写自己的 demonstrator，G3 的“多机构/I3 采用”都在同一个 Horizon Europe 项目内部，不是独立采用；无量化/规模/成本。按用户“尽量找严格”的要求**复核降为 `signal`，移出 `src/`**，只留 frontier 与 90 线索；正名 `CRM = Critical Raw Materials`。另核 Linked.Archi（2026-07-17）/ Atlas interop spike（2026-07-02）/ GMEOW 三份独立实现，均判 C。
- **上游改写**：mechanism OKF 节把“从 OKF 到本体”重写为**两个方向 + 一条缝**（投影有损 / 上提需关系定型人审 / relationship-typing gap），映射缺口分“规范明确不做 / 规范明确没有 / 实现与分析”三档；E-32 补“非对称投影 + 没有完成迁移的案例”；L-22 收窄，新增 **06-L23**（非对称投影，已核工程文档互证）；frontier 新增三份实现 + 两条抓取失败待评估（Zenodo NKB、SAP community）。
- **下游回写**：4b 重写为 9 节（结论 / 问题 / 规范 / 谁在用 / Knowledge Catalog / 两个方向 / 3 条信号 / 反例 / 证据台账）；删伪阈值与 GitHub 501 计数（复跑 477，只进 90）；Kunstenpunt 从“B 类反例”降为 `signal` 且改“数据标准先行”；京东海博移出正文只留 90.2c；90.3 新增“OKF→本体迁移完成案例 = 0”阴性行；README 证据基座加“admitted 格式/架构证据 2”。
- **图与文字对齐（SVG 生产在前，重写在后）**：`landscape-stack.svg` 底部原写“可长期用，也可按需升级到语义层”，与重写后的“不会自己升级、无迁移完成案例”冲突——改为“不是本体；要约束/权限时另建语义层”；Wiki/OKF 卡片摘要由“低成本 · LLM 友好”改为“非本体 · 无约束”（价值说明下沉到底部注）。`heavy-to-light.svg` 的 Wiki/OKF 卡补“非本体 · 无推理”，证据徽标由“A（中泰）/ signal”改成“A（中泰）· 迁移案例 0”。两张图的 `<desc>` 与 02 图注同步补“知识容器、不是本体”。
- **自检**：`check_repo` 通过（537 md；E=32，Q=3，C=4，L=85；10 论文 / 8 开源 / 17 材料卡；0 坏链/0 坏锚）；顺带把脚本里过期的结论等级期望 15/3 同步为 19/4。

## 2026-11-12 05 三期：可读性收口（77 → 85.6）

- **问题**：二期后自评 77，卡在四处：C2 同一批数字在 5 页重复；A2 只有空决策卡；B1 场景在 00 不在 README；B3 产品名无解释；D2 口径散落。
- **做法**：五个编辑代理并发——03.5/04.5 台账改引用 + 06.1 作 canonical（C2）；07.5b 填好的决策卡示例（A2）；README 问题链主线 + 00 承接句（B1）；01.2c 产品名表 + 1.2d 类比（B3）；90.3b 九类口径与不可比说明（D2）；另加 06.1 证据类型图例（D1）。
- **自评**：85.6/100（可对外区间）。C2 仍 3（主路径约 3 万字 > 2 万字档）；A1/A3/D3 仍 4（缺人月、项目级 postmortem、五平台客户）。评分见 [05 质量评估](../../deliverables/_plans/2026-11-12-05-quality-review.md)。
- **自检**：`check_repo` 通过（0 坏链/0 坏锚）。

## 2026-11-12 05 缺口收口（二期）：一致性 + 成本锚点 + OKF 卡

- **问题**：05 一期成稿后，C 层有 7 处一致性冲突（Palantir 等级、A 弱/probation 写法、三件套/四件套、四种/五种形态、G1 同名、gap 计数、probation 到期日）；成本章停在“没有金额”；OKF 章的事实没有上游卡；五平台客户侧与失败率只有“缺”没有“判定”。
- **上游**：E-28 移出阿里 C、加“严格 OWL 只有 Netflix”；E-29 改正向并加“未测图引擎”；E-30 标窗口外源并写“五平台 0 具名客户”；E-32 去京东海博、改链 Google OKF 卡；conclusions 出处纪律补 web 材料规则；claims L-18–L-22 对齐；mechanism F7/F8/F10 与 OKF 节措辞同步；frontier 补两条判定。
- **证据**：新增 [Google OKF 卡](../../src/web/google-okf/google-okf.card.md)（`admitted`，规范正文 + 三篇博客逐字核）；成本章补五类价锚点（£10.09M/5 年、$1.14M/年、¥115–190 万、¥178.8 万/年、$37–175/月）；04 补 3 家农商行客户自述（signal）、五平台 0 客户、7 例采购流标（授标前、供给薄）；08 补 Westpac 退出与“项目级 postmortem 不存在”。
- **一致性**：Palantir 统一 C；A（弱）/A（probation）统一并在 02.5/01.2b 定义；三件套→四件套；四种形态→五种；G1 拆成“时效门”与“缺口 1–6”；VB Pulse 日期、Netflix 4h/1–2h、QCon 日期、中泰 OKF 补进 04；删 158 万/501 两处无出处精确数。
- **评分**：[05 质量评估](../../deliverables/_plans/2026-11-12-05-quality-review.md) 77/100（可读可用）；冷读代理结论与主线一致。
- **自检**：`check_repo` 通过（534 md；E=32，Q=3，C=4，L=84；10 论文 / 8 开源 / 17 材料卡；0 坏链）。

## 2026-11-12 路线 B 收口：坏链/错页 + p_h 标定贯通

- **问题**：349a8e4 批量追加后有 11 条嵌套坏链（内外两层方括号指向同一 mechanism）；E-01/E-18 指错页，E-14 的 p_h 口径与 compilation mechanism/02 相反。
- **conclusions**：11 条链接改为单层；E-01→compilation §实施决策，E-18→metrics §方法要求，E-14→新 p_h 标定锚点；E-08/E-19 路径标签改为名字；E-21 阈值改为“自己的 gate 重标，论文数值只作单设置参考”；E-23 改为动作先行；E-07 去掉断裂标记；E-22 补“换域/换 backbone 重跑融合消融”。18 条在役做法逐条过三条测试，只改不满足的 4 条，其余保留；E-14/E-22/E-23 的做法句压回一句级。
- **compilation**：新增“p_h 标定（判门用）”（100–200 smoke；1,600–2,000 shadow + 95% CI 下界；先 shadow；门实现先固定），并对齐 §实施决策/§stop/§第一个 sprint/§V3。
- **02**：evaluation 样本表、R3 做法与验收、acceptance/canonical 的 R3 停线改为 CI 下界；01 e3 数据表加标定指针，形成 E-14→mechanism→交付物的贯通样例。
- **check_repo**：嵌套链接记为 error（已验证注入后 exit 1）；active E 的做法/链接覆盖当时保持 warning，二审改为 error。
- **自检**：`check_repo` 通过（504 md，计数不变）；05 未纳入本轮。

## 2026-11-12 路线 B 二审：p_h 口径清尾 + 闸门升级

- **问题**：一审只把 CI 口径修到 compilation/02 主路径；01/03 与 feasibility 仍有多处 `p_h ≥/< p_min` 点估计判门，feasibility 的 sprint 仍写 100–200 问判门。
- **清尾**：01（capabilities/canonical/acceptance/e3）、03（context/appendix）、02 R3 适用性、03-knowledge README、feasibility mechanism（实施决策/stop/sprint/go/no-go）、E-19 全部改为 `p_h` 的 95% CI 下界；feasibility sprint 的 100–200 改 smoke，判门 1,600–2,000 并链到 compilation §p_h。
- **闸门升级**：`check_repo` 的 active E 检查从 warning 改为 error；要求 `**做法` 标记 + 实际 markdown 链接指向 mechanism/read-path/execution-forms/output-validation/consumability。
- **自检**：`check_repo` 通过（504 md，计数不变）。

## 2026-11-12 meta 目录重组 + meta/AGENTS.md 门牌 + 每份交付物 SCOPE.md

- **问题**：meta 根 14 个文件平铺，fresh agent 进来不知道读哪个；交付物只有 README，定位靠 meta 一个远页，容易跑偏。
- **meta 重组**：根只留 `README.md`（文件索引）+ `AGENTS.md`（30 秒入口）+ 子目录：`rules/`（conventions/checklist/excluded-sources/source-types/topic-research-protocol/loading）、`deliverables/`（scope/quality）、`status/`（state/state-log/term-baseline/models）、`templates/`（note-template/subtopic-template）、`audits/`、`archive/`、`tools/`。归档 2 个已完成开源计划（detox plan + absorption）。
- **meta/AGENTS.md 的定位**：只做门牌与指路，**不新增规则**；规则唯一出处仍是 CHARTER / 根 AGENTS / rules/。这样既给 fresh agent 就近入口，又不制造第二个路由器（ADR 0012）；该约束写进文件自身的「维护约束」节。
- **每份交付物 SCOPE.md**：01–05 各一份，含初心/定性/回答的问题/读者拿到/in-out-of-scope/红线/发挥空间/答不了怎么办；`check_repo` 强制存在。meta 页降为五份总索引 + 共用规矩。
- **04 改名**：`04-ontology-in-production` → `04-worked-example`（37 文件 98 处引用同步；名实不符是漂移温床——它是合成示例，不是生产现状）。
- **链接修复**：迁移产生 275 处相对链接断点，按「最长后缀匹配」重算并回落；check_repo 现在全绿。
- **自检**：464 md；0 坏链/0 坏锚。

## 2026-11-12 交付物定位系统（ADR 0014）

- **起因**：用户指出 04 *ontology-in-production* 跑偏——原想答「业界落地现状 + 靠谱与否证据」，却长成「不证明生产」的合成教程。根因：每份交付物的初心/定性/scope/红线从没定义成模型必须遵守的东西。
- **决策**：定位权威放 meta（单一出处，沿用 ADR 0012）——新增 meta/deliverables/scope.md；AGENTS 路由 / loading 加载集 / checklist 交稿闸只放指针；README 放读者钩子并指回。否决「散进 5 份 README」「塞进 AGENTS」。
- **定性五分**：01 判断 / 02 做法 / 03 机制 / 04 示例（合成）/ 05 现状（实证）。04 与 05 分界钉死：04 合成「怎么建」，05 实证「业界怎么样」。
- **防漂移硬规矩**：改/建前先读 scope；**答不了初心问题标 gap + frontier，禁止偷换成更容易的问题**；定性不混。
- **落地**：04 内容不动、如实定性为合成示例；新开 deliverables/10-production-landscape/（证据基座缺口如实标明，先补真实生产原料再过门写，不编）。GLOSSARY 加「交付物定位」。
- **自检**：check_repo 通过（458 md，新增 deliverable-scope / ADR 0014 / 05 README）。

## 2026-11-12 topics 撤回源叙述页对账

- **范围**：purge 后 topics 叙述页仍把撤回源数字当 `已核` 活证据的漂移（交付物正文经扫描已干净，漂移在上游 topics）。
- **方法**：逐页判断——经验性结论唯一支撑撤回源 → 降 `推测`/历史示例；方法论/设计框架保留为 `推测`；admitted 源（CASTON/FIRME/CAI/CASEL/N&D/SLB/Agents/E-20）内容保留；混合页加对账横幅区分 admitted/撤回。
- **覆盖**：01-constraint（action-gate/reasoning-gate/reversibility）、02-judgment（evidence/checker/calibration）、05-produce（README/claims/generation/representation/lifecycle）、06-measure（metrics/mechanism/failure-attribution/feasibility/claims）。11 提交。
- **等级修正**：06-L2（E-06 Diagnose）已核→withdrawn；05-L1/L8 注 E-02 撤回。
- **其他**：01 capabilities 补 frontmatter；generation run 日志加 pre-purge 快照注记。
- **验证**：交付物正文 grep 无撤回源当活证据；check_repo 通过（455 md）。
- **剩余长尾**：个别混合页行级标记（已有横幅覆盖）；历史 run 日志为快照，不作现役判断。

## 2026-11-12 指令层结构整改（ADR 0012）

- **诊断**：[指令层审计](../audits/2026-11-12-instruction-layer-audit.md)——8 张路由表、准入规则 7 处复制、修复回路缺失、3 处已证实漂移。
- **AGENTS 重写**：唯一任务路由表 + 常设修复回路（完成判据：被指句可追 admitted 源 digest 节，否则显式标推测/gap）；「单向不可反向」改为「判断顺流而下，证据逆流而上」。
- **单一出处**：门→CHARTER §4；字段→conventions（词汇冻结，新增需 ADR）；计数→state；digest 契约→src/README；质量口径→rubric。README/loading/topics/deliverables/src README 的复制件删除或改指针。
- **计划层**：_plans 现行唯一（IA 计划）；core-plan 降为交接快照/日志，不再自称「唯一执行口径」；16 处「现行」重标为参考/日志。
- **漂移修正**：README 不再抄材料卡数（旧 9≠state 11）；src/README manifest 注释 28→10；AGENTS 的 G2 丢限定转述删除。
- **新术语**：修复回路（GLOSSARY）；checklist §3 增修复回路收口检查。
- **自检**：check_repo 通过（452 md）。

## 2026-11-12 内容层 purge 对账 + 缺口盘点

- **frontier 对账**：六派候选队列把 18 篇移出论文从「已入档」改「已移出」+ tombstone；pre-window 候选（LOGicalThought/APEX-MEM/KROMA/AriadneMem/Time is Not a Label/OpenPort/Outcome-Oriented）标「G1 不过」；本轮计划改写到过门新源。
- **硬对象**：T05/T06/T07/P02/P03 补标撤回（唯一锚 E-02/03/04 已撤回）；累计 20 撤回、现存 74（H3 33/H2 41）；M04 换锚 E-15。
- **execution-forms**：形态表从 36 源（含移出 18）重建为 18 源，与 state 一致；换词检查标历史快照。
- **frontmatter 卫生**：8 个交付物页 `evidence:` 加 withdrawn 注记；loading/appendix 旧数（28 篇/26 来源）修正。
- **判断层核验**：claims.md 27 条撤回 L 与 state 吻合，无需改。
- **缺口盘点**：[content-gap-survey](../../deliverables/_plans/2026-11-12-content-gap-survey.md)——证据基座、按派缺口、横切缺口、P0–P4 行动清单；外部前沿对齐由两个只读调研代理补充。
- **工具**：check_repo 对象地址检查识别显式 `<a id>` 锚点（与链接检查对齐）。
- **自检**：check_repo 通过（453 md）。

## 2026-11-11 撤回补偿：W 表 + 自测协议

- **W 表**：01 canonical §5、02 canonical §1.1、03 evidence/ledger §2.5 各一张；每行给「不能再用 + 重启前先量」，正文改短引用。
- **补协议**：01 map/acceptance/capabilities/decision-record；02 R4/R5/R6/R12 + acceptance/cost/readiness/case/traceability；03 五张位置卡 §7；04 build/reference。
- **换叙事**：03 README 新增「今天能验证什么」（可见性/离线校验/记忆/OBDA），并写明矩阵 `●` 少 ≠ 框架失效。
- **瘦身**：四份术语来源表 57→33 行；01 五页路径恢复；重复 banner 合并。
- **指标**：02 免责措辞 175→100（−43%）、03 224→196；效应量不恢复（有意）。
- **质量**：§12.3 桌面复评 01=87 / 02=84 / 03=85 / 04=86。
- **自检**：check_repo 通过（444 md）。

## 2026-11-11 内容精读 + 长尾旧数字清理

- **精读**：[content-read](../../deliverables/_plans/2026-11-11-content-read.md) 逐页读 01–04（约 41 万字符），判词 01 B+ / 02 B / 03 B+ / 04 B+。
- **清理**：撤回源（E-02/03/04/13/16/26、Grid、OA-RAG、OntoAct、Commit Boundary）的具体数值从 02/03/04 主路径删除或改定性；01 的 acceptance/canonical/boundaries/README/glossary 同步。
- **修正**：03 覆盖率矩阵 `action×A` 由 `●`→`?D`、`checker×B` 由 `●`→`◐`（原用撤回 E 撑 `●`）；SFE-O 不再作为 R0/成本出处；04 路线分数表标「源已移出、数值停用」；commit 卡点名 Commit Boundary 已移出。
- **自检**：`check_repo` 通过（443 md）；全文扫描只剩 admitted 源（E-05/E-12/E-14/E-17/E-20/E-21）的数字。

## 2026-11-11 规范主干接线 + 术语 v1 + 冷读收口

- **第 7 步**：四份术语页各加「§0 名词从哪来（N / local）」；01/02/03/04 + START 的定义句标 `（N: 标准名）`/`（local）`；`topics/trunk.md §5.1` 给标准→页面索引。
- **第 8 步**：`meta/status/term-baseline.md` 增 29 词 + 06 试点 1 词（「任务账/风险账」）；GLOSSARY 39 条全有 `_origin_/_anchor_/_scope_`；06-measure 试点 0 冲突，见 [术语审计](../audits/2026-11-11-term-baseline.md)。
- **第 9 步**：代理冷读 68→86；修 START「只记一句」与 01 的口径冲突、map 等级列混装 `gap`/`设计`、`gap` 只给「曾有 E 被撤回」、#14 例外、START 两个裸词；见 [cold-read](../../deliverables/_plans/2026-11-11-cold-read.md)。
- **第 10 步**：质量 §12.2 01=85 / 02=82 / 03=83 / 04=87（非真人冷读）；`check_repo` 通过（442 md）。
- **仍剩**：真人冷读、C2 冗余、02/03 长尾旧数字、ISO 21838 条款号。

## 2026-11-11 导航与质量管道修复

- **质量路径**：README §0 增「质量口径 / 最新评分」；deliverables README §质量评估 增 [§8 收口复评](../../deliverables/_plans/2026-11-11-quality-review.md#8-收口复评2026-11-11) 直链；`_plans/README` 增状态列。
- **计数**：state 拆为当前页 + 本日志；材料卡 8→12（4 web + 8 标准）；execution-forms 表补 10 源到 36；checker 新增 state 文件数、论文/开源/材料卡/形态分布比对。
- **指针**：01–06 派 README 的 `claims/sources/frontier` 改为链接；START/rubric/review 入库。
- **自检**：check_repo 新增锚点校验；修 5 个坏锚；「0 坏链」现在覆盖文件链 + 锚点。
- **归档**：checklist §7 与 src/README §5.1(7) 改指 conventions 长度目标 + digest 模板，不再把 archive/digest-audit 当现行标准。
- **小节**：src/README §0 重号修正；topics/README 八→九；loading ADR 0001–0010；`.tmp-venv/` 入 `.gitignore`。
- **自检**：`check_repo` 通过（531 个 md；E=27，Q=3，C=4，L=79；28 论文 / 8 开源 / 12 材料卡）。
- **内容合并（2026-11-11）**：01 六个能力页 → [capabilities/README](../../deliverables/01-capability-status/03-capabilities/README.md)（-6）；04 example 3→1（-2）；01–04 110→102，<600 字页 47→38；B3 首屏加内码映射。详见 [review §9](../../deliverables/_plans/2026-11-11-quality-review.md#9-c2b3-合并2026-11-11)。

## 2026-11-11 EXP-001 read-path 三执行点复查

- **做了什么**：仓库外 clone 两个候选，读代码 + 复跑测试。sparql-guard `6b68d769` 跑 `npx vitest run`：**76/76 passed**；holosdb `666238f` 的 `cargo test -p holos-security` 未跑成（本机 rustc 目标 x86_64 / arm64 linker 不匹配），代码读到 20 条 `#[test]`。
- **结论**：read-path 至少三个执行点——post-filter（trustgraph，node/subject，fail-open）、rewrite（sparql-guard，node+graph，fail-closed）、scan（holosdb，predicate+graph，默认 deny）。三者不能互替；E-23 的「单实现」限定只指 post-filter。
- **没证明**：没有泄漏率/误拦率；没有 harness 集成；两个候选都是 1★/单作者，未入库。
- **落点**：[read-path §3/§7](../../topics/01-constraint/commit-gate/read-path.md)、[F8](../templates/subtopic-template/findings.md)、[frontier](../templates/subtopic-template/frontier.md)；03 claim 走查、01 #8、02 R8 各加一句限定。
- **EXP-002**：sparql-guard 10 用例实跑（`test/exp002.test.ts`）7 pass + 1 fail-closed + 1 anonymous + 1 alias leak + 1 partial，0 false-block；trustgraph/holosdb 用代码忠实复刻（未跑产品）：trustgraph 5 leak + 1 conditional + 1 partial；holosdb 1 alias leak + 4 undecidable。
- **下一步**：补 trustgraph/holosdb 两列，或先接受「1/3 实跑 + 2/3 代码映射」的结论；不是再找引擎。
- **自检**：`check_repo` 通过。

## 2026-11-11 01/02/03 整改（02→01→03）

- **依据**：[差距评估报告](../../deliverables/_plans/2026-11-10-gap-assessment-report.md)（27 格：1 L2 / 2 L1+ / 0 fixture）+ [整改计划](../../deliverables/_plans/2026-11-11-remediation-plan.md)。
- **02**：新增 [artifact-pack](../../deliverables/02-engineering-playbook/05-appendices/04-artifact-pack.md)、[glossary](../../deliverables/02-engineering-playbook/02-sections/90-glossary.md)、[canonical](../../deliverables/02-engineering-playbook/02-sections/91-canonical.md)、5 组读者检查；对账 false-veto / R1 / 162（补 13 plant elements）。冷读 partial：卡点是 citation 正确性等真 gap；顺手修了 9.7k total vs 5,000 generated 的口径。
- **01**：A/B/C/D 改为有序规则（含 undetermined）；新增 [decision-record](../../deliverables/01-capability-status/02-sections/09-decision-record.md)（K1→A、读路径→B、离线 SHACL→A）、[glossary](../../deliverables/01-capability-status/02-sections/90-glossary.md)、[canonical](../../deliverables/01-capability-status/02-sections/91-canonical.md)；9 条期待补「没过怎么办」；C 桶统一 3；#12 标非本体。冷读第二轮 `yes`。
- **03**：新增 [claim-walkthrough](../../deliverables/03-mechanism-reference/02-sections/95-claim-walkthrough.md)、[reader-checks](../../deliverables/03-mechanism-reference/02-sections/92-reader-checks.md)、[glossary](../../deliverables/03-mechanism-reference/02-sections/90-glossary.md)；修 coverage「只有 G 没有 ●」→ C/E/F/G、覆盖率定义、E-22 台账、30%→31%、M1–M5 去重。冷读 partial：强读法需实测，属真 gap。
- **第二轮收口（2026-11-11）**：01 模板 + 第四记录（落盘→C）+ 逐数等级；02 分诊优先级 + 第二个 worked example（R1）+ citation 协议；03 placement + claim 模板 + D2 清理 + alias 规范；EXP-003 alias 前置。外部来源：新增 [ALCE](../audits/2026-11-11-source-purge.md#src-web-alce)、[OWL 2 Profiles](../../src/web/w3c-owl2-profiles/w3c-owl2-profiles.card.md)、[SHACL-AF](../../src/web/w3c-shacl-af/w3c-shacl-af.card.md) 三张卡（摘要级/待核，不升 E）。复评见 [gap report §10.7](../../deliverables/_plans/2026-11-10-gap-assessment-report.md#107-第二轮收口2026-11-11外部来源--文档层)。
- **证据层（2026-11-11）**：EXP-004 引文审计（20 对，κ=1.0；E 行 strict S=5/20；E+锚 11–13/20）；EXP-005 alias 前置在真实 sparql-guard 上 leak 1→0、false-block 0；EXP-006 holosdb 20/20 单测复跑通过；M1 因无干净被试标 `未测`（见 [03 gaps](../../deliverables/03-mechanism-reference/05-evidence/03-gaps.md)）。
- **未做**：不改 04；不新增 E/L；M1/M2 仍 gap；citation 仍无标签；不做外部读者。
- **自检**：529 文件；`check_repo` 通过（2026-11-11）。

## 2026-11-10 04 可执行性与决策支持补强（文档，不实现）

> 只做文档；fixture 只读复跑（rdflib/pyshacl/jsonschema），不做实验、不加 engine。现行计数看顶部表。

- **新增**：transfer（4 推导 + principal/多标签 2 决策 + 最小路径 + 自测）；templates（T1–T8 空表）；decision（成本五维/TCO、4 阶段、规模边界、conditional、memo、RACI）。
- **验收**：acceptance 增「期待与数据需求」X1–X5（验收规格，非 E）；README/GUIDE/sections/map/relations/body 索引接通。
- **缺口补齐**：新增 label-source（标签源三种路径 + 准入 8 问 + 50 列验证 + 停）；worked-example（3 表/6 列、多标签 B、5 规则/5 测试/2 audit）；decision §2.5（打标/执行层/审计公式 + 敏感性）；templates T9（成本工作纸）。
- **结构**：README 归位——04/README 只留读者卡/问题索引/产物地图/起点/门槛与边界入口/支持页；8 步读路径移入 GUIDE，5 组门槛移入 acceptance，3 条不能证明移入 boundaries，why-not-SQL 移入 relations；example/README 拆出 run.md / data.md；evidence/README 拆出 ledger.md / sources.md。
- **一致性**：CQ1 与 shape 片段加 `ontology.ttl` 同图前置；example 7→8 规则；T9 R4/R5；T11 命中 R5/R8；E-24 与 evidence 11 测试/8 规则/R4/R5；A.5 `CQ1` 改「2 列/2 表」；C.4/journey/B.6 去 `0/7` 混用；A.4 三组 catch/FA 补标签与样本量；glossary 加 PPV。
- **复跑**：3/3 parse；11 类/5 属性；pyshacl 2 violations；CQ1 2（TBox 同图）/CQ2 7 列 4 表/CQ3 4 dataset；audit schema 0 错；policy 11/11（含 T11 命中 R5/R8）。
- **未做**：不做实验；不加新 E；成本只有量级（`推测`），没有单价与 ROI；多标签/principal 是决策表，不是结论；worked-example 是示意，不是第二 fixture。
- **check**：`check_repo` 0 坏链 / 0 未定义 ID（508 文件；E=27，L=79）。

## 2026-11-10 04 内容整改（阅读/消化，不做实现）

> 历史快照：只记录这次改了什么；**没有跑示例、没有做实验**。现行计数看顶部表。

- **04**：B.6/A.5 的 CQ 期望拆 raw/governed + principal；CQ3 归 `governance`（R8）；`skip` 明确为未判定；C.2 8 条规则/11 条测试 + 判定顺序；C.4 per-subject + query log + 3 条样例；A.5 版本来源表；11 类改 WorkEmail（删 Address）；shape 范围 1–4；新增 journey/glossary；17 条边界。
- **topics**：policy 11 测试/R8/判定顺序；read-path object 计数 1 vs 3；consumability 范围补充。
- **未做**：不跑 rdflib/pyshacl/SPARQL；不做实验；不加 engine/harness/reference filter/EXP；不改 9 件产物数量；snapshot 仍是日期标签，严格 replay 未做。
- **check**：`check_repo` 0 坏链 / 0 未定义 ID（499 文件；E=27，L=79）。

## 2026-11-10 04 内容供给执行（W0–W3 主体，历史快照）

- **W0**：12 张矩阵骨架入 [04-matrix-skeletons](../../deliverables/_plans/2026-11-10-04-matrix-skeletons.md)；12 条承重句冻结。
- **W1**：T2 [querying/compare](../../topics/03-knowledge/querying/compare.md)（4×8 矩阵、17 类失败、决策树）；T5 [output-validation](../../topics/02-judgment/checker/output-validation.md)（六类 + 三态）；consume v2（决策表、2×2、失败目录）。
- **W2**：T3 [policy](../../topics/01-constraint/policy/README.md)（3 F / 3 G、7 列 schema、10 测试）；T4 [read-path](../../topics/01-constraint/commit-gate/read-path.md)（10 用例、第二实现否决）；govern v2（10 测试、12 泄漏用例、audit schema）。
- **W3**：T1 [consumability](../../topics/05-produce/representation/consumability.md)（三关、3×4、10 坏样本）；T6 [propagation](../../topics/06-measure/metrics/propagation.md)（10×3 故障矩阵、成本量级）；build v2（三关、10 坏样本）。
- **产物**：04 九件（5 主 + policy_tests / audit.schema / leak_cases / fault_matrix）。
- **收口**：M1–M4/M8/M9 标准已入材料卡；Great Expectations / OpenLineage 已入 OSS digest；M5–M7/M10 按 D7 降为候选；E23–E27 全部已升（读路径/策略层/可消费性/路线/输出）；04 body 14.12k（执行后修订 ≤15k）；模板 2 / gap 3；已核 17。
- **check**：495 文件；E=27，L=79；0 断链。

## 2026-11-10 04 内容供给计划（新）

- **新增**：[04-content-supply](../../deliverables/_plans/2026-11-10-04-content-supply.md)。
- **方向**：不再从 04 倒查；12 条承重句 → 6 张矩阵/目录（新页型 `compare.md`）→ 12 个 M 来源 + 1 个论文槽位；8 条靠整理/标准、4 条靠新证据。
- **三波**：W1 查询/输出 → W2 策略/执行 → W3 建/跨段；每波 gate，不过就删句。
- **停止线**：<7 条承重句有表/产物 → 04 并进 02 的 R13，目录删除。
- **口径**：标准/基准不套论文新鲜度；adjunct OSS 标 `ontology_role: adjunct`，不单独撑 E；计划不产生 E/L。

## 2026-11-10 04 重写（D1–D6，历史快照）

- **定位**：单读者（落地团队）；三链；一个 fixture（5 表/13 列）；5 件产物（契约/TBox/shapes/ABox/3 SPARQL/policy/2 audit）。
- **预算**：正文 11,995 / 12k；导航 1,457（8.5%）；md 17,045。
- **执行验证**：TBox+ABox 108 triples；CQ1 2/2、CQ2 7/4、CQ3 4、T1 3；pyshacl 2 violations；JSON 2 条可解析。
- **冷读**：4 轮（v1 12 blockers → v2/v3/v4 各 3 个 P0）；P0-1/2/3 定向复核 PASS；P1-4/5/6 已修；P2 剩余（Address 未用、CQ1 子类路径装饰、policy engine/Rego=gap）。
- **kill criterion**：不 kill；04 是「可执行的集成指南」，不是效果证明（建=模板、用=E-21 单设置、治=E-22/E-20 强但单企业/单实现）。
- **计划**：[04-deep-plan](../../deliverables/_plans/2026-11-10-04-deep-plan.md) §7.5–7.6。

## 2026-11-10 两个剩余缺口收口

- **E-03/E-12 的 H3**：[O-F14](../../topics/objects.md)（E-12 边际分解 54.6+19.8=74.4pp，薄层 73.4%）、O-F15（E-03 token 效率 12.7×，派生）；对象 **94**（H3 36 / H2 58），**E 级 H3 10/10**。两者均 `derived`，不改变单源事实。
- **C-03 的 2×2**：[06-L16](../../topics/06-measure/claims.md) + [O-M04](../../topics/objects.md) + [03 measurement §2.5](../../deliverables/03-mechanism-reference/04-across-positions/03-measurement.md#25-机制类型与尺子分派)；逐格已核，方向翻转仍是跨来源综合（无同数据集两把尺子对照）。
- **阶段盘点**：[stage-review](../../deliverables/_plans/2026-11-10-stage-review.md)：四层水位、三个闭合、三个仍开。

## 2026-11-10 交付物接线（M/R/X）

- **ADR**：[0009](../../adr/0009-object-layer.md) 状态改为**接受（方案 A）**；[checklist](../rules/checklist.md) §3、[loading](../rules/loading.md) 规则 1、[objects](../../topics/objects.md) 头部三处同步：O 可作地址，主句仍落 E。
- **M**：[02 §5.1](../../deliverables/02-engineering-playbook/02-sections/05-acceptance.md#51-验收与-stop按机制选尺) 13 行 × 7 列；13/13 有出处，11 行挂 E/公式，2 行 `工程建议/gap`（R0、commit）。
- **R**：[03 boundaries §0](../../deliverables/03-mechanism-reference/05-evidence/02-boundaries.md#0-反例集r-table) 12 条反例，带数/条件/`O-Rxx`；B1–B15 原表保留。
- **X**：[03 execution-forms §3](../../deliverables/03-mechanism-reference/04-across-positions/02-execution-forms.md) 5 行加 `O` 列，补 OPA；Qlever 标「无代码锚」。
- **冷读**：3 条路径（编译/checker/read-path）均 2–3 跳到 digest 锚；0 断链，0 交付物 L 引用；1 个误读风险（O 是地址不是结论）已在 M-table 脚注写明。
- **计划**：[wiring-plan](../../deliverables/_plans/2026-11-10-wiring-plan.md) 全部验收勾选；check_repo 通过（467 文件；objects 91 / H3 33 / H2 58）。

## 2026-11-09 硬对象层（O-xx，R1–R5）

- **新增** [topics/objects.md](../../topics/objects.md)：地址层，不是结论层；**91 个对象**（C15 代码 / F13 公式 / T13 停线 / M3 矩阵 / N29 数值 / R12 反例 / P6 协议），H3 33 / H2 58；10 条承重 E 各 ≥3；**E 级 H3 8/10**；锚点 25 处（`path#anchor`）全部打开。
- **执行对比**：R1 C+F 22 个（H3 18，E 覆盖 2/10）→ R2 +T 35（22，2/10）→ R3 +M 38（**25，2/10**）→ R4 +N 67（27，**10/10**）→ R5 +F6/R12/P6 91（33，10/10；**E 级 H3 2/10 → 8/10**）。**R3 已到 25 个 H3 但覆盖只有 2/10**：H3 是手段，E 覆盖是目的。详见 [plan §12](../../deliverables/_plans/2026-11-09-hard-objects-plan.md#12-执行对比六轮以及达到目的是什么意思)。
- **偏差/收口**：F 9/13 到 H3（F03–F06 缺 γ/单价/样本量实测，保持 H2）；承重 E 的 H3 覆盖 8/10（E-01/E-02/E-04/E-05/E-14/E-15/E-17/E-20），超过计划 ≥7/10；E-03/E-12 无可复算量；R12/P6 已补完。
- **待决**：[ADR 0009](../../adr/0009-object-layer.md)（O 能否进交付物）状态为**提议**；在定案前按方案 B，交付物不引 O。
- **首轮抓到的偏差**：`O-F01` 复算 digest §4.3「Q=1,000、c=10 → 3.12%」得 3.08%（差 0.04pp），`c`/`Q` 疑为 rounded。
- **自检**：`check_repo.py` 已加 O 检查（warn-only）：对象字段/重复 ID/硬度/锚点/未定义引用；输出 `objects: 91 (H3 33 / H2 58 / H1 0)`，0 warning。

## 2026-11-09 交付物逆向补齐 + 硬对象产线

- **新增**：[reverse-gap-plan](../../deliverables/_plans/2026-11-09-reverse-gap-plan.md)：从四份交付物反扫 topics/src，诊断四种薄法（17/22 单源、31/73 推测、13 行停线 0 出处、5 个门无第二实现/标签），给三条硬杠、旗舰三件（门槛表 / 反例集 / 执行矩阵）、上游订货单（TB/CA/FC/QP/S2/LB）与 WP0–WP8。
- **新增**：[hard-objects-plan](../../deliverables/_plans/2026-11-09-hard-objects-plan.md)：把判断做成可引用/可复算/可核对的对象（O-xx）；H0–H3 分级、六字段 schema、`topics/objects.md` 注册表、五条产线（C/F/N/T/M+R/P/L）、10 天 60–80 个对象；O 能否进交付物待 ADR 0009。
- **定位**：工作底稿，不产生 E/L；与 [01 计划](../../deliverables/_plans/01-capability-status.md)（E1–E9 证据）、04 计划（intake/scope）分工，不重复。
- **口径**：desk research + 只读代码；不向用户要资产/人/价/签核（ADR 0007）；停线出处标不出就标 gap，不编。

## 2026-11-09 D1 第一轮证据回抽

- **数据表**：[e3](../../deliverables/01-capability-status/09-data/e3-compilation.md) / [e4](../../deliverables/01-capability-status/09-data/e4-checker.md) / [e5](../../deliverables/01-capability-status/09-data/e5-false-veto.md) / [e6](../../deliverables/01-capability-status/09-data/e6-memory.md) / [e7-e8](../../deliverables/01-capability-status/09-data/e7-e8-code.md) / [P0 扫描](../../deliverables/01-capability-status/09-data/p0-source-scan.md)。
- **D1 verdict**：5 条 `supported（限定）`、1 条 `conditional`、3 条 `unknown`；见 [01 §2.4](../../deliverables/01-capability-status/02-sections/02-map.md#24-e1e9-verdict2026-11-09-第一轮) 与 [§9](../../deliverables/01-capability-status/02-sections/05-acceptance.md#52-期待与数据需求验收规格)。
- **关键结论**：E5 false-veto 仍 `unknown`（1,745 blocked 无标签）；E8 无写授权实现；E4 的 data-derived 在 UniProt 真实答案上过 +5pp/FA≤15%，curated FA 16.8% 超线；E6 只有部分设置过 +10pp/90%。
- **P0 候选**：2610.16838（授权 benchmark，go）、2607.22868（false-block/miss 前沿，go）；尚无 commit gate 实现。
- **topics 回写**：[02/checker F9](../../topics/02-judgment/checker/findings.md#f9--用-d1-的5pp--fa15阈值套-e-02) 已落账（data-derived 在 UniProt 真实答案上过 +5pp/FA≤15%；curated FA 超线）；其他数据表结论仍留在 deliverables 工作底稿，待第二轮决定是否升。
- **下一步**：落盘 2610.16838；读 2607.22868 正文；复核 sparql-guard 候选（是否建卡/是否有 harness 调用点）。

## 2026-11-09 D3 机制参考 v1.0 结构

- **四层结构**：[03 README](../../deliverables/03-mechanism-reference/README.md)（主张类型 E/C/H/D/G + 四轴 crosswalk + 六位置表）→ `positions/`（context/memory/evidence/checker/action/commit + outside）→ `across-positions/`（measurement/coverage/execution-forms）→ `evidence-ledger` / `boundaries` / `gaps`。
- **上游合成件**：[execution-forms 执行链](../../topics/execution-forms.md#执行链求值决策执行授权审计)（求值→决策→执行→授权→审计）；[metrics/coverage](../../topics/06-measure/metrics/coverage.md)（七类失效 × 八位置矩阵）；[metrics/mechanism 八行分派](../../topics/06-measure/metrics/mechanism.md#按位置分派八行设计)。
- **关键修正**：「强度–覆盖率反向」保留为 H（摘要），矩阵为 D（操作定义）；矩阵显示位置是专门化的，**不能排成一条强度线**；`checker` 4 个 `●/◐`、`action` 3 个，不能按格子数排强弱。
- **未新增 E；新增 1 条 L**：只抽取现有 E-01–E-20 与 C-03/C-04；分类设计记为 06-L15；commit 写路径、false-veto、M1 同本体跨位置仍标缺口。
- **页码/主证据**：position 卡的 8 字段（机制/触发/能改变/拦不住/使能/证据/可证伪/上游）统一；六位置表与附录互链，附录降为长版论证。
- 自检：`python3 meta/tools/check_repo.py` 通过（426 文件；E=20，Q=3，C=4，L=66；24 论文 / 4 开源）。

## 2026-11-09 交付物重构

- **三个子目录 = 三种交付物**：新增 [01 现状](../../deliverables/01-capability-status/README.md)（能力矩阵：A 可先落地 / B 可试点 / C 只能设计 / D 反向；可当工作前提/不能当工作前提；距离表）、[02 工程实施](../../deliverables/02-engineering-playbook/README.md)（五步法、R1–R9、4 个开源参考、论文/开源指示分级、参考架构、最小落地路线、验收表）、[03 机制参考](../../deliverables/03-mechanism-reference/README.md)（三层分工、三条轴、六位置一页表、15 条边界）。
- **没有独立 handbook**：原 7 章、4–6 万字书稿计划废弃；唯一保留的是原第三章，现为 [03 的长版附录](../../deliverables/03-mechanism-reference/05-appendix-constraint-spectrum.md)。原 outline / planning-notes / handbook README 已删除，git 历史保留。理由：书稿无独立角色、后四章缺证据、主线过强。
- **E-16 数字口径修正**：conclusions、ch03、01-constraint/sources、01-constraint/claims 的注记原来写成 `Tacit-FLE 64.3/66.7/65.0% vs IfR 64.3–65.0%`，与 OntoAct digest（Table 1）不符；改为 `78.6/83.3/90.0% vs IfR 64.3/66.7/65.0%`。这是转写错误，不是新判断；01-L11 原本就是对的。
- **交付物 README**：清单改为三个子目录（01 判断 / 02 操作 / 03 依据）+ 03 的附录；新增「handbook 的去留」与待做（图/Deck/案例页）。
- **01 证据计划**：新增 [plan.md](../../deliverables/_plans/01-capability-status.md)：E1–E9 的覆盖审计、现有 digest 回抽（H1–H6）、新 `src/` 来源（P0/P1/P2）、WBS、排期、DoD 与停止规则。定位是工作计划，不是结论。
- **反向加载**：[meta/loading](../rules/loading.md#从交付物倒查反向加载) 新增「从交付物倒查」三条链（01 期待→plan→digest；02 recipe→mechanism→digest；03 边界→E→附录）；三份 README 加「加载集」表；[topics/README](../../topics/README.md) 与 [src/README](../../src/README.md) 加反向读法指针。
- **支持层契约**：[meta/loading](../rules/loading.md) 加「支持层契约」；[conclusions](../../topics/conclusions.md) 加反向阅读规则（E→digest §4/§5→frontier）；[topics/README](../../topics/README.md) 加反向路由表；[src/README](../../src/README.md) 加 digest 四节锚点；[plan](../../deliverables/_plans/01-capability-status.md) 加 E1–E9 → frontier 指针。目的：先保证 E→digest→frontier 可走，再开始倒逼。
- **验收规格**：三份 README 末尾各加「期待与数据需求」：把期待写成可证伪句，列出「支持它需要的数据 / 现在的证据 / 缺口」。作用是逆向暴露证据缺口，不是新结论。
- **术语**：GLOSSARY 新增「评测账本（Evaluation Ledger）」，与「台账」区分；交付物里的 `p_h`/false-veto/审批成本都指前者。
- 自检：`python3 meta/tools/check_repo.py` 通过（329 文件 / 22 论文 / 4 开源；E=20，Q=3，C=4，L=65）。

## 2026-11-09 手册第三章初稿

- 原第三章现为 [03 的长版附录](../../deliverables/03-mechanism-reference/05-appendix-constraint-spectrum.md)：9 节、约 0.97 万中文字符；12 条 E + C-03；强度/覆盖率反向标组织假设；六个位置逐节；E-20 放 3.3。
- 原 planning-notes / outline 已删除（git 历史保留）；第三章证据行、图法与「准确率说法集中在弱端」的收窄记录不再有文件指针。
- 更新 [deliverables/README.md](../../deliverables/README.md) 清单。
- 写作检验：topics 够用；六位置逐节未出现必须回写的判断缺口；已知缺口仍是 commit 写路径无实现、false-veto 未测、E-20 非效应量。
- 自检：`python3 meta/tools/check_repo.py` 通过（327 文件 / 22 论文 / 4 开源；E=20，Q=3，C=4，L=65）。

## 扫描状态（全局视图）

> 历史快照（2026-11-09）；现行候选队列看各派 `frontier.md`，本表不再每周更新。

| 派 | 最后扫描 | 下一步 | 入口 |
|---|---|---|---|
| 01 约束 | 2026-11-09（开源 trustgraph） | false-veto/剪枝率；Commit Boundary 实现 | [frontier](../templates/subtopic-template/frontier.md) |
| 02 判定 | 2026-11-07（首轮外部） | LogT / CORE-LLM-Bench 待落盘 | [frontier](../templates/subtopic-template/frontier.md) |
| 03 知识 | 2026-11-07（首轮外部） | Grep 候选；投影粒度 | [frontier](../templates/subtopic-template/frontier.md) |
| 04 状态 | 2026-11-07（首轮外部） | APEX-MEM 候选；determinism 设计 | [frontier](../templates/subtopic-template/frontier.md) |
| 05 生产 | 2026-11-08（G-X 回写） | KROMA 候选；可消费性 | [frontier](../templates/subtopic-template/frontier.md) |
| 06 测量 | 2026-11-07（首轮外部） | AgentDebugX 候选；机制→尺子表 | [frontier](../templates/subtopic-template/frontier.md) |

## 2026-11-09 删除 D0/试点线

按用户决定，“D0 资产门 + 内部试点”整条线删除：

- 删除 `meta/implementation/`（7 个文件：plan/status/gates/cost-model/d0-gate/report/README）。
- 删除 `deliverables/pilot-playbook.md`。
- 删除 `experiments/EXP-004-narrow-deep-k1.md`、`EXP-005-action-gate-shadow.md`、`EXP-006-ontology-checker.md`、`_pilot-template.md`。
- 不再请求具名域、日志、题库、人或单价；外部客户试点不是本仓库的路径。
- git 历史保留；若以后真要做企业试点，可从历史恢复，但不在门厅出现。

## 执行形态代码核对（2026-11-09）

在 card 所 pin 的 commit 上读代码（未跑测试；不改结论等级为「已证」）：

| 项目 | commit | `seam` | `execution_form` | 核对要点 |
|---|---|---|---|---|
| trustgraph | `184f622` | `read-path` | `engine` | SHACL-AF 策略求值；fail-open；只删 subject 侧；31 条策略测试存在 |
| semantica | `39cf721` | `checker` | `compiled` | 本体→SHACL；pyshacl `inference="none"`；CLI 校验 |
| ontop | `964dbb7` | `supply` | `engine` | TBox 饱和 + 查询重写 → SQL；不是 gate |
| open-ontologies | `375fbc4` | `none` | `engine` | SHACL→SPARQL / verified Core；影响报告 + CI 规则门；不是单次写授权 |

写入位置：[topics/execution-forms.md](../../topics/execution-forms.md#代码级核对2026-11-09)（矩阵 + 4 条代码级判断）、[seams](../../topics/seams.md#轴外位置可记录但不是六时刻)、4 个 digest 的「2026-11-09 代码核对」段、checker F7 的接口边界。

关键发现：`engine` 不是一种语义（OWL 重写 / SHACL-AF / SHACL 校验）；执行 ≠ 健全（trustgraph fail-open）；执行 ≠ 授权（open-ontologies 只做 CI/报告）；三态在 JSON 保留、在 shell 退出码被折叠。已升 [E-20](../../topics/conclusions.md)（`已核（代码）`，不是 `已证`）。

## 冷启动复测（2026-11-09）

只读新 agent 复测：实际加载约 2,100 行 / 27 个文件；结论「能读懂，不能 15 分钟改仓」。首轮发现 4 处入口问题（loading 的 E-19/EXP/ADR 计数、README/state 的 18+2+3+4 计数、manifest 21–22 行断裂、topics/README updated），均已修复；复核 4/4 pass。`experiments/` 已无目录，D0/试点只在 ADR/归档/state 删除记录中。15 分钟路径已补 `meta/state`，并明确「只够读懂，不够改仓」。

## 薄页合并审计（2026-11-09）

15 个独立来源 <2 的子主题逐页审计：全部有独立机制或独立判断，**本轮 0 个合并**；`determinism` / `lifecycle` 列为下轮复核。规则与审计表见 [ADR 0008](../../adr/0008-thin-subtopics-merge-audit.md)。「薄」是来源计数，不是冗余信号。

## 本轮修复（2026-11-09）

- E 层：全部 E-xx 出处改链 digest（17 条）；E-04 去掉“支撑 P3”的范畴错误，改标 P3a，并新增“E-04 能/不能支撑什么”范围框；Q-03 收窄到单基准/单 gate；outline 第 6 章去掉“reward 低估”的方向断言；合法意图归因降回 `推测`。E-04 共 37 处引用，4 类过度解读（结构有效 / P3b / reward 低估 / 合法意图）已修。
- 硬矛盾：E-05 错挂回改；02-L2 改为“模型自评”；开源接缝改为 `read-path` / `supply` / `none`；manifest 合并为 22 篇单账；GLOSSARY 工位改为 3 个；P3 拆 P3a/P3b。
- 结构：新增 `execution_form` 轴（[topics/execution-forms.md](../../topics/execution-forms.md)，[ADR 0006](../../adr/0006-execution-form-axis.md)）、`evidence_role`、`also_supports`；26 个来源全部落字段（9/4/6/3；engine 4 / compiled 7 / context 2 / label 1 / none 12）；E 行影响列改用 P1a/P1b/P1c/P2/P3a/P3b；15 个薄子主题标记；L1/L2/L3 定义与长度门重写。
- 账本：meta 索引 + 归档（8 个一次性文档 + full-audit）；state.md（本页）；可执行自检（ADR 0005）；ADR 索引（含 0006）；manifest 合并为 22 篇单账（含批次列），删除 manifest-scan。

## 2026-11-09 02 工程手册 v2

- **结构**：02 改为「README 门厅 + `recipes/`（R0–R12）+ `operations/`（账本/评测/成本/上线/领域）+ `appendices/`（接口/追溯/案例）」；README 保留决策图与 R 索引，细节下沉到分片，避免单页继续膨胀。
- **三份同构**：01/02/03 统一为 `0 一页结论 / 1 怎么读 / 2 地图 / 3 主体 / 4 边界 / 5 验收 / 6 关系与维护`；顶层 [deliverables/README](../../deliverables/README.md) 做总导读；每份另有 `GUIDE.md` 做本份导读，子 README 只做索引，`sections/` 放 2/4/5/6，主体分别是 `capabilities/` / `recipes/` / `positions/`，条目字段统一为「一句话/适用/证据等级/边界/去哪」。01 的旧 `plan.md` 移到 [`deliverables/_plans/`](../../deliverables/_plans/README.md)，不占交付正文章节。
- **新增**：R0 本体可执行性体检（四项准入：名字/单位、声明、覆盖、执行落点）；R10 离线/CI SHACL；R11 OBDA 查询重写；R12 受监管供给（citation + solver + 人签核）。R1–R9 保留编号，避免 01/03 的 R 引用漂移。
- **R8 第二实现**：外部扫描发现 `Matdata-eu/sparql-guard`（Apache-2.0，HEAD `6b68d769`）：TS 代理 + 查询重写，fail-closed、subject+object 两侧、有一组 vitest 用例（外部复核 76/76 通过，未在仓库内复跑）；**未按仓库标准入库**（单作者/1★/无 harness 调用点/无泄漏率）。它只说明 read-path 是 family（post-filter vs query rewrite），不升第七时刻，也不改 01 的 B 评级。候选记在 [commit-gate frontier](../templates/subtopic-template/frontier.md)。
- **证据边界**：false-veto、grounding 校准、commit 写路径、第二 read-path 调用点仍缺；02 只写测量协议与 stop，不写「已解决」。
- 自检：`python3 meta/tools/check_repo.py` 通过（426 文件；E=20，Q=3，C=4，L=66；24 论文 / 4 开源）。

## 2026-11-09 04 落地生命周期

- **新增 04-worked-example**：README 索引 + `GUIDE.md` 本份导读 + `sections/`（map/boundaries/acceptance/relations）+ `body/`（build/consume/govern）+ `evidence/`；按 0–6 与前三份同构。
- **读者**：本体/数据工程师（建）、应用/agent 工程师（用）、治理/安全（治）；决策者仍走 01，工程负责人走 02，架构师走 03。
- **证据边界**：外部来源（Ontology Generation、Axiom Benchmark、CK25、GGC、SAGA、SchemaForge、Build2SPARQL、VAULT、Graph-Agentic RAG、Enterprise Agentic Systems、AWS 指南）只作“信号/候选”，**未入库、未升 E**；04 正文只引 E-xx + 这些信号，不把厂商/摘要数字写成结论。
- 自检：`python3 meta/tools/check_repo.py` 通过（426 文件；E=20，Q=3，C=4，L=66；24 论文 / 4 开源）。

## 2026-11-09 04 支撑执行（E-21/E-22）

> 取代上一节的“外部信号未升 E”状态。

- 论文线冻结：GGC（SG）、Glyph（US）、NLKGQ（DE）、KGVoyager（US）入库；2512/2507/2503/CK25/VAULT/SPARQL-LLM/CQ4OE/OntoExtend/QRAKEN/PPC 删除。
- 页面/E：`03/querying`、`01/access-control`；E-21/E-22；04 B.3/C.1 引 E，build 保持 signal。
- 工程线：OPA、Qlever 入档；Web：HN Netflix 材料卡（不升 E）。
- 自检：`check_repo` 通过（462 文件；E=22，L=73；28 论文/6 开源）。

## 2026-11-11 K0–K4 来源核查

- 新增 [K0–K4 来源说明](../../deliverables/01-capability-status/02-sections/92-k-ladder.md) 与 [核查笔记](../../deliverables/_plans/2026-11-11-k-ladder-provenance.md)。
- 结论：K0–K4 是 N&D 论文（arXiv:2610.11768）的五个累积实验条件，**不是行业标准，也不是成熟度模型**；OpenAlex 2026-11-11 快照为 preprint、0 引用；另一篇 2026 preprint 用 K0–K6 表示知识操作，记号已撞车。
- 定义修正：K0 = PLC 地址 + 原始整数（不再叫「地址级标签」）；K1 = tag 名/单位/质量码，别名/槽位是工程扩展；K2 = 塔投影文本（不含推导量），固定分节是工程建议。
- 01/02/03/04 的定义锚点与首用处改用「原始点位 / 点位语义 / 知识投影文本」；K 只作回查标签。

## 2026-11-11 证据重置收口（交付物第一轮）

- 指挥板：[meta/2026-11-11-command-board.md](../../deliverables/_plans/2026-11-11-command-board.md)；01 回执见 [handoff](../../deliverables/_plans/2026-11-11-adr-0011-handoff-to-01.md)。
- 01：E-02/E-03/E-04/E-13/E-16 撤回后，#4/#5/#6/#11 转 gap；计数 **A=3 / B=4 / C=2 / 非本体=1 / gap=4**；首屏/地图/canonical/决策记录/验收/边界/能力页已同步。
- 02：R4/R5/R6/R12 转 gap；计数 **A=3 / B=4 / C=1 / gap=4**（不含 R0）；受影响 recipe/索引/验收/追溯已标撤回。
- 03/04：受影响位置卡、证据台账、边界、附录已加“withdrawn/历史”标注；未逐句重写的旧数字不得作为结论。
- 自检：`check_repo` 通过（434 md；10 论文 / 8 开源 / 11 材料卡）。

## 2026-11-11 术语基线 v0 + 03 附录

- 新建 [term-baseline.md](./term-baseline.md)：10 词 v0；K 行 `local`；8 张标准卡补 `standing: normative`。
- 03 附录 evidence/checker/action 三节与证据表已改为“原锚撤回/历史”；02 R4/R5/R6 证据段删旧数字。
- `check_repo` 通过（435 md）。

## 2026-11-11 长尾清理（02/03）

- 02 R4/R5 的预算、成本、步骤与 domains 的 OA-RAG 数字改历史；03 checker/action 开头、附录 3.5/3.6 证据行改撤回。
- `check_repo` 通过（435 md）。

## 2026-11-11 桌面复评（证据重置后）

- 01=84 / 02=81 / 03=82 / 04=86（12 维，非冷读）；02/03 下降来自 gap 行扩大，不是文笔。
- 02 canonical/regulated 的最后旧数字已标历史；`check_repo` 通过（436 md）。

## 2026-11-12 交付物 IA 整改（README 索引 + 序号目录 + 语气）

- **计划**：[2026-11-12-deliverable-ia-plan](../../deliverables/_plans/2026-11-12-deliverable-ia-plan.md)。
- **01**（`95ca558`）：README 索引化；`02-sections/00-overview`、`02-map`、`04-boundaries`、`05-acceptance`、`09-decision-record`、`90-glossary`、`91-canonical`、`92-k-ladder`、`93-templates`；`03-capabilities`、`09-data`。
- **02**（`ad14c08`）：`02-sections`、`03-recipes`、`04-operations`、`05-appendices`；README 56 行。
- **03**（`5927a9b`）：`02-sections`、`03-positions`、`04-across-positions`、`05-evidence`、`09-appendix`；README 56 行。
- **04**（`136db9a`）：`02-sections`、`03-body`、`04-evidence`、`05-example`；README 60 行。
- **链接**：700+ 相对链接按「旧位置解析、新位置重算」重写；目录表加纯文本路径列；`check_repo` 0 坏链/坏锚（450 md）。
- **语气**：README 与 overview 去除故事化第二人称；案例改为第三人称事实框。
