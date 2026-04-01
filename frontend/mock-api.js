/**
 * Mock API 拦截器。
 *
 * 主要服务页面：
 * - login.html
 * - admin.html
 *
 * 工作方式：
 * - 在 mock 模式开启时，接管 window.fetch
 * - 先把 URL 解析成 path
 * - 再到 window.mockData 中找匹配数据
 * - 找到就返回模拟 Response，找不到就回退真实 fetch
 *
 * 适合排查：
 * - 页面到底有没有真正走到 fetch
 * - 当前请求 path 为什么没有命中 mock 数据
 * - mock 模式是否已经启用
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
   * 检查是否启用了模拟模式。
   *
   * 这是整个拦截器是否生效的总开关。
   *
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
   * 从 URL 中提取路径部分。
   *
   * 之所以只取 path，是因为 mockData 的 key 主要按 `/auth/login` 这类路径组织。
   *
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
   * 根据请求信息查找匹配的模拟数据。
   *
   * 查找顺序：
   * 1. 先按 path 直接匹配
   * 2. 再按 `METHOD + path` 精确匹配
   *
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
   * 拦截后的 fetch 函数。
   *
   * 这是真正的入口点。页面代码仍然正常调用 fetch，
   * 只是这里决定“返回 mock”还是“放行真实请求”。
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
  // 这一段不是给业务页面主动调用的，而是在脚本加载时自动执行：
  // - 如果 mock 已开启，就插入左下角可见徽标
  // - 并把启停工具挂到 window.mockApiUtils，方便开发联调时手工开关

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

  // 暴露工具函数到全局作用域，方便在浏览器控制台快速启停 mock 模式。
  // login.html / admin.html 本身不会主动调用这些函数，主要给手工排障和联调使用。
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
