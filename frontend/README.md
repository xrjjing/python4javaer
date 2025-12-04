# Frontend 前端页面

本目录包含 Python 学习项目的静态前端页面，配合 `rbac_auth_service` 后端服务使用。

## 页面说明

| 文件 | 用途 |
|------|------|
| `portal.html` | 汇总入口，一站式链接全部前端页面与课程导航 |
| `index.html` | 学习导航主页，包含章节导航和在线 Python 执行器 |
| `login.html` | RBAC 登录页面 |
| `admin.html` | RBAC 管理后台（用户/角色/权限管理） |
| `log-detective.html` | 日志侦探工具（日志分析与安全检测） |
| `mock-data.js` | 模拟数据文件，用于前端独立开发 |
| `mock-api.js` | Fetch 拦截器，实现模拟 API 响应 |

> 旧版控制台 `rbac_admin.html` 位于 `rbac_auth_service/app/static/` 目录

## 快速启动

### 方式一：配合后端服务（推荐）

```bash
# 1. 启动 RBAC 后端服务
cd ../rbac_auth_service
python init_rbac_data.py  # 初始化数据（首次运行）
uvicorn app.main:app --reload --port 8000

# 2. 在另一个终端启动前端静态服务
cd ../frontend
python -m http.server 5500

# 3. 访问前端页面
# http://127.0.0.1:5500/portal.html   # 汇总入口（推荐）
# http://127.0.0.1:5500/login.html
# http://127.0.0.1:5500/admin.html

# 注意：旧版控制台已挂载到后端，访问：
# http://127.0.0.1:8000/rbac-admin/rbac_admin.html
```

### 方式二：独立运行

```bash
# 使用 Python 内置 HTTP 服务器
cd frontend
python -m http.server 5500

# 访问 http://127.0.0.1:5500/index.html
```

> 独立运行时需配置 API 地址，见下方「API 配置」。

### 方式三：模拟数据模式（无需后端）

前端页面支持模拟数据模式，可在不启动后端服务的情况下预览完整的页面交互效果。

**启用方式：**

```bash
# 1. 启动静态服务器
cd frontend
python -m http.server 5500

# 2. 使用 URL 参数访问（临时启用）
# http://127.0.0.1:5500/login.html?mock=true
# http://127.0.0.1:5500/admin.html?mock=true

# 或者在浏览器控制台执行（持久启用）
localStorage.setItem('mockApi', 'true')
# 然后刷新页面
```

**停用模拟模式：**

```javascript
// 方式 1：移除 URL 中的 ?mock=true

// 方式 2：在控制台执行
localStorage.removeItem('mockApi')

// 方式 3：使用工具函数
window.mockApiUtils.disableMock()
```

**模拟数据说明：**

模拟数据包含以下内容，能完整展示所有页面功能：
- **4 个用户**：admin（超级管理员）、developer、viewer（已禁用）、tester
- **4 个角色**：Administrator、Developer、Viewer、Tester
- **7 个权限**：read、write、delete、manage_users、manage_roles、view_logs、export_data
- **6 条审计日志**：包含不同级别（INFO、WARN、ERROR）和不同服务的日志记录

**特性：**
- ✅ 非侵入式设计：不影响真实 API 调用
- ✅ 网络延迟模拟：300ms 延迟，更真实
- ✅ 完整日志输出：方便调试和追踪
- ✅ 可视化标识：页面左下角显示 "🎭 Mock Mode" 徽章

> 注意：模拟模式仅用于前端开发预览，不替代真实的后端联调测试。

## API 配置

前端页面默认请求同源 API。独立运行时需指定后端地址：

### 推荐方式：使用 config.js（统一配置）

编辑 `frontend/config.js` 文件：

```javascript
window.AppConfig = {
    apiBaseUrl: 'http://127.0.0.1:8000',      // 网关服务
    logApiBaseUrl: 'http://127.0.0.1:8002',   // 审计日志服务
    enableMock: false
};
```

