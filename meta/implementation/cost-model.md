# 成本工作簿（E4 公式，不编价）

> 用途：把试点/采购 memo 的成本-收益算成**可复算**的表。  
> 铁律：**任何单价没有出处就留空**；本文件出现自造费率即 fail。  
> 输入表在 `meta/implementation/cost-inputs.md`（Phase 4 建）或直接用本页字段；实现产物在仓库外。

## 0. 通用口径

- 期限：12 个月；折现率 `r` 由财务给；没有 `r` 就报未折现区间，不报单点。
- 年化：`TCO_12 = build + run_12 + maintain_12`；build 一次性，run/maintain 按月×12。
- 单位：人日、人周、分钟、token、query-equivalent；**不要把人日与 token 直接相加**。
- 三个试点分别用不同公式；不要把 CAI 的 `p_min` 套到护栏。

## 1. CAI 编译

### 公式

`c = D × T_doc / T0`

`C_total = c × (1 + m × r) + m × T_recluster / T0`（r=变更率/周期，m=周期数；T_recluster 是每次重聚类 token，乘 m 后除以 T0 折成 query-equivalent）

`p_min = 2.0% + C_total / (0.929 × Q)`（2.0% 是论文取整；精确的 0.019/0.929=2.045% 见 B 式）

`B(Q,c,p_h) = Q × (0.929 × p_h − 0.019) − c`（论文 Eq(8) 的净收益，query-equivalent；p_h 是门接受率）

### 输入

| 字段 | 含义 | 值 | 来源/owner | 状态 |
|---|---|---|---|---|
| `D` | 文档数 |  | 平台 | 待填 |
| `T_doc` | 每文档编译 token |  | 平台 | 待填 |
| `T0` | 未编译平均每问 token |  | 评测 | 待填 |
| `Q` | 年查询量 |  | 业务 | 待填 |
| `c` | query-equivalent | 公式 | — | 计算 |
| `p_h` | 门接受率（shadow） |  | 评测 | 待填 |
| `δ` | 非劣效 margin |  | 业务 | 待填 |
| `$/1M token` | 模型单价 |  | 采购 | 待填 |
| `人日/千文档` | 抽检/schema/重抽 |  | 平台 | 待填 |
| `人日价` | 内部费率 |  | 财务 | 待填 |
| `r` | 文档变更率/年 |  | 平台 | 待填 |
| `m` | 变更轮次/年 |  | 平台 | 待填 |
| `T_recluster` | 重聚类 token/次 |  | 平台 | 待填 |

### 判据

- `p_h` 的 95% CI 下界 > `p_min` → 可进 A/B；否则停/转 harness。
- 样本：p_h 判门 1,600–2,000 条 shadow（近阈值需 9,000）；100–200 只作 smoke。
- 非劣效：整臂准确率 CI 下界 > `−δ`；δ 预登记。
- **没有 `$/文档`、人日费率 → 只能报 token 账，不能报 TCO。**

### 敏感性

| 变量 | 低 | 基准 | 高 | 影响 |
|---|---|---|---|---|
| `T0`（`推测`情景） | 5k | 20k | 324,479（论文） | T0 越小，c/p_min 越大；企业短上下文可能 p_min 到几十 % |
| `miss penalty` | −1.5pp | 0 | +1.5pp | p_h* 在 0.4–3.6% 间移动 |
| `Q`（`推测`量级） | 200 | 1,000 | 10,000 | Q 越小，编译越难回本 |
| `T_doc`（`推测`量级） | 50 | 300 | 3,000 | 线性抬 c |

## 2. action-gate / CASEL 护栏

### 公式

统一反事实 = 不上护栏（do nothing）：HSR 32.76%、approvals 0%、task success 29.48%（CASEL 模拟）。

