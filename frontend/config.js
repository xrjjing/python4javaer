// frontend/config.js
// 统一前端调用的后端服务地址配置
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
