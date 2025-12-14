/* 工具箱（M18）数据格式转换工具
 *
 * 设计目标：
 * - JSON ↔ YAML/XML 双向转换
 * - 依赖 CDN：js-yaml、fast-xml-parser
 */
(function (root, factory) {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        root.DogToolboxM18Utils = factory();
    }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    /**
     * JSON 转 YAML
     * @param {string} jsonText - JSON 字符串
     * @returns {{result: string, error: string|null}}
     */
    function jsonToYaml(jsonText) {
        const s = String(jsonText ?? '').trim();
        if (!s) return { result: '', error: null };

        try {
            const obj = JSON.parse(s);
            // 使用 js-yaml 库（需要 CDN 引入）
            if (typeof jsyaml === 'undefined') {
                return { result: '', error: 'js-yaml 库未加载' };
            }
            const yaml = jsyaml.dump(obj, {
                indent: 2,
                lineWidth: -1, // 不自动换行
                noRefs: true,
                sortKeys: false
            });
            return { result: yaml, error: null };
        } catch (e) {
            return { result: '', error: e.message };
        }
    }

    /**
     * YAML 转 JSON
     * @param {string} yamlText - YAML 字符串
     * @param {number} indent - JSON 缩进
     * @returns {{result: string, error: string|null}}
     */
    function yamlToJson(yamlText, indent) {
        const s = String(yamlText ?? '').trim();
        if (!s) return { result: '', error: null };

        try {
            if (typeof jsyaml === 'undefined') {
                return { result: '', error: 'js-yaml 库未加载' };
            }
            const obj = jsyaml.load(s);
            const indentVal = parseInt(String(indent), 10) || 2;
            return { result: JSON.stringify(obj, null, indentVal), error: null };
        } catch (e) {
            return { result: '', error: e.message };
        }
    }

    /**
     * JSON 转 XML
     * @param {string} jsonText - JSON 字符串
     * @param {string} rootName - 根元素名称
     * @returns {{result: string, error: string|null}}
     */
    function jsonToXml(jsonText, rootName) {
        const s = String(jsonText ?? '').trim();
        if (!s) return { result: '', error: null };

        try {
            const obj = JSON.parse(s);
            // 使用 fast-xml-parser（需要 CDN 引入）
            if (typeof fxparser === 'undefined' && typeof XMLBuilder === 'undefined') {
                // 使用简单实现作为降级方案
                // 如果是数组，需要包装在根元素中
                const root = rootName || 'root';
                if (Array.isArray(obj)) {
                    let xml = `<${root}>\n`;
                    for (const item of obj) {
                        xml += simpleJsonToXml(item, 'item', '  ');
                    }
                    xml += `</${root}>\n`;
                    return { result: xml, error: null };
                }
                return { result: simpleJsonToXml(obj, root), error: null };
            }

            const Builder = (typeof fxparser !== 'undefined' && fxparser.XMLBuilder) || (typeof XMLBuilder !== 'undefined' && XMLBuilder);
            const builder = new Builder({
                ignoreAttributes: false,
                format: true,
                indentBy: '  '
            });

            const wrapped = {};
            wrapped[rootName || 'root'] = obj;
            return { result: builder.build(wrapped), error: null };
        } catch (e) {
            return { result: '', error: e.message };
        }
    }

    /**
     * XML 转 JSON
     * @param {string} xmlText - XML 字符串
     * @param {number} indent - JSON 缩进
     * @returns {{result: string, error: string|null}}
     */
    function xmlToJson(xmlText, indent) {
        const s = String(xmlText ?? '').trim();
        if (!s) return { result: '', error: null };

        try {
            if (typeof fxparser === 'undefined' && typeof XMLParser === 'undefined') {
                return { result: '', error: 'fast-xml-parser 库未加载' };
            }

            const Parser = (typeof fxparser !== 'undefined' && fxparser.XMLParser) || (typeof XMLParser !== 'undefined' && XMLParser);
            const parser = new Parser({
                ignoreAttributes: false,
                attributeNamePrefix: '@_'
            });

            const obj = parser.parse(s);
            const indentVal = parseInt(String(indent), 10) || 2;
            return { result: JSON.stringify(obj, null, indentVal), error: null };
        } catch (e) {
            return { result: '', error: e.message };
        }
    }

    /**
     * 简单的 JSON 转 XML 实现（降级方案）
     */
    function simpleJsonToXml(obj, tagName, indent) {
        indent = indent || '';
        const nextIndent = indent + '  ';
        let xml = '';

        if (obj === null || obj === undefined) {
            return `${indent}<${tagName}/>\n`;
        }

        if (typeof obj !== 'object') {
            // 基本类型
            const escaped = String(obj)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;');
            return `${indent}<${tagName}>${escaped}</${tagName}>\n`;
        }

        if (Array.isArray(obj)) {
            // 数组：每个元素用 tagName 包装
            const itemTag = tagName || 'item';
            for (const item of obj) {
                xml += simpleJsonToXml(item, itemTag, indent);
            }
            return xml;
        }

        // 对象
        xml += `${indent}<${tagName}>\n`;
        for (const [key, value] of Object.entries(obj)) {
            // 处理特殊字符的键名
            const safeKey = key.replace(/[^a-zA-Z0-9_-]/g, '_');
            if (Array.isArray(value)) {
                for (const item of value) {
                    xml += simpleJsonToXml(item, safeKey, nextIndent);
                }
            } else {
                xml += simpleJsonToXml(value, safeKey, nextIndent);
            }
        }
        xml += `${indent}</${tagName}>\n`;
        return xml;
    }

    /**
     * 检测文本格式
     * @param {string} text - 输入文本
     * @returns {string} 'json' | 'yaml' | 'xml' | 'unknown'
     */
    function detectFormat(text) {
        const s = String(text ?? '').trim();
        if (!s) return 'unknown';

        // 检测 JSON
        if ((s.startsWith('{') && s.endsWith('}')) ||
            (s.startsWith('[') && s.endsWith(']'))) {
            try {
                JSON.parse(s);
                return 'json';
            } catch (e) {
                // 不是有效 JSON，继续检测
            }
        }

        // 检测 XML
        if (s.startsWith('<?xml') || (s.startsWith('<') && s.endsWith('>'))) {
            return 'xml';
        }

        // 默认假设为 YAML
        return 'yaml';
    }

    return {
        jsonToYaml,
        yamlToJson,
        jsonToXml,
        xmlToJson,
        detectFormat,
        simpleJsonToXml
    };
});
