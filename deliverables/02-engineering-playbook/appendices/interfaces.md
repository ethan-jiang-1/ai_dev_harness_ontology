---
status: draft
updated: 2026-11-09
parent: ../README.md
basis: R0–R12 的 mechanism/数据契约；E-20
---

# 附录 A · 接口总表

> 一页查「这个接缝要什么字段」。字段名多数是各 mechanism 的工程配方（`推测`）；数字/条件回 E-xx。
>
> **三条通用规则**：
> 1. 三态显式：`pass` / `flag` / `unknown`；`unknown` 不是 pass。
> 2. 版本绑定：每个产物带 `id/version/hash/generated_at`；决策绑定 `snapshot_id`。
> 3. 可追溯：每条结论/决策能回指 `claim_id`/`node_id`/`policy_version`。

## 1. 通用 artifact

```text
artifact: {kind, id, version, hash, generated_at, supersedes, valid_from}
decision: {decision_id, snapshot_id, ontology_version, policy_version,
           evidence_version, model_version, prompt_version}
```

## 2. 供给

### 2.1 tag registry / slot map（R1）

```text
tag:  {label, unit, quality_flag, aliases[], source}
slot: {entity_type, slot, unit}
```

### 2.2 projection（R2）

```text
header: {system_id, tower_version, projection_version, generated_at,
         covered_sections, projection_chars, rubric_version}
body:   固定分节 + 每条 [node_id]
map:    statement_id → node_id（同版本）
```

### 2.3 claim index（R3）

```text
{claim_id, text, span_start, span_end, chunk_id,
 source_version, extractor_version, acl}
```

### 2.4 tool policy（R3）

```text
{tool: off | compiled-only | compiled-first}
```

### 2.5 OBDA（R11）

```text
ontology.ttl, mapping.ttl (R2RML), query.rq, db.properties
CLI: ontop query -m ... -t ... -q ... -p ...
```

## 3. 输出

### 3.1 evidence contract（R4）

```text
{answer, observations[], grounding: entailed|supported|related|unrelated}
```

- `observations`：concept card / ASK / SELECT bindings。
- `E=∅` 时不报 grounding。
- 卡字段：`iri, label, definition, parents[], children[], relations[], comments[], source`。

### 3.2 checker verdict（R5）

```text
{verdict: pass|flag|unknown,
 constraint_id, query_fragment, message, evidence}
```

- `unknown` 不阻断。
- 报告 checked/passed/undetermined 三个数。

## 4. 约束

### 4.1 action gate（R6）

```text
Layer A: tool {name, args, mutating, slots[]}
         inverse_edge {tool, tier T1–T5, weight, loss_class, bound?, curator, status}
Layer B: slot(entity_type, id) = value; state_hash
output:  {decision: APPROVE|VETO|ESCALATE, phi, pi, bottleneck}
log:     {tool, entity, tier, phi, tau, decision, reason,
          trajectory_id, approval, rollback}
```

### 4.2 read-path policy（R8）

```text
policy_graph: urn:graph:policy
shape: NodeShape + sh:SPARQLTarget + sh:SPARQLRule + tg-pol:blocks
request: {query, user_context}
```

### 4.3 commit gate（R9）

```text
mutation_context {mutation_id, class, head_id, target_id, policy_version, snapshot_id}
q_m[] {claim_id, predicate, scope, version}
evidence {obs_id, claim_id, role, provenance, hypothesis_id, source_id}
promotion {claim_id, obs_id, role, validation_basis, policy_version, promoted_by, promoted_at}
verdict {status, failed_claims[], unresolved[], scope_valid, versions_valid}
```

## 5. 状态

### 5.1 registry / edge（R7）

```text
registry {canonical_id, type, normalized_name, aliases[],
          first_seen, last_seen, source_version}
edge {head_id, target_id, relation, source_indicator, observations[],
      state, score, first_seen, last_seen}
match_log {surface, layer_hit, score, anchor, alias_written, period}
```

### 5.2 relational / reasoning state（R7）

```text
relational {fact_id, validity, scope, supersedes[], conflicts[], concept_id}
reasoning {request_id, used_facts[], roles[], priority[]}  # 不回写事实
```

## 6. 离线/CI

### 6.1 SHACL report（R10）

```text
{conforms: true|false|null,
 violations: [{focus_node, path, constraint, severity, message, source}],
 checked, passed, undetermined}
```

### 6.2 change impact（R10）

```text
{entailments_lost, lost_by_warrant, monotonicity_violations, skipped, exit_code}
```

## 7. 受监管（R12）

```text
citation {doc_id, version, page, span, clause_id, retrieved_at}
study input {study_type, network_model, state_hash, solver_config}
study output {result, solver_version, provenance, warnings}
strict_pass {task_id, tool_calls[], network_state_hash, study_type, pass|fail, reason}
memory {kind, content, source, approved_by, version}
decision_point {decision_id, findings, citations, signer, timestamp}
```

## 8. 最容易错的四个接口

1. **`conforms:null` vs `false`。** 前者是「没检查完」，不能当 pass；shell exit code 可能把两者折叠。
2. **`p_h` vs `φ`。** `p_h` 是证据门放行率，不是答对率；φ 要另抽 accepted query。
3. **`approval` 没有 minutes。** 只记「批准了」算不出审批成本。
4. **commit verdict 只有 status。** 没有 `failed_claims[]`/`unresolved[]`，defer 无法重入。

**出处**：[execution-forms](../../../topics/execution-forms.md) · 各 R 的 mechanism 页 · E-20
