/* 工具箱（M11）文本去重/排序工具
 *
 * 设计目标：
 * - 纯算法、无 DOM 依赖
 * - 支持多种排序和去重方式
 */
(function (root, factory) {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        root.DogToolboxM11Utils = factory();
    }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    /**
     * 按行去重
     * @param {string} text - 输入文本
     * @param {boolean} caseSensitive - 是否区分大小写
     * @param {boolean} trimLines - 是否去除首尾空白
     * @returns {string}
     */
    function deduplicate(text, caseSensitive, trimLines) {
        const lines = String(text ?? '').split(/\r?\n/);
        const seen = new Set();
        const result = [];

        for (const line of lines) {
            let key = trimLines ? line.trim() : line;
            if (!caseSensitive) key = key.toLowerCase();

            if (!seen.has(key)) {
                seen.add(key);
                result.push(trimLines ? line.trim() : line);
            }
        }

        return result.join('\n');
    }

    /**
     * 排序
     * @param {string} text - 输入文本
     * @param {string} order - 'asc' | 'desc' | 'length-asc' | 'length-desc' | 'random'
     * @param {boolean} caseSensitive - 是否区分大小写
     * @returns {string}
     */
    function sortLines(text, order, caseSensitive) {
        const lines = String(text ?? '').split(/\r?\n/);

        let compareFn;
        switch (order) {
            case 'desc':
                compareFn = (a, b) => {
                    const aa = caseSensitive ? a : a.toLowerCase();
                    const bb = caseSensitive ? b : b.toLowerCase();
                    return bb.localeCompare(aa, 'zh-CN');
                };
                break;
            case 'length-asc':
                compareFn = (a, b) => a.length - b.length;
                break;
            case 'length-desc':
                compareFn = (a, b) => b.length - a.length;
                break;
            case 'random':
                return shuffleArray(lines).join('\n');
            case 'asc':
            default:
                compareFn = (a, b) => {
                    const aa = caseSensitive ? a : a.toLowerCase();
                    const bb = caseSensitive ? b : b.toLowerCase();
                    return aa.localeCompare(bb, 'zh-CN');
                };
                break;
        }

        return lines.sort(compareFn).join('\n');
    }

    /**
     * 反转行顺序
     */
    function reverseLines(text) {
        const lines = String(text ?? '').split(/\r?\n/);
        return lines.reverse().join('\n');
    }

    /**
     * 移除空行
     */
    function removeEmptyLines(text) {
        const lines = String(text ?? '').split(/\r?\n/);
        return lines.filter(line => line.trim() !== '').join('\n');
    }

    /**
     * 去除每行首尾空白
     */
    function trimAllLines(text) {
        const lines = String(text ?? '').split(/\r?\n/);
        return lines.map(line => line.trim()).join('\n');
    }

    /**
     * 添加行号
     */
    function addLineNumbers(text, startNum) {
        const lines = String(text ?? '').split(/\r?\n/);
        const start = parseInt(String(startNum), 10) || 1;
        const width = String(start + lines.length - 1).length;
        return lines.map((line, i) => {
            const num = String(start + i).padStart(width, ' ');
            return `${num}. ${line}`;
        }).join('\n');
    }

    /**
     * 移除行号
     */
    function removeLineNumbers(text) {
        const lines = String(text ?? '').split(/\r?\n/);
        return lines.map(line => {
            return line.replace(/^\s*\d+[.\s:)\]]+\s*/, '');
        }).join('\n');
    }

    /**
     * Fisher-Yates 洗牌
     */
    function shuffleArray(array) {
        const arr = array.slice();
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    /**
     * 统计行数
     */
    function countLines(text) {
        const s = String(text ?? '');
        if (!s) return 0;
        return s.split(/\r?\n/).length;
    }

    /**
     * 统计去重后行数
     */
    function countUniqueLines(text, caseSensitive) {
        const lines = String(text ?? '').split(/\r?\n/);
        const seen = new Set();
        for (const line of lines) {
            const key = caseSensitive ? line : line.toLowerCase();
            seen.add(key);
        }
        return seen.size;
    }

    return {
        deduplicate,
        sortLines,
        reverseLines,
        removeEmptyLines,
        trimAllLines,
        addLineNumbers,
        removeLineNumbers,
        countLines,
        countUniqueLines
    };
});
