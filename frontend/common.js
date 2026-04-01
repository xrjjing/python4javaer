/**
 * 前端公共工具文件。
 *
 * 主要服务页面：
 * - admin.html：用户/角色/权限表格渲染、调试面板、Toast 提示
 * - log-detective.html：统一 API 请求日志输出
 *
 * 排查建议：
 * - 如果页面请求发出去了但你想看请求/响应日志，先看 logApiActivity()
 * - 如果表格不显示，先看 renderGenericTable()
 * - 如果后端返回异常但页面只提示 Error，先看 apiClient() 如何解析 response.json()
 */

// ============================================
// API 客户端（带脱敏日志）
// ============================================

/**
 * 脱敏处理：移除敏感字段。
 *
 * 这个函数不参与真实业务提交，只用于调试日志展示。
 * 目的是避免在 debug-panel 中直接打印密码、token 等敏感数据。
 *
 * @param {string|FormData} body - 请求体
 * @returns {string} 脱敏后的字符串
 */
function sanitizeBody(body) {
    if (!body) return '';

    // 如果是 FormData，转换为对象
    if (body instanceof FormData) {
        const obj = {};
        for (const [key, value] of body.entries()) {
            obj[key] = value;
        }
        body = obj;
    }

    // 如果是字符串，尝试解析为对象
    if (typeof body === 'string') {
        try {
            body = JSON.parse(body);
        } catch {
            return '[Raw String Body]';
        }
    }

    // 脱敏敏感字段
    const sensitiveFields = ['password', 'token', 'secret', 'api_key', 'access_token'];
    const sanitized = { ...body };

    sensitiveFields.forEach(field => {
        if (field in sanitized) {
            sanitized[field] = '***REDACTED***';
        }
    });

    return JSON.stringify(sanitized);
}

/**
 * 记录 API 活动到调试面板。
 *
 * 上游通常是 apiClient()，下游是 admin.html 底部的 debug-panel DOM。
 * 若当前页面没有 debug-panel / log-container，本函数会直接静默返回。
 *
 * @param {string} type - 日志类型 (REQUEST/RESPONSE/ERROR)
 * @param {string|number} method - HTTP 方法或状态码
 * @param {string} url - 请求 URL
 * @param {any} data - 数据内容
 * @param {number} duration - 请求耗时（毫秒）
 */
// 调试面板写入入口：admin.html 勾选“调试模式”后，页面请求日志最终都会通过这里落到 #log-container。
function logApiActivity(type, method, url, data, duration = 0) {
    const logContainer = document.getElementById('log-container');
    if (!logContainer) return; // 如果没有日志面板，跳过

    const timestamp = new Date().toLocaleTimeString('zh-CN', { hour12: false });
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';

    let emoji = '';
    let color = '';
    let message = '';

    switch (type) {
        case 'REQUEST':
            emoji = '🟢';
            color = '#10b981';
            message = `[${method}] ${url}`;
            if (data) message += ` | Body: ${data}`;
            break;
        case 'RESPONSE':
            emoji = '🔵';
            color = '#3b82f6';
            message = `[${method}] ${duration}ms | URL: ${url}`;
            break;
        case 'ERROR':
            emoji = '🔴';
            color = '#ef4444';
            message = `[ERROR] ${url} | ${data}`;
            break;
    }

    // FIX: Use DOM API instead of innerHTML to prevent XSS
    const iconSpan = document.createElement('span');
    iconSpan.style.color = color;
    iconSpan.textContent = emoji;

    const timeSpan = document.createElement('span');
    timeSpan.style.color = 'var(--text-muted)';
    timeSpan.style.marginRight = '8px';
    timeSpan.textContent = timestamp;

    const msgSpan = document.createElement('span');
    msgSpan.textContent = message;

    logEntry.appendChild(iconSpan);
    logEntry.appendChild(timeSpan);
    logEntry.appendChild(msgSpan);

    logContainer.appendChild(logEntry);
    logContainer.scrollTop = logContainer.scrollHeight; // 自动滚动到底部
}

/**
 * 统一的 API 客户端。
 *
 * 调用链：
 * 页面按钮/初始化逻辑 -> apiClient() -> fetch() -> logApiActivity()
 *
 * 说明：
 * - 本函数不替代页面自己的鉴权逻辑，只负责统一发请求和记录日志
 * - 默认假设返回体是 JSON；如果后端返回非 JSON，这里会抛错
 *
 * @param {string} url - 请求 URL
 * @param {object} options - fetch 选项
 * @returns {Promise<any>} 响应数据
 */
