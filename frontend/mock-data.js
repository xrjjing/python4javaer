/**
 * Mock Data for Frontend Development
 *
 * 用于前端开发的模拟数据，可以在不启动后端服务的情况下预览页面交互
 *
 * 使用方式：
 * 1. URL 参数：访问页面时添加 ?mock=true
 * 2. localStorage：在控制台执行 localStorage.setItem('mockApi', 'true')
 */

const mockData = {
  // POST /auth/login - 登录接口
  '/auth/login': {
    code: 'OK',
    message: '登录成功',
    data: {
      access_token: 'mock-jwt-token-eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9',
      token_type: 'bearer',
      expires_in: 3600
    }
  },

  // GET /auth/me - 获取当前用户信息
  '/auth/me': {
    code: 'OK',
    message: '获取成功',
    data: {
      id: 1,
      username: 'admin',
      is_active: true,
      is_superuser: true,
      roles: [
        { id: 1, name: '系统管理员', description: '拥有所有权限的超级管理员' }
      ],
      permissions: ['read', 'write', 'delete', 'manage_users', 'manage_roles'],
      created_at: '2025-11-01T10:00:00Z',
      updated_at: '2025-11-30T15:30:00Z'
    }
  },

  // GET /users/ - 获取用户列表
  '/users/': {
    code: 'OK',
    message: '查询成功',
    data: [
      {
        id: 1,
        username: 'admin',
        is_active: true,
        is_superuser: true,
        roles: [
          { id: 1, name: '系统管理员', description: '拥有所有权限' }
        ],
        created_at: '2025-11-01T10:00:00Z'
      },
      {
        id: 2,
        username: '张三',
        is_active: true,
        is_superuser: false,
        roles: [
          { id: 2, name: '开发人员', description: '负责系统开发' }
        ],
        created_at: '2025-11-15T14:20:00Z'
      },
      {
        id: 3,
        username: '李四',
        is_active: false,
        is_superuser: false,
        roles: [
          { id: 3, name: '访客', description: '只读访问权限' }
        ],
        created_at: '2025-11-20T09:30:00Z'
      },
      {
        id: 4,
        username: '王五',
        is_active: true,
        is_superuser: false,
        roles: [
          { id: 4, name: '测试人员', description: '负责功能测试' }
        ],
        created_at: '2025-11-25T16:45:00Z'
      }
    ]
  },

  // GET /rbac/roles - 获取角色列表
  '/rbac/roles': {
    code: 'OK',
    message: '查询成功',
    data: [
      {
        id: 1,
        name: '系统管理员',
        description: '拥有所有权限的超级管理员',
        permissions: [
          { id: 1, code: 'read', description: '读取权限' },
          { id: 2, code: 'write', description: '写入权限' },
          { id: 3, code: 'delete', description: '删除权限' },
          { id: 4, code: 'manage_users', description: '用户管理' },
          { id: 5, code: 'manage_roles', description: '角色管理' }
        ]
      },
      {
        id: 2,
        name: '开发人员',
        description: '负责系统开发，可以读写数据',
        permissions: [
          { id: 1, code: 'read', description: '读取权限' },
          { id: 2, code: 'write', description: '写入权限' }
        ]
      },
      {
        id: 3,
        name: '访客',
        description: '只读用户，仅能查看数据',
        permissions: [
          { id: 1, code: 'read', description: '读取权限' }
        ]
      },
      {
        id: 4,
        name: '测试人员',
        description: '负责功能测试，可以读写测试数据',
        permissions: [
          { id: 1, code: 'read', description: '读取权限' },
          { id: 2, code: 'write', description: '写入权限' }
        ]
      }
    ]
  },

  // GET /rbac/permissions - 获取权限列表
  '/rbac/permissions': {
    code: 'OK',
    message: '查询成功',
    data: [
      { id: 1, code: 'read', description: '读取权限 - 允许查看数据' },
      { id: 2, code: 'write', description: '写入权限 - 允许创建和修改数据' },
      { id: 3, code: 'delete', description: '删除权限 - 允许删除数据' },
      { id: 4, code: 'manage_users', description: '用户管理 - 允许管理用户账号' },
      { id: 5, code: 'manage_roles', description: '角色管理 - 允许管理角色和权限' },
      { id: 6, code: 'view_logs', description: '日志查看 - 允许查看审计日志' },
      { id: 7, code: 'export_data', description: '数据导出 - 允许导出数据' }
    ]
  },

  // GET /logs - 获取审计日志
  '/logs': {
    code: 'OK',
    message: 'Success',
    data: [
      {
        id: 'log-001',
        level: 'INFO',
        service: 'rbac_auth_service',
        operation: 'user.login',
        user: 'admin',
        message: '用户登录成功',
        timestamp: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
        details: { ip: '192.168.1.100', user_agent: 'Mozilla/5.0' }
      },
      {
        id: 'log-002',
        level: 'WARN',
        service: 'rbac_auth_service',
        operation: 'user.login.failed',
        user: 'unknown',
        message: '登录失败：用户名或密码错误',
        timestamp: new Date(Date.now() - 10 * 60 * 1000).toISOString(),
        details: { ip: '192.168.1.101', attempt_count: 3 }
      },
      {
        id: 'log-003',
        level: 'INFO',
        service: 'rbac_auth_service',
        operation: 'user.create',
        user: 'admin',
        message: '创建新用户：developer',
        timestamp: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
        details: { new_user_id: 2 }
      },
      {
        id: 'log-004',
        level: 'ERROR',
        service: 'integration_gateway_service',
        operation: 'api.call.failed',
        user: 'developer',
        message: 'API调用失败：连接超时',
        timestamp: new Date(Date.now() - 60 * 60 * 1000).toISOString(),
        details: { endpoint: '/external/api/v1/data', error: 'Connection timeout' }
      },
      {
        id: 'log-005',
        level: 'INFO',
        service: 'rbac_auth_service',
        operation: 'role.assign',
        user: 'admin',
        message: '为用户 developer 分配角色 Developer',
        timestamp: new Date(Date.now() - 90 * 60 * 1000).toISOString(),
        details: { user_id: 2, role_id: 2 }
      },
      {
        id: 'log-006',
        level: 'INFO',
        service: 'log_audit_service',
        operation: 'logs.query',
        user: 'admin',
        message: '查询审计日志',
        timestamp: new Date(Date.now() - 2 * 60 * 1000).toISOString(),
        details: { filter: 'last_24h', count: 150 }
      }
    ]
  }
};

// 暴露给全局作用域，供 mock-api.js 使用
window.mockData = mockData;

// 如果是在模块环境中（例如 Node.js），也支持导出
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
  module.exports = mockData;
}