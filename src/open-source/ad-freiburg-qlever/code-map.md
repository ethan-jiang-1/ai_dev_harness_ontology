# QLever · 代码地图

> 只做定位；判断回 [digest](./digest.md)，来源回 [card](./card.md)。pin `0998359`。

| 文件/目录 | 符号/作用 | 看什么 |
|---|---|---|
| `src/ServerMain.cpp` | 主入口 | 起 HTTP server |
| `src/engine/Server.cpp` | `Server` | endpoint、请求处理、结果导出 |
| `src/parser/SparqlParser.cpp` | `SparqlParser` | SPARQL 1.1 解析 |
| `src/engine/QueryPlanner.cpp` | `QueryPlanner` | join 顺序/算子选择 |
| `src/engine/QueryExecutionTree.cpp` | `QueryExecutionTree` | 算子树求值 |
| `src/index/Index.cpp` | `Index` | RDF 索引/permutation/统计 |
| `src/engine/ExportQueryExecutionTrees.cpp` | 导出 | JSON/CSV/TSV 结果 |
| `src/libqlever/` | 嵌入式库 | 进程内使用 |
| `test/` | 测试 | CI/回归证据 |
