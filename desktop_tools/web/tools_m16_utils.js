/* 工具箱（M16）JSON 树形视图工具
 *
 * 设计目标：
 * - 解析 JSON 为可交互的树结构
 * - 展开/折叠节点
 * - 面包屑导航
 */
(function (root, factory) {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        root.DogToolboxM16Utils = factory();
    }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    /**
     * 获取值的类型标签
     * @param {*} value - 任意值
     * @returns {string} 类型标签
     */
    function getValueType(value) {
        if (value === null) return 'null';
        if (value === undefined) return 'undefined';
        if (Array.isArray(value)) return 'array';
        return typeof value;
    }

    /**
     * 格式化显示值
     * @param {*} value - 值
     * @param {string} type - 类型
     * @returns {string} 格式化后的显示文本
     */
    function formatValue(value, type) {
        switch (type) {
            case 'string':
                // 截断过长字符串
                const str = String(value);
                if (str.length > 100) {
                    return `"${str.substring(0, 100)}..."`;
                }
                return `"${str}"`;
            case 'number':
            case 'boolean':
                return String(value);
            case 'null':
                return 'null';
            case 'undefined':
                return 'undefined';
            case 'array':
                return `Array(${value.length})`;
            case 'object':
                const keys = Object.keys(value);
                return `Object{${keys.length}}`;
            default:
                return String(value);
        }
    }

    /**
     * 转义 HTML 特殊字符
     */
    function escapeHtml(str) {
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    /**
     * 生成唯一路径 ID
     * 使用字符编码避免 ID 冲突（如 "a-b" 和 "a_b"）
     */
    function pathToId(path) {
        return 'jtree-' + path.map(p => String(p).split('').map(c => {
            if (/^[a-zA-Z0-9]$/.test(c)) return c;
            return '_' + c.charCodeAt(0).toString(16) + '_';
        }).join('')).join('-');
    }

    /**
     * 渲染 JSON 树形节点
     * @param {*} value - 当前值
     * @param {string} key - 当前键名
     * @param {Array} path - 路径数组
     * @param {number} depth - 当前深度
     * @param {boolean} isLast - 是否为最后一项
     * @returns {string} HTML 字符串
     */
    function renderNode(value, key, path, depth, isLast) {
        const type = getValueType(value);
        const displayValue = formatValue(value, type);
        const nodeId = pathToId(path);
        const isExpandable = type === 'object' || type === 'array';
        const indent = depth * 20;

        let html = '<div class="jtree-node" data-path="' + escapeHtml(path.join('.')) + '" data-depth="' + depth + '">';
        html += '<div class="jtree-row" style="padding-left:' + indent + 'px">';

        // 展开/折叠按钮
        if (isExpandable) {
            html += '<span class="jtree-toggle expanded" data-node-id="' + nodeId + '" onclick="toggleJsonTreeNode(this)">▼</span>';
        } else {
            html += '<span class="jtree-toggle-placeholder"></span>';
        }

        // 键名
        if (key !== null && key !== undefined) {
            html += '<span class="jtree-key">' + escapeHtml(key) + '</span>';
            html += '<span class="jtree-colon">:</span>';
        }

        // 值
        html += '<span class="jtree-value jtree-type-' + type + '">' + escapeHtml(displayValue) + '</span>';

        html += '</div>'; // .jtree-row

        // 子节点容器
        if (isExpandable) {
            html += '<div class="jtree-children" id="' + nodeId + '">';
            if (type === 'array') {
                value.forEach((item, index) => {
                    const childPath = path.concat(index);
                    html += renderNode(item, index, childPath, depth + 1, index === value.length - 1);
                });
            } else if (type === 'object') {
                const keys = Object.keys(value);
                keys.forEach((k, index) => {
                    const childPath = path.concat(k);
                    html += renderNode(value[k], k, childPath, depth + 1, index === keys.length - 1);
                });
            }
            html += '</div>'; // .jtree-children
        }

        html += '</div>'; // .jtree-node
        return html;
    }

    /**
     * 解析 JSON 并生成树形 HTML
     * @param {string} jsonText - JSON 字符串
     * @returns {{html: string, error: string|null, breadcrumb: Array}}
     */
    function parseAndRender(jsonText) {
        const s = String(jsonText ?? '').trim();
        if (!s) {
            return {
                html: '<div class="jtree-empty">输入 JSON 数据以查看树形结构</div>',
                error: null,
                breadcrumb: []
            };
        }

        try {
            const obj = JSON.parse(s);
            const type = getValueType(obj);

            let html = '<div class="jtree-root">';
            if (type === 'array') {
                obj.forEach((item, index) => {
                    html += renderNode(item, index, [index], 0, index === obj.length - 1);
                });
            } else if (type === 'object') {
                const keys = Object.keys(obj);
                keys.forEach((k, index) => {
                    html += renderNode(obj[k], k, [k], 0, index === keys.length - 1);
                });
            } else {
                // 基本类型
                html += renderNode(obj, null, [], 0, true);
            }
            html += '</div>';

            return { html, error: null, breadcrumb: ['root'] };
        } catch (e) {
            return {
                html: '<div class="jtree-error">JSON 解析错误: ' + escapeHtml(e.message) + '</div>',
                error: e.message,
                breadcrumb: []
            };
        }
    }

    /**
     * 展开所有节点
     * @param {HTMLElement} container - 树形容器
     */
    function expandAll(container) {
        if (!container) return;
        container.querySelectorAll('.jtree-toggle').forEach(toggle => {
            toggle.classList.add('expanded');
            toggle.textContent = '▼';
        });
        container.querySelectorAll('.jtree-children').forEach(children => {
            children.style.display = 'block';
        });
    }

    /**
     * 折叠所有节点
     * @param {HTMLElement} container - 树形容器
     */
    function collapseAll(container) {
        if (!container) return;
        container.querySelectorAll('.jtree-toggle').forEach(toggle => {
            toggle.classList.remove('expanded');
            toggle.textContent = '▶';
        });
        container.querySelectorAll('.jtree-children').forEach(children => {
            children.style.display = 'none';
        });
    }

    /**
     * 切换单个节点展开/折叠状态
     * @param {HTMLElement} toggle - 切换按钮元素
     */
    function toggleNode(toggle) {
        if (!toggle) return;
        const nodeId = toggle.getAttribute('data-node-id');
        const children = document.getElementById(nodeId);
        if (!children) return;

        const isExpanded = toggle.classList.contains('expanded');
        if (isExpanded) {
            toggle.classList.remove('expanded');
            toggle.textContent = '▶';
            children.style.display = 'none';
        } else {
            toggle.classList.add('expanded');
            toggle.textContent = '▼';
            children.style.display = 'block';
        }
    }

    /**
     * 获取节点的路径值
     * @param {string} jsonText - JSON 字符串
     * @param {string} pathStr - 点分隔的路径字符串
     * @returns {*} 路径对应的值
     */
    function getValueAtPath(jsonText, pathStr) {
        if (!jsonText || !pathStr) return undefined;
        try {
            const obj = JSON.parse(jsonText);
            const parts = pathStr.split('.');
            let current = obj;
            for (const part of parts) {
                if (current === null || current === undefined) return undefined;
                current = current[part];
            }
            return current;
        } catch (e) {
            return undefined;
        }
    }

    return {
        getValueType,
        formatValue,
        parseAndRender,
        expandAll,
        collapseAll,
        toggleNode,
        getValueAtPath,
        escapeHtml,
        pathToId
    };
});
