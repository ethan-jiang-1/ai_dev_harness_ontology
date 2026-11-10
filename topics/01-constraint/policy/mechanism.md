# 策略层 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，缺口回 [frontier](./frontier.md)。
> 标准/实现未入库；条款/API 在入库前标 `待核`。

## 链路

```
source/column
  → tag / level            (access-control；Glyph)
  → policy                 (principal, action, resource_kind, condition, effect, obligation, version)
  → decision               (allow / deny / skip)
  → audit                  (decision_id, who, judged_subject, policy_version, reason, outcome)
  → execution              (read-path post-filter；commit gate 未实现)
```

**策略层只到 decision**；执行在 [read-path](../commit-gate/read-path.md)，写授权在 [commit-gate](../commit-gate/README.md)。

## 7 列 schema

| 列 | 取值 | 来源 | 不能推出什么 |
|---|---|---|---|
| `principal` | 用户/角色/服务 | 04 契约（UI/agent→steward，governance→analyst） | 身份认证 |
| `action` | read / write / export | 04 契约 | 动作可逆性 |
| `resource_kind` | column / table / dataset | 04 fixture | 资源级联 |
| `condition` | `resource_level` / `user_context.clearance` / 时间/用途 | 工程选择；标准只给等级 | `clearance` 在 input 里，但 7 条规则均未消费 |
| `effect` | allow / deny / skip | 工程选择 | `skip` 是第 4 值，XACML/ODRL 都没有；skip ≠ allow |
| `obligation` | log / mask / approve | XACML obligation / ODRL duty | 04 policy.json **无此字段**；执行器不一定履行 |
| `version` | policy_version | 工程选择 | 版本一定可回放 |

## 冲突消解对照

| 语义 | XACML 3.0 | ODRL 2.2 | Rego/OPA | OpenFGA |
|---|---|---|---|---|
| 冲突 | deny-overrides / permit-overrides / first-applicable / deny-unless-permit / permit-unless-deny | `odrl:conflict`：perm / prohibit / invalid | 作者写规则序；默认 deny（约定） | 无冲突概念（关系闭包） |
| 默认 | 由 policy set 决定 | 未指定 | deny | deny |
| 义务 | obligation | duty | 无内置 | 无 |
| 版本 | policy version | profile | bundle | model id |
| 适用 | 通用 | 内容/数据 | 通用 | ReBAC |

> 这张表是 `待核`：入库后按条款/文档核对，不把摘要当条款。ODRL 的默认冲突策略（§2.10）本轮未取到正文；XACML obligation 能否挂 Deny（`FulfillOn`）也待核。

## 10 条测试（对齐 04 policy.json）

| # | principal | action | resource_level | clearance | 期望 | 依据 |
|---|---|---|---:|---:|---|---|
| 1 | analyst | read | 2 | 2 | allow | level ≤2 |
| 2 | analyst | read | 3 | 2 | deny | level ≥3 |
| 3 | analyst | read | null | 2 | deny | 缺 level = deny |
| 4 | steward | read | 4 | 2 | allow | steward 例外 |
| 5 | service | write | 2 | — | deny | 写路径不授权 |
| 6 | any | read | table/dataset | — | skip | 表/数据集不按列判 |
| 7 | any | any | 无命中 | — | deny | 默认 deny |
| 8 | analyst | read | dataset 3 | 2 | skip | kind 先于 level |
| 9 | steward | read | table null | 3 | **未定** | R4 vs R6 优先级未写全 |
| 10 | analyst | delete | 1 | 2 | deny | 未覆盖 action → 默认 deny |

**规则**：先 `kind` 后 `level`（6 先于 1–3）；列内 deny-overrides；`skip` 必须带 `reason`，不能当 allow。

## 标签 → level → 处置（骨架）

| 标签/类别 | level | 处置（工程选择） | 来源 |
|---|---:|---|---|
| 一般数据 | 1–2 | 默认可读；按角色 | 工程映射（43697 只分三级） |
| 重要数据 | 3 | 仅 steward/授权角色；审计 | 工程映射 |
| 核心数据 | 4 | deny by default；审批 + 审计 | 工程映射 |
| 个人信息（Email/Phone） | 2–3 | 按用途/同意；最小化 | GB/T 35273 类别（待核） |
| 敏感个人信息（SSN/金融） | 3–4 | deny by default；去标识 | GB/T 35273 类别（待核） |

> `level` 与处置的对应是**工程选择**，不是标准原文：GB/T 43697 只分**核心/重要/一般**三级，GB/T 35273 只定义个人信息/敏感个人信息，**都不给 1–4 数值，也不给「analyst 能不能读」**。`clearance` 在 10 条用例里取 1–5，没有一条改变 decision。

## 审计最小单元

```json
{
  "decision_id": "dec-0001",
  "who": "analyst:alice",
  "action": "read",
  "resource_kind": "column",
  "judged_subject": ":col_ssn",
  "resource_level": 4,
  "user_context": {"role": "analyst", "clearance": 2},
  "policy_version": "0.3.0",
  "effect": "deny",
  "reason": "policy_deny",
  "obligation": "log_decision",
  "outcome": "row withheld"
}
```

**要求**：`decision_id` 唯一；`policy_version` 与 `tag_version` 可回放；`skip` 带 `reason`；`outcome` 写实际结果，不只写 decision。

## stop

- 没有 principal/action 来源 → 不写策略表，只写「标签 ≠ 策略」。
- 没有冲突消解选择 → 不写 deny-overrides；写「未定」。
- 7 条测试跑不出期望 decision → 不写「策略可判定」。
- 没有版本/审计字段 → 不写「可审计」。