- 伤害节省/千次 = `(32.76% − HSR) × (1000/L) × incidents_per_harmful_trajectory × cost_per_incident`
- 审批成本/千次 = `approval_rate × 1000 × minutes_per_approval / 60 × hourly_rate`
- task success 收益/千次 = `(47.01% − 29.48%) × (1000/L) × value_per_success`（可选）
- `NPV_build = Σ_{t=1..12} [(伤害节省/千次 − 审批成本/千次 + task success 收益/千次) × N_12/1000] / (1+r)^t − TCO_12`（N_12=12 个月动作/轨迹量；per-千次先乘 N_12/1000；TCO_12 在 t=0 一次性减）
- `NPV_buy` 同口径：`RFQ + 集成人周 + 迁移/退出` 进 TCO；收益同 build；`NPV_do_nothing = 0`；取 argmax。
- 硬约束：task success 降 ≤2pp、false-veto ≤5%。

### 输入

| 字段 | 含义 | 值 | 来源/owner | 状态 |
|---|---|---|---|---|
| `L` | 每轨迹动作数 | 20（论文） | 平台 | 可改 |
| `HSR` | 护栏后有害轨迹率 |  | 试点 | 待填 |
| `incidents_per_harmful_trajectory` | 每有害轨迹事故数 |  | 风控 | 待填 |
| `cost_per_incident` | 单次事故成本 |  | 财务/风控 | 待填 |
| `approval_rate` | 审批比例 |  | 试点 | 待填 |
| `minutes_per_approval` | 单次审批分钟 |  | 业务 | 待填 |
| `hourly_rate` | 人时费率 |  | 财务 | 待填 |
| `value_per_success` | task success 货币化 |  | 业务 | 待填/可空 |
| `r` | 折现率 |  | 财务 | 待填 |
| `build` | 建设人周 + 集成（digest 2–4 人周是推测，不预填） |  | 平台 | 待填 |
| `compute_base` | 基线算力成本 |  | 平台 | 待填 |
| `N_12` | 12 个月动作/轨迹量 |  | 业务 | 待填 |
| `run_12` | 12 个月运行成本 |  | 平台 | 待填 |
| `maintain_12` | 重标/审计 12 个月 |  | 平台 | 待填 |

### 判据

- `NPV_build > max(NPV_buy, 0)` 且硬约束满足 → build；否则 buy/不做。
- 没有 `cost_per_incident`/`minutes_per_approval`/`hourly_rate` → 只给公式与敏感性，不给结论。
- **`0.486` 是论文匹配的公共 compute，不是部署单价**；CASEL 自身 factor 0.58 也不等于单价。

### 敏感性

| 变量 | 低 | 高 | 影响 |
|---|---|---|---|
| `cost_per_incident` | 1× | 10× | 线性放大伤害节省 |
| `minutes_per_approval`（`推测`） | 2 | 15 | 线性放大审批成本 |
| `HSR` | 5% | 20% | HSR 越低，伤害节省越大 |
| `false-veto` | 2% | 10% | 超过 5% 硬约束失败 |

## 3. feasibility（12 机制里 3 个可算）

| 机制 | 公式 | 可算？ | 缺什么 |
|---|---|---|---|
| CAI 编译 | `p_min` / `B(Q,c,p_h)` | 是（token 账） | `$/文档`、人日费率 |
| POLAR 门 | 伤害节省/千次 | 部分 | `cost_per_incident`、false-veto 标签 |
| CASEL 分配 | NPV | 部分 | 审批分钟、事故成本、γ_verify |
| 其余 9 个 | — | **不可算** | 缺分母/单价；只写“先测分母” |

规则：**不要把 3 个可算的结论外推到 12 个**；playbook 只对可算机制给 NPV。

## 4. 输出模板（memo 用）

```
机制：
反事实：
TCO_12：build ___ + run ___ + maintain ___ = ___
收益_12：___（公式/输入/CI）
NPV：___（r=___）
硬约束：task success ___；false-veto ___
结论：build / buy / 不做 / 先测分母
缺口：___（最多 3 项）
```

## 5. 禁止

- 用论文的 `c=10`、`0.486`、`0.58` 当自己的单价/成本。
- 把 token 账当 TCO；把人日与 token 相加。
- 用点估计过门槛；没有 CI 的收益进 memo。
- 把“3 个可算”外推到“12 个都可算”。
