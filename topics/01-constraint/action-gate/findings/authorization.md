# 可逆性不等于安全/授权

## F4

- **判断**：可逆性分数是「注释可恢复性」，不是「动作安全」或「用户授权」；外部副作用可能完全合法，零售退货/换货可能被误拦。
- **等级**：`推测`（机制解释；原 POLAR 已移出，其 retail 回退观察作历史线索）。
- **条件**：T5 `external_side_effect` 只看可逆性；retail 的退货/换货是合法用户请求。
- **反例/边界**：不是所有 retail 动作都合法；需要意图/授权层区分；原 POLAR（已移出）block log 没有 harm/authorization 标签。
- **来源**：[POLAR digest](../../../../meta/audits/2026-11-11-source-purge.md#src-2610-08082) · [action-gate README](../README.md)

**工程含义**：门可以问「能不能撤销」，但不能只问这个；合法意图的动作需要第二把尺（意图/授权/业务规则），否则 false-veto 可能把合法请求拦掉。
