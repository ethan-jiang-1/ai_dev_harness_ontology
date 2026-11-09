# OPA · 代码地图

> 只做定位；判断回 [digest](./digest.md)，来源回 [card](./card.md)。pin `3dc83ae`。

| 文件/目录 | 符号/作用 | 看什么 |
|---|---|---|
| `cmd/run.go` | `run` 命令 | 服务启动、配置、插件加载 |
| `server/server.go` | `Server` | REST decision API；`/v1/data/...` |
| `rego/rego.go` | `Rego` | 查询入口；policy + input + data |
| `topdown/topdown.go` | 求值 | Rego 规则求值、builtins |
| `plugins/bundle/` | bundle 插件 | 策略分发/激活/版本 |
| `plugins/logs/` | decision logs | 审计字段：input/decision/path |
| `ast/` + `compile/` | AST/编译器 | Rego 解析/类型检查/编译 |
| `ADOPTERS.md` | 生产采用列表 | 影响力证据，不是质量证明 |