### 兼容方式：使用全局变量（向后兼容）

```javascript
// 在页面加载前设置（可在 <head> 中添加）
window.API_BASE_URL = 'http://127.0.0.1:8000';
window.LOG_API_BASE_URL = 'http://127.0.0.1:8002';
```

**注意**：推荐使用 `config.js` 方式，全局变量方式仅为向后兼容保留。

## 默认账号

初始化数据后可用以下账号登录：

| 用户名 | 密码 | 角色 |
|--------|------|------|
| `admin` | `admin123` | 超级管理员 |
| `zhangsan` | `123456` | 普通用户 |
| `lisi` | `123456` | 审计员 |

## 技术说明

- 纯静态 HTML/CSS/JavaScript，无需构建工具
- 使用 CSS 变量实现亮/暗主题切换
- 使用 Pyodide 在浏览器中运行 Python 代码
- 使用 Prism.js + CodeJar 实现代码高亮和编辑
- 使用 OAuth2 密码模式进行身份认证
- Token 存储于 `localStorage`

## 安全注意事项

1. **生产环境**：必须使用 HTTPS
2. **Token 存储**：当前使用 localStorage，生产环境建议改用 httpOnly cookie
3. **CORS**：后端已配置允许跨域，生产环境需限制 `allow_origins`
4. **密码传输**：当前明文传输，生产环境必须使用 HTTPS

## 目录结构

```
frontend/
├── portal.html         # 前端入口汇总页
├── index.html          # 学习导航主页
├── login.html          # 登录页面
├── admin.html          # 管理后台
├── mock-data.js        # 模拟数据（用于前端独立开发）
├── mock-api.js         # Fetch 拦截器（实现模拟 API）
└── README.md           # 本文件

# 旧版控制台位于后端静态目录：
rbac_auth_service/app/static/
└── rbac_admin.html     # 旧版 RBAC 控制台
```

## 与后端服务的对应关系

```
前端页面                    后端服务                                API 路径
──────────────────────────────────────────────────────────────────────────
login.html            →    rbac_auth_service (8001)         →    POST /auth/login
admin.html            →    rbac_auth_service (8001)         →    GET /auth/me
                           log_audit_service (8002)         →    GET/POST/PATCH /users
                                                                  GET/POST/PATCH /rbac/roles
                                                                  GET/POST /rbac/permissions
                                                                  GET /audit-logs
log-detective.html    →    integration_gateway_service (8000) →  POST /gateway/log-detective/analyze
                           ↓
                           log_detective_service (9003)      →    POST /internal/log-detective/analyze
```

**说明**：
- `login.html` 和 `admin.html` 直接调用 RBAC 和审计日志服务
- `log-detective.html` 通过网关调用日志侦探服务（演示网关转发模式）
- 详细的服务说明见各服务目录下的 `09_项目说明.md`

## 常见问题

### Q: 登录后跳转失败？

检查后端服务是否正常运行，以及 API 地址配置是否正确。

### Q: 浏览器控制台报 CORS 错误？

确保后端 `allow_origins` 包含前端地址，或使用后端静态文件挂载方式访问。

### Q: Python 代码无法运行？

Pyodide 首次加载需要下载约 10MB 的 Python 运行时，请等待加载完成。

### Q: 如何判断是否在使用模拟数据？

启用模拟模式后，页面会有以下标识：
1. 左下角显示绿色的 "🎭 Mock Mode" 徽章
2. 浏览器控制台会输出 `[Mock API]` 相关日志
3. 网络请求的响应头包含 `X-Mock-API: true`

### Q: 模拟模式会影响真实 API 调用吗？

不会。只有在明确启用模拟模式（URL 参数或 localStorage）时才会拦截请求。未启用时，所有请求都会正常发送到真实后端。

### Q: 模拟数据可以自定义吗？

可以。直接编辑 `mock-data.js` 文件，添加或修改模拟响应数据。修改后刷新页面即可生效。
