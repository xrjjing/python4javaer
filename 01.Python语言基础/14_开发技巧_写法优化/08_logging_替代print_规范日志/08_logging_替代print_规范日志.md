# 08_logging_替代print_规范日志

## 技巧说明

- 小脚本可以用 `print`，但服务与批处理项目推荐使用 `logging`；
- 可以按级别过滤、输出到文件、统一格式；
- 方便后续用日志分析脚本做统计。

---

## 示例 demo（见 `demo_logging.py`）

示例涵盖：

- 基本配置 `logging.basicConfig`；
- 使用 `logger.info / warning / error` 输出不同级别日志；
- 在异常时附带堆栈信息。

---

## 练习建议

1. 把「日志归档」「监控数据处理」项目中的关键 `print` 改写成 `logger.info / warning / error`；  
2. 学习如何将日志输出到文件（在 `basicConfig` 中配置 `filename`）；  
3. 思考应该在哪些地方使用 `info`，哪些地方用 `warning` 或 `error`。

