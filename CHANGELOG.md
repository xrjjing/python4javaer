# Changelog

## [Unreleased]

### Added
- 添加数据验证工具函数（validate_amount, validate_date, validate_time, validate_string）
- 添加常量定义（MAX_AMOUNT, BUDGET_WARNING_THRESHOLD, VALID_RECORD_TYPES 等）
- 添加 API 层错误处理装饰器 `api_error_handler`，统一异常捕获和错误返回格式
- 前端添加图表 RAF 管理（state.chartRAF）和 cancelPendingChartRAF() 函数

### Changed
- 狗狗工具箱重命名为"狗狗百宝箱"：统一 main.py 窗口标题、数据目录(.dog_toolbox)、index.html 标题/Logo、build.py 打包名；副标题改为 Dog Toolbox
- 将记账应用(bookkeeping_app)从 desktop_tools 移至根目录，成为独立项目
- 更新 GitHub Actions workflow 支持同时打包"本地工具箱"和"喵喵记账"两个桌面应用
- 更新 README.md 添加 desktop_tools 和 bookkeeping_app 目录说明
- ID 生成方式从时间戳改为 UUID（generate_unique_id 函数），避免并发碰撞
- 账户余额计算改用 Decimal 类型，避免浮点数精度问题
- add_record/update_record 添加事务一致性保护（先保存记录，成功后再更新余额，失败时回滚）
- 前端图表渲染使用 requestAnimationFrame 优化，防止内存泄漏

### Fixed
- 修复 bookkeeping_app 的 import 路径，使其作为独立项目运行
- 修复 build.py 中的 services 目录路径引用
- 修复 desktop_tools/services/__init__.py 移除已删除的 bookkeeping 导入
- 添加 GitHub Actions release job 所需的 contents:write 权限
- 修复 bookkeeping_app/build.py 的跨平台分隔符问题（Windows 用 `;`，其他平台用 `:`）
- 修复记录/账户/预算等添加方法缺少输入验证的问题
- 修复账户余额更新可能产生精度漂移的问题
