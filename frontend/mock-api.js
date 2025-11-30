/**
 * Mock API Interceptor
 *
 * 优雅的 fetch 拦截器，用于在开发环境下模拟后端 API 响应
 *
 * 特性：
 * - 非侵入式设计：不影响生产环境的真实 API 调用
 * - 灵活的开关机制：支持 URL 参数或 localStorage 控制
 * - 模拟网络延迟：更真实地模拟网络请求
 * - 完整的日志输出：方便调试和追踪
 *
 * 使用方法：
 * 1. URL 参数方式（临时）：http://localhost/page.html?mock=true
 * 2. localStorage 方式（持久）：localStorage.setItem('mockApi', 'true')
 *
 * 停用方法：
 * 1. 移除 URL 中的 ?mock=true
 * 2. localStorage.removeItem('mockApi')
 */

(function() {
  'use strict';

  // ==================== 配置区 ====================

  /**
   * 模拟网络延迟时间（毫秒）
   * 设置为 0 可以获得即时响应
   */
  const MOCK_API_DELAY = 300;

  /**
   * 是否在控制台显示详细日志
   */
  const ENABLE_VERBOSE_LOGGING = true;

  // ==================== 核心功能 ====================

  /**
   * 检查是否启用了模拟模式
   * @returns {boolean} 如果启用了模拟模式则返回 true
   */
  function isMockMode() {
    // 方式 1：URL 参数检查
    const urlParams = new URLSearchParams(window.location.search);
    const isUrlMock = urlParams.get('mock') === 'true';

    // 方式 2：localStorage 检查
    let isStorageMock = false;
    try {
      isStorageMock = localStorage.getItem('mockApi') === 'true';
    } catch (e) {
      // 处理 localStorage 不可用的情况（如隐私模式）
    }

    return isUrlMock || isStorageMock;
  }

  /**
   * 从 URL 中提取路径部分
   * @param {string} url - 完整的 URL 字符串
   * @returns {string} URL 的路径部分
   */
  function extractPathFromUrl(url) {
    try {
      const urlObj = new URL(url, window.location.origin);
      return urlObj.pathname;
    } catch (e) {
      // 如果 URL 解析失败，返回原始 URL
      return url;
    }
  }

  /**
   * 格式化日志输出
   * @param {string} type - 日志类型（info, success, warn, error）
   * @param {string} message - 日志消息
   * @param {*} data - 附加数据
   */
  function log(type, message, data) {
    if (!ENABLE_VERBOSE_LOGGING) return;

    const styles = {
      info: 'color: #2196F3; font-weight: bold;',
      success: 'color: #4CAF50; font-weight: bold;',
      warn: 'color: #FF9800; font-weight: bold;',
      error: 'color: #F44336; font-weight: bold;'
    };

    const prefix = '[Mock API]';
    console.log(`%c${prefix} ${message}`, styles[type] || styles.info);
    if (data !== undefined) {
      console.log(data);
    }
  }

  /**
   * 创建模拟的 Response 对象
   * @param {*} data - 响应数据
   * @param {number} status - HTTP 状态码
   * @returns {Response} 模拟的 Response 对象
   */
  function createMockResponse(data, status = 200) {
    return new Response(JSON.stringify(data), {
      status: status,
      statusText: status === 200 ? 'OK' : 'Error',
      headers: {
        'Content-Type': 'application/json',
        'X-Mock-API': 'true',
        'X-Mock-Timestamp': new Date().toISOString()
      }
    });
  }

  /**
   * 根据请求信息查找匹配的模拟数据
   * @param {string} method - HTTP 方法
   * @param {string} path - 请求路径
   * @returns {*} 模拟数据或 null
   */
  function findMockData(method, path) {
    if (!window.mockData) {
      log('warn', 'mockData 未定义，请确保已加载 mock-data.js');
      return null;
    }

    // 尝试直接匹配路径
    if (window.mockData[path]) {
      return window.mockData[path];
    }

    // 尝试匹配带方法的完整键（例如 "POST /auth/login"）
    const fullKey = `${method} ${path}`;
    if (window.mockData[fullKey]) {
      return window.mockData[fullKey];
    }

    return null;
  }

  // ==================== Fetch 拦截器 ====================

  // 保存原始的 fetch 函数
  const originalFetch = window.fetch;

  /**
   * 拦截后的 fetch 函数
   * 在模拟模式下返回模拟数据，否则调用真实 API
   */
  window.fetch = function(url, options = {}) {
    // 如果未启用模拟模式，直接调用原始 fetch
    if (!isMockMode()) {
      return originalFetch.apply(this, arguments);
    }

    const method = (options.method || 'GET').toUpperCase();
    const path = extractPathFromUrl(url);

    log('info', `拦截请求: ${method} ${path}`);

    // 查找匹配的模拟数据
    const mockResponseData = findMockData(method, path);

    if (mockResponseData) {
      log('success', `找到模拟数据: ${path}`, mockResponseData);

      // 返回一个 Promise，模拟异步网络请求
      return new Promise(resolve => {
        setTimeout(() => {
          const response = createMockResponse(mockResponseData);
          log('success', `返回模拟响应 (延迟 ${MOCK_API_DELAY}ms): ${path}`);
          resolve(response);
        }, MOCK_API_DELAY);
      });
    } else {
      log('warn', `未找到模拟数据: ${path}，回退到真实 API 调用`);
      // 如果没有找到模拟数据，回退到真实 fetch
      return originalFetch.apply(this, arguments);
    }
  };

  // ==================== 初始化 ====================

  if (isMockMode()) {
    log('success', '🎭 模拟 API 模式已激活', {
      '延迟时间': `${MOCK_API_DELAY}ms`,
      '详细日志': ENABLE_VERBOSE_LOGGING ? '已启用' : '已禁用',
      '停用方法': [
        '1. 移除 URL 中的 ?mock=true',
        '2. 执行 localStorage.removeItem("mockApi")'
      ]
    });

    // 在页面上显示一个提示标识
    const mockBadge = document.createElement('div');
    mockBadge.id = 'mock-api-badge';
    mockBadge.innerHTML = '🎭 Mock Mode';
    mockBadge.style.cssText = `
      position: fixed;
      bottom: 20px;
      left: 20px;
      background: #4CAF50;
      color: white;
      padding: 8px 16px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: bold;
      box-shadow: 0 2px 8px rgba(0,0,0,0.2);
      z-index: 9999;
      cursor: pointer;
      transition: all 0.3s ease;
    `;
    mockBadge.title = '点击查看模拟模式信息';

    mockBadge.addEventListener('click', () => {
      alert(
        '🎭 模拟 API 模式已激活\n\n' +
        '当前所有 API 请求都会返回模拟数据\n\n' +
        '停用方法：\n' +
        '1. 移除 URL 中的 ?mock=true\n' +
        '2. 在控制台执行：localStorage.removeItem("mockApi")'
      );
    });

    // 等待 DOM 加载完成后添加标识
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        document.body.appendChild(mockBadge);
      });
    } else {
      document.body.appendChild(mockBadge);
    }
  }

  // 暴露工具函数到全局作用域，方便调试
  window.mockApiUtils = {
    isMockMode,
    enableMock: () => {
      localStorage.setItem('mockApi', 'true');
      log('success', '模拟模式已启用，请刷新页面');
    },
    disableMock: () => {
      localStorage.removeItem('mockApi');
      log('info', '模拟模式已禁用，请刷新页面');
    }
  };

})();