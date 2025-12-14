# Changelog

## [Unreleased]

### Added
- 添加数据验证工具函数（validate_amount, validate_date, validate_time, validate_string）
- 添加常量定义（MAX_AMOUNT, BUDGET_WARNING_THRESHOLD, VALID_RECORD_TYPES 等）
- 添加 API 层错误处理装饰器 `api_error_handler`，统一异常捕获和错误返回格式
- 前端添加图表 RAF 管理（state.chartRAF）和 cancelPendingChartRAF() 函数

### Changed
- ID 生成方式从时间戳改为 UUID（generate_unique_id 函数），避免并发碰撞
- 账户余额计算改用 Decimal 类型，避免浮点数精度问题
- add_record/update_record 添加事务一致性保护（先保存记录，成功后再更新余额，失败时回滚）
- 前端图表渲染使用 requestAnimationFrame 优化，防止内存泄漏

### Fixed
- 修复记录/账户/预算等添加方法缺少输入验证的问题
- 修复账户余额更新可能产生精度漂移的问题

---

> **注意**：以下三个桌面应用已拆分为独立项目：
> - 狗狗百宝箱 → `/Users/xrj/PycharmProjects/doggy-toolbox`
> - 喵喵存金罐 → `/Users/xrj/PycharmProjects/meow-piggy-bank`
> - 牛牛待办 → `/Users/xrj/PycharmProjects/moo-todo`
