// frontend/config.js
// 统一前端调用的后端服务地址配置。
//
// 主要被以下页面读取：
// - login.html：优先读取 authApiBaseUrl
// - admin.html：读取 authApiBaseUrl 和 logApiBaseUrl
// - log-detective.html：读取 gatewayApiBaseUrl
// - portal.html：只把当前地址展示出来，帮助联调确认
//
// 真实关系：
// - login.html / admin.html 主要直连 RBAC 服务
// - admin.html 额外读取审计日志服务
// - log-detective.html 只打网关，由网关再转发到日志分析服务
//
// 排查建议：
// - 登录报错先看 authApiBaseUrl
// - 日志侦探 502/连不上网关先看 gatewayApiBaseUrl
// - Admin 审计日志为空先看 logApiBaseUrl
window.AppConfig = {
    // RBAC 认证与权限服务
    authApiBaseUrl: 'http://127.0.0.1:8001',

    // API 网关服务（Integration Gateway）
    gatewayApiBaseUrl: 'http://127.0.0.1:8000',

    // 兼容旧代码用的基础地址（历史上部分页面直接使用 apiBaseUrl）
    // 新代码应优先使用 authApiBaseUrl / gatewayApiBaseUrl
    apiBaseUrl: 'http://127.0.0.1:8000',

    // 审计日志服务（可直接访问，或由网关转发）
    logApiBaseUrl: 'http://127.0.0.1:8002',

    // 特性开关：是否启用前端 Mock 模式
    enableMock: false
};
