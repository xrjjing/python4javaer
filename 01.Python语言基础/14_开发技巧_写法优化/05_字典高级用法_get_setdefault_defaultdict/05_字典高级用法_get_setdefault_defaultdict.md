# 05_字典高级用法_get_setdefault_defaultdict

## 技巧说明

- `dict.get(key, default)`：安全访问字典键；
- `dict.setdefault(key, default)`：不存在则初始化；
- `collections.defaultdict`：适合做分组统计。

---

## 示例 demo（见 `demo_dict_advanced.py`）

示例涵盖：

- 用 `get` 读取可选配置；
- 用 `setdefault` 按 key 分组合并列表；
- 用 `defaultdict(list)` 简化聚合代码。

---

## 练习建议

1. 在日志统计项目中，使用 `defaultdict(int)` 统计日志级别数量；  
2. 在监控项目中，使用 `defaultdict(list)` 聚合同一指标的所有值；  
3. 在配置加载代码中使用 `get` 提供默认值，而不是手写 `if key in config`。

