# 输出后判定 · 发现（F）

> 只放已经能站住的判断。`F` 编号是子主题局部编号；跨页引用写 `checker/Fx`。

## 索引
> **2026-11-12 对账（等级以 README 为准）**：本页索引里的「已核」是**撤源前**的记录；支撑它的来源已按 [CHARTER §4](../../../CHARTER.md#4-素材准入material-gate) 移出，这些条目现等级见 [README](./README.md)（多已降 `推测`/`withdrawn`）。**引用请用 README 的等级，不要用本页索引的历史等级。**


| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 三种本体来源在漏检/误报上无单一向优 | 已核 |
| F2 | curated 真实答案 precision 仅略优于随机；FA 主源是 declaration/domain-range，不是「与数据矛盾」 | 已核 |
| F3 | 空结果重试是强基线；ontology check 必须先超过它 | 已核 |
| F4 | curated + data-derived 组合无净收益 | 已核 |
| F5 | specific feedback 修复更多，但 corrupt 也更多 | 已核 |
| F6 | LLM judge 检错更多，但修坏多于修好；不能默认更好 | 已核（单图比较器） |
| F7 | checker 的答案应分三态：通过 / 违反 / 未检查完；把「没检查完」合并进 pass 会污染 catch/FA | 已核（代码；未跑） |
| F8 | SHACL 求值器的「覆盖」与「保证」不可兼得：默认支持 `sh:sparql` 但会 skip；verified 覆盖 Core 但拒绝 `sh:sparql`（22/120） | 已核（代码；未跑） |
| F9 | 用 D1 的 +5pp/FA≤15% 阈值：data-derived 在 UniProt 真实答案上过线；curated 高 catch 但 FA 超线；masked LLM 增量不足 | 分析 |

## F1 · 三源权衡

- **判断**：curated 抓得多、FA 高；data-derived FA 低、catch 低；LLM 生成不稳定。
- **数字（真实答案，UniProt，3,383 可检查；catch/FA）**：curated 18.9/16.8；data-derived 8.2/3.5；LLM masked 5.0/1.8；空结果重试 2.5/0.1。
- **precision 单列（人工故障 + 25% 错答案假设，不是真实答案口径）**：curated 57.1、data-derived 72.3、LLM masked 93.7、空结果 100。
- **条件**：5 图、7 模型、210 题 ×3 attempts；UniProt confirmatory。
- **边界**：其他图 exploratory；private 只报率。
- **工程含义**：data-derived summary 规模按 1–2 万实体估，超过就分域重建；重建频率与部署抽样是工程配方，不是论文测量（`推测`；见 [mechanism](./mechanism.md) 建库参数）。
- **来源**：Table 2, p.7；§5 RQ1。

## F2 · curated 不是权威

- **判断**：curated 在真实答案上的 precision 只略高于同率随机 flag（+1.6 点，CI −2.3~+6.3，跨零）；57.1% 是人工故障 + 25% 错答案假设下的 precision，不是真实答案口径。
- **FA 归因**：curated 的 FA 主源是 domain/range 与 declaration check（C3：curated 与 masked LLM 的人工故障 FA 差异，由这两类承担；盲审 32 个 FA 的双标注一致项中，undeclared term 17、closed-world 11，data clash 0；Table 6 / Appendix D.1）。「curated schema 与自身数据矛盾」是 Table 5 的独立观察，不是 FA 主因；审计仍必要，但不能拿它解释 FA。
- **对照**：data-derived 真实答案 precision 29.9%，比同率随机 flag 高 +14.4 点；但它 catch 只有 8.2%。
- **数字**：14.3% Linked Data triples 使用未声明属性（外部 crawl 统计，非本文测量）；每个缺失声明会经 declaration check 误报用到它的正确答案。
- **工程含义**：上线前先自动补声明（domain/range），补不了的进人工队列；审计 Table 5 的矛盾，但不要把它当 FA 主因。curated 审计工期未测——`1–2 人日` 是 data-derived setup 的估算，不能挪到 curated（`推测`；见 [mechanism](./mechanism.md)「curated 审计」）。
- **条件**：precision 数字：UniProt curated；真实答案 + 人工故障（precision 口径）。FA 归因：32 条盲审样本（四个公开图）+ C3 消融（curated vs masked LLM）。
- **边界**：不是所有 curated 本体都矛盾；需审计。盲审样本小，FA 归因不是全量分解。
- **来源**：Table 2/3/5/6, p.7–8；Appendix D.1/D.2；digest §5 第1条、§6.1 第2条。

## F3 · 空结果基线

- **判断**：查询返回空就重试，不需要本体；人工 fault 上 catch 79.2%、FA 0%；真实答案 catch 2.5%、FA 0.1%。
- **含义**：ontology check 只有抓到「空结果重试抓不到」的错，才有增量价值。
- **来源**：Table 2, p.7；§5 RQ1。

## F4 · 组合无净收益

- **判断**：curated + data-derived 组合 catch 19.5%、FA 17.8%；比 curated 单用只多 0.6 点 catch，却多 1.0 点 FA；C4 无净收益。
- **条件**：UniProt；同一 compiler；组合策略。
- **来源**：Table 2/3；§5 RQ3。

## F5 · feedback 的双刃

- **判断**：specific feedback 修复 28.3% flagged wrong，但 corrupt 1.0% flagged correct；generic 是 20.2% / 0.2%；C5 最终准确率差异未确立。
- **含义**：specific 的净修复更高（28.3% vs 20.2%），但 corrupt 也更多（1.0% vs 0.2%）；C5 最终准确率差异未确立（0.2，CI −3.2~3.1），不能默认 generic 更安全。未验证前先 generic 是风险默认，不是安全结论（`推测`）。
- **来源**：Table 2/3, p.7；§5 RQ3。

## F6 · LLM judge：检错更多，但修坏多于修好

- **判断**：UniProt 真实答案上 LLM judge catch 40.3%、FA 16.2%、precision 31.3%；catch 高于 curated（18.9）与 data-derived（8.2），FA 与 curated（16.8）接近、高于 data-derived（3.5）。人工故障上，curated/data-derived/masked LLM 对 changes of meaning 的 catch 是 0%（Table 4）；judge 能抓这类语义错（它判定的 41 个 changes of meaning 全抓到；Appendix C.2）。
- **代价**：把 flag 当行动信号后，40 条修好 / 83 条修坏（Table 11）。人工故障（有题面文本的 2,238 条）上 catch 98.7/98.0（Sonnet/Haiku），但会把 30–38% 答案仍正确的故障查询 flag。
- **含义**：检错多不等于净收益；judge 每条答案要一次模型调用，成本/稳定性未测。不能默认 judge 更好；也不能只凭 corrupt>fixed 判它无用——需在目标错误分布上测净修复（fixed − corrupted）；这是部署判断（`推测`）。
- **条件**：UniProt 主表；Appendix C.2 比较器；真实答案由 agent 自己的模型扮演，人工故障由 Claude Sonnet 5.5 / Haiku 5.5 扮演。
- **边界**：单图为主；成本/稳定性未做头对头。
- **来源**：Appendix C.2, Table 11；§6 Discussion；digest §6.5 部署度量。

## F7 · 三态：通过 / 违反 / 未检查完

- **判断**：checker 不能只有「通过/违反」两态。开源实现（open-ontologies）把「没检查完」做成独立状态：默认 SHACL 路径会 skip 不支持的约束（`skipped_constraints`），verified 路径用 exit code 3 = `undetermined`，并且明确不以 `conforms: true` 冒充「全查过」。把这两态合并，catch/FA 的分母就被污染——「没查」会被算成「查过且通过」。
- **等级**：已核（代码；本次未跑起来）。
- **条件**：适用于任何「部分覆盖」的 checker：shapes 不完整、约束被 skip、样本抽样、离线标注集缺答案。
- **含义**：checker 的度量要同时报三个数：checked / passed / undetermined（或 skipped）；否则 catch 与 FA 都不可比。这直接约束 G1/G5 的评测口径。
- **接口边界（2026-11-09 代码核对）**：exit 3 是 `oo-shacl` 子进程的；外层 `gate_exit_code` 把 `conforms:null` 映射为 exit 2，与解析失败同码。三态在 JSON 里保留（`conforms:null` + `undetermined`），在 shell 退出码里被折叠。引用「exit 3」时必须说明是哪一层。
- **来源**：[open-ontologies digest](../../../src/open-source/fabio-rovai-open-ontologies/digest.md) §3–§5；`src/shacl_verified.rs`、`src/shacl.rs`、`src/main.rs` 的 `gate_exit_code`。

## F8 · 覆盖与保证不可兼得

- **判断**：open-ontologies 的两条 SHACL 求值路径不是 superset：默认路径把约束编译成 SPARQL，支持 `sh:sparql` 与自定义组件，但会 skip 一部分约束；verified 路径（`oo-shacl`）覆盖 SHACL Core、声明的 soundness 有机器检查定理，但**明确拒绝** `sh:sparql` 与用户自定义组件（W3C 120 条里 22 条）。CLI 也拒绝把 `--verified` 与 temporal scope 合用，否则 scope 会被静默丢弃。
- **等级**：已核（代码；本次未跑）。
- **含义**：checker 选型不是「越强越好」，而是「用覆盖换保证」或反之；引用时必须说明用的是哪条路径、它拒了什么。这与 F7 的三态是同一件事的两面：保证越强，undetermined/拒绝的边界越显式。
- **来源**：[open-ontologies digest](../../../src/open-source/fabio-rovai-open-ontologies/digest.md) §3–§5；`src/shacl_verified.rs`、`src/main.rs` 的 `Shacl` 分发。

## F9 · 用 D1 的「+5pp / FA≤15%」阈值套 E-02

- **判断**：在 UniProt 真实答案上，相对空结果重试（catch 2.5% / FA 0.1%），data-derived 的增量 catch 为 **+5.7pp**、FA **3.5%**，过 D1 的工程阈值；curated 增量 **+16.4pp** 但 FA **16.8%** 超线；masked LLM 增量 **+2.5pp**，不足。
- **等级**：分析（E-02 + D1 工程阈值；不是论文结论）。
- **边界**：单图（UniProt）；语义错 0%（changes of meaning 结构检查抓不到）；部署故障分布未知；阈值是工程选择，不是论文的显著性判断。
- **含义**：E4 的 verdict 应写成「data-derived 在 UniProt 真实答案上过线；curated 高 catch 但 FA 超线；masked LLM 增量不足」；不能写成「checker 有效」或「curated 更好」。
- **来源**：E-02；[e4 数据表](../../../deliverables/01-capability-status/09-data/e4-checker.md)。
