# 访问控制 · 未发现与下一步

> `G` = gap（还没站住的判断）；`N` = next（下一步看什么）。稳定判断回 [findings](./findings.md)。
> 错误路径/对象方向的代码细节在 [commit-gate F5–F7](../commit-gate/findings.md)；本页只留访问控制自己的缺口。

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | 策略冲突/优先级 | 多策略命中同一节点/资源时谁赢、默认 allow 还是 deny，决定「策略存在」是否等于「策略可控」；`sh:order` 首命中只是执行顺序，不是冲突消解 | 策略语言/冲突消解规范 + 重叠策略、缺省策略、冲突策略的行为测试 | XACML/OPA/Cedar 的 combining algorithms；trustgraph 策略样例；访问控制策略冲突文献 | 高 |
| G2 | 审计/策略版本 | 判定要能回答「谁、何时、依据哪版策略/标签、为什么 allow/deny」；没有它就无法复核、回滚或举证 | decision record schema（subject/resource/action/decision/policy_version/label_version）+ 策略版本化/回滚 + 回放测试 | OPA decision logs；trustgraph policy events；数据治理审计标准 | 高 |
| G3 | 第二实现 / 对象方向 | `read-path` 目前只有 1 个实现（[E-20](../../conclusions.md)），不能判断「返回前过滤」是普遍形态还是单项目选择；对象方向是否受控另见 [commit-gate F7](../commit-gate/findings.md)，执行者/写路径问题见 [commit-gate G1/G4](../commit-gate/frontier.md) | 第二个独立实现，用同一策略/同一查询对照返回结果；覆盖 subject 与 object 两侧 | commit-gate 候选队列的 sparql-guard；其他 SPARQL 代理/策略网关 | 高 |
| G4 | 标签体系跨企业 / 未标注率 / OOD | Glyph 单企业、内部 275-leaf 本体、无 OOD、未报漏标/未标注率；标签覆盖不到的地方，访问控制会默认放行或默认拒绝，两者都未测 | 275 leaves → 目标企业词表的映射及映射准确率；表级不相交/OOD 上的 F2；独立抽样的漏标率；未标注列的默认处置 | SOTAB/GitTables（作者点名未做）；Glyph 后续引用；企业目录合作 | 高 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变哪条 F/G | 成本 |
|---|---|---|---|---|
| N1 | 第二 read-path 实现的行为对照 | 先复核 commit-gate 候选 `Matdata-eu/sparql-guard`（未入库）；检索 `SPARQL policy filter read path`、`query rewriting access control` | F2 / G3 | 中 |
| N2 | 漏标率 / 未标注率 / OOD | Glyph 作者后续；SOTAB/GitTables 探针；`column sensitivity classification out-of-distribution`、`ontology mapping enterprise taxonomy` | F1 / G4 | 高 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-09 | Glyph + trustgraph 定稿 | 标签层有生产级来源；策略层无来源；执行层单实现 | 3 F / 4 G / 2 N；先补 G1/G2/G4 |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| Glyph（2609.10430） | 标签层唯一生产级来源；不产策略判定、不执行访问控制 | 已入档（[F1](./findings.md)） | 补漏标率/OOD（N2） |
| trustgraph（开源） | 读路径 SHACL-AF 过滤；单实现 | 已入档（[F2](./findings.md)） | 错误路径/对象方向见 commit-gate F5–F7 |
| 第二 read-path 实现 | 判断「返回前过滤」是否普遍；对象方向是否被覆盖 | 待扫描 | N1 |
| OPA（open-policy-agent/opa） | 通用策略引擎；补策略层决策点；不解析本体/不消费标签 | 已入档（adjunct） | 接 label→policy、冲突/审计测试 |
| 标签→策略属性接口 | Glyph 与 trustgraph 之间缺的那段 | 待扫描 | G1/G4 |
