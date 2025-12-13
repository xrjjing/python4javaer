# Changelog

## [Unreleased]

### Added
- 喵喵存金罐：新增账户余额调整功能
  - 手动调整账户余额（对账校正）
  - 实时显示当前余额与调整差额
  - 支持添加备注
- 喵喵存金罐：新增账户转账功能
  - 账户间转账，自动更新双方余额
  - 使用 Decimal 精确计算避免浮点精度问题
  - 转账弹窗显示账户余额，方便选择
  - 支持添加备注
- 喵喵存金罐：新增数据备份与恢复功能
  - 一键导出所有数据为 JSON 文件（分类、标签、账户、预算、账本、记录、主题）
  - 导入 JSON 备份文件恢复数据（覆盖现有数据）
  - 数据统计卡片显示当前数据量
  - 导入前确认提示，防止误操作
- 狗狗百宝箱：新增数据备份与恢复功能
  - 一键导出所有数据为 JSON 文件（页签、命令、凭证、节点、主题）
  - 导入 JSON 备份文件恢复数据（覆盖现有数据）
  - 数据统计卡片显示当前数据量
  - 导入前确认提示，防止误操作
- 狗狗百宝箱：新增 IP/Cron/SQL 工具（M15）
  - IP 工具：IPv4/IPv6 验证、十进制/十六进制/二进制转换
  - IP 工具：CIDR 子网计算（网络地址、广播地址、子网掩码、可用主机数）
  - IP 工具：IP 类别识别（A/B/C/D/E）与私有地址检测
  - Cron 解析：解析 5/6 字段 Cron 表达式，生成人类可读描述
  - Cron 解析：常用预设（每5分钟、每小时、每天、每周一、每月）
  - Cron 解析：显示未来 5 次运行时间
  - SQL 格式化：关键字大写、主要子句换行缩进
  - SQL 格式化：压缩模式、自动提取涉及表名
- 狗狗百宝箱：新增颜色转换器（M14）
  - 支持多种颜色格式输入：HEX（#RGB、#RRGGBB、#RRGGBBAA）、RGB/RGBA、HSL/HSLA
  - 输出 8 种格式：HEX、HEXA、RGB、RGBA、HSL、HSLA、HSV、CMYK
  - 实时颜色预览（支持透明度棋盘格背景）
  - 自动检测输入格式并判断深浅色
  - 相关色方案：互补色、三等分色、类似色
  - 点击色板可快速复制 HEX 值
- 狗狗百宝箱：新增 cURL 解析工具（M13）
  - 解析 cURL 命令提取 URL、方法、请求头、请求体、Cookie 等信息
  - 支持多种 cURL 选项：-X, -H, -d, --data-raw, --json, -b, -u, -k, -A, -e, -F 等
  - 智能处理 shell 引号（单引号、双引号、$'...' ANSI-C 引用）
  - 生成 6 种语言代码：JavaScript Fetch、Axios、Python requests、Node.js http、PHP cURL、Go
  - JSON 请求体自动格式化显示
- 狗狗百宝箱：新增密码生成器工具（M9）
  - 支持自定义密码长度（8-128位）和批量生成（1-100条）
  - 可选字符集：大写字母、小写字母、数字、特殊符号
  - 排除易混淆字符选项（0OoIl1）
  - 使用 crypto.getRandomValues 安全随机生成
  - 实时显示密码强度评分（弱/中等/强/非常强）
- 狗狗百宝箱：新增 JSON 格式化工具（M10）
  - 支持 JSON 格式化/美化（2空格、4空格、Tab缩进）
  - 支持 JSON 压缩（minify）
  - 实时校验 JSON 有效性并显示错误行号
  - 尝试修复常见 JSON 错误（尾部逗号、单引号）
- 狗狗百宝箱：新增文本处理工具（M11）
  - 去重：支持区分大小写和忽略首尾空白选项
  - 排序：字母升/降序、长度升/降序、随机打乱、反转
  - 行处理：删除空行、去首尾空白、添加/移除行号
  - 实时显示行数和去重后行数统计
- 狗狗百宝箱：新增正则表达式测试工具（M12）
  - 实时匹配高亮，显示匹配位置和分组
  - 支持替换功能（支持 $1, $2... 分组引用）
  - 内置常用正则预设（邮箱、手机号、URL、IP、日期等）
  - 支持 g/i/m/s 标志切换
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