// 通用请求入口：保留原始 fetch 的调用方式，但额外补了请求/响应日志，适合需要排查链路的页面。
async function apiClient(url, options = {}) {
    const method = options.method || 'GET';
    const startTime = Date.now();

    // 脱敏处理：不记录完整敏感信息
    const safeBody = sanitizeBody(options.body);
    logApiActivity('REQUEST', method, url, safeBody);

    try {
        const response = await fetch(url, options);
        const data = await response.json();
        const duration = Date.now() - startTime;

        logApiActivity('RESPONSE', response.status, url, data, duration);

        if (!response.ok) {
            throw new Error(data.detail || data.message || `HTTP ${response.status}`);
        }

        return data;
    } catch (error) {
        logApiActivity('ERROR', '---', url, error.message);
        throw error;
    }
}

// ============================================
// 通用表格渲染器
// ============================================

/**
 * 安全的通用表格渲染器。
 *
 * 主要供 admin.html 使用，把“数组数据 + 列配置”渲染成 tbody。
 * 如果你发现表格标题有了但数据区为空，优先确认：
 * 1) elementId 对应的 tbody 是否存在
 * 2) data 是否真的是数组
 * 3) render 函数是否返回了 HTMLElement 或可转字符串的值
 *
 * @param {string} elementId - tbody 元素的 ID
 * @param {Array} data - 数据数组
 * @param {Array} columns - 列定义数组
 * @example
 * renderGenericTable('users-table', users, [
 *   { key: 'id' },
 *   { key: 'username' },
 *   { key: 'roles', render: (roles) => roles.map(r => r.name).join(', ') }
 * ]);
 */
// 通用表格渲染入口：admin.html 的 users / roles / permissions 三个表格都通过这里渲染 tbody。
function renderGenericTable(elementId, data, columns) {
    const tbody = document.getElementById(elementId);

    // 边界检查
    if (!tbody) {
        console.error(`Table element #${elementId} not found`);
        return;
    }

    // 安全清空表格
    tbody.replaceChildren();

    // 处理空数据
    if (!data || data.length === 0) {
        const tr = document.createElement('tr');
        const td = document.createElement('td');
        td.colSpan = columns.length;
        td.textContent = 'No data available';
        td.style.textAlign = 'center';
        td.style.color = 'var(--text-muted)';
        tr.appendChild(td);
        tbody.appendChild(tr);
        return;
    }

    // 渲染数据行
    data.forEach(item => {
        const tr = document.createElement('tr');

        columns.forEach(col => {
            const td = document.createElement('td');

            if (col.render) {
                // 使用自定义渲染函数
                const content = col.render(item[col.key], item);

                if (content instanceof HTMLElement) {
                    // 安全插入 DOM 节点
                    td.appendChild(content);
                } else if (content != null) {
                    // 安全设置文本（转换为字符串）
                    td.textContent = String(content);
                } else {
                    td.textContent = '-';
                }
            } else {
                // 默认文本渲染（使用 nullish 合并处理 0/false）
                const value = item[col.key];
                td.textContent = value ?? '-';
            }

            tr.appendChild(td);
        });

        tbody.appendChild(tr);
    });
}

// ============================================
// 调试面板管理
// ============================================

/**
 * 切换调试面板显示状态。
 *
 * admin.html 右上角“调试模式”复选框最终会走到这里。
 *
 * @param {boolean} show - 是否显示
 */
// 调试面板显隐：只改 UI 状态，不会影响业务请求是否发送。
function toggleDebugPanel(show) {
    const debugPanel = document.getElementById('debug-panel');
    if (debugPanel) {
        debugPanel.style.display = show ? 'block' : 'none';
    }
}

/**
 * 清空调试日志。
 *
 * 只清空前端面板中的 DOM，不影响任何真实请求或后端日志。
 */
function clearDebugLogs() {
    const logContainer = document.getElementById('log-container');
    if (logContainer) {
        logContainer.replaceChildren();
    }
}

// ============================================
// 工具函数
// ============================================

/**
 * 显示 Toast 提示。
 *
 * 这是一个非常轻量的提示实现，适合后台页的小反馈，不承担复杂状态管理。
 *
 * @param {string} message - 提示消息
 * @param {string} type - 类型 (success/error/info)
 */
// 轻量提示组件：当前主要在 admin.html 的错误/成功反馈里使用。
function showToast(message, type = 'info') {
    // 简单实现，可以后续增强为更美观的 Toast 组件
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        info: '#3b82f6'
    };

    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors[type] || colors.info};
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    toast.textContent = message;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ============================================
// 导出（如果使用模块化）
// ============================================

// 如果使用 ES6 模块，可以取消注释
// export { apiClient, renderGenericTable, toggleDebugPanel, clearDebugLogs, showToast };
