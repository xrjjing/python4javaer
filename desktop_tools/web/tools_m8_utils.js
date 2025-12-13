/* 工具箱（M8）通用算法工具：URL 编解码 / 进制转换 / 字符统计
 *
 * 设计目标：
 * - 纯算法、无 DOM 依赖，便于在浏览器与 Node 环境复用与单元测试
 * - 输入输出统一按 UTF-8 处理
 */
(function (root, factory) {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        root.DogToolboxM8Utils = factory();
    }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    // ==================== URL 编解码 ====================

    function urlEncode(text) {
        return encodeURIComponent(String(text ?? ''));
    }

    function urlDecode(text) {
        const s = String(text ?? '');
        try {
            return decodeURIComponent(s);
        } catch (e) {
            throw new Error('非法 URL 编码：' + (e.message || String(e)));
        }
    }

    function urlEncodeBatch(text) {
        const lines = String(text ?? '').split(/\r?\n/);
        return lines.map(line => line === '' ? '' : urlEncode(line)).join('\n');
    }

    function urlDecodeBatch(text) {
        const lines = String(text ?? '').split(/\r?\n/);
        const results = [];
        const errors = [];
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            if (line === '') {
                results.push('');
                continue;
            }
            try {
                results.push(urlDecode(line));
            } catch (e) {
                errors.push(`第 ${i + 1} 行：${e.message || String(e)}`);
                results.push(line);
            }
        }
        return { result: results.join('\n'), errors };
    }

    // ==================== 进制转换 ====================

    function detectRadix(text) {
        const s = String(text ?? '').trim().toLowerCase();
        if (!s) return null;
        if (/^0x[0-9a-f]+$/i.test(s)) return { radix: 16, value: s.slice(2) };
        if (/^0o[0-7]+$/i.test(s)) return { radix: 8, value: s.slice(2) };
        if (/^0b[01]+$/i.test(s)) return { radix: 2, value: s.slice(2) };
        if (/^[0-9]+$/.test(s)) return { radix: 10, value: s };
        if (/^[0-9a-f]+$/i.test(s) && /[a-f]/i.test(s)) return { radix: 16, value: s };
        return null;
    }

    function parseNumber(text, radix) {
        const s = String(text ?? '').trim();
        if (!s) return null;

        let actualRadix = radix;
        let valueStr = s;

        if (!actualRadix || actualRadix === 'auto') {
            const detected = detectRadix(s);
            if (!detected) throw new Error('无法识别输入格式');
            actualRadix = detected.radix;
            valueStr = detected.value;
        } else {
            actualRadix = parseInt(String(radix), 10);
            if (![2, 8, 10, 16].includes(actualRadix)) {
                throw new Error('仅支持 2/8/10/16 进制');
            }
            // 去除前缀
            const lower = s.toLowerCase();
            if (actualRadix === 16 && lower.startsWith('0x')) valueStr = s.slice(2);
            else if (actualRadix === 8 && lower.startsWith('0o')) valueStr = s.slice(2);
            else if (actualRadix === 2 && lower.startsWith('0b')) valueStr = s.slice(2);
        }

        // 校验字符
        const charSets = {
            2: /^[01]+$/,
            8: /^[0-7]+$/,
            10: /^[0-9]+$/,
            16: /^[0-9a-fA-F]+$/
        };
        if (!charSets[actualRadix].test(valueStr)) {
            throw new Error(`输入包含非法字符（${actualRadix} 进制）`);
        }

        try {
            return { value: BigInt('0x0' + (actualRadix === 16 ? valueStr : '0')) || BigInt(parseInt(valueStr, actualRadix).toString()), radix: actualRadix };
        } catch (e) {
            // 使用 BigInt 解析
        }

        // BigInt 解析
        if (actualRadix === 10) {
            return { value: BigInt(valueStr), radix: actualRadix };
        }
        if (actualRadix === 16) {
            return { value: BigInt('0x' + valueStr), radix: actualRadix };
        }
        if (actualRadix === 8) {
            return { value: BigInt('0o' + valueStr), radix: actualRadix };
        }
        if (actualRadix === 2) {
            return { value: BigInt('0b' + valueStr), radix: actualRadix };
        }

        throw new Error('进制转换失败');
    }

    function bigIntToRadix(value, radix) {
        const r = parseInt(String(radix), 10);
        if (![2, 8, 10, 16].includes(r)) {
            throw new Error('仅支持 2/8/10/16 进制输出');
        }
        const v = BigInt(value);
        if (v < 0n) {
            // 负数处理：显示负号
            return '-' + (-v).toString(r);
        }
        return v.toString(r);
    }

    function convertRadix(text, fromRadix, toRadix) {
        const parsed = parseNumber(text, fromRadix);
        if (!parsed) throw new Error('输入为空或无法解析');
        return bigIntToRadix(parsed.value, toRadix);
    }

    function convertToAllRadix(text, fromRadix) {
        const parsed = parseNumber(text, fromRadix);
        if (!parsed) {
            return { bin: '', oct: '', dec: '', hex: '', detectedRadix: null };
        }
        return {
            bin: bigIntToRadix(parsed.value, 2),
            oct: bigIntToRadix(parsed.value, 8),
            dec: bigIntToRadix(parsed.value, 10),
            hex: bigIntToRadix(parsed.value, 16).toUpperCase(),
            detectedRadix: parsed.radix
        };
    }

    // ==================== 字符统计 ====================

    function utf8ByteLength(text) {
        const s = String(text ?? '');
        if (typeof TextEncoder !== 'undefined') {
            return new TextEncoder().encode(s).length;
        }
        // 兜底计算
        let len = 0;
        for (let i = 0; i < s.length; i++) {
            const code = s.charCodeAt(i);
            if (code <= 0x7f) len += 1;
            else if (code <= 0x7ff) len += 2;
            else if (code >= 0xd800 && code <= 0xdbff) {
                // 代理对，占 4 字节
                len += 4;
                i++; // 跳过低代理
            } else len += 3;
        }
        return len;
    }

    function countChineseChars(text) {
        const s = String(text ?? '');
        // 匹配中文字符（CJK 统一汉字）
        const matches = s.match(/[\u4e00-\u9fff\u3400-\u4dbf\u{20000}-\u{2a6df}\u{2a700}-\u{2b73f}\u{2b740}-\u{2b81f}\u{2b820}-\u{2ceaf}]/gu);
        return matches ? matches.length : 0;
    }

    function countEnglishWords(text) {
        const s = String(text ?? '');
        // 匹配英文单词（连续字母）
        const matches = s.match(/[a-zA-Z]+/g);
        return matches ? matches.length : 0;
    }

    function countLines(text) {
        const s = String(text ?? '');
        if (!s) return 0;
        return s.split(/\r?\n/).length;
    }

    function charStats(text) {
        const s = String(text ?? '');
        const chars = Array.from(s);
        const charsNoSpace = chars.filter(c => !/\s/.test(c));

        return {
            charCount: chars.length,
            charCountNoSpace: charsNoSpace.length,
            byteCount: utf8ByteLength(s),
            lineCount: countLines(s),
            chineseCount: countChineseChars(s),
            englishWordCount: countEnglishWords(s)
        };
    }

    return {
        // URL 编解码
        urlEncode,
        urlDecode,
        urlEncodeBatch,
        urlDecodeBatch,
        // 进制转换
        detectRadix,
        parseNumber,
        convertRadix,
        convertToAllRadix,
        // 字符统计
        charStats,
        utf8ByteLength,
        countChineseChars,
        countEnglishWords,
        countLines
    };
});
