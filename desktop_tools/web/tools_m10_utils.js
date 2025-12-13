/* 工具箱（M10）JSON 格式化工具
 *
 * 设计目标：
 * - 纯算法、无 DOM 依赖
 * - JSON 格式化/压缩/校验
 */
(function (root, factory) {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        root.DogToolboxM10Utils = factory();
    }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    /**
     * 格式化 JSON
     * @param {string} text - JSON 字符串
     * @param {number|string} indent - 缩进（2/4/'\t'）
     * @returns {{result: string, error: string|null, line: number|null}}
     */
    function formatJson(text, indent) {
        const s = String(text ?? '').trim();
        if (!s) return { result: '', error: null, line: null };

        try {
            const obj = JSON.parse(s);
            const indentVal = indent === 'tab' ? '\t' : (parseInt(String(indent), 10) || 2);
            return { result: JSON.stringify(obj, null, indentVal), error: null, line: null };
        } catch (e) {
            const lineInfo = extractErrorLine(e.message, s);
            return { result: '', error: e.message, line: lineInfo };
        }
    }

    /**
     * 压缩 JSON（移除空白）
     * @param {string} text - JSON 字符串
     * @returns {{result: string, error: string|null, line: number|null}}
     */
    function minifyJson(text) {
        const s = String(text ?? '').trim();
        if (!s) return { result: '', error: null, line: null };

        try {
            const obj = JSON.parse(s);
            return { result: JSON.stringify(obj), error: null, line: null };
        } catch (e) {
            const lineInfo = extractErrorLine(e.message, s);
            return { result: '', error: e.message, line: lineInfo };
        }
    }

    /**
     * 校验 JSON
     * @param {string} text - JSON 字符串
     * @returns {{valid: boolean, error: string|null, line: number|null}}
     */
    function validateJson(text) {
        const s = String(text ?? '').trim();
        if (!s) return { valid: true, error: null, line: null };

        try {
            JSON.parse(s);
            return { valid: true, error: null, line: null };
        } catch (e) {
            const lineInfo = extractErrorLine(e.message, s);
            return { valid: false, error: e.message, line: lineInfo };
        }
    }

    /**
     * 从错误消息中提取行号
     */
    function extractErrorLine(message, text) {
        // 尝试从错误消息中提取位置信息
        // 格式如: "at position 123" 或 "at line 5 column 10"
        const posMatch = message.match(/position\s+(\d+)/i);
        if (posMatch) {
            const pos = parseInt(posMatch[1], 10);
            return positionToLine(text, pos);
        }

        const lineMatch = message.match(/line\s+(\d+)/i);
        if (lineMatch) {
            return parseInt(lineMatch[1], 10);
        }

        return null;
    }

    /**
     * 字符位置转行号
     */
    function positionToLine(text, pos) {
        if (!text || pos < 0) return 1;
        const before = text.substring(0, pos);
        return (before.match(/\n/g) || []).length + 1;
    }

    /**
     * 尝试修复常见 JSON 错误
     * @param {string} text - 可能格式不正确的 JSON
     * @returns {string} 尝试修复后的字符串
     */
    function tryFixJson(text) {
        let s = String(text ?? '').trim();
        if (!s) return s;

        // 移除尾部逗号
        s = s.replace(/,(\s*[}\]])/g, '$1');

        // 修复单引号为双引号
        // 简单处理：只处理属性名和字符串值的单引号
        // 注意：这是一个简化实现，复杂情况可能失败
        s = s.replace(/'([^'\\]*(\\.[^'\\]*)*)'/g, '"$1"');

        return s;
    }

    return {
        formatJson,
        minifyJson,
        validateJson,
        tryFixJson,
        extractErrorLine,
        positionToLine
    };
});
