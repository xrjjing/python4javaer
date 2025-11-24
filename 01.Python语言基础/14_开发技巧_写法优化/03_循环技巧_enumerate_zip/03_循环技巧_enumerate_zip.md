# 03_循环技巧_enumerate_zip

## 技巧说明

- `enumerate(iterable)`：在遍历时同时取得索引和值；
- `zip(a, b, ...)`：并行遍历多个序列；
- 让循环逻辑更清晰，减少手工管理下标。

---

## 示例 demo（见 `demo_loops.py`）

示例涵盖：

- 用 `enumerate` 打印行号与内容；
- 用 `zip` 同时遍历名字和分数；
- 用 `enumerate(zip(...))` 组合多种信息。

---

## 练习建议

1. 将你的「九九乘法表」或其他循环练习改写成使用 `enumerate`；  
2. 在成绩统计类代码中，用 `zip(names, scores)` 替代手写下标；  
3. 在日志分析/监控项目里，如果需要输出「编号 + 内容」，优先使用 `enumerate`。

