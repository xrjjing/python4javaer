/* 工具箱（M12）正则表达式测试工具
 *
 * 设计目标：
 * - 纯算法、无 DOM 依赖
 * - 支持正则匹配、替换、提取
 * - 支持多种常用正则预设
 */
(function (root, factory) {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        root.DogToolboxM12Utils = factory();
    }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    /**
     * 解析正则表达式字符串
     * @param {string} pattern - 正则模式
     * @param {string} flags - 标志（g, i, m, s, u）
     * @returns {{regex: RegExp|null, error: string|null}}
     */
    function parseRegex(pattern, flags) {
        if (!pattern) {
            return { regex: null, error: null };
        }
        try {
            const regex = new RegExp(pattern, flags || '');
            return { regex, error: null };
        } catch (e) {
            return { regex: null, error: e.message };
        }
    }

    /**
     * 测试正则匹配
     * @param {string} text - 测试文本
     * @param {string} pattern - 正则模式
     * @param {string} flags - 标志
     * @returns {{matches: Array, error: string|null}}
     */
    function testMatch(text, pattern, flags) {
        const { regex, error } = parseRegex(pattern, flags);
        if (error) {
            return { matches: [], error };
        }
        if (!regex) {
            return { matches: [], error: null };
        }

        const matches = [];
        const hasGlobal = flags.includes('g');

        if (hasGlobal) {
            let match;
            while ((match = regex.exec(text)) !== null) {
                matches.push({
                    index: match.index,
                    match: match[0],
                    groups: match.slice(1),
                    namedGroups: match.groups || {}
                });
                if (match[0].length === 0) {
                    regex.lastIndex++;
                }
            }
        } else {
            const match = regex.exec(text);
            if (match) {
                matches.push({
                    index: match.index,
                    match: match[0],
                    groups: match.slice(1),
                    namedGroups: match.groups || {}
                });
            }
        }

        return { matches, error: null };
    }

    /**
     * 正则替换
     * @param {string} text - 原文本
     * @param {string} pattern - 正则模式
     * @param {string} replacement - 替换文本
     * @param {string} flags - 标志
     * @returns {{result: string, count: number, error: string|null}}
     */
    function replaceAll(text, pattern, replacement, flags) {
        const { regex, error } = parseRegex(pattern, flags);
        if (error) {
            return { result: text, count: 0, error };
        }
        if (!regex) {
            return { result: text, count: 0, error: null };
        }

        let count = 0;
        const result = text.replace(regex, (...args) => {
            count++;
            return replacement.replace(/\$(\d+|&|`|')/g, (m, ref) => {
                if (ref === '&') return args[0];
                if (ref === '`') return text.slice(0, args[args.length - 2]);
                if (ref === "'") return text.slice(args[args.length - 2] + args[0].length);
                const idx = parseInt(ref, 10);
                return args[idx] ?? m;
            });
        });

        return { result, count, error: null };
    }

    /**
     * 提取所有匹配
     * @param {string} text - 原文本
     * @param {string} pattern - 正则模式
     * @param {string} flags - 标志
     * @param {number} groupIndex - 要提取的分组索引（0 = 完整匹配）
     * @returns {{extracted: string[], error: string|null}}
     */
    function extractAll(text, pattern, flags, groupIndex) {
        const globalFlags = flags.includes('g') ? flags : flags + 'g';
        const { regex, error } = parseRegex(pattern, globalFlags);
        if (error) {
            return { extracted: [], error };
        }
        if (!regex) {
            return { extracted: [], error: null };
        }

        const extracted = [];
        let match;
        const idx = groupIndex || 0;

        while ((match = regex.exec(text)) !== null) {
            const value = idx === 0 ? match[0] : (match[idx] ?? '');
            extracted.push(value);
            if (match[0].length === 0) {
                regex.lastIndex++;
            }
        }

        return { extracted, error: null };
    }

    /**
     * 常用正则预设
     */
    const PRESETS = {
        email: {
            pattern: '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}',
            name: '邮箱',
            description: '匹配电子邮箱地址'
        },
        phone_cn: {
            pattern: '1[3-9]\\d{9}',
            name: '手机号（中国）',
            description: '匹配中国大陆手机号'
        },
        url: {
            pattern: 'https?://[^\\s<>"{}|\\\\^`\\[\\]]+',
            name: 'URL',
            description: '匹配 HTTP/HTTPS 链接'
        },
        ipv4: {
            pattern: '(?:(?:25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d\\d?)',
            name: 'IPv4',
            description: '匹配 IPv4 地址'
        },
        date_iso: {
            pattern: '\\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\\d|3[01])',
            name: '日期（ISO）',
            description: '匹配 YYYY-MM-DD 格式日期'
        },
        time_24h: {
            pattern: '(?:[01]\\d|2[0-3]):[0-5]\\d(?::[0-5]\\d)?',
            name: '时间（24h）',
            description: '匹配 HH:mm 或 HH:mm:ss 格式'
        },
        chinese: {
            pattern: '[\\u4e00-\\u9fa5]+',
            name: '中文字符',
            description: '匹配连续的中文字符'
        },
        number: {
            pattern: '-?\\d+(?:\\.\\d+)?',
            name: '数字',
            description: '匹配整数或小数'
        },
        hex_color: {
            pattern: '#(?:[0-9a-fA-F]{3}){1,2}\\b',
            name: '十六进制颜色',
            description: '匹配 #RGB 或 #RRGGBB'
        },
        uuid: {
            pattern: '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}',
            name: 'UUID',
            description: '匹配 UUID v4 格式'
        }
    };

    /**
     * 获取预设列表
     */
    function getPresets() {
        return Object.entries(PRESETS).map(([key, value]) => ({
            key,
            ...value
        }));
    }

    /**
     * 获取预设
     */
    function getPreset(key) {
        return PRESETS[key] || null;
    }

    /**
     * 转义正则特殊字符
     */
    function escapeRegex(str) {
        return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    return {
        parseRegex,
        testMatch,
        replaceAll,
        extractAll,
        getPresets,
        getPreset,
        escapeRegex
    };
});
